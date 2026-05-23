# SAFE-FAST Duplicate Suppression Design Review

## Review Status

- Review status: PASS
- Scope: documentation and duplicate-suppression design only
- Repo: `nickmancini1/safe-fast-backendnew`
- Branch: `main`
- Baseline: `patch8`
- Work mode: build work only, no live trade decisions
- Continuous Watcher implementation started: no
- Watcher runtime code created: no
- Runtime schema files created: no
- Production/live readiness claimed: no

This review defines the future SAFE-FAST duplicate suppression design for repeated watcher alerts and trigger cards. It does not implement watcher code, create runtime schema files, change `main.py`, change engine logic, touch Railway/deploy/production files, fetch live data, create generated replay reports, create generated chart outcome reports, model option P&L, add account sizing, or make live trade decisions.

Continuous Watcher implementation remains deferred.

## Source Documents Reviewed

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_STRICT_MASTER_HANDOFF_POST_SHADOW_LOG_REVIEW.md`
- `SAFE_FAST_TRIGGER_CARD_CONTRACT_SCHEMA_REVIEW.md`
- `SAFE_FAST_WATCHER_STATE_SCHEMA_DESIGN_REVIEW.md`
- `SAFE_FAST_SHADOW_LOG_SCHEMA_REVIEW.md`

## Design Purpose

Duplicate suppression should reduce repeated same-state phone alerts and repeated full-card noise while preserving every material change that could affect review, watchability, stale/spent discipline, unavailable-field handling, or future shadow audit.

The purpose is to suppress repeated same-state alerts/cards without hiding material changes.

Suppression is an attention-management layer only. It must not approve trades, hide no-trade reasons, hide stale/spent status, override blockers, override trigger-card wording rules, or change SAFE-FAST engine behavior.

## Accepted Suppression Key Inputs

Future duplicate suppression must use this accepted key:

`symbol + setup_family + direction + stage + trigger_status + freshness_state + primary_blocker + trigger_zone_bucket + invalidation_bucket`

Required field meanings:

| Key input | Normalized source |
| --- | --- |
| `symbol` | Watcher state `symbol`; full-card `symbol`. |
| `setup_family` | Watcher state `setup_type`; full-card `setup_type`; normalized to the accepted setup-family enum. |
| `direction` | Watcher state `direction`; full-card `direction`. |
| `stage` | Watcher state `stage`; full-card `stage`. |
| `trigger_status` | Watcher state `trigger_status`; full-card `trigger_status`. |
| `freshness_state` | Watcher state `fresh_stale_spent_state`; full-card `fresh_stale_spent_state`. |
| `primary_blocker` | Watcher state `primary_blocker`; derived from normalized blocker reason code, not mutable prose. |
| `trigger_zone_bucket` | Watcher state `trigger_zone_bucket`; derived from accepted trigger level/zone rules or explicit unconfirmed marker. |
| `invalidation_bucket` | Watcher state `invalidation_bucket`; derived from accepted invalidation rules or explicit unconfirmed marker. |

The key must be built from normalized fields and reason codes, not human-facing text alone. If a required key field is unavailable, the key must include the explicit unconfirmed marker rather than inventing a value.

## Required Normalized Inputs

Future watcher state and trigger-card projection must expose these normalized inputs before suppression can make a decision:

- Candidate identity: `candidate_id`, `watch_session_id`, `state_version`, `regular_session_date`.
- Setup identity: `symbol`, `setup_type`, `direction`.
- Lifecycle state: `stage`, `trigger_status`, `fresh_stale_spent_state`.
- Trigger context: `trigger_level_or_zone`, `trigger_zone_bucket`, `confirmation_timeframe_rule`, `distance_to_trigger`.
- Invalidation context: `invalidation_level_or_condition`, `invalidation_bucket`.
- Risk context: `blockers`, `cautions`, `primary_blocker`, blocker severity, caution severity, `no_trade_reason`, `watch_only`.
- Evidence context: `source_kind`, `source_as_of`, `evidence_rows`, `evidence_quality`, `unavailable_fields`.
- News context: `headline_news_status`, defaulting to `NEWS_UNCONFIRMED` unless a later explicit news-source review reads a valid source.
- Transition context: `previous_stage`, `previous_trigger_status`, `previous_fresh_stale_spent_state`, `state_changed`, `state_change_reason_codes`, `material_change_flags`.
- Output context: `trigger_card_projection_status`, `phone_alert_summary_status`, `full_card_required_fields_status`.
- Focus context: `best_candidate_ranking_inputs`, `focus_rank_bucket`, `focus_rank_reason`.
- Suppression context: `duplicate_suppression_key_fields`, `suppression_fingerprint`, `repeat_count`, `last_alerted_at`, `last_suppressed_at`, `last_suppression_reason`.

If the full trigger-card projection is incomplete, suppression may prevent phone noise, but the shadow log must still preserve the incomplete projection status and unavailable fields.

## Suppression Fingerprint Rules

The future `suppression_fingerprint` should be a deterministic representation of:

- the accepted suppression key inputs
- normalized blocker and caution severity summaries
- normalized trigger path identifier
- evidence-quality state
- critical unavailable-field set
- session-boundary interpretation state
- best-current-candidate identity or deterministic rank bucket when available
- source freshness/as-of bucket when available
- `headline_news_status` only when the status is source-confirmed

Fingerprint rules:

- Use normalized enums, buckets, reason codes, and deterministic identifiers.
- Do not hash mutable phone-alert wording or full-card prose as the primary identity.
- Preserve explicit unconfirmed markers in the fingerprint.
- Treat missing and unconfirmed differently from confirmed none.
- Keep stale/spent/no-fresh-trigger status visible in the fingerprint.
- Recompute the fingerprint on each state observation before deciding whether to alert, suppress, or log no-alert/no-material-change.
- Store the fingerprint in watcher state and every relevant shadow-log alert or suppression record.

The exact hash algorithm remains a future implementation detail. The design requirement is deterministic equality for same-state repeats and deterministic inequality for material changes.

## Material Changes That Must Break Suppression

Suppression must not hide any of these changes:

- stage change
- trigger_status change
- freshness/stale/spent transition
- primary blocker change
- blocker/caution severity change
- trigger-zone material movement
- invalidation material movement
- evidence quality change
- critical field became available
- critical field became unavailable
- session-boundary interpretation change
- new best current candidate
- trigger path changed
- `headline_news_status` change only when source-confirmed

Each material change should produce a new alert decision path and a shadow-log record explaining why the previous duplicate state no longer applies.

## Non-Material Repeats That May Be Suppressed

Same-state repeats may be suppressed when all accepted suppression key fields and material-change checks are unchanged.

Examples of suppressible repeats:

- Same symbol, setup family, direction, stage, trigger status, freshness state, primary blocker, trigger-zone bucket, and invalidation bucket.
- Same no-trade reason with no new blocker, no blocker severity change, and no caution severity change.
- Same stale/spent/no-fresh-trigger state where no fresh trigger path has appeared.
- Same unavailable-field set with no critical field becoming available or unavailable.
- Same evidence quality and evidence reference bucket.
- Same best-current-candidate identity or same deterministic focus bucket.
- Same `NEWS_UNCONFIRMED` status.
- Wording-only changes that do not alter normalized state, reason codes, material fields, or review meaning.

Suppressed repeats should still update repeat counters and last-seen/last-suppressed metadata in future watcher state and shadow logs.

## Stale / Spent No-Fresh-Trigger Discipline

Duplicate suppression must preserve stale/spent discipline:

- A stale/spent card must explicitly remain `stale/spent/no-fresh-trigger`.
- Repeated stale/spent cards may be suppressed only when no fresh trigger path, rebuilding path, blocker change, evidence-quality change, or session-boundary reinterpretation appears.
- A fresh current-session trigger path must break suppression even if it shares symbol, setup family, direction, or nearby price context with a prior spent setup.
- A transition from fresh to stale, stale to spent, prior-session to stale/spent, or stale/spent to rebuilding is material.
- Phone alerts and full cards must not imply actionability for stale/spent repeated context.

No-fresh-trigger wording must remain visible in the full-card record and any phone alert that is emitted.

## Unavailable Fields And NEWS_UNCONFIRMED

Unavailable fields must use explicit markers such as:

- `TRIGGER_LEVEL_UNCONFIRMED`
- `DISTANCE_TO_TRIGGER_UNCONFIRMED`
- `INVALIDATION_UNCONFIRMED`
- `SOURCE_AS_OF_UNCONFIRMED`
- `EVIDENCE_ROWS_UNCONFIRMED`
- `SESSION_DATE_UNCONFIRMED`
- `FRESHNESS_UNCONFIRMED`
- `NEWS_UNCONFIRMED`

Unavailable-field rules:

- Do not infer missing trigger, invalidation, freshness, source, evidence, session, or news fields from later movement or live assumptions.
- A critical field becoming available must break suppression.
- A critical field becoming unavailable must break suppression.
- Missing trigger, invalidation, freshness, source-as-of, or evidence should preserve watch-only/no-trade wording unless accepted evidence later resolves the field.
- Suppression may treat repeated unavailable-field states as duplicates only when the unavailable-field set and all material state fields are unchanged.

Headline/news rules:

- Default to `NEWS_UNCONFIRMED`.
- `NEWS_UNCONFIRMED` repeats are non-material unless a later explicit source-confirmed status replaces them.
- A `headline_news_status` change breaks suppression only when source-confirmed.
- Do not create news blockers or cautions without a valid source.
- Do not invent headlines, macro events, earnings, filings, signals, outcomes, trigger levels, P&L, or trade facts.

## Phone Alert Vs Laptop / Full-Card Behavior

Phone behavior:

- Phone alerts should be short and should avoid repeated same-state noise.
- Suppressed phone repeats must not erase shadow-log audit records.
- Phone summaries must preserve symbol, setup family, stage, trigger zone/level or unconfirmed marker, next condition, freshness state, blocker/caution summary, `headline_news_status`, and no-trade warning when applicable.
- Phone alerts must emit again for material changes.

Laptop/full-card behavior:

- The full-card output remains the complete local review artifact.
- A repeated full card may be marked suppressed/no-alert when unchanged, but the local watcher must retain enough state/log detail for later ChatGPT review.
- Full-card records must preserve diagnostic reason codes, unavailable fields, evidence references, duplicate-suppression key fields, best-candidate ranking inputs, blocker/caution details, trigger context, invalidation context, and source-as-of metadata.
- Suppression must never downgrade the full-card field requirements.

## Shadow-Log Requirements

For emitted alerts, future shadow-log records should include:

- `event_type` such as `alert_decision`
- `alert_decision` such as `emit_phone_alert` or `emit_full_card_only`
- `suppression_fingerprint`
- `duplicate_suppression_key_fields`
- `material_change_flags`
- `state_snapshot`
- `trigger_card_snapshot`
- `evidence_refs`
- `unavailable_fields`
- `review_label`, initially `UNREVIEWED`

For suppressed duplicates, future shadow-log records should include:

- `event_type: suppressed_duplicate`
- `alert_decision: suppress_duplicate`
- `suppression_fingerprint`
- `duplicate_suppression_key_fields`
- `repeat_count`
- `last_alerted_at`
- `last_suppressed_at`
- `last_suppression_reason`
- `material_change_flags`
- `state_snapshot`
- `trigger_card_snapshot` or projection-incomplete marker
- `evidence_refs`
- `unavailable_fields`
- `review_label`, initially `UNREVIEWED`

Suppression records must be append-only review artifacts. They must prove what was suppressed, why it was suppressed, and which fields would have broken suppression if they had changed.

## Manual Review Labels And Auditability

Manual review labels from the shadow-log contract remain valid for duplicate suppression review, including:

- `UNREVIEWED`
- `correct_and_useful`
- `correct_but_early_noisy`
- `correct_but_late`
- `duplicate_noisy`
- `stale_spent_error`
- `wrong_stage`
- `wrong_trigger_status`
- `wrong_freshness_state`
- `evidence_unconfirmed`
- `unavailable_field_handling_error`
- `news_unconfirmed_expected`
- `review_inconclusive`

Auditability expectations:

- Every emitted alert and suppressed duplicate must be explainable from normalized fields.
- Every suppression decision must show the fingerprint and key inputs used.
- Every material-change break must show the changed field or reason code.
- Repeat counts must be preserved.
- Review labels must not become live trade approvals, option P&L claims, account-sizing decisions, production readiness claims, or live trade readiness claims.

## Explicit No-Go Boundaries

- No watcher implementation.
- No watcher runtime code.
- No runtime schema files.
- No generated replay reports.
- No generated chart outcome reports.
- No `main.py` / engine changes.
- No Railway.
- No production.
- No deploy files.
- No live backend.
- No auto-trading.
- No broker/order execution.
- No option P&L.
- No account sizing.
- No live data fetches.
- No live trade decisions.
- No invented headlines/news.
- No invented trigger levels, outcomes, trades, P&L, or live facts.
- No production readiness or live trade readiness claims.

## Future Implementation Test Requirements

This review does not create tests. Future implementation requires explicit authorization and replay/regression coverage before runtime work.

Future tests should cover:

- deterministic suppression key construction
- deterministic suppression fingerprint equality for same-state repeats
- fingerprint break on stage change
- fingerprint break on trigger_status change
- fingerprint break on freshness/stale/spent transition
- fingerprint break on primary blocker change
- fingerprint break on blocker/caution severity change
- fingerprint break on trigger-zone material movement
- fingerprint break on invalidation material movement
- fingerprint break on evidence quality change
- fingerprint break when critical fields become available
- fingerprint break when critical fields become unavailable
- fingerprint break on session-boundary interpretation change
- fingerprint break on new best current candidate
- fingerprint break on trigger path change
- source-confirmed `headline_news_status` changes
- `NEWS_UNCONFIRMED` repeat handling
- stale/spent no-fresh-trigger repeat suppression
- fresh current-session trigger breaking prior stale/spent suppression
- phone alert emission versus laptop/full-card logging
- shadow-log records for emitted alerts
- shadow-log records for suppressed duplicates
- manual review label preservation

SAFE-FAST engine changes remain out of scope and require replay/regression cases first.

## Review Decision

Duplicate suppression design review status: PASS.

Reason: the accepted suppression key inputs, normalized watcher-state and trigger-card dependencies, suppression fingerprint rules, material-change break rules, non-material repeat rules, stale/spent no-fresh-trigger discipline, unavailable-field and `NEWS_UNCONFIRMED` handling, phone/full-card behavior, shadow-log requirements, manual review/audit expectations, no-go boundaries, and future test requirements are documented without implementing watcher code or making live/production/options/account-sizing claims.

Continuous Watcher implementation remains deferred. The next bounded watcher-foundation design step is best-current-candidate / focus ranking design review only, before diagnostics, headline/news source policy, or any watcher implementation.
