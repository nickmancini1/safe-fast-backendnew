# SAFE-FAST Richer Historical Export Package Spec

## Scope

This build-only spec defines the exact richer historical evidence package that can be exported later and dropped into the repo for structural intake.

It is not proof review. It does not accept proof, claim profitability, reactivate parked rows, authorize live data, authorize alerts, authorize broker/order/account work, authorize Railway/deploy work, or authorize changes to `main.py`.

Proof accepted: NO.

Profitability claim made: NO.

Current intake-ready count: 0.

## Package Root

A future package directory must contain:

- `manifest.json`.
- One file per required evidence group.
- Evidence files in CSV or JSONL format.

The package-intake helper is:

- `watcher_foundation/source_evidence_package_intake.py`.

With no package path, the helper prints the required package checklist to stdout only:

- `python -B -m watcher_foundation.source_evidence_package_intake`

With a package path supplied later, the helper structurally validates the manifest and required files:

- `python -B -m watcher_foundation.source_evidence_package_intake <package_path>`

## Template Package

The repo now includes a header-only package template for future evidence exports:

- `historical_signal_replay/source_data/richer_export_package_template/`
- `historical_signal_replay/source_data/richer_export_package_template/manifest.example.json`
- 9 `.template.csv` files, one per required evidence group.

The template can be checked with:

- `python -B -m watcher_foundation.source_evidence_package_intake --validate-template`

## Work Package

The repo now includes a fillable header-only work package for future evidence exports:

- `historical_signal_replay/source_data/richer_export_package_work/`
- `historical_signal_replay/source_data/richer_export_package_work/manifest.json`
- 9 required work files using the real package filenames.

The work package manifest must include:

- `package_status`: `needs_real_evidence`
- `proof_accepted`: `false`
- `profitability_claimed`: `false`

Each evidence file entry must include:

- `fill_status`: `unfilled`

Each work file must include `fill_status` plus the evidence group's required headers. The work files are intentionally header-only.

The work package can be checked with:

- `python -B -m watcher_foundation.source_evidence_package_intake --validate-work-package`

Work package validation means only:

- the work package directory exists,
- `manifest.json` exists,
- all 9 work file entries are represented,
- all 9 work files exist,
- required headers are present,
- every group is clearly unfilled.

Work package validation does not count as real evidence. A real future package still needs source-backed resolved evidence values before real package structural validation can pass.

Template validation means only:

- the template directory exists,
- the manifest example exists,
- all 9 template file entries are represented,
- all 9 template files exist,
- each template file contains the required headers.

Template validation does not count as real evidence. A real future package still needs `manifest.json`, accepted file entries, and resolved evidence values before package structural validation can pass.

Template counts:

- Template files represented: 9.
- Template counts as real evidence: NO.
- Work package files represented: 9.
- Work package counts as real evidence: NO.
- Intake-ready count: 0.
- Parked/source_data_insufficient count: 4.
- Replace count: 3.
- Proof accepted: NO.
- Profitability claim made: NO.

## Manifest Schema

Required manifest file:

- `manifest.json`

Required `schema_version`:

- `safe-fast-richer-historical-export-package-v1`

Required top-level manifest fields:

- `schema_version`
- `package_name`
- `created_utc`
- `source_system`
- `evidence_files`
- `proof_accepted`
- `profitability_claimed`

Required manifest guardrail values:

- `proof_accepted`: `false`
- `profitability_claimed`: `false`

Required fields for each `evidence_files` entry:

- `evidence_name`
- `candidate_id`
- `file_name`
- `format`
- `source_export_type`
- `timestamp_session_window`

Accepted `format` values:

- `csv`
- `jsonl`

The manifest must include all 9 required evidence file entries. Missing entries fail structural validation.

## Required File Groups

