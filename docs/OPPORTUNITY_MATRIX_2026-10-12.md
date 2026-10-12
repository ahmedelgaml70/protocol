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


### E.2 Stripe Express and region-dependent payout traps (new check)

- [Bountymin GitHub App](https://github.com/apps/bountymin-bot) self-advertises a seven-day Stripe Express escrow process and coverage in 115+ countries. **No specifically verified, currently open, funded issue, recent actual recipient payout or Egypt-supported onboardable account was established.** Marketing is not a positive G0–G4 verdict.
- [Stripe published general country availability](https://stripe.com/global) does **not list Egypt**. However, standard merchant account availability and Stripe **Connect recipient** payout eligibility are NOT necessarily identical. An individual platform might have a permitted cross-border flow; verify the exact platform/Connect country settings rather than assuming universal rejection.
- [Stripe Connect stablecoin payout supported-country list](https://docs.stripe.com/crypto/stablecoin-payouts) also omits Egypt in the published list, and currently only US Connect platforms can send stablecoin payouts. Do not propose a default "just take Stripe USDC" workaround.
- [Stripe opening an account in another country](https://support.stripe.com/questions/requirements-to-open-a-stripe-account-in-another-country?locale=en-GB) ordinarily requires a genuinely registered entity, tax details, physical premises and supported bank account; no fictitious residence or identity workaround.
- **Status:** Bountymin and generic Stripe-only bounty platforms are **NOT READY** for this user until the specific recipient onboarding and last successful payout are verified; do not treat location as an absolute prohibition on other payout channels.


## F. Four more models falsified or gated (October 12, second research round)

Full contract/read-only primary source + dated independent market measurements: [RESEARCH_ROUND2_RELAYER_AGENT_MARKETS_2026_10_12.md](RESEARCH_ROUND2_RELAYER_AGENT_MARKETS_2026_10_12.md).

| Mechanism | What actually transfers value | What a new participant could receive | Status |
|---|---|---|---|
| Hyperlane `InterchainGasPaymaster.claim()` | All contract fees → **configured beneficiary**, NOT `msg.sender`; `setBeneficiary` owner-only | **$0 merely calling `claim`**. Relaying for own registered paying routes requires demand, infrastructure and gas | **REJECT public-claim hypothesis** [mainline source](https://github.com/hyperlane-xyz/hyperlane-monorepo/blob/main/solidity/contracts/hooks/igp/InterchainGasPaymaster.sol) |
| Archr.fun new Robinhood Chain 1% cranks | 1% of actual *processed* protocol fee leg for pool fee collection, reward conversion, holder delivery | Unknown; primary docs indicate existing platform bot, small app-level cached history and no current measured outstanding fees | **WATCH only, no bot** [official rewards docs](https://archr.fun/docs/rewards) |
| TaskMarket USDC escrow tasks | Worker receives **92.5% of reward only if accepted/awarded** under default 7.5% fee | Unknown currently; external Oct 10 audit sampled 7 open / 84 new in prior 30d and ~$0.025 expected reward per attempt, cost estimate larger for normal models; no direct user task claim verified | **CONDITIONAL but scale fails** [official fees](https://docs.taskmarket.dev/concepts/fees-payments), [dated independent audit](https://shaduf.ai/p/agentic-freelance/opportunities/) |
| x402 pay-per-call API | Only actual unrelated buyer requests pay USDC to hosted endpoint | No guaranteed requests; September x402stats threshold filtered to 78/19,015 organic sellers and ChainWard traced self-funded buyer loops | **CONDITIONAL service model, not client-free money** [Sep market audit](https://x402stats.io/reports/2026-09), [loop evidence](https://chainward.ai/decodes/x402-on-base) |

**Critical math check:** Independent Shaduf Oct 7 sampled ~$212 in *combined agent-worker payouts* over 30 days in its surveyed board set; a new participant making $900 would have to earn **>4× that entire observed sample**, before any task-work model cost, acceptance or market growth. This is a **comparative scale warning, not a ceiling on the future agent economy**. Current TaskMarket API was not directly accessible via the external research environment; no independent live open-task count established.

**Core source check:** Hyperlane IGP contract explicitly transfers fee balance to `beneficiary` on public `claim()`. This is a decisive counterexample to the false heuristic "public claim method + funded contract = anyone earns the balance". The caller may spend gas without receiving funds.


## G. Live Convex / Aura / Solana program audit — 12 October (latest continuation)

[Detailed source and scan report, draft PR #11](https://github.com/ahmedelgaml70/protocol/blob/research/convex-earmark-100/docs/CONVEX_KEEPER_KICK_AUDIT_2026_10_12.md). [Research PR](https://github.com/ahmedelgaml70/protocol/pull/11), [successful short Booster + kick history run](https://github.com/ahmedelgaml70/protocol/actions/runs/38277038085), [incomplete historic eligibility run](https://github.com/ahmedelgaml70/protocol/actions/runs/38277359911). **13/13 offline safety tests passed; no wallet action.**

| Candidate | Actual recent on-chain evidence | Gating deficiency and status |
|---|---|---|
| **Convex Finance Ethereum \`earmarkRewards(pid)\`** | Deployed Booster official address checked; not shut down, **583 pools**, live caller incentive **50 bps (0.5%)**. A narrow latest-800-block sample had **30 CRV outgoing transfers** over **4 tx**, but **none directly paid \`tx.from\`**. All four outer calls targeted intermediary contracts; this filter cannot capture their ultimate payout routing. | **WATCH/NOT READY**. A source-level \`msg.sender\` incentive is real, but we have **not verified a current unharvested pool, executable reward or independent net payout**. The first 7,400-block sample exceeded a cap (INCOMPLETE); 800-block sample completed. |
| **Convex V2 \`kickExpiredLocks(account)\`** | Official deployed locker checked; live \`kickRewardPerEpoch=25/10000\` = **0.25% per overdue epoch**, grace \`4\` weekly epochs. **Zero \`KickReward\` events** in completed ~7,400-block on-chain sample. | **WATCH/UNKNOWN current eligibility**. A separate three-window search for stale accounts (160d, 205d, 270d) was **INCOMPLETE** due free historical RPC HTTP 400/525. **Never report zero kickable holders** from zero returned logs on failed API calls. | 
| **Aura Finance \`earmarkRewards\`** | Older official docs showed 0.5% third-party harvest, but [current official app](https://app.aura.finance/) declares **Aura Sunset** and pools withdrawal-only; [Balancer BIP-928](https://forum.balancer.fi/t/bip-928-orderly-winddown-of-balancer-and-distribution-of-the-treasury/7107/23) approved September 29 with October 30 wind-down dates. | **STOP for new recurring harvest strategy**. Old mechanism does not imply fresh emissions.
| **Dead Man's Vault (Solana)** | Github project describes default 0.005 SOL keeper bounty and ~0.01–0.03 SOL cleanup rents, but its [published program ID](https://github.com/Romulus-Sol/DMV) is explicitly **Devnet**. | **STOP until verified real-money mainnet deployment and payable matured vault**. A demo/devnet reward is not transferable cash.

**Important new anti-error rule:** historical Github source may initialize a reward at **100 bps**, while the **deployed contract now returns 25 bps**. Always read current chain-state configuration. Also, outbound \`Transfer\` logs from a vault are not caller earnings unless the actual *beneficiary/recipient* is verified, including any intermediate helper's downstream transfers.

At Oct 12 spot indications ([CVX ~$2.12](https://www.investing.com/crypto/convex-finance/cvx-usd-historical-data), [CRV ~$0.366](https://metamask.io/en-GB/price/curve-dao-token)), $25 gross from *one overdue 0.25% epoch* requires ~4,717 eligible CVX; $25 gross from 0.5% earmark requires **$5,000 of currently unharvested CRV**. Neither eligible unclaimed condition has been demonstrated and both exclude gas, failure and conversion. **Current verdict: no ready payment.**


## H. Latest direct real-time funding tests, Ethereum + Base (2026-10-12)

Detailed evidence [PR #12](https://github.com/ahmedelgaml70/protocol/pull/12) / [complete audit](https://github.com/ahmedelgaml70/protocol/blob/research/prefund-live-gates-100/docs/PREFUNDED_LIVE_GATE_AUDIT_2026_10_12.md) / [successful GitHub Actions run](https://github.com/ahmedelgaml70/protocol/actions/runs/38279897335).

| Candidate | Exact live/current evidence | Verdict |
| --- | --- | --- |
| **Permanent Collection Ethereum \`BuybackBurner.executeStep(uint256)\`** | Public deployed ETH caller reward = min(0.5% of executed step, 0.01 ETH); deployed \`maxStep=1 ETH\` so **≤0.005 ETH per full-size step** with present params. **Block 26,177,686 \`remainingEth=0 ETH\`**, so maximum presently funded reward = **0 ETH**. | **STOP until burner accrues new ETH**, despite separate Patron live bid balance. [Primary contract source](https://github.com/ripe0x/permanent-collection/blob/master/contracts/src/BuybackBurner.sol) |
| **BasedAgents Base USDC agent tasks** | HTTP GET 20 open tasks, **one API-tagged funded**, **1 USDC** test hire 'please ignore'; **zero funded open ≥25 USDC**. Ten historical settled feed entries; small amounts, not individually chain-receipt matched. Explicitly unescrowed/unknown $0.25 and $2 items cannot count as prefunded. | **STOP for $900 scale** without much larger independently funded new inventory. [Source repo](https://github.com/maxfain/basedagents), [platform](https://basedagents.ai/docs/getting-started) |
| **Aeterna inheritance 1% keeper** | Solidity bounty source integrates **Base Sepolia** Aave pool and repo demo accelerates time. No user-paid live mainnet deploy or claims verified. | **STOP testnet** [source](https://github.com/ch2llgao/Aeterna) |
| **PolyDispute 10 USDC \`arm()\`** | Site advertises bounty if dispute pool fills, but markets/testnet and planned external audit; no supported payable mainnet pool; dispute/Polymarket dependence also misaligned. | **STOP** [official](https://polydispute.finance/how-it-works) |
| **openbounty.app** | Publisher pays after quorum acceptance; not prefunded; explanatory payment flow on **Base Sepolia** and example tasks explicitly illustrative. | **STOP** pending real escrow and mainnet payouts [site](https://openbounty.app/) |

**Technical details**: registered \`claimable\` API tasks ≠ confirmed escrow; \`payment_status=pending\` ≠ paid; \`250000\` six-decimal USDC = **$0.25** (NOT $250 or $250,000). Older Burner documentation claims maximum **0.05 ETH**, whereas actual source/live getter caps at **0.01 ETH**. Read code and deployed getters. Low/current-zero funding defeats grander announced reward rates.


## I. Flight fulfilment from already funded orders — direct public settlement census

**BRIJ Travel:** [Full Oct 12 audit](BOOKING_FULFILLMENT_BRIJ_AUDIT_2026_10_12.md) / [official order explorer](https://docs.brij.fi/bounties) / [public fulfiller metrics](https://docs.brij.fi/fulfillers). The bounty explorer shows historical on-chain escrow purchases, including 732.47 USDC customer ticket order settled Sep 29. But public supplier-network records show **zero orders actually captured in last 30 days across either of two named partner/domain categories** (each four assigned, all refunded), and both require **whitelisted wallet + taker deposit + separate card-fronting of the actual airline fare**. Customer ticket price is not solver profit; the platform's external contributor fee and funding availability remain unclear. **STOP** for <$100/$900 net November goal. Do not double-count overlapping supplier domains. Not an open booking/refund faucet; no calls or applications made.


## J. Arc / Base / Bountic current open-task census — Oct 12 17:16 UTC

[Primary code and audit PR #13](https://github.com/ahmedelgaml70/protocol/pull/13) / [full report](https://github.com/ahmedelgaml70/protocol/blob/research/arc-base-escrow-100/docs/ARC_BASE_BOUNTIC_AUDIT_2026_10_12.md) / [passed CI and live evidence](https://github.com/ahmedelgaml70/protocol/actions/runs/38283082911).

| Platform | Actual observed inventory and payment evidence | Verdict |
|---|---|---|
| ArcBounty, Arc mainnet chain 5042 | Official chain-storage API: 16 posted, 12 historically paid, **22.77 USDC total worker payments**, **0 open tasks** | STOP NOW: zero unclaimed current payout |
| BaseBounty, Base mainnet chain 8453 | Distinct deployed chain and escrow, 9 posted, 3 paid, **2.97 USDC total worker payments**, **0 open tasks** | STOP NOW: zero unclaimed current payout |
| Bountic Locus escrow site | Advertises **55 USDC total funded / 5 bounties / 0 payouts**. One $10 open issue #12 shows **19 competing PRs**, optional source material mismatched with issue headline; payment requires maintainer approval after winning PR merger | REJECT: user avoids competing for low-value coding bounties, no verified worker payout proof |
| AgentPay; Legwork | Base Sepolia/USDC testnet demonstrations, Legwork has in-person World ID physical errand element | STOP: not suitable online withdrawable income |
| Aither queued Q4 100 USDC contract audit | Not open payment; listed task is security-oriented | STOP: security bounty excluded |

Current available worker income in two live mainnet task escrows was **0 USDC**, despite 25.74 USDC aggregate past worker payouts. Do not count publisher budgets, marketing figures or old transactions as today's available cash. Need a concrete open unreserved task ≥25 net USD with timely authorized payout BEFORE integrating SDKs or signing transactions. Sample was timestamped 17:16 UTC; future jobs could appear.


### Additional mainnet/self-dealing gate

- **Claudelance Celo:** [official README](https://github.com/yeheskieltame/claudelance) says pre-adoption, **one unique poster**, all 80/96 historic V2 settlements and agent payments are **operator-owned swarm self-tests**, not third-party economic demand. Tables suggesting $500–$3,000 bounties describe task capacity, not actual paid open offers. **STOP pending independent users**.
- **Hive Stellar:** [source](https://github.com/Alouzious/hive) badge/deployment say **testnet**, with mainnet after hackathon and mocked transaction signing. **STOP, no real current withdrawable income**.
