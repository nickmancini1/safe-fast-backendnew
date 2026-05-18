# SAFE-FAST On-Demand Trigger Card Requirement Review

## Review Status

- Review status: PASS
- Baseline: patch8
- Repo: safe-fast-backendnew
- Branch: main
- Work mode: build work only, no live trade decisions

## Baseline Checked

- SPY/QQQ closeout complete: yes. Repo evidence shows SPY real historical replay v1 three-setup closeout passed, QQQ three-setup historical replay closeout passed, and QQQ chart outcome closeout passed.
- IWM active path: yes. `SAFE_FAST_BUILD_STATE.md` and `SAFE_FAST_IWM_HISTORICAL_SAMPLE_COLLECTION_WORKSHEET.md` keep IWM as the next broader coverage target, with concrete sample population still pending.
- GLD deferred: yes.
- Continuous Watcher deferred: yes.
- Known commit distinction: `5d33edc Add QQQ chart outcome closeout review` remains the completed QQQ closeout milestone, while current local HEAD is `5d114c8 Add IWM historical sample collection worksheet`. This is an expected distinction, not a conflict.
- Do-not-touch boundaries: this review is docs-only and does not touch `main.py`, engine logic, replay runner logic, schemas, fixtures, generated reports, Railway, production, option P&L, account sizing, auto-trading, live trade decisions, or Continuous Watcher implementation.

## Repo State Checked

- Git status result: `## main...origin/main`
- Latest commits:
  - `5d114c8 Add IWM historical sample collection worksheet`
  - `1ff5daf Add IWM historical replay candidate selection review`
  - `8b49ca6 Add IWM fixture replay candidate inventory`
  - `de6cf3b Add IWM broader coverage planning review`
  - `5c1e564 Add next broader coverage decision review`
  - `3faf90d Repair build-state header after QQQ closeout`
  - `5d33edc Add QQQ chart outcome closeout review`
  - `723a69f Add QQQ post-aggregate chart outcome decision review`
  - `ac1d046 Add QQQ aggregate chart outcome output validation`
  - `872906e Add QQQ chart outcome aggregate summary`
  - `29fc799 Add QQQ Continuation chart outcome output validation`
  - `afb498f Add QQQ Continuation chart outcome calculation`
- Conflicts found: none. The known `5d33edc` milestone vs `5d114c8` HEAD distinction was reviewed and is not a conflict.

## Problem Being Locked

Existing engine trigger/stage tests can prove internal state transitions and selected user-facing stage messages. That is necessary, but it is not enough by itself for on-demand manual use.

User-facing output must also expose the actual trigger path. The output should prevent a "wait, wait, too late" failure mode where SAFE-FAST confirms that a setup is valid, developing, pending, triggered, stale, or spent, but does not show the trader what level, candle rule, freshness rule, invalidation, and next alert condition define the path.

Vague language such as "wait for confirmation" or "recovery confirmation" is insufficient unless it is paired with the actual trigger path.

## Trigger Card Requirement

Every on-demand SAFE-FAST read that has a valid, developing, pending, triggered, stale, or spent setup must expose a trigger card with:

- setup type
- direction
- stage
- trigger status
- trigger level or zone
- candle/timeframe rule
- current distance to trigger when available
- early warning threshold when available
- invalidation level or condition
- fresh/stale/spent condition
- next check / next alert condition
- blockers/cautions affecting trigger readiness

## Setup-Type Requirements

### Ideal trigger card

The Ideal trigger card must expose the retest/recovery path instead of only saying "recovery confirmation." It must show the setup type as Ideal, direction, current stage, trigger status, the actual trigger level or zone, the completed-candle/timeframe confirmation rule, current distance to trigger when available, early warning threshold when available, invalidation level or condition, fresh/stale/spent rule, next check or next alert condition, and any blockers/cautions that affect trigger readiness.

### Clean Fast Break trigger card

The Clean Fast Break trigger card must expose the tight-pause or higher-base break path instead of only saying "wait for break" or "fresh completed breakout required." It must show the setup type as Clean Fast Break, direction, current stage, trigger status, actual break level or zone, completed-candle/timeframe confirmation rule, current distance to trigger when available, early warning threshold when available, invalidation level or condition, fresh/stale/spent rule, next check or next alert condition, and blockers/cautions affecting readiness.

