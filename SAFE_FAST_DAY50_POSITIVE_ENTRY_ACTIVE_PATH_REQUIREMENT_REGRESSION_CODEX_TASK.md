# SAFE-FAST Day 50 Positive-Entry Active-Path Requirement Regression

## Required startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DAY50_POSITIVE_ENTRY_REMAINING_EVIDENCE_GAP_CLOSEOUT_RESULT.md`
2. `historical_signal_replay/results/day50_positive_entry_remaining_evidence_gap_closeout.json`
3. `SAFE_FAST_DAY50_POSITIVE_ENTRY_ACTIVE_PATH_RULE_EVIDENCE_REPAIR_RESULT.md`
4. `historical_signal_replay/results/day50_positive_entry_active_path_rule_evidence_repair.json`
5. `SAFE_FAST_DATA_SOURCE_REGISTRY.md`
6. `SAFE_FAST_PROJECT_DASHBOARD.md`
7. `SAFE_FAST_PROJECT_RULE_INDEX.md`

Expected branch: `main`.

If local Git or canonical control files disagree with the remaining evidence-gap closeout result, stop and report the exact conflict.

## Objective

Create the next bounded grouped active-path requirement regression package from existing local fixture/source evidence only.

Use the remaining evidence-gap closeout result as the source of truth. The open group is exactly the four active-path requirements that still block `TRADE_CANDIDATE` before selected-contract identity:

- GLD Clean Fast Break `fresh_or_spent_unconfirmed`
- GLD Ideal `fresh_or_spent_unconfirmed`
- IWM Continuation `prior_completed_shelf_break_spent_TO_REVIEW`
- IWM Ideal `fresh_or_spent_unconfirmed`

## Required routing

- Do not run a new setup-source pass.
- Do not run an open-ended candidate scan.
- Do not request option data.
- Do not request exit data.
- Preserve QQQ Clean Fast Break 001 as regression-only.
- Preserve QQQ Ideal as outside the narrowed Ideal path unless source-backed active-path evidence and regression cases explicitly repair it.
- Preserve the contract-selected closeout result: `0` additional entries from local quote-update evidence.
- Name exact blockers by field/source/dataset/schema/API/calculator/timestamp window.
- Preserve `VALID_TRADE_CAPTURED`, `TRUE_NO_TRADE`, `MISSING_DATA`, `MISSED_VALID_TRADE`, `INVALID_TRADE_ALLOWED`, and `UNRESOLVED` as separate scorecard categories.

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
Do not request option data.
Do not request exit data.
Do not claim profitability, proof, readiness, promotion, paper eligibility, or live eligibility.
Do not commit or push.

Do not weaken frozen rules.
Do not reopen closed setup-source candidates.
Do not replay rejected intake rows.
Do not rerun the confirmed QQQ safety rejection as a live candidate.
Do not run an open-ended candidate scan.
Do not create another governance-only chain.
Do not turn rejected rows into vague missing-data cases.

## Required outputs

Create a result file and machine-readable JSON for this active-path requirement regression package.

Update:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`
- `SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt`

Create exactly one next grouped task based on the regression result.

## Required tests

Run focused active-path requirement regression tests, remaining evidence-gap closeout tests, active-path rule/evidence repair tests, Day 50 trade-candidate rule-gap closeout tests, Day 50 contract-selected missing-evidence closeout tests, Day 50 selected-contract blocker closeout tests, Day 50 evidence-backed positive-entry batch tests, accepted setup evidence replay-after-intake closeout tests, accepted setup evidence replay-after-intake tests, accepted complete setup evidence intake tests, Day 50 post-closure expansion tests, Day 50 exact setup-source closure tests, Day 50 source-resolution tests, data-source registry tests, Day 48 positive-trade funnel regression twice, relevant Ideal/CFB/Continuation/stage/session tests, contract-selection and quote-freshness tests, evidence validator, package-to-intake bridge, future-chat consistency tests, and `git diff --check`.
