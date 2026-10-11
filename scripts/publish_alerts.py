#!/usr/bin/env python3
"""Deduplicated GitHub issue publisher for historical research signals only.

Does not execute any chain action. Treats downloaded workflow JSON as untrusted;
accepts a single allowlisted research signal and preserves manual issue notes.
"""
import argparse
from datetime import datetime, timezone, timedelta
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import urllib.request

KEY = "pooltogether-base-current-claimer-paid-history"
TITLE = "[Protocol Radar] PoolTogether Base rewards — research only"
START = "<!-- protocol-radar:pooltogether-base-paid-history -->"
END = "<!-- /protocol-radar:pooltogether-base-paid-history -->"
FINGERPRINT = re.compile(r"<!-- digest:([0-9a-f]{64}) -->")
REPO_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
TX_PATTERN = re.compile(r"^0x[0-9a-f]{64}$")


def build_managed_section(signal):
    if signal.get("key") != KEY or signal.get("status") != "RESEARCH_ONLY_NOT_EXECUTION_READY":
        raise ValueError("Unknown or unsafe signal type")
    examples = signal.get("examples", [])
    if not isinstance(examples, list) or not (1 <= len(examples) <= 3):
        raise ValueError("Expected one to three validated examples")
    parts, hashes = [], []
    for e in examples:
        h = str(e.get("transaction_hash", "")).lower()
        fee = str(e.get("accrued_reward_tokens", ""))
        if not TX_PATTERN.fullmatch(h) or not re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", fee):
            raise ValueError("Invalid tx or fee")
        parts.append(f"- https://basescan.org/tx/{h} : {fee} prize-token units accrued, not withdrawn")
        hashes.append(h)
    token = str(signal.get("prize_token_address", "")).lower()
    claimer = str(signal.get("claimer", "")).lower()
    if not re.fullmatch(r"0x[0-9a-f]{40}", token) or claimer != "0xcdce635b774de77cdf791647601dba64a75547ba":
        raise ValueError("Unrecognized deployed token or claimer")
    digest = hashlib.sha256((token+"|"+"|".join(sorted(hashes))).encode()).hexdigest()
    block = "\n".join([
        START, f"<!-- digest:{digest} -->",
        "## Historical PoolTogether fee evidence — research only",
        "The read-only Base scanner found completed claims sent to the current published",
        "Claimer with nonzero accrued rewards and successful transaction receipts.",
        "",
        "**This is NOT a currently available bounty, net profit, or an instruction to trade.**",
        "",
        f"Prize-token contract: {token}",
        f"Current Claimer: {claimer}",
        f"Selected claim receipts: {int(signal.get('current_claims_observed',0))}",
        "",
        "### Completed transactions", *parts, "",
        "### Required before financial action",
        "Check deployed code, fee withdrawal rights, token liquidity, current unclaimed prizes,",
        "gas, competition, and simulation. Do not connect a wallet or spend funds.",
        "See Protocol Radar run artifact (retained 7 days).",
        END,
    ])
    return block, digest


def api(method, path, token, repo, payload=None):
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}{path}",
        data=json.dumps(payload).encode() if payload is not None else None,
        method=method,
        headers={"Authorization": "Bearer "+token,
                 "Accept": "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28",
                 "Content-Type": "application/json",
                 "User-Agent": "protocol-radar-research/1.0"},
    )
    with urllib.request.urlopen(req, timeout=20) as res:
        return json.load(res)


def publish(signal, repo, token):
    managed, digest = build_managed_section(signal)
    issues = []
    for page in range(1, 6):
        batch = api("GET", f"/issues?state=open&per_page=100&page={page}", token, repo)
        if not isinstance(batch, list):
            raise ValueError("Invalid API issue list")
        issues.extend(x for x in batch if "pull_request" not in x)
        if len(batch) < 100:
            break
    matches = [issue for issue in issues if START in (issue.get("body") or "")]
    if len(matches) > 1:
        raise ValueError("Ambiguous duplicate radar issues; refusing to alter them")
    if not matches:
        created = api("POST", "/issues", token, repo, {"title": TITLE, "body": managed})
        return "created", created["html_url"]
    current = matches[0]
    body = current.get("body") or ""
    m = FINGERPRINT.search(body)
    if m and m.group(1) == digest:
        return "unchanged", current["html_url"]
    when = datetime.fromisoformat(current["updated_at"].replace("Z", "+00:00"))
    if datetime.now(timezone.utc)-when < timedelta(hours=12):
        return "rate-limited", current["html_url"]
    start = body.index(START)
    end = body.find(END, start)
    if end < 0:
        raise ValueError("Managed issue section is incomplete")
    new_body = body[:start] + managed + body[end+len(END):]  # keep user-added text
    changed = api("PATCH", f"/issues/{current['number']}", token, repo, {"body": new_body})
    return "updated", changed["html_url"]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--signals", default="reports/alerts.json")
    args = parser.parse_args(argv)
    data = json.loads(Path(args.signals).read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or data.get("execution_ready") is not False or data.get("funds_spent_usd") != 0:
        raise ValueError("Invalid research-only alert envelope")
    signals = data.get("signals")
    if not isinstance(signals, list) or len(signals) > 5:
        raise ValueError("Invalid signal array")
    if not signals:
        print("No research signals. No issues written.")
        return 0
    repo, token = os.environ.get("GITHUB_REPOSITORY",""), os.environ.get("GITHUB_TOKEN","")
    if not REPO_PATTERN.fullmatch(repo) or not token:
        raise ValueError("Missing GitHub repository or token")
    for signal in signals:
        result, url = publish(signal, repo, token)
        print(result, url)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError) as exc:
        print("Alert generation failed safely:", type(exc).__name__, file=sys.stderr)
        raise SystemExit(2)
