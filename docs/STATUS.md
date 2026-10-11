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
