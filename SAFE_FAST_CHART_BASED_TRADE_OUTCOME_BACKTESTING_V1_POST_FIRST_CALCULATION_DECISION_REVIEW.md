# SAFE-FAST Chart-Based Trade Outcome Backtesting v1 Post-First-Calculation Decision Review

## Review Status

- **Post-first-calculation decision status:** PASS
- **Baseline:** patch8
- **Latest local commit reviewed:** `2324b9a Add first real chart outcome output validation`
- **Scope:** docs-only next-step decision review after validating the first real chart-only SPY Continuation outcome calculation.

This review does not implement new calculation, change `main.py`, change schemas, change fixtures, change runner code, model option P&L, add account sizing, start watcher work, auto-trade, use live reads, or make live trade decisions.

## Inputs Reviewed

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_FIRST_REAL_CALCULATION_REVIEW.md`
- `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_FIRST_REAL_CALCULATION_OUTPUT_VALIDATION_REVIEW.md`
- `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_CALCULATION_RULES_PLAN.md`
- `chart_trade_outcome_backtesting/reports/first_spy_continuation_chart_outcome_result_v1.json`
- `historical_signal_replay/reports/second_real_spy_ideal_replay_v1_signal_log.jsonl`
- `historical_signal_replay/reports/third_real_spy_clean_fast_break_replay_v1_signal_log.jsonl`

## Current Real Calculation Coverage

- **SPY Continuation:** real chart outcome calculation exists and output validation passed.
- **SPY Ideal:** real replay signal log contains an eligible `TRADE` row at `2026-05-13T11:30:00-04:00`, but no real chart outcome calculation exists yet.
- **SPY Clean Fast Break:** real replay signal log contains eligible `TRADE` rows at `2026-04-13T12:30:00-04:00` and `2026-04-15T14:30:00-04:00`, but no real chart outcome calculation exists yet.

## Options Compared

1. **Add second real chart outcome calculation for SPY Ideal**
   - Status: selected.
   - Reason: this is the next bounded calculation step and expands real chart outcome coverage from Continuation into a second setup family while preserving the existing chart-only v1 boundary.

2. **Add third real chart outcome calculation for SPY Clean Fast Break**
   - Status: rejected for this immediate next task.
   - Reason: Clean Fast Break also needs real chart outcome coverage, but it should follow the second-family Ideal calculation so setup-family expansion remains one bounded calculation at a time.

3. **Build aggregate chart outcome summary reporting**
   - Status: rejected for now.
   - Reason: aggregate reporting would be premature while only one setup family has a real chart outcome calculation. Summary reporting should wait until all three setup families have real calculation outputs.

4. **Move to watcher planning**
   - Status: rejected.
   - Reason: watcher planning is explicitly not the next step and should not start while chart outcome backtesting v1 has not yet covered all three setup families with real calculations.

## Decision

- **Decision status:** PASS
- **Chosen next step:** add second real chart outcome calculation for SPY Ideal.
- **Decision rule applied:** because all three setup families do not yet have real chart outcome calculations, choose the next bounded calculation step.
- **Reason:** first SPY Continuation output validation passed, but SPY Ideal and SPY Clean Fast Break still lack real chart outcome calculations. The next safest expansion is one additional bounded real calculation for the second setup family, SPY Ideal, before Clean Fast Break or any aggregate reporting.

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

Create the second real chart-only outcome calculation for the SPY Ideal sample, using the existing calculation rules plan as the source of truth, without modeling option P&L, adding account sizing, starting watcher work, changing `main.py`, changing schemas or fixtures without explicit authorization, auto-trading, live reads, or live trade decisions.
