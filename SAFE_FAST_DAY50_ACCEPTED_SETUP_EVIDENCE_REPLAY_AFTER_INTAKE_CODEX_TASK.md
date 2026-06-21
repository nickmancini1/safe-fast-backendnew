# SAFE-FAST Day 50 Accepted Setup Evidence Replay After Intake

## Required startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DAY50_ACCEPTED_COMPLETE_SETUP_EVIDENCE_INTAKE_RESULT.md`
2. `historical_signal_replay/results/day50_accepted_complete_setup_evidence_intake.json`
3. `SAFE_FAST_DAY50_POSITIVE_ENTRY_EXPANSION_AFTER_SETUP_SOURCE_CLOSURE_RESULT.md`
4. `historical_signal_replay/results/day50_positive_entry_expansion_after_setup_source_closure.json`
5. `SAFE_FAST_DAY50_EXACT_SETUP_SOURCE_EVIDENCE_COMPLETION_RESULT.md`
6. `historical_signal_replay/results/day50_exact_setup_source_evidence_completion.json`
7. `SAFE_FAST_DATA_SOURCE_REGISTRY.md`
8. `SAFE_FAST_PROJECT_DASHBOARD.md`
9. `SAFE_FAST_PROJECT_RULE_INDEX.md`

Expected branch: `main`.

If local Git or canonical control files disagree with the Day 50 accepted complete setup evidence intake result, stop and report the exact conflict.

## Objective

Replay the accepted complete setup-evidence intake result through the positive-entry gate.

Use only the ingested accepted setup-evidence record(s). Do not run another open-ended candidate scan.

The current accepted intake record is `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`. It has accepted complete setup evidence, but its accepted blocker/caution review is `fail`, so it must not become a trade candidate unless the replay proves an existing accepted rule says otherwise.

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

Do not reopen closed setup-source candidates.
Do not turn rejected intake rows into vague missing-data results.

## Required outputs

Create a result file and machine-readable JSON for this task.

Update:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`
- `SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt`

Create exactly one next grouped task based on the result.

## Required tests

Run focused replay-after-intake tests, accepted complete setup evidence intake tests, Day 50 post-closure expansion tests, Day 50 exact setup-source closure tests, Day 50 source-resolution tests, data-source registry tests, Day 48 positive-trade funnel regression twice, relevant Ideal/CFB/Continuation/stage/session tests, contract-selection and quote-freshness tests, evidence validator, package-to-intake bridge, future-chat consistency tests, and `git diff --check`.
