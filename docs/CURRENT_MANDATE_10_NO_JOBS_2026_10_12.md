# Hard reset — latest user direction: $10, NO WORK/CLIENTS — 2026-10-12

**This addendum supersedes prior $100 and 30-day operational numbers wherever they conflict, without altering historical archived findings.** The user just explicitly restated: **we have $10**, seek **$1,000 very fast**, no jobs, tasks, freelancing, clients, selling services, promotion, discounts, affiliate/referrals or speculative long waits. They wish to creatively identify legitimate, overlooked, already-funded value **obtainable through lawful, public, permissionless actions**, crypto or non-crypto, with ChatGPT doing investigative/computational work. Receive options: PayPal, Airtm, RedotPay, Binance; payment rail is NOT a source of earnings and Binance Pay is not an Ethereum wallet. The user explicitly rejected the recent live Upwork opportunities, even if budgets were large.

**DO NOT SUGGEST Upwork again** for this challenge, even if zero proposals or a $500 project. Stop seeking work-for-hire. Do NOT claim $100 still available as the current budget: use the latest explicit **$10** limit. Deadline should be treated as **AS FAST AS POSSIBLE**; the earlier November 12 date is historical and NOT a hard constraint the user restated in this message.

## Financial reality / safety

$10 to $1,000 is a **100× total increase / 9,900% gain**. With no customers, work, referrals, promotional grants, privileged entitlements or high-loss-risk speculation, that gain must come from someone else's **pre-authorized, legitimately caller-rewarded pool** (or an uncommon windfall). None of the on-chain searches to date has proven a present, independently executable, positive-net reward path to $990. **Do not promise an easy trick, free mining with incredible yields, riskless 100× returns, exploitable vulnerabilities or guaranteed success.** Nor rationalize accessing owner-owned funds via a permissionless \`claim\` function that pays a fixed beneficiary; a public function is not public entitlement.

No keys/signatures, wallet connections, unauthorized claims, account creation, real transactions, external website mutations, deposits, collateral staking, margin/flash trading, subscriptions or spending of **any** of the $10 without explicit per-action owner approval. Public-code review and read-only network queries are authorized. Preserve $0 spent/$0 actually earned until verifiable user-controlled cash receipt.

## New research (sources dated/accessed Oct 12, 2026)

### 1. lolpad.fun — verified mainnet graduated-curve caller bounty, but NO scale

**Sources:**
- https://lolpad.fun/docs/contracts/graduation.html
- https://lolpad.fun/docs/guides/graduation.html
- https://lolpad.fun/docs/getting-started/project-status.html
- https://lolpad.fun/docs/backend/rest-api.html

