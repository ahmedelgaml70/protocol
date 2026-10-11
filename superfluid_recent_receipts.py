#!/usr/bin/env python3
"""Read-only audit of recent Superfluid Base ETHx liquidation receipts.

Consumes an archived Superfluid subgraph sample, deduplicates by transaction,
then checks the largest and newest ETHx transactions on Base RPC. Calculates
a conditional 1 ETHx = 1 ETH transfer-minus-gas proxy, NOT realized profit.
Never signs or sends transactions.
"""
import argparse
from collections import defaultdict
from decimal import Decimal
import json
import os
from pathlib import Path
import sys

from superfluid_receipts import RPC, RPCError, parse_receipt, CHAIN_ID, ETHX, DEFAULT_RPC

BATCH_LIQUIDATOR = "0x6b008bac0e5846cb5d9ca02ca0e801fcbf88b6f9"
TYPES = {0: "patrician_priority", 1: "pleb", 2: "pirate"}


def select_transactions(report, limit):
    if report.get("network") != "base-mainnet":
        raise ValueError("Only base-mainnet indexed activity is supported")
    if not 1 <= limit <= 100:
        raise ValueError("Limit must be 1..100")
    grouped = defaultdict(lambda: {"reward_raw": 0, "events": 0, "timestamp": "", "types": set()})
    for event in report.get("events", []):
        if event.get("token_address", "").lower() != ETHX.lower():
            continue
        tx_hash = event.get("transaction_hash", "")
        if not (tx_hash.startswith("0x") and len(tx_hash) == 66
                and all(c in "0123456789abcdefABCDEF" for c in tx_hash[2:])):
            raise ValueError("Invalid indexed transaction hash")
        row = grouped[tx_hash]
        raw = int(event["reward_raw"])
        if raw < 0:
            raise ValueError("Negative reward amount")
        row["reward_raw"] += raw
        row["events"] += 1
        row["timestamp"] = max(row["timestamp"], event["timestamp_utc"])
        row["types"].add(int(event["liquidation_type_code"]))
    if not grouped:
        return [], 0
    top_count = max(1, limit // 2)
    biggest = sorted(grouped, key=lambda h: (-grouped[h]["reward_raw"], h))[:top_count]
    newest = sorted(grouped, key=lambda h: (grouped[h]["timestamp"], h), reverse=True)
    chosen = list(dict.fromkeys(biggest + newest))[:limit]
    return [(h, grouped[h]) for h in chosen], len(grouped)


def audit_receipts(report, rpc, limit=12):
    if int(rpc.rpc("eth_chainId", []), 16) != CHAIN_ID:
        raise RPCError("RPC is not Base mainnet (8453)")
    selected, population = select_transactions(report, limit)
    rows = []
    for tx_hash, event in selected:
        tx = rpc.rpc("eth_getTransactionByHash", [tx_hash])
        receipt = rpc.rpc("eth_getTransactionReceipt", [tx_hash])
        observed = parse_receipt(tx, receipt)
        if tx.get("hash", "").lower() != tx_hash.lower():
            raise ValueError("Transaction hash mismatch")
        transferred = sum(int(x["amount_raw"]) for x in observed.get("inbound_transfers", [])
                          if x["from"].lower() == BATCH_LIQUIDATOR)
        fee = observed.get("full_fee_wei")
        parity_proxy = (
            (Decimal(transferred) - Decimal(fee)) / Decimal(10**18)
            if fee is not None and observed["status"] == "SUCCESS" else None
        )
        rows.append({
            "transaction_hash": tx_hash,
            "indexed_timestamp_utc": event["timestamp"],
            "indexed_ethx_reward_raw": str(event["reward_raw"]),
            "indexed_events_in_tx": event["events"],
            "indexed_types": [TYPES.get(t, f"unknown_{t}") for t in sorted(event["types"])],
            "submitting_address": observed.get("sender"),
            "receipt_status": observed["status"],
            "ethx_transferred_batch_to_submitter_raw": str(transferred),
            "reported_full_gas_fee_wei": fee,
            "ethx_to_eth_parity_proxy_after_gas": str(parity_proxy) if parity_proxy is not None else None,
            "parity_proxy_computable": parity_proxy is not None,
            "warning": "1 ETHx=1 ETH is an assumption; this is NOT actual profit. Token exit liquidity, swap costs, missed opportunities, failed-call losses, and future competition excluded."
        })
    return {
        "network": "base-mainnet", "chain_id": CHAIN_ID,
        "method": "subgraph discovery + read-only RPC receipt checks",
        "distinct_ethx_transactions_in_input_sample": population,
        "receipts_checked": len(rows), "all_ethx_transactions_checked": len(rows) == population,
        "rows": rows, "transactions_sent": 0, "verified_realized_profit_usd": None
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--activity", default="evidence/superfluid-base-2026-10-11-activity-full.json")
    parser.add_argument("--rpc", default=os.environ.get("BASE_RPC_URL", DEFAULT_RPC))
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--output", default="superfluid_recent_receipts.json")
    args = parser.parse_args(argv)
    try:
        source = json.loads(Path(args.activity).read_text(encoding="utf-8"))
        result = audit_receipts(source, RPC(args.rpc), args.limit)
    except (KeyError, ValueError, OSError, RPCError) as exc:
        print(f"RECEIPT AUDIT FAILED: {type(exc).__name__}: {str(exc)[:180]}", file=sys.stderr)
        return 2
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("Distinct ETHx transactions:", result["distinct_ethx_transactions_in_input_sample"])
    print("Receipts checked:", result["receipts_checked"])
    for row in result["rows"]:
        print(row["transaction_hash"][:14], row["receipt_status"],
              "ETH parity proxy after gas:", row["ethx_to_eth_parity_proxy_after_gas"])
    print("READ ONLY; not realized profit or current availability. Output:", args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
