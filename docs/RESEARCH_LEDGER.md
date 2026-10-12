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

## Superfluid security status (2026-10-11 review)

Superfluid DAO's Security Council reported a September 2026 Celo-only incident involving insolvency / broken stream liquidations. According to its October 2 technical report, a September 4 hotfix restored liquidation; it stated other supported networks were unaffected. We will **exclude Celo from the initial legitimate-bounty search** until new deployment conditions and liquidator economics are independently verified, and we will not attempt or automate any security exploit.

Source (original security council): https://forum.superfluid.org/t/security-council-preliminary-disclosure-of-a-security-incident-that-impacted-g-liquidity-on-celo-network/1743

Superfluid's official Sentinel provides `/nextliquidations` on *a running instance*, not automatically as a public hosted web API. Its normal startup expects a funded signer and RPC; do not run it in signing mode. Documentation: https://github.com/superfluid-org/superfluid-sentinel

**Subgraph lead:** Superfluid's documented public schema/SKD subgraph queries can help enumerate stream state, but no live stream-subgraph endpoint has been confirmed accessible in this tool session. Real solvency remains an on-chain calculation rather than just a stale subgraph snapshot.

## Competition and free infrastructure details

Kerf explicitly states that its own off-chain keeper scans open RangeOrders with Multicall3 and tries to fill an eligible order when the bounty is at least `GAS_BOUNTY_MULTIPLE = 3` times its estimated gas cost. This makes a 1% theoretical bounty an **actively contested** payout; the 1–3× gas segment may still be net positive but is small and not proven accessible to us. Source: https://www.kerf.finance/docs/range-orders .

Robinhood Chain's ~100ms block rate means historical inspection windows must be defined in timestamps, not guessed from block counts. The `30,000` block default is likely roughly 50 minutes, which risks a false 'no activity' inference. Source: https://www.ankr.com/docs/changelog/robinhood-chain/ (published Oct 1, 2026).

New zero-key observation source: Triport public keyless RPC `https://triport.io/rpc/robinhood/public`, 60 calls/minute, `eth_call`, `eth_getCode`, `eth_estimateGas` available, `eth_getLogs` unavailable. Use for **current contract state only**, not historical payout measurement. Source: https://triport.io/docs/robinhood/public .

### Decision note
**Kerf current classification: RESEARCH, lower priority until actual paid transactions / current eligible order evidence are observed.** The official bot raises the effective entry difficulty. Continue scanning, but do not equate the repo's 4 bounty mechanisms with actual available revenue. No new positive-net claim has been made.

## User-supplied live Kerf RangeOrders countercheck (2026-10-11)

Observed block 86,104,491: `nextOrderId=1`, 0 orders scanned, 0 errors. This shows no placed RangeOrders under the source's monotonically increasing order numbering, subject to validating deployed code. **PIVOT:** deprioritize the RangeOrders target; do not continue writing a keeper for it without a subsequent observed `Placed` event or `nextOrderId>1`. Other Kerf keeper harvest and perp contracts are separate and still lack activity proof. See [saved user input](../evidence/kerf-rangeorders-4663-block-86104491.json).

New candidate cross-check: Velocity docs describe 1-cent flat order trigger/cancel incentives and typically cent-scale fill incentives. The documented mechanism is real as *a published protocol claim*, but independent deployment and payouts were not confirmed here and the unit economics would require substantial volume. Another candidate, Atomic Green, appears in DeFiLlama with an Aug 2026 signature replay exploit; treat its keeper documentation as inadequate without incident remediation confirmation. Liquity V2 is prioritized for review of transaction *success and actual compensation*; mere method-call listings or old txs are insufficient. Details in [docs/CANDIDATE_TRIAGE.md](CANDIDATE_TRIAGE.md).

### Liquity V2 latest screen: economic activity matters

