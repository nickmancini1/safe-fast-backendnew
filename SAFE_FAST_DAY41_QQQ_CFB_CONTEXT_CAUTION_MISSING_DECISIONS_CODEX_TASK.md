# SAFE-FAST Day 41 QQQ CFB context/caution missing decisions task

Baseline:
- Latest commit before this task: 3ce6409 Add QQQ CFB context caution regression fixtures

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Decide the missing QQQ CFB context/caution rules so calculator work can proceed.
- Keep decisions explicit, conservative, and testable.
- Do not fill evidence.
- Do not backtest.
- Do not choose a real trade.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark QQQ ready.

Missing decisions to resolve:
1. option thresholds and selected-contract policy
2. execution entry/fill/quote-age/spread/liquidity rules
3. historical headline/no-headline source policy
4. whether any unknown component can pass complete caution review

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_TRADE_PLAN_COMPLETENESS_GATE.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_DECISION.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_DECISION_STILL_BLOCKED.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_REGRESSION_FIXTURES_REVIEW.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_FIXTURES_BLOCKED.md
- SAFE_FAST_DAY41_DATABENTO_QQQ_DOWNLOAD_VALIDATION.md
- SAFE_FAST_DAY41_DATABENTO_QQQ_EVIDENCE_FIELD_MAPPING.md
- SAFE_FAST_DAY41_DATABENTO_QQQ_OPRA_NORMALIZER_REVIEW.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md

Task:
1. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_MISSING_DECISIONS.md
2. For each missing decision, either:
   - accept a first conservative testable rule, or
   - state exactly why the repo still cannot support a rule.
3. If accepting rules, define:
   - allowed statuses
   - required raw inputs
   - thresholds
   - timestamps
   - future-data rejection
   - missing-data behavior
   - regression fixture cases needed next
4. Required conservative defaults to evaluate:
   - no selected option contract means option_context_status remains unknown
   - no headline source means headline_context_status remains unknown unless a repo-backed no-headline source exists
   - no execution fill rule means execution_context_status remains unknown
   - complete_caution_review_status cannot pass if any component is unknown
5. Do not invent a tradable contract or fake headline check.
6. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - SAFE_FAST_BUILD_STATE.md
7. Run:
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1

Allowed writes:
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_MISSING_DECISIONS_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_MISSING_DECISIONS.md
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
