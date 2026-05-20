# SAFE-FAST IWM Continuation 001 Replay Fixture Specification Review

## Review Status

- Review status: PASS
- Baseline: patch8
- Repo: safe-fast-backendnew
- Branch: main
- Work mode: build work only, no live trade decisions

## Baseline Checked

- Current HEAD: `2727576 Add IWM Continuation 001 real historical replay review`
- IWM source CSV validation: PASS
- Bounded source-window selection: PASS
- Worksheet population: PASS
- IWM Ideal 001 fixture output validation: PASS
- IWM Clean Fast Break 001 fixture output validation: PASS
- IWM Continuation 001 readiness: PASS
- IWM Continuation 001 real historical replay review: PASS
- Trigger-card contracts complete for this phase: yes; unavailable fields must remain UNCONFIRMED rather than invented.
- IWM active target: yes; IWM remains the active broader coverage target.
- GLD deferred: yes.
- Continuous Watcher deferred: yes.

## Repo State Checked

- Git status result before edits: `## main...origin/main`
- Latest commits:
  - `2727576 Add IWM Continuation 001 real historical replay review`
  - `baa36b6 Add IWM Continuation 001 replay readiness review`
  - `be235a1 Add IWM Clean Fast Break 001 replay fixture output validation`
  - `4cdc80b Add IWM Clean Fast Break 001 replay fixture asset`
  - `0c06755 Add IWM Clean Fast Break 001 replay fixture specification review`
  - `ba419e7 Add IWM Clean Fast Break 001 real historical replay review`
  - `02f583d Add IWM Clean Fast Break 001 replay readiness review`
  - `5fe91e1 Add IWM Ideal 001 replay fixture output validation`
  - `6ca2eb4 Add IWM Ideal 001 replay fixture asset`
  - `0e03c26 Add IWM Ideal 001 replay fixture specification review`
  - `98a926e Add IWM Ideal 001 real historical replay review`
  - `6393e54 Add IWM Ideal 001 replay readiness review`
- Conflicts found: none. The worktree was clean before edits and `2727576` was the current HEAD. The older `5d33edc` build-state milestone is the known non-conflict described in the task.

## Fixture Candidate

