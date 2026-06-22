# SAFE-FAST Day 50 Review-Only Package to Candidate Contract Task

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_ACCEPTED_SETUP_REPLAY_MAPPER_RESULT.md`
2. `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_MAPPER_TO_GENERATION_RETRY_RESULT.md`
3. `historical_signal_replay/results/day50_raw_data_positive_entry_accepted_setup_replay_mapper.json`
4. `historical_signal_replay/results/day50_raw_data_positive_entry_mapper_to_generation_retry.json`
5. Existing generation/intake/backtest modules and tests relevant to raw-data positive-entry generation

## Objective

Implement the smallest bounded contract that can promote accepted review-only setup-time packages into generated candidates when, and only when, the package contains all evidence required by the existing generation path.

This is not a planning-only task.

## Required work

1. Define the exact contract between:
   - accepted mapper package
   - generated candidate
   - setup-qualified candidate

2. Process the three March 16, 2026 SPY packages separately:
   - Ideal
   - Clean Fast Break
   - Continuation

3. For each setup family, produce one of these exact outcomes:
   - generated_candidate_created
   - setup_qualified_created
   - trade_candidate_created
   - selected_contract_created
   - eligible_entry_created
   - recorded_entry_created
   - rejected_with_exact_contract_gap

4. If a generated candidate can be created, continue through the existing local funnel as far as evidence permits.

5. If trade-candidate or selected-contract is reached, immediately run the existing local costed entry/exit replay or backtest path where exact local evidence exists.

6. If option evidence or exit-path evidence is missing, do not guess and do not download. Produce one grouped exact evidence request with:
   - setup family
   - symbol
   - contract if known
   - timestamp window
   - source/dataset/schema needed
   - exact field missing
   - whether it blocks entry, exit, costs, or P&L

## Guardrails

Do not loosen thresholds to force a candidate.

Do not convert review-only packages into candidates unless the contract is satisfied.

Do not mix the three SPY opportunities with preserved regression controls.

Preserve:

- no-hindsight boundaries
- setup-time boundaries
- developing-stage transitions
- session-boundary and carry-forward rules
- stable winner selection
- stale/spent rejection
- blocker rejection
- freshness rules
- no-trade behavior

Do not touch:

- `main.py`
- production/live backend
- Railway/deploy files
- broker/account/order/alert code
- credentials, secrets, tokens, or `.env`
- frozen `patch8` thresholds
- paid-data downloads

## Required tests

Create focused tests covering:

- Ideal package-to-candidate contract
- Clean Fast Break package-to-candidate contract
- Continuation package-to-candidate contract
- contract rejection with exact missing fields
- no-hindsight preservation
- session-boundary preservation
- stable winner selection
- no-trade preservation
- unchanged 17 mapper regression cases
- unchanged mapper-to-generation retry controls

Run the relevant batch:

- new contract tests
- mapper tests
- mapper-to-generation retry tests
- raw-data positive-entry generation tests
- Day 51 handoff consistency test
- mapper validator
- retry validator
- safe checks with `-ExecutionPolicy Bypass`
- `git diff --check`

## Outputs

Create:

- `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_REVIEW_ONLY_PACKAGE_TO_CANDIDATE_CONTRACT_RESULT.md`
- machine-readable JSON result under `historical_signal_replay/results/`
- focused implementation file
- focused validator file
- focused tests

Update:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`
- `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`
- `SAFE_FAST_DATA_SOURCE_REGISTRY.md`
- `SAFE_FAST_NEXT_CHAT_HANDOFF_START_HERE.md`
- Day 51 handoff consistency test if required

Final summary must include:

- per-setup stage reached
- whether any generated candidate was created
- whether any setup-qualified candidate was created
- whether any trade candidate was created
- whether any selected contract was created
- whether any costed backtest was possible
- exact remaining blocker per setup
- tests run
- files changed
- exact next substantive action