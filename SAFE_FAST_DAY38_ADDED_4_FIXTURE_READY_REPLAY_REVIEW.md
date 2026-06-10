# SAFE-FAST Day 38 Added 4 Fixture-Ready Replay Review

Project day: Day 38
Baseline before review: `94c1741 Add Day 38 added 4 fixture-ready replay request`
Mode: docs-only fixture-ready replay review; no proof accepted

## Purpose

Review all 4 added SPY/QQQ source-window candidates together using the fixture-ready replay request.

This review does not accept proof, does not claim profitability, does not use live data, does not use broker/order/account/options/P&L data, does not authorize alerts, and does not modify `main.py`, trading logic, Railway, deploy, replay runner, schemas, fixtures, or generated replay outputs.

## Files Read

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`
- `SAFE_FAST_DAY38_ADDED_4_FIXTURE_READY_REPLAY_REQUEST.md`
- `SAFE_FAST_DAY38_ADDED_4_ROW_BY_ROW_REPLAY_READINESS_REVIEW.md`
- `SAFE_FAST_DAY38_ADDED_4_REPLAY_READINESS_WORKSHEET.md`
- `SAFE_FAST_DAY38_LARGE_SPY_QQQ_SOURCE_POOL_EXPANSION_PASS.md`
- `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`
- `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`
- `historical_signal_replay/reports/first_real_spy_continuation_replay_v1_signal_log.jsonl`
- `historical_signal_replay/reports/first_real_qqq_continuation_replay_v1_signal_log.jsonl`
- `historical_signal_replay/reports/first_real_qqq_clean_fast_break_replay_v1_signal_log.jsonl`

## Batch Decision

| result | count |
| --- | ---: |
| keep | 0 |
| block | 2 |
| drop | 0 |
| replace | 2 |

The two focus candidates are `replace` because their fresh/non-duplicate identity remains `UNCLEAR` after the fixture-ready request review. The request already said to replace either focus candidate if freshness cannot be proven rather than spending single-candidate rescue work.

The other 2 candidates remain `block` because exact setup candle, trigger, failure level, freshness/final-signal, blocker/caution review, no-hindsight replay output, terminal chart-only outcome, and regression protection remain missing.

## Candidate 1: SPY-SOURCE-WINDOW-CONTINUATION-005

| field | review |
| --- | --- |
| exact rows | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` lines 233-253; `2026-05-01T09:30:00-04:00` through `2026-05-05T15:30:00-04:00` |
| setup candle | MISSING |
| trigger | MISSING |
| failure level | MISSING |
| freshness | UNCLEAR - prior SPY Continuation replay log marks the 04-30 trigger spent by `2026-04-30T15:30:00-04:00`, but no accepted repo rule proves the 05-01 through 05-05 structure is a fresh new Continuation instead of same-lifecycle follow-through. |
| blocker | MISSING complete same-lifecycle/freshness and blocker/caution review; 24H, macro, IV, event, headline, option, account, broker, execution, overlap, and stale/spent signal checks remain incomplete. |
| outcome | MISSING |
| no-hindsight check | MISSING accepted replay output; ordered source rows and favorable-looking movement are not proof. |
| keep/block/drop/replace | replace |
| fastest next action | Replace with a cleaner non-overlapping SPY/QQQ Continuation or Clean Fast Break candidate. Do not spend single-candidate rescue work unless a future accepted session-boundary/freshness rule is created first. |

## Candidate 2: QQQ-SOURCE-WINDOW-CONTINUATION-002

| field | review |
| --- | --- |
| exact rows | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv` lines 87-107; `2026-04-02T09:30:00-04:00` through `2026-04-07T15:30:00-04:00` |
| setup candle | MISSING |
| trigger | MISSING |
| failure level | MISSING |
| freshness | UNCLEAR - lines 87-107 may be a fresh Continuation or same rebound context after QQQ lines 66-86; no accepted fixture output or freshness rule decides it. |
| blocker | MISSING complete same-context/freshness and blocker/caution review; 24H, macro, IV, event, headline, option, account, broker, execution, overlap, and stale/spent signal checks remain incomplete. |
| outcome | MISSING |
| no-hindsight check | MISSING accepted replay output; the 04-07 recovery is not proof. |
| keep/block/drop/replace | replace |
| fastest next action | Replace with a cleaner non-overlapping QQQ Continuation or QQQ Clean Fast Break candidate. Do not keep rescuing the same rebound-context window without an accepted freshness/session-boundary rule. |

## Candidate 3: SPY-SOURCE-WINDOW-CLEAN-FAST-BREAK-003

| field | review |
| --- | --- |
| exact rows | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` lines 79-99; `2026-03-31T09:30:00-04:00` through `2026-04-02T15:30:00-04:00` |
| setup candle | MISSING |
| trigger | MISSING |
| failure level | MISSING |
| freshness | MISSING |
| blocker | MISSING complete blocker/caution review; source rows carry `CONTEXT_24H_DAILY_UNCONFIRMED`, `MACRO_UNCONFIRMED`, `IV_UNCONFIRMED`, and `EVENT_UNCONFIRMED`; clean-break-vs-noisy-rebound decision is not accepted. |
| outcome | MISSING |
| no-hindsight check | MISSING accepted replay output; ordered source rows alone are not proof. |
| keep/block/drop/replace | block |
| fastest next action | Keep blocked as a batch candidate only. Fill exact setup candle, trigger, failure level, freshness, blocker/caution, no-hindsight, outcome, and regression fields in a real replay fixture pass; drop if that pass proves noisy rebound rather than Clean Fast Break. |

## Candidate 4: SPY-SOURCE-WINDOW-CONTINUATION-004

| field | review |
| --- | --- |
| exact rows | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` lines 93-113; `2026-04-02T09:30:00-04:00` through `2026-04-07T15:30:00-04:00` |
| setup candle | MISSING |
| trigger | MISSING |
| failure level | MISSING |
| freshness | UNCLEAR |
| blocker | MISSING complete blocker/caution review; source rows carry unconfirmed 24H/macro/IV/event context; 04-07 shake/recovery invalidation decision is not accepted. |
| outcome | MISSING |
| no-hindsight check | MISSING accepted replay output. |
| keep/block/drop/replace | block |
| fastest next action | Keep blocked as a batch candidate only. Fill exact trigger, invalidation, 04-07 invalidation/freshness status, blocker/caution, no-hindsight, outcome, and regression fields in a real replay fixture pass. |

## Guardrail Result

- No proof was accepted.
- No profitability claim was made.
- Directional movement was not accepted as proof.
- Source-visible structure was treated as candidate-shape input only.
- `MISSING` evidence remains a blocker.
- `UNCLEAR` freshness or invalidation remains a blocker.
- The two focus candidates should be replaced for runway purposes because freshness/identity was not proven.
- Unit tests were not run by instruction.
- `main.py`, trading logic, Railway, deploy, replay runner, schemas, fixtures, generated replay outputs, live data, broker/order/account/options/P&L, alerts, and production behavior were not changed.

## Fastest Next Action

Replace `SPY-SOURCE-WINDOW-CONTINUATION-005` and `QQQ-SOURCE-WINDOW-CONTINUATION-002` with cleaner non-overlapping SPY/QQQ candidates. Keep `SPY-SOURCE-WINDOW-CLEAN-FAST-BREAK-003` and `SPY-SOURCE-WINDOW-CONTINUATION-004` blocked until a real replay fixture pass fills exact setup-time and no-hindsight fields.
