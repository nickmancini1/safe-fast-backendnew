# SAFE-FAST Day 41 QQQ CFB context/caution decision task

Baseline:
- Latest commit before this task: 5dec718 Record QQQ CFB context caution decision needed

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Decide the first usable QQQ Clean Fast Break context/caution label rules.
- Keep rules explicit, conservative, and testable.
- Do not fill evidence.
- Do not backtest.
- Do not choose a trade.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark QQQ ready.

Fields to define:
- option_context_status
- headline_context_status
- execution_context_status
- complete_caution_review_status

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_RULE.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_DECISION_NEEDED.md
- SAFE_FAST_DAY41_QQQ_CFB_RULE_DECISION_PACKAGE.md
- SAFE_FAST_DAY41_DATABENTO_QQQ_DOWNLOAD_VALIDATION.md
- SAFE_FAST_DAY41_DATABENTO_QQQ_EVIDENCE_FIELD_MAPPING.md
- SAFE_FAST_DAY41_DATABENTO_QQQ_OPRA_NORMALIZER_REVIEW.md
- SAFE_FAST_TRADE_PLAN_COMPLETENESS_GATE.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
- historical_signal_replay/source_data/richer_export_package_work/

Task:
1. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_DECISION.md
2. Define first accepted testable rules for:
   - option_context_status
   - headline_context_status
   - execution_context_status
   - complete_caution_review_status
3. For each rule, define:
   - allowed statuses
   - required raw inputs
   - allowed timestamps
   - forbidden future data
   - missing-data behavior
   - caution behavior
   - fail behavior
   - unknown behavior
   - exact regression fixture cases needed next
4. If any rule cannot be honestly decided from repo evidence, create:
   - SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_DECISION_STILL_BLOCKED.md
   and name the exact missing human decision.
5. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - SAFE_FAST_BUILD_STATE.md
6. Run:
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1

Allowed writes:
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_DECISION_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_DECISION.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_DECISION_STILL_BLOCKED.md
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
