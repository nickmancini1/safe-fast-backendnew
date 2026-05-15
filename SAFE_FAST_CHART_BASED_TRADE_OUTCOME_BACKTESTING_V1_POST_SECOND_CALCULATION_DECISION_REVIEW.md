# SAFE-FAST Chart-Based Trade Outcome Backtesting v1 Post-Second-Calculation Decision Review

## Review Status

- **Decision status:** PASS
- **Baseline:** patch8
- **Latest local commit before decision:** `988c9ee Add second real chart outcome output validation`
- **Scope:** docs-only next-step decision review after second real chart outcome calculation output validation.

This review decides the next bounded chart-based trade outcome backtesting v1 step only. It does not implement new calculation, change `main.py`, change schemas, change fixtures, change runner code, model option P&L, add account sizing, start watcher work, auto-trade, use live reads, or make live trade decisions.

## Evidence Reviewed

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_FIRST_REAL_CALCULATION_OUTPUT_VALIDATION_REVIEW.md`
- `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_SECOND_REAL_CALCULATION_OUTPUT_VALIDATION_REVIEW.md`
- `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_CALCULATION_RULES_PLAN.md`
- `chart_trade_outcome_backtesting/reports/first_spy_continuation_chart_outcome_result_v1.json`
- `chart_trade_outcome_backtesting/reports/second_spy_ideal_chart_outcome_result_v1.json`
- `historical_signal_replay/reports/third_real_spy_clean_fast_break_replay_v1_signal_log.jsonl`

## Current Validated Coverage

- **SPY Continuation:** validated real chart outcome calculation exists; first output validation review status is PASS.
- **SPY Ideal:** validated real chart outcome calculation exists; second output validation review status is PASS.
- **SPY Clean Fast Break:** real historical replay signal rows exist, including eligible `TRADE` rows with `current_state: signal`, `trigger_state: triggered`, no primary blocker, numeric trigger/invalidation, and selected setup type `Clean Fast Break`; chart outcome calculation does not yet exist.

## Options Compared

- **Option 1: Add third real chart outcome calculation for SPY Clean Fast Break.**
  - **Decision:** choose next.
  - **Reason:** Continuation and Ideal are validated, but Clean Fast Break does not yet have chart outcome calculation coverage. Adding the third setup-family calculation is the next bounded step before summary reporting or watcher planning.
- **Option 2: Build aggregate chart outcome summary reporting.**
  - **Decision:** reject for now.
  - **Reason:** aggregate reporting would summarize incomplete setup-family coverage because Clean Fast Break does not yet have a real chart outcome calculation.
- **Option 3: Move to watcher planning.**
  - **Decision:** reject for now.
  - **Reason:** watcher planning should not start until all three setup families have real chart outcome calculation coverage; this review explicitly preserves the no-watcher boundary.

## Decision

- **Chosen next step:** add third real chart outcome calculation for SPY Clean Fast Break.
- **Reason:** SPY Continuation and SPY Ideal calculations are validated, but SPY Clean Fast Break has eligible historical signal evidence without a corresponding chart outcome calculation. The next bounded v1 step is to add that third setup-family calculation using the existing calculation rules plan.
- **Rejected alternatives:** build aggregate chart outcome summary reporting; move to watcher planning.
- **Real calculation implementation started:** no
- **Option P&L modeled:** no
- **Account sizing added:** no
- **Watcher work started:** no
- **`main.py` changed:** no
- **Schemas changed:** no
- **Fixtures changed:** no
- **Runner code changed:** no

## Recommended Next Task

Create the third real chart-only outcome calculation for the SPY Clean Fast Break sample using the existing calculation rules plan as the source of truth, without modeling option P&L, adding account sizing, starting watcher work, changing `main.py`, changing schemas or fixtures without explicit authorization, changing runner code, changing historical replay runners, auto-trading, live reads, or live trade decisions.
