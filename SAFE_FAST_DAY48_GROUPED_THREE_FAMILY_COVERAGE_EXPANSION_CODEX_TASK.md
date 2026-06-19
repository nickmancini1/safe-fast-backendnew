# SAFE-FAST Day 48 Grouped Three-Family Coverage Expansion - Codex Task

## Baseline

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DAY48_ACTUAL_GROUPED_THREE_FAMILY_REPLAY_TEST_RESULT.md`
2. `SAFE_FAST_PROJECT_DASHBOARD.md`
3. `SAFE_FAST_PROJECT_RULE_INDEX.md`
4. Existing Ideal, Clean Fast Break, and Continuation replay fixtures/tests
5. Existing candidate packets and locally available replay data

## Active Objective

Expand grouped replay coverage only where existing local fixtures/data support it.

The Day 48 actual grouped run showed deterministic execution across 12 runnable lifecycle fixtures, but coverage is thin because all final grouped lifecycle outcomes are `NO_TRADE`, GLD/IWM rows remain shape-only review candidates, and Ideal/Continuation still lack option-execution/P&L validation.

## Required Work

1. Inventory additional local fixture/data coverage available for Ideal, Clean Fast Break, and Continuation.
2. Identify which candidates can become stronger replay/regression cases without downloading data.
3. Add or repair test-harness coverage only when it exercises existing frozen behavior.
4. Preserve no-trade controls and ambiguous/pending controls.
5. Report exact missing fixture, data, runner, or rule dependencies for anything that cannot be expanded.

## Restrictions

Do not modify:

- frozen trading behavior;
- live or production backend;
- `main.py`;
- Railway or deployment files;
- broker, account, or order code;
- credentials or `.env`;
- raw vendor data.

Do not download data.

Do not claim profitability, proof, readiness, promotion, or live eligibility.

## Required Result

Create a result file named:

`SAFE_FAST_DAY48_GROUPED_THREE_FAMILY_COVERAGE_EXPANSION_RESULT.md`

Update:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`

The next task must be determined from actual expansion evidence.

## Tests

Run:

- direct safe-check script;
- execution-policy bypass if direct PowerShell is blocked;
- focused grouped replay tests affected by the expansion;
- relevant family-specific replay/regression tests;
- evidence content validator;
- package-to-intake bridge;
- `git diff --check`.

Remove generated `__pycache__` directories.
