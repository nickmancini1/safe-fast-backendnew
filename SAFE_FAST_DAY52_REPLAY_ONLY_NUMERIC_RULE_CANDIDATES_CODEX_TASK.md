# SAFE-FAST Day 52 Replay-Only Numeric Rule Candidates

Read `SAFE_FAST_BUILD_STATE.md` first.

The local repository is the only source of truth.

Use bounded reads. Do not begin with broad repository-wide scans.

## Current blocker

The accepted full-session replay has six exact unresolved fields:

- Ideal trigger
- Ideal invalidation
- Clean Fast Break trigger
- Clean Fast Break invalidation
- Continuation trigger
- Continuation invalidation

No accepted numeric values currently exist.

## Objective

Build and test a replay-only numeric rule candidate layer that produces actual trigger and invalidation values for all three setup families.

This is research evidence, not a frozen trading-rule promotion.

Do not overwrite the accepted unresolved blockers. Keep provisional results separate and clearly marked:

`PROVISIONAL_REPLAY_ONLY`

## Required reads

Read these first:

1. `SAFE_FAST_BUILD_STATE.md`
2. `SAFE_FAST_NEXT_CHAT_HANDOFF_START_HERE.md`
3. `SAFE_FAST_DAY52_NUMERIC_TRIGGER_INVALIDATION_RESULT.md`
4. `historical_signal_replay/day52_numeric_trigger_invalidation.py`
5. `historical_signal_replay/day52_full_session_recognition_manifest.py`
6. `historical_signal_replay/results/day52_numeric_trigger_invalidation.json`
7. `historical_signal_replay/results/day52_full_session_setup_time_review.json`
8. `tests/test_day52_numeric_trigger_invalidation.py`
9. `tests/test_day52_full_session_recognition_manifest.py`
10. the three accepted March 16, 2026 setup-time packages
11. directly referenced mapper and candidate-pipeline files
12. directly referenced frozen `patch8` setup definitions

## Candidate rules

Implement only structural candidates using information available through the setup-time cutoff.

Do not add:

- ATR offsets
- percentage offsets
- tick buffers
- volatility multipliers
- optimized thresholds
- discretionary tolerances

### Candidate A: setup-bar range

For bullish direction:

- trigger = setup-time bar high
- invalidation = setup-time bar low

For bearish direction:

- trigger = setup-time bar low
- invalidation = setup-time bar high

### Candidate B: setup-structure range

Use an already identified setup structure when available through the cutoff.

- Ideal: accepted signal/setup structure boundary
- Clean Fast Break: accepted base or initial-break structure boundary
- Continuation: accepted pullback or continuation-base boundary

For bullish direction:

- trigger = upper structure boundary
- invalidation = lower structure boundary

For bearish direction:

- trigger = lower structure boundary
- invalidation = upper structure boundary

### Candidate C: named level

Where an accepted package or mapper already contains an explicit breakout, reclaim, resistance, support, pivot, or base level:

- trigger = the named directional level
- invalidation = the opposite accepted structure boundary

Do not create a named level from future bars.

## Candidate priority

Use this fixed priority without looking at later price performance:

1. existing explicit named level;
2. existing accepted structure boundary;
3. setup-time bar range.

Do not choose a candidate because it later made money or produced favorable movement.

## Required provenance

Every numeric value must record:

- setup family
- direction
- candidate rule ID
- provisional status
- source timestamp
- source row
- source field
- source value
- calculation
- final numeric value
- comparison operator
- information cutoff
- future-row exclusion proof

## Known setups

Produce actual provisional trigger and invalidation values for:

- Ideal
- Clean Fast Break
- Continuation

Each family must produce at least Candidate A when its setup-time OHLCV row and direction exist.

If Candidate B or C cannot be produced, report the exact missing structural field.

## Full-session replay

Run the complete March 16, 2026 SPY session.

Do not restrict processing to the three known windows.

Report separately for every candidate rule and setup family:

- records evaluated
- numeric pairs produced
- blocked records
- setup-qualified under provisional mode
- duplicates
- suppressed records
- selected winners
- recognition-layer executable records
- illegal transitions
- no-hindsight violations

Keep accepted-mode counts separate from provisional-mode counts.

## Trigger observation

After constructing values strictly from setup-time evidence, replay later bars only to report:

- trigger observed after cutoff
- invalidation observed after cutoff
- which occurred first
- neither observed

This is descriptive replay evidence only.

Do not use this outcome to construct or select the numeric rule.

Do not calculate option P&L.

## Required outputs

Produce:

- focused replay-only implementation
- machine-readable JSON result
- focused result document
- validator
- focused tests
- updated provisional full-session manifest or clearly separate provisional manifest
- compact setup-time review with post-cutoff fields excluded

Do not create a second competing production engine.

## Required tests

Add tests for:

- actual numeric Candidate A values for all three families
- Candidate B structural provenance where available
- Candidate C named-level provenance where available
- bullish calculations
- bearish calculations
- future-row rejection
- post-cutoff mutation invariance
- finite values
- trigger/invalidation directional validity
- candidate priority independent of future performance
- accepted and provisional modes remain separate
- no-hindsight behavior
- strict no-trade behavior
- stage-transition protection
- session-boundary behavior
- carry-forward behavior
- duplicate suppression
- stable winner selection
- replay chunking invariance
- candidate-order invariance
- deterministic reruns
- complete-session opportunity accounting

Run relevant Day 50, Day 51, and Day 52 bounded regressions.

Run affected validators.

Run:

`powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`

Run:

`git diff --check`

## Canonical state

Update only factual current-state sections whose state changed:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`
- `SAFE_FAST_NEXT_CHAT_HANDOFF_START_HERE.md`

State clearly:

- accepted numeric rules remain unresolved unless separately proven;
- provisional replay-only numeric candidates now exist;
- provisional replay results are not profitability proof;
- exact next decision needed to promote or reject a candidate;
- profitability proof: `NO`;
- paper/live eligibility: `NO`.

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

Do not download or purchase data.

Do not perform option selection, fills, exits, or P&L.

Do not claim profitability or paper/live readiness.

## Completion

Remove generated `__pycache__` directories.

Do not run `git add` or `git commit` inside the Codex sandbox.

Finish with:

- `READY_FOR_OPERATOR_COMMIT`
- exact changed/untracked files
- actual provisional values for all three families
- candidate rule used for each value
- accepted-mode counts
- provisional-mode counts
- tests and validators passed
- exact promotion decision still required
- profitability proof: `NO`
- paper/live eligibility: `NO`
