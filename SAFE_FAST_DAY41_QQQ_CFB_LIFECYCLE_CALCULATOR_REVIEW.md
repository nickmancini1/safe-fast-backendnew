# SAFE-FAST Day 41 QQQ CFB Lifecycle Calculator Review

## Scope

Candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Symbol/setup: QQQ / Clean Fast Break.

Baseline: `3a26ca8 Add QQQ CFB lifecycle regression fixtures`.

This review covers the focused QQQ Clean Fast Break lifecycle calculator and tests. It does not fill evidence, backtest, choose a trade, calculate P&L, mark QQQ ready, accept proof, or claim profitability.

## Created

- Calculator: `historical_signal_replay/cfb_lifecycle_calculator.py`.
- Tests: `tests/test_cfb_lifecycle_calculator.py`.

## Calculator Behavior

The calculator classifies the accepted first QQQ Clean Fast Break lifecycle states:

- `fresh`;
- `stale`;
- `spent`;
- `expired`;
- `unknown`.

It preserves:

- `lifecycle_as_of`;
- `reviewed_before_signal`;
- explicit `rejection_reason`;
- ignored future/forbidden input metadata.

It applies the accepted state precedence:

1. `unknown`;
2. `spent`;
3. `fresh`;
4. `expired`;
5. `stale`.

It treats missing required data, wrong symbol, wrong setup type, missing timestamps, missing stage, missing trigger state, missing prior-state marker, missing trigger, missing invalidation, missing lifecycle rule metadata, or missing source-backed row ordering as `unknown`.

It rejects future replay rows, future candles, option context, fills, P&L, profitability, and readiness as setup-time lifecycle inputs and does not let them alter the lifecycle state.

It handles higher-base refresh as fresh only when a new source-backed higher-base trigger, invalidation, and completed breakout are present at the decision timestamp. Missing new trigger metadata remains stale with an explicit rejection reason.

## Fixture Coverage

The test file uses `historical_signal_replay/fixtures/qqq_cfb_lifecycle_regression_fixtures.json` and proves all 18 fixtures pass.

Covered cases include:

- fresh target initial break;
- spent same-session follow-through;
- stale higher-base watch;
- spent prior-completed-break/no-fresh-trigger;
- exact-boundary fresh versus later expired review;
- missing-data unknowns;
- wrong-symbol and wrong-setup unknowns;
- future replay-row rejection;
- future candle rejection;
- option/fill/P&L/profitability/readiness ignored;
- higher-base refresh allowed and rejected;
- spent-over-expired and unknown-over-fresh/spent precedence.

## Current Result

Lifecycle calculator created: YES.

Tests created: YES.

Lifecycle evidence filled: NO.

Backtest authorized: NO.

Trade chosen: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Intake-ready count changed: NO.

Proof accepted: NO.

Profitability claimed: NO.
