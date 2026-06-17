# SAFE-FAST Day 45 CFB Backtest Gate Decision

## Direct Answer

`SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` cannot enter a countable backtest after this package.

It can remain the first Clean Fast Break backtest-prep reference because it has usable starter entry evidence, but countable testing is still blocked until the remaining human decisions are accepted and covered by regression tests.

## What Still Blocks SPY CFB 002

- No accepted option exit rule or exit fill basis.
- No accepted translation from underlying invalidation `678.45` to an option stop/exit.
- No accepted time exit, end-of-day handling, max-hold rule, or expiration-proximity rule.
- No accepted cost/slippage numeric assumptions.
- No accepted sample-size threshold.
- No accepted promotion criteria.
- Headline/no-headline policy remains unresolved, so complete caution remains blocker-preserving.

## Cheap Starter Data Use

Cheap starter data can still test the rule-gate package:

- selected-contract/no-fallback behavior;
- setup-time-safe quote handling;
- long-call ask entry basis presence;
- quote-after-signal rejection;
- stale quote rejection;
- named failure diagnosis;
- missing exit, stop, cost, sample-size, and promotion blockers.

Cheap starter data is not enough to count full trade outcomes because the exit path, stop path, time exit, and cost model are not accepted.

## Full-Window Data Decision

Full-window Databento is deferred now.

The next data step is not a download. The next step is to accept exact exit, stop, time, cost/slippage, sample-size, and promotion rules, then write regression tests. Only after those rules specify exact option fields and windows should a full-window cost check be run for user approval.

## Guardrails

- Backtest authorized: NO.
- P&L calculated: NO.
- Proof accepted: NO.
- Profitability claimed: NO.
- Candidate marked ready: NO.
- Intake-ready count changed: NO.
