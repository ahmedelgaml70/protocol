# Roadmap (revisable, evidence-driven)

## Phase 0 — workspace / knowledge capture
- [x] Create public `protocol` repository.
- [x] Record original prompts and constraints.
- [x] Document known mechanisms, blockers, research standards and capital guardrails.

## Phase 1 — proof of events, $0 at risk
- [x] Prepare read-only Kerf order and history scanning.
- [x] Offline unit tests.
- [ ] Connect to a working chain RPC outside the isolated tool environment.
- [ ] Capture a time-stamped report with deployed bytecode and event history.
- [ ] Establish whether actual caller rewards have happened.

## Phase 2 — measure accessible opportunity
- [ ] Confirm current verified deployed source, upgradeability, underlying token liquidity.
- [ ] Find one OPEN opportunity and record its chain/block/transaction evidence.
- [ ] Measure observed keeper concentration, reward frequency, and latency.
- [ ] Check competitors on at least one additional low-fee chain/protocol (Superfluid first).
- [ ] Model realistic gas, conversion and failed-call costs.

## Phase 3 — decision, not automatic execution
- [ ] Compare opportunity gross vs conservative realizable net under a $10 budget.
- [ ] Call simulation or fork dry-run, prove exact caller permission and expected token receipt.
- [ ] Obtain explicit approval for any real transaction or spending.
- [ ] Log post-trade net with receipts only if a user-approved execution occurs.

## Pivot triggers
Pivot if there are no paid events in a meaningful window, rewards are entirely captured by protected keepers, economics cannot be priced, contract code is unaudited/unverifiable, chain is inaccessible, or reward cannot be withdrawn.

## Why this is not an autonomous money printer
Read-only code doesn't make money; contracts don't reserve public rewards; the profitability of historically paid bounties does not show a new entrant can win. This project searches for evidence first.

## Added investigations

- [x] Inspect three extra published reward mechanisms in Kerf.
- [x] Create read-only event history census for PositionKeeper, LPVault and PreMarketPerp.
- [x] Check selectors/topics against local Ethereum Keccak reference implementation.
- [ ] Run `make test` on the committed GitHub revision; fix any failures.
- [ ] Run `make multi-history` from a machine with RPC access; record block range, raw events and keeper concentration.
- [ ] Enumerate **all** VaultFactory vaults if six seed vaults show paid activity.
- [ ] Confirm all deployed source/bytecode and token payout transfer events on Blockscout.
- [ ] Assess eligible actions with truly positive **net** realized-value rewards.

## Low-friction on-chain evidence
- [x] Identify keyless read-only RPC with current `eth_call`, `eth_getCode` and gas estimation.
- [x] Add `make scan-free` to check the 10 newest published Kerf orders without credentials.
- [ ] Run this command from a network-accessible machine and preserve the report block number, results and errors.
- [ ] Measure **timestamp coverage** for each historical scan; do not assume 30k blocks = a day.
- [ ] Use historical events from official RPC/provider supporting `eth_getLogs`, to quantify keeper profits rather than assuming gross bounty is profit.

## Evidence-first pivot after live report

- [x] Receive first user RPC report for Kerf RangeOrders (block 86,104,491): `nextOrderId=1`, zero orders and errors.
- [x] Archive sanitized report and deprioritize this contract.
- [ ] Identify **one deployed protocol with receipt-verified historical positive caller payouts** before building another scanner.
- [ ] Verify actual *current* eligible opportunities separately; don't infer from historic activity.
- [ ] Compare true net after gas, priority, exit liquidity, token sale and failed attempts; risk budget ≤$10.

## Superfluid receipt-first progress
- [x] Find publicly inspectable successful historical third-party token transfers (Base May 9–10, 2026).
- [x] Capture raw token inflow and ETH gas data with explorer provenance.
- [x] Add read-only reproducible `superfluid_receipts.py` and offline test fixtures.
- [ ] Run full GitHub checkout's unit tests and receipt RPC audit from a connected machine.
- [ ] Obtain **recent** event counts and payee concentration by month, especially September–October 2026.
- [ ] Determine which independent callers receive rewards vs designated TOGA Patrician in each phase.
- [ ] Verify token exit liquidity, gas, caller competition, and **currently eligible** Pleb/Pirate opportunity.
