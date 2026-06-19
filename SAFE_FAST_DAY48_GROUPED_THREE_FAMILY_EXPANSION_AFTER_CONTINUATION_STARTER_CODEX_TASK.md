# SAFE-FAST Day 48 Grouped Three-Family Expansion After Continuation Starter - Codex Task

## Required startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DAY48_CONTINUATION_STARTER_COVERAGE_RESULT.md`
2. `SAFE_FAST_DAY48_GROUPED_THREE_FAMILY_COVERAGE_EXPANSION_RESULT.md`
3. `SAFE_FAST_DAY48_ACTUAL_GROUPED_THREE_FAMILY_REPLAY_TEST_RESULT.md`
4. `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`
5. `SAFE_FAST_PROJECT_DASHBOARD.md`
6. `SAFE_FAST_PROJECT_RULE_INDEX.md`

If local git or canonical control files disagree with the current active task, stop and report the exact conflict.

## Active objective

Create the next bounded grouped three-family expansion package using only existing local fixtures and source rows.

Prioritize the smallest evidence-backed expansion after the Continuation starter result:

- add setup-time option-contract fixtures only where local rows already support them;
- otherwise preserve abstention, `UNKNOWN`, blocked, and no-trade results;
- include loser/no-trade and ambiguous controls;
- do not download data;
- do not backfill missing option or context evidence from future rows.

## Required constraints

Do not modify:

- `main.py`;
- production or live backend;
- Railway or deployment files;
- broker, account, or order code;
- credentials or `.env`;
- raw market data;
- accepted execution or risk thresholds.

Do not claim profitability, proof, readiness, promotion, paper eligibility, live eligibility, or intake-ready status.

## Required result

Create a result document for the grouped expansion evidence actually implemented.

Update:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`

Run focused tests, grouped Day 48 tests, safe checks, evidence validator, package-to-intake bridge, and `git diff --check`.

Do not commit or push.
