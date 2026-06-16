# SAFE-FAST Day 41 SPY CFB starter option/execution/context batch task

Baseline:
- Latest commit before this task: a6b5daa Fill SPY CFB lifecycle evidence batch

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.
- Then read SAFE_FAST_DAY41_STARTER_BATCH_OPTION_INSPECTION.md.
- Then read SAFE_FAST_DAY41_STARTER_BATCH_RULE_AND_DATA_MATRIX.md.

Goal:
- Process SPY CFB 002 and SPY CFB 003 together.
- Use cheap starter Databento data only.
- Do not download more data.
- Do not use full-window data.
- Do not split into one tiny task per field.
- Move option/execution/context as far as the starter data and accepted CFB rules honestly allow.
- Do not backtest.
- Do not calculate P&L.
- Do not claim proof or profitability.
- Do not mark either candidate ready.

Candidates:
- SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002
- SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003

Use only local starter files:
- SPY_REAL_HISTORICAL_CLEAN_FAST_BREAK_002_definitions_full_day.csv
- SPY_REAL_HISTORICAL_CLEAN_FAST_BREAK_002_statistics_full_day.csv
- SPY_REAL_HISTORICAL_CLEAN_FAST_BREAK_002_tcbbo_signal_10min.csv
- SPY_REAL_HISTORICAL_CLEAN_FAST_BREAK_002_trades_signal_10min.csv
- SPY_REAL_HISTORICAL_CLEAN_FAST_BREAK_003_definitions_full_day.csv
- SPY_REAL_HISTORICAL_CLEAN_FAST_BREAK_003_statistics_full_day.csv
- SPY_REAL_HISTORICAL_CLEAN_FAST_BREAK_003_tcbbo_signal_10min.csv
- SPY_REAL_HISTORICAL_CLEAN_FAST_BREAK_003_trades_signal_10min.csv

Clean Fast Break family rule to assess:
- Use the existing QQQ CFB rule structure as the proposed CFB-family default only if no repo conflict exists.
- Contract side: long call.
- Expiration: nearest reviewed expiration with DTE >= 14.
- Strike: lowest call strike at or above the candidate trigger/level.
- Quote: nearest quote at or before signal time.
- Spread cap: 0.15 and 2.00%.
- Bid size >= 1.
- Ask size >= 1.
- Trade volume >= 1.
- Open interest >= 1 if setup-time-safe same-contract open interest exists.
- If contract is newly listed and prior-day open interest cannot exist, use the accepted new-contract OI exception: option context may be caution, not clean, if quote/spread/size/volume/listing gates pass.
- No fallback if top ranked contract fails.
- Execution quote freshness:
  - clean if quote age <= 60 seconds
  - caution if quote age > 60 seconds and <= 5 minutes
  - fail if quote age > 5 minutes
- No future data.
- No P&L/fill/proof/readiness inference.

Task:
1. Create:
   - SAFE_FAST_DAY41_SPY_CFB_STARTER_OPTION_EXECUTION_CONTEXT_BATCH_REVIEW.md

2. For both SPY CFB candidates, find:
   - signal time
   - trigger/level needed for strike selection
   - setup-window quote rows
   - setup-window trade rows
   - setup-time-safe statistics/open-interest rows
   - candidate evidence rows

3. If trigger/level is missing for either candidate, do not guess.
   - Mark that candidate blocked with exact missing field.
   - Continue processing the other candidate if possible.

4. If the CFB-family contract rule can be applied without conflict:
   - create or update grouped SPY CFB contract-selection fixtures
   - extend/reuse the contract selector safely
   - run tests
   - select/abstain for both SPY CFB candidates from starter data only

5. If execution-context rule can be applied:
   - create or update grouped SPY CFB execution fixtures
   - extend/reuse the execution-context calculator safely
   - run tests
   - classify execution context for both candidates from starter data only

6. If option/execution/context evidence can be filled from accepted rules and source-backed starter data:
   - fill only those SPY CFB context/caution fields
   - do not alter unrelated fields

7. If a field cannot be filled:
   - leave it blocked
   - state the exact blocker
   - do not request full-window data in this task

8. Update:
   - SAFE_FAST_PROJECT_DASHBOARD.md
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_BUILD_STATE.md
   - historical_signal_replay/candidate_packets/SPY_REAL_HISTORICAL_CLEAN_FAST_BREAK_002.md
   - historical_signal_replay/candidate_packets/SPY_REAL_HISTORICAL_CLEAN_FAST_BREAK_003.md

9. Run:
   - python -m unittest tests.test_cfb_contract_selector if present
   - python -m unittest tests.test_execution_context_calculator if present
   - python -m unittest tests.test_context_caution_calculator if present
   - powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1
   - relevant content validator and bridge if safe/local

Allowed writes:
- SAFE_FAST_DAY41_SPY_CFB_STARTER_OPTION_EXECUTION_CONTEXT_BATCH_CODEX_TASK.md
- SAFE_FAST_DAY41_SPY_CFB_STARTER_OPTION_EXECUTION_CONTEXT_BATCH_REVIEW.md
- historical_signal_replay/fixtures/
- historical_signal_replay/cfb_contract_selector.py
- historical_signal_replay/execution_context_calculator.py
- historical_signal_replay/context_caution_calculator.py
- tests/
- historical_signal_replay/source_data/richer_export_package_work/
- historical_signal_replay/candidate_packets/SPY_REAL_HISTORICAL_CLEAN_FAST_BREAK_002.md
- historical_signal_replay/candidate_packets/SPY_REAL_HISTORICAL_CLEAN_FAST_BREAK_003.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_BUILD_STATE.md

Do not write:
- raw Databento files
- full-window data
- unrelated evidence fields
- backtest code
- P&L
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
