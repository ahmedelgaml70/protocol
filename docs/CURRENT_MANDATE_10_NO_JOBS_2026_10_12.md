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


## 2026-10-12 17:55 UTC — real mainnet bounty census (LATEST COMPLETED EXPERIMENT)

[Draft PR #14](https://github.com/ahmedelgaml70/protocol/pull/14) / [detailed Harbor+other mechanism audit](https://github.com/ahmedelgaml70/protocol/blob/research/harbor-bounties-10/docs/HARBOR_REAL_FUNDED_BOUNTY_NEGATIVE_NET_2026_10_12.md) / [successful mainnet GitHub Actions run](https://github.com/ahmedelgaml70/protocol/actions/runs/38287408674). Latest $10 limit respected; **no spend/sign/transfer**. Harbor's Ethereum mainnet official actual contract state shows FIVE managers, THREE funded and successfully simulated independent caller harvests. **All three are negative net at Oct 12 market prices and measured gas.**

- ETH/fxUSD: 0.1033828689 fxSAVE gross (~$0.1158) vs ~$0.1727 Ethereum gas = ~**-$0.0569** before selling token.
- BTC/fxUSD: 0.0103006452 fxSAVE gross (~$0.0115) vs ~$0.1727 gas = ~**-$0.1612**.
- BTC/stETH: 0.00003630945 wstETH gross (~$0.1136) vs ~$0.1791 gas = ~**-$0.0655**.
- USD/stETH and USD/WBTC harvestable 0, rebalance state flagged true yet actual rebalance simulations REVERT; no valid caller reward. Payout recipient verified from source \`harvest(address bountyReceiver, uint256 minBounty)\`; ratios read live (1%); no token held by user.
- This is a **genuine real funded onchain bounty** that still fails economics, unlike historical receipts. Gas at sample ~0.2283 gwei, very cheap; token USD values are cited approximation, not executable token swaps.

Additional first-party checks: Velocity Solana keeper fills mostly **cents per fill**, 1-cent cancels/trigger and $1,000 staked TWAP crank that pays $0; fillr technical docs contradict homepage and say DEVNET; Caliper's token is mainnet but harvest vaults TESTNET; GBLIN old named keeper tool appears linked to superseded v1 and cannot be used as current contract evidence; ADAM current displayed unsplit pool 0.0056 ETH at 0.5% keeper share implies ~$0.071 gross, and no verified profitable call. Source links and caveats in PR #14.

**No actionable positive-net reward verified**. Reject any gas spend here. Future focus: low-fee chains, currently funded caller bounty >=$25 with independently verifiable source/bytecode and real present state. Stop re-creating generalized bot scanners without pre-flight economics.


## Later 2026-10-12 research — Moto.fun, Omora and Kairos

**Latest evidence:** [draft PR #15](https://github.com/ahmedelgaml70/protocol/pull/15) / [detailed audit](https://github.com/ahmedelgaml70/protocol/blob/research/motofun-keeper-10/docs/MOTOFUN_OMORA_KAIROS_AUDIT_2026_10_12.md) / [successfully completed live scan](https://github.com/ahmedelgaml70/protocol/actions/runs/38289424666).

- Moto.fun Ethereum launchpad does have real **permissionless \`graduate(token)\` caller ETH bounty** (documented starting parameter 0.015 ETH, actual payout depends on current pot and settings). However first-party live API venue-wide **75 coins, 69 bonding, 6 already graduated, ZERO frozen** at ~18:13 UTC; contract-level chain ID 1 and bytecode for official curve & lens verified at Ethereum block **26,178,111**. First page individually 23 bonding/2 graduated. Official API \`GET /config\` unexpectedly 404, first unsuccessful scan was marked incomplete, successful retry used first-party published addresses as fallbacks. **No currently open ready-to-graduate coin found**; no ether spent or transaction sent.
- Omora Base-mainnet \`FeeManager.collect\` public function directs 70% to creator and 30% protocol, **zero to unrelated caller**. \`claimFees\` only for creator's own entitlement; no public maintenance bounty. Source verified in GitHub.
- Kairos main website documents **2% USDC-equivalent liquidation bounty of collateral**, suggesting $25 bounty needs $1,250 of actually qualifying liquidatable buyer collateral, but accessible current deployed source/market list is **NOT** verified (connected GitHub original source repo 404); no profitable callable transaction shown. Do not trade, deposit, or exploit audited vulnerabilities. Historical Base beta is NOT evidence that the current Ethereum main app has no positions.

**Decision:** all new routes remain unproved as PRESENT paid opportunities. $10 untouched, $0 earned. No jobs/clients/marketing, no transaction approved.
