# QQQ Continuation Real Historical Replay v1 Fixture Design Review

## Scope

- **Baseline:** patch8
- **Latest local commit noted for this task:** `e2b7577 Add QQQ Continuation source window selection`
- **Source CSV used:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`
- **Selection review used:** `historical_signal_replay/source_data/QQQ_CONTINUATION_WINDOW_SELECTION_REVIEW.md`
- **Planning review used:** `historical_signal_replay/QQQ_REAL_HISTORICAL_REPLAY_V1_PLANNING_REVIEW.md`
- **Coverage plan used:** `SAFE_FAST_BROADER_CHART_OUTCOME_BACKTESTING_COVERAGE_PLAN.md`
- **Purpose:** design the QQQ Continuation real historical replay v1 fixture from the selected QQQ source-data window.

This is design only. It does not create the fixture, change OHLCV data, fabricate source rows, fabricate final labels, start chart outcome calculations, model option P&L, add account sizing, modify `main.py`, change schemas, change runner code, change chart outcome code, or start watcher implementation.

## Design Status

- **Design status:** PASS
- **Reason:** the selected QQQ window contains enough real completed 1H RTH rows to design a bounded Continuation candidate signal/stage/lifecycle fixture while preserving row-by-row no-hindsight boundaries.

## Source Window

- **Source CSV used:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`
- **Symbol:** QQQ
- **Timeframe:** 1h_rth
- **Selected timestamp window:** 2026-04-20T09:30:00-04:00 through 2026-05-01T15:30:00-04:00
- **Selected row count:** 70
- **Setup family candidate:** Continuation

## Source-Only Read

- 2026-04-17 prior context closed the already reviewed upside run at 648.78 after reaching 650.00.
- 2026-04-20 pulls back and starts a shelf/base attempt in the mid-640s, trading from 642.52 to 648.76 and closing at 646.80.
- 2026-04-21 retests the same area, reaches 650.20 early, sells to 642.21 by the close, and still remains within the broader post-impulse continuation area rather than adding a new clean fast-break-only profile.
- 2026-04-22 recovers above the 04-20/04-21 shelf area, presses from 650.15 to 655.33, and closes at 655.08.
- 2026-04-23 probes higher to 656.92, then shakes down into 645.525 before closing at 651.41, giving useful no-hindsight context for a tested/rebuilt Continuation state.
- 2026-04-24 gaps/reclaims above the 04-22 and 04-23 highs, reaches 664.51, and closes at 663.91.
- 2026-04-27 holds a narrow higher base around 660.69 to 664.42 and closes at 664.27.
- 2026-04-28 pulls back to 653.81 and rebuilds into a 657.57 close without using later 04-30 or 05-01 strength.
- 2026-04-29 firms in the upper 650s/low 660s and closes at 661.61.
- 2026-04-30 reclaims and extends above the prior higher-base area, reaching 668.75 and closing at 667.60.
- 2026-05-01 pushes to 675.97 and closes at 674.16; this can represent later spent/follow-through context only, not a trade outcome or profitability conclusion.
- The source CSV contains 24H/daily, macro, IV, and event context as explicitly unconfirmed; the future fixture should preserve those unconfirmed statuses.

## Proposed Fixture Row Design

- **Proposed fixture row count:** 6
- **Fixture type:** QQQ Continuation candidate signal/stage/lifecycle fixture
- **Input design:** each fixture row should include QQQ source candles only through that row timestamp, copied exactly from the source CSV with no OHLCV edits.
- **Output design:** expected output labels should be treated as fixture assertions derived from row-by-row no-hindsight review, not as source-data labels.

Proposed rows:

| Row | Timestamp | Proposed row role | Source-only basis |
| --- | --- | --- | --- |
| 1 | 2026-04-20T15:30:00-04:00 | `watching_continuation_pullback_shelf_developing` | Completed rows through 04-20 show a pullback/base attempt after the prior upside run, with the session holding the mid-640s and closing at 646.80; no 04-21 retest, 04-22 recovery, or later push is available to this row. |
| 2 | 2026-04-21T15:30:00-04:00 | `watching_continuation_shelf_retest_no_trigger` | Completed rows through 04-21 show a second test of the shelf/base area from 650.20 down to 642.21 and a 644.28 close, but no completed recovery above the shelf is available yet. |
| 3 | 2026-04-22T15:30:00-04:00 | `continuation_recovery_above_shelf_candidate` | Completed rows through 04-22 show a recovery above the 04-20/04-21 shelf area and a 655.08 close after a 655.33 high, without using the 04-23 shake or 04-24 higher push. |
| 4 | 2026-04-24T15:30:00-04:00 | `continuation_higher_base_rebuild_candidate` | Completed rows through 04-24 include the 04-23 shake and 04-24 recovery to 664.51/663.91, supporting a rebuilt higher-base Continuation candidate without using 04-27 through 05-01 rows. |
| 5 | 2026-04-30T15:30:00-04:00 | `continuation_triggered_signal_stage_candidate` | Completed rows through 04-30 show the 04-27 higher base, 04-28 pullback, 04-29 firming, and 04-30 completed push to 668.75/667.60 above the higher-base area; no 05-01 push is available to this row. |
| 6 | 2026-05-01T15:30:00-04:00 | `continuation_spent_or_follow_through_no_fresh_trigger` | The selected window has extended to 675.97 after the earlier 04-30 completed push; this row can represent spent/follow-through/no-fresh-trigger context without asserting trade outcome, P&L, or execution results. |

