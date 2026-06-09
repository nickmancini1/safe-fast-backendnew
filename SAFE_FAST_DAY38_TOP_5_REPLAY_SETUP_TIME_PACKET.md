# SAFE-FAST Day 38 Top 5 Replay Setup-Time Packet

Project day: Day 38
Baseline before packet: `9c9edb6 Add Day 38 kept candidates batch replay setup-time worksheet`
Mode: docs-only bounded replay/setup-time packet; all five kept candidates together; no proof accepted

## Purpose

Create one bounded replay/setup-time packet for the five kept Day 38 candidates together.

This packet is not proof. It does not accept replay signal/stage output, chart-only outcome, copied invalidation, directional movement, or prior review status as profitability proof.

## Files Read

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`
- `SAFE_FAST_DAY38_KEPT_CANDIDATES_BATCH_REPLAY_SETUP_TIME_WORKSHEET.md`
- `SAFE_FAST_DAY38_FULL_20_CANDIDATE_DEEP_BATCH_REVIEW.md`
- `SAFE_FAST_DAY38_TOP_5_CANDIDATES_DEEP_BATCH_REVIEW.md`
- `historical_signal_replay/REAL_HISTORICAL_REPLAY_V1_SPY_THREE_SETUP_CLOSEOUT_REVIEW.md`
- `historical_signal_replay/QQQ_IDEAL_REPLAY_EVIDENCE_AND_NEXT_STEP_REVIEW.md`
- `historical_signal_replay/QQQ_FIRST_REAL_HISTORICAL_REPLAY_V1_FIXTURE_DESIGN_REVIEW.md`
- `historical_signal_replay/QQQ_FIRST_REAL_HISTORICAL_REPLAY_V1_FIXTURE_CREATION_REVIEW.md`
- `historical_signal_replay/QQQ_CLEAN_FAST_BREAK_REPLAY_EVIDENCE_AND_NEXT_STEP_REVIEW.md`
- `historical_signal_replay/QQQ_CONTINUATION_REPLAY_EVIDENCE_AND_NEXT_STEP_REVIEW.md`
- `historical_signal_replay/reports/first_real_qqq_clean_fast_break_replay_v1_signal_log.jsonl`
- `historical_signal_replay/reports/first_real_qqq_continuation_replay_v1_signal_log.jsonl`
- `historical_signal_replay/reports/first_real_spy_continuation_replay_v1_signal_log.jsonl`
- `historical_signal_replay/reports/second_real_spy_ideal_replay_v1_signal_log.jsonl`
- `historical_signal_replay/reports/first_real_qqq_ideal_replay_v1_signal_log.jsonl`
- `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`
- `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`
- `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_FIRST_REAL_CALCULATION_REVIEW.md`
- `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_SECOND_REAL_CALCULATION_REVIEW.md`
- `SAFE_FAST_QQQ_IDEAL_CHART_OUTCOME_CALCULATION_REVIEW.md`
- `SAFE_FAST_QQQ_CLEAN_FAST_BREAK_CHART_OUTCOME_CALCULATION_REVIEW.md`
- `SAFE_FAST_QQQ_CONTINUATION_CHART_OUTCOME_CALCULATION_REVIEW.md`

## Packet Guardrails

- Keep all five candidates in this one packet.
- Do not invent evidence.
- Do not accept proof.
- Do not claim profitability.
- Treat replay signal/stage rows as setup-time input only.
- Treat chart-only terminal outcome as request/review input only.
- Keep no-hindsight boundaries separate from after-setup outcome.
- If a requested field is not repo-backed, mark it `TO_FILL` or `UNAVAILABLE`.

## Batch Candidates

### `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`

- candidate_id: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`
- symbol: QQQ
- setup_type: Clean Fast Break
- exact source file: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`
- exact row/window reference: source CSV line 132, `2026-04-13T12:30:00-04:00`; replay signal log `historical_signal_replay/reports/first_real_qqq_clean_fast_break_replay_v1_signal_log.jsonl` row 3; source window repo-backed as `2026-04-08T09:30:00-04:00` through `2026-04-13T12:30:00-04:00`.
- setup-time row request: use only the completed source CSV row at line 132 and replay signal-log row 3 as the setup-time packet row; preserve this as setup-time input only.
- trigger request: carry `trigger_state=triggered`, `trigger_level=613.67`, `trigger_changed=true`, `final_verdict=TRADE`, `stage=clean_fast_break_initial_break_candidate`, and `setup_state=initial_break_candidate`; do not treat the verdict label as proof or execution instruction.
- invalidation request: carry copied invalidation `609.58`; confirm it remains the pre-entry invalidation for this request and not an after-outcome adjustment.
- freshness request: mark signal/stage freshness present only at replay layer; setup-specific stale/spent and gap-context freshness rules remain `TO_FILL`.
- blocker request: carry `primary_blocker=null`, `cautions_watchouts=[MACRO_UNCONFIRMED, IV_UNCONFIRMED, EVENT_UNCONFIRMED]`, `context_24h=CONTEXT_24H_DAILY_UNCONFIRMED`, `room_status=unconfirmed`, `wall_thesis_fit=unconfirmed`, and `extension_status=unconfirmed`; gap context, option, account, broker, and execution blockers remain `TO_FILL`.
- no-hindsight request: use only source rows and replay fields available through `2026-04-13T12:30:00-04:00`; do not use the `2026-04-13T15:30:00-04:00` follow-through row or chart outcome to justify setup identity.
- terminal chart-only outcome request: carry the existing QQQ Clean Fast Break chart-only outcome review as request input only: entry at next eligible candle open `2026-04-13T13:30:00-04:00`, copied invalidation not reached, terminal follow-through at `2026-04-13T15:30:00-04:00`, same-day classification, no option P&L, no account sizing, no broker/order execution.
- what is already repo-backed: exact source CSV line 132; setup-time timestamp and stage; replay signal-log row 3; trigger state and level; copied invalidation; primary blocker null; unconfirmed macro/IV/event/24H contexts; chart-only outcome review boundary.
- what still must be filled: setup-specific stale/spent rule, gap-context review, complete blocker/caution review, no-hindsight packet signoff, repeatability rows, economics, option performance, spread/slippage/fill, account risk, execution path, and entry/exit usefulness.
- fastest next action: add repeat QQQ Clean Fast Break rows in batch form after this packet, with the same setup-time, trigger, invalidation, freshness, blocker, no-hindsight, and chart-only terminal outcome request fields.

### `QQQ-REAL-HISTORICAL-CONTINUATION-001`

- candidate_id: `QQQ-REAL-HISTORICAL-CONTINUATION-001`
- symbol: QQQ
- setup_type: Continuation
- exact source file: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`
- exact row/window reference: source CSV line 226, `2026-04-30T15:30:00-04:00`; replay signal log `historical_signal_replay/reports/first_real_qqq_continuation_replay_v1_signal_log.jsonl` row 5; source window repo-backed as `2026-04-20T09:30:00-04:00` through `2026-04-30T15:30:00-04:00`.
- setup-time row request: use only the completed source CSV row at line 226 and replay signal-log row 5 as the setup-time packet row; preserve next-session outcome as separate after-setup input only.
- trigger request: carry `trigger_state=triggered`, `trigger_level=664.51`, `trigger_changed=true`, `final_verdict=TRADE`, `stage=continuation_triggered_signal_stage_candidate`, and `setup_state=signal_stage`; do not treat the verdict label as proof or execution instruction.
- invalidation request: carry copied invalidation `653.81`; confirm it remains the pre-entry invalidation for this request and not an after-outcome adjustment.
- freshness request: mark signal/stage freshness present only at replay layer; next-session entry freshness remains `TO_FILL` and must be decided before any promotion.
- blocker request: carry `primary_blocker=null`, `cautions_watchouts=[MACRO_UNCONFIRMED, IV_UNCONFIRMED, EVENT_UNCONFIRMED]`, `context_24h=CONTEXT_24H_DAILY_UNCONFIRMED`, `room_status=unconfirmed`, `wall_thesis_fit=unconfirmed`, and `extension_status=unconfirmed`; session-boundary, option, account, broker, and execution blockers remain `TO_FILL`.
- no-hindsight request: use only source rows and replay fields available through `2026-04-30T15:30:00-04:00`; do not use `2026-05-01` outcome rows to justify setup identity or freshness.
- terminal chart-only outcome request: carry the existing QQQ Continuation chart-only outcome review as request input only: entry at next eligible session open `2026-05-01T09:30:00-04:00`, copied invalidation not reached, terminal follow-through at `2026-05-01T09:30:00-04:00`, same-day classification from the entry session, no option P&L, no account sizing, no broker/order execution.
- what is already repo-backed: exact source CSV line 226; setup-time timestamp and stage; replay signal-log row 5; trigger state and level; copied invalidation; primary blocker null; unconfirmed macro/IV/event/24H contexts; chart-only next-session outcome review boundary.
- what still must be filled: next-session freshness rule, session-boundary blocker review, complete blocker/caution review, no-hindsight packet signoff, repeatability rows, economics, option performance, spread/slippage/fill, account risk, execution path, and entry/exit usefulness.
- fastest next action: test QQQ Continuation next-session freshness in batch form before any promotion, then add repeat QQQ Continuation rows.

### `SPY-REAL-HISTORICAL-CONTINUATION-001`

- candidate_id: `SPY-REAL-HISTORICAL-CONTINUATION-001`
- symbol: SPY
- setup_type: Continuation
- exact source file: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`
- exact row/window reference: source CSV line 229, `2026-04-30T12:30:00-04:00`; replay signal log `historical_signal_replay/reports/first_real_spy_continuation_replay_v1_signal_log.jsonl` row 5; source window repo-backed as `2026-04-24T09:30:00-04:00` through `2026-04-30T15:30:00-04:00`.
- setup-time row request: use only the completed source CSV row at line 229 and replay signal-log row 5 as the setup-time packet row; preserve later same-day follow-through as separate after-setup input only.
- trigger request: carry `trigger_state=triggered`, `trigger_level=715.61`, `trigger_changed=true`, `final_verdict=TRADE`, `stage=triggered_signal_stage_candidate`, and `setup_state=signal_stage`; do not treat the verdict label as proof or execution instruction.
- invalidation request: carry copied pre-entry invalidation `708.37`; confirm it remains the pre-entry invalidation for this request and not an after-outcome adjustment.
- freshness request: mark signal/stage freshness present only at replay layer; setup-specific stale/spent and finer intrabar ordering rules remain `TO_FILL`.
- blocker request: carry `primary_blocker=null`, `cautions_watchouts=[MACRO_UNCONFIRMED, IV_UNCONFIRMED, EVENT_UNCONFIRMED]`, `context_24h=CONTEXT_24H_DAILY_UNCONFIRMED`, `room_status=unconfirmed`, `wall_thesis_fit=unconfirmed`, and `extension_status=unconfirmed`; macro, IV, event, headline, option, account, broker, execution, and finer intrabar context remain `TO_FILL`.
- no-hindsight request: use only source rows and replay fields available through `2026-04-30T12:30:00-04:00`; do not use the later `2026-04-30T13:30:00-04:00` chart outcome to justify setup identity.
- terminal chart-only outcome request: carry the existing SPY Continuation chart-only outcome review as request input only: entry at `2026-04-30T13:30:00-04:00`, copied invalidation not reached, terminal follow-through at `2026-04-30T13:30:00-04:00`, same-day classification, no option P&L, no account sizing, no broker/order execution.
- what is already repo-backed: exact source CSV line 229; setup-time timestamp and stage; replay signal-log row 5; trigger state and level; copied invalidation; primary blocker null; unconfirmed macro/IV/event/24H contexts; chart-only outcome review boundary.
- what still must be filled: setup-specific stale/spent rule, finer intrabar ordering review, complete blocker/caution review, no-hindsight packet signoff, repeatability rows, economics, option performance, spread/slippage/fill, account risk, execution path, and entry/exit usefulness.
- fastest next action: add repeat SPY Continuation rows before treating this as more than one selected review anchor.

### `SPY-REAL-HISTORICAL-IDEAL-001`

- candidate_id: `SPY-REAL-HISTORICAL-IDEAL-001`
- symbol: SPY
- setup_type: Ideal
- exact source file: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`
- exact row/window reference: source CSV line 291, `2026-05-13T11:30:00-04:00`; replay signal log `historical_signal_replay/reports/second_real_spy_ideal_replay_v1_signal_log.jsonl` row 5; source window repo-backed as `2026-05-06T09:30:00-04:00` through `2026-05-13T14:30:00-04:00`.
- setup-time row request: use only the completed source CSV row at line 291 and replay signal-log row 5 as the setup-time packet row; preserve later same-day follow-through as separate after-setup input only.
- trigger request: carry `trigger_state=triggered`, `trigger_level=740.75`, `trigger_changed=true`, `final_verdict=TRADE`, `stage=ideal_triggered_signal_stage_candidate`, and `setup_state=signal_stage`; do not treat the verdict label as proof or execution instruction.
- invalidation request: carry copied pre-entry invalidation `731.83`; confirm it remains the pre-entry invalidation for this request and not an after-outcome adjustment.
- freshness request: mark signal/stage freshness present only at replay layer; setup-specific stale/spent rules remain `TO_FILL`.
- blocker request: carry `primary_blocker=null`, `cautions_watchouts=[MACRO_UNCONFIRMED, IV_UNCONFIRMED, EVENT_UNCONFIRMED]`, `context_24h=CONTEXT_24H_DAILY_UNCONFIRMED`, `room_status=unconfirmed`, `wall_thesis_fit=unconfirmed`, and `extension_status=unconfirmed`; gap context, option, account, broker, and execution blockers remain `TO_FILL`.
- no-hindsight request: use only source rows and replay fields available through `2026-05-13T11:30:00-04:00`; do not use the later `2026-05-13T12:30:00-04:00` entry/outcome row to justify setup identity.
- terminal chart-only outcome request: carry the existing SPY Ideal chart-only outcome review as request input only: entry at `2026-05-13T12:30:00-04:00`, copied invalidation not reached, terminal follow-through at `2026-05-13T13:30:00-04:00`, same-day classification, no option P&L, no account sizing, no broker/order execution.
- what is already repo-backed: exact source CSV line 291; setup-time timestamp and stage; replay signal-log row 5; trigger state and level; copied invalidation; primary blocker null; unconfirmed macro/IV/event/24H contexts; chart-only outcome review boundary.
- what still must be filled: setup-specific stale/spent rule, gap-context review, complete blocker/caution review, no-hindsight packet signoff, repeatability rows, economics, option performance, spread/slippage/fill, account risk, execution path, proof that modest chart R remains useful after costs and timing, and entry/exit usefulness.
- fastest next action: add more SPY Ideal rows before treating this as more than one selected review anchor.

### `QQQ-REAL-HISTORICAL-IDEAL-001`

- candidate_id: `QQQ-REAL-HISTORICAL-IDEAL-001`
- symbol: QQQ
- setup_type: Ideal
- exact source file: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`
- exact row/window reference: source CSV line 286, `2026-05-13T12:30:00-04:00`; replay signal log `historical_signal_replay/reports/first_real_qqq_ideal_replay_v1_signal_log.jsonl` row 5; selected source window repo-backed as `2026-05-05T09:30:00-04:00` through `2026-05-14T15:30:00-04:00`, with fixture row 5 stopping at `2026-05-13T12:30:00-04:00`.
- setup-time row request: use only the completed source CSV row at line 286 and replay signal-log row 5 as the setup-time packet row; preserve next-session/fast-swing outcome as separate after-setup input only.
- trigger request: carry `trigger_state=triggered`, `trigger_level=714.59`, `trigger_changed=true`, `final_verdict=TRADE`, `stage=ideal_triggered_signal_stage_candidate`, and `setup_state=signal_stage`; do not treat the verdict label as proof or execution instruction.
- invalidation request: carry copied invalidation `696.66`; confirm it remains the pre-entry invalidation for this request and not an after-outcome adjustment.
- freshness request: mark signal/stage freshness present only at replay layer; fast-swing hold and setup-specific stale/spent rules remain `TO_FILL`.
- blocker request: carry `primary_blocker=null`, `cautions_watchouts=[MACRO_UNCONFIRMED, IV_UNCONFIRMED, EVENT_UNCONFIRMED]`, `context_24h=CONTEXT_24H_DAILY_UNCONFIRMED`, `room_status=unconfirmed`, `wall_thesis_fit=unconfirmed`, and `extension_status=unconfirmed`; wide chart-risk distance, macro, IV, event, headline, option, account, broker, execution, and fast-swing hold context remain `TO_FILL`.
- no-hindsight request: use only source rows and replay fields available through `2026-05-13T12:30:00-04:00`; do not use the `2026-05-14` fast-swing outcome to justify setup identity or hold freshness.
- terminal chart-only outcome request: carry the existing QQQ Ideal chart-only outcome review as request input only: entry at `2026-05-13T13:30:00-04:00`, copied invalidation not reached, terminal follow-through at `2026-05-14T09:30:00-04:00`, fast-swing classification, likely chart risk noted as chart-only, no option P&L, no account sizing, no broker/order execution.
- what is already repo-backed: exact source CSV line 286; setup-time timestamp and stage; replay signal-log row 5; trigger state and level; copied invalidation; primary blocker null; unconfirmed macro/IV/event/24H contexts; chart-only fast-swing outcome review boundary.
- what still must be filled: wide-risk usefulness review, fast-swing freshness/hold rule, complete blocker/caution review, no-hindsight packet signoff, repeatability rows, economics, option performance, spread/slippage/fill, account risk, execution path, and entry/exit usefulness.
- fastest next action: compare against additional QQQ Ideal rows and decide whether wide-risk Ideal signals are useful enough after freshness, blocker, and economics gaps are filled.

## Batch Summary

- total kept candidates in packet: 5
- exact source CSV row references filled: 5
- replay signal-log rows filled: 5
- trigger fields carried: 5
- invalidation fields carried: 5
- primary blocker fields carried: 5
- freshness fields still requiring setup-specific review: 5
- terminal chart-only outcome requests carried as request input only: 5
- candidates with accepted proof: 0
- profitability claim made: no

## Fastest Batch Next Action

Prioritize QQQ Clean Fast Break and QQQ Continuation repeat rows after this packet, while separately filling QQQ Continuation next-session freshness, QQQ Ideal fast-swing/wide-risk usefulness, complete blocker/caution review, and no-hindsight signoff for all five.

## Guardrail Result

- No accepted proof was created.
- No profitability claim was made.
- Directional movement was not accepted as proof.
- Chart-only terminal outcome remains request/review input only.
- Replay signal/stage/lifecycle output remains setup-time input only.
- Unit tests were not run by instruction.
