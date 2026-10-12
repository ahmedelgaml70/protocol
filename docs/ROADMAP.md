# Roadmap (revisable, evidence-driven)

## Phase 0 — workspace / knowledge capture
- [x] Create public `protocol` repository.
- [x] Record original prompts and constraints.
- [x] Document known mechanisms, blockers, research standards and capital guardrails.

## Phase 1 — proof of events, $0 at risk
- [x] Prepare read-only Kerf order and history scanning.
- [x] Offline unit tests.
- [ ] Connect to a working chain RPC outside the isolated tool environment.
- [ ] Capture a time-stamped report with deployed bytecode and event history.
- [ ] Establish whether actual caller rewards have happened.

## Phase 2 — measure accessible opportunity
- [ ] Confirm current verified deployed source, upgradeability, underlying token liquidity.
- [ ] Find one OPEN opportunity and record its chain/block/transaction evidence.
- [ ] Measure observed keeper concentration, reward frequency, and latency.
- [ ] Check competitors on at least one additional low-fee chain/protocol (Superfluid first).
- [ ] Model realistic gas, conversion and failed-call costs.

## Phase 3 — decision, not automatic execution
- [ ] Compare opportunity gross vs conservative realizable net under a $10 budget.
- [ ] Call simulation or fork dry-run, prove exact caller permission and expected token receipt.
- [ ] Obtain explicit approval for any real transaction or spending.
- [ ] Log post-trade net with receipts only if a user-approved execution occurs.

## Pivot triggers
Pivot if there are no paid events in a meaningful window, rewards are entirely captured by protected keepers, economics cannot be priced, contract code is unaudited/unverifiable, chain is inaccessible, or reward cannot be withdrawn.

## Why this is not an autonomous money printer
Read-only code doesn't make money; contracts don't reserve public rewards; the profitability of historically paid bounties does not show a new entrant can win. This project searches for evidence first.

## Added investigations

- [x] Inspect three extra published reward mechanisms in Kerf.
- [x] Create read-only event history census for PositionKeeper, LPVault and PreMarketPerp.
- [x] Check selectors/topics against local Ethereum Keccak reference implementation.
- [ ] Run `make test` on the committed GitHub revision; fix any failures.
- [ ] Run `make multi-history` from a machine with RPC access; record block range, raw events and keeper concentration.
- [ ] Enumerate **all** VaultFactory vaults if six seed vaults show paid activity.
- [ ] Confirm all deployed source/bytecode and token payout transfer events on Blockscout.
- [ ] Assess eligible actions with truly positive **net** realized-value rewards.

## Low-friction on-chain evidence
- [x] Identify keyless read-only RPC with current `eth_call`, `eth_getCode` and gas estimation.
- [x] Add `make scan-free` to check the 10 newest published Kerf orders without credentials.
- [ ] Run this command from a network-accessible machine and preserve the report block number, results and errors.
- [ ] Measure **timestamp coverage** for each historical scan; do not assume 30k blocks = a day.
- [ ] Use historical events from official RPC/provider supporting `eth_getLogs`, to quantify keeper profits rather than assuming gross bounty is profit.

## Evidence-first pivot after live report

- [x] Receive first user RPC report for Kerf RangeOrders (block 86,104,491): `nextOrderId=1`, zero orders and errors.
- [x] Archive sanitized report and deprioritize this contract.
- [ ] Identify **one deployed protocol with receipt-verified historical positive caller payouts** before building another scanner.
- [ ] Verify actual *current* eligible opportunities separately; don't infer from historic activity.
- [ ] Compare true net after gas, priority, exit liquidity, token sale and failed attempts; risk budget ≤$10.

