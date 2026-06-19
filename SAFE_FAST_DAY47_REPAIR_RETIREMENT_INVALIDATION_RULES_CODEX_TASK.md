# SAFE-FAST Day 47 Repair Retirement Invalidation Rules - Codex Task

## Required startup

Read these files in order before making any change:

1. `SAFE_FAST_BUILD_STATE.md`
2. `SAFE_FAST_DAY47_GROUPED_REPLAY_REGRESSION_RULES_RESULT.md`
3. `SAFE_FAST_DAY47_DATA_COST_LEDGER_RULES_RESULT.md`
4. `SAFE_FAST_DAY47_PORTFOLIO_INTERACTION_RULES_RESULT.md`
5. `SAFE_FAST_DAY47_RISK_CAPITAL_RULES_RESULT.md`
6. `SAFE_FAST_DAY47_TO_DAY90_CONSOLIDATED_AUDIT_AND_COMPLETION_PLAN_RESULT.md`
7. `SAFE_FAST_PROJECT_DASHBOARD.md`
8. `SAFE_FAST_PROJECT_RULE_INDEX.md`
9. `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`

Expected starting state:

- branch: `main`
- commit: current local HEAD after the grouped replay/regression rules package is committed, if the user commits it
- clean repo except for this task file if it has not been committed

If the repo, control files, or result documents disagree, stop and report the exact conflict. Local git is the source of truth.

This is SAFE-FAST build-governance and rule-definition work, not live trade evaluation.

Do not modify the frozen engine baseline, `main.py`, live backend, production files, Railway, broker/account/order code, credentials, `.env`, or raw market data.

Do not download data and do not run a new backtest.

## Objective

Implement the next grouped Day 47-to-Day 90 rule package identified by the consolidated audit: repair-cycle limits, setup-family retirement, replacement, narrowing, and invalidation thresholds after grouped replay/regression governance is defined.

Use existing canonical owners. Update existing canonical documents rather than creating duplicate authorities.

## Required rule content

Define conservative repair, retirement, replacement, narrowing, and invalidation rules for:

- maximum repair cycles before a family/symbol/path must be narrowed, retired, or redesigned;
- criteria for bounded repair versus broad redesign;
- criteria for replacing candidates, examples, controls, or protected holdout slices;
- criteria for narrowing a setup family, symbol, expiration, liquidity bucket, time-of-day bucket, or regime path;
- criteria for retiring or invalidating a setup family/path;
- preservation of losers, no-trade controls, ambiguous cases, missing-data cases, and invalidated evidence;
- stale, missing, contradictory, or unverifiable repair/invalidation evidence;
- whether each rule is accepted, provisional governance, blocked, or still missing.

For every changed or accepted repair/retirement/invalidation rule, state:

- required evidence;
- required regression or consistency cases;
- automatic failure conditions;
- whether existing CFB replay outputs remain review-only or become invalidated;
- why the rule does not claim proof, profitability, readiness, paper eligibility, or live readiness.

## Change-control requirements

- Do not silently alter an existing accepted CFB trading rule, execution-realism rule, risk/capital rule, portfolio-interaction rule, data-cost ledger rule, or grouped replay/regression rule.
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
5. focused tests for the new repair/retirement/invalidation rule package and control-file agreement;
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
