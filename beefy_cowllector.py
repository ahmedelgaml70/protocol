#!/usr/bin/env python3
"""Read-only economic screen for Beefy's published Cowllector v2 last reports.

This is the Cowllector operator's LAST report per vault, not all harvests.
Estimated gains from the API are NOT authenticated on-chain recipient payouts,
actual profits, an unclaimed reward, or a green light to execute anything.
"""
import argparse
from collections import Counter
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import sys
import urllib.error
import urllib.request

SOURCE = "https://cowllector.beefy.com/api/v1/last-harvest-reports"
ALLOWED_CHAINS = {"base", "arbitrum", "optimism", "polygon", "ethereum"}
FIELDS = (
    "simulation_gas_estimated_call_rewards_wei",
    "simulation_gas_transaction_cost_estimation_wei",
    "simulation_gas_estimated_gain_wei",
    "transaction_estimated_profit_wei",
)
# API JSON schema uses JS numbers for wei amounts, which can lose base-unit precision.
MAX_RESPONSE_BYTES = 18_000_000


def fetch_reports(url=SOURCE, timeout=30):
    if url != SOURCE:
        raise ValueError("Only the official documented Cowllector endpoint is accepted")
    req = urllib.request.Request(
        url, headers={"Accept": "application/json", "User-Agent": "protocol-readonly-beefy/1.0"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        payload = response.read(MAX_RESPONSE_BYTES + 1)
    if len(payload) > MAX_RESPONSE_BYTES:
        raise ValueError("Cowllector response exceeded size limit")
    result = json.loads(payload)
    if not isinstance(result, dict) or not isinstance(result.get("data"), list):
        raise ValueError("Cowllector API response not a {data:[...]} object")
    return result["data"]


def parse_utc(value):
    if not isinstance(value, str):
        raise ValueError("Missing report time")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("Report timestamp missing time zone")
    return parsed.astimezone(timezone.utc)


def api_number(value):
    """Approximate ONLY. Upstream represents wei as JSON numbers (JS precision)."""
    if value is None or isinstance(value, bool):
        return None
    try:
        v = Decimal(str(value))
        if v.is_finite() and abs(v) < Decimal(10) ** 40:
            return v
    except (ValueError, InvalidOperation):
        pass
    return None


def summarize(records, now, hours=72, chains=None, top=20):
    """Classify observations; do not convert token units to market prices."""
    if not isinstance(records, list):
        raise ValueError("Expected Cowllector report array")
    if not (1 <= hours <= 30*24) or not (1 <= top <= 100):
        raise ValueError("hours 1..720 and top 1..100 required")
    chosen = set(chains or ["base", "arbitrum", "optimism"])
    if not chosen.issubset(ALLOWED_CHAINS):
        raise ValueError("Unsupported chain requested")
    cutoff = now - timedelta(hours=hours)
    chain_counts = Counter()
    stages = Counter()
    all_recent = 0
    candidates = []
    invalid_rows = 0
    for item in records:
        if not isinstance(item, dict):
            invalid_rows += 1
            continue
        chain = str(item.get("chain", "")).lower()
        if chain not in chosen:
            continue
        try:
            stamp = parse_utc(item.get("datetime"))
        except ValueError:
            invalid_rows += 1
            continue
        if stamp < cutoff or stamp > now + timedelta(minutes=15):
            continue
        all_recent += 1
        chain_counts[chain] += 1
        if item.get("summary_harvested") is True:
            stages["operator_reported_harvested"] += 1
        if item.get("transaction_ok") is True:
            stages["operator_reported_tx_ok"] += 1
        if item.get("eol") is not False:
            stages["end_of_life_or_unknown"] += 1
            continue
        stages["active_vault"] += 1
        if item.get("run_ok") is not True:
            stages["operator_run_not_ok"] += 1
            continue
        stages["active_run_ok"] += 1
        if not isinstance(item.get("vault_id"), str) or not isinstance(item.get("strategy_address"), str):
            invalid_rows += 1
            continue
        values = {k: api_number(item.get(k)) for k in FIELDS}
        if item.get("simulation_ok") is not True:
            stages["simulation_not_ok"] += 1
            continue
        stages["simulation_ok"] += 1
        call_reward = values["simulation_gas_estimated_call_rewards_wei"]
        gas_cost = values["simulation_gas_transaction_cost_estimation_wei"]
        estimated_gain = values["simulation_gas_estimated_gain_wei"]
        if call_reward is None or gas_cost is None:
            stages["simulation_reward_or_gas_missing"] += 1
            continue
        stages["simulation_reward_and_gas_available"] += 1
        if call_reward < 0 or gas_cost < 0:
            stages["invalid_negative_report_amount"] += 1
            continue
        stages["simulation_nonnegative_reward_and_gas"] += 1
        if call_reward > 0:
            stages["simulated_positive_reward"] += 1
        # Conservative fixed-position comparison for the SAME published native-like unit.
        margin = call_reward - gas_cost
        if margin <= 0:
            stages["simulated_nonpositive_margin"] += 1
            continue
        stages["simulated_positive_margin"] += 1
        tx_hash = item.get("transaction_hash")
        if not isinstance(tx_hash, str) or len(tx_hash) != 66 or not tx_hash.startswith("0x"):
            tx_hash = None
        # No independent receipt check; never describe these as realized gains.
        candidates.append({
            "vault_id": item["vault_id"][:120],
            "chain": chain,
            "strategy": item["strategy_address"].lower()[:42],
            "report_time_utc": stamp.isoformat(),
            "operator_reported_harvested": item.get("summary_harvested") is True,
            "operator_reported_tx_success": item.get("transaction_ok") is True,
            "operator_tx_hash_unverified": tx_hash,
            "estimated_call_reward_api_wei_approx": str(call_reward),
            "estimated_gas_cost_api_wei_approx": str(gas_cost),
            "estimated_gas_margin_api_wei_approx": str(margin),
            "operator_estimated_gain_api_wei_approx": str(estimated_gain) if estimated_gain is not None else None,
            "fee_asset_price_verified": False,
            "actual_caller_payout_verified": False,
            "currently_available": False,
        })
    candidates.sort(
        key=lambda v: (Decimal(v["estimated_gas_margin_api_wei_approx"]), v["vault_id"]),
        reverse=True,
    )
    return {
        "source": SOURCE, "report_type": "LATEST_PER_VAULT_NOT_HISTORICAL_CENSUS",
        "observed_at_utc": now.isoformat(),
        "lookback_hours": hours,
        "chains_checked": sorted(chosen),
        "total_api_rows": len(records),
        "recent_rows_selected_chains": all_recent,
        "recent_rows_by_chain": dict(chain_counts),
        "invalid_rows": invalid_rows,
        "evidence_funnel": dict(stages),
        "evidence_funnel_comment": "Values count recent latest-per-vault snapshots, not independent successful transactions. Missing fields and incomplete simulations must NEVER be treated as zero profitability.",
        "estimated_positive_margin_rows": len(candidates),
        "top_estimated_positive_margin_reports": candidates[:top],
        "report_truncated_to_top": len(candidates)>top,
        "transactions_sent": 0,
        "profit_usd_verified": False,
        "warning": "Cowllector v2 LAST per-vault report (not all transactions); upstream wei are JS numbers with potential precision loss. Profitability figures are operator simulation estimates, NOT verified net receipts; fee token may not equal gas token and reported amounts may refer to prior blocks. No unclaimed reward confirmed."
    }


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--hours", type=int, default=72)
    p.add_argument("--chains", default="base,arbitrum,optimism")
    p.add_argument("--top", type=int, default=20)
    p.add_argument("--output", default="beefy_cowllector.json")
    args=p.parse_args(argv)
    try:
        chosen = [x.strip() for x in args.chains.lower().split(",")]
        if len(set(chosen)) != len(chosen):
            raise ValueError("Duplicate requested chains")
        # validate all options before remote fetch
        if not set(chosen).issubset(ALLOWED_CHAINS):
            raise ValueError("Invalid chain name")
        if not (1 <= args.hours <= 720 and 1 <= args.top <= 100):
            raise ValueError("Invalid hours or top")
        reports=fetch_reports()
        out=summarize(reports,datetime.now(timezone.utc),args.hours,chosen,args.top)
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print("BEEFY COWLLECTOR READ FAILED:",type(exc).__name__,str(exc)[:120],file=sys.stderr)
        return 2
    Path(args.output).write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("Latest per-vault rows:",out["total_api_rows"],"recent:",out["recent_rows_selected_chains"])
    print("Estimated positive margins:",out["estimated_positive_margin_rows"])
    print("RESEARCH ONLY; no caller reward receipts verified. Output:",args.output)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
