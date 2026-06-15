# SAFE-FAST Day 41 QQQ CFB open-interest gate decision task

Baseline:
- Latest commit before this task: b6569f4 Rerun QQQ option context with trades statistics

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Decide how QQQ CFB option_context_status should handle missing setup-time-safe open interest.
- Do not fill evidence.
- Do not backtest.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark QQQ ready.

Known current result:
- Wider quotes fixed the quote blocker.
- New trades fixed the volume blocker.
- Top contract has setup-time trade volume 65.
- New statistics file has 0 rows.
- Same-contract setup-time-safe open interest is still missing.
- Current selector abstains because open interest is required and no fallback is allowed.

Top contract:
- QQQ 260427C00615000
- instrument_id: 1023411456
- expiration: 2026-04-27
- strike: 615 call
- DTE: 14
- signal time: 2026-04-13T12:30:00-04:00

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_TRADE_PLAN_COMPLETENESS_GATE.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTION_DECISION.md
- SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_RERUN_WITH_TRADES_STATS_REVIEW.md
- SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_RERUN_WITH_WIDER_QUOTES_REVIEW.md
- SAFE_FAST_DAY41_QQQ_CFB_TOP_CONTRACT_QUOTE_COVERAGE_AUDIT.md
- SAFE_FAST_DAY41_DATABENTO_QQQ_DOWNLOAD_VALIDATION.md
- SAFE_FAST_DAY41_DATABENTO_QQQ_EVIDENCE_FIELD_MAPPING.md
- historical_signal_replay/cfb_contract_selector.py
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md

Task:
1. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_OPEN_INTEREST_GATE_DECISION.md
2. Decide whether the first QQQ CFB option-context rule should:
   - keep same-contract setup-time-safe open interest required,
   - allow open_interest_status = unknown while still evaluating quote/spread/volume,
   - allow volume-only liquidity for regression,
   - or require another source before option_context_status can pass.
3. Do not fake open interest.
4. Do not use after-signal statistics.
5. Do not infer trade quality, fill, P&L, proof, profitability, or readiness.
6. If a rule change is accepted, define:
   - allowed statuses
   - required raw inputs
   - missing-open-interest behavior
   - how option_context_status should classify this QQQ case
   - exact regression fixture updates needed
   - exact selector changes needed
7. If no honest decision is supported, create:
   - SAFE_FAST_DAY41_QQQ_CFB_OPEN_INTEREST_GATE_STILL_BLOCKED.md
   and name the exact missing source or human decision.
8. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - SAFE_FAST_BUILD_STATE.md
9. Run:
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1

Allowed writes:
- SAFE_FAST_DAY41_QQQ_CFB_OPEN_INTEREST_GATE_DECISION_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_OPEN_INTEREST_GATE_DECISION.md
- SAFE_FAST_DAY41_QQQ_CFB_OPEN_INTEREST_GATE_STILL_BLOCKED.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
- SAFE_FAST_BUILD_STATE.md

Do not write:
- evidence fills
- selector code
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
