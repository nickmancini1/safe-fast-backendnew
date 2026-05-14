# SAFE-FAST Chart-Based Trade Outcome Backtesting v1 Sample Fixture Review

## Sample Fixture Status

- **Status:** PASS
- **Baseline:** patch8
- **Latest local commit reviewed:** `656eb59 Add chart-based trade outcome backtesting v1 schemas`
- **Scope:** create first chart-based trade outcome backtesting v1 sample input/output fixture only.
- **Backtesting implementation started:** no

## Files Created

- `chart_trade_outcome_backtesting/fixtures/first_spy_continuation_chart_outcome_input_v1.json`
- `chart_trade_outcome_backtesting/fixtures/first_spy_continuation_chart_outcome_expected_output_v1.json`
- `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_SAMPLE_FIXTURE_REVIEW.md`

## Source Basis

- **Source replay fixture:** `historical_signal_replay/fixtures/first_real_spy_continuation_replay_v1_fixture.json`
- **Source signal log:** `historical_signal_replay/reports/first_real_spy_continuation_replay_v1_signal_log.jsonl`
- **Source summary:** `historical_signal_replay/reports/first_real_spy_continuation_replay_v1_summary.json`
- **Source candle CSV:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`
- **Source row:** `triggered_signal_stage_candidate`
- **Source row index:** 5
- **Source signal timestamp:** `2026-04-30T12:30:00-04:00`
- **Symbol:** SPY
- **Setup family:** Continuation

## Fixture Boundary

This fixture is chart-only sample/scaffold. It does not implement a backtest runner and does not prove final trade outcome performance.

Included chart-only fields:

- entry condition
- invalidation condition
- follow-through condition
- failure condition
- time-stop condition
- max favorable move
- max adverse move
- same-day / fast-swing classification
- headline and gap-risk context
- likely chart risk versus full-risk note

Excluded by design:

- option P&L
- option-spread pricing
- Greeks
- account sizing
- account drawdown
- broker/order execution
- watcher state mutation
- auto-trading
- live trade decisions

## Expected Output Status

The expected output fixture is intentionally marked as sample/scaffold. It uses the real source candles around the SPY Continuation signal, but the measured terminal outcome is not final backtest proof because no backtest runner exists yet.

The sample output uses:

- entry policy: `next_eligible_candle_after_signal`
- entry price policy: `next_eligible_candle_open`
- sample entry timestamp: `2026-04-30T13:30:00-04:00`
- sample entry reference price: `715.82`
- copied replay invalidation: `708.37`
- sample follow-through threshold: `2.0` favorable underlying points
- sample terminal candle: `2026-04-30T13:30:00-04:00`
- sample same-day classification: `same_day`

## Non-Changes

- **`main.py` changed:** no
- **Historical replay runner changed:** no
- **Schemas changed:** no
- **Historical replay fixtures changed:** no
- **Reports changed:** no
- **Backtesting implementation started:** no
- **Option P&L modeled:** no
- **Account sizing added:** no
- **Watcher implementation started:** no

## Validation

- **Input fixture JSON validation result:** PASS
- **Expected output fixture JSON validation result:** PASS
- **Input schema JSON validation result:** PASS
- **Output schema JSON validation result:** PASS
- **Historical signal replay runner result:** PASS
- **Contract tests result:** PASS
- **Stage-message result:** PASS
- **Fixture validation result:** PASS
- **Full replay result:** PASS

## Recommended Next Task

Validate chart-based trade outcome sample fixture against schemas without implementing a backtest runner, modeling option P&L, adding account sizing, changing `main.py`, changing historical replay artifacts, or starting watcher implementation.
