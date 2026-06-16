# SAFE-FAST Day 41 QQQ diagnosis and batch candidate restart task

Baseline:
- Latest commit: f4a8781 Fill QQQ CFB execution context evidence

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.
- Then read SAFE_FAST_PROJECT_PROOF_PIPELINE.md.
- Then read SAFE_FAST_TRADE_PLAN_COMPLETENESS_GATE.md.

Goal:
- Stop grinding one QQQ issue.
- Diagnose QQQ once.
- Start batch-mode progress across the remaining candidates.
- Reuse existing tools instead of rebuilding from scratch.
- Do not backtest yet.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark any candidate ready.

Known QQQ result:
- QQQ CFB gap context passed.
- QQQ lifecycle/stale-spent passed.
- QQQ option context became caution.
- QQQ execution context failed.
- Complete caution review failed.
- Reason: selected option quote was too old.
- QQQ stays not ready.

Task:
1. Create:
   - SAFE_FAST_DAY41_BATCH_RESTART_QQQ_DIAGNOSIS_AND_CANDIDATE_PLAN.md

2. Diagnose QQQ in plain English:
   - what passed
   - what failed
   - why it failed
   - what this teaches the project
   - whether QQQ should stay parked
   - what should not be repeated

3. Build a batch candidate table for all known parked/replace candidates:
   - QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001
   - SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003
   - SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002
   - SPY-REAL-HISTORICAL-IDEAL-001
   - QQQ-REAL-HISTORICAL-CONTINUATION-001
   - QQQ-REAL-HISTORICAL-IDEAL-001
   - SPY-REAL-HISTORICAL-CONTINUATION-001

4. For each candidate, record:
   - setup type
   - symbol
   - known signal date/time if available
   - what data is already in repo
   - what Databento data is likely needed
   - which existing calculators/tools can be reused
   - which evidence checks can be attempted in batch
   - which checks are blocked by missing rules
   - whether it should be processed now, parked, or replaced

5. Create or update compact candidate packets for every candidate in:
   - historical_signal_replay/candidate_packets/

6. Create:
   - SAFE_FAST_DAY41_BATCH_NEXT_ACTIONS.md

7. The batch next-actions doc must define a grouped plan, not one tiny task:
   - batch data-needs check
   - batch Databento cost-check plan
   - batch evidence-preflight plan
   - batch calculator reuse plan
   - batch rule-gap list
   - next 2-3 candidates to process together

8. Update:
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_BUILD_STATE.md

9. Run:
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1

Allowed writes:
- SAFE_FAST_DAY41_QQQ_CFB_DIAGNOSIS_AND_NEXT_CANDIDATE_CODEX_TASK.md
- SAFE_FAST_DAY41_BATCH_RESTART_QQQ_DIAGNOSIS_AND_CANDIDATE_PLAN.md
- SAFE_FAST_DAY41_BATCH_NEXT_ACTIONS.md
- historical_signal_replay/candidate_packets/
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
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
