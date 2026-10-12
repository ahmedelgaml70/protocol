# Research playbook — evidence before implementation
**Current user-approved objective:** investigate lawful payment opportunities worldwide using **at most $100**, aiming for **$1,000 net-withdrawable total by 2026-11-12**. This is not a guarantee and does not authorize transactions, account creation or submission.

## The new strategy: start with real cash, work backward

Previously the project started from a technically fascinating protocol and built read-only bot code, then discovered there were no active orders, all payouts already taken, or keeper competition too intense. **Invert the sequence**:

1. **Identify a distinct payer and already-funded payment pathway.** Examples: a job's token credits locked in a published contract; an approved invoiceable bounty issued by a verified organization; a platform with actual approved task supply. A headline programme award, DEX TVL or marketing claim is not funding evidence.
2. **Determine exactly why they pay:** a specific unfinished contractual task, an objective deliverable, a time-gated service, real unused business capacity, or a publicly callable maintenance action. A theoretical "public good" is not a payout mechanism.
3. **Prove the proposed claimant can participate.** Does the task permit an arbitrary new wallet or account? Does it require a bond, deposit, private authorization, programming proof, KYC, residency, a buyer or collateral? Is the action still open and not already assigned?
4. **Look for recent actual settlement.** Confirm payee, reward denomination, clearing date, receipt/bank/payment rail; distinguish on-chain `Payment` event from transferable tokens delivered to a wallet, and from token market valuation. For bounties, actual merged PR plus sponsor-paid settlement is stronger than an issue label.
5. **Test a particular current action at a timestamp** (read-only contract simulation, exact open issue with unassigned state, accepted task inventory, confirmed offer). Record expiration and competitor pressure.
6. **Calculate the entire economic path:** reward × expected successful tasks − transaction fees − source/hosting costs − failed attempts − conversion/slippage − taxes/refunds − capital lock. Determine first-to-final-cleared-payment delay. Project $900 net only from demonstrated task/reward capacity, not APY or extrapolated one unusual receipt.
7. **Only with explicit user approval**, carry out a limited, real action (registration, PR, application, signature, spending). Verify cleared funds before scaling. No unattended financial execution.

## Mandatory gate table

| Gate | Required proof | Fail outcome |
|---|---|---|
| G0: funded | Public escrow/payment transactions, verified sponsor spend, platform cash settlements; payer distinct | UNKNOWN / REJECT |
| G1: legitimate access | Official rules permit user/newcomer; check country, wallet, KYC, bond, role and availability | REJECT if truly prohibited |
| G2: real payer track record | Recent real payment or independent sponsor financial confirmation; not points/reputation only | RESEARCH ONLY |
| G3: currently open work | Exact unclaimed action/task and clock/chain timestamp, not historical event | RESEARCH ONLY |
| G4: attributable positive net | Fees, slippage, failures and conversion covered at conservative fair price | REJECT if expected negative |
| G5: 30-day scale | Plausible inventory + quality/throughput + actual cash settlement by Nov 12 | DEPRIORITIZE if 1-off pennies |
| G6: explicit approval | User expressly authorized *specific* spending, external PR, signing, account registration, outreach or other external change | STOP before execution |
| G7: actual settlement | Money really reaches user's authorized, withdrawable account; proof without private account data | Only this is earned income |

**No candidate currently clears G0–G5.** On-chain Keep3r clears G0 and G2 historically, but G3 fails in the 19 checked strategies, G1 not confirmed, G4/G5 unfavorable.

## Scoring in discovery phase (0–100), not a profit probability

Score only after G0 evidence:
- Verified actual funded payout history (0–25)
- Newcomer access and no specialist credentials/collateral (0–20)
- Specific currently open payment or task (0–20)
- Profit after full costs and cashable asset (0–15)
- Competition and realistic completion under constraints (0–10)
- Credible repeatable throughput within 30 days (0–10).

Reject early if under 60 or mandatory hard exclusion breached. >80 means worth deeper review, **not** READY. Payout receipt quality outranks sponsor headline.

## Fast discovery lanes, deliberately independent

