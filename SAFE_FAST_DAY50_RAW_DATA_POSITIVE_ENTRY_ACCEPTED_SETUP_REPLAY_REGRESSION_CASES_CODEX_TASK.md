# SAFE-FAST Day 50 Raw-Data Positive-Entry Accepted Setup Replay Regression Cases

## Required startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_ACCEPTED_SETUP_REPLAY_PATH_DECISION_RESULT.md`
2. `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_SETUP_TIME_REPLAY_MAPPING_RESULT.md`
3. `historical_signal_replay/results/day50_raw_data_positive_entry_setup_time_replay_mapping.json`
4. `SAFE_FAST_DATA_SOURCE_REGISTRY.md`
5. `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`
6. `SAFE_FAST_PROJECT_DASHBOARD.md`
7. `SAFE_FAST_PROJECT_RULE_INDEX.md`

## Active objective

Define the bounded replay/regression cases and accepted field boundaries required before any raw one-minute underlying OHLCV setup-replay mapping path can be implemented for the Day 50 SPY raw-data positive-entry retry.

This is still planning/governance and regression-definition work only.

## Restrictions

- Do not implement the raw OHLCV setup-label mapper.
- Do not retry the Day 50 SPY raw-data positive-entry opportunities.
- Do not request more data.
- Do not request option data.
- Do not request exit-path data.
- Do not touch `main.py`, Railway/deploy files, production/live backend, broker/order/account code, credentials, or `.env`.
- Do not weaken frozen trading rules.
- Do not infer SAFE-FAST labels directly from raw vendor bars.
- Do not claim proof, profitability, readiness, promotion, paper eligibility, or live eligibility.
- Stop after defining the bounded regression cases, field boundaries, non-goals, and exact next task.

## Required output

Create one result document and update canonical handoff/control files with:

- exact replay/regression cases required before implementation;
- accepted field-boundary definitions for `setup_time_row`, `trigger`, `invalidation`, `freshness_final_signal_state`, `blocker_caution_review`, `session_boundary_behavior`, and `no_hindsight_boundary`;
- covered setup families: Ideal, Clean Fast Break, and Continuation for SPY March 16, 2026 only;
- exact missing-data, wrong-symbol, wrong-window, no-hindsight, duplicate, and raw-vendor-label rejection cases;
- exact non-goals and forbidden inferences;
- exact next task.
