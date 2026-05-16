# QQQ Clean Fast Break Real Historical Replay v1 Fixture Design Review

## Scope

- **Baseline:** patch8
- **Latest local commit noted for this task:** `6d46545 Add QQQ Clean Fast Break source window selection`
- **Source CSV used:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`
- **Selection review used:** `historical_signal_replay/source_data/QQQ_CLEAN_FAST_BREAK_WINDOW_SELECTION_REVIEW.md`
- **Planning review used:** `historical_signal_replay/QQQ_REAL_HISTORICAL_REPLAY_V1_PLANNING_REVIEW.md`
- **Coverage plan used:** `SAFE_FAST_BROADER_CHART_OUTCOME_BACKTESTING_COVERAGE_PLAN.md`
- **Purpose:** design the QQQ Clean Fast Break real historical replay v1 fixture from the selected QQQ source-data window.

This is design only. It does not create the fixture, change OHLCV data, fabricate source rows, fabricate final labels, start chart outcome calculations, model option P&L, add account sizing, modify `main.py`, change schemas, change runner code, change chart outcome code, or start watcher implementation.

## Design Status

- **Design status:** PASS
- **Reason:** the selected QQQ window contains enough real completed 1H RTH rows to design a bounded Clean Fast Break candidate signal/stage/lifecycle fixture while preserving row-by-row no-hindsight boundaries.

## Source Window

- **Source CSV used:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`
- **Symbol:** QQQ
- **Timeframe:** 1h_rth
- **Selected timestamp window:** 2026-04-08T09:30:00-04:00 through 2026-04-17T15:30:00-04:00
- **Selected row count:** 56
- **Setup family candidate:** Clean Fast Break

## Source-Only Read

- 2026-04-08 provides pre-pause impulse/context rows after prior-window weakness, with the selected session trading from 602.13 to 609.89 and closing at 605.92.
- 2026-04-09 starts to reclaim the range and closes at 610.08 after reaching 610.50.
- 2026-04-10 forms the compact pause/base, with the selected session contained from 609.58 to 613.67 and closing at 611.02.
- 2026-04-13 reclaims the pause area, closes above the 04-10 613.67 high during the 12:30 completed row, and reaches 617.96 by the 15:30 row.
- 2026-04-14 gaps above the 04-13 close and continues higher from the 620 area to a 628.60 high.
- 2026-04-15 extends the post-break sequence to 637.65 by the close.
- 2026-04-16 pauses and digests the advance between 635.255 and 642.18 while holding above the original break zone.
- 2026-04-17 continues bounded follow-through to a 650.00 high and closes the selected window at 648.78.
- The source CSV contains 24H/daily, macro, IV, and event context as explicitly unconfirmed; the future fixture should preserve those unconfirmed statuses.

## Proposed Fixture Row Design

- **Proposed fixture row count:** 6
- **Fixture type:** QQQ Clean Fast Break candidate signal/stage/lifecycle fixture
- **Input design:** each fixture row should include QQQ source candles only through that row timestamp, copied exactly from the source CSV with no OHLCV edits.
- **Output design:** expected output labels should be treated as fixture assertions derived from row-by-row no-hindsight review, not as source-data labels.

Proposed rows:

| Row | Timestamp | Proposed row role | Source-only basis |
| --- | --- | --- | --- |
| 1 | 2026-04-08T15:30:00-04:00 | `watching_clean_fast_break_gap_impulse_context` | Completed rows through 04-08 show a wide pre-pause context day from 602.13 to 609.89; no later 04-09/04-10 pause or 04-13 break is available to this row. |
| 2 | 2026-04-10T15:30:00-04:00 | `watching_clean_fast_break_tight_pause_context` | Completed rows through 04-10 show a compact pause/base with 04-10 high 613.67, low 609.58, and close 611.02; no later break is available to this row. |
| 3 | 2026-04-13T12:30:00-04:00 | `clean_fast_break_initial_break_candidate` | Completed bars through 12:30 have reclaimed the pause area and closed at 614.60, above the 04-10 high of 613.67. |
| 4 | 2026-04-13T15:30:00-04:00 | `clean_fast_break_follow_through_confirming_context` | The 04-13 close at 617.32 extends beyond the initial completed break without using any 04-14 through 04-17 follow-through data. |
| 5 | 2026-04-16T13:30:00-04:00 | `watching_higher_base_after_fast_break` | After the 04-13 break and 04-14/04-15 advance, completed rows through 04-16 13:30 show digestion between 635.255 and 642.18 above the original break zone; no 04-17 follow-through is available to this row. |
| 6 | 2026-04-17T15:30:00-04:00 | `clean_fast_break_post_break_no_fresh_trigger` | The selected window has already followed through to a 650.00 high after the earlier 04-13 completed break; this row can represent post-break/spent context without asserting trade outcome, P&L, or execution results. |

