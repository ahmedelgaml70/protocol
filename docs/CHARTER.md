# Project charter

**Name:** Protocol / Permissionless Bounty Radar
**Created:** 2026-10-11
**Capital:** $10 available in principle; **$0 allocated or spent by this project**.
**Target:** $1,000 total (100× gross target from $10), rapidly if legitimate opportunities exist.
**Reality check:** This is an aspirational target. No credible evidence supports reliable or guaranteed 100× returns on demand.

## What counts
Legitimate, documented permissionless actions where a blockchain contract rewards any qualified external caller: liquidation initiation, expired-stream closure, vault harvesting, range-order filling, or other keeper functions. Potentially use small fee funds for operations whose principal is supplied by the protocol or a flash loan, **but flash loans still require correct atomic execution and gas**.

## What does not count
Jobs, freelancing/tasks, waiting for a client, promoting or discounting products, paid acquisition, referrals, speculative token trading, unsafe 'glitches', theft, exploits, market manipulation, or promises of quick guaranteed money. No deposit solely to qualify for rewards.

## Success ladder
- L0: Documented reward mechanism.
- L1: Proven real historical on-chain payouts; exact chain/token/amount.
- L2: Open eligible opportunity at a known block (not hypothetical).
- L3: Independent executable simulation, permitted caller, full costs and exit liquidity quantified.
- L4: Small live execution **only after explicit approval**.
- L5: Actual realized proceeds, verifiable transaction hashes and accurate budget accounting.
Only L5 is profit. Never collapse L0–L4 into 'earned money'.

## Accounting rules
Profit = realizable value of reward - gas - bid/priority fees - protocol/flash-loan fees - swaps/slippage - bridge/withdrawal costs - loss from failed attempts - any other attributable expense.
Keep reward token units and USD figures separate. Prefer realized rather than oracle valuations; timestamp quotes. Track adverse outcomes.

## Guardrails
- Never commit wallet credentials, addresses belonging to the user, account numbers or payment details.
- Research uses read-only RPC by default, no signing path.
- GitHub is public; PRs/code must be checked for secrets.
- No autonomous payments or execution.
