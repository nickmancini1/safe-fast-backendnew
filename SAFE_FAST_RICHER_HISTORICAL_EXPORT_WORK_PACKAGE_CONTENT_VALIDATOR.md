# SAFE-FAST Richer Historical Export Work Package Content Validator

## Scope

This build-only validator checks whether the richer historical export work package contains real filled evidence rows.

It is not proof review. It does not accept proof, claim profitability, reactivate parked rows, authorize live data, authorize alerts, authorize broker/order/account work, authorize Railway/deploy work, or authorize changes to `main.py`.

Proof accepted: NO.

Profitability claim made: NO.

## Validator

- Validator path: `watcher_foundation/source_evidence_work_package_content_validator.py`.
- Test path: `tests/test_source_evidence_work_package_content_validator.py`.
- Work package folder: `historical_signal_replay/source_data/richer_export_package_work/`.
- Evidence requests checked: 9.

Run:

- `python -B -m watcher_foundation.source_evidence_work_package_content_validator`

The CLI prints the content validation table to stdout only.

Each content result now exposes the mapped `rule_family` value used by the
evidence-package-to-intake bridge.

## Content Rules

For each of the 9 work files, content validation checks:

- file exists,
- required headers exist,
- at least one real evidence row exists,
- required evidence fields are present and non-empty,
- `fill_status` is not `placeholder`, `needs_real_evidence`, or `unfilled`,
- row `candidate_id` matches the request,
- row `rule_family` matches the request rule family,
- `source_time`, `source_session`, and `source_window` are present with resolved values.

Unresolved values remain blockers when they are empty, `None`, `missing`, `unclear`, or `incomplete` in any casing.

## Current Result

The current work package is intentionally header-only. It validates structurally but does not contain real evidence rows.

- Work files checked: 9.
- Current work package content passed requests: 0.
- Current work package content failed requests: 9.
- Intake-ready count: 0.
- Parked/source_data_insufficient count: 4.
- Replace count: 3.
- Proof accepted: NO.
- Profitability claim made: NO.

## Guardrail Result

Passing content validation for a work file would only show that the file contains a request-shaped row. It would not reactivate a parked row, make a row intake-ready, permit proof review, accept proof, or claim profitability.

Proof accepted: NO.

Profitability claim made: NO.

## Bridge Use

The content validator is the input for `watcher_foundation/source_evidence_package_to_intake_bridge.py`.

The bridge aggregates the 9 request results by parked candidate and allows reconsideration eligibility only when every required request for that candidate passes.

Current bridge result from the header-only work package:

- Requests mapped: 9.
- Parked candidates mapped: 4.
- Passed requests: 0.
- Failed requests: 9.
- Reconsideration-eligible candidates: 0.
- Intake-ready count: 0.
- Parked/source_data_insufficient count: 4.
- Replace count: 3.
- Proof accepted: NO.
- Profitability claim made: NO.
