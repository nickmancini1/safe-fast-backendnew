# SAFE-FAST Day 48 Continuation Starter Coverage — Codex Task

## Required startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DAY48_GROUPED_THREE_FAMILY_COVERAGE_EXPANSION_RESULT.md`
2. `SAFE_FAST_DAY48_ACTUAL_GROUPED_THREE_FAMILY_REPLAY_TEST_RESULT.md`
3. `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`
4. `SAFE_FAST_PROJECT_DASHBOARD.md`
5. `SAFE_FAST_PROJECT_RULE_INDEX.md`
6. Existing Continuation replay runners, tests, candidate packets, fixtures, and local source rows

Expected branch: `main`
Expected starting commit: `4acb43a`
Expected status: clean except this task file

If local git or the canonical control files disagree, stop and report the exact
conflict.

This is actual SAFE-FAST build testing, not another governance-only task and
not live trade evaluation.

## Active objective

Create and execute the first stronger local Continuation coverage package using
only existing repository fixtures and existing local replay/source rows.

Do not download data.

Do not cherry-pick only favorable Continuation examples.

Include every locally runnable Continuation candidate or fixture that can be
tested without new data.

## Required execution

For each runnable Continuation case, execute as much of the existing frozen
rule stack as the evidence supports:

1. chronological lifecycle and developing-stage transitions;
2. session-boundary carry-forward and reset behavior;
3. candidate qualification or rejection;
4. deterministic option-contract selection;
5. execution-realism checks;
6. context and caution calculations;
7. winner selection and tie-breaking;
8. final entry, no-trade, unresolved, or blocked result.

Preserve `UNKNOWN`, abstention, and no-trade results when evidence is
insufficient. Do not manufacture a passing entry.

Run the complete Continuation package twice and compare outputs for exact
determinism.

Also rerun the existing grouped three-family replay tests to prove the new
Continuation coverage does not break Ideal or Clean Fast Break behavior.

## Allowed changes

You may add or repair:

- Continuation replay/test harnesses;
- focused fixtures built from existing local rows;
- focused tests;
- result documentation;
- control-file references.

Do not change frozen recognition or trading rules merely to make a test pass.

Do not modify:

- `main.py`;
- production or live backend;
- Railway or deployment files;
- broker, account, or order code;
- credentials or `.env`;
- raw market data;
- accepted execution or risk thresholds.

If existing frozen behavior fails, preserve the failure and create one grouped
repair task instead of silently patching the rule.

## Required result

Create:

`SAFE_FAST_DAY48_CONTINUATION_STARTER_COVERAGE_RESULT.md`

For every Continuation case, report:

- candidate identifier;
- evidence source;
- chronological stage path;
- session-boundary behavior;
- candidate qualification result;
- contract-selection result;
- execution result;
- context/caution result;
- winner result;
- final outcome and exact reason;
- first-run result;
- second-run result;
- deterministic or unstable;
- remaining missing evidence.

Report totals for:

- candidates found;
- runnable candidates;
- accepted-entry stages;
- final entries;
- no-trades;
- unresolved cases;
- blocked cases;
- stable cases;
- unstable cases;
- failures.

Do not claim profitability, proof, readiness, promotion, or live eligibility.

## Control files and next task

Update:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`

All three must contain one clearly labeled and matching current active-task
reference. Historical task references may remain historical but must not be
mistaken for the current task.

Create or reuse exactly one next grouped task based on actual test evidence:

- grouped Continuation repair if behavior fails;
- grouped three-family expansion if Continuation execution works but coverage
  remains thin;
- grouped missing-data cost check only when unavailable data is the proven
  blocker.

Do not route back into a governance-only task chain.

## Required tests

Run:

1. direct safe-check script;
2. execution-policy bypass if direct PowerShell is blocked;
3. all existing Continuation replay tests;
4. the new Continuation starter package twice;
5. existing Day 48 grouped three-family replay tests;
6. lifecycle and developing-stage tests;
7. session-boundary tests;
8. contract-selection tests;
9. execution-realism tests;
10. context/caution tests;
11. winner-stability tests;
12. evidence content validator;
13. package-to-intake bridge;
14. `git diff --check`.

Remove generated `__pycache__` directories.

Do not commit or push.

## Final summary

Return only:

- Baseline
- Fixed
- Blocked
- Next
- Tests
- Files changed
- Continuation totals
- Stage-transition result
- Session-boundary result
- Contract-selection result
- Execution-realism result
- Winner-stability result
- Exact next grouped task filename