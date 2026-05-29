# SAFE-FAST Local Next-Step Build Plan After Day 60 Diagnostics

## Baseline

- Baseline: patch8.
- Repo: `safe-fast-backendnew`.
- Branch context: `main`.
- This is a local-only build plan after the Day 60 watcher viability/diagnostics carry-forward.

## Current proven foundation

- Day 60 shadow watcher viability/diagnostics requirements are preserved in `SAFE_FAST_DAY60_SHADOW_WATCHER_VIABILITY_DIAGNOSTICS_REQUIREMENTS.md`.
- Watcher foundation closeout, replay/regression readiness, local replay/regression validation, shadow review labeling, shadow review sample pack, and shadow review/export bundle review-package work are already documented as completed at their accepted local-only depth.
- The current foundation supports local, caller-provided, in-memory watcher review workflows and documentation review.
- Existing local watcher foundation behavior remains bounded to watch-only interpretation and review support.
- Existing docs preserve the Day 60 target, viability proof requirement, diagnostics requirement, improvement-loop expectation, controlled shadow-data requirement, post-Day-60 $20-tier role, and firm-language boundaries for future chats.

## Still-not-proven / no-go boundaries

- Day 60 shadow watcher viability is not proven yet.
- Diagnostics usefulness is not proven yet.
- Controlled shadow data is not collected, generated, or started by this plan.
- No live data readiness is proven.
- No watcher loop, scheduler, alert delivery, production service, or live backend readiness is proven.
- No broker/order execution, account sizing, option P&L, auto-trading, or live trade decision behavior is proven or allowed.
- No production, Railway, deployment, secret, credential, or `.env` readiness is proven or allowed.

## Active objective

Define the next safe local-only build step toward the Day 60 shadow watcher target while preserving all no-go boundaries and avoiding any live data, loops, alerts, production behavior, broker/order execution, option P&L, account sizing, or live trade decisions.

## Recommended next local-only build step

Implement a local-only Day 60 shadow watcher input-contract preflight validator.

The validator should accept only caller-provided in-memory dictionaries representing future controlled shadow-session rows or batches. It should validate that the minimum required review fields, provenance fields, no-trade fields, diagnostics placeholders, and unavailable-field semantics are present before any future controlled shadow-data workflow is attempted.

The validator must not fetch data, create data, read live sources, run watcher loops, schedule recurring work, send alerts, write reports/logs, approve trades, calculate option P&L, size accounts, call brokers, or make live trade decisions.

This step is intentionally before controlled shadow data. It proves that future controlled shadow inputs can be checked locally for shape and boundary compliance before any shadow data collection begins.

## Exact allowed files for the next build step

- `watcher_foundation/day60_shadow_contract.py`
- `watcher_foundation/__init__.py`
- `tests/test_day60_shadow_contract.py`
- `SAFE_FAST_BUILD_STATE.md`

No other files should be changed during the next build step unless the user explicitly authorizes a narrower alternative before work begins.

## Exact forbidden files/systems

- `main.py`
- Existing engine logic
- Existing watcher loop or scheduler systems
- Railway files
- Deploy files
- Production files
- Live backend files
- Live data integrations
- Broker/order execution systems
- Account sizing systems
- Option P&L systems
- Alert delivery systems
- Generated report/log output paths
- Secrets
- `.env` files
- Credentials
- Deployment settings

The next step must not start live data, watcher loops, alerts, production behavior, broker/order execution, option P&L, account sizing, or live trade decisions.

## Required tests for the next build step

Run targeted local tests only:

- `python -m unittest discover -s tests -p test_day60_shadow_contract.py`

Run the focused watcher regression set only if the implementation touches shared watcher exports or shared helpers:

- `python -m unittest tests.test_watcher_foundation_scaffold tests.test_watcher_state_tracking tests.test_trigger_card_projection tests.test_shadow_log_writer tests.test_duplicate_suppression_runtime tests.test_focus_ranking_runtime tests.test_diagnostics_runtime tests.test_headline_news_policy_placeholder tests.test_watcher_pipeline_integration tests.test_watcher_pipeline_sequence_regression tests.test_watcher_batch_runner tests.test_watcher_fixture_regression_pack tests.test_day60_shadow_contract`

Always run:

- `git diff --check`

The tests must verify valid in-memory contract payloads, missing required fields, invalid field types, forbidden broker/order/account/option/P&L/trade-decision fields, unavailable-field semantics, diagnostics placeholder preservation, no-trade wording, and no file/network/subprocess/live-data side effects.

## Required doc/build-state updates after the next build step

Update `SAFE_FAST_BUILD_STATE.md` with:

- Status of the local-only Day 60 shadow watcher input-contract preflight validator.
- Baseline: patch8.
- Exact implementation files changed.
- Exact test files changed.
- Exact test commands and results.
- Scope preserved wording confirming no `main.py`, no engine logic, no watcher loops, no live data, no alerts, no generated reports/logs, no production/deploy changes, no broker/order/account/options/P&L behavior, no live trade decisions, and no secrets/.env/credentials/deployment settings.
- Next objective after user review/commit.

## Viability proof and diagnostics remain required later

The next build step does not prove Day 60 watcher viability and does not prove diagnostics usefulness. Viability proof and diagnostics proof remain required later, after the local contract and future controlled shadow workflow are explicitly authorized, implemented, and reviewed under local-only boundaries.

## Controlled shadow data remains future work

Controlled shadow data is future work and is not started by this planning task. This planning task creates only a docs-only next-step plan and a build-state update.