- **Contract callers:** permissionless liquidation/claim/settle/rebalance, distributed chain networks, protocol-paid third parties. Seek recent exact payout transfers FIRST; use chain explorer or official verified subgraph/contract; if no live work stop.
- **Pre-funded public digital tasks:** backed issues/sponsor funds on GitHub, community maintenance incentives, fixed deliverables. Verify current open issue, no insider assignment, actual escrow and *historical paid merges*. Don't waste time on synthetic label spam, future funding promises, security exploits or contests.
- **Platform-assigned work (constraint exception only):** official paid tests, transcription/QA with approved tasks and first cash payout. Confirm no cold-client chase and no calls if disallowed. This is WORK, not passive mechanism; disclose that difference.
- **Niche data/licensing/API rewards:** platform automatically pays publishers/operators based on actual buyer usage. Verify active buyers and volume before producing content; user disfavours waiting for customers.
- **Economically backed edge cases:** legally claimable and consented fees/rebates/refunds if already owned; not someone else's recoverable funds. No hypothetical unearned cash.
- **Cross-language/cross-network unserved supply:** search diverse jurisdictions where settlement and regulations permit. Candidate must still pass G0–G5.

## Source hierarchy and cross-check
1. Deployed code/address, real settlement transaction/receipts, payment processor’s official records, sponsor official rules.
2. Independent verified third-party transaction explorers, financial statements, dated repository releases and operator postmortems.
3. Community experience (Reddit/other discussion): use as a hypothesis/risk signal, **not** proof of payment or sufficient demand.
4. Promotional claims, agent-written bounty postings, reported yields, anonymous screenshots, rumors: NOT verified.

For every fresh claim record `as_of_utc`, URL, publication date vs actual event date, chain/block if applicable, asset decimals, payment beneficiary and status. Watch for testnet/mainnet mix-ups, deprecated code versions, source-vs-bytecode drift, expired bounty deadlines, self-payments, fake TVL and tokens without volume.

## Branch, code and data policy

- **Main:** `AGENTS.md` + current canonical docs are research direction. Historic `README.md` / `docs/CHARTER.md` retain prior $10 wording for provenance, marked superseded. Primary old evidence is in `evidence/`.
- **Draft code:** PR [#8 0xSplits](https://github.com/ahmedelgaml70/protocol/pull/8), [#9 Liquity/Sovryn](https://github.com/ahmedelgaml70/protocol/pull/9), [#10 Keep3r](https://github.com/ahmedelgaml70/protocol/pull/10). Do not merge or execute without explicit approval; no need to rebuild their scanners.
- **New candidate experiment:** minimal new branch from main, no secrets or personal wallets, read-only operations, offline tests, manual CI, bounded rate limits, compressed sanitized JSON with evidence dates; only create a PR when substantive.
- **Github Actions:** do not reinstate original paused cron; scheduled jobs are unsuitable for speed races anyway. Manual tests and small public read-only scans preferred. Do not pay for new RPC/API service.
- **Data labeling:** `confirmed`, `historical`, `sampled_negative`, `partial`, `unverified`, `rejected`; use `partial` not zero for RPC failures. Report all limits and caveats.
- No private keys, API tokens, user wallet/address, account IDs, payment handles, government IDs, secret URLs, or customer data in public repo. No finance, wallet, signup, proposal submission or deployment without permission.

## Candidate record template

Copy and fill the following when a prospect survives primary source checking:

```yaml
id: 2026-10-12-NNN
name: "..."
date_seen_utc: "..."
category: "permissionless_contract|funded_public_task|platform_assigned|usage_royalty|other"
status: "lead|research|watch|stop|ready"
user_constraints_exception: false
sponsor_and_current_official_source: "https://..."
external_source_and_date: "https://..."
payout_proof:
  escrow_or_funding: "URL / chain / block / direct payment proof / unresolved"
  historical_payment: "URL / tx id / verified recipient / none"
  exact_current_task: "URL / block and expiring condition / unverified"
reward:
  asset: "..."
  gross_amount: null
  cashable_amount_usd: null
  withdrawal_method: "..."
  withdrawal_timing_days: null
requirements:
  new_user_eligible: null
  egypt_supported: null
  bond_usd: null
  skill_or_task_burden: "..."
  competing_claims: null
costs:
  gas_or_work_cost_usd: null
  fees_usd: null
  failed_attempt_or_approval_risk: "..."
projected_30day_net_usd: null  # never fill from conjecture
verdict_reason: "..."
next_falsification_test: "..."
user_permission_required_before_action: true
```

## Reporting after every meaningful iteration

Update [OPPORTUNITY_MATRIX_2026-10-12.md](OPPORTUNITY_MATRIX_2026-10-12.md) (or create a new dated extension) with changes and links; add short dated entry to [HANDOFF_2026-10-12.md](HANDOFF_2026-10-12.md) if status/protocol approach materially changes; correct stale top-line metrics in root README and AGENTS. Prove one current available positive-net payout before spending more than a small number of tool calls on implementation.

**User-facing status should always include:** investigated source families, actual surviving candidates, precise blocker for each, $spent, $actually earned, next smallest decisive test. Report no verified paid candidate plainly instead of generating filler recommendations.