## Superfluid receipt-first progress
- [x] Find publicly inspectable successful historical third-party token transfers (Base May 9–10, 2026).
- [x] Capture raw token inflow and ETH gas data with explorer provenance.
- [x] Add read-only reproducible `superfluid_receipts.py` and offline test fixtures.
- [ ] Run full GitHub checkout's unit tests and receipt RPC audit from a connected machine.
- [ ] Obtain **recent** event counts and payee concentration by month, especially September–October 2026.
- [ ] Determine which independent callers receive rewards vs designated TOGA Patrician in each phase.
- [ ] Verify token exit liquidity, gas, caller competition, and **currently eligible** Pleb/Pirate opportunity.

## Recent activity verification without full-node indexing

- [x] Inspect upstream Superfluid GraphQL schema for `AgreementLiquidatedV2Event` fields.
- [x] Add read-only 30-day liquidation event sample script and offline validation.
- [ ] Obtain current, timestamped last-30-days sample via `make superfluid-activity`.
- [ ] Verify **successful receipts and actual reward transfers** for recent event candidates.
- [ ] Determine which payout receivers are protected/preferred TOGA participants versus independent Pleb/Pirate callers.
- [ ] Check observable positive-net frequency; reject if absent before building executors.

**Critical interpretation rule:** the indexed event's `liquidatorAccount` can be the Superfluid **Batch Liquidator contract**, rather than the externally owned submitting wallet. This is proven in the May 9 Base transaction: indexed `liquidatorAccount=0x6b008BAc...`, but tx sender and actual ETHx recipient is `0xC20a5455...`. Treat indexed account concentration as *contract/event routing*, **not** executor competition. The script labels this explicitly; to measure human/bot-initiator concentration, enumerate transaction hashes and inspect `tx.from`, `eth_getTransactionReceipt`, and actual token transfers.

## October activity validated from user-uploaded report
- [x] Archive both uploaded read-only reports in GitHub.
- [x] Compute 300 capped indexed events, 270 distinct transaction hashes and actual 3-period split.
- [x] Isolate ETHx 46 events / 35 transactions, identifying high-value historical Oct 8 outliers.
- [x] Add next-phase read-only receipt sampler (largest+latest ETHx).
- [ ] Run `make superfluid-recent` and validate actual submitting-wallet transfers and full Base gas.
- [ ] Separate reward-receiver routing, transaction winners and token sale liquidity for major payout tokens.
- [ ] Make 30-day index complete using safe pagination; currently sample truncated to ~16 days.
- [ ] Find an *open, payable, permissionless* liquidation at a pinned block if economically warranted.
- [ ] If economic upside is too small or dominated by keeper competition, pivot rather than expanding code indefinitely.

## Post receipt-economics pivot (October 12)
- [x] Archive user's 12 real RPC receipts and compute exact ETHx token-inflow vs Base L1+L2 fees by submitting wallet.
- [x] Verify successful receipts can still be gas-negative; calculate 6/12 conditional net positive, 6/12 conditional net negative in a **biased sample**.
- [x] Separate USDCx Patrician-priority rewards from public Pleb-phase rewards.
- [x] Add explicit **STOP / monitor only** decision on Base liquidation execution.
- [ ] Search fresh, higher-value successful public-caller payout transactions on low-fee networks **before building a new bot**.
- [ ] Require evidence that operator profit > costs under conservative exit liquidity assumptions and is plausibly accessible with a $10 budget.
- [ ] Check a second asset/network before investing further in Superfluid; early pivot if prize pool is small/priority-locked.

## New reward evidence gate
- [x] Check current PoolTogether Base contract deployment and event ABI versus deprecated version.
- [x] Add no-key read-only ClaimedPrize / accrued fee recipient + gas audit.
- [ ] Run the latest GitHub test suite and PoolTogether 6h RPC scan.
- [ ] If fresh positive rewards appear, verify who receives fees, whether POOL reward is withdrawable/liquid, and competitive gas net.
- [ ] Then only identify an actually UNCLAIMED eligible action, with simulation; no spending yet.

