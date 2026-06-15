# SAFE-FAST Day 41 QQQ CFB new-contract open-interest exception rule task

Baseline:
- Latest commit before this task: 6befebd Audit QQQ CFB target contract listing open interest

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Decide a conservative rule for newly listed contracts where prior-day open interest cannot exist.
- Do not fill evidence.
- Do not backtest.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark QQQ ready.

Known facts:
- Target contract: QQQ 260427C00615000
- instrument_id: 1023411456
- Listed before setup: 2026-04-13T12:00:00.445628903Z
- Signal time: 2026-04-13T12:30:00-04:00
- Apr 10 parent definitions had 0 target matches.
- Setup-time quote exists.
- Setup-time trade volume exists: 65.
- Setup-time same-contract open interest does not exist.
- Current OI gate blocks option_context_status.

Proposed conservative rule to assess:
- If a selected contract was not listed on the prior trading day, prior-day open interest is not required.
- It must still have:
  - listed before signal,
  - setup-time-safe quote,
  - setup-time-safe spread within accepted caps,
  - setup-time trade volume >= accepted minimum,
  - no future data,
  - no fallback.
- Result should be caution, not clean, because open interest is unavailable.
- If any of those checks fail, result stays unknown or fail based on the accepted rule.
- This does not prove trade quality, fills, P&L, readiness, or profitability.

Read:
- SAFE_FAST_DAY41_QQQ_CFB_TARGET_CONTRACT_LISTING_OI_AUDIT.md
- SAFE_FAST_DAY41_QQQ_CFB_OPEN_INTEREST_GATE_DECISION.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTION_DECISION.md
- SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_RERUN_WITH_TRADES_STATS_REVIEW.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md

Task:
1. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_NEW_CONTRACT_OI_EXCEPTION_RULE.md
2. Decide whether to accept the proposed conservative new-contract OI exception.
3. If accepted, define:
   - allowed statuses
   - required raw inputs
   - listing-before-signal rule
   - prior-day-not-listed rule
   - quote/spread/volume requirements
   - missing-data behavior
   - no-fallback behavior
   - expected QQQ result
   - regression fixtures needed next
4. If not accepted, create:
   - SAFE_FAST_DAY41_QQQ_CFB_NEW_CONTRACT_OI_EXCEPTION_STILL_BLOCKED.md
   and state the exact missing human decision.
5. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - SAFE_FAST_BUILD_STATE.md
6. Run:
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1

Allowed writes:
- SAFE_FAST_DAY41_QQQ_CFB_NEW_CONTRACT_OI_EXCEPTION_RULE_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_NEW_CONTRACT_OI_EXCEPTION_RULE.md
- SAFE_FAST_DAY41_QQQ_CFB_NEW_CONTRACT_OI_EXCEPTION_STILL_BLOCKED.md
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