### Continuation trigger card

The Continuation trigger card must expose the shelf/reclaim/hold/break path. It must show the setup type as Continuation, direction, current stage, trigger status, shelf trigger level or zone, completed-candle/timeframe confirmation rule, current distance to trigger when available, early warning threshold when available, invalidation level or condition, fresh/stale/spent rule, next check or next alert condition, and blockers/cautions affecting readiness. Put-side Continuations must use the inverse below-shelf trigger path where applicable.

## SPY Trigger-Surface Audit

- Rating: PARTIAL

Repo evidence proves SPY internal signal/stage/lifecycle coverage across Continuation, Ideal, and Clean Fast Break. `historical_signal_replay/REAL_HISTORICAL_REPLAY_V1_SPY_THREE_SETUP_CLOSEOUT_REVIEW.md` confirms all three setup families have real SPY source windows, fixtures, signal logs, summaries, runner output validation, expected setup-family counts, stage counts, lifecycle sequences, and no-hindsight boundaries.

SPY generated signal logs include trigger-surface data fields such as `setup_type`, `stage`, `trigger_state`, `trigger_level`, `invalidation`, `primary_blocker`, `cautions_watchouts`, state changes, trigger changes, and duplicate alert suppression keys. That is evidence of internal and replay-output trigger/stage metadata.

However, the reviewed SPY closeout is explicitly signal/stage/lifecycle replay only. It does not prove a required on-demand trigger card with all fields listed in this review, including direction, current distance to trigger, early warning threshold, fresh/stale/spent rule phrased as a card field, next alert condition, and full blocker/caution relationship to trigger readiness. The user-facing contracts prove selected humanized next-step and stage-surface language, not a complete trigger-card surface for every on-demand setup state.

## QQQ Trigger-Surface Audit

- Rating: PARTIAL

Repo evidence proves QQQ internal signal/stage/lifecycle coverage across Ideal, Clean Fast Break, and Continuation. `historical_signal_replay/QQQ_THREE_SETUP_REAL_HISTORICAL_REPLAY_CLOSEOUT_REVIEW.md` confirms all three setup families have reviewed QQQ replay evidence, generated signal logs, generated summaries, runner output validation, expected setup-family counts, and lifecycle/stage sequences. `SAFE_FAST_QQQ_CHART_OUTCOME_CLOSEOUT_REVIEW.md` confirms the QQQ chart-only closeout phase used accepted replay/source artifacts and preserved copied trigger references and invalidation.

QQQ fixtures and signal logs include trigger metadata fields such as `setup_type`, `stage`, `trigger_state`, `trigger_level`, `invalidation`, `primary_blocker`, `cautions_watchouts`, lifecycle state, trigger changes, and duplicate alert suppression keys. That supports internal trigger/stage and replay-output correctness.

However, the reviewed QQQ closeouts do not prove that every on-demand read exposes a complete user-facing trigger card with all required fields. The closeouts prove replay evidence, stage/lifecycle sequencing, chart-only outcome boundaries, and copied trigger/invalidation references. They do not prove direction, current distance to trigger, early warning threshold, next alert condition, fresh/stale/spent card wording, and blocker/caution readiness relationship are surfaced together as a user-facing trigger card for every valid, developing, pending, triggered, stale, or spent setup.

## Impact On Completed SPY/QQQ Closeout

- SPY/QQQ closeout is not being redone.
- This is an output-surface audit.
- The PARTIAL ratings become follow-up surface/contract work, not replay redo.

## Impact On IWM/GLD

- IWM and GLD inherit the trigger-card requirement.
- Future IWM/GLD replay/review assets must check trigger-card clarity, not only trigger/stage correctness.

## Required Follow-Up

Because SPY/QQQ trigger-card surface is partial, create an on-demand trigger-card surface contract gap review before deeper IWM work.

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

- IWM historical sample population
- IWM replay coverage
- IWM chart-only outcomes
- IWM aggregate closeout
- GLD broader coverage
- Continuous Watcher behavior
- alert suppression
- shadow/live validation
- option P&L
- account sizing
- production readiness
