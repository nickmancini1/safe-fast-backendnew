# SAFE-FAST Day 45 CFB Backtest-Prep Implementation Task

Baseline:
- Previous exact-values package: `SAFE_FAST_DAY45_CFB_EXACT_TRADE_RULE_VALUES.md`.

First action:
- Read `SAFE_FAST_BUILD_STATE.md`.
- Then read `SAFE_FAST_PROJECT_DASHBOARD.md`.
- Then read `SAFE_FAST_PROJECT_RULE_INDEX.md`.
- Then read `SAFE_FAST_DAY45_CFB_EXACT_TRADE_RULE_VALUES.md`.
- Then read `SAFE_FAST_DAY45_CFB_EXACT_TRADE_RULE_VALUES_REVIEW.md`.
- Then read `historical_signal_replay/fixtures/cfb_exit_stop_cost_regression_fixtures.json`.

Goal:
- Implement grouped Clean Fast Break trade-rule checker updates and tests for the accepted exact values.
- Prepare the first backtest-prep harness structure only if all required values remain accepted.
- Do not download data.
- Do not run a backtest.
- Do not calculate P&L.
- Do not mark any candidate ready.

Reference candidates:
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`
- `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`

Required implementation coverage:
- Long-call-only entry gate.
- Setup, option-context, and execution-context pass requirement.
- Entry ask plus `0.02` slippage basis.
- Exit bid minus `0.02` slippage basis.
- Earliest exit among profit target, option premium stop, setup invalidation stop, and `15:45 ET` time exit.
- Profit target at `+25%` from slippage-adjusted entry.
- Option stop at `-15%` from slippage-adjusted entry.
- Setup invalidation stop using the accepted underlying invalidation.
- Zero-cost fill rejection.
- Named failure reason requirement.
- Sample-size promotion blocker below `20` valid completed CFB examples.
- Promotion blocker without positive expectancy review after costs.

Allowed writes:
- `historical_signal_replay/cfb_trade_rule_checker.py`
- `tests/test_cfb_trade_rule_checker.py`
- `historical_signal_replay/fixtures/cfb_exit_stop_cost_regression_fixtures.json`
- New focused backtest-prep harness files only if they do not run a backtest or calculate P&L.
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`
- `SAFE_FAST_BUILD_STATE.md`
- `historical_signal_replay/candidate_packets/`

Excluded writes:
- raw Databento files
- evidence fills
- P&L outputs
- generated backtest result reports
- `main.py`
- live/engine/broker/order/account/Railway files
- `.env` or secrets

Required checks:
- `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`
- `python -m unittest tests.test_cfb_trade_rule_checker`
- `python -m watcher_foundation.source_evidence_work_package_content_validator`
- `python -m watcher_foundation.source_evidence_package_to_intake_bridge`

Final response:
- Baseline:
- Fixed:
- Blocked:
- Next:
- Tests:
- Files changed:
