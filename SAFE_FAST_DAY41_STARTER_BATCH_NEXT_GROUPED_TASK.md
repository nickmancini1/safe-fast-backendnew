# SAFE-FAST Day 41 Starter Batch Next Grouped Task

## Purpose

Avoid one-field grinding by grouping candidates by setup family and data readiness. The starter Databento files are present and inspectable for all six candidates, so the next useful step is setup-family rule/regression authorization, not another single evidence-field fill.

## Recommended Next Task

Create the SPY Clean Fast Break grouped rule/regression package for:

- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`

## Why This Group Comes First

- Both candidates share the Clean Fast Break family and SPY symbol.
- Both already have source/replay rows and existing partial work-package rows.
- Starter Databento files now exist for definitions, statistics, 10-minute quotes, and 10-minute trades.
- The two candidates cover different lifecycle shapes:
  - CFB 002: initial-break lifecycle.
  - CFB 003: higher-base fresh-break lifecycle.
- Grouping them can create one SPY CFB lifecycle/contract/context foundation instead of grinding one missing field at a time.

## Allowed Next-Task Shape

The next grouped task should:

1. Read build state, dashboard, rule index, starter inspection, and candidate packets.
2. Define SPY CFB lifecycle rule/regression requirements for initial break and higher-base fresh break.
3. Define what can be reused from QQQ CFB as structure only, and what cannot be reused without SPY-specific authorization.
4. Create data-only regression fixtures or a decision-needed document, depending on whether the rule is accepted.
5. Keep starter option inspection read-only and raw-field based until the SPY CFB rule package exists.
6. Update dashboard, rule index, build state, and candidate packets.
7. Run `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`.

## Explicit Non-Goals

- Do not download more data.
- Do not use full-window data.
- Do not fill evidence.
- Do not backtest.
- Do not choose a real option contract or trade.
- Do not calculate P&L.
- Do not claim proof, profitability, or readiness.
- Do not modify `main.py`, live/engine trading logic, broker/order/account code, Railway/deploy files, `.env`, secrets, raw Databento files, or generated live reports/logs.

## Later Grouped Tasks

### Ideal Group

- Candidates:
  - `SPY-REAL-HISTORICAL-IDEAL-001`
  - `QQQ-REAL-HISTORICAL-IDEAL-001`
- Start with Ideal lifecycle/gap/context and contract-selection rule decisions.
- Do not apply CFB lifecycle or contract-selection rules by assumption.

### Continuation Group

- Candidates:
  - `QQQ-REAL-HISTORICAL-CONTINUATION-001`
  - `SPY-REAL-HISTORICAL-CONTINUATION-001`
- Start by defining request-shaped evidence package requirements and Continuation lifecycle/contract-selection rules.
- These are replacement-path candidates and need a new setup-family rule/evidence path before processing.

## Stop Condition

Stop after the grouped rule/regression package or decision-needed artifact is created and project state is updated. Evidence fill and trade-plan proof must remain separate later tasks.
