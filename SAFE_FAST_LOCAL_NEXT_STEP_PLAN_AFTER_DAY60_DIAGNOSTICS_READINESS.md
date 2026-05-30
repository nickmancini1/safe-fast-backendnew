# SAFE-FAST Local Next-Step Plan After Day 60 Diagnostics Readiness

## Baseline

- **Baseline:** patch8
- **Repo:** `safe-fast-backendnew`
- **Branch:** `main`
- **Day context:** Day 28
- **Latest completed code milestone:** `db48832 Add Day 60 diagnostics readiness evaluator`
- **Latest pushed state before this plan:** `e977830 Sync build state after Day 28 recovery addendum`

## Current Proven Foundation

- The local-only Day 60 shadow watcher input-contract preflight validator is implemented and committed.
- The local-only Day 60 shadow session dry-run adapter is implemented and committed.
- The local-only Day 60 shadow review/diagnostics packet builder is implemented and committed.
- The local-only Day 60 diagnostics readiness evaluator is implemented and committed.
- The Day 28 recovery addendum is implemented and synced.
- In-depth diagnostics and whole-system optimization requirements are preserved.
- Current proof remains local, in-memory, and bounded to watcher-foundation review mechanics.
- Current proof does not include controlled shadow data, live data, generated reports/logs, alerts, broker/order execution, option P&L, account sizing, production readiness, or live trade decisions.

## Still Not Proven / No-Go Boundaries

- Day 60 shadow watcher viability is not proven.
- Trading-plan viability proof is not complete.
- Viability proof still requires future outcome evidence.
- Outcome scoring is not yet contract-validated.
- Diagnostic usefulness is not proven by real reviewed outcomes.
- Controlled shadow data remains future work and is not started by this plan.
- Live data readiness is not proven and is not started by this plan.
- Production readiness is not proven.
- Broker/order execution is not proven and remains forbidden.
- Option P&L and account sizing are not proven and remain forbidden.
- Live trade readiness and live trade decisions remain forbidden.

## Active Objective

Create exactly one next local-only implementation step:

**A local-only in-memory Day 60 outcome scoring contract validator.**

The future validator should accept caller-provided in-memory outcome-review rows only, validate the fields and boundaries needed for viability proof review, reject fabricated or forbidden proof fields, and return in-memory validation results only.

## Allowed Next Implementation Step

The next implementation may add only the local-only in-memory Day 60 outcome scoring contract validator.

Required behavior:

- Accept caller-provided in-memory outcome-review rows only.
- Validate required viability proof fields.
- Validate no-hindsight outcome review boundaries.
- Preserve missing or unavailable fields explicitly.
- Reject fabricated proof values.
- Reject broker/order/account/options/P&L/trade-decision fields.
- Return in-memory validation results only.
- Write no files, logs, reports, artifacts, exports, or generated output.
- Fetch no data and read no live sources.
- Start no live data.
- Create no watcher loops, schedulers, daemons, polling, background workers, or alert delivery.
- Send no alerts.
- Touch no broker/order/account/options/P&L systems.
- Make no live trade decisions.

## Exact Allowed Files For The Next Implementation Step

- `watcher_foundation/day60_outcome_scoring_contract.py`
- `watcher_foundation/__init__.py`
- `tests/test_day60_outcome_scoring_contract.py`
- `SAFE_FAST_BUILD_STATE.md`

No other files are allowed for the next implementation step unless the user explicitly expands scope.

## Exact Forbidden Files / Systems

- `main.py`
- Trading engine logic
- Railway files
- Deploy/production configuration
- Secrets, `.env`, credentials, tokens, keys, or account settings
- Live backend or live data startup code
- Watcher loops, schedulers, polling loops, daemons, or background workers
- Alert delivery systems
- Generated logs, generated reports, exports, artifacts, or output directories
- Broker/order/account systems
- Options, option P&L, account sizing, position sizing, or trade execution systems
- Live trade decision logic

## Required Tests

Add focused local unit tests for the outcome scoring contract validator covering:

- A complete caller-provided in-memory outcome-review row returns in-memory validation results.
- Required viability proof fields are enforced.
- Missing or unavailable viability proof fields remain explicit and are not fabricated.
- No-hindsight outcome review boundary fields are enforced.
- Fabricated proof values are rejected.
- Broker/order/account/options/P&L/trade-decision fields are rejected.
- Multiple in-memory rows return row-level validation results without writing files/logs/reports.
- The validator fetches no data, starts no live data, creates no watcher loops, sends no alerts, touches no broker/order/account/options/P&L systems, and makes no live trade decisions.

Required validation commands for that future implementation:

- `python -m unittest discover -s tests -p test_day60_outcome_scoring_contract.py`
- `python -m unittest discover -s tests -p test_day60_shadow_readiness.py`
- `python -m unittest discover -s tests -p test_day60_shadow_review_packet.py`
- `python -m unittest discover -s tests -p test_day60_shadow_session.py`
- `python -m unittest discover -s tests -p test_day60_shadow_contract.py`
- `git diff --check`

## Required Doc / Build-State Updates

The next implementation must update `SAFE_FAST_BUILD_STATE.md` in the same implementation change with:

- status of the local-only in-memory Day 60 outcome scoring contract validator
- baseline `patch8`
- implementation file and test file
- focused test result
- relevant regression test results
- `git diff --check` result
- preserved scope/no-go boundaries
- next objective after the validator

Do not create another standalone build-state sync after a sync. If commit hash/status wording is stale after the implementation commit, update only the build state as explicitly requested.

## Diagnostics And Optimization Boundary

In-depth diagnostics are required before optimization.

Whole-system optimization must be evidence-backed and regression-tested. No rule, contract, ranking, trigger, invalidation, freshness, duplicate-suppression, or user-facing workflow change may be promoted without outcome evidence, diagnosed failure category, targeted fix path, regression coverage, and preserved no-trade boundaries.

## Boundary Statement

This plan does not start controlled shadow data, live data, watcher loops, alerts, generated logs/reports, broker/order execution, option P&L, account sizing, production work, or live trade decisions. Controlled shadow data remains future work and is not started by this plan.
