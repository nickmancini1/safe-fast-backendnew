# SAFE-FAST Day 38 Added 4 Fixture-Ready Replay Request

Project day: Day 38
Baseline before request: `6040059 Add Day 38 added 4 row-by-row replay readiness review`
Mode: docs-only fixture-ready replay request; no proof accepted

## Purpose

Create one replay request for all 4 added SPY/QQQ source-window candidates together.

This request does not accept proof, does not claim profitability, does not use live data, does not use broker/order/account/options/P&L data, does not authorize alerts, and does not modify `main.py`, trading logic, Railway, deploy, replay runner, schemas, fixtures, or generated replay outputs.

## Files Read

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`
- `SAFE_FAST_DAY38_ADDED_4_ROW_BY_ROW_REPLAY_READINESS_REVIEW.md`
- `SAFE_FAST_DAY38_ADDED_4_REPLAY_READINESS_WORKSHEET.md`
- `SAFE_FAST_DAY38_LARGE_SPY_QQQ_SOURCE_POOL_EXPANSION_PASS.md`

## Batch Request

Review all 4 candidates together in one fixture-ready replay pass:

1. `SPY-SOURCE-WINDOW-CONTINUATION-005`
2. `QQQ-SOURCE-WINDOW-CONTINUATION-002`
3. `SPY-SOURCE-WINDOW-CLEAN-FAST-BREAK-003`
4. `SPY-SOURCE-WINDOW-CONTINUATION-004`

The first two must be handled first because their fresh/non-duplicate setup identity is still `UNCLEAR`.

## Batch Decision Before Replay

| result | count |
| --- | ---: |
| keep | 0 |
| block | 4 |
| drop | 0 |
| replace | 0 |

All 4 candidates remain source-backed candidates only. They are blocked until replay/setup-time fields are completed from accepted setup-time evidence.

## Required Fixture Output Fields

For each candidate, the replay fixture request must produce or explicitly preserve:

- exact source rows
- setup candle request
- trigger request
- failure level request
- freshness request
- blocker request
- outcome request
- no-hindsight request
- what is already known
- what is missing
- keep/block/drop/replace
- fastest next action

Use `MISSING` where evidence is missing. Use `UNCLEAR` where repo-backed evidence exists but does not decide the issue. Do not fill gaps with directional movement or after-the-fact chart appearance.

## Candidate 1: SPY-SOURCE-WINDOW-CONTINUATION-005

| field | request |
| --- | --- |
| exact source rows | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` lines 233-253; `2026-05-01T09:30:00-04:00` through `2026-05-05T15:30:00-04:00` |
| setup candle request | MISSING - identify the exact completed Continuation setup candle from lines 233-253, or return MISSING if no valid setup candle exists. |
| trigger request | MISSING - identify the exact Continuation trigger row and trigger level from setup-time rows only, or return MISSING. |
| failure level request | MISSING - identify the exact invalidation/failure level from setup-time evidence only, or return MISSING. |
| freshness request | UNCLEAR - decide first whether this is a fresh non-duplicate Continuation or same-lifecycle follow-through from the 04-30 SPY Continuation anchor. The prior SPY Continuation replay log marks the 04-30 trigger spent by `2026-04-30T15:30:00-04:00`, but no accepted rule proves the 05-01 through 05-05 structure is a fresh new setup. |
| blocker request | MISSING - complete same-lifecycle/freshness review and full blocker/caution review, including 24H, macro, IV, event, headline, option, account, broker, execution, overlap, and stale/spent signal checks. |
| outcome request | MISSING - produce terminal chart-only outcome tied to the accepted setup candle if one exists; do not treat favorable movement as proof. |
| no-hindsight request | MISSING - produce row-by-row replay output showing only evidence available at each row; ordered source rows alone are not proof. |
| what is already known | Accepted local SPY source CSV exists; exact source rows exist; source-visible high-base pullback/recovery structure exists; the window sits after the counted 04-30 SPY Continuation and before the counted 05-06 SPY Ideal window. |
| what is missing | Accepted proof that this is a fresh non-duplicate Continuation, replay fixture row, setup candle, trigger, failure level, freshness/final-signal review, blocker/caution review, no-hindsight replay output, terminal chart-only outcome, economics/usefulness notes, option performance, spread/slippage/fill, account risk, execution path, entry/exit usefulness, and regression protection. |
| keep/block/drop/replace | block |
| fastest next action | Decide fresh/non-duplicate setup identity first. If fresh identity remains UNCLEAR or fails, keep blocked and replace rather than spending single-candidate rescue work. If viable, fill exact setup candle, trigger, failure level, freshness/final-signal, blocker/caution, no-hindsight, outcome, and regression fields in the same batch pass. |

