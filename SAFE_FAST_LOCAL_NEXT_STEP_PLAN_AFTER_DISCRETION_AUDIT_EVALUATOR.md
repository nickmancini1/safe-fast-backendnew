# SAFE-FAST Local Next-Step Plan After Discretion Audit Evaluator

## Baseline

- **Baseline:** patch8
- **Repo:** `safe-fast-backendnew`
- **Branch:** `main`
- **Day context:** Day 28
- **Latest completed milestone commit:** `ecf9f4b Add local next-step plan after discretion audit evaluator`
- **Latest build-state sync after discretion audit coverage next-step plan:** `477ecb8 Sync build state after discretion audit coverage next-step plan`; bookkeeping only, not a new milestone.
- **Work mode:** build work only, not live trade chat

## Current Proven Foundation

- The local-only in-memory SAFE-FAST trading-plan discretion audit evaluator is implemented, committed, and synced.
- The evaluator accepts caller-provided in-memory rule and contract descriptions only.
- The evaluator identifies hidden discretionary language, supported discretion areas, safety discretion, forbidden signal discretion, and unsupported areas needing review.
- Existing proof layers remain local-only, in-memory, caller-provided-data layers.
- Existing proof layers preserve explicit no-trade, watch-only, no-live-data, no-controlled-shadow-data, no-watcher-loop, no-alert, and no-broker boundaries.
- Viability proof remains the highest priority.

## Still Not Proven / No-Go Boundaries

- SAFE-FAST trading-plan viability is not proven.
- The discretion audit evaluator identifies discretion in supplied descriptions, but it does not prove complete coverage across every major SAFE-FAST trading-plan area.
- Historical optimization itself has not started.
- This plan does not start optimization.
- This plan does not change rules yet.
- Controlled shadow data has not started.
- Live data has not started.
- Watcher loops, alert delivery, production readiness, broker/order execution, option P&L, account sizing, live trade readiness, and live trade decisions remain forbidden.
- No rule, contract, ranking, trigger, invalidation, freshness, duplicate suppression, alert workflow, user-facing workflow, production, Railway/deploy, `main.py`, or engine-logic change is authorized by this plan.

## Active Objective

Create exactly one next local-only implementation step:

**A local-only in-memory SAFE-FAST discretion audit coverage evaluator.**

The future evaluator must verify that caller-provided discretion-audit summaries cover all required SAFE-FAST trading-plan areas before any later rule review, evidence-backed fix, or optimization-readiness discussion depends on the audit.

## Required Coverage Areas

The future evaluator must require audit coverage for all of these SAFE-FAST trading-plan areas:

- setup recognition
- trigger
- invalidation
- fresh/stale/spent
- blocker/caution
- ranking/focus
- outcome scoring
- diagnostics
- user workflow

## Allowed Next Implementation Step

The next implementation may add only the local-only in-memory SAFE-FAST discretion audit coverage evaluator.

Required behavior:

- Accept caller-provided in-memory discretion-audit summaries only.
- Verify audit coverage across required SAFE-FAST trading-plan areas.
- Require coverage for setup recognition, trigger, invalidation, fresh/stale/spent, blocker/caution, ranking/focus, outcome scoring, diagnostics, and user workflow.
- Identify missing audit areas.
- Identify areas with forbidden signal discretion.
- Identify areas with only safety discretion.
- Identify areas marked `inconclusive`, `unavailable_evidence`, or `needs_review`.
- Return an in-memory coverage summary only.
- Not change trading rules.
- Not optimize.
- Write no files, logs, reports, artifacts, exports, or generated output.
- Fetch no data and read no live sources.
- Start no live data or controlled shadow data.
- Create no watcher loops, schedulers, daemons, polling, background workers, or alert delivery.
- Send no alerts.
- Touch no broker/order/account/options/P&L systems.
- Make no live trade decisions.

## Exact Allowed Files For The Next Implementation Step

- `watcher_foundation/discretion_audit_coverage.py`
- `watcher_foundation/__init__.py`
- `tests/test_discretion_audit_coverage.py`
- `SAFE_FAST_BUILD_STATE.md`

No other files are allowed for the next implementation step unless the user explicitly expands scope.

