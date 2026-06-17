# SAFE-FAST Day 45 CFB Next Grouped Implementation Task

Baseline:
- Latest task before this file: `SAFE_FAST_DAY45_CFB_GROUPED_TRADE_RULE_PACKAGE_CODEX_TASK.md`.

First action:
- Read `SAFE_FAST_BUILD_STATE.md`.
- Read `SAFE_FAST_PROJECT_DASHBOARD.md`.
- Read `SAFE_FAST_PROJECT_RULE_INDEX.md`.
- Read `SAFE_FAST_DAY45_CFB_GROUPED_TRADE_RULE_PACKAGE.md`.
- Read `SAFE_FAST_DAY45_CFB_BACKTEST_PREP_READINESS_REVIEW.md`.
- Read `historical_signal_replay/fixtures/cfb_trade_rule_regression_fixtures.json`.

Goal:
- Implement the CFB trade-rule checker plus focused tests using the grouped fixture file.

Scope:
- Build a checker that evaluates the accepted first-pass trade-rule gates only.
- Use `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` as the usable reference fixture.
- Use `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` as the quote-after-signal no-trade fixture.
- Use `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` as the stale-quote failed-execution fixture.
- Preserve blocker outputs for missing exit, stop/invalidation, cost/slippage, sample-size, and promotion gates.
- Keep failure labels named and explicit.

Required tests:
- SPY CFB 002 reaches `blocked_pre_backtest` because exit/cost/sample/promotion decisions are still missing, not because entry evidence is unusable.
- SPY CFB 003 returns `no_trade` with `quote_after_signal`.
- QQQ CFB 001 returns `no_trade` with `quote_age_above_5_minutes`.
- Missing selected contract blocks entry.
- Missing entry quote blocks entry.
- Missing exit rule blocks countable results.
- Missing invalidation blocks entry.
- Missing cost/slippage blocks countable results.
- Missing failure diagnosis blocks known blockers.
- Missing sample-size gate blocks promotion.
- Missing promotion gate blocks readiness.
- Forbidden P&L/proof/profitability/readiness fields cannot improve status.

Allowed writes:
- New checker module under `historical_signal_replay/` if needed.
- Focused tests under `tests/`.
- Existing fixture file only if a bug is found in fixture shape.
- Project dashboard, rule index, build state, and candidate packets for status updates.

Excluded writes:
- Raw Databento files.
- Evidence fills.
- Backtest code or harness.
- P&L files.
- `main.py`.
- Live/engine/broker/order/account/Railway files.
- `.env` or secrets.

Stop condition:
- Stop after checker/tests/status docs are updated.
- Do not proceed to backtest-prep harness until the user explicitly authorizes it.

