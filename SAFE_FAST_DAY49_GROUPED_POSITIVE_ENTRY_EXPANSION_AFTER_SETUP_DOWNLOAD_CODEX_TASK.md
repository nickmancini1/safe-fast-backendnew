# SAFE-FAST Day 49 Grouped Positive-Entry Expansion After Setup Download

## Startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_SETUP_TIME_DOWNLOAD_AND_REPLAY_RESULT.md`
2. `historical_signal_replay/results/day48_positive_trade_capture_funnel.json`
3. `historical_signal_replay/day48_positive_trade_capture_funnel.py`
4. `historical_signal_replay/day49_grouped_positive_entry_setup_time.py`
5. `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`
6. `SAFE_FAST_PROJECT_DASHBOARD.md`
7. `SAFE_FAST_PROJECT_RULE_INDEX.md`

This is build testing, not live trading.

## Objective

Expand positive-entry coverage in a grouped, evidence-driven way after the Day 49 setup-time download proved two additional real stale-quote no-trade controls.

Focus on finding or preparing the smallest grouped path toward more valid positive entries and at least one losing valid-entry example while preserving:

- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` as the review-only positive winner reference;
- `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`, `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`, `SPY-REAL-HISTORICAL-IDEAL-001`, and `SPY-REAL-HISTORICAL-CONTINUATION-001` as stale-quote true no-trade controls;
- remaining missing-data and unresolved cases as separate from true no-trades.

## Restrictions

Do not modify production, live backend, `main.py`, Railway, deployment, broker, account, order, credential, or `.env` files.

Do not download data unless this task first creates an exact scoped missing-data request package and stops at cost-check/no-download status.

Do not download exit data unless a later task explicitly authorizes it after a valid entry is proven.

Do not calculate P&L without a valid entry and authorized exit evidence.

Do not claim profitability, proof, readiness, promotion, paper eligibility, or live eligibility.

Do not commit or push.

## Required Result

Create one result document that reports:

- grouped candidate inventory reviewed;
- before/after funnel totals;
- positive-entry candidates found or not found;
- true no-trade controls preserved;
- missing-data cases that remain;
- unresolved cases that remain;
- whether a new exact cost-check package is needed;
- exact next grouped task filename.

Run focused funnel tests, validator, grouped replay tests affected by the change, safe checks, evidence validator, intake bridge, and `git diff --check`.
