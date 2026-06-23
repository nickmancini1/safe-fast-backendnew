# SAFE-FAST Day 52 Numeric Trigger and Invalidation Implementation

Read `SAFE_FAST_BUILD_STATE.md` before touching any engine or replay logic.

The local repository is the only source of truth.

Use bounded file reads. Do not begin with broad repository-wide file scans.

## Baseline

Expected starting implementation baseline:

- Day 52 full-session recognition manifest committed
- one SPY March 16, 2026 session
- 751 chronological source rows
- 390 unique timestamps
- 2,253 recognition records
- all three known setup records blocked by `numeric_trigger_and_invalidation_missing`
- profitability proof: `NO`
- paper/live eligibility: `NO`

Verify the real branch, HEAD, status, files, and results before acting.

## Required reads

Read these first:

1. `SAFE_FAST_BUILD_STATE.md`
2. `SAFE_FAST_NEXT_CHAT_HANDOFF_START_HERE.md`
3. `SAFE_FAST_PROJECT_DASHBOARD.md`
4. `SAFE_FAST_PROJECT_RULE_INDEX.md`
5. `SAFE_FAST_DAY51_SPY_NUMERIC_SETUP_AND_OPRA_COST_CHECK_RESULT.md`
6. `historical_signal_replay/day51_spy_numeric_setup_and_opra_cost_check.py`
7. `tests/test_day51_spy_numeric_setup_and_opra_cost_check.py`
8. `watcher_foundation/day51_spy_numeric_setup_and_opra_cost_check_validator.py`
9. `SAFE_FAST_DAY52_FULL_SESSION_RECOGNITION_MANIFEST_RESULT.md`
10. `historical_signal_replay/day52_full_session_recognition_manifest.py`
11. `historical_signal_replay/results/day52_full_session_recognition_manifest.json`
12. `historical_signal_replay/results/day52_full_session_setup_time_review.json`
13. `tests/test_day52_full_session_recognition_manifest.py`
14. `watcher_foundation/day52_full_session_recognition_manifest_validator.py`

Follow direct references from those files to the accepted mapper, candidate pipeline, candidate packets, frozen `patch8` rules, and source data.

## Objective

Implement the accepted, deterministic, no-hindsight path that converts setup-time SPY OHLCV evidence into numeric:

- trigger
- invalidation

for:

- Ideal
- Clean Fast Break
- Continuation

Integrate the result into the existing Day 52 full-session recognition manifest.

Do not create a separate competing recognition engine.

## Rule-source discipline

Do not invent thresholds, buffers, offsets, tolerances, or structural definitions.

For every numeric value, record:

- setup family
- direction
- rule identifier
- existing source file or frozen rule supporting it
- source bar timestamp
- source field
- source value
- calculation
- final numeric value
- comparison operator
- no-hindsight cutoff

Reuse existing accepted `patch8`, mapper, candidate-pipeline, and Day 51 numeric behavior wherever it already defines the rule.

If a family genuinely lacks an accepted rule, return a family-specific machine-readable blocker such as:

`NUMERIC_RULE_UNRESOLVED_<FAMILY>_<FIELD>`

Do not use one blanket blocker when some fields or families can be completed.

## Required behavior

Create or extend family-specific deterministic constructors.

Each constructor must:

1. accept only evidence observable through the setup-time cutoff;
2. reject future rows;
3. calculate trigger and invalidation independently of future price movement;
4. preserve the exact source rows and fields;
5. return stable reason codes;
6. return the same result across repeated runs and replay chunking;
7. block rather than guess when required evidence is absent or ambiguous.

Numeric values must be finite and directionally valid under the accepted family rule.

A setup may advance to `setup-qualified` only when all existing required fields pass:

- setup-time row
- numeric trigger
- numeric invalidation
- freshness/final-signal state
- blocker/caution review
- session-boundary behavior
- no-hindsight boundary

Illegal stage skipping must fail validation.

## Known setup requirement

