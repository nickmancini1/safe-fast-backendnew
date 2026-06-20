# SAFE-FAST Day 49 Grouped Positive-Entry Setup Evidence Completion or Replacement

## Required startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_SETUP_FIELD_COMPLETION_RESULT.md`
2. `historical_signal_replay/results/day49_grouped_positive_entry_setup_field_completion.json`
3. `SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_CANDIDATE_EXPANSION_RESULT.md`
4. `historical_signal_replay/fixtures/day49_positive_entry_candidate_expansion_manifest.json`
5. `SAFE_FAST_DAY48_POSITIVE_TRADE_CAPTURE_AND_MISS_ANALYSIS_RESULT.md`
6. `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`
7. `SAFE_FAST_PROJECT_DASHBOARD.md`
8. `SAFE_FAST_PROJECT_RULE_INDEX.md`
9. Existing tracked and ignored local source-data directories, candidate packets,
   signal logs, replay fixtures, builders, validators, and family tests

Expected branch: `main`
Expected status: clean except this task file only when it is supplied untracked;
otherwise clean when the task is already committed.

Local Git and `SAFE_FAST_BUILD_STATE.md` are the current source of truth.

This filename is retained for control-file continuity. Do not create another
deterministic candidate batch before completing or replacing the current eight.

This is actual build testing, not live trading and not governance-only work.

## Current evidence

The frozen development batch contains eight candidates:

- 2 Ideal
- 1 Clean Fast Break
- 5 Continuation

All eight currently stop before `SETUP_QUALIFIED`.

They are `MISSING_DATA`, not confirmed no-trades.

The immediate problem is incomplete setup-time evidence, not option selection.

Do not request option data for a candidate that has not reached
`TRADE_CANDIDATE`.

## Active objective

Move the current eight candidates forward by doing all of the following in one
grouped task:

1. identify every exact missing setup field;
2. resolve every field possible from existing local data;
3. rerun every resolved candidate chronologically;
4. replace only candidates proven unusable with deterministic candidates that
   already have complete local setup evidence;
5. build one exact grouped setup-data request for any remaining genuine source
   gaps;
6. perform a cost check when credentials and network are available;
7. do not download data.

Do not finish by merely reporting the same eight missing-data results again.

## Step 1 - Exact missing-field matrix

For each of the eight frozen candidates, create a machine-readable matrix
containing:

- candidate identifier;
- setup family;
- underlying;
- direction;
- signal timestamp and timezone;
- source files and source-row identifiers;
- every required setup field;
- current field value;
- whether the value is present, derivable, contradictory, or absent;
- exact rule consumer;
- exact reason `SETUP_QUALIFIED` cannot currently be evaluated;
- smallest evidence needed to resolve it.

Use the canonical setup rules already in the repository.

Do not invent a value.

Do not use future bars or later outcome information.

## Step 2 - Exhaust local evidence first

Search all relevant tracked and ignored local evidence, including:

- historical replay source rows;
- signal logs;
- candidate packets;
- local market-data drops;
- existing manifests;
- prior grouped replay fixtures;
- session and lifecycle fixtures.

A clean Git status does not mean ignored data is absent.

Derive a setup field only when the derivation is deterministic, chronological,
and already supported by a frozen rule or an existing tested calculator.

For every derived field, record:

- input rows;
- timestamps;
- calculation or rule version;
- result;
- validation test.

Do not change setup thresholds to make a candidate qualify.

## Step 3 - Complete or replace

After local evidence is exhausted, classify each frozen candidate as:

- `SETUP_EVIDENCE_COMPLETED`
- `EXACT_EXTERNAL_SETUP_DATA_REQUIRED`
- `SOURCE_CONTRADICTION`
- `CANDIDATE_UNUSABLE`

For `SETUP_EVIDENCE_COMPLETED`, rerun the candidate through:

1. `SETUP_DEVELOPING`
2. `SETUP_QUALIFIED`
3. `TRADE_CANDIDATE`

For `CANDIDATE_UNUSABLE`, replacement is permitted only when:

- the unusable reason is documented;
- no protected holdout candidate is used;
- the replacement is the earliest unused candidate with complete local
  setup-time evidence;
- selection uses no option outcome, trade outcome, winner, or loser information;
- the replacement is frozen in the same machine-readable manifest.