| Evidence name | Candidate ID | Required file name | Accepted formats | Required timestamp/session/window | Required fields |
|---|---|---|---|---|---|
| QQQ CFB gap-context completeness fields/rule | `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | `qqq_cfb_gap_context_completeness_fields_rule.jsonl` | CSV or JSONL | 2026-04 QQQ Clean Fast Break setup window; source CSV line 132; replay log lines 3-4 | `gap_context_status`; `gap_context_as_of`; `gap_context_reviewed_before_signal` |
| QQQ CFB stale/spent expiry rule/regressions | `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | `qqq_cfb_stale_spent_expiry_rule_regressions.jsonl` | CSV or JSONL | QQQ Clean Fast Break log lines 3-6, including fresh and later spent lifecycle rows | `clean_fast_break_stale_spent_expiry_rule`; `clean_fast_break_expiry_regression_rows` |
| QQQ CFB complete context/caution fields | `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | `qqq_cfb_complete_context_caution_fields.jsonl` | CSV or JSONL | QQQ Clean Fast Break setup-time row at source CSV line 132 and replay log line 3 | `option_context_status`; `headline_context_status`; `execution_context_status`; `complete_caution_review_status` |
| SPY CFB 003 higher-base/fresh-break expiry rule/regressions | `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | `spy_cfb_003_higher_base_fresh_break_expiry_rule_regressions.jsonl` | CSV or JSONL | 2026-04-15 14:30 SPY signal row and later spent lifecycle row; log lines 5-6 | `clean_fast_break_higher_base_fresh_break_expiry_rule`; `higher_base_fresh_break_expiry_regression_rows` |
| SPY CFB 003 complete context/caution fields | `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | `spy_cfb_003_complete_context_caution_fields.jsonl` | CSV or JSONL | 2026-04-15 14:30 SPY setup-time row; source CSV line 154; replay log line 5 | `option_context_status`; `headline_context_status`; `execution_context_status`; `complete_caution_review_status` |
| SPY CFB 002 initial-break expiry rule/regressions | `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | `spy_cfb_002_initial_break_expiry_rule_regressions.jsonl` | CSV or JSONL | 2026-04-13 12:30 SPY signal row and same-session follow-through/spent row; log lines 2-3 | `clean_fast_break_initial_break_expiry_rule`; `initial_break_expiry_regression_rows` |
| SPY CFB 002 complete context/caution fields | `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | `spy_cfb_002_complete_context_caution_fields.jsonl` | CSV or JSONL | 2026-04-13 12:30 SPY setup-time row; source CSV line 138; replay log line 2 | `option_context_status`; `headline_context_status`; `execution_context_status`; `complete_caution_review_status` |
| SPY Ideal stale/spent expiry rule/regressions | `SPY-REAL-HISTORICAL-IDEAL-001` | `spy_ideal_stale_spent_expiry_rule_regressions.jsonl` | CSV or JSONL | 2026-05-13 11:30 SPY Ideal signal row and later spent lifecycle row; log lines 5-6 | `spy_ideal_stale_spent_expiry_rule`; `spy_ideal_expiry_regression_rows` |
| SPY Ideal gap/headline/option/execution/complete caution fields | `SPY-REAL-HISTORICAL-IDEAL-001` | `spy_ideal_gap_headline_option_execution_complete_caution_fields.jsonl` | CSV or JSONL | 2026-05-13 11:30 SPY Ideal setup-time row; source CSV line 291; replay log line 5 | `gap_context_status`; `headline_context_status`; `option_context_status`; `execution_context_status`; `complete_caution_review_status` |

## File Content Rules

CSV files:

- The first row must contain headers.
- The first data row must contain all required fields for that evidence group.

JSONL files:

- The first non-empty line must be a JSON object.
- That object must contain all required fields for that evidence group.

Field values are unresolved blockers if they are empty, `None`, `missing`, `unclear`, or `incomplete` in any casing.

## Structural Validation Result

Passing package structural validation means only:

- the manifest exists,
- the manifest schema and guardrails are valid,
- all 9 required evidence file entries are present,
- every required file can be read or represented,
- every required field is present with a resolved value.

Passing package structural validation does not:

- reactivate any parked row,
- make any row intake-ready,
- allow proof review,
- accept proof,
- claim profitability.

## Current Counts

- Acquisition requests represented: 9.
- Intake-ready count: 0.
- Parked/source_data_insufficient count: 4.
- Replace count: 3.
- Proof accepted: NO.
- Profitability claim made: NO.
