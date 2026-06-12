# SAFE-FAST Richer Historical Evidence Inventory

## Scope

This build-only inventory checks whether the local repo already contains richer historical evidence packages that satisfy any of the 9 source-evidence acquisition requests.

It is not proof review. It does not accept proof, claim profitability, reactivate parked rows, authorize live data, authorize alerts, authorize broker/order/account work, authorize Railway/deploy work, or authorize changes to `main.py`.

Proof accepted: NO.

Profitability claim made: NO.

## Files Inspected

- `historical_signal_replay/source_data`.
- `historical_signal_replay/reports`.
- `SAFE_FAST_DAY38_*.md`.
- `SAFE_FAST_DAY39_COMBINED_HANDOFF_AND_FAST_CANDIDATE_FUNNEL.md`.
- `SAFE_FAST_ACTIVE_PATH_EVIDENCE_REQUIREMENTS.md`.
- `SAFE_FAST_RULE_FAMILY_DECISION_TABLE.md`.
- `SAFE_FAST_SOURCE_EVIDENCE_GAP_MAP.md`.
- `watcher_foundation/candidate_freshness_blocker_rule_gate.py`.
- `watcher_foundation/candidate_freshness_blocker_state.py`.
- `watcher_foundation/candidate_source_pool_intake.py`.
- `watcher_foundation/replacement_source_row_packet.py`.
- `watcher_foundation/replacement_source_row_packet_builder.py`.
- `watcher_foundation/replacement_source_row_packet_template.py`.
- `watcher_foundation/replacement_source_row_window_extractor.py`.
- `watcher_foundation/source_evidence_gap_scanner.py`.

## Inventory Summary

- Acquisition requests checked: 9.
- Local evidence packages found that satisfy a request: 0.
- Validator-passed local requests: 0.
- Failed requests: 9.
- Intake-ready count: 0.
- Parked/source_data_insufficient count: 4.
- Replace count: 3.
- Proof accepted: NO.
- Profitability claim made: NO.

## Request Results

| Evidence name | Candidate ID | Local evidence found | Validator result | Exact export/file still needed |
|---|---|---|---|---|
| QQQ CFB gap-context completeness fields/rule | `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | NO | FAIL | setup-time QQQ source CSV export or replay-log enrichment for 2026-04 QQQ Clean Fast Break setup window, source CSV line 132, replay log lines 3-4, containing `gap_context_status`, `gap_context_as_of`, and `gap_context_reviewed_before_signal`. |
| QQQ CFB stale/spent expiry rule/regressions | `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | NO | FAIL | rule document plus regression fixture rows for QQQ Clean Fast Break log lines 3-6, containing `clean_fast_break_stale_spent_expiry_rule` and `clean_fast_break_expiry_regression_rows`. |
| QQQ CFB complete context/caution fields | `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | NO | FAIL | setup-time QQQ source CSV export or replay-log enrichment for source CSV line 132 and replay log line 3, containing `option_context_status`, `headline_context_status`, `execution_context_status`, and `complete_caution_review_status`. |
| SPY CFB 003 higher-base/fresh-break expiry rule/regressions | `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | NO | FAIL | rule document plus regression fixture rows for the 2026-04-15 14:30 SPY signal row and later spent lifecycle row, log lines 5-6, containing `clean_fast_break_higher_base_fresh_break_expiry_rule` and `higher_base_fresh_break_expiry_regression_rows`. |
| SPY CFB 003 complete context/caution fields | `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | NO | FAIL | setup-time SPY source CSV export or replay-log enrichment for source CSV line 154 and replay log line 5, containing `option_context_status`, `headline_context_status`, `execution_context_status`, and `complete_caution_review_status`. |
| SPY CFB 002 initial-break expiry rule/regressions | `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | NO | FAIL | rule document plus regression fixture rows for the 2026-04-13 12:30 SPY signal row and same-session follow-through/spent row, log lines 2-3, containing `clean_fast_break_initial_break_expiry_rule` and `initial_break_expiry_regression_rows`. |
| SPY CFB 002 complete context/caution fields | `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | NO | FAIL | setup-time SPY source CSV export or replay-log enrichment for source CSV line 138 and replay log line 2, containing `option_context_status`, `headline_context_status`, `execution_context_status`, and `complete_caution_review_status`. |
| SPY Ideal stale/spent expiry rule/regressions | `SPY-REAL-HISTORICAL-IDEAL-001` | NO | FAIL | rule document plus regression fixture rows for the 2026-05-13 11:30 SPY Ideal signal row and later spent lifecycle row, log lines 5-6, containing `spy_ideal_stale_spent_expiry_rule` and `spy_ideal_expiry_regression_rows`. |
| SPY Ideal gap/headline/option/execution/complete caution fields | `SPY-REAL-HISTORICAL-IDEAL-001` | NO | FAIL | setup-time SPY source CSV export or replay-log enrichment for source CSV line 291 and replay log line 5, containing `gap_context_status`, `headline_context_status`, `option_context_status`, `execution_context_status`, and `complete_caution_review_status`. |

## Local Evidence Finding

The local repo contains source CSV rows, replay lifecycle logs, Day 38/Day 39 review docs, and watcher helpers that identify the missing evidence. Those materials are useful audit context, but they do not supply any full acquisition-request evidence package.

The source CSV rows contain OHLCV plus unconfirmed 24H, macro, IV, and event context fields. The replay logs contain lifecycle labels, trigger/invalidation values, unconfirmed room/wall-thesis fields, and unconfirmed caution lists. The docs and helpers preserve the same conclusion: the requested gap-context fields, setup-specific expiry rules/regression rows, option/headline/execution context fields, and complete caution-review fields are still absent.

## Guardrail Result

No parked row is reactivated. No request enters proof review. The richer historical evidence inventory confirms the current repo still needs new source-backed exports or rule/regression files before any parked-row reassessment.

Proof accepted: NO.

Profitability claim made: NO.
