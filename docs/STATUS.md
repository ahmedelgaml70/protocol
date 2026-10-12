# Status (2026-10-11)

**User goal:** grow a $10 budget toward $1,000 quickly without jobs, clients, promotions or referrals, ideally via legitimate permissionless crypto rewards.

**Actual realized profit:** $0 confirmed.
**Funds used by project:** $0. No wallet keys requested, no transaction authorized or sent.
**Best investigated leads:** Kerf RangeOrders read-only calls; Superfluid public liquidations.
**Main infrastructure blocker:** the previous isolated build environment could not resolve the Robinhood Chain RPC hostname, so it could not certify live fillable orders or any historical payout sample.
**Repo:** public, so keep secrets/local reports out of version control.

## Next measurable result
Run the RPC-backed scripts, inspect resulting reports, and audit any `Filled` events, caller concentration, output token properties, and real market liquidity. If no events, or only privileged keeper rewards, pivot.

This file is a snapshot, not a live performance claim.

## 2026-10-11 source verification update
- Confirmed via the Kerf source repository that `RangeOrders.sol` declares the ten-field order struct, public `fillable(uint256)`, read-only `orders(uint256)` and `nextOrderId()`, and permissionless `fill(uint256)` paying `KEEPER_BOUNTY_BPS = 100` (1%) of converted output.
- Confirmed the Kerf repository **claims** deployment of RangeOrders at `0xfE368De9fB4b0Ce845a7546B4261d4D15dC87C0C`, Robinhood Chain ID 4663, deployed block 56,938,742. The project identifies itself as beta and unaudited.
- Confirmed Robinhood Chain's official public RPC `https://rpc.mainnet.chain.robinhood.com`; it is rate-limited.
- **Not yet independently verified:** compiled-bytecode match, actual event activity, active fillable orders, realized token value, profitable outsider execution.
- Earlier local scanner package: 5 offline tests passed on the predecessor version. The re-authored GitHub repository version has unit tests committed but was **not executed through this GitHub connector session**. Do not claim its test suite passed until it is run.
- Do not enable GitHub Actions by default; run offline tests locally and store only sanitized result summaries.

## Continued session — 2026-10-11

- Verified the published source's `RangeOrders` ten-field struct, permissionless `fill`, event formats, 1% output-bounty, and the 4663 deployment manifest claim.
- Independently checked all existing manually coded function selectors and `Placed`/`Filled`/`Cancelled` event topics against Ethereum Keccak-256; they agree with the signatures.
- Discovered three further bounty classes in the *same published contract repo*: PositionKeeper harvest (0–3% of fees), LPVault harvest (0.5%), PreMarketPerp undercollateralized position liquidation (1% of positive remaining margin subject to available funds).
- Added `kerf_multi_history.py` and six offline unit tests. **These new tests are written but NOT EXECUTED in this repository environment.**
- Found official Blockscout free API information; account-generated API key required. This does not resolve RPC access by itself.
- We have **zero verified open, positive-net, execution-ready bounties**, zero wallet transactions, zero project expenditure.
- The accessible earlier **original ZIP's** five legacy offline tests were executed in the current session and passed; this is not a test result for the modified GitHub repo.

## Free RPC discovery / coverage correction (2026-10-11)
- Found and documented a **keyless no-wallet live read-only source**: `https://triport.io/rpc/robinhood/public`, up to 60 calls per minute per IP (shared and best-effort). It supports `eth_call`, `eth_getCode`, `eth_estimateGas`, and other light reads; **not `eth_getLogs`**. The repository now exposes `make scan-free` (last ten order IDs).
- Source: https://triport.io/docs/robinhood/public
- `make history` and `make multi-history` must continue using the official RPC or a provider with log access.
- Corrected interpretation: approximately 0.1-second blocks means a 30,000-block lookback is roughly 50 minutes and cannot support claims about daily keeper opportunities. See https://www.ankr.com/docs/changelog/robinhood-chain/ .
- Kerf's own bot reportedly sweeps all open orders and only fills when its estimated bounty is at least **3x gas**, so independent profits may be unusually competitive. Source: https://www.kerf.finance/docs/range-orders .
- In this session, local predecessor v0.1 offline tests were rerun and **all 5 passed**. The latest GitHub-revision tests remain unexecuted in this environment; do not equate the two.

