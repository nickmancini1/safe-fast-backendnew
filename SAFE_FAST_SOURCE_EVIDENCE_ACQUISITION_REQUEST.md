# SAFE-FAST Source-Evidence Acquisition Request

## Scope

This build-only request converts `SAFE_FAST_SOURCE_EVIDENCE_GAP_MAP.md` into the exact source evidence needed before any parked/source-data-insufficient path can be reconsidered.

It is not proof review. It does not accept proof, claim profitability, reactivate parked rows, authorize live data, authorize alerts, authorize broker/order/account work, authorize Railway/deploy work, or authorize changes to `main.py`.

Proof accepted: NO.

Profitability claim made: NO.

Current intake-ready count: 0.

## Summary

- Acquisition request path: `SAFE_FAST_SOURCE_EVIDENCE_ACQUISITION_REQUEST.md`.
- Gap scanner: `watcher_foundation/source_evidence_gap_scanner.py`.
- Scanner test: `tests/test_source_evidence_gap_scanner.py`.
- Acquisition validator: `watcher_foundation/source_evidence_acquisition_validator.py`.
- Acquisition validator test: `tests/test_source_evidence_acquisition_validator.py`.
- Parked rows covered: 4.
- Acquisition request rows: 9.
- Gap rows covered: 9.
- Acquisition validator requests represented: 9.
- Acquisition validator current no-evidence result: 9 failed requests; parked rows stay parked.
- Current repo data sufficient for any parked row: NO.
- Current repo data can supply requested evidence now: NO.
- Intake-ready count: 0.
- Parked/source_data_insufficient count: 4.
- Replace count: 3.

## Parked Rows Covered

- `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`.
- `SPY-REAL-HISTORICAL-IDEAL-001`.

## Acquisition Request Table

