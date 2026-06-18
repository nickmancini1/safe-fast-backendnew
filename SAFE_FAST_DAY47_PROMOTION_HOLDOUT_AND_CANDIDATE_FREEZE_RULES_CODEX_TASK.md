# SAFE-FAST Day 47 Promotion, Holdout, and Candidate-Freeze Rules — Codex Task

## Required startup

Read these files in order before making any change:

1. `SAFE_FAST_BUILD_STATE.md`
2. `SAFE_FAST_DAY47_TO_DAY90_CONSOLIDATED_AUDIT_AND_COMPLETION_PLAN_RESULT.md`
3. `SAFE_FAST_PROJECT_DASHBOARD.md`
4. `SAFE_FAST_PROJECT_RULE_INDEX.md`

Expected starting state:

- branch: `main`
- commit: `d23a343`
- clean repo except for this task file

If the repo, control files, or audit result disagree, stop and report the exact
conflict. Local git is the source of truth.

This is SAFE-FAST build-governance work, not live trade evaluation.

Do not modify the frozen engine baseline, live backend, production files,
Railway, broker/account/order code, credentials, `.env`, or raw market data.

Do not download data and do not run a new backtest.

## Objective

Implement the first grouped Day 47-to-Day 90 rule package identified by the
consolidated audit:

1. promotion gates;
2. falsifiable final outcomes;
3. sample-size and coverage contract;
4. protected holdout rules;
5. candidate-selection and contract-selection freeze rules.

Use the canonical owners assigned by the audit result. Update existing canonical
documents rather than creating duplicate authorities.

If no canonical implementation document exists for one of these rules, create
one consolidated canonical rule document rather than several overlapping files.

## Required rule content

### Promotion ladder

Define explicit gates for:

1. development evidence;
2. grouped replay eligibility;
3. regression acceptance;
4. protected-holdout evaluation;
5. controlled paper-validation eligibility;
6. paper-to-live review eligibility.

For every gate, state:

- required evidence;
- required tests;
- minimum sample or coverage requirement;
- execution-cost assumptions;
- risk requirements;
- automatic failure conditions;
- permitted next action;
- who or what may approve advancement.

No setup family or combined plan advances because a date was reached.

No result may skip a gate.

### Falsifiable final outcomes

Define exactly four Day 90 outcomes:

1. `PAPER_VALIDATION_ELIGIBLE`
2. `BOUNDED_REPAIR_REQUIRED`
3. `NARROWED_PLAN`
4. `REDESIGN_REQUIRED`

For each outcome, provide deterministic entry criteria, disqualifiers, required
evidence, and the exact permitted next work.

Do not allow an undefined outcome such as “continue developing.”

### Sample-size and coverage contract

Create explicit numerical minimums for each setup family:

- Ideal
- Clean Fast Break
- Continuation

The contract must separately cover:

- accepted entries;
- rejection/no-trade controls;
- ambiguous or boundary cases;
- winners;
- losers;
- major market regimes;
- volatility conditions;
- trend and chop;
- time-of-day periods;
- weekdays;
- liquidity and spread conditions;
- symbols and expirations approved by the plan;
- developing-stage transitions;
- session-boundary cases.

Use existing repo evidence and audit decisions wherever they already determine
a value.

Where the repo has no evidence-backed numerical value, define a conservative
provisional value, label it clearly as a governance assumption, and require it
to be frozen before protected holdout evidence is opened.

Do not leave `TBD`, “sufficient,” “representative,” or similar vague language.

### Protected holdout

Define rules requiring:

- holdout candidates and dates to be selected before outcome inspection;
- a committed manifest containing exact candidate identifiers, timestamps,
  setup families, data references, and hashes where available;
- holdout data to remain excluded from tuning, repair, threshold selection, and
  winner selection;
- rule and configuration versions to be frozen before reveal;
- any post-reveal rule change to invalidate the affected holdout result;
- replacement holdout evidence to be newly selected and documented;
- complete reporting of passing, failing, rejected, and missing-data cases;
- no selective removal of unfavorable examples.

### Candidate and option-contract freeze

Define deterministic rules requiring candidate generation and option-contract
selection to use only information available at the decision timestamp.

The frozen record must include:

- candidate-generation rule version;
- setup-family label and stage;
- underlying;
- direction;
- signal timestamp and timezone;
- expiration-selection rule;
- strike-selection rule;
- call or put;
- liquidity and spread filters;
- quote-age limit;
- selected raw symbol and instrument identifier when available;
- reason for every exclusion;
- deterministic tie-break;
- evidence that outcome data was unavailable during selection.

Explicitly prohibit:

- selecting candidates because they later looked profitable;
- replacing losing candidates after outcome inspection;
- selecting the best-performing contract retrospectively;
- using future bars, quotes, classifications, or exit information;
- excluding valid candidates without a recorded pre-outcome rule.

### Decision tables and consistency

Add compact decision tables making every rule operational.

Ensure all canonical control files agree on:

- current commit;
- active objective;
- what is now defined;
- what remains unproven;
- exact next grouped task filename.

Preserve the audit requirement that future chats must read
`SAFE_FAST_BUILD_STATE.md` first and must not restart completed discovery.

## Change-control requirements

- Follow the canonical ownership map in the audit result.
- Remove or mark superseded duplicate language where necessary.
- Do not silently alter an existing accepted trading rule.
- State why every frozen or accepted rule changed.
- Create or update focused consistency tests.
- Every changed behavior or rule requires matching documentation.
- Create one result document for this task.
- Create or reuse exactly one next grouped Codex task according to the ordered
  audit plan.
- Do not commit or push.

## Required tests

Run:

1. `scripts/safe_fast_run_safe_checks.ps1`
2. the existing evidence content validator;
3. the existing package-to-intake bridge;
4. `tests/test_day47_to_day90_audit_consistency.py`;
5. focused tests for the new rule package and control-file agreement;
6. `git diff --check`.

If direct PowerShell execution is blocked, run the existing process-level
execution-policy bypass and report both results accurately.

Remove generated `__pycache__` directories before the final status check.

## Final summary

Return only:

- Baseline
- Fixed
- Blocked
- Next
- Tests
- Files changed
- Exact canonical rule document
- Exact numerical sample contract
- Exact next grouped task filename

Do not claim profitability, readiness, proof, or promotion merely because these
governance rules were documented.
