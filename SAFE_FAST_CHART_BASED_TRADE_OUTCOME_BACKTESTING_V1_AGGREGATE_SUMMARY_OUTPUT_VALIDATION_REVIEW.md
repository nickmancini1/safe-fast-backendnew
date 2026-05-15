# SAFE-FAST Chart-Based Trade Outcome Backtesting v1 Aggregate Summary Output Validation Review

## Review Status

- **Aggregate summary output validation status:** PASS
- **Baseline:** patch8
- **Latest local commit before validation:** `6b566dd Add Codex workflow helper`
- **Summary report file:** `chart_trade_outcome_backtesting/reports/spy_three_setup_chart_outcome_summary_v1.json`
- **Summary script file:** `chart_trade_outcome_backtesting/summarize_chart_outcomes.py`
- **Scope:** validate the aggregate chart outcome summary report only.

This validation did not implement a new chart outcome calculation, scan OHLCV source rows for new outcomes, change `main.py`, change schemas, change fixtures, change historical replay runners, model option P&L, add account sizing, start watcher work, auto-trade, use live reads, or make live trade decisions.

## Inputs Read

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_AGGREGATE_SUMMARY_REVIEW.md`
- `chart_trade_outcome_backtesting/summarize_chart_outcomes.py`
- `chart_trade_outcome_backtesting/reports/spy_three_setup_chart_outcome_summary_v1.json`
- `chart_trade_outcome_backtesting/reports/first_spy_continuation_chart_outcome_result_v1.json`
- `chart_trade_outcome_backtesting/reports/second_spy_ideal_chart_outcome_result_v1.json`
- `chart_trade_outcome_backtesting/reports/third_spy_clean_fast_break_chart_outcome_result_v1.json`

## Output Validation

- **Summary report exists:** PASS
- **Summary JSON validation result:** PASS
- **Sample count validation result:** PASS; exactly 3 samples included
- **Setup-family validation result:** PASS; includes Continuation, Ideal, and Clean Fast Break
- **Follow-through/failure/time-stop validation result:** PASS; 2 follow-through, 0 failure/invalidated, 1 time stop
- **MFE validation result:** PASS; summary values match source result files
- **MAE validation result:** PASS; summary values match source result files

## Validated Aggregate Values

- **Samples included:** 3
- **Setup families included:** Continuation, Ideal, Clean Fast Break
- **Follow-through/failure/time-stop summary:** 2 follow-through, 0 failure/invalidated, 1 time stop
- **MFE summary:** average 1.5817 points / 0.2177% / 0.1922R; max 2.29 points / 0.3199% / 0.3074R
- **MAE summary:** average 0.3617 points / 0.0507% / 0.0547R; max 0.735 points / 0.105% / 0.1286R
- **By-family MFE values:** Continuation 2.29 points / 0.3199% / 0.3074R; Ideal 2.17 points / 0.2926% / 0.2192R; Clean Fast Break 0.285 points / 0.0407% / 0.0499R
- **By-family MAE values:** Continuation 0.0 points / 0.0% / 0.0R; Ideal 0.35 points / 0.0472% / 0.0354R; Clean Fast Break 0.735 points / 0.105% / 0.1286R

## Boundary Checks

- **Chart-only boundary:** preserved
- **Option P&L modeled:** no
- **Account sizing added:** no
- **Watcher work started:** no
- **Watcher output included:** no
- **Broker/order execution modeled:** no
- **`main.py` changed:** no
- **Schemas changed:** no
- **Fixtures changed:** no
- **Runner code changed:** no

## Validation

- **Chart fixture validation result:** PASS; `python -B chart_trade_outcome_backtesting/validate_chart_outcome_fixtures.py`
- **Chart runner result:** PASS; `python -B chart_trade_outcome_backtesting/run_chart_outcome_backtest.py`
- **Aggregate summary script result:** PASS; `python -B chart_trade_outcome_backtesting/summarize_chart_outcomes.py`
- **Summary JSON validation result:** PASS; `python -m json.tool chart_trade_outcome_backtesting/reports/spy_three_setup_chart_outcome_summary_v1.json`
- **Historical signal replay result:** PASS; `python -B historical_signal_replay/run_signal_replay.py`
- **Contract tests result:** PASS; all 35 `replay/test_on_demand_*contract.py` files passed locally
- **Stage-message result:** PASS; `python -B replay/test_on_demand_stage_messages.py`
- **Fixture validation result:** PASS; `python -B replay/validate_fixtures.py`
- **Full replay result:** PASS; `python -B replay/run_replay.py` returned `16/16 passed`, `local_fixture_engine=16`, `placeholder_scaffold=0`

## Recommended Next Task

Create a bounded next-step decision review after aggregate summary output validation, without implementing new calculations, modeling option P&L, adding account sizing, starting watcher work, changing `main.py`, changing schemas or fixtures, changing historical replay runners, auto-trading, live reads, or live trade decisions.