## Proposed Lifecycle / Stage Sequence

1. `watching_continuation_pullback_shelf_developing`
2. `watching_continuation_shelf_retest_no_trigger`
3. `continuation_recovery_above_shelf_candidate`
4. `continuation_higher_base_rebuild_candidate`
5. `continuation_triggered_signal_stage_candidate`
6. `continuation_spent_or_follow_through_no_fresh_trigger`

The future fixture should decide final exact enum/string values from existing signal replay conventions, but the intended lifecycle path is:

- post-impulse Continuation pullback/shelf developing
- shelf retest with no fresh completed trigger
- recovery above the shelf candidate
- higher-base rebuild candidate after a shake
- completed Continuation trigger-stage candidate
- spent/follow-through/no-fresh-trigger state

## No-Hindsight Reasoning

- **No-hindsight result:** PASS
- Each proposed row uses only source rows at or before that row timestamp.
- Row 1 does not use the later 04-21 retest, 04-22 recovery, 04-24 higher-base push, 04-30 completed push, or 05-01 extension.
- Row 2 does not use the later 04-22 recovery, 04-24 higher-base push, 04-30 completed push, or 05-01 extension to label the shelf retest successful.
- Row 3 may use completed bars through 2026-04-22T15:30:00-04:00 only and must not assume the 04-23 shake, 04-24 recovery, or later higher-base behavior.
- Row 4 may use completed bars through 2026-04-24T15:30:00-04:00 only and must not use the 04-27 hold, 04-28 pullback, 04-30 push, or 05-01 extension.
- Row 5 may use completed bars through 2026-04-30T15:30:00-04:00 only and must not use the 05-01 high or close.
- Row 6 may acknowledge that the earlier 04-30 completed push is no longer fresh, but it must not include profitability, option behavior, trade outcome, or account-sizing conclusions.
- 24H/daily, macro, IV, and event context remains unconfirmed because the source CSV does not provide confirmed context values.

## Expected Output Fields

The future fixture should include expected output fields consistent with existing Historical Signal Replay v1 lifecycle fixtures:

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

## Duplicate / State-Change Plan

- Row 1 should establish the first QQQ Continuation pullback/shelf observation for the proposed fixture.
- Row 2 should be a meaningful change from initial pullback/shelf to retested shelf/no-trigger state.
- Row 3 should be a meaningful change to recovery-above-shelf candidate state.
- Row 4 should be a meaningful change to higher-base/rebuild candidate after the 04-23 shake and 04-24 recovery.
- Row 5 should be a meaningful change to completed trigger-stage candidate after the 04-30 push.
- Row 6 should be a meaningful change to spent/follow-through/no-fresh-trigger state.
- Duplicate alert suppression keys should change only when state, stage, trigger, or blocker meaning changes; any repeated higher-base or no-trigger state should reuse the prior meaningful key if the final fixture uses the same session/date key policy.

## Known Limits

- This design does not create the fixture.
- This design does not finalize engine labels; it proposes fixture row roles for the next approved fixture-creation task.
- The source window is completed 1H RTH OHLCV only. It cannot prove intrabar pending behavior unless the fixture explicitly treats pending language as completed-bar review state.
- The Continuation setup-family candidate is a design candidate from source-window shape only, not a fabricated source-data label.
- 24H/daily, macro, IV, event, headline, wall-thesis, room, and extension details are unconfirmed unless represented by existing fixture conventions.
- The design does not prove profitability, chart outcome quality, option P&L, account sizing, production readiness, watcher readiness, alert quality, live trade decisions, order routing, or broker execution behavior.

## Watcher Deferral

- **Watcher remains deferred:** yes
- **Watcher implementation started:** no
- **Reason:** this task only designs a future QQQ Continuation replay fixture. QQQ Continuation fixture creation, historical replay output validation, chart outcome calculation, aggregate QQQ coverage, and broader QQQ/IWM/GLD coverage remain incomplete.

## Boundary Result

- **Boundary result:** PASS
- **Fixture created:** no
- **OHLCV data changed:** no
- **Fabricated labels added:** no
- **Chart outcome calculation started:** no
- **Option P&L modeled:** no
- **Account sizing added:** no
- **Watcher implementation started:** no
- **`main.py` changed:** no
- **Schemas changed:** no
- **Runner code changed:** no
- **Chart outcome code changed:** no

## Recommended Next Task

Create the QQQ Continuation real historical replay v1 fixture from this approved design, preserving exact source OHLCV rows and staying signal/stage/lifecycle only.