### Source Row Notes

| CSV line | timestamp | row note |
| ---: | --- | --- |
| 233 | `2026-05-01T09:30:00-04:00` | Follow-through after the 04-30 SPY Continuation anchor; fresh setup identity UNCLEAR. |
| 234-239 | `2026-05-01T10:30:00-04:00` through `2026-05-01T15:30:00-04:00` | Holds/fades from the morning high; no accepted new trigger. |
| 240 | `2026-05-04T09:30:00-04:00` | Opens 720.07, high 721.715, close 721.24; no accepted setup candle. |
| 241-246 | `2026-05-04T10:30:00-04:00` through `2026-05-04T15:30:00-04:00` | Pulls to 714.99 low and recovers to 718.07 close; possible base context only. |
| 247 | `2026-05-05T09:30:00-04:00` | Opens higher and closes 723.29; no accepted trigger. |
| 248-253 | `2026-05-05T10:30:00-04:00` through `2026-05-05T15:30:00-04:00` | Pushes to 725.04 high then closes 723.71; outcome and trigger remain MISSING. |

## Candidate 2: QQQ-SOURCE-WINDOW-CONTINUATION-002

| field | request |
| --- | --- |
| exact source rows | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv` lines 87-107; `2026-04-02T09:30:00-04:00` through `2026-04-07T15:30:00-04:00` |
| setup candle request | MISSING - identify the exact completed Continuation setup candle from lines 87-107, or return MISSING if no valid setup candle exists. |
| trigger request | MISSING - identify the exact Continuation trigger row and trigger level from setup-time rows only, or return MISSING. |
| failure level request | MISSING - identify the exact invalidation/failure level from setup-time evidence only, or return MISSING. |
| freshness request | UNCLEAR - decide first whether lines 87-107 are a fresh Continuation or same rebound context after QQQ lines 66-86. |
| blocker request | MISSING - complete same-context/freshness review and full blocker/caution review, including 24H, macro, IV, event, headline, option, account, broker, execution, overlap, and stale/spent signal checks. |
| outcome request | MISSING - produce terminal chart-only outcome tied to the accepted setup candle if one exists; do not treat the 04-07 recovery as proof. |
| no-hindsight request | MISSING - produce row-by-row replay output showing only evidence available at each row; ordered source rows alone are not proof. |
| what is already known | Accepted local QQQ source CSV exists; exact source rows exist; QQQ source validation was previously PASS; source-visible rebuild/hold structure exists; window is before the counted 04-08 through 04-17 QQQ Clean Fast Break lifecycle. |
| what is missing | Accepted setup candle, trigger, failure level, freshness/final-signal review, blocker/caution review, no-hindsight replay output, terminal chart-only outcome, proof this is a fresh Continuation instead of same rebound context, economics/usefulness notes, option performance, spread/slippage/fill, account risk, execution path, entry/exit usefulness, and regression protection. |
| keep/block/drop/replace | block |
| fastest next action | Decide fresh/same-context status before any proof review. If fresh identity remains UNCLEAR or fails, keep blocked and replace rather than spending single-candidate rescue work. If viable, fill exact replay fields in the same batch pass. |

### Source Row Notes

| CSV line | timestamp | row note |
| ---: | --- | --- |
| 87 | `2026-04-02T09:30:00-04:00` | Opens lower, lows 571.92, closes 578.23; possible reset/recovery context only. |
| 88 | `2026-04-02T10:30:00-04:00` | Reaches 585.9899 high and 583.96 close; no accepted trigger. |
| 89-93 | `2026-04-02T11:30:00-04:00` through `2026-04-02T15:30:00-04:00` | Holds/rebuilds into 584.96 close; setup candle remains MISSING. |
| 94 | `2026-04-06T09:30:00-04:00` | Reaches 590.61 high and 588.52 close; no accepted trigger/freshness. |
| 95-100 | `2026-04-06T10:30:00-04:00` through `2026-04-06T15:30:00-04:00` | Holds mostly 584.69-589.13 and closes 588.53; setup identity remains UNCLEAR. |
| 101-102 | `2026-04-07T09:30:00-04:00` through `2026-04-07T10:30:00-04:00` | Shakes to 578.4001 low; failure level and invalidation status MISSING/UNCLEAR. |
| 103-107 | `2026-04-07T11:30:00-04:00` through `2026-04-07T15:30:00-04:00` | Recovers to 588.72 close; recovery is not proof. |

## Candidate 3: SPY-SOURCE-WINDOW-CLEAN-FAST-BREAK-003

| field | request |
| --- | --- |
| exact source rows | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` lines 79-99; `2026-03-31T09:30:00-04:00` through `2026-04-02T15:30:00-04:00` |
| setup candle request | MISSING - identify the exact completed Clean Fast Break setup candle from lines 79-99, or return MISSING if no valid setup candle exists. |
| trigger request | MISSING - identify exact Clean Fast Break trigger row and trigger level from setup-time rows only, or return MISSING. |
| failure level request | MISSING - identify exact invalidation/failure level from setup-time evidence only, or return MISSING. |
| freshness request | MISSING - decide final-signal/stale/spent status from row-by-row replay evidence. |
| blocker request | MISSING - complete full blocker/caution review, including `CONTEXT_24H_DAILY_UNCONFIRMED`, `MACRO_UNCONFIRMED`, `IV_UNCONFIRMED`, `EVENT_UNCONFIRMED`, headline, option, account, broker, execution, and clean-break-vs-noisy-rebound checks. |
| outcome request | MISSING - produce terminal chart-only outcome tied to the accepted setup candle if one exists; do not treat the 04-01 extension as proof. |
| no-hindsight request | MISSING - produce accepted row-by-row replay output; ordered source rows alone are not proof. |
| what is already known | Accepted local SPY source CSV exists; exact source rows exist; source validation was previously PASS; unavailable context fields are explicitly unconfirmed; source rows show 03-31 rebound, 04-01 continuation, and 04-02 pullback/recovery shape. |
| what is missing | Accepted replay fixture row, setup candle, trigger, failure level, freshness/final-signal review, blocker/caution review, no-hindsight replay output, terminal chart-only outcome, economics/usefulness notes, option performance, spread/slippage/fill, account risk, execution path, entry/exit usefulness, and regression protection. |
| keep/block/drop/replace | block |
| fastest next action | Fill exact replay request fields for SPY CSV lines 79-99. Drop if row-by-row replay proves noisy rebound rather than Clean Fast Break. |

