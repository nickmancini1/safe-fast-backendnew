# SAFE-FAST Shadow Log Schema Review

## Review Status

- Review status: PASS
- Scope: documentation and shadow-log schema design only
- Repo: `safe-fast-backendnew`
- Branch: `main`
- Work mode: build work only, no live trade decisions
- Continuous Watcher implementation started: no
- Watcher code created: no
- Runtime schema file created: no
- Production/live readiness claimed: no

This review defines the future SAFE-FAST watcher shadow-log record shape for later local review. It does not implement watcher code, create runtime schema files, change `main.py`, change engine logic, touch Railway/deploy/production files, fetch live data, create generated replay reports, create generated chart outcome reports, model option P&L, add account sizing, or make live trade decisions.

## Source Documents Reviewed

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_CONTINUOUS_WATCHER_FOUNDATION_SHADOW_ARCHITECTURE_PLAN.md`
- `SAFE_FAST_TRIGGER_CARD_CONTRACT_SCHEMA_REVIEW.md`
- `SAFE_FAST_WATCHER_STATE_SCHEMA_DESIGN_REVIEW.md`
- `SAFE_FAST_POST_GLD_WATCHER_TRANSITION_HARDENING_PLAN.md`
- `SAFE_FAST_ALL_SYMBOL_CURRENT_DEPTH_CLOSEOUT_REVIEW.md`
- `SAFE_FAST_CONTINUOUS_WATCHER_MVP_PLAN.md`

## Schema Purpose

The shadow log is the append-only review trail for future watcher observations, state transitions, trigger-card snapshots, alert decisions, suppressed repeats, unavailable-field handling, evidence references, and manual review labels.

The shadow log is a review artifact. It is not a trade ledger, execution log, order audit log, option P&L report, account-sizing report, production readiness proof, live trade readiness proof, or live trade decision.

## Storage Shape

The future shadow log should be line-oriented and append-only, with one JSON-compatible object per event. A JSONL-style shape is preferred for reviewability and replay-friendly diffing, but this review does not create a `.json`, `.jsonl`, or `.schema.json` runtime file.

Each log record should include:

| Field | Requirement |
| --- | --- |
| `schema_version` | Required stable version string for the shadow-log record contract. |
| `log_record_id` | Deterministic or append-safe unique record ID. |
| `event_type` | Allowed event type from this review. |
| `event_at` | Observation/log timestamp or explicit unconfirmed marker. |
| `source_as_of` | Source timestamp/as-of metadata or explicit unconfirmed marker. |
| `watch_session_id` | Deterministic watcher session/window ID when available. |
| `candidate_id` | Candidate identity from watcher state when available. |
| `symbol` | `SPY`, `QQQ`, `IWM`, `GLD`, or explicit unconfirmed handling. |
| `setup_type` | `Ideal`, `Clean Fast Break`, `Continuation`, or `UNCONFIRMED`. |
| `direction` | `bullish/call-side`, `bearish/put-side`, `neutral/unknown`, or `UNCONFIRMED`. |
| `state_version` | Watcher state version associated with this event. |
| `state_snapshot` | Required for observation, transition, trigger-card, and alert decision records. |
| `previous_state_snapshot` | Required for transition records when available; otherwise explicit unconfirmed marker. |
| `trigger_card_snapshot` | Full-card projection or explicit unavailable/incomplete marker. |
| `material_change_flags` | Material-change flags from watcher state. |
| `suppression_fingerprint` | Suppression fingerprint when relevant or explicit unavailable marker. |
| `alert_decision` | Alert/suppress/no-alert decision for alert-decision records. |
| `evidence_refs` | Deterministic source/evidence references or explicit unconfirmed marker. |
| `unavailable_fields` | Missing fields that must not be invented. |
| `review_label` | Manual or later review label, initially `UNREVIEWED`. |
| `review_notes` | Optional plain-English review notes; no live trade decisions. |

## Allowed Event Types

The shadow log should support these event types:

- `state_observation`
- `lifecycle_transition`
- `trigger_card_snapshot`
- `alert_decision`
- `suppressed_duplicate`
- `blocker_caution_change`
- `unavailable_field_change`
- `evidence_quality_change`
- `best_candidate_snapshot`
- `manual_review_label`
- `shadow_review_summary`

Event types are for later review and diagnostics only. They must not execute trades, place orders, size accounts, model options, promote production status, or create live trade decisions.

## State Snapshot Requirements

`state_snapshot` should preserve the accepted watcher state contract without field loss. At minimum it should include:

- identity fields: `candidate_id`, `symbol`, `setup_type`, `direction`, `watch_session_id`, `regular_session_date`, `state_version`
- lifecycle fields: `stage`, `trigger_status`, `fresh_stale_spent_state`
- trigger context: `trigger_level_or_zone`, `trigger_zone_bucket`, `confirmation_timeframe_rule`, `distance_to_trigger`, `invalidation_level_or_condition`, `invalidation_bucket`
- evidence fields: `source_kind`, `source_as_of`, `evidence_rows`, `evidence_quality`, `unavailable_fields`
- risk fields: `blockers`, `cautions`, `primary_blocker`, `headline_news_status`, `no_trade_reason`, `watch_only`
- transition fields: `state_changed`, `state_change_reason_codes`, `material_change_flags`, `next_check_or_next_alert_condition`
- suppression fields: `duplicate_suppression_key_fields`, `suppression_fingerprint`, `repeat_count`, `last_alerted_at`, `last_suppressed_at`, `last_suppression_reason`
- focus fields: `best_candidate_ranking_inputs`, `focus_rank_bucket`, `focus_rank_reason`
- diagnostic fields: `diagnostic_reason_codes`, `diagnostic_explanation`, `diagnostic_scope`
- output bridge fields: `trigger_card_projection_status`, `phone_alert_summary_status`, `full_card_required_fields_status`

The log must not rely on mutable wording alone. Reviewable fields and normalized reason codes must remain available.

## Trigger-Card Snapshot Requirements

When `event_type` is `trigger_card_snapshot` or `alert_decision`, the record should retain the full trigger-card projection or a clear incomplete marker.

Required trigger-card snapshot fields mirror the accepted trigger-card contract:

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
- `headline_news_status`
- `diagnostic_reason_codes`
- `no_trade_reason`
- `duplicate_suppression_key_fields`
- `best_candidate_ranking_inputs`

If the trigger-card projection is incomplete, the shadow log must show which required fields are missing and keep the candidate watch-only.

## Alert Decision Requirements

Future alert-decision records should distinguish:

- `emit_phone_alert`
- `emit_full_card_only`
- `suppress_duplicate`
- `no_alert_no_material_change`
- `no_alert_incomplete_projection`
- `no_alert_watch_only`

Alert records should include the reason codes and the material-change flags that led to the decision. Phone alerts are summaries only and must not drop stale/spent warnings, no-trade warnings, blockers, critical unavailable fields, or `NEWS_UNCONFIRMED`.

## Suppressed Duplicate Requirements

Suppressed duplicate records should preserve enough information to prove what was suppressed and why.

Required fields:

- `suppression_fingerprint`
- `duplicate_suppression_key_fields`
- `repeat_count`
- `last_alerted_at`
- `last_suppressed_at`
- `last_suppression_reason`
- `material_change_flags`
- `state_snapshot`
- `trigger_card_snapshot` or projection status

Suppression must not hide:

- new blocker
- blocker or caution severity change
- stale/spent transition
- changed trigger path
- changed invalidation context
- evidence-quality downgrade
- critical field becoming unavailable
- critical field becoming available
- new best current candidate

Detailed duplicate-suppression rules remain deferred to a later bounded duplicate suppression design review.

## Unavailable-Field Semantics

Unavailable fields must be explicit in every relevant log record. Required markers include:

- `TRIGGER_LEVEL_UNCONFIRMED`
- `DISTANCE_TO_TRIGGER_UNCONFIRMED`
- `INVALIDATION_UNCONFIRMED`
- `SOURCE_AS_OF_UNCONFIRMED`
- `EVIDENCE_ROWS_UNCONFIRMED`
- `SESSION_DATE_UNCONFIRMED`
- `FRESHNESS_UNCONFIRMED`
- `NEWS_UNCONFIRMED`

Missing trigger, invalidation, freshness, source-as-of, evidence, or news source fields must not be inferred from later movement, live assumptions, or wording. They should lower review confidence and preserve watch-only/no-trade status unless accepted evidence later resolves them.

## Manual Review Labels

The shadow log should support at least these manual review labels:

- `UNREVIEWED`
- `correct_and_useful`
- `correct_but_early_noisy`
- `correct_but_late`
- `wrong_setup_type`
- `wrong_stage`
- `wrong_trigger_status`
- `wrong_freshness_state`
- `missing_trigger_card`
- `duplicate_noisy`
- `stale_spent_error`
- `missed_setup`
- `evidence_unconfirmed`
- `unavailable_field_handling_error`
- `news_unconfirmed_expected`
- `review_inconclusive`

Manual review labels are for shadow accuracy review only. They must not become live trade approvals, option P&L claims, account-sizing decisions, production readiness claims, or live trade readiness claims.

## Shadow Review Summary Requirements

Future summary records should aggregate local shadow-log facts by:

- symbol
- setup family
- direction
- lifecycle stage
- trigger status
- freshness state
- alert decision
- review label
- blocker/caution category
- unavailable-field category
- evidence quality

Summaries should count observations, emitted alerts, suppressed duplicates, material transitions, incomplete trigger-card projections, stale/spent errors, missed setup labels, and review-inconclusive records.

Summaries must not claim generated replay results, generated chart outcomes, option P&L, account sizing, production readiness, live trade readiness, or live trade decisions.

## Privacy And Local Review Boundary

The shadow log should be local review output for later ChatGPT inspection. It should not include broker account identifiers, account balances, position sizes, order IDs, fills, option contracts, or secrets.

If a later implementation needs source identifiers or data-provider metadata, those fields should stay evidence-focused and should not become execution or account records.

## Replay / Regression Prerequisites

This schema review is a design prerequisite only. Future implementation still requires explicitly authorized tests and replay/regression cases for:

- state observation logging
- lifecycle transition logging
- stale/spent/no-fresh-trigger logging
- trigger-card snapshot completeness
- unavailable-field preservation
- material-change detection
- alert decision logging
- duplicate suppression logging
- best-current-candidate snapshot logging
- manual review label handling
- shadow review summary generation

SAFE-FAST engine changes remain out of scope and require replay/regression cases first.

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

Shadow log schema review status: PASS.

Reason: the future shadow-log record envelope, allowed event types, state snapshot requirements, trigger-card snapshot requirements, alert decision requirements, suppressed duplicate requirements, unavailable-field semantics, manual review labels, shadow summary fields, privacy/local-review boundary, replay/regression prerequisites, and no-go boundaries are documented without implementing watcher code or making live/production/options/account-sizing claims.

Continuous Watcher implementation remains deferred. The next bounded watcher-foundation design step is duplicate suppression design review only, before any watcher implementation.
