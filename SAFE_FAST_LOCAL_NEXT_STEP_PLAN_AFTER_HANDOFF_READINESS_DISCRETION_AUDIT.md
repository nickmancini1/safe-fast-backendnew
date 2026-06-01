# SAFE-FAST Local Next-Step Plan After Handoff-Readiness Discretion Audit

## Baseline

- **Baseline:** patch8
- **Repo:** `safe-fast-backendnew`
- **Branch:** `main`
- **Day context:** Day 28
- **Latest completed milestone commit:** `f71580d Add handoff readiness plan after historical optimization readiness`
- **Latest build-state sync after handoff-readiness plan:** `6438bec Sync build state after handoff readiness plan`
- **Work mode:** build work only, not live trade chat

## Current Proven Foundation

- The handoff-readiness plan after historical optimization readiness is implemented, committed, and synced.
- The local-only Day 60 outcome scoring contract validator is implemented and tested.
- The local-only Day 60 outcome scoring summary evaluator is implemented and tested.
- The local-only Day 60 outcome diagnostics evaluator is implemented and tested.
- The local-only Day 60 optimization readiness gate is implemented and tested.
- The local-only historical outcome proof preflight validator is implemented and tested.
- The local-only historical outcome proof summary evaluator is implemented and tested.
- The local-only historical outcome diagnostics evaluator is implemented and tested.
- The local-only historical optimization readiness gate is implemented and tested.
- Existing proof layers are local-only, in-memory, caller-provided-data layers.
- Existing proof layers preserve explicit no-trade, watch-only, no-live-data, no-controlled-shadow-data, and no-broker boundaries.
- Viability proof remains the highest priority.

## Still Not Proven / No-Go Boundaries

- SAFE-FAST trading-plan viability is not proven.
- The trading-plan discretion audit is not implemented yet.
- Hidden discretion in trading-plan language is not fully audited yet.
- Historical optimization itself has not started.
- This plan does not start optimization.
- This plan does not change rules yet.
- Controlled shadow data has not started.
- Live data has not started.
- Watcher loops, alert delivery, production readiness, broker/order execution, option P&L, account sizing, live trade readiness, and live trade decisions remain forbidden.
- No rule, contract, ranking, trigger, invalidation, freshness, duplicate suppression, alert workflow, user-facing workflow, production, Railway/deploy, `main.py`, or engine-logic change is authorized by this plan.

## Active Objective

Create exactly one next local-only implementation step:

**A local-only in-memory SAFE-FAST trading-plan discretion audit evaluator.**

The future evaluator must audit caller-provided in-memory rule and contract descriptions for hidden discretionary language. It must help identify where discretion appears in the trading plan without changing rules, optimizing behavior, fetching data, writing outputs, or making trade decisions.

## Discretion Rule To Preserve

- Signal logic should be as non-discretionary as possible.
- Human discretion may exist only as a no-trade veto, review note, or safety pause.
- Human discretion must not create a signal.
- Human discretion must not approve a trade.
- Human discretion must not override missing proof.
- Human discretion must not move triggers.
- Human discretion must not hide failures.
- Human discretion must not change outcome review after the fact.
- Ambiguous cases should remain explicit as `inconclusive`, `unavailable_evidence`, or `needs_review`.

## Allowed Next Implementation Step

The next implementation may add only the local-only in-memory SAFE-FAST trading-plan discretion audit evaluator.

Required behavior:

- Accept caller-provided in-memory rule and contract descriptions only.
- Identify hidden discretionary language.
- Flag vague phrases including `looks good`, `wait for confirmation`, `strong enough`, `weak signal`, `use judgment`, `good setup`, `bad setup`, `probably`, `maybe`, and `feels right`.
- Classify whether discretion appears in setup recognition, trigger, invalidation, fresh/stale/spent, blocker/caution, ranking/focus, outcome scoring, diagnostics, or user workflow.
- Distinguish safety discretion from signal discretion.
- Allow human discretion only for no-trade veto, review note, or safety pause.
- Treat discretion that can create a signal, approve a trade, override missing proof, move triggers, hide failures, or change outcome review after the fact as forbidden signal discretion.
- Return an in-memory audit summary only.
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

