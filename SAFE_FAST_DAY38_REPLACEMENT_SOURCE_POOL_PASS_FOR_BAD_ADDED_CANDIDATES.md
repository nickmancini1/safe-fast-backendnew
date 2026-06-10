# SAFE-FAST Day 38 Replacement Source Pool Pass For Bad Added Candidates

Project day: Day 38
Baseline before review: `e74ab27 Add Day 38 added 4 fixture-ready replay review`
Mode: docs-only replacement source-pool pass; no proof accepted

## Purpose

Replace the two bad Day 38 added candidates in one batch if cleaner non-duplicate SPY/QQQ candidates exist in the current repo sources.

Bad candidates to replace:

- `SPY-SOURCE-WINDOW-CONTINUATION-005`
- `QQQ-SOURCE-WINDOW-CONTINUATION-002`

This pass does not accept proof, does not claim profitability, does not use live data, does not use broker/order/account/options/P&L data, does not authorize alerts, and does not modify `main.py`, trading logic, Railway, deploy files, replay runner, schemas, fixtures, or generated replay outputs.

## Files Read

- `SAFE_FAST_DAY38_ADDED_4_FIXTURE_READY_REPLAY_REVIEW.md`
- `SAFE_FAST_DAY38_LARGE_SPY_QQQ_SOURCE_POOL_EXPANSION_PASS.md`
- `SAFE_FAST_DAY38_FULL_20_CANDIDATE_DEEP_BATCH_REVIEW.md`
- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`
- `SAFE_FAST_DAY38_SPY_QQQ_SOURCE_WINDOW_CANDIDATE_PASS.md`
- `SAFE_FAST_DAY38_SPY_SOURCE_WINDOW_CONTINUATION_002_REVIEW.md`
- `SAFE_FAST_DAY38_QQQ_BLOCKER_RESOLUTION_REVIEW.md`
- `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`
- `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`

## Search Terms Used

- `SPY`
- `QQQ`
- `Ideal`
- `Clean Fast Break`
- `Continuation`
- `source window`
- `trigger`
- `invalidation`
- `freshness`
- `blocker`
- `outcome`
- `no-hindsight`

## Replacement Decision

No new clean non-duplicate replacement was added from current repo sources.

Reason: the cleaner-looking SPY/QQQ source candidates are already counted in the Day 38 pool, so adding them again would violate the duplicate rule. The remaining unused source ranges reviewed in this pass do not supply a cleaner setup identity with repo-backed setup-time evidence.

| result | count |
| --- | ---: |
| replacements needed | 2 |
| replacement candidates reviewed | 6 |
| add_as_replacement | 0 |
| duplicate | 3 |
| drop | 2 |
| unavailable | 1 |
| blocked_missing_proof | 0 |

## Candidate Review

| candidate_id | symbol | setup_type | source file | row/window reference | why it is cleaner | what proof exists | what proof is missing | status | fastest next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SPY-SOURCE-WINDOW-CONTINUATION-002` | SPY | Continuation | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` | CSV lines 156-169; `2026-04-16T09:30:00-04:00` through `2026-04-17T15:30:00-04:00` | Cleaner than `SPY-SOURCE-WINDOW-CONTINUATION-005` because it is a distinct higher-base window after the 04-13/04-15 Clean Fast Break lifecycle and before the counted 04-30 SPY Continuation. It has a bounded 04-16 base and 04-17 break candidate. | Accepted local SPY source CSV exists; exact rows exist; source validation PASS is recorded; `SAFE_FAST_DAY38_SPY_SOURCE_WINDOW_CONTINUATION_002_REVIEW.md` records candidate setup row `2026-04-17T09:30:00-04:00`, candidate trigger level `702.78`, candidate invalidation `698.53`, and source-only no-hindsight boundary. | Accepted replay fixture row; accepted setup-time trigger; accepted invalidation; accepted freshness/final-signal review; accepted blocker/caution review; no-hindsight replay output; terminal chart-only outcome review; economics; option performance; spread/slippage/fill; account risk; execution path; entry/exit usefulness; regression protection. | duplicate | Do not add as replacement. It is already counted in the Day 38 pool. Fastest valid action is its already-defined bounded setup-time replay worksheet/request. |
| `SPY-SOURCE-WINDOW-CONTINUATION-003` | SPY | Continuation | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` | CSV lines 170-197; `2026-04-20T09:30:00-04:00` through `2026-04-23T15:30:00-04:00` | Cleaner than `SPY-SOURCE-WINDOW-CONTINUATION-005` because it is before the counted 04-24 through 04-30 SPY Continuation lifecycle and is not the 05-01 same-lifecycle follow-through question. | Accepted local SPY source CSV exists; exact source rows exist; source-visible pullback/recovery/rebuild structure exists; local no-hindsight source boundary exists. | Accepted replay fixture row; accepted setup-time row; trigger; invalidation; freshness/final-signal review; blocker/caution review; terminal chart-only outcome; proof that 04-23 shake did or did not invalidate; economics; option performance; spread/slippage/fill; account risk; execution path; entry/exit usefulness; regression protection. | duplicate | Do not add as replacement. It is already counted in the Day 38 pool. Fastest valid action is the existing setup-time replay worksheet for 04-20 through 04-23. |
| `QQQ-SOURCE-WINDOW-CLEAN-FAST-BREAK-002` | QQQ | Clean Fast Break | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv` | CSV lines 66-86; `2026-03-30T09:30:00-04:00` through `2026-04-01T15:30:00-04:00` | Cleaner than `QQQ-SOURCE-WINDOW-CONTINUATION-002` because it is a separate earlier QQQ Clean Fast Break candidate outside the counted 04-08 through 04-17 QQQ Clean Fast Break lifecycle and not the 04-02 through 04-07 same-rebound Continuation question. | Accepted local QQQ source CSV exists; exact rows exist; QQQ source validation PASS is recorded; source-window review records 03-30 flush/base, 03-31 reclaim/extension, and 04-01 continuation shape; context fields are explicitly unconfirmed; no after-the-fact outcome labels are added. | Accepted replay fixture row; accepted setup-time row; trigger; invalidation; freshness/final-signal review; blocker/caution review; no-hindsight replay output; terminal chart-only outcome; proof it is clean enough and not noisy reversal; economics; option performance; spread/slippage/fill; account risk; execution path; entry/exit usefulness; regression protection. | duplicate | Do not add as replacement. It is already counted in the Day 38 pool. Fastest valid action is the existing bounded replay readiness/setup-time review for QQQ CSV lines 66-86. |
| `SPY-UNUSED-SOURCE-RANGE-03-25-03-30` | SPY | UNCLEAR | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` | CSV lines 51-78; `2026-03-25T09:30:00-04:00` through `2026-03-30T15:30:00-04:00` | MISSING. It is not cleaner. The inspected rows are mostly decline/chop into 03-30 and do not provide a clean repo-backed Ideal, Clean Fast Break, or Continuation identity. | Accepted local SPY source rows exist; context fields are explicitly unconfirmed. | Clean setup identity; accepted setup-time row; trigger; invalidation; freshness/final-signal review; blocker/caution review; no-hindsight replay output; terminal outcome; economics; regression protection. | drop | Do not count. Fastest next action is no action unless new repo-backed review material identifies a clean setup-time row without hindsight. |
| `SPY-UNUSED-SOURCE-RANGE-04-08-04-09` | SPY | UNCLEAR | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` | CSV lines 114-127; `2026-04-08T09:30:00-04:00` through `2026-04-09T15:30:00-04:00` | MISSING. It is not cleaner as a replacement because it sits immediately before the already counted SPY Clean Fast Break selected/countable window beginning 04-10 and has no accepted separate setup identity. | Accepted local SPY source rows exist; context fields are explicitly unconfirmed. | Proof that this is a separate non-overlapping setup; accepted setup-time row; trigger; invalidation; freshness/final-signal review; blocker/caution review; no-hindsight replay output; terminal outcome; economics; regression protection. | drop | Do not count. Treat as possible context before the counted 04-10 Clean Fast Break window only. |
| `QQQ-UNUSED-SOURCE-RANGE-03-25-03-27` | QQQ | UNCLEAR | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv` | CSV lines 45-65; `2026-03-25T09:30:00-04:00` through `2026-03-27T15:30:00-04:00` | MISSING. It is not cleaner. The rows trend lower into 03-27 and do not provide a clean repo-backed Ideal, Clean Fast Break, or Continuation candidate. | Accepted local QQQ source rows exist; context fields are explicitly unconfirmed. | Clean setup identity; accepted setup-time row; trigger; invalidation; freshness/final-signal review; blocker/caution review; no-hindsight replay output; terminal outcome; economics; regression protection. | unavailable | Do not count. Current repo sources do not provide a clean non-duplicate QQQ replacement beyond the already-counted QQQ Clean Fast Break 002 candidate. |

