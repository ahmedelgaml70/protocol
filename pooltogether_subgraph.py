#!/usr/bin/env python3
"""PoolTogether Base: official Graph subgraph discovery + on-chain receipt validation.

Read-only. A prize claim is already complete; even a verified fee does NOT
represent an unclaimed reward, withdrawable cash, profitable action, or
authorization to send transactions.
"""
import argparse
from datetime import datetime, timezone, timedelta
from decimal import Decimal
import json
import os
from pathlib import Path
import re
import sys
import urllib.request

from kerf_radar import JSONRPC, RPCError, words
from pooltogether_claim_history import (
    PRIZE_POOL, CLAIMER, TOPIC, PRIZE_TOKEN_SELECTOR, decode_claim
)

ENDPOINT = "https://api.studio.thegraph.com/query/41211/pt-v5-base/version/latest"
RPC_URL = "https://base-rpc.publicnode.com"
QUERY = """query Claims($since:BigInt!,$limit:Int!){
 prizeClaims(first:$limit,orderBy:timestamp,orderDirection:desc,
             where:{timestamp_gte:$since}){
   txHash timestamp claimReward claimRewardRecipient
 }
 _meta { block { number } }
}"""
HASH = re.compile(r"^0x[0-9a-fA-F]{64}$")


def graph_query(since, limit, endpoint=ENDPOINT):
    req = urllib.request.Request(
        endpoint,
        data=json.dumps({"query": QUERY, "variables": {
            "since": str(since), "limit": limit
        }}).encode(),
        headers={"Content-Type": "application/json",
                 "User-Agent": "protocol-research-graph/0.1"},
    )
    with urllib.request.urlopen(req, timeout=20) as stream:
        payload = json.load(stream)
    if not isinstance(payload, dict) or payload.get("errors"):
        raise ValueError("Official subgraph failed or returned GraphQL errors")
    data = payload.get("data")
    if not isinstance(data, dict) or not isinstance(data.get("prizeClaims"), list):
        raise ValueError("GraphQL response missing prizeClaims")
    return data


