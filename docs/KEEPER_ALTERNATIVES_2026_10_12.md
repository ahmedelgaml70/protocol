# Permissionless keeper shortlist — 12 October 2026

**Objective:** research lawful third-party contract-caller rewards with ≤$10 execution budget and no clients or promotion. Goal $1,000 remains aspirational; no live executable profit verified.

## Prioritized candidate: PoolTogether V5 prize claiming

Official documentation says any user may invoke Claimer.claimPrizes to claim other depositors' prizes and earn an auction-derived reward credited to a fee recipient. The PrizePool ClaimedPrize event identifies the token prize, raw claimReward and claimRewardRecipient; the reward accrues and requires later withdrawal. This is a mechanism, **not an open opportunity or realized income**.

Official Base deployment addresses:
- PrizePool: 0x45b2010d8a4f08b53c9fa7544c51dfd9733732cb
- Current Claimer: 0xcdCE635b774DE77cdF791647601dba64a75547ba
- Deprecated Claimer: 0x5ffeee76d1e2d2d1d18ba0bc77d8d047b85e1e87 (old 2026 transactions NOT proof of current activity)
- POOL token: 0xd652C5425aea2Afd5fb142e120FeCf79e18fafc3

**ABI trap:** older PoolTogether/v5-prize-pool source used uint16 drawId and a different event hash, whereas the current official docs link GenerationSoftware/pt-v5-prize-pool revision 568ca55 using ClaimedPrize with uint24 drawId. Historical Arbiscan receipt displays topic0 0x81d4e3306aa30f56dc9c3949abd8c27539b445f9ef380425f39f3f7114888e4f. A detector using the older ABI may falsely report zero payouts. Deployed bytecode/source must still be validated.

New script: python3 pooltogether_claim_history.py --lookback-hours 6. It only uses public read-only Base RPC to verify the contract exists, scan recent ClaimedPrize event rewards, and inspect up to 10 transaction submitters and gas receipts. It does NOT find unclaimed winning accounts or execute claims. A short empty window is not definitive inactivity. The full GitHub revision's tests are not yet executed.

Reward asset must be queried from deployed PrizePool.prizeToken(); do not assume POOL governance token. DeFiLlama's protocol yield fees and token-holder revenues are NOT keeper claimReward income. Old 2026 claims from the deprecated contract do not pass our freshness proof.

## Other candidates and elimination

| Protocol | Documented offer | Key obstacle | Priority |
| --- | --- | --- | --- |
| Ripe Protocol Base / Robinhood Chain | Anyone may liquidate; keeper reward about 1% of debt, subject to collateral surplus | No independently verified actual caller payout; total active borrowing only tens of thousands of dollars in DeFiLlama snapshots; reward asset, deployed calls, liquidity unverified | #2 research |
| GMX V2 | Prepaid order execution fee covers keeper gas | Primarily gas reimbursement; needs signed oracle prices and competes with professional keepers | Low |
| GBLIN treasury keeper | Older marketing cites ETH bounty | Official repo supersedes the previously advertised vault addresses; current auction mechanics differ. Public leaderboard initial zero/loading text is not onchain proof | Reject legacy |
| lolpad.fun Arc | Anyone may graduate locked curve; bounty ramps to max 5 USDC | Bounty is zero first 120 blocks, own keeper normally acts before reward; no actual paid backup bounty verified | Low |
| fillr Solana | Permissionless SOL bounty to filled launch-limit order | Technical docs say devnet pending audit, despite mainnet claims elsewhere; no verifiable payout receipts | Defer |
| Synthetix V3 Base/Arbitrum | Legacy keeper settlement rewards | Official June 14, 2025 blog: Base perpetual futures fully deprecated July 7, 2025; Arbitrum already wound down | Reject |

## Gate 0 checklist

1. Identify the currently deployed contract and correct ABI; reject deprecated addresses.
2. Prove a recent successful fee-paying transaction on this deployment (reward recipient, fee token units, withdrawal path).
3. Match receipt gas to the actual submitting wallet, account for fee recipient potentially differing.
4. Determine token market depth/realizable sale value, price, competition, and failed-attempt costs.
5. Check a CURRENT eligible action and successful read-only simulation. No sending or signing without explicit user approval.

## Primary sources

- https://dev.pooltogether.com/protocol/deployments/base/
- https://dev.pooltogether.com/protocol/guides/bots/claiming-prizes/
- https://dev.pooltogether.com/protocol/reference/prize-pool/prizepool/
- https://dev.pooltogether.com/protocol/reference/prize-claimer/claimer/
- https://github.com/GenerationSoftware/pt-v5-prize-pool/blob/568ca55a911a9310bc767a173a0c8a734f7f158c/src/PrizePool.sol
- https://arbiscan.io/tx/0x45c1f8429341de8e7f1ca0040cac9a5e638c1e8b4fe9fd849718a26a4791b01b
- https://defillama.com/protocol/pooltogether-v5
- https://docs.ripe.finance/core-protocol/04-liquidations
- https://defillama.com/protocol/ripe-protocol
- https://docs.gmx.io/docs/api/contracts/architecture/
- https://github.com/gblinproject/GBLIN-Protocol
- https://lolpad.fun/docs/guides/graduation.html
- https://github.com/usefillr/program
- https://usefillr.app/docs
- https://blog.synthetix.io/l2s-are-dead-long-live-ethereum/

**Profit actually realized by us:** $0. **Capital used:** $0. $10 remains untouched.

## Source verification update — Ripe and PoolTogether

Ripe is not a direct call to AuctionHouse: Teller.vy external liquidateUser/liquidateManyUsers passes msg.sender as keeper, while AuctionHouse.vy requires its caller be the authorized Teller (assert msg.sender == _getTellerAddr()). GREEN/sGREEN rewards are minted through _handleGreenForUser only if totalKeeperRewards > 0.
Actual keeper reward is conditionally derived in AuctionHouse._calcLiqFees as max(minKeeperFee, debt*keeperFeeRatio/HUNDRED_PERCENT), possibly capped by maxKeeperFee and by collateral surplus minus base liquidation fee. Existing liquidation episodes and recovery-free cases can pay ZERO. Merely calling the function, or finding an unhealthy account, does not guarantee payment.
Ripe current source: https://github.com/Ripe-Foundation/ripe-protocol/blob/master/contracts/core/Teller.vy (liquidateUser lines 619-641) and https://github.com/Ripe-Foundation/ripe-protocol/blob/master/contracts/core/AuctionHouse.vy (routing lines 240-284, fees lines 1393-1412).

PoolTogether correction: the reward is denominated in PrizePool.prizeToken(), NOT necessarily the separately documented POOL governance token. The scanner reads deployed prizeToken() (selector 0xd0ef024a, independently checked against Ethereum Keccak), decimals() on that token, and labels tx.to as matching the currently published Claimer or not. Real conversion values cannot be calculated until the reward token is identified on-chain.

Current evidence status: neither Ripe nor the current PoolTogether Base Claimer has a successfully verified recent external-caller net-positive payout in this investigation. No wallet activity authorized.