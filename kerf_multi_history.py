#!/usr/bin/env python3
"""Read-only event census for three additional Kerf bounty mechanisms.

Counts historical protocol events, *not* net gains or live claimable funds.
Uses published addresses (Kerf deployment manifest); seed vaults only, so
this is NOT a complete audit of all vaults created since deployment.
Requires a working Robinhood Chain RPC endpoint. No wallet, no signing.
"""
import argparse
from collections import Counter
import json
import os
from pathlib import Path
import sys
from kerf_radar import CHAIN_ID, DEFAULT_RPC, JSONRPC, RPCError, RANGE_ORDERS, words
from block_range import start_block_for_hours

DEPLOYMENT_BLOCK_CLAIM = 56938742
KEEPER = "0x5D9120F45271374c7c8E185CCa121D88A250a71A"
PERP = "0xf9BbAC0f3a05EDf75b6d01D54Fe194f10B50034c"
# Directly from https://github.com/KerfFinance/kerf-contracts/blob/main/deployments/robinhood.json
SEED_VAULTS = {
    "ETH Vault": "0x964837e37D9ca6697544cA583dFb7e02B5dB6E28",
    "USDG Vault": "0x5a3Ca1c1234Eda1AAb3698EEed1A4d95B7DF3ADe",
    "NVDA Hedged": "0x4FDC405e485340f0d99e3Bc7dfA3bfb59796e506",
    "SPY Hedged": "0x8F6b0e2D4ba796396ca73cf95B2679B473087E6D",
    "Income NVDA": "0x558ad16e6A90509cd392845265dF42B4205e3400",
    "Protected SPY": "0xc73Fd4a393cCB10977E764BeE0ca57E8b13D62Bd",
}
# Keccak-256 of canonical Solidity event signatures (validated against published source).
TOPICS = {
    "0xd7612277cfab99e98a6e102dadbfb19c48b33e6bd1ba17ee3b1778c2c04ef888": "VaultHarvest",
    "0x68cf8717f566d6a94c69f0a80648ec78112c770669f3f1c33183693e7e9c8c48": "PositionHarvest",
    "0xf4c6cbfcc96248be8ecbaf76de0fee34f71f2fadd9af537dd38c2657621930d6": "PerpLiquidation",
}
VAULT_BY_ADDRESS = {v.lower(): k for k, v in SEED_VAULTS.items()}
VALID_ADDRESSES = set(VAULT_BY_ADDRESS) | {KEEPER.lower(), PERP.lower()}


def decode_event(entry):
    src = entry.get("address", "").lower()
    topics = entry.get("topics", [])
    if src not in VALID_ADDRESSES or not topics:
        return None
    kind = TOPICS.get(topics[0].lower())
    if not kind:
        return None
    payload = words(entry.get("data", "0x"))
    out = {
        "kind": kind, "block_number": int(entry["blockNumber"], 16),
        "tx_hash": entry["transactionHash"], "contract": src,
    }
    if kind == "VaultHarvest":
        if src not in VAULT_BY_ADDRESS or len(topics) != 1 or len(payload) != 6:
            raise ValueError("Unexpected vault harvest event shape")
        out.update({
            "vault": VAULT_BY_ADDRESS[src], "fees0_raw": str(payload[0]),
            "fees1_raw": str(payload[1]),
            "bounty0_raw": str(payload[4]), "bounty1_raw": str(payload[5])
        })
    elif kind == "PositionHarvest":
        if src != KEEPER.lower() or len(topics) != 3 or len(payload) != 5:
            raise ValueError("Unexpected PositionKeeper harvest event shape")
        out.update({
            "token_id": int(topics[1], 16),
            "keeper": "0x" + f"{int(topics[2],16) & ((1<<160)-1):040x}",
            "fees0_raw": str(payload[0]), "fees1_raw": str(payload[1]),
            "bounty0_raw": str(payload[2]), "bounty1_raw": str(payload[3]),
            "compounded": bool(payload[4])
        })
    else:
        if src != PERP.lower() or len(topics) != 3 or len(payload) != 1:
            raise ValueError("Unexpected premarket perp liquidation shape")
        out.update({
            "position_id": int(topics[1],16),
            "liquidator": "0x" + f"{int(topics[2],16) & ((1<<160)-1):040x}",
            "bounty_usdg_raw": str(payload[0])
        })
    return out


