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
