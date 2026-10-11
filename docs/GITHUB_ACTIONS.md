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
