# Keep3r V2 funded-job and live payouts audit — 12 October 2026

**Objective:** Seek $900 net gain on top of the user's $100 starting capital by Nov 12, 2026, without client acquisition, speculative trading, account breaches, or premature transactions. **No user funds spent, no verified user earnings.**

## Deployment and reproducibility

- Canonical Ethereum Keep3r V2 registry: `0xeb02addCfD8B773A5FFA6B9d1FE99c566f8c44CC`.
- Official job docs: https://docs.keep3r.network/core/jobs
- Official keeper eligibility: https://docs.keep3r.network/core/keepers
- Official job registry: https://github.com/keep3r-network/job-registry/blob/main/v2.json
- Observer: `research/keep3r/keep3r_funding.py`, `research/keep3r/keep3r_activity.py`.
- CI: `.github/workflows/keep3r-funded.yml`, with strict read-only Ethereum JSON-RPC, pinned eth-abi/eth-utils/pycryptodome, safety tests, results artifacts, GitHub token contents:read. No transaction signing/sending or secret keys.
- Successful credit scan: https://github.com/ahmedelgaml70/protocol/actions/runs/38262159290
- Successful historical receipt/economics scan: https://github.com/ahmedelgaml70/protocol/actions/runs/38263077386
- Main branch unchanged; research branch is `research/keep3r-funded-credit-100`.

## Empirical Ethereum state (at ~14:28 UTC Oct 12, 2026)

Registry lists **42 jobs**. All 42 read successfully in the later scan (0 RPC per-field errors). Six jobs had positive observed KP3R liquidity credits or direct ERC-20 job credits.

| Registered job | Recorded job credits | Latest workedAt UTC | Assessment |
| --- | --- | --- | --- |
| `0x5D469E1ef75507b0E0439667ae45e280b9D81B9C` | 19,881.72684723384 DAI plus KP3R credits | 2026-06-05 21:00:23 | Official registry: MakerDAOUpkeep; governance retired Keep3r execution lane June 8, 2026; **not claimable by us** |
| `0xf4F748D45E03a70a9473394B28c3C7b5572DfA82` | ~3,909 KP3R job liquidity credits | 2026-10-12 12:20:59 | **Only recently working job in latest bounded sample**, Yearn-style harvest; no current newly eligible call proven |
| `0x220A85Bcd2212Ab0B27EFD0dE8B5e03175f0aDEE` | ~395.9 KP3R credits | 2026-04-16 | Stale activity |
| `0xDEE991cBf8527a33E84a2aaB8a65d68d5d591BAA` | ~263.9 KP3R credits | 2024-04-06 | Stale activity |
| `0x1f5F0DA9391ab08C7F0150D45B41F6900fB4fD0c` | ~306.1 KP3R credits | 2025-07-17 | Stale activity |
| `0xe74379eD6e94c85da90d27b92df670Db282995aF` | ~28.5 KP3R credits | 2026-08-16 | Stale activity |

### Historical actual keeper payouts, 7,200 latest blocks

The Ethereum registry emitted **20** verifiable `KeeperWork(credit,job,keeper,payment,gasLeft)` events, all for `0xf4f748...`. All 20 corresponding successful transaction receipts were inspected.

- Payment token was KP3R at `0x1cEB5cB57C4D4E2b2433641b95Dd330A33185A44`.
- **Total historical gross payment: 58.923388859722181751 KP3R**.
- **Average: 2.946169442986109087 KP3R** per paid work event.
- Minimum per call 2.241201708011726422 KP3R; maximum 3.923271446081767336 KP3R.
- Two keeper addresses won **all 20**: `0xda27e18bef83bcf38197b6120a78c15319534d43` 16/20 and `0x9fbdcd966fcd54382277a33b185c970fba22b28e` 4/20.
- Combined receipt gasUsed*effectiveGasPrice for those transactions was **0.013478222435865014 ETH**, average 0.0006739111217932507 ETH per transaction. This is gas charged in these prior successful receipts, not total cost of unsuccessful competing attempts, and sender may not always equal beneficiary.
- This is **historical**; no wallet under the user's control received any of it, and credits are not a public faucet.