## Replacement Result

- `SPY-SOURCE-WINDOW-CONTINUATION-005`: removed from replacement path; no new non-duplicate SPY replacement added from current repo sources.
- `QQQ-SOURCE-WINDOW-CONTINUATION-002`: removed from replacement path; no new non-duplicate QQQ replacement added from current repo sources.
- Replacement slots added: 0.
- Candidate pool should not count duplicates to preserve the Day 38 evidence standard.
- The cleaner-looking candidates remain useful, but only through their already-counted blocked paths.

## Guardrail Result

- No proof was accepted.
- No profitability claim was made.
- Directional source movement was not accepted as proof.
- Duplicates were not counted.
- `MISSING` evidence remains a blocker.
- `UNCLEAR` setup identity remains a blocker.
- Unit tests were not run by instruction.
- `main.py`, trading logic, Railway, deploy files, replay runner, schemas, fixtures, generated replay outputs, live data, broker/order/account/options/P&L, alerts, and production behavior were not changed.

## Fastest Next Action

Run the already-defined bounded setup-time replay work for the cleaner counted candidates instead of searching the same exhausted source pool again:

1. `SPY-SOURCE-WINDOW-CONTINUATION-002`, CSV lines 156-169.
2. `QQQ-SOURCE-WINDOW-CLEAN-FAST-BREAK-002`, CSV lines 66-86.

Only add new replacements later if new non-duplicate repo-backed source rows become available.
