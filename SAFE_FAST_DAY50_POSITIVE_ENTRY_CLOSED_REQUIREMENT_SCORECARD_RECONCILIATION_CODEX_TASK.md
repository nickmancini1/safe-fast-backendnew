# SAFE-FAST Day 50 End-to-End Raw-Data Positive-Entry Generation

## Required startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DATA_SOURCE_REGISTRY.md`
2. `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`
3. `SAFE_FAST_DAY50_POSITIVE_ENTRY_ACTIVE_PATH_REQUIREMENT_REGRESSION_RESULT.md`
4. `SAFE_FAST_DAY50_EVIDENCE_BACKED_POSITIVE_ENTRY_TESTING_BATCH_RESULT.md`
5. `SAFE_FAST_DAY48_POSITIVE_TRADE_CAPTURE_AND_MISS_ANALYSIS_RESULT.md`
6. `SAFE_FAST_PROJECT_DASHBOARD.md`
7. `SAFE_FAST_PROJECT_RULE_INDEX.md`
8. Existing frozen Ideal, Clean Fast Break, and Continuation calculators
9. Existing underlying and option-data manifests, ignored local raw data,
   replay runners, candidate generators, validators, and regression tests

Expected branch: `main`.

Expected status: clean.

Local Git and `SAFE_FAST_BUILD_STATE.md` control the current baseline.

This task performs actual candidate generation and replay testing.

## Current measured baseline

The existing measured batch contains:

- setup-qualified candidates: 13;
- trade candidates: 9;
- selected contracts: 5;
- eligible entries: 1;
- recorded entries: 1;
- valid captured trades: 1;
- true no-trades: 4;
- missed valid trades: 0;
- invalid trades allowed: 0.

The prior candidate pool is fully classified and remains regression evidence.

## Active objective

Generate a fresh development batch directly from complete timestamped
underlying-market evidence rather than from incomplete candidate rows.

Run the frozen SAFE-FAST rules over raw chronological data to discover:

1. Ideal setups;
2. Clean Fast Break setups;
3. Continuation setups.

Then run every generated candidate through contract selection, quote
freshness, execution eligibility, and entry recording.

The result must establish new complete candidates or produce one exact,
cost-checked data request capable of generating them.

## Raw-data inventory

Inventory all existing tracked and ignored local underlying data.

For each symbol and date range, record:

- source;
- dataset;
- schema;
- bar or event resolution;
- timestamps and timezone;
- session coverage;
- completeness;
- candidate families that can be evaluated;
- whether the evidence supports exact setup trigger, invalidation, freshness,
  final-signal state, and session-boundary evaluation.

Use the canonical source registry.

One-hour bars may support context but may not establish an intraday setup
trigger when the frozen rule requires finer resolution.

## Exact underlying-data requirement

For each setup family, identify the minimum accepted underlying-data resolution
needed to calculate:

- setup development;
- trigger;
- invalidation;
- freshness or spent state;
- final-signal state;
- prior completed structure;
- blocker and caution state;
- session-boundary behavior;
- no-hindsight decision boundary.

Map every required field to its exact local calculator and source.

## Candidate generation

Generate candidates deterministically from raw chronological data.

Candidate generation must:

- use only information available at or before each decision timestamp;
- exclude protected holdout periods;
- exclude previously measured candidate identifiers;
- avoid duplicate signals from the same opportunity;
- avoid selection based on later option performance or trade outcome;
- preserve winners and losers equally;
- produce stable candidate identifiers;
- run twice with identical output.

Target the earliest unused complete-data windows.

Generate up to 10 candidates per family when the available data supports them.

When fewer exist, include every valid generated candidate.

Create:

`historical_signal_replay/fixtures/day50_raw_data_positive_entry_candidate_manifest.json`

The manifest must record:

- candidate identifier;
- setup family;
- symbol;
- direction;
- signal timestamp;
- timezone;
- source data;
- rule version;
- complete chronological stage path;
- exclusion reason for every rejected raw-data opportunity.

## Full trade funnel

Run every generated candidate through:

1. `SETUP_DEVELOPING`
2. `SETUP_QUALIFIED`
3. `TRADE_CANDIDATE`
4. `CONTRACT_SELECTED`
5. `PRICE_ACCEPTABLE`
6. `ENTRY_ELIGIBLE`
7. `ENTRY_RECORDED`
8. `EXIT_EVALUATED`
9. `FINAL_OUTCOME`

For each candidate, record:

- highest stage reached;
- first stage not reached;
- exact blocker;
- setup-rule evidence;
- selected-contract evidence;
- quote timestamp and exact quote age;
- bid, ask, spread, and displayed size when available;
- execution result;
- entry result;
- final classification.

Allowed classifications:

