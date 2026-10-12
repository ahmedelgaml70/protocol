# Protocol — permissionless opportunity research

**Status:** research only · **Budget:** $10 reserved · **Verified collectible net profit:** none · **Real transactions:** disabled.

This repository is the working source of truth for the $10 → $1,000 challenge: finding lawful, permissionless rewards that can be captured through on-chain operations **without clients, jobs, promotional campaigns, or airdrop speculation**.

The $1,000 target is an aspiration, **not a forecast or guarantee**. A 100× return in a short period is highly unlikely. We will spend nothing until a verifiable, repeatable, positive-net opportunity has survived independent on-chain checks.

## Quick start

Install Python 3.10+; the observation tools use only the Python standard library.

```sh
python3 -m unittest discover -s tests -v
python3 kerf_radar.py --max-orders 100 --output report.json
python3 kerf_history.py --lookback-blocks 30000 --output history.json
```

These commands do not require a wallet. Live scans require a working Robinhood Chain RPC endpoint; an unreachable RPC is reported as an error, never converted to a claim that no opportunities exist.

## Project map

- [Original user prompts](docs/ORIGINAL_PROMPTS.md) — the exact motivation, constraints, and operating request.
- [Project charter](docs/CHARTER.md) — scope, $10 budget, disallowed approaches, and success criteria.
- [Research ledger](docs/RESEARCH_LEDGER.md) — checked protocols, source documentation, unresolved questions and false-positive risks.
- [Opportunity evaluation](docs/EVALUATION.md) — net payout, competition, proof requirements, and go/no-go gates.
- [Plan](docs/ROADMAP.md) — steps from detection to independent verification.
- [Agent instructions](AGENTS.md) — rules for anyone (human or AI) continuing this project.
- `kerf_radar.py`, `kerf_history.py` — read-only Kerf RangeOrders monitors.
- `tests/` — offline tests. `prices.example.json` — empty by design.
- `.gitignore` — protects local settings, keys, outputs and bytecode caches.

## What is already established

Official protocol documentation describes rewards for external callers (including qualified liquidations and keeper calls). **A published reward formula is not a verified opportunity.** No candidate has yet been demonstrated to be profitable, claimable, and executable with only $10 including gas, conversion costs and competition.

**No signing keys, seed phrases, private wallet data or RPC API credentials belong in this repo.** The repository is public. No automated money-moving software should be enabled by default.

## Core questions

1. Does the exact deployed contract authorize **anyone** to claim the reward?
2. Is a qualifying on-chain opportunity **currently open**, with a traceable event or view-call proof?
3. Is the output actually transferable/liquid and worth more than the full gas + priority + conversion costs?
4. Can a $10 wallet afford **all** necessary inputs and failed-call risk?
5. Is execution allowed under the protocol's rules and local law, without exploiting private data or systems?
6. Can we substantiate the answer with fresh, reproducible data?

Only after all six checks may a candidate be described as execution-ready. See docs/EVALUATION.md.

## References

- Kerf published code: https://github.com/KerfFinance/kerf-contracts
- Kerf explanation: https://www.kerf.finance/docs/range-orders
- Robinhood Chain network docs: https://docs.robinhood.com/chain/connecting/
- Superfluid Sentinel: https://github.com/superfluid-org/superfluid-sentinel

This is not financial advice or a promise of returns. The default operating mode is **read-only observation**.

## Extended read-only historical bounty census

The 1% range-order bounty is not Kerf's only published permissionless reward. The source also exposes PositionKeeper harvesting (caller share up to 3% of collected fees), LPVault harvesting (0.5% of collected fees), and PreMarketPerp liquidations (1% of remaining positive margin, capped by available funds). These apply only when their respective conditions are satisfied.

```sh
make multi-history
# or: python3 kerf_multi_history.py --lookback-blocks 30000
```

The extended observer reads **six seed vaults only**, plus one keeper and one perp contract. It records raw event amounts, not USD, and does **not** discover all factory-created vaults. It does not forecast currently claimable rewards. Zero events in its output mean zero *observed in that range*, not zero opportunity across the ecosystem.

**Test status:** the original local v0.1 package passed five offline tests. The revised GitHub modules and expanded tests are committed, but have **not** been executed in a network-capable local copy during this session. Run `make test` before trusting output.

