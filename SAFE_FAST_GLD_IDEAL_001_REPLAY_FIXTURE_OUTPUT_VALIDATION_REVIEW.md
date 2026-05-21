# SAFE-FAST GLD Ideal 001 Replay Fixture Output Validation Review

## Review Status

- Review status: PASS
- Baseline: patch8
- Repo: safe-fast-backendnew
- Branch: main
- Work mode: build work only, no live trade decisions

## Baseline Checked

- Current HEAD verified before edits: `0d2f0e4 Fix latest completed commit after GLD Ideal fixture asset`
- GLD Ideal 001 fixture asset exists: yes.
- GLD source CSV validation PASS: yes.
- GLD bounded source-window selection PASS: yes.
- GLD historical sample worksheet PASS: yes.
- GLD Ideal 001 replay readiness PASS: yes.
- GLD Ideal 001 real historical replay review PASS: yes.
- GLD Ideal 001 fixture specification PASS: yes.
- Closest existing fixture output validation pattern inspected: `SAFE_FAST_IWM_IDEAL_001_REPLAY_FIXTURE_OUTPUT_VALIDATION_REVIEW.md`
- GLD active target: yes; GLD remains the active broader coverage target.
- Continuous Watcher deferred: yes.
- News/headline context source status: no live headline/news source was fetched or read; headline/news context remains `NEWS_UNCONFIRMED`.

## Repo State Checked

- Git status result before edits: `## main...origin/main`
- Latest commits checked:
  - `0d2f0e4 Fix latest completed commit after GLD Ideal fixture asset`
  - `7640b1d Add GLD Ideal 001 replay fixture asset`
  - `d646c08 Fix latest completed commit after GLD Ideal fixture spec`
  - `d92b563 Add GLD Ideal 001 fixture specification review`
  - `6550d8a Fix latest completed commit after GLD Ideal replay review`
  - `9cd707c Add GLD Ideal 001 real historical replay review`
- Conflicts found: none. The worktree was clean before this docs/output-validation task.

## Fixture Checked

- Fixture path: `historical_signal_replay/fixtures/first_real_gld_ideal_replay_v1_fixture.json`
- Source CSV path: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv`
- Sample ID: `GLD-SAMPLE-IDEAL-001`
- Window ID: `GLD-WINDOW-IDEAL-001`
- Source window: `2026-05-04T09:30:00-04:00` to `2026-05-08T15:30:00-04:00`
- Source row range: rows 204-238
- Source row count: 35
- Fixture lifecycle row count: 6
- Setup type: `Ideal`
- Symbol: `GLD`
- Timeframe/session: `1h_rth`, `America/New_York`, `session_type=regular`, `regular_session=true`
- Source/vendor/as-of: `dxlink_candles.get_1h_ema50_snapshot`; `dxFeed via tastytrade dxLink`; `2026-05-20T16:25:45Z`

## Validation Performed

- PASS: `python -m json.tool historical_signal_replay\fixtures\first_real_gld_ideal_replay_v1_fixture.json > $null`
- PASS: `python -B replay\validate_fixtures.py`; result was `Fixture validation passed.`
- PASS: `python -m json.tool historical_signal_replay\schemas\signal_replay_input_v1.schema.json > $null`
- PASS: `python -m json.tool historical_signal_replay\schemas\signal_replay_output_v1.schema.json > $null`
- PASS: targeted Python validation using `historical_signal_replay.signal_replay.validate_lifecycle_fixture`
- PASS: targeted JSON Schema validation against `historical_signal_replay/schemas/signal_replay_input_v1.schema.json` and `historical_signal_replay/schemas/signal_replay_output_v1.schema.json`
- PASS: targeted source-window consistency check; each fixture lifecycle input is a cumulative prefix of GLD source rows 204-238 ending at the row timestamp, with OHLCV values matching the source CSV.
- PASS: source-window row count and span; rows 204-238 contain 35 GLD rows from `2026-05-04T09:30:00-04:00` through `2026-05-08T15:30:00-04:00`.
- PASS: GLD symbol preservation; fixture metadata, inputs, expected outputs, and winner-selection surface preserve `GLD`.
- PASS: Ideal identity preservation; expected output rows use `setup_type: Ideal` and winner-selection selected setup type `Ideal`.
- PASS: timeframe/session preservation; selected source rows and fixture metadata preserve `1h_rth`, `America/New_York`, and regular-session status.
- PASS: source metadata preservation; source, source-as-of, and data vendor match the validated GLD source CSV review.
- PASS: OHLCV validity; selected source rows have numeric OHLCV, high/low envelopes contain open and close, volume is non-negative, and fixture candle values match source rows exactly.
- PASS: trigger-card/unconfirmed-field handling; trigger, invalidation, room, extension, 24H/daily, macro, IV, event, and headline/news fields are kept `TO_REVIEW` / `UNCONFIRMED` where repo data does not prove exact values.
- PASS: news/headline handling; output surfaces preserve `NEWS_UNCONFIRMED`, and no headline/news blocker, caution, or clear status was invented.
- PASS: no option P&L/account sizing/live trade contamination; fixture purpose, boundary notes, and output rows remain signal/stage/lifecycle only and exclude option economics, account sizing, broker execution, auto-trading, production readiness, generated reports, chart outcomes, and live trade decisions.
- NOT RUN: broad `python -B replay\run_replay.py`; this GLD task was fixture-output validation only, and no broad replay/regression or generated replay report was required.
- PASS: generated reports status; no generated GLD replay reports were written.

## Output Summary

- Fixture lifecycle rows: 6
- Output setup count: `Ideal: 6`
- Output verdict count: `NO_TRADE: 3`, `PENDING: 3`
- Lifecycle row timestamps: `2026-05-04T15:30:00-04:00`, `2026-05-05T15:30:00-04:00`, `2026-05-06T09:30:00-04:00`, `2026-05-06T15:30:00-04:00`, `2026-05-07T10:30:00-04:00`, and `2026-05-08T15:30:00-04:00`
- Unconfirmed fields preserved: 24H/daily, macro, IV, event, trigger level, invalidation, room, extension, and headline/news context.

## Output Validation Result

PASS. The GLD Ideal 001 replay fixture output validates cleanly enough for the current phase and is sufficient to proceed to the GLD Clean Fast Break 001 replay readiness review or next GLD setup-family step.

## Fixture Corrections

No fixture changes were needed. The existing fixture JSON syntax, lifecycle shape, source-window references, cumulative candle inputs, GLD symbol, Ideal candidate identity, trigger-card surfaces, unconfirmed-field handling, and boundary exclusions validated without fixture correction.

## Replay Runner / Report Status

- Replay runner changed: no
- Generated reports created: no
- Generated report paths: none
- Reports tracked by repo convention: not applicable for this task; existing output-validation pattern supports targeted fixture validation without creating GLD generated replay reports.

## Next Task

Create GLD Clean Fast Break 001 replay readiness review, or continue with the next GLD setup-family step from the existing GLD worksheet pattern.

## Boundary Check

- main.py changed: no
- engine logic changed: no
- replay runner changed: no
- schemas changed: no
- fixtures changed: no
- reports changed: no
- Railway touched: no
- production touched: no
- Continuous Watcher implementation started: no
- option P&L modeled: no
- account sizing added: no
- auto-trading added: no
- live trade decisions added: no

## What Remains Unproven

- GLD Clean Fast Break readiness/review
- GLD Continuation readiness/review
- GLD chart-only outcomes
- GLD aggregate closeout
- Continuous Watcher behavior
- alert suppression
- shadow/live validation
- option P&L
- account sizing
- production readiness
