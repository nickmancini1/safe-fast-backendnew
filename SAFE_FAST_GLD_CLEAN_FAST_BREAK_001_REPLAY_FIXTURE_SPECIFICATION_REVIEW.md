# SAFE-FAST GLD Clean Fast Break 001 Replay Fixture Specification Review

## Review Status

- Review status: PASS
- Baseline: patch8
- Repo: safe-fast-backendnew
- Branch: main
- Work mode: build work only, no live trade decisions

## Baseline Checked

- Current required local HEAD before edits: `470081f Fix latest completed commit after GLD Clean Fast Break replay review`
- Current HEAD verified before edits: `470081f Fix latest completed commit after GLD Clean Fast Break replay review`
- Latest completed committed build milestone before this specification review: GLD Clean Fast Break 001 real historical replay review asset, commit `2ae012e Add GLD Clean Fast Break 001 real historical replay review`
- Build state reviewed: yes
- GLD Clean Fast Break 001 real historical replay review reviewed: yes
- GLD Clean Fast Break 001 replay readiness review reviewed: yes
- GLD historical sample worksheet reviewed: yes
- GLD bounded source-window selection review reviewed: yes
- GLD source CSV validation review reviewed: yes
- News/headline risk plan reviewed: yes
- Closest existing fixture specification pattern inspected: `SAFE_FAST_IWM_CLEAN_FAST_BREAK_001_REPLAY_FIXTURE_SPECIFICATION_REVIEW.md`
- GLD active target: yes
- Continuous Watcher deferred: yes

## Repo State Checked

- Git status result before edits: `## main...origin/main`
- Latest required commit present: yes, `470081f Fix latest completed commit after GLD Clean Fast Break replay review`
- Uncommitted changes before task: none
- Conflicts found: none
- Protected completed replay review changed: no

Latest commits verified before edits:

- `470081f Fix latest completed commit after GLD Clean Fast Break replay review`
- `2ae012e Add GLD Clean Fast Break 001 real historical replay review`
- `47596b5 Fix latest completed commit after GLD Clean Fast Break readiness review`
- `30dac4a Add GLD Clean Fast Break 001 readiness review`
- `474c982 Fix latest completed commit after GLD Ideal fixture output validation`
- `fd30283 Add GLD Ideal 001 fixture output validation`

## Fixture Candidate

