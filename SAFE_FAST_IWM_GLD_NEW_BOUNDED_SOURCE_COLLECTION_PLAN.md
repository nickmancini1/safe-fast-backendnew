# SAFE-FAST IWM/GLD New Bounded Source Collection Plan

Project day: Day 36 working day
Repo baseline: patch8
Latest committed baseline before this plan: d233511 Add IWM Continuation replacement candidate source selection worksheet
Mode: build-only; not live trade chat

## Purpose

This docs-only plan defines the next source collection task after both current Day 36 replacement paths failed.

The current repo does not provide a cleaner accepted setup-time candidate for:

- IWM Continuation
- GLD Ideal

The next move is to collect cleaner bounded real historical candidates with complete setup-time fields.

This plan does not invent evidence, does not fake proof, does not use hindsight filling, and does not authorize live data, alerts, broker/order/account/options/P&L, account sizing, Railway, production, or live trade decisions.

## Current blocker

Current blocked candidates:

- IWM Continuation 001
- GLD Ideal 001

Blocked reason:

- no accepted setup-time signal row
- no accepted numeric trigger
- no accepted numeric invalidation
- no accepted freshness/final-signal decision
- unresolved blocker/caution status
- no terminal outcome eligibility before setup-time acceptance

## Collection target

Collect replacement candidates for both missing Day 60 pairs:

1. IWM Continuation
2. GLD Ideal

The collection must prefer candidates that are easier to accept or reject from setup-time evidence.

## Candidate intake requirements

Each future candidate must include:

- symbol
- setup type
- candidate ID
- exact date
- exact source window start
- exact source window end
- timeframe
- data source
- source-as-of timestamp if available
- setup-time candidate row
- trigger candidate
- trigger basis
- invalidation candidate
- invalidation basis
- freshness/final-signal candidate
- blocker/caution status
- unavailable fields
- no-hindsight boundary
- after-setup outcome window only after setup-time row is frozen

## Required candidate IDs

Use these IDs for the next collection worksheet:

- IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001
- IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002
- GLD-REPLACEMENT-IDEAL-CANDIDATE-001
- GLD-REPLACEMENT-IDEAL-CANDIDATE-002

## Acceptance gate

A replacement candidate can proceed only if the setup-time row can answer:

- exact setup-time signal timestamp
- accepted setup identity
- accepted final verdict or rejected verdict
- accepted trigger state
- accepted numeric trigger
- accepted trigger basis
- accepted numeric invalidation
- accepted invalidation basis
- accepted freshness/final-signal decision
- accepted blocker/caution decision

If any of those fields are missing, the candidate must be marked missing-evidence/inconclusive.

## Outcome gate

Terminal outcome can be reviewed only after setup-time evidence is frozen.

No candidate may be selected because the chart moved afterward.

After-setup movement is allowed only to classify outcome after setup-time proof is accepted or rejected.

## Search priority

Preferred candidate shape:

- clean setup-time row
- clear trigger
- clear invalidation
- clear freshness/final-signal
- clear blocker/caution status
- minimal session-boundary ambiguity
- minimal winner-selection ambiguity
- enough after-setup window for terminal outcome review

Avoid candidates with:

- trigger only described as a zone
- invalidation only described as a broad area
- PENDING final verdict
- TO_REVIEW trigger state
- null trigger
- null invalidation
- unresolved completed-candle-hold question
- unresolved fresh/spent question
- unresolved primary blocker
- mixed setup identity

## Output file for next task

Create:

SAFE_FAST_IWM_GLD_REPLACEMENT_SOURCE_COLLECTION_WORKSHEET.md

That worksheet must list candidate rows using the intake requirements above.

## Smallest next build step

Create the replacement source collection worksheet.

The worksheet should not prove anything yet. It should collect candidate rows and mark each one:

- ready for acceptance review
- missing-evidence/inconclusive
- rejected as not clean enough
- blocked by unavailable source fields

## Tests

Tests not run. Docs-only source collection plan.

Required validation:

- git diff --check
- clean post-commit status

## No-go boundaries preserved

- no main.py
- no engine logic
- no replay code
- no live data
- no watcher loops
- no alerts
- no broker/order/account/options/P&L
- no account sizing
- no Railway/deploy/production
- no generated reports/logs
- no live trade decisions
