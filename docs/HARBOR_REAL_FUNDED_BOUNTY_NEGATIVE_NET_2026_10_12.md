# New caller-reward mechanisms — Harbor live bounty economics, Solana/Robinhood validation
**Observation:** 2026-10-12 at approximately 17:55 UTC, Ethereum block **26,178,021**. **Latest user objective:** $10 total available capital → aspirational $1,000 as quickly as possible. **NO jobs, clients, task markets, marketing or customer acquisition.** No spend, wallet activity, subscriptions or externally published contracts. This report is a research snapshot; future balances can change.

**Primary live execution:** https://github.com/ahmedelgaml70/protocol/actions/runs/38287408674
**Source and CI:** \`research/harbor/harbor_live.py\` and \`test_harbor_live.py\`, \`.github/workflows/harbor-bounties.yml\` on \`research/harbor-bounties-10\`. Tests: 4/4 passed; live Ethereum chain ID 1 verified; five published deployed managers checked, no transaction signed or broadcast.

## Most important finding: true, funded, executable rewards do exist — but currently lose money

The source code [baofinance/harbor, StabilityPoolManager_v1.sol](https://github.com/baofinance/harbor/blob/main/src/minter/StabilityPoolManager_v1.sol) defines two PUBLIC entry points:
- \`harvest(address bountyReceiver,uint256 minBounty)\`: reads \`MINTER.harvestable()\`, pays \`harvestable × harvestBountyRatio / 1e18\` **in WRAPPED_COLLATERAL_TOKEN directly to bountyReceiver**, distributes rest. Does NOT require caller staked collateral or upfront ownership. \`minBounty\` is a caller-configurable guard, not an upfront payment.
- \`rebalance(address bountyReceiver,uint256 minPeggedLiquidated)\`: liquidity restoration when collateral ratio threshold breached, paying a bounty from wrapped collateral / leveraged output. Requires actual pool pegged balance and successful redemption. A mere true \`rebalanceable()\` is INSUFFICIENT.
- Off-chain [official Harbor docs](https://docs.harborfinance.io/tech-docs/contracts/stability-pool-manager/) describe intended semantics. [Official Ethereum deployed manager/token map](https://github.com/baofinance/harbor-docs/blob/harbor-docs/static/integrators/addresses/mainnet-v1.json) distinguishes live from relaunch-pending markets.

### Complete five-market current state and dry run

All quantities are the wrapped reward token, NOT dollars, and exact when shown. The **fxSAVE** wrapper is the f(x) USD Saving token \`0x7743e50F534a7f9F1791DdE7dCD89F7783Eefc39\` (18 decimals). The **wstETH** wrapper is \`0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0\` (18 decimals).

| Live Harbor manager market | Current harvestable | Live harvest reward rate | Gross CALLER reward | Read-only \`eth_call\` | Est. gas cost in ETH |
|---|---:|---:|---:|---|---:|
| ETH/fxUSD | 10.338286893776817624 fxSAVE | 1% | **0.103382868937768176 fxSAVE** | SUCCESS | 0.000068106661897470 ETH (298,270 gas) |
| BTC/fxUSD | 1.030064520920529924 fxSAVE | 1% | **0.010300645209205299 fxSAVE** | SUCCESS | 0.000068104378507860 ETH (298,260 gas) |
| BTC/stETH | 0.003630945473818365 wstETH | 1% | **0.000036309454738183 wstETH** | SUCCESS | 0.000070638027619116 ETH (309,356 gas) |
| USD/stETH | 0 wstETH | 1% | 0 | not attempted | — |
| USD/WBTC | 0 WBTC | 1% | 0 | not attempted | — |

**Rebalance:** first three \`rebalanceable=false\`. USD/stETH and USD/WBTC \`rebalanceable=true\`, but \`eth_call(rebalance(dummy,0))\` REVERTED for both, returning error selector \`0xcba94f20\` and peggedToken \`0x2536A8636A99466173229AB15fdb37Fcaa05BA1A\` in returndata; the source has a \`NoTokensToLiquidate(address)\` branch. Exact error selector should be ABI-verified before affirming a decoded error label. **Neither is presently a successful rebalance payout**.

**Reported ETH network gas price** from the RPC at this snapshot: 0.228338961 gwei. Current fee environment is very low for Ethereum; future fee may be higher. Gas estimates, not paid gas, because no transaction executed.

### Conservative comparable USD viability screen (reference, NOT execution price)

Time-matched, non-orderbook USD price references dated 2026-10-12:
- fxSAVE reference ~$1.12 USD/token, [CoinGecko fxSAVE](https://www.coingecko.com/en/coins/fx-usd-saving) (asset is NOT zero-valued merely because a separate site's primary widget shows 0.00; consult token contract + quote).
- wstETH roughly ~$3,129 USD/token, [wrapped stETH Oct 12 quoted forecast/market reference](https://blockspot.io/coin/wrapped-steth/price-prediction/); older [CoinLore daily WSTETH history](https://www.coinlore.com/coin/wrapped-steth/historical-data) confirms same scale but is not contemporaneous executable depth.
- ETH dated Oct 12 about **$2,536**, [Investing.com ETH/USD October 12 history](https://www.investing.com/crypto/ethereum/eth-usd-historical-data).

| Opportunity | Reference gross USD | Est. ETH gas USD | **Indicative gross-minus-gas USD** |
|---|---:|---:|---:|
| ETH/fxUSD | **$0.115789** | **$0.172718** | **-$0.056930** |
| BTC/fxUSD | **$0.011537** | **$0.172713** | **-$0.161176** |
| BTC/stETH | **$0.113612** | **$0.179138** | **-$0.065526** |

The screen already loses money in **all three**. It excludes fxSAVE/wstETH conversion or redemption, approval, swaps, routing, MEV and failed tx costs — those make the economics even less favorable. The simulation does NOT prove we would be first into the next block. Thus **do NOT spend any part of $10 on these three harvests.**

**Potential improvement test if network gas falls or yield accrues:** The breakeven for ETH/fxUSD at current gas+fxSAVE prices requires **>=0.15421 fxSAVE caller payout**, or **>=15.421 fxSAVE harvestable** (currently 10.338). This ignores conversion fees, competition and gas buffers. For a safe actual attempt a **several-times margin** over total costs is required; mere mathematical breakeven is insufficient.

## Four other new mechanism families examined

### Velocity Protocol (Solana, public filler)
- [Official keeper incentives](https://docs.velocity.exchange/protocol/how-it-works/keepers/keeper-incentives) and [how fills work](https://docs.velocity.exchange/protocol/trading/how-fills-work): real Solana exchange, permissionless order filling; reward = lesser of 10% taker fee and age-based fourth-root formula; typical newly filled orders pay **1–4 cents**, expired order cancel/trigger = **$0.01** each.
- **$990 gross would require 99,000 successfully won one-cent cancel/trigger operations before fees**. A few unusual old large orders can pay more, but orderbook competition and successful account execution are unknown. The \`mark TWAP\` crank **pays $0** and requires **$1,000 insurance stake**, wholly disqualified.
- Official docs say the Velocity program is **NOT yet open source** pending audit; deployed code and current open work were not independently verified. **STOP for high-value/fast $1k**, avoid building fill-bot.

### fillr Solana pre-launch order fills
- [Marketing homepage](https://usefillr.app/) prominently says **mainnet/live** and default **0.001 SOL** keeper bounty.
- [Its own more specific documentation](https://usefillr.app/docs) explicitly says **protocol currently DEPLOYED TO DEVNET, mainnet follows audit**, with only Jupiter keeper-fill demo running on mainnet. This is a MATERIAL first-party marketing-versus-deployment conflict. A 0.001 SOL demo bounty is not presently independent mainnet profit. **STOP** until verified mainnet program and actual funded unfilled commitments.

### Caliper vault fee harvest (Robinhood Chain)
- [Official Caliper docs](https://www.caliper.finance/docs/) say up to **300bps/3% of accrued fees** payable to any harvest caller. But **Chapter 09 states protocol vault/factory/fee router are on ROBINHOOD CHAIN TESTNET 46630, while only the CALI token is MAINNET 4663**.
- Claimed "token on mainnet" is not evidence the separate harvest reward contracts are live with real deposited assets. **STOP** and do not try to execute testnet vaults for $.

### GBLIN Base keeper incentive, ADAM Ethereum ETH fee sweep, Infinite Trading
- [GBLIN prior MCP README](https://github.com/gblinproject/gblin-treasury-risk-regime) references Base **0.00005 ETH floor to 0.01 ETH ceiling** keeper rebalance rewards. However the same repository's top-level current deployment text marks previous \`0x36C81d7E...\` vault as **SUPERSEDED**, current vault address \`0xc2181d97...\`. Current mainline README does not feature the old \`find_keeper_bounty\` entry point, and GitHub connector access/actual current source validation failed. **Version drift: no current publicly claimable reward has been proven.** Do not treat old tool examples as executable current bounty.
- [ADAM mainnet token-staker protocol](https://adam.sites.imd.fun/) shows a live UI **0.0056 ETH unsplit fees** and 0.5% to caller on fee processing. Illustrative total **0.000028 ETH / ~$0.071 gross** at Oct 12 ETH reference, BEFORE gas and any cooldown/MEV. No independent on-chain dry-run/gas or payout receipt was done. **Low value; no $25+ opportunity**.
- [Infinite Trading docs](https://www.infinitetrading.io/docs) pay 0.1–0.5% of the 10% *fee* taken on harvested earnings to caller, i.e. **0.01–0.05% of actual harvested earnings**, not 0.1–0.5% of deposits. To gross $990 needs ~$1.98m–$9.9m of eligible successfully harvested earnings captured by one newcomer, before gas. No current harvest inventory verified.

## Conclusions and next direction

**This live study establishes a useful positive FACT:** $10-free-capital independent caller bounties can be truly funded and successful in read-only simulations on actual mainnet. The surprise is that **even with extremely low gas (0.228 gwei), the profitable opportunity isn't there yet**; each candidate pays only ~$0.01–$0.12 before estimated gas ~$0.17–$0.18.

The data suggests prioritizing **low-fee chains with directly queryable live call rewards** of at least **$25** and **already large enough fee backlogs**. Reject launchpads with only devnet contracts and small caps. The obstacle is market supply and capture probability, not writing bots or having a better AI prompt.

Do NOT assume the user has a free EVM wallet; user's supported Binance Pay/PayPal/Airtm/RedotPay methods alone don't authorize gas-capable wallet signing. No user consent to spend or sign has been granted.

**Status:** $10 intact, $0 spent, $0 user earned. No current net positive reward, no legit evidence for reaching $1,000 fast. Next research should target an actually deployed low-fee mainnet keeper with an independent \$25+ unharvested callable payout; if it cannot be verified, record rejection and move to new classes rather than more protocol clone scanners.
