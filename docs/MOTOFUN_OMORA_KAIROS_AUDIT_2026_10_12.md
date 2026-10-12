# Research round — Moto.fun live graduation, Omora Base fee collection, Kairos USDC liquidations
**Observed:** 2026-10-12 ~18:13 UTC, latest user capital limit **$10**, user goal **$1,000 as fast as possible**. **NO paid tasks, jobs, clients, outreach, marketing, referrals or speculative capital deposits.** Read-only research only; no keys/wallets/signatures/broadcasts, user cash spent **$0**, user cash received **$0**.

## 1. Moto.fun: nontrivial ETH keeper bounty, currently no eligible frozen coins

**Mechanism confirmed from first-party current documentation**
- [Official Ethereum addresses](https://docs.motoswap.org/dev/addresses): deployed \`LaunchpadCurve\` **0xb65b67e986d7B097652920d72202F2c78319BC2C**, \`LaunchpadLens\` **0xb631697124c8e6Bb6C221Cc017e47D4168bd3411**.
- [Official contract inventory](https://docs.motoswap.org/dev/reference/fun-contracts-full-inventory): \`graduate(address token)\` is public, signerless, paid from the frozen coin pot to \`msg.sender\`; target curve's published starting \`graduationBounty\` setting was **0.015 ETH**, but actual \`bountyNow\` can be clamped at \`pot/50\` and current parameter could have changed. Never quote 0.015 ETH as guaranteed live reward.
- Exact \`LaunchpadLens.graduationReadiness(address)\` returns seven words: readiness \`Ready=0, TooFresh=1, Stale=2, Missing=3, OutOfBand=4, Upstream=5, NotFrozen=6\`, \`readyAt\`, \`minMotoOut\`, \`quotedOut\`, \`deviationBps\`, \`bountyNow\`, \`sellsOpenAt\`. The \`Ready\` status *alone* permits a safe \`eth_call\` preflight, not a guaranteed inclusion.
- \`GasTank.refill(address)\` is also permissionless, but its ETH always goes to **owner-registered payee**, **NOT caller**. This is the same failed claim/recipient class as Hyperlane IGP. Do not attempt to extract its balance.

**Direct reproducible live evidence**
- GitHub source branch **\`research/motofun-keeper-10\`**, script \`research/motofun/live.py\`, safety tests \`test_live.py\`, read-only GitHub workflow \`.github/workflows/motofun-research.yml\`.
- Successful GitHub action: **https://github.com/ahmedelgaml70/protocol/actions/runs/38289424666** (earlier **38289328304** failed because main \`GET /config\` returned HTTP 404; correctly marked incomplete; no false zero).
- Date **October 12, 2026 ~18:13:19 UTC**, official public \`GET https://api.motoswap.org/motofun/stats\` returned: **75 total coins, 69 bonding, ZERO frozen, SIX graduated**, 24-hour traded value ~**$132.73**, 24-hour fees **$1.59277**, cumulative fees ~**$1,962.8196**, 2 trades in 24h, 0 launches in 24h. These are first-party indexed statistics at API read, not an independent full-block audit.
- \`GET /motofun/coins?limit=100\` returned **25 most recent** per page, **hasMore=true**. 23 bonding, 2 graduated, ZERO frozen in that first page. This first-page sample alone is not exhaustive; the independent aggregate venue counts are the stronger zero-frozen indicator.
- \`GET /config\` returned **404**, unlike the official [REST API documentation](https://docs.motoswap.org/dev/fun/api) which claims the route exists. An explicit read-only fallback used the curve/lens addresses independently published by the **official documentation**. At **Ethereum mainnet block 26,178,111**, connected Ethereum RPC verified chain 1 and that both curve and lens had deployed code. It did **not** independently verify live \`graduationBounty()\`, current ownership, upgrade authority or whether the official static docs reflect an upgrade.
- No coin was listed frozen, so no \`graduationReadiness(address)\` simulation or gas estimate was attempted. **Do not claim an actually executable $0.015 ETH payout**.

**Verdict:** **NO current unclaimed graduation reward identified**. The potential per-transaction reward is more meaningful than typical cents-level cranks, but 75 coins only 6 already graduated and **zero** at currently payable frozen stage, with 2 trades in 24 hours. There is no empirical basis for a $990 net short-term income stream. Avoid buying coins, stakers, or running latency competition with platform's own graduation keeper.

## 2. Omora, Base mainnet: public collect but NO caller reward

First-party GitHub repo [Omora contract-code](https://github.com/Omora-Launchpad/contract-code) publicly enumerates V4, V3, V2 and V1 deployment addresses on Base mainnet. Source [contracts/src/FeeManager.sol](https://github.com/Omora-Launchpad/contract-code/blob/main/contracts/src/FeeManager.sol) inspected via connected GitHub app:
- \`collect(PoolId id,uint256 minEthFromTokenSwap)\` is PUBLIC and gathers fee proceeds from Uniswap v4 positions. But code routes them **70% to the creator's claimable balance, 30% to protocol bucket**, NOT to \`msg.sender\`.
- \`claimFees(address currency)\` only pays \`creatorClaimable[msg.sender][currency]\` and \`_resolveRecipient(msg.sender)\`; there is no independent third-party bounty and a claimant cannot choose another user's recipient.
- \`payKol(...)\` and \`withdrawTreasury(...)\` are \`onlyOwner\`. Simply calling public \`collect\` risks paying gas to assist a creator/protocol while receiving $0.

**Verdict STOP**. Real mainnet deployment and fee value do not imply public collector incentives. No Ethereum/Base on-chain transaction performed, no need to build scanner.

## 3. Kairos swaps: potentially material, legal 2% liquidation fee, but current availability UNVERIFIED

**First-party [Kairos learn page](https://kairosswap.com/learn)** says a swap buyer posts a liquidation bounty equal to **2% of their collateral**, returned to buyer if swap settles but paid to **the liquidator** if a qualifying liquidation occurs. [Kairos terms](https://kairosswap.com/terms) confirm liquidation is permissionless and the user can forfeit both collateral and liquidation bounty. This is structurally distinct from lending-liquidation debt funding: a third party may only pay gas, though exact runtime semantics must be independently verified.

**Critical limitations:** The source repo \`kairosswap/protocol\` named in [Guardian's August 25 2026 follow-up](https://www.guardian.security/portfolio/kairos/follow-up-review-2026-08-25/) currently returned **404** to the connected GitHub app, so direct deployment source, verified addresses, market enumeration, any live liquidatable swap, per-swap collateral and earnings CANNOT be independently established. A previous audit described 16 high-severity and many medium findings, with incomplete remediations and permissionless vulnerabilities. Some audit examples are *exploit demonstrations*, NOT safe or approved income strategies. **Do not exploit audit weaknesses, rely on third-party LP value dilution, or open speculative self-trading positions.**

**Simple threshold:** if reward is literally 2% of buyer collateral, a gross **$25 USDC** third-party keeper payout needs **$1,250 collateral in a presently liquidatable swap**, and $990 gross requires $49,500 of aggregate qualifying *liquidated buyer collateral* captured, before gas, contention and conversion. These are arithmetic thresholds, not proof of existing qualified swaps. Live treasury backing != available liquidation opportunity.

**Verdict RESEARCH-HOLD** pending first-party verifiable deployed contracts and exact on-chain candidate/preview. Do not spend the $10 or register.

## Cumulative gates and next decisive direction

- Early decisive proof: Moto venue 0 frozen; Omora public collection pays owner; Kairos 2% could justify research but no verified deployed and open position. All fail present *legitimate transferable positive-net payout* by different mechanisms.
- There is still NO confirmed route to $1,000 from $10 quickly without work or high risk. Promised “money glitches” frequently confuse owner liabilities, public maintenance calls, token-level testnet deployments and tradable cash. Preserve user capital.
- Rather than build new bots indiscriminately, target **on-chain protocol caller fees >=$25** with an exact verified funded and currently eligible item, preferably on cheap Base/Optimism/Arbitrum. Require true claimant vs intended beneficiary.
- If future work retries Moto, use docs addresses only when explicit runtime \`/config\` broken and **verify live bytecode and source**; seek actual frozen coins, not all 75. An apparently frozen listing can become unfrozen and revert before inclusion. Don't silently treat failures as zero.
- Experimental code remains on **draft/unmerged** research branch; README/AGENTS and latest mandate on main should point to this file/PR.

**Result for user:** $10 intact, $0 spent, $0 received, zero verified positive-net current calls.
