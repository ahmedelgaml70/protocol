# GitHub Actions operating guide — protocol

## Workflows (automatic after commit to main)

| Workflow | Trigger | Permissions | Purpose |
| --- | --- | --- | --- |
| [Protocol Tests](../.github/workflows/tests.yml) | Push/PR/manual | contents:read | Standard-library Python syntax and unit tests |
| [Protocol Radar](../.github/workflows/protocol-radar.yml) | 17 and 47 minutes of every hour UTC/manual | contents:read | Read-only 6h PoolTogether Base reward logs and 3d Superfluid Base indexed liquidations |
| [Protocol Opportunity Alert](../.github/workflows/opportunity-alert.yml) | After completed successful Radar runs | actions:read + issues:write | Validate JSON and create/update one deduplicated research issue ONLY on evidence from current PoolTogether Claimer |

## Manual control

On GitHub, open **Actions → Protocol Radar → Run workflow** to start an immediate scan. The scheduled scan runs approximately every 30 minutes, but GitHub may delay or drop runs under load. Reports appear on the run's page as a downloadable **protocol-radar-report** artifact; retention is 7 days. Scan output is never committed to the repository. No secrets or wallets are needed.

## What each scan really proves

- **PoolTogether:** Current Base PrizePool `ClaimedPrize` events in a recent 6-hour window; receipt samples show accrued claimReward, actual fee recipient and whether tx.to is the current published Claimer. It does NOT identify an unclaimed prize, prove fee withdrawal, or measure USD net profit. Empty 6h log sample is INSUFFICIENT to claim no activity.
- **Superfluid:** Recent Base liquidation subgraph events and contract/event routing. No unclaimed streams, complete 30-day census, or operator profit are proven; historical liquidation events are already taken.
- **Ripe:** NOT IMPLEMENTED for automated monitoring. Source-only reward mechanism is logged as an open research task, not an observed opportunity.
- **Alerts:** Current-claimer receipt + nonzero accrued payout is labeled a **historical research signal**, NEVER `execution ready`. No alerts from unavailable scanner data or Superfluid event counts alone. Any incomplete scan is explicitly labeled incomplete, not zero activity.

## Budget and security

Runs on public-repository standard GitHub-hosted runners; GitHub's standard hosted runner usage for public repositories is generally free subject to current platform terms, quotas and availability. No paid RPC plan, GitHub-hosted runner upgrade or service subscription is configured. Reports may contain public on-chain addresses, transaction hashes and public RPC metadata. Never set wallet/seed/private keys or paid API credentials in GitHub. The Alert workflow is deliberately privileged only for issues, does not execute untrusted source from pull requests, and parses downloaded artifacts strictly as JSON.

**There is absolutely no chain transaction/signing/broadcast path** in the workflows. The repo's existing scanners are restricted to read-only calls. No balance or wallet approval is involved. The full capital budget remains $10, never automatically spent.

## On failure

Read Protocol Radar's `manifest.json` for individual statuses. Network timeout, DNS errors, remote RPC rate limits, or missing data appear as `incomplete` or `timeout`; a scan with 0 events is distinct from failed data access. If the alert workflow fails due to GitHub permissions, inspect repository Settings → Actions → General and verify workflow permissions, or check whether organization rules restrict issue writing. Do not grant broader permissions or secrets without necessity.

## Disable

GitHub → Actions → Protocol Radar → ... → Disable workflow. This stops scheduled scans and downstream alert triggers. Tests remain independent. Workflow schedules do not guarantee second-level execution and are unsuitable for competitive liquidations.

## Sources

- https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
- https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions
- https://docs.github.com/en/actions/concepts/workflows-and-actions/workflow-artifacts

Initial-smoke-test behavior: changes to the radar workflow YAML itself on the default branch also start a read-only scan. The issue-writer explicitly ignores push-triggered scans, so this helps verify infrastructure without publishing any alert. Ordinary code pushes still run only the test workflow.

## First smoke-test result and data provider fix (2026-10-12)

