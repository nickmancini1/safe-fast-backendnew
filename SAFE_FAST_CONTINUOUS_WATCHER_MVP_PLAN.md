# SAFE-FAST Continuous Watcher MVP Plan - Deferred Planning Reference

## Planning Status

- **Continuous Watcher MVP planning status:** DEFERRED PLANNING ONLY
- **Baseline:** patch8
- **Latest local commit before planning:** `69fffc2 Add next phase decision after chart outcome closeout`
- **Scope:** deferred docs-only planning reference for a bounded watch-only Continuous Watcher MVP.

This watcher plan is deferred planning only. No watcher implementation or deeper watcher design should proceed until broader chart-based trade outcome backtesting coverage is planned and reviewed. A Continuous Watcher must not be designed or built around only the three current SPY chart outcome samples.

This plan does not implement watcher code, change `main.py`, change schemas, change fixtures, change runner code, change chart outcome code, model option P&L, add account sizing, touch Railway/deploy/production files, auto-trade, use live reads, or make live trade decisions.

## Inputs Reviewed

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_NEXT_BOUNDED_PHASE_AFTER_CHART_OUTCOME_V1_CLOSEOUT_REVIEW.md`
- `SAFE_FAST_PROJECT_MASTER_HANDOFF.md`
- `SAFE_FAST_ACCOUNT_MODE_AND_TRADE_STYLE_PLAN.md`
- `historical_signal_replay/REAL_HISTORICAL_REPLAY_V1_SPY_THREE_SETUP_CLOSEOUT_REVIEW.md`
- `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_CLOSEOUT_REVIEW.md`

## Watch-Only Scope

The Continuous Watcher MVP is a watch-only state tracker and alert planner. It may observe allowed symbols, preserve setup identity, track lifecycle changes, and emit planned alert text only when a meaningful state change occurs.

The MVP must not place orders, recommend live entries as execution instructions, size positions, select option contracts, model option P&L, infer unavailable live data, or promote a setup into a live trade decision.

## Allowed Universe

Only these symbols are in scope:

- SPY
- QQQ
- IWM
- GLD

Any other symbol must be out of scope for MVP planning and later implementation unless a separate bounded task expands the universe.

## Allowed Setup Families

Only these setup families are in scope:

- Ideal
- Clean Fast Break
- Continuation

Setup identity must be preserved through blockers, cautions, market-closed gates, unavailable live fields, and session-boundary handling. A blocked or not-ready setup remains its recognized family when the evidence supports that identity.

## Lifecycle States To Track

The watcher MVP should track a compact lifecycle model for each `symbol + setup_family + direction` candidate:

- `not_present`: no recognized setup candidate is currently active.
- `forming_context`: early structure exists, but the setup is not yet near an actionable trigger stage.
- `watching`: setup family is recognized and worth monitoring, but trigger requirements are incomplete.
- `pending_confirmation`: trigger-adjacent behavior exists, but completed-candle approval, next-bar hold, retest hold, or required confirmation is not proven.
- `trigger_candidate`: a fresh qualifying signal-stage candidate exists in chart/state terms, still watch-only.
- `blocked`: setup identity exists, but a hard blocker prevents trade readiness.
- `caution`: setup identity exists with non-blocking risk context that must be surfaced.
- `spent`: prior trigger or break already happened and is not fresh for the current decision window.
- `invalidated`: setup thesis failed, invalidation broke, or required structure no longer exists.
- `expired`: setup aged out, crossed a session boundary without fresh confirmation, or no longer belongs to the active watch window.

The implementation phase may refine names only after replay/regression cases prove the mapping, but it should not expand beyond signal/stage/lifecycle tracking without explicit approval.

## Meaningful State-Change Rules

Alerts should be considered only when the candidate changes in a way that affects the human review decision. Meaningful changes include:

- New allowed setup family appears for an allowed symbol.
- Setup family changes between Ideal, Clean Fast Break, and Continuation.
- Lifecycle advances toward readiness, such as `forming_context` to `watching`, `watching` to `pending_confirmation`, or `pending_confirmation` to `trigger_candidate`.
- Lifecycle degrades away from readiness, such as `trigger_candidate` to `spent`, `blocked`, `invalidated`, or `expired`.
- First hard blocker appears, clears, or changes priority.
- First caution appears, clears, or materially changes risk context.
- Trigger freshness changes, especially fresh current-session trigger versus prior-session spent context.
- Market/session status changes the current state interpretation.
- Previously unavailable required live field becomes confirmed or confirmed data becomes unavailable/unconfirmed.

Non-meaningful formatting changes, timestamp-only refreshes, repeated identical state, and unchanged cautions/blockers should not create new alerts.

## Duplicate Alert Suppression Rules

The MVP should suppress duplicate alert spam using a stable state fingerprint. The fingerprint should be based on symbol, setup family, direction, lifecycle state, trigger freshness, first blocker, first caution, session date, and relevant proof-mode evidence keys.

Suppression requirements:

- Do not alert again for the same state fingerprint during the same active watch window.
- Do not alert repeatedly on every poll while the state remains unchanged.
- Allow a new alert when the state fingerprint changes meaningfully.
- Allow a new alert after an invalidated, expired, or spent setup later rebuilds into a fresh setup.
- Preserve a state history sufficient for shadow review, including suppressed repeat counts.
- Include a reason when an alert is suppressed.

## Unavailable Live-Field Handling

Unavailable live fields must be marked `unconfirmed`. The watcher must not invent live reads, macro data, IV data, headline data, 24H context, account status, option chain data, liquidity, fills, or broker/order state.

If `getSafeFastOnDemand` or another approved future data source is unavailable, the watcher should keep chart/setup fields that are actually available and label missing fields as `unconfirmed`, not `false`, not passed, and not failed unless existing evidence proves failure.

Unavailable fields may be surfaced as caution/context when relevant, but they must not be converted into live trade permission.

## Session-Boundary Handling

Session boundaries must prevent stale prior-session triggers from becoming fresh current-session alerts.

Requirements:

- Track the regular-session date associated with each setup state.
- Treat prior-session completed breaks as spent context unless a fresh current-session trigger appears.
- Preserve weekend and known-market-holiday carry-forward rules from existing protected behavior.
- Expire or downgrade states that aged out across sessions without fresh confirmation.
- Generate a new alert only when a fresh current-session state change occurs or when prior-session context materially changes the current watch decision.

## Same-State Repeat Handling

Repeated identical states should be counted, not alerted. The watcher plan should require storage of:

- first seen timestamp
- last seen timestamp
- repeat count
- last alert timestamp
- last suppression reason

Same-state repeats may update internal evidence for shadow review, but they should produce no user-facing alert unless a configured heartbeat/report view is explicitly added in a later bounded task.

## Alert Payload Requirements

Each alert payload should include enough information for a human to review the setup without implying live execution:

- symbol
- setup family
- direction when known
- lifecycle state
- previous lifecycle state
- state-change reason
- trigger freshness
- session date
- key level or trigger reference when available
- invalidation reference when available
- first blocker when present
- cautions/watchouts when present
- unavailable fields marked `unconfirmed`
- duplicate-suppression fingerprint
- evidence snapshot ID or source row/timestamp reference
- plain-English summary
- plain-English next review condition
- explicit `watch_only: true`
- explicit `live_trade_decision: false`

The payload must not include option contract P&L, account sizing, broker/order instructions, auto-trade flags, or production deployment instructions.

## Plain-English Output Requirements

User-facing output should be concise and decision-aiding:

- Name the symbol and setup family plainly.
- State what changed since the prior watcher state.
- Explain whether the setup is forming, watching, pending confirmation, trigger-candidate, blocked, spent, invalidated, or expired.
- Humanize raw reason keys instead of exposing internal labels alone.
- Say what evidence is still needed for the next watch-only review step.
- Mark unavailable fields as unconfirmed.
- Avoid language that sounds like an order instruction, position size recommendation, or live trade command.

## Proof-Mode Evidence Requirements

Before watcher implementation or deeper watcher design can proceed, broader chart-based trade outcome backtesting coverage must be planned and reviewed. After that prerequisite review, proof-mode evidence for any later watcher work must include:

- replay/regression cases for lifecycle transitions across Ideal, Clean Fast Break, and Continuation
- duplicate suppression tests for same-state repeats and meaningful changes
- session-boundary tests for prior-session, weekend, and holiday carry-forward
- unavailable live-field tests proving fields are marked `unconfirmed`
- alert payload contract tests proving watch-only and no-live-trade boundaries
- historical replay evidence for SPY, QQQ, IWM, and GLD before broader claims are made
- shadow-review logs comparing watcher state changes against human-reviewed chart context

Proof-mode evidence must prove state tracking and alert discipline, not profitability or live trading readiness.

## Shadow-Review Requirements

Shadow review must run before any production or proof-mode promotion decision. It should compare watcher observations with human chart review and record:

- correct setup family recognition
- correct lifecycle state
- missed meaningful changes
- false meaningful changes
- duplicate alerts that should have been suppressed
- suppressed alerts that should have been sent
- session-boundary mistakes
- unavailable-field handling mistakes
- plain-English output clarity issues

Shadow review should produce a written review artifact with pass/fail status and known limits before implementation is considered ready for any live-adjacent use.

## Boundaries

- **Plan status:** deferred planning only
- **Deeper watcher design before broader chart-based backtesting coverage is planned/reviewed:** no
- **Option P&L modeled:** no
- **Account sizing added:** no
- **Production/Railway touched:** no
- **Live trade decisions:** no
- **Auto-trading:** no
- **Broker/order execution:** no
- **Watcher implementation started:** no
- **`main.py` changed:** no
- **Schemas changed:** no
- **Fixtures changed:** no
- **Runner code changed:** no
- **Chart outcome code changed:** no

## Known Limits

- This is a deferred planning document only.
- No watcher storage, alert service, scheduler, poller, data adapter, or UI exists from this task.
- The current validated chart outcome evidence is limited to three SPY setup-family samples.
- A watcher should not be designed or implemented around only those three SPY chart outcome samples.
- QQQ, IWM, and GLD remain allowed universe members but do not yet have matching closeout evidence in the inspected chart outcome closeout.
- Live macro, IV, headline, event, account, option-chain, and broker data remain unavailable unless explicitly supplied by later approved sources.
- The plan does not prove profitability, account safety, production readiness, or live trading readiness.

## Recommended Next Task

Plan broader chart-based trade outcome backtesting coverage before Continuous Watcher implementation or deeper watcher design, without changing `main.py`, schemas, fixtures, runner code, reports, chart outcome code, option P&L, account sizing, production/Railway, or live trade behavior.
