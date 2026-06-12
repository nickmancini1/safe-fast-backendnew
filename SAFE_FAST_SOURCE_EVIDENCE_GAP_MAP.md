# SAFE-FAST Source-Evidence Gap Map

## Scope

This build-only gap map records the source fields and rule evidence missing from the four parked/source-data-insufficient rows.

It is not proof review. It does not accept proof, claim profitability, reactivate parked rows, authorize live data, authorize alerts, authorize broker/order/account work, authorize Railway/deploy work, or authorize changes to `main.py`.

Proof accepted: NO.

Profitability claim made: NO.

Current intake-ready count: 0.

## Summary

- Gap scanner: `watcher_foundation/source_evidence_gap_scanner.py`.
- Scanner test: `tests/test_source_evidence_gap_scanner.py`.
- Acquisition request: `SAFE_FAST_SOURCE_EVIDENCE_ACQUISITION_REQUEST.md`.
- Acquisition validator: `watcher_foundation/source_evidence_acquisition_validator.py`.
- Parked rows covered: 4.
- Gap rows: 9.
- Acquisition request rows: 9.
- Acquisition validator requests represented: 9.
- Acquisition validator current no-evidence result: 9 failed requests; parked rows stay parked.
- Required evidence families represented: 6.
- Current repo data sufficient for any parked row: NO.
- Current repo data can supply acquisition request evidence now: NO.
- Intake-ready count: 0.
- Parked/source_data_insufficient count: 4.
- Replace count: 3.

## Required Evidence Families

- QQQ gap-context completeness.
- Clean Fast Break stale/spent expiry.
- Clean Fast Break higher-base/fresh-break expiry.
- Clean Fast Break initial-break expiry.
- SPY Ideal stale/spent expiry.
- Complete context/caution fields.

## Schema Evidence Checked

- `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv` header contains OHLCV plus `context_24h_status`, `macro_context_status`, `iv_context_status`, `event_context_status`, and matching as-of fields. It does not contain gap, room, option, headline, execution, or complete caution-review fields.
- `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` header contains OHLCV plus `context_24h_status`, `macro_context_status`, `iv_context_status`, `event_context_status`, and matching as-of fields. It does not contain gap, room, option, headline, execution, or complete caution-review fields.
- `historical_signal_replay/reports/first_real_qqq_clean_fast_break_replay_v1_signal_log.jsonl` has lifecycle labels and unconfirmed context fields, but no accepted QQQ gap-context completeness field and no accepted Clean Fast Break stale/spent expiry rule.
- `historical_signal_replay/reports/third_real_spy_clean_fast_break_replay_v1_signal_log.jsonl` has initial-break, higher-base/fresh-break, and spent lifecycle labels, but no accepted setup-time Clean Fast Break expiry rule.
- `historical_signal_replay/reports/second_real_spy_ideal_replay_v1_signal_log.jsonl` has triggered and spent lifecycle labels, but no accepted setup-time SPY Ideal stale/spent expiry rule.

## Gap Table