- Sample ID: `GLD-SAMPLE-CLEAN-FAST-BREAK-001`
- Window ID: `GLD-WINDOW-CLEAN-FAST-BREAK-001`
- Source CSV path: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv`
- Source window: `2026-04-29T09:30:00-04:00` to `2026-05-08T15:30:00-04:00`
- Source row range: rows 183-238
- Source row count: 56
- Timeframe/session: dxLink `1h_rth`, regular RTH rows, `America/New_York`
- Source/vendor/as-of: `dxlink_candles.get_1h_ema50_snapshot`; `dxFeed via tastytrade dxLink`; `2026-05-20T16:25:45Z`
- Setup type: Clean Fast Break CANDIDATE / NEEDS REVIEW
- Direction: bullish/call-side CANDIDATE if later fixture/replay validation confirms; this is not a live trade direction.
- Candidate stage: base/rebuild into fast upside reclaim CANDIDATE
- Source-only shape: 2026-04-29 base/rebuild context from `416.74` open to `417.465` close, 2026-04-30/2026-05-01 move and hold around the `423.08` to `427.92` area, 2026-05-04/2026-05-05 lower base/rebuild with the `413.2801` window low, 2026-05-06 gap/reclaim into a `433.19` high, 2026-05-07 push to the `437.42` window high and pullback, and 2026-05-08 pullback/hold rows ending at `433.795`.

## Source CSV Facts

- Validated source CSV row count: 290.
- Validated source CSV span: `2026-03-23T09:30:00-04:00` to `2026-05-20T11:30:00-04:00`.
- Selected GLD Clean Fast Break row count: 56.
- Selected GLD Clean Fast Break timestamp span: `2026-04-29T09:30:00-04:00` to `2026-05-08T15:30:00-04:00`.
- Symbol validation: PASS; all selected rows are `GLD`.
- Timeframe/session validation: PASS; all selected rows are `1h_rth`, `America/New_York`, `session_type=regular`, and `regular_session=true`.
- OHLCV validation: PASS; selected rows have numeric OHLCV, high/low envelopes contain open and close, and volume is non-negative.
- Window open: `416.74`
- Window final close: `433.795`
- Window high: `437.42`
- Window low: `413.2801`
- Window volume sum: `18481229.424997`
- Session dates covered: `2026-04-29`, `2026-04-30`, `2026-05-01`, `2026-05-04`, `2026-05-05`, `2026-05-06`, `2026-05-07`, and `2026-05-08`.
- Missing source rows inside selected window: none found.
- Context fields in source CSV remain unavailable/unconfirmed: 24H/daily, macro, IV, and event context.
- Headline/news context: `NEWS_UNCONFIRMED`; no news or headline source was fetched or read for this review.

## Fixture Purpose

The future fixture JSON should prove GLD Clean Fast Break 001 signal/stage/lifecycle/trigger-card behavior against a real, bounded GLD 1H RTH source window. It must use exact source CSV candles, preserve no-hindsight cumulative row inputs, and keep unavailable context fields unconfirmed.

The fixture must not prove or claim chart outcome quality, generated replay report status, option P&L, account sizing, broker/order execution, auto-trading behavior, production readiness, or live trade suitability.

## Fixture Specification

- Expected fixture file name/path if fixture creation is approved in the next task: `historical_signal_replay/fixtures/first_real_gld_clean_fast_break_replay_v1_fixture.json`
- Fixture type: first real historical GLD Clean Fast Break replay v1 fixture.
- Fixture boundary: signal/stage/lifecycle/trigger-card proof only.
- Input source: copy exact GLD 1H RTH OHLCV source rows from the source CSV; do not edit OHLCV values.
- No-hindsight rule: each lifecycle row must include only source candles available at or before that row timestamp.
- Context fields: keep 24H/daily, macro, IV, event, and headline/news context unconfirmed because no valid source for those fields was read in this task.
- Proposed fixture row count: 6, following the existing IWM Clean Fast Break fixture specification style.

Proposed lifecycle row roles for future fixture creation:

| Row | Timestamp | Proposed row role | Source-only basis |
| --- | --- | --- | --- |
| 1 | `2026-04-29T15:30:00-04:00` | `watching_clean_fast_break_base_rebuild_context` | Completed rows through 2026-04-29 show early bounded-window base/rebuild context ending with `417.465` close; no 2026-04-30/2026-05-01 move, 2026-05-04/2026-05-05 lower base, 2026-05-06 reclaim, or later follow-through is available. |
| 2 | `2026-05-01T15:30:00-04:00` | `watching_clean_fast_break_pre_reclaim_range_context` | Completed rows through 2026-05-01 show the 2026-04-30/2026-05-01 move and hold around the `423.08` to `427.92` area; no 2026-05-04/2026-05-05 lower base or 2026-05-06 gap/reclaim is available. |
| 3 | `2026-05-05T15:30:00-04:00` | `watching_clean_fast_break_lower_base_before_reclaim` | Completed rows through 2026-05-05 include the lower base/rebuild after the `413.2801` window low and end with `418.17` close; no 2026-05-06 gap/reclaim or later action is available. |
| 4 | `2026-05-06T09:30:00-04:00` | `clean_fast_break_initial_reclaim_candidate` | Completed rows through 2026-05-06 09:30 show gap/reclaim behavior with `430.1` open, `433.19` high, and `432.06` close above the prior reviewed `425.4500` to `427.9200` area; later same-day hold and 2026-05-07 action are unavailable. |
| 5 | `2026-05-07T10:30:00-04:00` | `clean_fast_break_follow_through_extension_candidate` | Completed rows through 2026-05-07 10:30 include follow-through to the `437.42` window high; later 2026-05-07 pullback and 2026-05-08 rows are unavailable. |
| 6 | `2026-05-08T15:30:00-04:00` | `clean_fast_break_pullback_hold_or_no_fresh_trigger_review` | Full selected window is available and ends after 2026-05-08 pullback/hold rows with `433.795` close; this row can review follow-through, stale/spent/no-fresh-trigger, or hold context only if the future fixture asserts it from replay evidence. |

## Expected Source-Backed Assertions

- The fixture validates GLD only and uses symbol `GLD`.
- The fixture source metadata references `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv`.
- The fixture source row range is rows 183-238.
- The fixture source window is `2026-04-29T09:30:00-04:00` through `2026-05-08T15:30:00-04:00`.
- The source window row count is 56.
- Each fixture input row includes cumulative 1H RTH source candles only through that row timestamp.
- OHLCV values match the source CSV exactly.
- All selected source candles remain `GLD`, `1h_rth`, `America/New_York`, `session_type=regular`, and `regular_session=true`.
- Source/source-as-of/vendor fields match the validated CSV review exactly.
- Setup type remains `Clean Fast Break` or explicitly `UNCONFIRMED` only where a row-level assertion requires it; the fixture must not relabel the candidate as Continuation or Ideal without repo-backed evidence.
- Candidate lifecycle may progress from base/rebuild context to pre-reclaim range context, lower-base-before-reclaim context, initial reclaim candidate, follow-through/extension candidate, and pullback-hold or no-fresh-trigger review.
- Trigger-card surface is present and specific enough to avoid vague confirmation-only output.
- The completed 1H RTH candle rule is preserved; no intrabar or live approval is inferred.
- Duplicate/state-change fields distinguish meaningful lifecycle changes from repeated same-state rows.
- Replay output validates against existing Historical Signal Replay v1 input/output schema expectations.
- No generated reports are created as part of this specification review.

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

- exact final Clean Fast Break identity assertion for each row
- exact trigger level inside the source-backed `425.4500` to `427.9200` prior area or later hold toward `433.1900`
- exact invalidation level near the `413.2801` base-low zone, or nearer accepted structure low if accepted
- exact accepted signal row, if any
- final stage and final verdict for each lifecycle row
- trigger state, trigger level/zone, and completed-candle approval state
- fresh/stale/spent determination after the 2026-05-07 follow-through and 2026-05-08 pullback/hold rows
- room status
- extension status
- EMA/trend context
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
- Do not assert final invalidation.
- Do not assert final accepted signal row.
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

PASS. Fixture JSON creation may begin in the next bounded task because the source CSV, bounded window, source row count, candidate setup family, candidate direction, candidate stage, lifecycle row roles, trigger-card fields, unconfirmed fields, expected fixture path, and post-creation validation requirements are specified from existing repo evidence.

## Required Validation After Fixture Creation

- Run fixture JSON syntax validation.
- Run the repo's current fixture validator, currently `python -B replay\validate_fixtures.py`.
- Run targeted source-window consistency validation against `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv`.
- Confirm fixture inputs validate against `historical_signal_replay/schemas/signal_replay_input_v1.schema.json`.
- Confirm replay outputs validate against `historical_signal_replay/schemas/signal_replay_output_v1.schema.json`.
- Confirm every fixture row uses only source candles at or before its row timestamp.
- Confirm GLD OHLCV values match the source CSV exactly.
- Confirm unavailable 24H/daily, macro, IV, event, and headline/news context remains unconfirmed.
- Confirm no option P&L, account sizing, broker/order/execution, auto-trading, production, or live-trade fields are added.
- Confirm no generated reports are created unless a later task explicitly asks for replay output/report generation.

## Next Task

Create GLD Clean Fast Break 001 replay fixture JSON asset only, using this fixture specification. Do not create generated replay reports, chart outcomes, aggregate closeout, watcher work, option P&L, account sizing, production readiness claims, or live trade decisions in this specification-review task.

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

- GLD Clean Fast Break fixture JSON correctness
- GLD Clean Fast Break fixture/replay execution
- GLD generated replay reports
- GLD chart-only outcome behavior
- GLD Continuation readiness/review
- GLD aggregate closeout
- Continuous Watcher behavior
- alert suppression
- shadow/live validation
- option P&L
- account sizing
- production readiness
