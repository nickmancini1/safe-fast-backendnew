# SAFE-FAST Day 41 QQQ CFB contract selection decision task

Baseline:
- Latest commit before this task: 869d0ef Record QQQ CFB selected contract policy blocker

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Decide the first usable QQQ Clean Fast Break contract-selection rule for testing.
- Do not select a real trade for execution.
- Do not backtest.
- Do not calculate P&L.
- Do not fill evidence.
- Do not claim proof or profitability.
- Do not mark QQQ ready.

Current blocker:
- QQQ has Databento option data and a reviewed option universe policy.
- SAFE-FAST still lacks the exact rule for side, expiration, strike/moneyness, ranking, spread threshold, liquidity threshold, and statistics timestamp handling.

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_TRADE_PLAN_COMPLETENESS_GATE.md
- SAFE_FAST_DAY41_QQQ_CFB_SELECTED_CONTRACT_POLICY.md
- SAFE_FAST_DAY41_QQQ_CFB_SELECTED_CONTRACT_POLICY_DECISION_NEEDED.md
- SAFE_FAST_DAY41_DATABENTO_QQQ_DOWNLOAD_VALIDATION.md
- SAFE_FAST_DAY41_DATABENTO_QQQ_EVIDENCE_FIELD_MAPPING.md
- SAFE_FAST_DAY41_DATABENTO_QQQ_OPRA_NORMALIZER_REVIEW.md
- historical_signal_replay/databento_opra_normalizer.py
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md

Task:
1. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTION_DECISION.md
2. Decide the first conservative test rule for:
   - call/put side
   - expiration choice
   - strike choice
   - moneyness preference
   - one-contract ranking
   - maximum spread
   - minimum volume/open-interest
   - quote timestamp rule
   - statistics timestamp rule
   - missing-data behavior
   - rejected-contract behavior
3. If repo evidence cannot honestly support any part, create:
   - SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTION_DECISION_STILL_BLOCKED.md
   and name the exact human decision needed.
4. Do not invent a profitable contract.
5. Do not use future data.
6. Do not infer fills, P&L, proof, or readiness.
7. Define exact regression cases needed next.
8. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - SAFE_FAST_BUILD_STATE.md
9. Run:
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1

Allowed writes:
- SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTION_DECISION_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTION_DECISION.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTION_DECISION_STILL_BLOCKED.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
- SAFE_FAST_BUILD_STATE.md

Do not write:
- evidence fills
- calculator code
- backtest code
- trade-selection code
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
