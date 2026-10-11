# Candidate triage — evidence first

As of 2026-10-11. This file ranks **research priority**, not expected profit. Treat all web claims as unverified until traceable on-chain activity is confirmed.

| Protocol/operation | Deployment/reward-rule evidence | Independently verified payout activity this turn | Capital/no-client fit | Decision |
|---|---|---|---|---|
| Kerf RangeOrders (Robinhood 4663) | Published source & deployment claim | **No:** user's `nextOrderId=1` at block 86,104,491 means zero created orders under documented monotonic numbering | Good in principle; no activity | **STOP** until new orders appear |
| Kerf PositionKeeper / LPVault / PreMarketPerp | Published source rewards | None established | Gas-only in some scenarios | **HOLD**: require fee/liquidation events before more code |
| Liquity V2 liquidation trigger | Official docs specify fixed 0.0375 WETH plus collateral component | Historical liquidation calls visible at an Etherscan-labeled trove manager, including June 2026; **caller profit not substantiated**, some Feb 2026 calls visibly reverted | Potential if available when needed; gas cost and priority matter | **LOW PRIORITY pending data quality review**: DeFiLlama reports $0 Q3 2026 liquidation gas compensation; recent payout frequency not established |
| Superfluid stream liquidation | Official sentinel / protocol rules | No up-to-date unclaimed reward evidence available in this session | Possible gas-only in eligible phase; priority keeper | **RESEARCH PRIORITY 1 (still speculative)**: demand a fresh paid public-caller receipt before coding; avoid Celo security incident scope |
| Velocity Protocol on Solana | Published keeper docs & program IDs, 2026 audit announcement | On-chain deployment and paid caller events **not independently verified here** | Flat cancel/trigger $0.01 and tiny fill rewards; difficult to reach goal without volume | **LOW PRIORITY**, avoid writing bot on promise alone |
| Atomic Green / Atomic | Public docs assert USDC.e liquidation rewards | External DeFiLlama notes Aug 8, 2026 exploit (~$29,984) and small TVL; no current payout events verified | Unclear | **DEFER** pending provenance, recovery and safety verification |

## Evidence and limitations

**User-provided on-chain scan (not an independent RPC reproduction):** [Kerf report](../evidence/kerf-rangeorders-4663-block-86104491.json). Chain 4663, published RangeOrders address, block 86,104,491, `next_order_id=1`, zero scanned orders, zero errors. `orders_scanned=0` is because the public contract counter was still at its initial value. The scanner's `scan_is_full_history=true` flag here means the numeric order range is exhausted; it does **not** prove independently that deployed bytecode matches the published source.

**Liquidity and reward requirements:** A candidate must first show a real historical paid event with transaction hash, payer/recipient, units, token address and transfer receipt; next, an eligible current state at a pinned block; last, an executable simulation and realistic *net* economics. No current contender passes all gates.

Primary/external sources:
- Kerf source and order IDs: https://www.kerf.finance/docs/range-orders
- Liquity V2 reward rules: https://docs.liquity.org/v2-faq/borrowing-and-liquidations
- Etherscan WETH trove manager (historical calls; individual transactions must be checked for success): https://etherscan.io/address/0x7bcb64b2c9206a5b699ed43363f6f98d4776cf5a
- Etherscan explicitly failed example: https://etherscan.io/tx/0x9c06addedd2b7f86a7e69271712c54fb74a0f7a73163f045aa6897ee49a2643c
- Superfluid Sentinel: https://github.com/superfluid-org/superfluid-sentinel
- Velocity rewards: https://docs.velocity.exchange/protocol/how-it-works/keepers/keeper-incentives
- Velocity source/audit announcement (Sep 17, 2026): https://velocity.exchange/blog/velocity-publishes-its-ottersec-audit-and-opens-its-source-code
- Atomic security/TVL independent cross-check: https://defillama.com/protocol/atomic-green

## Avoid false discovery

Anyone can publish a protocol and advertise a bounty formula that nobody has ever received. **Do not spend another programming session on it until there is independent on-chain evidence of use.** Likewise, do not equate 'transaction called' with 'transaction succeeded' or 'keeper earned' without receipt and token movements.

## This round's decision

Stop iterating on an apparently unused RangeOrders contract. Continue read-only research of real protocol payouts on established deployments. Zero user funds spent. $1,000 goal remains aspirational, not demonstrated.

