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
