# SAFE-FAST Day 38 SPY/QQQ Source Window Candidate Pass

Project day: Day 38
Baseline before review: `9a110e2 Add Day 38 SPY QQQ batch candidate expansion review`
Mode: bounded local source-window review only; watch-only; no trade decision

## Purpose

Find at least three additional clean, non-duplicate repo-backed SPY/QQQ historical candidates so the Day 38 candidate batch reaches at least 20 total examples.

This pass uses local repo files only. It does not use live data, network data, broker/order/account data, option data, alerts, Railway, production behavior, or trade decisions.

Directionally favorable chart movement is not accepted proof.

## Files Read

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`
- `SAFE_FAST_DAY38_EXISTING_HISTORICAL_CANDIDATE_BATCH_TRIAGE_REVIEW.md`
- `SAFE_FAST_DAY38_READY_CANDIDATES_DEEPER_BATCH_REVIEW.md`
- `SAFE_FAST_DAY38_SPY_QQQ_BATCH_CANDIDATE_EXPANSION_REVIEW.md`
- `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`
- `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`
- `historical_signal_replay/source_data/FIRST_REAL_SOURCE_HISTORICAL_DATA_VALIDATION_REVIEW.md`
- `historical_signal_replay/source_data/QQQ_FIRST_REAL_SOURCE_HISTORICAL_DATA_VALIDATION_REVIEW.md`
- `historical_signal_replay/reports/*_signal_log.jsonl`
- `historical_signal_replay/reports/*_regression_candidates.json`

## Search-Only Inspection Used

Searched local repo material for:

- `SPY`
- `QQQ`
- `Ideal`
- `Clean Fast Break`
- `Continuation`
- `source CSV`
- `source window`
- `replay readiness`
- `chart-only outcome`
- `trigger`
- `invalidation`
- `freshness`
- `blocker`
- `terminal outcome`

## Candidate Review

| candidate_id | symbol | setup_type | source file | source window or row range | why it qualifies | what proof exists | what proof is missing | status | fastest next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SPY-SOURCE-WINDOW-CONTINUATION-002` | SPY | Continuation | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` | CSV lines 156-169; `2026-04-16T09:30:00-04:00` through `2026-04-17T15:30:00-04:00` | Distinct higher-base continuation window after the 04-13/04-15 Clean Fast Break lifecycle and before the already counted 04-30 SPY Continuation. The 04-16 rows consolidate in the 698.53-702.78 area, then 04-17 gaps above that range and extends to 712.38 before closing 710.04. This is not the dropped weak 04-15 SPY Clean Fast Break sample. | Accepted local SPY source CSV exists; source validation is PASS; exact local rows exist; 24H/macro/IV/event context is explicitly unconfirmed rather than fabricated; source-visible base and break/follow-through structure exists. | Replay fixture row, accepted setup-time trigger, invalidation, freshness/final-signal review, blocker/caution review, no-hindsight replay output, exact chart-only terminal outcome, profitability proof, option performance, spread/slippage/fill evidence, account risk, and entry/exit economics. | `add_to_batch` | Build a bounded replay request for this exact row range and require completed trigger, invalidation, freshness, blocker, and terminal chart-only outcome fields before deeper proof review. |
| `SPY-SOURCE-WINDOW-CONTINUATION-003` | SPY | Continuation | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` | CSV lines 170-197; `2026-04-20T09:30:00-04:00` through `2026-04-23T15:30:00-04:00` | Distinct source-window continuation/rebuild candidate after the 04-17 extension and before the already counted first SPY Continuation selected window that begins 04-24. The 04-20 rows hold a tight upper range, 04-21 pulls back, 04-22 recovers to a 711.45 high / 711.21 close, and 04-23 provides shake/rebuild context without overlapping the counted 04-30 signal row. | Accepted local SPY source CSV exists; exact source rows and line range exist; source-visible pullback/recovery/rebuild structure exists; no-hindsight boundary is preserved because only local OHLCV rows are used. | Replay fixture row, accepted setup-time trigger, invalidation, freshness/final-signal review, blocker/caution review, terminal chart-only outcome, proof that 04-23 shake did or did not invalidate the candidate, profitability proof, option performance, spread/slippage/fill evidence, account risk, and entry/exit economics. | `add_to_batch` | Build a setup-time replay worksheet for the 04-20 through 04-23 source rows and decide whether the 04-22 recovery is a valid fresh Continuation trigger or only context for the later 04-24/04-30 lifecycle. |
| `QQQ-SOURCE-WINDOW-CLEAN-FAST-BREAK-002` | QQQ | Clean Fast Break | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv` | CSV lines 66-86; `2026-03-30T09:30:00-04:00` through `2026-04-01T15:30:00-04:00` | Distinct earlier QQQ source-window break candidate, separate from the already counted 04-13 QQQ Clean Fast Break. The 03-30 session flushes and bases from 555.60 to 568.04, 03-31 reclaims and extends through 578.64, and 04-01 continues to 587.739 before late-session digestion. | Accepted local QQQ source CSV exists; QQQ source validation is PASS; exact local rows exist; candidate is outside the already counted 04-08 through 04-17 QQQ Clean Fast Break window; no after-the-fact outcome labels are added. | Replay fixture row, accepted setup-time trigger, invalidation, freshness/final-signal review, blocker/caution review, terminal chart-only outcome, proof this is a clean enough Clean Fast Break rather than a noisy reversal, profitability proof, option performance, spread/slippage/fill evidence, account risk, and entry/exit economics. | `add_to_batch` | Build a bounded replay readiness review for 03-30 through 04-01 and either promote as a QQQ Clean Fast Break candidate with exact trigger/invalidation or drop if row-by-row review proves it is too noisy. |

## Non-Counted Rows

| candidate_id | symbol | setup_type | source | reason not counted | status |
| --- | --- | --- | --- | --- | --- |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | SPY | Clean Fast Break | `historical_signal_replay/reports/third_real_spy_clean_fast_break_replay_v1_signal_log.jsonl` row `2026-04-15T14:30:00-04:00` | This is the dropped weak SPY Clean Fast Break sample from the deeper batch review. Its chart-only outcome time-stopped with too little favorable movement. | `drop_not_clean_enough` |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | SPY | Clean Fast Break | `historical_signal_replay/reports/third_real_spy_clean_fast_break_replay_v1_signal_log.jsonl` row `2026-04-13T12:30:00-04:00` | Already added by `SAFE_FAST_DAY38_SPY_QQQ_BATCH_CANDIDATE_EXPANSION_REVIEW.md`. | `duplicate_do_not_count` |
| `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | QQQ | Clean Fast Break | `historical_signal_replay/reports/first_real_qqq_clean_fast_break_replay_v1_signal_log.jsonl` row `2026-04-13T12:30:00-04:00` | Already counted in the Day 38 ready/deeper batch path. | `duplicate_do_not_count` |
| `QQQ-REAL-HISTORICAL-CONTINUATION-001` | QQQ | Continuation | `historical_signal_replay/reports/first_real_qqq_continuation_replay_v1_signal_log.jsonl` row `2026-04-30T15:30:00-04:00` | Already counted in the Day 38 ready/deeper batch path. | `duplicate_do_not_count` |
| `QQQ-CLEAN-FAST-BREAK-HIGHER-BASE-04-16` | QQQ | Clean Fast Break | `historical_signal_replay/reports/first_real_qqq_clean_fast_break_replay_v1_signal_log.jsonl` row `2026-04-16T13:30:00-04:00` | Prior expansion found this path but no fresh trigger row was present in the inspected replay output. | `blocked_missing_proof` |

## Review Summary

- previous batch size: 17
- new clean candidates found: 3 source-window candidates
- candidates added: 3
- new estimated batch size: 20
- whether batch is now at least 20: yes
- strongest pairs: QQQ Clean Fast Break, QQQ Continuation, SPY Continuation, SPY Ideal
- weakest pairs: prior SPY Clean Fast Break 04-15 remains dropped; QQQ Ideal still needs wide-risk review; the three new source-window candidates are weaker than fixture-backed candidates until replay trigger/invalidation/freshness/blocker/terminal outcome proof exists
- fastest next action: run bounded replay readiness/setup-time review on the three added source-window candidates, starting with `SPY-SOURCE-WINDOW-CONTINUATION-002`, and require exact trigger, invalidation, freshness/final-signal, blocker/caution, no-hindsight, and terminal chart-only outcome fields before any proof review
- no proof accepted: yes
- no profitability claim: yes

## Conclusion

This bounded local pass found three additional non-duplicate SPY/QQQ source-window candidates and raises the estimated Day 38 batch from 17 to 20 examples.

The batch-size target is now met, but the new additions are candidates only. They do not have accepted proof, do not prove profitability, and do not authorize live data, alerts, broker/order/account/options/P&L work, Railway, production, or trade decisions.