| Evidence name | Candidate ID | Setup type | Symbol | Required source/export type | Required timestamp/session/window | Required fields | Why it is needed | Rule it would resolve | Current repo data can supply | Expected action after acquisition |
|---|---|---|---|---|---|---|---|---|---|---|
| QQQ CFB gap-context completeness fields/rule | `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | Clean Fast Break | QQQ | setup-time QQQ source CSV export or replay-log enrichment | 2026-04 QQQ Clean Fast Break setup window; source CSV line 132; replay log lines 3-4 | `gap_context_status`; `gap_context_as_of`; `gap_context_reviewed_before_signal` | Proves whether the QQQ gap context was known and reviewed before the Clean Fast Break signal. | Clean Fast Break gap context | NO | Rerun the gap scanner and, only if fields are source-backed and regression-covered, consider un-parking this requirement. |
| QQQ CFB stale/spent expiry rule/regressions | `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | Clean Fast Break | QQQ | rule document plus regression fixture rows for QQQ Clean Fast Break | QQQ Clean Fast Break log lines 3-6, including fresh and later spent lifecycle rows | `clean_fast_break_stale_spent_expiry_rule`; `clean_fast_break_expiry_regression_rows` | Defines when the QQQ Clean Fast Break signal remains fresh or becomes stale/spent before proof review. | Clean Fast Break stale/spent expiry | NO | Add rule-gate regression rows, rerun scanners, then reassess parked status without accepting proof. |
| QQQ CFB complete context/caution fields | `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | Clean Fast Break | QQQ | setup-time QQQ source CSV export or replay-log enrichment | QQQ Clean Fast Break setup-time row at source CSV line 132 and replay log line 3 | `option_context_status`; `headline_context_status`; `execution_context_status`; `complete_caution_review_status` | Replaces unconfirmed context with source-backed blocker and caution evidence; primary blocker null is not enough. | Context/caution review | NO | Rerun scanner and intake helper; keep parked unless every context/caution field is source-backed. |
| SPY CFB 003 higher-base/fresh-break expiry rule/regressions | `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | Clean Fast Break | SPY | rule document plus regression fixture rows for SPY Clean Fast Break | 2026-04-15 14:30 SPY signal row and later spent lifecycle row; log lines 5-6 | `clean_fast_break_higher_base_fresh_break_expiry_rule`; `higher_base_fresh_break_expiry_regression_rows` | Defines whether a higher-base/fresh-break Clean Fast Break is still fresh at setup time or already stale/spent. | Clean Fast Break expiry | NO | Add higher-base/fresh-break expiry regressions, rerun scanners, then reassess parked status without proof promotion. |
| SPY CFB 003 complete context/caution fields | `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | Clean Fast Break | SPY | setup-time SPY source CSV export or replay-log enrichment | 2026-04-15 14:30 SPY setup-time row; source CSV line 154; replay log line 5 | `option_context_status`; `headline_context_status`; `execution_context_status`; `complete_caution_review_status` | Completes source-backed blocker/caution context for the fresh-break row before any intake-ready decision. | Context/caution review | NO | Rerun scanner and intake helper; keep parked unless context and caution fields are complete. |
| SPY CFB 002 initial-break expiry rule/regressions | `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | Clean Fast Break | SPY | rule document plus regression fixture rows for SPY Clean Fast Break | 2026-04-13 12:30 SPY signal row and same-session follow-through/spent row; log lines 2-3 | `clean_fast_break_initial_break_expiry_rule`; `initial_break_expiry_regression_rows` | Defines whether an initial-break Clean Fast Break is fresh or stale/spent at setup time. | Clean Fast Break expiry | NO | Add initial-break expiry regressions, rerun scanners, then reassess parked status without proof promotion. |
| SPY CFB 002 complete context/caution fields | `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | Clean Fast Break | SPY | setup-time SPY source CSV export or replay-log enrichment | 2026-04-13 12:30 SPY setup-time row; source CSV line 138; replay log line 2 | `option_context_status`; `headline_context_status`; `execution_context_status`; `complete_caution_review_status` | Completes source-backed blocker/caution context for the initial-break row before any intake-ready decision. | Context/caution review | NO | Rerun scanner and intake helper; keep parked unless context and caution fields are complete. |
| SPY Ideal stale/spent expiry rule/regressions | `SPY-REAL-HISTORICAL-IDEAL-001` | Ideal | SPY | rule document plus regression fixture rows for SPY Ideal | 2026-05-13 11:30 SPY Ideal signal row and later spent lifecycle row; log lines 5-6 | `spy_ideal_stale_spent_expiry_rule`; `spy_ideal_expiry_regression_rows` | Defines whether the same-session SPY Ideal signal is still fresh or has become stale/spent before proof review. | Ideal stale/spent expiry | NO | Add SPY Ideal stale/spent regressions, rerun scanners, then reassess parked status without proof promotion. |
| SPY Ideal gap/headline/option/execution/complete caution fields | `SPY-REAL-HISTORICAL-IDEAL-001` | Ideal | SPY | setup-time SPY source CSV export or replay-log enrichment | 2026-05-13 11:30 SPY Ideal setup-time row; source CSV line 291; replay log line 5 | `gap_context_status`; `headline_context_status`; `option_context_status`; `execution_context_status`; `complete_caution_review_status` | Completes gap, headline, room, option, execution, and caution context for the Ideal setup before any intake-ready decision. | Context/caution review | NO | Rerun scanner and intake helper; keep parked unless every Ideal context/caution field is source-backed. |

## Row Results

- `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`: acquisition requests cover QQQ gap-context completeness, Clean Fast Break stale/spent expiry, and complete context/caution fields; current repo data can supply them: NO.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`: acquisition requests cover higher-base/fresh-break expiry and complete context/caution fields; current repo data can supply them: NO.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`: acquisition requests cover initial-break expiry and complete context/caution fields; current repo data can supply them: NO.
- `SPY-REAL-HISTORICAL-IDEAL-001`: acquisition requests cover SPY Ideal stale/spent expiry and gap/headline/option/execution/complete caution fields; current repo data can supply them: NO.

## Guardrail Result

No parked row can be reactivated from this request alone. Acquisition must add source-backed fields/rules, then the scanner and intake helper must rerun before any status change is considered.

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

## Richer Historical Evidence Inventory Result

- Inventory path: `SAFE_FAST_RICHER_HISTORICAL_EVIDENCE_INVENTORY.md`.
- Local repo files inspected: historical source data, replay reports, SAFE-FAST Day 38/Day 39 docs, active-path/gap/rule docs, and watcher source-row packet helpers.
- Acquisition requests checked: 9.
- Local evidence found that satisfies a request: NO for all 9 requests.
- Local tastytrade/dxLink evidence pull attempted: YES.
- tastytrade helper/config path found: `dxlink_candles.py` and `historical_signal_replay/export_dxlink_source_csv.py`.
- Local tastytrade/dxLink exports checked: QQQ source CSV line 132; SPY source CSV lines 138, 154, and 291; related replay log rows.
- Local tastytrade/dxLink exports provide OHLCV/source/vendor/as-of evidence, but do not provide the required gap, headline, option, execution, complete-caution, or SAFE-FAST rule/regression artifact fields.
- Unsupported request fields are marked `TASTYTRADE_DATA_NOT_AVAILABLE` in the richer export work package and remain blockers.
- Validator result: FAIL for all 9 requests when limited to existing local repo evidence.
- Exact exports/files still needed: the 9 request-shaped source exports or rule/regression files listed in the acquisition table above.
- Intake-ready count: 0.
- Parked/source_data_insufficient count: 4.
- Replace count: 3.
- Proof accepted: NO.
- Profitability claim made: NO.

## Richer Historical Export Package Spec Result

- Export package spec path: `SAFE_FAST_RICHER_HISTORICAL_EXPORT_PACKAGE_SPEC.md`.
- Package-intake helper: `watcher_foundation/source_evidence_package_intake.py`.
- Package-intake test: `tests/test_source_evidence_package_intake.py`.
- Required manifest: `manifest.json`.
- Manifest schema version: `safe-fast-richer-historical-export-package-v1`.
- Accepted evidence file formats: CSV or JSONL.
- Required evidence file groups represented: 9.
- The package spec covers the same 9 acquisition requests listed above.
- With no package supplied, the helper prints the required package checklist to stdout only.
- With a package path supplied later, the helper validates manifest structure, required file entries, accepted formats, and required fields.
- Structural package validation alone does not reactivate parked rows, make rows intake-ready, allow proof review, accept proof, or claim profitability.
- Intake-ready count: 0.
- Parked/source_data_insufficient count: 4.
- Replace count: 3.
- Proof accepted: NO.
- Profitability claim made: NO.
