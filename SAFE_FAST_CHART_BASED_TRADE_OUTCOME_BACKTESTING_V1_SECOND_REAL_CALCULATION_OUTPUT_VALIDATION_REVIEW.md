# SAFE-FAST Chart-Based Trade Outcome Backtesting v1 Second Real Calculation Output Validation Review

## Review Status

- **Validation status:** PASS
- **Baseline:** patch8
- **Latest local commit before validation:** `0f0df18 Add second real chart outcome calculation`
- **Scope:** validate the second real chart-only SPY Ideal outcome calculation output.

This review validates only underlying-chart outcome calculation output. It does not model option P&L, add account sizing, start watcher work, alter `main.py`, alter schemas, alter fixtures, alter historical source data, alter historical replay reports, alter calculation code, or alter the historical replay runner.

## Output Validated

- **Input fixture:** `chart_trade_outcome_backtesting/fixtures/second_spy_ideal_chart_outcome_input_v1.json`
- **Expected output fixture:** `chart_trade_outcome_backtesting/fixtures/second_spy_ideal_chart_outcome_expected_output_v1.json`
- **Result report:** `chart_trade_outcome_backtesting/reports/second_spy_ideal_chart_outcome_result_v1.json`
- **Source CSV:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`
- **Source signal log:** `historical_signal_replay/reports/second_real_spy_ideal_replay_v1_signal_log.jsonl`

## Validation Findings

- **Runner execution result:** PASS; `python -B chart_trade_outcome_backtesting/run_chart_outcome_backtest.py`
- **Result report exists:** PASS; `chart_trade_outcome_backtesting/reports/second_spy_ideal_chart_outcome_result_v1.json`
- **Output schema validation result:** PASS; runner validated output schema and `python -m json.tool chart_trade_outcome_backtesting/reports/second_spy_ideal_chart_outcome_result_v1.json` parsed successfully.
- **Expected output comparison result:** PASS; result matches expected output excluding only the runner-written `notes` text.
- **Entry validation result:** PASS; entry timestamp `2026-05-13T12:30:00-04:00` and entry reference price `741.73` match the next eligible real SPY 1H RTH source row after source signal timestamp `2026-05-13T11:30:00-04:00`.
- **Invalidation validation result:** PASS; invalidation `731.83` is copied from the eligible replay signal row, and real source lows through terminal follow-through did not touch or cross invalidation.
- **Follow-through/failure/time-stop validation result:** PASS; bullish follow-through threshold is predeclared at `2.0` favorable points, entry `741.73` plus threshold requires `743.73`, and the real `2026-05-13T13:30:00-04:00` high `743.9` reached follow-through before invalidation or time stop.
- **MFE validation result:** PASS; MFE `2.17` points / `0.2926%` / `0.2192R` is calculated from real source rows only through the first terminal candle.
- **MAE validation result:** PASS; MAE `0.35` points / `0.0472%` / `0.0354R` is calculated from real source rows only through the first terminal candle.

## Boundary Checks

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
- **Output JSON parse/schema validation result:** PASS; `python -m json.tool chart_trade_outcome_backtesting/reports/second_spy_ideal_chart_outcome_result_v1.json`
- **Historical signal replay result:** PASS; `python -B historical_signal_replay/run_signal_replay.py`
- **Contract tests result:** PASS; all 35 `replay/test_on_demand_*contract.py` files passed locally.
- **Stage-message result:** PASS; `python -B replay/test_on_demand_stage_messages.py`
- **Fixture validation result:** PASS; `python -B replay/validate_fixtures.py`
- **Full replay result:** PASS; `python -B replay/run_replay.py` returned `16/16 passed`, `local_fixture_engine=16`, `placeholder_scaffold=0`.

## Recommended Next Task

Create a bounded next-step decision review for chart-based trade outcome backtesting v1 after second real calculation output validation, without modeling option P&L, adding account sizing, starting watcher work, changing `main.py`, changing schemas or fixtures, changing historical replay runners, auto-trading, live reads, or live trade decisions.
