# SAFE-FAST Local Next-Step Plan After Historical Outcome Proof Summary

## Baseline

- **Baseline:** patch8
- **Repo:** `safe-fast-backendnew`
- **Branch:** `main`
- **Day context:** Day 28
- **Latest completed code milestone:** `bf9cd8c Add historical outcome proof summary evaluator`
- **Latest build-state sync after historical outcome proof summary evaluator:** `dfd3acd Sync build state after historical outcome proof summary evaluator`

## Current Proven Foundation

- The local-only Day 60 outcome scoring contract validator is implemented, committed, tested, and synced.
- The local-only Day 60 outcome scoring summary evaluator is implemented, committed, tested, and synced.
- The local-only Day 60 outcome diagnostics evaluator is implemented, committed, tested, and synced.
- The local-only Day 60 optimization readiness gate is implemented, committed, tested, and synced.
- The local-only in-memory historical outcome proof preflight validator is implemented, committed, tested, and synced.
- The local-only in-memory historical outcome proof summary evaluator is implemented, committed, tested, and synced.
- The current foundation accepts caller-provided in-memory historical outcome proof rows, validates them through the existing historical proof preflight path, and returns an in-memory historical proof summary only.
- Historical proof is continuing locally, but final viability is not proven yet.
- Viability proof remains the highest priority.

## Still Not Proven / No-Go Boundaries

- Historical outcome diagnostics are not yet implemented.
- Historical outcome proof summary is not final viability proof.
- Trading-plan viability is not yet proven.
- Diagnostics usefulness against historical outcome proof summaries is not yet proven.
- Optimization has not started and must not start from this plan.
- Diagnostics must remain in-depth before optimization.
- Controlled shadow data remains future work and is not started by this plan.
- Live data remains later and is not started by this plan.
- Day 60 shadow watcher viability is not proven.
- Production readiness is not proven.
- Broker/order execution is not proven and remains forbidden.
- Option P&L and account sizing are not proven and remain forbidden.
- Live trade readiness and live trade decisions remain forbidden.

## Active Objective

Create exactly one next local-only implementation step:

**A local-only in-memory historical outcome diagnostics evaluator.**

The future evaluator must move toward historical diagnostics by accepting the in-memory historical outcome proof summary and returning an in-memory historical diagnostics summary only.

## Allowed Next Implementation Step

The next implementation may add only the local-only in-memory historical outcome diagnostics evaluator.

Required behavior:

- Accept the in-memory historical outcome proof summary only.
- Identify historical diagnostic failure categories.
- Preserve the evidence used for each diagnostic finding.
- Preserve affected setup type when available.
- Preserve affected symbol when available.
- Preserve affected stage when available.
- Preserve trigger, invalidation, and freshness relationship when available.
- Preserve missing or unavailable evidence explicitly.
- Map historical diagnostic gaps to next fix paths.
- Label likely causes as candidates only, not asserted facts.
- Return an in-memory historical diagnostics summary only.
- Not optimize.
- Write no files, logs, reports, artifacts, exports, or generated output.
- Fetch no data and read no live sources.
- Start no live data or controlled shadow data.
- Create no watcher loops, schedulers, daemons, polling, background workers, or alert delivery.
- Send no alerts.
- Touch no broker/order/account/options/P&L systems.
- Make no live trade decisions.

## Exact Allowed Files For The Next Implementation Step

- `watcher_foundation/historical_outcome_diagnostics.py`
- `watcher_foundation/__init__.py`
- `tests/test_historical_outcome_diagnostics.py`
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

## Required Tests

Add focused local unit tests for the historical outcome diagnostics evaluator covering:

- The evaluator accepts the in-memory historical outcome proof summary only.
- Historical diagnostic failure categories are identified from summary inputs without fabricating unavailable facts.
- Evidence used for each finding is preserved.
- Affected setup type, symbol, stage, and trigger/invalidation/freshness relationship are preserved when available.
- Missing or unavailable evidence remains explicit.
- Historical diagnostic gaps map to next fix paths.
- Likely causes are labeled as candidates only, not asserted facts.
- The evaluator returns an in-memory historical diagnostics summary only.
- Optimization is not started.
- The evaluator writes no files/logs/reports and fetches no data.
- The evaluator starts no live data or controlled shadow data.
- The evaluator creates no watcher loops, sends no alerts, touches no broker/order/account/options/P&L systems, and makes no live trade decisions.

Required validation commands for that future implementation:

- `python -m unittest discover -s tests -p test_historical_outcome_diagnostics.py`
- `python -m unittest discover -s tests -p test_historical_outcome_proof_summary.py`
- `python -m unittest discover -s tests -p test_historical_outcome_proof_preflight.py`
- `python -m unittest discover -s tests -p test_day60_outcome_diagnostics.py`
- `python -m unittest discover -s tests -p test_day60_outcome_scoring_summary.py`
- `python -m unittest discover -s tests -p test_day60_outcome_scoring_contract.py`
- `git diff --check`

## Required Doc / Build-State Updates

The next implementation must update `SAFE_FAST_BUILD_STATE.md` in the same implementation change with:

- status of the local-only in-memory historical outcome diagnostics evaluator
- baseline `patch8`
- implementation file and test file
- focused test result
- relevant regression test results
- `git diff --check` result
- preserved scope/no-go boundaries
- next objective after the evaluator

Do not create another standalone build-state sync after a sync. If commit hash/status wording is stale after the implementation commit, update only the build state as explicitly requested.

## Diagnostics And Optimization Boundary

Diagnostics must be in-depth before optimization.

This plan does not start optimization. No rule, contract, ranking, trigger, invalidation, freshness, duplicate suppression, alert workflow, or user-facing workflow change may be promoted in this step. Any future optimization must be evidence-backed and regression-tested after a diagnosed failure category, targeted fix path, and preserved no-trade boundaries exist.

## Boundary Statement

This continues historical proof locally but does not prove final viability yet.

This plan does not start controlled shadow data, live data, watcher loops, alerts, generated logs/reports, broker/order execution, option P&L, account sizing, production work, optimization, or live trade decisions. Controlled shadow data remains future work and is not started by this plan. Live data remains later and is not started by this plan. Viability proof remains the highest priority.
