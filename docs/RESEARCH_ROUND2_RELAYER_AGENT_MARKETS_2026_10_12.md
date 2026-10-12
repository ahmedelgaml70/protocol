# New money-mechanism audit — relayers, fee cranks, agent task markets and x402

**Observed:** October 12, 2026. **Scope:** read-only first-party contract/docs inspection + independent dated market measurements. **Cash actually earned:** $0. **Capital spent:** $0. **Verified new execution-ready payment:** none.

> Research gate: the same $100 starting capital / $1,000 total withdrawable by November 12, 2026, no cold clients or security exploits, no speculative capital deployment. This document extends [canonical handoff](HANDOFF_2026-10-12.md), [matrix](OPPORTUNITY_MATRIX_2026-10-12.md), [playbook](RESEARCH_PLAYBOOK.md). Dates and evidence tiers matter.

## Lane 1: Hyperlane cross-chain relayer, "permissionless" claiming

**Hypothesis:** A relayer can deliver otherwise unprocessed interchain messages, claim prepaid Interchain Gas Paymaster (IGP) fees and use <$100 to earn positive cash without attracting customers.

**Verified primary evidence:**
- Official Hyperlane relayer source says `Mailbox.process()` delivery is permissionless but **relayers receive no direct incentive from the protocol**; operators have to configure message/fee arrangements with origin/destination applications. [Hyperlane relayer docs](https://v2.hyperlane.xyz/docs/protocol/agents/relayer).
- Mainline [IGP source](https://github.com/hyperlane-xyz/hyperlane-monorepo/blob/main/solidity/contracts/hooks/igp/InterchainGasPaymaster.sol), read via connected GitHub tool on Oct 12: publicly callable `claim()` forwards **all native coin to the stored `beneficiary`**, and `claimToken(address)` similarly transfers ERC20 to the same beneficiary. Owner sets beneficiary via `setBeneficiary()` guarded by `onlyOwner`. **Caller's address does not become beneficiary**.
- Official [keyfunder README](https://github.com/hyperlane-xyz/hyperlane-monorepo/blob/main/typescript/keyfunder/README.md) describes a maintained process that claims accumulated IGP fees and replenishes relayer wallets.
- Independent DefiLlama protocol tracker [IGP revenue methodology](https://investors.defillama.com/protocol/hyperlane?events=false&incentives=true&tvl=false) counts fees paid to published relayer contracts. **This is not gross earnings available for third-party public claim.** Dynamic dashboard totals cannot establish any new operator's net.

**Decision: STOP as a "collect stranger's fee" loophole.** Publicly callable transfer is **not a reward for caller**. Setting up an independent relayer is allowed in principle, but requires message senders paying *our* configured relayer/beneficiary, operational destination gas and running infrastructure, which conflicts with no clients, $100 risk cap and deadline. No currently funded user-addressable message or contract payment found.

## Lane 2: archr.fun fee-crank bounty on Robinhood Chain

**Hypothesis:** New 2026 micro-launchpad on Robinhood Chain pays any caller 1% of moved trading fees for collecting from v4 pools, converting and pushing distributions; fewer bots than Ethereum.

**Primary evidence:**
- [Archr "Getting rewards"](https://archr.fun/docs/rewards) states the **three fee-processing jobs are permissionless**, each pays the initiator 1% of moved fees; archr also runs its own keeper.
- [Archr how it works](https://archr.fun/docs) identifies the jobs' sources as real LP fees from trading and says a bot already collects them.
- [Archr technical page](https://archr.fun/docs/technical) shows deployer/locker/distributor/hook architecture on Robinhood Chain (4663). **The documentation is a project claim**; contracts' current bytecode/executable specific caller rewards have **not been independently audited in this round**.
- A search crawler snapshot of [archr.fun](https://archr.fun/) from approximately 6 days before this research showed **3 listed tokens and about $159 cumulative holder rewards**, which is *historical and from project UI*, not an independently verified current on-chain fee state. Opening the current web page yielded JS-loading placeholders ('—') so the 3-token/$159 figure is **not revalidated at the current block**.
- The advertised 1% is a share of *actually moved* fees, not a right to 1% of cumulative user-facing platform rewards. No currently uncollected fee pool, gas estimate or actual caller payout receipt was verified.

**Decision: WATCH / G0 mechanism only, no funded executable candidate.** Even small headline platform rewards and an existing in-house keeper suggest restricted opportunity; do **not** write another generic bot, launch/buy tokens, or send gas. If a later direct on-chain observation finds ≥$20 *net callable fee* with uncollected state and affordable gas, revisit exact contract simulation.

## Lane 3: Agent-first paid task marketplaces

**Hypothesis:** Machines can perform numerous escrow-funded tasks without cold outreach or application bidding, and USDC settles immediately.

**First-party settlement rules:**
- [TaskMarket docs](https://docs.taskmarket.dev/features/x402-pay) and [API reference](https://docs.taskmarket.dev/api/reference) say requester funds tasks in USDC; `POST /api/tasks` creates escrow; submit requires EIP-191 signature; in many modes requester must accept, select winner or adjudicate. Some alternative task modes have added x402 spend.
- [TaskMarket Fees and Payments](https://docs.taskmarket.dev/concepts/fees-payments): **default 7.5% platform fee**, e.g. $10 gross → $9.25 accepted worker net; posting escrow is not payment approval. Claim-mode sometimes requires refundable/forfeitable deposit; accept/rate/proof actions have nominal 0.001 USDC costs.
- Direct first-party `https://api.taskmarket.dev/api/tasks/stats` and `/api/tasks` were **not accessible via this web tool** at audit time. No assertion about the precise current number of open tasks is based on our independent live API scan.

**Independent dated measurement — caveat: not independently reproduced:**
- [Shaduf paid-opportunities directory](https://shaduf.ai/p/agentic-freelance/opportunities/), updated as recently as **Oct 10** for TaskMarket, reports 27 paid-work venues, **13** with some primary evidence of payouts, and **zero** venues recommended "go with owner" at its assumed central AI-cost band; 9 probe, 18 avoid. Their venue tests were NOT actually executed by their own research pool.
- [Shaduf overview](https://shaduf.ai/p/agentic-freelance/) estimated about **$212 of entire measured agent work payout volume in the prior 30 days** across its sampled platforms as of Oct 7, a partial sample, not a universal market census or ceiling.
- TaskMarket sample: 7 open tasks, 84 new in 30 days and expected payment around **$0.025 per attempted submission** at Oct 10 snapshot, with a measured history of **requester-unawarded escrowed tasks**. Cost estimates of $0.072 to $0.32 per attempt at mid-range model prices exceeded expected payout; these are Shaduf's modelling assumptions, not our actual operator bills.
- TaskMarket has **real paid agent work**, but requesters can decline work, tasks are competitive, many rewards tiny and user strongly prefers avoiding gig bidding. The $100 is not a substitute for available high-paying task inventory.

**Decision: CONDITIONALLY WATCH, NOT READY for $900.** G0 plausible escrow and G2 payment history established through platform/on-chain evidence reported externally; specific open task, accepted worker eligibility, assured release, independent payoff and sufficient volume G1/G3/G4/G5 unproven. Do not register an agent wallet or submit/bid without approval. Revisit only if verified task pays materially more and can be preassigned or first-come, no paid bid/risk.

## Lane 4: x402 autonomous API sellers

**Hypothesis:** Publish one autonomous data/API service and earn $900 from agents paying per request without directly contacting customers.

**Independent measured buyer/seller evidence:**
- [x402stats September 2026 report](https://x402stats.io/reports/2026-09), dated September, counts 19,015 raw receiving wallets, **78** "organic" seller wallets with ≥$100 per month, ≥3 buyers and average ≥$0.001/payment; top ten had **79%** of filtered volume, median receiving wallet earned around **$0.04 monthly**. Thresholds are that report's *defined filter*, not a claim of universal earnings or exact current market share.
- [ChainWard September 27 study](https://chainward.ai/decodes/x402-on-base): among Sep 15–21 Base x402 transactions, **$128,977** settled, of which at least **$56,268 (43.6%)** looped through self-funded parties, and $30,000 additional round trips were flagged separately. Authors explicitly do not label all remaining money independent.
- [Shaduf x402 walkthrough](https://shaduf.ai/p/agentic-freelance/walkthroughs/x402-seller/) says in its Oct 3 sample, 27 sellers reached >$1k from at least five buyers, at most one partly provided agent work, and the largest buyers shared funding sources. These are time-scoped estimates.
- Offering an x402 endpoint requires real independently paying demand; being technically able to receive USDC does not create users. Some facilitators require API registration and fee checks; consumer ChatGPT subscription is not an authorization for programmatic API consumption.

**Decision: CONDITIONAL long-horizon builder, not a buyer-free $900 opportunity in a month.** Only re-open if a product has demonstrably existing unaffiliated API buyers and recurring need that is unserved; user does not want to seek clients or wait for discovery.

## Combined 2026-10-12 falsification result

| Lane | Documented financial mechanism | Independent recent payment/access proof | Specific current, accessible positive-net call or work | Verdict |
|---|---|---|---|---|
| Hyperlane public `claim()` | YES; proceeds go to fixed `beneficiary` | Contract access semantics verified | **NO** (caller gets nothing) | STOP |
| archr Robinhood keeper | Advertises 1% of processed fees | No independently verified caller receipts; project UI small/partly stale | **UNKNOWN** | WATCH only |
| TaskMarket/agent boards | YES, USDC escrow and some historical paid work | Independent retrospective study; not our live API | **NO VERIFIED CURRENT $900 CAPACITY** | CONDITIONAL |
| x402 API seller | YES, USDC per actual buyer request | Dated on-chain revenue with major wash/loop caveats | **NO VERIFIED USERS/RECEIVABLE** | CONDITIONAL |

### Hard-stop checklist newly learned
1. A `claim()` function **can be public but pay a different beneficiary**; read the transfer recipient in source/receipt. Public authorization ≠ public reward.
2. A "1% bounty" is not meaningful until the **actual present fee base**, unpaid/uncollected, its unit, and gas are measured. A project homepage aggregate is not a user opportunity.
3. "Task escrow exists" is not enough when a requester can simply refuse all submissions; check payment-award history and contractual timeout/release.
4. A large x402 "monthly volume" metric can include operator loops, small transfers, facilitators and test traffic; trace unrelated buyers before evaluating demand.
5. Do not auto-produce an AI gig marketplace bot that expectedly costs more per attempt than expected paid reward.

**Next falsifiable research test (preferred):** find a *specific* reward ≥$25 with verifiable current funding, first-come or objective uncontested eligibility, and payout to the **caller** (not beneficiary) on a low-fee chain; confirm current claimable amount and recent third-party payout receipts **before** coding a watcher. For non-crypto alternatives, demand a specific pre-funded independent-payer task with guaranteed assignment, compatible payout and actual approval under the one-month deadline. Do not build first and hope money appears.

**Result:** We have improved the exclusion logic and documented four distinct economic structures. **No verifiable executable positive-net reward, $0 realized, $0 spent.**

## Operational scale sanity checks (scenarios, NOT observed earnings)

Our financial gap is **$900 net** over 30 days, or **$30 net/day**, excluding any desire to protect the original $100.

- If an Archr-style caller earns **1% of eligible processed fees**, it needs **$90,000 in fees actually processed by that caller** to collect $900 *gross before any gas*. The percentage is not of trading volume and applies to the specific eligible fee-processing step. Three potential distinct cranks do not prove three times the same accessible dollars. The project's cached small public history is not evidence such an unprocessed backlog exists.
- If a contested task paid a hypothetical **$1.85 net** per winning accepted submission, a new entrant would need **487 winning paid tasks** in 30 days, versus independent Shaduf's historical observation of only **84 newly posted TaskMarket tasks over 30 days** (snapshot Oct 10). This arithmetic is *illustrative* and does not assume the market remains unchanged, nor that $1.85 is every job's reward. There are no 487 presently verified awarded jobs accessible to the user.
- An x402 service earning a hypothetical $0.05 *net* per independent user request needs **18,000 real external paid requests** in 30 days. This is a demand/customer-acquisition challenge, not a payment integration trick; a zero-buyer API earns $0.
- Hyperlane IGP public `claim()`: **no amount of balance creates caller reward** without beneficiary rights; cost of executing the public method could make the caller poorer.

**Technical lesson:** ROI fantasy is often defeated by denominator confusion: fee volume vs gross swaps; number of advertised tasks vs approved/won tasks; protocol credit vs per-call payout; recipient vs caller; website reported buyers vs unaffiliated actual paying buyers.
