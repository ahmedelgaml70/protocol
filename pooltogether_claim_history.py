#!/usr/bin/env python3
"""Read-only PoolTogether V5 Base claimer reward evidence audit.

Queries *current published* PrizePool ClaimedPrize logs and receipts,
records actual claimReward accrual and receiver vs tx sender, and gas cost.
It DOES NOT claim prizes, sign, swap, withdraw or broadcast transactions.
A historical claimed prize cannot be claimed a second time.
"""
import argparse
from collections import defaultdict, Counter
from decimal import Decimal
import json
import os
from pathlib import Path
import sys

from kerf_radar import JSONRPC, RPCError, words
from block_range import start_block_for_hours

CHAIN_ID = 8453
PRIZE_POOL = "0x45b2010d8a4f08b53c9fa7544c51dfd9733732cb"
CLAIMER = "0xcdCE635b774DE77cdF791647601dba64a75547ba"
POOL_TOKEN = "0xd652C5425aea2Afd5fb142e120FeCf79e18fafc3"
TOPIC = "0x81d4e3306aa30f56dc9c3949abd8c27539b445f9ef380425f39f3f7114888e4f"
DEFAULT_RPC = "https://mainnet.base.org"


def read_address(topic):
    x = int(topic, 16)
    if x >> 160:
        raise ValueError("Invalid address topic padding")
    return "0x" + f"{x:040x}"


def decode_claim(log):
    """ABI indexed vault/winner/recipient + six non-indexed values."""
    if log.get("address", "").lower() != PRIZE_POOL.lower():
        raise ValueError("Log not from expected prize pool")
    topics = log.get("topics", [])
    if len(topics) != 4 or topics[0].lower() != TOPIC.lower():
        raise ValueError("Unexpected claimed-prize event topics")
    data = words(log.get("data", "0x"))
    if len(data) != 6:
        raise ValueError("Unexpected ClaimedPrize event data shape")
    if data[0] >= 2**24 or data[1] >= 2**8 or data[2] >= 2**32:
        raise ValueError("Out-of-range draw/tier/prize index")
    if data[3] >= 2**152 or data[4] >= 2**96:
        raise ValueError("Malformed payout or claim fee")
    if data[5] >= 2**160:
        raise ValueError("Bad reward recipient address")
    return {
        "transaction_hash": log["transactionHash"].lower(),
        "block_number": int(log["blockNumber"], 16),
        "vault": read_address(topics[1]),
        "winner": read_address(topics[2]),
        "prize_recipient": read_address(topics[3]),
        "draw_id": data[0],
        "tier": data[1],
        "prize_index": data[2],
        "prize_payout_raw": str(data[3]),
        "claim_reward_raw": str(data[4]),
        "reward_recipient": "0x" + f"{data[5]:040x}"
    }


def collect(rpc, latest, start, chunk):
    claims = []
    for left in range(start, latest + 1, chunk):
        right = min(latest, left + chunk - 1)
        result = rpc.rpc("eth_getLogs", [{
            "address": PRIZE_POOL,
            "fromBlock": hex(left),
            "toBlock": hex(right),
            "topics": [TOPIC]
        }])
        if not isinstance(result, list):
            raise RPCError("eth_getLogs did not return a list")
        claims.extend(decode_claim(log) for log in result)
    return claims


def summarize(claims, decimals, start, latest):
    by_tx = defaultdict(list)
    by_receiver = Counter()
    for x in claims:
        by_tx[x["transaction_hash"]].append(x)
        by_receiver[x["reward_recipient"]] += int(x["claim_reward_raw"])
    return {
        "chain_id": CHAIN_ID,
        "prize_pool": PRIZE_POOL,
        "current_published_claimer": CLAIMER,
        "pool_token_contract": POOL_TOKEN,
        "token_decimals_verified_onchain": decimals,
        "from_block": start,
        "to_block": latest,
        "claimed_prize_events": len(claims),
        "unique_transactions": len(by_tx),
        "events_with_positive_claim_reward": sum(int(x["claim_reward_raw"]) > 0 for x in claims),
        "total_claim_reward_tokens": str(
            Decimal(sum(int(x["claim_reward_raw"]) for x in claims)) / (10**decimals)
        ),
        "reward_receivers": [
            {"address": a, "claim_reward_tokens": str(Decimal(v)/(10**decimals))}
            for a, v in by_receiver.most_common(25)
        ],
        "claims": claims,
        "transactions_sent": 0,
        "profit_usd_verified": False,
        "warning": "Indexed claimReward is an ACCRUED reward balance for fee recipient, not proof of token withdrawal, realized USD profit, or open claim."
    }