- `watcher_foundation/discretion_audit.py`
- `watcher_foundation/__init__.py`
- `tests/test_discretion_audit.py`
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
- Optimization changes to rules, contracts, ranking, triggers, invalidation, freshness, duplicate suppression, alert workflow, or user-facing workflow
- Any file outside the exact allowed files list

## Required Tests

Add focused local unit tests for the discretion audit evaluator covering:

- The evaluator accepts caller-provided in-memory rule and contract descriptions only.
- Hidden discretionary language is identified.
- Vague phrases are flagged, including `looks good`, `wait for confirmation`, `strong enough`, `weak signal`, `use judgment`, `good setup`, `bad setup`, `probably`, `maybe`, and `feels right`.
- Discretion is classified across setup recognition, trigger, invalidation, fresh/stale/spent, blocker/caution, ranking/focus, outcome scoring, diagnostics, and user workflow.
- Safety discretion is distinguished from signal discretion.
- Human discretion is allowed only for no-trade veto, review note, or safety pause.
- Signal discretion that can create a signal, approve a trade, override missing proof, move triggers, hide failures, or change outcome review after the fact is rejected or clearly flagged as forbidden.
- The evaluator returns an in-memory audit summary only.
- The evaluator does not change trading rules.
- The evaluator does not optimize.
- The evaluator writes no files/logs/reports and fetches no data.
- The evaluator starts no live data or controlled shadow data.
- The evaluator creates no watcher loops, sends no alerts, touches no broker/order/account/options/P&L systems, and makes no live trade decisions.

Required validation commands for that future implementation:

- `python -m unittest discover -s tests -p test_discretion_audit.py`
- `python -m unittest tests.test_watcher_foundation_scaffold`
- `git diff --check`

## Required Doc / Build-State Updates

The next implementation must update `SAFE_FAST_BUILD_STATE.md` in the same implementation change with:

- status of the local-only in-memory SAFE-FAST trading-plan discretion audit evaluator
- baseline `patch8`
- implementation file and test file
- focused test result
- relevant regression test results
- `git diff --check` result
- preserved scope/no-go boundaries
- next objective after the evaluator

Do not create another standalone build-state sync after a sync. If commit hash/status wording is stale after the implementation commit, update only the build state as explicitly requested.

## Optimization And Rule-Change Boundary

This plan does not start optimization.

This plan does not change rules yet.

Future rule changes require evidence, a diagnosed failure category, a targeted fix path, and regression tests. A discretionary preference or vague review note is not enough to change a SAFE-FAST rule, trigger, invalidation, freshness state, ranking/focus rule, blocker/caution rule, outcome scoring rule, diagnostic label, or user workflow.

## Viability Priority

Viability proof remains the highest priority.

Detection alone is not enough. A watcher alone is not enough. A discretion audit is a guardrail for preserving rule-based proof; it does not prove SAFE-FAST viability by itself.

The next implementation should make hidden discretion visible so later evidence-backed fixes can be reviewed without letting judgment create signals, approve trades, override missing proof, move triggers, hide failures, or rewrite outcomes after the fact.

## Boundary Statement

This plan is docs-only and recommends one local-only in-memory evaluator.

This plan does not start controlled shadow data, live data, watcher loops, alerts, generated logs/reports, broker/order execution, option P&L, account sizing, production work, optimization, rule changes, or live trade decisions.

This plan does not modify `main.py`, trading engine logic, Railway/deploy files, secrets, `.env` files, credentials, generated output paths, watcher loops, schedulers, polling, alert delivery, broker/order/account behavior, options behavior, option P&L, position sizing, account sizing, or live trade decision logic.
