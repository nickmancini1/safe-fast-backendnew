# SAFE-FAST Day 41 QQQ CFB context/caution rule task

Baseline:
- Latest commit before this task: f984e35 Fill QQQ CFB lifecycle evidence

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Define or identify the missing QQQ Clean Fast Break context/caution rule needed for the remaining evidence checks.
- Do not fill evidence yet.
- Do not backtest.
- Do not choose a trade.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark QQQ ready.

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_PROJECT_PROOF_PIPELINE.md
- SAFE_FAST_TRADE_PLAN_COMPLETENESS_GATE.md
- SAFE_FAST_DAY41_QQQ_CFB_RULE_DECISION_PACKAGE.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
- historical_signal_replay/source_data/richer_export_package_work/

Task:
1. Find the remaining failed QQQ CFB evidence requests after gap context and lifecycle passed.
2. Identify the exact context/caution fields still missing.
3. Search the repo for existing context/caution rules.
4. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_RULE.md
5. If existing repo evidence supports a rule, define:
   - complete context status
   - caution context status
   - required raw inputs
   - allowed timestamps
   - forbidden future data
   - missing-data behavior
   - exact regression cases needed next
6. If repo evidence does not support an honest rule, create:
   - SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_DECISION_NEEDED.md
   and name the exact missing decision.
7. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - SAFE_FAST_BUILD_STATE.md
8. Run:
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1

Allowed writes:
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_RULE_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_RULE.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_DECISION_NEEDED.md
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
