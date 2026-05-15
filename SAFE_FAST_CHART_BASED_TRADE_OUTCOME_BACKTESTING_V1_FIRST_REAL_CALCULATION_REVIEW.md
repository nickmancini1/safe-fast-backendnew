# SAFE-FAST Chart-Based Trade Outcome Backtesting v1 First Real Calculation Review

## Review Status

- **Calculation status:** PASS
- **Baseline:** patch8
- **Latest local commit before calculation:** `3a0b34e Add chart outcome calculation rules plan`
- **Scope:** first real chart-only outcome calculation for the first SPY Continuation sample only
- **Calculation rules source:** `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_CALCULATION_RULES_PLAN.md`
- **Sample used:** `chart_trade_outcome_backtesting/fixtures/first_spy_continuation_chart_outcome_input_v1.json`
- **Source signal log:** `historical_signal_replay/reports/first_real_spy_continuation_replay_v1_signal_log.jsonl`
- **Source OHLCV:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`
- **Report file:** `chart_trade_outcome_backtesting/reports/first_spy_continuation_chart_outcome_result_v1.json`

## Calculation Result

- **Symbol:** SPY
- **Setup family:** Continuation
- **Direction:** CALL
- **Eligible signal row:** `triggered_signal_stage_candidate`
- **Signal timestamp:** `2026-04-30T12:30:00-04:00`
- **Entry result:** entry reached at `2026-04-30T13:30:00-04:00` using next eligible 1H RTH candle open `715.82`
- **Invalidation result:** copied pre-entry invalidation `708.37`; not reached before terminal follow-through
- **Follow-through/failure/time-stop result:** follow-through reached on `2026-04-30T13:30:00-04:00` when high `718.11` reached the predeclared 2.0 point favorable touch threshold; failure and time stop did not trigger
- **MFE result:** `2.29` points, `0.3199%`, `0.3074R`, at `2026-04-30T13:30:00-04:00`
- **MAE result:** `0.0` points, `0.0%`, `0.0R`, at `2026-04-30T13:30:00-04:00`
- **Same-day/fast-swing classification:** `same_day`

## Boundary Checks

- **Chart-only boundary:** preserved; only underlying-chart OHLCV outcome behavior was calculated
- **Real source OHLCV rows only:** yes
- **Fabricated prices/timestamps:** no
- **Headline/gap-risk context:** preserved as unavailable/unconfirmed where source context does not confirm it
- **Likely-risk vs full-risk notes:** preserved as chart-only notes
- **Option P&L modeled:** no
- **Account sizing added:** no
- **Broker/order execution modeled:** no
- **Watcher work started:** no
- **`main.py` changed:** no
- **Schemas changed:** no
- **Fixtures changed:** no
- **Historical replay runner changed:** no

## Validation

- **Chart fixture validation:** PASS; `python -B chart_trade_outcome_backtesting/validate_chart_outcome_fixtures.py`
- **Chart runner:** PASS; `python -B chart_trade_outcome_backtesting/run_chart_outcome_backtest.py`
- **Output JSON parse/schema validation:** PASS; runner validates the emitted report against `chart_trade_outcome_backtesting/schemas/chart_outcome_backtest_output_v1.schema.json`, and `python -m json.tool chart_trade_outcome_backtesting/reports/first_spy_continuation_chart_outcome_result_v1.json` parses successfully

## Next Task

Validate first real chart outcome calculation output.