## Scan-window fix (2026-10-11, follow-up)

Committed `block_range.py` with logarithmic timestamp-based block lookup and integrated `--lookback-hours` (24h default) into both Kerf historical scanners. Added three offline unit tests for range selection. The standalone algorithm was independently exercised locally using a synthetic timestamped chain: **3/3 tests passed**. The full GitHub repository test suite still needs execution on an Internet-enabled local checkout. No live payout results are established.

## First user-returned live report (2026-10-11)

Received `report.json` generated via the read-only RangeOrders scanner; archived as [evidence/kerf-rangeorders-4663-block-86104491.json](../evidence/kerf-rangeorders-4663-block-86104491.json). Raw report: chain 4663; reported contract `0xfE368De9fB4b0Ce845a7546B4261d4D15dC87C0C`; block **86,104,491**; nextOrderId **1**; 0 orders scanned, 0 open, 0 fillable, 0 errors, 0 transactions sent, 0 spent. The source documents order IDs starting at 1, so **no orders seem to have been created in the published contract by this block**, assuming deployed behavior matches source. The report was provided by the user and not independently reproduced here; treat as a trustworthy provisional observation, not cryptographic verification.

**Decision:** stop development focused only on Kerf RangeOrders. Investigate different deployed protocols by first establishing actual historical paid events (receipts/token transfers). Keep Kerf's other independent mechanisms as unverified, not disproven. Research triage: [docs/CANDIDATE_TRIAGE.md](CANDIDATE_TRIAGE.md). Net confirmed realized income remains **$0**, project expenditure **$0**.

### DeFiLlama Liquity V2 screen (2026-10-11)

Cross-check: DefiLlama's published income statement reports Q3 2026 **$0 gas compensation**, versus Q2 **$1.13K**. This reporting may not capture every liquidation transfer and does not establish zero actual liquidations; it **does** defeat any assumption that there's currently an abundant verified opportunity. Priority reduced pending current on-chain payout proof. Also found an Etherscan historical liquidation call that reverted `NothingToLiquidate()` with gas paid. Source: https://defillama.com/protocol/liquity-v2 and https://etherscan.io/tx/0x9c06addedd2b7f86a7e69271712c54fb74a0f7a73163f045aa6897ee49a2643c .

## Read-only Superfluid receipts — October 11, 2026

Found two **successfully executed** Superfluid Base batch-liquidator transactions from May 2026 with actual ETHx transfers to the initiator. First has positive illustrative transfer value relative to gas, **+$0.6348** under ETHx≈ETH price-parity assumption before additional costs; second **-$0.0294** on same assumptions. Data source: BaseScan receipts, not independently queried via RPC in this environment. New `superfluid_receipts.py` can repeat the audit read-only; a local implementation passed four synthetic offline tests, committed code may require its own test run. Evidence and citations in `docs/RESEARCH_LEDGER.md`.

**Research status:** Superfluid Base now passes Gate 0 *historical paid caller*, but still lacks confirmed current October 2026 eligible Pleb/Pirate liquidation, front-running/competition assessment and actual exchange liquidity. No funding or wallet actions.

## Subgraph activity observer — 2026-10-11

Added `superfluid_activity.py` to obtain recent indexed `AgreementLiquidatedV2Event` data without RPC block-range scanning. Official subgraph schema was inspected for these field names. The result records timestamps, transaction hashes, raw reward amounts, receiver addresses, and caller concentration (not profits). Equivalent local summary implementation was tested with three offline synthetic tests; the committed exact checkout requires full suite verification. External endpoint is **not reachable by our current tool environment**, so September–October 2026 activity has **not yet been observed**.

Run `make superfluid-activity` from a network-enabled terminal, then inspect sanitized `superfluid_activity.json`. Do not assume a stream is currently liquidatable based on this index.

**Critical interpretation rule:** the indexed event's `liquidatorAccount` can be the Superfluid **Batch Liquidator contract**, rather than the externally owned submitting wallet. This is proven in the May 9 Base transaction: indexed `liquidatorAccount=0x6b008BAc...`, but tx sender and actual ETHx recipient is `0xC20a5455...`. Treat indexed account concentration as *contract/event routing*, **not** executor competition. The script labels this explicitly; to measure human/bot-initiator concentration, enumerate transaction hashes and inspect `tx.from`, `eth_getTransactionReceipt`, and actual token transfers.

