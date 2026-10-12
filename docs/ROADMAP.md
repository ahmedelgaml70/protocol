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
