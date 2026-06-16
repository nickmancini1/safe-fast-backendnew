# SAFE-FAST Day 41 SPY Batch Next Task

## One Grouped Task

Run one SPY Databento cost-check and source-availability preflight for:

- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`.
- Optional same pass: `SPY-REAL-HISTORICAL-IDEAL-001`.

## First Action

Read, in order:

1. `SAFE_FAST_BUILD_STATE.md`.
2. `SAFE_FAST_PROJECT_DASHBOARD.md`.
3. `SAFE_FAST_PROJECT_RULE_INDEX.md`.
4. `SAFE_FAST_DAY41_SPY_BATCH_PREFLIGHT.md`.
5. `SAFE_FAST_DAY41_SPY_BATCH_DATABENTO_COST_CHECK_PLAN.md`.
6. The three SPY candidate packets in `historical_signal_replay/candidate_packets/`.

## Goal

Produce a grouped SPY cost-check result and rule/data availability review. Do not split the work into three tiny candidate tasks.

## Allowed Work

- Check whether Databento `OPRA.PILLAR` can cost-estimate the requested SPY `definition`, `tcbbo`, `trades`, and `statistics` windows.
- Record the exact dataset, schemas, windows, symbol/parent/instrument filtering approach, and estimated cost if available.
- Record whether any matching SPY OPRA files are already local.
- Record which checks can be attempted immediately from local source/replay/work-package rows.
- Record which checks remain blocked until a later authorized pull.
- Update the dashboard, rule index, build state, and SPY candidate packets if needed.
- Run `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`.

## Not Allowed

- Do not download Databento data unless a new task explicitly authorizes it.
- Do not write raw vendor files.
- Do not fill evidence rows.
- Do not backtest.
- Do not calculate P&L.
- Do not choose a real trade.
- Do not mark any candidate ready.
- Do not claim proof or profitability.
- Do not modify `main.py`, live/engine trading logic, broker/order/account files, Railway/deploy files, `.env`, or secrets.

## Required Output Doc

Create:

- `SAFE_FAST_DAY41_SPY_BATCH_DATABENTO_COST_CHECK_RESULT.md`

The result must cover all three SPY candidates in one table and must explicitly say whether the next authorized step should be data download, rule/regression fixture work, or stopping because cost/source coverage is not acceptable.

## Required Stop Condition

Stop after the cost-check/result doc and safe-check run. Do not continue into evidence fill, selector application, or backtest.