def collect(rpc, start, end, chunk=2000):
    events = []
    addresses = [KEEPER, PERP] + list(SEED_VAULTS.values())
    for left in range(start, end + 1, chunk):
        right = min(end, left + chunk - 1)
        raw = rpc.rpc("eth_getLogs", [{
            "address": addresses,
            "fromBlock": hex(left), "toBlock": hex(right),
            "topics": [list(TOPICS.keys())]
        }])
        if not isinstance(raw, list):
            raise RPCError("RPC eth_getLogs did not return a list")
        for event in raw:
            item = decode_event(event)
            if item:
                events.append(item)
    return events


def summarize(events, start, end):
    kinds = Counter(e["kind"] for e in events)
    keeper_captures = Counter(
        e["keeper"].lower() for e in events if e["kind"] == "PositionHarvest"
    )
    perp_captures = Counter(
        e["liquidator"].lower() for e in events if e["kind"] == "PerpLiquidation"
    )
    paid = {
        "vault_positive_bounties": sum(
            int(e["bounty0_raw"]) + int(e["bounty1_raw"]) > 0
            for e in events if e["kind"] == "VaultHarvest"
        ),
        "position_positive_bounties": sum(
            int(e["bounty0_raw"]) + int(e["bounty1_raw"]) > 0
            for e in events if e["kind"] == "PositionHarvest"
        ),
        "perp_positive_bounties": sum(
            int(e["bounty_usdg_raw"]) > 0
            for e in events if e["kind"] == "PerpLiquidation"
        )
    }
    return {
        "chain_id": CHAIN_ID, "scan_from_block": start, "scan_to_block": end,
        "coverage": "six published seed vaults + the single PositionKeeper and PreMarketPerp addresses ONLY",
        "event_counts": dict(kinds), "positive_reward_event_counts": paid,
        "unique_position_keeper_callers": len(keeper_captures),
        "unique_perp_liquidator_callers": len(perp_captures),
        "top_position_keeper_share": max(keeper_captures.values()) / sum(keeper_captures.values())
            if keeper_captures else None,
        "top_perp_liquidator_share": max(perp_captures.values()) / sum(perp_captures.values())
            if perp_captures else None,
        "observations": events,
        "transactions_sent": 0, "funds_spent_usd": 0,
        "warning": "Historical raw events only. Different bounty tokens MUST NOT be summed. No USD value, transaction fees or realized profit established."
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--rpc", default=os.environ.get("ROBINHOOD_RPC_URL", DEFAULT_RPC))
    p.add_argument("--lookback-blocks", type=int, default=None, help="Manual block window; overrides hours")
    p.add_argument("--lookback-hours", type=float, default=24, help="Last N hours, uses block timestamps")
    p.add_argument("--chunk", type=int, default=2000)
    p.add_argument("--output", default="multi_bounty_history.json")
    a = p.parse_args(argv)
    if a.lookback_blocks is not None and not (1 <= a.lookback_blocks <= 5000000):
        p.error("--lookback-blocks must be 1..5000000")
    if not 0 < a.lookback_hours <= 720:
        p.error("--lookback-hours must be >0 and <=720")
    if not 1 <= a.chunk <= 5000:
        p.error("--chunk must be 1..5000")
    rpc = JSONRPC(a.rpc)
    try:
        chain = int(rpc.rpc("eth_chainId", []), 16)
        if chain != CHAIN_ID:
            raise RPCError(f"Unexpected chain ID {chain}")
        latest = int(rpc.rpc("eth_blockNumber", []), 16)
        start = (max(DEPLOYMENT_BLOCK_CLAIM, latest - a.lookback_blocks + 1)
                 if a.lookback_blocks is not None
                 else start_block_for_hours(rpc, latest, DEPLOYMENT_BLOCK_CLAIM, a.lookback_hours))
        if start > latest:
            raise RPCError("Deployment block later than current chain tip")
        for contract in (KEEPER, PERP, *SEED_VAULTS.values()):
            if rpc.rpc("eth_getCode", [contract, hex(latest)]) in ("0x", None):
                raise RPCError("Missing expected deployed contract code; inspect manifest")
        result = summarize(collect(rpc, start, latest, a.chunk), start, latest)
    except (RPCError, ValueError) as exc:
        print(f"MULTI BOUNTY HISTORY FAILED: {exc}", file=sys.stderr)
        return 2
    Path(a.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("Historic events", result["event_counts"])
    print("Positive reward events", result["positive_reward_event_counts"])
    print("READ ONLY; no funds moved. Output:", a.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
