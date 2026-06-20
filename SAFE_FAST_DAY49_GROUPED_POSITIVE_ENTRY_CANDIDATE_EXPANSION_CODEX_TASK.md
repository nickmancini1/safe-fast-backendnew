# SAFE-FAST Day 49 Grouped Positive-Entry Candidate Expansion — Codex Task

## Startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_EXPANSION_AFTER_SETUP_DOWNLOAD_RESULT.md`
2. `SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_SETUP_TIME_DOWNLOAD_AND_REPLAY_RESULT.md`
3. `SAFE_FAST_DAY48_POSITIVE_TRADE_CAPTURE_AND_MISS_ANALYSIS_RESULT.md`
4. `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`
5. `SAFE_FAST_PROJECT_DASHBOARD.md`
6. `SAFE_FAST_PROJECT_RULE_INDEX.md`
7. Current future-chat handoff files named by the rule index
8. Existing Ideal, Clean Fast Break, and Continuation candidate packets,
   signal logs, source rows, replay runners, calculators, fixtures, manifests,
   and regression tests

Expected branch: `main`
Expected starting commit: `46ab96e`
Expected status: clean except this task file.

If local Git or the canonical control files disagree, stop and identify the
exact conflict.

This is actual SAFE-FAST testing.

Do not replace execution with another governance-only document.

## Current evidence

The existing measured batch contains:

- 1 valid captured trade;
- 4 true no-trades;
- 6 missing-data cases;
- 4 unresolved cases;
- 1 winner;
- 0 losers;
- 0 proven missed valid trades;
- 0 invalid trades allowed.

The existing candidates remain regression controls.

Do not spend this task repeatedly re-confirming the same no-trades.

## Active objective

Expand the development candidate pool and test whether SAFE-FAST can capture
legitimate entries across:

1. Ideal;
2. Clean Fast Break;
3. Continuation.

The goal is not to increase trade count by weakening rules.

The goal is to test more genuine opportunities and identify exactly where valid
entries are captured or lost.

## Freeze a new candidate batch

Before inspecting option outcomes, create a machine-readable manifest of new
development candidates.

Exclude:

- protected holdout candidates;
- the existing measured 15-candidate funnel set;
- candidates already used as current positive or rejection controls;
- duplicate signals representing the same underlying opportunity.

Select candidates deterministically using only pre-outcome information.

Use chronological order from the available unused candidate universe.

Target up to 8 new candidates per setup family, or every available unused
candidate when fewer than 8 exist.

Do not select candidates because their later price move looked profitable.

For every selected candidate, freeze:

- candidate identifier;
- setup family;
- underlying;
- direction;
- signal timestamp;
- timezone;
- session date;
- source rows;
- candidate-generation rule version;
- lifecycle rule version;
- exclusion reason for every otherwise eligible candidate not selected;
- confirmation that the candidate is development evidence, not holdout.

Create:

`historical_signal_replay/fixtures/day49_positive_entry_candidate_expansion_manifest.json`

Add a focused validator proving selection is deterministic and outcome-blind.

## Chronological underlying replay

For every frozen candidate, replay evidence in timestamp order through:

1. `SETUP_DEVELOPING`
2. `SETUP_QUALIFIED`
3. `TRADE_CANDIDATE`

Record:

- complete stage path;
- highest stage reached;
- first failed stage;
- exact blocker;
- session-boundary behavior;
- whether the setup was recognized before the move;
- whether it became a possible trade.

Do not use future bars or later classifications.

## Option-contract and fresh-quote testing

For every candidate that reaches `TRADE_CANDIDATE`, enumerate the bounded
contract set permitted by the existing frozen rules.

Use only information available at or before the signal.

For each eligible contract, record:

- raw symbol;
- expiration;
- strike;
- option type;
- quote-update timestamp at or before the signal;
- exact quote age;
- bid;
- ask;
- spread;
- displayed size when available;
- pass or fail reason.

Use local quote-update evidence first.

Do not rely on TCBBO alone to determine quote freshness.

Prefer CMBP-1 quote updates when available.

Use CBBO-1s only when existing focused tests prove it preserves the frozen
quote-age rule.

Apply the existing deterministic contract ranking only after stale, late,
wide-spread, and otherwise ineligible contracts are removed.

Do not select the historically best-performing contract.

## Complete trade funnel

Trace every runnable candidate through:

1. `SETUP_DEVELOPING`
2. `SETUP_QUALIFIED`
3. `TRADE_CANDIDATE`
4. `CONTRACT_SELECTED`
5. `PRICE_ACCEPTABLE`
6. `ENTRY_ELIGIBLE`
7. `ENTRY_RECORDED`
8. `EXIT_EVALUATED`
9. `FINAL_OUTCOME`

Use exactly one final classification:

- `VALID_TRADE_CAPTURED`
- `TRUE_NO_TRADE`
- `MISSING_DATA`
- `MISSED_VALID_TRADE`
- `INVALID_TRADE_ALLOWED`
- `UNRESOLVED`

