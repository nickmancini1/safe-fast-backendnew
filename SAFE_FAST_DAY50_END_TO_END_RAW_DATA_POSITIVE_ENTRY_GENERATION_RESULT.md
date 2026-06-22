# SAFE-FAST Day 50 End-to-End Raw-Data Positive-Entry Generation Result

## Baseline

- Branch: `main`.
- Current task file executed: `SAFE_FAST_DAY50_POSITIVE_ENTRY_CLOSED_REQUIREMENT_SCORECARD_RECONCILIATION_CODEX_TASK.md` as superseded by the user instruction to run end-to-end raw-data positive-entry generation.
- Required startup files read first: `SAFE_FAST_BUILD_STATE.md`, data-source registry, proof pipeline, Day 50 active-path requirement regression result, Day 50 evidence-backed positive-entry batch result, Day 48 positive-trade funnel result, dashboard, rule index, local calculators, manifests, raw data, runners, validators, and tests.
- Existing measured batch remains the regression control: `13` setup-qualified, `9` trade candidates, `5` selected contracts, `1` eligible entry, `1` recorded entry, `1` valid captured trade, `4` true no-trades, `0` missed valid trades, and `0` invalid trades allowed.
- This task performed actual raw-data inventory and deterministic generation attempt from local chronological underlying evidence.

## Fixed

- Added focused generator: `historical_signal_replay/day50_end_to_end_raw_data_positive_entry_generation.py`.
- Added focused validator: `watcher_foundation/day50_end_to_end_raw_data_positive_entry_generation_validator.py`.
- Added focused tests: `tests/test_day50_end_to_end_raw_data_positive_entry_generation.py`.
- Created candidate manifest: `historical_signal_replay/fixtures/day50_raw_data_positive_entry_candidate_manifest.json`.
- Created machine-readable result: `historical_signal_replay/results/day50_end_to_end_raw_data_positive_entry_generation.json`.

## Raw-Data Generation Result

- Raw opportunities inspected: `33`.
- New generated candidates: `0`.
- New setup-qualified candidates: `0`.
- New trade candidates: `0`.
- New selected contracts: `0`.
- New price-accepted candidates: `0`.
- New eligible entries: `0`.
- New recorded entries: `0`.
- New exits evaluated: `0`.
- New valid trades captured: `0`.
- New true no-trades: `0`.
- New exact-data-required cases: `0`.
- New missed valid trades: `0`.
- New invalid trades allowed: `0`.
- New unresolved cases: `0`.
- New winners: `0`.
- New losers: `0`.
- Deterministic comparison: `PASS`; the full generated-candidate funnel was run twice with identical output.

## Per-Family Totals

| Family | Raw opportunities inspected | Generated | Setup-qualified | Trade candidates | Selected contracts | Eligible entries | Recorded entries |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Ideal | 11 | 0 | 0 | 0 | 0 | 0 | 0 |
| Clean Fast Break | 11 | 0 | 0 | 0 | 0 | 0 | 0 |
| Continuation | 11 | 0 | 0 | 0 | 0 | 0 | 0 |
| Combined | 33 | 0 | 0 | 0 | 0 | 0 | 0 |

## Exact Blocker

Every inspected raw-data opportunity was rejected before candidate creation because local underlying evidence is one-hour OHLCV only for the relevant windows. The registry and prior closeout state require exact setup-time row, trigger, invalidation, freshness/final-signal state, blocker/caution state, session-boundary behavior, and no-hindsight boundary from accepted SAFE-FAST replay/calculators. One-hour bars may support context, but they do not establish exact intraday setup triggers or accepted active-path fields.

## Exact Grouped Data Request

- Request ID: `DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M`.
- Request type: underlying setup-time data only.
- Symbol: `SPY`.
- Window: `2026-03-16T09:30:00-04:00` through `2026-03-16T16:00:00-04:00`.
- Dataset/schema/stype: `DBEQ.BASIC / ohlcv-1m / raw_symbol`.
- Required resolution: `1 minute RTH bars`.
- Field consumers: setup-time row, trigger, invalidation, freshness/final-signal state, prior completed structure, blocker/caution review, session-boundary behavior, and no-hindsight boundary.
- Setup-family decisions resolved: Ideal, Clean Fast Break, and Continuation.
- Checked cost: `0.001370869577`.
- Credential used for cost check: `YES`.
- Download created: `NO`.
- Actual billed cost: `NOT_AVAILABLE`.
- Option request created: `NO`.
- Exit-path request created: `NO`.

## Existing Regression Result

- Day 48 positive-trade funnel rerun twice through the generator control path: deterministic; each preserved the existing combined control totals.
- Day 50 evidence-backed batch preserved: `13` setup-qualified, `9` trade candidates, `5` selected contracts, `1` eligible entry, `1` recorded entry.
- New-candidate results are separate from existing regression controls.

## Guardrails

No `main.py`, trading logic, Railway/deploy files, broker/account/order code, credentials, `.env`, frozen thresholds, production/live backend, Schwab authentication, data download, option request, exit-path request, proof, profitability claim, readiness claim, promotion, paper eligibility, or live eligibility was changed or created.

## Next

Exact next task: `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_UNDERLYING_SETUP_TIME_COSTED_REQUEST_CODEX_TASK.md`.

Reason: acquire or otherwise supply the exact cost-checked SPY one-minute underlying setup-time window, then rerun this raw-data positive-entry generator without changing frozen trading rules.

## Tests

- `python -B -m unittest discover -s tests -p "test_day50_end_to_end_raw_data_positive_entry_generation.py"`: PASS, `9` tests.
- `python -B -m historical_signal_replay.day50_end_to_end_raw_data_positive_entry_generation`: PASS, wrote `33` raw opportunities inspected, `0` setup-qualified, `0` trade candidates, `0` selected contracts, `0` eligible entries, `0` recorded entries, checked cost `0.001370869577`.
- `python -B -m watcher_foundation.day50_end_to_end_raw_data_positive_entry_generation_validator`: PASS, `0` problems.
