# SAFE-FAST Day 41 QQQ CFB Execution Context Calculator Review

## Scope

Target candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Setup type: QQQ Clean Fast Break.

Signal/setup time: `2026-04-13T12:30:00-04:00` (`2026-04-13T16:30:00Z`).

Target contract: `QQQ   260427C00615000`.

Instrument id: `1023411456`.

Baseline from task file: `e3f4d44 Add QQQ CFB execution context fixtures`.

This review records implementation of the accepted QQQ CFB execution-context calculator against data-only regression fixtures. It does not fill evidence, backtest, choose a real trade, calculate P&L, claim proof or profitability, mark QQQ ready, or change intake-ready status.

## Artifact Created

Calculator file: `historical_signal_replay/execution_context_calculator.py`.

Test file: `tests/test_execution_context_calculator.py`.

Fixture file used: `historical_signal_replay/fixtures/qqq_cfb_execution_context_regression_fixtures.json`.

Accepted rule source: `SAFE_FAST_DAY41_QQQ_CFB_EXECUTION_CONTEXT_RULE_DECISION.md`.

## Implemented Behavior

- calculates quote age as setup boundary minus selected quote `ts_event`;
- classifies `execution_context_status` as `clean`, `caution`, `fail`, or `unknown`;
- rejects quote `ts_event` after signal as `fail`;
- rejects missing bid, missing ask, bad spread, missing size, and missing setup-time-safe trade volume;
- returns `unknown` for missing source data or unresolved timestamps;
- refuses fallback after the selected/top-ranked contract fails a gate;
- ignores forbidden fill, broker/order/account, outcome, P&L, proof, profitability, and readiness inputs without allowing them to improve status.

## Fixture Results

Fixture count: `13`.

All `13` accepted fixtures passed, including clean and caution quote-age boundaries, stale quote failure, the known QQQ stale quote failure, quote-after-signal rejection, missing bid/ask, bad spread, missing size/volume, missing source data, no fallback, and forbidden P&L/proof/readiness fields.

## Known QQQ Result

The known QQQ selected quote at `2026-04-13T16:06:30.640301037Z` against setup boundary `2026-04-13T16:30:00Z` has calculated quote age `1409.359699` seconds, about `23` minutes `29.359699` seconds.

The calculator result for that fixture is:

- `execution_context_status=fail`;
- `rejection_reason=quote_age_above_5_minutes`.

## Validation

Focused test command:

`python -m unittest tests.test_execution_context_calculator`

Focused test result: PASS, `5` tests, covering all `13` accepted fixtures.

Safe-check command:

`powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`

Safe-check result: PASS, `3` checks.

## Still Not Authorized

Evidence filled: NO.

Backtest authorized: NO.

Real trade chosen: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Intake-ready count changed: NO.

Proof accepted: NO.

Profitability claimed: NO.

Raw Databento files changed: NO.

`main.py`, live/engine trading logic, Railway/deploy files, broker/order/account files, `.env`, secrets, and generated live reports/logs changed: NO.
