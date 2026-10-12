# October 12, 2026 — live Arc/Base escrow boards and Bountic funded issue audit

## Operating charter and verdict
User's current objective is to pursue **$1,000 total withdrawable** by November 12, 2026, beginning with at most **$100 operating capital**, entirely online. This is an aggressive aspiration, **not a forecast**. The required net gain is $900. Keep the strict exclusions: no client solicitation, paid bidding/competition, security exploitation, conventional AI-training jobs, contest entry, marketing/referrals, speculative token bets or purchasing supplier inventory, and no third-party account, payments, contracts or signed transactions without express approval.

**Research-only result: $0 spent; $0 earned; zero currently open jobs on the two completed mainnet USDC boards. No READY $25+ payout.**

## A. Two genuinely deployed permissionless task escrows (historically paid)

Primary code source: https://github.com/Sofiia7/ARC/blob/main/frontend/app/api/v1/bounties/route.ts and https://github.com/Sofiia7/ARC/blob/main/frontend/lib/publicApi.ts . First-party official [developers guide](https://arcbounty.app/developers) says the public \`/api/v1/bounties?status=open\` reads blockchain storage, JSON API is free/no key, 30-second cache. States returned as decimals in USDC; output explicitly includes reservedFor, audience, workerBondRequired, workerBondUsdc, fee-adjusted workerPayoutUsdc and deadline. A future available job must pass all those constraints; a reserved-for-specific-address bounty cannot be taken by a new random wallet.

