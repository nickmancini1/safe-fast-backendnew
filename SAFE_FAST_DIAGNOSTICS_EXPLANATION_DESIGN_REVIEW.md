# SAFE-FAST Diagnostics Explanation Design Review

## Review Status

- Review status: PASS
- Scope: documentation and diagnostics explanation design only
- Repo: `nickmancini1/safe-fast-backendnew`
- Branch: `main`
- Baseline: `patch8`
- Work mode: build work only, no live trade decisions
- Continuous Watcher implementation started: no
- Watcher runtime code created: no
- Runtime schema files created: no
- Production/live readiness claimed: no

This review defines the future SAFE-FAST diagnostics explanation design for trigger cards, watcher state, shadow logs, duplicate suppression, and focus ranking. It does not implement watcher code, create runtime schema files, change `main.py`, change engine logic, touch Railway/deploy/production files, fetch live data, create generated replay reports, create generated chart outcome reports, model option P&L, add account sizing, or make live trade decisions.

Continuous Watcher implementation remains deferred.

## Source Documents Reviewed

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_STRICT_MASTER_HANDOFF_POST_SHADOW_LOG_REVIEW.md`
- `SAFE_FAST_TRIGGER_CARD_CONTRACT_SCHEMA_REVIEW.md`
- `SAFE_FAST_WATCHER_STATE_SCHEMA_DESIGN_REVIEW.md`
- `SAFE_FAST_SHADOW_LOG_SCHEMA_REVIEW.md`
- `SAFE_FAST_DUPLICATE_SUPPRESSION_DESIGN_REVIEW.md`
- `SAFE_FAST_BEST_CURRENT_CANDIDATE_FOCUS_RANKING_DESIGN_REVIEW.md`

## Design Purpose

Diagnostics explain why a future SAFE-FAST watcher card or state record says what it says.

The diagnostics layer should explain:

- setup identity
- lifecycle stage
- trigger status
- blocker or caution status
- freshness, stale, and spent state
- unavailable fields
- evidence quality
- focus ranking
- duplicate suppression
- headline/news status
- no-trade boundary
- next check or next alert condition

Diagnostics are explanation-only. They must not override setup recognition, lifecycle stage logic, trigger logic, blockers, stale/spent discipline, focus ranking, duplicate suppression, no-trade boundaries, or any future SAFE-FAST engine decision. Diagnostics must make a card easier to audit; they must not create a trade, promote a card to live readiness, erase missing evidence, or soften no-trade wording.

## Required Diagnostic Inputs

Diagnostics must be derived from normalized fields accepted by the prior watcher-foundation contracts.

From the trigger-card contract:

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
- `no_trade_reason`
- `duplicate_suppression_key_fields`
- `best_candidate_ranking_inputs`

From the watcher-state contract:

- `candidate_id`
- `watch_session_id`
- `regular_session_date`
- `state_version`
- `previous_stage`
- `previous_trigger_status`
- `previous_fresh_stale_spent_state`
- `trigger_zone_bucket`
- `invalidation_bucket`
- `source_kind`
- `evidence_quality`
- `primary_blocker`
- `watch_only`
- `state_changed`
- `state_change_reason_codes`
- `material_change_flags`
- `trigger_card_projection_status`
- `phone_alert_summary_status`
- `full_card_required_fields_status`

From the shadow-log contract:

- `log_record_id`
- `event_type`
- `event_at`
- `state_snapshot`
- `previous_state_snapshot`
- `trigger_card_snapshot`
- `alert_decision`
- `evidence_refs`
- `review_label`
- `review_notes`

From the duplicate-suppression contract:

- accepted suppression key inputs
- `suppression_fingerprint`
- `repeat_count`
- `last_alerted_at`
- `last_suppressed_at`
- `last_suppression_reason`
- material-change break reasons

From the focus-ranking contract:

- `best_candidate_ranking_inputs`
- `focus_rank_bucket`
- `focus_rank_reason`
- selected `primary_focus` candidate identity when available
- prior `primary_focus` candidate identity when available
- `focus_change_reason_codes`

If an input is unavailable, diagnostics must consume the explicit unavailable marker. They must not infer missing values from price movement, future candles, live assumptions, mutable prose, or desired wording.

## Required Diagnostic Outputs

Future diagnostics should expose these output fields in watcher state, trigger-card full output, and relevant shadow-log records:

| Field | Requirement |
| --- | --- |
| `diagnostic_reason_codes` | Ordered normalized reason codes explaining the card/state. |
| `diagnostic_explanation` | Plain-English explanation derived from the normalized reason codes and evidence. |
| `diagnostic_scope` | Scope marker showing what the explanation covers, such as setup, lifecycle, trigger, blocker, freshness, focus, suppression, or next condition. |
| `evidence_refs` | Deterministic evidence references or explicit unconfirmed marker. |
| `unavailable_fields` | Full missing-field list preserved from source state/card/log contracts. |
| `no_trade_reason` | Required when blocked, stale/spent, unconfirmed, evidence-poor, incomplete, or otherwise not actionable. |
| `next_check_or_next_alert_condition` | Specific future condition that would justify checking again or alerting again. |
| `focus_rank_reason` | Explanation for selected focus bucket or demotion. |
| `suppression_reason` | Explanation for emitted, suppressed, repeated, or no-alert duplicate-suppression outcome. |

The explanation fields must be reproducible from normalized inputs. Mutable prose can summarize the result, but normalized reason codes and evidence references are the audit source.

## Allowed Diagnostic Reason-Code Groups

Diagnostic reason codes should be grouped by purpose. A future implementation may add specific codes inside these groups, but must preserve these group names and boundaries.

### `setup_identity`

Explains setup family and direction, including confirmed `Ideal`, `Clean Fast Break`, `Continuation`, or `UNCONFIRMED` identity.

Allowed examples:

- `setup_identity.confirmed_ideal`
- `setup_identity.confirmed_clean_fast_break`
- `setup_identity.confirmed_continuation`
- `setup_identity.unconfirmed`
- `setup_identity.direction_unconfirmed`

### `lifecycle_stage`

Explains why the candidate is forming, near trigger, pending candle approval, triggered for shadow review, blocked, stale/spent, rebuilding, or unavailable.

Allowed examples:

- `lifecycle_stage.forming_developing`
- `lifecycle_stage.near_trigger`
- `lifecycle_stage.pending_completed_candle_approval`
- `lifecycle_stage.triggered_signal_stage_shadow_only`
- `lifecycle_stage.blocked_no_trade`
- `lifecycle_stage.stale_spent_no_fresh_trigger`
- `lifecycle_stage.rebuilding`
- `lifecycle_stage.unavailable_unconfirmed`

### `trigger_status`

Explains the current trigger path state.

Allowed examples:

- `trigger_status.no_valid_trigger`
- `trigger_status.waiting_for_trigger`
- `trigger_status.near_trigger`
- `trigger_status.pending_completed_candle`
- `trigger_status.triggered_shadow_only`
- `trigger_status.failed_hold`
- `trigger_status.stale`
- `trigger_status.spent`
- `trigger_status.unconfirmed`

### `blocker`

Explains accepted blockers or the absence of blockers.

Allowed examples:

- `blocker.none_confirmed`
- `blocker.primary_blocker_active`
- `blocker.trigger_missing`
- `blocker.invalidation_missing`
- `blocker.freshness_missing`
- `blocker.evidence_missing`
- `blocker.source_missing`
- `blocker.news_source_confirmed_block`

### `caution`

Explains accepted cautions or the absence of cautions.

Allowed examples:

- `caution.none_confirmed`
- `caution.context_risk`
- `caution.evidence_partial`
- `caution.unavailable_noncritical_field`
- `caution.news_source_confirmed_caution`

### `freshness`

Explains current freshness.

Allowed examples:

- `freshness.fresh_current_session`
- `freshness.prior_session`
- `freshness.rebuilding`
- `freshness.unconfirmed`

### `stale_spent`

Explains stale, spent, or no-fresh-trigger state.

Allowed examples:

- `stale_spent.stale_no_fresh_trigger`
- `stale_spent.spent_no_fresh_trigger`
- `stale_spent.prior_session_no_fresh_trigger`
- `stale_spent.rebuilding_required`

### `unavailable_field`

Explains missing or unconfirmed fields.

Allowed examples:

- `unavailable_field.trigger_level_unconfirmed`
- `unavailable_field.distance_to_trigger_unconfirmed`
- `unavailable_field.invalidation_unconfirmed`
- `unavailable_field.source_as_of_unconfirmed`
- `unavailable_field.evidence_rows_unconfirmed`
- `unavailable_field.session_date_unconfirmed`
- `unavailable_field.freshness_unconfirmed`
- `unavailable_field.news_unconfirmed`

### `evidence_quality`

Explains evidence strength.

Allowed examples:

- `evidence_quality.deterministic`
- `evidence_quality.partial`
- `evidence_quality.unconfirmed`
- `evidence_quality.missing`

### `focus_ranking`

Explains focus selection or demotion.

Allowed examples:

- `focus_ranking.primary_focus_selected`
- `focus_ranking.secondary_watch`
- `focus_ranking.watch_only_blocked`
- `focus_ranking.stale_spent_context`
- `focus_ranking.unavailable_unconfirmed`
- `focus_ranking.demoted_by_blocker`
- `focus_ranking.demoted_by_stale_spent`
- `focus_ranking.demoted_by_evidence`
- `focus_ranking.demoted_by_unavailable_fields`
- `focus_ranking.proximity_not_enough`

### `duplicate_suppression`

Explains alert emission, suppression, or material-change break.

Allowed examples:

- `duplicate_suppression.emit_material_change`
- `duplicate_suppression.emit_new_primary_focus`
- `duplicate_suppression.suppress_same_state_repeat`
- `duplicate_suppression.no_alert_no_material_change`
- `duplicate_suppression.break_stage_changed`
- `duplicate_suppression.break_trigger_status_changed`
- `duplicate_suppression.break_freshness_changed`
- `duplicate_suppression.break_blocker_changed`
- `duplicate_suppression.break_evidence_quality_changed`
- `duplicate_suppression.break_unavailable_field_changed`
- `duplicate_suppression.break_focus_changed`

### `headline_news_status`

Explains the headline/news context without inventing news.

Allowed examples:

- `headline_news_status.news_unconfirmed`
- `headline_news_status.news_clear_source_confirmed`
- `headline_news_status.news_caution_source_confirmed`
- `headline_news_status.news_block_source_confirmed`

### `no_trade_boundary`

Explains why the output is watch-only or no-trade.

Allowed examples:

- `no_trade_boundary.watch_only`
- `no_trade_boundary.blocker_active`
- `no_trade_boundary.stale_spent`
- `no_trade_boundary.unavailable_critical_field`
- `no_trade_boundary.evidence_unconfirmed`
- `no_trade_boundary.triggered_shadow_only`
- `no_trade_boundary.no_live_trade_approval`

### `next_condition`

Explains what must happen next.

Allowed examples:

- `next_condition.wait_for_defined_trigger`
- `next_condition.wait_for_completed_candle_rule`
- `next_condition.resolve_blocker`
- `next_condition.resolve_unavailable_field`
- `next_condition.wait_for_rebuilt_structure`
- `next_condition.new_material_change_required`
- `next_condition.no_repeat_alert_until_change`

## Plain-English Explanation Rules

Diagnostic explanations must be short, direct, and tied to evidence.

Rules:

- Explain what the candidate is, where it is in the lifecycle, why it is or is not actionable in shadow review, and what condition comes next.
- Use the accepted setup, stage, trigger-status, freshness, blocker, caution, focus, and suppression terms.
- Keep no-trade wording explicit when required.
- Say `triggered_signal_stage` is shadow signal review only, not live trade approval.
- Say stale/spent candidates have no fresh trigger.
- Say missing fields are unconfirmed, not absent-by-proof unless evidence supports that.
- Do not say "wait for confirmation" without naming the trigger path or completed-candle rule when available.
- Do not make trigger levels, invalidation levels, news, outcomes, trades, P&L, or live facts sound known when they are unavailable.
- Do not let focus ranking or phone urgency imply actionability.
- Do not use diagnostics to relabel setup identity or lifecycle stage.

## Unavailable-Field And NEWS_UNCONFIRMED Handling

Unavailable fields must remain explicit in diagnostic reason codes, explanations, trigger cards, watcher state, and shadow logs.

Required unavailable markers include:

- `TRIGGER_LEVEL_UNCONFIRMED`
- `DISTANCE_TO_TRIGGER_UNCONFIRMED`
- `INVALIDATION_UNCONFIRMED`
- `SOURCE_AS_OF_UNCONFIRMED`
- `EVIDENCE_ROWS_UNCONFIRMED`
- `SESSION_DATE_UNCONFIRMED`
- `FRESHNESS_UNCONFIRMED`
- `NEWS_UNCONFIRMED`

Rules:

- Missing trigger, invalidation, freshness, source, evidence, session, or news fields must not be invented.
- Critical unavailable fields should produce `no_trade_reason` and `no_trade_boundary` diagnostics.
- Unavailable proximity must not be treated as close proximity.
- `NEWS_UNCONFIRMED` is the default until a later explicit news-source policy/source review reads a valid source.
- `NEWS_UNCONFIRMED` by itself must not create a news blocker or news caution.
- Source-confirmed `NEWS_CAUTION` or `NEWS_BLOCK` may be explained only when the valid source and policy are available.
- Do not invent headlines, macro events, earnings, filings, signals, trigger levels, outcomes, trades, P&L, or live facts.

## Phone Alert Vs Laptop / Full-Card Behavior

Phone behavior:

- Phone alerts may include a short diagnostic explanation.
- Phone diagnostics must preserve symbol, setup family, stage, trigger zone/level or unconfirmed marker, next condition, freshness, blocker/caution summary, `headline_news_status`, and no-trade warning when applicable.
- Phone diagnostics must not include long audit detail.
- Phone diagnostics must not imply trade approval.
- Repeated same-state phone diagnostics may be suppressed only under the duplicate-suppression rules.

Laptop/full-card behavior:

- Laptop/full-card diagnostics must include full `diagnostic_reason_codes`, `diagnostic_explanation`, `diagnostic_scope`, `evidence_refs`, `unavailable_fields`, `no_trade_reason`, `next_check_or_next_alert_condition`, `focus_rank_reason`, and `suppression_reason`.
- Full-card diagnostics must preserve enough detail for later ChatGPT review.
- Full-card diagnostics must explain primary focus selection and demotion when focus ranking is present.
- Full-card diagnostics must explain emitted versus suppressed alert decisions when duplicate suppression is present.
- Full-card diagnostics remain local review artifacts, not live trade decisions.

## Shadow-Log Requirements

Future shadow-log records should preserve diagnostic fields for:

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

Required diagnostic-related fields in relevant records:

- `diagnostic_reason_codes`
- `diagnostic_explanation`
- `diagnostic_scope`
- `evidence_refs`
- `unavailable_fields`
- `no_trade_reason`
- `next_check_or_next_alert_condition`
- `focus_rank_reason`
- `suppression_reason`
- `material_change_flags`
- `review_label`, initially `UNREVIEWED`

Diagnostic shadow-log records must remain append-only review artifacts. They must prove why a card/state/alert/suppression/focus decision was explained the way it was, without relying on mutable prose alone.

## Manual Review Labels And Auditability

Manual review labels from prior contracts remain valid for diagnostic review, including:

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
- `primary_focus_correct`
- `primary_focus_too_aggressive`
- `primary_focus_too_conservative`
- `secondary_watch_should_have_been_primary`
- `blocked_candidate_ranked_too_high`
- `stale_spent_ranked_too_high`
- `unconfirmed_ranked_too_high`
- `proximity_overweighted`

Additional diagnostic-review labels may include:

- `diagnostic_correct`
- `diagnostic_too_vague`
- `diagnostic_missing_no_trade_reason`
- `diagnostic_missing_next_condition`
- `diagnostic_missing_evidence_ref`
- `diagnostic_overstated_actionability`
- `diagnostic_unavailable_field_error`
- `diagnostic_news_policy_error`
- `diagnostic_suppression_reason_error`
- `diagnostic_focus_reason_error`

Auditability expectations:

- Every diagnostic explanation must map back to normalized reason codes.
- Every reason code must map back to accepted inputs or explicit unavailable markers.
- Every no-trade diagnostic must preserve the `no_trade_reason`.
- Every unavailable-field diagnostic must preserve the unavailable field name.
- Every focus diagnostic must preserve the ranking input or demotion reason.
- Every suppression diagnostic must preserve the fingerprint/key or material-change break reason.
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

- diagnostic reason-code generation for setup identity
- diagnostic reason-code generation for lifecycle stage
- diagnostic reason-code generation for trigger status
- blocker and caution explanation
- freshness explanation
- stale/spent no-fresh-trigger explanation
- unavailable-field preservation
- `NEWS_UNCONFIRMED` default explanation
- source-confirmed news status explanation only after valid source policy exists
- evidence-quality explanation
- no-trade reason preservation
- next-condition explanation
- focus-rank reason preservation
- suppression reason preservation
- phone alert diagnostic summary completeness
- laptop/full-card diagnostic completeness
- shadow-log diagnostic field preservation
- manual review label preservation
- diagnostics cannot override setup identity
- diagnostics cannot override lifecycle stage
- diagnostics cannot override blockers or stale/spent status
- diagnostics cannot promote triggered shadow review to live trade approval
- diagnostics cannot fabricate trigger levels, invalidation, news, outcomes, trades, P&L, or live facts

SAFE-FAST engine changes remain out of scope and require replay/regression cases first.

## Review Decision

Diagnostics explanation design review status: PASS.

Reason: the purpose, explanation-only boundary, required inputs, required outputs, reason-code groups, plain-English explanation rules, unavailable-field and `NEWS_UNCONFIRMED` handling, phone/full-card behavior, shadow-log requirements, manual review/audit expectations, no-go boundaries, and future implementation test requirements are documented without implementing watcher code or making live/production/options/account-sizing claims.

Continuous Watcher implementation remains deferred. The next bounded watcher-foundation design step is headline/news source policy design review only, before any watcher implementation.
