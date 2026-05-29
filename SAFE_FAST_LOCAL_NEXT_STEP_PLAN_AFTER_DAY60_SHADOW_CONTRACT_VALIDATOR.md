# SAFE-FAST Local Next-Step Plan After Day 60 Shadow Contract Validator

## Baseline

- Baseline: patch8.
- Repo: `safe-fast-backendnew`.
- Branch context: `main`.
- Current date context: Day 27, with 33 days remaining to Day 60.
- Current validator commit: `40ddbc5 Add Day 60 shadow watcher input contract validator`.
- Current build-state sync: `c82b72c Sync build state after Day 60 shadow contract validator`.
- This plan is local-only and docs-only. It does not create another build-state sync after a sync.

## Current Proven Foundation

- The local-only Day 60 shadow watcher input-contract validator is implemented and committed.
- The validator accepts caller-provided in-memory Day 60 shadow contract rows and batches.
- The validator checks required contract fields, trigger-card shape, provenance, diagnostics placeholders, unavailable-field semantics, evidence references, no-hindsight boundaries, no-trade boundaries, and forbidden execution/trade fields.
- The validator returns defensive in-memory accepted-row copies and in-memory batch summaries.
- The existing watcher foundation remains bounded to local watch-only review behavior.
- The Day 60 viability, diagnostics, controlled shadow-data, and no-trade requirements remain preserved in project docs and build state.

## Still-Not-Proven / No-Go Boundaries

- Day 60 shadow watcher viability is not proven.
- Diagnostics usefulness is not proven.
- Controlled shadow data is not collected, generated, fetched, or started by this plan.
- Live data readiness is not proven.
- Watcher loop, scheduler, alert delivery, generated log/report, production service, and live backend readiness are not proven.
- Broker/order execution, account sizing, option P&L, auto-trading, and live trade decision behavior are not proven and remain forbidden.
- Production, Railway, deployment, secret, credential, and `.env` readiness are not proven and remain forbidden.

## Active Objective

Define exactly one next safe local-only implementation step after the Day 60 shadow contract validator that moves toward the Day 60 shadow watcher path without starting live data, watcher loops, alerts, generated logs/reports, broker/order execution, option P&L, account sizing, production behavior, or live trade decisions.

## Recommended Next Local-Only Implementation Step

Implement a local-only in-memory Day 60 shadow session dry-run adapter.

The adapter should accept only caller-provided rows that are already shaped for the Day 60 shadow contract. It should validate those rows with the existing Day 60 shadow contract validator and return an in-memory dry-run session summary only.

The adapter must preserve accepted and rejected row reasons from validation. It may add session-level counts and caller-provided session metadata, but it must not fetch data, create market data, start live data, create watcher loops, send alerts, write logs, write reports, touch broker/order/account/options/P&L systems, or make live trade decisions.

This is the only recommended next implementation step.

## Exact Allowed Files For The Next Implementation Step

- `watcher_foundation/day60_shadow_session.py`
- `watcher_foundation/__init__.py`
- `tests/test_day60_shadow_session.py`
- `SAFE_FAST_BUILD_STATE.md`

No other files should be changed during the next implementation step unless the user explicitly authorizes a narrower adjustment before work begins.

## Exact Forbidden Files / Systems

- `main.py`
- Existing trading engine logic
- Railway files
- Deploy files
- Production files
- Live backend files
- Live data integrations
- Source-data exporters or fetchers
- Watcher loop systems
- Scheduler systems
- Alert delivery systems
- Generated report paths
- Generated log paths
- Broker systems
- Order systems
- Account systems
- Account sizing systems
- Option P&L systems
- Secrets
- `.env` files
- Credentials
- Deployment settings

The next step must not start live data, watcher loops, alerts, generated logs/reports, production behavior, broker/order execution, option P&L, account sizing, or live trade decisions.

## Required Tests For The Next Implementation Step

Run targeted local tests:

- `python -m unittest discover -s tests -p test_day60_shadow_session.py`

Run the existing validator tests:

- `python -m unittest discover -s tests -p test_day60_shadow_contract.py`

Run the focused watcher regression set if shared watcher exports or shared helpers are touched:

- `python -m unittest tests.test_watcher_foundation_scaffold tests.test_watcher_state_tracking tests.test_trigger_card_projection tests.test_shadow_log_writer tests.test_duplicate_suppression_runtime tests.test_focus_ranking_runtime tests.test_diagnostics_runtime tests.test_headline_news_policy_placeholder tests.test_watcher_pipeline_integration tests.test_watcher_pipeline_sequence_regression tests.test_watcher_batch_runner tests.test_watcher_fixture_regression_pack tests.test_day60_shadow_contract tests.test_day60_shadow_session`

Always run:

- `git diff --check`

The tests must verify that the dry-run adapter accepts caller-provided contract-shaped rows, calls the Day 60 contract validator, returns an in-memory summary only, preserves accepted row copies, preserves rejected row reasons, preserves watch-only/no-trade boundaries, rejects invalid input through validator behavior, and has no file/network/subprocess/live-data side effects.

## Required Doc / Build-State Updates After The Next Implementation Step

Update `SAFE_FAST_BUILD_STATE.md` with:

- Status of the local-only in-memory Day 60 shadow session dry-run adapter.
- Baseline: patch8.
- Exact implementation files changed.
- Exact test files changed.
- Exact test commands and results.
- Scope preserved wording confirming no `main.py`, no engine logic, no live data, no watcher loops, no alerts, no generated reports/logs, no production/deploy changes, no broker/order/account/options/P&L behavior, no live trade decisions, and no secrets/.env/credentials/deployment settings.
- Next objective after user review/commit.

Do not create a build-state-only sync after a sync. The implementation step should receive a normal milestone commit if the user reviews and approves it.

## Viability Proof And Diagnostics Remain Required Later

The next implementation step does not prove Day 60 watcher viability and does not prove diagnostics usefulness. Viability proof and diagnostics proof remain required later after the local-only dry-run path, controlled shadow data boundaries, and future review workflow are explicitly authorized, implemented, and reviewed.

## Controlled Shadow Data Remains Future Work

Controlled shadow data remains future work and is not started by this plan. This plan does not authorize data collection, data fetching, live source reads, generated logs/reports, watcher loops, alerts, production behavior, or live trade decisions.