Official deployed adapter addresses [contracts/DEPLOYMENTS.md](https://github.com/Sofiia7/ARC/blob/main/contracts/DEPLOYMENTS.md):
- Arc mainnet chain 5042, adapter \`0x73c617e808ED5c7Ca41413DFC6EE940dDcBb0b8D\`, escrow \`0x64cA39Fc57315D0D488acCaC07c37C6E841CD058\`, ERC20 USDC 6 decimals, native gas token USDC (network currency 18 decimals); v4.7. The code/docs say a 2-of-3 Safe controls the escrow proxy upgrade. \`maxBountyAmount\` per new task = 500 USDC.
- Base mainnet chain 8453, adapter \`0x32c215908a46Eb5D34e4E5146c99891eD3014Fee\`, escrow \`0x6D9317eC0Fca3aFd5439d539064DBA94197c4AC4\`; v4.7. Governance source notes remaining single-EOA arbitrator authority before a Safe acceptance action.
- Task-worker fee 1% off the gross, plus network gas and possible refundable worker bond: official [startup](https://arcbounty.app/start) and [SDK](https://www.npmjs.com/package/arcbounty-agent-sdk). On Arc, work may be agent-only, human-only, or anyone and agent-only listings require ERC-8004 identity. Work release can be auto-approved only **14 days** after review silence, with disputes lasting longer. Therefore same-day payout is not guaranteed merely by completing work.

### Actual live API inventory, timestamped

GitHub Actions run: **https://github.com/ahmedelgaml70/protocol/actions/runs/38283082911**.
Run obtained successful HTTP JSON from both official mainnet \`/api/v1/stats\`, \`/api/v1/bounties?status=open\`, \`/api/v1/bounties?status=paid\`; both chainId/testnet flags independently checked against official deployment config (API report, not independent chain node proof). Github Actions passed all four offline safety tests and preserved full JSON report artifact for 7 days.

**Observed 2026-10-12 17:16 UTC:**

| Current API report | ArcBounty, chain 5042 | BaseBounty, chain 8453 |
| --- | ---: | ---: |
| Historical posted jobs | 16 | 9 |
| Historical approved/auto-approved paid jobs | 12 | 3 |
| Historical gross posted USDC | 40.00 | 11.00 |
| Historical payout to workers, net of protocol fee, USDC | **22.77** | **2.97** |
| Currently open jobs / unreserved jobs | **0 / 0** | **0 / 0** |
| Available net worker reward in current open jobs | **0 USDC** | **0 USDC** |
| Open jobs with net ≥25 USDC | **0** | **0** |

Arc's paid list includes net payments of 0.99, 1.98 and 2.97 USDC; Base's three payments all 0.99 USDC. First-party Sep 16 report also described an outside agent getting 7.92 USDC from four tasks, which is encouraging as real paid infrastructure, **not** a currently open bounty for us.

**Strong bounded negative:** As of the stated API storage snapshot, *no* jobs existed in the \`open\` status on either board. We cannot earn already-completed historic payouts. New listings could appear later. This is not a claim that no jobs exist on other chains or sites, nor independent verification of every historic transfer.

Source account distinction: The Arc and Base deployed contracts are separate and the two sites may have some shared developer/operator traffic; don't treat them as independent scalable consumer demand in forecasting. Mainnet USC payment needs wallet/gas and settlement; no account was registered, wallet funded, or task claimed.

## B. Bountic — issuer-claimed funded USDC issue, not proven payouts

Official marketplace: https://bountic.vercel.app/ , explorer https://bountic.vercel.app/explore , specific open listing https://bountic.vercel.app/b/skndash96/bountic/issues/12 ; official GitHub Marketplace listing https://github.com/marketplace/bountic-app .

Publisher UI snapshot 2026-10-12: **5 bounties created, $55 total funded, ZERO payouts made**. Explorer lists 4 locked issues ($35, $5, $5 and $0) and only **one open listed issue** for **$10**.
- Issue #12 has **nineteen separately listed competing pull requests** in its public activity feed, for the same $10 nominal fund. Publication counts may include stale/duplicate submissions and don't establish 19 currently valid contestants, but are sufficient evidence of crowding.
- Page header identifies a feature request "Multiple PR contributors payout distribution", while the displayed issue body asks about a Medusa \`inventory_quantity\` cart GET bug — **scope ambiguity**. Do not start work until clarified and payment terms verifiable.
- Even when PR merges, the Bountic marketplace [official README](https://github.com/marketplace/bountic-app) says the maintainer must **click approve or reply /approve** to release funds. This is discretionary, not automatic when any contributor files a PR. Zero paid history means G2 not met.
- The UI's $55 funded is **platform-provided**, not independently matched to escrow tx custody; zero payouts means there is no demonstrated worker payment. No third-party PR sent.

**Decision: REJECT $10 opportunity** because payoff is tiny, coding-specific, heavily competed and payout method/history insufficient. DO NOT confuse $55 total pooled budget with new worker entitlement.

## C. Further unrelated escrow ideas excluded early

- [AgentPay](https://github.com/ndsgbm-web/agentpay) publicly documents collateral USDC pool and task scraping, but the given deployment is **Base Sepolia testnet**, using mock USDC; no mainnet paid-worker receipts. **Reject**.
- [Legwork](https://github.com/RubenSousaDinis/legwork) runs Base Sepolia USDC escrow demonstration; requires **physical-location, World ID verified human** tasks rather than remote PC work; $3 real errand was **paid separately from testnet**, not a programmable new Internet-only bounty. **Reject**.
- [Aither](https://aither.site/) advertises Q4 "queued" 100 USDC adversarial review of escrow and bond contracts, but security audit is **user excluded**, and Q4 placeholder is not open funded cash; 3 USDC writing item similarly queued, not available. **Reject**.
- [Agent Bounties Github issues](https://github.com/NSPG13/agent-bounties) may show funded/settled historical jobs at 0.10–2 USDC, and GMV prize contests that explicitly require funding other people's work, sometimes despite ongoing public issue status. Prior Protocol study ruled out unverified high-value open claim. **Do not infer live reward from a label, a past claim, or a creator's GMV prize**.

## Implementation / permission scope

- Branch \`research/arc-base-escrow-100\` (unmerged), code \`research/arc_bounty/board_probe.py\`, four test cases \`test_board_probe.py\`, GitHub workflow \`.github/workflows/arc-base-readonly.yml\`; HTTP GET allowlist with no credential/POST/signer, rejects testnet/wrong-chain/API errors as incomplete.
- CI trigger: manual or on branch source changes only, no automatic recurring jobs or third-party software installation. \`contents:read\`; developer spend and money transferred **$0**. Artifacts expire after seven days; this document retains core quantified results.
- The user explicitly requested every investigation be legible to any future agent. Record this in the root handoff/decision matrix after review. Do **not** merge research branches without permission.

## Next action / strategy decision

The mere fact an outsider was paid or an official smart escrow exists does NOT imply open unclaimed work. These two real mainnet escrows show a combined **$25.74 historically paid net USDC across their entire recorded existence**, compared to the **$900 net incremental target**, and **zero current open jobs**. That is strong scale evidence against putting developer time into a competing generic worker bot on these two platforms. Bountic has $55 advertised funding but no completed payouts and 19 PR submissions toward only one visible open $10 issue.

**New research gate:** Do not implement keeper/agent integration unless a *specific present, unreserved reward* is verified at **≥$25 net**, and aggregate payout velocity can support ~$900 net before deadline without spending material capital. If all externally accessible current reward venues fail that gate, do not force a speculative 10× return. Preserve the original $100.

**Current state:** $100 available, $0 spent, $0 earned, zero discovered currently executable positive-net $25+ earning opportunities.