- [x] Resolve Ripe Teller-to-AuctionHouse caller/keeper authorization and GREEN mint reward conditions in source.
- [ ] Find a successful recent Ripe Teller liquidation receipt showing GREEN minted to external caller; otherwise hold.
- [ ] Obtain current Base PrizePool ClaimedPrize receipts, actual prizeToken() value, and current Claimer tx.to before profit assertions.

## Automation operations
- [x] Add tests.yml for Python syntax and offline unit tests on repository updates.
- [x] Add protocol-radar.yml to run PoolTogether and Superfluid read-only scanners approximately every 30 minutes.
- [x] Add opportunity-alert.yml with a strict, deduplicated and **research-only** issue-writing gate.
- [x] Add scripts/run_radar.py, assess_radar.py, publish_alerts.py and offline tests.
- [ ] Inspect GitHub Actions run outcome and fix initial CI/configuration problems.
- [ ] Audit whether Base RPC serves 6-hour pool prize-claim logs without key or rate issues.
- [ ] Verify future alerts correspond to actual fee accrual and are never represented as currently collectible.
- [ ] Design Ripe evidence discovery once a deployed contract and payout receipt are independently established.

- [x] Identify a published PoolTogether Base GraphQL index and cross-check its schema against the current PrizePool source.
- [x] Integrate zero-key indexed prize claim discovery with independently read-only Base receipt validation.
- [ ] Verify official Graph Studio public endpoint works in GitHub Actions; if not, mark PoolTogether incomplete and pivot provider without fake zero results.

- [x] Verify initial GitHub Tests: 41 unit tests passed.
- [x] Verify full read-only Radar workflow: both indexed PoolTogether and Superfluid results succeeded; artifact stored and read back.
- [x] Fix public RPC historical-log and pruned-genesis limitations using the official PoolTogether indexed API + independent receipt verification.
- [ ] Observe a first **scheduled** radar run and ensuing workflow_run alert gate; do not create manual financial alerts.
- [ ] If PoolTogether indexed claims remain zero for a meaningful time span, pivot to other active protocols before building a keeper.

- [x] Expand PoolTogether Base indexed discovery from sparse 3-day window to a 30-day bounded historical sample; retain truncation flag.
- [x] Read official Ripe September 2026 open production keeper activation blocker #236; separate its deleveraging scope from liquidation public ABI.
- [ ] Record what the 30-day PoolTogether Base index actually returns and whether ANY current-claimer fee recipient earned rewards in validated receipts.
- [ ] Make alert workflow's first eligible scheduled run observable; don't mislabel skipped push-triggered runs.

- [x] Verify 30-day official PoolTogether Base index snapshot was not truncated and had 0 prize claims; downgrade Base claiming.
- [x] Identify Beefy native-token caller incentive, in-house Cowllector competition and historical gas-negative Base receipt.
- [ ] Prove recent *third-party* Beefy harvest with actual native/wrapped native fee payment net-positive on a low-fee chain.
- [ ] Verify the `workflow_run` research alert pipeline consumes a trusted smoke artifact successfully and exits without issue creation on zero signals.

- [x] End-to-end downstream read-only artifact download → research signal evaluation → no-issue branch tested with trusted default-branch push, 41 tests passed.
- [ ] Wait for actual qualifying on-chain evidence before verifying positive issue-create path; **do not fabricate evidence** for production alert testing.
- [x] Close idle PoolTogether Base Claiming issue #4 and shift research priority to Beefy public harvest issue #6.
- [ ] Investigate whether Beefy has actual current independent caller net-positive harvest receipts and a practical native-token payout versus gas.

- [x] Find maintained Beefy Cowllector v2 public last-harvest-reports API and inspect reward, gas and transaction output schema.
- [x] Add strict, read-only Beefy economic screen with 5 offline tests and integrate into Radar.
- [ ] Inspect real GitHub Actions Beefy API smoke result; retry only if endpoint or schema fails.
- [ ] Confirm recent example operator tx by live blockchain receipt and fee recipient; distinguish Cowllector-paid payouts from outside callers.
- [ ] Identify actual positive-net external caller payout and currently claimable harvest if evidence warrants; no auto execution.

- [x] Run independent RPC receipt verification for seven Base Beefy incumbent harvests; all successful, none WETH-positive vs gas.
- [x] Distinguish failed receipt RPC (incomplete) from verified zero/negative payouts; fixed false-good handling and retried official Base RPC.
- [x] Preserve exact seven hashes, observed WETH transfers and full gas in evidence file and CI artifact.
- [ ] Stop adding Beefy execution code until credible outside-caller positive-net examples emerge; pivot to higher payout types.

- [x] Extract Ripe current Base mainnet Teller/AuctionHouse/GREEN addresses and the LiquidateUser event ABI from canonical deployment manifest.
- [ ] Check Ripe current deployment bytecode and successful recent LiquidateUser receipts independently, including GREEN mint to actual independent submitting wallet.
- [ ] Verify GREEN token redeemability/realizable sale value and gas, then a current eligible account; no spend.

- [x] Identify Ripe official Base Teller/AuctionHouse/GREEN/sGREEN/MissionControl manifest contracts.
- [x] Validate Ripe event ABI and account for default sGREEN share mint, not just GREEN direct reward.
- [x] Add read-only code-presence and 6-hour historical event/receipt checks to GitHub Radar; no wallet.
- [ ] Verify live contract code and event index access, especially whether free RPC permits Ripe eth_getLogs.
- [ ] If history can be retrieved, assess nonzero keeperFee and actual GREEN/sGREEN to tx.from with gas and fee recipient.
- [ ] Do not send any transaction or assume token redeems at $1 without verified liquidity; current eligibility unproven.

- [x] Query deployed Ripe MissionControl `getGenLiqConfig()` and live pause flags: enabled, configured 1% keeper fee.
- [x] Correct GitHub Radar to classify Ripe unavailable history as incomplete, preserving proof of code and live config separately.
- [ ] Test alternate keyless Base RPC event-history providers without spending and retain provider failure states.
- [ ] Independently verify a positive GREEN/sGREEN mint receipt to external Teller caller; fee config is not a payout.

- [x] Try two additional documented keyless Base history RPC endpoints in real GitHub Actions; record authentication/HTTP failures exactly.
- [x] Disable repeat scheduled Ripe history requests after four independent free sources failed; retain manual history command.
- [ ] Find a verified working keyless historical event index or independent recent caller receipt; otherwise hold Ripe and pursue larger viable public bounty pools.

- [x] Find a documented keyless Base provider explicitly supporting filtered eth_getLogs within 2,000-block ranges (SolidRPC), rather than relying on paid Blockscout PRO.
- [ ] Run bounded 6-hour Ripe AuctionHouse log test with paced SolidRPC and inspect actual on-chain event/receipt result.
- [ ] If event history is accessible, extend one-time lookback carefully; only gate on verified actual GREEN/sGREEN to independent submitter and net after gas.

- [x] Prove filtered LiquidateUser eth_getLogs is available through paced keyless SolidRPC; 6h complete 10,801 blocks, zero events.
- [x] Independently hash the current manifest LiquidateUser ABI to validate its topic selector.
- [x] Avoid frequent free-provider backfills; add daily 24h Ripe history workflow with explicit completeness assertions.
- [x] Distinguish unrelated GREEN/sGREEN transfers from supported keeper rewards using positive keeperFee and mint/provenance conditions.
- [ ] Inspect first daily 24h audit result and verified tx receipts, if any.
- [ ] Audit GREEN/sGREEN sale/redemption economics only when a real positive payout appears.