## Proposed Lifecycle / Stage Sequence

1. `watching_clean_fast_break_gap_impulse_context`
2. `watching_clean_fast_break_tight_pause_context`
3. `clean_fast_break_initial_break_candidate`
4. `clean_fast_break_follow_through_confirming_context`
5. `watching_higher_base_after_fast_break`
6. `clean_fast_break_post_break_no_fresh_trigger`

The future fixture should decide final exact enum/string values from existing signal replay conventions, but the intended lifecycle path is:

- gap/impulse Clean Fast Break context
- tight-pause Clean Fast Break candidate context
- completed initial break candidate
- same-session follow-through context
- later higher-base or digestion watch state
- post-break/no-fresh-trigger state

## No-Hindsight Reasoning

- **No-hindsight result:** PASS
- Each proposed row uses only source rows at or before that row timestamp.
- Row 1 does not use the later 04-10 tight pause, 04-13 break, or 04-14 through 04-17 follow-through to call the context successful.
- Row 2 does not use the later 04-13 break or later follow-through to label the 04-10 pause as successful.
- Row 3 may use completed bars through 2026-04-13T12:30:00-04:00 only and must not assume the 04-13 close or any later follow-through.
- Row 4 may acknowledge completed 04-13 follow-through but must not use 04-14 gap/follow-through, 04-15 extension, 04-16 digestion, or 04-17 highs.
- Row 5 may use completed bars through 2026-04-16T13:30:00-04:00 only and must not assume the 04-17 continuation.
- Row 6 may acknowledge that the earlier 04-13 break is no longer fresh, but it must not include profitability, option behavior, trade outcome, or account-sizing conclusions.
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

- Row 1 should establish the first QQQ Clean Fast Break gap/impulse context observation for the proposed fixture.
- Row 2 should be a meaningful change from broad context to tight-pause candidate context.
- Row 3 should be a meaningful change to an initial completed break candidate.
- Row 4 should be a meaningful change to follow-through context, unless the final fixture treats Row 3 and Row 4 as one unchanged triggered state.
- Row 5 should be a meaningful change to a later higher-base or digestion watch state after the prior fast-break sequence has already developed.
- Row 6 should be a meaningful change to post-break/no-fresh-trigger state.
- Duplicate alert suppression keys should change only when state, stage, trigger, or blocker meaning changes; any repeated triggered/follow-through state should reuse the prior meaningful key if the final fixture uses the same session/date key policy.

## Known Limits

- This design does not create the fixture.
- This design does not finalize engine labels; it proposes fixture row roles for the next approved fixture-creation task.
- The source window is completed 1H RTH OHLCV only. It cannot prove intrabar pending behavior unless the fixture explicitly treats pending language as completed-bar review state.
- The Clean Fast Break setup-family candidate is a design candidate from source-window shape only, not a fabricated source-data label.
- 24H/daily, macro, IV, event, headline, wall-thesis, room, and extension details are unconfirmed unless represented by existing fixture conventions.
- The design does not prove profitability, chart outcome quality, option P&L, account sizing, production readiness, watcher readiness, alert quality, live trade decisions, order routing, or broker execution behavior.

## Watcher Deferral

- **Watcher remains deferred:** yes
- **Watcher implementation started:** no
- **Reason:** this task only designs a future QQQ Clean Fast Break replay fixture. QQQ Clean Fast Break fixture creation, historical replay output validation, chart outcome calculation, aggregate QQQ coverage, and broader QQQ/IWM/GLD coverage remain incomplete.

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

Create the QQQ Clean Fast Break real historical replay v1 fixture from this approved design, preserving exact source OHLCV rows and staying signal/stage/lifecycle only.