## Further elimination evidence: Liquity V2 Q3 payout metric

DeFiLlama's [Liquity V2 income statement](https://defillama.com/protocol/liquity-v2) reports **$0 gas compensation in Q3 2026**, following roughly $1.13K for Q2 2026 and $8.2K for Q1 2026 in the same table. This is a **reported dashboard metric**, not a complete independent on-chain liquidation census; the data may be incomplete or aggregate differently from individual receiver transfers. Even so, it undermines the assumption that recurring liquidations currently provide an attractive inflow. Do **not** build a dedicated Liquity trigger bot without first checking fresh transaction receipts / recipient WETH transfers.

Example of the danger of counting attempts as income: https://etherscan.io/tx/0x9c06addedd2b7f86a7e69271712c54fb74a0f7a73163f045aa6897ee49a2643c shows **reverted** `NothingToLiquidate()` and a nonrefundable gas fee. The transaction is dated Feb 5, 2026.

**Generalized research priority:** look for *successfully paid* receipts and transfer logs in mature deployments on inexpensive networks, then verify publicly callable interfaces. Reject stale dashboard payouts and theoretical permissionless functions as standalone evidence.

## Superfluid historical paid-caller evidence update (May 2026 transactions reviewed 2026-10-11)

**Gate 0 PASSED historically:** BaseScan records Base Superfluid batch liquidator paying ETHx to the external submitting caller in successful transactions on May 9 and May 10, 2026; see [evidence snapshot](../evidence/superfluid-base-2026-05-samples.json). One illustrative payout yielded +$0.63 vs gas before exit fees under assumed ETHx=ETH; another lost about $0.03. **No proof that non-designated callers can compete profitably now.** This is a *RESEARCH* category, not WATCH/READY. No live 2026-10 event has been authenticated.

## Updated Superfluid assessment (full October user sample)
**Priority: verify just a sample of recent receipt winners, then decide.** 300 events / 270 transactions in truncated ~16 days, but only 46 ETHx events (35 tx) and **0.03134 ETHx indexed rewards in total**. 90.26% arose in just two Oct 8 events. Large raw amounts of arbitrary tokens cannot be considered USD earnings without pricing and liquidity. Confirm successful ERC20 payouts to transaction sender, gas and competition before committing further development. A single indexed liquidator account corresponds to a Batch Liquidator contract; it is **not** evidence of just one bot.

**Asset-quality gate:** 184 token addresses across 300 events, with 180 singleton token addresses. Do not attribute stable/USD value to singleton rewards until contract, DEX liquidity, redemption and spread are verified. The large number of distinct tokens inflates apparent activity relative to easily liquidated earnings opportunities.

## Superfluid Base — October receipt-economics decision

Classification **historically profitable for some existing executors**, **NOT ready for us**. The 12 selected successful ETHx transactions have conditional 1 ETHx=1 ETH after-gas total +0.03008534 ETH-equivalent, almost entirely won by one wallet. Another wallet's 6 sampled successful calls have negative conditional economics. Most USDCx historical reward volume (127.77 of 127.84 USDCx) belongs to the protected priority period. SUP rewards are relatively small in token quantity and require pricing.

**Current missing gates:** no unclaimed stream; no proof that a newcomer can reliably beat entrenched keepers; no failure-attempt dataset; no redeemability-adjusted P&L. Do not risk $10 or build live executor yet.

See [receipt analysis](../evidence/superfluid-base-2026-10-receipt-analysis.json) and [decision](OCT_2026_DECISION.md).

## 2026-10-12 added candidates
PoolTogether V5 Base **#1** for read-only Gate 0 of the **current** claimer; Ripe Protocol Base **#2** pending real keeper payout proof. Deprecated Synthetix Perps Base/Arbitrum, superseded GBLIN contracts, unverified fillr and mostly-zero lolpad fallback bounty are not execution candidates. Details: docs/KEEPER_ALTERNATIVES_2026_10_12.md.

## Automation evidence update (Oct 11 2026)
PoolTogether Base live official prize-claim index, synced within 1 block of chain tip, showed **zero indexed claims in the previous three days**. This is an actual bounded negative observation, not an RPC failure; its present prize token is WETH. Lower near-term claiming research priority until new positive non-deprecated receipts appear. Superfluid had 52 recent liquidation events in three days, but prior P&L study showed low and concentrated rewards; remains observe only. No open claimable target or repeatable positive net found.
