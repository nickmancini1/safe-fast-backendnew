# SAFE-FAST IWM Clean Fast Break 001 Replay Fixture Specification Review

## Review Status

- Review status: PASS
- Baseline: patch8
- Repo: safe-fast-backendnew
- Branch: main
- Work mode: build work only, no live trade decisions

## Baseline Checked

- Current HEAD: `ba419e7 Add IWM Clean Fast Break 001 real historical replay review`
- IWM source CSV validation: PASS
- Bounded source-window selection: PASS
- Worksheet population: PASS
- IWM Ideal 001 fixture output validation: PASS
- IWM Clean Fast Break 001 readiness: PASS
- IWM Clean Fast Break 001 real historical replay review: PASS
- Trigger-card contracts complete for this phase: yes; unavailable fields must remain UNCONFIRMED rather than invented.
- IWM active target: yes; IWM remains the active broader coverage target.
- GLD deferred: yes.
- Continuous Watcher deferred: yes.

## Repo State Checked

- Git status result before edits: `## main...origin/main`
- Latest commits:
  - `ba419e7 Add IWM Clean Fast Break 001 real historical replay review`
  - `02f583d Add IWM Clean Fast Break 001 replay readiness review`
  - `5fe91e1 Add IWM Ideal 001 replay fixture output validation`
  - `6ca2eb4 Add IWM Ideal 001 replay fixture asset`
  - `0e03c26 Add IWM Ideal 001 replay fixture specification review`
  - `98a926e Add IWM Ideal 001 real historical replay review`
  - `6393e54 Add IWM Ideal 001 replay readiness review`
  - `4fe06a0 Populate IWM historical sample worksheet`
  - `f83f222 Add IWM bounded source-window selection review`
  - `4fe8d43 Add IWM source CSV validation`
  - `1237f14 Add IWM source CSV export blocked review`
  - `6cdeec3 Add IWM source CSV export request review`
- Conflicts found: none. The worktree was clean before edits and `ba419e7` was the current HEAD.

## Fixture Candidate

