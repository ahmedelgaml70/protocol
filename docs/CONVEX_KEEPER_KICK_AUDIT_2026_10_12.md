# Convex Earmark and Expired CVX Lock Bounties — live research (2026-10-12)

**Project objective:** no more than **$100 starting operating capital**; aspire to **$1,000 total net withdrawable by Nov 12, 2026**; no spending or wallet transactions authorized. **Verified user earnings: $0; spent: $0.**

## Status

**Research-only / NOT READY.** A genuinely incentive-paying deployed contract exists, but **no presently available, positive-net and realistically winnable transaction** has been demonstrated. Need better archival index access and exact beneficiary tracing before more code; do not buy CVX or CRV.

## 1. Sources and contract provenance

- Official Curve Ethereum Convex Booster: \`0xF403C135812408BFbE8713b5A23a04b3D48AAE31\`. Official [deployment registry](https://docs.convexfinance.com/convexfinance/faq/contract-addresses); canonical [Booster.sol](https://github.com/convex-eth/platform/blob/main/contracts/contracts/Booster.sol). \`earmarkRewards(uint256)\` is public, pays \`earmarkIncentive / 10,000\` of **actual collected CRV** to \`msg.sender\`, not to every ETH submitting address when a wrapper contract is used.
- Official mainnet Convex V2 locker \`0x72a19342e8F1838460eBFCCEf09F6585e32db86E\`. Verified against same official deployment registry and [CvxLockerV2.sol](https://github.com/convex-eth/platform/blob/main/contracts/contracts/CvxLockerV2.sol). \`kickExpiredLocks(account)\` is public, sends a percentage of overdue CVX to \`msg.sender\` and remaining unlocked CVX to the **original owner** (not a permission to appropriate the owner's total balance). Terms/eligibility: after a four-epoch grace delay, percentage grows by fixed basis points per overdue epoch, capped by source. Official [CVX locking FAQ](https://docs.convexfinance.com/convexfinance/general-information/understanding-cvx/vote-locking) describes 0.25% per overdue week.
- Beware **source initialization vs live settings**: CvxLockerV2 source starts at \`kickRewardPerEpoch = 100\` bps, whereas actual deployed **live on-chain value was 25 bps** as measured in this run. A naive code-reader might incorrectly recommend a 1% kicker reward. Current on-chain state wins.

## 2. GitHub implementation

Branch: \`research/convex-earmark-100\`. All methods strictly read-only; no signing, token purchase, account setup, gas or user wallet.

| Program | Proof attempted |
|---|---|
| \`research/convex/convex_earmark.py\` | Inspect deployed Booster parameter, bytecode and ~800-block CRV token transfers FROM Booster, deduplicate tx; confirm only **direct externally-submitted** earmarks paid \`tx.from\`, never assume every Booster transfer is keeper earnings |
| \`research/convex/convex_kicks.py\` | Query current live V2 locker kick parameters and ~7,400-block \`KickReward(address,address,uint256)\` events; receipt verify if any |
| \`research/convex/convex_lock_candidates.py\` | Sample historical \`Staked\` events from **three tiny non-contiguous** historical windows (160d/205d/270d), read present next-unprocessed \`userLocks\`, if mature then \`eth_call\` simulate + gas estimate. Not a comprehensive list or live opportunity guarantee |
| \`research/convex/test_convex_earmark.py\`, \`test_convex_kicks.py\`, \`test_convex_lock_candidates.py\` | ABI decoding, timestamp calculations, read-only method protections. **13 of 13 offline tests passed** in the latest CI run |
| \`.github/workflows/convex-earmark.yml\` | GitHub Actions push/manual trigger, \`contents: read\`, pinned eth-abi & Keccak libs, JSON evidence artifact stored for seven days, no scheduled unattended execution |

## 3. Verifiable on-chain results — Oct 12, 2026

### 3.1 Booster sample

[Successful short-window run](https://github.com/ahmedelgaml70/protocol/actions/runs/38276766050), independently executed from GitHub-hosted runner against Ethereum publicnode.

- Chain ID Ethereum mainnet = 1, deployed Booster code nonempty.
- \`Booster.isShutdown() = false\`, \`poolLength() = 583\`.
- **Current** \`earmarkIncentive() = 50 / 10,000 = 0.5%\` of actual CRV harvested.
- In the **latest ~800-block bounded sample**, **30** CRV \`Transfer\` events FROM Booster in **four distinct transaction hashes**.
- The 30 transfers were primarily LP reward destinations, lockers/staking pools, protocol fee addresses, and some **possibly intermediate harvesting contracts**; **zero recorded CRV transfer recipients equaled the transaction submitter**. Four transactions targeted addresses **other than Booster**, and their call selectors were not \`earmarkRewards(uint256)\` at the top-level.
- This proves there were active CRV distributions in the sample, but **NOT** the direct EOA caller payout size. The reward can be directed to an *intermediary contract* which then distributes or retains it. Thus \`direct_earmark_calls_paid = 0\` is a **very narrow filter**, NOT an assertion Convex gave no kicker rewards. Some recipients' contracts may have controlled the harvested call.
- The first 7,400-block scan exceeded the conservative 140-log safety cap. It was marked **incomplete**, not zero; [initial failed run](https://github.com/ahmedelgaml70/protocol/actions/runs/38276521864). Narrowing to 800 blocks let us inspect all transfers.

**No open current \`earmarkRewards(pid)\` pool was independently simulated**, and no network-level gas-to-CRV expected value was proven. Current asset valuation ~[0.367 USD/CRV as of Oct 12](https://metamask.io/en-GB/price/curve-dao-token), but a snapshot quote is **not executable conversion price**. At 0.5%, $25 gross requires **~$5,000 worth of *currently unharvested CRV* per execution**, before gas and slippage. This has not been observed.

### 3.2 CVX locker kick sample

[GitHub Action with current settings and bounded kick history](https://github.com/ahmedelgaml70/protocol/actions/runs/38277038085).

- Deployed \`kickRewardPerEpoch() = 25\` basis points **per overdue epoch**; \`kickRewardEpochDelay() = 4\`, \`denominator() = 10000\`, \`rewardsDuration() = 604800\` seconds (one week).
- Exact live rate = **0.25% per overdue week after four weekly grace periods**, capped/weighted by source (and subject to lock eligibility).
- Recent **~7,400 Ethereum blocks** produced **0 successful \`KickReward\` events** in the bounded on-chain scan. This is **zero historical receipts in the checked period**, not absence of outstanding expired locks.
- A value example **only**: at [Oct 12 CVX ~ $2.12/CVX](https://www.investing.com/crypto/convex-finance/cvx-usd-historical-data), **one** 0.25% reward on a 4,717-CVX expired stake is ~11.79 CVX, $25 gross before gas, conversion and competition. Delayed extra epochs change the rate; this does not identify such an available holder.

### 3.3 Actual current expired-lock candidate census (FAILED / INCOMPLETE)

[Eligibility sampler run](https://github.com/ahmedelgaml70/protocol/actions/runs/38277359911). 13/13 offline tests passed, but all three old \`Staked\` log queries, anchored at 160/205/270 days, returned HTTP 400 on the accessible free RPC; another provider returned HTTP 525 for chain ID. Therefore the sampler observed **zero eligible addresses because it could not enumerate ANY sample accounts**, not because no owner is kickable.

**Record status = INCOMPLETE, not 0 eligible opportunities.** More fresh paid API/archival research is possible, but our $100 capital does not justify buying a subscription without first proving the historical record can yield a current sufficiently large kick.

## 4. External protocol lifecycle finding — important trap

- **Aura Finance (separate from Convex)** officially decided to sunset; [current Aura app](https://app.aura.finance/) says pools are in withdrawal-only mode with staged redemptions. Its older [FAQs](https://docs.aura.finance/developers/frequently-asked-questions) show 0.5% \`earmarkRewards(pid)\` but this is NOT evidence of continuing fresh harvest bounty volume in Oct 2026. **STOP Aura** as a high-frequency keeper candidate.
- **Balancer DAO [BIP-928](https://forum.balancer.fi/t/bip-928-orderly-winddown-of-balancer-and-distribution-of-the-treasury/7107) was approved Sept 29, 2026**; official schedule has applicable pools moving to withdrawals-only Oct 30 and limited v3 extensions until Nov 30. A protocol's historical TVL and gauge emissions are not forward-looking harvest revenue. Avoid coupling Aura/Balancer legacy rewards to an aspirational Nov 12 cash target.
- **Solana Dead Man's Vault** project [main README](https://github.com/Romulus-Sol/DMV) advertises permissionless inherited-vault completion reward default 0.005 SOL and close-rent bounty ~0.01–0.03 SOL, but explicitly publishes its deployed Program ID as **DEVNET**, not a funded mainnet fleet. Its website [changelog](https://dmv.palatinearc.com/changelog.html) confirms the devnet state. **STOP for withdrawable 30-day cash** until independent verified mainnet deployments and available expired vaults.

## 5. Decision and smallest next test

**Do not buy an archival RPC plan, bond CVX, lock tokens, or broadcast transactions.** Cap software effort: all three experiments were completed with read-only GitHub Actions and explicit failure reporting. Neither an executable CRV harvest nor an eligible CVX expired-account kicker has been discovered.

If an authenticated *free* archive/source index becomes available (Blockscout/Etherscan with legitimate free quota, or official subgraph), query one narrow older historical \`Staked\` window on Convex Locker V2, extract limited unique actual account IDs and simulate those addresses using \`eth_call\`. **Do not conflate an HTTP 400 with no registered holders**. If no eligible profitable account is found, rotate quickly to a DIFFERENT well-funded reward type, not another broad on-chain indexing project.

At present: **$100 unspent, zero real user cash received, no verified positive-net caller execution**.