**API fallback:** Blockscout documents a free PRO API for Robinhood Chain (up to 5 requests/sec and 100,000 credits/day), but a user-created API key is required. Free access does not guarantee unlimited `eth_getLogs` volume: https://github.com/blockscout/docs/blob/main/robinhood-api.mdx


## Fastest free live test (no wallet or API key)

Run `make scan-free` on a normal Internet-connected computer. This checks a small recent window of **10 Kerf order IDs** on a documented, keyless, **read-only** Robinhood Chain RPC endpoint operated by Triport. Its free endpoint supports `eth_call`, `eth_getCode`, and `eth_estimateGas`, but explicitly blocks `eth_getLogs`; historical event scanners must use the official Robinhood Chain RPC (or an RPC key that allows logs).

```bash
git pull
make test
make scan-free
```

If the endpoint is unreachable, the scan returns an explicit error. If it returns zero fillable orders, it only proves **none in the last 10 order IDs at the scanned block**, and does not prove that the protocol or older orders have none. A positive result is not execution-ready: bounty amount uses simplified V3 range math; the `fillable` view can become stale. None of this sends transactions.

Triport free RPC rules: https://triport.io/docs/robinhood/public
Official Robinhood Chain RPC: https://docs.robinhood.com/chain/connecting/

### Activity window caveat

Robinhood Chain is described as an approximately **100 ms** block-time chain (actual timing varies). A default `--lookback-blocks 30000` history audit may cover only approximately **50 minutes**, not a day. For ~24 hours of *nominal* chain time, roughly 864000 blocks are needed; the actual wall-clock span must be measured using on-chain block timestamps. Increase the history lookback and choose a provider that supports `eth_getLogs`, mindful of rate limits and log-range caps. Never describe a 30k-block scan as a full-day audit.

## Time-accurate event history

As of this revision, `make history` and `make multi-history` scan the last **24 hours**, computed using actual on-chain block timestamps. You may override with `--lookback-hours N` (up to 720) or a manual `--lookback-blocks N`; those are not equivalent and the latter does not imply any particular elapsed time. This prevents accidental undercounting on Robinhood Chain's very short block cadence. A provider with `eth_getLogs` access is still required for historical auditing. The separate `block_range.py` module uses only `eth_getBlockByNumber` and has standalone offline tests.

## Evidence-driven pivot: Kerf RangeOrders inactive at sampled block

The user ran the first live read-only scan. At Robinhood Chain block **86,104,491**, `next_order_id = 1`, zero orders and zero errors. Given Kerf's documented monotonically increasing order IDs starting at 1, the contract appears unused for placing range orders as of that block. **Do not keep attempting to harvest its nonexistent orders.** This is evidence from a user-provided report, not an independently repeated RPC verification; see [saved input](evidence/kerf-rangeorders-4663-block-86104491.json). The scan took no actions and spent nothing.

Further research is prioritized in [candidate triage](docs/CANDIDATE_TRIAGE.md). No verified real income exists yet. Other Kerf contract mechanisms are **not** disproved by RangeOrders' empty counter.

## First verified caller payout receipts: Superfluid on Base

We found successful *historical* transfers from Superfluid's Base batch-liquidator to an external submitting caller, on **May 9–10, 2026**. One was economically promising before token conversion; a second lost money versus gas alone. These are **not** proof of an open bounty now. See [receipts evidence](evidence/superfluid-base-2026-05-samples.json) and [research notes](docs/RESEARCH_LEDGER.md).

Read-only receipt verification (no wallet or keys):
```sh
make test
make superfluid-receipts
```

`superfluid_receipts.py` reads Base chain ID and two existing transactions via `eth_getTransactionByHash` and `eth_getTransactionReceipt`, extracts ERC20 ETHx transfers to the submitting caller and reported gas/L1 fee. It **never broadcasts**. It intentionally does not calculate profits from unverifiable token prices. For missing L1 fee, it flags an incomplete fee assessment. Use a third-party RPC only if it supports these methods; shared public RPCs may be rate limited.

## Check recent Superfluid liquidation activity (no wallet)

Superfluid's official `AgreementLiquidatedV2Event` subgraph schema includes transaction hashes, caller and reward receiver addresses, token addresses, timestamps, and raw reward amounts. A new standard-library Python observer queries the **last 30 days**, samples the most recent events and reports caller concentration:

```sh
make superfluid-activity
# or: python3 superfluid_activity.py --network base-mainnet --days 30 --limit 300
```

