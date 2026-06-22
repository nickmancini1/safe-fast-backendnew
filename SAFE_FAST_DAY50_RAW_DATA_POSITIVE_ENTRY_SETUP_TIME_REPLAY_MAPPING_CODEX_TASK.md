# SAFE-FAST Day 50 Raw-Data Positive-Entry Setup-Time Replay Mapping

## Required startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_UNDERLYING_SETUP_TIME_COSTED_REQUEST_RESULT.md`
2. `historical_signal_replay/results/day50_end_to_end_raw_data_positive_entry_generation.json`
3. `historical_signal_replay/results/day50_raw_data_positive_entry_underlying_setup_time_costed_request.json`
4. `historical_signal_replay/fixtures/day50_raw_data_positive_entry_candidate_manifest.json`
5. `SAFE_FAST_DATA_SOURCE_REGISTRY.md`
6. `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`
7. `SAFE_FAST_PROJECT_DASHBOARD.md`
8. `SAFE_FAST_PROJECT_RULE_INDEX.md`

## Active objective

Use only the acquired Day 50 SPY one-minute underlying setup-time evidence:

- Request ID: `DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M`
- CSV: `historical_signal_replay/source_data/external_underlying_data_drop/SAFE_FAST_DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M.csv`
- Dataset/schema/stype: `DBEQ.BASIC / ohlcv-1m / raw_symbol`
- Window: `2026-03-16T09:30:00-04:00` through `2026-03-16T16:00:00-04:00`

Map the evidence through accepted SAFE-FAST replay/calculators, if such accepted paths already exist, to establish or reject exact setup-time row, trigger, invalidation, freshness/final-signal state, blocker/caution state, session-boundary behavior, and no-hindsight boundary for the three SPY setup-family opportunities.

## Restrictions

- Do not request more data.
- Do not request option data.
- Do not request exit-path data.
- Do not touch `main.py`, Railway/deploy files, production/live backend, broker/order/account code, credentials, or `.env`.
- Do not weaken frozen trading rules.
- Do not infer SAFE-FAST labels directly from raw vendor bars without an accepted local rule/calculator path.
- Do not claim proof, profitability, readiness, promotion, paper eligibility, or live eligibility.
- Stop after this exact mapping/rejection task is handled.

## Required output

Create one result document and update the canonical handoff/control files with:

- whether each of the three SPY setup-family opportunities can establish exact setup-time fields;
- exact blockers for every rejected opportunity;
- any new setup-qualified, trade-candidate, selected-contract, eligible-entry, or recorded-entry totals;
- deterministic comparison;
- exact next task.
