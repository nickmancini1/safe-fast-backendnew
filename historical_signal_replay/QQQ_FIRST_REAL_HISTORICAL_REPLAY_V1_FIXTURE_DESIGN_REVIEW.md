# QQQ First Real Historical Replay v1 Fixture Design Review

## Scope

- **Baseline:** patch8
- **Latest local commit noted for this task:** `251fadf Add QQQ first source window selection`
- **Source CSV used:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`
- **Selection review used:** `historical_signal_replay/source_data/QQQ_FIRST_WINDOW_SELECTION_REVIEW.md`
- **Planning review used:** `historical_signal_replay/QQQ_REAL_HISTORICAL_REPLAY_V1_PLANNING_REVIEW.md`
- **Coverage plan used:** `SAFE_FAST_BROADER_CHART_OUTCOME_BACKTESTING_COVERAGE_PLAN.md`
- **Purpose:** design the first QQQ real historical replay v1 fixture from the selected QQQ Ideal source-data window.

This is design only. It does not create the fixture, change OHLCV data, fabricate source rows, fabricate final labels, start chart outcome calculations, model option P&L, add account sizing, modify `main.py`, change schemas, change runner code, change chart outcome code, or start watcher implementation.

## Design Status

- **Design status:** PASS
- **Reason:** the selected QQQ window contains enough real completed 1H RTH rows to design a bounded Ideal candidate signal/stage/lifecycle fixture while preserving row-by-row no-hindsight boundaries.

## Source Window

- **Source CSV used:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`
- **Symbol:** QQQ
- **Timeframe:** 1h_rth
- **Selected timestamp window:** 2026-05-05T09:30:00-04:00 through 2026-05-14T15:30:00-04:00
- **Selected row count:** 56
- **Setup family candidate:** Ideal

## Source-Only Read

- 2026-05-05 forms pre-context/base rows around the 681-682 area, with the selected-session high at 682.7734 and close at 681.51.
- 2026-05-06 gaps higher and advances from a 687.75 open to a 695.575 close, establishing upside impulse context without requiring later rows.
- 2026-05-07 pauses and pulls back from the 701.23 high area into the 691.78-693.08 low area, then closes at 694.92.
- 2026-05-08 resumes upside progression and reaches 711.14 by the 15:30 row.
- 2026-05-11 extends the selected-window high to 714.59, then closes at 713.35 after a late-session pullback.
- 2026-05-12 opens below the prior close, pulls back in a multi-bar sequence to a 696.66 low by 12:30, then recovers to a 707.22 close.
- 2026-05-13 reclaims the pullback area and closes above the prior selected-window high by 12:30, then reaches 716.65 by 13:30.
- 2026-05-14 follows through to higher highs inside the selected window, reaching 722.03 by 11:30 and closing the selected range at 719.73.
- The source CSV contains 24H/daily, macro, IV, and event context as explicitly unconfirmed; the future fixture should preserve those unconfirmed statuses.

## Proposed Fixture Row Design

- **Proposed fixture row count:** 6
- **Fixture type:** first QQQ real Historical Signal Replay v1 Ideal candidate signal/stage/lifecycle fixture
- **Input design:** each fixture row should include QQQ source candles only through that row timestamp, copied exactly from the source CSV with no OHLCV edits.
- **Output design:** expected output labels should be treated as fixture assertions derived from row-by-row no-hindsight review, not as source-data labels.

Proposed rows:

| Row | Timestamp | Proposed row role | Source-only basis |
| --- | --- | --- | --- |
| 1 | 2026-05-08T15:30:00-04:00 | `watching_ideal_impulse_context` | Completed rows through 05-08 show QQQ advancing from the 05-05 base and 05-06 gap/impulse into a 711.14 high; no later 05-11 high or 05-12 pullback is available to this row. |
| 2 | 2026-05-12T10:30:00-04:00 | `watching_ideal_pullback_retest_developing` | After the 05-11 high, QQQ opens lower and pulls back through 704.94 and 699.48 lows; using only rows through this timestamp, the retest is developing and no recovery trigger is confirmed. |
| 3 | 2026-05-12T12:30:00-04:00 | `watching_ideal_retest_hold_unconfirmed` | The 12:30 row reaches the selected pullback low at 696.66 and closes at 700.235; the row can represent retest/hold review but must not assume the later 14:30-15:30 recovery. |
| 4 | 2026-05-12T15:30:00-04:00 | `ideal_retest_recovery_confirmation_candidate` | Completed bars through the 05-12 close recover from 696.66 to 707.22; this can represent a recovery-confirmation candidate without using 05-13 or 05-14 follow-through. |
| 5 | 2026-05-13T12:30:00-04:00 | `ideal_triggered_signal_stage_candidate` | Completed bars through 05-13 12:30 close at 714.805 reclaim the prior selected-window high of 714.59 after the 05-12 retest, giving the first proposed fresh completed-bar signal-stage candidate. |
| 6 | 2026-05-14T11:30:00-04:00 | `ideal_follow_through_no_fresh_trigger` | The sequence has already followed through to a 722.03 high after the earlier 05-13 trigger candidate; this row can acknowledge no fresh first trigger without asserting trade outcome, P&L, or execution results. |

