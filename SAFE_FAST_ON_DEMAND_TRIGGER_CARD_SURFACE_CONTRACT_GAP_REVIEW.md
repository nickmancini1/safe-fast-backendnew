# SAFE-FAST On-Demand Trigger Card Surface Contract Gap Review

## Review Status

- Review status: PASS
- Baseline: patch8
- Repo: safe-fast-backendnew
- Branch: main
- Work mode: build work only, no live trade decisions

## Baseline Checked

- SPY/QQQ closeout complete: yes. Repo evidence keeps SPY and QQQ real historical replay/chart closeout accepted.
- Trigger-card requirement review complete: yes. `SAFE_FAST_ON_DEMAND_TRIGGER_CARD_REQUIREMENT_REVIEW.md` found SPY and QQQ trigger-card surface coverage PARTIAL.
- SPY/QQQ audits PARTIAL: yes. Existing artifacts prove trigger/stage metadata and selected user-facing stage language, not complete trigger-card fields.
- IWM still next: yes. IWM remains the next broader coverage target after trigger-card surface contract planning/coverage.
- GLD deferred: yes.
- Continuous Watcher deferred: yes.
- Do-not-touch boundaries: this review is docs-only. No `main.py`, engine logic, replay runner logic, schemas, fixtures, generated reports, Railway, production, option P&L, account sizing, auto-trading, live trade decisions, or Continuous Watcher implementation are touched.

## Repo State Checked

- Git status result: `## main...origin/main`
- Latest commits:
  - `5dc2481 Add on-demand trigger card requirement review`
  - `5d114c8 Add IWM historical sample collection worksheet`
  - `1ff5daf Add IWM historical replay candidate selection review`
  - `8b49ca6 Add IWM fixture replay candidate inventory`
  - `de6cf3b Add IWM broader coverage planning review`
  - `5c1e564 Add next broader coverage decision review`
  - `3faf90d Repair build-state header after QQQ closeout`
  - `5d33edc Add QQQ chart outcome closeout review`
  - `723a69f Add QQQ post-aggregate chart outcome decision review`
  - `ac1d046 Add QQQ aggregate chart outcome output validation`
  - `872906e Add QQQ chart outcome aggregate summary`
  - `29fc799 Add QQQ Continuation chart outcome output validation`
- `5dc2481` present: yes.
- Conflicts found: none. The known `5d33edc` QQQ closeout milestone vs newer HEAD distinction is not a conflict.

## Existing Protection Found

- Trigger-stage correctness: protected by `replay/test_on_demand_trigger_stage_contract.py`, including intrabar Continuation breaks waiting for completed-candle approval, completed triggers while market closed not becoming live trades, and too-early holds not becoming trigger-ready.
- Pending completed candle approval: protected by `replay/test_on_demand_soft_extension_pending_trigger_contract.py` and `replay/test_on_demand_pending_completed_approval_surface_contract.py`, including specific completed 1H approval language with trigger level instead of generic live-trigger wording.
- Spent/stale Continuation behavior: protected by session-boundary and spent/prior Continuation contracts that prevent prior completed shelf breaks from becoming fresh triggers and prevent spent Continuation context from stealing winner/setup identity from fresh Ideal or Clean Fast Break candidates.
- Session-boundary carry-forward: protected by `replay/test_on_demand_session_boundary_contract.py`, `replay/test_on_demand_session_boundary_surface_contract.py`, `replay/test_on_demand_session_boundary_fresh_break_contract.py`, weekend carry, and holiday carry contracts.
- User-facing stage surface: protected by `replay/test_on_demand_user_facing_stage_surface_contract.py`, session-boundary surface coverage, pending completed approval surface coverage, 24H/macro/IV surface contracts, and next-bar hold failure surface coverage.
- Setup identity across Ideal / Clean Fast Break / Continuation: protected by Ideal chop identity, Clean Fast Break chop identity, spent Continuation / Ideal identity, spent Continuation / Clean Fast Break identity, mixed setup stage, winner-selection, and raw NO_TRADE winner override contracts.
- Put-side Continuation stage behavior: protected by `replay/test_on_demand_put_continuation_stage_contract.py`, including inverse below-shelf trigger path and market-closed completed trigger gating.

