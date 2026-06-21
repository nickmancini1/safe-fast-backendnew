# SAFE-FAST Day 50 Positive-Entry Trade-Candidate Rule Gap Closeout

## Required startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DAY50_POSITIVE_ENTRY_CONTRACT_SELECTED_MISSING_EVIDENCE_RESULT.md`
2. `historical_signal_replay/results/day50_positive_entry_contract_selected_missing_evidence.json`
3. `SAFE_FAST_DAY50_EVIDENCE_BACKED_POSITIVE_ENTRY_TESTING_BATCH_RESULT.md`
4. `historical_signal_replay/results/day50_evidence_backed_positive_entry_testing_batch.json`
5. `SAFE_FAST_DATA_SOURCE_REGISTRY.md`
6. `SAFE_FAST_PROJECT_DASHBOARD.md`
7. `SAFE_FAST_PROJECT_RULE_INDEX.md`

Expected branch: `main`.

If local Git or canonical control files disagree with the contract-selected missing-evidence result, stop and report the exact conflict.

## Objective

Close out the Day 50 batch's remaining `TRADE_CANDIDATE` first-blocker group using existing local fixture/source evidence first.

Do not run a new setup-source pass, do not run an open-ended candidate scan, and do not request option data for rows that remain blocked before selected-contract identity.

## Required routing

- Use the Day 50 evidence-backed positive-entry batch as the source of truth.
- Target only candidates whose first stage not reached is `TRADE_CANDIDATE`.
- Name exact blockers by field/source/dataset/schema/API/calculator/timestamp window.
- Preserve `VALID_TRADE_CAPTURED`, `TRUE_NO_TRADE`, `MISSING_DATA`, `MISSED_VALID_TRADE`, `INVALID_TRADE_ALLOWED`, and `UNRESOLVED` as separate scorecard categories.
- Preserve QQQ Clean Fast Break 001 as regression-only.
- Preserve the contract-selected closeout result: `0` additional entries from local quote-update evidence.

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
Do not request option data unless an existing candidate reaches a valid task-approved paid-data request gate and the request receives an exact cost check plus user approval.
Do not request exit data before a valid entry is established.
Do not claim profitability, proof, readiness, promotion, paper eligibility, or live eligibility.
Do not commit or push.

Do not weaken frozen rules.
Do not reopen closed setup-source candidates.
Do not replay rejected intake rows.
Do not rerun the confirmed QQQ safety rejection as a live candidate.
Do not run an open-ended candidate scan.
Do not create another governance-only chain.
Do not turn rejected rows into vague missing-data cases.

`SAFE_FAST_DB_AUTH` may be used only for exact cost checks if a valid paid-data request is created. Never print, save, document, or echo it.

## Required outputs

Create a result file and machine-readable JSON for this closeout.

Update:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`
- `SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt`

Create exactly one next grouped task based on the closeout result.

## Required tests

Run focused closeout tests, Day 50 contract-selected missing-evidence closeout tests, Day 50 selected-contract blocker closeout tests, Day 50 evidence-backed positive-entry batch tests, accepted setup evidence replay-after-intake closeout tests, accepted setup evidence replay-after-intake tests, accepted complete setup evidence intake tests, Day 50 post-closure expansion tests, Day 50 exact setup-source closure tests, Day 50 source-resolution tests, data-source registry tests, Day 48 positive-trade funnel regression twice, relevant Ideal/CFB/Continuation/stage/session tests, contract-selection and quote-freshness tests, evidence validator, package-to-intake bridge, future-chat consistency tests, and `git diff --check`.