- Sample ID: `IWM-SAMPLE-CLEAN-FAST-BREAK-001`
- Window ID: `IWM-WINDOW-CLEAN-FAST-BREAK-001`
- Source CSV path: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv`
- Source window: `2026-04-08T09:30:00-04:00` to `2026-04-17T15:30:00-04:00`
- Source row count: 56
- Timeframe/session: dxLink `1h_rth`, regular RTH rows, `America/New_York`
- Setup type: Clean Fast Break CANDIDATE / NEEDS REVIEW
- Direction: bullish/call-side CANDIDATE, repo-backed by the bounded selection, worksheet, readiness review, and real historical replay review; this is not a live trade direction.
- Candidate stage: tight pause into upside break and follow-through CANDIDATE
- Fixture specification creation status from prior review: GO

## Fixture Specification

- Proposed fixture/review asset name: first real IWM Clean Fast Break replay v1 fixture.
- Proposed fixture path if fixture JSON creation is approved: `historical_signal_replay/fixtures/first_real_iwm_clean_fast_break_replay_v1_fixture.json`
- Source rows/window to use: exact IWM source rows from `2026-04-08T09:30:00-04:00` through `2026-04-17T15:30:00-04:00`; each fixture row must include only candles available at or before that row timestamp.
- Required input fields: `symbol`, `timestamp`, `candles_1h_rth`, `context_24h_daily`, `market_calendar_session`, `macro_context`, `iv_context`, and `event_context`.
- Expected output fields: `timestamp`, `symbol`, `setup_type`, `setup_state`, `stage`, `trigger_state`, `trigger_level`, `invalidation`, `room_status`, `extension_status`, `context_24h`, `wall_thesis_fit`, `final_verdict`, `primary_blocker`, `cautions_watchouts`, `winner_selection_result`, `human_next_step`, `first_seen`, `last_seen`, `state_changed`, `prior_state`, `current_state`, `trigger_changed`, `blocker_changed`, and `duplicate_alert_suppression_key`.
- Expected setup identity assertions: symbol remains `IWM`; setup type remains `Clean Fast Break` or explicitly `UNCONFIRMED` only where a row-level assertion requires it; the fixture must not relabel this candidate as Continuation without repo-backed proof.
- Expected stage assertions: lifecycle should cover gap/impulse context, tight-pause context, initial completed break candidate, follow-through context, later higher-base/digestion watch state, and post-break/no-fresh-trigger state.
- Expected trigger-card assertions: trigger-card surface must include setup identity, stage, trigger state, trigger level or explicit TO REVIEW/UNCONFIRMED status, invalidation or explicit TO REVIEW/UNCONFIRMED status, completed 1H RTH candle rule, blocker/caution context, freshness/spent status, and a human next step that does not imply live approval.
- Expected blocker/caution assertions: gap/extension and unavailable 24H/daily, macro, IV, and event context should surface as cautions or unconfirmed context; blocker/caution output must not destroy Clean Fast Break setup identity.
- Missing/unconfirmed fields that must remain explicitly unconfirmed: exact final trigger level inside the repo-backed `262.75` to `262.90` pause-high area, exact invalidation around the `260.03` to `260.34` pause-low area if accepted, completed-candle approval state, current distance/proximity, room status, extension status, final blocker priority, final caution list, exact accepted signal row, final fresh/stale/spent determination for 2026-04-14 through 2026-04-17, 24H/daily context, macro context, IV context, and event context.
- No-trade discipline assertions: fixture output is signal/stage/trigger-card proof only; it must not infer live trade approval, option P&L, account sizing, broker execution, production readiness, or auto-trading.

Proposed lifecycle row roles for fixture creation:

| Row | Timestamp | Proposed row role | Source-only basis |
| --- | --- | --- | --- |
| 1 | `2026-04-08T15:30:00-04:00` | `watching_clean_fast_break_gap_impulse_context` | Completed rows through 2026-04-08 show broad gap/impulse context and the start of the bounded window; no later pause or break is available. |
| 2 | `2026-04-10T15:30:00-04:00` | `watching_clean_fast_break_tight_pause_context` | Completed rows through 2026-04-10 show the compact pause/base near the 2026-04-09/2026-04-10 highs; no 2026-04-13 break is available. |
| 3 | `2026-04-13T12:30:00-04:00` | `clean_fast_break_initial_break_candidate` | Completed rows through 12:30 show IWM closing above the reviewed pause-high area; no later same-day or follow-through data is used. |
| 4 | `2026-04-13T15:30:00-04:00` | `clean_fast_break_follow_through_confirming_context` | Completed 2026-04-13 rows show same-session follow-through to `265.36` high and `265.06` close without using 2026-04-14 onward. |
| 5 | `2026-04-16T13:30:00-04:00` | `watching_higher_base_after_fast_break` | Completed rows through this timestamp show digestion after the 2026-04-13 break and 2026-04-14/2026-04-15 advance, without using 2026-04-17 data. |
| 6 | `2026-04-17T15:30:00-04:00` | `clean_fast_break_post_break_no_fresh_trigger` | The selected window has already followed through to `277.63` after the earlier completed break; this can represent post-break/spent context only. |

## Expected Replay Assertions

- Setup type remains Clean Fast Break or Clean Fast Break candidate, not falsely relabeled as Continuation.
- Trigger-card surface is present for each meaningful lifecycle row.
- Trigger path fields are present or explicitly UNCONFIRMED.
- Output does not collapse into vague confirmation-only language.
- Blockers/cautions do not destroy setup identity.
- No live trade approval is inferred.
- No option P&L is inferred.
- Missing data remains marked UNCONFIRMED where applicable.
- Each fixture input row uses cumulative source candles only through that row timestamp.
- OHLCV values match `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv` exactly.
- The completed 1H RTH candle rule is preserved; no intrabar or live approval is inferred.
- Duplicate/state-change fields distinguish meaningful lifecycle changes from repeated same-state rows.

## Fixture Creation Decision

- Fixture JSON creation status: GO
- Generated reports status: not created
- Replay runner changes required: no
- Schema changes required: no

GO. Fixture JSON creation may begin next because the source CSV, bounded source window, row count, candidate setup family, repo-backed candidate direction, candidate stage, trigger-card fields, unconfirmed fields, expected fixture path, and validation requirements are specified from existing repo evidence.

## Required Validation After Fixture Creation

- Run fixture JSON syntax validation.
- Run fixture/schema validation against `historical_signal_replay/schemas/signal_replay_input_v1.schema.json` and `historical_signal_replay/schemas/signal_replay_output_v1.schema.json`.
- Run targeted IWM Clean Fast Break fixture/replay validation.
- Run source-window consistency check against `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv`.
- Run the existing historical signal replay runner if applicable.
- Do not promote generated reports without validation.
- Update build state after validation.
- Confirm no option P&L, account sizing, broker/order/execution, auto-trading, production, or live-trade fields are added.

## Next Task

Create IWM Clean Fast Break 001 replay fixture JSON asset.

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

- IWM Clean Fast Break fixture JSON creation
- IWM Clean Fast Break fixture/replay execution
- IWM Continuation readiness/review
- IWM chart-only outcomes
- IWM aggregate closeout
- GLD broader coverage
- Continuous Watcher behavior
- alert suppression
- shadow/live validation
- option P&L
- account sizing
- production readiness
