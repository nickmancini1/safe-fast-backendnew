# SAFE-FAST Day 41 QQQ CFB Execution Context Fixtures Review

## Scope

Target candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Setup type: QQQ Clean Fast Break.

Signal/setup time: `2026-04-13T12:30:00-04:00` (`2026-04-13T16:30:00Z`).

Target contract: `QQQ   260427C00615000`.

Instrument id: `1023411456`.

Baseline from task file: `4d6d363 Accept QQQ CFB execution context rule`.

This review records data-only regression fixtures for the accepted QQQ CFB execution-context rule. It does not create calculator code, fill evidence, backtest, choose a real trade, calculate P&L, claim proof or profitability, mark QQQ ready, or change intake-ready status.

## Artifact Created

Fixture file: `historical_signal_replay/fixtures/qqq_cfb_execution_context_regression_fixtures.json`.

Fixture count: `13`.

Accepted rule source: `SAFE_FAST_DAY41_QQQ_CFB_EXECUTION_CONTEXT_RULE_DECISION.md`.

## Fixture Coverage

The fixture file covers:

- clean quote age at exactly `60` seconds;
- caution quote age just above `60` seconds;
- caution quote age at exactly `5` minutes;
- fail quote age above `5` minutes;
- known QQQ stale quote fail for `QQQ   260427C00615000` / `instrument_id=1023411456`;
- quote after signal rejected;
- missing bid rejected;
- missing ask rejected;
- bad spread rejected;
- missing size rejected;
- missing volume rejected;
- missing source data returns `unknown`;
- no fallback after selected/top-ranked contract failure, with forbidden P&L/proof/readiness fields rejected.

Each fixture includes:

- `fixture_id`;
- `signal_time`;
- `quote_time`;
- `bid`;
- `ask`;
- `spread`;
- `bid_size`;
- `ask_size`;
- `setup_time_trade_volume`;
- `expected_quote_age_seconds`;
- `expected_execution_context_status`;
- `expected_rejection_reason`;
- `reason`.

## Rule Boundaries Preserved

The fixtures preserve the accepted execution-context boundaries:

- Databento TCBBO `ts_event` is the quote-time source;
- quote age is setup boundary minus selected quote `ts_event`;
- quote at or before setup and quote age `<= 60` seconds is `clean`;
- quote at or before setup and quote age `> 60` seconds and `<= 5` minutes is `caution`;
- quote age `> 5` minutes, quote after signal, spread failure, missing or invalid bid/ask, missing or invalid size, missing setup-time-safe trade volume, or fallback is `fail`;
- missing source data or unresolved timestamp/rule proof is `unknown`;
- later long-call fill testing uses ask only, but this fixture task does not create fill evidence or P&L.

## Validation

JSON parse and required-field validation command:

`python -c "<local required-field validator>"`

Result: PASS, `13` fixtures, required fields present.

Safe-check command:

`powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`

Result: PASS, `3` checks.

## Still Not Authorized

Execution calculator code changed: NO.

Evidence filled: NO.

Backtest authorized: NO.

Real trade chosen: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Intake-ready count changed: NO.

Proof accepted: NO.

Profitability claimed: NO.

Raw Databento files changed: NO.

## Next

The next bounded step, only when explicitly requested, is execution-context calculator/rule implementation against these fixtures. Evidence fill, entry, exit, cost/slippage, proof, profitability, readiness, and intake-ready changes remain blocked.
