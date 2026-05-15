# SAFE-FAST Chart-Based Trade Outcome Backtesting v1 Post-Three-Calculation Decision Review

## Review Status

- **Post-three-calculation decision status:** PASS
- **Baseline:** patch8
- **Latest local commit before decision:** `d4904a1 Add third real chart outcome output validation`
- **Scope:** docs-only next-step decision review after all three real SPY setup-family chart outcome calculations and output validations.

This review decides the next bounded chart-based trade outcome backtesting v1 step only. It does not implement new calculation, change `main.py`, change schemas, change fixtures, change runner code, model option P&L, add account sizing, start watcher work, auto-trade, use live reads, or make live trade decisions.

## Evidence Reviewed

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_FIRST_REAL_CALCULATION_OUTPUT_VALIDATION_REVIEW.md`
- `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_SECOND_REAL_CALCULATION_OUTPUT_VALIDATION_REVIEW.md`
- `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_THIRD_REAL_CALCULATION_OUTPUT_VALIDATION_REVIEW.md`
- `chart_trade_outcome_backtesting/reports/first_spy_continuation_chart_outcome_result_v1.json`
- `chart_trade_outcome_backtesting/reports/second_spy_ideal_chart_outcome_result_v1.json`
- `chart_trade_outcome_backtesting/reports/third_spy_clean_fast_break_chart_outcome_result_v1.json`
- `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_CALCULATION_RULES_PLAN.md`
- `SAFE_FAST_PROJECT_MASTER_HANDOFF.md`

## Current Validated Coverage

- **SPY Continuation:** validated real chart outcome calculation exists; terminal outcome is `follow_through`, same-day classification is `same_day`, MFE is `2.29` points / `0.3074R`, and MAE is `0.0` points / `0.0R`.
- **SPY Ideal:** validated real chart outcome calculation exists; terminal outcome is `follow_through`, same-day classification is `same_day`, MFE is `2.17` points / `0.2192R`, and MAE is `0.35` points / `0.0354R`.
- **SPY Clean Fast Break:** validated real chart outcome calculation exists; terminal outcome is `time_stop`, same-day classification is `time_stop_same_day`, MFE is `0.285` points / `0.0499R`, and MAE is `0.735` points / `0.1286R`.

All three outputs preserve the chart-only boundary. They do not model option P&L, account sizing, broker/order execution, live trade permission, or watcher state.

## Options Compared

1. **Build aggregate chart outcome summary reporting next**
   - **Decision:** choose next.
   - **Reason:** all three SPY setup-family chart-only outcome calculations have validated outputs, but there is no combined result summary yet. A bounded aggregate summary is the next step needed before expanding symbols, planning watcher work, or planning option/risk layers.

2. **Add broader symbol chart outcome coverage next**
   - **Decision:** reject for now.
   - **Reason:** broader symbol coverage should follow a combined summary of the already validated SPY Continuation, SPY Ideal, and SPY Clean Fast Break outcomes. Expanding symbols before summary reporting would add more outputs without first consolidating the completed setup-family evidence.

3. **Start Continuous Watcher MVP planning next**
   - **Decision:** reject.
   - **Reason:** watcher work should not start before validated chart outcome calculations are summarized. The current step remains chart-based outcome backtesting documentation and reporting, not watcher design or implementation.

4. **Start option/risk layer planning next**
   - **Decision:** reject.
   - **Reason:** option P&L, account sizing, debit exposure, and risk-layer planning should not start before the validated chart-only SPY outcome set has a combined result summary. The chart-only boundary remains active.

## Decision

- **Decision status:** PASS
- **Chosen next step:** build aggregate chart outcome summary reporting next.
- **Decision rule applied:** choose aggregate chart outcome summary reporting next because all three SPY setup-family chart-only outcome calculations are validated, but there is no combined result summary yet. Do not choose watcher, option/risk, or broader symbols before summarizing the validated SPY outcomes.
- **Reason:** SPY Continuation, SPY Ideal, and SPY Clean Fast Break now each have validated chart-only outcome outputs. A combined summary is needed to make the completed SPY setup-family evidence reviewable before any broader expansion.
- **Rejected alternatives:** add broader symbol chart outcome coverage next; start Continuous Watcher MVP planning next; start option/risk layer planning next.

## Boundary Checks

- **Real calculation implementation started:** no
- **Option P&L modeled:** no
- **Account sizing added:** no
- **Watcher work started:** no
- **`main.py` changed:** no
- **Schemas changed:** no
- **Fixtures changed:** no
- **Runner code changed:** no

## Validation To Run

- `python -B chart_trade_outcome_backtesting/validate_chart_outcome_fixtures.py`
- `python -B chart_trade_outcome_backtesting/run_chart_outcome_backtest.py`
- `python -B historical_signal_replay/run_signal_replay.py`
- all `replay/test_on_demand_*contract.py` files
- `python -B replay/test_on_demand_stage_messages.py`
- `python -B replay/validate_fixtures.py`
- `python -B replay/run_replay.py`

## Recommended Next Task

Create aggregate chart outcome summary reporting for the three validated SPY setup-family chart-only outputs, without implementing new calculations, modeling option P&L, adding account sizing, starting watcher work, changing `main.py`, changing schemas or fixtures, changing historical replay runners, auto-trading, live reads, or live trade decisions.