def select_tx_hashes(indexed, since, limit):
    """Deduplicate latest indexed prize claims, rejecting invalid/stale entries."""
    candidates = {}
    for e in indexed:
        h = str(e.get("txHash", "")).lower()
        if not HASH.fullmatch(h):
            raise ValueError("Bad transaction hash in GraphQL index")
        stamp = int(e["timestamp"])
        if stamp < since:
            raise ValueError("Out-of-window indexed claim")
        reward = int(e["claimReward"])
        if reward < 0:
            raise ValueError("Negative indexed claim reward")
        if h not in candidates:
            candidates[h] = {"timestamp": stamp, "indexed_reward_raw": 0,
                             "indexed_claim_events": 0}
        row = candidates[h]
        row["timestamp"] = max(row["timestamp"], stamp)
        row["indexed_reward_raw"] += reward
        row["indexed_claim_events"] += 1
    latest = sorted(candidates, key=lambda k: (-candidates[k]["timestamp"], k))
    largest = sorted(candidates, key=lambda k: (-candidates[k]["indexed_reward_raw"], k))
    top = max(1, limit // 2)
    chosen = list(dict.fromkeys(largest[:top] + latest))[:limit]
    return chosen, len(candidates)


def read_contract_token(rpc, block):
    token_result = words(rpc.call(PRIZE_POOL, PRIZE_TOKEN_SELECTOR, block))
    if len(token_result) != 1 or not (0 < token_result[0] < 2**160):
        raise ValueError("Invalid prizeToken() contract response")
    address = "0x" + f"{token_result[0]:040x}"
    decimals = words(rpc.call(address, "0x313ce567", block))
    if len(decimals) != 1 or decimals[0] > 36:
        raise ValueError("Invalid deployed prize token decimals")
    return address, decimals[0]


def verify_receipt(rpc, tx_hash, decimals):
    tx = rpc.rpc("eth_getTransactionByHash", [tx_hash])
    receipt = rpc.rpc("eth_getTransactionReceipt", [tx_hash])
    if not isinstance(tx, dict) or not isinstance(receipt, dict):
        raise ValueError("Missing chain transaction or receipt")
    if tx.get("hash", "").lower() != tx_hash or int(receipt.get("status", "0x0"), 16) != 1:
        raise ValueError("Invalid or failed claimed-prize receipt")
    found = []
    for log in receipt.get("logs", []):
        topics = log.get("topics") or []
        if log.get("address", "").lower() == PRIZE_POOL.lower() and topics and topics[0].lower() == TOPIC:
            found.append(decode_claim(log))
    if not found:
        raise ValueError("Indexed claim did not match a current PrizePool receipt log")
    raw = sum(int(e["claim_reward_raw"]) for e in found)
    recips = sorted({e["reward_recipient"] for e in found if int(e["claim_reward_raw"]) > 0})
    sender = tx["from"].lower()
    dest = (tx.get("to") or "").lower()
    gas = int(receipt["gasUsed"], 16) * int(receipt["effectiveGasPrice"], 16)
    l1 = receipt.get("l1Fee")
    full = gas + int(l1, 16) if l1 is not None else None
    return {
        "transaction_hash": tx_hash, "transaction_destination": dest,
        "submitting_address": sender,
        "sent_to_published_current_claimer": dest == CLAIMER.lower(),
        "receipt_status": "SUCCESS", "verified_prize_pool_event_count": len(found),
        "event_claim_reward_tokens": str(Decimal(raw) / Decimal(10**decimals)),
        "reward_recipients": recips, "fee_recipient_is_submitter": recips == [sender],
        "network_fee_wei": str(full) if full is not None else None,
        "l1_fee_available": l1 is not None,
        "warning": "Accrued historical fee, not net profit or an unclaimed prize"
    }


def inspect(rpc, indexed, since, limit, receipt_limit, meta_block=None):
    chain = int(rpc.rpc("eth_chainId", []), 16)
    if chain != 8453:
        raise RPCError(f"Wrong chain {chain}; expected Base 8453")
    latest = int(rpc.rpc("eth_blockNumber", []), 16)
    block = hex(latest)
    if rpc.rpc("eth_getCode", [PRIZE_POOL, block]) in ("0x", None):
        raise RPCError("Base PrizePool contract code missing")
    token, decimals = read_contract_token(rpc, block)
    hashes, distinct = select_tx_hashes(indexed, since, receipt_limit)
    checked, errors = [], []
    for h in hashes:
        try:
            checked.append(verify_receipt(rpc, h, decimals))
        except (RPCError, ValueError, TypeError, KeyError) as exc:
            errors.append({"transaction_hash": h, "error": type(exc).__name__})
    return {
        "chain_id": 8453, "source": "PoolTogether official Base subgraph + on-chain receipt check",
        "prize_pool": PRIZE_POOL, "current_published_claimer": CLAIMER,
        "prize_token_contract_verified_onchain": token, "token_decimals_verified_onchain": decimals,
        "observed_block_number": latest, "subgraph_head_block_number": meta_block,
        "since_utc": datetime.fromtimestamp(since, timezone.utc).isoformat(),
        "indexed_claim_events": len(indexed), "indexed_may_be_truncated": len(indexed) == limit,
        "distinct_indexed_claim_transactions": distinct,
        "receipt_samples": checked, "receipt_errors": errors,
        "claimed_prize_events": sum(e["verified_prize_pool_event_count"] for e in checked),
        "events_with_positive_claim_reward": sum(Decimal(e["event_claim_reward_tokens"]) > 0 for e in checked),
        "transactions_sent": 0, "profit_usd_verified": False,
        "warning": "Receipt samples only; index lag possible. Completed claims are no longer open; no fee liquidation or net USD profitability demonstrated."
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--endpoint", default=ENDPOINT)
    p.add_argument("--rpc", default=os.environ.get("BASE_RPC_URL", RPC_URL))
    p.add_argument("--days", type=float, default=3)
    p.add_argument("--limit", type=int, default=150)
    p.add_argument("--receipts", type=int, default=10)
    p.add_argument("--output", default="pooltogether_claim_history.json")
    a = p.parse_args(argv)
    if not 0 < a.days <= 30 or not 1 <= a.limit <= 500 or not 1 <= a.receipts <= 30:
        p.error("days >0..30, index limit 1..500, receipt limit 1..30 required")
    since = int((datetime.now(timezone.utc) - timedelta(days=a.days)).timestamp())
    try:
        data = graph_query(since, a.limit, a.endpoint)
        meta = data.get("_meta") or {}
        index_block = (meta.get("block") or {}).get("number")
        result = inspect(JSONRPC(a.rpc), data["prizeClaims"], since, a.limit, a.receipts, index_block)
    except (RPCError, OSError, ValueError, TypeError, KeyError) as exc:
        print(f"POOLTOGETHER INDEX SCAN FAILED: {type(exc).__name__}: {str(exc)[:160]}", file=sys.stderr)
        return 2
    Path(a.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("Indexed claims:", result["indexed_claim_events"],
          "receipt validated:", len(result["receipt_samples"]),
          "current Claimer positive:", sum(
              e["sent_to_published_current_claimer"] and Decimal(e["event_claim_reward_tokens"])>0
              for e in result["receipt_samples"]))
    print("READ ONLY. No prize claimed. Output:", a.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