- Sample ID: `IWM-SAMPLE-CONTINUATION-001`
- Window ID: `IWM-WINDOW-CONTINUATION-001`
- Source CSV path: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv`
- Source window: `2026-04-20T09:30:00-04:00` to `2026-05-01T15:30:00-04:00`
- Source row count: 70
- Timeframe/session: dxLink `1h_rth`, regular RTH rows, `America/New_York`
- Setup type: Continuation CANDIDATE / NEEDS REVIEW
- Direction: bullish/call-side CANDIDATE, repo-backed by the bounded source-window selection, worksheet, readiness review, and real historical replay review; this is not a live trade direction.
- Candidate stage: shelf/base, pullback, rebuild, potential completed break CANDIDATE
- Fixture specification creation status from prior review: GO

## Fixture Specification

- Proposed fixture/review asset name: first real IWM Continuation replay v1 fixture.
- Proposed fixture path if fixture JSON creation is approved: `historical_signal_replay/fixtures/first_real_iwm_continuation_replay_v1_fixture.json`
- Source rows/window to use: exact IWM source rows from `2026-04-20T09:30:00-04:00` through `2026-05-01T15:30:00-04:00`; each fixture row must include only candles available at or before that row timestamp.
- Required input fields: `symbol`, `timestamp`, `candles_1h_rth`, `context_24h_daily`, `market_calendar_session`, `macro_context`, `iv_context`, and `event_context`.
- Expected output fields: `timestamp`, `symbol`, `setup_type`, `setup_state`, `stage`, `trigger_state`, `trigger_level`, `invalidation`, `room_status`, `extension_status`, `context_24h`, `wall_thesis_fit`, `final_verdict`, `primary_blocker`, `cautions_watchouts`, `winner_selection_result`, `human_next_step`, `first_seen`, `last_seen`, `state_changed`, `prior_state`, `current_state`, `trigger_changed`, `blocker_changed`, and `duplicate_alert_suppression_key`.
- Expected setup identity assertions: symbol remains `IWM`; setup type remains `Continuation` or explicitly `UNCONFIRMED` only where a row-level assertion requires it; the fixture must not relabel this candidate as Ideal or Clean Fast Break without repo-backed proof.
- Expected stage assertions: lifecycle should cover post-impulse shelf/base development, shelf retest/no-trigger state, recovery above shelf candidate, higher-base/rebuild candidate, completed trigger-stage candidate, and spent/follow-through/no-fresh-trigger context.
- Expected shelf/base assertions: shelf/base context must be represented from bounded source rows only, including the higher-price consolidation around `274` to `279`, the 2026-04-28 to 2026-04-29 dip/rebuild with `270.37` window low, the 2026-04-30 reclaim to `278.22` high and `277.92` close, and the 2026-05-01 follow-through attempt to `279.81`.
- Expected trigger-card assertions: output must include setup identity, stage, trigger state, trigger level or explicit TO REVIEW/UNCONFIRMED status, invalidation or explicit TO REVIEW/UNCONFIRMED status, completed 1H RTH candle rule, blocker/caution context, freshness/spent status, and a human next step that does not imply live approval.
- Expected stale/spent assertions: the fixture should explicitly preserve reviewability of whether the 2026-04-30 reclaim/break is fresh at its candidate signal row and whether 2026-05-01 is follow-through/spent/no-fresh-trigger context.
- Expected session-boundary/carry-forward assertions if relevant: because the candidate spans 2026-04-30 into 2026-05-01, prior-session completed shelf-break context must not become a fresh current-session trigger unless row-level fixture evidence supports that assertion.
- Expected blocker/caution assertions: prior impulse, extension risk, unavailable higher-timeframe context, unavailable macro/IV/event context, and session-boundary carry-forward risk should surface as cautions or unconfirmed context; blocker/caution output must not destroy Continuation setup identity.
- Missing/unconfirmed fields that must remain explicitly unconfirmed: exact final shelf definition, exact trigger basis/state, exact trigger level around the `274.38` recovery area or the later `278` to `279.81` hold/reclaim area, exact invalidation near `270.37` or nearer accepted structure low, current distance/proximity, final fresh/stale/spent determination, exact accepted signal row, room status, extension status, final blocker priority, final caution list, 24H/daily context, macro context, IV context, and event context.
- No-trade discipline assertions: fixture output is signal/stage/trigger-card proof only; it must not infer live trade approval, option P&L, account sizing, broker execution, production readiness, or auto-trading.

Proposed lifecycle row roles for fixture creation:

| Row | Timestamp | Proposed row role | Source-only basis |
| --- | --- | --- | --- |
| 1 | `2026-04-20T15:30:00-04:00` | `watching_continuation_pullback_shelf_developing` | Completed rows through 2026-04-20 show IWM holding the post-impulse higher-price area and closing at `277.34`; no later retest, recovery, 2026-04-30 reclaim, or 2026-05-01 follow-through is available. |
| 2 | `2026-04-21T15:30:00-04:00` | `watching_continuation_shelf_retest_no_trigger` | Completed rows through 2026-04-21 show a retest/pullback from the higher area into a `274.53` close, but no completed recovery above the later reviewed shelf/reclaim path is available. |
| 3 | `2026-04-22T15:30:00-04:00` | `continuation_recovery_above_shelf_candidate` | Completed rows through 2026-04-22 show recovery to a `276.48` close, without using the 2026-04-23/2026-04-24 action or later 2026-04-30 push. |
| 4 | `2026-04-24T15:30:00-04:00` | `continuation_higher_base_rebuild_candidate` | Completed rows through 2026-04-24 can represent higher-base/rebuild context before the later 2026-04-28/2026-04-29 dip and 2026-04-30 reclaim are known. |
| 5 | `2026-04-30T15:30:00-04:00` | `continuation_triggered_signal_stage_candidate` | Completed rows through 2026-04-30 include the 2026-04-28/2026-04-29 dip/rebuild, the `270.37` window low, and a reclaim to `278.22` high / `277.92` close; no 2026-05-01 high or close is available. |
| 6 | `2026-05-01T15:30:00-04:00` | `continuation_spent_or_follow_through_no_fresh_trigger` | The selected window has followed through to `279.81` after the earlier 2026-04-30 completed reclaim/break candidate; this row can represent spent/follow-through/no-fresh-trigger context only. |

## Expected Replay Assertions

- Setup type remains Continuation or Continuation candidate, not falsely relabeled as Ideal or Clean Fast Break.
- Shelf/base context is represented without inventing proof.
- Trigger-card surface is present for each meaningful lifecycle row.
- Trigger path fields are present or explicitly UNCONFIRMED.
- Output does not collapse into vague confirmation-only language.
- Developing lifecycle / pending completed-candle discipline is represented with completed 1H RTH rows only.
- Stale/spent condition remains reviewable, especially across 2026-04-30 into 2026-05-01.
- Session-boundary carry-forward risk is considered where relevant.
- Blockers/cautions do not destroy setup identity.
- No live trade approval is inferred.
- No option P&L is inferred.
- Missing data remains marked UNCONFIRMED where applicable.
- Each fixture input row uses cumulative source candles only through that row timestamp.
- OHLCV values match `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv` exactly.
- Replay output validates against existing Historical Signal Replay v1 input/output schema expectations.
- Duplicate/state-change fields distinguish meaningful lifecycle changes from repeated same-state rows.

## Fixture Creation Decision

- Fixture JSON creation status: GO
- Generated reports status: not created
- Replay runner changes required: no
- Schema changes required: no

GO. Fixture JSON creation may begin next because the source CSV, bounded source window, source row count, candidate setup family, repo-backed candidate direction, candidate stage, shelf/base and trigger-card requirements, continuation-specific assertions, unconfirmed fields, expected fixture path, and post-creation validation requirements are specified from existing repo evidence.

## Required Validation After Fixture Creation

- Run fixture JSON syntax validation.
- Run fixture/schema validation against `historical_signal_replay/schemas/signal_replay_input_v1.schema.json` and `historical_signal_replay/schemas/signal_replay_output_v1.schema.json`.
- Run targeted IWM Continuation fixture/replay validation.
- Run source-window consistency check against `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv`.
- Run shelf/base and trigger-card output validation.
- Check stale/spent/session-boundary review fields where applicable.
- Run the existing historical signal replay runner if applicable.
- Do not promote generated reports without validation.
- Update build state after validation.
- Confirm no option P&L, account sizing, broker/order/execution, auto-trading, production, or live-trade fields are added.

## Next Task

Create IWM Continuation 001 replay fixture JSON asset.

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

- IWM Continuation fixture JSON creation
- IWM Continuation fixture/replay execution
- IWM chart-only outcomes
- IWM aggregate closeout
- GLD broader coverage
- Continuous Watcher behavior
- alert suppression
- shadow/live validation
- option P&L
- account sizing
- production readiness
