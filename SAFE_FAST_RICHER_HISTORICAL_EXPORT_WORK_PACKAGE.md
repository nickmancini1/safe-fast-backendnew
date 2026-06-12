# SAFE-FAST Richer Historical Export Work Package

## Scope

This build-only work package creates a fillable local package directory for the 9 richer historical evidence exports.

It is not proof review. It does not accept proof, claim profitability, reactivate parked rows, authorize live data, authorize alerts, authorize broker/order/account work, authorize Railway/deploy work, or authorize changes to `main.py`.

Proof accepted: NO.

Profitability claim made: NO.

## Work Package Folder

- `historical_signal_replay/source_data/richer_export_package_work/`
- `manifest.json`
- 9 working CSV-format files using the required real package filenames.

The work files now include one repo-known prefill row each with `fill_status` set to `partial_missing_required_evidence`. Known candidate metadata, setup time, trigger, invalidation, source file, source line/section, no-hindsight boundary, outcome-window input, rule family, and request ID are filled where local docs/source rows/logs support them.

Missing required evidence fields remain explicitly marked `MISSING_REQUIRED_EVIDENCE`. These rows validate as work-package structure only and do not count as complete evidence.

## Manifest

The work package manifest uses:

- `schema_version`: `safe-fast-richer-historical-export-package-v1`
- `package_status`: `needs_real_evidence`
- `proof_accepted`: `false`
- `profitability_claimed`: `false`

Each evidence file entry includes `fill_status: "unfilled"`.

## Work Files

| Evidence group | Work file |
|---|---|
| QQQ CFB gap-context completeness | `qqq_cfb_gap_context_completeness_fields_rule.jsonl` |
| QQQ CFB stale/spent expiry rule/regressions | `qqq_cfb_stale_spent_expiry_rule_regressions.jsonl` |
| QQQ CFB complete context/caution fields | `qqq_cfb_complete_context_caution_fields.jsonl` |
| SPY CFB 003 higher-base/fresh-break expiry rule/regressions | `spy_cfb_003_higher_base_fresh_break_expiry_rule_regressions.jsonl` |
| SPY CFB 003 complete context/caution fields | `spy_cfb_003_complete_context_caution_fields.jsonl` |
| SPY CFB 002 initial-break expiry rule/regressions | `spy_cfb_002_initial_break_expiry_rule_regressions.jsonl` |
| SPY CFB 002 complete context/caution fields | `spy_cfb_002_complete_context_caution_fields.jsonl` |
| SPY Ideal stale/spent expiry rule/regressions | `spy_ideal_stale_spent_expiry_rule_regressions.jsonl` |
| SPY Ideal gap/headline/option/execution/complete caution fields | `spy_ideal_gap_headline_option_execution_complete_caution_fields.jsonl` |

## Validation

Validate the work package structure:

- `python -B -m watcher_foundation.source_evidence_package_intake --validate-work-package`

Work package validation checks:

- the work folder exists,
- `manifest.json` exists,
- `package_status` is `needs_real_evidence`,
- all 9 work file entries are represented,
- all 9 work files exist,
- each work file contains `fill_status` plus the required evidence headers,
- every manifest evidence entry has `fill_status: "unfilled"`.

Work package validation does not:

- count as real evidence,
- reactivate parked rows,
- make any row intake-ready,
- allow proof review,
- accept proof,
- claim profitability.

Validate work package content:

- `python -B -m watcher_foundation.source_evidence_work_package_content_validator`

Content validation checks whether each of the 9 work files contains at least one real evidence row. It checks required headers, non-empty required fields, non-placeholder `fill_status`, matching `candidate_id`, matching `rule_family`, and resolved `source_time`, `source_session`, and `source_window` fields. It reports partial rows separately from header-only rows.

The current work package has partial prefilled rows, so content validation currently reports:

- content passed requests: 0.
- content failed requests: 9.
- partial rows: 9.
- header-only rows: 0.

Content validation does not count as proof review, reactivate parked rows, make rows intake-ready, accept proof, or claim profitability.

Bridge content validation into parked-candidate reconsideration decisions:

- `python -B -m watcher_foundation.source_evidence_package_to_intake_bridge`

The bridge maps all 9 evidence requests to 4 parked candidates. A candidate becomes reconsideration-eligible only when every required request for that candidate passes content validation. Reconsideration eligibility does not make the candidate intake-ready, allow proof review, accept proof, or claim profitability.

## Current Counts

- Work package files represented: 9.
- Work package validates structurally: YES.
- Work package counts as real evidence: NO.
- Work package content passed requests: 0.
- Work package content failed requests: 9.
- Partial rows: 9.
- Header-only rows: 0.
- Evidence-package-to-intake bridge requests mapped: 9.
- Evidence-package-to-intake bridge parked candidates mapped: 4.
- Reconsideration-eligible candidates: 0.
- Intake-ready count: 0.
- Parked/source_data_insufficient count: 4.
- Replace count: 3.
- Proof accepted: NO.
- Profitability claim made: NO.
