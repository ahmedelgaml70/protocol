#!/usr/bin/env python3
"""Read-only Kerf RangeOrders historical event audit: event counts, not USD profits."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys
from kerf_radar import CHAIN_ID, DEFAULT_RPC, RANGE_ORDERS, JSONRPC, RPCError, address, words
from block_range import start_block_for_hours

# Event topics derived from the published Kerf contract's event signatures.
TOPICS = {
    "0x1d431d65f6966945cfbd29e001d16ca848fea8ed2592fea14adf6a7f8fb98620": "Placed",
    "0xdef4cdb91e8c5e2777b0bf9645ce2c7e0b64a3b3fb94e37c6d78cde1043f80cb": "Filled",
    "0x85880e29de5e2bae8d4c8c1ff6f504e15a1ad0b94b8102feb034e4390ce26a75": "Cancelled"
}
# Unverified source-repository deployment claim, NOT an observed deployment proof.
CLAIMED_DEPLOYMENT_BLOCK = 56938742


def fetch_events(rpc, start, end, chunk=2000):
    out = []
    for left in range(start, end + 1, chunk):
        right = min(end, left + chunk - 1)
        logs = rpc.rpc("eth_getLogs", [{
            "address": RANGE_ORDERS,
            "fromBlock": hex(left), "toBlock": hex(right),
            "topics": [list(TOPICS)]
        }])
        for event in logs:
            topics = event.get("topics", [])
            name = TOPICS.get(topics[0].lower()) if topics else None
            if not name or len(topics) < 2:
                continue
            row = {
                "event": name,
                "order_id": int(topics[1], 16),
                "block": int(event["blockNumber"], 16),
                "tx_hash": event["transactionHash"]
            }
            data = words(event.get("data", "0x"))
            if name == "Filled":
                if len(topics) < 3 or len(data) != 3:
                    raise ValueError("Unexpected Filled event ABI; recheck contract")
                row.update({
                    "keeper": address(int(topics[2], 16)),
                    "amount_out_raw": str(data[0]),
                    "fees_earned_raw": str(data[1]),
                    "bounty_raw": str(data[2])
                })
            elif name == "Placed":
                if len(topics) < 3 or len(data) != 5:
                    raise ValueError("Unexpected Placed event ABI; recheck contract")
                row["owner"] = address(int(topics[2], 16))
            out.append(row)
    return out


def summarize(events, chain_id, start, end):
    fills = [e for e in events if e["event"] == "Filled"]
    winners = Counter(e["keeper"].lower() for e in fills)
    return {
        "chain_id": chain_id, "contract": RANGE_ORDERS,
        "from_block": start, "to_block": end,
        "total_events": len(events),
        "placed_events": sum(e["event"] == "Placed" for e in events),
        "filled_events": len(fills),
        "cancelled_events": sum(e["event"] == "Cancelled" for e in events),
        "unique_keeper_addresses": len(winners),
        "top_keeper_fill_share": max(winners.values()) / len(fills) if fills else None,
        "keepers_by_fills": [{"address": x, "fills": n} for x, n in winners.most_common(20)],
        "events": events,
        "transactions_sent": 0, "funds_spent_usd": 0,
        "warning": "Bounties are raw, different token units; no realized profits established."
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--rpc", default=DEFAULT_RPC)
    p.add_argument("--lookback-blocks", type=int, default=None, help="Manual block window; overrides hours")
    p.add_argument("--lookback-hours", type=float, default=24, help="Last N hours, uses block timestamps")
    p.add_argument("--chunk", type=int, default=2000)
    p.add_argument("--output", default="history.json")
    a = p.parse_args(argv)
    if a.lookback_blocks is not None and not (1 <= a.lookback_blocks <= 5000000):
        p.error("--lookback-blocks must be 1..5000000")
    if not 0 < a.lookback_hours <= 720 or not 1 <= a.chunk <= 10000:
        p.error("hours range >0..720 and chunk 1..10000 required")
    rpc = JSONRPC(a.rpc)
    try:
        chain = int(rpc.rpc("eth_chainId", []), 16)
        if chain != CHAIN_ID:
            raise RPCError("Unexpected chain ID")
        latest = int(rpc.rpc("eth_blockNumber", []), 16)
        if rpc.rpc("eth_getCode", [RANGE_ORDERS, hex(latest)]) in ("0x", None):
            raise RPCError("Contract bytecode absent")
        start = (max(CLAIMED_DEPLOYMENT_BLOCK, latest - a.lookback_blocks + 1)
                 if a.lookback_blocks is not None
                 else start_block_for_hours(rpc, latest, CLAIMED_DEPLOYMENT_BLOCK, a.lookback_hours))
        events = fetch_events(rpc, start, latest, a.chunk)
        report = summarize(events, chain, start, latest)
    except (RPCError, ValueError) as exc:
        print(f"HISTORY FAILED: {exc}", file=sys.stderr)
        return 2
    Path(a.output).write_text(json.dumps(report, indent=2) + "\n", encoding="utf8")
    print(f"Range {start}–{latest} | fills {report['filled_events']} | keepers {report['unique_keeper_addresses']}")
    print("READ ONLY; no funds spent. Output:", a.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
