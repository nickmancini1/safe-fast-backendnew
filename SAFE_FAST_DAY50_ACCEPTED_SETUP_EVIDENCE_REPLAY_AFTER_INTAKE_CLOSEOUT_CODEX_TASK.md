# SAFE-FAST Day 50 Accepted Setup Evidence Replay After Intake Closeout

## Required startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DAY50_ACCEPTED_SETUP_EVIDENCE_REPLAY_AFTER_INTAKE_RESULT.md`
2. `historical_signal_replay/results/day50_accepted_setup_evidence_replay_after_intake.json`
3. `SAFE_FAST_DAY50_ACCEPTED_COMPLETE_SETUP_EVIDENCE_INTAKE_RESULT.md`
4. `historical_signal_replay/results/day50_accepted_complete_setup_evidence_intake.json`
5. `SAFE_FAST_PROJECT_DASHBOARD.md`
6. `SAFE_FAST_PROJECT_RULE_INDEX.md`
7. `SAFE_FAST_DATA_SOURCE_REGISTRY.md`

Expected branch: `main`.

If local Git or canonical control files disagree with the accepted setup evidence replay-after-intake result, stop and report the exact conflict.

## Objective

Close out the accepted setup evidence replay-after-intake result and choose the next bounded evidence-producing task.

The current replay result is that `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` is a legitimate safety rejection, not an evidence or harness problem. It remains `SETUP_QUALIFIED`, does not reach `TRADE_CANDIDATE`, and remains a true no-trade because accepted `blocker_caution_review=fail` maps to the existing `quote_age_above_5_minutes` frozen-rule failure.

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
Do not request option data unless a candidate reaches `TRADE_CANDIDATE`.
Do not request exit data before a valid entry is established.
Do not claim profitability, proof, readiness, promotion, paper eligibility, or live eligibility.
Do not commit or push.

Do not weaken frozen rules.
Do not reopen closed setup-source candidates.
Do not replay rejected intake rows.
Do not run another open-ended candidate scan.
Do not turn rejected rows into vague missing-data cases.

## Required outputs

Create a result file and machine-readable JSON for this closeout.

Update:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`
- `SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt`

Create exactly one next grouped task based on the closeout result.

## Required tests

Run focused closeout tests, accepted setup evidence replay-after-intake tests, accepted complete setup evidence intake tests, Day 50 post-closure expansion tests, Day 50 exact setup-source closure tests, Day 50 source-resolution tests, data-source registry tests, Day 48 positive-trade funnel regression twice, relevant Ideal/CFB/Continuation/stage/session tests, contract-selection and quote-freshness tests, evidence validator, package-to-intake bridge, future-chat consistency tests, and `git diff --check`.
