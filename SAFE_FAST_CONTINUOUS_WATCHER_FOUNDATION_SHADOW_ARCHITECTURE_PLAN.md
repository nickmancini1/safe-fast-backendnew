# SAFE-FAST Continuous Watcher Foundation / Shadow Architecture Plan

## Plan Status

- Plan status: PASS
- Scope: documentation and build-control planning only
- Repo: `safe-fast-backendnew`
- Branch: `main`
- Work mode: build work only, no live trade decisions
- Watcher implementation started: no
- Production/live readiness claimed: no

This document is a future-chat-safe foundation plan for a SAFE-FAST Continuous Watcher shadow architecture. It does not implement watcher code, change `main.py`, change trading engine logic, touch Railway/deploy/production files, fetch live data, model option P&L, add account sizing, or make live trade decisions.

## Source Documents Reviewed

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_POST_GLD_WATCHER_TRANSITION_HARDENING_PLAN.md`
- `SAFE_FAST_ALL_SYMBOL_CURRENT_DEPTH_CLOSEOUT_REVIEW.md`
- `SAFE_FAST_DAY60_PRODUCT_BUSINESS_HANDOFF_ADDENDUM.md`
- `SAFE_FAST_PROJECT_MASTER_HANDOFF.md`
- `SAFE_FAST_NEWS_AND_HEADLINE_RISK_PLAN.md`

## Watcher Purpose

The watcher target is a shadow/watch-only SAFE-FAST lifecycle monitor for SPY, QQQ, IWM, and GLD. It should track forming and changing Ideal, Clean Fast Break, and Continuation setups, produce trigger-card outputs, preserve stale/spent/no-fresh-trigger discipline, suppress duplicate same-state alerts, focus attention on the best current candidate, and create review artifacts for later shadow accuracy review.

The watcher is an attention and review tool. It is not an execution system.

## Watcher Non-Goals

- No auto-trading.
- No broker/order execution.
- No option P&L or option fill modeling.
- No account sizing.
- No production/live backend promotion.
- No live trade decisions.
- No headline/news invention.
- No generated replay reports or generated chart outcome reports in this planning task.
- No replacement of SAFE-FAST setup, stage, blocker, caution, freshness, or no-trade rules.

## Required Inputs

Future watcher implementation must define and validate inputs before code promotion:

- Symbol universe: `SPY`, `QQQ`, `IWM`, `GLD`.
- Setup families: `Ideal`, `Clean Fast Break`, `Continuation`.
- Timeframe source and source-as-of metadata.
- Current and prior candle evidence sufficient to classify setup family and lifecycle state.
- Trigger level or trigger zone when available.
- Confirmation timeframe rule.
- Invalidation level or invalidation condition when available.
- Fresh/stale/spent state evidence.
- Blockers and cautions with reason codes.
- Market/session state when used.
- News/headline risk status only from a future valid source, otherwise `NEWS_UNCONFIRMED`.
- Evidence row references or equivalent deterministic source references.

## Unavailable-Field Handling

Unavailable fields must be explicit, not inferred.

- Missing numeric trigger: include the field as unavailable and avoid trigger-distance claims.
- Missing invalidation: include the field as unavailable and avoid risk or trade-readiness claims.
- Missing source-as-of: mark source freshness unavailable.
- Missing news/headline source: set news risk to `NEWS_UNCONFIRMED`.
- Missing evidence rows: block promotion beyond shadow review until deterministic evidence references exist.
- Missing completed-candle confirmation: use pending/completed-candle approval state, not live-trigger language.
- Missing fresh/stale/spent evidence: do not promote to triggered or trade-ready language.

Unavailable fields may lower focus ranking or force watch-only/no-trade status. They must never be silently treated as clear.

## Setup Families Tracked

- `Ideal`
- `Clean Fast Break`
- `Continuation`

Setup identity must be preserved through blockers and cautions. A blocked Ideal remains an Ideal, a blocked Clean Fast Break remains a Clean Fast Break, and a stale/spent Continuation remains a Continuation context instead of becoming a fresh trigger.

## Symbols Tracked

- `SPY`
- `QQQ`
- `IWM`
- `GLD`

The current all-symbol closeout supports foundation planning at known-limits depth only. IWM and GLD retain PARTIAL chart-only outcome limits.

## Lifecycle States

The watcher foundation should support these shadow lifecycle states:

- `forming/developing`: setup structure is present or emerging, but trigger path is not ready or not close enough.
- `near-trigger`: setup has a defined trigger path and is close enough to merit attention, subject to blockers/cautions.
- `pending completed-candle approval`: intrabar or provisional trigger evidence exists, but completed-candle confirmation is still required.
- `triggered signal stage`: completed trigger evidence exists for shadow signal review, without implying live trade approval.
- `blocked/no-trade`: setup exists but no-trade discipline blocks action because of structure, risk, missing fields, market/session gate, freshness, or other accepted blocker.
- `stale/spent/no-fresh-trigger`: prior trigger context exists, but it is no longer fresh and must not be treated as a current entry trigger.
- `rebuilding`: prior setup failed, stalled, or spent and requires rebuilt structure before it can become a fresh candidate again.

## Trigger-Card Output Shape

Future watcher trigger cards must follow the hardening-plan schema:

```json
{
  "symbol": "SPY | QQQ | IWM | GLD",
  "setup_type": "Ideal | Clean Fast Break | Continuation",
  "direction": "call | put | bullish | bearish | unconfirmed",
  "stage": "forming/developing | near-trigger | pending completed-candle approval | triggered signal stage | blocked/no-trade | stale/spent/no-fresh-trigger | rebuilding",
  "trigger_status": "developing | near | pending_confirmation | triggered_shadow | blocked | stale | spent | unavailable",
  "trigger_level_or_zone": "number, range, condition, or UNAVAILABLE",
  "confirmation_timeframe_rule": "completed candle/timeframe rule or UNAVAILABLE",
  "distance_to_trigger": "numeric distance, bucket, or UNAVAILABLE",
  "invalidation_level_or_condition": "number, condition, or UNAVAILABLE",
  "fresh_stale_spent_state": "fresh | stale | spent | no_fresh_trigger | unconfirmed",
  "next_check_or_next_alert_condition": "material state-change condition",
  "blockers": [],
  "cautions": [],
  "unavailable_fields": [],
  "source_as_of": "timestamp or UNAVAILABLE",
  "evidence_rows": []
}
```

Vague language such as "wait for confirmation" is insufficient unless paired with the actual trigger path, confirmation rule, unavailable fields, and next alert condition.

## Diagnostic / Explanation Scope

Diagnostics are explanation-only for the watcher foundation. They may explain:

- why a setup family was selected
- why a lifecycle state was assigned
- why a blocker or caution appears
- why a candidate is stale, spent, or no-fresh-trigger
- what evidence rows support the current state
- what unavailable fields prevent stronger claims
- what material change would flip the state

Diagnostics must not change decisions, override setup/stage logic, or promote any candidate to live-trade status unless explicitly authorized in a later tested task.

## Headline / News Handling

Headline/news risk remains a risk/context layer, not a signal engine.

- Default status: `NEWS_UNCONFIRMED`.
- Do not fetch live data in this planning task.
- Do not fabricate headlines, calendars, macro events, earnings, filings, or causal explanations.
- Keep `NEWS_UNCONFIRMED` unless a future explicitly authorized task reads a valid source.
- Future valid-source rules must define source, source-as-of timestamp, symbol relevance, expiration/staleness, severity, and caution/block behavior.
- Most news should be caution, not a hard blocker.
- News must not create trades, replace setup logic, erase setup identity, or turn a bad setup into a trade.

## Duplicate Suppression And Material-Change Alerts

Initial duplicate suppression key:

`symbol + setup_family + direction + stage + trigger_status + freshness_state + primary_blocker + trigger_zone_bucket + invalidation_bucket`

Suppress repeated same-state observations when the suppression key and material fields have not changed.

Material changes that should allow a new alert:

- stage change
- trigger status change
- fresh-to-stale or stale-to-spent change
- primary blocker change
- blocker or caution severity change
- trigger zone material movement
- invalidation material movement
- completed-candle approval state change
- new best current candidate
- previously unavailable critical field becomes available
- evidence quality materially improves or degrades

Duplicate suppression must preserve no-trade discipline. It should suppress repeated noise, not hide a new blocker, stale/spent transition, or changed trigger path.

## Best-Current-Candidate / Focus Ranking Rules

Focus ranking is for attention only. It is not trade approval.

Recommended ranking order:

1. Eligibility and lifecycle-stage validity.
2. Freshness and no-fresh-trigger discipline.
3. Setup family priority only if later explicitly defined.
4. Trigger proximity when trigger distance is available.
5. Blocker severity.
6. Context risk and cautions.
7. Stale/spent demotion.
8. Evidence quality and unavailable-field count.
9. Deterministic tie-breaker, such as symbol order then setup family order.

Do not rank simply by closest-to-trigger. A blocked, stale, or unavailable-field-heavy setup must not outrank a cleaner current candidate solely because it is closer to a level.

## No-Trade Discipline Preservation

The watcher must preserve SAFE-FAST no-trade rules:

- blocked/no-trade remains blocked even if near trigger
- stale/spent/no-fresh-trigger remains unavailable for fresh entry
- pending completed-candle approval does not become triggered until confirmation rules are satisfied
- unavailable trigger, invalidation, freshness, or source fields prevent trade-readiness claims
- market/session gates and existing accepted blockers retain priority
- focus ranking cannot override no-trade status
- shadow signal stage is not live trade approval

## Logs / Review Artifacts Needed For Shadow Review

Future shadow review needs deterministic logs and artifacts before implementation promotion:

- state observation log per symbol/setup family
- emitted alert log
- suppressed duplicate log with suppression key and reason
- trigger-card snapshot log
- lifecycle transition log
- blocker/caution change log
- unavailable-field log
- evidence-row/source reference log
- best-current-candidate ranking snapshot
- manual review labels for alert quality
- shadow review summary by symbol/setup family/stage

Review labels should support at least: correct and useful, correct but early/noisy, correct but late, wrong setup type, wrong stage, missing trigger card, duplicate/noisy, stale/spent error, and missed setup.

## Replay / Regression Gates Before Implementation

Watcher implementation must not start from this plan alone. Before implementation, a separate explicitly authorized task must define tests and gates for:

- watcher state schema/design review
- trigger-card contract/schema review
- shadow log schema review
- duplicate suppression design review
- lifecycle transition replay cases
- stale/spent/no-fresh-trigger replay cases
- unavailable-field handling cases
- material-change alert cases
- best-current-candidate ranking cases
- news `NEWS_UNCONFIRMED` default handling

Engine changes still require replay/regression cases first. This plan does not authorize engine changes.

## Promotion Gates Before Any Production / Live Use

Before any production/live use, SAFE-FAST would need a later separate promotion path with:

- passing watcher replay/regression tests
- shadow-mode run logs
- alert accuracy review
- duplicate suppression review
- stale/spent error review
- trigger-card completeness review
- unavailable-field review
- source freshness/recovery review
- news-source policy review if news is enabled
- no-trade discipline review
- manual review signoff
- explicit build-state update

These are future gates only. This plan makes no watcher readiness, production readiness, live trade readiness, option readiness, or account-sizing readiness claim.

## No-Go Boundaries

- No Railway.
- No production deploy.
- No `main.py` / engine changes in this task.
- No auto-trading.
- No broker/order execution.
- No option P&L.
- No account sizing.
- No live trade decisions.
- No generated reports created in this planning task.
- No live data fetched.
- No watcher implementation code created.

## Implementation Deferred

- Watcher code is not started.
- This plan is only a design/control handoff.
- Continuous Watcher implementation remains deferred.
- Next implementation work requires a separate explicitly authorized task with tests and a build-state update.
- Any future engine behavior change requires replay/regression cases first.

## First Watcher Foundation Implementation Candidate

Recommended next bounded watcher-foundation design step:

`trigger-card contract/schema review`

Reason: the repo pattern treats trigger cards as the core watcher product surface, and the accepted hardening plan already defines the required field shape. A trigger-card contract/schema review should lock field names, enums, unavailable-field semantics, evidence references, and no-trade wording before watcher state code, duplicate suppression, alert delivery, or shadow logs are implemented. This reduces the risk of building watcher mechanics around vague or unstable output.

This is not a code implementation recommendation. It is the next design-review task only.