Do not replace a candidate simply because it failed a legitimate setup rule.

Do not create another batch made entirely of incomplete candidates.

## Step 4 - Exact grouped external request

For candidates classified `EXACT_EXTERNAL_SETUP_DATA_REQUIRED`, create one
smallest grouped request package covering only the exact missing setup fields.

The request must state:

- candidate;
- missing field;
- decision the field resolves;
- dataset and schema;
- symbol;
- exact start and end timestamps;
- timezone;
- required rows or fields;
- why local evidence is insufficient;
- estimated response consumer.

Requirements:

- underlying/setup evidence only;
- no option request;
- no exit-path request;
- no unrestricted full-session request;
- no fields unrelated to `SETUP_QUALIFIED`;
- no duplicated request where one grouped window safely covers related fields.

Run an exact cost check when safe credentials and HTTPS are available.

Do not download.

Do not infer approval.

## Step 5 - Mandatory rerun

Run the completed/replaced batch twice.

Report deterministic equality.

Rerun the existing 15-candidate positive-trade funnel as regression controls.

Report for the current development batch:

- candidates completed locally;
- candidates replaced;
- candidates needing exact external data;
- contradictory candidates;
- unusable candidates;
- setup developing;
- setup qualified;
- trade candidates;
- first blockers by field and stage;
- stable and unstable cases.

Any candidate reaching `TRADE_CANDIDATE` must be routed next into grouped
contract/quote testing using existing frozen option rules.

## Completion gate

This task is complete only when every one of the eight candidate slots has one
of these outcomes:

1. complete setup evidence and an evaluated qualification result;
2. a deterministic complete-evidence replacement and evaluated result;
3. an exact validated external setup-data request with checked cost or a precise
   reason the cost is unavailable;
4. a documented contradiction or permanent unusable classification.

No candidate may remain labeled only as vague `MISSING_DATA`.

Do not create another candidate-expansion task while unresolved setup-field
work remains.

## Required outputs

Create:

- `SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_SETUP_EVIDENCE_COMPLETION_OR_REPLACEMENT_RESULT.md`
- `historical_signal_replay/results/day49_positive_entry_setup_evidence_completion.json`
- a focused validator and tests
- one request manifest only when external setup data is genuinely required

Update:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`
- current future-chat handoff files when the active state changes

Future chats must be told plainly:

- the eight cases are missing-evidence cases, not no-trades;
- no more incomplete candidate batches are permitted;
- complete, replace, or request exact evidence first.

## Next-task routing

Create exactly one next grouped task based on the result:

- grouped option-contract and fresh-quote testing when candidates reach
  `TRADE_CANDIDATE`;
- exact setup-data approval/download task when a cost check succeeds;
- grouped setup-rule repair only when complete evidence proves a rule or harness
  defect;
- no additional candidate batch unless every current slot has been completed,
  replaced, or formally closed.

Do not create a governance-only task.

## Restrictions

Do not modify:

- frozen trading thresholds;
- production or live backend;
- `main.py`;
- Railway or deployment files;
- broker, account, or order code;
- credentials or `.env`.

Do not download data.

Do not calculate option profit or loss before a valid entry exists.

Do not claim profitability, proof, readiness, promotion, or live eligibility.

Do not commit or push.

## Required tests

Run:

1. direct safe checks;
2. execution-policy bypass when needed;
3. missing-field matrix validator;
4. local derivation tests;
5. deterministic replacement-selection tests;
6. completed/replaced batch twice;
7. existing positive-trade funnel regression twice;
8. all Ideal, Clean Fast Break, and Continuation replay tests;
9. stage and session-boundary tests;
10. evidence validator;
11. intake bridge;
12. handoff/control-file consistency tests;
13. `git diff --check`.

Remove generated `__pycache__` directories.

## Final summary

Return only:

- Baseline
- Fixed
- Blocked
- Next
- Tests
- Files changed
- Candidate slots completed locally
- Candidate slots replaced
- Exact external setup-data requests
- Contradictory or unusable candidates
- Setup-qualified total
- Trade-candidate total
- First blockers by field
- Existing regression-control result
- Exact checked cost or `NOT_AVAILABLE`
- Exact next grouped task filename