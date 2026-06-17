# SAFE-FAST Day 46 Next Grouped Backtest Batch Decision

## Decision

The next grouped work is a Clean Fast Break expansion and data-needed planning package, not a new backtest run.

Keep the current three Clean Fast Break anchors together:

- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`: positive review-only reference, `completed_profit_target`, adjusted result `+1.61`.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`: no-trade control, `quote_after_signal`.
- `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`: no-trade control, `quote_age_above_5_minutes`.

The first positive CFB result is useful, but it is still one example. It should be compared against more valid CFB examples before any sample, expectancy, proof, profitability, or promotion discussion.

## Setup-Family Routing

`SPY-REAL-HISTORICAL-IDEAL-001` is not ready enough to join a grouped backtest run. It has starter lifecycle and blocker-preserving context/caution evidence, but Ideal-specific gap/context thresholds, setup-time option/execution rules, entry, exit, stop, time-exit, cost, slippage, sample-size, and promotion rules are still incomplete.

`QQQ-REAL-HISTORICAL-IDEAL-001` remains parked behind a future grouped Ideal rule/evidence package. It has replay and starter option data, but no current richer work-package request and no accepted QQQ Ideal rule path.

Continuation candidates stay parked. `SPY-REAL-HISTORICAL-CONTINUATION-001` and `QQQ-REAL-HISTORICAL-CONTINUATION-001` have replay artifacts and starter option data, but no accepted Continuation lifecycle, request-shaped evidence, contract-selection, context, entry, exit, cost, slippage, sample-size, or promotion rules.

## Next Grouped Work

The next package should build a grouped CFB expansion/data-needed plan before any new backtest:

- identify additional CFB candidates or CFB-like candidates that can be evaluated under the existing CFB rule family;
- require setup-family-specific lifecycle rules before any candidate is added;
- require contract-selection, option context, execution context, entry, exit, stop, time-exit, cost, and slippage rules before any completed result is counted;
- preserve named no-trade/failure reasons, especially `quote_after_signal` and `quote_age_above_5_minutes`;
- preserve the minimum `20` valid completed CFB examples blocker before promotion;
- list exact missing local data and exact later cost-check needs before any Databento request.

## Current Blockers

- More completed valid CFB examples are needed; one positive SPY CFB reference is not representative.
- The current repo does not identify another ready completed CFB backtest row in this task.
- Ideal comparison is useful but not backtest-ready because Ideal-specific trade-plan rules are incomplete.
- Continuation comparison is not ready because Continuation-specific rule/evidence packages do not exist.
- Any additional full-window option data requires exact grouped cost check and user approval first.

## Guardrails Preserved

- Databento downloaded: NO.
- Raw Databento files changed: NO.
- New backtest run: NO.
- New P&L calculated: NO.
- Proof accepted: NO.
- Profitability claimed: NO.
- Candidate marked ready: NO.
- Intake-ready count changed: NO.
- `main.py`, live/engine trading logic, broker/order/account files, Railway/deploy files, `.env`, secrets, raw vendor data, and backtest code changed: NO.
