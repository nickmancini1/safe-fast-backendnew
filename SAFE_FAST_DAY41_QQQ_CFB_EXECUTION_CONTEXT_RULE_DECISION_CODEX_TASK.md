# SAFE-FAST Day 41 QQQ CFB execution context rule decision task

Baseline:
- Latest commit before this task: ebf7b99 Fill QQQ CFB option context with new contract OI exception

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Decide the first QQQ CFB execution context rule.
- Execution context means: was the selected option quote usable at the setup time?
- Do not fill evidence yet.
- Do not backtest.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark QQQ ready.

Known current QQQ state:
- gap_context_status = clean
- lifecycle/stale-spent status filled
- option_context_status = caution
- headline_context_status = unknown
- execution_context_status = unknown
- complete_caution_review_status = unknown

Known selected contract:
- QQQ 260427C00615000
- instrument_id: 1023411456
- expiration: 2026-04-27
- strike: 615 call
- signal time: 2026-04-13T12:30:00-04:00
- nearest setup-safe quote found: 2026-04-13T16:06:30.640301037Z
- bid 7.76
- ask 7.80
- spread 0.04
- setup-time trade volume 65
- option context became caution through the new-contract OI exception

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_TRADE_PLAN_COMPLETENESS_GATE.md
- SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_NEW_CONTRACT_OI_EVIDENCE_FILL_REVIEW.md
- SAFE_FAST_DAY41_QQQ_CFB_NEW_CONTRACT_OI_EXCEPTION_SELECTOR_REVIEW.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTION_DECISION.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md

Proposed conservative execution rule to assess:
- clean: quote at or before signal and quote age <= 60 seconds
- caution: quote at or before signal and quote age > 60 seconds but <= 5 minutes
- fail: quote age > 5 minutes, spread too wide, missing bid/ask, missing size, missing volume, or quote after signal
- unknown: missing source data or unresolved rule
- long-call fill basis for later testing: ask price only, but do not calculate P&L in this task
- no future quotes
- no fallback
- no fill/proof/profitability/readiness inference

Task:
1. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_EXECUTION_CONTEXT_RULE_DECISION.md
2. Decide whether to accept the proposed conservative rule.
3. If accepted, define:
   - execution_context_status values
   - quote age thresholds
   - bid/ask/spread requirements
   - size/volume requirements
   - fill basis for later testing
   - missing-data behavior
   - future-data rejection
   - expected QQQ result
   - regression fixtures needed next
4. If not accepted, create:
   - SAFE_FAST_DAY41_QQQ_CFB_EXECUTION_CONTEXT_RULE_STILL_BLOCKED.md
   and state the exact missing decision.
5. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - SAFE_FAST_BUILD_STATE.md
6. Run:
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1

Allowed writes:
- SAFE_FAST_DAY41_QQQ_CFB_EXECUTION_CONTEXT_RULE_DECISION_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_EXECUTION_CONTEXT_RULE_DECISION.md
- SAFE_FAST_DAY41_QQQ_CFB_EXECUTION_CONTEXT_RULE_STILL_BLOCKED.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
- SAFE_FAST_BUILD_STATE.md

Do not write:
- evidence fills
- calculator code
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
