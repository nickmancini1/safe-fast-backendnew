# SAFE-FAST Day 50 Evidence-Backed Positive-Entry Testing Batch

## Required startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DAY50_ACCEPTED_SETUP_EVIDENCE_REPLAY_AFTER_INTAKE_CLOSEOUT_RESULT.md`
2. `historical_signal_replay/results/day50_accepted_setup_evidence_replay_after_intake_closeout.json`
3. `SAFE_FAST_DAY50_ACCEPTED_SETUP_EVIDENCE_REPLAY_AFTER_INTAKE_RESULT.md`
4. `historical_signal_replay/results/day50_accepted_setup_evidence_replay_after_intake.json`
5. `SAFE_FAST_DAY50_ACCEPTED_COMPLETE_SETUP_EVIDENCE_INTAKE_RESULT.md`
6. `historical_signal_replay/results/day50_accepted_complete_setup_evidence_intake.json`
7. `SAFE_FAST_DAY48_POSITIVE_TRADE_CAPTURE_AND_MISS_ANALYSIS_RESULT.md`
8. `historical_signal_replay/results/day48_positive_trade_capture_funnel.json`
9. `SAFE_FAST_PROJECT_DASHBOARD.md`
10. `SAFE_FAST_PROJECT_RULE_INDEX.md`
11. `SAFE_FAST_DATA_SOURCE_REGISTRY.md`

Expected branch: `main`.

If local Git or canonical control files disagree with the closeout result, stop and report the exact conflict.

## Objective

Run the next bounded positive-entry testing batch using existing evidence-backed candidates and regression controls only.

The confirmed QQQ safety rejection is closed as regression-only. Do not reopen it as a candidate. Preserve it only as a true no-trade regression anchor.

## Required routing

Use evidence-backed positive-entry inputs before any new setup-source or governance pass:

- include existing positive-entry regression controls;
- preserve `VALID_TRADE_CAPTURED`, `TRUE_NO_TRADE`, `MISSING_DATA`, `MISSED_VALID_TRADE`, `INVALID_TRADE_ALLOWED`, and `UNRESOLVED` as separate scorecard categories;
- select only candidates with repo-backed setup evidence sufficient for the stage being tested;
- report exact blockers by field/source/dataset/schema/API/calculator/timestamp window when a candidate cannot advance.

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

Do not weaken frozen rules.
Do not reopen closed setup-source candidates.
Do not replay rejected intake rows.
Do not rerun the confirmed QQQ safety rejection as a live candidate.
Do not run an open-ended candidate scan.
Do not create another governance-only chain.
Do not turn rejected rows into vague missing-data cases.

`SAFE_FAST_DB_AUTH` may be used only for exact cost checks if a valid paid-data request is created. Never print, save, document, or echo it.

## Required outputs

Create a result file and machine-readable JSON for this testing batch.

Update:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`
- `SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt`

Create exactly one next grouped task based on the batch result.

## Required tests

Run focused batch tests, closeout tests, accepted setup evidence replay-after-intake tests, accepted complete setup evidence intake tests, Day 50 post-closure expansion tests, Day 50 exact setup-source closure tests, Day 50 source-resolution tests, data-source registry tests, Day 48 positive-trade funnel regression twice, relevant Ideal/CFB/Continuation/stage/session tests, contract-selection and quote-freshness tests, evidence validator, package-to-intake bridge, future-chat consistency tests, and `git diff --check`.
