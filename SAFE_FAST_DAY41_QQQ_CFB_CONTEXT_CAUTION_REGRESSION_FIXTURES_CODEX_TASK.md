# SAFE-FAST Day 41 QQQ CFB context/caution regression fixtures task

Baseline:
- Latest commit before this task: 9ecc166 Accept QQQ CFB context caution framework

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.

Goal:
- Add regression fixtures for the accepted QQQ CFB context/caution framework.
- Do not invent missing human decisions.
- Do not fill evidence.
- Do not create calculator code.
- Do not backtest.
- Do not choose a trade.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark QQQ ready.

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_DECISION.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_DECISION_STILL_BLOCKED.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_RULE.md
- SAFE_FAST_DAY41_QQQ_CFB_RULE_DECISION_PACKAGE.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md

Known blocked human decisions:
- option thresholds and selected-contract policy
- execution entry/fill/quote-age/spread/liquidity rules
- historical headline/no-headline source policy
- whether any unknown component can pass complete caution review

Task:
1. Create:
   - historical_signal_replay/fixtures/qqq_cfb_context_caution_regression_fixtures.json
2. Create:
   - SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_REGRESSION_FIXTURES_REVIEW.md
3. Fixtures must cover only the accepted framework behavior:
   - option_context_status: clean, caution, fail, unknown
   - headline_context_status: clean, caution, fail, unknown
   - execution_context_status: clean, caution, fail, unknown
   - complete_caution_review_status precedence:
     - fail beats everything
     - unknown beats caution/clean unless later human decision changes this
     - caution beats clean
     - all clean becomes clean
   - missing-data behavior
   - future-data rejection behavior
   - no-hindsight timestamp behavior
4. Fixtures must not decide missing option thresholds, selected contract, execution fill, quote-age, spread/liquidity, or headline-source policy.
5. If any required fixture cannot be honest without a missing human decision, create:
   - SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_FIXTURES_BLOCKED.md
   and name the exact missing decision.
6. Validate the JSON parses and all required fields exist.
7. Run:
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1
8. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
   - SAFE_FAST_BUILD_STATE.md

Allowed writes:
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_REGRESSION_FIXTURES_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_REGRESSION_FIXTURES_REVIEW.md
- SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_FIXTURES_BLOCKED.md
- historical_signal_replay/fixtures/qqq_cfb_context_caution_regression_fixtures.json
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
