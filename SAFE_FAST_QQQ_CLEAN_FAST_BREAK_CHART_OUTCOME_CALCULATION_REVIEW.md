# SAFE-FAST QQQ Clean Fast Break Chart Outcome Calculation Review

## Review Status

- **Calculation status:** PASS
- **Baseline:** patch8
- **Latest local commit before calculation:** `8ad5782 Add QQQ Ideal chart outcome output validation`
- **Sample used:** QQQ Clean Fast Break accepted historical signal replay row `clean_fast_break_initial_break_candidate`
- **Symbol/setup:** QQQ / Clean Fast Break
- **Input fixture:** `chart_trade_outcome_backtesting/fixtures/qqq_clean_fast_break_chart_outcome_input_v1.json`
- **Expected output fixture:** `chart_trade_outcome_backtesting/fixtures/qqq_clean_fast_break_chart_outcome_expected_output_v1.json`
- **Report file:** `chart_trade_outcome_backtesting/reports/qqq_clean_fast_break_chart_outcome_result_v1.json`

## Calculation Result

- **Chart-only boundary:** PASS; uses real QQQ 1H RTH source OHLCV rows only and excludes option P&L, account sizing, broker/order execution, watcher behavior, auto-trading, and live trade decisions.
- **Entry result:** entry reached at `2026-04-13T13:30:00-04:00`, reference price 614.59, using the next eligible candle open after the `2026-04-13T12:30:00-04:00` signal row.
- **Invalidation result:** copied invalidation 609.58 was not reached before terminal follow-through.
- **Follow-through/failure/time-stop result:** follow-through reached at `2026-04-13T15:30:00-04:00` high 617.96 before invalidation or time stop; classified as `same_day`.
- **MFE result:** 3.37 points / 0.5483% / 0.6727 chart R at `2026-04-13T15:30:00-04:00`.
- **MAE result:** 0.78 points / 0.1269% / 0.1557 chart R at `2026-04-13T13:30:00-04:00`.
- **Headline/gap-risk context:** macro/IV/event unconfirmed, headline unavailable, chart gap down -1.565 points / -0.2561%, gap cause unknown.
- **Likely risk vs full-risk note:** likely chart risk is underlying-chart distance only; full financial risk remains unmodeled.

## Boundary

- **Option P&L modeled:** no
- **Account sizing added:** no
- **Watcher work started:** no
- **`main.py` changed:** no
- **Schemas changed:** no
- **Historical replay fixtures changed:** no
- **Historical replay runner changed:** no

## Validation

- **Chart fixture validation result:** PASS; `python -B chart_trade_outcome_backtesting/validate_chart_outcome_fixtures.py`
- **Chart runner result:** PASS; `python -B chart_trade_outcome_backtesting/run_chart_outcome_backtest.py`
- **Output JSON validation result:** PASS; `python -m json.tool chart_trade_outcome_backtesting/reports/qqq_clean_fast_break_chart_outcome_result_v1.json`
- **Historical signal replay result:** PASS; `python -B historical_signal_replay/run_signal_replay.py`
- **Contract tests result:** PASS; all `replay/test_on_demand_*contract.py` files passed locally
- **Stage-message result:** PASS; `python -B replay/test_on_demand_stage_messages.py`
- **Fixture validation result:** PASS; `python -B replay/validate_fixtures.py`
- **Full replay result:** PASS; `python -B replay/run_replay.py`

## Next Task

Validate QQQ Clean Fast Break chart outcome calculation output.
