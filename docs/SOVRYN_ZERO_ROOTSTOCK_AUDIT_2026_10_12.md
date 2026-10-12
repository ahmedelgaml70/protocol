# Sovryn Zero Rootstock: funded-liquidation research — 2026-10-12

**Intended outcome:** legal, real on-chain caller compensation with no upfront speculative deposit and operating capital capped at $100. No tokens, gas, or wallet transactions spent. No profit verified.

## Source-grounded mechanism

Sovryn's own documentation says any external caller can liquidate undercollateralized Zero Lines of Credit and get **20 ZUSD + 0.5% RBTC collateral**, funded from the borrower's reserve/collateral. This is **not** the 200 LUSD amount of Liquity V1. A 20 ZUSD base payment would require 45 successfully won liquidations just to reach $900 gross reward on the fixed component, ignoring market prices and all expenses.

Official sources:
- https://wiki.sovryn.com/en/sovryn-dapp/subprotocols/zero-zusd
- https://build.sovryn.com/builder-portal/smart-contracts/zero/trove_manager
- Official SDK deployment: https://github.com/DistributedCollective/zero
- Rootstock official RPC / chain ID: https://dev.rootstock.io/dev-tools/wallets/metamask/
- External TVL context (not evidence of claimant income): https://defillama.com/protocol/sovryn-zero

### Mainnet parameters used

Rootstock chain ID 30. TroveManager `0x82B09695ee4F214f3A0803683C4AaEc332E4E0a3`; SortedTroves `0xdeEB95480B94f9395514Fe35CAF692A1C788DfE9`; PriceFeed `0x6D1d9574d67e04cf35Fa1d916F763eDDae03b75d`; LiquityBaseParams `0xf8B04A36c36d5DbD1a9Fe7B74897c609d6A17aa2`; ZUSD `0xdB107FA69E33f05180a4C2cE9c2E7CB481645C2d`. All addresses from the published Sovryn Zero mainnet SDK deployment, verified by current `eth_getCode` in live GitHub Actions.

## Live read-only empirical check

- Primary run: https://github.com/ahmedelgaml70/protocol/actions/runs/38256252228
- Provider-fallback run: https://github.com/ahmedelgaml70/protocol/actions/runs/38256360360
- Current-state check successfully accessed public Rootstock and sampled **up to 12 lowest nominal-collateral-ratio** troves from SortedTroves with on-chain price and MCR. **0 currently eligible liquidation simulations** were found in that bounded sample.
- Historic event lookup remains **unknown**, NOT zero. Rootstock's keyless public endpoint explicitly rejects `eth_getLogs` as unavailable (JSON-RPC code -32601). Alternate keyless providers did not produce a complete recent history either. No paid RPC plan or service subscription authorized.
- Receipt economics, reward-token convertibility, competition and opportunity velocity are unverified.

## Security and scope

`research/liquity/sovryn_zero.py` imports a strict JSON-RPC whitelist from `liquity_compensation.py`; no signing/send method is permitted. There are no user wallet credentials or money transfers. GitHub Actions receives `contents:read` only. 10 offline tests passed during successful run.

Zero eligible sampled troves is NOT proof no eligible position exists elsewhere or when market prices change. Even a simulated liquidation could be front-run or revert.

**Decision:** retain as a *small payout* watch hypothesis; not an execution candidate. The $1,000-by-November-12 target remains unproven under the constraints. Avoid putting any part of the $100 into a wallet solely on the basis of the documented reward mechanism.
