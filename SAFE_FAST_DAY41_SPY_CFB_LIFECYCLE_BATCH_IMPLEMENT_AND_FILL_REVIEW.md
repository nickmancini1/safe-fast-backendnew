# SAFE-FAST Day 41 SPY CFB Lifecycle Batch Implement And Fill Review

## Scope

- Candidates:
  - `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`
  - `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`
- Task mode: grouped calculator/test implementation and lifecycle-only evidence fill.
- Baseline stated by task file: `570f29c Add grouped SPY CFB lifecycle rule fixtures`.

## Implementation

- Reused `historical_signal_replay/cfb_lifecycle_calculator.py`.
- Extended calculator support for the accepted SPY lifecycle rule metadata:
  - `spy_cfb_exact_signal_candle_freshness`.
- Preserved existing QQQ lifecycle defaults and unsafe-inference refusal helpers.
- Added fixture identity inference so fixture-driven calls validate expected `QQQ` or `SPY` symbol from `candidate_id`.
- Added the accepted SPY higher-base watch behavior: a higher-base watch row with no completed breakout remains `stale` rather than being consumed as `spent` only because an earlier break existed.

## Tests

- Updated `tests/test_cfb_lifecycle_calculator.py`.
- Existing QQQ lifecycle fixture coverage remains: `18` fixtures.
- New SPY lifecycle fixture coverage: `12` fixtures from `historical_signal_replay/fixtures/spy_cfb_lifecycle_regression_fixtures.json`.
- Focused SPY tests cover:
  - SPY CFB 002 fresh initial break, spent same-session follow-through, and expired later review.
  - SPY CFB 003 stale higher-base watch, fresh higher-base break, and later spent context.
  - wrong symbol/setup, missing trigger/invalidation, future replay-row rejection, and forbidden option/fill/P&L/proof/profitability/readiness inputs.

## Evidence Fill

Filled only lifecycle/stale-spent/expiry evidence rows:

- `historical_signal_replay/source_data/richer_export_package_work/spy_cfb_002_initial_break_expiry_rule_regressions.jsonl`
  - `fill_status=complete`
  - `clean_fast_break_initial_break_expiry_rule` filled from the accepted grouped SPY CFB lifecycle package.
  - `initial_break_expiry_regression_rows` filled from the accepted SPY fixture file and calculator-backed test coverage.
- `historical_signal_replay/source_data/richer_export_package_work/spy_cfb_003_higher_base_fresh_break_expiry_rule_regressions.jsonl`
  - `fill_status=complete`
  - `clean_fast_break_higher_base_fresh_break_expiry_rule` filled from the accepted grouped SPY CFB lifecycle package.
  - `higher_base_fresh_break_expiry_regression_rows` filled from the accepted SPY fixture file and calculator-backed test coverage.

No context/caution evidence fields were changed.

## Validation

- `python -m unittest tests.test_cfb_lifecycle_calculator`
  - Result: PASS, `10` tests.
- `python -m watcher_foundation.source_evidence_work_package_content_validator`
  - Result: PASS command.
  - Work files checked: `9`.
  - Passed requests: `5`.
  - Failed requests: `4`.
  - Partial rows: `4`.
  - Header-only rows: `0`.
- `python -m watcher_foundation.source_evidence_package_to_intake_bridge`
  - Result: PASS command.
  - Passed requests: `5`.
  - Failed requests: `4`.
  - Reconsideration-eligible candidates: `1` (`QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` only).
  - SPY CFB 002 decision: `parked/source_data_insufficient`.
  - SPY CFB 003 decision: `parked/source_data_insufficient`.
  - Intake-ready count: `0`.
  - Proof allowed: `NO`.

## Guardrails

- Evidence filled: lifecycle/stale-spent/expiry only.
- Raw Databento files changed: NO.
- Databento downloaded: NO.
- Full-window data used or requested: NO.
- Backtest authorized or run: NO.
- Real trade chosen: NO.
- P&L calculated: NO.
- Candidate marked ready: NO.
- Intake-ready count changed: NO.
- Proof accepted: NO.
- Profitability claim made: NO.
- `main.py`, live/engine trading logic, Railway/deploy files, broker/order/account files, `.env`, secrets, generated live reports/logs, raw vendor data, trade-selection code, and P&L files changed: NO.

## Remaining Blockers

- SPY CFB 002 context/caution row remains blocked on:
  - `option_context_status`
  - `headline_context_status`
  - `execution_context_status`
  - `complete_caution_review_status`
- SPY CFB 003 context/caution row remains blocked on:
  - `option_context_status`
  - `headline_context_status`
  - `execution_context_status`
  - `complete_caution_review_status`
- SPY CFB contract-selection, headline/no-headline source policy, execution context, entry, fill, exit, stop/invalidation, time exit, cost/slippage, sample-size, and promotion gates remain undecided.
