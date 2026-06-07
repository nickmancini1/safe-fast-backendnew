# SAFE-FAST IWM/GLD Local Source Export Instruction

Project day: Day 36
Repo baseline: patch8
Current baseline commit: 6fe551e Add IWM GLD replacement source row readiness review
Mode: local evidence collection instruction only

## Purpose

This file defines the local source export instruction needed to collect bounded historical 1H RTH source rows for the four reserved IWM/GLD replacement candidates.

This is local evidence collection instruction only. It does not collect rows, export data, create proof, accept proof, or make a trade decision.

No live trading, broker/order/account data, options/P&L, alerts, production, Railway, secrets, live data fetch, generated reports/logs, account sizing, or live trade decisions are authorized.

## Reserved Candidate IDs

- `IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001`
- `IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002`
- `GLD-REPLACEMENT-IDEAL-CANDIDATE-001`
- `GLD-REPLACEMENT-IDEAL-CANDIDATE-002`

## Packet Acceptance Rule

Candidate stays missing-evidence/inconclusive if any accepted setup-time trigger, numeric trigger, invalidation, freshness/final-signal, blocker/caution, or terminal outcome proof is unavailable.

## Lower-Tier Handoff Rule

A future packet must explain what setup appeared, what happened after, evidence used, missing evidence, diagnosis, likely cause candidate, next fix path, regression needed, and lower-tier handoff summary.

## Future Validation Path

Once rows are supplied, use the existing replacement source row packet builder, validator, and readiness reviewer.

A complete packet can become `ready_for_acceptance_review`, but this instruction does not create accepted proof.

## Source Row Requirements

Each reserved candidate needs bounded historical 1H RTH rows from a local source. The setup-time row must be chosen before after-setup movement is reviewed. After-setup rows are only for the outcome window after setup-time evidence is frozen.

Unavailable fields must be explicit for every candidate. Do not fill missing trigger, invalidation, freshness/final-signal, blocker/caution, or outcome fields from memory, guesses, screenshots, or after-setup movement.

### IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001

- symbol: `IWM`
- setup_type: `Continuation`
- required timeframe: historical 1H RTH rows
- source-row need: local bounded IWM source rows with source/export name, row numbers or row range, timestamps, timezone/session metadata, and OHLCV
- setup-time row need: exact candidate setup-time row timestamp and OHLCV selected without after-setup hindsight
- trigger candidate need: explicit Continuation trigger candidate from setup-time evidence
- trigger basis need: source-backed basis for the trigger candidate, including numeric trigger if available
- invalidation candidate need: explicit invalidation candidate from setup-time evidence
- invalidation basis need: source-backed basis for invalidation, including numeric invalidation if available
- freshness/final-signal need: setup-time freshness or final-signal state
- blocker/caution need: blocker/caution status at setup time
- no-hindsight boundary need: statement that after-setup movement did not choose or alter the setup-time row, trigger, invalidation, freshness, or blocker status
- after-setup outcome window need: bounded rows after the frozen setup-time row for later terminal outcome review
- unavailable fields must be explicit
- watch_only=true
- no_trade_decision=true

### IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002

- symbol: `IWM`
- setup_type: `Continuation`
- required timeframe: historical 1H RTH rows
- source-row need: local bounded IWM source rows with source/export name, row numbers or row range, timestamps, timezone/session metadata, and OHLCV
- setup-time row need: exact candidate setup-time row timestamp and OHLCV selected without after-setup hindsight
- trigger candidate need: explicit Continuation trigger candidate from setup-time evidence
- trigger basis need: source-backed basis for the trigger candidate, including numeric trigger if available
- invalidation candidate need: explicit invalidation candidate from setup-time evidence
- invalidation basis need: source-backed basis for invalidation, including numeric invalidation if available
- freshness/final-signal need: setup-time freshness or final-signal state
- blocker/caution need: blocker/caution status at setup time
- no-hindsight boundary need: statement that after-setup movement did not choose or alter the setup-time row, trigger, invalidation, freshness, or blocker status
- after-setup outcome window need: bounded rows after the frozen setup-time row for later terminal outcome review
- unavailable fields must be explicit
- watch_only=true
- no_trade_decision=true

### GLD-REPLACEMENT-IDEAL-CANDIDATE-001

- symbol: `GLD`
- setup_type: `Ideal`
- required timeframe: historical 1H RTH rows
- source-row need: local bounded GLD source rows with source/export name, row numbers or row range, timestamps, timezone/session metadata, and OHLCV
- setup-time row need: exact candidate setup-time row timestamp and OHLCV selected without after-setup hindsight
- trigger candidate need: explicit Ideal trigger candidate from setup-time evidence
- trigger basis need: source-backed basis for the trigger candidate, including numeric trigger if available
- invalidation candidate need: explicit invalidation candidate from setup-time evidence
- invalidation basis need: source-backed basis for invalidation, including numeric invalidation if available
- freshness/final-signal need: setup-time freshness or final-signal state
- blocker/caution need: blocker/caution status at setup time
- no-hindsight boundary need: statement that after-setup movement did not choose or alter the setup-time row, trigger, invalidation, freshness, or blocker status
- after-setup outcome window need: bounded rows after the frozen setup-time row for later terminal outcome review
- unavailable fields must be explicit
- watch_only=true
- no_trade_decision=true

### GLD-REPLACEMENT-IDEAL-CANDIDATE-002

- symbol: `GLD`
- setup_type: `Ideal`
- required timeframe: historical 1H RTH rows
- source-row need: local bounded GLD source rows with source/export name, row numbers or row range, timestamps, timezone/session metadata, and OHLCV
- setup-time row need: exact candidate setup-time row timestamp and OHLCV selected without after-setup hindsight
- trigger candidate need: explicit Ideal trigger candidate from setup-time evidence
- trigger basis need: source-backed basis for the trigger candidate, including numeric trigger if available
- invalidation candidate need: explicit invalidation candidate from setup-time evidence
- invalidation basis need: source-backed basis for invalidation, including numeric invalidation if available
- freshness/final-signal need: setup-time freshness or final-signal state
- blocker/caution need: blocker/caution status at setup time
- no-hindsight boundary need: statement that after-setup movement did not choose or alter the setup-time row, trigger, invalidation, freshness, or blocker status
- after-setup outcome window need: bounded rows after the frozen setup-time row for later terminal outcome review
- unavailable fields must be explicit
- watch_only=true
- no_trade_decision=true

## No-Promotion Rule

This instruction does not create accepted proof. IWM Continuation and GLD Ideal remain missing-evidence/inconclusive until rows and accepted proof exist.
