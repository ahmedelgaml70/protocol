# Instructions for any agent continuing the Protocol research project

**CURRENT USER MANDATE OVERRIDE — 2026-10-12:** [Read the $10/no-jobs hard reset](docs/CURRENT_MANDATE_10_NO_JOBS_2026_10_12.md). The latest user message explicitly sets **$10**, not $100, and rejects ALL jobs, paid tasks, client services, promotions, discounts, referral schemes and waiting for customers. Goal: lawful, online, already-funded permissionless rewards as fast as possible, with $1,000 total aspirational; no present income verified, no spending permitted. **Do not suggest Upwork or work-for-hire again.** Earlier $100/Nov 12 documents remain historical research only, not current instructions.

**Canonical current version:** 2026-10-12, supersedes older $10 / one-week directives.

## READ THESE FIRST, IN THIS ORDER
1. **[LATEST MANDATE: $10, NO JOBS, fast legitimate money harvesting](docs/CURRENT_MANDATE_10_NO_JOBS_2026_10_12.md)**
2. [Complete handoff and timeline](docs/HANDOFF_2026-10-12.md)
2. [Opportunity / rejection / evidence matrix](docs/OPPORTUNITY_MATRIX_2026-10-12.md)
3. [Payer-first evidence playbook and candidate schema](docs/RESEARCH_PLAYBOOK.md)
4. [Copyable new-agent continuation prompt](docs/CONTINUE_AS_AGENT.md)
5. [New study: Hyperlane, Archr, TaskMarket and x402](docs/RESEARCH_ROUND2_RELAYER_AGENT_MARKETS_2026_10_12.md)
6. [Latest study: Convex live harvest and kick bounty audit (PR #11)](https://github.com/ahmedelgaml70/protocol/blob/research/convex-earmark-100/docs/CONVEX_KEEPER_KICK_AUDIT_2026_10_12.md)
7. [Newest live funded-task and burn-bounty audit (PR #12)](https://github.com/ahmedelgaml70/protocol/blob/research/prefund-live-gates-100/docs/PREFUNDED_LIVE_GATE_AUDIT_2026_10_12.md)
8. [Booking fulfillment audit: why real customer escrows do not imply payable work](docs/BOOKING_FULFILLMENT_BRIJ_AUDIT_2026_10_12.md)
9. [Live Arc/Mainnet and BaseBounty plus Bountic audit (PR #13)](https://github.com/ahmedelgaml70/protocol/blob/research/arc-base-escrow-100/docs/ARC_BASE_BOUNTIC_AUDIT_2026_10_12.md)
10. [Original user prompts](docs/ORIGINAL_PROMPTS.md) and [historical research log](docs/RESEARCH_LEDGER.md)

**The previous complete version of this AGENTS.md is preserved at [docs/archive/AGENTS_BEFORE_2026_10_12_HANDOFF.md](docs/archive/AGENTS_BEFORE_2026_10_12_HANDOFF.md)**. It remains useful for historic technical failure details but has outdated constraints.

## Mission and hard truth

User goal: **Starting capital up to $100, pursue $1,000 total net-withdrawable proceeds before November 12, 2026**, online and global. Real cash needed above starting funds: $900. **This is aspirational, not an expected 900% monthly ROI.** Last verified result: **$0 spent, $0 user-earned, zero current execution-ready opportunities**. No invented rewards, guaranteed income, promises or theoretical APY projections.

Strong user preferences: no cold clients, sales calls, paid freelancer bids, referral marketing, promotional funnels, AI-training work, security bug bounties/hacks, contests, speculative crypto deposits, or long lockups. Platform-assigned work or coding/documentation bounties are *conditional exceptions*, not automatically approved. Research worldwide; user's Egyptian residence is not a blanket exclusion. Verify actual service country/payment eligibility. Prior supported or available pay routes may include PayPal, Airtm, RedotPay, Binance/Binance Pay and others, but each individual payer's explicit supported method must be checked. Binance Pay is not a substitute for an EVM signing wallet.

## Guardrails — REQUIRED
- Do not submit transactions, sign, connect funded wallets, spend, open user accounts, apply for third-party work, submit outside PRs, send messages, purchase API access, configure subscriptions, or merge research-code branches without **user approval for the specific action**.
- Research, read-only GitHub checks and requested documentation updates are allowed. No wallet keys, user addresses, personal identifiers, payment handles or secrets in this **public repository**. Scrub all JSON artifacts and logs.
- Source-of-truth: `main` for charter, handoff, methodology, outcome ledger, older `evidence/`. Experimental branches **PR #8 (0xSplits)**, **PR #9 (Liquity/Sovryn)**, **PR #10 (Keep3r)**, **PR #11 (Convex)** and **PR #12 (funded live gates)** are draft/unmerged and should not be mistakenly described as merged. Preserve all previous factual evidence and user prompts.
- **No bot before current payout proof.** Find who has escrowed funds, the exact current unclaimed action, recent actual payees, any keeper bond, country rules, deadline and net economics first. Only then build the smallest read-only simulation needed.
- A transaction history or budget balance is not an open income opportunity. `eth_call` success is not a guaranteed winning transaction. A payable formula, treasury TVL, APY, points or future airdrop is not bankable cash.
- Explicitly separate `ZERO_IN_BOUNDED_SUCCESSFUL_SCAN` and `INCOMPLETE_RPC`. Stop if blocked; do not state no opportunity exists system-wide. Timestamp on-chain scans in UTC and include block/address/chain.
- Price assets at independently grounded contemporaneous executable rates and check exit slippage; treat token rewards separately from USDC/DAI/actual settled fiat.
- Research security/legality: no exploits, oracle manipulation, unauthorized claims, third-party refunds, nonconsensual wallet recovery, market manipulation or evasion of KYC.

## Working loop

**Real funded payer → specific publicly eligible action → recent payment/receipt → still open now → full net/settlement by deadline → only then user-approved attempt.** Explore multiple unrelated mechanisms, including non-crypto. Criticize each lead; record why it failed. Favor proving/disproving an opportunity over coding another general-purpose crawler.

Review and update [OPPORTUNITY_MATRIX_2026-10-12.md](docs/OPPORTUNITY_MATRIX_2026-10-12.md) for real new evidence; update [HANDOFF](docs/HANDOFF_2026-10-12.md) for important status/plan changes. Don't duplicate old conclusions as new discoveries. Keep historical detail in the archive. Do not re-enable the paused on-chain scheduled radar or introduce unattended spend.

## The strongest lessons so far

- Kerf RangeOrders counter showed zero orders; building a filler was pointless.
- Superfluid ETHx had some real historic paid keeper calls, but many positive-looking rewards were priority-designated or negative after gas; historical liquidation cannot be reclaimed.
- Beefy incumbents, Morpho MEV competition, and insufficient Ripe/PoolTogether activity defeated advertised incentives.
- 0xSplits scans were narrow; 7-day Liquity and Rootstock historical RPC attempts were incomplete; no universal-negative claims.
- Keep3r's ~19,881 DAI job-credit balance belonged to an already-retired MakerDAOUpkeep; a different active Keep3r job paid 20 historic calls to **two** keepers, and its 19 recently worked strategies all returned **workable=false** at the latest preflight. DO NOT claim large funding ≡ free reward.
- FLOP testnet rewards locked until future mainnet, PERPTools points and Papertrade loss-for-token mechanics cannot substantiate near-term withdrawable dollars.
- Public Github `bounty` labels can be unbacked, expired or synthetic. The Oct 12 candidate `SUSU-LABS/susu-indexer#46` offers $40 for a precise nonsecurity code task but escrow/payout pathway is unproven, and the `NSPG13/agent-bounties#1262` explicitly says unfunded. No approved applicant activity.

At the end of every session report: **time-scoped verified claims**, active/refuted leads, direct source links, capital spent, cash actually received, files/branches updated and smallest next falsification test. Zero income is a valid result; fabricated optimism is not.
