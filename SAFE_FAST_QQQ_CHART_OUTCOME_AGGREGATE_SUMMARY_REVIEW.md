# SAFE-FAST QQQ Chart Outcome Aggregate Summary Review

## Status

- **Summary status:** PASS
- **Baseline:** patch8
- **Latest local commit before summary:** 29fc799 Add QQQ Continuation chart outcome output validation
- **Summary script file:** `chart_trade_outcome_backtesting/summarize_chart_outcomes.py`
- **Summary report file:** `chart_trade_outcome_backtesting/reports/qqq_three_setup_chart_outcome_summary_v1.json`
- **Source schema:** `chart_trade_outcome_backtesting/schemas/chart_outcome_backtest_output_v1.schema.json`

## Scope

- **Samples included:** 3
- **Setup families included:** Ideal, Clean Fast Break, Continuation
- **Source result files read:**
  - `chart_trade_outcome_backtesting/reports/qqq_ideal_chart_outcome_result_v1.json`
  - `chart_trade_outcome_backtesting/reports/qqq_clean_fast_break_chart_outcome_result_v1.json`
  - `chart_trade_outcome_backtesting/reports/qqq_continuation_chart_outcome_result_v1.json`
- **Source result schema validation:** each source result is validated against `chart_outcome_backtest_output_v1.schema.json` before summary output is written.
- **New OHLCV outcome calculation:** no

## Aggregate Result

- **Total samples:** 3
- **Follow-through count:** 3
- **Failure count:** 0
- **Time-stop count:** 0
- **Same-day / fast-swing classification:** same_day 2, fast_swing 1
- **Headline/gap-risk context:** chart gap detected in 3 of 3 samples; gap cause known in 0 of 3; macro/IV/event context unconfirmed in 3 of 3; headline context unavailable in 3 of 3.

## MFE / MAE

- **Aggregate MFE:** average 4.9633 points / 0.7410% / 0.4583 chart R; max 6.62 points / 0.9893% / 0.6727 chart R.
- **Aggregate MAE:** average 0.7450 points / 0.1112% / 0.0798 chart R; max 1.115 points / 0.1560% / 0.1557 chart R.
- **Ideal MFE/MAE:** MFE 4.9 points / 0.6855% / 0.2703 chart R; MAE 1.115 points / 0.1560% / 0.0615 chart R.
- **Clean Fast Break MFE/MAE:** MFE 3.37 points / 0.5483% / 0.6727 chart R; MAE 0.78 points / 0.1269% / 0.1557 chart R.
- **Continuation MFE/MAE:** MFE 6.62 points / 0.9893% / 0.4318 chart R; MAE 0.34 points / 0.0508% / 0.0222 chart R.

## Boundary Review

- **Chart-only boundary preserved:** yes
- **3-sample QQQ proof, not profitability proof:** yes
- **Option P&L modeled:** no
- **Account sizing added:** no
- **Broker/order execution modeled:** no
- **Watcher work started:** no
- **`main.py` changed:** no
- **Schemas changed:** no
- **Fixtures changed:** no
- **Historical replay runner changed:** no
- **Existing QQQ chart outcome result files changed:** no

## Next Task

- **Recommended next task:** validate QQQ aggregate chart outcome summary report.
