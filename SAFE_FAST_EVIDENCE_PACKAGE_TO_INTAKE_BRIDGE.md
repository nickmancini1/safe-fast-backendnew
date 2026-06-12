# SAFE-FAST Evidence Package to Intake Bridge

## Day 41 Raw Tastytrade Correction

tastytrade is a raw-data source. SAFE-FAST must calculate its own trade-plan labels from raw market and option data.

The bridge must not treat a tastytrade capability check as proof by itself. Raw tastytrade evidence can only affect reconsideration eligibility after the work-package content validator passes every required request for a parked candidate.

The next task should test tastytrade raw data availability for underlying candles, option chain snapshot/history, bid/ask quotes, spread, quote timestamps, volume/open interest if available, expiration/strike metadata, underlying price around signal, and data through signal time only. The raw fields must then be mapped to the 9 evidence requests.

First target: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`, QQQ CFB gap context. Even if all QQQ CFB requests pass later, the bridge may only mark the candidate reconsideration-eligible. Intake-ready still requires later SAFE-FAST gates. Proof remains NO.

## Scope

This build-only bridge maps richer historical export work-package content validation into parked-candidate intake decisions.

It is not proof review. It does not accept proof, claim profitability, reactivate parked rows, authorize live data, authorize alerts, authorize broker/order/account work, authorize Railway/deploy work, or authorize changes to `main.py`.

Proof accepted: NO.

Profitability claim made: NO.

## Bridge

- Bridge path: `watcher_foundation/source_evidence_package_to_intake_bridge.py`.
- Test path: `tests/test_source_evidence_package_to_intake_bridge.py`.
- Input validator: `watcher_foundation/source_evidence_work_package_content_validator.py`.
- Work package folder: `historical_signal_replay/source_data/richer_export_package_work/`.
- Evidence requests mapped: 9.
- Parked candidates mapped: 4.

Run:

- `python -B -m watcher_foundation.source_evidence_package_to_intake_bridge`

The CLI prints the bridge table to stdout only.

## Candidate Requirements

| Candidate ID | Required evidence requests |
|---|---|
| `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | QQQ CFB gap context; QQQ CFB expiry; QQQ CFB context/caution |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | SPY CFB 003 expiry; SPY CFB 003 context/caution |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | SPY CFB 002 expiry; SPY CFB 002 context/caution |
| `SPY-REAL-HISTORICAL-IDEAL-001` | SPY Ideal expiry; SPY Ideal context/caution |

## Decision Rule

A parked candidate is reconsideration-eligible only if all required evidence requests for that candidate pass content validation.

If any required request fails, the candidate stays `parked/source_data_insufficient`.

Reconsideration eligibility does not make a row intake-ready, allow proof review, accept proof, or claim profitability. It only identifies which parked candidates have enough request-shaped package content to be reassessed by the later scanner/intake path.

## Current Result

The current work package is intentionally partial: all 9 files have repo-known prefill rows, and all 9 still fail content validation because required acquisition evidence remains unresolved. After the local tastytrade/dxLink evidence pull attempt, unsupported request fields are marked `TASTYTRADE_DATA_NOT_AVAILABLE` and remain blockers.

The QQQ Clean Fast Break gap-context row has been rechecked against source CSV line 132 and replay log lines 3-4. Its three required gap-context fields are now named as annotated `MISSING_REQUIRED_EVIDENCE` blockers, so the request still fails and the QQQ candidate stays parked.

- Passed requests: 0.
- Failed requests: 9.
- Reconsideration-eligible candidates: 0.
- Intake-ready count: 0.
- Parked/source_data_insufficient count: 4.
- Replace count: 3.
- Proof accepted: NO.
- Profitability claim made: NO.

## Guardrail Result

The bridge does not turn content validation into proof. It only prevents future evidence rows from being interpreted candidate-by-candidate unless every required request for that candidate passes.

Proof accepted: NO.

Profitability claim made: NO.
