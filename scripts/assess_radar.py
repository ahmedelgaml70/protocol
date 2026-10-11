#!/usr/bin/env python3
"""Strictly convert recent receipt evidence into research-only alert signals.

No historical event is a currently open bounty. This tool never computes USD profit.
"""
import argparse
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import re

CLAIMER = "0xcdce635b774de77cdf791647601dba64a75547ba"
PRIZE_POOL = "0x45b2010d8a4f08b53c9fa7544c51dfd9733732cb"
TX_HASH = re.compile(r"^0x[0-9a-fA-F]{64}$")
ADDRESS = re.compile(r"^0x[0-9a-fA-F]{40}$")

def read_json(path):
    path = Path(path)
    if path.stat().st_size > 5_000_000:
        raise ValueError("Oversized report")
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise ValueError("Report root must be object")
    return obj

def pool_signal(manifest, report):
    checks = manifest.get("checks", [])
    check = next((x for x in checks
                  if isinstance(x, dict) and x.get("scanner") == "pooltogether-base"), None)
    if not check or check.get("status") != "ok":
        return None
    if (report.get("chain_id") != 8453
            or str(report.get("prize_pool", "")).lower() != PRIZE_POOL
            or str(report.get("current_published_claimer", "")).lower() != CLAIMER):
        return None
    token = str(report.get("prize_token_contract_verified_onchain", "")).lower()
    if not ADDRESS.fullmatch(token):
        return None
    rows = report.get("receipt_samples", [])
    if not isinstance(rows, list):
        return None
    matches = []
    for r in rows:
        if not isinstance(r, dict):
            continue
        h = str(r.get("transaction_hash", "")).lower()
        if not TX_HASH.fullmatch(h):
            continue
        if not r.get("sent_to_published_current_claimer"):
            continue
        if str(r.get("transaction_destination", "")).lower() != CLAIMER:
            continue
        if not r.get("l1_fee_available") or r.get("network_fee_wei") is None:
            continue
        try:
            earned = Decimal(str(r.get("event_claim_reward_tokens")))
            fee_wei = int(r["network_fee_wei"])
        except (TypeError, ValueError, InvalidOperation):
            continue
        if not earned.is_finite() or earned <= 0 or fee_wei < 0:
            continue
        recips = r.get("reward_recipients", [])
        if not isinstance(recips, list) or not recips or not all(
                isinstance(a, str) and ADDRESS.fullmatch(a) for a in recips):
            continue
        matches.append({"transaction_hash": h, "accrued_reward_tokens": str(earned),
                        "full_gas_fee_wei": str(fee_wei),
                        "reward_recipients": [x.lower() for x in recips],
                        "is_submitter_reward_receiver": bool(r.get("fee_recipient_is_submitter"))})
    if not matches:
        return None
    matches.sort(key=lambda x: (Decimal(x["accrued_reward_tokens"]), x["transaction_hash"]),
                 reverse=True)
    return {
        "key": "pooltogether-base-current-claimer-paid-history",
        "status": "RESEARCH_ONLY_NOT_EXECUTION_READY",
        "protocol": "PoolTogether V5", "network": "Base", "chain_id": 8453,
        "prize_pool": PRIZE_POOL, "claimer": CLAIMER,
        "prize_token_address": token,
        "current_claims_observed": len(matches),
        "examples": matches[:3],
        "warning": "Historical accrued claim rewards, NOT proof of withdrawal or profit. "
                   "No current unclaimed prize, competition or sale price verified.",
    }

def evaluate(manifest, reports):
    if manifest.get("schema_version") != 1 or manifest.get("purpose") != "READ_ONLY_RESEARCH":
        raise ValueError("Invalid manifest purpose/schema")
    signals = []
    if "pooltogether-base" in reports:
        signal = pool_signal(manifest, reports["pooltogether-base"])
        if signal:
            signals.append(signal)
    return {"schema_version": 1,
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "signals": signals, "execution_ready": False, "funds_spent_usd": 0}

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--report-dir", default="reports")
    p.add_argument("--output", default="alerts.json")
    args = p.parse_args(argv)
    folder = Path(args.report_dir)
    manifest = read_json(folder / "manifest.json")
    reports = {}
    for item in manifest.get("checks", []):
        if (isinstance(item, dict) and item.get("scanner") == "pooltogether-base"
                and item.get("status") == "ok"
                and item.get("report_file") == "pooltogether_claim_history.json"):
            reports["pooltogether-base"] = read_json(folder / "pooltogether_claim_history.json")
    decision = evaluate(manifest, reports)
    Path(args.output).write_text(json.dumps(decision, indent=2) + "\n", encoding="utf-8")
    print("Research signals:", len(decision["signals"]), "execution-ready: NO")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