Official project reports Arc mainnet chain 5042, deployed Sep 16, with public \`BondingCurve.graduate()\` during \`LOCKED\` state. The permissionless call pays \`msg.sender\` through a bounty ledger, **but:**
- grace first 120 blocks: **0 USDC**;
- over next 1,200 blocks it ramps to **5 USDC maximum** (full bounty only if keeper fails to migrate for roughly 11 minutes);
- platform's own always-on keeper normally graduates **within grace** so outsider payout generally zero;
- 10,000 USDC graduation threshold and 200 USDC protocol graduation fee are NOT amounts available to public callers.
- 200 successful max-cap outsider calls would be needed to gross $1,000 before network fees, payout claims and competition. No present caller eligible open graduation identified.
- \`GET /api/v1/tokens?state=locked\` and \`/status\` endpoints are officially documented, but direct access from our web environment failed, so **current live locked inventory = UNKNOWN**. A $5 cap already fails target-scale gate; do not code a bot solely because a potential future locked token exists.

**Verdict:** WATCH only if specific unexpectedly aged LOCKED token found by a free exact open source, but no rational path to 100×/quick $1,000 established. Do not conflate graduation fee with caller bounty.

### 2. Base DeadManSwitch — mainnet-claimed 0.5% caller reward but repo DISAPPEARED

A search-indexed [GitHub README](https://github.com/lordbasilaiassistant-sudo/deadman-switch) advertises Base mainnet deployment at \`0x40f1AAb4c82D48260Ab1207e27329d51290025DB\`, reward 0.5% of expired payout to triggerer. **Critical Oct 12 verification failure:** both connected GitHub API read and an independent direct web open return **HTTP 404 / NOT FOUND** for the referenced source repository. Search results may be stale, the contract may still exist, and its bytecode/source mapping and available funded expired vaults have NOT been independently checked. Do NOT treat the README as current verified deployment or as proof of any payout. **Verdict: RESEARCH ONLY after verified current explorer source/bytecode, actual funded vault inventory and beneficiary-safe semantics.** If unavailable, STOP; no $10 gas experimentation on unverified code.

### 3. Nest on Robinhood Chain — maximum 1% harvest bounty, but demand & source uncertain

[makeanest.fun/docs](https://makeanest.fun/docs) indexed copy describes Robinhood Chain claim-vault harvests where \`harvest()\` pays **1% of actual creator fees collected, capped at 0.02 ETH per transaction** to independent caller; the burn-to-redeem vault harvest is explicitly UNPAID, and \`claim()\` pays only authorized owners/holders. The same copy documents one or a few launch coins, tiny/microcaps, and an in-house keeper. A third-party [Blockspot snapshot](https://blockspot.io/nl/coin/nest-3/) claims makeanest.fun **offline since Oct 11**; the first-party docs timed out when opened in our web reader, so verify independently before any activity. No contract-address/source-to-bytecode verified, no current accrued unharvested fees nor actual historic recipient proof. **Verdict:** possible attractive *formula* compared to $5 but extremely high uncertainty; no executable opportunity. $25 gross at 1% requires **$2,500 in ACTUALLY UNHARVESTED CREATOR FEES** right now, not $2,500 cumulative trading or market cap. A 0.02 ETH cap does not say a fresh caller will earn 0.02 ETH.

### 4. Kaleido on Robinhood Chain — real-design 0.25% public fee harvest but no current revenue evidence

[First-party KALEIDO docs](https://kaleido.money/docs.html) advertise public \`pokeFees()\` with **0.25% of actual WETH-side harvested fees**, capped; only existing share owners can claim dividend balances, and \`sweepForfeits()\` sends reallocated funds to owners, not caller. An available $25 gross reward would require $10,000 in actually unharvested WETH-side fee value at 0.25%; no such backlog verified, no current successful third-party claim receipts checked. **Verdict:** no demonstrated positive-net catch, don't buy token to speculate or trigger unknown function.

### 5. General IExternallyExecutableBounty proposal — actual standard draft, not inventory

[March 16, 2026 draft ERC](https://ethereum-magicians.org/t/draft-erc-externally-executable-bounty-a-standard-interface-for-permissionless-task-automation/28002) proposes \`getExecutableTasks()\`, \`taskBounty(id)\` and \`executeTask(id)\` to standardize discovery and ETH payout, with testnet bot success reported. There is **no proven widely adopted, verified funded MAINNET task registry or currently executable >=$25 payout** from the draft. Interesting future *indexing* idea, not current money. **Verdict:** WATCH design, do not spend on generalized collector.

### 6. Ekubo publicly callable protocol revenue buyback — pays DAO, NOT caller

[Official Ekubo governance docs](https://docs.ekubo.org/products/governance/) and [official blog](https://blog.ekubo.org/where-the-revenue-goes/) explain anyone may execute the buyback function but protocol revenues/proceeds route to the DAO via TWAMM. **No documented caller bounty**. [Live public dashboard](https://ekubo.org/governance/revenue-buybacks?lang=en) showed $0 pending in the browser snapshot, separately. **Verdict: STOP "call and collect the treasury"** for identical beneficiary error as Hyperlane IGP.

## Target-selection framework for next agent

**Never code first.** Prioritize a single source **only after ALL of:**
1. Exact verified mainnet deployed code/bytecode and current transaction source (not search-indexed 404);
2. **Mechanism transfers reward to the independent arbitrary caller**, not owner, treasury, token-holder, or payee;
3. A real *currently funded, unexecuted and executable* item with **gross >= $25**, ideally >= $100, identified from a free current-state read; not cumulative platform totals, ad-bounty, old closed receipts or pending obligations;
4. Read-only \`eth_call\` from a dummy address + gas estimate and exact reward token/price/cash-out liquidity, with healthy safety buffer;
5. Competition/payout velocity realistically enough for ~$990 before 30 days (ideally far faster), or identify that it is a one-off windfall with low likelihood;
6. No deposit, stake, supplier purchase, client, job, referral, marketing, collateral lock or front-running/illicit exploitation required.

Do NOT recommend old excluded Kerf/PoolTogether/Beefy/Superfluid/Ripe/Morpho/0xSplits/Liquity/Sovryn/Keep3r/Convex/ArcBounty/BaseBounty etc without **new material exact live evidence**. Source-of-truth historic $100/Nov12 records remain for context; this hard-reset addendum governs **latest user preference and $10 capital ceiling**.

**Verdict this research turn:** possible overlooked *structural* source classes found but **zero actual available positive-net caller payouts verified**; $10 principal untouched, $0 user earnings. Research must distinguish creative hypothesis from withdrawable money. No repo bots/transactions created during this turn; documentation only.
