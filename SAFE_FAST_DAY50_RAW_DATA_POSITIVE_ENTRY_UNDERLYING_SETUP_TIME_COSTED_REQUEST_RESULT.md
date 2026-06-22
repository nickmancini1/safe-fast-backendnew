# SAFE-FAST Day 50 Raw-Data Positive-Entry Underlying Setup-Time Costed Request Result

## Scope

- Task executed: `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_UNDERLYING_SETUP_TIME_COSTED_REQUEST_CODEX_TASK.md`.
- Exact request ID: `DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M`.
- Symbol: `SPY`.
- Window: `2026-03-16T09:30:00-04:00` through `2026-03-16T16:00:00-04:00`.
- Dataset/schema/stype: `DBEQ.BASIC / ohlcv-1m / raw_symbol`.
- Approved checked cost: `0.001370869577`.

## Evidence Acquisition

- Exact underlying setup-time evidence acquired or supplied: `YES`.
- Download manifest: `historical_signal_replay/source_data/external_underlying_data_drop/SAFE_FAST_DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M_DOWNLOAD_MANIFEST.json`.
- CSV path: `historical_signal_replay/source_data/external_underlying_data_drop/SAFE_FAST_DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M.csv`.
- DBN path: `historical_signal_replay/source_data/external_underlying_data_drop/SAFE_FAST_DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M.dbn.zst`.
- Downloaded row count: `751`.
- CSV SHA256: `094ded7e41756704bd4654b63e4adc05fcd5ebe372cf230dcda7880725b41ddd`.
- DBN SHA256: `b8b046051890ea334f61cbc5d77bb84fd25fcbf6b43d7422e37444b92224ff4d`.
- Validation problems: `0`.
- Fresh checked cost: `0.001370869577`.
- Actual billed cost: `NOT_AVAILABLE`.
- Option data requested: `NO`.
- Exit-path data requested: `NO`.

## Generator Rerun

- Machine-readable acquisition result: `historical_signal_replay/results/day50_raw_data_positive_entry_underlying_setup_time_costed_request.json`.
- Machine-readable generator result: `historical_signal_replay/results/day50_end_to_end_raw_data_positive_entry_generation.json`.
- Candidate manifest: `historical_signal_replay/fixtures/day50_raw_data_positive_entry_candidate_manifest.json`.
- Raw opportunities inspected: `36`.
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

## Exact Blockers

- `33` previously inspected local raw opportunities remain rejected as `underlying_resolution_insufficient_for_exact_setup_trigger`; their exact failed fields remain `setup_time_row`, `trigger`, `invalidation`, `freshness_final_signal_state`, `blocker_caution_review`, `session_boundary_behavior`, and `no_hindsight_boundary`.
- `3` new SPY one-minute opportunities were inspected from the acquired Day 50 evidence, one each for Ideal, Clean Fast Break, and Continuation.
- The `3` new one-minute opportunities are rejected as `setup_time_replay_mapping_not_established`.
- Exact failed fields for the `3` new one-minute opportunities: `setup_time_row`, `trigger`, `invalidation`, `freshness_final_signal_state`, `blocker_caution_review`, `session_boundary_behavior`, and `no_hindsight_boundary`.
- Reason: exact one-minute underlying setup-time evidence is present for the authorized SPY session, but raw OHLCV rows alone do not name the accepted SAFE-FAST setup-time row, trigger, invalidation, freshness/final-signal state, blocker/caution state, session-boundary behavior, or no-hindsight boundary.

## Determinism

- Deterministic two-run comparison: `PASS`.
- First run equals second run: `true`.
- Hashes match: `true`.

## Guardrails

- Frozen trading rules changed: `NO`.
- `main.py` changed: `NO`.
- Railway/deploy files changed: `NO`.
- Production/live backend changed: `NO`.
- Broker/order/account code changed: `NO`.
- Credentials or `.env` changed: `NO`.
- Schwab authentication performed: `NO`.
- Broker mutation attempted: `NO`.
- Proof accepted: `NO`.
- Profitability claimed: `NO`.
- Promotion decision made: `NO`.
- Paper eligibility claimed: `NO`.
- Live eligibility claimed: `NO`.

## Checks

- `python -B -m unittest discover -s tests -p "test_day50_raw_data_positive_entry_underlying_setup_time_request.py"`: PASS, `4` tests.
- `python -B -m unittest discover -s tests -p "test_day50_end_to_end_raw_data_positive_entry_generation.py"`: PASS, `10` tests.
- `python -B -m historical_signal_replay.day50_end_to_end_raw_data_positive_entry_generation`: PASS, wrote `36` raw opportunities inspected, `0` setup-qualified, `0` trade candidates, `0` selected contracts, `0` eligible entries, `0` recorded entries, checked cost `0.001370869577`.
- `python -B -m watcher_foundation.day50_end_to_end_raw_data_positive_entry_generation_validator`: PASS, `0` problems.

## Next

Exact next task: `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_SETUP_TIME_REPLAY_MAPPING_CODEX_TASK.md`.

Reason: map the acquired one-minute SPY setup-time evidence through accepted SAFE-FAST replay/calculators to establish or reject exact setup-time row, trigger, invalidation, freshness, blocker/caution, session-boundary, and no-hindsight fields without changing frozen trading rules.
