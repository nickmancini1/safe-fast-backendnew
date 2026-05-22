# SAFE-FAST GLD Continuation 001 Replay Fixture Specification Review

## Review Status

- Review status: PASS
- Baseline: patch8
- Repo: safe-fast-backendnew
- Branch: main
- Work mode: build work only, no live trade decisions

## Baseline Checked

- Current required local HEAD before edits: `636b4b8 Fix latest completed commit after GLD Continuation replay review`
- Current HEAD verified before edits: `636b4b8 Fix latest completed commit after GLD Continuation replay review`
- Latest completed committed build milestone before this specification review: GLD Continuation 001 real historical replay review asset, commit `f25b037 Add GLD Continuation 001 real historical replay review`
- Build state reviewed: yes
- GLD Continuation 001 real historical replay review reviewed: yes
- GLD Continuation 001 replay readiness review reviewed: yes
- GLD historical sample worksheet reviewed: yes
- GLD bounded source-window selection review reviewed: yes
- GLD source CSV validation review reviewed: yes
- News/headline risk plan reviewed: yes
- Closest existing fixture specification pattern inspected: `SAFE_FAST_IWM_CONTINUATION_001_REPLAY_FIXTURE_SPECIFICATION_REVIEW.md`
- GLD active target: yes
- Continuous Watcher deferred: yes

## Repo State Checked

- Git status result before edits: `## main...origin/main`
- Latest required commit present: yes, `636b4b8 Fix latest completed commit after GLD Continuation replay review`
- Uncommitted changes before task: none
- Conflicts found: none
- Protected completed replay review changed: no

Latest commits verified before edits:

- `636b4b8 Fix latest completed commit after GLD Continuation replay review`
- `f25b037 Add GLD Continuation 001 real historical replay review`
- `bf54932 Fix latest completed commit after GLD Continuation readiness review`
- `256ae25 Add GLD Continuation 001 replay readiness review`
- `5668706 Fix latest completed commit after GLD Clean Fast Break fixture output validation`
- `43b2ce1 Add GLD Clean Fast Break 001 fixture output validation`

## Fixture Candidate

