# Decision memo — 12 October 2026

## Question
Can we legitimately turn a $10 execution budget into $1,000 rapidly by initiating Superfluid Base liquidations?

## Evidence assembled
- October Base Superfluid GraphQL report: capped 300 events, 270 transaction hashes, September 26–October 11, **not** a complete 30-day census.
- 46 indexed ETHx liquidation events across 35 transaction hashes; 0.031339692062159336 ETHx recorded at event level.
- Actual RPC receipts, deliberately *not randomly* sampled: 12/35 ETHx transaction hashes. All 12 succeeded and show gas costs; six transfers exceeded fee at assumed ETHx=ETH, six did not.
- Raw ETHx actually transferred to submitting wallets: 0.030309319221334120 ETHx; network L1+L2 fees: 0.000223981813189343 ETH. Aggregate *conditional* after-gas sum: +0.030085337408144777 ETH-equivalent.
- Five positive calls by one address accumulated +0.029372300769558454 ETH-eq; one other caller +0.000749116379986537; another caller's six audited calls totaled -0.000036079741400214.
- One positive indexed event appears without a matching direct ETHx transfer to the submitting wallet; do not conflate subgraph `rewardAmount` with `tx.from` receipts.
- Public-phase USDCx reward amounts: 0.069260546346828494 USDCx across 19 Pleb events; 127.773801231671400105 USDCx credited during priority Patrician phase (33 events). The latter is **not** open caller bounty.
- 14 SUP indexed events aggregate 923.978211804928731971 tokens, not dollars. Assess price/liquidity before assigning cash value.

## Interpretation
Real publicly callable protocol rewards exist and external bots collect tokens; gas is small compared with two rare ETHx outliers. But the **observed opportunity pool in liquid tokens is limited**, high-value wins cluster in an existing operator, and event data show no presently available unclaimed stream. A tiny successful historic bounty is not a scalable return strategy.

## Decision (execution)
**Do not trade / do not deploy.** This route does not presently meet requirements for an accessible, rapidly repeatable $1,000 return. Keep code and historical evidence, stop adding Base-specific executors. Spend $0; $10 budget stays intact.

## Next hypotheses
1. Target larger fixed *native/stablecoin* public caller incentives on low-fee networks, with **actual recent paid events first**.
2. Consider direct ETH bounty tasks only where deployer, contract, and payouts are verified (not a proposal alone). One March 2026 draft ERC [IExternallyExecutableBounty](https://ethereum-magicians.org/t/draft-erc-externally-executable-bounty-a-standard-interface-for-permissionless-task-automation/28002) claims CREATE2 TaskRegistry deployments on Ethereum/Base/Arbitrum. This is **unverified current adoption or payout activity**: do not build an executor until successful TaskExecuted receipts exist.
3. Check other Superfluid networks only when payout density and independent caller compensation justify work.

## Methodology, provenance, open risks
User-provided read-only receipts: [12 October Base receipts](../evidence/superfluid-base-2026-10-recent-receipts-rpc.json). [Derived exact BigInt arithmetic](../evidence/superfluid-base-2026-10-receipt-analysis.json). [Complete capped event sample](../evidence/superfluid-base-2026-10-11-activity-full.json). No private wallet keys or account data used; the indexed wallet addresses are public transaction participants.

Profit requires realizable sale price, failed attempt data, connection/monitoring cost, and exit fees. Current receipts do **not** establish these or future access.