## Uploaded activity and receipt evidence — 2026-10-11

Validated both user-supplied files programmatically and archived them to `evidence/`. Current Base indexed activity is **real**, unlike Kerf RangeOrders: 300 events in a capped sample (270 transactions), spanning Sept 26 to Oct 11; 40 priority Patrician events (code 0), 231 Pleb (1), 29 Pirate (2). Their single indexed `liquidatorAccount` is the Batch Liquidator contract, not proof of an exclusive submitting operator. All 300 indexed reward amounts are >0 but values/prices and actual transfers are not established for these current transactions.

46 ETHx events across 35 txs sum to **0.031339692062159336 ETHx indexed rewards** in the sample, ~90.26% in two Oct 8 events (hashes in `evidence/superfluid-base-2026-10-11-analysis.json`). **This is historical event data, not money that can still be claimed.** The two old May RPC receipts confirm token transfer/gas, but they do not validate Oct winners. No real user profit, no spending, no signed calls.

New `superfluid_recent_receipts.py` and 3 offline tests cover a limited Base ETHx receipt sample. An equivalent implementation passed 3 synthetic local tests; complete GitHub checkout test suite still needs execution. Next run `make superfluid-recent`, then independently verify actual recipients, net *before swap* and caller concentration for Oct 8/Oct 11.

### Token concentration correction
The sample has **184 unique reward token contract addresses**, **180 appearing exactly once**. This does NOT mean those tokens are scams, but it makes a raw event-count or raw reward-amount headline poor evidence of liquid USD rewards. Focus next receipt audit on ETHx before spending time pricing other tokens.

## 2026-10-12 — October 12-receipt RPC audit

User uploaded read-only `superfluid_recent_receipts.json`; archived without secrets at `evidence/superfluid-base-2026-10-recent-receipts-rpc.json`, derived with exact base-unit arithmetic at `evidence/superfluid-base-2026-10-receipt-analysis.json`. All **12/12 receipts succeeded**; **6 conditional positive**, **6 conditional negative** based on 1 ETHx = 1 ETH transfer minus full receipt fees. Combined conditional net across intentionally selected transactions **+0.030085337408144777 ETH-eq**; **not realized profit**, nor representative of all 35 ETHx txs, nor of failed keeper attempts.

Per submitter: 0xa4dd...fc41 had 5 positive (+0.02937230077 ETH-eq), 0x4ead...9239 had 1 positive (+0.00074911638), 0xc20a...47f3 had 6 negative (−0.00003607974). Another critical detail: in one Oct 9 receipt, indexed event showed reward but **direct ETHx transfer to transaction submitter was zero**; investigate transfers to other addresses before imputing total protocol reward as bot income.

Original 300-event dataset: USDCx 52 events (33 priority Patrician/19 Pleb), **127.7738 USDCx priority** vs **0.06926 public-phase** rewards. SUP 14 events, 923.9782 tokens whose market value must be independently checked. This makes the number of 'events' a weak income proxy.

**Decision:** No execution; pause development of a live Superfluid Base keeper. Shift to evidence of larger paid public-caller transactions across several other mature protocols/networks, while optionally auditing the remaining 23 ETHx receipts only if a reason emerges. Details in `docs/OCT_2026_DECISION.md`. User profit $0, spending $0, budget $10 retained.

