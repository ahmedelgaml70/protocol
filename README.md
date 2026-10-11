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