### Source Row Notes

| CSV line | timestamp | row note |
| ---: | --- | --- |
| 79 | `2026-03-31T09:30:00-04:00` | Opens 638.94, closes 642.50 after a 638.31 low; candidate context only. |
| 80 | `2026-03-31T10:30:00-04:00` | Pulls to 637.98 low, closes 640.68; potential failure/reference area is not accepted. |
| 81 | `2026-03-31T11:30:00-04:00` | Rebuilds to 642.11 close; no trigger accepted. |
| 82 | `2026-03-31T12:30:00-04:00` | Extends to 649.43 high and 647.00 close; no completed setup candle accepted. |
| 83 | `2026-03-31T13:30:00-04:00` | Holds upper area; no accepted trigger. |
| 84 | `2026-03-31T14:30:00-04:00` | Pushes to 649.91 high and 649.402 close; no accepted trigger. |
| 85 | `2026-03-31T15:30:00-04:00` | Reaches 651.53 high and 650.235 close; possible source-visible break context only. |
| 86 | `2026-04-01T09:30:00-04:00` | Gaps/extends to 656.05 high and 655.03 close; no accepted fresh trigger. |
| 87-92 | `2026-04-01T10:30:00-04:00` through `2026-04-01T15:30:00-04:00` | Continuation then fade/hold; terminal outcome is not accepted. |
| 93-99 | `2026-04-02T09:30:00-04:00` through `2026-04-02T15:30:00-04:00` | Pullback/recovery day; may weaken clean-fast-break identity, but no accepted drop decision exists. |

## Candidate 4: SPY-SOURCE-WINDOW-CONTINUATION-004

