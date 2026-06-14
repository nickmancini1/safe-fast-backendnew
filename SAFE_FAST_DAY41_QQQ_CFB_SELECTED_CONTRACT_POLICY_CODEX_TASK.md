# SAFE-FAST Day 41 QQQ CFB selected-contract policy task

Baseline:
- Latest commit before this task: 809bd5e Fill QQQ CFB context caution evidence

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Define the first QQQ Clean Fast Break selected-contract policy.
- Do not choose a real trade yet.
- Do not backtest.
- Do not calculate P&L.
- Do not fill evidence.
- Do not claim proof or profitability.
- Do not mark QQQ ready.

Why:
- Current QQQ context/caution status is unknown because SAFE-FAST has no selected option contract or reviewed option universe.
- Without a contract policy, option context and execution context cannot honestly become clean/caution/fail.

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_TRADE_PLAN_COMPLETENESS_GATE.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_MISSING_DECISIONS.md
- SAFE_FAST_DAY41_DATABENTO_QQQ_DOWNLOAD_VALIDATION.md
- SAFE_FAST_DAY41_DATABENTO_QQQ_EVIDENCE_FIELD_MAPPING.md
- SAFE_FAST_DAY41_DATABENTO_QQQ_OPRA_NORMALIZER_REVIEW.md
- historical_signal_replay/databento_opra_normalizer.py
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md

Task:
1. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_SELECTED_CONTRACT_POLICY.md
2. Define a conservative first policy for reviewed option universe and selected-contract eligibility.
3. Include:
   - call/put side rule, or state if still blocked
   - expiration selection rule
   - strike selection rule
   - moneyness/ATM/ITM/OTM rule
   - minimum bid/ask data requirement
   - maximum spread rule, or state if still blocked
   - minimum volume/open-interest rule, or state if still blocked
   - quote timestamp/no-hindsight rule
   - missing-data behavior
   - rejected-contract behavior
   - exact regression cases needed next
4. If repo evidence cannot support an honest policy, create:
   - SAFE_FAST_DAY41_QQQ_CFB_SELECTED_CONTRACT_POLICY_DECISION_NEEDED.md
   and name the exact human decision needed.
5. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - SAFE_FAST_BUILD_STATE.md
6. Run:
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1

Allowed writes:
- SAFE_FAST_DAY41_QQQ_CFB_SELECTED_CONTRACT_POLICY_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_SELECTED_CONTRACT_POLICY.md
- SAFE_FAST_DAY41_QQQ_CFB_SELECTED_CONTRACT_POLICY_DECISION_NEEDED.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
- SAFE_FAST_BUILD_STATE.md

Do not write:
- evidence fills
- calculator code
- backtest code
- actual trade-selection code
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
