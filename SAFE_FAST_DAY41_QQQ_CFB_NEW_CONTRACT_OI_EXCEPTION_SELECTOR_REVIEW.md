# SAFE-FAST Day 41 QQQ CFB New-Contract OI Exception Selector Review

## Scope

Target candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Setup type: QQQ Clean Fast Break.

Signal/setup time: `2026-04-13T12:30:00-04:00` (`2026-04-13T16:30:00Z`).

Target contract: `QQQ   260427C00615000`.

Instrument id: `1023411456`.

Baseline from task file: `fbaa6b6 Add QQQ CFB new contract OI exception fixtures`.

This review records the selector implementation for the accepted new-contract open-interest exception. It does not fill evidence, backtest, choose a real trade, calculate P&L, claim proof or profitability, mark QQQ ready, or change intake-ready status.

## Implementation

Updated selector file: `historical_signal_replay/cfb_contract_selector.py`.

Updated test file: `tests/test_cfb_contract_selector.py`.

The selector now includes `evaluate_new_contract_oi_exception_from_fixture` and `evaluate_new_contract_oi_exception` for the accepted listing-aware exception.

The original `select_contract_from_fixture` and `select_contract` contract-selection path remains unchanged for the original 18 fixtures.

## Accepted Behavior

The new exception evaluator returns `option_context_status=caution` only when:

- the already selected contract identity is present;
- the contract was listed before the setup/signal boundary;
- the selected contract did not exist on the prior trading day;
- a setup-time-safe quote exists;
- spread is at or below `0.15`;
- spread percent is at or below `2.00%`;
- bid size is at least `1`;
- ask size is at least `1`;
- setup-time trade volume is at least `1`;
- no setup-time-safe open interest exists only because the contract is newly listed;
- no future data is detected;
- no fallback is used.

The evaluator still returns `unknown` for listing-after-signal, prior-day-present missing open interest, missing listing timestamp, missing quote, quote-after-signal, spread failure, spread-percent failure, bid-size failure, ask-size failure, trade-volume failure, no-fallback failure, and future-data detection.

## Regression Results

Command:

`python -m unittest tests.test_cfb_contract_selector`

Result: PASS, `12` tests.

Coverage:

- original contract-selection fixtures: `18` passing;
- new-contract open-interest exception fixtures: `13` passing;
- valid new-contract exception returns `caution`;
- prior-day-present missing open interest remains `unknown`;
- no-fallback and future-data rejection are preserved;
- selector outputs still do not infer trade choice, fill, P&L, proof, profitability, or readiness.

Safe-check command:

`powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`

Result: PASS, `3` checks.

## Not Changed

Evidence filled: NO.

Backtest authorized: NO.

Real trade chosen: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Intake-ready count changed: NO.

Proof accepted: NO.

Profitability claimed: NO.

Raw Databento files changed: NO.

`main.py`, live/engine trading logic, broker/order/account files, Railway/deploy files, `.env`, secrets, generated live reports, and generated live logs changed: NO.
