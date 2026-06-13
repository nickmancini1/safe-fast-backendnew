# SAFE-FAST Day 41 QQQ gap threshold fixture decision task

Baseline:
- Latest commit before this task: 2691a47 Record QQQ CFB rule decision package

First action:
- Read SAFE_FAST_BUILD_STATE.md first.

Goal:
- Decide the first usable QQQ Clean Fast Break gap-context threshold fixture set.
- Add regression fixtures before calculator work.
- Do not fill evidence.
- Do not backtest.
- Do not choose a trade.
- Do not calculate P&L.

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_PROOF_PIPELINE.md
- SAFE_FAST_TRADE_PLAN_COMPLETENESS_GATE.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_DAY41_QQQ_CFB_RULE_DECISION_PACKAGE.md
- SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_RULE_DEFINITION.md
- SAFE_FAST_DAY41_QQQ_GAP_THRESHOLD_DECISION_PACKAGE.md
- SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_CALCULATION_REVIEW.md

Known QQQ raw values:
- Candidate: QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001
- Signal time: 2026-04-13T12:30:00-04:00
- Previous close: 611.02
- Signal-day open: 609.455
- Gap amount: -1.565
- Gap percent: about -0.2561%

Task:
1. Create:
   - SAFE_FAST_DAY41_QQQ_GAP_THRESHOLD_FIXTURE_DECISION.md
2. Define a first accepted test-fixture threshold set for QQQ CFB gap context.
3. Keep it conservative and explicit.
4. The doc must define:
   - clean
   - caution
   - fail
   - unknown
   - exact boundary examples
   - missing-data behavior
   - future-data rejection behavior
   - expected status for the known QQQ gap
5. The doc must clearly say this is a rule/fixture decision for testing, not proof or profitability.
6. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_BUILD_STATE.md

Allowed writes:
- SAFE_FAST_DAY41_QQQ_GAP_THRESHOLD_FIXTURE_DECISION_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_GAP_THRESHOLD_FIXTURE_DECISION.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_BUILD_STATE.md

Do not write:
- calculator code
- evidence fills
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
