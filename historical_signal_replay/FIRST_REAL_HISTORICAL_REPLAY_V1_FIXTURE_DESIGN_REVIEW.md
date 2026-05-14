# First Real Historical Replay v1 Fixture Design Review

## Scope

- **Baseline:** patch8
- **Latest local commit noted for this task:** `65ebee3 Add first real SPY source window selection`
- **Source CSV used:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`
- **Selection review used:** `historical_signal_replay/source_data/FIRST_REAL_SPY_WINDOW_SELECTION_REVIEW.md`
- **Purpose:** design the first real historical replay v1 fixture from the selected SPY source-data window.

This is design only. It does not create the fixture, change OHLCV data, fabricate source rows, start backtesting, model trade outcomes, model option P&L, add account sizing, modify trading logic, or change replay runner/test/schema behavior.

## Design Status

- **Design status:** PASS
- **Reason:** the selected window contains enough real completed 1H RTH SPY rows to design a bounded Continuation candidate signal/stage/lifecycle fixture while preserving no-hindsight row boundaries.

## Source Window

- **Source CSV used:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`
- **Symbol:** SPY
- **Timeframe:** 1h_rth
- **Selected timestamp window:** 2026-04-24T09:30:00-04:00 through 2026-04-30T15:30:00-04:00
- **Selected row count:** 35
- **Setup family candidate:** Continuation

## Source-Only Read

- 2026-04-24 through 2026-04-27 shows upside progression from the low 710s into the 715 area, with the selected-window high reaching 715.61 at 2026-04-27T15:30:00-04:00.
- 2026-04-28 through 2026-04-29 compresses mostly below the prior 715 area, with a two-session pullback/shelf range using observed lows around 708.37-710.79 and observed highs around 711.99-712.88.
- 2026-04-30 opens above the prior pullback/shelf area, fades back toward it, then closes progressively higher through 714.43, 715.18, 715.83, 717.88, 719.12, and 718.42.
- The source CSV contains unavailable 24H/daily, macro, IV, and event context as explicitly unconfirmed; the future fixture should preserve those unconfirmed statuses.

## Proposed Fixture Row Design

- **Proposed fixture row count:** 6
- **Fixture type:** first real SPY Continuation candidate signal/stage/lifecycle fixture
- **Input design:** each fixture row should include SPY source candles only through that row timestamp, copied exactly from the source CSV with no OHLCV edits.
- **Output design:** expected output labels should be treated as fixture assertions derived from the row-by-row no-hindsight review, not as source-data labels.

Proposed rows:

| Row | Timestamp | Proposed row role | Source-only basis |
| --- | --- | --- | --- |
| 1 | 2026-04-28T13:30:00-04:00 | `watching_developing_pullback_shelf` | After the 04-24/04-27 push, SPY has pulled back and is rebuilding below the prior 715 area; no completed break is present. |
| 2 | 2026-04-29T12:30:00-04:00 | `watching_developing_shelf_no_trigger` | The pullback/shelf remains bounded below the prior 715 area; no fresh completed trigger is present. |
| 3 | 2026-04-29T15:30:00-04:00 | `watching_developing_repeated_same_state` | The same developing shelf state persists into the close; this row can exercise no-duplicate behavior without a meaningful state change. |
| 4 | 2026-04-30T09:30:00-04:00 | `opening_probe_no_completed_approval` | The open/high probe above the prior shelf fades to a 712.01 close; the completed bar does not confirm follow-through above the broader prior 715 area. |
| 5 | 2026-04-30T12:30:00-04:00 | `triggered_signal_stage_candidate` | Completed bars have reclaimed the shelf and the 12:30 close at 715.83 is above the 04-27 selected-window high of 715.61. |
| 6 | 2026-04-30T15:30:00-04:00 | `spent_or_follow_through_no_fresh_trigger` | The move has already followed through to 719.79 high / 718.42 close after the earlier completed trigger candidate; fixture should not treat this as a fresh first trigger. |

## Proposed Lifecycle / Stage Sequence

1. `watching_developing_pullback_shelf`
2. `watching_developing_shelf_no_trigger`
3. `watching_developing_repeated_same_state`
4. `opening_probe_no_completed_approval`
5. `triggered_signal_stage_candidate`
6. `spent_or_follow_through_no_fresh_trigger`

The future fixture should decide final exact enum/string values from existing signal replay conventions, but the intended lifecycle path is:

- developing Continuation candidate
- repeated unchanged developing state
- incomplete or unapproved opening probe
- completed trigger/signal-stage candidate
- later spent/no-fresh-trigger state

## No-Hindsight Reasoning

- Each proposed row uses only source rows at or before that row timestamp.
- Row 1 does not use the later 04-29 or 04-30 break/follow-through to assert a confirmed trigger.
- Rows 2 and 3 do not use 04-30 data to call the shelf successful.
- Row 4 is evaluated as a completed 09:30 bar only; it should not invent intrabar state or assume later 10:30-15:30 follow-through.
- Row 5 may use completed bars through 2026-04-30T12:30:00-04:00 only.
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

- Rows 1 and 2 should be meaningful developing-state observations if their selected output fields differ.
- Row 3 should intentionally test repeated same-state handling: `state_changed: false`, `trigger_changed: false`, and `blocker_changed: false` if the future fixture keeps the same current state and blocker as row 2.
- Row 4 should be a meaningful change from developing shelf to opening-probe / no-completed-approval state.
- Row 5 should be a meaningful change to triggered signal-stage candidate.
- Row 6 should be a meaningful change to spent / no-fresh-trigger state.
- Duplicate alert suppression keys should change only when state, stage, trigger, or blocker meaning changes; the repeated developing row should reuse the prior meaningful key if the final fixture uses the same session/date key policy.

## Known Limits

- This design does not create the fixture.
- This design does not finalize engine labels; it proposes fixture row roles for the next approved fixture-creation task.
- The source window is completed 1H RTH OHLCV only. It cannot prove intrabar pending behavior unless the fixture explicitly treats pending language as completed-bar review state.
- 24H/daily, macro, IV, event, wall-thesis, room, and extension details are unconfirmed unless represented by existing fixture conventions.
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

Create the first real historical replay v1 fixture from this approved design, preserving exact source OHLCV rows and staying signal/stage/lifecycle only.
