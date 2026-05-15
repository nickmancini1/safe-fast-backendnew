# SAFE-FAST Chart-Based Trade Outcome Backtesting v1 First Real Calculation Output Validation Review

## Review Status

- **Validation status:** PASS
- **Baseline:** patch8
- **Latest local commit before validation:** `2ad782e Add first real chart outcome calculation`
- **Scope:** validate first real chart-only SPY Continuation outcome calculation output
- **Sample/result file:** `chart_trade_outcome_backtesting/reports/first_spy_continuation_chart_outcome_result_v1.json`
- **Input fixture:** `chart_trade_outcome_backtesting/fixtures/first_spy_continuation_chart_outcome_input_v1.json`
- **Rules source:** `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_CALCULATION_RULES_PLAN.md`

## Validation Findings

- **Runner execution result:** PASS; `python -B chart_trade_outcome_backtesting/run_chart_outcome_backtest.py`
- **Result report exists:** yes
- **Output schema validation result:** PASS; runner validated the emitted report and `python -m json.tool chart_trade_outcome_backtesting/reports/first_spy_continuation_chart_outcome_result_v1.json` parsed successfully
- **Entry validation result:** PASS; entry timestamp `2026-04-30T13:30:00-04:00` and entry reference price `715.82` match the next eligible real SPY 1H RTH source row after source signal timestamp `2026-04-30T12:30:00-04:00`
- **Invalidation validation result:** PASS; invalidation `708.37` is copied from the eligible replay signal row, and the terminal candle low `715.82` did not touch or cross invalidation before follow-through
- **Follow-through/failure/time-stop validation result:** PASS; bullish follow-through threshold is predeclared at `2.0` favorable points, entry `715.82` plus threshold requires `717.82`, and the real terminal candle high `718.11` reached follow-through on `2026-04-30T13:30:00-04:00`; failure and time stop did not trigger
- **MFE validation result:** PASS; MFE `2.29` points, `0.3199%`, `0.3074R` is calculated from the real terminal/source candle high `718.11` minus entry `715.82`, using chart risk `7.45`
- **MAE validation result:** PASS; MAE `0.0` points, `0.0%`, `0.0R` is calculated from the real terminal/source candle low `715.82` versus entry `715.82`, using no candles after terminal condition
- **Chart-only boundary:** preserved
- **Option P&L modeled:** no
- **Account sizing added:** no
- **Watcher work started:** no
- **`main.py` changed:** no
- **Schemas changed:** no
- **Fixtures changed:** no
- **Calculation code changed:** no
- **Historical replay runner changed:** no

## Validation Commands

- **Chart fixture validation result:** PASS; `python -B chart_trade_outcome_backtesting/validate_chart_outcome_fixtures.py`
- **Chart runner result:** PASS; `python -B chart_trade_outcome_backtesting/run_chart_outcome_backtest.py`
- **Output JSON parse result:** PASS; `python -m json.tool chart_trade_outcome_backtesting/reports/first_spy_continuation_chart_outcome_result_v1.json`
- **Historical signal replay result:** PASS; `python -B historical_signal_replay/run_signal_replay.py`
- **Contract tests result:** PASS; all 35 `replay/test_on_demand_*contract.py` files passed locally
- **Stage-message result:** PASS; `python -B replay/test_on_demand_stage_messages.py`
- **Fixture validation result:** PASS; `python -B replay/validate_fixtures.py`
- **Full replay result:** PASS; `python -B replay/run_replay.py` returned `16/16 passed`, `local_fixture_engine=16`, `placeholder_scaffold=0`

## Boundary Checks

- **Chart-only boundary preserved:** yes
- **Real source rows only:** yes
- **No option P&L:** yes
- **No account sizing:** yes
- **No watcher work:** yes
- **No `main.py` changes:** yes
- **No schema changes:** yes
- **No fixture changes:** yes
- **No historical replay runner changes:** yes

## Recommended Next Task

Create a bounded next-step decision review for chart-based trade outcome backtesting v1 after the first real calculation output validation, without modeling option P&L, adding account sizing, starting watcher work, changing `main.py`, changing schemas or fixtures, changing historical replay runners, auto-trading, live reads, or live trade decisions.