- [x] Validate daily 24-hour Ripe history on real Base chain: 43,201 consecutive blocks with zero liquidation events, complete source.
- [x] Mark Ripe Base low-priority for rapid recurring payouts; maintain only low-volume historical monitoring.
- [ ] Audit permissionless **Morpho Blue Base** liquidation history with official GraphQL query before any automation/executor proposals.
- [ ] Match actual repay/seize token receipts, gas, token pricing, caller concentration and capital/flash-loan requirements if sufficient recent activity is observed.

- [x] Build one-shot read-only Morpho Base official GraphQL liquidation activity probe with offline input-validation tests.
- [ ] Verify actual Morpho API query in GitHub Actions; if supported, evaluate freshness, liquidation volume and liquidator concentration.
- [ ] Use recent verified receipts/DEX prices to test conservative net and flash-liquidity feasibility before considering any executor.

- [x] Live-confirm Morpho free GraphQL endpoint returns recent Base Liquidation records, cap 100, without keys.
- [x] Correct event/transaction aggregation with on-chain logIndex; two new offline regression tests.
- [ ] Rerun GraphQL and analyze *true distinct events*, transaction batching, date coverage, caller diversity and economic viability (not raw token amounts).

- [x] Add read-only independent receipts for 8 sample Morpho liquidations, requiring exact event logIndex, market, indexed caller and raw repayment/collateral agreement.
- [ ] Confirm external Morpho index and actual Base receipts agree on current submitted events, including true gas and caller routing.
- [ ] Quantify realizable bonus, token liquidity and gas after receipts verified; do not extrapolate from raw event counts.

- [x] Independently validate the 8 newest Morpho Base liquidation transaction receipts: 8/8 success, exact event logIndex/caller/raw debt and seizure match, fees accounted for.
- [x] Fix mocked caller-topic mismatch, confirm 70/70 Python offline unit tests pass on GitHub.
- [x] Archive bounded, biased Morpho events and independent receipt evidence with correct sample/truncation limitations.
- [ ] Fetch Morpho market token metadata, decimal precision, debt repayment valuation, collateral liquidity and realizable swap price to compute conservative net per transaction.
- [ ] Investigate flash-funded / delegated liquidation route and onchain operator competition before considering whether $10 gas budget is realistic.
- [ ] Check current eligible unliquidated account only if historically proven conservatively profitable outsider route exists; no signing/spending without separate approval.

- [x] Obtain correct market loan/collateral token addresses, decimals and current API reference USD prices for 98/100 indexed events.
- [x] Calculate strictly **illustrative gross** current-reference spreads without falsely labeling them historic realized profit.
- [ ] Reconstruct largest Morpho Base liquidation batch transaction full token flows (including swaps and flash loan) and historical execution-time exchange quotes; distinguish market oracle/reference valuation from realizable cash.
- [ ] Verify liquid collateral exit and conservative expected net AFTER gas/flash/DEX/slippage, failed-call loss, and any capital requirements for a newcomer.
- [ ] Independently check open, unliquidated borrower only after robust positive historic realized-dollar test; never sign or spend without separate explicit approval.


## Pivot (effective 2026-10-12)

- [x] Reassess keeper route based on read-only actual payouts; discontinue as primary plan.
- [x] Stop twice-hourly automatic on-chain scans but preserve manual dispatch and all tests.
- [x] Verify new platforms' country eligibility, payout speed, fees and contradictions from official documents.
- [x] Evaluate potential reusable digital products against observed marketplace listings and payment rails.
- [ ] Before spending $10 or making storefront: verify upfront Etsy setup fee quoted to Egyptian seller and Payoneer onboarding, or use a strictly free platform if plausible exposure exists.
- [ ] Verify product-specific **recent buyer evidence**, not generic template marketplace popularity, and develop one original premium interactive lecture/motion asset only when the niche passes the demand gate.
- [ ] If user explicitly permits platform-assigned contractor work despite no-freelancing preference: check open entry flow for GoTranscript Arabic, BetaTesting, PlaytestCloud and uTest; do not apply without approval.
- [ ] Do not claim payout accessibility until there is current inventory and a verified supported Egypt payout option.
