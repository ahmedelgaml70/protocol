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
