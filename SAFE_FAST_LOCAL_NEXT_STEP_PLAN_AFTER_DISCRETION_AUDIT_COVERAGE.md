# SAFE-FAST Local Next-Step Plan After Discretion Audit Coverage

## Baseline and Day Context

- **Baseline:** patch8.
- **Day context:** Day 28.
- **Work mode:** SAFE-FAST build work only, not live trade chat.

## Current Proven Foundation

- The local-only trading-plan discretion audit evaluator is implemented and committed.
- The local-only discretion audit coverage evaluator is implemented and synced.
- The current foundation can evaluate caller-provided in-memory audit summaries for coverage across SAFE-FAST trading-plan areas.
- The current foundation still returns in-memory results only and preserves no-trade, no-optimization, no-live-data, and no-broker boundaries.

## Still Not Proven / No-Go Boundaries

- Actual SAFE-FAST rule and contract descriptions have not yet been inventoried for audit readiness.
- Hidden discretion has not yet been audited in the actual rule and contract inventory.
- No trading rules have been changed.
- No optimization has started.
- No live data or controlled shadow data has started.
- No generated reports, logs, watcher loops, alerts, broker/order/account/options/P&L behavior, or live trade decisions are allowed.
- Viability proof remains the highest priority.

## Active Objective

Create exactly one next local-only implementation step:

**Local-only in-memory SAFE-FAST discretion audit rule-inventory preflight validator.**

The validator must prepare caller-provided rule and contract inventory items for later discretion audit coverage without auditing yet.

## Required Future Validator Behavior

- Accept caller-provided in-memory rule/contract inventory items only.
- Validate that each item has `area`, `source`, `text`, `rule_purpose`, and `audit_readiness` fields.
- Require each item to map to one SAFE-FAST trading-plan area: `setup recognition`, `trigger`, `invalidation`, `fresh/stale/spent`, `blocker/caution`, `ranking/focus`, `outcome scoring`, `diagnostics`, or `user workflow`.
- Preserve unavailable fields explicitly.
- Reject broker/order/account/options/P&L/trade-decision fields.
- Return in-memory validation results only.
- Not audit yet.
- Not change trading rules.
- Not optimize.
- Write no files, logs, or reports.
- Fetch no data.
- Start no live data or controlled shadow data.
- Create no watcher loops.
- Send no alerts.
- Touch no broker/order/account/options/P&L.
- Make no live trade decisions.

## Exact Allowed Files for the Next Implementation Step

- `watcher_foundation/discretion_audit_inventory.py`
- `watcher_foundation/__init__.py`
- `tests/test_discretion_audit_inventory.py`
- `SAFE_FAST_BUILD_STATE.md`

## Exact Forbidden Files / Systems

- `main.py`
- Trading engine logic
- Railway/deploy files
- Production or live backend integration
- Generated output paths
- Report/log writers
- Live data startup
- Controlled shadow data startup
- Watcher loops, schedulers, polling, or background workers
- Alert delivery systems
- Broker/order/account/options/P&L systems
- Secrets, `.env`, credentials, or deployment settings
- Any code path that can make live trade decisions

## Required Tests

- Add focused unit tests in `tests/test_discretion_audit_inventory.py`.
- Required coverage:
  - accepts valid caller-provided in-memory inventory items
  - requires `area`, `source`, `text`, `rule_purpose`, and `audit_readiness`
  - requires area mapping to one allowed SAFE-FAST trading-plan area
  - preserves unavailable fields explicitly
  - rejects broker/order/account/options/P&L/trade-decision fields
  - returns in-memory validation results only
  - does not audit hidden discretion yet
  - does not write files/logs/reports or fetch data
- Run the focused test file.
- Run the watcher foundation scaffold/import regression if `watcher_foundation/__init__.py` changes.
- Run `git diff --check`.

## Required Doc / Build-State Updates

- Update `SAFE_FAST_BUILD_STATE.md` with the implementation status.
- Record baseline `patch8`.
- Record allowed implementation files and test file.
- Record focused test results.
- Record `git diff --check` result.
- Preserve the no-go scope: no `main.py`, no engine logic, no live data, no controlled shadow data, no watcher loops, no alerts, no generated reports/logs, no broker/order/account/options/P&L, no live trade decisions, and no secrets/.env/credentials/deploy settings.

## Rule and Optimization Boundary

- This plan does not start optimization.
- This plan does not change rules yet.
- Future rule changes require evidence, a diagnosed failure category, a targeted fix path, and regression tests before implementation.
- Viability proof remains the highest priority.

