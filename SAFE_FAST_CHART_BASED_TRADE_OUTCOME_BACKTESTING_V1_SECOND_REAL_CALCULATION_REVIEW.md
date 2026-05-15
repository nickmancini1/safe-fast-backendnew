# SAFE-FAST Chart-Based Trade Outcome Backtesting v1 Second Real Calculation Review

## Review Status

- **Calculation status:** PASS
- **Baseline:** patch8
- **Latest local commit before calculation:** `f81055d Add post-first chart outcome decision review`
- **Scope:** second real chart-only outcome calculation for the SPY Ideal sample.

This review covers only underlying-chart outcome measurement from real SPY 1H RTH OHLCV rows. It does not model option P&L, account sizing, broker/order execution, watcher behavior, auto-trading, live reads, or live trade decisions.

## Inputs Used

- `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_CALCULATION_RULES_PLAN.md`
- `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_POST_FIRST_CALCULATION_DECISION_REVIEW.md`
- `chart_trade_outcome_backtesting/fixtures/second_spy_ideal_chart_outcome_input_v1.json`
- `historical_signal_replay/reports/second_real_spy_ideal_replay_v1_signal_log.jsonl`
- `historical_signal_replay/reports/second_real_spy_ideal_replay_v1_summary.json`
- `historical_signal_replay/fixtures/second_real_spy_ideal_replay_v1_fixture.json`
- `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`

## Calculation Result

- **Sample used:** `chart_trade_outcome_backtesting/fixtures/second_spy_ideal_chart_outcome_input_v1.json`
- **Symbol/setup:** SPY Ideal
- **Report file:** `chart_trade_outcome_backtesting/reports/second_spy_ideal_chart_outcome_result_v1.json`
- **Eligible signal row:** `ideal_triggered_signal_stage_candidate` at `2026-05-13T11:30:00-04:00`
- **Entry result:** entry reached at `2026-05-13T12:30:00-04:00` using next eligible 1H RTH candle open `741.73`
- **Invalidation result:** copied pre-entry invalidation `731.83`; not reached before terminal follow-through
- **Follow-through/failure/time-stop result:** follow-through reached on `2026-05-13T13:30:00-04:00`; failure not reached; time stop not reached
- **MFE result:** `2.17` points / `0.2926%` / `0.2192R`
- **MAE result:** `0.35` points / `0.0472%` / `0.0354R`
- **Same-day/fast-swing classification:** `same_day`

## Boundary Checks

- **Chart-only boundary:** preserved
- **Headline/gap-risk context:** preserved as unconfirmed/unavailable; chart gap recorded from source candles with unknown cause
- **Likely-risk vs full-risk notes:** preserved as chart-only notes
- **Option P&L modeled:** no
- **Account sizing added:** no
- **Broker/order execution modeled:** no
- **Watcher work started:** no
- **`main.py` changed:** no
- **Schemas changed:** no
- **Historical replay fixtures changed:** no
- **Historical replay runner changed:** no

## Validation

- **Chart fixture validation:** PASS; `python -B chart_trade_outcome_backtesting/validate_chart_outcome_fixtures.py`
- **Chart runner:** PASS; `python -B chart_trade_outcome_backtesting/run_chart_outcome_backtest.py`
- **Output JSON parse/schema validation:** PASS; runner validated output schema and `python -m json.tool chart_trade_outcome_backtesting/reports/second_spy_ideal_chart_outcome_result_v1.json` parsed successfully

## Recommended Next Task

Validate second real chart outcome calculation output.