- `VALID_TRADE_CAPTURED`
- `TRUE_NO_TRADE`
- `EXACT_DATA_REQUIRED`
- `MISSED_VALID_TRADE`
- `INVALID_TRADE_ALLOWED`
- `UNRESOLVED`

## Option evidence

Use existing local option evidence first.

For candidates reaching `TRADE_CANDIDATE`:

- enumerate the bounded contract set permitted by frozen rules;
- use `definition` for contract identity;
- use `cmbp-1` for exact quote-update freshness when available;
- use validated `cbbo-1s` when one-second evidence satisfies the rule;
- use `trades` and `statistics` only for their accepted consumers;
- rank contracts only after freshness, spread, liquidity, expiration, and strike
  requirements pass.

Record each eligible contract and exact pass or failure reason.

## Exact grouped data request

When local underlying data cannot generate complete candidates, create one
smallest grouped request covering the earliest unused development windows.

The request must include:

- exact symbols;
- exact dates;
- exact timestamps and timezone;
- exact dataset and schema;
- exact required resolution;
- exact field consumer;
- exact setup-family decision the data resolves;
- subtotal by symbol and window;
- checked total cost.

Use underlying setup-time data first.

For generated candidates that reach `TRADE_CANDIDATE` but lack option evidence,
create a separate setup-time option request.

Keep underlying and option requests separate.

Keep exit-path requests separate from entry qualification.

Perform cost checks when credentials and network access are available.

## Required measured output

Create:

1. `SAFE_FAST_DAY50_END_TO_END_RAW_DATA_POSITIVE_ENTRY_GENERATION_RESULT.md`
2. `historical_signal_replay/results/day50_end_to_end_raw_data_positive_entry_generation.json`
3. focused generator and validator code
4. focused tests
5. exactly one evidence-driven next task

Report per family and combined:

- raw opportunities inspected;
- candidates generated;
- setup-qualified candidates;
- trade candidates;
- selected contracts;
- prices accepted;
- eligible entries;
- recorded entries;
- valid captured trades;
- true no-trades;
- exact-data-required cases;
- missed valid trades;
- invalid trades allowed;
- unresolved cases;
- winners;
- losers;
- first blockers by stage;
- deterministic comparison across two runs.

Separate new-candidate results from existing regression controls.

## Concrete completion standard

This task must produce at least one of these concrete results:

1. new complete candidates reaching `SETUP_QUALIFIED`;
2. new candidates reaching `TRADE_CANDIDATE`;
3. new selected contracts or recorded entries;
4. one exact grouped, cost-checked raw-data request that supplies the data
   required to generate complete candidates.

The result must state which outcome was achieved.

## Regression protection

Rerun:

- the existing 15-candidate positive-trade funnel twice;
- the Day 50 evidence-backed batch;
- Ideal tests;
- Clean Fast Break tests;
- Continuation tests;
- developing-stage tests;
- session-boundary tests;
- contract-selection tests;
- quote-freshness tests;
- execution tests;
- context and caution tests;
- winner-selection tests;
- evidence validators;
- package-to-intake bridge;
- future-chat consistency tests.

## Control files and future chats

Update:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`
- `SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt`
- current canonical handoff files when the active state changes

The handoff must report:

- new candidates generated;
- setup-qualified total;
- trade-candidate total;
- selected-contract total;
- eligible-entry total;
- recorded-entry total;
- exact next action.

## Restrictions

Keep frozen trading rules and accepted thresholds unchanged.

Keep production, live backend, `main.py`, Railway, deployment, broker,
account, order, credential, and `.env` files unchanged.

Do not commit or push.

## Required tests

Run:

1. direct safe checks;
2. execution-policy bypass when required;
3. raw-data inventory tests;
4. candidate-generation determinism tests;
5. no-lookahead tests;
6. setup-family classification tests;
7. full generated batch twice;
8. existing positive-trade regressions twice;
9. option-contract and quote-freshness tests;
10. execution and winner tests;
11. evidence validator;
12. intake bridge;
13. future-chat consistency tests;
14. `git diff --check`.

Remove generated `__pycache__` directories.

## Final summary

Return only:

- Baseline
- Fixed
- Blocked
- Next
- Tests
- Files changed
- Raw opportunities inspected
- New Ideal totals
- New Clean Fast Break totals
- New Continuation totals
- New combined totals
- Existing regression result
- Setup-qualified candidates
- Trade candidates
- Selected contracts
- Eligible entries
- Recorded entries
- Valid trades captured
- True no-trades
- Exact-data-required cases
- Missed valid trades
- Invalid trades allowed
- Winners
- Losers
- Exact checked cost or `NOT_AVAILABLE`
- Concrete completion outcome
- Exact next task filename