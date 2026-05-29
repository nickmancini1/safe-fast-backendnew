# SAFE-FAST Day 60 Shadow Watcher Viability Diagnostics Requirements

## Purpose

This document exists so future chats do not lose the user's requirements around Day 60, shadow data, viability proof, diagnostics, and post-Day-60 workflow.

## Current Boundary Versus Day 60 Target

- Current foundation work is local-only unless a later bounded task explicitly authorizes controlled shadow data.
- "No live data" means no live data during the current local-only foundation phase.
- The Day 60 target will require a controlled shadow watcher path with market data input.
- Any shadow-data phase must remain no-trade, no-broker, no-order-execution, no account sizing, no option P&L, no live trade decisions, and no production deployment unless separately authorized and validated.
- Live data is not permission to trade.

## Day 60 Shadow Watcher Requirement

By Day 60, SAFE-FAST will be moving toward a working shadow SAFE-FAST Continuous Watcher prototype that watches SPY / QQQ / IWM / GLD, detects forming Ideal / Clean Fast Break / Continuation setups, exposes trigger cards, alerts on meaningful state changes, suppresses repeat same-state noise, ranks or focuses the best current candidate, and creates reviewable local evidence when explicitly authorized.

## Viability Proof Requirement

A watcher is not enough by itself. SAFE-FAST must eventually prove whether the trading plan is viable. The project must not stop at "it detected setups." It must be able to evaluate whether detected setups would have produced useful trading behavior under a no-hindsight review process.

## Required Future Tracking Fields

The future system must track:

- which setup type appeared: Ideal, Clean Fast Break, or Continuation
- symbol
- timestamp
- timeframe
- direction
- stage when detected
- whether the setup was forming, near-trigger, triggered, blocked, stale, spent, rebuilding, or invalidated
- the trigger card shown at the time
- trigger level or trigger zone when available
- confirmation rule
- current distance to trigger when available
- early-warning or near-trigger threshold when available
- invalidation level or invalidation condition
- fresh/stale/spent condition
- next check or next alert condition
- blocker/caution relationship to trigger readiness
- whether it later followed through or failed
- how far it moved after the trigger or candidate point
- maximum favorable move
- maximum adverse move
- time to follow-through
- time to failure
- whether it became stale or spent
- whether blockers were true blockers or false blockers
- whether missed setups had a repeated pattern
- whether bad alerts came from trigger logic, stage logic, stale/spent logic, market context, data quality, ranking/focus logic, or unavailable evidence
- evidence references used for review
- explicit no-hindsight boundary

## Diagnostic Requirement If Results Are Not Successful

If the plan is not proven successful, SAFE-FAST must not simply declare failure. It must run diagnostic review to identify why the results are not working and what category of issue needs fixing.

Diagnostic categories must include at least:

- setup recognition failure
- stage-transition failure
- trigger-card failure
- trigger level or trigger-zone failure
- invalidation failure
- fresh/stale/spent classification failure
- blocker/caution classification failure
- duplicate suppression failure
- ranking/focus failure
- session-boundary carry-forward failure
- data-quality or missing-evidence issue
- market-context issue
- outcome-scoring issue
- review/logging issue

## Required Improvement Loop

Signal detection -> shadow alert/log -> outcome scoring -> diagnostic review -> rule adjustment -> regression test -> repeat.

No rule adjustment is promoted without regression evidence.

## Post-Day-60 $20-Tier Role

After Day 60, the $20 tier will be used for focused continuation, not rediscovery.

It will support:

- watcher-log review
- alert accuracy review
- outcome review
- diagnostic pattern review
- smaller Codex prompts
- alert tuning suggestions
- documentation/build-state maintenance
- targeted contract fixes
- handoff clarity

Future chats should rely on SAFE_FAST_BUILD_STATE.md, this new addendum, the Day 60 addendum, latest handoff package, watcher logs, trigger-card contracts, accuracy-review checklist, and current objective.

## Required Language Rule

Future chats must use firm project language.

Use "will" for agreed project direction.
Use "is proven" only when repo evidence exists.
Use "is not proven yet" when evidence does not exist.
Use "is blocked" when current boundaries prevent action.
Use "requires validation" when a step must be tested before promotion.
Avoid loose planning words like "could" and "probably" when describing agreed requirements.

## No-Go Boundaries

No production readiness, no live backend readiness, no Railway/deploy readiness, no broker/order execution, no auto-trading, no option P&L, no account sizing, no live trade decisions, no secrets/.env/credentials edits, no phone alerts, no watcher loops, and no generated reports/logs unless explicitly authorized.
