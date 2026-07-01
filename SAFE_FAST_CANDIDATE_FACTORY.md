# SAFE-FAST Candidate Factory

Purpose:
Build a repeatable path toward a profitable trading plan.

Candidate finding and backtesting are bottlenecks.
Candidate work must be a factory, not a random hunt.

A candidate is not replay-ready just because it looks interesting.

Before replay, a candidate must have:
- date
- ticker
- setup type
- exact SAFE-FAST rule reason
- market context
- contract or contract-selection rule
- raw-data source
- schemas
- time windows
- cost/approval state
- destination
- expected replay output
- exact kill condition

Separate broad observation from SAFE-FAST translation.

SAFE-FAST translation means:
Does the broad market information become an Ideal, Clean Fast Break, or Continuation setup under exact SAFE-FAST rules?

Candidate path:
candidate -> raw evidence -> replay -> entry/exit/P&L -> exact result -> tests -> commit -> clean status

Rules:
- no broad hunt while replaying
- no replay before raw data is confirmed
- no profitability claim from one trade
- no paper/live eligibility unless proven
