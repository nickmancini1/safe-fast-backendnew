# SAFE-FAST Day 45 CFB Backtest-Prep Readiness Review

## Direct Answer

`SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` is the first Clean Fast Break backtest-prep reference, but not a backtest-ready or proof-ready candidate yet.

The first grouped trade-rule package accepts enough conservative gates to build a checker and tests: setup-time-safe entry eligibility, selected-contract/no-fallback use, long-call ask entry basis, post-signal quote rejection, stale-quote rejection, and named failure diagnosis. It does not accept enough exit, stop, time-exit, cost/slippage, sample-size, or promotion detail to count a result.

## First Reference

- First backtest-prep reference: `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`.
- Reason: lifecycle evidence passes; starter selected contract is `SPY   260427C00685000`; option context is `clean`; execution context is `clean`; selected quote age is about `55.485181` seconds; long-call entry ask basis can use ask `6.35` for regression work.

## Repair References

- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`: repair/no-trade reference because the top-ranked starter quote/trade row is after the setup boundary. Under the first package, this is `quote_after_signal` and no fallback is allowed.
- `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`: repair/failed-execution reference because selected quote age is about `23m 29.359699s`, producing `quote_age_above_5_minutes`.

## Accepted Trade Rules

- Entry eligibility uses setup-time-safe data only.
- Selected/top-ranked contract must be used; no fallback contract is allowed after a gate failure.
- Long-call entry fill basis is ask price for first regression work.
- Quotes after setup/signal are rejected.
- Selected quotes older than five minutes are rejected for execution eligibility.
- Failure and no-trade cases require named diagnosis labels.

## Decisions Still Needed

- Exact entry timing after setup.
- Exit rule and option exit fill basis.
- Stop/invalidation translation from underlying invalidation to option exit.
- Time exit, end-of-day handling, maximum hold, and expiration-proximity handling.
- Cost and slippage numeric assumptions.
- Sample-size thresholds by setup family, symbol, pass/fail, and no-trade category.
- Promotion criteria from reconsideration-eligible to intake-ready and later stages.

## First CFB Backtest Batch Blockers

- No accepted exit rule.
- No accepted stop/invalidation-to-option-exit rule.
- No accepted time-exit rule.
- No accepted cost/slippage assumptions.
- No accepted sample-size gate.
- No accepted promotion gate.
- Headline/no-headline policy remains unresolved, so complete caution can remain blocker-preserving even when starter option/execution context is clean.

## Data Need

More data is deferred now.

The current starter data is enough to define the grouped rule package and build checker fixtures. Full-window Databento should wait until the checker and missing-rule decisions specify exact fields/windows, then a cost check and user approval are required before any download.

## Guardrails

- Backtest authorized: NO.
- Trade chosen: NO.
- P&L calculated: NO.
- Proof accepted: NO.
- Profitability claimed: NO.
- Candidate marked ready: NO.
- Intake-ready count changed: NO.

