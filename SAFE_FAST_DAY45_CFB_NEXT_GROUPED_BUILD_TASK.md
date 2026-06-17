# SAFE-FAST Day 45 CFB Next Grouped Build Task

Baseline:
- Current task package: `SAFE_FAST_DAY45_CFB_EXIT_STOP_COST_RULE_PACKAGE.md`.

First action:
- Read `SAFE_FAST_BUILD_STATE.md`.
- Then read `SAFE_FAST_PROJECT_DASHBOARD.md`.
- Then read `SAFE_FAST_PROJECT_RULE_INDEX.md`.
- Then read `SAFE_FAST_DAY45_CFB_EXIT_STOP_COST_RULE_PACKAGE.md`.
- Then read `SAFE_FAST_DAY45_CFB_BACKTEST_GATE_DECISION.md`.

Goal:
- Convert the grouped CFB exit/stop/time/cost/sample/promotion package into accepted regression decisions only after the missing human choices are explicit.
- Keep batching across `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`, `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`, and `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Task:
1. Decide exact first-pass values for:
   - option exit basis;
   - stop/invalidation translation;
   - time exit/end-of-day/max-hold/expiration-proximity handling;
   - cost/slippage assumptions;
   - sample-size thresholds;
   - promotion criteria.
2. Add or update regression fixtures only after those choices are accepted.
3. Update the CFB trade-rule checker only if the fixture decisions require code support.
4. Run safe local tests.
5. Do not download data, backtest, calculate P&L, mark readiness, or change intake-ready status.

Allowed writes:
- CFB rule package docs.
- CFB fixture files.
- `historical_signal_replay/cfb_trade_rule_checker.py` only if explicitly required by accepted fixtures.
- Focused checker tests.
- Project dashboard, rule index, build state, and relevant CFB candidate packets.

Excluded writes:
- raw Databento files;
- evidence fills;
- backtest code;
- P&L files;
- `main.py`;
- live/engine/broker/order/account/Railway files;
- `.env` or secrets.

Final response:
Baseline:
Fixed:
Blocked:
Next:
Tests:
Files changed:
