# SAFE-FAST Day 50 Raw-Data Positive-Entry Setup-Time Replay Mapping Result

## Scope

- Task executed: `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_SETUP_TIME_REPLAY_MAPPING_CODEX_TASK.md`.
- Machine-readable result: `historical_signal_replay/results/day50_raw_data_positive_entry_setup_time_replay_mapping.json`.
- Mapping helper: `historical_signal_replay/day50_raw_data_positive_entry_setup_time_replay_mapping.py`.
- Validator: `watcher_foundation/day50_raw_data_positive_entry_setup_time_replay_mapping_validator.py`.
- Focused tests: `tests/test_day50_raw_data_positive_entry_setup_time_replay_mapping.py`.
- Exact request ID: `DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M`.
- Evidence used: `historical_signal_replay/source_data/external_underlying_data_drop/SAFE_FAST_DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M.csv`.
- Dataset/schema/stype: `DBEQ.BASIC / ohlcv-1m / raw_symbol`.
- Authorized window: `SPY`, `2026-03-16T09:30:00-04:00` through `2026-03-16T16:00:00-04:00`.

## Evidence Validation

- Used only acquired Day 50 SPY one-minute underlying setup-time evidence: `YES`.
- Source CSV row count: `751`.
- Source symbol set: `SPY`.
- Source event timestamp span: `2026-03-16T13:30:00.000000000Z` through `2026-03-16T19:59:00.000000000Z`.
- Required OHLCV columns present: `YES`.
- Chronological rows: `YES`.
- Raw vendor data modified: `NO`.
- Additional data requested: `NO`.
- Option data requested: `NO`.
- Exit-path data requested: `NO`.

## Mapping Outcome

The acquired SPY one-minute OHLCV evidence was valid underlying evidence, but it did not establish exact SAFE-FAST setup-time fields for any of the three setup-family opportunities.

Raw vendor OHLCV bars were not treated as SAFE-FAST labels. Existing accepted paths checked for the three families require prerequisite SAFE-FAST state inputs such as setup identity, exact setup/replay row, trigger, invalidation, lifecycle stage, trigger state, prior state, accepted lifecycle rule metadata, context/caution component inputs, and no-hindsight replay boundary. Those prerequisites are not supplied by the raw vendor OHLCV file.

## Per-Family Results

| Setup family | Exact setup-time fields established | Candidate generated | Setup-qualified | Trade candidate | Exact blocker |
| --- | ---: | ---: | ---: | ---: | --- |
| Ideal | `NO` | `NO` | `NO` | `NO` | `accepted_setup_time_replay_mapping_path_absent` |
| Clean Fast Break | `NO` | `NO` | `NO` | `NO` | `accepted_setup_time_replay_mapping_path_absent` |
| Continuation | `NO` | `NO` | `NO` | `NO` | `accepted_setup_time_replay_mapping_path_absent` |

Exact failed fields for all three SPY opportunities:

- `setup_time_row`
- `trigger`
- `invalidation`
- `freshness_final_signal_state`
- `blocker_caution_review`
- `session_boundary_behavior`
- `no_hindsight_boundary`

## Totals

- Raw opportunities mapped: `3`.
- Exact setup-time field packages established: `0`.
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
- New exact-data-required cases: `3`.
- New missed valid trades: `0`.
- New invalid trades allowed: `0`.
- New unresolved cases: `0`.
- New winners: `0`.
- New losers: `0`.

## Determinism

- Deterministic comparison: `PASS`.
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

- `python -B -m unittest discover -s tests -p "test_day50_raw_data_positive_entry_setup_time_replay_mapping.py"`: PASS, `7` tests.
- `python -B -m historical_signal_replay.day50_raw_data_positive_entry_setup_time_replay_mapping`: PASS, wrote `3` mapped, `0` established, `0` setup-qualified, `0` trade candidates.
- `python -B -m watcher_foundation.day50_raw_data_positive_entry_setup_time_replay_mapping_validator`: PASS, `0` problems.
- `python -B -m unittest discover -s tests -p "test_day50_end_to_end_raw_data_positive_entry_generation.py"`: PASS, `10` tests.
- `python -B -m watcher_foundation.day50_end_to_end_raw_data_positive_entry_generation_validator`: PASS, `0` problems.

## Next

Exact next task: `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_ACCEPTED_SETUP_REPLAY_PATH_DECISION_CODEX_TASK.md`.

Reason: decide whether to create a bounded accepted setup-replay mapping path with replay/regression cases before any raw one-minute OHLCV evidence can generate setup-time labels.
