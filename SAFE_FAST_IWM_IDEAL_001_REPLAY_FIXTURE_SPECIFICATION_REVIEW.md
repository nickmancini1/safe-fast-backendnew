# SAFE-FAST IWM Ideal 001 Replay Fixture Specification Review

## Review Status

- Review status: PASS
- Baseline: patch8
- Repo: safe-fast-backendnew
- Branch: main
- Work mode: build work only, no live trade decisions

## Baseline Checked

- Current required HEAD: `98a926e Add IWM Ideal 001 real historical replay review`
- Current HEAD verified before edits: `98a926e Add IWM Ideal 001 real historical replay review`
- Build state reviewed: yes
- IWM Ideal 001 real historical replay review reviewed: yes
- IWM Ideal 001 replay readiness review reviewed: yes
- IWM historical sample worksheet reviewed: yes
- IWM bounded source-window selection review reviewed: yes
- IWM source CSV validation review reviewed: yes
- Existing historical signal replay fixtures reviewed: yes
- Historical signal replay schemas reviewed: yes
- IWM active target: yes
- GLD deferred: yes
- Continuous Watcher deferred: yes

## Repo State Checked

- Git status result before edits: `## main...origin/main`
- Latest required commit present: yes, `98a926e Add IWM Ideal 001 real historical replay review`
- Uncommitted changes before task: none
- Conflicts found: none
- Protected completed replay review changed: no

## Fixture Candidate

