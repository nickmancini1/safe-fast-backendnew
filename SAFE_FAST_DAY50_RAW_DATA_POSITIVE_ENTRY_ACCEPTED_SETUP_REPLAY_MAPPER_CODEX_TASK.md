# SAFE-FAST Day 50 Raw-Data Positive-Entry Accepted Setup Replay Mapper

## Required startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_ACCEPTED_SETUP_REPLAY_REGRESSION_CASES_RESULT.md`
2. `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_ACCEPTED_SETUP_REPLAY_PATH_DECISION_RESULT.md`
3. `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_SETUP_TIME_REPLAY_MAPPING_RESULT.md`
4. `historical_signal_replay/results/day50_raw_data_positive_entry_setup_time_replay_mapping.json`
5. `SAFE_FAST_DATA_SOURCE_REGISTRY.md`
6. `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`
7. `SAFE_FAST_PROJECT_DASHBOARD.md`
8. `SAFE_FAST_PROJECT_RULE_INDEX.md`

## Active objective

Implement the bounded raw one-minute underlying OHLCV setup-replay mapper for the Day 50 SPY raw-data positive-entry retry only after honoring the accepted replay/regression cases and field boundaries.

## Scope

- Covered symbol/date: SPY on March 16, 2026 only.
- Covered evidence: `historical_signal_replay/source_data/external_underlying_data_drop/SAFE_FAST_DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M.csv`.
- Covered dataset/schema/stype: `DBEQ.BASIC / ohlcv-1m / raw_symbol`.
- Covered setup families: Ideal, Clean Fast Break, and Continuation only.
- Covered fields: `setup_time_row`, `trigger`, `invalidation`, `freshness_final_signal_state`, `blocker_caution_review`, `session_boundary_behavior`, and `no_hindsight_boundary`.

## Required implementation gates

- Implement only the bounded mapper needed to produce or reject setup-time field packages under the accepted field boundaries.
- Add focused replay/regression cases for every case defined in `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_ACCEPTED_SETUP_REPLAY_REGRESSION_CASES_RESULT.md`.
- Preserve deterministic output across repeated runs.
- Preserve existing Day 50 regression controls separately and unchanged.
- Report before-and-after funnel totals.

## Restrictions

- Do not request more data.
- Do not request option data.
- Do not request exit-path data.
- Do not infer SAFE-FAST labels directly from raw vendor bars.
- Do not weaken frozen trading rules.
- Do not reopen closed safety rejections or preserved controls.
- Do not touch `main.py`, Railway/deploy files, production/live backend, broker/order/account code, credentials, or `.env`.
- Do not perform Schwab authentication or any broker mutation.
- Do not claim proof, profitability, readiness, promotion, paper eligibility, or live eligibility.

## Required output

Create one result document and any necessary focused machine-readable result, tests, and validator updates with:

- implemented bounded mapper behavior;
- every accepted replay/regression case and result;
- exact field packages produced or exact failed fields for Ideal, Clean Fast Break, and Continuation;
- exact missing-data, wrong-symbol, wrong-window, no-hindsight, duplicate, and raw-vendor-label rejection outcomes;
- deterministic comparison result;
- preserved Day 50 controls and scorecard;
- exact non-goals and forbidden inferences;
- exact next task.