## Proposed Lifecycle / Stage Sequence

1. `watching_ideal_impulse_context`
2. `watching_ideal_pullback_retest_developing`
3. `watching_ideal_retest_hold_unconfirmed`
4. `ideal_retest_recovery_confirmation_candidate`
5. `ideal_triggered_signal_stage_candidate`
6. `ideal_follow_through_no_fresh_trigger`

The future fixture should decide final exact enum/string values from existing signal replay conventions, but the intended lifecycle path is:

- trend-aligned Ideal candidate context
- pullback/retest developing
- retest hold still unconfirmed
- recovery confirmation candidate
- completed trigger/signal-stage candidate
- later follow-through/no-fresh-trigger state

## No-Hindsight Reasoning

- **No-hindsight result:** PASS
- Each proposed row uses only source rows at or before that row timestamp.
- Row 1 does not use the later 05-11 high, 05-12 pullback, or 05-13/05-14 recovery to label a completed Ideal.
- Row 2 does not use later 05-12 recovery bars or 05-13 highs to call the retest successful.
- Row 3 may observe the completed 12:30 retest low/close, but it must not assume the later 14:30/15:30 recovery.
- Row 4 may use completed bars through 2026-05-12T15:30:00-04:00 only; it must not use 05-13 reclaim/follow-through to validate the recovery.
- Row 5 may use completed bars through 2026-05-13T12:30:00-04:00 only and should be the first proposed fresh completed-bar signal-stage candidate.
- Row 6 may acknowledge that the earlier trigger candidate is no longer fresh, but it must not include profitability, option behavior, trade outcome, or account-sizing conclusions.
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

- Row 1 should establish the first QQQ Ideal candidate observation for the proposed fixture.
- Row 2 should be a meaningful change from impulse context to developing pullback/retest.
- Row 3 can test a hold-unconfirmed state; if the future fixture keeps the same final state and blocker as Row 2, it may instead be modeled as a repeated same-state duplicate-suppression row.
- Row 4 should be a meaningful change to recovery confirmation candidate if the final fixture treats the 05-12 close as a confirmed recovery state.
- Row 5 should be a meaningful change to triggered signal-stage candidate.
- Row 6 should be a meaningful change to follow-through/no-fresh-trigger state.
- Duplicate alert suppression keys should change only when state, stage, trigger, or blocker meaning changes; any repeated retest/developing row should reuse the prior meaningful key if the final fixture uses the same session/date key policy.

## Known Limits

- This design does not create the fixture.
- This design does not finalize engine labels; it proposes fixture row roles for the next approved fixture-creation task.
- The source window is completed 1H RTH OHLCV only. It cannot prove intrabar pending behavior unless the fixture explicitly treats pending language as completed-bar review state.
- The Ideal setup-family candidate is a design candidate from source-window shape only, not a fabricated source-data label.
- 24H/daily, macro, IV, event, headline, wall-thesis, room, and extension details are unconfirmed unless represented by existing fixture conventions.
- The design does not prove profitability, chart outcome quality, option P&L, account sizing, production readiness, watcher readiness, alert quality, live trade decisions, order routing, or broker execution behavior.

## Watcher Deferral

- **Watcher remains deferred:** yes
- **Watcher implementation started:** no
- **Reason:** this task only designs a future QQQ replay fixture. QQQ fixture creation, historical replay output validation, chart outcome calculation, aggregate QQQ coverage, and broader QQQ/IWM/GLD coverage remain incomplete.

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

Create the first QQQ real historical replay v1 fixture from this approved design, preserving exact source OHLCV rows and staying signal/stage/lifecycle only.
