# SAFE-FAST Chart-Based Trade Outcome Backtesting v1 Third Real Calculation Output Validation Review

## Review Status

- **Validation status:** PASS
- **Baseline:** patch8
- **Latest local commit before validation:** `a09c123 Add third real chart outcome calculation`
- **Scope:** validate third real chart-only SPY Clean Fast Break outcome calculation output.

This validation is chart-only. It verifies the already-created SPY Clean Fast Break calculation output against the documented v1 rules, expected output fixture, schema, replay signal row, and real SPY 1H RTH source rows. It does not model option P&L, add account sizing, start watcher work, change `main.py`, change schemas, change fixtures, change historical source data, or change calculation code.

## Source Artifacts

- **Build state:** `SAFE_FAST_BUILD_STATE.md`
- **Third calculation review:** `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_THIRD_REAL_CALCULATION_REVIEW.md`
- **Rules plan:** `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_CALCULATION_RULES_PLAN.md`
- **Calculation code:** `chart_trade_outcome_backtesting/chart_outcome_backtest.py`
- **Runner:** `chart_trade_outcome_backtesting/run_chart_outcome_backtest.py`
- **Input fixture:** `chart_trade_outcome_backtesting/fixtures/third_spy_clean_fast_break_chart_outcome_input_v1.json`
- **Expected output fixture:** `chart_trade_outcome_backtesting/fixtures/third_spy_clean_fast_break_chart_outcome_expected_output_v1.json`
- **Result report:** `chart_trade_outcome_backtesting/reports/third_spy_clean_fast_break_chart_outcome_result_v1.json`
- **Output schema:** `chart_trade_outcome_backtesting/schemas/chart_outcome_backtest_output_v1.schema.json`
- **SPY source rows:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`
- **Replay signal log:** `historical_signal_replay/reports/third_real_spy_clean_fast_break_replay_v1_signal_log.jsonl`

## Validation Findings

- **Runner execution result:** PASS; `python -B chart_trade_outcome_backtesting/run_chart_outcome_backtest.py` completed successfully and reported `option_pnl_modeled: false`, `account_sizing_added: false`, and `watcher_implementation_started: false`.
- **Result report exists:** PASS; `chart_trade_outcome_backtesting/reports/third_spy_clean_fast_break_chart_outcome_result_v1.json` exists and parsed with `python -m json.tool`.
- **Output schema validation result:** PASS; the runner validated the generated result against `chart_outcome_backtest_output_v1.schema.json`.
- **Expected output comparison result:** PASS; actual result matches `third_spy_clean_fast_break_chart_outcome_expected_output_v1.json` excluding only runner-written `notes`.
- **Entry validation result:** PASS; entry timestamp `2026-04-15T15:30:00-04:00` and entry reference price `699.995` are sourced from the next eligible real SPY 1H RTH source row after source signal timestamp `2026-04-15T14:30:00-04:00`.
- **Invalidation validation result:** PASS; invalidation `694.2801` is copied from the eligible replay signal row, and the real terminal candle low `699.26` did not touch or cross invalidation before the same-day time stop.
- **Follow-through/failure/time-stop validation result:** PASS; bullish follow-through required entry `699.995` plus predeclared `2.0` favorable points, or `701.995`; the real terminal candle high `700.28` did not reach follow-through, invalidation was not reached, and the predeclared one-candle same-day time stop applied at the `2026-04-15T15:30:00-04:00` close `699.84`.
- **MFE validation result:** PASS; MFE `0.285` points / `0.0407%` / `0.0499R` is calculated from the real `2026-04-15T15:30:00-04:00` source row high `700.28` only, through the first terminal candle.
- **MAE validation result:** PASS; MAE `0.735` points / `0.105%` / `0.1286R` is calculated from the real `2026-04-15T15:30:00-04:00` source row low `699.26` only, through the first terminal candle.
- **Chart-only boundary:** preserved; result contains chart outcome fields only and keeps unavailable headline, option-chain, account, and broker context unavailable by design.
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
- **Output JSON parse/schema validation result:** PASS; runner validated output schema and `python -m json.tool chart_trade_outcome_backtesting/reports/third_spy_clean_fast_break_chart_outcome_result_v1.json` parsed successfully
- **Expected output comparison result:** PASS; actual result matches expected output excluding only runner-written `notes`
- **Historical signal replay result:** PASS; `python -B historical_signal_replay/run_signal_replay.py`
- **Contract tests result:** PASS; all `replay/test_on_demand_*contract.py` files passed locally
- **Stage-message result:** PASS; `python -B replay/test_on_demand_stage_messages.py`
- **Fixture validation result:** PASS; `python -B replay/validate_fixtures.py`
- **Full replay result:** PASS; `python -B replay/run_replay.py` returned `16/16 passed`, `local_fixture_engine=16`, `placeholder_scaffold=0`

## Recommended Next Task

Create a bounded next-step decision review for chart-based trade outcome backtesting v1 after all three real setup-family calculations have been validated, without modeling option P&L, adding account sizing, starting watcher work, changing `main.py`, changing schemas or fixtures, changing historical replay runners, auto-trading, live reads, or live trade decisions.
