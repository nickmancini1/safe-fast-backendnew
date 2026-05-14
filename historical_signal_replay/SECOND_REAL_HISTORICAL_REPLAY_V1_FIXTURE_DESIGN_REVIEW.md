# Second Real Historical Replay v1 Fixture Design Review

## Scope

- **Baseline:** patch8
- **Latest local commit noted for this task:** `e107eaf Add second real SPY source window selection`
- **Source CSV used:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`
- **Selection review used:** `historical_signal_replay/source_data/SECOND_REAL_SPY_WINDOW_SELECTION_REVIEW.md`
- **Purpose:** design the second real historical replay v1 fixture from the selected SPY source-data window.

This is design only. It does not create the fixture, change OHLCV data, fabricate source rows, fabricate final labels, start backtesting, model trade outcomes, model option P&L, add account sizing, modify trading logic, or change replay runner/test/schema behavior.

## Design Status

- **Design status:** PASS
- **Reason:** the selected window contains enough real completed 1H RTH SPY rows to design a bounded Ideal candidate signal/stage/lifecycle fixture while preserving no-hindsight row boundaries.

## Source Window

- **Source CSV used:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`
- **Symbol:** SPY
- **Timeframe:** 1h_rth
- **Selected timestamp window:** 2026-05-06T09:30:00-04:00 through 2026-05-13T14:30:00-04:00
- **Selected row count:** 41
- **Setup family candidate:** Ideal

## Source-Only Read

- 2026-05-06 opens with upward impulse behavior from 728.21 open to a 733.77 close, with the selected-window high reaching 734.58 by 15:30.
- 2026-05-07 pulls back from the 735-736 area into the 729.75-730.40 low area, then closes at 731.57. This preserves a higher-price structure relative to the 2026-05-06 open but does not by itself confirm a fresh Ideal trigger.
- 2026-05-08 and 2026-05-11 extend the advance, with the selected-window high reaching 740.75 at 2026-05-11T13:30:00-04:00.
- 2026-05-12 opens below the prior close and pulls back in a multi-bar sequence to 731.83-732.11 lows, then recovers into 738.20 by the close.
- 2026-05-13 opens near the recovered area, holds above the prior day's low area, and later extends to new selected-window highs through 743.90 by 13:30 before the selected window ends at 14:30.
- The source CSV contains unavailable 24H/daily, macro, IV, and event context as explicitly unconfirmed; the future fixture should preserve those unconfirmed statuses.

## Proposed Fixture Row Design

- **Proposed fixture row count:** 6
- **Fixture type:** second real SPY Ideal candidate signal/stage/lifecycle fixture
- **Input design:** each fixture row should include SPY source candles only through that row timestamp, copied exactly from the source CSV with no OHLCV edits.
- **Output design:** expected output labels should be treated as fixture assertions derived from row-by-row no-hindsight review, not as source-data labels.

Proposed rows:

| Row | Timestamp | Proposed row role | Source-only basis |
| --- | --- | --- | --- |
| 1 | 2026-05-11T13:30:00-04:00 | `watching_ideal_impulse_context` | The window has advanced from the 05-06 open into a 740.75 high; this provides pre-retest trend context only, with no pullback/retest row yet complete. |
| 2 | 2026-05-12T10:30:00-04:00 | `watching_ideal_pullback_retest_developing` | After the 05-11 high, SPY pulls back through 734.57 and 731.835 lows; using only rows through this timestamp, the retest is developing and no recovery trigger is confirmed. |
| 3 | 2026-05-12T12:30:00-04:00 | `watching_ideal_retest_hold_unconfirmed` | The 11:30 and 12:30 bars stop making materially lower lows and close back to 734.35, but the row should remain unconfirmed because later recovery and 05-13 highs are not yet available. |
| 4 | 2026-05-12T15:30:00-04:00 | `ideal_retest_recovery_confirmation_candidate` | Completed bars through the 05-12 close show recovery from the retest low area to 738.20; this can represent a signal-stage candidate without using 05-13 follow-through. |
| 5 | 2026-05-13T11:30:00-04:00 | `ideal_triggered_signal_stage_candidate` | The 05-13 11:30 completed bar closes at 741.725 above the prior selected-window high of 740.75, giving a fresh completed-bar breakout/reclaim candidate after the 05-12 retest. |
| 6 | 2026-05-13T14:30:00-04:00 | `ideal_follow_through_no_fresh_trigger` | The sequence has already followed through to a 743.90 high by 13:30; the 14:30 row can acknowledge no fresh first trigger without asserting trade outcome, P&L, or execution results. |

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

- Each proposed row uses only source rows at or before that row timestamp.
- Row 1 does not use the later 05-12 pullback or 05-13 breakout to label a completed Ideal.
- Row 2 does not use later 05-12 recovery bars or 05-13 highs to call the retest successful.
- Row 3 may observe that price has stopped making materially lower lows through 12:30, but it must not assume the 14:30/15:30 recovery or the next-session extension.
- Row 4 may use completed bars through 2026-05-12T15:30:00-04:00 only; it must not use 05-13 to validate the recovery.
- Row 5 may use completed bars through 2026-05-13T11:30:00-04:00 only and should be the first proposed fresh completed-bar signal-stage candidate.
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

- Row 1 should establish the first Ideal candidate observation for the proposed fixture.
- Row 2 should be a meaningful change from impulse context to developing pullback/retest.
- Row 3 can test a hold-unconfirmed state; if the future fixture keeps the same final state and blocker as row 2, it may instead be modeled as a repeated same-state duplicate-suppression row.
- Row 4 should be a meaningful change to recovery confirmation candidate if the final fixture treats the 05-12 close as a confirmed recovery state.
- Row 5 should be a meaningful change to triggered signal-stage candidate.
- Row 6 should be a meaningful change to follow-through/no-fresh-trigger state.
- Duplicate alert suppression keys should change only when state, stage, trigger, or blocker meaning changes; any repeated retest/developing row should reuse the prior meaningful key if the final fixture uses the same session/date key policy.

## Known Limits

- This design does not create the fixture.
- This design does not finalize engine labels; it proposes fixture row roles for the next approved fixture-creation task.
- The source window is completed 1H RTH OHLCV only. It cannot prove intrabar pending behavior unless the fixture explicitly treats pending language as completed-bar review state.
- 24H/daily, macro, IV, event, wall-thesis, room, and extension details are unconfirmed unless represented by existing fixture conventions.
- The Ideal setup-family candidate is a design candidate from source-window shape only, not a fabricated source-data label.
- The design does not prove profitability, trade outcome, option P&L, account sizing, production readiness, alert quality, live trade decisions, order routing, or broker execution behavior.

## Boundary Result

- **Boundary result:** PASS
- **Fixture created:** no
- **Backtesting started:** no
- **OHLCV data changed:** no
- **`main.py` changed:** no
- **`dxlink_candles.py` changed:** no
- **Replay tests changed:** no
- **Schemas changed:** no
- **Generated reports changed:** no
- **Runner code changed:** no

## Recommended Next Task

Create the second real historical replay v1 fixture from this approved design, preserving exact source OHLCV rows and staying signal/stage/lifecycle only.
