# Opportunity matrix and decision ledger
**Snapshot:** 2026-10-12. **Goal:** $100 operating capital → **$1,000 total available cash** by November 12, 2026, aspirational only. **User cash earned: $0. Money spent: $0.**

Read [canonical handoff](HANDOFF_2026-10-12.md) and [research playbook](RESEARCH_PLAYBOOK.md). This is a **snapshot of investigations**, not an evergreen assertion about opportunities. Incomplete scans are NEVER to be interpreted as zero activity. Prior source links and the underlying documents remain linked below.

## Verdict definitions
- **STOP:** clear disqualifier (not genuinely funded, closed, wrong payout timeline, excessive risk, unsafe, lack of realistic economics); revisit only for a new material fact.
- **WATCH:** real mechanism / paid history, no presently verified opportunity, possibly feasible in future.
- **RESEARCH:** particular uncertainty is worth a cheap read-only check; do not treat as executable.
- **CONDITIONAL:** violates user's strict no-tasks or no-clients preference; only user-approved exception.
- **READY:** current task/reward validated through funding, eligibility, actual payment proof, net and payout timing. **No candidate is READY.**

## A. DeFi and permissionless contract mechanism evidence

| Candidate | Source-level mechanism | What was actually observed | Principal blocker | Verdict and proof |
|---|---|---|---|---|
| Kerf RangeOrders (Robinhood 4663) | Claimed 1% caller fill bounty | User-returned block 86,104,491, nextOrderId=1, zero orders; see main evidence | No created orders in observed contract | **STOP this contract** [source](https://github.com/KerfFinance/kerf-contracts), [JSON](../evidence/kerf-rangeorders-4663-block-86104491.json) |
| Other Kerf harvests/perps | PositionKeeper ≤3% harvested fees, LPVault 0.5%, PreMarketPerp 1% of eligible margin | Source-verified bounty declarations, not independent profitable current payout | Activity and true deployed state unverified | **RESEARCH only if new paid evidence** [details](RESEARCH_LEDGER.md) |
| Superfluid Base | Distressed stream liquidation rewards | Oct 11 capped index: 300 events / 270 tx; Oct 12 targeted 12 historic ETHx receipts, six positive/six negative under imperfect parity proxy | Priority routing, bot concentration and stale closed historical claims | **WATCH, not spend** [decision](OCT_2026_DECISION.md), [receipts](../evidence/superfluid-base-2026-10-receipt-analysis.json) |
| PoolTogether V5 Base | Permissionless prize claims and recipient fee | Official index zero `prizeClaims` in sampled 30 days; prize token Base WETH | No recent observed payout activity | **STOP until material activity** [index](../evidence/pooltogether-base-30day-2026-10-11.json) |
| Beefy harvest | Caller `harvest()` fee documented | 7 successful past Base Cowllector receipts; caller fee below gas in all seven observed | Official competing harvester, negative historical gross economics | **STOP** [receipt proof](../evidence/beefy-base-2026-10-12-receipt-proof.json) |
| Ripe | External liquidation/caller incentive | Incentive state verified; 24-hour Base event scan returned zero | No actually paid current reward found | **STOP** [24h](../evidence/ripe-base-2026-10-12-24h-history.json) |
| Morpho Blue Base | Permissionless liquidation incentives | 100 historical liquidation events, 37 unique tx; eight inspected receipts; historical present-price spread not actual profit | MEV, debt funding/flash loan, exit asset and gas, no now-eligible target | **WATCH** [receipts](../evidence/morpho-base-2026-10-12-proof.json), [valuation warning](../evidence/morpho-base-2026-10-12-current-reference-screen.json) |
| 0xSplits V2/V2o1/V2o2 | Distributor share of properly executed revenue distributions; Push/Pull differ | Three chain, three factory version, four narrow historical samples; no qualifying reward screens in successfully scanned windows | Existing bots and historic RPC gaps; incomplete coverage | **STOP expansion** [PR #8](https://github.com/ahmedelgaml70/protocol/pull/8), [audit](https://github.com/ahmedelgaml70/protocol/blob/research/splits-100/docs/SPLITS_CROSSCHAIN_AUDIT_2026_10_12.md) |
| Liquity V1 and V2 | V1 200 LUSD + 0.5% ETH; V2 0.0375 WETH + conditional collateral reward | Short 24h sample: 0 `Liquidation` events in 4 tracked contracts; V1 lowest ~12 troves 0 eligible simulations | Infrequent eligible liquidations, costly Ethereum gas, RPC blocks 7-day scans | **WATCH** [PR #9](https://github.com/ahmedelgaml70/protocol/pull/9), [audit](https://github.com/ahmedelgaml70/protocol/blob/research/liquity-compensation-100/docs/LIQUITY_COMPENSATION_AUDIT_2026_10_12.md) |
| Sovryn Zero / Rootstock | 20 ZUSD + 0.5% RBTC compensation | Current up-to-12 lowest-ratio troves: 0 candidates; official deployed bytecode; 3 free endpoints cannot provide full history | No live target observed and no reliable historic paid sample | **WATCH** [PR #9](https://github.com/ahmedelgaml70/protocol/pull/9), [audit](https://github.com/ahmedelgaml70/protocol/blob/research/liquity-compensation-100/docs/SOVRYN_ZERO_ROOTSTOCK_AUDIT_2026_10_12.md) |
| Keep3r V2 Ethereum (registry) | Credits escrowed by registered jobs, emitted `KeeperWork` payment | 42 jobs; six credited; 20 actual historic payments to two keepers; active `0xf4f748...` job 19 past strategies all currently not-workable | Economic capture already won by 2 incumbents, keeper registration/access and exit illiquidity, no open action | **WATCH / best documented funded lane, NOT READY** [PR #10](https://github.com/ahmedelgaml70/protocol/pull/10), [audit](https://github.com/ahmedelgaml70/protocol/blob/research/keep3r-funded-credit-100/docs/KEEP3R_V2_FUNDED_WORK_AUDIT_2026_10_12.md) |
| Keep3r MakerDAOUpkeep | 19,881.726847 DAI job credits plus liquidity credits observed | Last on-chain worked June 5, 2026; Sky action removed keeper lane June 8 | Existing funds are not public to withdraw; work retired | **STOP** [official registry](https://github.com/keep3r-network/job-registry/blob/main/v2.json), [audit](https://github.com/ahmedelgaml70/protocol/blob/research/keep3r-funded-credit-100/docs/KEEP3R_V2_FUNDED_WORK_AUDIT_2026_10_12.md) |
| Aave / direct flash loan | Flash liquidity can temporarily finance liquidations | Official mechanism known; NO current executable US$900 reward found | Debt, atomic repay, auction risk, competition, gas | **RESEARCH only with specific live target** [docs](https://aave.com/docs/) |
| Atomic Arbitrum | Website advertises USDC.e liquidation bounty | No independent paying mainnet contract or recent receipt verified in session | Claim unverified; audit and execution path uncertain | **STOP** until bytecode and paid receipt verified |
| Velodrome Relay | Public late-epoch compounding incentive in VELO | Contract source formula inspected | Time gate and privileged early keepers; no net opportunity proven | **WATCH (low)** [contracts](https://github.com/velodrome-finance/relay) |
| Arcron Algorand | Public keeper from escrowed ALGO tasks | Official project says TestNet-only / upgradeable / unaudited | No real-money ALGO payout confirmed | **STOP for November cash** [source](https://github.com/CorvidLabs/arcron) |
| Soroban Keeper Network | On-chain escrow-funded task execution design | Public demo/testnet only in research | Mainnet paid job list unverified | **STOP for November cash** |

### Keep3r receipt economics: unusually high-quality data but no current target

- Job `0xf4f748d45e03a70a9473394b28c3c7b5572dfa82` emitted 20 successful KeeperWork events in recent ~7,200 Ethereum blocks, all with receipts inspected.
- Total **58.923388859722181751 KP3R**, mean **2.946169442986109087 KP3R**, per-call range **2.241201708011726422–3.923271446081767336 KP3R**.
- **Two keeper addresses** received all 20: 16 and 4. Combined tx gasUsed × effectiveGasPrice: **0.013478222435865014 ETH**, *excluding failed attempts and some intermediaries*.
- Previous Oct 12 market-reference illustration ~**$55 gross vs $34 gas** across incumbents. Prices/market depth must be refreshed before valuation; even this **does NOT represent user's earning**.
- Live read-only `workable(address)` for **19 distinct previously worked strategies** = false across all checked; no live candidate. [Run](https://github.com/ahmedelgaml70/protocol/actions/runs/38264464096).

## B. Token, farming, airdrop and speculative strategies

| Mechanism | Verified / proposed design | Disqualifier | Decision |
|---|---|---|---|
| FLOP testnet | Proposed 90-day testnet, genesis/mainnet early 2027, inference-based qualification, locks/agent-spend unlock | Rewards unlikely liquid by November 12; third-party SDK cannot prove official eligibility | **WATCH only long-term, $0 spend** |
| PERPTools | Point accrual/AI agents, prospective $PERP conversion; minimum active agent AUM about $30 | Unknown token exchange value, uncertain TGE and 1 USDC withdrawal fee; trading loss risk | **STOP as one-month cash** |
| Papertrade PAPER | Tokens minted for realized trading losses | Not equivalent to redeemable USD, oracle and pool risks, basis-neutral hedges can lose | **STOP no deposit** |
| Polymarket arbitrage | Mathematically documented yes/no odds imbalances | Execution/MEV, tiny capital, fees, no current verifiable exploitable quote | **STOP** |
| Robinhood Chain LP | Concentrated-liquidity fees | Impermanent loss, LVR, token price risk, TVL ≠ investor APY, $100 too little to scale | **STOP** |
| Meme/airdrops/rebates without funded claim | “points now, future tokens later” | Zero verifiable deadline liquidity, potential speculation/deposits | **STOP** |

The older user-provided promotional summary about FLOP, PERPTools, Papertrade, Polymarket and Robinhood Chain should be treated as **claims to verify**, not trusted factual source, including precise projections/ROI, secondary-market figures and rumored disqualification rates.

## C. Outside DeFi — direct provider work and digital payments

| Candidate class | Paid mechanism / first source | Blocker / what is missing | Status |
|---|---|---|---|
| PlaytestCloud | Published per-approved-game-test rates ($5–$9 typical 15min), invite-based payout | Work availability, think-aloud/recording, first payment and invitation frequency unknown | **CONDITIONAL (platform tasks)** [official](https://players.playtestcloud.com/article/118-how-much-money-will-i-earn) |
| GoTranscript Arabic | Advertises language-specific per-audio-minute compensation and weekly approved-task payouts | Testing/admission, audio supply, actual clock-hour compensation; conventional work exception | **CONDITIONAL** [official](https://gotranscript.com/arabic-transcription-job) |
| uTest / Userbrain / Speechpad | Provider-assigned QA/testing/transcription tasks, official payout methods | Qualification, available volume and short approval/withdrawal timeline | **CONDITIONAL, low confidence of $900** [prior notes](GLOBAL_INCOME_PIVOT_2026_10_12.md) |
| Paid open-source GitHub docs/bugs | Some verifiable programme rules and sponsor issue budgets | PR merge discretion, unconfirmed escrow, many copies/AI-generated issues, coding requirement, payee eligibility | **RESEARCH as exception** |
| Hashgraph Guardian | Official quarterly bounty programme; advertised docs $250–$500, features larger | No matching live `label:bounty` issue in connector query, quarterly payouts and coding scope | **STOP for monthly cash until real open issue** [official policy](https://github.com/hashgraph/guardian/blob/main/BOUNTY-PROGRAM.md) |
| Fastify | Official approved PR + expense process, suggested ~$50/hour bounty formula | No live bounty label issue found; funds approval and payment timing discretionary | **STOP** [policy](https://github.com/fastify/fastify/blob/main/EXPENSE_POLICY.md) |
| SUSU-LABS indexer issue #46 | GitHub currently shows open, offered **$40** for network-passphrase configuration correction | No independently verified payment escrow or payout rail and coding, first-month scale weak | **UNVERIFIED/NOT READY** [issue](https://github.com/SUSU-LABS/susu-indexer/issues/46) |
| sharmiaalono/go-github issue #5 | Open labelled **$10** and bountyhub, pagination fix | Low amount, dev complexity, no escrow/settlement receipt verified | **STOP** [issue](https://github.com/sharmiaalono/go-github/issues/5) |
| NSPG13 agent-bounties issue #1262 | Proposed 14.50 USDC developer reward | Issue explicitly says **UNFUNDED PRECOMMIT**, requires special verifier infrastructure | **STOP** [issue](https://github.com/NSPG13/agent-bounties/issues/1262) |
| Activepieces Algora old listings | Historical $100 rewarded issues exist | Example from 2025 already closed; current open bounty inventory not independently found | **STOP until active paying issue proven** |
| BountyBook, Algora board | Third-party May 2026 empirical research reports payout pipeline failure, Algora historical recruiter pivot | Independent study dated May 2026 cannot prove same status Oct 2026; verify current official payout before work | **WATCH only if payment resumes** [independent snapshot](https://github.com/ir272/autonomous-earning-experiment) |
| Cloudflare Pay Per Use | Published Sept 2026 publisher revenue beta, monthly settlement | Need content, accepted publisher, actual buyer use, potentially next-month settlement | **LONG-TERM** [prior notes](UNIVERSAL_CASH_HUNT_2026_10_12.md) |
| x402 paid API | Stablecoin automatic paid calls for consumer agents | Need differentiated paid service, active buyers; user does not want client demand | **CONDITIONAL / not next-month proof** |
| Honeygain/Mysterium capacity share | Rent bandwidth; third-party payments sometimes | Earnings tiny, geography/network demand, privacy/ISP risk and payout threshold | **STOP for $900 goal** |
| Stock/book/asset micro-resale | Need buyer/payment, platform terms, delivery rights | Inventory, customers, scams/fees; violates no-client/marketing constraints | **STOP unless exact verified buyer order** |

## D. Never repeat these methodological errors

1. **Advertising, token incentive %, TVL, treasury balances, APY, swap volume or quarterly prize budget are NOT a caller payout**. Do not claim a budget is public money.
2. A **historical paid tx is already captured**; it establishes mechanism but is not a claim.
3. **No RPC support → status=INCOMPLETE**, never 0. A bounded source-accurate 24h scan must not be claimed to cover 7d or all contracts.
4. **Keepers concentrate** and may require KYC, staked collateral, expensive gas or private priority rights; model true entrant value rather than incumbent average.
5. **Claiming someone else's refunds/royalties/rewards is not allowed**. Never ask for or assume their wallet ownership or eligibility.
6. Respect exclusions, especially **no security bug exploitation, no contest entry, no deliberate trading loss / oracle manipulations, no cold outreach**.
7. No external action without user approval: wallet signing, account registration, GitHub outside PR, applying, emailing, spending, moving money, or merging research branches.

**Verdict for the overall goal as of 2026-10-12:** none READY; $100 preserved; $0 realized. See [handoff](HANDOFF_2026-10-12.md) for recommended continuation.


## E. Explicit payment-rail falsification: bounty marketplace UI ≠ escrow (2026-10-12)

1. **Opire current official payment terms**: [Opire Costs & Payments](https://docs.opire.dev/rewards/pricing) explicitly states: "Creating or claiming a bounty does not create an automatic payment." The developer submits a PR; the **individual bounty creator decides whether work meets requirements and arranges payment directly**. Therefore the Opire bot/issue badge is NOT evidence of held funds or an automatic Stripe payment. An older third-party May 2026 directory described Stripe Connect payouts, but the current first-party terms take precedence. **Status: STOP unless the particular sponsor's verified funds, jurisdiction, terms and payment arrangement are independently established before work.**
2. **openbounty.ai**: The public homepage displays seemingly "funded" issues ($800, $250, etc.) and counts, but explicitly says **"Mock-payments mode — no real funds move during MVP."** These cards are NOT executable funded cash offers. **Status: STOP until the platform demonstrates live payouts with transaction/processor evidence.** [Source](https://openbounty.ai/).
3. **Open Collective expenses**: Even when an expense is publicly visible, it may be **Pending** rather than paid, and administrators/fiscal hosts can approve or reject it. Example publicly posted Oct 9, 2026 [$200 invoice](https://opencollective.com/ofitech/expenses/349784) shows pending status and is for a SECURITY bug report, which is also excluded by user constraints. Do not treat an invoice or collective balance as money already transferred.
4. **Bounty programme vs available task**: Hashgraph Guardian's programme specifies quarterly accounting and Fastify's bounty terms require accepted PR and expense approval; no current open funded task from our narrow GitHub label queries. No immediate earnings established.

**New universal gate:** Payment-platform badges, issue labels, "funded" UI cards and finance dashboards are treated as marketing until (a) a specific payer has demonstrably reserved/paid funds, (b) an accepted contribution and recent *cleared* payee transaction are verified, and (c) the current claimant's eligibility and cash timeline are documented. Never start unpaid PR work based on screenshots of a platform's demo feed.
