# 0xSplits cross-chain reward discovery — evidence gate (2026-10-12)

**Budget:** $100 proposed ceiling, **$0 spent**. Target: $1,000 withdrawable by 2026-11-12 (aspirational, not forecast).

## Branch and run references

Research branch: `research/splits-100`, PR #8 (draft). No main-branch merge, private keys, signing, gas expenditure, or automatic transactions.

- First completed three-chain factory sample: https://github.com/ahmedelgaml70/protocol/actions/runs/38248613755
- Added pre-existing-contract distribution activity: https://github.com/ahmedelgaml70/protocol/actions/runs/38249195371
- Scan logic: `research/splits/splits_expanded.py`, `research/splits/splits_activity.py`.
- Workflow: `.github/workflows/splits-expanded.yml`.
- Safety/ABI tests: **15/15 passed** in the second run.

## First completed factory-creation sampling results

Factory generations: PushSplit V2, V2o1, V2o2; networks: Base, Optimism, Arbitrum; tracked balances: official native USDC, WETH and network native coin. Historical windows are **four non-contiguous 1,600-block samples** anchored at 0, 7, 30 and 90 days prior to run, not a full historical index.

| Chain | Sampled factory creation events | Positive caller reward screens | Completeness |
| --- | ---: | ---: | --- |
| Base | 0 | 0 | Partial: free provider pruned old blocks / other RPCs throttled |
| Optimism | 0 | 0 | Partial in first run |
| Arbitrum | 0 | 0 | Completed bounded sampled scan via public Arbitrum RPC |

A zero finding means only zero events in **successfully scanned sampled windows**, not that all older deployed Splits have no balances or incentives.

## Previously deployed Split distribution activity (second run)

Instead of relying on factory creation alone, `splits_activity.py` scans factory-associated PushSplit `SplitDistributed` event topics in the same bounded windows and, when found, inspects read-only transaction receipts for direct ERC-20 transfers from the split wallet to a named distributor.

| Chain | Verified PushSplit distribution transactions in completed sampled windows | Status |
| --- | ---: | --- |
| Base | Not determined | All activity windows failed via accessible free RPC providers; **incomplete**, not zero |
| Optimism | 0 | Successfully sampled using official Optimism public RPC |
| Arbitrum | 0 | Successfully sampled using official Arbitrum public RPC |

**No verified positive-net payout was found.** These results do not prove the protocol never pays. In particular, events from other non-contiguous windows or older factories/versions and non-ERC20 native transfers may be missed. Historical distributions would already be completed, not an available new opportunity.

## Data-access and safety limitations

- `eth_getLogs` across all contract addresses may be rate-limited or rejected by keyless RPC providers.
- Reading the live `splitHash()` guards against blindly accepting old creation parameters as a current incentive.
- A successful `eth_call` is not a guaranteed mined transaction, and `eth_estimateGas` may omit L1 fees.
- Direct token transfers to a distributor could be ordinary recipient payments rather than caller compensation.
- Official SDK has a GraphQL client requiring a Bearer API key; the old published subgraph repository is deprecated. No credential, paid data plan or full index was acquired.
- No execution code, seed phrase, private key or broadcast function was added to GitHub.

## Decision

**Deprioritize 0xSplits for the one-month cash target** unless a separately evidenced positive-net, currently funded, realistically executable distribution is first identified. Further expanding random sampling windows on free endpoints is unlikely to be an efficient use of effort. Leave the scan read-only, manually invoked on the research branch, and preserve $100 capital.

Follow-up research should first locate actual *current* funded rewards (not broad historical formulas), a known deployed contract, verified accessible payout assets, and demonstrated net receipt economics. Only after such proof should further automation or deployment be considered.
