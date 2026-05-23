# SAFE-FAST Trigger-Card Contract / Schema Review

## Review Status

- Review status: PASS
- Scope: documentation and contract design only
- Repo: `safe-fast-backendnew`
- Branch: `main`
- Work mode: build work only, no live trade decisions
- Continuous Watcher implementation started: no
- Production/live readiness claimed: no

This review defines the future SAFE-FAST watcher trigger-card output contract. It does not implement watcher code, create JSON schema files, change `main.py`, change engine logic, touch Railway/deploy/production files, fetch live data, create generated replay reports, create generated chart outcome reports, model option P&L, add account sizing, or make live trade decisions.

## Source Documents Reviewed

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_POST_GLD_WATCHER_TRANSITION_HARDENING_PLAN.md`
- `SAFE_FAST_CONTINUOUS_WATCHER_FOUNDATION_SHADOW_ARCHITECTURE_PLAN.md`
- `SAFE_FAST_ALL_SYMBOL_CURRENT_DEPTH_CLOSEOUT_REVIEW.md`
- `SAFE_FAST_DAY60_PRODUCT_BUSINESS_HANDOFF_ADDENDUM.md`
- `SAFE_FAST_NEWS_AND_HEADLINE_RISK_PLAN.md`

## Contract Purpose

The trigger card is the stable output surface for future SAFE-FAST watcher observations. It must show what setup exists, where it is in the lifecycle, what trigger path is being watched, what is missing or blocked, what needs to happen next, and what evidence supports the card.

The card is an attention and review artifact. It is not trade approval, broker/order execution, account sizing, option P&L, production readiness, live trade readiness, or a live trade decision.

## Required Trigger-Card Fields

Every full trigger card must include these fields:

| Field | Requirement |
| --- | --- |
| `symbol` | One of the supported watcher symbols when known; otherwise explicit unconfirmed handling. |
| `setup_type` | SAFE-FAST setup family or `UNCONFIRMED`. |
| `direction` | Directional setup side or `UNCONFIRMED`. |
| `stage` | Lifecycle stage. |
| `trigger_status` | Current trigger state. |
| `trigger_level_or_zone` | Numeric level, zone, condition, or unconfirmed marker. |
| `confirmation_timeframe_rule` | Actual candle/timeframe confirmation rule or unconfirmed marker. |
| `distance_to_trigger` | Numeric distance, bucket, or unconfirmed marker. Do not infer when trigger is missing. |
| `invalidation_level_or_condition` | Numeric invalidation, condition, or unconfirmed marker. |
| `fresh_stale_spent_state` | Freshness state. |
| `next_check_or_next_alert_condition` | Specific next condition that would justify a check or new alert. |
| `blockers` | List of blocker objects or an explicit none/unconfirmed state. |
| `cautions` | List of caution objects or an explicit none/unconfirmed state. |
| `unavailable_fields` | Missing fields that must not be invented. |
| `source_as_of` | Source timestamp/as-of metadata or unconfirmed marker. |
| `evidence_rows` | Deterministic evidence references or unconfirmed marker. |
| `headline_news_status` | News/headline context status. |
| `diagnostic_reason_codes` | Explanation-only reason codes. |
| `no_trade_reason` | Required when blocked, stale/spent, unconfirmed, or otherwise not actionable. |
| `duplicate_suppression_key_fields` | Inputs needed to create the suppression key. |
| `best_candidate_ranking_inputs` | Inputs needed for focus ranking. |

## Allowed Values

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

### Blocker And Caution Severity

- `none`
- `caution`
- `block`
- `unconfirmed`

Blocker and caution entries should include at least severity, reason code, plain-English reason, evidence reference when available, and whether the item affects actionability.

### `headline_news_status`

- `NEWS_CLEAR`
- `NEWS_CAUTION`
- `NEWS_BLOCK`
- `NEWS_UNCONFIRMED`

### Unavailable Field Pattern

Unavailable values must use `*_UNCONFIRMED` or blank only where the consuming format explicitly allows blank. Preferred explicit examples:

- `TRIGGER_LEVEL_UNCONFIRMED`
- `DISTANCE_TO_TRIGGER_UNCONFIRMED`
- `INVALIDATION_UNCONFIRMED`
- `SOURCE_AS_OF_UNCONFIRMED`
- `EVIDENCE_ROWS_UNCONFIRMED`
- `NEWS_UNCONFIRMED`

Missing data must be marked unconfirmed, not invented.

## Plain-English Wording Rules

- Vague "wait for confirmation" wording is not allowed unless paired with the actual trigger path and confirmation rule.
- Every card must explain what needs to happen next.
- Every blocked/no-trade card must explain why it is not actionable.
- Every stale/spent card must explicitly say there is no fresh trigger.
- Every missing data field must be marked unconfirmed, not inferred or filled from future movement.
- Pending completed-candle cards must say what candle/timeframe must complete and what must hold or reclaim.
- Triggered signal stage means shadow signal review only. It must not say live trade approved.
- If trigger level, invalidation, freshness, evidence, or source-as-of is missing, the card must avoid trade-readiness claims.

## Phone Alert Format

The phone version must be short and readable. It must include:

- `symbol`
- `setup_type`
- `stage`
- trigger zone/level
- what needs to happen next
- fresh/stale/spent state
- blocker/caution summary
- `headline_news_status`
- no-trade warning when applicable
- one-line next action

Phone alerts are summaries only. The full trigger card and log remain on the laptop/local watcher output for later ChatGPT review.

## Laptop / Full-Card Format

The laptop/full-card version must be complete enough for later ChatGPT review. It must include:

- source/evidence rows
- diagnostic reason codes
- unavailable fields
- duplicate-suppression key inputs
- best-candidate ranking inputs
- blocker/caution details
- trigger and invalidation context
- diagnostic explanation fields
- source-as-of metadata
- no-trade reason when applicable
- next check or next alert condition

## Diagnostic Scope

Diagnostics are explanation-only at first. They may explain why SAFE-FAST called:

- setup type
- lifecycle stage
- blocker
- caution
- freshness state
- stale/spent state
- next step
- no-go or no-trade status

Diagnostics must not change trading decisions, override setup/stage logic, override blockers, override stale/spent discipline, or promote any card to live trade status in this contract.

## Headline / News Scope

Headline/news is a context and risk layer, not a signal engine.

- Default to `NEWS_UNCONFIRMED` unless a future explicit source-review reads a valid source.
- Do not create news blockers or cautions without a valid source.
- Do not fabricate headlines, macro events, earnings, filings, signals, outcomes, trigger levels, P&L, or trade facts.
- Most news should be `NEWS_CAUTION`, not `NEWS_BLOCK`.
- Use `NEWS_BLOCK` only for immediate/material risk to the setup, trade window, intended hold window, gap risk, liquidity/execution, or event-driven invalidation.
- News must not create trades, erase setup identity, or turn a bad setup into a trade.

## Duplicate Suppression Support

Each full trigger card must include enough inputs to support this suppression key:

`symbol + setup_family + direction + stage + trigger_status + freshness_state + primary_blocker + trigger_zone_bucket + invalidation_bucket`

Material changes that should create alerts:

- stage change
- trigger status change
- fresh-to-stale/spent change
- blocker/caution severity change
- trigger-zone material movement
- invalidation material movement
- new best candidate

Non-material repeated same-state cards should be suppressible. Suppression must not hide new blockers, stale/spent transitions, changed trigger paths, or materially changed evidence quality.

## Best Current Candidate / Focus Support

Each full trigger card must include ranking inputs for:

- eligibility/stage validity
- freshness
- setup family priority only if explicitly defined
- trigger proximity
- blocker severity
- context risk
- stale/spent demotion
- evidence quality
- deterministic tie-breaker

Do not rank simply by closest-to-trigger. No-trade discipline remains above focus ranking. A blocked, stale, spent, unconfirmed, or evidence-poor setup must not outrank a cleaner current candidate solely because it is close to a level.

## No-Go Boundaries

- No watcher implementation.
- No `main.py` / engine changes.
- No Railway.
- No production.
- No auto-trading.
- No broker/order execution.
- No option P&L.
- No account sizing.
- No live trade decisions.
- No generated reports.
- No live data fetches.
- No production readiness or live trade readiness claims.

## Generic Review Examples

These examples are generic wording patterns only. They do not assert live market data, live signals, trigger levels, P&L, or trade facts.

### Near-Trigger Setup

`SYMBOL` has a `Clean Fast Break` `bullish/call-side` setup in `near-trigger` stage. Trigger zone is `TRIGGER_ZONE_UNCONFIRMED` unless supplied by accepted evidence. Next step: price must reach the defined reclaim/break zone and satisfy the stated completed-candle rule. Freshness is `fresh` if evidence supports it; otherwise `unconfirmed`. No live trade approval is implied.

### Pending Completed-Candle Approval

`SYMBOL` has an `Ideal` setup in `pending_completed_candle_approval`. Next step: the specified confirmation candle must complete while holding the trigger path condition. Until that candle completes, trigger status remains `pending_completed_candle`, not `triggered`.

### Stale / Spent No-Fresh-Trigger

`SYMBOL` has a `Continuation` context in `stale/spent/no-fresh-trigger`. There is no fresh trigger now. Next step: wait for rebuilt structure and a new valid trigger path before the card can become actionable in shadow review.

### Blocked / No-Trade

`SYMBOL` has a `UNCONFIRMED` or blocked setup in `blocked/no-trade`. It is not actionable because required trigger, invalidation, freshness, source, or evidence fields are unavailable or because an accepted blocker is active. Next step: resolve the named blocker or keep the card watch-only.

### Phone Alert Version

`SYMBOL | Ideal | near-trigger | zone: UNCONFIRMED | next: needs completed-candle hold through trigger path | fresh: unconfirmed | risk: caution/blocker summary | news: NEWS_UNCONFIRMED | no trade until trigger/invalidation/evidence are confirmed.`

## Review Decision

Trigger-card contract/schema review status: PASS.

Reason: the required full-card fields, allowed values, unavailable-field handling, phone-alert requirements, full-card review requirements, diagnostic/news boundaries, duplicate suppression support, best-current-candidate inputs, wording rules, and no-go boundaries are defined for future watcher foundation work.

Continuous Watcher implementation remains deferred. The next objective is the master handoff package, preserving this trigger-card contract and all no-go boundaries.
