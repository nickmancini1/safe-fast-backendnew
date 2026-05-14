# Third Real Historical Replay v1 Fixture Design Review

## Scope

- **Baseline:** patch8
- **Latest local commit noted for this task:** `f96729c Add third real SPY source window selection`
- **Source CSV used:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`
- **Selection review used:** `historical_signal_replay/source_data/THIRD_REAL_SPY_WINDOW_SELECTION_REVIEW.md`
- **Purpose:** design the third real historical replay v1 fixture from the selected SPY source-data window.

This is design only. It does not create the fixture, change OHLCV data, fabricate source rows, fabricate final labels, start backtesting, model trade outcomes, model option P&L, add account sizing, modify trading logic, or change replay runner/test/schema behavior.

## Design Status

- **Design status:** PASS
- **Reason:** the selected window contains enough real completed 1H RTH SPY rows to design a bounded Clean Fast Break candidate signal/stage/lifecycle fixture while preserving no-hindsight row boundaries.

## Source Window

- **Source CSV used:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`
- **Symbol:** SPY
- **Timeframe:** 1h_rth
- **Selected timestamp window:** 2026-04-10T09:30:00-04:00 through 2026-04-15T15:30:00-04:00
- **Selected row count:** 28
- **Setup family candidate:** Clean Fast Break

## Source-Only Read

- 2026-04-10 forms a tight pause after prior upside context, with selected-window prices contained between 678.45 and 682.03 and a close at 679.31.
- 2026-04-13 reclaims the prior pause area, breaks above the 04-10 selected-window high during the 12:30 row, and closes the session at 686.00 after reaching 686.295.
- 2026-04-14 gaps above the 04-13 close and follows through to the 694 area, holding above the 04-13 break zone for the full regular session.
- 2026-04-15 builds a tighter higher-price base from 09:30 through 13:30, then completes a fresh break above 700 during the 14:30 row and holds near that area into the close.
- The source CSV contains unavailable 24H/daily, macro, IV, and event context as explicitly unconfirmed; the future fixture should preserve those unconfirmed statuses.

## Proposed Fixture Row Design

- **Proposed fixture row count:** 6
- **Fixture type:** third real SPY Clean Fast Break candidate signal/stage/lifecycle fixture
- **Input design:** each fixture row should include SPY source candles only through that row timestamp, copied exactly from the source CSV with no OHLCV edits.
- **Output design:** expected output labels should be treated as fixture assertions derived from row-by-row no-hindsight review, not as source-data labels.

Proposed rows:

| Row | Timestamp | Proposed row role | Source-only basis |
| --- | --- | --- | --- |
| 1 | 2026-04-10T15:30:00-04:00 | `watching_clean_fast_break_tight_pause_context` | The 04-10 session is a bounded tight pause with selected-window high 682.03 and low 678.45; no later break is available to this row. |
| 2 | 2026-04-13T12:30:00-04:00 | `clean_fast_break_initial_break_candidate` | Completed bars through 12:30 have reclaimed the 04-10 pause and closed at 682.48, above the 04-10 high of 682.03. |
| 3 | 2026-04-13T15:30:00-04:00 | `clean_fast_break_follow_through_confirming_context` | The 04-13 close at 686.00 extends beyond the initial break without using any 04-14 or 04-15 data. |
| 4 | 2026-04-15T11:30:00-04:00 | `watching_higher_base_after_fast_break` | After the 04-13 and 04-14 advance, 04-15 holds a tight higher-price base below 698 using only completed rows through 11:30. |
| 5 | 2026-04-15T14:30:00-04:00 | `clean_fast_break_fresh_break_signal_candidate` | The completed 14:30 row breaks above the 04-15 base and reaches 700.03 with a 700.01 close; this is the first proposed fresh completed-bar signal-stage candidate for the higher base. |
| 6 | 2026-04-15T15:30:00-04:00 | `clean_fast_break_post_break_no_fresh_trigger` | The 15:30 row holds near the 700 area after the earlier 14:30 completed break; it should not be treated as a new first trigger. |

## Proposed Lifecycle / Stage Sequence

1. `watching_clean_fast_break_tight_pause_context`
2. `clean_fast_break_initial_break_candidate`
3. `clean_fast_break_follow_through_confirming_context`
4. `watching_higher_base_after_fast_break`
5. `clean_fast_break_fresh_break_signal_candidate`
6. `clean_fast_break_post_break_no_fresh_trigger`

The future fixture should decide final exact enum/string values from existing signal replay conventions, but the intended lifecycle path is:

- tight-pause Clean Fast Break candidate context
- completed initial break candidate
- same-session follow-through context
- later higher-base watch state
- completed fresh break/signal-stage candidate
- post-break/no-fresh-trigger state

## No-Hindsight Reasoning

- Each proposed row uses only source rows at or before that row timestamp.
- Row 1 does not use the later 04-13 reclaim/break to label the 04-10 pause as successful.
- Row 2 may use completed bars through 2026-04-13T12:30:00-04:00 only and must not assume the 04-13 close or any later follow-through.
- Row 3 may acknowledge completed 04-13 follow-through but must not use 04-14 gap/follow-through or 04-15 higher-base behavior.
- Row 4 may use completed bars through 2026-04-15T11:30:00-04:00 only and must not assume the later 14:30 break above 700.
- Row 5 may use completed bars through 2026-04-15T14:30:00-04:00 only and should be the first proposed fresh completed-bar signal-stage candidate for the 04-15 higher base.
- Row 6 may acknowledge that the earlier 14:30 break is no longer fresh, but it must not include profitability, option behavior, trade outcome, or account-sizing conclusions.
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

- Row 1 should establish the first Clean Fast Break tight-pause candidate observation for the proposed fixture.
- Row 2 should be a meaningful change from tight-pause context to an initial completed break candidate.
- Row 3 should be a meaningful change to follow-through context, unless the final fixture treats Row 2 and Row 3 as one unchanged triggered state.
- Row 4 should be a meaningful change to watching a later higher-base state after the prior fast-break sequence has already developed.
- Row 5 should be a meaningful change to a fresh completed break/signal-stage candidate above the 04-15 higher base.
- Row 6 should be a meaningful change to post-break/no-fresh-trigger state.
- Duplicate alert suppression keys should change only when state, stage, trigger, or blocker meaning changes; any repeated triggered/follow-through state should reuse the prior meaningful key if the final fixture uses the same session/date key policy.

## Known Limits

- This design does not create the fixture.
- This design does not finalize engine labels; it proposes fixture row roles for the next approved fixture-creation task.
- The source window is completed 1H RTH OHLCV only. It cannot prove intrabar pending behavior unless the fixture explicitly treats pending language as completed-bar review state.
- 24H/daily, macro, IV, event, wall-thesis, room, and extension details are unconfirmed unless represented by existing fixture conventions.
- The Clean Fast Break setup-family candidate is a design candidate from source-window shape only, not a fabricated source-data label.
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

Create the third real historical replay v1 fixture from this approved design, preserving exact source OHLCV rows and staying signal/stage/lifecycle only.
