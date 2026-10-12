# New cash-reward search: Liquity V1/V2 (12 October 2026)

**Goal:** use at most $100 operating capital to seek up to $1,000 in *withdrawable* net proceeds before November 12, 2026. No customers, jobs, promotional campaigns, speculative token deposits, or signing without explicit user approval.

## Why these contracts were screened

Liquity V1's documented liquidator compensation is **200 LUSD + 0.5% of liquidated ETH collateral**. The official V2 formula is **0.0375 WETH + min(0.5% of eligible collateral, 2 collateral-token units)**, with V2 collateral compensation conditional on the offset fraction. A fixed reward formula is **not** a currently available action. Economic value depends on real token prices, exchange liquidity, competing bots and Ethereum fees.

Primary sources:
- V1 deployed contract addresses and official docs: https://docs.liquity.org/liquity-v1/documentation/resources
- V1 liquidation compensation: https://docs.liquity.org/liquity-v1/faq/borrowing
- V2 deployment addresses (CURRENT): https://docs.liquity.org/v2-documentation/technical-docs-and-audits
- V2 compensation: https://docs.liquity.org/v2-faq/borrowing-and-liquidations
- V2 event ABI: https://github.com/liquity/bold/blob/main/contracts/src/Interfaces/ITroveEvents.sol
- V1 event ABI: https://github.com/liquity/dev/blob/main/packages/contracts/contracts/Interfaces/ITroveManager.sol

**Warning:** Liquity's separate `/v2-documentation/technical-resources` page is labeled *Legacy V2 and Testnet*. Do not point an active opportunity scanner at those older addresses. The current V2 mainnet contracts were checked against *Technical Docs & Audits*.

## Read-only implementation

- `research/liquity/liquity_compensation.py`: Ethereum chain-ID checks; bytecode checks; recent `Liquidation` event reads for V1 ETH and V2 ETH/wstETH/rETH; receipt/fee-token transfer inspection for up to 16 historical events; a 12-position V1 SortedTroves tail eligibility sample with `eth_call` simulations.
- `research/liquity/test_liquity_compensation.py`: offline ABI and non-broadcast safety tests.
- `.github/workflows/liquity-compensation.yml`: push/manual GitHub Actions; no credential or private key; `contents:read`; downloadable JSON artifacts expire after seven days.
- No wallet signing, transactions, gas expenses, or capital use.

## Live evidence

### Completed ~24-hour on-chain sample

**GitHub Actions:** https://github.com/ahmedelgaml70/protocol/actions/runs/38255083682

- Provider: `ethereum-rpc.publicnode.com`; valid Ethereum mainnet check, official contract bytecode presence and successful bounded event log read.
- V1 ETH: 0 `Liquidation` events in sampled ~7,400 blocks.
- V2 ETH: 0.
- V2 wstETH: 0.
- V2 rETH: 0.
- The read-only V1 SortedTroves tail check reviewed up to 12 borrowers and found **0 successfully simulated liquidations**.
- This is a **valid short-window negative**, NOT proof of no potential opportunities outside the time/position scope.

### Seven-day extended historical screen

- Initial extended run: https://github.com/ahmedelgaml70/protocol/actions/runs/38255259774
- Reduced RPC log-range run: https://github.com/ahmedelgaml70/protocol/actions/runs/38255494602

The extended historical lookups returned `status=incomplete` for all four branch scans. A workflow run itself was marked successful because the current V1 tail scan ran, **NOT** because seven-day history was successfully audited. **Never report seven-day event count = 0.** All branch counts are **unknown** for that range. The short-window negative is the only verified on-chain event count.

## Fork investigation and exclusions

- Felix CDP is an active Liquity V2 fork but its own source documents **zero fixed WHYPE gas compensation**; parent Liquity V2 parameters must not be copied onto forks: https://github.com/felixprotocol/felix-contracts
- Nerite Arbitrum site currently warns users to close positions following Kelp hack exposure. Deprioritize for new capital actions: https://www.nerite.org/
- Sovryn Zero Rootstock does have a genuine, different documented formula **20 ZUSD + 0.5% RBTC collateral**, not V1's 200 LUSD. Its 2026 on-chain activity and actual payouts are **unverified**; separate candidate if evidence emerges: https://wiki.sovryn.com/en/sovryn-dapp/subprotocols/zero-zusd
- Money Protocol on Rootstock documents **200 BPD + 0.5% BTC** as a theoretical reward, but DefiLlama showed only ~$6k TVL and no tracked 30-day fees in late September/October 2026; reject as a primary search avenue absent stronger activity evidence: https://defillama.com/protocol/money-protocol

## Decision and next evidence gate

**Current executable positive-net opportunity found: none. Actual money earned: $0. Spent: $0.**

Do not fund a wallet or deploy a liquidator. Keep Liquity on passive source-based watch rather than increasing RPC expenses. A promotion to execution research would require: (1) current eligible collateral position, (2) exact `eth_call` successful simulation at current block, (3) measured gas and real token transfers to caller, (4) net proceeds after fees and conversion, and (5) realistic capture odds versus established bots. Even a positive read-only simulation can become stale or be front-run.

**Economic stop condition:** no payout receipts plus no current candidate means no reason to spend $100 or promise $1,000 in a month. Continue cross-domain prefunded-reward discovery rather than arbitrarily multiplying historical-scan windows.
