# SAFE-FAST Local Next-Step Plan After Day 60 Optimization Readiness

## Baseline

- **Baseline:** patch8
- **Repo:** `safe-fast-backendnew`
- **Branch:** `main`
- **Day context:** Day 28
- **Latest completed code milestone:** `2c4fe53 Add Day 60 optimization readiness gate`
- **Latest build-state sync after optimization readiness gate:** `710f74b Sync build state after Day 60 optimization readiness gate`

## Current Proven Foundation

- The local-only Day 60 shadow watcher input-contract preflight validator is implemented, committed, tested, and synced.
- The local-only Day 60 shadow session dry-run adapter is implemented, committed, tested, and synced.
- The local-only Day 60 shadow review/diagnostics packet builder is implemented, committed, tested, and synced.
- The local-only Day 60 diagnostics readiness evaluator is implemented, committed, tested, and synced.
- The local-only Day 60 outcome scoring contract validator is implemented, committed, tested, and synced.
- The local-only Day 60 outcome scoring summary evaluator is implemented, committed, tested, and synced.
- The local-only Day 60 outcome diagnostics evaluator is implemented, committed, tested, and synced.
- The local-only Day 60 optimization readiness gate is implemented, committed, tested, and synced.
- The current foundation is local, in-memory, caller-provided-input only, and bounded to historical/outcome review readiness mechanics.
- Historical proof begins after the local diagnostics foundation; this plan is the first bounded move toward historical outcome proof preflight validation.

## Still Not Proven / No-Go Boundaries

- Historical outcome proof is not yet proven.
- Trading-plan viability is not yet proven.
- Viability proof remains the highest priority.
- Optimization itself has not started.
- Controlled shadow data remains future work and is not started by this plan.
- Live data remains later and is not started by this plan.
- Day 60 shadow watcher viability is not proven.
- Diagnostics usefulness against real reviewed outcomes is not proven.
- Production readiness is not proven.
- Broker/order execution is not proven and remains forbidden.
- Option P&L and account sizing are not proven and remain forbidden.
- Live trade readiness and live trade decisions remain forbidden.

## Active Objective

Create exactly one next local-only implementation step:

**A local-only in-memory historical outcome proof preflight validator.**

The future validator must prepare caller-provided historical outcome proof rows for the existing outcome scoring contract without fetching data, generating proof, writing files, or starting any shadow/live workflow.

## Allowed Next Implementation Step

The next implementation may add only the local-only in-memory historical outcome proof preflight validator.

Required behavior:

- Accept caller-provided historical outcome proof rows only.
- Verify each row is shaped for the existing outcome scoring contract.
- Verify no-hindsight historical review boundaries.
- Verify symbol, setup type, timeframe, trigger/invalidation references, outcome window, evidence references, and unavailable fields are explicit.
- Reject fabricated proof values.
- Reject broker/order/account/options/P&L/trade-decision fields.
- Return in-memory validation results only.
- Write no files, logs, reports, artifacts, exports, or generated output.
- Fetch no data and read no live sources.
- Start no live data or controlled shadow data.
- Create no watcher loops, schedulers, daemons, polling, background workers, or alert delivery.
- Send no alerts.
- Touch no broker/order/account/options/P&L systems.
- Make no live trade decisions.

## Exact Allowed Files For The Next Implementation Step

- `watcher_foundation/historical_outcome_proof_preflight.py`
- `watcher_foundation/__init__.py`
- `tests/test_historical_outcome_proof_preflight.py`
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

Add focused local unit tests for the historical outcome proof preflight validator covering:

- The validator accepts caller-provided historical outcome proof rows only.
- Rows shaped for the existing outcome scoring contract are accepted.
- Rows missing required outcome scoring contract shape are rejected.
- No-hindsight historical review boundaries are required and preserved.
- Symbol, setup type, timeframe, trigger/invalidation references, outcome window, evidence references, and unavailable fields must be explicit.
- Fabricated proof values are rejected.
- Broker/order/account/options/P&L/trade-decision fields are rejected.
- Validation results are returned in memory only.
- The validator writes no files/logs/reports and fetches no data.
- The validator starts no live data or controlled shadow data.
- The validator creates no watcher loops, sends no alerts, touches no broker/order/account/options/P&L systems, and makes no live trade decisions.

Required validation commands for that future implementation:

- `python -m unittest discover -s tests -p test_historical_outcome_proof_preflight.py`
- `python -m unittest discover -s tests -p test_day60_outcome_scoring_contract.py`
- `python -m unittest discover -s tests -p test_day60_outcome_scoring_summary.py`
- `python -m unittest discover -s tests -p test_day60_outcome_diagnostics.py`
- `python -m unittest discover -s tests -p test_day60_optimization_readiness.py`
- `git diff --check`

## Required Doc / Build-State Updates

The next implementation must update `SAFE_FAST_BUILD_STATE.md` in the same implementation change with:

- status of the local-only in-memory historical outcome proof preflight validator
- baseline `patch8`
- implementation file and test file
- focused test result
- relevant regression test results
- `git diff --check` result
- preserved scope/no-go boundaries
- next objective after the validator

Do not create another standalone build-state sync after a sync. If commit hash/status wording is stale after the implementation commit, update only the build state as explicitly requested.

## Boundary Statement

Historical proof begins after the local diagnostics foundation, and this plan starts only the local preflight validation layer for caller-provided historical outcome proof rows.

This plan does not start controlled shadow data, live data, watcher loops, alerts, generated logs/reports, broker/order execution, option P&L, account sizing, production work, optimization, or live trade decisions. Controlled shadow data remains future work and is not started by this plan. Live data remains later and is not started by this plan. Viability proof remains the highest priority.
