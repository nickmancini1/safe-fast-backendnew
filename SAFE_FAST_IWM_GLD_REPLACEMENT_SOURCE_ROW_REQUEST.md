# SAFE-FAST IWM/GLD Replacement Source Row Request

Project day: Day 36 working day
Repo baseline: patch8
Latest committed baseline before this request: 7e69635 Add IWM GLD replacement source collection worksheet
Mode: build-only; not live trade chat

## Purpose

This docs-only request defines the exact local source rows needed to populate the replacement source collection worksheet.

This is not live data.
This is not broker work.
This is not a generated report.
This is not a trade decision.
This is not option P&L.
This is not account sizing.
This is not production or Railway work.

## Current blocker

The current repo does not provide accepted setup-time proof for:

- IWM Continuation
- GLD Ideal

The existing IWM Continuation 001 and GLD Ideal 001 candidates are blocked because they lack accepted setup-time signal rows, accepted numeric trigger, accepted invalidation, accepted freshness/final-signal, accepted blocker/caution status, and terminal outcome eligibility.

## Source rows needed

Populate these four replacement candidate slots:

| Candidate ID | Symbol | Setup type | Required source |
| --- | --- | --- | --- |
| IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001 | IWM | Continuation | local historical 1H RTH source rows |
| IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002 | IWM | Continuation | local historical 1H RTH source rows |
| GLD-REPLACEMENT-IDEAL-CANDIDATE-001 | GLD | Ideal | local historical 1H RTH source rows |
| GLD-REPLACEMENT-IDEAL-CANDIDATE-002 | GLD | Ideal | local historical 1H RTH source rows |

## Required fields for each candidate

Each candidate source row packet must include:

- candidate ID
- symbol
- setup type
- timeframe
- source file path or source export name
- source row number or row range
- source window start timestamp
- source window end timestamp
- setup-time candidate row timestamp
- setup-time candidate row OHLCV
- trigger candidate
- trigger basis
- invalidation candidate
- invalidation basis
- freshness/final-signal candidate
- blocker/caution status
- unavailable fields
- no-hindsight boundary statement
- after-setup outcome window start
- after-setup outcome window end

## Acceptance requirements

The next worksheet may not use after-setup movement to choose the setup-time row.

The setup-time row must be selected first.

A candidate can proceed to acceptance review only if it can support:

- exact setup-time signal timestamp
- accepted setup identity or rejected setup identity
- accepted final verdict or rejected verdict
- accepted trigger state
- accepted numeric trigger
- accepted trigger basis
- accepted numeric invalidation
- accepted invalidation basis
- accepted freshness/final-signal decision
- accepted blocker/caution decision

If those fields are unavailable, the candidate stays missing-evidence/inconclusive.

## Local source request

Find or provide local historical 1H RTH rows for:

### IWM Continuation replacement candidate 001

Need a cleaner IWM Continuation candidate than IWM Continuation 001.

Required characteristics:

- Continuation setup candidate
- clear setup-time row
- clear trigger candidate
- clear invalidation candidate
- clear freshness/final-signal candidate
- clear blocker/caution status
- minimal session-boundary ambiguity
- minimal winner-selection ambiguity
- enough after-setup window to measure terminal outcome later

### IWM Continuation replacement candidate 002

Need a second IWM Continuation candidate, preferably from a different date/window than candidate 001.

Same requirements as candidate 001.

### GLD Ideal replacement candidate 001

Need a cleaner GLD Ideal candidate than GLD Ideal 001.

Required characteristics:

- Ideal setup candidate
- clear setup-time row
- clear trigger candidate
- clear invalidation candidate
- clear freshness/final-signal candidate
- clear blocker/caution status
- minimal completed-candle-hold ambiguity
- enough after-setup window to measure terminal outcome later

### GLD Ideal replacement candidate 002

Need a second GLD Ideal candidate, preferably from a different date/window than candidate 001.

Same requirements as candidate 001.

## Source quality rules

Do not use:

- live data
- broker/order/account data
- option P&L
- account sizing data
- after-setup movement to choose the setup-time row
- generated reports/logs
- production/Railway output
- screenshots without source rows
- memory or guesses without repo/local source reference

Allowed:

- existing repo source CSV references
- existing local historical exports
- manually provided local source row packets
- docs-only source row references
- bounded historical windows with source row numbers

## Output required from next task

Create:

SAFE_FAST_IWM_GLD_REPLACEMENT_SOURCE_ROW_PACKET.md

That packet must populate the four candidate IDs or explicitly mark them unavailable.

Each candidate must be classified as:

- ready for acceptance review
- missing-evidence/inconclusive
- rejected as not clean enough
- blocked by unavailable source fields

## Smallest next evidence-backed fix

Create `SAFE_FAST_IWM_GLD_REPLACEMENT_SOURCE_ROW_PACKET.md`.

That packet is the first real source-population step after the current docs-only request.

## Tests

Tests not run. Docs-only source row request.

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