- Sample ID: `GLD-SAMPLE-CONTINUATION-001`
- Window ID: `GLD-WINDOW-CONTINUATION-001`
- Source CSV path: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv`
- Source window: `2026-04-08T09:30:00-04:00` to `2026-04-17T15:30:00-04:00`
- Source row range: rows 78-133
- Source row count: 56
- Timeframe/session: dxLink `1h_rth`, regular RTH rows, `America/New_York`
- Source/vendor/as-of: `dxlink_candles.get_1h_ema50_snapshot`; `dxFeed via tastytrade dxLink`; `2026-05-20T16:25:45Z`
- Setup type: Continuation CANDIDATE / NEEDS REVIEW
- Direction: bullish/call-side CANDIDATE if later fixture/replay validation confirms; this is not a live trade direction.
- Candidate stage: elevated shelf/base into potential completed break and follow-through CANDIDATE
- Source-only shape: rows 78-84 show 2026-04-08 trading from `440.12` open down to the `431.31` window low and a `434.51` close; rows 85-98 show 2026-04-09/2026-04-10 consolidation with highs up to `440.905`; rows 99-105 show 2026-04-13 rebuilding from a `431.6501` session low to a `435.4` close; rows 106-112 show the 2026-04-14 push from `439.23` open to a `445.18` session high and `445.02` close; rows 113-126 show 2026-04-15/2026-04-16 pullback/hold context; rows 127-133 show 2026-04-17 extension to the `448.7` window high and a `445.88` final close.

## Source CSV Facts

- Validated source CSV row count: 290.
- Validated source CSV span: `2026-03-23T09:30:00-04:00` to `2026-05-20T11:30:00-04:00`.
- Selected GLD Continuation row count: 56.
- Selected GLD Continuation timestamp span: `2026-04-08T09:30:00-04:00` to `2026-04-17T15:30:00-04:00`.
- Symbol validation: PASS; all selected rows are `GLD`.
- Timeframe/session validation: PASS; all selected rows are `1h_rth`, `America/New_York`, `session_type=regular`, and `regular_session=true`.
- OHLCV validation: PASS; selected rows have numeric OHLCV, high/low envelopes contain open and close, and volume is non-negative.
- Window open: `440.12`
- Window final close: `445.88`
- Window high: `448.7`
- Window low: `431.31`
- Window volume sum: `23374834.689361`
- Session dates covered: `2026-04-08`, `2026-04-09`, `2026-04-10`, `2026-04-13`, `2026-04-14`, `2026-04-15`, `2026-04-16`, and `2026-04-17`.
- Missing source rows inside selected window: none found.
- Context fields in source CSV remain unavailable/unconfirmed: 24H/daily, macro, IV, and event context.
- Headline/news context: `NEWS_UNCONFIRMED`; no news or headline source was fetched or read for this review.

## Fixture Purpose

The future fixture JSON should prove GLD Continuation 001 signal/stage/lifecycle/trigger-card behavior against a real, bounded GLD 1H RTH source window. It must use exact source CSV candles, preserve no-hindsight cumulative row inputs, and keep unavailable context fields unconfirmed.

The fixture must not prove or claim chart outcome quality, generated replay report status, option P&L, account sizing, broker/order execution, auto-trading behavior, production readiness, or live trade suitability.

## Fixture Specification

- Expected fixture file name/path if fixture creation is approved in the next task: `historical_signal_replay/fixtures/first_real_gld_continuation_replay_v1_fixture.json`
- Fixture type: first real historical GLD Continuation replay v1 fixture.
- Fixture boundary: signal/stage/lifecycle/trigger-card proof only.
- Input source: copy exact GLD 1H RTH OHLCV source rows from the source CSV; do not edit OHLCV values.
- No-hindsight rule: each lifecycle row must include only source candles available at or before that row timestamp.
- Context fields: keep 24H/daily, macro, IV, event, and headline/news context unconfirmed because no valid source for those fields was read in this task.
- Proposed fixture row count: 6, following the existing IWM Continuation fixture specification style.

Proposed lifecycle row roles for future fixture creation:

| Row | Timestamp | Proposed row role | Source-only basis |
| --- | --- | --- | --- |
| 1 | `2026-04-08T15:30:00-04:00` | `watching_continuation_pullback_shelf_developing` | Completed rows through 2026-04-08 show the first bounded-window session falling from `440.12` open to the `431.31` window low and ending with `434.51` close; no 2026-04-09/2026-04-10 consolidation, 2026-04-13 rebuild, 2026-04-14 push, or later extension is available. |
| 2 | `2026-04-10T15:30:00-04:00` | `watching_continuation_elevated_shelf_no_trigger` | Completed rows through 2026-04-10 show consolidation with highs up to `440.905` and a `437.16` close; no 2026-04-13 rebuild, 2026-04-14 push, or 2026-04-17 extension is available. |
| 3 | `2026-04-13T15:30:00-04:00` | `continuation_rebuild_below_trigger_candidate` | Completed rows through 2026-04-13 show rebuilding from a `431.6501` session low to a `435.4` close, still before the later 2026-04-14 push above the reviewed shelf area. |
| 4 | `2026-04-14T15:30:00-04:00` | `continuation_completed_break_candidate` | Completed rows through 2026-04-14 include the push from `439.23` open to `445.18` high and `445.02` close; no 2026-04-15/2026-04-16 pullback/hold context or 2026-04-17 extension is available. |
| 5 | `2026-04-16T15:30:00-04:00` | `continuation_pullback_hold_or_stale_review` | Completed rows through 2026-04-16 include the post-2026-04-14 pullback/hold context ending with `440.12` close; no 2026-04-17 extension is available. |
| 6 | `2026-04-17T15:30:00-04:00` | `continuation_extension_spent_or_no_fresh_trigger_review` | Full selected window is available and includes the 2026-04-17 extension to the `448.7` window high and final `445.88` close; this row can review follow-through, stale/spent, or no-fresh-trigger context only if the future fixture asserts it from replay evidence. |

## Expected Source-Backed Assertions

- The fixture validates GLD only and uses symbol `GLD`.
- The fixture source metadata references `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv`.
- The fixture source row range is rows 78-133.
- The fixture source window is `2026-04-08T09:30:00-04:00` through `2026-04-17T15:30:00-04:00`.
- The source window row count is 56.
- Each fixture input row includes cumulative 1H RTH source candles only through that row timestamp.
- OHLCV values match the source CSV exactly.
- All selected source candles remain `GLD`, `1h_rth`, `America/New_York`, `session_type=regular`, and `regular_session=true`.
- Source/source-as-of/vendor fields match the validated CSV review exactly.
- Setup type remains `Continuation` or explicitly `UNCONFIRMED` only where a row-level assertion requires it; the fixture must not relabel the candidate as Ideal or Clean Fast Break without repo-backed evidence.
- Candidate lifecycle may progress from pullback/shelf development to elevated shelf/no-trigger context, rebuild-below-trigger context, completed-break candidate, pullback-hold or stale review, and extension/spent or no-fresh-trigger review.
- Shelf/base context is represented from bounded source rows only and does not invent final shelf proof.
- Trigger-card surface is present and specific enough to avoid vague confirmation-only output.
- The completed 1H RTH candle rule is preserved; no intrabar or live approval is inferred.
- Session-boundary carry-forward risk remains reviewable because the candidate spans multiple sessions and the 2026-04-14 push must not automatically become a fresh 2026-04-17 trigger.
- Duplicate/state-change fields distinguish meaningful lifecycle changes from repeated same-state rows.
- Replay output validates against existing Historical Signal Replay v1 input/output schema expectations.
- No generated reports are created as part of this specification review.

## Shelf / Base Fields To Review

The future fixture should preserve these shelf/base fields for output validation, but they remain TO REVIEW / UNCONFIRMED until fixture creation and validation:

- shelf definition
- shelf/base level or zone, including the reviewed `440.905` area only as source-backed review context
- shelf/base trigger basis
- shelf/base low or invalidation relation, including the `431.31` window low or a nearer accepted structure low only as source-backed review context
- shelf/base freshness
- whether the 2026-04-14 push is a completed break candidate
- whether the 2026-04-17 extension is follow-through, spent, stale, or no-fresh-trigger context

## Trigger-Card Fields To Review

The future fixture should include or preserve these trigger-card fields for output validation:

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
- `news_risk_level` only if the future fixture schema/output surface supports it; otherwise preserve headline/news context externally as `NEWS_UNCONFIRMED`.

Trigger-card fields that remain TO REVIEW / UNCONFIRMED until fixture creation:

- exact final Continuation identity assertion for each row
- exact trigger level or zone around the source-backed `440.905` reviewed area or later 2026-04-14/2026-04-17 behavior
- exact invalidation level near the `431.31` to `431.6501` lower area, or nearer accepted structure low if accepted
- exact accepted signal row, if any
- final stage and final verdict for each lifecycle row
- trigger state, trigger level/zone, and completed-candle approval state
- fresh/stale/spent determination after the 2026-04-14 push and 2026-04-17 extension
- room status
- extension status
- higher-timeframe 24H/daily context
- macro context
- IV context
- event context
- headline/news context
- final blocker priority
- final caution/watchout list
- current/live distance or proximity

## Assertions Not Allowed In This Task

- Do not assert final trigger level.
- Do not assert final shelf definition.
- Do not assert final invalidation.
- Do not assert final accepted signal row.
- Do not assert final fresh/stale/spent state.
- Do not assert final blocker priority.
- Do not assert final caution list.
- Do not assert final chart outcome.
- Do not assert generated replay report behavior.
- Do not assert option P&L.
- Do not assert account sizing.
- Do not assert broker/order/execution behavior.
- Do not assert production readiness.
- Do not assert live trade approval.
- Do not assert headline/news clarity, caution, or block status from invented or unread sources.

## News And Headline Context

- News/headline status for this fixture specification: `NEWS_UNCONFIRMED`.
- No live headline/news source was read.
- No headline/news blocker or caution was asserted.
- Future review must evaluate headline/news risk as context after setup and stage, before trade style, following `SAFE_FAST_NEWS_AND_HEADLINE_RISK_PLAN.md`.
- News must not create a setup, erase setup identity, or replace setup/stage logic.

## Fixture Creation Decision

- Fixture JSON status during this task: NO-GO; no fixture JSON was created.
- Generated replay report status: NO-GO; no generated replay report was created.
- Chart outcome status: NO-GO; no chart outcome was created.
- Replay runner changes required: no.
- Schema changes required: no.
- Next-task fixture asset creation status: GO if this specification review is accepted.

PASS. Fixture JSON creation may begin in the next bounded task because the source CSV, bounded window, source row count, candidate setup family, candidate direction, candidate stage, lifecycle row roles, shelf/base review fields, trigger-card fields, unconfirmed fields, expected fixture path, and post-creation validation requirements are specified from existing repo evidence.

## Required Validation After Fixture Creation

- Run fixture JSON syntax validation.
- Run the repo's current fixture validator, currently `python -B replay\validate_fixtures.py`.
- Run targeted source-window consistency validation against `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv`.
- Confirm fixture inputs validate against `historical_signal_replay/schemas/signal_replay_input_v1.schema.json`.
- Confirm replay outputs validate against `historical_signal_replay/schemas/signal_replay_output_v1.schema.json`.
- Confirm every fixture row uses only source candles at or before its row timestamp.
- Confirm GLD OHLCV values match the source CSV exactly.
- Confirm unavailable 24H/daily, macro, IV, event, and headline/news context remains unconfirmed.
- Confirm shelf/base, trigger-card, fresh/stale/spent, and session-boundary fields remain reviewable where exact proof is unavailable.
- Confirm no option P&L, account sizing, broker/order/execution, auto-trading, production, or live-trade fields are added.
- Confirm no generated reports are created unless a later task explicitly asks for replay output/report generation.

## Next Task

Create GLD Continuation 001 replay fixture JSON asset only, using this fixture specification. Do not create generated replay reports, chart outcomes, aggregate closeout, watcher work, option P&L, account sizing, production readiness claims, or live trade decisions in this specification-review task.

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

- GLD Continuation fixture JSON correctness
- GLD Continuation fixture/replay execution
- GLD generated replay reports
- GLD chart-only outcome behavior
- GLD aggregate closeout
- Continuous Watcher behavior
- alert suppression
- shadow/live validation
- option P&L
- account sizing
- production readiness
