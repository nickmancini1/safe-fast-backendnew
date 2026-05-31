# SAFE-FAST Local Next-Step Plan After Historical Outcome Diagnostics

## Baseline

- **Baseline:** patch8
- **Repo:** `safe-fast-backendnew`
- **Branch:** `main`
- **Day context:** Day 28
- **Latest completed code milestone:** `002cb0a Add historical outcome diagnostics evaluator`
- **Latest build-state sync after historical outcome diagnostics evaluator:** `8310296 Sync build state after historical outcome diagnostics evaluator`

## Current Proven Foundation

- The local-only Day 60 outcome scoring contract validator is implemented, committed, tested, and synced.
- The local-only Day 60 outcome scoring summary evaluator is implemented, committed, tested, and synced.
- The local-only Day 60 outcome diagnostics evaluator is implemented, committed, tested, and synced.
- The local-only Day 60 optimization readiness gate is implemented, committed, tested, and synced.
- The local-only in-memory historical outcome proof preflight validator is implemented, committed, tested, and synced.
- The local-only in-memory historical outcome proof summary evaluator is implemented, committed, tested, and synced.
- The local-only in-memory historical outcome diagnostics evaluator is implemented, committed, tested, and synced.
- The current foundation accepts caller-provided in-memory historical outcome proof summaries and returns in-memory historical outcome diagnostics only.
- Historical diagnostics now preserve diagnosed failure categories, evidence, affected setup type, symbol, stage, trigger/invalidation/freshness relationship, unavailable evidence, candidate-only likely causes, and next fix paths.
- Historical proof is continuing locally, but final viability is not proven yet.
- Viability proof remains the highest priority.

## Still Not Proven / No-Go Boundaries

- Historical optimization readiness is not yet gated.
- Historical outcome diagnostics are not final viability proof.
- Trading-plan viability is not yet proven.
- Optimization has not started and must not start from this plan.
- No rule, contract, ranking, trigger, invalidation, freshness, duplicate suppression, alert workflow, or user-facing workflow change is proven or allowed by this plan.
- Controlled shadow data remains future work and is not started by this plan.
- Live data remains later and is not started by this plan.
- Day 60 shadow watcher viability is not proven.
- Production readiness is not proven.
- Broker/order execution is not proven and remains forbidden.
- Option P&L and account sizing are not proven and remain forbidden.
- Live trade readiness and live trade decisions remain forbidden.

## Active Objective

Create exactly one next local-only implementation step:

**A local-only in-memory historical optimization readiness gate.**

The future gate must move toward historical optimization readiness by accepting the in-memory historical outcome diagnostics summary and returning an in-memory historical optimization readiness summary only. It must not start optimization.

## Allowed Next Implementation Step

The next implementation may add only the local-only in-memory historical optimization readiness gate.

Required behavior:

- Accept the in-memory historical outcome diagnostics summary only.
- Verify each potential historical fix path has a diagnosed failure category.
- Verify evidence is present or explicitly unavailable.
- Verify affected setup type is identified when available.
- Verify affected symbol is identified when available.
- Verify affected stage is identified when available.
- Verify trigger, invalidation, and freshness relationship is identified when available.
- Verify affected system area is identified when available.
- Verify the required regression test path is identified.
- Reject shallow labels like `failed setup`, `bad alert`, `weak signal`, or `bad trade` without evidence.
- Return an in-memory historical optimization readiness summary only.
- Not change rules, contracts, ranking, triggers, invalidation, freshness, duplicate suppression, alerts, or user-facing workflow.
- Not optimize.
- Write no files, logs, reports, artifacts, exports, or generated output.
- Fetch no data and read no live sources.
- Start no live data or controlled shadow data.
- Create no watcher loops, schedulers, daemons, polling, background workers, or alert delivery.
- Send no alerts.
- Touch no broker/order/account/options/P&L systems.
- Make no live trade decisions.

## Exact Allowed Files For The Next Implementation Step

- `watcher_foundation/historical_optimization_readiness.py`
- `watcher_foundation/__init__.py`
- `tests/test_historical_optimization_readiness.py`
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

Add focused local unit tests for the historical optimization readiness gate covering:

- The gate accepts the in-memory historical outcome diagnostics summary only.
- Each potential historical fix path requires a diagnosed failure category.
- Evidence is required unless explicitly unavailable.
- Affected setup type, symbol, stage, trigger/invalidation/freshness relationship, and affected system area are preserved when available.
- Missing or unavailable evidence remains explicit.
- The required regression test path is identified for each readiness item.
- Shallow labels like `failed setup`, `bad alert`, `weak signal`, or `bad trade` are rejected when evidence is missing.
- The gate returns an in-memory historical optimization readiness summary only.
- Optimization is not started.
- The gate does not change rules, contracts, ranking, triggers, invalidation, freshness, duplicate suppression, alerts, or user-facing workflow.
- The gate writes no files/logs/reports and fetches no data.
- The gate starts no live data or controlled shadow data.
- The gate creates no watcher loops, sends no alerts, touches no broker/order/account/options/P&L systems, and makes no live trade decisions.

Required validation commands for that future implementation:

- `python -m unittest discover -s tests -p test_historical_optimization_readiness.py`
- `python -m unittest discover -s tests -p test_historical_outcome_diagnostics.py`
- `python -m unittest discover -s tests -p test_historical_outcome_proof_summary.py`
- `python -m unittest discover -s tests -p test_historical_outcome_proof_preflight.py`
- `python -m unittest discover -s tests -p test_day60_optimization_readiness.py`
- `python -m unittest discover -s tests -p test_day60_outcome_diagnostics.py`
- `python -m unittest discover -s tests -p test_day60_outcome_scoring_summary.py`
- `python -m unittest discover -s tests -p test_day60_outcome_scoring_contract.py`
- `git diff --check`

## Required Doc / Build-State Updates

The next implementation must update `SAFE_FAST_BUILD_STATE.md` in the same implementation change with:

- status of the local-only in-memory historical optimization readiness gate
- baseline `patch8`
- implementation file and test file
- focused test result
- relevant regression test results
- `git diff --check` result
- preserved scope/no-go boundaries
- next objective after the gate

Do not create another standalone build-state sync after a sync. If commit hash/status wording is stale after the implementation commit, update only the build state as explicitly requested.

## Optimization Boundary

This plan does not start optimization.

The next step is a readiness gate only. Future optimization must be evidence-backed and regression-tested after a diagnosed failure category, targeted fix path, required regression path, and preserved no-trade boundaries exist. No optimization is accepted without evidence, a diagnosed failure category, and regression coverage.

## Boundary Statement

This continues historical proof locally but does not prove final viability yet.

Controlled shadow data remains future work and is not started by this plan. Live data remains later and is not started by this plan. Viability proof remains the highest priority.

This plan does not start controlled shadow data, live data, watcher loops, alerts, generated logs/reports, broker/order execution, option P&L, account sizing, production work, optimization, or live trade decisions.
