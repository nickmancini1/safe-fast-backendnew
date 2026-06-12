# SAFE-FAST Richer Historical Export Package Template

## Scope

This build-only template gives future historical evidence exports an exact folder shape to fill in before running package intake.

It is not proof review. It does not accept proof, claim profitability, reactivate parked rows, authorize live data, authorize alerts, authorize broker/order/account work, authorize Railway/deploy work, or authorize changes to `main.py`.

Proof accepted: NO.

Profitability claim made: NO.

## Template Folder

- `historical_signal_replay/source_data/richer_export_package_template/`
- `manifest.example.json`
- 9 header-only CSV template files.

The template files are intentionally header-only. They validate as template structure only and do not count as real evidence.

## Template Files

| Evidence group | Template file |
|---|---|
| QQQ CFB gap-context completeness | `qqq_cfb_gap_context_completeness_fields_rule.template.csv` |
| QQQ CFB stale/spent expiry rule/regressions | `qqq_cfb_stale_spent_expiry_rule_regressions.template.csv` |
| QQQ CFB complete context/caution fields | `qqq_cfb_complete_context_caution_fields.template.csv` |
| SPY CFB 003 higher-base/fresh-break expiry rule/regressions | `spy_cfb_003_higher_base_fresh_break_expiry_rule_regressions.template.csv` |
| SPY CFB 003 complete context/caution fields | `spy_cfb_003_complete_context_caution_fields.template.csv` |
| SPY CFB 002 initial-break expiry rule/regressions | `spy_cfb_002_initial_break_expiry_rule_regressions.template.csv` |
| SPY CFB 002 complete context/caution fields | `spy_cfb_002_complete_context_caution_fields.template.csv` |
| SPY Ideal stale/spent expiry rule/regressions | `spy_ideal_stale_spent_expiry_rule_regressions.template.csv` |
| SPY Ideal gap/headline/option/execution/complete caution fields | `spy_ideal_gap_headline_option_execution_complete_caution_fields.template.csv` |

## Validation

Print the package and template checklist:

- `python -B -m watcher_foundation.source_evidence_package_intake`

Validate the template structure:

- `python -B -m watcher_foundation.source_evidence_package_intake --validate-template`

Validate a future filled package:

- `python -B -m watcher_foundation.source_evidence_package_intake <package_path>`

Template validation checks the folder, manifest example, all 9 template files, and required headers.

Template validation does not:

- reactivate parked rows,
- make any row intake-ready,
- allow proof review,
- accept proof,
- claim profitability.

## Current Counts

- Template files represented: 9.
- Intake-ready count: 0.
- Parked/source_data_insufficient count: 4.
- Replace count: 3.
- Proof accepted: NO.
- Profitability claim made: NO.
