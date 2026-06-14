# SAFE-FAST Day 41 QQQ CFB stale/spent expiry rule task

Baseline:
- Latest commit before this task: 17d433e Fill QQQ CFB gap context evidence

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Define the QQQ Clean Fast Break stale/spent expiry rule.
- Do not fill evidence yet.
- Do not backtest.
- Do not choose a trade.
- Do not calculate P&L.
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
1. Find any existing repo language for Clean Fast Break stale/spent/expiry.
2. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_STALE_SPENT_EXPIRY_RULE.md
3. Define:
   - when a QQQ CFB setup is fresh
   - when it becomes stale
   - when it becomes spent
   - when it expires
   - what timestamp controls the decision
   - what data is allowed before/at signal time
   - what future data is forbidden
   - what missing data means
   - exact regression fixture cases needed next
4. If repo evidence is not enough to define an honest rule, create:
   - SAFE_FAST_DAY41_QQQ_CFB_STALE_SPENT_EXPIRY_DECISION_NEEDED.md
   and state the exact decision needed.
5. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - SAFE_FAST_BUILD_STATE.md

Allowed writes:
- SAFE_FAST_DAY41_QQQ_CFB_STALE_SPENT_EXPIRY_RULE_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_STALE_SPENT_EXPIRY_RULE.md
- SAFE_FAST_DAY41_QQQ_CFB_STALE_SPENT_EXPIRY_DECISION_NEEDED.md
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
