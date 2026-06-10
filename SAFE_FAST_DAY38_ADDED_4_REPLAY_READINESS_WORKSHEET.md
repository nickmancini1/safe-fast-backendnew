# SAFE-FAST Day 38 Added 4 Replay Readiness Worksheet

Project day: Day 38
Baseline before worksheet: `c21642e Add Day 38 large SPY QQQ source pool expansion pass`
Mode: docs-only replay-readiness worksheet; no proof accepted

## Purpose

Create one bounded replay-readiness worksheet for the 4 newly added SPY/QQQ source-window candidates together.

This worksheet does not accept proof, does not claim profitability, does not use live data, does not use broker/order/account/options/P&L data, does not authorize alerts, and does not modify `main.py`, trading logic, Railway, deploy, replay runner, schemas, or fixtures.

## Files Read

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`
- `SAFE_FAST_DAY38_LARGE_SPY_QQQ_SOURCE_POOL_EXPANSION_PASS.md`
- `SAFE_FAST_DAY38_FULL_20_CANDIDATE_DEEP_BATCH_REVIEW.md`
- `SAFE_FAST_DAY38_SPY_QQQ_SOURCE_WINDOW_CANDIDATE_PASS.md`
- `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`
- `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`
- `historical_signal_replay/source_data/FIRST_REAL_SPY_WINDOW_SELECTION_REVIEW.md`
- `historical_signal_replay/source_data/SECOND_REAL_SPY_WINDOW_SELECTION_REVIEW.md`
- `historical_signal_replay/source_data/THIRD_REAL_SPY_WINDOW_SELECTION_REVIEW.md`
- `historical_signal_replay/source_data/QQQ_FIRST_WINDOW_SELECTION_REVIEW.md`
- `historical_signal_replay/source_data/QQQ_CLEAN_FAST_BREAK_WINDOW_SELECTION_REVIEW.md`
- `historical_signal_replay/source_data/QQQ_CONTINUATION_WINDOW_SELECTION_REVIEW.md`
- `historical_signal_replay/reports/*_signal_log.jsonl`

## Batch Decision

| result | count |
| --- | ---: |
| keep | 0 |
| block | 4 |
| drop | 0 |
| replace | 0 |

All 4 candidates remain source-backed candidates only. They are blocked from proof review until exact replay/setup-time fields are completed.

## Replay-Readiness Worksheet

| candidate_id | symbol | setup_type | source file | row/window reference | setup candle needed | trigger needed | failure level needed | freshness needed | blocker check needed | outcome needed | no-hindsight check needed | what is already known | what is missing | keep/block/drop/replace | fastest next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SPY-SOURCE-WINDOW-CLEAN-FAST-BREAK-003` | SPY | Clean Fast Break | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` | CSV lines 79-99; `2026-03-31T09:30:00-04:00` through `2026-04-02T15:30:00-04:00` | MISSING - exact completed setup candle must be selected from the source rows. | MISSING - exact Clean Fast Break trigger level and trigger row are not accepted. | MISSING - exact invalidation/failure level is not accepted. | MISSING - final-signal/stale/spent status is not accepted. | MISSING - 24H, macro, IV, event, headline, option, account, broker, execution, and clean-break-vs-noisy-rebound checks are not complete. | MISSING - terminal chart-only outcome tied to the accepted setup candle is not complete. | MISSING - replay output proving row-by-row no-hindsight handling is not accepted. | Accepted local SPY source CSV exists; exact source rows exist; source validation was previously PASS; unavailable context fields are explicitly unconfirmed; source rows show 03-31 rebound, 04-01 continuation, and 04-02 pullback/recovery shape. | Accepted replay fixture row, setup candle, trigger, failure level, freshness/final-signal review, blocker/caution review, no-hindsight replay output, terminal chart-only outcome, economics/usefulness notes, option performance, spread/slippage/fill, account risk, execution path, entry/exit usefulness, and regression protection. | block | Run bounded row-by-row replay-readiness review for SPY CSV lines 79-99; drop if the accepted row review proves noisy rebound rather than Clean Fast Break. |
| `SPY-SOURCE-WINDOW-CONTINUATION-004` | SPY | Continuation | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` | CSV lines 93-113; `2026-04-02T09:30:00-04:00` through `2026-04-07T15:30:00-04:00` | MISSING - exact completed setup candle must be selected from the source rows. | MISSING - exact Continuation trigger level and trigger row are not accepted. | MISSING - exact invalidation/failure level is not accepted. | MISSING - fresh continuation status is not accepted. | MISSING - 04-07 shake/recovery, 24H, macro, IV, event, headline, option, account, broker, and execution checks are not complete. | MISSING - terminal chart-only outcome tied to the accepted setup candle is not complete. | MISSING - replay output proving row-by-row no-hindsight handling is not accepted. | Accepted local SPY source CSV exists; exact source rows exist; source-visible shelf/rebuild structure exists; unavailable context fields are unconfirmed; window is before the already counted 04-10 Clean Fast Break window. | Accepted replay fixture row, setup candle, trigger, failure level, freshness/final-signal review, blocker/caution review, no-hindsight replay output, terminal chart-only outcome, proof that 04-07 did or did not invalidate the continuation, economics/usefulness notes, option performance, spread/slippage/fill, account risk, execution path, entry/exit usefulness, and regression protection. | block | Review lines 93-113 together with the other added windows and decide exact trigger, invalidation, and 04-07 invalidation/freshness status before proof review. |
| `SPY-SOURCE-WINDOW-CONTINUATION-005` | SPY | Continuation | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` | CSV lines 233-253; `2026-05-01T09:30:00-04:00` through `2026-05-05T15:30:00-04:00` | MISSING - exact completed setup candle must be selected from the source rows. | MISSING - exact Continuation trigger level and trigger row are not accepted. | MISSING - exact invalidation/failure level is not accepted. | UNCLEAR - fresh non-duplicate continuation versus same-lifecycle follow-through from the 04-30 SPY Continuation anchor is unresolved. | MISSING - same-lifecycle/freshness, 24H, macro, IV, event, headline, option, account, broker, and execution checks are not complete. | MISSING - terminal chart-only outcome tied to the accepted setup candle is not complete. | MISSING - replay output proving row-by-row no-hindsight handling is not accepted. | Accepted local SPY source CSV exists; exact source rows exist; source-visible high-base pullback/recovery structure exists; window sits after the counted 04-30 SPY Continuation and before the counted 05-06 SPY Ideal window. | Accepted proof that this is a fresh non-duplicate Continuation, replay fixture row, setup candle, trigger, failure level, freshness/final-signal review, blocker/caution review, no-hindsight replay output, terminal chart-only outcome, economics/usefulness notes, option performance, spread/slippage/fill, account risk, execution path, entry/exit usefulness, and regression protection. | block | Review freshness and same-lifecycle status first; only continue if the row-by-row review proves a fresh Continuation candidate separate from the 04-30 anchor. |
| `QQQ-SOURCE-WINDOW-CONTINUATION-002` | QQQ | Continuation | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv` | CSV lines 87-107; `2026-04-02T09:30:00-04:00` through `2026-04-07T15:30:00-04:00` | MISSING - exact completed setup candle must be selected from the source rows. | MISSING - exact Continuation trigger level and trigger row are not accepted. | MISSING - exact invalidation/failure level is not accepted. | UNCLEAR - fresh Continuation versus same rebound context after the 03-30 through 04-01 QQQ source-window candidate is unresolved. | MISSING - same-context/freshness, 24H, macro, IV, event, headline, option, account, broker, and execution checks are not complete. | MISSING - terminal chart-only outcome tied to the accepted setup candle is not complete. | MISSING - replay output proving row-by-row no-hindsight handling is not accepted. | Accepted local QQQ source CSV exists; exact source rows exist; QQQ source validation was previously PASS; source-visible rebuild/hold structure exists; window is before the counted 04-08 through 04-17 QQQ Clean Fast Break lifecycle. | Accepted setup candle, trigger, failure level, freshness/final-signal review, blocker/caution review, no-hindsight replay output, terminal chart-only outcome, proof this is a fresh Continuation instead of same rebound context, economics/usefulness notes, option performance, spread/slippage/fill, account risk, execution path, entry/exit usefulness, and regression protection. | block | Review lines 87-107 row by row and decide freshness/same-context status before any proof review. |

## Fastest Next Action

Run one bounded row-by-row replay-readiness review for all 4 added windows together, in this order:

1. Decide fresh/non-duplicate setup identity for `SPY-SOURCE-WINDOW-CONTINUATION-005` and `QQQ-SOURCE-WINDOW-CONTINUATION-002`.
2. Select exact completed setup candle, trigger, and failure level for any candidate that survives identity review.
3. Complete freshness/final-signal, blocker/caution, no-hindsight replay output, and terminal chart-only outcome fields.
4. Keep candidates blocked until regression protection and economics/usefulness notes exist.

## Guardrail Result

- No proof was accepted.
- No profitability claim was made.
- Directional movement was not accepted as proof.
- Source-visible structure was treated as candidate-shape input only.
- Missing evidence remains a blocker, not low confidence.
- Unit tests were not run by instruction.
- `main.py`, trading logic, Railway, deploy, replay runner, schemas, fixtures, and generated replay outputs were not changed.
