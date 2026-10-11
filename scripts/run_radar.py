#!/usr/bin/env python3
"""Run documented research-only scanners, retaining explicit failures as failures."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CHECKS = (
    ("pooltogether-base", "pooltogether_claim_history.json",
     ["pooltogether_claim_history.py", "--rpc", "https://base-rpc.publicnode.com", "--lookback-hours", "6",
      "--chunk", "1000", "--max-sample-receipts", "10"], 240),
    ("superfluid-base", "superfluid_activity.json",
     ["superfluid_activity.py", "--network", "base-mainnet",
      "--days", "3", "--limit", "300"], 90),
)

def utc_now():
    return datetime.now(timezone.utc).isoformat()

def scan(name, filename, command, timeout, output_dir):
    outfile = output_dir / filename
    outfile.unlink(missing_ok=True)
    entry = {"scanner": name, "report_file": filename, "started_at_utc": utc_now(),
             "status": "incomplete", "exit_code": None}
    try:
        result = subprocess.run([sys.executable, *command, "--output", str(outfile)],
                                cwd=ROOT, capture_output=True, text=True,
                                timeout=timeout, check=False)
        entry["exit_code"] = result.returncode
        if result.returncode == 0 and outfile.is_file():
            try:
                with outfile.open(encoding="utf-8") as f:
                    report = json.load(f)
                if not isinstance(report, dict):
                    raise ValueError("report must be a JSON object")
                entry["status"] = "ok"
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                entry["error"] = "invalid output: " + type(exc).__name__
                outfile.unlink(missing_ok=True)
        else:
            entry["error"] = "scanner exit code: " + str(result.returncode)
        entry["stdout_tail"] = result.stdout[-500:]
        entry["stderr_tail"] = result.stderr[-500:]
    except subprocess.TimeoutExpired:
        entry["status"] = "timeout"
        entry["error"] = f"timed out after {timeout} seconds"
        outfile.unlink(missing_ok=True)
    except OSError as exc:
        entry["error"] = type(exc).__name__
        outfile.unlink(missing_ok=True)
    entry["finished_at_utc"] = utc_now()
    return entry

def build_manifest(output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    entries = [scan(n, f, cmd, timeout, output_dir) for n, f, cmd, timeout in CHECKS]
    return {"schema_version": 1, "generated_at_utc": utc_now(),
            "purpose": "READ_ONLY_RESEARCH",
            "checks": entries,
            "not_implemented": ["ripe-live-payout"],
            "transactions_sent": 0, "funds_spent_usd": 0,
            "warning": "Inactivity and scanner errors are different. No live eligibility or profits are established."}

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", default="reports")
    args = p.parse_args(argv)
    out = Path(args.output_dir).resolve()
    if out == ROOT or out == Path("/") or not str(out).startswith(str(ROOT) + "/"):
        p.error("output directory must be a subdirectory of the repository")
    manifest = build_manifest(out)
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    for item in manifest["checks"]:
        print(item["scanner"], item["status"], item.get("error", ""))
    print("READ ONLY; manifest and reports stored in", out)
    return 0  # A failed network read is explicitly incomplete, never "zero rewards".

if __name__ == "__main__":
    raise SystemExit(main())
