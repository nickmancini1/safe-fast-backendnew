# SAFE-FAST QQQ Continuation Chart Outcome Calculation Review

## Review Status

- **Calculation status:** PASS
- **Baseline:** patch8
- **Latest local commit before calculation:** `fc21fd3 Add QQQ Clean Fast Break chart outcome output validation`
- **Sample used:** QQQ Continuation accepted historical signal replay row `continuation_triggered_signal_stage_candidate`
- **Symbol/setup:** QQQ / Continuation
- **Input fixture:** `chart_trade_outcome_backtesting/fixtures/qqq_continuation_chart_outcome_input_v1.json`
- **Expected output fixture:** `chart_trade_outcome_backtesting/fixtures/qqq_continuation_chart_outcome_expected_output_v1.json`
- **Report file:** `chart_trade_outcome_backtesting/reports/qqq_continuation_chart_outcome_result_v1.json`

## Calculation Result

- **Chart-only boundary:** PASS; uses real QQQ 1H RTH source OHLCV rows only and excludes option P&L, account sizing, broker/order execution, watcher behavior, auto-trading, and live trade decisions.
- **Entry result:** entry reached at `2026-05-01T09:30:00-04:00`, reference price 669.14, using the next eligible candle open after the `2026-04-30T15:30:00-04:00` signal row.
- **Invalidation result:** copied invalidation 653.81 was not reached before terminal follow-through.
- **Follow-through/failure/time-stop result:** follow-through reached at `2026-05-01T09:30:00-04:00` high 675.76 before invalidation or time stop; classified as `same_day`.
- **MFE result:** MFE 6.62 points / 0.9893% / 0.4318 chart R.
- **MAE result:** MAE 0.34 points / 0.0508% / 0.0222 chart R.
- **Headline/gap-risk context:** macro/IV/event unconfirmed, headline unavailable, chart gap up 1.54 points / 0.2307%, gap cause unknown.
- **Likely risk vs full-risk note:** likely chart risk is underlying-chart distance only; full financial risk remains unmodeled.

## Boundaries

- **Option P&L modeled:** no
- **Account sizing added:** no
- **Watcher work started:** no
- **`main.py` changed:** no
- **Schemas changed:** no
- **Historical replay fixtures changed:** no
- **Historical replay runner changed:** no

## Next Task

Validate QQQ Continuation chart outcome calculation output.
