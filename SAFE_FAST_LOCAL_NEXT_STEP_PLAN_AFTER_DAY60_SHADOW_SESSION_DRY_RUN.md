# SAFE-FAST Local Next-Step Plan After Day 60 Shadow Session Dry-Run

## Baseline

- Baseline: patch8.
- Repo: `safe-fast-backendnew`.
- Branch context: `main`.
- Current date context: Day 27, with 33 days remaining to Day 60.
- Current dry-run adapter milestone: `eb84a4f Add Day 60 shadow session dry-run adapter`.
- Current build-state sync after dry-run adapter: `d56107f Sync build state after Day 60 shadow session dry-run adapter`.
- This plan is local-only and docs-only. It does not create another standalone build-state sync after a sync.

## Current Proven Foundation

- The local-only Day 60 shadow watcher input-contract validator is implemented and committed.
- The local-only Day 60 shadow session dry-run adapter is implemented and committed.
- The dry-run adapter accepts caller-provided in-memory rows already shaped for the Day 60 shadow contract.
- The dry-run adapter validates rows through the local Day 60 shadow contract validator.
- The dry-run adapter returns in-memory dry-run session summaries only.
- The dry-run adapter preserves accepted row copies, rejected row reasons, session-level counts, optional caller-provided session metadata, and explicit watch-only/no-trade/no-live-data/no-alert/no-file/no-broker flags.
- Existing Day 60 shadow work remains bounded to local, caller-provided, in-memory review behavior.

## Still-Not-Proven / No-Go Boundaries

- Day 60 shadow watcher viability is not proven.
- Diagnostics usefulness is not proven.
- Review-ready diagnostics are not proven.
- Future outcome scoring is not proven.
- Viability-review workflow usefulness is not proven.
- Controlled shadow data is not collected, generated, fetched, or started by this plan.
- Live data readiness is not proven.
- Watcher loops, schedulers, alert delivery, generated logs/reports, production service behavior, and live backend readiness are not proven.
- Broker/order execution, account sizing, option P&L, auto-trading, and live trade decision behavior are not proven and remain forbidden.
- Production, Railway, deployment, secret, credential, and `.env` readiness are not proven and remain forbidden.

## Active Objective

Define exactly one next safe local-only implementation step after the Day 60 shadow session dry-run adapter that moves toward Day 60 viability review and diagnostics without starting live data, watcher loops, alerts, generated logs/reports, broker/order execution, option P&L, account sizing, production behavior, or live trade decisions.

## Recommended Next Local-Only Implementation Step

Implement a local-only in-memory Day 60 shadow review/diagnostics packet builder.

The builder should accept the dry-run adapter result and return an in-memory review packet only. It should preserve accepted and rejected row summaries, preserve the no-trade/no-live/no-alert/no-file/no-broker flags, add review-ready diagnostic placeholders, add future outcome-scoring placeholders, and add viability-review placeholders.

This is the only recommended next implementation step.

The builder must not write files, logs, or reports. It must not fetch data, start live data, create watcher loops, send alerts, touch broker/order/account/options/P&L systems, or make live trade decisions.

## Exact Allowed Files For The Next Implementation Step

- `watcher_foundation/day60_shadow_review_packet.py`
- `watcher_foundation/__init__.py`
- `tests/test_day60_shadow_review_packet.py`
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

- `python -m unittest discover -s tests -p test_day60_shadow_review_packet.py`

Run the existing dry-run adapter tests:

- `python -m unittest discover -s tests -p test_day60_shadow_session.py`

Run the existing validator tests:

- `python -m unittest discover -s tests -p test_day60_shadow_contract.py`

Run the focused watcher regression set if shared watcher exports or shared helpers are touched:

- `python -m unittest tests.test_watcher_foundation_scaffold tests.test_watcher_state_tracking tests.test_trigger_card_projection tests.test_shadow_log_writer tests.test_duplicate_suppression_runtime tests.test_focus_ranking_runtime tests.test_diagnostics_runtime tests.test_headline_news_policy_placeholder tests.test_watcher_pipeline_integration tests.test_watcher_pipeline_sequence_regression tests.test_watcher_batch_runner tests.test_watcher_fixture_regression_pack tests.test_day60_shadow_contract tests.test_day60_shadow_session tests.test_day60_shadow_review_packet`

Always run:

- `git diff --check`

The tests must verify that the review/diagnostics packet builder accepts only an in-memory dry-run adapter result, preserves accepted and rejected row summaries, preserves no-trade/no-live/no-alert/no-file/no-broker flags, adds review-ready diagnostic placeholders, adds future outcome-scoring placeholders, adds viability-review placeholders, returns an in-memory packet only, and has no file/network/subprocess/live-data side effects.

## Required Doc / Build-State Updates After The Next Implementation Step

Update `SAFE_FAST_BUILD_STATE.md` with:

- Status of the local-only in-memory Day 60 shadow review/diagnostics packet builder.
- Baseline: patch8.
- Exact implementation files changed.
- Exact test files changed.
- Exact test commands and results.
- Scope preserved wording confirming no `main.py`, no engine logic, no live data, no watcher loops, no alerts, no generated reports/logs, no production/deploy changes, no broker/order/account/options/P&L behavior, no live trade decisions, and no secrets/.env/credentials/deployment settings.
- Next objective after user review/commit.

Do not create a build-state-only sync after a sync. The implementation step should receive a normal milestone commit if the user reviews and approves it.

## Viability Proof And Diagnostics Remain Required Later

The next implementation step does not prove Day 60 watcher viability and does not prove diagnostics usefulness. Viability proof and diagnostics proof remain required later after the local-only review packet shape, controlled shadow data boundaries, and future review workflow are explicitly authorized, implemented, and reviewed.

## Controlled Shadow Data Remains Future Work

Controlled shadow data remains future work and is not started by this plan. This plan does not authorize data collection, data fetching, live source reads, generated logs/reports, watcher loops, alerts, production behavior, or live trade decisions.