The output is `superfluid_activity.json`; it is gitignored. A saturated sample is flagged (`sample_may_be_truncated`). The subgraph has only indexed event history: it **does not** establish any live stream insolvency or an opportunity to claim; receipt-level token transfers and current chain state must still be checked. The endpoint is public but availability and freshness are unverified here.

Additional networks: `--network arbitrum-one`, `--network optimism-mainnet`, `--network polygon-mainnet`. Celo remains excluded from the initial security-sensitive investigation.

**Critical interpretation rule:** the indexed event's `liquidatorAccount` can be the Superfluid **Batch Liquidator contract**, rather than the externally owned submitting wallet. This is proven in the May 9 Base transaction: indexed `liquidatorAccount=0x6b008BAc...`, but tx sender and actual ETHx recipient is `0xC20a5455...`. Treat indexed account concentration as *contract/event routing*, **not** executor competition. The script labels this explicitly; to measure human/bot-initiator concentration, enumerate transaction hashes and inspect `tx.from`, `eth_getTransactionReceipt`, and actual token transfers.

## Second user-returned evidence (October 11, 2026)

The 30-day query captured its **maximum 300 indexed Base Superfluid liquidation events**, from September 26 to October 11. They correspond to **270 unique transaction hashes**. Period codes map to 40 Patrician (reward intended for priority recipient), 231 Pleb, and 29 Pirate events. Indexing the Batch Liquidator as `liquidatorAccount` is **not** a count of competing transaction submitters.

ETHx accounts for **46 indexed events**, **35 unique transactions** and **0.031339692062159336 ETHx indexed rewards** in the *captured sample* before gas and conversion. Two October 8 events contribute **90.26%** of that ETHx total; their actual ERC20 transfers to submitters still need receipt verification. Do not confuse this with the full 30 days or with realizable USD proceeds.

