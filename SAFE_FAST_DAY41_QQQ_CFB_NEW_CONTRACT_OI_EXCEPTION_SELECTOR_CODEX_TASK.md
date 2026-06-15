# SAFE-FAST Day 41 QQQ CFB new-contract OI exception selector task

Baseline:
- Latest commit before this task: fbaa6b6 Add QQQ CFB new contract OI exception fixtures

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Update the QQQ CFB contract selector to support the accepted new-contract OI exception.
- Keep the old contract-selection tests passing.
- Do not fill evidence.
- Do not backtest.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark QQQ ready.

Accepted new-contract OI exception:
- If selected contract was not listed on prior trading day, prior-day open interest is not required.
- Contract must be listed before signal.
- Quote must be setup-time-safe.
- Spread must pass accepted caps.
- Bid/ask size must pass.
- Setup-time trade volume must pass.
- No future data.
- No fallback.
- Result is caution, not clean, because open interest is unavailable.

Read:
- SAFE_FAST_DAY41_QQQ_CFB_NEW_CONTRACT_OI_EXCEPTION_RULE.md
- SAFE_FAST_DAY41_QQQ_CFB_NEW_CONTRACT_OI_EXCEPTION_FIXTURES_REVIEW.md
- historical_signal_replay/fixtures/qqq_cfb_new_contract_oi_exception_regression_fixtures.json
- SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTION_DECISION.md
- historical_signal_replay/fixtures/qqq_cfb_contract_selection_regression_fixtures.json
- historical_signal_replay/cfb_contract_selector.py
- tests/test_cfb_contract_selector.py
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md

Task:
1. Update:
   - historical_signal_replay/cfb_contract_selector.py
2. Update or add tests in:
   - tests/test_cfb_contract_selector.py
3. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_NEW_CONTRACT_OI_EXCEPTION_SELECTOR_REVIEW.md
4. Selector must:
   - keep all original 18 contract-selection fixtures passing
   - pass all 13 new-contract OI exception fixtures
   - return caution for the valid new-contract OI exception case
   - still reject future data, missing quote, bad spread, bad size, low volume, and fallback
   - still reject contracts that existed prior day but lack required OI
   - not infer fills, P&L, proof, profitability, or readiness
5. Run:
   - python -m unittest tests.test_cfb_contract_selector
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1
6. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - SAFE_FAST_BUILD_STATE.md

Allowed writes:
- SAFE_FAST_DAY41_QQQ_CFB_NEW_CONTRACT_OI_EXCEPTION_SELECTOR_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_NEW_CONTRACT_OI_EXCEPTION_SELECTOR_REVIEW.md
- historical_signal_replay/cfb_contract_selector.py
- tests/test_cfb_contract_selector.py
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
- SAFE_FAST_BUILD_STATE.md

Do not write:
- evidence fills
- backtest code
- P&L
- raw Databento files
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