## Gap Identified

The remaining gap is user-facing trigger-card completeness, not a full SPY/QQQ replay redo.

Repo evidence already protects many internal trigger-state, stage, freshness, identity, and selected user-facing messages. It does not yet prove that every valid, developing, pending, triggered, stale, or spent setup exposes one complete trigger card with all fields together.

Missing or unproven trigger-card fields:

- actual trigger level or zone
- candle/timeframe confirmation rule
- current distance to trigger when available
- early-warning/near-trigger threshold when available
- invalidation level or condition
- fresh/stale/spent rule
- next check or next alert condition
- blocker/caution relationship to trigger readiness

## Required Contract Coverage

Needed future contract tests:

1. Ideal trigger-card surface contract: proves Ideal setup type, direction, stage, trigger status, retest/recovery trigger zone, completed-candle rule, invalidation, freshness rule, next check, and readiness blockers/cautions are surfaced together.
2. Clean Fast Break trigger-card surface contract: proves Clean Fast Break setup type, direction, stage, trigger status, tight-pause/base break level, completed-candle rule, invalidation, freshness rule, next check, and readiness blockers/cautions are surfaced together.
3. Continuation trigger-card surface contract: proves Continuation setup type, direction, stage, trigger status, shelf/reclaim/hold/break path, shelf trigger level or zone, completed-candle rule, invalidation, freshness rule, next check, and readiness blockers/cautions are surfaced together.
4. Put-side trigger-card surface contract: proves inverse put-side trigger direction and below-shelf confirmation are surfaced as user-facing card fields, not only internal stage state.
5. Stale/spent trigger-card surface contract: proves prior/stale/spent Continuation states show no fresh trigger, spent rule, trigger reference when available, invalidation/condition when available, and the next valid recheck condition.
6. Blocked-but-identifiable setup trigger-card surface contract: proves Ideal, Clean Fast Break, or Continuation identity remains visible on the trigger card when blockers/cautions prevent readiness.
7. Near-trigger / early-warning trigger-card surface contract, if current engine data supports it: proves distance-to-trigger and early-warning threshold fields are present and correctly labeled when available.
8. Missing-data/unconfirmed trigger-card surface contract, if live fields are unavailable: proves unavailable trigger-card fields are marked unconfirmed rather than invented.

## Test Priority

1. Continuation stale/spent trigger card
2. Ideal forming/pending trigger card
3. Clean Fast Break forming/pending trigger card
4. Put-side trigger card
5. Blocked setup trigger card
6. Near-trigger/early-warning card
7. Missing-data/unconfirmed card

## Impact On SPY/QQQ

- SPY/QQQ replay closeout remains accepted.
- No replay redo required.
- Follow-up work is surface-contract coverage.

## Impact On IWM/GLD

- IWM/GLD replay/review assets must include trigger-card surface checks.
- Deeper IWM sample work should resume after the first trigger-card surface contract task is planned or created.
- GLD remains deferred.

## Recommended Next Task

Create first on-demand trigger-card surface contract test, starting with Continuation stale/spent trigger card.

## Boundary Check

- main.py changed: no
- engine logic changed: no
- replay runner changed: no
- schemas changed: no
- fixtures changed: no
- reports changed: no
- Railway touched: no
- production touched: no
- Continuous Watcher implementation started: no
- option P&L modeled: no
- account sizing added: no
- auto-trading added: no
- live trade decisions added: no

## What Remains Unproven

- trigger-card surface contracts
- IWM sample population
- IWM replay coverage
- IWM chart-only outcomes
- IWM aggregate closeout
- GLD broader coverage
- Continuous Watcher behavior
- alert suppression
- shadow/live validation
- option P&L
- account sizing
- production readiness