| field | request |
| --- | --- |
| exact source rows | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` lines 93-113; `2026-04-02T09:30:00-04:00` through `2026-04-07T15:30:00-04:00` |
| setup candle request | MISSING - identify the exact completed Continuation setup candle from lines 93-113, or return MISSING if no valid setup candle exists. |
| trigger request | MISSING - identify exact Continuation trigger row and trigger level from setup-time rows only, or return MISSING. |
| failure level request | MISSING - identify exact invalidation/failure level from setup-time evidence only, including whether 04-07 lows invalidate the setup. |
| freshness request | UNCLEAR - decide fresh continuation/final-signal/stale status from row-by-row replay evidence. |
| blocker request | MISSING - complete full blocker/caution review, including 04-07 shake/recovery, 24H, macro, IV, event, headline, option, account, broker, execution, overlap, and stale/spent signal checks. |
| outcome request | MISSING - produce terminal chart-only outcome tied to the accepted setup candle if one exists; do not treat the 04-07 recovery as proof. |
| no-hindsight request | MISSING - produce accepted row-by-row replay output. |
| what is already known | Accepted local SPY source CSV exists; exact source rows exist; source-visible shelf/rebuild structure exists; unavailable context fields remain unconfirmed; window is before the already counted 04-10 Clean Fast Break window. |
| what is missing | Accepted replay fixture row, setup candle, trigger, failure level, freshness/final-signal review, blocker/caution review, no-hindsight replay output, terminal chart-only outcome, proof that 04-07 did or did not invalidate the continuation, economics/usefulness notes, option performance, spread/slippage/fill, account risk, execution path, entry/exit usefulness, and regression protection. |
| keep/block/drop/replace | block |
| fastest next action | Fill exact trigger, invalidation, 04-07 invalidation/freshness status, blocker/caution, no-hindsight, outcome, and regression fields in the same batch pass. |

### Source Row Notes

| CSV line | timestamp | row note |
| ---: | --- | --- |
| 93 | `2026-04-02T09:30:00-04:00` | Opens lower, lows 645.11, closes 650.34; possible reset/recovery context only. |
| 94 | `2026-04-02T10:30:00-04:00` | Reaches 657.92 high and 655.28 close; trigger not accepted. |
| 95-99 | `2026-04-02T11:30:00-04:00` through `2026-04-02T15:30:00-04:00` | Pullback and recovery into 655.88 close; setup candle remains MISSING. |
| 100 | `2026-04-06T09:30:00-04:00` | Opens 655.86, high 659.68, closes 658.39; possible continuation hold only. |
| 101-106 | `2026-04-06T10:30:00-04:00` through `2026-04-06T15:30:00-04:00` | Holds 655.52-658.92 range; no accepted trigger/failure level. |
| 107 | `2026-04-07T09:30:00-04:00` | Drops to 651.926 low and closes 654.40; invalidation status UNCLEAR. |
| 108 | `2026-04-07T10:30:00-04:00` | Drops to 651.06 low; invalidation status UNCLEAR. |
| 109-113 | `2026-04-07T11:30:00-04:00` through `2026-04-07T15:30:00-04:00` | Recovers into 659.26 close; recovery is not proof. |

## Regression Protection Request

Before any future proof review or promotion, create replay/regression protection that verifies at least:

- fixture rows preserve exact source row boundaries for all 4 candidates
- setup candle, trigger, failure level, freshness, blocker, and outcome fields are not inferred from after-the-fact movement
- same-lifecycle or duplicate Continuation cases remain blocked unless a fresh setup rule is accepted
- `MISSING` evidence blocks proof
- `UNCLEAR` freshness or invalidation blocks proof
- terminal outcome is chart-only review input, not proof by itself
- no-hindsight replay output is required before any accepted proof count changes

## Replay Request Result

- `SPY-SOURCE-WINDOW-CONTINUATION-005`: block.
- `QQQ-SOURCE-WINDOW-CONTINUATION-002`: block.
- `SPY-SOURCE-WINDOW-CLEAN-FAST-BREAK-003`: block.
- `SPY-SOURCE-WINDOW-CONTINUATION-004`: block.

## Fastest Next Action

Run one fixture-ready replay build/review for all 4 windows together, starting with fresh/non-duplicate identity for `SPY-SOURCE-WINDOW-CONTINUATION-005` and `QQQ-SOURCE-WINDOW-CONTINUATION-002`.

If either freshness/identity issue cannot be proven from accepted setup-time evidence, keep it blocked and replace it rather than doing single-candidate rescue work.

For any survivor, fill exact setup candle, trigger, failure/invalidation, freshness/final-signal, blocker/caution, no-hindsight replay output, terminal chart-only outcome, and regression protection before proof review.

## Guardrail Result

- No proof was accepted.
- No profitability claim was made.
- Directional movement was not accepted as proof.
- Source-visible structure was treated as candidate-shape input only.
- Missing evidence remains a blocker, not low confidence.
- Unclear freshness or invalidation remains a blocker.
- Unit tests were not run by instruction.
- `main.py`, trading logic, Railway, deploy, replay runner, schemas, fixtures, generated replay outputs, live data, broker/order/account/options/P&L, alerts, and production behavior were not changed.
