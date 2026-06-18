# SAFE-FAST Day 47 CFB Execution Realism Rules - Codex Task

## Required startup

Read these files in order before making any change:

1. `SAFE_FAST_BUILD_STATE.md`
2. `SAFE_FAST_DAY47_PROMOTION_HOLDOUT_AND_CANDIDATE_FREEZE_RULES_RESULT.md`
3. `SAFE_FAST_PROJECT_DASHBOARD.md`
4. `SAFE_FAST_PROJECT_RULE_INDEX.md`
5. `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`
6. `SAFE_FAST_DAY45_CFB_EXACT_TRADE_RULE_VALUES.md`

Expected starting state:

- branch: `main`
- commit: current local HEAD after the Day 47 promotion/holdout/candidate-freeze rule package is committed, if the user commits it
- clean repo except for this task file if it has not been committed

If the repo, control files, or result document disagree, stop and report the exact conflict. Local git is the source of truth.

This is SAFE-FAST build-governance and rule-definition work, not live trade evaluation.

Do not modify the frozen engine baseline, `main.py`, live backend, production files, Railway, broker/account/order code, credentials, `.env`, or raw market data.

Do not download data and do not run a new backtest.

## Objective

Implement the next grouped Day 47-to-Day 90 rule package identified by the consolidated audit and by `SAFE_FAST_DAY47_PROMOTION_HOLDOUT_AND_CANDIDATE_FREEZE_RULES_RESULT.md`: Clean Fast Break execution realism before more countable results.

Use existing canonical owners. Update existing canonical documents rather than creating duplicate authorities.

## Required rule content

Define conservative Clean Fast Break execution realism rules for:

- latency from signal to usable quote/fill decision;
- order size and minimum quote size;
- partial-fill behavior;
- target-touch and stop-touch recognition;
- same-interval target/stop ordering;
- bid/ask/spread handling beyond the already accepted first-pass values;
- quote-age behavior, preserving the current `5` minute stale-quote failure rule unless explicitly narrowed with regression coverage;
- no-fallback selected-contract discipline;
- missing, delayed, crossed, locked, zero, or malformed quote behavior;
- whether each rule is accepted, provisional governance, blocked, or still missing.

For every changed or accepted execution rule, state:

- required evidence;
- required regression cases;
- automatic failure conditions;
- whether existing CFB replay outputs remain review-only or become invalidated;
- why the rule does not claim proof, profitability, readiness, paper eligibility, or live readiness.

## Change-control requirements

- Do not silently alter an existing accepted CFB trading rule.
- State why every frozen or accepted rule changed.
- Create or update focused consistency/regression tests.
- Every changed behavior or rule requires matching documentation.
- Create one result document for this task.
- Create or reuse exactly one next grouped Codex task according to the ordered audit plan.
- Do not commit or push.

## Required tests

Run:

1. `scripts/safe_fast_run_safe_checks.ps1`
2. the existing evidence content validator;
3. the existing package-to-intake bridge;
4. `tests/test_day47_to_day90_audit_consistency.py`;
5. focused tests for the new execution-realism rule package and control-file agreement;
6. `git diff --check`.

If direct PowerShell execution is blocked, run the existing process-level execution-policy bypass and report both results accurately.

Remove generated `__pycache__` directories before the final status check.

## Final summary

Return only:

- Baseline
- Fixed
- Blocked
- Next
- Tests
- Files changed
- Exact canonical rule document
- Exact next grouped task filename

Do not claim profitability, readiness, proof, or promotion merely because these governance rules were documented.
