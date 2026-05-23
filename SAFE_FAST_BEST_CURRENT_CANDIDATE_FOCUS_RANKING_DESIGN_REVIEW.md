# SAFE-FAST Best Current Candidate / Focus Ranking Design Review

## Review Status

- Review status: PASS
- Scope: documentation and focus-ranking design only
- Repo: `nickmancini1/safe-fast-backendnew`
- Branch: `main`
- Baseline: `patch8`
- Work mode: build work only, no live trade decisions
- Continuous Watcher implementation started: no
- Watcher runtime code created: no
- Runtime schema files created: no
- Production/live readiness claimed: no

This review defines the future SAFE-FAST best-current-candidate / focus ranking design for attention and review prioritization only. It does not implement watcher code, create runtime schema files, change `main.py`, change engine logic, touch Railway/deploy/production files, fetch live data, create generated replay reports, create generated chart outcome reports, model option P&L, add account sizing, or make live trade decisions.

Continuous Watcher implementation remains deferred.

## Source Documents Reviewed

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_STRICT_MASTER_HANDOFF_POST_SHADOW_LOG_REVIEW.md`
- `SAFE_FAST_TRIGGER_CARD_CONTRACT_SCHEMA_REVIEW.md`
- `SAFE_FAST_WATCHER_STATE_SCHEMA_DESIGN_REVIEW.md`
- `SAFE_FAST_SHADOW_LOG_SCHEMA_REVIEW.md`
- `SAFE_FAST_DUPLICATE_SUPPRESSION_DESIGN_REVIEW.md`

## Design Purpose

Best-current-candidate ranking should select the single strongest current candidate for attention/focus among available watcher candidates, plus secondary buckets for review context.

The output is an attention-management and review artifact. It is not trade approval, broker/order execution, account sizing, option P&L, production readiness, live trade readiness, or a live trade decision.

Focus ranking must answer: "Which candidate deserves attention now?" It must not answer: "Which trade should be taken?"

## Accepted Ranking Inputs

Future focus ranking must use the accepted ranking inputs from the trigger-card and watcher-state reviews:

- eligibility/stage validity
- freshness
- setup family priority only if explicitly defined
- trigger proximity when available
- blocker severity
- caution/context risk
- stale/spent demotion
- evidence quality
- unavailable-field count
- deterministic tie-breaker

These inputs must be normalized fields, reason codes, buckets, and explicit unavailable markers. Ranking must not depend on mutable prose alone.

## Dominant No-Trade Discipline

No-trade discipline is dominant over trigger proximity.

Blocked, stale, spent, unconfirmed, or evidence-poor candidates must not outrank cleaner current candidates solely because they are closer to a trigger level.

Ranking rules must preserve these constraints:

- A candidate with an accepted blocker remains watch-only unless the blocker is resolved by accepted evidence.
- A stale/spent candidate remains demoted unless accepted fresh current-session evidence creates a new valid trigger path.
- An unconfirmed candidate remains below confirmed candidates with cleaner evidence and fewer unavailable critical fields.
- Trigger proximity may improve rank only after eligibility/stage validity, freshness, blocker severity, caution/context risk, and evidence quality have been considered.
- Missing trigger, invalidation, freshness, source-as-of, or evidence fields must lower confidence and preserve no-trade wording.
- `triggered_signal_stage` remains shadow signal review only and must not imply live trade approval.

## Eligible Focus Buckets

Future focus output should assign candidates to one of these review buckets:

| Focus bucket | Meaning |
| --- | --- |
| `primary_focus` | Best current candidate for attention. Must be the cleanest current candidate after no-trade discipline, freshness, evidence quality, and unavailable-field handling. |
| `secondary_watch` | Current candidate worth watching after the primary focus, but not the top attention item. |
| `watch_only_blocked` | Candidate has a blocker, severe caution, or critical missing field that prevents stronger focus. |
| `stale_spent_context` | Candidate is stale, spent, prior-session, or has no fresh trigger, and is retained only as context. |
| `unavailable_unconfirmed` | Candidate lacks enough accepted identity, source, trigger, freshness, or evidence fields to compete with cleaner candidates. |

Only `primary_focus` and `secondary_watch` are attention buckets. None of the buckets are trade-approval buckets.

## Ranking Order

The future deterministic rank should be evaluated in this order:

1. Exclude or demote invalid lifecycle states into `watch_only_blocked`, `stale_spent_context`, or `unavailable_unconfirmed`.
2. Prefer confirmed eligible/current stages over blocked, stale/spent, unavailable, or unconfirmed stages.
3. Prefer fresh current candidates over stale, spent, prior-session, or freshness-unconfirmed candidates.
4. Prefer lower blocker severity and lower caution/context risk.
5. Prefer stronger evidence quality and fewer critical unavailable fields.
6. Apply setup family priority only if a later accepted design explicitly defines that priority for the specific comparison.
7. Apply trigger proximity only when trigger distance is available and after no-trade discipline has been satisfied.
8. Apply a deterministic tie-breaker from stable identity and evidence fields.

This order is a design contract, not runtime code.

## Setup Family Comparison

`Ideal`, `Clean Fast Break`, and `Continuation` must be compared without hardcoding unsafe trade priority.

Comparison rules:

- No setup family automatically outranks another setup family solely by name.
- Setup family priority may be used only if explicitly defined by a later accepted review or implementation task.
- A cleaner current `Continuation` can outrank a blocked or stale `Ideal`.
- A cleaner current `Ideal` can outrank a closer but evidence-poor `Clean Fast Break`.
- A cleaner current `Clean Fast Break` can outrank a stale/spent `Continuation`.
- If setup family priority is unavailable or not explicitly defined, compare by lifecycle validity, freshness, blocker/caution severity, evidence quality, unavailable-field count, then proximity and deterministic tie-breaker.

The ranking result must explain why the selected focus candidate won without implying that its setup family is a live-trade priority.

## Duplicate Suppression Interaction

Duplicate suppression must include best-current-candidate identity or deterministic focus bucket when available, as documented in the duplicate suppression design review.

Focus ranking interacts with suppression as follows:

- A repeated same-state `primary_focus` candidate may be suppressible when all accepted suppression key fields, material-change flags, focus identity, focus bucket, evidence quality, unavailable-field set, and no-trade wording are unchanged.
- A suppressed repeat must still preserve shadow-log audit detail for later review.
- Suppression must not hide a new best current candidate.
- Suppression must not hide a candidate moving into or out of `primary_focus`.
- Suppression must not hide a demotion caused by blocker severity, stale/spent status, evidence downgrade, or a critical field becoming unavailable.

## Material Focus Changes That Break Suppression

These focus changes must break duplicate suppression:

- `primary_focus` candidate identity changed
- candidate moved into `primary_focus`
- candidate moved out of `primary_focus`
- focus bucket changed
- focus-rank reason changed materially
- blocker severity changed for a focus candidate
- caution/context risk changed materially for a focus candidate
- freshness changed, especially fresh to stale/spent or stale/spent to rebuilding/current
- evidence quality changed
- critical field became available
- critical field became unavailable
- trigger proximity bucket changed materially after no-trade discipline is satisfied
- deterministic tie-breaker changed because stable identity/evidence fields changed
- source-confirmed `headline_news_status` changed

Each material focus change should produce a new alert decision path and a future shadow-log record explaining which focus input changed.

## Unavailable Fields And NEWS_UNCONFIRMED

Unavailable fields must remain explicit and must lower review confidence.

Required markers include:

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
- A high unavailable-field count should demote the candidate.
- Missing critical fields should push the candidate toward `unavailable_unconfirmed` or `watch_only_blocked`.
- A critical field becoming available is a material focus change.
- A critical field becoming unavailable is a material focus change.
- Unavailable proximity must not be treated as close proximity.

Headline/news rules:

- Default to `NEWS_UNCONFIRMED`.
- `NEWS_UNCONFIRMED` does not create a news blocker or news caution by itself.
- A source-confirmed `NEWS_CAUTION` or `NEWS_BLOCK` can affect caution/context risk or blocker severity.
- `NEWS_UNCONFIRMED` repeats are non-material unless replaced by a source-confirmed status.
- Do not invent headlines, macro events, earnings, filings, signals, trigger levels, outcomes, trades, P&L, or live facts.

## Phone Alert Vs Laptop / Full-Card Behavior

Phone behavior:

- Phone alerts may highlight the `primary_focus` candidate when a material focus change occurs.
- Phone alerts must be short and must preserve symbol, setup family, focus bucket, stage, trigger zone/level or unconfirmed marker, next condition, freshness state, blocker/caution summary, `headline_news_status`, and no-trade warning when applicable.
- Phone alerts must not present focus as trade approval.
- Phone alerts may suppress repeated same-focus states when duplicate suppression rules allow it.

Laptop/full-card behavior:

- The laptop/full-card output must retain complete ranking inputs for every candidate considered.
- Full-card records must show why the primary focus was selected and why other candidates were demoted.
- Full-card records must preserve unavailable fields, evidence references, duplicate-suppression fields, diagnostic reason codes, no-trade reasons, and normalized focus reason codes.
- Full-card output remains the authoritative local review artifact for later ChatGPT review.

## Shadow-Log Requirements

Future `best_candidate_snapshot` records should include:

- `event_type: best_candidate_snapshot`
- `watch_session_id`
- selected `primary_focus` `candidate_id`
- prior `primary_focus` `candidate_id` when available
- all candidate focus buckets
- normalized ranking inputs for each candidate
- `focus_rank_reason`
- `focus_change_reason_codes`
- `material_change_flags`
- `duplicate_suppression_key_fields`
- `suppression_fingerprint`
- `state_snapshot` for the selected candidate
- `trigger_card_snapshot` or projection-incomplete marker
- `evidence_refs`
- `unavailable_fields`
- `headline_news_status`
- `review_label`, initially `UNREVIEWED`

The record must make the focus decision auditable without relying on mutable prose. It must not become a trade ledger, execution record, option P&L report, account-sizing report, production readiness proof, live trade readiness proof, or live trade decision.

## Manual Review Labels And Auditability

Manual review labels from the shadow-log contract remain valid for focus ranking review, including:

- `UNREVIEWED`
- `correct_and_useful`
- `correct_but_early_noisy`
- `correct_but_late`
- `wrong_setup_type`
- `wrong_stage`
- `wrong_trigger_status`
- `wrong_freshness_state`
- `stale_spent_error`
- `missed_setup`
- `evidence_unconfirmed`
- `unavailable_field_handling_error`
- `news_unconfirmed_expected`
- `review_inconclusive`

Additional focus-review labels may include:

- `primary_focus_correct`
- `primary_focus_too_aggressive`
- `primary_focus_too_conservative`
- `secondary_watch_should_have_been_primary`
- `blocked_candidate_ranked_too_high`
- `stale_spent_ranked_too_high`
- `unconfirmed_ranked_too_high`
- `proximity_overweighted`

Auditability expectations:

- Every focus decision must be explainable from normalized fields.
- Every demotion must show the rank input or reason code that caused it.
- Every material focus change must be visible in future shadow logs.
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

- deterministic focus bucket assignment
- blocked candidate cannot outrank cleaner current candidate solely by proximity
- stale candidate cannot outrank cleaner current candidate solely by proximity
- spent candidate cannot outrank cleaner current candidate solely by proximity
- unconfirmed candidate cannot outrank cleaner current candidate solely by proximity
- evidence-poor candidate cannot outrank cleaner current candidate solely by proximity
- unavailable proximity does not count as close proximity
- `Ideal`, `Clean Fast Break`, and `Continuation` comparison without hardcoded unsafe trade priority
- setup family priority ignored unless explicitly defined
- blocker severity demotion
- caution/context risk demotion
- evidence quality promotion/demotion
- unavailable-field count demotion
- critical field became available as material focus change
- critical field became unavailable as material focus change
- `NEWS_UNCONFIRMED` default handling
- source-confirmed news status affecting focus only through caution/blocker rules
- deterministic tie-breaker stability
- new primary focus breaking duplicate suppression
- focus bucket change breaking duplicate suppression
- repeated same-focus state suppressible when no material field changed
- phone alert emission for material focus change
- laptop/full-card preservation of all ranking inputs
- shadow-log `best_candidate_snapshot` records
- manual review label preservation

SAFE-FAST engine changes remain out of scope and require replay/regression cases first.

## Review Decision

Best-current-candidate / focus ranking design review status: PASS.

Reason: the purpose, attention-only boundary, accepted ranking inputs, no-trade-dominant ranking order, eligible focus buckets, setup-family comparison rules, duplicate suppression interaction, material focus-change break rules, unavailable-field and `NEWS_UNCONFIRMED` handling, phone/full-card behavior, shadow-log requirements, manual review/audit expectations, no-go boundaries, and future test requirements are documented without implementing watcher code or making live/production/options/account-sizing claims.

Continuous Watcher implementation remains deferred. The next bounded watcher-foundation design step is diagnostics explanation design review only, before headline/news source policy or any watcher implementation.
