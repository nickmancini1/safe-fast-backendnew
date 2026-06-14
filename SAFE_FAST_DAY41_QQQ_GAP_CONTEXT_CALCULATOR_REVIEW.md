# SAFE-FAST Day 41 QQQ Gap-Context Calculator Review

## Scope

Baseline: `b03976c Add SAFE-FAST project speed layer`.

Candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Setup type: QQQ Clean Fast Break.

Signal/setup time: `2026-04-13T12:30:00-04:00`.

This task implemented the QQQ Clean Fast Break gap-context calculator against the accepted regression fixtures. It did not fill evidence, backtest, choose a trade, calculate P&L, accept proof, claim profitability, or mark the candidate ready.

## Files Created

- `historical_signal_replay/gap_context_calculator.py`
- `tests/test_gap_context_calculator.py`

## Calculator Behavior

The calculator:

- calculates gap amount as `signal_day_open - previous_close`;
- calculates gap percent as `(signal_day_open - previous_close) / previous_close * 100`;
- classifies status using the accepted fixture thresholds:
  - `clean`: absolute gap percent `<= 0.30%`;
  - `caution`: absolute gap percent `> 0.30%` and `<= 0.75%`;
  - `fail`: absolute gap percent `> 0.75%`;
  - `unknown`: missing, invalid, wrong-symbol, or unproven no-hindsight inputs;
- returns `gap_context_as_of` from the latest allowed source timestamp;
- returns `gap_context_reviewed_before_signal` only when required inputs and no-hindsight timing pass;
- reports post-signal source timestamps in `rejected_future_source_times` and does not let them change setup-time gap context;
- returns clear missing-data errors for missing previous close and signal-day open;
- exposes refusal helpers for trade choice, P&L, proof, and readiness inference.

## Regression Coverage

Focused tests use `historical_signal_replay/fixtures/qqq_gap_context_regression_fixtures.json` and cover:

- clean boundary at exactly `+0.30%`;
- caution lower boundary just above `+0.30%`;
- caution upper boundary at exactly `+0.75%`;
- fail just above `+0.75%`;
- missing previous close as `unknown`;
- missing signal-day open as `unknown`;
- future-data rejection for `2026-04-13T13:30:00-04:00`;
- known QQQ target fixture returning `clean`;
- no output field or helper implying trade choice, P&L, proof, or readiness.

## Known QQQ Target Result

Inputs:

- Previous regular-session close: `611.02`.
- Signal-day open: `609.455`.
- Signal/setup time: `2026-04-13T12:30:00-04:00`.

Calculator result under the accepted fixture rule:

- Gap amount: `-1.565`.
- Gap percent: about `-0.2561290956106183%`.
- Direction: `down`.
- Gap-context status: `clean`.
- Gap-context as-of: `2026-04-13T12:30:00-04:00`.
- Reviewed before signal: `true`.

This is a tested fixture-label result only. It is not evidence fill, trade proof, profitability proof, or readiness.

## Tests Run

- `python -m unittest tests.test_gap_context_calculator`: PASS, 8 tests.
- `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`: PASS, 3 checks.

## Guardrails Preserved

- Evidence filled: NO.
- Backtest authorized: NO.
- Trade chosen: NO.
- P&L calculated: NO.
- QQQ candidate marked ready: NO.
- Intake-ready count changed: NO.
- Proof accepted: NO.
- Profitability claimed: NO.
- Raw Databento files changed: NO.
- `main.py`, live/engine/broker/order/account/Railway files, `.env`, secrets, generated reports/logs, trade-selection code, backtest code, and P&L files changed: NO.