Illustrative, **not actual realized USD profit**: using around $0.9352/KP3R as an Oct 12 market reference (CoinCodex) and ~$2,545.78/ETH (Investing.com Binance historical record), the 20 payments would represent approximately **$55.10 gross** and **$34.31 observed successful transaction gas**, leaving **$20.79 theoretical difference** split across incumbents before unbonding, transaction competition, failed attempts, price/volume slippage, swap fees and taxes. This is a sanity check, not trading advice. The reported KP3R 24-hour trading volume was only about $247 on CoinCodex on Oct 11–12, emphasizing exit liquidity constraints. Sources:
- https://coincodex.com/crypto/keep3rv1/historical-data/
- https://www.investing.com/crypto/ethereum/eth-usd-historical-data
- https://github.com/keep3r-network/keep3r-network-v2
- https://etherscan.io/tx/0xd71f5235d5a18fd618852dca045057349c4a94444445a7b269764301b1197bc0

### Disqualifications and caution

**MakerDAOUpkeep** has ~19.9k DAI earmarked in Keep3r credits, but the official **Sky governance executive action removed the Keep3r CRON_SEQUENCER lane on June 8, 2026**, consistent with the last workedAt timestamp June 5. The funded DAI is *not* a right to withdraw it or proof work can be done. Official proposal:
https://vote.makerdao.com/sky-executive/template-executive-vote-rwa001-a-offboarding-keeper-network-adjustments-allocator-spark-a-parameter-updates-mkr-to-sky-delayed-upgrade-penalty-increase-prime-agent-proxy-spells-june-4-2026

**Active job 0xf4...** has historical `KeeperWorked(strategy)` and strategy harvest events consistent with Yearn-type automation. New-keeper eligibility is **not verified**. Some Yearn Keep3r contracts require at least **50 bonded KP3R** and/or substantial stealth deposits; DO NOT conflate different contract addresses. The official Yearn StealthHarvest contract with a documented 1 ETH Stealth Vault requirement is **0x2150...**, and the ordinary older HarvestV2 job is **0x620b...**; neither equals **0xf4f748...**. Therefore the exact new-keeper bond/access/callable parameter for 0xf4... still requires source-to-bytecode matching and execution simulation before any approval to transact. 
- https://github.com/yearn/keep3r-jobs/blob/master/doc/HarvestV2Keep3rStealthJob.md
- https://github.com/yearn/keep3r-jobs/blob/master/doc/HarvestV2Keep3rJob.md

## Decision

The search has crossed **two significant evidence gates**: on-chain funding and **historical actual successful rewards**. It **has not** crossed the distinct gates of presently executable work, affordability for a fresh keeper with $100, winning ability, timely liquid payout, and repeatable $900 net.

**Keep3r 0xf4... = best currently active paid-job research target, but not investment-ready.** Observe its verified contract source and permission checks; read-only simulate potential work. Do NOT claim a 'hidden $19,881' opportunity. Do NOT bond KP3R, buy ETH, send, or approve without user authorization. Leave the user capital untouched. If no affordable eligible work is verifiably open, stop development and rotate to other economic models.

## Additional live eligibility check (Oct 12, ~14:39 UTC)

- New no-wallet probe: `research/keep3r/keep3r_preflight.py`.
- GitHub Actions: https://github.com/ahmedelgaml70/protocol/actions/runs/38264464096
- Decoded **20** job-specific `KeeperWorked(address)` events in the recent historical block range, representing **19 distinct strategy contracts**.
- Current-state `eth_call` to **`workable(address)`** succeeded for all 19, and **all returned `false`**.
- The script therefore submitted **zero** dummy-caller `work(address)` simulations; there was nothing flagged workable at the observation block.
- This is an actual block-specific negative finding for those 19 previously active strategies. It **does not** prove no new or previously unworked strategies could become eligible, or that they will not become workable in future.
- **Current directly identified positive-net work: zero.** Continue to reject gas spends, staking or keeper registration before a realistically accessible positive-net call is observed. The existing record of 20 paid transactions is historical and cannot be collected retroactively.