### Testing and infrastructure status (2026-10-12)
- Locally executed ten synthetic tests of equivalent Superfluid activity/receipt audit modules in `/mnt/data/protocol_audit`; all 10 passed. **This does not claim the complete, exact GitHub checkout's tests were executed.**
- Direct Internet access from the container remains blocked (DNS lookup failure for Base RPC and Superfluid GraphQL); uploaded user read-only data remain our verified local on-chain inputs.
- Specific next executable research is **external payout discovery** (issue #3), not a real transaction. No need for user wallet/API credentials.
- With purely illustrative ETH price $2,000–$3,000, the selected 12-call +0.0300853374 ETH-equivalent gas-only proxy corresponds to about $60.17–$90.26 before exchange, operational and failed-attempt costs. These are *scenario prices*, not actual market quotes or new earnings.

## 2026-10-12 keeper pivot
PoolTogether Base PrizePool/Claimer (current) and deprecated Claimer identified from official docs; current pinned source event ABI verified; old PoolTogether repo ABI differs (uint16 vs uint24 drawId). Added a read-only 6-hour event/receipt scanner plus 4 synthetic test cases, **not executed in the exact GitHub revision**. Current positive rewards NOT verified. Ripe is secondary pending real payout proof; discarded obsolete Synthetix Base, superseded GBLIN, and unverified small/upcoming mechanisms. See docs/KEEPER_ALTERNATIVES_2026_10_12.md.

2026-10-12 verification update: PoolTogether scan now reads deployed PrizePool.prizeToken() and on-chain decimals rather than assuming POOL governance-token payouts; it labels the actual transaction destination. Updated synthetic tests, full checkout unexecuted. Ripe has public Teller.liquidateUser() forwarding msg.sender as keeper to restricted AuctionHouse, which mints GREEN reward only if nonzero and collateral/liquidation conditions satisfy caps. Neither candidate yet has verified recent positive net payout to independent caller.

## GitHub Actions — automation installed (2026-10-12)

Workflows added under `.github/workflows/`: tests on push/PR; twice-hourly read-only radar; post-radar deduplicated GitHub issue alerts. Only the third workflow has `issues: write` (plus actions read). No keys or transactions; public repository hosted-runner standard tier. PoolTogether Base and Superfluid Base observers enabled. Ripe observation **unimplemented** until source-to-deployment and historical payout evidence passes Gate 0. Reports are transient artifacts with 7-day retention, not committed or falsely interpreted as zero on RPC errors. This commit does **not yet prove Actions has executed successfully**; verify run status under the repository Actions tab.

### Actions initial smoke (2026-10-12)
- GitHub Actions tests run successful, 36 offline tests passed.
- Radar smoke run #38177006035 completed, artifact archived: Superfluid Base 3-day subgraph success 52 indexed events; PoolTogether Base default RPC denied `eth_getLogs` via HTTPError (status incomplete).
- Alert pipeline skipped the push-triggered smoke scan by design, avoiding unapproved issue creation. Radar now uses keyless PublicNode endpoint for PoolTogether; fresh smoke test triggered to determine whether it serves actual event filter.

### PublicNode follow-up and pruned-history fix
PublicNode accepted PoolTogether RPC queries but returned RPC error 4444 on old block 1 (pruned; oldest available block around 51,000,000). Root cause was our timestamp-search helper querying genesis for a recent 6-hour window. Fixed `block_range.py` to exponential-backtrack from latest and binary-search a recent bracket; old history is never requested unless it is truly needed. Offline equivalence tests passed for normal and pruned histories. New smoke run triggered.

### Third smoke and subgraph alternative (2026-10-12)
The 2026-10-11 21:39 UTC smoke run confirmed 52 recent Superfluid events and PoolTogether `eth_getLogs` still received HTTPError even after improving time-window selection (PublicNode pruned history fixed). A new PoolTogether official subgraph + independently verified Base receipt scanner has been added. The scheduler now runs it rather than repeatedly querying an unsupported free RPC log method. New smoke run required to confirm Graph Studio public endpoint responsiveness. No user funds spent.

### Live CI validation completed (2026-10-11 21:42 UTC)
**[Radar smoke run #38177465238](https://github.com/ahmedelgaml70/protocol/actions/runs/38177465238) SUCCESS**, both PoolTogether and Superfluid scanners `ok`, artifact uploaded. PoolTogether official Base subgraph: 0 indexed prize claims in trailing 3 days, tip block 52,482,798, indexed head 52,482,797, prizeToken read from chain Base WETH 0x4200000000000000000000000000000000000006. This verifies backend reachability/freshness for that window, not overall liquidity or future opportunities. Superfluid Base: 52 indexed liquidation events over trailing 3 days, source sample not capped. Python CI [run #38177465230](https://github.com/ahmedelgaml70/protocol/actions/runs/38177465230) passed **41/41** tests. Alert workflow recognized by GitHub but intentionally skipped on push smoke, **not yet end-to-end verified for scheduled runs**. No current executable candidate, no profit, funds intact. Baseline: evidence/github-actions-smoke-2026-10-11.json.

## 2026-10-12 — 30-day PoolTogether proof and Ripe blocker
PoolTogether 3-day activity was zero from a near-tip official index, so the scheduled read-only GraphQL discovery was expanded to **30 days** (max 500 indexed claims; up to 10 receipt checks). This is more meaningful for deciding whether the current Base prize claimer is active. Any nonzero accrued reward still must pass receipt and withdrawal/economic checks.

Ripe's own GitHub [issue #236](https://github.com/Ripe-Foundation/ripe-protocol/issues/236) opened Sep 20 2026 is labeled `activation-blocker` for **retained Pool-1 deleverage keeper preflight/integration**, still open. This does not say public `Teller.liquidateUser` is disabled, but proves key keeper operations have unresolved production-integration concerns. Directly paying *external* liquidation receipts are not yet confirmed; Ripe remains source-only / HOLD.

### First 30-day PoolTogether index (2026-10-11 21:47 UTC)
[Actions #38177834708](https://github.com/ahmedelgaml70/protocol/actions/runs/38177834708) completed successfully. Current official Base PoolTogether Graph index near tip returned **zero prizeClaims in full trailing 30-day requested window**, `indexed_may_be_truncated=false`, zero receipt samples/error, WETH prize token. No public caller fees recorded **by this index in this window**, subject to index correctness; do not assert the protocol is inactive globally. Superfluid Base 52 liquidation events in trailing three days, no claimability. **PoolTogether Base downgraded from active high priority to low-frequency observation.**

Added a safe end-to-end alert pipeline smoke gate for trusted default-branch push radar runs; will record CI result when run completes.

## 2026-10-11 21:50 UTC — Alert workflow smoke passed
The end-to-end no-signal branch of the issue alert workflow passed: [run #38177999974](https://github.com/ahmedelgaml70/protocol/actions/runs/38177999974) successfully downloaded the read-only radar artifact, ran the strict assessment (`Research signals: 0; execution-ready: NO`) and exited without creating an issue (`No research signals. No issues written.`). [Tests #38177985661](https://github.com/ahmedelgaml70/protocol/actions/runs/38177985661) passed **41/41**; [Radar #38177985561](https://github.com/ahmedelgaml70/protocol/actions/runs/38177985561) succeeded. The **positive issue-creation path is still UNTESTED** because there is no genuine qualifying fee event; do not claim otherwise. PoolTogether Base issue #4 closed after 30d no claims; Beefy evidence-first research issue #6 opened. Evidence: `evidence/github-actions-alert-smoke-2026-10-11.json`.

## 2026-10-12 Cowllector v2 discovery

The maintained Cowllector v2 README states the bot is focused on consistent harvests (one per day per strategy), NOT necessarily operator profitability. Its public API at https://cowllector.beefy.com/api/v1/last-harvest-reports exposes the latest per-vault simulation and transaction report, including operator estimated native-like call reward, transaction gas, estimated profit and transaction hash. This is a richer research source than unverified strategy incentive marketing, but is **neither a complete historical census nor independently verified receipts**. Amounts may be approximate JS numbers, and operator reward asset may not be identical to gas asset.

Committed beefy_cowllector.py and five offline tests; Radar now attempts Base/Arbitrum/Optimism 72-hour reports. API availability in GitHub Actions was unconfirmed at commit time. The Beefy data cannot generate financial alerts. No transaction, wallet key or spend.

Scheduled-radar cadence caveat: between initial setup and 2026-10-12 05:03 UTC there was one recorded GitHub schedule run (at 00:44 UTC), successfully followed by a zero-signal alert run. The desired :17/:47 cron does not ensure real-time 30-minute starts.
## 2026-10-12 — Receipt-verified Beefy Base harvest economics

**First live data:** Cowllector v2 returned 1,085 LAST-per-vault reports. In Base/Arbitrum/Optimism over 72h, 645 latest reports had valid reward and gas simulation fields; 514 showed a *positive gross* caller reward but **zero showed a positive estimated reward-minus-gas margin**. Eight records were marked harvested, seven from Base and one from Arbitrum. This was an operator-report economics screen, not actual payouts.

**Independent read-only Base receipts:** GitHub Actions [run #38207227507](https://github.com/ahmedelgaml70/protocol/actions/runs/38207227507) verified the seven Base reported harvests, all successful transactions to the declared strategies. In aggregate the SAME existing Cowllector wallet `0x03d9964f4d93a24b58c0fc3a8df3474b59ba8557` received **0.000011705879359994 WETH** and paid **0.000056682286523025 ETH** in full reported Base receipt gas. **Conditional deficit = −0.000044976407163031 ETH-equivalent** on WETH≈ETH assumption. **0/7** were positive after gas by this limited token flow measure. This is direct chain movement evidence for the incumbent, not proof about an outsider's access/earnings.

Source data artifact and exact transaction links in [receipt evidence](../evidence/beefy-base-2026-10-12-receipt-proof.json). In-house bot explicitly does NOT require every harvest to be profitable; it prioritizes frequent compounding per [maintained Cowllector v2 README](https://github.com/beefyfinance/beefy-cowllector-v2). Hence actual gas-negative calls are consistent with stated operating policy.

**Strict status: STOP** building a Beefy execution bot for the user's $10 risk capital. The 72h snapshot does not prove profitable external calls never exist, and the single Arbitrum receipt was not independently checked. But the observed reward density fails the project’s priority gate; other native/stablecoin public-bounty mechanisms deserve attention before more Beefy coding.

Full project suite [passed 52 offline tests](https://github.com/ahmedelgaml70/protocol/actions/runs/38207227503). No wallet key, signature, transaction or spend has been made.

2026-10-12 Ripe deployment research: official current Base manifest parsed successfully via its GitHub blob; Teller 0xae87deB25Bc5030991Aa5E27Cbab38f37a112C13 and AuctionHouse 0xe9Dc24Ab1dC4746C7A43FAce3f895D9176D4C235, GreenToken 0xd1Eac76497D06Cf15475A5e3984D5bC03de7C707. The Loan LiquidateUser event includes keeperFee, but actual token mint and third-party receipt not yet verified. The official Params Explorer was unreachable via outside browser and therefore not treated as on-chain inactivity. Next proof gate tracked in issue #5. No wallet actions.

## 2026-10-12 — Ripe Base live-Gate audit implemented
Official Base v1 current-manifest addresses previously extracted and event ABI now used in `ripe_base.py` with tests: Teller 0xae87deB25Bc5030991Aa5E27Cbab38f37a112C13, AuctionHouse 0xe9Dc24Ab1dC4746C7A43FAce3f895D9176D4C235, GREEN 0xd1Eac76497D06Cf15475A5e3984D5bC03de7C707, sGREEN 0xaa0f13488CE069A7B5a099457c753A7CFBE04d36 and MissionControl 0x559E53F42b68b4995732Dba4aF300796761DBC19. `LiquidateUser(address,uint256,uint256,uint256,bool,uint256,uint256,uint256,uint256)` topic `0x2ad3b92c...` checked with Ethereum Keccak-256. The auditor requires positive keeperFee to identify potential bounty and independently checks the submitting wallet's GREEN/sGREEN Transfer receipt and full Base gas; never prices unrelated units as ETH. Read-only public RPC and optional unkeyed explorer history fallback may fail; status must remain incomplete instead of fabricated zero. GitHub scheduled scanner checks code and history separately. **First live run pending**.

## 2026-10-12 — Ripe Base deployment & live keeper config PROVED; payout history UNKNOWN

[GitHub Actions #38211967821](https://github.com/ahmedelgaml70/protocol/actions/runs/38211967821) reached Ripe Base via official RPC and confirmed deployed bytecode for all 5 manifest contracts. Live `isPaused()` on Teller, AuctionHouse, MissionControl each returned **false**, and the deployed MissionControl `getGenLiqConfig()` returned **canLiquidate=true**, keeper ratio **100 basis points = 1%**, minimum keeper fee **1 GREEN**, maximum **25,000 GREEN**, 10% LTV payback buffer, GREEN/sGREEN each 18 decimals. These are **settings only**, not actually paid rewards; keeper may receive zero under insufficient collateral or retry conditions. Source metadata: [snapshot](../evidence/ripe-base-2026-10-12-state.json).

The history observer's 6h `eth_getLogs` request failed with HTTPError and the keyless Blockscout fallback returned HTTP 403. The manifest marks **ripe-base-history `incomplete` and event count `null`**, no invented zero. A follow-up attempts independently documented keyless Ankr/Blast RPC endpoints before conceding the collection gap. Need any positive event and independently matched **GREEN OR sGREEN** receipt to tx.from plus realistic token exit liquidity; no source bytecode match or execution eligibility yet verified.

### Ripe keyless history provider decision (Oct 12)
Primary official Base RPC `eth_getLogs` rejected; independent keyless Ankr rejected eth_chainId as unauthorized; Blast Base RPC rejected eth_getLogs; public Blockscout REST returned HTTP 403. All tested in actual GitHub Actions (#38212232932), and `history_event_count=null` is **unknown, not zero**. The 6-hour `ripe-base-history` scan is **removed from recurring twice-hourly checks** to avoid useless provider retry/spam. Ripe **deployment/config remains monitored**; the historical scanner is preserved as opt-in `make ripe-history` or `python3 ripe_base.py --check history` for future working providers. No paid subscription, keys or signing.

## Ripe historical provider experiment — 2026-10-12

A candidate keyless Base endpoint `https://rpc.solidrpc.io/public/evm/8453` advertises filtered `eth_getLogs` up to 2,000 blocks per request in its published documentation. Re-enabling Ripe historical discovery **as a bounded six-hour experiment**, 1,500-block chunks, explicitly paced to <=~1.2 RPC requests/sec for this endpoint. Source https://solidrpc.io/docs/public-rpc . It has NOT yet returned verified payout receipts; first live Actions smoke will determine viability. The provider says public routes are for lightweight queries, not indexing or production backfills.

## 2026-10-12 — Keyless Ripe event history confirmed, separated from high-frequency Radar

[SolidRPC GitHub smoke #38213201010](https://github.com/ahmedelgaml70/protocol/actions/runs/38213201010) queried **10,801 Base blocks** (52,487,975 through 52,498,775 inclusive) at **06:35:57 UTC** and received `history_status=complete`, `history_event_count=0`, no positive keeperFee event or receipt, with **no RPC or explorer error**. All 5 manifest contracts remained deployed; on-chain liquidation settings remained enabled and unpaused. The event signature `LiquidateUser(address,uint256,uint256,uint256,bool,uint256,uint256,uint256,uint256)` independently hashes with Ethereum Keccak-256 to the configured topic `0x2ad3b92c465bc7ea1f27bef4120c0dee3b47cb039ba2af1c17061d831a465d2b`, so mismatched topic was ruled out.

This validates a six-hour **negative activity observation**, not a monthly census or proof no eligible borrower exists now. To respect SolidRPC's explicit policy against public-route production indexing, the repeated six-hour backfill was removed from twice-hourly Protocol Radar and placed in a **separate once-daily 24-hour, paced, limited-read `Ripe Keeper Evidence` workflow**; first daily workflow smoke will test it. Payout evidence hardened: raw GREEN/sGREEN incoming transfers alone do not certify a bounty; `keeper_reward_receipt_supported` requires a positive `LiquidateUser.keeperFee` and GREEN/sGREEN mint or GREEN transferred from AuctionHouse to the tx submitter. No wallet or gas spending.

## Ripe Base 24h evidence — October 12 06:42 UTC
The inaugural isolated daily workflow [#38213678949](https://github.com/ahmedelgaml70/protocol/actions/runs/38213678949) **passed**. Filtered read-only `eth_getLogs` complete across block range **52,455,744–52,498,944** (43,201 inclusive) on Base official AuctionHouse; `history_event_count=0`, `unique_liquidation_transactions=0`, `receipt_errors=[]`, all runtime settings enabled. **No historical rewards in this day**, and no current eligible borrower verified. Current Base Ripe liquidation revenue thesis fails the *frequent-paid-activity* evidence gate. The claim is bounded to this chain, address and 24h; not historical or network-wide impossibility. Low-rate daily audit remains, no execution. New alternative to screen: Morpho Blue indexed liquidation activity and actual operator economics, beginning with public free GraphQL API and read-only transactions, not flash loan bots.
