# New project direction (2026-10-12)

**Read [docs/INCOME_PIVOT_2026_10_12.md](docs/INCOME_PIVOT_2026_10_12.md) before pursuing further leads.** The historical on-chain keeper mission below is superseded for active research, not erased. User's constraints: $10 maximum initial cash exposure, online/computer-based, worldwide but from Egypt, no clients/cold outreach, no call-based jobs, no AI training or security bounties, no referral/affiliate campaigns, no contests, no speculative trades, no signing or wallet transactions, no account/profile changes without explicit user approval. The user also ruled out routine freelance job hunting; platform-assigned compensated work should be labeled **constraint exception**, not a direct fit.

**Current protocol-radar cron is intentionally paused.** It remains manually runnable. Do not restore scheduled runs or write financial alerts based on phantom opportunities without new evidence and permission.

**Priority:** show a real, open route with eligibility from Egypt, payout rail/time, access to current work/buyers, reward after fees, and likelihood of reaching money within seven days. Do not build another automation for unverified supply/demand. $1,000 in seven days remains an aspirational target, not a guarantee. Explicit user approval required before spending, registering an account, listing products or applying to platforms.

---

# Operating instructions for AI agents and human collaborators

## Mission
Find legitimate, permissionless, on-chain actions that pay an external caller. Work toward the user's aspirational $10 → $1,000 goal without clients, service work, promotion, airdrop guessing, gambling, or requiring substantial upfront capital.

## Non-negotiable rules
1. **Evidence before claims.** Distinguish protocol-documentation facts, observed blockchain events, inferred possibilities, and executed net profits. Never fabricate an open bounty.
2. **Read-only by default.** No private keys, wallet connections, signed transactions, transfers, approvals, funded infrastructure, or contracts deployed without explicit transaction-specific user approval.
3. **Never put credentials or identifying wallet/account data in the public repository.** Use environment variables for RPC URLs; never log URLs with API keys.
4. **Budget: $10 total risk capital.** No opportunity is approved just because the headline bonus is large. Exclude all input costs, fee costs, token exit/market impact, failed-call risk and capital locking first.
5. **Audit deployed contracts.** Published GitHub source is not proof it matches the deployment. Check chain ID, code, protocol status, upgradeability and contract address.
6. **Stay legitimate.** No exploitation of security vulnerabilities, stolen funds, oracle manipulation, unauthorized transactions, or terms violations. Only documented, contract-authorized public actions.
7. **Confront competition.** A fillable view at one block does not reserve the transaction. Account for keeper priority rules, gas auctions, private order flow, transaction ordering and reverted transaction fees.
8. **Fail closed.** Unknown price or gas means NOT_VERIFIED, never 'execution ready'. If RPC is unavailable, output an error—not zero opportunities.
9. **Keep provenance.** Save block number, chain, address, RPC method, URL/source, observation timestamp and version for reproducibility. Never commit generated data with personal info.
10. **Maintain a decision log.** Each rejected approach must record the blocker so research doesn't circle back without new evidence.
11. **No guarantees.** 100× quickly is not an expected outcome. A successful observation test doesn't imply financial success.
12. **Prefer small, verifiable experiments.** Work across many protocols and choose based on expected net value, evidence, and competition—not hype.

## Default research loop
Discover candidate → verify primary source/deployed address → inspect historical payout events → observe open opportunities → check executor permissions → estimate conservative net amount → check fill/call simulation → produce evidence-backed recommendation. Never auto-execute.

## What to update after each session
- `docs/RESEARCH_LEDGER.md`: sourced facts and rejected hypotheses;
- `docs/STATUS.md`: current blockers, next action and actual measured results;
- tests if any parser or calculation changes;
- `docs/ROADMAP.md` when process changes.

## Explicit permission policy
The user authorizes commits of the requested repository project. This does **not** constitute approval to transfer crypto, expose secrets, purchase services, enable unattended financial execution, or spend funds. Ask before any such action.

