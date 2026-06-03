# SAFE-FAST Local Next-Step Plan After Discretion Audit Inventory

## 1. Baseline and Day 31 Context

- **Baseline:** patch8.
- **Repo:** `safe-fast-backendnew`.
- **Branch:** `main`.
- **Current working day context:** Day 31.
- **Work mode:** SAFE-FAST build work only, not live trade chat.
- **Latest completed build milestone per build state:** `0d23423 Add post-handoff Day 31 discretion audit inventory addendum`.
- **Latest completed code milestone:** `660c334 Add discretion audit inventory validator`.
- **Latest checkpoint per intro:** `fc64232 Sync build state after post-handoff Day 31 addendum`.
- **Actual local HEAD observed for this planning task:** `0e4a0c0 Replace next chat intro block with Day 31 handoff instructions`.
- **Commit/status note:** build-state sync, handoff, and intro commits are bookkeeping/docs commits and may be Git HEAD without being a new completed build milestone.

## 2. Current Fixed Foundation

- Replay/regression foundation is complete.
- Shadow review/export bundle foundation is complete.
- Day 60 local input-contract validator is complete.
- Day 60 shadow session dry-run adapter is complete.
- Day 60 review/diagnostics packet builder is complete.
- Day 60 diagnostics readiness evaluator is complete.
- Day 60 outcome scoring contract validator is complete.
- Day 60 outcome scoring summary evaluator is complete.
- Day 60 outcome diagnostics evaluator is complete.
- Day 60 optimization readiness gate is complete.
- Historical outcome proof preflight validator is complete.
- Historical outcome proof summary evaluator is complete.
- Historical outcome diagnostics evaluator is complete.
- Historical optimization readiness gate is complete.
- Trading-plan discretion audit evaluator is complete.
- Discretion audit coverage evaluator is complete.
- Discretion audit inventory validator is complete.
- Strict Day 28 handoff package remains valid as historical handoff context.
- Post-handoff Day 31 discretion audit inventory addendum is complete and supersedes the strict Day 28 handoff for latest status/objective.

## 3. What Remains Unproven

- Final SAFE-FAST trading-plan viability is not proven.
- Actual historical success is not proven.
- Controlled shadow data has not started.
- Live data has not started.
- Alerts have not started.
- Generated logs/reports have not started.
- Trading success is not proven.
- Broker/order/account/options/P&L behavior remains forbidden.
- Account sizing remains forbidden.
- Production readiness is not proven.
- Railway/deploy readiness is not proven.
- Live backend readiness is not proven.
- Live trade readiness and live trade decisions remain forbidden.
- The inventory validator validates caller-provided inventory shape, but there is not yet a local bridge that converts accepted inventory items into discretion-audit evaluator input and optionally evaluates coverage readiness.

## 4. Active Objective

Create exactly one next bounded local-only implementation step after the discretion audit inventory validator:

**A local-only in-memory discretion audit inventory-to-audit/coverage bridge readiness gate.**

The future gate must connect the already implemented inventory validator, discretion audit evaluator, and discretion audit coverage evaluator without creating inventory, auditing repo files automatically, changing rules, optimizing, writing outputs, or touching any live/production/trading system.

## 5. Exact Next Implementation Step

Add a local-only in-memory bridge module that:

- Accepts caller-provided in-memory inventory items only.
- First runs the existing discretion audit inventory validator.
- Converts only accepted inventory items into existing discretion audit evaluator input.
- Does not invent, rewrite, or improve rule text.
- Preserves `item_id`, `area`, `source`, `text`, `rule_purpose`, `audit_readiness`, `unavailable_fields`, and `watch_only` boundaries.
- Supplies evaluator `review_context` from preserved inventory metadata rather than hidden inference; if a context value is unavailable, the bridge must mark it explicitly rather than inventing proof.
- Runs or prepares for the existing discretion audit evaluator and existing discretion audit coverage evaluator only when the validated input has enough accepted inventory items to do so under explicit watch-only boundaries.
- Returns one combined in-memory readiness/audit/coverage summary only.

The future step must not create actual rule inventory, scan repo files, audit hidden discretion in repo files automatically, change rules, optimize, write output files/logs/reports, fetch data, start live data or controlled shadow data, create watcher loops, send alerts, touch broker/order/account/options/P&L, touch account sizing, or make live trade decisions.

## 6. Required Future Behavior

- Validate input with `validate_discretion_audit_inventory` before any audit or coverage call.
- Keep rejected inventory items rejected and report their validation reasons in memory.
- Convert accepted items into existing `audit_trading_plan_discretion` item shape using only caller-provided accepted inventory values.
- Preserve the original inventory item fields in the combined summary.
- Preserve unavailable fields explicitly, including when they block audit or coverage confidence.
- Preserve `watch_only=True` and fail if any accepted item cannot maintain the watch-only boundary.
- Return readiness state for inventory validation, audit execution eligibility, coverage execution eligibility, and coverage completeness.
- Return existing audit and coverage summaries by value, defensively copied.
- Mark bridge output as local-only, in-memory, watch-only, no-trade, no-rule-change, no-optimization, no-file-write, no-live-data, no-controlled-shadow-data, no-alert, and no-broker.
- Avoid creating any new discretion rule text, trading rule text, trigger text, invalidation text, freshness text, blocker/caution text, ranking/focus text, outcome-scoring text, diagnostic text, or user-workflow text.
- Treat human discretion only as no-trade veto, review note, or safety pause.

## 7. Exact Allowed Files for the Future Implementation Step

