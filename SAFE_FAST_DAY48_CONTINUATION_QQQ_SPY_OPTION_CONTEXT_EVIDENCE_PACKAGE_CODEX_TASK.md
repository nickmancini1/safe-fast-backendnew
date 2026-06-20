# SAFE-FAST Day 48 Continuation QQQ/SPY Option-Context Evidence Package — Codex Task

## Required startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DAY48_GROUPED_THREE_FAMILY_EXPANSION_AFTER_CONTINUATION_STARTER_RESULT.md`
2. `SAFE_FAST_DAY48_CONTINUATION_STARTER_COVERAGE_RESULT.md`
3. `SAFE_FAST_DAY48_ACTUAL_GROUPED_THREE_FAMILY_REPLAY_TEST_RESULT.md`
4. `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`
5. `SAFE_FAST_PROJECT_DASHBOARD.md`
6. `SAFE_FAST_PROJECT_RULE_INDEX.md`
7. Existing Continuation fixtures, candidate packets, local source rows,
   option selectors, execution calculators, and context/caution calculators

Expected branch: `main`
Expected starting commit: `ad0188a`
Expected status: clean except this task file

If local git and the canonical files disagree, stop and report the conflict.

This is grouped evidence preparation and focused testing, not live trade
evaluation and not another governance-only task.

## Active objective

Create and validate one request-shaped evidence package for the existing QQQ
and SPY Continuation candidates whose local rule stacks currently abstain
because option-contract, execution, or context evidence is missing.

Preserve GLD and IWM as missing-trigger/no-local-option-package controls.

Do not request, purchase, or construct GLD/IWM option evidence.

Do not download data.

A cost-only check is permitted only after the exact request package passes all
local validation.

## Required execution

### 1. Freeze the candidate set

From committed fixtures and results, identify every currently runnable QQQ and
SPY Continuation candidate.

For each candidate, record:

- candidate identifier;
- underlying;
- direction;
- signal timestamp;
- timezone;
- lifecycle stage at signal;
- session date;
- source-row identifiers;
- frozen setup/rule version;
- exact reason contract selection currently abstains;
- exact missing execution fields;
- exact missing context/caution fields.

Do not add or remove candidates based on later outcomes.

### 2. Search existing local evidence first

Inspect existing repository fixtures, local source rows, manifests, and ignored
raw-data directories before proposing any external request.

Record exactly which required fields are:

- already available locally;
- present but unusable;
- missing;
- contradictory;
- outside the permitted timestamp window.

Do not claim data is missing merely because it is ignored by git.

### 3. Re-run what local evidence supports

When sufficient local fields already exist, build focused fixtures and execute
the frozen Continuation stack through:

1. chronological lifecycle;
2. contract selection;
3. execution realism;
4. context/caution;
5. winner selection;
6. final entry, no-trade, unresolved, or blocked result.

Run the focused package twice and require deterministic equality.

Do not manufacture a selected contract, fill, context value, or trade.

### 4. Build one exact grouped request package for remaining gaps

For QQQ and SPY only, define the smallest request that can answer the remaining
questions.

The package must state for every request:

- candidate identifier;
- decision the data will answer;
- dataset;
- schema;
- symbol type;
- underlying or exact option symbol when deterministically known;
- signal timestamp and timezone;
- start and end timestamps;
- setup-time window;
- conditional exit-path window, kept separate;
- required quote, trade, statistics, or context fields;
- expected selector/execution/context consumer;
- missing-data behavior;
- why a narrower request is insufficient.

Do not broaden symbols, dates, contracts, schemas, or windows for convenience.

Do not include exit-path data when no valid entry can be established.

### 5. Validate the package

Create a machine-readable manifest plus a focused validator proving:

- only frozen QQQ/SPY Continuation candidates are included;
- GLD/IWM are excluded from requests and retained as controls;
- all timestamps are chronological and timezone-explicit;
- no outcome information influenced candidate or contract selection;
- setup and conditional-exit windows remain separate;
- every requested field maps to a named unresolved rule decision;
- no secret or credential is stored.

### 6. Optional cost-only check

After local validation passes, use the existing Databento cost-check workflow
for the exact grouped request when working HTTPS and credentials are available.

Do not download.

Record:

- exact checked total;
- subtotal by candidate;
- subtotal by schema/window;
- request shape used;
- any rejected request and corrected shape;
- `NOT_AVAILABLE` with the exact reason when a fresh check cannot run.

No purchase approval may be inferred from this task.

## Required outputs

Create:

1. `SAFE_FAST_DAY48_CONTINUATION_QQQ_SPY_OPTION_CONTEXT_EVIDENCE_PACKAGE_RESULT.md`
2. One machine-readable request manifest using the repository’s canonical
   evidence-package location and naming convention
3. Focused tests validating the manifest and control behavior

Update:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`

The control files must agree on the current objective and exact next grouped
task.

## Next-task decision

Create or reuse exactly one next task based on evidence:

- grouped local Continuation execution test when local evidence is sufficient;
- exact selected-request download task requiring user approval when the cost
  check succeeds and external data is necessary;
- package-repair task only when the request shape or validation fails.

Do not route into another general governance task.

## Restrictions

Do not modify:

- frozen recognition or trading behavior;
- accepted execution or risk thresholds;
- production/live backend;
- `main.py`;
- Railway or deployment files;
- broker, account, or order code;
- credentials or `.env`.

Do not run a profitability backtest.

Do not claim proof, profitability, readiness, promotion, or live eligibility.

## Required tests

Run:

1. direct safe-check script;
2. execution-policy bypass if direct PowerShell is blocked;
3. existing Continuation starter tests;
4. existing grouped three-family Day 48 tests;
5. contract-selection tests;
6. execution-realism tests;
7. context/caution tests;
8. winner-stability tests;
9. the new package validator;
10. evidence content validator;
11. package-to-intake bridge;
12. `git diff --check`.

Remove generated `__pycache__` directories.

Do not commit or push.

## Final summary

Return only:

- Baseline
- Fixed
- Blocked
- Next
- Tests
- Files changed
- QQQ candidates and missing fields
- SPY candidates and missing fields
- GLD/IWM control result
- Local evidence reused
- Exact request manifest
- Exact checked cost or `NOT_AVAILABLE`
- Exact next grouped task filename