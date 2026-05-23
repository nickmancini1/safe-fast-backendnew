# SAFE-FAST Watcher State Schema / Design Review

## Review Status

- Review status: PASS
- Scope: documentation and state-schema design only
- Repo: `safe-fast-backendnew`
- Branch: `main`
- Work mode: build work only, no live trade decisions
- Continuous Watcher implementation started: no
- Watcher code created: no
- Production/live readiness claimed: no

This review defines the future internal SAFE-FAST watcher state shape that can support trigger-card generation, lifecycle tracking, stale/spent discipline, duplicate suppression, and later shadow-log review. It does not implement watcher code, create runtime schema files, change `main.py`, change engine logic, touch Railway/deploy/production files, fetch live data, create generated replay reports, create generated chart outcome reports, model option P&L, add account sizing, or make live trade decisions.

## Source Documents Reviewed

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_MASTER_HANDOFF_POST_TRIGGER_CARD_REVIEW.md`
- `SAFE_FAST_POST_GLD_WATCHER_TRANSITION_HARDENING_PLAN.md`
- `SAFE_FAST_CONTINUOUS_WATCHER_FOUNDATION_SHADOW_ARCHITECTURE_PLAN.md`
- `SAFE_FAST_TRIGGER_CARD_CONTRACT_SCHEMA_REVIEW.md`
- `SAFE_FAST_ALL_SYMBOL_CURRENT_DEPTH_CLOSEOUT_REVIEW.md`
- `SAFE_FAST_CONTINUOUS_WATCHER_MVP_PLAN.md`

## Design Purpose

The watcher state is the internal, deterministic state record for a single watched candidate. It is not the user-facing trigger card itself, but it must contain enough normalized fields to produce a trigger card, explain lifecycle transitions, preserve unavailable-field discipline, support duplicate suppression, and create later shadow-review logs.

The state record is a shadow/watch-only artifact. It is not trade approval, broker/order execution, account sizing, option P&L, production readiness, live trade readiness, or a live trade decision.

## State Identity

Each future watcher state record should be keyed by:

`symbol + setup_type + direction + watch_session_id + candidate_id`

Minimum identity fields:

| Field | Requirement |
| --- | --- |
| `candidate_id` | Deterministic ID for the active watcher candidate. |
| `symbol` | One of `SPY`, `QQQ`, `IWM`, `GLD`, or explicit unconfirmed handling. |
| `setup_type` | `Ideal`, `Clean Fast Break`, `Continuation`, or `UNCONFIRMED`. |
| `direction` | `bullish/call-side`, `bearish/put-side`, `neutral/unknown`, or `UNCONFIRMED`. |
| `watch_session_id` | Deterministic session/window identifier, not an account or broker session. |
| `regular_session_date` | Session date when known; otherwise explicit unconfirmed marker. |
| `first_seen_at` | Source timestamp or observation timestamp when first seen. |
| `last_seen_at` | Source timestamp or observation timestamp when last seen. |
| `state_version` | Monotonic version for this candidate state record. |

`candidate_id` should not depend on mutable wording. It should be derived from stable evidence references when available and from deterministic identity inputs when evidence rows are unavailable.

## Required Watcher State Fields

Every future full watcher state record should include these field groups:

| Group | Required fields |
| --- | --- |
| Identity | `candidate_id`, `symbol`, `setup_type`, `direction`, `watch_session_id`, `regular_session_date`, `state_version` |
| Lifecycle | `stage`, `trigger_status`, `fresh_stale_spent_state`, `previous_stage`, `previous_trigger_status`, `previous_fresh_stale_spent_state` |
| Trigger context | `trigger_level_or_zone`, `trigger_zone_bucket`, `confirmation_timeframe_rule`, `distance_to_trigger`, `invalidation_level_or_condition`, `invalidation_bucket` |
| Evidence | `source_kind`, `source_as_of`, `evidence_rows`, `evidence_quality`, `unavailable_fields` |
| Risk and discipline | `blockers`, `cautions`, `primary_blocker`, `headline_news_status`, `no_trade_reason`, `watch_only` |
| Transition support | `state_changed`, `state_change_reason_codes`, `material_change_flags`, `next_check_or_next_alert_condition` |
| Suppression support | `duplicate_suppression_key_fields`, `suppression_fingerprint`, `repeat_count`, `last_alerted_at`, `last_suppressed_at`, `last_suppression_reason` |
| Focus support | `best_candidate_ranking_inputs`, `focus_rank_bucket`, `focus_rank_reason` |
| Diagnostics | `diagnostic_reason_codes`, `diagnostic_explanation`, `diagnostic_scope` |
| Output bridge | `trigger_card_projection_status`, `phone_alert_summary_status`, `full_card_required_fields_status` |

## Allowed Values

The watcher state must use the accepted trigger-card enums where fields overlap.

### `setup_type`

- `Ideal`
- `Clean Fast Break`
- `Continuation`
- `UNCONFIRMED`

### `direction`

- `bullish/call-side`
- `bearish/put-side`
- `neutral/unknown`
- `UNCONFIRMED`

### `stage`

- `forming/developing`
- `near-trigger`
- `pending_completed_candle_approval`
- `triggered_signal_stage`
- `blocked/no-trade`
- `stale/spent/no-fresh-trigger`
- `rebuilding`
- `unavailable/unconfirmed`

### `trigger_status`

- `no_valid_trigger`
- `waiting_for_trigger`
- `near_trigger`
- `pending_completed_candle`
- `triggered`
- `failed_hold`
- `stale`
- `spent`
- `unconfirmed`

### `fresh_stale_spent_state`

- `fresh`
- `stale`
- `spent`
- `prior-session`
- `rebuilding`
- `unconfirmed`

### `evidence_quality`

- `deterministic`
- `partial`
- `unconfirmed`
- `missing`

### `state_changed`

- `true`
- `false`
- `unconfirmed`

### `material_change_flags`

Allowed flags:

- `stage_changed`
- `trigger_status_changed`
- `freshness_changed`
- `primary_blocker_changed`
- `blocker_severity_changed`
- `caution_severity_changed`
- `trigger_zone_changed`
- `invalidation_changed`
- `best_candidate_changed`
- `evidence_quality_changed`
- `critical_field_became_available`
- `critical_field_became_unavailable`
- `session_boundary_changed`
- `no_material_change`

### `headline_news_status`

- `NEWS_CLEAR`
- `NEWS_CAUTION`
- `NEWS_BLOCK`
- `NEWS_UNCONFIRMED`

Default remains `NEWS_UNCONFIRMED` unless a later explicit valid-source review reads and documents a valid headline/news source.

## Unavailable-Field Semantics

Unavailable fields must be explicit in watcher state and must project into trigger cards without being softened or hidden.

Required explicit markers include:

- `TRIGGER_LEVEL_UNCONFIRMED`
- `DISTANCE_TO_TRIGGER_UNCONFIRMED`
- `INVALIDATION_UNCONFIRMED`
- `SOURCE_AS_OF_UNCONFIRMED`
- `EVIDENCE_ROWS_UNCONFIRMED`
- `SESSION_DATE_UNCONFIRMED`
- `FRESHNESS_UNCONFIRMED`
- `NEWS_UNCONFIRMED`

If a critical field is unavailable, the state must not claim live trade readiness, option readiness, account readiness, production readiness, or a completed live-trade decision. Missing trigger, invalidation, freshness, source-as-of, or evidence should force watch-only/no-trade wording unless accepted evidence proves otherwise.

## Lifecycle Transition Rules

The state model must preserve these transition rules:

- `forming/developing` can advance to `near-trigger` only when a trigger path is defined or explicitly tracked as a known zone/condition.
- `near-trigger` can advance to `pending_completed_candle_approval` only when provisional trigger evidence exists and the completed-candle rule is still unresolved.
- `pending_completed_candle_approval` can advance to `triggered_signal_stage` only when the accepted confirmation rule is satisfied.
- `triggered_signal_stage` remains shadow signal review only and must not imply live trade approval.
- Any stage can degrade to `blocked/no-trade` when an accepted blocker or critical unavailable field prevents stronger claims.
- Prior or already-used trigger context must become `stale/spent/no-fresh-trigger` unless accepted fresh current-session evidence exists.
- `stale/spent/no-fresh-trigger` can move to `rebuilding` only when the old trigger path is no longer the current candidate and rebuilt structure is being watched.
- `rebuilding` can move toward `forming/developing` or `near-trigger` only through a new valid setup path, not by reusing spent evidence.
- `unavailable/unconfirmed` must remain watch-only until missing identity, source, evidence, or lifecycle fields become confirmed.

Transitions must be based on accepted evidence and existing SAFE-FAST rules. Diagnostics, focus ranking, trigger proximity, and phone-alert urgency must not override no-trade discipline.

## State Change Detection

A future watcher state update should be considered material when any of these changes occur:

- stage changes
- trigger status changes
- freshness changes, especially fresh to stale or spent
- primary blocker changes
- blocker or caution severity changes
- trigger zone changes materially
- invalidation changes materially
- critical unavailable field becomes available or unavailable
- evidence quality changes materially
- session boundary changes state interpretation
- best current candidate changes

Repeated same-state observations should update `last_seen_at` and `repeat_count`, but should not create a new alert unless a later bounded design explicitly adds heartbeat reporting.

## Trigger-Card Projection

The watcher state must be able to project into the accepted trigger-card contract without field loss.

Projection requirements:

- Every required trigger-card field must map from a watcher state field or an explicit unconfirmed marker.
- `blockers`, `cautions`, `headline_news_status`, `diagnostic_reason_codes`, `no_trade_reason`, `duplicate_suppression_key_fields`, and `best_candidate_ranking_inputs` must remain available for full-card review.
- Phone alerts may summarize state, but they must not drop no-trade warnings, stale/spent wording, or critical unavailable-field warnings.
- The full-card projection must remain reviewable later from local/laptop watcher output.

If projection cannot produce all required full-card fields, set `trigger_card_projection_status` to incomplete and keep the candidate watch-only.

## Duplicate Suppression Bridge

The watcher state should expose the accepted suppression key inputs:

`symbol + setup_family + direction + stage + trigger_status + freshness_state + primary_blocker + trigger_zone_bucket + invalidation_bucket`

State records should also retain:

- `suppression_fingerprint`
- `repeat_count`
- `last_alerted_at`
- `last_suppressed_at`
- `last_suppression_reason`

Suppression must not hide a new blocker, stale/spent transition, changed trigger path, changed invalidation context, evidence-quality downgrade, or new best current candidate.

## Best Current Candidate Support

Watcher state may include focus-ranking inputs, but focus ranking is attention-only.

Required ranking inputs:

- eligibility/stage validity
- freshness
- setup family priority only if explicitly defined
- trigger proximity when available
- blocker severity
- context risk
- stale/spent demotion
- evidence quality
- unavailable-field count
- deterministic tie-breaker

A blocked, stale, spent, unconfirmed, or evidence-poor candidate must not outrank a cleaner current candidate solely because it is closer to a trigger level.

## Diagnostics Scope

Diagnostic fields may explain:

- setup type
- lifecycle stage
- trigger status
- blocker or caution
- freshness state
- stale/spent/no-fresh-trigger status
- unavailable fields
- evidence quality
- next check or next alert condition

Diagnostics must not change decisions, override setup/stage logic, override blockers, override stale/spent discipline, or promote any state to live trade status.

## Shadow Review Readiness

This state schema is sufficient as a design prerequisite for later shadow-log schema review because it identifies:

- stable candidate identity
- lifecycle state and prior state
- material-change flags
- evidence and source fields
- unavailable-field handling
- trigger-card projection fields
- duplicate suppression fields
- focus-ranking fields
- diagnostic fields

It is not runtime proof. Later implementation still requires explicitly authorized tests and replay/regression cases for lifecycle transitions, stale/spent handling, unavailable-field handling, material-change alerts, duplicate suppression, trigger-card projection, and focus ranking.

## No-Go Boundaries

- No watcher implementation.
- No watcher runtime schema file.
- No `main.py` / engine changes.
- No Railway.
- No production.
- No auto-trading.
- No broker/order execution.
- No option P&L.
- No account sizing.
- No live trade decisions.
- No generated replay reports.
- No generated chart outcome reports.
- No live data fetches.
- No production readiness or live trade readiness claims.

## Review Decision

Watcher state schema/design review status: PASS.

Reason: the future internal watcher state identity, required fields, enums, unavailable-field semantics, lifecycle transition rules, material-change detection, trigger-card projection bridge, duplicate suppression bridge, best-current-candidate support, diagnostics scope, shadow-review prerequisites, and no-go boundaries are documented without implementing watcher code or making live/production/options/account-sizing claims.

Continuous Watcher implementation remains deferred. The next bounded watcher-foundation design step is shadow log schema review only, before duplicate suppression design review or any watcher implementation.
