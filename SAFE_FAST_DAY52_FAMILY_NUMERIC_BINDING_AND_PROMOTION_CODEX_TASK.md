# SAFE-FAST Day 52 Family Numeric Binding and Promotion

Read `SAFE_FAST_BUILD_STATE.md` first.

The local repository is the only source of truth.

Use bounded reads and targeted searches. Do not begin with a broad repository-wide `rg --files` scan.

## Current proven state

A separate `PROVISIONAL_REPLAY_ONLY` package produced:

- Ideal: trigger 668.36, invalidation 667.87
- Clean Fast Break: trigger 668.36, invalidation 667.87
- Continuation: trigger 668.36, invalidation 667.87

All three used `CANDIDATE_A_SETUP_BAR_RANGE`.

Accepted numeric rules remain:

- established: 0
- unresolved: 6

The identical values across all three setup families require an immediate binding and provenance audit before any promotion.

## Objective

Audit and correct the setup-time row binding for Ideal, Clean Fast Break, and Continuation.

Then implement, test, and decide the accepted numeric trigger and invalidation rule separately for each family.

Do not stop with another planning-only result when local evidence supports implementation.

## Required reads

Read these first:

1. `SAFE_FAST_BUILD_STATE.md`
2. `SAFE_FAST_NEXT_CHAT_HANDOFF_START_HERE.md`
3. `SAFE_FAST_DAY52_REPLAY_ONLY_NUMERIC_RULE_CANDIDATES_RESULT.md`
4. `SAFE_FAST_DAY52_NUMERIC_TRIGGER_INVALIDATION_RESULT.md`
5. `SAFE_FAST_DAY52_FULL_SESSION_RECOGNITION_MANIFEST_RESULT.md`
6. `historical_signal_replay/day52_replay_only_numeric_rule_candidates.py`
7. `historical_signal_replay/day52_numeric_trigger_invalidation.py`
8. `historical_signal_replay/day52_full_session_recognition_manifest.py`
9. the three accepted March 16, 2026 setup-time packages
10. directly referenced mapper and candidate-pipeline results
11. directly referenced frozen `patch8` setup definitions
12. the affected Day 50, Day 51, and Day 52 tests and validators

## First required audit

For each family, identify and report:

- candidate/package ID
- expected opportunity timestamp
- actual bound setup-time timestamp
- source row index
- OHLCV values
- direction
- no-hindsight cutoff
- code path that selected the row

Determine whether the identical values are:

1. legitimate because the three labels intentionally share one setup-time row; or
2. a binding defect that reused one row across distinct opportunities.

The previously mapped Ideal, Clean Fast Break, and Continuation opportunities must not silently collapse onto one row.

If binding is wrong, fix it before evaluating numeric rules.

Add a regression proving that each family binds to its intended package and timestamp.

## Family-specific numeric decision

Evaluate Candidate A separately for each family.

Candidate A:

For bullish setups:

- trigger = correctly bound setup-time bar high
- invalidation = correctly bound setup-time bar low

For bearish setups:

- trigger = correctly bound setup-time bar low
- invalidation = correctly bound setup-time bar high

Candidate A may be promoted for a family only when:

- the setup-time row is correctly bound;
- its high/low represents the accepted family structure;
- required evidence existed by the cutoff;
- positive and negative regression cases pass;
- no future outcome influenced the decision;
- stage-transition and no-trade protections pass.

Do not assume that one rule must be promoted for all three families.

## Structural alternatives

Where Candidate A is not semantically correct, use an existing accepted structural field if available:

- Ideal: accepted ideal signal or setup structure boundary
- Clean Fast Break: accepted base, break, or higher-base boundary
- Continuation: accepted pullback or continuation-base boundary

Do not add buffers, offsets, percentages, ATR values, volatility multipliers, or optimized thresholds.

Do not derive a rule from favorable later movement.

If a required structural field is not currently emitted, implement the smallest deterministic no-hindsight extraction from existing setup evidence.

Only leave an unresolved blocker when the local evidence genuinely cannot define the field.

## Required decision for each family

Produce one outcome:

- `PROMOTE_CANDIDATE_A`
- `PROMOTE_EXISTING_STRUCTURAL_RULE`
- `REVISE_AND_IMPLEMENT`
- `REJECT_WITH_EXACT_BLOCKER`

For every promoted or revised rule, record:

- family
- direction
- rule ID
- rule source
- setup-time timestamp
- source row and field
- calculation
- numeric trigger
- numeric invalidation
- comparison operators
- no-hindsight cutoff
- regression cases
- accepted status

## Accepted-mode integration

For every family with an accepted rule:

- remove its unresolved numeric blocker;
- integrate the rule into the accepted numeric constructor;
- integrate it into the accepted full-session manifest;
- enforce all setup-qualified predicates;
- rerun the complete 751-row March 16, 2026 SPY session;
- report accepted-mode counts separately by family;
- preserve deterministic duplicate suppression and winner selection.

Do not convert provisional status into accepted status by renaming fields.

## Required tests

Add focused tests for:

- intended setup timestamp for Ideal
- intended setup timestamp for Clean Fast Break
- intended setup timestamp for Continuation
- no cross-family setup-row reuse
- legitimate overlap behavior, if overlap is proven
- family-specific trigger construction
- family-specific invalidation construction
- source provenance
- positive regression cases
- negative regression cases
- future-row rejection
- post-cutoff mutation invariance
- exact stage-transition requirements
- illegal stage skipping
- session-boundary protection
- carry-forward protection
- stale/spent protection
- no-trade protection
- duplicate suppression
- stable winner selection
- replay chunking invariance
- candidate-order invariance
- deterministic reruns
- full-session accepted-mode counts
- accepted and provisional modes remain separate

Run relevant bounded Day 50, Day 51, and Day 52 regressions.

Run affected validators.

Run:

`powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`

Run:

`git diff --check`

## Required outputs

Produce:

- focused implementation
- machine-readable result
- focused result document
- validator
- focused tests
- updated accepted full-session manifest
- updated setup-time review
- explicit family-by-family decision matrix

Update only factual current-state sections of:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`
- `SAFE_FAST_NEXT_CHAT_HANDOFF_START_HERE.md`

The handoff must preserve:

- complete-session opportunity accounting
- machine-enforced stage contracts
- recognition/economic separation
- no-hindsight timing
- deterministic duplicate and winner behavior
- reproducibility metadata
- untouched holdout requirement
- exact profitability and paper/live status

Do not create another broad planning document.

## Guardrails

Do not modify:

- `main.py`
- production/live backend
- Railway/deploy
- broker/account/order/fill/alert code
- credentials, secrets, tokens, or `.env`
- sizing
- frozen `patch8` thresholds

Do not purchase or download data.

Do not perform option selection, fills, exits, or P&L.

Do not claim profitability, paper eligibility, or live eligibility.

## Completion

Remove generated `__pycache__` directories.

Do not run `git add` or `git commit` inside the Codex sandbox.

Finish with:

- `READY_FOR_OPERATOR_COMMIT`
- exact changed/untracked files
- binding audit result for each family
- exact setup-time timestamp for each family
- family-by-family promotion decision
- accepted trigger and invalidation values, where established
- accepted-mode full-session counts
- tests and validators passed
- exact remaining blockers
- profitability proof: `NO`
- paper/live eligibility: `NO`