## Learned failure — unused contract

The first user-supplied live scan of Kerf RangeOrders showed `nextOrderId=1` (contract's initial ID), zero orders and no errors. Do not create another full bot just because documentation mentions a caller bounty. **Gate 0: find a recent successful on-chain payout first.** Evidence: `evidence/kerf-rangeorders-4663-block-86104491.json`. User-provided reports are labeled as such, not represented as independently reproduced.

## Learned lesson — read event types and deduplicate by transaction

The October 11 Superfluid subgraph returns **300 liquidation events but only 270 unique tx hashes**. Some transactions batch multiple stream liquidations. Period codes are 0 Patrician, 1 Pleb, 2 Pirate. Patrician reward receiver is priority-designated; 1/2 have permissionless rewards but recorded historical events are already collected. Do **not** treat the Batch Liquidator intermediate address as an actual distinct bot, or price arbitrary raw token amounts as USD. Match `tx.from` to actual ERC20 `Transfer` recipients, calculate Base L1+L2 gas, and deduplicate. Count attempts that fail in any realistic profitability model.

## New stop rule (Superfluid audit, October 12)
A high event count does not imply a valuable/public reward pool. Superfluid Base activity yielded priority-locked USDCx payouts and ETHx rewards concentrated in one successful keeper. Six of 12 **successful** selected ETHx calls were economically negative versus gas under parity. Do NOT automate live liquidation on the user's budget until we verify a current eligibility window, realistic competitive fill probability, and conservative expected net that accounts for failed calls. Document decisions before adding bots. Original user receipts and full report must remain in `evidence/`.

## Source-version trap
Do not assume same-named event across old repositories uses same ABI. Legacy PoolTogether/v5-prize-pool defines ClaimedPrize with uint16 drawId whereas the newer docs-pinned GenerationSoftware/pt-v5-prize-pool defines uint24 drawId, changing topic0. Only count current deployed contract reward and validated recipient; never call aggregate protocol fee revenue keeper income.

## Automated GitHub Actions safety policy
Actions only run public read-only research scripts. PR workflows get read-only contents permission, and only the post-radar workflow has issues:write. The alert stage consumes untrusted workflow artifacts as **data only** and must never execute downloaded code. Alerts mean historical research evidence, not current executable opportunity or profit; wallet execution must remain separately and explicitly user-approved. Ripe integration is not yet implemented. See docs/GITHUB_ACTIONS.md.

## Beefy automation guard

Beefy's v2 Cowllector API last-harvest-reports are ONLY the incumbent operator's most recent report per vault; simulated call reward and gas estimates are not third-party net profit. Amounts are JS JSON numbers and might not be exact wei. Never open execution-ready alerts from these, nor submit/simulate actual transactions that spend gas without explicit authorization. Require independent success receipt, true reward transfer to tx sender, token exit liquidity and current permissionless eligibility before grading opportunity.

## Morpho PnL data integrity (October 12)
Official GraphQL `Liquidation` event count differs from unique tx count (100 events / 37 txs); uniquely identify logs using txHash + marketId + logIndex. Receipt-level `Liquidate.caller` may represent a contract and differ from submitting `tx.from`. Never price or subtract `seizedAssets` from `repaidAssets` directly without each market's correct token, decimals, credible exit liquidity and swap fees. A successful historical liquidation is already taken. Synthetic 70-test suite passed. No auto flash loan, liquidation, signing, spending or wallet secrets.

## Morpho reference-price false-positive rule
NEVER label `indicative_current_reference_valuation.gross_current_reference_spread_usd` as realized PnL or accessible profit. It reprices historical collateral/repaid token raw quantities at current API priceUsd, without executable sale, flash loan, DEX gas, fees, slippage or failures. Even $64K summed across capped events is not a user's opportunity. Require whole transaction cashflow plus live eligible target and conservative net before considering execution; no auto trade/wallet.
