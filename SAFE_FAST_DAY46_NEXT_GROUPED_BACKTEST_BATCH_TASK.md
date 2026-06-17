# SAFE-FAST Day 46 Next Grouped Backtest Batch Task

Baseline:
- Latest completed review before this task: `SAFE_FAST_DAY46_FIRST_BACKTEST_REVIEW_AND_EXPANSION_PLAN.md`.
- First completed CFB reference: `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`, review-only `completed_profit_target`, adjusted result `+1.61`.

First action:
- Read `SAFE_FAST_BUILD_STATE.md`.
- Then read `SAFE_FAST_PROJECT_DASHBOARD.md`.
- Then read `SAFE_FAST_PROJECT_RULE_INDEX.md`.
- Then read `SAFE_FAST_DAY46_FIRST_BACKTEST_REVIEW_AND_EXPANSION_PLAN.md`.
- Then read `SAFE_FAST_DAY46_CANDIDATE_EXPANSION_PRIORITY_TABLE.md`.
- Then read the relevant candidate packets in `historical_signal_replay/candidate_packets/`.

Goal:
- Build the next grouped batch plan without one-example grinding.
- Keep SPY CFB 002 as a positive reference, not proof.
- Keep SPY CFB 003 and QQQ CFB 001 as no-trade controls.
- Add setup-family comparison only where rules and data are ready enough.
- Do not download data.
- Do not calculate new P&L unless a later explicit task authorizes a grouped backtest run.
- Do not claim proof or profitability.
- Do not mark any candidate ready.

Batch anchors:
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`: positive Clean Fast Break reference from the first completed review-only run.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`: quote-after-signal no-trade control.
- `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`: stale-quote no-trade control.
- `SPY-REAL-HISTORICAL-IDEAL-001`: next setup-family comparison candidate only if its Ideal-specific rule/data state is ready enough.
- Continuation candidates: include only if their rule/data state supports grouped processing.

Task:
1. Review the current rule/data state for the batch anchors.
2. Decide whether the next grouped work is:
   - more CFB examples;
   - CFB plus SPY Ideal comparison;
   - repair/no-trade validation;
   - or a data-needed/cost-check planning package.
3. If more candidates are added, require:
   - setup-family-specific lifecycle rules;
   - contract-selection rules;
   - option/context/execution rules;
   - entry/exit/stop/time/cost/slippage rules;
   - named failure/no-trade reasons;
   - sample-size and promotion blockers preserved.
4. Keep all candidate outcomes as review-only until a later explicit promotion/proof task exists.
5. Update dashboard, rule index, build state, and relevant candidate packets with the grouped-batch decision.

Allowed writes:
- `SAFE_FAST_DAY46_NEXT_GROUPED_BACKTEST_BATCH_TASK.md`
- new Day 46 grouped-batch review/planning docs
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`
- `SAFE_FAST_BUILD_STATE.md`
- `historical_signal_replay/candidate_packets/`

Excluded writes:
- raw Databento files
- backtest code
- new P&L calculations
- `main.py`
- live/engine/broker/order/account/Railway files
- `.env` or secrets

Required checks:
- `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`
- content validator if safe/local
- bridge if safe/local

Final response:
Baseline:
Fixed:
Blocked:
Next:
Tests:
Files changed:
