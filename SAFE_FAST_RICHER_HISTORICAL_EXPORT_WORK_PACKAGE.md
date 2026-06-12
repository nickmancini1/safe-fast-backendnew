# SAFE-FAST Richer Historical Export Work Package

## Scope

This build-only work package creates a fillable local package directory for the 9 richer historical evidence exports.

It is not proof review. It does not accept proof, claim profitability, reactivate parked rows, authorize live data, authorize alerts, authorize broker/order/account work, authorize Railway/deploy work, or authorize changes to `main.py`.

Proof accepted: NO.

Profitability claim made: NO.

## Work Package Folder

- `historical_signal_replay/source_data/richer_export_package_work/`
- `manifest.json`
- 9 header-only working CSV-format files using the required real package filenames.

The work files are intentionally header-only and include `fill_status` as the first header. They validate as work-package structure only and do not count as real evidence.

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

## Current Counts

- Work package files represented: 9.
- Work package validates structurally: YES.
- Work package counts as real evidence: NO.
- Intake-ready count: 0.
- Parked/source_data_insufficient count: 4.
- Replace count: 3.
- Proof accepted: NO.
- Profitability claim made: NO.
