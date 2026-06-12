# SAFE-FAST Source-Evidence Acquisition Validator

## Scope

This build-only validator checks future acquired source-evidence packages against the 9 source-evidence acquisition requests.

It is not proof review. It does not accept proof, claim profitability, reactivate parked rows, authorize live data, authorize alerts, authorize broker/order/account work, authorize Railway/deploy work, or authorize changes to `main.py`.

Proof accepted: NO.

Profitability claim made: NO.

Current intake-ready count: 0.

## Summary

- Validator: `watcher_foundation/source_evidence_acquisition_validator.py`.
- Validator test: `tests/test_source_evidence_acquisition_validator.py`.
- Source requests loaded from: `watcher_foundation/source_evidence_gap_scanner.py`.
- Acquisition request source doc: `SAFE_FAST_SOURCE_EVIDENCE_ACQUISITION_REQUEST.md`.
- Acquisition requests represented: 9.
- Parked rows covered: 4.
- Current validator result with no new evidence: all acquisition requests fail validation as blockers; parked rows stay parked.
- Intake-ready count: 0.
- Parked/source_data_insufficient count: 4.
- Replace count: 3.

## Covered Requests

- QQQ CFB gap-context completeness.
- QQQ CFB stale/spent expiry rule/regressions.
- QQQ CFB complete context/caution fields.
- SPY CFB 003 higher-base/fresh-break expiry rule/regressions.
- SPY CFB 003 complete context/caution fields.
- SPY CFB 002 initial-break expiry rule/regressions.
- SPY CFB 002 complete context/caution fields.
- SPY Ideal stale/spent expiry rule/regressions.
- SPY Ideal gap/headline/option/execution/complete caution fields.

## Validation Rules

For each acquisition request, the validator defines:

- evidence name.
- affected candidate ID.
- setup type.
- symbol.
- accepted source/export type.
- required timestamp/session/window.
- required fields.
- rule it would resolve.
- current parked status.

A supplied in-memory evidence record passes only when it matches the request evidence name, candidate ID, rule resolved, accepted source/export type, and contains every required field with a resolved value.

Missing required fields are blockers.

Unresolved required values are blockers when they are empty, `None`, `missing`, `unclear`, or `incomplete`.

Passing validation for one request does not reactivate a parked row, permit proof review, or claim profitability. It only means that the supplied record satisfies that request-shaped validation check.

## Current No-Evidence Result

- Passed requests: 0.
- Failed requests: 9.
- Blocker fields: 28.
- Validator result: all acquisition requests fail validation as blockers; parked rows stay parked.
- Proof allowed rows: 0.
- Proof accepted: NO.
- Profitability claim made: NO.

## Guardrail Result

No parked row can be reactivated without a supplied source-backed evidence package that passes the relevant request validations and a later explicit scanner/intake reassessment.

Proof accepted: NO.

Profitability claim made: NO.

## Richer Historical Evidence Inventory Result

- Inventory path: `SAFE_FAST_RICHER_HISTORICAL_EVIDENCE_INVENTORY.md`.
- Local repo files inspected: `historical_signal_replay/source_data`, `historical_signal_replay/reports`, SAFE-FAST Day 38/Day 39 docs, active-path/gap/rule docs, and watcher helpers that produce or validate source-row packets.
- Acquisition requests checked: 9.
- Local evidence packages found that satisfy a request: 0.
- Validator-passed local requests: 0.
- Failed requests: 9.
- Intake-ready count: 0.
- Parked/source_data_insufficient count: 4.
- Replace count: 3.
- Result: the repo contains useful source CSV rows, replay lifecycle logs, review docs, and helper definitions, but no full gap-context, setup-specific expiry-rule/regression, or complete context/caution evidence package required by the 9 acquisition requests.

Proof accepted: NO.

Profitability claim made: NO.
