# Read-only 0xSplits reward observation (Base)

**Goal:** investigate permissionless caller rewards without spending the $100 research capital, connecting wallets, or broadcasting transactions. The $1,000 goal by November 12, 2026 is aspirational, not projected.

## Source and coverage

- `splits_observer.py` examines **only** 0xSplits V2o2 **Push Splits** created through the official factory on **Base** in the latest **4,000 blocks**.
- The one tracked ERC-20 is **native Base USDC**, contract `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`.
- Official upstream V2o2 Push Split factory: `0x8E8eB0cC6AE34A38B67D5Cf91ACa38f60bc3Ecf4`, from the 0xSplits SDK constants. The observer independently checks deployed bytecode before trusting the address.
- It reads SplitCreated and SplitUpdated events, validates configuration against the on-chain `splitHash()`, checks combined wallet/Warehouse token balance, estimates configured caller reward, then performs `eth_call` of the distribution as an unprivileged dummy caller.
- Gas estimates are best-effort, can omit L1 data fees, and **are not net USD profit**.
- This is a bounded sample, not coverage of previously deployed Push Splits, Pull Splits, other versions/tokens or chains. Zero candidates does not mean zero cross-chain opportunities.

## Run using GitHub Actions

The workflow at `.github/workflows/splits-research.yml` runs on pushes to branch `research/splits-100` affecting these research files. After incorporation into the default branch, it can also be started manually using **Actions → 0xSplits Read-Only Research → Run workflow**.

A run: (1) installs pinned open-source ABI decoding packages; (2) runs four offline tests; (3) tries three public RPC endpoints sequentially, stops after the first full successful observation; (4) uploads JSON under artifact `splits-research-read-only` for seven days, even if scanning fails.

JSON contains `status: observation_not_profit` for a successfully completed bounded read-only scan, or `status: incomplete` for RPC/unavailable data. An error never becomes a fabricated empty result.

**No schedule, wallet, private keys, contract signing, or paid RPC credentials.** The workflow receives `contents: read` permissions.

## Before any execution

Require: independently validated recent real paid caller receipts, present still-open reward, correct configured incentive, current contract and token state, verified execution gas including L1 fees, executable exit depth/slippage, competition and failed-attempt costs, and fresh exact simulation. No transactions or money movement without user approval.

Official upstream references:
- https://github.com/0xSplits/splits-contracts-monorepo/blob/main/packages/splits-v2/src/splitters/push/PushSplit.sol
- https://github.com/0xSplits/splits-contracts-monorepo/blob/main/packages/splits-v2/src/splitters/SplitFactoryV2.sol
- https://github.com/0xSplits/splits-contracts-monorepo/blob/main/packages/splits-v2/src/libraries/SplitV2.sol
- https://github.com/0xSplits/splits-sdk/blob/main/packages/splits-sdk/src/constants/index.ts

**Money spent:** $0. **Income realized:** $0.

## Extended cross-chain historical sampling (research branch)

The separate `splits_expanded.py` scanner extends the original near-tip Base probe without adding wallet or transaction capabilities. Run it from `research/splits`:

```sh
python splits_expanded.py --chain base
python splits_expanded.py --chain optimism
python splits_expanded.py --chain arbitrum
```

Or inspect **0xSplits Historical Cross-Chain Research** GitHub Actions; the matrix scans these chains separately. It samples only four **noncontiguous 1,600-block creation windows**, anchored at latest, 7 days, 30 days and 90 days ago using actual on-chain timestamps, across three officially published V2 PushSplit factory generations. It checks only native USDC, WETH and native coin balances. This is **not** a complete historical index. There is no scheduler and no money-moving path.

The scanner records `status: incomplete` for inaccessible historical blocks or failed per-factory windows. `partial_observation_not_profit` indicates that *some* windows succeeded, not that older contracts were exhaustively checked. A configuration is accepted only when its creation or bounded update event matches the live `splitHash()`. Historical records that do not match are rejected rather than guessed.

If the RPC endpoint prunes older blocks or rejects large historical log ranges, it is unsafe to infer that no deployments exist. The retired upstream `0xSplits/splits-subgraph` repository is deprecated; the official SDK's `https://api.splits.org/graphql` client currently configures an API-key Bearer header. Historical full-index access through that service has **not** been verified without credentials. No paid data plan is configured.

USDC references:
- https://developers.circle.com/stablecoins/usdc-contract-addresses
- https://github.com/0xSplits/splits-sdk/blob/main/packages/splits-sdk/src/constants/index.ts
- https://github.com/0xSplits/splits-sdk/blob/main/packages/splits-sdk/src/subgraph/index.ts

**Stop gate:** if sampled historical factories show no meaningful distributor rewards, do not extrapolate an economic opportunity. Require a directly evidenced, present, successfully simulated positive-net reward before any transaction or further expensive automation.
