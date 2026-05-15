# SAFE-FAST Chart-Based Trade Outcome Backtesting v1 Aggregate Summary Review

## Review Status

- **Aggregate summary reporting status:** PASS
- **Baseline:** patch8
- **Latest local commit before summary:** `23576ee Add post-three chart outcome decision review`
- **Summary script file:** `chart_trade_outcome_backtesting/summarize_chart_outcomes.py`
- **Summary report file:** `chart_trade_outcome_backtesting/reports/spy_three_setup_chart_outcome_summary_v1.json`
- **Scope:** bounded aggregate summary reporting for the three validated SPY setup-family chart-only outcome result files.

This review covers summary reporting only. It does not implement a new chart outcome calculation, scan OHLCV source rows for new outcomes, change `main.py`, change schemas, change fixtures, change historical replay runners, model option P&L, add account sizing, start watcher work, auto-trade, use live reads, or make live trade decisions.

## Inputs Read

- `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_POST_THREE_CALCULATION_DECISION_REVIEW.md`
- `chart_trade_outcome_backtesting/reports/first_spy_continuation_chart_outcome_result_v1.json`
- `chart_trade_outcome_backtesting/reports/second_spy_ideal_chart_outcome_result_v1.json`
- `chart_trade_outcome_backtesting/reports/third_spy_clean_fast_break_chart_outcome_result_v1.json`
- `chart_trade_outcome_backtesting/schemas/chart_outcome_backtest_output_v1.schema.json`
- `chart_trade_outcome_backtesting/validate_chart_outcome_fixtures.py`
- `chart_trade_outcome_backtesting/run_chart_outcome_backtest.py`

## Summary Output

- **Samples included:** 3
- **Setup families included:** SPY Continuation, SPY Ideal, SPY Clean Fast Break
- **Follow-through/failure/time-stop summary:** 2 follow-through, 0 failure/invalidated, 1 time stop
- **MFE summary:** Continuation 2.29 points / 0.3199% / 0.3074R; Ideal 2.17 points / 0.2926% / 0.2192R; Clean Fast Break 0.285 points / 0.0407% / 0.0499R
- **MAE summary:** Continuation 0.0 points / 0.0% / 0.0R; Ideal 0.35 points / 0.0472% / 0.0354R; Clean Fast Break 0.735 points / 0.105% / 0.1286R
- **Same-day/fast-swing classification summary:** 2 `same_day`; 1 `time_stop_same_day`
- **Headline/gap-risk context summary:** chart gaps detected in all 3 samples; gap cause known in 0 samples; macro/IV/event context remains unconfirmed and headline context unavailable.

## Boundary Checks

- **Chart-only boundary:** preserved
- **3-sample SPY proof:** yes
- **Profitability proof:** no
- **New outcome calculation from OHLCV source rows:** no
- **Option P&L modeled:** no
- **Account sizing added:** no
- **Broker/order execution modeled:** no
- **Watcher work started:** no
- **Watcher output included:** no
- **`main.py` changed:** no
- **Schemas changed:** no
- **Fixtures changed:** no
- **Existing chart outcome result files changed:** no
- **Historical replay runner changed:** no

## Validation

- **Chart fixture validation result:** PASS; `python -B chart_trade_outcome_backtesting/validate_chart_outcome_fixtures.py`
- **Chart runner result:** PASS; `python -B chart_trade_outcome_backtesting/run_chart_outcome_backtest.py`
- **Aggregate summary script result:** PASS; `python -B chart_trade_outcome_backtesting/summarize_chart_outcomes.py`
- **Summary JSON validation result:** PASS; `python -m json.tool chart_trade_outcome_backtesting/reports/spy_three_setup_chart_outcome_summary_v1.json`
- **Historical signal replay result:** PASS; `python -B historical_signal_replay/run_signal_replay.py`
- **Contract tests result:** PASS; all `replay/test_on_demand_*contract.py` files passed locally
- **Stage-message result:** PASS; `python -B replay/test_on_demand_stage_messages.py`
- **Fixture validation result:** PASS; `python -B replay/validate_fixtures.py`
- **Full replay result:** PASS; `python -B replay/run_replay.py` returned `16/16 passed`, `local_fixture_engine=16`, `placeholder_scaffold=0`

## Recommended Next Task

Validate aggregate chart outcome summary report.
