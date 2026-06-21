# SAFE-FAST Day 50 Accepted Complete Setup Evidence Intake

## Required startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DAY50_POSITIVE_ENTRY_EXPANSION_AFTER_SETUP_SOURCE_CLOSURE_RESULT.md`
2. `historical_signal_replay/results/day50_positive_entry_expansion_after_setup_source_closure.json`
3. `SAFE_FAST_DAY50_EXACT_SETUP_SOURCE_EVIDENCE_COMPLETION_RESULT.md`
4. `historical_signal_replay/results/day50_exact_setup_source_evidence_completion.json`
5. `SAFE_FAST_DATA_SOURCE_REGISTRY.md`
6. `historical_signal_replay/config/safe_fast_data_source_registry.json`
7. `SAFE_FAST_PROJECT_DASHBOARD.md`
8. `SAFE_FAST_PROJECT_RULE_INDEX.md`

Expected branch: `main`.

If local Git or canonical control files disagree with the Day 50 post-closure expansion result, stop and report the exact conflict.

## Objective

Intake or validate only exact accepted, complete setup evidence for future positive-entry expansion.

Do not select a candidate unless the evidence is already accepted and complete for setup-time row, trigger, invalidation, freshness/final-signal state, blocker/caution review, no-hindsight boundary, and session-boundary behavior when applicable.

Closed setup-source candidates may be listed only as regression records unless this task finds a later bounded artifact that explicitly provides exact accepted setup-source evidence for that same candidate.

## Restrictions

Do not modify:

- `main.py`
- Railway/deploy files
- broker/account/order code
- credentials
- `.env`
- frozen trading thresholds
- production/live backend

Do not authenticate to Schwab.
Do not download data.
Do not request option data before a candidate reaches `TRADE_CANDIDATE`.
Do not request exit data before a valid entry is established.
Do not claim profitability, proof, readiness, promotion, paper eligibility, or live eligibility.
Do not commit or push.

Do not create another vague missing-data batch. If no accepted complete setup evidence exists, report zero intake-ready candidates and stop with an exact next action.

## Required outputs

Create a result file and machine-readable JSON for this task.

Update:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`
- `SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt`

Create exactly one next grouped task based on the result.

## Required tests

Run focused intake tests, Day 50 post-closure expansion tests, Day 50 exact setup-source closure tests, Day 50 source-resolution tests, data-source registry tests, Day 48 positive-trade funnel regression twice, relevant Ideal/CFB/Continuation/stage/session tests, contract-selection and quote-freshness tests, evidence validator, package-to-intake bridge, future-chat consistency tests, and `git diff --check`.
