# SAFE-FAST Day 52 Full-Session Recognition Proof

Read `SAFE_FAST_BUILD_STATE.md` first.

The local repository is the only source of truth. Inspect current history, current canonical state, accepted mapper, candidate pipeline, numeric setup work, validators, tests, and locally available replay data before editing.

Do not redo completed mapper or candidate work.

## Ultimate project goal

Build and prove a profitable SAFE-FAST trading plan that reliably recognizes Ideal, Clean Fast Break, and Continuation setups without hindsight, preserves strict no-trade discipline, and passes replay/regression validation before paper or live use.

Current profitability proof: `NO`.

Current paper/live eligibility: `NO`.

## Active objective

Implement a deterministic full-session recognition replay manifest.

Begin with the validated March 16, 2026 SPY one-minute session containing 751 chronological rows. Include any other locally available compatible sessions without acquiring new data.

The replay must scan the complete session. It must not restrict evaluation to the three previously identified favorable windows.

This task concerns recognition, lifecycle, stage transitions, duplicate handling, winner selection, session behavior, and no-hindsight proof.

It must not depend on OPRA availability, selected option contracts, fills, exits, or profitability.

## Required implementation

Reuse or extend the accepted mapper and candidate pipeline. Do not create a parallel recognition engine unless the existing path cannot support deterministic full-session enumeration.

For each session and each setup family:

- Ideal
- Clean Fast Break
- Continuation

record every relevant developing opportunity and its final disposition.

Allowed final dispositions must include:

- rejected
- developing at session end
- setup-qualified
- duplicate
- suppressed
- selected winner
- blocked by missing evidence
- recognition-layer executable

Every record must contain, where applicable:

- deterministic candidate ID
- session date
- setup family
- direction
- observation timestamp
- setup-time row
- trigger
- invalidation
- freshness/final-signal state
- blocker/caution review
- session-boundary state
- carry-forward state
- no-hindsight cutoff
- chronological stage-transition history
- duplicate group ID
- suppression reason
- winner-selection result
- exact rejection or blocker code
- final disposition

Missing required evidence must block advancement. It must never be converted into reduced confidence, a guessed value, or an inferred pass.

## Machine-enforced stage contracts

Define exact predicates for every implemented transition.

At minimum, advancement to setup-qualified must require:

- setup-time row
- numeric trigger
- numeric invalidation
- freshness/final-signal state
- blocker/caution review
- session-boundary behavior
- no-hindsight boundary

Illegal stage skipping must fail validation.

Every rejection and blocker must use a stable machine-readable reason code.

## No-hindsight protection

- Process bars chronologically.
- Do not inspect future rows when creating setup-time fields.
- Record the exact information cutoff for each decision.
- Do not use later favorable movement to create, classify, or approve a setup.
- Do not use same-bar information before it would have been observable.
- Do not use the known three windows as the complete opportunity universe.
- Produce a setup-time review view that excludes all post-cutoff fields.

## Determinism protection

Results must remain identical across:

- repeated runs
- candidate enumeration order changes
- replay chunk-size changes
- stable timestamp-preserving input reorderings
- session-boundary splits and recombination

Winner selection must not depend on dictionary order, filesystem order, or insertion order.

Where setup families overlap, record all valid recognition labels but apply one explicit deterministic economic-winner rule. Do not create more than one economic candidate from the same duplicate group unless an existing frozen rule explicitly permits it.

## Recognition versus economics

Keep three layers separate:

1. underlying recognition and lifecycle;
2. option contract selection;
3. entry, exit, costs, and net result.

Missing OPRA data may block layers 2 and 3. It must not prevent honest measurement of layer 1.

Do not claim that recognition success proves profitability.

## Reproducibility metadata

The machine-readable manifest must record:

- git commit
- frozen-rule/configuration hash
- source-file hashes
- dataset
- schema
- symbol
- session date
- coverage timestamps
- timezone
- source row count
- missing intervals
- run identifier
- implementation version

Equivalent evidence and configuration must produce equivalent decisions.

## Required outputs

Produce concrete implementation and evidence, not another planning loop:

- focused implementation
- machine-readable JSON manifest
- manifest validator
- focused result document
- focused regression tests
- compact setup-time review output with future information excluded

Reuse existing locations and naming patterns where practical.

Do not add broad architecture or handoff-only documents.

## Required tests

Add and run focused protection for:

- Ideal full-session recognition
- Clean Fast Break full-session recognition
- Continuation full-session recognition
- complete-session opportunity accounting
- known-window versus complete-session bias exposure
- legal stage transitions
- illegal stage skipping
- exact blocker/rejection codes
- no-hindsight cutoffs
- setup-time review field exclusion
- session-boundary behavior
- carry-forward behavior
- stale and spent behavior
- duplicate grouping
- deterministic suppression
- stable winner selection
- strict no-trade behavior
- missing-evidence blocking
- repeated-run determinism
- replay chunking invariance
- candidate input-order invariance

Run the relevant existing Ideal, Clean Fast Break, Continuation, stage-transition, session-boundary, duplicate, winner-selection, no-trade, and no-hindsight regressions.

Run:

- focused tests
- relevant bounded regressions
- all affected validators
- `scripts/safe_fast_run_safe_checks.ps1`
- `git diff --check`

Do not run unrelated broad suites.

## Project questions whose answers must remain explicit

- What proves recognition works?
  Complete chronological session accounting with independent validation, not three selected examples.

- Can recognition be measured without option data?
  Yes. OPRA is a separate economic-evidence layer.

- Is March 16, 2026 enough to prove profitability?
  No. It can validate pipeline behavior only.

- What happens to ambiguous evidence?
  It remains unresolved or blocked. It is never forced into a positive or negative label.

- What happens after weak, failed, or negative results?
  Record the exact failure and make the smallest evidence-backed correction. Do not loosen frozen thresholds silently.

- What blocks promotion?
  Any hindsight violation, unstable winner, illegal transition, unexplained full-session false-positive behavior, or lack of positive untouched net results after costs.

## Canonical state and next-chat continuity

Audit existing control documents before updating them. Correct stale active-objective statements without duplicating historical text.

Update only factual current-state sections of:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`
- `SAFE_FAST_NEXT_CHAT_HANDOFF_START_HERE.md`

The canonical handoff must explicitly state:

- latest verified commit
- what is fixed
- what remains unproven
- active objective
- exact next task
- full-session manifest result
- exact remaining blockers
- profitability proof: `NO`
- paper/live eligibility: `NO`

Documentation updates must be in the same implementation commit as the factual result.

## Guardrails

Do not modify:

- `main.py`
- production/live backend
- Railway/deploy
- broker, account, order, fill, or alert code
- credentials, tokens, secrets, or `.env`
- sizing
- frozen `patch8` thresholds

Do not buy or download data.

Do not perform option P&L work in this task.

Do not claim profitability or paper/live readiness.

## Completion

After required checks pass:

1. remove generated `__pycache__` directories;
2. stage only expected files;
3. run `git diff --cached --check`;
4. commit the implementation if repository permissions permit;
5. do not push;
6. require a clean working tree if commit succeeds.

If `.git` permissions block the commit, stop after one attempt. Report the exact expected file list and verification results. Do not retry repeatedly.

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
