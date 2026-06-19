# SAFE-FAST Day 48 Actual Grouped Three-Family Replay Test — Codex Task

## Baseline

Read SAFE_FAST_BUILD_STATE.md first.

Then read:

1. SAFE_FAST_PROJECT_PROOF_PIPELINE.md
2. SAFE_FAST_PROJECT_DASHBOARD.md
3. SAFE_FAST_PROJECT_RULE_INDEX.md
4. Existing Ideal, Clean Fast Break, and Continuation replay runners and tests
5. Existing candidate packets and locally available replay data

Expected branch: main  
Expected starting commit: 426a49f  
Expected status: clean except this task file

This user-directed testing task supersedes the queued repair-retirement
governance task as the immediate objective.

Do not run another governance-only task.

## Active objective

Perform the actual grouped replay and regression test now using existing data
and fixtures across:

- Ideal
- Clean Fast Break
- Continuation

Also test:

- chronological developing-stage transitions;
- session-boundary carry-forward and reset behavior;
- accepted-entry cases;
- rejection and no-trade controls;
- ambiguous or boundary cases already available;
- deterministic winner selection and tie-breaking;
- identical output across two repeated grouped runs;
- preservation of previously accepted behavior.

This is build validation, not live trade evaluation.

## Required execution

1. Inventory all currently runnable candidates for all three setup families.
2. Include every runnable candidate; do not select only successful examples.
3. Run the complete grouped batch twice.
4. Compare both runs for deterministic equality.
5. Record each candidate's chronological stage path and final outcome.
6. Run all existing family-specific replay and regression tests.
7. Run developing-stage, session-boundary, and winner-stability tests.
8. Report passes, failures, unresolved cases, and missing coverage honestly.

If one family cannot run:

- run the other families;
- identify the exact missing data, fixture, runner, or rule dependency;
- do not replace execution with more governance documentation.

Replay/test-harness repairs are allowed only when they exercise existing frozen
behavior. Do not change recognition or trading rules merely to make a test pass.

## Restrictions

Do not modify:

- frozen trading behavior;
- live or production backend;
- main.py;
- Railway or deployment files;
- broker, account, or order code;
- credentials or .env.

Do not download data during this task.

Do not claim profitability, proof, readiness, promotion, or live eligibility.

## Required result

Create:

SAFE_FAST_DAY48_ACTUAL_GROUPED_THREE_FAMILY_REPLAY_TEST_RESULT.md

The result must show, for every candidate:

- candidate identifier;
- setup family;
- evidence source;
- chronological stage path;
- session-boundary behavior;
- entry, rejection, unresolved, or blocked result;
- exact reason;
- winner-selection result;
- first-run result;
- second-run result;
- stability result;
- regression result;
- remaining limitation.

Report totals for each family:

- candidates found;
- candidates runnable;
- entries;
- no-trades;
- ambiguous cases;
- passes;
- failures;
- blocked cases;
- stable cases;
- unstable cases.

## Control files and next action

Update:

- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md

The next task must be determined by actual test evidence:

- grouped repair when behavior fails;
- grouped expansion when execution works but coverage is thin;
- grouped cost check only when missing data is a proven blocker.

Do not route back into another governance-only chain.

## Tests

Run:

- direct safe-check script;
- execution-policy bypass if direct PowerShell is blocked;
- all existing Ideal replay tests;
- all existing Clean Fast Break replay tests;
- all existing Continuation replay tests;
- developing-stage transition tests;
- session-boundary tests;
- winner-selection stability tests;
- evidence content validator;
- package-to-intake bridge;
- the complete grouped batch twice;
- git diff --check.

Remove generated __pycache__ directories.

Do not commit or push.

## Final summary

Return only:

- Baseline
- Fixed
- Blocked
- Next
- Tests
- Files changed
- Ideal totals
- Clean Fast Break totals
- Continuation totals
- Stage-transition result
- Session-boundary result
- Winner-stability result
- Exact next grouped task filename
