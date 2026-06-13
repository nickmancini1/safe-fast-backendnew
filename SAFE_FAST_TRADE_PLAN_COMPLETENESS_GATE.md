# SAFE-FAST Trade Plan Completeness Gate

## Rule

A SAFE-FAST result cannot count as a trade-plan result unless the setup has a complete, fixed trade plan before the outcome is judged.

This gate is project-wide. It is not QQQ-only and it is not limited to Clean Fast Break.

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

- QQQ gap thresholds are not accepted.
- Contract-selection rules are not accepted for the target candidate.
- Exact entry and exit rules are not accepted.
- Stale/spent rules still need setup-specific validation.
- Stage-transition rules need project-wide indexing and validation.
- Sample-size requirements are not accepted.
- Promotion gates need to be enforced before intake-ready status.
- Databento file validation is structural and does not yet prove SAFE-FAST field mapping.
- Option fields still need mapping into SAFE-FAST option, execution, caution, and trade-plan evidence fields.

Proof accepted: NO.

Profitability claimed: NO.
