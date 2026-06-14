# SAFE-FAST Day 41 QQQ CFB Lifecycle Regression Fixtures Review

## Scope

Candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Symbol/setup: QQQ / Clean Fast Break.

Baseline: `cec29a7 Accept QQQ CFB stale spent expiry rule`.

This review covers data-only lifecycle regression fixtures. It does not create calculator logic, fill evidence, backtest, choose a trade, calculate P&L, mark QQQ ready, accept proof, or claim profitability.

## Created Fixture File

Path: `historical_signal_replay/fixtures/qqq_cfb_lifecycle_regression_fixtures.json`.

The fixture file records regression cases for the accepted first QQQ Clean Fast Break lifecycle decision in `SAFE_FAST_DAY41_QQQ_CFB_STALE_SPENT_EXPIRY_DECISION.md`.

## Coverage

The fixture set covers:

- fresh target initial break at `2026-04-13T12:30:00-04:00`;
- spent same-session follow-through at `2026-04-13T15:30:00-04:00`;
- stale higher-base watch at `2026-04-16T13:30:00-04:00`;
- spent prior-completed-break/no-fresh-trigger context at `2026-04-17T15:30:00-04:00`;
- exact-boundary fresh versus later expired review;
- expired later review without spent evidence;
- unknown missing trigger, missing invalidation, missing timestamp/stage/prior-state/row-ordering, wrong symbol, and wrong setup type;
- future replay-row rejection;
- future candle rejection;
- option, fill, P&L, profitability, and readiness ignored for lifecycle state;
- higher-base refresh allowed only with new source-backed trigger, invalidation, and completed breakout;
- higher-base refresh rejected when required new trigger-path metadata is missing;
- state precedence where spent wins over expired and unknown wins over otherwise fresh/spent-looking contexts.

Every fixture includes:

- `fixture_id`;
- `setup_type`;
- `signal_time`;
- `source_time`;
- `candle_start`;
- `candle_end`;
- `candidate_state_inputs`;
- `expected_lifecycle_status`;
- `expected_as_of`;
- `expected_reviewed_before_signal`;
- `expected_rejection_reason`;
- `reason`.

## Validation

JSON parse validation: PASS.

Required-field validation: PASS.

Safe-check runner: PASS.

## Current Result

Lifecycle regression fixture rows added: YES.

Lifecycle calculator created: NO.

Evidence filled: NO.

Backtest authorized: NO.

Trade chosen: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Intake-ready count changed: NO.

Proof accepted: NO.

Profitability claimed: NO.
