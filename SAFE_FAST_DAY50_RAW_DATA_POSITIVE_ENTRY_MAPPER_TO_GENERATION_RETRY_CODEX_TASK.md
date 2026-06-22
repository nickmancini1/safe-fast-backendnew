# SAFE-FAST Day 50 Mapper-to-Generation Retry Task

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_ACCEPTED_SETUP_REPLAY_MAPPER_RESULT.md`
2. `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_ACCEPTED_SETUP_REPLAY_REGRESSION_CASES_RESULT.md`
3. The bounded mapper implementation and its JSON result
4. The existing historical generation, intake, replay, and costed-backtest paths

## Objective

Implement and execute the smallest bounded bridge needed to retry the three March 16, 2026 SPY setup-time packages through the existing historical candidate-generation path:

- Ideal
- Clean Fast Break
- Continuation

This is an implementation and validation task, not another planning-only task.

Do not modify the frozen live/production engine.

## Required behavior

1. Process each setup family separately.
2. Freeze all information at its accepted setup-time boundary.
3. Preserve no-hindsight behavior.
4. Preserve session-boundary behavior and carry-forward rules.
5. Validate developing-stage transitions.
6. Preserve stable winner selection.
7. Preserve blocker, stale/spent, freshness, invalidation, and no-trade behavior.
8. Do not combine the three SPY opportunities with preserved regression-control totals.
9. Do not loosen thresholds merely to produce candidates.
10. Do not invent missing fields or infer unavailable option evidence.

## Required substantive work

- Connect accepted mapper packages to the existing historical generation path using the smallest bounded adapter or bridge.
- Retry all three mapped SPY opportunities.
- Record every stage reached by each setup:
  - mapped package
  - generated candidate
  - setup-qualified
  - trade candidate
  - selected contract
  - eligible entry
  - recorded entry
- For every setup that reaches trade-candidate or selected-contract status, immediately continue through the existing local costed entry/exit replay or backtest path when exact evidence already exists.
- Report costed results separately by setup family.
- If exact option or exit-path evidence is unavailable, do not guess or download data. Finish all locally supported work and produce one grouped exact evidence request containing source, schema, symbol/contract, and timestamp window.
- If a setup fails to advance, report:
  - exact setup family
  - exact failed stage
  - exact failure category
  - exact missing or rejected evidence
  - smallest evidence-backed repair
  - required regression protection

## Regression batch

Create focused tests for the bridge and run the relevant existing tests together in one bounded batch covering:

- Ideal
- Clean Fast Break
- Continuation
- all 17 accepted mapper cases
- generation retry
- developing-stage transitions
- session boundaries and carry-forward
- stable winner selection
- no-trade preservation
- no-hindsight preservation
- existing positive-entry funnel controls

Also run:

- the mapper validator
- the Day 51 handoff consistency test
- `scripts/safe_fast_run_safe_checks.ps1` using `-ExecutionPolicy Bypass`
- `git diff --check`

Do not run unrelated broad test suites unless a changed dependency requires them.

## Outputs

Create:

- `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_MAPPER_TO_GENERATION_RETRY_RESULT.md`
- a machine-readable JSON result under `historical_signal_replay/results/`
- focused implementation and regression-test files

Update:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`
- `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`
- `SAFE_FAST_DATA_SOURCE_REGISTRY.md`
- `SAFE_FAST_NEXT_CHAT_HANDOFF_START_HERE.md`
- the Day 51 handoff consistency test where required

State exact before-and-after funnel totals.

## Prohibited scope

Do not touch:

- `main.py`
- production/live backend
- Railway or deploy files
- broker, account, order, or alert behavior
- credentials, tokens, secrets, or `.env`
- sizing
- live trading
- frozen `patch8` thresholds
- paid-data downloads

Do not claim profitability, paper eligibility, or live eligibility.

Finish with a compact summary of implementation, per-setup outcomes, tests, changed files, blockers, and the exact next substantive action.