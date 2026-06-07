# SAFE-FAST IWM/GLD Replacement Candidate Selection Review

Project day: Day 36 working day
Repo baseline: patch8
Latest committed baseline before this review: c80bd9e Add IWM Continuation trigger invalidation freshness acceptance review
Mode: build-only; not live trade chat

## Purpose

This docs-only review selects the next evidence path after the current IWM Continuation 001 and GLD Ideal 001 candidates both failed setup-time acceptance.

This review does not invent evidence, does not fake proof, does not use hindsight filling, and does not authorize live data, alerts, broker/order/account/options/P&L, account sizing, Railway, production, or live trade decisions.

## Current blocker

Both Day 36 missing pairs are blocked at setup-time acceptance.

- IWM Continuation 001 has no accepted setup-time signal row and no accepted trigger/invalidation/freshness proof.
- GLD Ideal 001 has no accepted setup-time signal row and no accepted trigger/invalidation/freshness proof.
- GLD Ideal 001 also failed setup-time row acceptance.
- Neither current candidate can be promoted to worked proof or failed proof.
- Neither current candidate supports profitability proof.

## Decision

Stop trying to promote the current IWM Continuation 001 and GLD Ideal 001 candidates unless explicitly requested later.

The next evidence-backed move is to select a cleaner replacement candidate.

## Replacement candidate requirement

A replacement candidate must have, or be able to support without hindsight:

- one exact setup-time signal timestamp
- one accepted setup identity
- one accepted final verdict or clearly rejected verdict
- one accepted trigger state
- one accepted numeric trigger
- one accepted trigger basis
- one accepted numeric invalidation
- one accepted invalidation basis
- one accepted freshness/final-signal decision
- one accepted blocker/caution decision
- terminal outcome eligibility only after setup-time evidence is frozen

If these fields cannot be established, the replacement candidate must stay missing-evidence/inconclusive.

## Selection target

Select a replacement candidate for GLD Ideal first.

Reason:

- GLD Ideal is one setup family only.
- The prior GLD window is smaller than the IWM Continuation chain.
- The prior GLD blocker is clear: no accepted setup-time row.
- A cleaner GLD Ideal replacement candidate should be faster to accept or reject than continuing to drill the existing IWM Continuation chain.
- IWM remains important, but the current IWM Continuation candidate has more session/freshness/winner-selection ambiguity.

## Rejected current candidates

### IWM Continuation 001

Rejected for promotion.

Reason:

- candidate/review chain exists
- no accepted setup-time signal row
- no accepted numeric trigger
- no accepted numeric invalidation
- no accepted freshness/final-signal
- unresolved blocker/caution status
- no terminal outcome eligibility before setup-time acceptance

Status: remains missing-evidence/inconclusive.

### GLD Ideal 001

Rejected for promotion.

Reason:

- candidate/review chain exists
- no accepted setup-time signal row
- no accepted numeric trigger
- no accepted numeric invalidation
- no accepted freshness/final-signal
- unresolved completed-candle-hold / setup-confirming uncertainty
- no terminal outcome eligibility before setup-time acceptance

Status: remains missing-evidence/inconclusive.

## Next worksheet to create

Create `SAFE_FAST_GLD_IDEAL_REPLACEMENT_CANDIDATE_SOURCE_SELECTION_WORKSHEET.md`.

That worksheet must search existing repo sources only and choose one of:

1. a cleaner GLD Ideal replacement candidate with enough setup-time fields to proceed;
2. no acceptable GLD Ideal replacement candidate exists in current repo sources;
3. GLD Ideal should stay blocked and IWM Continuation replacement search should become next.

## Acceptance rule for the next worksheet

The next worksheet may not use chart movement to choose a signal row.

The setup-time row must be selected before terminal outcome is considered.

If no setup-time row can be selected without hindsight, the worksheet must mark GLD Ideal replacement search as missing-evidence/inconclusive and name the next source gap.

## Tests

Tests not run. Docs-only replacement-candidate selection review.

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
