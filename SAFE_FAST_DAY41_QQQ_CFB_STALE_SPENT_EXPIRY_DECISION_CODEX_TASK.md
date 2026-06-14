# SAFE-FAST Day 41 QQQ CFB stale/spent expiry decision task

Baseline:
- Latest commit before this task: 07ea738 Record QQQ CFB stale spent expiry decision needed

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Decide the first usable QQQ Clean Fast Break stale/spent/expiry lifecycle rule.
- Keep it explicit, conservative, and testable.
- Do not fill evidence.
- Do not backtest.
- Do not choose a trade.
- Do not calculate P&L.
- Do not mark QQQ ready.

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_DAY41_QQQ_CFB_STALE_SPENT_EXPIRY_RULE.md
- SAFE_FAST_DAY41_QQQ_CFB_STALE_SPENT_EXPIRY_DECISION_NEEDED.md
- SAFE_FAST_DAY41_QQQ_CFB_RULE_DECISION_PACKAGE.md
- SAFE_FAST_TRADE_PLAN_COMPLETENESS_GATE.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md

Task:
1. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_STALE_SPENT_EXPIRY_DECISION.md
2. Define the first accepted QQQ CFB lifecycle rule for testing:
   - fresh
   - stale
   - spent
   - expired
   - unknown
3. Define:
   - freshness window
   - stale timing
   - spent behavior
   - expiry clock
   - higher-base refresh behavior
   - state precedence
   - missing-data behavior
   - future-data rejection behavior
   - required regression fixture cases
4. If repo evidence still does not support a decision, do not fake it. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_STALE_SPENT_EXPIRY_DECISION_STILL_BLOCKED.md
   and name the exact missing human decision.
5. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - SAFE_FAST_BUILD_STATE.md

Allowed writes:
- SAFE_FAST_DAY41_QQQ_CFB_STALE_SPENT_EXPIRY_DECISION_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_STALE_SPENT_EXPIRY_DECISION.md
- SAFE_FAST_DAY41_QQQ_CFB_STALE_SPENT_EXPIRY_DECISION_STILL_BLOCKED.md
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
