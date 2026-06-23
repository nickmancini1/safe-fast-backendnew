# SAFE-FAST Day 51 Completion and Backtest Batch

Read `SAFE_FAST_BUILD_STATE.md` first.

The repository is the source of truth. Inspect current git history and all newer result files before acting.

Required reads include:

- `SAFE_FAST_DAY51_SPY_NUMERIC_SETUP_AND_OPRA_COST_CHECK_RESULT.md`
- `historical_signal_replay/results/day51_spy_numeric_setup_and_opra_cost_check.json`
- the accepted mapper result
- mapper-to-generation retry result
- review-only-package-to-candidate result
- option-contract evidence review result
- current build state, dashboard, rule index, proof pipeline, data registry, and canonical handoff

## Objective

Complete the substantive unfinished path from the three March 16, 2026 SPY setup-qualified candidates to actual costed backtest results.

Process separately:

- Ideal
- Clean Fast Break
- Continuation

Do not create another planning-only loop. Do not merely restate existing blockers.

## Required execution

1. Verify numeric trigger, invalidation, setup timestamp, direction, freshness, session boundary, and no-hindsight boundary for each setup.
2. Use existing local option evidence and frozen contract-selection rules.
3. Advance each setup as far as valid evidence permits:
   - generated candidate
   - setup-qualified
   - trade candidate
   - selected contract
   - eligible entry
   - recorded entry
   - costed exit replay
4. For every executable setup, report:
   - signal time
   - selected option contract
   - entry time and price
   - exit time and price
   - gross P&L
   - spread, slippage, commissions, and fees
   - net P&L
   - holding duration
   - exit reason
5. Keep setup-family results separate.

## Data behavior

Search all existing local evidence before requesting anything.

If exact OPRA evidence is absent:

- run the existing Databento exact cost-estimation path for the smallest bounded grouped request;
- include definitions, quotes, trades, statistics, volume/open interest, entry window, and exit window only where required;
- report the exact dataset, schema, symbols, timestamps, and cost;
- do not purchase or download nonzero-cost data without explicit approval.

If the exact cost is zero, or the evidence is already locally available, continue immediately through contract selection and costed backtesting.

The final outcome must be either:

- actual per-setup costed backtest results, or
- one exact `APPROVAL_REQUIRED` grouped request with a numerical cost and the precise backtest stages it unlocks.

`NOT_AVAILABLE` is not acceptable unless the cost-estimation API was actually attempted and the exact technical failure is recorded.

## Audit unfinished work

Inspect results and task references added since commit `5daa06f`.

- Do not redo completed mapper or candidate work.
- Resolve any result that names a missing next task.
- Resolve stale control-document references.
- Do not commit obsolete handoff-only WIP.
- Do not modify or delete git stashes.

## Regression batch

Run the relevant tests together, including:

- all `test_day50_raw_data_positive_entry_*.py` tests;
- `test_day51_spy_numeric_setup_and_opra_cost_check.py`;
- all new focused tests;
- mapper, retry, candidate-contract, option-review, and numeric/OPRA validators;
- contract-selection and deterministic winner-selection controls;
- execution-cost and exit-replay controls;
- no-hindsight, no-trade, session-boundary, carry-forward, stale/spent, blocker, and stage-transition protections;
- Day 51 handoff consistency;
- `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`;
- `git diff --check`.

Do not run unrelated broad suites.

## Required updates

Update only files whose factual state changed:

- `SAFE_FAST_BUILD_STATE.md`
- dashboard
- rule index
- proof pipeline
- data-source registry
- canonical handoff
- focused implementation, JSON result, validator, and tests

Do not touch:

- `main.py`
- production/live backend
- Railway/deploy
- broker/account/order/alert code
- credentials, secrets, tokens, or `.env`
- sizing
- frozen `patch8` thresholds

Do not claim profitability, paper eligibility, or live eligibility without evidence.

## Commit requirement

After all relevant checks pass:

1. remove generated `__pycache__` directories;
2. stage only expected files;
3. run `git diff --cached --check`;
4. commit the completed batch;
5. do not push;
6. require a clean working tree.

The final response must show exactly:

- `COMMIT_HASH: <full hash>`
- `COMMIT_MESSAGE: <message>`
- `GIT_STATUS_SHORT: CLEAN`
- per-setup backtest result or exact approval-required cost
- tests passed
