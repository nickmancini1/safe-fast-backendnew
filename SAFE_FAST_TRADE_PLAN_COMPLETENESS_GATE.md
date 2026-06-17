# SAFE-FAST Trade Plan Completeness Gate

## Rule

A SAFE-FAST result cannot count as a trade-plan result unless the setup has a complete, fixed trade plan before the outcome is judged.

This gate is project-wide. It is not QQQ-only and it is not limited to Clean Fast Break.

Day 60 is a progress checkpoint, not a forced finish. The next $200 month is the final high-intensity build sprint before moving toward the $20 tier, but the calendar does not weaken this gate. Weak, failed, missing, unclear, or unprofitable results trigger diagnosis and repair, not forced passes.

## Required Fields

Every countable trade-plan result must define:

- exact option contract selection rule
- side
- expiration
- strike
- entry timing
- fill assumption
- bid/ask/mid/spread rule
- volume, open-interest, and liquidity minimums
- exit rule
- stop or invalidation rule
- time exit or end-of-day rule if applicable
- cost and slippage assumptions
- failure conditions

The final sprint should define these fields in grouped rule packages where possible: entry, exit, stop/invalidation, cost/slippage, failure diagnosis, and comparison across candidate families.

## Counting Rule

Do not count:

- a chart-only result as trade proof
- a setup-recognition result as profitability
- a raw vendor-data validation as execution proof
- a favorable move after signal as a win unless entry, exit, fill, spread, cost, invalidation, and failure rules were fixed first
- an option quote as a fill
- a structurally valid data file as a completed SAFE-FAST evidence row

## Missing Items

If any required field is missing, the result is blocked from trade-plan counting.

The correct next action is to identify the missing field and either source it, define the rule with regression protection, narrow the setup path, replace the path, or document the blocker. The whole project is not called dead because one item is missing.

## Current Known Gaps

- Trade-plan readiness still needs grouped work across candidate families.
- Exact entry and exit rules are not accepted project-wide.
- Stale/spent rules still need setup-specific validation.
- Stage-transition rules need project-wide indexing and validation.
- Sample-size requirements are not accepted.
- Promotion gates need to be enforced before intake-ready status.
- Full-window Databento data requires exact cost check and user approval before download; the known SPY 3-candidate full-window warning cost was about `$72.36`.
- A final decision package is required before moving toward the $20 tier.

Proof accepted: NO.

Profitability claimed: NO.