def attach_receipt_samples(rpc, output, sample=10):
    by_tx = defaultdict(list)
    for row in output["claims"]:
        by_tx[row["transaction_hash"]].append(row)
    keys = sorted(
        by_tx,
        key=lambda h: (-sum(int(x["claim_reward_raw"]) for x in by_tx[h]), h)
    )[:sample]
    receipts = []
    for h in keys:
        tx = rpc.rpc("eth_getTransactionByHash", [h])
        receipt = rpc.rpc("eth_getTransactionReceipt", [h])
        if not tx or not receipt or int(receipt["status"], 16) != 1:
            raise ValueError("A ClaimedPrize event must have successful accessible receipt")
        gas = int(receipt["gasUsed"], 16) * int(receipt["effectiveGasPrice"], 16)
        l1 = int(receipt["l1Fee"], 16) if receipt.get("l1Fee") is not None else None
        fee_raw = sum(int(x["claim_reward_raw"]) for x in by_tx[h])
        sender = tx["from"].lower()
        recipients = {x["reward_recipient"] for x in by_tx[h] if int(x["claim_reward_raw"]) > 0}
        receipts.append({
            "transaction_hash":h,
            "sender":sender,
            "event_claim_reward_tokens":str(Decimal(fee_raw)/(10**output["token_decimals_verified_onchain"])),
            "reward_recipients":sorted(recipients),
            "fee_recipient_is_submitter":len(recipients)==1 and sender in recipients,
            "network_fee_wei":str(gas+l1) if l1 is not None else None,
            "l1_fee_available":l1 is not None,
            "warning":"Claims are already executed; fees are accrued to reward recipients, not necessarily transferred in tx."
        })
    output["receipt_samples"] = receipts
    output["receipt_sample_nonrandom"] = True
    return output


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--rpc", default=os.environ.get("BASE_RPC_URL", DEFAULT_RPC))
    p.add_argument("--lookback-hours", type=float, default=6)
    p.add_argument("--chunk", type=int, default=1000)
    p.add_argument("--max-sample-receipts", type=int, default=10)
    p.add_argument("--output", default="pooltogether_claim_history.json")
    a = p.parse_args(argv)
    if not 0 < a.lookback_hours <= 72 or not 100 <= a.chunk <= 2000:
        p.error("--lookback-hours must be (0,72]; --chunk 100..2000")
    if not 0 <= a.max_sample_receipts <= 100:
        p.error("--max-sample-receipts must be 0..100")
    rpc = JSONRPC(a.rpc)
    try:
        chain = int(rpc.rpc("eth_chainId", []),16)
        if chain != CHAIN_ID:
            raise RPCError("Wrong chain; expected Base 8453")
        latest = int(rpc.rpc("eth_blockNumber", []), 16)
        if rpc.rpc("eth_getCode", [PRIZE_POOL, hex(latest)]) in ("0x", None):
            raise RPCError("No PrizePool code at published Base address")
        decimals_result = words(rpc.call(POOL_TOKEN, "0x313ce567", hex(latest)))
        if len(decimals_result) != 1 or not 0 <= decimals_result[0] <= 36:
            raise ValueError("Could not verify POOL token decimals")
        start = start_block_for_hours(rpc,latest, 1, a.lookback_hours)
        claims = collect(rpc,latest,start,a.chunk)
        out = summarize(claims,decimals_result[0],start,latest)
        attach_receipt_samples(rpc,out,a.max_sample_receipts)
    except (RPCError, ValueError, OSError, KeyError) as exc:
        print(f"POOLTOGETHER SCAN FAILED: {type(exc).__name__}: {str(exc)[:200]}",file=sys.stderr)
        return 2
    Path(a.output).write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("Events:",out["claimed_prize_events"],"positive:",out["events_with_positive_claim_reward"],
          "transactions:",out["unique_transactions"])
    print("Raw accrued POOL fees:",out["total_claim_reward_tokens"])
    print("READ ONLY; no prize claimed, no tokens moved. Output:",a.output)
    return 0


if __name__=="__main__":
    raise SystemExit(main())