- `watcher_foundation/discretion_audit_inventory_bridge.py`
- `watcher_foundation/__init__.py`
- `tests/test_discretion_audit_inventory_bridge.py`
- `SAFE_FAST_BUILD_STATE.md`

No other files are allowed for the future implementation step unless the user explicitly expands scope.

## 8. Exact Forbidden Files / Systems

- `main.py`
- Trading engine logic
- Railway/deploy files
- Production or live backend integration
- Existing frozen strict Day 28 handoff docs unless explicitly authorized
- Day 31 addendum unless explicitly authorized
- Next-chat intro block unless a clear repo-doc reason is identified first
- Generated output paths
- Report/log writers
- Live data startup
- Controlled shadow data startup
- Watcher loops, schedulers, polling, daemons, or background workers
- Alert delivery systems
- Broker/order/account/options/P&L systems
- Account sizing or position sizing systems
- Secrets, `.env`, credentials, tokens, keys, or deployment settings
- Any code path that can make live trade decisions

## 9. Required Tests for the Future Implementation Step

Add focused local unit tests in `tests/test_discretion_audit_inventory_bridge.py` covering:

- Accepts caller-provided in-memory inventory items only.
- Runs the existing inventory validator before audit conversion.
- Rejects invalid inventory through existing validator behavior.
- Converts only accepted inventory items into existing discretion audit evaluator input.
- Preserves `item_id`, `area`, `source`, `text`, `rule_purpose`, `audit_readiness`, `unavailable_fields`, and `watch_only`.
- Does not invent or rewrite rule text.
- Preserves unavailable fields explicitly in the combined summary.
- Runs or prepares for existing discretion audit evaluator output under watch-only boundaries.
- Runs or prepares for existing coverage evaluator output only when justified by valid audit output.
- Returns a combined in-memory readiness/audit/coverage summary only.
- Handles partial inventory coverage without claiming complete coverage.
- Identifies coverage gaps through existing coverage evaluator behavior.
- Preserves no-trade, no-rule-change, no-optimization, no-file-write, no-live-data, no-controlled-shadow-data, no-alert, and no-broker boundaries.
- Rejects broker/order/account/options/P&L/trade-decision fields through existing validator behavior.
- Does not scan repo files, fetch data, start threads, invoke subprocesses, or write files/logs/reports.

Required validation commands for that future implementation:

- `python -m unittest discover -s tests -p test_discretion_audit_inventory_bridge.py`
- `python -m unittest discover -s tests -p test_discretion_audit_inventory.py`
- `python -m unittest discover -s tests -p test_discretion_audit.py`
- `python -m unittest discover -s tests -p test_discretion_audit_coverage.py`
- `python -m unittest tests.test_watcher_foundation_scaffold`
- `git diff --check`

## 10. Required Doc / Build-State Updates for the Future Implementation Step

The future implementation must update `SAFE_FAST_BUILD_STATE.md` with:

- Implementation status for the local-only in-memory discretion audit inventory-to-audit/coverage bridge readiness gate.
- Baseline `patch8` and Day 31 context.
- Exact implementation file and test file.
- Focused test result.
- Inventory, audit, coverage, and watcher-foundation regression test results.
- `git diff --check` result.
- Preserved scope and no-go boundaries.
- Next local-only objective after the bridge gate.

Do not claim final viability, historical success, shadow/live readiness, production readiness, Railway readiness, live backend readiness, live trade readiness, or live trade decision readiness.

## 11. No-Go Boundaries

- No `main.py`.
- No engine logic.
- No Railway/deploy files.
- No production or live backend work.
- No live data.
- No controlled shadow data.
- No watcher loops.
- No alerts.
- No generated reports/logs.
- No broker/order/account/options/P&L.
- No account sizing.
- No live trade decisions.
- No secrets, `.env`, credentials, tokens, or deployment settings.
- No rule changes.
- No optimization.
- No hidden repo-file discretion audit automation.
- No actual rule inventory creation.

## 12. Viability Priority and Required Viability Loop

Viability proof is the highest priority.

Detection alone is not enough. A watcher alone is not enough. The bridge gate only helps make discretion-audit inputs reviewable before later evidence-backed viability work; it does not prove SAFE-FAST viability by itself.

Required viability loop:

detect -> score outcome -> diagnose deeply -> analyze whole system -> decide fix path -> adjust rule/contract/test -> run regression -> review again

Diagnostics must remain in-depth. Shallow labels like failed setup, bad alert, weak signal, or bad trade are not enough. Diagnostics must identify evidence, likely cause, affected setup type, affected symbol when available, affected stage, trigger/invalidation/freshness relationship, affected system area, and next fix path.

## 13. Discretion Rule

Human discretion may exist only as:

- no-trade veto
- review note
- safety pause

Human discretion must never:

- create a signal
- approve a trade
- override missing proof
- move triggers
- hide failures
- change outcome after the fact

Setup recognition, trigger, invalidation, fresh/stale/spent, blocker/caution, ranking/focus, outcome scoring, diagnostics, and user workflow should be rule-based.

## 14. Boundary Statement

This docs-only plan does not start code work, optimization, controlled shadow data, live data, watcher loops, alerts, generated reports/logs, broker/order/account/options/P&L, account sizing, production/Railway/live backend work, or live trade decisions.

This docs-only plan does not modify `main.py`, engine logic, watcher code, tests, Railway/deploy files, secrets, `.env` files, credentials, tokens, deployment settings, generated output paths, report/log writers, watcher loops, alert delivery, broker/order/account behavior, options behavior, option P&L, position sizing, account sizing, or live trade decision logic.
