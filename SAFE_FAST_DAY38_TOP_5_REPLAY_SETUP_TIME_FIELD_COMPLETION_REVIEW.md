# SAFE-FAST Day 38 Top 5 Replay Setup-Time Field Completion Review

Project day: Day 38
Baseline before review: `0b0c5c5 Add Day 38 top 5 replay setup-time packet`
Mode: docs-only field completion review; all five candidates together; no proof accepted

## Purpose

Fill the top-5 replay/setup-time packet as much as repo evidence allows.

This review does not accept proof, claim profitability, make trade decisions, or treat replay labels, copied invalidations, or chart-only outcomes as trading-system proof.

## Files Read

- `SAFE_FAST_DAY38_TOP_5_REPLAY_SETUP_TIME_PACKET.md`
- `SAFE_FAST_DAY38_KEPT_CANDIDATES_BATCH_REPLAY_SETUP_TIME_WORKSHEET.md`
- `SAFE_FAST_DAY38_FULL_20_CANDIDATE_DEEP_BATCH_REVIEW.md`
- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`
- `historical_signal_replay/reports/first_real_qqq_clean_fast_break_replay_v1_signal_log.jsonl`
- `historical_signal_replay/reports/first_real_qqq_continuation_replay_v1_signal_log.jsonl`
- `historical_signal_replay/reports/first_real_spy_continuation_replay_v1_signal_log.jsonl`
- `historical_signal_replay/reports/second_real_spy_ideal_replay_v1_signal_log.jsonl`
- `historical_signal_replay/reports/first_real_qqq_ideal_replay_v1_signal_log.jsonl`
- `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`
- `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`
- `SAFE_FAST_QQQ_CLEAN_FAST_BREAK_CHART_OUTCOME_CALCULATION_REVIEW.md`
- `SAFE_FAST_QQQ_CONTINUATION_CHART_OUTCOME_CALCULATION_REVIEW.md`
- `SAFE_FAST_QQQ_IDEAL_CHART_OUTCOME_CALCULATION_REVIEW.md`
- `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_FIRST_REAL_CALCULATION_REVIEW.md`
- `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_SECOND_REAL_CALCULATION_REVIEW.md`

## Field Status Rule

- `FILLED`: repo-backed field exists for setup-time packet use only.
- `UNCLEAR`: repo-backed partial evidence exists, but the required rule or review is not complete.
- `MISSING`: no repo-backed field was found.

## Field Completion Table

| candidate_id | exact source file | exact row/window reference | setup-time row | trigger | invalidation | freshness | blocker | no-hindsight boundary | terminal chart-only outcome | fastest next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | FILLED: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv` | FILLED: source CSV line 132, `2026-04-13T12:30:00-04:00`; replay signal-log row 3; source window `2026-04-08T09:30:00-04:00` through `2026-04-13T12:30:00-04:00`. | FILLED: source line 132 and replay row 3, `clean_fast_break_initial_break_candidate`, setup-time input only. | FILLED: `trigger_state=triggered`, `trigger_level=613.67`, `trigger_changed=true`, `final_verdict=TRADE`, `stage=clean_fast_break_initial_break_candidate`, `setup_state=initial_break_candidate`; not proof or execution instruction. | FILLED: copied invalidation `609.58`; repo-backed in replay row and chart-only review as copied invalidation not reached. | UNCLEAR: signal/stage freshness exists at replay layer, but setup-specific stale/spent and gap-context freshness rules remain unfilled. | UNCLEAR: primary blocker `null` is filled; macro/IV/event/24H contexts are unconfirmed; gap context, option, account, broker, execution, and complete caution review remain missing. | FILLED: use only rows and replay fields through `2026-04-13T12:30:00-04:00`; do not use `2026-04-13T15:30:00-04:00` follow-through or outcome to justify setup identity. | FILLED as chart-only input: entry `2026-04-13T13:30:00-04:00`; invalidation not reached; terminal follow-through `2026-04-13T15:30:00-04:00`; `same_day`; no option P&L, account sizing, broker/order execution. | FILLED: add repeat QQQ Clean Fast Break rows in batch form with the same field requirements. |
| `QQQ-REAL-HISTORICAL-CONTINUATION-001` | FILLED: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv` | FILLED: source CSV line 226, `2026-04-30T15:30:00-04:00`; replay signal-log row 5; source window `2026-04-20T09:30:00-04:00` through `2026-04-30T15:30:00-04:00`. | FILLED: source line 226 and replay row 5, `continuation_triggered_signal_stage_candidate`, setup-time input only. | FILLED: `trigger_state=triggered`, `trigger_level=664.51`, `trigger_changed=true`, `final_verdict=TRADE`, `stage=continuation_triggered_signal_stage_candidate`, `setup_state=signal_stage`; not proof or execution instruction. | FILLED: copied invalidation `653.81`; repo-backed in replay row and chart-only review as copied invalidation not reached. | UNCLEAR: signal/stage freshness exists at replay layer, but next-session entry freshness is unresolved. | UNCLEAR: primary blocker `null` is filled; macro/IV/event/24H contexts are unconfirmed; session-boundary, option, account, broker, execution, and complete caution review remain missing. | FILLED: use only rows and replay fields through `2026-04-30T15:30:00-04:00`; do not use `2026-05-01` outcome rows to justify setup identity or freshness. | FILLED as chart-only input: entry `2026-05-01T09:30:00-04:00`; invalidation not reached; terminal follow-through `2026-05-01T09:30:00-04:00`; entry-session `same_day`; no option P&L, account sizing, broker/order execution. | FILLED: test QQQ Continuation next-session freshness in batch form, then add repeat QQQ Continuation rows. |
| `SPY-REAL-HISTORICAL-CONTINUATION-001` | FILLED: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` | FILLED: source CSV line 229, `2026-04-30T12:30:00-04:00`; replay signal-log row 5; source window `2026-04-24T09:30:00-04:00` through `2026-04-30T15:30:00-04:00`. | FILLED: source line 229 and replay row 5, `triggered_signal_stage_candidate`, setup-time input only. | FILLED: `trigger_state=triggered`, `trigger_level=715.61`, `trigger_changed=true`, `final_verdict=TRADE`, `stage=triggered_signal_stage_candidate`, `setup_state=signal_stage`; not proof or execution instruction. | FILLED: copied pre-entry invalidation `708.37`; repo-backed in replay row and chart-only review as copied invalidation not reached. | UNCLEAR: signal/stage freshness exists at replay layer, but setup-specific stale/spent and finer intrabar ordering rules remain unfilled. | UNCLEAR: primary blocker `null` is filled; macro/IV/event/24H contexts are unconfirmed; headline, option, account, broker, execution, finer intrabar context, and complete caution review remain missing. | FILLED: use only rows and replay fields through `2026-04-30T12:30:00-04:00`; do not use later `2026-04-30T13:30:00-04:00` outcome to justify setup identity. | FILLED as chart-only input: entry `2026-04-30T13:30:00-04:00`; invalidation not reached; terminal follow-through `2026-04-30T13:30:00-04:00`; `same_day`; no option P&L, account sizing, broker/order execution. | FILLED: add repeat SPY Continuation rows before treating this as more than one selected review anchor. |
| `SPY-REAL-HISTORICAL-IDEAL-001` | FILLED: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` | FILLED: source CSV line 291, `2026-05-13T11:30:00-04:00`; replay signal-log row 5; source window `2026-05-06T09:30:00-04:00` through `2026-05-13T14:30:00-04:00`. | FILLED: source line 291 and replay row 5, `ideal_triggered_signal_stage_candidate`, setup-time input only. | FILLED: `trigger_state=triggered`, `trigger_level=740.75`, `trigger_changed=true`, `final_verdict=TRADE`, `stage=ideal_triggered_signal_stage_candidate`, `setup_state=signal_stage`; not proof or execution instruction. | FILLED: copied pre-entry invalidation `731.83`; repo-backed in replay row and chart-only review as copied invalidation not reached. | UNCLEAR: signal/stage freshness exists at replay layer, but setup-specific stale/spent rules remain unfilled. | UNCLEAR: primary blocker `null` is filled; macro/IV/event/24H contexts are unconfirmed; gap context, headline, option, account, broker, execution, and complete caution review remain missing. | FILLED: use only rows and replay fields through `2026-05-13T11:30:00-04:00`; do not use later `2026-05-13T12:30:00-04:00` entry/outcome row to justify setup identity. | FILLED as chart-only input: entry `2026-05-13T12:30:00-04:00`; invalidation not reached; terminal follow-through `2026-05-13T13:30:00-04:00`; `same_day`; no option P&L, account sizing, broker/order execution. | FILLED: add more SPY Ideal rows before treating this as more than one selected sample. |
| `QQQ-REAL-HISTORICAL-IDEAL-001` | FILLED: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv` | FILLED: source CSV line 286, `2026-05-13T12:30:00-04:00`; replay signal-log row 5; selected source window `2026-05-05T09:30:00-04:00` through `2026-05-14T15:30:00-04:00`, with fixture row 5 stopping at `2026-05-13T12:30:00-04:00`. | FILLED: source line 286 and replay row 5, `ideal_triggered_signal_stage_candidate`, setup-time input only. | FILLED: `trigger_state=triggered`, `trigger_level=714.59`, `trigger_changed=true`, `final_verdict=TRADE`, `stage=ideal_triggered_signal_stage_candidate`, `setup_state=signal_stage`; not proof or execution instruction. | FILLED: copied invalidation `696.66`; repo-backed in replay row and chart-only review as copied invalidation not reached. | UNCLEAR: signal/stage freshness exists at replay layer, but fast-swing hold and setup-specific stale/spent rules remain unfilled. | UNCLEAR: primary blocker `null` is filled; macro/IV/event/24H contexts are unconfirmed; wide chart-risk distance, headline, option, account, broker, execution, fast-swing hold context, and complete caution review remain missing. | FILLED: use only rows and replay fields through `2026-05-13T12:30:00-04:00`; do not use `2026-05-14` fast-swing outcome to justify setup identity or hold freshness. | FILLED as chart-only input: entry `2026-05-13T13:30:00-04:00`; invalidation not reached; terminal follow-through `2026-05-14T09:30:00-04:00`; `fast_swing`; likely chart risk noted as chart-only; no option P&L, account sizing, broker/order execution. | FILLED: compare against additional QQQ Ideal rows and decide whether wide-risk Ideal signals are useful enough after freshness, blocker, and economics gaps are filled. |

## Summary

- total reviewed: 5
- fully filled count: 0
- missing-field count: 10 incomplete required fields, counted as freshness plus blocker/caution review for each of the five candidates
- blocked count: 5 blocked from proof/promotion by incomplete freshness/final-signal rules, incomplete blocker/caution review, repeatability, economics, option performance, spread/slippage/fill, account risk, execution path, and entry/exit usefulness
- best candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`
- fastest next action: add repeat QQQ Clean Fast Break rows in batch form, while also testing QQQ Continuation next-session freshness and completing blocker/caution review for all five

## Guardrail Result

- No proof was accepted.
- No profitability claim was made.
- No trade decision was made.
- Directional movement was not accepted as proof.
- Chart-only terminal outcome remains review/input only.
- Replay signal/stage output remains setup-time input only.
- Unit tests were not run by instruction.