Evidence: [full activity](evidence/superfluid-base-2026-10-11-activity-full.json), [user's RPC receipts](evidence/superfluid-base-2026-05-receipts-rpc.json), [derived summary](evidence/superfluid-base-2026-10-11-analysis.json).

**Follow-up read-only receipt cross-check** for the largest and most recent ETHx liquidations:

```sh
git pull
make test
make superfluid-recent
```

This checks up to 12 deduplicated Base transactions, prioritizing the biggest observed ETHx reward amounts and recency. The resulting local `superfluid_recent_receipts.json` is ignored by git. It explicitly reports transferred token units, gas and a *hypothetical* ETH-parity proxy—**not earnings or live claimability**.

## October 2026 payout audit: decision after receipt verification

We received a read-only Base receipt audit of **12 of the 35 distinct ETHx liquidation transactions** captured in the truncated October subgraph sample. **All 12 transactions succeeded**, but the executor economic proxy splits **six positive / six negative**. The sample was intentionally selected by largest bounty and recency, so its apparent profitability is **selection-biased**.

- Received by submitting wallets: **0.030309319221334120 ETHx**.
- Full reported transaction fees: **0.000223981813189343 ETH**.
- Net proxy at assumed 1 ETHx ≈ 1 ETH: **+0.030085337408144777 ETH-equivalent** across the selected 12 historical calls, *not* verified dollar profit.
- Wallet `0xa4dd…fc41` submitted five positive transactions totaling **+0.029372300769558454 ETH-equivalent** after fees; `0xc20a…47f3` submitted six negative ones totaling **−0.000036079741400214**; one other wallet was positive.
- 1 of 12 calls had indexed ETHx rewards but **no direct ETHx transfer from the batch contract to the submitting wallet**; other beneficiary routing is not excluded.
- In the full 300-event index, 52 USDCx events account for ~127.84 USDCx, but **127.77 USDCx** were Patrician-priority rewards. Public Pleb-phase indexed rewards are only **~0.06926 USDCx**. A further 14 events totaled 923.98 SUP tokens, whose value is price/liquidity-dependent.

**Conclusion:** Superfluid is legitimate, liquidations happen, and bots can collect them. This audit does **not** support a reliable rapid $1,000 path with a $10 risk budget. Treat **Base ETHx as an observational learning channel**, not an execution-ready strategy.

Saved proof: [uploaded receipt report](evidence/superfluid-base-2026-10-recent-receipts-rpc.json), [reproducible derived calculations](evidence/superfluid-base-2026-10-receipt-analysis.json), [decision record](docs/OCT_2026_DECISION.md).

Optional full-sample audit (no wallet, 35 historical ETHx transaction receipts; RPC rate limits may apply):

```sh
make superfluid-all
```

## Next read-only Gate-0 candidate: PoolTogether V5 Base

Official current Base contracts pay fee recipients for permissionless prize claims. Recent current-deployment reward receipts must still be proven; older claimer is deprecated. Run `make pooltogether-check` (read-only, 6h) for a first current event sample. See [research and ABI warnings](docs/KEEPER_ALTERNATIVES_2026_10_12.md). No wallet or funds needed.

**POOL token valuation warning:** the PoolTogether claim reward is denominated in the PrizePool's own prizeToken() (looked up via read-only eth_call), not automatically in POOL governance-token units. The historical scanner also flags transactions whose destination is the current documented Claimer versus another address.

## Automatic GitHub Actions — read-only radar

Configured three GitHub Actions workflows: **Protocol Tests** (push/PR), **Protocol Radar** (roughly twice hourly at :17 and :47 UTC, plus manual trigger), and **Protocol Opportunity Alert** (runs after completed valid radar run, with issue-only write permission). No private keys, wallets, signing or transaction sending.

Radar collects a 6-hour recent **PoolTogether Base** ClaimedPrize sample (on-chain accrued fee/receipt evidence) and a 3-day **Superfluid Base** liquidation activity sample. Ripe is explicitly not implemented until deployment and real-payout proof. Network errors are recorded as **incomplete**, never as zero payout; every run stores read-only JSON reports as GitHub artifacts for 7 days. Alerts are strictly **research-only**, deduplicated and suppressed without verified current-claimer fee receipts. They are not buy/sell instructions or execution-ready signals.

Read [automation operations and limitations](docs/GITHUB_ACTIONS.md). To run now: GitHub **Actions → Protocol Radar → Run workflow**. Scheduled runs may be delayed; they are unsuitable for winning sub-second liquidations.

**PoolTogether automation backend (revised):** GitHub Actions now uses [pooltogether_subgraph.py](pooltogether_subgraph.py), reading recent `prizeClaims` from the official PoolTogether Base Graph Studio endpoint and cross-checking selected completed transactions against on-chain PrizePool receipt logs. The earlier [pooltogether_claim_history.py](pooltogether_claim_history.py) remains available for manual raw log scans where `eth_getLogs` is supported; public Base RPC endpoints rejected those log scans in live CI. An index query alone never triggers an alert without actual valid receipts to the current Claimer.

## First fully operational GitHub Radar result — 2026-10-11

[Successful smoke run](https://github.com/ahmedelgaml70/protocol/actions/runs/38177465238): 41 offline tests passed in a separate CI run; both scheduled-scanner components produced valid JSON. PoolTogether official Base index returned **0 prize claims in the trailing three days** (index one block behind chain tip) and resolved the actual prize token to Base WETH `0x4200000000000000000000000000000000000006`. This is **not a claim that the protocol never pays**, only that the indexed bounded period was quiet. Superfluid returned **52 indexed liquidation events in three days**. Ripe remains unimplemented. No wallets, keys, financial transactions or profit. [Reproducible baseline summary](evidence/github-actions-smoke-2026-10-11.json).

**Candidate update, October 12:** A fresh [30-day PoolTogether Base index](evidence/pooltogether-base-30day-2026-10-11.json) returned no `prizeClaims`, so the Base claimer is a passive watch, not a demonstrated recurring income source. Next researcher lead is Beefy public harvest caller incentives, but its own Cowllector bot already competes and a historical Base example had gas greater than the illustrated receiver payout. No money actions are enabled.

**Verified alert pipeline smoke:** GitHub Actions successfully downloaded a real radar report, evaluated 0 qualifying signals and created 0 issues ([run](https://github.com/ahmedelgaml70/protocol/actions/runs/38177999974)). The production issue-writing branch remains untested until a genuine positive research signal appears. PoolTogether Base was deprioritized after zero indexed claims in 30d; [Beefy harvest research #6](https://github.com/ahmedelgaml70/protocol/issues/6) is a fresh read-only candidate, not verified income.

## Beefy operator economics added to automated Radar

Beefy's maintained Cowllector v2 publicly documents a last-harvest-reports API. Radar now uses beefy_cowllector.py to screen the LAST report per vault for Base, Arbitrum, and Optimism, retaining estimated caller-fee, gas-cost and reported outcome fields as a third transient artifact. These are the incumbent bot's own simulated estimates, not independent wallet earnings or live opportunities. No Beefy alert/execute path was added.

API source: https://github.com/beefyfinance/beefy-cowllector-v2/blob/main/apps/api/README.md . Use docs/GITHUB_ACTIONS.md for limitations.

**Actual Beefy receipts (Oct 12):** 7/7 recent existing Cowllector Base harvest transactions succeeded but ALL paid less WETH to the submitting bot than its receipt-reported gas cost. Totals: 0.000011705879359994 WETH received, 0.000056682286523025 ETH gas, conditional −0.000044976407163031 ETH-equivalent after gas. All sent by one existing bot. This directly verified negative example **reinforces not deploying a harvest bot**. See [evidence](evidence/beefy-base-2026-10-12-receipt-proof.json) and [decision](docs/RESEARCH_LEDGER.md). No third-party profit and no user spend.

## Read-only Ripe Base deployment and keeper receipt checks

The repository now runs `ripe_base.py` in two separate GitHub Actions stages: **deployment code presence** (Ripe official Base v1 manifest Teller, AuctionHouse, GREEN, sGREEN, MissionControl) and **6-hour historical LiquidateUser event + receipt audit**. Payout verification accounts for **both GREEN and default sGREEN**, and only treats positive ERC-20 incoming transfers/minted shares to the real tx sender as historical credit evidence. KeeperFee event values, transaction gas (ETH) and GREEN/sGREEN reward amounts are **not directly comparable** without market-value conversion and redemption. Explorer/RPC failures are marked incomplete, not zero payouts. No keys, no transactions, no execution bot.

**Ripe live Base proof (Oct 12):** Current Teller/AuctionHouse/MissionControl unpaused and `canLiquidate=true`; fee config 1% of debt, nominal 1–25,000 GREEN, subject to debt/collateral caps. This is *not income*. Primary+free explorer historical logs unavailable; fallback keyless RPC providers under test. [Exact snapshot](evidence/ripe-base-2026-10-12-state.json).

## Ripe 24-hour empirical screen

[Daily Ripe Keeper Evidence](https://github.com/ahmedelgaml70/protocol/actions/runs/38213678949) successfully queried **43,201 consecutive Base blocks (52,455,744–52,498,944)**, observing **0 current AuctionHouse LiquidateUser events** in 24 hours. No RPC failures or payouts in this bounded period. The mechanism was enabled (1% configured) but had no observed work. **Ripe Base downgraded for rapid-income purposes;** daily low-rate research remains optional. [Permanent evidence summary](evidence/ripe-base-2026-10-12-24h-history.json). Not a claim no payouts ever.

## Morpho Base liquidation activity read-only screen

Following repeated low-activity / low-profit results for smaller permissionless keeper mechanisms, `Protocol Radar` also checks **historical Morpho Blue Base liquidations** from Morpho's official free [GraphQL API](https://docs.morpho.org/developers/borrow/tutorials/get-data/) using `morpho_liquidations.py`. It records the newest up to 100 Base liquidation events and caller concentration with a seven-day filter, distinguishing a capped sample. The returned `repaidAssets` and `seizedAssets` are **in different token units**, not cash profits. No active borrower is found, no flash loan executed, and there are no Morpho research alerts until independently verified positive-net receipts. A funded liquidation requires loan-token repayment; atomic flash liquidity can sometimes help but creates technical and execution risks.

## On-chain receipt-backed Morpho Blue investigation (October 12)

Following a successful [official Base Morpho GraphQL sample](https://github.com/ahmedelgaml70/protocol/actions/runs/38214499956) of **100 unique liquidation events in 37 transactions** (a capped sample, not the full 7 days), the [read-only on-chain receipt audit](https://github.com/ahmedelgaml70/protocol/actions/runs/38214906472) confirmed **8/8** selected transactions were successful and matched indexed `Liquidate` events, including market, log index, indexed caller, and raw repaid/seized token amounts. All 8 `Liquidate.caller` addresses were contracts different from `tx.from`; 7 distinct submitting wallets. Full Base gas for selected 8 transactions was **0.000550241901468437 ETH** in aggregate—historical cost, **not profit**. The audited calls are completed, not available. [Permanent findings](evidence/morpho-base-2026-10-12-proof.json) · [Research gate issue #7](https://github.com/ahmedelgaml70/protocol/issues/7). **70 offline tests passed** after a synthetic fixture correction.