| Candidate ID | Evidence family | Existing source evidence checked | Missing field names or rule names | Current repo has required evidence | Current repo data sufficient for row | Status | Proof allowed |
|---|---|---|---|---|---|---|---|
| `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | QQQ gap-context completeness | QQQ source CSV line 132; QQQ Clean Fast Break log lines 3-4 | `gap_context_status`; `gap_context_as_of`; `gap_context_reviewed_before_signal` | NO | NO | `parked/source_data_insufficient` | NO |
| `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | Clean Fast Break stale/spent expiry | QQQ Clean Fast Break log lines 3-6; rule-family decision table; rule-gate tests | `clean_fast_break_stale_spent_expiry_rule`; `clean_fast_break_expiry_regression_rows` | NO | NO | `parked/source_data_insufficient` | NO |
| `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | Complete context/caution fields | QQQ source CSV line 132; QQQ Clean Fast Break log line 3 | `option_context_status`; `headline_context_status`; `execution_context_status`; `complete_caution_review_status` | NO | NO | `parked/source_data_insufficient` | NO |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | Clean Fast Break higher-base/fresh-break expiry | SPY source CSV line 154; SPY Clean Fast Break log lines 5-6 | `clean_fast_break_higher_base_fresh_break_expiry_rule`; `higher_base_fresh_break_expiry_regression_rows` | NO | NO | `parked/source_data_insufficient` | NO |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | Complete context/caution fields | SPY source CSV line 154; SPY Clean Fast Break log line 5 | `option_context_status`; `headline_context_status`; `execution_context_status`; `complete_caution_review_status` | NO | NO | `parked/source_data_insufficient` | NO |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | Clean Fast Break initial-break expiry | SPY source CSV line 138; SPY Clean Fast Break log lines 2-3 | `clean_fast_break_initial_break_expiry_rule`; `initial_break_expiry_regression_rows` | NO | NO | `parked/source_data_insufficient` | NO |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | Complete context/caution fields | SPY source CSV line 138; SPY Clean Fast Break log line 2 | `option_context_status`; `headline_context_status`; `execution_context_status`; `complete_caution_review_status` | NO | NO | `parked/source_data_insufficient` | NO |
| `SPY-REAL-HISTORICAL-IDEAL-001` | SPY Ideal stale/spent expiry | SPY source CSV line 291; SPY Ideal log lines 5-6 | `spy_ideal_stale_spent_expiry_rule`; `spy_ideal_expiry_regression_rows` | NO | NO | `parked/source_data_insufficient` | NO |
| `SPY-REAL-HISTORICAL-IDEAL-001` | Complete context/caution fields | SPY source CSV line 291; SPY Ideal log line 5 | `gap_context_status`; `headline_context_status`; `option_context_status`; `execution_context_status`; `complete_caution_review_status` | NO | NO | `parked/source_data_insufficient` | NO |

## Row Results

- `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`: current repo data sufficient: NO; required missing fields/rules are QQQ gap-context completeness, Clean Fast Break stale/spent expiry, and complete context/caution fields.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`: current repo data sufficient: NO; required missing fields/rules are Clean Fast Break higher-base/fresh-break expiry and complete context/caution fields.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`: current repo data sufficient: NO; required missing fields/rules are Clean Fast Break initial-break expiry and complete context/caution fields.
- `SPY-REAL-HISTORICAL-IDEAL-001`: current repo data sufficient: NO; required missing fields/rules are SPY Ideal stale/spent expiry and complete context/caution fields.

## Acquisition Request Result

- Acquisition request path: `SAFE_FAST_SOURCE_EVIDENCE_ACQUISITION_REQUEST.md`.
- Acquisition request rows: 9.
- All 4 parked rows covered: YES.
- Every gap row has an acquisition request: YES.
- Current repo data can supply requested evidence now: NO.
- Expected action after acquisition: rerun `python -B -m watcher_foundation.source_evidence_gap_scanner` and `python -B -m watcher_foundation.candidate_source_pool_intake`; keep rows parked unless source-backed fields/rules and required regressions are present.
- Proof accepted: NO.
- Profitability claim made: NO.

## Guardrail Result

No parked row can be reactivated from lifecycle labels, `final_verdict=TRADE`, primary blocker null, or unconfirmed context fields.

Proof accepted: NO.

Profitability claim made: NO.

## Acquisition Validator Result

- Validator path: `watcher_foundation/source_evidence_acquisition_validator.py`.
- Validator doc: `SAFE_FAST_SOURCE_EVIDENCE_ACQUISITION_VALIDATOR.md`.
- Validator test: `tests/test_source_evidence_acquisition_validator.py`.
- Requests represented: 9.
- Parked rows covered: 4.
- Current no-evidence validation result: all acquisition requests fail validation as blockers; parked rows stay parked.
- Intake-ready count: 0.
- Parked/source_data_insufficient count: 4.
- Replace count: 3.
- Proof accepted: NO.
- Profitability claim made: NO.
