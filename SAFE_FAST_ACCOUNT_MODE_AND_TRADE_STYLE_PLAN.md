# SAFE-FAST Account Mode and Trade Style Plan

## Purpose

SAFE-FAST is not a generic day-trading system and not a loose swing-trading system.

SAFE-FAST should become a personal trading operating system that:
- identifies one of the 3 allowed setup types
- identifies the setup stage
- protects a small account while proving edge
- classifies whether a setup is suitable for same-day, fast swing, overnight, watch-only, or no trade
- uses planned invalidation risk, not just full debit exposure
- keeps strict no-trade discipline

## Current Account

Current account size: $1,500.

The account should be treated as proof-mode capital until the system proves repeatability.

## Core System Identity

Keep the original SAFE-FAST identity:

- Few, high-quality trades
- Universe: SPY, QQQ, IWM, GLD only
- Setup types: Ideal, Clean Fast Break, Continuation only
- Defined-risk debit verticals
- 14-30 DTE
- $5-$10 width
- $250-$300 preferred debit/risk band
- Hard max $400 exposure
- 1H + 24H context
- 1H 50 EMA is primary invalidation reference
- Default target: 40%-60% on spread
- 70% only if structure remains clean and room still exists
- Max 1 open trade
- No chasing late moves
- No trading without room
- No holding past invalidation

## Risk Model

SAFE-FAST should distinguish:

1. Max theoretical debit exposure
   - the full debit paid for the spread

2. Planned invalidation risk
   - estimated loss if exited at the SAFE-FAST invalidation level

3. Gap/headline risk
   - extra risk if price gaps, liquidity widens, or headlines move the market before exit

The system should not assume the full debit is the planned risk.
But the system must still surface full debit exposure and gap/headline risk.

## Account Modes

### PROOF_MODE

Used while account is small and edge is still being proven.

Goal:
- protect account
- prove setup recognition
- prove stage correctness
- avoid large drawdowns
- collect clean trade data

Rules:
- one trade at a time
- use settled cash only
- prefer fast setups
- avoid slow multi-day holds unless structure is unusually clean
- no capital additions until proof criteria are met
- planned risk must be controlled by invalidation
- full debit exposure must be visible

Allowed trade styles:
- WATCH_ONLY
- SAME_DAY_ONLY
- FAST_SWING_ALLOWED
- NO_TRADE

Overnight is rare and must require very clean structure.

### GROWTH_MODE

Used only after proof-mode evidence is strong.

Goal:
- add capital after evidence
- allow more flexibility
- still avoid reckless size increases

Rules:
- strict setup quality remains
- overnight allowed only when structure, room, macro, and 24H context justify it
- partial exits may be considered if position size allows
- more capital does not mean more loose trades

Allowed trade styles:
- WATCH_ONLY
- SAME_DAY_ONLY
- FAST_SWING_ALLOWED
- OVERNIGHT_ALLOWED
- RETEST_ONLY
- NO_TRADE

### SCALING_MODE

Used only after repeatability is proven and account size supports better management.

Goal:
- scale trade management, not emotional risk

Rules:
- possible 2-contract entries on A+ setups
- take one contract off at first target
- runner only if structure remains clean
- no increasing trade count just because account is larger
- no margin-driven overreach without separate approval

Allowed trade styles:
- SAME_DAY_ONLY
- FAST_SWING_ALLOWED
- OVERNIGHT_ALLOWED
- PARTIAL_PLUS_RUNNER
- RETEST_ONLY
- WATCH_ONLY
- NO_TRADE

## Trade Style Definitions

### WATCH_ONLY

Setup may be forming, but action is not close enough or account-mode risk is not acceptable.

### SAME_DAY_ONLY

Setup may be valid, but overnight/headline/gap risk is not worth carrying.
Trade must either work quickly or be closed.

### FAST_SWING_ALLOWED

Setup is clean enough to hold briefly, usually 1-3 days, if invalidation remains intact.

### OVERNIGHT_ALLOWED

Only for clean setups with:
- supportive or acceptable 24H context
- clean 1H structure
- clear room
- no major event risk
- not extended
- valid invalidation

### RETEST_ONLY

Trigger or move already happened, but trade is only acceptable on controlled retest near the mapped level.

### PARTIAL_PLUS_RUNNER

Scaling-mode only. Take partial profit early and hold a runner only if structure remains clean.

### NO_TRADE

Hard failure or rule violation.

## Proof Criteria Before Adding Capital

Do not add capital until the system has evidence.

Suggested review threshold:
- 30-50 logged trades or valid skipped signals
- positive expectancy
- controlled drawdowns
- rule-following documented
- same-day vs overnight results reviewed
- clear evidence SAFE-FAST avoids bad trades
- no repeated emotional overrides

Capital add status:
- NOT_READY
- READY_TO_REVIEW
- APPROVED_TO_ADD

## Required Future Engine Fields

Future SAFE-FAST output should include:

- account_mode
- trade_style
- hold_permission
- max_theoretical_debit_exposure
- planned_invalidation_risk_estimate
- gap_headline_risk
- speed_to_profit
- overnight_permission
- capital_add_status
- exit_plan

## Build Rule

Do not add this logic to engine behavior until on-demand setup recognition and stage correctness are stable and protected by replay/contract tests.