## Exact Forbidden Files / Systems

- `main.py`
- Trading engine logic
- Railway files
- Deploy/production configuration
- Secrets, `.env`, credentials, tokens, keys, or account settings
- Live backend or live data startup code
- Controlled shadow data startup code
- Watcher loops, schedulers, polling loops, daemons, or background workers
- Alert delivery systems
- Generated logs, generated reports, exports, artifacts, or output directories
- Broker/order/account systems
- Options, option P&L, account sizing, position sizing, or trade execution systems
- Live trade decision logic
- Optimization changes to rules, contracts, ranking, triggers, invalidation, freshness, duplicate suppression, alert workflow, diagnostics, outcome scoring, or user-facing workflow
- Any file outside the exact allowed files list

## Required Tests

Add focused local unit tests for the discretion audit coverage evaluator covering:

- The evaluator accepts caller-provided in-memory discretion-audit summaries only.
- The evaluator requires all required trading-plan areas.
- Missing setup recognition coverage is identified.
- Missing trigger coverage is identified.
- Missing invalidation coverage is identified.
- Missing fresh/stale/spent coverage is identified.
- Missing blocker/caution coverage is identified.
- Missing ranking/focus coverage is identified.
- Missing outcome scoring coverage is identified.
- Missing diagnostics coverage is identified.
- Missing user workflow coverage is identified.
- Areas with forbidden signal discretion are identified.
- Areas with only safety discretion are identified.
- Areas marked `inconclusive`, `unavailable_evidence`, or `needs_review` are identified.
- The evaluator returns an in-memory coverage summary only.
- The evaluator does not change trading rules.
- The evaluator does not optimize.
- The evaluator writes no files/logs/reports and fetches no data.
- The evaluator starts no live data or controlled shadow data.
- The evaluator creates no watcher loops, sends no alerts, touches no broker/order/account/options/P&L systems, and makes no live trade decisions.

Required validation commands for that future implementation:

- `python -m unittest discover -s tests -p test_discretion_audit_coverage.py`
- `python -m unittest discover -s tests -p test_discretion_audit.py`
- `python -m unittest tests.test_watcher_foundation_scaffold`
- `git diff --check`

## Required Doc / Build-State Updates

The next implementation must update `SAFE_FAST_BUILD_STATE.md` in the same implementation change with:

- status of the local-only in-memory SAFE-FAST discretion audit coverage evaluator
- baseline `patch8`
- implementation file and test file
- focused test result
- relevant discretion-audit and watcher-foundation regression test results
- `git diff --check` result
- preserved scope/no-go boundaries
- next objective after the coverage evaluator

Do not create another standalone build-state sync after a sync. If commit hash/status wording is stale after the implementation commit, update only the build state as explicitly requested.

## Optimization And Rule-Change Boundary

This plan does not start optimization.

This plan does not change rules yet.

Future rule changes require evidence, a diagnosed failure category, a targeted fix path, and regression tests. A discretionary preference, vague review note, missing coverage result, or coverage-only finding is not enough to change a SAFE-FAST rule, trigger, invalidation, freshness state, ranking/focus rule, blocker/caution rule, outcome scoring rule, diagnostic label, or user workflow.

## Viability Priority

Viability proof remains the highest priority.

Detection alone is not enough. A watcher alone is not enough. A discretion audit coverage evaluator is a guardrail for ensuring the discretion audit actually reviews the major trading-plan areas; it does not prove SAFE-FAST viability by itself.

The next implementation should make audit coverage gaps visible so later evidence-backed fixes can be reviewed without letting judgment create signals, approve trades, override missing proof, move triggers, hide failures, or rewrite outcomes after the fact.

## Boundary Statement

This plan is docs-only and recommends one local-only in-memory coverage evaluator.

This plan does not start controlled shadow data, live data, watcher loops, alerts, generated logs/reports, broker/order execution, option P&L, account sizing, production work, optimization, rule changes, or live trade decisions.

This plan does not modify `main.py`, trading engine logic, Railway/deploy files, secrets, `.env` files, credentials, generated output paths, watcher loops, schedulers, polling, alert delivery, broker/order/account behavior, options behavior, option P&L, position sizing, account sizing, or live trade decision logic.