Initial read-only smoke run [#38177006035](https://github.com/ahmedelgaml70/protocol/actions/runs/38177006035) succeeded at the workflow level and uploaded a 7-day report artifact. Superfluid Base's indexed 3-day sample succeeded (52 recent events). PoolTogether failed **eth_getLogs with HTTPError** at Base's default public RPC, so it was recorded as `incomplete`, NOT no claim rewards. The PoolTogether scanner in the scheduled runner was changed to the free, keyless PublicNode Base RPC (`https://base-rpc.publicnode.com`) whose public dashboard reports current `eth_getLogs` operations. This fallback still must be empirically tested for our filter and retention window; failures are never turned into success. Source: https://base.publicnode.com/

PublicNode response in second smoke run: `eth_getBlockByNumber` for genesis rejected due to pruning, not an `eth_getLogs` failure. Time window lookup fixed to start from chain tip. See `block_range.py`. Reports still fail safely if even required recent history is missing.

## Third smoke: fall back from eth_getLogs to PoolTogether's official subgraph

PublicNode's free RPC offers chain calls and recent blocks, but the third smoke test #38177235012 again failed `eth_getLogs` with HTTPError. This is a provider limitation, NOT proof of zero claims. Official PoolTogether docs publish https://api.studio.thegraph.com/query/41211/pt-v5-base/version/latest and its source schema provides `prizeClaims` with tx hashes, fee amounts and timestamps. The scheduled PoolTogether observer now queries that source for recent claims and **independently validates selected receipts on Base** through PublicNode. If GraphQL is blocked or stale, it records a scanner failure and cannot trigger an issue. The old direct-logs script is retained for manual use with a provider that supports the method.

Source: https://dev.pooltogether.com/protocol/subgraphs/ and https://github.com/GenerationSoftware/pt-v5-subgraph/blob/main/schema.graphql

## Verified initial operational baseline

Smoke run https://github.com/ahmedelgaml70/protocol/actions/runs/38177465238 **completed successfully**; PoolTogether official Graph Studio index and Base receipt RPC both accessible. PoolTogether's `prizeToken()` returned **Base WETH** (0x4200000000000000000000000000000000000006); 0 indexed claims appeared in the last 3 days, with the index **one block behind** chain tip. Superfluid Base returned 52 liquidation events, uncapped, over the same 3-day lookback. Tests run https://github.com/ahmedelgaml70/protocol/actions/runs/38177465230 passed **41 unit tests**. The research alert workflow was skipped for this `push` smoke as specified and awaits its first eligible `schedule` or `workflow_dispatch` completion for full write-path verification. All operations remain read-only; evidence snapshot: ../evidence/github-actions-smoke-2026-10-11.json.

## Expanded PoolTogether historical coverage (2026-10-12)
The first fully working 3-day Base PrizeClaims index had zero successful historical claims. A 3-day negative observation is not enough for Gate 0 elimination. The indexed discovery is therefore expanded to **30 days, capped at 500 newest claims**, with up to 10 actual receipt validations. `indexed_may_be_truncated=true` means the requested history was not exhaustively covered; an untruncated zero means no indexed PrizeClaim entities in this bounded range, subject to source/subgraph limitations. No signing, no wallet; the limited subset of receipts cannot prove profit by itself.

## Downstream notification smoke test (2026-10-12)
The post-radar `workflow_run` alert pipeline now also reviews **trusted default-branch push smoke scans**, in addition to the scheduled/manual scans. This tests artifact downloading, JSON evidence gate, and no-signal issue suppression without changing the research-only action policy. Only repository default-branch radar workflow changes trigger this kind of push scan; forks and PR artifacts are excluded by the job condition. The privileged stage never runs downloaded scripts. For a report with no current Claimer fee-receipt evidence, it **must exit without opening an issue**. Actual issue writing is not considered verified unless a genuinely qualifying signal eventually appears.

## End-to-end alert workflow smoke, verified
On trusted default-branch radar push, [alert workflow run #38177999974](https://github.com/ahmedelgaml70/protocol/actions/runs/38177999974) downloaded the real report artifact, assessed 0 signals and made **zero** issue changes, passing all steps. [Python Tests #38177985661](https://github.com/ahmedelgaml70/protocol/actions/runs/38177985661) passed 41/41. The alert publisher's **true issue-create branch is not yet tested against GitHub**—it requires a real qualifying historical fee receipt, which none of the 30-day PoolTogether Base scans found. Production never injects synthetic profit evidence to force an alert.

## Beefy Cowllector v2 — third read-only scanner

Protocol Radar now includes a 72-hour screen of Base, Arbitrum, Optimism latest-per-vault Cowllector operator reports through the publicly documented GET https://cowllector.beefy.com/api/v1/last-harvest-reports. The operator provides simulated reward and gas amount fields, success/skip status, and most recent transaction hash. The resulting beefy_cowllector.json is a transient artifact, not a trade recommendation, and DOES NOT trigger opportunity alerts.

The API provides only the last report for each vault, not all transactions; it encodes wei as JSON numbers which may not retain exact integer precision. Its estimated gains do not prove economic realizability or that an outside caller can win them. Network/server errors are explicitly marked incomplete. The maintained Cowllector v2 bot prioritizes at least daily harvesting, even when not profitable (see official README).

Source: https://github.com/beefyfinance/beefy-cowllector-v2/blob/main/apps/api/README.md and https://github.com/beefyfinance/beefy-cowllector-v2/blob/main/apps/api/src/routes/last-harvest-reports.ts .

### Independent Beefy receipts smoke verified (2026-10-12)
The fourth read-only scanner `beefy_receipts.py` reads the reported most recent Beefy Base tx hashes, fetches native Base receipts and WETH logs via `https://mainnet.base.org`, and compares transferred WETH to receipt L1+L2 gas. The initial attempt using PublicNode could not retrieve transactions and was **correctly changed to `incomplete`**; the subsequent run #38207227507 using the Base official public RPC verified 7/7 receipts with no errors. All seven were conditional WETH gas-negative and belong to the existing in-house bot. The scanner does not send transactions, and its balance proxy is not realized profit. See evidence/beefy-base-2026-10-12-receipt-proof.json.

## Read-only Ripe deployment & event checks

Two new independent scanner entries are in Radar: `ripe-base-deployment` queries chain ID + bytecode presence at the **five** official Base manifest contracts, while `ripe-base-history` tries timestamp-bounded AuctionHouse `LiquidateUser` logs via Base JSON-RPC; only on a retrieval error does it attempt a bounded free Blockscout explorer fallback. When events exist, it validates successful tx receipts, direct Teller routing, GREEN ERC-20 and *sGREEN ERC4626 shares* credited to the real tx sender, and recorded Base gas. No token is assigned USD value and no historical event is currently claimable. If no free logs access, `history_status=incomplete` is explicit; not zero payouts. Free explorer site access may be unavailable and its public API must not be confused with a paid PRO endpoint. Ripe emits NO alert based only on this observer. No wallet, transaction, or gas use is authorized.

## Ripe history provider failures and anti-spam safeguard

Run #38212232932 empirically checked keyless history sources: official Base eth_getLogs HTTP rejection, Ankr unauthorized on eth_chainId, Blast eth_getLogs HTTP rejection, Blockscout Base address logs HTTP 403. The history collector correctly emitted `history_status=incomplete` / event count null and GitHub manifest labeled its check `incomplete`, not `ok` or 0. To avoid repeating failed queries every scheduled run, the recurring `ripe-base-history` entry has been **disabled**, while `ripe-base-deployment` remains active and checks runtime flags. Read-only history is available for troubleshooting using `make ripe-history`; without a valid free event index, no negative inference can be made. No paid RPC or signing. Outcome archived in evidence/ripe-base-2026-10-12-history-providers.json.

## Ripe history provider experiment — 2026-10-12

SolidRPC's [keyless EVM public RPC documentation](https://solidrpc.io/docs/public-rpc) explicitly lists Base `https://rpc.solidrpc.io/public/evm/8453`, `eth_getLogs`, and a **2,000-block ceiling** for filtered queries. A new `ripe-base-history` scan is added with **6h lookback**, **1,500 blocks/request** and slow `0.85 s` pacing for this particular endpoint to honor the public rate limit. A one-page explorer fallback remains available on errors, but failure is reported `incomplete`, not zero events; this provider may still throttle or refuse request patterns. Retain only if real GitHub Actions validates it and avoid scaling to an aggressive production indexer; the provider explicitly warns against high-volume indexing. The scanner invokes only the allowlisted read-only RPC methods and never sends a transaction.

## Ripe schedule isolated (October 12)

The first successful SolidRPC experiment covered 10,801 Base blocks in 6h with **zero matching `AuctionHouse.LiquidateUser` logs**, no historical lookup failure. The history worker is now **Ripe Keeper Evidence** under `.github/workflows/ripe-history.yml`, scheduled **once daily at 06:13 UTC** with a bounded 24-hour historical interval and max ten receipt verifications. It does not execute wallets, and it will explicitly fail if historical data or receipts are incomplete, retaining a seven-day JSON artifact for diagnosis. The twice-hourly Protocol Radar continues only Ripe deployed-configuration checks, reducing anonymous RPC traffic. Keyless SolidRPC explicitly warns against bulk production indexing; daily is a small research audit, not competitive execution. The downstream research issue writer only reacts to the named Protocol Radar workflow and is not wired to this separate history worker.

## Morpho research-only GraphQL source
One lightweight additional `morpho-base-liquidations` scanner queries the **official public Morpho Blue Base** GraphQL indexed liquidation transactions, request limit 100 and lookback seven days. JSON artifact includes tx hashes, raw repaid and seized token units, address of indexed liquidator, and cap marker. No wallet, no signing, no transaction broadcast, no USD PnL calculation and **no Morpho alert issue creation** from this observer. Query availability is assessed by actual GitHub run, not assumed. API reference https://docs.morpho.org/developers/borrow/tutorials/get-data/ .

## Morpho Base receipt cross-check
The history index's newest up to **8 unique transactions** are independently checked by `morpho_receipts.py` using **Base public read-only RPC** for successful transaction receipt, correct Morpho Blue `Liquidate` event topic and logIndex, indexed market and caller, raw repaid/seized values and full reported Base gas. The process *does not price token movements*, examine flash-loan PnL or find still-open borrowers. The result is an integrity check, not a profitable-trade signal. If any receipt mismatches, the scanner must return `incomplete`, not claim no liquidations. Official source: https://github.com/morpho-org/morpho-blue/blob/main/src/libraries/EventsLib.sol .
