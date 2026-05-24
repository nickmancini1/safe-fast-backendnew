# SAFE-FAST Headline / News Source Policy Design Review

## Review Status

- Review status: PASS
- Scope: documentation and headline/news source policy design only
- Repo: `nickmancini1/safe-fast-backendnew`
- Branch: `main`
- Baseline: `patch8`
- Work mode: build work only, no live trade decisions
- Continuous Watcher implementation started: no
- Watcher runtime code created: no
- Runtime schema files created: no
- Production/live readiness claimed: no

This review defines the future SAFE-FAST headline/news source policy for watcher cards, watcher state, shadow logs, diagnostics, duplicate suppression, and focus ranking. It does not implement watcher code, create runtime schema files, change `main.py`, change engine logic, touch Railway/deploy/production files, fetch live data, create generated replay reports, create generated chart outcome reports, model option P&L, add account sizing, or make live trade decisions.

Continuous Watcher implementation remains deferred.

## Source Documents Reviewed

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_STRICT_MASTER_HANDOFF_POST_SHADOW_LOG_REVIEW.md`
- `SAFE_FAST_TRIGGER_CARD_CONTRACT_SCHEMA_REVIEW.md`
- `SAFE_FAST_WATCHER_STATE_SCHEMA_DESIGN_REVIEW.md`
- `SAFE_FAST_SHADOW_LOG_SCHEMA_REVIEW.md`
- `SAFE_FAST_DUPLICATE_SUPPRESSION_DESIGN_REVIEW.md`
- `SAFE_FAST_BEST_CURRENT_CANDIDATE_FOCUS_RANKING_DESIGN_REVIEW.md`
- `SAFE_FAST_DIAGNOSTICS_EXPLANATION_DESIGN_REVIEW.md`
- `SAFE_FAST_NEWS_AND_HEADLINE_RISK_PLAN.md`

## Design Purpose

Headline/news handling is a future risk and context layer. It must use valid sources only, preserve SAFE-FAST no-trade discipline, and default to `NEWS_UNCONFIRMED` when source data is unavailable.

News is not a signal engine. SAFE-FAST remains setup first, stage second, structure/risk/news context third, and trade style last. Headline/news context must not create headline-chasing behavior.

## Allowed Headline / News Statuses

Future watcher outputs may use only these statuses:

- `NEWS_CLEAR`
- `NEWS_CAUTION`
- `NEWS_BLOCK`
- `NEWS_UNCONFIRMED`

Default status is `NEWS_UNCONFIRMED` unless valid source data is available and preserved with source-as-of and evidence metadata.

## Valid-Source Requirements

A headline/news status may be source-confirmed only when the future watcher has a valid, reviewable source for the claim.

Valid-source requirements:

- Source identity must be recorded.
- Source-as-of timestamp must be recorded.
- Evidence reference must be recorded.
- The source must be appropriate for the risk category being evaluated.
- The source must distinguish scheduled events, earnings/component events, filings, market-wide headlines, ETF-specific context, and unavailable data.
- The source must be recent enough for the assessed trade window or hold window.
- The source must be reviewable later from laptop/full-card output and future shadow logs.

Examples of source categories that may be valid in a later authorized implementation include scheduled macro calendars, earnings calendars, SEC filing sources, trusted market news/headline sources, exchange/broker outage status sources, and accepted internal source snapshots. This review does not approve any live fetch, vendor integration, runtime source adapter, or production data dependency.

## Invalid Or Unavailable Source Handling

Invalid, missing, stale, ambiguous, or non-reviewable source data must not be treated as clear news.

Rules:

- If source data is unavailable, set `headline_news_status` to `NEWS_UNCONFIRMED`.
- If source-as-of is unavailable, preserve `SOURCE_AS_OF_UNCONFIRMED`.
- If evidence references are unavailable, preserve `EVIDENCE_ROWS_UNCONFIRMED` or the accepted equivalent explicit marker.
- If the source cannot support the asserted event, filing, headline, or macro claim, treat the field as unconfirmed.
- If sources disagree, preserve caution/unconfirmed wording until a later explicit policy resolves source priority.
- `NEWS_UNCONFIRMED` by itself must not create a news blocker or news caution, but it may preserve watch-only/no-trade wording when the intended hold depends on news clarity.

SAFE-FAST must not invent news, macro events, earnings, filings, headlines, rumors, signals, outcomes, trigger levels, trades, P&L, or live facts.

## Caution Policy

Most news should be caution or context, not a hard blocker.

`NEWS_CAUTION` may apply when valid source data shows context risk that matters to the setup, trade window, hold window, gap risk, liquidity/execution safety, or event-driven invalidation risk but does not directly require a hard block.

Valid caution examples by category:

- Scheduled macro event later today, tomorrow morning, or during a possible hold window.
- Major macro event later this week when overnight or swing exposure is relevant.
- Fed speaker, Treasury auction, CPI/PPI/PCE/NFP, GDP, ISM/PMI, jobless claims, JOLTS, retail sales, or similar scheduled event with timing risk.
- Mega-cap earnings or large component event relevant to SPY or QQQ.
- Rates, credit, regional-bank, liquidity, or growth context relevant to IWM.
- Real-yield, dollar, Fed, inflation, geopolitical, or central-bank-gold context relevant to GLD.
- Market-wide headline risk that is unresolved but not immediate enough for a hard block.
- Elevated event-day uncertainty where the setup is still watchable but not clean enough for stronger wording.

`NEWS_CAUTION` must remain a risk/context label. It must not create a setup, approve a trade, or erase existing no-trade reasons.

## Hard-Block Policy

`NEWS_BLOCK` is allowed only for immediate and material risk that directly threatens the setup, trade window, intended hold window, overnight gap risk, liquidity/execution safety, or event-driven invalidation risk.

Possible valid hard-block categories:

- FOMC decision or press conference inside the intended trade window.
- CPI, NFP, or similarly material data release minutes before entry or inside the intended hold window.
- Emergency central bank action.
- Active exchange, broker, data-provider, or execution outage affecting the contemplated instrument or execution path.
- Severe unresolved geopolitical escalation during the intended hold window.
- Major component shock large enough to directly threaten SPY or QQQ during the trade window.
- Event-day IV/liquidity conditions combined with weak structure or fragile setup quality.

Hard blocks must be source-confirmed, specific, and auditable. A normal headline, distant event, generic risk, or vague rumor should not become `NEWS_BLOCK`.

## Setup And Stage Boundaries

Headline/news context must not:

- create a setup
- erase setup identity
- promote a bad setup
- override stage logic
- override stale/spent discipline
- override duplicate suppression
- override focus ranking
- create live trade approval
- convert `triggered_signal_stage` into live trade readiness
- replace trigger, invalidation, freshness, evidence, or source requirements

News can only add context, caution, block status, unavailable-field state, no-trade wording, and review/audit detail.

## Source-As-Of And Evidence Requirements

Every source-confirmed `NEWS_CLEAR`, `NEWS_CAUTION`, or `NEWS_BLOCK` must preserve:

- `headline_news_status`
- `news_source_kind`
- `news_source_name`
- `news_source_as_of`
- `news_evidence_refs`
- `news_event_time` when applicable
- `news_event_scope` such as macro, earnings, filing, market-wide headline, ETF-specific context, outage, or unconfirmed
- `news_reason_code`
- short plain-English `news_reason`
- `news_affects_window` when applicable
- unavailable-field markers for anything missing

If these fields cannot be produced, the future watcher must keep the news status unconfirmed or incomplete rather than filling values from assumptions.

## Unavailable-Field Handling

Required unavailable markers include:

- `NEWS_UNCONFIRMED`
- `SOURCE_AS_OF_UNCONFIRMED`
- `EVIDENCE_ROWS_UNCONFIRMED`
- `NEWS_SOURCE_UNCONFIRMED`
- `NEWS_EVENT_TIME_UNCONFIRMED`
- `NEWS_REASON_UNCONFIRMED`

Unavailable news fields must be visible in trigger cards, watcher state, diagnostics, and shadow logs. They must not be hidden by phone-alert brevity, duplicate suppression, focus ranking, or diagnostic prose.

## Phone Alert Vs Laptop / Full-Card Behavior

Phone behavior:

- Phone alerts must show the headline/news status.
- Phone alerts may summarize only the short news reason.
- Phone alerts must preserve no-trade warnings when `NEWS_BLOCK`, critical unavailable fields, stale/spent status, or blockers apply.
- Phone alerts must not imply trade approval because news is clear or only caution.
- Phone alerts may suppress repeated same-news same-state observations only when duplicate suppression rules allow it.

Laptop/full-card behavior:

- Full cards must show the complete news source, source-as-of, evidence references, unavailable fields, reason codes, and plain-English reason.
- Full cards must distinguish source-confirmed `NEWS_CLEAR`, `NEWS_CAUTION`, and `NEWS_BLOCK` from `NEWS_UNCONFIRMED`.
- Full cards must preserve enough detail for later ChatGPT review.
- The laptop/full-card output remains the authoritative local review artifact.

## Shadow-Log Requirements

Future shadow-log records that include headline/news fields should preserve:

- `headline_news_status`
- `news_source_kind`
- `news_source_name`
- `news_source_as_of`
- `news_evidence_refs`
- `news_event_time`
- `news_event_scope`
- `news_reason_code`
- `news_reason`
- `news_affects_window`
- `unavailable_fields`
- `material_change_flags`
- `diagnostic_reason_codes`
- `review_label`, initially `UNREVIEWED`

Source-confirmed status changes may be material for duplicate suppression and focus ranking. Repeated `NEWS_UNCONFIRMED` observations are non-material unless other accepted material fields change or a source-confirmed status replaces them.

## Interaction With Diagnostics, Suppression, And Focus Ranking

Diagnostics:

- Diagnostics may explain `NEWS_UNCONFIRMED`, source-confirmed clear/caution/block, missing source fields, and no-trade boundary.
- Diagnostics must not invent a headline/news reason or soften unavailable-field wording.

Duplicate suppression:

- Source-confirmed `headline_news_status` changes can break suppression.
- Repeated same-state `NEWS_UNCONFIRMED` may be suppressible.
- Suppression must not hide a new source-confirmed caution, hard block, source-quality downgrade, or source-unavailable transition.

Focus ranking:

- Source-confirmed `NEWS_CAUTION` may increase caution/context risk.
- Source-confirmed `NEWS_BLOCK` may push a candidate into `watch_only_blocked`.
- `NEWS_UNCONFIRMED` must lower confidence only through explicit unavailable-field and no-trade rules; it must not be treated as clear news.
- Focus ranking remains attention-only and must not create trade approval.

## Manual Review Labels And Auditability

Manual review labels from prior watcher-foundation contracts remain valid, including:

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
- `diagnostic_news_policy_error`

Additional headline/news review labels may include:

- `news_status_correct`
- `news_status_too_aggressive`
- `news_status_too_conservative`
- `news_source_invalid`
- `news_source_stale`
- `news_source_missing`
- `news_caution_expected`
- `news_block_expected`
- `news_block_too_aggressive`
- `news_clear_overstated`
- `news_unconfirmed_expected`

Auditability expectations:

- Every source-confirmed news status must map back to a valid source and evidence reference.
- Every unavailable source must preserve `NEWS_UNCONFIRMED`.
- Every news caution or block must have a normalized reason code.
- Every hard block must explain why risk is immediate and material.
- Manual labels must not become live trade approvals, option P&L claims, account-sizing decisions, production readiness claims, or live trade readiness claims.

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
- No broker/order execution.
- No auto-trading.
- No option P&L.
- No account sizing.
- No live data fetches.
- No live trade decisions.
- No invented headlines/news.
- No invented macro events.
- No invented earnings.
- No invented filings.
- No invented rumors.
- No invented signals.
- No invented outcomes.
- No invented trigger levels.
- No invented trades.
- No invented P&L.
- No invented live facts.
- No production readiness or live trade readiness claims.

## Future Implementation Test Requirements

This review does not create tests. Future implementation requires explicit authorization and replay/regression coverage before runtime work.

Future tests should cover:

- default unavailable source returns `NEWS_UNCONFIRMED`
- invalid source returns `NEWS_UNCONFIRMED`
- stale source returns unconfirmed or caution according to accepted policy
- valid source-confirmed clear context returns `NEWS_CLEAR`
- valid source-confirmed caution context returns `NEWS_CAUTION`
- valid source-confirmed immediate/material risk returns `NEWS_BLOCK`
- most normal news remains caution/context rather than hard block
- `NEWS_UNCONFIRMED` cannot be treated as clear news
- missing source-as-of is preserved
- missing evidence reference is preserved
- source-confirmed status changes break duplicate suppression
- repeated `NEWS_UNCONFIRMED` same-state handling
- phone alert summary preserves news status and no-trade wording
- laptop/full-card output preserves source, source-as-of, evidence, reason code, and unavailable fields
- shadow-log records preserve headline/news fields
- diagnostics explain news status without inventing facts
- focus ranking handles source-confirmed caution and block without creating trade approval
- news cannot create a setup
- news cannot erase setup identity
- news cannot promote a bad setup
- news cannot override stage logic
- news cannot override stale/spent discipline
- news cannot override duplicate suppression
- news cannot override focus ranking
- news cannot create live trade approval
- news cannot fabricate headlines, macro events, earnings, filings, trigger levels, outcomes, trades, P&L, or live facts

SAFE-FAST engine changes remain out of scope and require replay/regression cases first.

## Review Decision

Headline/news source policy design review status: PASS.

Reason: the allowed headline/news statuses, valid-source requirements, invalid/unavailable-source handling, caution and hard-block policy, no-invention rules, setup/stage/no-trade boundaries, source-as-of and evidence requirements, unavailable-field handling, phone/full-card behavior, shadow-log requirements, diagnostics/suppression/focus interactions, manual review/audit expectations, explicit no-go boundaries, and future implementation test requirements are documented without implementing watcher code or making live/production/options/account-sizing claims.

Continuous Watcher implementation remains deferred. The next bounded watcher-foundation step is strict watcher-foundation handoff / implementation readiness review only, before any watcher implementation.
