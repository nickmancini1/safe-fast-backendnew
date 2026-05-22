# SAFE-FAST Post-GLD Watcher Transition Hardening Plan

## Status

- **Plan status:** PASS
- **Scope:** docs/build-control clarification only
- **Active GLD work:** unchanged; GLD Continuation 001 fixture output validation and chart outcome closeout still come first
- **Continuous Watcher:** deferred
- **Watcher implementation started:** no
- **Production/live readiness claimed:** no

This plan hardens the future transition from GLD closeout into any Continuous Watcher foundation task. It does not start watcher implementation, change engine behavior, change `main.py`, touch Railway/deploy/production files, model option P&L, add account sizing, or make live trade decisions.

## Future Chat Handoff Rule

Before any post-GLD watcher task, future chats must read:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_POST_GLD_WATCHER_TRANSITION_HARDENING_PLAN.md`
- any current closeout/readiness review named by build state

Future chats must not infer watcher readiness from a single GLD fixture, chart-only outcome, or bookkeeping sync commit.

## Do Not Confuse With Active GLD Work

The active objective remains GLD Continuation 001 fixture output validation only. After that, GLD chart-only outcome closeout and current-depth closeout must still be completed before watcher transition review.

This plan is a referenced clarification plan, not a replacement objective. Do not claim GLD is complete from this document.

## No-Go Boundaries Preserved

- Do not touch `main.py` or trading engine logic unless a later task explicitly authorizes it with replay/regression cases first.
- Do not touch Railway, deploy, production, broker/order execution, auto-trading, account sizing, option P&L, live backend, or production/live trading logic.
- Do not make live trade decisions.
- Do not claim watcher readiness, production readiness, option readiness, account-sizing readiness, or live-trade readiness.
- News/headline context remains `NEWS_UNCONFIRMED` unless a valid source is actually read.

## 1. Known-Limits Closeout Checklist

Allowed matrix statuses are only: `PASS`, `PARTIAL`, `BLOCKED`, `NOT_STARTED`, `DEFERRED`, `NO_GO`.

Future chats must use this matrix before claiming a symbol/setup family is complete. "Current known-limits depth" means this exact matrix, with one row per symbol/setup family and one status per required artifact/check.

| Symbol / setup family | Source CSV | Source validation | Bounded windows | Worksheet | Readiness review | Real historical replay review | Fixture specification | Fixture asset | Fixture output validation | Chart outcome planning | Per-setup chart outcome review | Aggregate summary | Closeout |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SPY / Ideal | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SPY / Clean Fast Break | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SPY / Continuation | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| QQQ / Ideal | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| QQQ / Clean Fast Break | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| QQQ / Continuation | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| IWM / Ideal | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| IWM / Clean Fast Break | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| IWM / Continuation | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| GLD / Ideal | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | NOT_STARTED | NOT_STARTED | NOT_STARTED | NOT_STARTED |
| GLD / Clean Fast Break | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | NOT_STARTED | NOT_STARTED | NOT_STARTED | NOT_STARTED |
| GLD / Continuation | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | NOT_STARTED | NOT_STARTED | NOT_STARTED | NOT_STARTED | NOT_STARTED |

Any `PARTIAL`, `BLOCKED`, `NOT_STARTED`, `DEFERRED`, or `NO_GO` cell must be named as a known limit in the all-symbol closeout review.

## 2. Build-State Bookkeeping Convention

Build state must separate:

- latest completed milestone commit
- current repo HEAD / bookkeeping sync commits

Bookkeeping-only commits are not conflicts. A milestone commit remaining older than HEAD is allowed when newer commits are sync-only. Exact conflict naming is required only when repo/build-state disagree on active objective, milestone status, or no-go boundaries.

## 3. Watcher Entry Criteria

Continuous Watcher foundation must not start until this minimum gate passes:

- SPY / QQQ / IWM / GLD current-depth closeout complete
- Ideal / Clean Fast Break / Continuation represented
- trigger-card fields documented
- stale, spent, and no-fresh-trigger rules preserved
- duplicate suppression requirements documented
- no production/live/auto-trade assumptions

Watcher work starts as shadow/watch-only only.

## 4. Diagnostics Scope

Diagnostics are explanation-only at first. They may explain why SAFE-FAST called a setup, stage, blocker, caution, next step, freshness, stale/spent state, or no-go status.

Diagnostics must not change decisions until explicitly approved later. They should expose evidence rows, reason codes, missing fields, and what would flip state.

## 5. Headline/News Source And Expiration Policy

News/headline risk remains a risk/context layer, not a signal engine. Keep `NEWS_UNCONFIRMED` unless a valid source is read.

Future rules must define valid source, `timestamp/source_as_of`, symbol relevance, same-day versus overnight relevance, expiration/staleness, severity, and whether caution/block applies.

Most news should be caution, not a hard blocker. Hard block only for immediate/material risk to the setup, trade window, hold window, gap risk, liquidity/execution, or event-driven invalidation.

## 6. Trigger-Card Schema

Before watcher work, trigger cards need this stable shape:

- `symbol`
- `setup_type`
- `direction`
- `stage`
- `trigger_status`
- `trigger_level_or_zone`
- `confirmation_timeframe_rule`
- `distance_to_trigger`
- `invalidation_level_or_condition`
- `fresh_stale_spent_state`
- `next_check_or_next_alert_condition`
- `blockers`
- `cautions`
- `unavailable_fields`
- `source_as_of`
- `evidence_rows`

Vague "wait for confirmation" language is not enough without a trigger path.

## 7. Duplicate Suppression Keys

Initial duplicate suppression key:

`symbol + setup_family + direction + stage + trigger_status + freshness_state + primary_blocker + trigger_zone_bucket + invalidation_bucket`

Material changes that should alert:

- stage change
- trigger status change
- fresh-to-stale/spent change
- blocker/caution severity change
- trigger zone material movement
- invalidation material movement
- new best candidate

Non-material repeated same-state observations are suppressible.

## 8. Best Current Candidate / Focus Ranking

Watcher focus ranking order:

1. eligibility/stage validity
2. freshness
3. setup family priority only if explicitly defined
4. trigger proximity
5. blocker severity
6. context risk
7. stale/spent demotion
8. evidence quality
9. deterministic tie-breaker

Do not rank simply by closest-to-trigger. No-trade discipline stays above attention/focus ranking.

## 9. Chart-Only Outcome Boundary

Chart-only outcomes support signal/watchability review only. They do not prove options profitability, option fills, Greeks, spread behavior, account safety, production readiness, or live trade readiness.

After GLD closeout, transition notes must say chart-only closeout supports watcher foundation, not live trading.

## 10. All-Symbol Closeout / Readiness Review

Before watcher implementation, create and pass:

`SAFE_FAST_ALL_SYMBOL_CURRENT_DEPTH_CLOSEOUT_REVIEW.md`

That review must confirm SPY / QQQ / IWM / GLD current-depth coverage, known limits, no-go items, trigger-card status, diagnostics/news deferral status, and the exact watcher foundation objective.

Do not start watcher implementation before this review passes.

## Next Task After This Docs Update

Return to GLD Continuation 001 fixture output validation. Do not create chart outcomes, aggregate closeout, watcher work, option P&L, account sizing, production readiness, or live trade decisions in this docs update.