Process the three established March 16, 2026 setup-time packages separately:

- Ideal
- Clean Fast Break
- Continuation

For each one, produce either:

- exact trigger and invalidation values with rule provenance; or
- one exact family-and-field-specific unresolved-rule blocker.

Do not leave `numeric_trigger_and_invalidation_missing` as the final result when local accepted evidence supports a more exact result.

## Full-session rerun

Rerun the complete 751-row session through the updated recognition path.

Report by setup family:

- records evaluated
- rejected
- developing
- duplicates
- suppressed
- blocked by exact reason
- setup-qualified
- selected winners
- recognition-layer executable

Do not limit evaluation to the three known windows.

Do not use future favorable movement to decide which records deserve numeric fields.

## Recognition/economic separation

This task is recognition-layer work only.

Do not require OPRA evidence to calculate underlying trigger and invalidation.

Do not perform:

- option selection
- option fills
- option exits
- option P&L
- sizing
- profitability claims

Missing OPRA evidence may block later economic stages only.

## Required evidence outputs

Produce concrete implementation and evidence:

- focused numeric trigger/invalidation implementation
- machine-readable JSON result
- focused result document
- validator
- focused tests
- updated full-session manifest
- updated setup-time review output with future fields excluded

Reuse existing files where appropriate instead of duplicating logic.

## Required tests

Add focused tests covering:

- exact Ideal trigger construction
- exact Ideal invalidation construction
- exact Clean Fast Break trigger construction
- exact Clean Fast Break invalidation construction
- exact Continuation trigger construction
- exact Continuation invalidation construction
- source-rule provenance
- future-row rejection
- mutation of post-cutoff bars does not change setup-time values
- missing-source-field blocker
- ambiguous-evidence blocker
- finite numeric values
- direction-valid trigger/invalidation relationship
- legal setup-qualified transition
- illegal stage skipping
- no-hindsight cutoff
- session-boundary protection
- carry-forward protection
- stale/spent protection
- no-trade protection
- duplicate suppression
- stable winner selection
- replay chunking invariance
- candidate-order invariance
- deterministic reruns
- all three setup families in full-session replay

Run the relevant existing Day 50, Day 51, and Day 52 bounded regressions.

Run affected validators.

Run:

`powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`

Run:

`git diff --check`

Do not run unrelated broad test suites.

## Canonical-state audit

Audit existing canonical files before updating them.

Update only factual state that changed:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`
- `SAFE_FAST_NEXT_CHAT_HANDOFF_START_HERE.md`

Do not duplicate historical explanations.

Correct stale active-objective or blocker statements.

The handoff must explicitly state:

- verified baseline
- what is fixed
- what remains unproven
- current setup-qualified counts by family
- exact remaining numeric blockers
- active next objective
- profitability proof: `NO`
- paper/live eligibility: `NO`

Preserve these project improvements where not already represented:

- complete-session opportunity accounting
- machine-enforced stage contracts
- recognition/economic separation
- strict no-hindsight timing
- deterministic duplicate and winner behavior
- reproducibility metadata
- compact canonical current state
- untouched holdout required before profitability claims

Do not create another planning-only document.

## Guardrails

Do not modify:

- `main.py`
- production/live backend
- Railway/deploy
- broker/account/order/fill/alert code
- credentials, secrets, tokens, or `.env`
- sizing
- frozen `patch8` thresholds

Do not buy or download data.

Do not claim profitability, paper eligibility, or live eligibility.

## Completion behavior

Remove generated `__pycache__` directories.

Do not attempt `git add` or `git commit` from the Codex sandbox. The operator will commit after reviewing the exact batch.

Finish by reporting:

- `READY_FOR_OPERATOR_COMMIT: YES` or `NO`
- exact changed and untracked files
- tests passed
- validators passed
- full-session counts by family
- exact trigger and invalidation for each known setup, or exact unresolved blocker
- exact remaining blockers
- profitability proof: `NO`
- paper/live eligibility: `NO`
