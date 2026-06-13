# SAFE-FAST Day 41 QQQ CFB rule decision package task

Baseline:
- Latest commit before this task: 9f3364a Add Databento OPRA normalizer

First action:
- Read SAFE_FAST_BUILD_STATE.md first.

Goal:
- Define exactly what rule decisions are still needed before QQQ evidence fill or backtest.
- Do not invent unsupported rules.
- Do not fill evidence.
- Do not choose a trade.
- Do not calculate P&L.
- Do not mark QQQ ready.

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_PROOF_PIPELINE.md
- SAFE_FAST_TRADE_PLAN_COMPLETENESS_GATE.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_PROJECT_CONTROL_CONSOLIDATION_AUDIT.md
- SAFE_FAST_DAY41_DATABENTO_QQQ_OPRA_NORMALIZER_REVIEW.md
- SAFE_FAST_DAY41_DATABENTO_QQQ_EVIDENCE_FIELD_MAPPING.md
- SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_RULE_DEFINITION.md
- SAFE_FAST_DAY41_QQQ_GAP_THRESHOLD_DECISION_PACKAGE.md
- historical_signal_replay/source_data/richer_export_package_work/

Task:
1. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_RULE_DECISION_PACKAGE.md
2. For QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001, list every missing rule decision needed before evidence fill/backtest:
   - gap thresholds
   - stale/spent rule
   - CFB expiry rule
   - stage transitions
   - contract selection
   - entry rule
   - fill assumption
   - spread/liquidity limits
   - exit rule
   - stop/invalidation rule
   - time exit
   - cost/slippage assumptions
   - failure diagnosis labels
   - sample-size requirement
   - promotion gate
3. For each rule, classify:
   - accepted/current
   - missing decision
   - pending validation
   - blocked by data
   - blocked by tests
4. If repo evidence supports a rule, cite the repo source in the doc.
5. If repo evidence does not support a rule, say the exact decision needed.
6. Create the smallest ordered implementation plan to get QQQ from raw data to a valid backtest path.
7. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_BUILD_STATE.md

Allowed writes:
- SAFE_FAST_DAY41_QQQ_CFB_RULE_DECISION_PACKAGE_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_RULE_DECISION_PACKAGE.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_BUILD_STATE.md

Do not write:
- evidence fills
- calculator code
- backtest code
- trade-selection code
- P&L
- raw data files
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
