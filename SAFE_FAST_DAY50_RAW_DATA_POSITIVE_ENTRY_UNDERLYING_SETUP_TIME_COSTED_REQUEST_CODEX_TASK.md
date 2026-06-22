# SAFE-FAST Day 50 Raw-Data Positive-Entry Underlying Setup-Time Costed Request

## Required startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DAY50_END_TO_END_RAW_DATA_POSITIVE_ENTRY_GENERATION_RESULT.md`
2. `historical_signal_replay/results/day50_end_to_end_raw_data_positive_entry_generation.json`
3. `historical_signal_replay/fixtures/day50_raw_data_positive_entry_candidate_manifest.json`
4. `SAFE_FAST_DATA_SOURCE_REGISTRY.md`
5. `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`
6. `SAFE_FAST_PROJECT_DASHBOARD.md`
7. `SAFE_FAST_PROJECT_RULE_INDEX.md`

## Active objective

Use only the exact cost-checked underlying setup-time request created by the raw-data generation result:

- Request ID: `DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M`
- Symbol: `SPY`
- Window: `2026-03-16T09:30:00-04:00` through `2026-03-16T16:00:00-04:00`
- Dataset/schema/stype: `DBEQ.BASIC / ohlcv-1m / raw_symbol`
- Checked cost: `0.001370869577`

Acquire or otherwise supply this exact underlying setup-time evidence only after confirming approval scope. Then rerun the raw-data positive-entry generator and validator without changing frozen rules.

## Restrictions

- Do not request option data.
- Do not request exit-path data.
- Do not touch `main.py`, Railway/deploy files, production/live backend, broker/order/account code, credentials, or `.env`.
- Do not weaken frozen trading rules.
- Do not claim proof, profitability, readiness, promotion, paper eligibility, or live eligibility.
- Stop after this exact request is handled and the raw-data generator is rerun.

## Required output

Create one result document and update the canonical handoff/control files with:

- whether the exact underlying setup-time evidence was acquired or supplied;
- checked cost and actual billed cost when available;
- new raw opportunities inspected;
- new setup-qualified candidates;
- new trade candidates;
- new selected contracts;
- new eligible entries;
- new recorded entries;
- exact blockers for every rejected opportunity;
- deterministic two-run comparison;
- exact next task.
