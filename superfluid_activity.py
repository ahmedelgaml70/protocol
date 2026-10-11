#!/usr/bin/env python3
"""Read-only historical Superfluid V2 liquidation sample via official subgraph.

Subgraph state can lag continuous streams. An indexed event is NOT a currently
claimable opportunity, independently validated receipt or realized profit.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone, timedelta
import json
from pathlib import Path
import sys
import urllib.request

ENDPOINTS = {
    "base-mainnet": "https://subgraph-endpoints.superfluid.dev/base-mainnet/protocol-v1",
    "arbitrum-one": "https://subgraph-endpoints.superfluid.dev/arbitrum-one/protocol-v1",
    "optimism-mainnet": "https://subgraph-endpoints.superfluid.dev/optimism-mainnet/protocol-v1",
    "polygon-mainnet": "https://subgraph-endpoints.superfluid.dev/polygon-mainnet/protocol-v1",
}
# Entity and field names match the published Superfluid monorepo GraphQL schema.
QUERY = """query($limit:Int!,$since:BigInt!){
 agreementLiquidatedV2Events(first:$limit,orderBy:timestamp,orderDirection:desc,where:{timestamp_gte:$since}){
  timestamp transactionHash token liquidatorAccount rewardAmountReceiver rewardAmount liquidationType
 }
}"""


def summarize(events, since, until, limit):
    """Summarize raw event counts, not incomparable cross-token reward totals."""
    if not isinstance(events, list):
        raise ValueError("Invalid subgraph data")
    rows, callers, tokens = [], Counter(), Counter()
    for e in events:
        ts = int(e["timestamp"])
        if ts < since or ts > until + 600:
            raise ValueError("Subgraph event outside expected time range")
        caller = e["liquidatorAccount"].lower()
        token = e["token"].lower()
        receiver = e["rewardAmountReceiver"].lower()
        amount = int(e["rewardAmount"])
        if amount < 0:
            raise ValueError("Negative reward amount")
        rows.append({
            "timestamp_utc": datetime.fromtimestamp(ts, timezone.utc).isoformat(),
            "transaction_hash": e["transactionHash"], "token_address": token,
            "caller": caller, "reward_receiver": receiver,
            "reward_raw": str(amount), "liquidation_type_code": e.get("liquidationType")
        })
        callers[caller] += 1
        tokens[token] += 1
    return {
        "window_since_utc": datetime.fromtimestamp(since, timezone.utc).isoformat(),
        "window_until_utc": datetime.fromtimestamp(until, timezone.utc).isoformat(),
        "events_sampled": len(rows), "sample_limit": limit,
        "sample_may_be_truncated": len(rows) == limit,
        "unique_caller_addresses": len(callers),
        "top_caller_event_share": max(callers.values())/len(rows) if rows else None,
        "caller_event_counts": callers.most_common(25),
        "event_counts_by_token_address": dict(tokens),
        "events": rows, "profit_usd_verified": False,
        "notice": "Indexed events only, not independently verified receipts; no live eligibility, token price, or realized profit."
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--network", choices=tuple(ENDPOINTS), default="base-mainnet")
    p.add_argument("--days", type=int, default=30)
    p.add_argument("--limit", type=int, default=300)
    p.add_argument("--output", default="superfluid_activity.json")
    args = p.parse_args(argv)
    if not 1 <= args.days <= 365 or not 1 <= args.limit <= 1000:
        p.error("days 1..365 and limit 1..1000 required")
    now = int(datetime.now(timezone.utc).timestamp())
    since = int((datetime.now(timezone.utc)-timedelta(days=args.days)).timestamp())
    payload = json.dumps({"query": QUERY, "variables": {
        "limit": args.limit, "since": str(since)
    }}).encode()
    req = urllib.request.Request(ENDPOINTS[args.network], data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "protocol-readonly-subgraph/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            result = json.load(response)
        if not isinstance(result, dict) or result.get("errors") or not isinstance(result.get("data"), dict):
            raise ValueError("GraphQL subgraph returned errors or empty data")
        data = summarize(result["data"]["agreementLiquidatedV2Events"], since, now, args.limit)
    except (OSError, TimeoutError, ValueError, TypeError, KeyError) as exc:
        print(f"ACTIVITY SCAN FAILED: {type(exc).__name__}: {str(exc)[:140]}", file=sys.stderr)
        return 2
    data["network"] = args.network
    data["data_source"] = ENDPOINTS[args.network]
    Path(args.output).write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")
    print("Indexed events:", data["events_sampled"],
          "unique callers:", data["unique_caller_addresses"],
          "potentially truncated:", data["sample_may_be_truncated"])
    print("READ ONLY. Output:", args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
