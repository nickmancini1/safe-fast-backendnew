# SAFE-FAST Candidate Factory

Purpose:
Build a repeatable path toward a profitable trading plan.

Candidate finding and backtesting are bottlenecks.
Candidate work must be a factory, not a random hunt.
Do not add a candidate-count target as repo fact unless a completed result establishes it.

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

Replay-ready candidates go directly to economics/P&L.
If SAFE-FAST is unprofitable, weak, missing evidence, or inconclusive, diagnose the exact cause and smallest evidence-backed fix.

Rules:
- no broad hunt while replaying
- no replay before raw data is confirmed
- no profitability claim from one trade
- no paper/live eligibility unless proven

## Tightening addendum

Candidate ledger rule:
Candidate work must track each candidate in one clear state:
- proposed
- evidence requested
- evidence present
- replayed
- killed
- blocked
- profitable result
- unprofitable result

Do not restart candidate discovery when a candidate is already in the ledger.
Do not replay a candidate until its SAFE-FAST rule reason and raw-data source are clear.
