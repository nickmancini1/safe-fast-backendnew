# SAFE-FAST Chart-Based Trade Outcome Backtesting v1 Next-Step Decision Review

## Review Status

- **Next-step decision status:** PASS
- **Baseline:** patch8
- **Latest local commit reviewed:** `3367935 Add chart outcome runner output validation`
- **Scope:** docs-only decision review for the next bounded chart-based trade outcome backtesting v1 validation/planning step after runner scaffold output validation.

This review does not implement real outcome calculation, change `main.py`, change schemas, change fixtures, change runner code, model option P&L, add account sizing, start watcher work, auto-trade, use live reads, or make live trade decisions.

## Evidence Reviewed

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_PLAN.md`
- `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_SCHEMA_DESIGN.md`
- `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_RUNNER_SCAFFOLD_PLAN.md`
- `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_RUNNER_OUTPUT_VALIDATION_REVIEW.md`
- `chart_trade_outcome_backtesting/README.md`
- `chart_trade_outcome_backtesting/chart_outcome_backtest.py`
- `chart_trade_outcome_backtesting/run_chart_outcome_backtest.py`
- `chart_trade_outcome_backtesting/fixtures/`
- `chart_trade_outcome_backtesting/reports/`

## Current Proven State

- Runner scaffold output validation is complete and recorded as PASS.
- The runner scaffold validates the existing SPY Continuation sample fixture, expected output fixture, source artifact availability, and emitted scaffold report.
- The emitted report remains scaffold/sample only and copies the expected output fixture as a scaffold target.
- The existing sample uses a 2.0 point favorable touch threshold as sample/scaffold context only, not as a finalized real backtest rule.
- Real outcome calculation has not started.
- Option P&L is not modeled.
- Account sizing is not added.
- Watcher work is not started.

## Options Compared

### 1. Plan Real Chart Outcome Calculation Rules Next

Status: chosen.

This is the safest next bounded step because the scaffold output is validated, but the detailed real calculation rules are not yet finalized enough for implementation. A rules-planning step can define the exact deterministic behavior for entry timing, invalidation touch/close handling, follow-through thresholds, first-terminal-condition ordering, time stops, MFE/MAE measurement boundaries, same-day versus fast-swing classification, source-end handling, and no-hindsight audit checks before any runner logic changes.

### 2. Implement Minimal Real Chart Outcome Calculation Next

Status: rejected for now.

Implementation would be premature because the current artifacts still treat the expected output as scaffold/sample only. Implementing calculation now risks hard-coding sample assumptions such as the 2.0 point favorable touch threshold, next-candle entry policy, same-candle terminal handling, or terminal-condition priority before those rules are explicitly reviewed and accepted as real v1 methodology.

### 3. Add More Chart Outcome Sample Fixtures Next

Status: rejected for now.

Additional fixtures will be useful later, especially for Ideal, Clean Fast Break, no-entry, invalidation, time-stop, and unresolved cases. They are not the safest immediate step because more fixtures would likely repeat or expand unfinalized assumptions. Rule planning should come first so later fixture additions are built against stable expected behavior.

## Decision

- **Chosen next step:** plan real chart outcome calculation rules next.
- **Reason:** scaffold output is validated, but real outcome calculation is not yet designed in enough operational detail to implement safely or expand fixture coverage without locking in sample-only assumptions.
- **Rejected alternatives:** implement minimal real chart outcome calculation next; add more chart outcome sample fixtures next.
- **Decision status:** PASS

## Boundary Confirmation

- **Real outcome calculation started:** no
- **Option P&L modeled:** no
- **Account sizing added:** no
- **Watcher work started:** no
- **`main.py` changed:** no
- **Schemas changed:** no
- **Fixtures changed:** no
- **Runner code changed:** no

## Recommended Next Task

Create a docs-only real chart outcome calculation rules plan for v1, covering entry timing, invalidation, follow-through, failure, time-stop, first-terminal-condition ordering, MFE/MAE measurement, same-day versus fast-swing classification, unresolved/source-end handling, and no-hindsight audit behavior. Do not implement real outcome calculation, model option P&L, add account sizing, change `main.py`, change schemas or fixtures, change runner code, start watcher behavior, auto-trade, use live reads, or make live trade decisions.
