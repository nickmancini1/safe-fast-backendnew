# SAFE-FAST Day 41 SPY CFB lifecycle batch implement and fill task

Baseline:
- Latest commit before this task: 570f29c Add grouped SPY CFB lifecycle rule fixtures

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Batch implement/test SPY CFB lifecycle logic for both SPY CFB candidates.
- Fill only lifecycle/stale-spent/expiry evidence if calculator-backed and source-backed.
- Do not split into one task per candidate.
- Do not download more data.
- Do not backtest.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark any candidate ready.

Candidates:
- SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002
- SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003

Read:
- SAFE_FAST_DAY41_SPY_CFB_GROUPED_RULE_REGRESSION_PACKAGE.md
- historical_signal_replay/fixtures/spy_cfb_lifecycle_regression_fixtures.json
- historical_signal_replay/cfb_lifecycle_calculator.py if present
- tests/test_cfb_lifecycle_calculator.py if present
- historical_signal_replay/candidate_packets/SPY_REAL_HISTORICAL_CLEAN_FAST_BREAK_002.md
- historical_signal_replay/candidate_packets/SPY_REAL_HISTORICAL_CLEAN_FAST_BREAK_003.md
- historical_signal_replay/source_data/richer_export_package_work/

Task:
1. Reuse the existing lifecycle calculator if it can safely support SPY CFB.
2. If needed, extend it without breaking QQQ tests.
3. Add fixture-driven tests for both SPY CFB candidates.
4. Tests must prove all SPY lifecycle fixtures pass.
5. If tests pass, fill only SPY CFB lifecycle/stale-spent/expiry evidence fields that are directly supported.
6. Do not alter unrelated evidence fields.
7. If evidence rows cannot be safely found or mapped, stop with a review doc instead of guessing.
8. Create:
   - SAFE_FAST_DAY41_SPY_CFB_LIFECYCLE_BATCH_IMPLEMENT_AND_FILL_REVIEW.md
9. Update:
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_BUILD_STATE.md
   - both SPY CFB candidate packets
10. Run:
   - python -m unittest tests.test_cfb_lifecycle_calculator
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1
   - relevant content validator and bridge if safe/local

Allowed writes:
- SAFE_FAST_DAY41_SPY_CFB_LIFECYCLE_BATCH_IMPLEMENT_AND_FILL_CODEX_TASK.md
- SAFE_FAST_DAY41_SPY_CFB_LIFECYCLE_BATCH_IMPLEMENT_AND_FILL_REVIEW.md
- historical_signal_replay/cfb_lifecycle_calculator.py
- tests/test_cfb_lifecycle_calculator.py
- historical_signal_replay/source_data/richer_export_package_work/
- historical_signal_replay/candidate_packets/SPY_REAL_HISTORICAL_CLEAN_FAST_BREAK_002.md
- historical_signal_replay/candidate_packets/SPY_REAL_HISTORICAL_CLEAN_FAST_BREAK_003.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_BUILD_STATE.md

Do not write:
- raw Databento files
- unrelated evidence fields
- backtest code
- P&L
- main.py
- live/engine/broker/order/account/Railway files
- .env or secrets

Final response:
Baseline:
Fixed:
Blocked:
Next:
Tests:
Files changed:
