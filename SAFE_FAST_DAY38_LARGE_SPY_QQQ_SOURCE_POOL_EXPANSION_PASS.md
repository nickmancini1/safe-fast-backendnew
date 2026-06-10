# SAFE-FAST Day 38 Large SPY/QQQ Source Pool Expansion Pass

Project day: Day 38
Baseline before review: `f6cb08e Preserve Day 38 speed discipline rule`
Mode: docs-only source-pool expansion; no proof accepted

## Purpose

Create a larger SPY/QQQ source-pool expansion pass without crawling one candidate at a time.

This pass uses local repo files only. It does not use live data, broker/order/account data, option data, alerts, Railway, production behavior, or trade decisions.

Directional movement, replay labels, copied invalidations, and source-visible follow-through are not accepted as proof.

## Files Read

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`
- `SAFE_FAST_DAY38_FULL_20_CANDIDATE_DEEP_BATCH_REVIEW.md`
- `SAFE_FAST_DAY38_TOP_5_REPLAY_SETUP_TIME_FIELD_COMPLETION_REVIEW.md`
- `SAFE_FAST_DAY38_QQQ_BLOCKER_RESOLUTION_REVIEW.md`
- `SAFE_FAST_DAY38_QQQ_REPLAY_READINESS_PACKET.md`
- `SAFE_FAST_DAY38_SPY_QQQ_SOURCE_WINDOW_CANDIDATE_PASS.md`
- `SAFE_FAST_PROFITABILITY_DEFINITION_AND_DECISION_POLICY_HARDENING_PLAN.md`
- `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`
- `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`
- `historical_signal_replay/source_data/FIRST_REAL_SPY_WINDOW_SELECTION_REVIEW.md`
- `historical_signal_replay/source_data/SECOND_REAL_SPY_WINDOW_SELECTION_REVIEW.md`
- `historical_signal_replay/source_data/THIRD_REAL_SPY_WINDOW_SELECTION_REVIEW.md`
- `historical_signal_replay/source_data/QQQ_FIRST_WINDOW_SELECTION_REVIEW.md`
- `historical_signal_replay/source_data/QQQ_CLEAN_FAST_BREAK_WINDOW_SELECTION_REVIEW.md`
- `historical_signal_replay/source_data/QQQ_CONTINUATION_WINDOW_SELECTION_REVIEW.md`
- `historical_signal_replay/reports/*_signal_log.jsonl`

## Search Scope

Searched local repo material for:

- `SPY`
- `QQQ`
- `Ideal`
- `Clean Fast Break`
- `Continuation`
- `source window`
- `replay readiness`
- `trigger`
- `invalidation`
- `freshness`
- `blocker`
- `outcome`
- `no-hindsight`

## Already Counted Or Protected Windows

These windows were treated as already counted, duplicate context, or protected prior lifecycle material:

- SPY Clean Fast Break selected/countable window: CSV lines 128-155, `2026-04-10` through `2026-04-15`.
- SPY source-window additions already counted: CSV lines 156-169 and 170-197.
- SPY Continuation selected/countable window: CSV lines 198-232, `2026-04-24` through `2026-04-30`.
- SPY Ideal selected/countable window: CSV lines 254-294, `2026-05-06` through `2026-05-13`.
- QQQ source-window addition already counted: CSV lines 66-86, `2026-03-30` through `2026-04-01`.
- QQQ Clean Fast Break selected/countable window: CSV lines 108-163, `2026-04-08` through `2026-04-17`.
- QQQ Continuation selected/countable window: CSV lines 164-233, `2026-04-20` through `2026-05-01`.
- QQQ Ideal selected/countable window: CSV lines 241-296, `2026-05-05` through `2026-05-14`.

## Candidate Review

| candidate_id | symbol | setup_type | source file | row/window reference | why it qualifies | what proof exists | what proof is missing | status | fastest next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SPY-SOURCE-WINDOW-CLEAN-FAST-BREAK-003` | SPY | Clean Fast Break | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` | CSV lines 79-99; `2026-03-31T09:30:00-04:00` through `2026-04-02T15:30:00-04:00` | Distinct earlier SPY upside break/reclaim window before all counted SPY April fast-break and continuation material. Source rows show 03-31 rebound from 637.98 to a 651.53 high and 650.24 close, 04-01 continuation to 658.52, and 04-02 pullback/recovery close at 655.88. | Accepted local SPY source CSV exists; exact source rows exist; source validation was previously recorded as PASS; 24H/macro/IV/event context is explicitly unconfirmed rather than fabricated; no-hindsight source boundary exists because only ordered OHLCV rows are used. | Accepted replay fixture row, exact setup-time row, Clean Fast Break trigger, invalidation, freshness/final-signal review, blocker/caution review, no-hindsight replay output, terminal chart-only outcome, clean-break-vs-reversal decision, economics, option performance, spread/slippage/fill, account risk, execution path, entry/exit usefulness, and regression protection. | `add_to_pool` | Build one bounded replay-readiness worksheet for SPY CSV lines 79-99 and drop if row-by-row review proves this is only a noisy rebound. |
| `SPY-SOURCE-WINDOW-CONTINUATION-004` | SPY | Continuation | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` | CSV lines 93-113; `2026-04-02T09:30:00-04:00` through `2026-04-07T15:30:00-04:00` | Distinct SPY continuation/rebuild source window after the 03-31/04-01 reclaim and before the counted 04-10 Clean Fast Break window. Source rows show 04-02 recovery from 645.11 to 655.88 close, 04-06 holding 655.52-659.68, and 04-07 shake/recovery closing 659.26. | Accepted local SPY source CSV exists; exact source rows exist; source-visible shelf/rebuild structure exists; unavailable context fields remain unconfirmed; no accepted future outcome is used. | Accepted replay fixture row, setup-time row, trigger, invalidation, freshness/final-signal review, blocker/caution review, no-hindsight replay output, terminal chart-only outcome, proof that 04-07 did or did not invalidate the continuation, economics, option performance, spread/slippage/fill, account risk, execution path, entry/exit usefulness, and regression protection. | `add_to_pool` | Batch this with the other new source windows and require exact trigger/invalidation/freshness fields before proof review. |
| `SPY-SOURCE-WINDOW-CONTINUATION-005` | SPY | Continuation | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` | CSV lines 233-253; `2026-05-01T09:30:00-04:00` through `2026-05-05T15:30:00-04:00` | Distinct SPY post-04-30 higher-base continuation candidate before the counted SPY Ideal window that starts 05-06. Source rows show 05-01 high-base follow-through to 724.85, 05-04 pullback to 714.99, and 05-05 recovery to 725.04 with 723.71 close. | Accepted local SPY source CSV exists; exact source rows exist; local no-hindsight source boundary exists; source-visible pullback/recovery structure exists. | Accepted proof that this is a fresh non-duplicate Continuation rather than same-lifecycle follow-through from 04-30; replay fixture row; trigger; invalidation; freshness/final-signal review; blocker/caution review; no-hindsight replay output; terminal chart-only outcome; economics; option performance; spread/slippage/fill; account risk; execution path; entry/exit usefulness; and regression protection. | `add_to_pool` | Review freshness first, because this may be either a fresh continuation or same-lifecycle follow-through from the 04-30 SPY Continuation anchor. |
| `QQQ-SOURCE-WINDOW-CONTINUATION-002` | QQQ | Continuation | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv` | CSV lines 87-107; `2026-04-02T09:30:00-04:00` through `2026-04-07T15:30:00-04:00` | Distinct QQQ continuation/rebuild candidate after the already counted 03-30 through 04-01 QQQ source-window candidate and before the counted 04-08 through 04-17 Clean Fast Break lifecycle. Source rows show 04-02 recovery to 585.99, 04-06 hold/extension to 590.61, and 04-07 shake/recovery close at 588.72. | Accepted local QQQ source CSV exists; exact source rows exist; QQQ source validation was previously recorded as PASS; source-visible rebuild/hold structure exists; context gaps are explicitly unconfirmed. | Accepted setup-time row, trigger, invalidation, freshness/final-signal review, blocker/caution review, no-hindsight replay output, terminal chart-only outcome, proof this is a fresh Continuation instead of same rebound context, economics, option performance, spread/slippage/fill, account risk, execution path, entry/exit usefulness, and regression protection. | `add_to_pool` | Add to the same bounded replay-readiness worksheet as the SPY additions and require row-by-row freshness and invalidation decisions. |
| `QQQ-SOURCE-WINDOW-CONTINUATION-003` | QQQ | Continuation | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv` | CSV lines 227-240; `2026-05-01T09:30:00-04:00` through `2026-05-04T15:30:00-04:00` | Apparent high-base/follow-through window after the 04-30 QQQ Continuation anchor. It has source-visible movement to 675.97 on 05-01 and digestion on 05-04. | Accepted local QQQ source rows exist; chart-only input for the 04-30 anchor already references 05-01 as next-session material. | Fresh non-overlapping setup identity is missing; prior replay row 6 marks the 04-30 shelf break spent by 05-01 15:30, and no accepted session-boundary rule proves this is a new candidate. Trigger, invalidation, freshness, blocker review, no-hindsight signoff, and terminal outcome are missing for any new setup. | `duplicate` | Do not count now. Revisit only if a session-boundary review proves a fresh setup separate from the 04-30 Continuation anchor. |
| `QQQ-SOURCE-WINDOW-IDEAL-002` | QQQ | Ideal | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv` | CSV lines 297-302; `2026-05-15T09:30:00-04:00` through `2026-05-15T14:30:00-04:00` | Apparent next pullback/recovery after the counted QQQ Ideal lifecycle, but the available source segment is only a partial single session at the end of the CSV. | Accepted local QQQ source rows exist for 05-15 through 14:30. | Full bounded window is unavailable; exact setup-time row, trigger, invalidation, freshness, blocker/caution review, no-hindsight replay output, and terminal outcome are missing. It is too short to add cleanly. | `unavailable` | Do not count unless more QQQ source rows after 05-15 become available. |
| `SPY-SOURCE-WINDOW-IDEAL-002` | SPY | Ideal | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` | CSV lines 23-50; `2026-03-19T09:30:00-04:00` through `2026-03-24T15:30:00-04:00` | Apparent early rebound/retest area, but the structure is choppy: 03-19 rebound, 03-20 breakdown, 03-23 rebound, 03-24 failure to extend cleanly. | Accepted local SPY source rows exist. | Clean setup identity is weak; accepted setup-time row, trigger, invalidation, freshness, blocker review, no-hindsight replay output, and terminal outcome are missing. | `drop` | Replace with cleaner SPY/QQQ source windows; do not spend single-candidate rescue work here. |
| `QQQ-SOURCE-WINDOW-IDEAL-003` | QQQ | Ideal | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv` | CSV lines 17-44; `2026-03-19T09:30:00-04:00` through `2026-03-24T15:30:00-04:00` | Apparent early rebound/retest area, but the source rows remain choppy and below a clean repeatable Ideal profile: 03-19 rebound, 03-20 breakdown, 03-23 rebound, and 03-24 weak close. | Accepted local QQQ source rows exist. | Clean setup identity is weak; accepted setup-time row, trigger, invalidation, freshness, blocker review, no-hindsight replay output, and terminal outcome are missing. | `drop` | Replace with cleaner QQQ Continuation/Clean Fast Break candidates; do not count. |

## Summary

- Previous candidate count: 20.
- New candidates found: 8 apparent SPY/QQQ source windows reviewed together.
- Clean candidates added: 4.
- Duplicates skipped: 1.
- Blocked: 4 added candidates are proof-blocked until replay/setup-time fields exist; 0 separate non-added blocked rows.
- Dropped: 2.
- Unavailable: 1.
- New total pool size: 24.
- Best symbol/setup pairs: SPY Continuation, QQQ Continuation, SPY Clean Fast Break, QQQ Clean Fast Break.
- Weakest symbol/setup pairs: QQQ Ideal wide-risk/late-source paths, SPY Ideal early choppy rebound paths, QQQ 05-01 same-lifecycle Continuation context.
- Fastest next action: create one bounded replay-readiness worksheet for the 4 new added source windows together: `SPY-SOURCE-WINDOW-CLEAN-FAST-BREAK-003`, `SPY-SOURCE-WINDOW-CONTINUATION-004`, `SPY-SOURCE-WINDOW-CONTINUATION-005`, and `QQQ-SOURCE-WINDOW-CONTINUATION-002`.

## Guardrail Result

- No proof was accepted.
- No profitability claim was made.
- Directional movement was not accepted as proof.
- Source-visible follow-through was treated as candidate-shape input only.
- Duplicates and same-lifecycle context were not counted.
- Missing trigger, invalidation, freshness, blocker review, no-hindsight replay output, terminal outcome, economics, option performance, spread/slippage/fill, account risk, execution path, entry/exit usefulness, and regression protection remain blockers.
- Unit tests were not run by instruction.
- Live data, alerts, broker/order/account/options/P&L, Railway, production, real money, and `main.py` or trading logic changes remain unauthorized.
