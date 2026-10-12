# Payer-first round 3: Permanent Collection + BasedAgents funded tasks (2026-10-12)

## Executive verdict
**No present $25–$100 payable opportunity survived.** User objective remains up to **$100 starting/operating budget**, aspirational **$1,000 total net-withdrawable by 2026-11-12** (requires +$900). **$0 capital spent; $0 income realized; no transactions, signing, task claims or account creation.**

This study follows [canonical handoff](HANDOFF_2026-10-12.md) and [opportunity matrix](OPPORTUNITY_MATRIX_2026-10-12.md). It intentionally tests **present funding** instead of extrapolating from advertised reward formulas or bot frameworks.

## Implementation and direct live proof
- Draft PR #12: https://github.com/ahmedelgaml70/protocol/pull/12
- Separate branch: \`research/prefund-live-gates-100\`, intentionally **draft/unmerged**.
- Strictly read-only: \`research/prefund/prefund_screen.py\` only allows \`eth_call\`, \`eth_getCode\`, \`eth_chainId\`, \`eth_blockNumber\`, \`eth_estimateGas\` and \`eth_gasPrice\`, plus allowlisted **GET** requests to public marketplace routes. No POST, wallet signature, deposit, payout claim, token purchase, account connection, application, commit to third-party repos, transaction submission or state change. Tests in \`test_prefund_screen.py\`.
- CI run after corrected USDC 6-decimal normalization: https://github.com/ahmedelgaml70/protocol/actions/runs/38279897335 ; GitHub Actions uploaded sanitized JSON \`prefund-live-gates.json\` as a short-lived artifact. If the artifact expires, this document preserves the decision and essential observations. Source repositories are external, not modified.

### Candidate 1: Permanent Collection \`BuybackBurner.executeStep(minOut)\`
**Official first-party sources:**
- Source and deployment registry: https://github.com/ripe0x/permanent-collection/blob/master/contracts/deployments.mainnet.json
- Source code https://github.com/ripe0x/permanent-collection/blob/master/contracts/src/BuybackBurner.sol
- Official live site: https://111.ripe.wtf/
- Official published contract addresses: https://111.ripe.wtf/docs/introduction/addresses

**Ethereum mainnet deployment** \`0xf8a2D6F8c58626eE3BcDb4638F2a2f30Fe021242\`, deployed in June 2026. Official BuybackBurner source has permissionless \`executeStep(uint256)\`, reward sent to \`msg.sender\`; ***live deployed parameter getters*** returned \`EXEC_REWARD_BPS()=50\` (0.5% of eligible step), \`EXEC_REWARD_CAP()=0.01 ETH\`. Source function **pro-rates the reward if the swap only partly fills**. The protocol document contains an older contradictory paragraph stating cap 0.05 ETH; use source/live getter **0.01 ETH**, not stale prose.

**Live at Ethereum block 26,177,686 (GitHub Action Oct 12, ~16:48 UTC):**
- Deployed bytecode and chain ID verified.
- \`remainingEth() = 0 ETH\` (no funds currently held for any buyback).
- \`maxStepWei() = 1 ETH\`; \`lastStepBlock()=0\`; \`minBlocksBetweenSteps()=1\`; pacing condition technically passes.
- **Maximum theoretical current gross caller payout: exactly 0 ETH**. Therefore no \`executeStep\` transaction or gas estimate attempted.
- **Decision: STOP / UNTIL A NEW FUNDED BURN APPEARS.** There is no payment to collect at the checked block. Site self-reports 0 active return auctions and 0 permanent traits; the protocol's buyback revenue relies on future return-auction outcomes; it should not be treated as a filled fund just because live bid contains >10 ETH. Bid cash belongs to *Patron*, not the *BuybackBurner*.

Important economic nuance: the contract's **0.01 ETH cap is a maximum** and at 0.5% reward implies needing ~2 ETH of actual permitted per-call step for the cap—but \`maxStepWei\` currently limits each step to 1 ETH, so the effective maximum per step under current settings is **0.005 ETH** (assuming full fill). The currently AVAILABLE maximum remains 0 ETH. No currently funded high-value action, no $900 scale.

### Candidate 2: BasedAgents agent tasks (real USDC platform)
**Official sources:**
- https://github.com/maxfain/basedagents
- https://basedagents.ai/docs/getting-started
- Public unauthenticated endpoint \`https://api.basedagents.ai/v1/tasks?status=open\`
- Public history endpoint \`https://api.basedagents.ai/v1/tasks/settled\`
- Public status endpoint \`https://api.basedagents.ai/v1/status\`
- Release notes https://github.com/maxfain/basedagents/blob/main/docs/releases/v0.9.0.md describe **1 USDC refundable concurrent-claim bond**; note more recent rules may supersede it, and it is a deposit requiring owner consent.
- Code/docs describe default custodial escrow in a platform house wallet on Base USDC. Such internal status is **not yet independent transaction-by-transaction chain verification**. Historic \`settled\` endpoint demonstrates listed claims of paid history but not every on-chain settlement amount verified separately.

**Live public REST GET snapshot Oct 12, ~16:48 UTC:**
- \`/v1/status\`: \`payments=enabled\`, \`escrow=enabled\` (platform-reported status only).
- \`/v1/tasks?status=open\`: **20 open tasks** visible.
- Of these, only **1** was explicitly \`escrow.status="funded"\`, a task called **"Test hire (please ignore)"** with **1,000,000 atomic Base USDC = 1 USDC**, \`claimable=true\`, \`payment_status=pending\`.
- \`funded_open_at_least_25_usdc_count = 0\`.
- Other open items include repeated **Industrial Sentinel** tasks with \`250000\` atomic USDC = **0.25 USDC**, \`2000000\` = **2 USDC**, \`payment_status=pending\` but **no \`escrow.status="funded"\` in returned object**. Do not count them as funded merely because \`claimable=true\`.
- Several trial tasks have **no bounty** and \`payment_status="none"\`. A \`claimable\` flag does NOT establish that the task will pay money.
- \`/v1/tasks/settled\` returned **10 historical entries**, shown with small amounts 0.10, 1, 2 and one 5 USDC in the returned sample. The record count and reward fields are self-reported REST history; the observer did not independently verify the payout tx for each entry or whether they all belong to unrelated buyers.

**Decision: STOP for Nov $900 goal** at current advertised inventory. A $1 "please ignore" testing task is not a commercially suitable objective. 20 open listings do not mean funded new work. Even if every explicitly funded task were paid to user, only $1 could be earned gross from this specific accessible sample, before possible bond and time. No registration, bond payment, claim or submission was made.

## Other new methods tested by first-party source

**PolyDispute:** https://polydispute.finance/how-it-works advertises \`arm()\` pays 10 USDC once an UMA dispute pool has been FULLY FUNDED and suitable market enters a 2h challenge; the site's own documentation says inspect *testnet* pools and warns external audit before mainnet. No independently verified mainnet pool or currently armable paid job, and paying/disputing a gambling market is contrary to user's constraints. **STOP: marketed future/testnet cash ≠ eligible live cash.**

**Aeterna:** https://github.com/ch2llgao/Aeterna documents a 1% keeper bounty for executeInheritance, but the implementation targets **Aave Base Sepolia TESTNET pool** \`0x8bAB6d1b75f19e9eD9fCe8b9BD338844fF79aE27\`. README demonstrates simulated 40-second expiry and testnet deposits, not real mainnet funds. **STOP** for withdrawable target.

**openbounty.app:** https://openbounty.app/ says publishing bounties is **not prefunded**, requires publisher to pay worker *after* evidence approval, and its explanatory flow names **Base Sepolia**. Its homepage “illustrative tasks” are explicitly not actual payouts. Distinguish from \`openbounty.ai\` mock marketplace previously rejected. **STOP** pending actual mainnet public task funding and cleared payments.

## New decision rules (important to preserve)
1. **Published cap is not achievable payout.** Formula \`min(step × 0.5%, 0.01 ETH)\`, live \`maxStep=1 ETH\` → max 0.005 ETH per full-size step, but current \`remainingEth=0\` → available 0 ETH. A near-empty internal balance is more decisive than a protocol-wide ETH live bid.
2. **Six decimals, not 18**: USDC \`250000\` means **$0.25**, not \`$250,000\` or \`$250\`; \`2000000\` is **$2**. Use token decimals and print numeric denomination beside all raw numbers.
3. **\`claimable=true\` is NOT \`escrow.funded\` or \`payment.settled\`.** Pending and unescrowed tasks are not held public cash. Even an API-reported funded escrow still requires independent on-chain/settlement check and genuine accepted work.
4. **Testnets are not cash**. Base Sepolia, Solana devnet, demonstration funding and fake agent bounty cards must be rejected before coding another watcher.
5. **Small real escrow is not sufficient opportunity volume**. One $1 funded test task is actual platform activity, not a plausible $900 portfolio.

## Research conclusion and next action

The user wants larger, novel, globally accessible payouts: we must **discover a sufficiently large *presently escrowed, payable, unreserved task or contract state before implementation***. Do not fill this gap with marketing rewards, future auctions, investor yield, unbacked open tasks, leaked wallets, protocol owner's unclaimed balances or contest entry. Avoid broad GitHub Actions scans without a concrete funding hypothesis.

Current: **$100 remains untouched; $0 earned; no READY verified opportunity.** Follow the canonical [research playbook](RESEARCH_PLAYBOOK.md) and [continuation instructions](CONTINUE_AS_AGENT.md).