- Sample ID: `IWM-SAMPLE-IDEAL-001`
- Window ID: `IWM-WINDOW-IDEAL-001`
- Source CSV path: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv`
- Source window: `2026-05-05T09:30:00-04:00` to `2026-05-14T15:30:00-04:00`
- Source row count: 56
- Timeframe/session: dxLink `1h_rth`, regular RTH rows, `America/New_York`
- Setup type: Ideal CANDIDATE / NEEDS REVIEW
- Direction: bullish/call-side CANDIDATE, repo-backed by the bounded selection, worksheet, readiness review, and replay review; this is not a live trade direction.
- Candidate stage: pullback/retest into recovery CANDIDATE
- Source-only shape: upside context into 2026-05-06, pullback/retest into the 2026-05-12 low near `278.29`, recovery into the 2026-05-13/2026-05-14 `283.56` to `285.655` area, and later same-window follow-through/no-fresh-trigger review through 2026-05-14 close.

## Fixture Specification

- Expected fixture file name/path if creation is approved: `historical_signal_replay/fixtures/first_real_iwm_ideal_replay_v1_fixture.json`
- Fixture type: first real historical IWM Ideal replay v1 fixture.
- Fixture boundary: signal/stage/lifecycle/trigger-card proof only.
- Input source: copy exact IWM 1H RTH OHLCV source rows from the source CSV; do not edit OHLCV values.
- No-hindsight rule: each lifecycle row must include only source candles available at or before that row timestamp.
- Context fields: keep 24H/daily, macro, IV, and event context unconfirmed because the source CSV marks those fields unconfirmed.
- Proposed fixture row count: 6, following the existing QQQ Ideal real replay fixture pattern.
- Proposed lifecycle row roles:
  - `watching_ideal_impulse_context` at or near `2026-05-08T15:30:00-04:00`
  - `watching_ideal_pullback_retest_developing` at or near `2026-05-12T10:30:00-04:00`
  - `watching_ideal_retest_hold_unconfirmed` at or near `2026-05-12T12:30:00-04:00`
  - `ideal_retest_recovery_confirmation_candidate` at or near `2026-05-12T15:30:00-04:00`
  - `ideal_triggered_signal_stage_candidate` at or near `2026-05-14T11:30:00-04:00`
  - `ideal_follow_through_no_fresh_trigger` at or near `2026-05-14T15:30:00-04:00`
- Trigger-card fields required in fixture/replay output:
  - `timestamp`
  - `symbol`
  - `setup_type`
  - `setup_state`
  - `stage`
  - `trigger_state`
  - `trigger_level`
  - `invalidation`
  - `room_status`
  - `extension_status`
  - `context_24h`
  - `wall_thesis_fit`
  - `final_verdict`
  - `primary_blocker`
  - `cautions_watchouts`
  - `winner_selection_result`
  - `human_next_step`
  - `first_seen`
  - `last_seen`
  - `state_changed`
  - `prior_state`
  - `current_state`
  - `trigger_changed`
  - `blocker_changed`
  - `duplicate_alert_suppression_key`
- Trigger-card fields to preserve as TO REVIEW / UNCONFIRMED until fixture creation:
  - exact final Ideal identity assertion for each row
  - exact trigger level inside the repo-backed `283.56` to `285.655` recovery area
  - exact invalidation level near the retest low zone if accepted
  - EMA/trend context
  - higher-timeframe 24H/daily context
  - macro context
  - IV context
  - event context
  - exact room status
  - exact extension status
  - final blocker priority
  - final caution/watchout list
  - final fresh/stale/spent determination for the 2026-05-14 recovery/follow-through rows
  - final accepted signal row, if any

## Expected Replay Assertions

- The fixture validates IWM only and uses symbol `IWM`.
- The fixture source metadata references `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv`.
- The fixture source window is `2026-05-05T09:30:00-04:00` through `2026-05-14T15:30:00-04:00`.
- The source window row count is 56.
- Each fixture input row includes cumulative 1H RTH source candles only through that row timestamp.
- OHLCV values match the source CSV exactly.
- Setup type remains `Ideal` or explicitly `UNCONFIRMED` only where a row-level assertion requires it; the fixture must not relabel the candidate as another setup without repo-backed evidence.
- Candidate stage progresses from impulse context to pullback/retest, hold/recovery review, signal-stage candidate, and follow-through/no-fresh-trigger review.
- Trigger-card surface is present and specific enough to avoid vague confirmation-only output.
- Trigger level, invalidation, blocker, caution, room, extension, context, and final verdict fields are either asserted from repo-backed fixture design or marked unconfirmed/review-limited.
- The completed 1H RTH candle rule is preserved; no intrabar or live approval is inferred.
- Duplicate/state-change fields distinguish meaningful lifecycle changes from repeated same-state rows.
- Replay output validates against existing Historical Signal Replay v1 input/output schema expectations.
- No generated reports are created as part of this specification review.

## Fixture Creation Decision

- Fixture JSON creation status: GO
- Generated reports status: not created
- Replay runner changes required: no
- Schema changes required: no

GO. Fixture JSON creation may begin next because the source CSV, bounded window, row count, candidate setup family, candidate direction, candidate stage, trigger-card fields, unconfirmed fields, expected fixture path, and post-creation validation requirements are specified from repo evidence.

## Required Validation After Fixture Creation

- Run fixture validation: `python -B historical_signal_replay/validate_fixtures.py` if that is the active validation path, or the repo's current fixture validator if named differently.
- Run historical signal replay: `python -B historical_signal_replay/run_replay.py` if that is the active runner path, or the repo's current replay runner if named differently.
- Confirm `historical_signal_replay/fixtures/first_real_iwm_ideal_replay_v1_fixture.json` exists and is the only fixture added in the fixture-creation task.
- Confirm fixture inputs validate against `historical_signal_replay/schemas/signal_replay_input_v1.schema.json`.
- Confirm replay outputs validate against `historical_signal_replay/schemas/signal_replay_output_v1.schema.json`.
- Confirm every fixture row uses only source candles at or before its row timestamp.
- Confirm IWM OHLCV values match the source CSV exactly.
- Confirm unavailable 24H/daily, macro, IV, and event context remains unconfirmed.
- Confirm no option P&L, account sizing, broker/order/execution, auto-trading, production, or live-trade fields are added.
- Confirm no generated reports are created unless a later task explicitly asks for replay output/report generation.

## Next Task

Create IWM Ideal 001 replay fixture JSON asset.

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

- IWM Ideal fixture JSON correctness
- IWM Ideal replay execution
- IWM Ideal replay output validation
- IWM Clean Fast Break replay readiness/review
- IWM Continuation replay readiness/review
- IWM stage/session/winner/no-trade edge reviews
- IWM chart-only outcome reviews
- IWM aggregate closeout
- GLD broader coverage
- Continuous Watcher behavior
- alert suppression
- shadow/live validation
- option P&L
- account sizing
- production readiness
