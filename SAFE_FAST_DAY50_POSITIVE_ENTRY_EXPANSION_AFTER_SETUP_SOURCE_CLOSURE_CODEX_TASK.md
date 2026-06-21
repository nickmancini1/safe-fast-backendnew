# SAFE-FAST Day 50 Positive-Entry Expansion After Setup-Source Closure

## Required startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DAY50_EXACT_SETUP_SOURCE_EVIDENCE_COMPLETION_RESULT.md`
2. `historical_signal_replay/results/day50_exact_setup_source_evidence_completion.json`
3. `SAFE_FAST_DAY50_GROUPED_REQUIRED_SETUP_SOURCE_RESOLUTION_AND_REPLAY_RESULT.md`
4. `historical_signal_replay/results/day50_required_setup_source_resolution.json`
5. `SAFE_FAST_DATA_SOURCE_REGISTRY.md`
6. `historical_signal_replay/config/safe_fast_data_source_registry.json`
7. `SAFE_FAST_PROJECT_DASHBOARD.md`
8. `SAFE_FAST_PROJECT_RULE_INDEX.md`
9. Existing positive-entry expansion, replay, evidence, validator, contract-selection, quote-freshness, package-to-intake bridge, and future-chat consistency tests.

Expected branch: `main`.

If local Git or canonical control files disagree with the Day 50 setup-source closure result, stop and report the exact conflict.

## Objective

Run the next positive-entry expansion only after the current Day 50 setup-source slots have been resolved or closed.

Use existing SAFE-FAST candidate selection controls. Do not resurrect the four closed setup-source candidates unless a later bounded task provides exact accepted setup-source evidence first.

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

`SAFE_FAST_DB_AUTH` may be used only for exact cost checks if a valid paid-data request is created. Never print, save, document, or echo it.

## Required outputs

Create a result file and machine-readable JSON for this task.

Update:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`
- `SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt`

Create exactly one next grouped task based on the result.

## Required tests

Run focused expansion tests, Day 50 exact setup-source closure tests, Day 50 source-resolution tests, data-source registry tests, Day 48 positive-trade funnel regression twice, relevant Ideal/CFB/Continuation/stage/session tests, contract-selection and quote-freshness tests, evidence validator, package-to-intake bridge, future-chat consistency tests, and `git diff --check`.
