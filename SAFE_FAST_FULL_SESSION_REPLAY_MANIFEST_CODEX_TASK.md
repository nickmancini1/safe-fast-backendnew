# SAFE-FAST Full-Session Replay Manifest Implementation

Read `SAFE_FAST_BUILD_STATE.md` first.

The local repository is the only source of truth.

Begin only from a clean `main` branch. Inspect current history, latest results, existing accepted mapper, candidate pipeline, numeric setup work, validators, and tests before changing anything.

Do not redo completed mapper or candidate work.

## Objective

Implement a deterministic recognition-layer full-session replay manifest for all locally available SPY one-minute sessions, beginning with the validated 751-row March 16, 2026 session.

The system must scan the complete chronological session and account for every possible:

- Ideal
- Clean Fast Break
- Continuation

development.

Do not limit replay to the three previously identified favorable windows.

This task is independent of OPRA, option contracts, fills, and profitability.

## Required manifest behavior

For every session and setup family, record every relevant event as one of:

- rejected
- developing
- setup-qualified
- duplicate
- suppressed
- selected winner
- blocked by missing evidence
- executable at the recognition layer

Each record must include, where applicable:

- deterministic candidate ID
- session and setup family
- observation timestamp
- setup-time row
- trigger value or exact missing-field blocker
- invalidation value or exact missing-field blocker
- freshness/final-signal state
- blocker/caution review
- session-boundary state
- carry-forward state
- no-hindsight cutoff
- complete stage-transition history
- duplicate group
- suppression reason
- winner-selection result
- final disposition
- exact rejection or blocker reason

Missing evidence must block advancement. It must never become reduced confidence or inferred proof.

## Determinism requirements

Results must remain identical across:

- repeated runs
- input-order variations that preserve timestamps
- replay chunk-size variations
- session-boundary splits
- candidate enumeration order

Winner selection must not depend on dictionary order, filesystem order, or insertion order.

## No-hindsight requirements

- Process rows chronologically.
- Do not inspect future bars when creating setup-time fields.
- Record the precise information cutoff used for every decision.
- Do not use favorable future movement to create or validate a setup.
- Do not use manually selected windows as the complete opportunity universe.
- Keep recognition separate from option-contract and execution evidence.

## Reproducibility metadata

Every generated manifest must include:

- git commit
- configuration or frozen-rule hash
- source-file hashes
- dataset and schema
- symbol
- session date
- coverage timestamps
- timezone
- row count
- missing intervals
- run identifier

## Required implementation outputs

Reuse or extend existing files where appropriate instead of creating parallel systems.

Produce:

- focused implementation
- machine-readable JSON manifest
- validator
- focused result file
- focused tests

Update only factual current-state sections of existing canonical files:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`
- `SAFE_FAST_NEXT_CHAT_HANDOFF_START_HERE.md`

Do not add another broad planning document.

The canonical handoff must clearly state:

- latest baseline
- what is fixed
- what remains unproven
- active objective
- exact next task
- profitability proof status
- paper/live eligibility status

Remove or correct stale current-objective statements only when the replacement is supported by committed evidence.

## Required tests

Include focused protection for:

- Ideal full-session recognition
- Clean Fast Break full-session recognition
- Continuation full-session recognition
- stage-transition legality
- session-boundary behavior
- carry-forward behavior
- duplicate suppression
- stable winner selection
- no-trade behavior
- no-hindsight behavior
- stale/spent behavior
- missing-evidence blockers
- chronological ordering
- replay chunking invariance
- candidate input-order invariance
- deterministic reruns
- hand-selected-window bias exposure

Run the relevant existing regression subset for all three setup families.

Run:

- focused tests
- relevant existing regressions
- validators
- `scripts/safe_fast_run_safe_checks.ps1`
- `git diff --check`

Do not run unrelated broad suites.

## Guardrails

Do not modify:

- `main.py`
- production/live backend
- Railway/deploy
- broker, account, order, fill, or alert code
- credentials, secrets, tokens, or `.env`
- sizing
- frozen `patch8` thresholds

Do not buy or download data.

Do not claim profitability, paper eligibility, or live eligibility.

If the current engine cannot perform full-session enumeration without an undefined rule, implement the smallest bounded adapter possible and record the exact unresolved rule. Do not silently invent thresholds.

## Completion

After all required checks pass:

1. remove generated `__pycache__` directories;
2. stage only expected files;
3. run `git diff --cached --check`;
4. commit the implementation;
5. do not push;
6. require a clean working tree.

Final response must show:

- `COMMIT_HASH`
- `COMMIT_MESSAGE`
- `GIT_STATUS_SHORT`
- sessions scanned
- rows scanned
- counts by setup family and final disposition
- tests passed
- exact remaining blockers
- profitability proof: `NO`
- paper/live eligibility: `NO`
