# SAFE-FAST Richer Historical Export Work Package Content Validator

## Day 41 Raw Tastytrade Correction

tastytrade should be treated as a raw-data source, not a SAFE-FAST label source.

The content validator should only pass rows when the work package contains real evidence sufficient for the required request fields. Raw tastytrade fields may support calculated SAFE-FAST labels, but tastytrade is not expected to directly provide labels such as fresh/stale, expired/valid, context clean/blocked, gap context complete, CFB expiry, Ideal stale/spent, option context usable, execution context usable, or caution clean.

The next data-only capability test should determine whether tastytrade can provide raw underlying candles, option chain snapshot/history, bid/ask quotes, spread, quote timestamps, volume/open interest if available, expiration/strike metadata, underlying price around signal, and data through signal time only. Those raw fields must then be mapped to the 9 evidence requests before any content row can pass.

For the first target, `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` QQQ CFB gap context, SAFE-FAST must calculate `gap_context_status`, `gap_context_as_of`, `gap_context_reviewed_before_signal`, `option_context_status`, `execution_context_status`, and `caution_context_status` from raw evidence if available.

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

Each content result also reports whether the row is `header_only`,
`partial_missing_required_evidence`, `complete`, or another failed row shape.

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

Unresolved values remain blockers when they are empty, `None`, `missing`, `unclear`, `incomplete`, `MISSING_REQUIRED_EVIDENCE`, or `TASTYTRADE_DATA_NOT_AVAILABLE` in any casing.

Annotated missing-evidence values such as `MISSING_REQUIRED_EVIDENCE: gap_context_status absent from source` also remain blockers. This allows a work row to name the exact missing field while preventing annotated blockers from being treated as completed evidence.

Annotated tastytrade-unavailable values such as `TASTYTRADE_DATA_NOT_AVAILABLE: option_context_status not present in local dxLink source CSV` also remain blockers. This prevents local tastytrade/dxLink unsupported fields from being treated as completed evidence.

## Current Result

The current work package is intentionally partial. It validates structurally and contains one repo-known prefill row per work file. A local tastytrade/dxLink evidence pull attempt checked the existing QQQ and SPY source CSV exports and replay logs, but every row still leaves required acquisition evidence unresolved as `TASTYTRADE_DATA_NOT_AVAILABLE` where local dxLink OHLCV exports cannot provide the requested field or rule artifact.

- Work files checked: 9.
- Current work package content passed requests: 0.
- Current work package content failed requests: 9.
- Partial rows: 9.
- Header-only rows: 0.
- QQQ CFB gap-context row now names the exact fields not available from local tastytrade/dxLink data: `gap_context_status`, `gap_context_as_of`, and `gap_context_reviewed_before_signal`.
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

Current bridge result from the partial work package:

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
