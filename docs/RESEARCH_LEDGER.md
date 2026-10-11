# Research ledger — what we have and have not proved

As of 2026-10-11. **The following are candidate mechanisms, not verified profitable current opportunities.** Source links are for independently re-checking contract versions, claims and economics.

| Candidate | Documented mechanism | Why it might be interesting | Important blocker | Current status |
|---|---|---|---|---|
| Superfluid Sentinel | Network supports liquidation/closure of failing payment streams and keeper operation; protocol has different priority/reward phases | Certain permissions can be open to public callers without repaying an entire loan | Priority designated operator; no measured open rewards, access and concentration not yet verified | L0 research |
| Kerf RangeOrders (Robinhood Chain) | Published contract claims a caller bounty when an eligible range order is filled (1% of converted principal in candidate code) | Public `nextOrderId`, `orders`, `fillable` let us examine actual state | Unaudited beta, own keeper competition, USD liquidity unknown, no observed live fillable order | L0 implementation; awaiting real RPC |
| Liquity V2 | Published liquidation gas compensation plus variable collateral compensation in qualifying circumstances | Initiator can sometimes call without funding full borrower debt | Depends on collateral/stability pool and liquidation frequency; previous research found weak activity | L0 research |
| Morpho Blue | Permissionless liquidation incentives and developer bot examples | Small/less crowded markets might exist | Borrower debt financing/flash loan/gas, bad debt, MEV | L0 research |
| Aave | Liquidation bonus to third-party debt repayers | Deep activity | Strong established keeper competition and capital/flash liquidity needs | L0 research |
| Beefy Finance | Some permissionless vault harvests pay call incentives | Small calls might reward gas-paying keeper | Existing automated keepers, unknown net economics | L0 research |
| Compound III | Collateral absorption and discounted collateral purchase mechanisms | May be automatable | Model differs from simple liquidation bounty; meaningful capital can be needed | Research only |

## Primary research links
- Superfluid Sentinel source: https://github.com/superfluid-org/superfluid-sentinel
- Superfluid documentation: https://docs.superfluid.org/
- Kerf contracts: https://github.com/KerfFinance/kerf-contracts
- Kerf range-order docs: https://www.kerf.finance/docs/range-orders
- Robinhood Chain connection: https://docs.robinhood.com/chain/connecting/
- Liquity documentation: https://docs.liquity.org/
- Morpho docs: https://docs.morpho.org/
- Morpho bot example: https://github.com/morpho-org/morpho-bots
- Aave docs: https://aave.com/docs/
- Beefy contracts: https://github.com/beefyfinance/beefy-contracts
- Compound docs: https://docs.compound.finance/

## Prior work and caveats
- A standalone Python Kerf observer and event-history script were built locally in the prior session; five offline tests passed there. It did NOT complete a live blockchain scan because the available container environment could not resolve the RPC hostname. Historical profits, fillable orders and execution feasibility were **not** established.
- Research notes previously reported that a Kerf source implementation grants 1% of converted principal to the filler; this is an **unverified deployment claim** until source-to-bytecode match/contract address are checked.
- Superfluid Sentinel was identified as a promising public tool, but a hosted accessible `/nextliquidations` feed was **not** established.
- No current bounty, on-chain proceeds, or verified 100× path has been discovered.
- Public protocol dashboards or formula examples are not evidence of our individual earnings. Re-check docs and deployments before acting.

## Research questions still open
1. Do Kerf current live orders exist, and have there been `Filled` transactions recently?
2. What reward token(s), verified decimals, exchange depth and realistic exit routes?
3. How many fills go to the official keeper, and at what time-to-fill?
4. Does Superfluid have actual unclosed Pleb/Pirate-phase streams on low-cost chains?
5. Do any reputable neglected keeper mechanisms consistently offer positive net rewards after realistic competition?

## Added source review — 2026-10-11

Verified **published source semantics** in KerfFinance/kerf-contracts; no live payout events independently observed in this tool session:

| Contract | Exposed public action | Fee/reward formula in source | Critical qualification |
|---|---|---|---|
| `PositionKeeper.sol` | `harvest(uint256 tokenId)` | position policy `bountyBps` capped at 300 bps (3%) of fees collected | Position must be enrolled; interval elapsed, fees accrued; `shouldHarvest(uint256)` provided. Bounty may be zero. |
| `LPVault.sol` (and derived seed vaults) | `harvest()` | `HARVEST_BOUNTY_BPS = 50` (0.5% of collected fees) | No guaranteed fee amount; position and minimum interval required; no general `shouldHarvest()` method in source. |
| `PreMarketPerp.sol` | `liquidate(uint256 id)` | `LIQ_BOUNTY_BPS = 100` (1% of remaining positive margin) | Only undercollateralized open positions; margin can be zero or negative; reward capped by contract's available payout funds. |
| `RangeOrders.sol` | `fill(uint256)` | `KEEPER_BOUNTY_BPS = 100` (1% of converted output) | Requires fully crossed range; caller competition and settlement costs. |

`kerf_multi_history.py` parses `Harvest`, `Harvested`, and `Liquidated` events from the claimed six deployed seed vaults, PositionKeeper and PreMarketPerp. Source deployment manifest: https://github.com/KerfFinance/kerf-contracts/blob/main/deployments/robinhood.json . This provides *historical activity evidence* only and is incomplete for vaults created later through VaultFactory.

Sources: [LPVault.sol](https://github.com/KerfFinance/kerf-contracts/blob/main/src/LPVault.sol), [PositionKeeper.sol](https://github.com/KerfFinance/kerf-contracts/blob/main/src/PositionKeeper.sol), [PreMarketPerp.sol](https://github.com/KerfFinance/kerf-contracts/blob/main/src/PreMarketPerp.sol), [RangeOrders.sol](https://github.com/KerfFinance/kerf-contracts/blob/main/src/RangeOrders.sol).

**Verification limits:** Direct explorer address/API requests were not accessible in the available browsing environment and direct RPC DNS was previously unavailable locally. The publicly published deployment manifest has not been verified against deployed bytecode. Do not extrapolate profitability or claim real payouts.

Blockscout reports Robinhood Chain public explorer and a free PRO API key tier; see https://github.com/blockscout/docs/blob/main/robinhood-api.mdx and https://www.blog.blockscout.com/build-on-robinhood-chain-with-the-blockscout-pro-api/ .