Missing option or context evidence must not be classified as a true no-trade.

A valid captured trade may later be either a winner or a loser.

Do not hide valid losing trades.

## Existing local evidence first

Inspect all existing tracked and ignored local data before creating an external
request.

A clean Git status does not mean ignored raw data is absent.

When local evidence proves a valid entry:

- record the entry using the canonical execution rules;
- do not download exit data in this task;
- create an exact exit-path cost-check task only for that valid entry.

When local evidence proves a safety failure:

- classify `TRUE_NO_TRADE`;
- report the exact contemporaneous failure.

When evidence is missing:

- classify `MISSING_DATA`;
- identify the exact missing setup-time fields;
- identify the exact decision those fields would resolve.

## Small grouped setup-time request

When external evidence is required, create the smallest grouped request covering
only frozen candidates that reached `TRADE_CANDIDATE`.

Requirements:

- setup-time evidence only;
- no exit-path data;
- no unrestricted option-chain request;
- bounded eligible contracts only;
- quote-update evidence capable of measuring freshness;
- exact symbols, schemas, timestamps, and timezones;
- every requested field mapped to an unresolved funnel decision.

Compare the smallest valid CMBP-1 and CBBO-1s request shapes when both are
available.

Perform an exact cost check when the Databento credential and network are
available.

Do not download data.

Do not infer purchase approval.

## Required execution

Run the complete new candidate batch twice.

Require deterministic equality.

Rerun all existing 15-candidate positive-trade funnel cases as regression
controls.

Rerun:

- Ideal tests;
- Clean Fast Break tests;
- Continuation tests;
- developing-stage tests;
- session-boundary tests;
- contract-selection tests;
- execution-realism tests;
- context and caution tests;
- winner-selection tests;
- stale-quote controls;
- wide-spread controls;
- quote-after-signal controls.

Do not change frozen trading rules merely to create a passing entry.

## Required result

Create:

`SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_CANDIDATE_EXPANSION_RESULT.md`

Report per family and combined:

- new candidates found;
- new candidates runnable;
- setup developing;
- setup qualified;
- trade candidates;
- contracts selected;
- prices accepted;
- entries eligible;
- entries recorded;
- exits evaluated;
- valid trades captured;
- true no-trades;
- missing-data cases;
- missed valid trades;
- invalid trades allowed;
- unresolved cases;
- winners;
- losers;
- stable cases;
- unstable cases;
- first blockers by stage;
- conversion rate between each funnel stage.

Separate new-candidate results from existing regression-control results.

Answer plainly:

1. Did SAFE-FAST recognize the new setups before the move?
2. How many became possible trades?
3. How many had a tradable option at that exact time?
4. How many were rejected by a real safety rule versus missing evidence?
5. How many valid trades were caught, missed, or incorrectly allowed?

## Control files and future chats

Update:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`
- current future-chat handoff files when the active state changes

Future chats must continue positive-entry expansion and must not return to
repeatedly confirming the same no-trade examples.

The current 15 candidates remain regression controls.

New development batches must add new candidate identifiers.

## Next-task routing

Create exactly one evidence-driven next grouped task:

- exit-path cost check when new valid entries are established;
- exact grouped setup-time cost check when missing data is the blocker;
- grouped repair when a valid trade is proven missed;
- grouped safety repair when an invalid trade is allowed;
- another deterministic candidate batch only when unused candidates remain.

Do not create another general governance task.

## Restrictions

Do not modify:

- production or live backend;
- `main.py`;
- Railway or deployment files;
- broker, account, or order code;
- credentials or `.env`;
- frozen trading rules or accepted thresholds.

Do not download data.

Do not claim profitability, proof, readiness, promotion, or live eligibility.

Do not commit or push.

## Required tests

Run:

1. direct safe checks;
2. execution-policy bypass when direct PowerShell is blocked;
3. candidate-manifest validator;
4. complete new candidate batch twice;
5. existing positive-trade funnel regression batch twice;
6. all three setup-family replay suites;
7. stage and session-boundary tests;
8. quote-freshness and contract-selection tests;
9. execution, context, and winner tests;
10. evidence validator;
11. package-to-intake bridge;
12. future-chat consistency tests;
13. `git diff --check`.

Remove generated `__pycache__` directories before final status.

## Final summary

Return only:

- Baseline
- Fixed
- Blocked
- Next
- Tests
- Files changed
- New Ideal totals
- New Clean Fast Break totals
- New Continuation totals
- New combined totals
- Existing regression-control result
- Valid trades captured
- True no-trades
- Missing-data cases
- Missed valid trades
- Invalid trades allowed
- Unresolved cases
- Winners
- Losers
- Five owner questions and answers
- Exact checked cost or `NOT_AVAILABLE`
- Exact next grouped task filename