DeFiLlama's aggregated Q3 2026 gas compensation for Liquity V2 is shown as **$0**, despite the documented `0.0375 WETH + collateral` reward formula. This may be a metric/reporting limitation and needs independent confirmation; it is evidence **against** assuming an accessible active reward market. A historical Feb 5, 2026 liquidation attempt at an Etherscan-labeled TroveManager reverted, demonstrating real gas-loss risk. Sources: https://defillama.com/protocol/liquity-v2 ; https://etherscan.io/tx/0x9c06addedd2b7f86a7e69271712c54fb74a0f7a73163f045aa6897ee49a2643c .

## Explorer-verified successful Superfluid Base payouts (historical, May 2026)

**This clears our Gate 0 (successful transfer to caller) for the *protocol mechanism*, not Gate 1 for a current collectible payout.** Primary transaction explorer pages:

- May 9, 2026 [tx 0x4688d170...](https://basescan.org/tx/0x4688d1709a06a8adde20328eb9e71e3955ff1e54e64234073515bfff8b75668b): Status **Success**, ETHx transfer to submitting caller `0xC20a5455...7cc9e47f3` of **0.000277410573088982 ETHx**, transaction fee **0.000004537004547885 ETH**. At explorer's historical ETH=$2,326.24, and ONLY if ETHx ≈ ETH in redeemable value, this is about **+$0.6348** after gas but before conversion/withdrawal/overhead. This is **not verified realized profit**, and the sender may be a preferred/automated keeper.
- May 10, 2026 [tx 0x8cf34f65...](https://basescan.org/tx/0x8cf34f65aea1f5743fadd59e91036444744263a6ecd75e9b719c04a35bb7a709): Status **Success**, ETHx transferred to the same caller **0.000000465912049232 ETHx**; gas **0.000012847657966968 ETH**. With historical ETH=$2,370.83 and hypothetical ETHx/ETH parity, approximately **-$0.02936** after gas alone.

**Key lesson:** An `AgreementLiquidatedV2` event indicates liquidation, but its `rewardAmount` is not necessarily the same as the net ERC20 amount transferred to a transaction caller from a batch; count actual token `Transfer` logs and gas and still distinguish transfer receipts from realized cash. Both transactions date from May, not October. No unclaimed job, Pleb eligibility, solvency state, caller priority, or current liquidity has been established.

Evidence snapshot: [historical Base receipts](../evidence/superfluid-base-2026-05-samples.json). Local read-only RPC confirmation script: [superfluid_receipts.py](../superfluid_receipts.py). Its logic was exercised with four offline synthetic tests locally; the version committed to GitHub should also be verified with `make test`.

Superfluid Pleb/Pirate caller rules: https://medium.com/superfluid-blog/introducing-sentinels-the-keepers-of-superfluid-protocol-4eadca384cbf . The presence of liquidations does not prove rewards are accessible to a new operator.

## Superfluid official indexed event source (candidate for freshness test)

Official upstream `AgreementLiquidatedV2Event` subgraph schema declares `transactionHash`, `timestamp`, `token`, `liquidatorAccount`, `rewardAmountReceiver`, `rewardAmount`, `liquidationType`. Source: https://github.com/superfluid-org/protocol-monorepo/blob/dev/packages/subgraph/schema.graphql

Known endpoint pattern: `https://subgraph-endpoints.superfluid.dev/base-mainnet/protocol-v1`. The newly committed `superfluid_activity.py` queries this over POST for up to 300 recent events, reports frequency and caller concentration. The output **must not be treated as a live list of unclaimed targets**: Superfluid streams update continuously and the subgraph does not automatically represent current balances. The endpoint's availability in the user's network is untested.

The script performs no signing or broadcasts. It must be run from an internet-connected environment; an error result is not evidence of zero liquidations.

**Critical interpretation rule:** the indexed event's `liquidatorAccount` can be the Superfluid **Batch Liquidator contract**, rather than the externally owned submitting wallet. This is proven in the May 9 Base transaction: indexed `liquidatorAccount=0x6b008BAc...`, but tx sender and actual ETHx recipient is `0xC20a5455...`. Treat indexed account concentration as *contract/event routing*, **not** executor competition. The script labels this explicitly; to measure human/bot-initiator concentration, enumerate transaction hashes and inspect `tx.from`, `eth_getTransactionReceipt`, and actual token transfers.

## October 11 submitted Superfluid reports: full data audit

Archive: [full October Base indexed activity](../evidence/superfluid-base-2026-10-11-activity-full.json), [actual May Base RPC receipts](../evidence/superfluid-base-2026-05-receipts-rpc.json), [summary](../evidence/superfluid-base-2026-10-11-analysis.json).

- 300 indexed events in the user's sample, **270 distinct tx hashes**, 15 days 19 hours 51 minutes covered despite asking for 30 days (sample cap reached). No overclaim of monthly census.
- Event type 0 (Patrician priority) 40; type 1 (Pleb) 231; type 2 (Pirate) 29. Mapping grounded in official Superfluid token liquidation type source and protocol docs: https://github.com/superfluid-org/protocol-monorepo/wiki/About-Buffer ; https://superfluid.gitbook.io/superfluid/sentinels/liquidations-and-toga . A Pleb/Pirate **event** was eventually executed; that event is no longer available to newcomers.
- Indexed `liquidatorAccount` is Batch Liquidator for all 300, and receiver is Batch Liquidator for 260; remaining 40 indexed reward receiver `0xa87f76e99f6c8ff8996d14f550cef47f193d9a09`. Only `tx.from` + receipt transfers can identify actual submitting-wallet winners.
- 46 events for Base ETHx `0x46fd5cfb4c12d87acd3a13e92baa53240c661d93`, 35 distinct tx, sum **0.031339692062159336 ETHx indexed event amounts**, not verified sales. **90.26%** is concentrated in 2 Oct 8 events (`0.014155765965924920` and `0.014130982209939863` ETHx).
- Of the latest 24 hours ending 20:47:30 UTC Oct 11, there were 19 indexed events, 14 transactions, 4 ETHx events; not 19 accessible reward openings.
- User-supplied May RPC receipts confirm 2 old successful transactions, ERC20 transfers to caller and complete gas breakdown. First rough parity-based net **0.000272873568541097 ETH equivalent** before conversion and other costs; second **−0.000012381745917736 ETH equivalent**. **Not actual realized profits**.

**Decision:** Superfluid clears *historical usage* gate and merits one tightly scoped receipt audit, **not** deploying a keeper. The tiny and concentrated ETHx raw incentives do not substantiate a plausible rapid $1,000 return. Other token amounts can be very large in raw base units but may be worth little or be illiquid. Reject unpriced rewards.

Relevant baseline evidence: https://basescan.org/tx/0x4688d1709a06a8adde20328eb9e71e3955ff1e54e64234073515bfff8b75668b and https://basescan.org/tx/0x8cf34f65aea1f5743fadd59e91036444744263a6ecd75e9b719c04a35bb7a709 .

**Additional computed observation from saved input:** 184 unique token addresses, of which 180 appear once. The remaining 4 tokens appear 52, 46, 14 and 8 times respectively. This underscores why reward amounts must be converted to *realizable* values only with verified liquidity; singleton tokens are not by themselves suspicious or worthless.

## October 12, 2026 — 12 ETHx transactions audited against Base RPC receipts

From the user's uploaded `superfluid_recent_receipts.json` (archived, separate from May samples): 12 of 35 distinct ETHx transactions; 12 success, 6 positive ETH-parity proxy, 6 negative. Selected to oversample the highest rewards and newest calls, **not a representative 6/12 winning rate for independent bots**.

| Submitting wallet | Receipts audited | Conditional net, ETH-equivalent |
|---|---:|---:|
| `0xa4ddac803117c6da2931fc40d2977c566896fc41` | 5 positive | +0.029372300769558454 |
| `0x4ead40da807fa1ccaa8be38f8dbc5be346a39239` | 1 positive | +0.000749116379986537 |
| `0xc20a5455035ab593682cf9b9916b9407cc9e47f3` | 6 negative | −0.000036079741400214 |

Important economic caveat: a historical call's `ETHx_transferred_batch_to_submitter - (Base L1+L2 gas)` is a conditional *economic proxy*, not actual USD realized: ETHx may not be redeemed at parity, token swaps/slippage and failed keeper attempts not counted, plus possible rewards to another beneficiary. The Oct 9 `0x6f3373f5...` tx includes an indexed reward, but the receipt auditor recorded **zero direct ETHx transfer to submitting wallet**; don't silently attribute an indexed reward to the operator.

**Liquid token filter:** 52 USDCx indexed events aggregate ~127.843 USDCx raw/18 decimals, but 33 priority-phase events account for ~127.774 USDCx; 19 public Pleb events account for only ~0.069261 USDCx before any gas. USDCx Base contract `0xd0438339...439af9ce1b` documented in [Superfluid x402 example](https://github.com/superfluid-org/x402-sf). SUP token `0xa69f8052...0644c8792` is identified by [official governance](https://forum.superfluid.org/t/superfluid-token-address-multisigs-official/92), 923.978 raw SUP tokens across 14 events; dollar value depends on current tradeable price and liquidity and cannot be inferred from numeric unit count. This is evidence against treating broad event volume as cash rewards.

**Decision:** Do not deploy a Base liquidator on $10. Original read-only source reports and computed metrics are preserved in `evidence/`, with a separate summary in `docs/OCT_2026_DECISION.md`.

## 2026-10-12 cross-protocol research
Investigated PoolTogether V5, Ripe, GMX, GBLIN, lolpad.fun, fillr and obsolete Synthetix. PoolTogether current Base PrizePool (0x45b2010...) emits ClaimedPrize with fee/reward receiver; the documented Claimer is 0xcdCE635..., NOT deprecated 0x5ffeee76... . Older source uses an incompatible event signature. Read-only reward scan added; no current positive event or profit verified. See docs/KEEPER_ALTERNATIVES_2026_10_12.md.

Ripe source audit: Teller public liquidation actions delegate via authorized AuctionHouse (only Teller may call it directly), forward msg.sender as keeper, and mint GREEN/sGREEN only on nonzero keeper-fee calculation capped by debt-based ratio and collateral surplus; zero possible. Source https://github.com/Ripe-Foundation/ripe-protocol/blob/master/contracts/core/Teller.vy and https://github.com/Ripe-Foundation/ripe-protocol/blob/master/contracts/core/AuctionHouse.vy . PoolTogether claimed reward denomination is the deployed PrizePool.prizeToken(), not necessarily the POOL governance token; script corrected. No recent live positive payout yet proved for either.

### Beefy Finance public harvest — source-backed competing keeper, no verified current profitable opportunity
Official Beefy docs explicitly permit public `harvest()` and describe a small native-token caller reward between 0.05% and 0.5% of harvested yield. Their Cowllector keeper competes for calls and uses economic thresholds. Historical BaseScan April 2026 `harvest(address callFeeRecipient)` [0xe4e186d7...](https://basescan.org/tx/0xe4e186d7f12205829e5db06fe7b641e64e0acea9e904bf012f8e6315984ebec8) shows WETH recipient ~0.00000304 and transaction fee ~0.00000844 ETH: conditional net negative. Must check tx sender versus fee recipient and current successful harvest fee payments with receipts. Do **not** infer generic expected profits from old/possibly internal vault examples. Sources: https://docs.beefy.finance/developer-documentation/strategy-contract ; https://docs.beefy.finance/dao/treasury .
## 2026-10-12 — Receipt-verified Beefy Base harvest economics

**First live data:** Cowllector v2 returned 1,085 LAST-per-vault reports. In Base/Arbitrum/Optimism over 72h, 645 latest reports had valid reward and gas simulation fields; 514 showed a *positive gross* caller reward but **zero showed a positive estimated reward-minus-gas margin**. Eight records were marked harvested, seven from Base and one from Arbitrum. This was an operator-report economics screen, not actual payouts.

**Independent read-only Base receipts:** GitHub Actions [run #38207227507](https://github.com/ahmedelgaml70/protocol/actions/runs/38207227507) verified the seven Base reported harvests, all successful transactions to the declared strategies. In aggregate the SAME existing Cowllector wallet `0x03d9964f4d93a24b58c0fc3a8df3474b59ba8557` received **0.000011705879359994 WETH** and paid **0.000056682286523025 ETH** in full reported Base receipt gas. **Conditional deficit = −0.000044976407163031 ETH-equivalent** on WETH≈ETH assumption. **0/7** were positive after gas by this limited token flow measure. This is direct chain movement evidence for the incumbent, not proof about an outsider's access/earnings.

Source data artifact and exact transaction links in [receipt evidence](../evidence/beefy-base-2026-10-12-receipt-proof.json). In-house bot explicitly does NOT require every harvest to be profitable; it prioritizes frequent compounding per [maintained Cowllector v2 README](https://github.com/beefyfinance/beefy-cowllector-v2). Hence actual gas-negative calls are consistent with stated operating policy.

**Strict status: STOP** building a Beefy execution bot for the user's $10 risk capital. The 72h snapshot does not prove profitable external calls never exist, and the single Arbitrum receipt was not independently checked. But the observed reward density fails the project’s priority gate; other native/stablecoin public-bounty mechanisms deserve attention before more Beefy coding.

Full project suite [passed 52 offline tests](https://github.com/ahmedelgaml70/protocol/actions/runs/38207227503). No wallet key, signature, transaction or spend has been made.

## Ripe official Base deployment manifest parsed (October 12, 2026)

Retrieved official Ripe-Foundation/ripe-protocol current Base v1 manifest (GitHub blob 7f62d51c72ce17c31f580869acd8819ee7afd8d7), not inferred from stale explorer contracts. Current advertised addresses: Teller 0xae87deB25Bc5030991Aa5E27Cbab38f37a112C13; AuctionHouse 0xe9Dc24Ab1dC4746C7A43FAce3f895D9176D4C235; GreenToken 0xd1Eac76497D06Cf15475A5e3984D5bC03de7C707; MissionControl 0x559E53F42b68b4995732Dba4aF300796761DBC19. AuctionHouse ABI has indexed-user LiquidateUser event with keeperFee (nonindexed), distinct from actual GREEN transfer/mint to transaction sender. A positive emitted keeperFee alone is not proof of outsider profit. No recent successful payout has been found; source-to-deployed bytecode matching and GREEN exit liquidity still require independent read-only verification. Source: https://github.com/Ripe-Foundation/ripe-protocol/blob/master/migration_history/base-mainnet/v1/current-manifest.json ; issue #5 in this repository.

## 2026-10-12 — Ripe Base deployment & live keeper config PROVED; payout history UNKNOWN

[GitHub Actions #38211967821](https://github.com/ahmedelgaml70/protocol/actions/runs/38211967821) reached Ripe Base via official RPC and confirmed deployed bytecode for all 5 manifest contracts. Live `isPaused()` on Teller, AuctionHouse, MissionControl each returned **false**, and the deployed MissionControl `getGenLiqConfig()` returned **canLiquidate=true**, keeper ratio **100 basis points = 1%**, minimum keeper fee **1 GREEN**, maximum **25,000 GREEN**, 10% LTV payback buffer, GREEN/sGREEN each 18 decimals. These are **settings only**, not actually paid rewards; keeper may receive zero under insufficient collateral or retry conditions. Source metadata: [snapshot](../evidence/ripe-base-2026-10-12-state.json).

The history observer's 6h `eth_getLogs` request failed with HTTPError and the keyless Blockscout fallback returned HTTP 403. The manifest marks **ripe-base-history `incomplete` and event count `null`**, no invented zero. A follow-up attempts independently documented keyless Ankr/Blast RPC endpoints before conceding the collection gap. Need any positive event and independently matched **GREEN OR sGREEN** receipt to tx.from plus realistic token exit liquidity; no source bytecode match or execution eligibility yet verified.
