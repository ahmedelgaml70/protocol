# Candidate evaluation / go–no-go

## Evidence schema (each observation)
- Protocol and contract + code hash + chain ID
- Observed UTC timestamp + pinned block number/hash
- Exact public action and caller authorization
- Live eligibility read from deployed contract
- Reward amount **in raw token units**, token contract, decimals
- Price source, age and method (do not substitute ticker symbols)
- Exit route, on-chain liquidity, slippage assumptions
- Estimated gas and max fee; private ordering/bidding assumptions
- Failure and frontrunning scenarios; keeper priority
- Input capital/allowances/flash-loan amounts
- Net value: conservative/central/adverse cases
- Simulation RPC, block tag, revert reason; evidence link
- Repro instructions + full uncertainties

## Conservative screening
Expected net in USD = reward realistically sold - (network gas + priority tips + flash costs + swap/bridge/withdrawal costs + expected failed-call losses + other outlays).
Claimable is not the same as fillable: other keepers can preempt it.
Unknown payout token value → **UNPRICED**. No successful estimate or trace → **NOT_SIMULATED**. Weak permission proof → **DO_NOT_EXECUTE**.

## Budget check
The available budget is $10. Do not even submit a potentially reverting transaction if the worst-case gas loss would exceed user-approved risk capital. Any action with non-refundable approval/bridge fees must be separately itemized.

## Decision categories
- **RESEARCH**: supported contract/document mechanism, no proven opportunity.
- **OBSERVED**: qualifying open on-chain state at a pinned block, but not profitable or not simulated.
- **WATCH**: potentially positive estimates but incomplete costs / competitive uncertainty.
- **REJECT**: negative estimate, no trusted exit, exploit/security issues or unaffordable costs.
- **READY_FOR_USER_REVIEW**: full evidence package and proven authorized simulation; still cannot execute without specific approval.

Never use 'guaranteed', 'risk-free', or 'execution-ready' for a contract merely because `fillable()` returns true.
