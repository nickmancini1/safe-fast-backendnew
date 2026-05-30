# SAFE-FAST Local Next-Step Plan After Day 60 Outcome Scoring Summary

## Baseline

- **Baseline:** patch8
- **Repo:** `safe-fast-backendnew`
- **Branch:** `main`
- **Day context:** Day 28
- **Latest completed code milestone:** `6702565 Add Day 60 outcome scoring summary evaluator`
- **Latest build-state sync after outcome scoring summary evaluator:** `5551444 Sync build state after Day 60 outcome scoring summary evaluator`

## Current Proven Foundation

- The local-only Day 60 shadow watcher input-contract preflight validator is implemented and committed.
- The local-only Day 60 shadow session dry-run adapter is implemented and committed.
- The local-only Day 60 shadow review/diagnostics packet builder is implemented and committed.
- The local-only Day 60 diagnostics readiness evaluator is implemented and committed.
- The local-only Day 60 outcome scoring contract validator is implemented, committed, and tested.
- The local-only Day 60 outcome scoring summary evaluator is implemented, committed, tested, and synced.
- The outcome scoring summary evaluator accepts caller-provided in-memory outcome-review rows only, validates them through the existing contract validator, and returns in-memory accepted rows, rejected rows with reasons, bucket counts, and unavailable outcome field summaries only.
- Current proof remains local, in-memory, and bounded to watcher-foundation review mechanics.

## Still Not Proven / No-Go Boundaries

- Day 60 shadow watcher viability is not proven.
- Trading-plan final viability is not proven.
- This diagnostics step will not prove final viability yet.
- Diagnostic usefulness against real reviewed outcomes is not proven.
- Controlled shadow data remains future work and is not started by this plan.
- Live data readiness is not proven and is not started by this plan.
- Production readiness is not proven.
- Broker/order execution is not proven and remains forbidden.
- Option P&L and account sizing are not proven and remain forbidden.
- Live trade readiness and live trade decisions remain forbidden.

## Active Objective

Create exactly one next local-only implementation step:

**A local-only in-memory Day 60 outcome diagnostics evaluator.**

The future evaluator should accept the in-memory outcome scoring summary and return an in-memory diagnostics summary only. It must move the build toward in-depth diagnostics before any optimization.

## Allowed Next Implementation Step

The next implementation may add only the local-only in-memory Day 60 outcome diagnostics evaluator.

Required behavior:

- Accept the in-memory outcome scoring summary only.
- Identify diagnostic failure categories.
- Preserve the evidence used for each diagnostic finding.
- Preserve affected setup type when available.
- Preserve affected symbol when available.
- Preserve affected stage when available.
- Preserve trigger, invalidation, and freshness relationship when available.
- Preserve missing or unavailable evidence explicitly.
- Produce likely cause candidates without fabricating facts.
- Map each diagnostic gap to a next fix path.
- Return an in-memory diagnostics summary only.
- Not optimize yet.
- Write no files, logs, reports, artifacts, exports, or generated output.
- Fetch no data and read no live sources.
- Start no live data.
- Create no watcher loops, schedulers, daemons, polling, background workers, or alert delivery.
- Send no alerts.
- Touch no broker/order/account/options/P&L systems.
- Make no live trade decisions.

## Exact Allowed Files For The Next Implementation Step

- `watcher_foundation/day60_outcome_diagnostics.py`
- `watcher_foundation/__init__.py`
- `tests/test_day60_outcome_diagnostics.py`
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
- Optimization changes to rules, contracts, ranking, triggers, invalidation, freshness, duplicate suppression, alert workflow, or user-facing workflow

## Required Tests

Add focused local unit tests for the outcome diagnostics evaluator covering:

- The evaluator accepts the in-memory outcome scoring summary only.
- Diagnostic failure categories are identified from summary inputs without fabricating unavailable facts.
- Evidence used for each finding is preserved.
- Affected setup type, symbol, stage, and trigger/invalidation/freshness relationship are preserved when available.
- Missing or unavailable evidence remains explicit.
- Likely cause candidates are produced as candidates only, not asserted facts.
- Each diagnostic gap maps to a next fix path.
- The evaluator returns an in-memory diagnostics summary only.
- Optimization is not started.
- The evaluator writes no files/logs/reports and fetches no data.
- The evaluator starts no live data, creates no watcher loops, sends no alerts, touches no broker/order/account/options/P&L systems, and makes no live trade decisions.

Required validation commands for that future implementation:

- `python -m unittest discover -s tests -p test_day60_outcome_diagnostics.py`
- `python -m unittest discover -s tests -p test_day60_outcome_scoring_summary.py`
- `python -m unittest discover -s tests -p test_day60_outcome_scoring_contract.py`
- `python -m unittest discover -s tests -p test_day60_shadow_readiness.py`
- `python -m unittest discover -s tests -p test_day60_shadow_review_packet.py`
- `python -m unittest discover -s tests -p test_day60_shadow_session.py`
- `python -m unittest discover -s tests -p test_day60_shadow_contract.py`
- `git diff --check`

## Required Doc / Build-State Updates

The next implementation must update `SAFE_FAST_BUILD_STATE.md` in the same implementation change with:

- status of the local-only in-memory Day 60 outcome diagnostics evaluator
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

This diagnostics plan does not prove final viability yet.

This plan does not start controlled shadow data, live data, watcher loops, alerts, generated logs/reports, broker/order execution, option P&L, account sizing, production work, optimization, or live trade decisions. Controlled shadow data remains future work and is not started by this plan.
