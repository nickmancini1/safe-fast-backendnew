# SAFE-FAST Day 41 QQQ CFB contract selector task

Baseline:
- Latest commit before this task: 3115468 Add QQQ CFB contract selection fixtures

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Implement the QQQ CFB contract selector using the accepted contract-selection fixtures.
- Do not fill evidence.
- Do not backtest.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark QQQ ready.

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTION_DECISION.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTION_FIXTURES_REVIEW.md
- historical_signal_replay/fixtures/qqq_cfb_contract_selection_regression_fixtures.json
- historical_signal_replay/databento_opra_normalizer.py
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
- SAFE_FAST_TRADE_PLAN_COMPLETENESS_GATE.md

Accepted rule:
- side: long calls
- expiration: nearest reviewed expiration with DTE >= 14
- strike: lowest call strike >= 613.67
- moneyness: OTM-by-trigger
- spread cap: 0.15
- spread percent cap: 2.00%
- minimum bid size: 1
- minimum ask size: 1
- minimum trade volume: 1
- minimum open interest: 1
- quote timestamp: nearest at or before signal time
- statistics timestamp: strict no-hindsight
- missing data: abstain
- fallback: none

Task:
1. Create:
   - historical_signal_replay/cfb_contract_selector.py
2. Create:
   - tests/test_cfb_contract_selector.py
3. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTOR_REVIEW.md
4. The selector must:
   - apply the accepted rule exactly
   - select one eligible contract only when all requirements pass
   - abstain if no contract passes
   - reject wrong side
   - reject DTE below 14
   - reject strike below 613.67
   - reject spread above cap
   - reject spread percent above cap
   - reject missing bid/ask
   - reject insufficient bid/ask size
   - reject insufficient volume/open interest
   - reject quote/statistics after signal time
   - refuse fallback selection
   - refuse P&L/proof/readiness inference
5. Tests must use:
   - historical_signal_replay/fixtures/qqq_cfb_contract_selection_regression_fixtures.json
6. Tests must prove all 18 fixtures pass.
7. Run:
   - python -m unittest tests.test_cfb_contract_selector
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1
8. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - SAFE_FAST_BUILD_STATE.md

Allowed writes:
- SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTOR_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTOR_REVIEW.md
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
