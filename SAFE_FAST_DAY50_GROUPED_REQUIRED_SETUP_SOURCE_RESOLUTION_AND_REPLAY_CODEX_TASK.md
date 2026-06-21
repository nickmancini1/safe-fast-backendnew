# SAFE-FAST Day 50 Grouped Required Setup-Source Resolution and Replay

## Required startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DATA_SOURCE_REGISTRY.md`
2. `historical_signal_replay/config/safe_fast_data_source_registry.json`
3. `SAFE_FAST_DAY50_DATA_SOURCE_REGISTRY_AND_SCHWAB_QUEUE_RESULT.md`
4. `SAFE_FAST_DAY50_SCHWAB_READ_ONLY_AUTH_AND_CAPABILITY_AUDIT_RESULT.md`
5. `SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_SETUP_EVIDENCE_COMPLETION_OR_REPLACEMENT_RESULT.md`
6. `historical_signal_replay/results/day49_positive_entry_setup_evidence_completion.json`
7. `SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_EXACT_SETUP_DATA_APPROVAL_DOWNLOAD_RESULT.md`
8. `SAFE_FAST_DAY48_POSITIVE_TRADE_CAPTURE_AND_MISS_ANALYSIS_RESULT.md`
9. `SAFE_FAST_PROJECT_DASHBOARD.md`
10. `SAFE_FAST_PROJECT_RULE_INDEX.md`
11. Existing Ideal, Clean Fast Break, and Continuation replay runners,
    calculators, fixtures, validators, ignored local data, and regression tests

Expected branch: `main`
Expected starting commit: `a262237`
Expected status: clean except this task file.

If local Git or the canonical control files disagree, stop and report the exact
conflict.

Schwab developer approval is pending. Do not authenticate to Schwab during this
task. Schwab approval does not block this grouped build work.

This is actual SAFE-FAST testing, not another governance-only task.

## Current candidate state

The current eight Day 49 candidate slots have formal outcomes:

- 4 require exact external setup data;
- 3 contain source conflicts;
- 1 is excluded as unusable.

The immediate objective is to resolve those outcomes and rerun the candidates.

Do not create another incomplete candidate batch.

Do not repeatedly reconfirm the existing no-trade controls except as regression
tests.

## Active objective

In one grouped execution:

1. resolve the four exact external setup-data cases;
2. resolve or formally close the three source conflicts;
3. preserve the one excluded candidate unless evidence proves the exclusion was
   incorrect;
4. rerun every resolvable candidate chronologically;
5. move every candidate that qualifies into option-contract and fresh-quote
   testing;
6. produce one exact next task from the results.

No slot may finish with only the vague label `MISSING_DATA`.

## Source-resolution rules

Use the canonical source registry.

For every required field, report:

- exact field name;
- plain-English meaning;
- whether it is required for the setup label, trade eligibility, execution,
  exit, optional context, or review only;
- exact primary source;
- exact fallback source;
- exact local calculator or consumer;
- decision timestamp and timezone;
- local evidence found;
- external evidence needed;
- final resolution.

### Setup labels

Ideal, Clean Fast Break, Continuation, developing stages, setup qualification,
and trade-candidate labels must be calculated by the frozen SAFE-FAST rule
engine.

Do not obtain setup labels from Databento, Schwab, tastytrade, TradingView,
news providers, or macro providers.

### Optional context

Volatility, headlines, macro information, scheduled events, and review-only
context must not block a technical setup unless an existing frozen rule
explicitly marks the field as required.

When optional context is absent, record `CONTEXT_UNKNOWN` and continue the
technical setup evaluation.

Do not silently convert optional context into a mandatory blocker.

### Historical market data

Use existing tracked and ignored local evidence first.

For underlying price and volume evidence:

- use the downloaded Databento data when its resolution satisfies the rule;
- identify when one-hour bars are too coarse;
- identify the exact required timestamp resolution;
- identify the smallest valid dataset, schema, symbol set, and time window.

For historical options evidence:

- primary source remains Databento `OPRA.PILLAR`;
- use `definition` for contract identity;
- use `cmbp-1` for exact quote updates and quote age;
- use validated `cbbo-1s` only when one-second resolution is sufficient;
- do not use `tcbbo` alone to establish quote freshness.

Do not download data in this task.

When paid data is genuinely required, create the smallest exact grouped request
and perform a cost check only when credentials and network are available.

No purchase approval may be inferred.

### News, macro, events, and volatility

Use the registry’s assigned sources:

- SEC and issuer releases for filings and company events;
- Federal Reserve, BLS, BEA, Treasury, and ALFRED for official historical
  releases and historical data vintages;
- Cboe for official volatility indexes;
- SAFE-FAST calculations for realized and option implied volatility when all
  inputs exist;
- Benzinga only when entitlement exists;
- TradingView, tastytrade, and Schwab as secondary checks where permitted.

Do not average conflicting sources.

Do not choose the source that produces the most favorable trade result.

## Source-conflict resolution

For each of the three source-conflict candidates, record:

- candidate identifier;
- field in conflict;
- each conflicting source;
- each value;
- each timestamp;
- whether the value was available at the decision time;
- registry priority;
- historical-vintage rule;
- chosen value or exclusion decision;
- exact reason.

Resolve the conflict using the registry’s source hierarchy.

When the primary source is authoritative and chronological, use it.

When the conflict cannot be safely resolved, classify the candidate
`SOURCE_CONFLICT_EXCLUDED`.

Do not leave a conflict open indefinitely.

## External-data cases

For each of the four exact external-data candidates:

1. inspect all local tracked and ignored evidence;
2. determine the exact missing required field;
3. determine whether it can be calculated locally;
4. determine whether the existing one-hour OHLCV data is too coarse;
5. identify the exact source and resolution needed;
6. build one grouped request for only unresolved required fields;
7. cost-check the request when possible;
8. do not download.

Do not request option data before a candidate reaches `TRADE_CANDIDATE`.

Do not request exit data before a valid entry is established.

## Mandatory replay

Rerun all resolved candidates twice through:

1. `SETUP_DEVELOPING`
2. `SETUP_QUALIFIED`
3. `TRADE_CANDIDATE`
4. `CONTRACT_SELECTED`
5. `PRICE_ACCEPTABLE`
6. `ENTRY_ELIGIBLE`
7. `ENTRY_RECORDED`
8. `EXIT_EVALUATED`
9. `FINAL_OUTCOME`

Use only information available at each chronological decision point.

For each candidate, report:

- highest stage reached;
- first stage not reached;
- exact blocker;
- setup-label result;
- source-resolution result;
- option-contract result when applicable;
- quote-freshness result when applicable;
- final classification;
- first-run result;
- second-run result;
- deterministic or unstable.

Allowed final classifications:

- `VALID_TRADE_CAPTURED`
- `TRUE_NO_TRADE`
- `EXACT_EXTERNAL_DATA_REQUIRED`
- `SOURCE_CONFLICT_EXCLUDED`
- `CANDIDATE_UNUSABLE`
- `MISSED_VALID_TRADE`
- `INVALID_TRADE_ALLOWED`
- `UNRESOLVED`

Do not classify absent evidence as a true no-trade.

## Required outputs

Create:

1. `SAFE_FAST_DAY50_GROUPED_REQUIRED_SETUP_SOURCE_RESOLUTION_AND_REPLAY_RESULT.md`
2. `historical_signal_replay/results/day50_required_setup_source_resolution.json`
3. focused builder or resolver code only when required;
4. focused tests;
5. exactly one evidence-driven next Codex task.

Update:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`
- current future-chat handoff files when active state changes

## Required result totals

Report:

- four external-data cases resolved locally;
- external-data cases still requiring exact requests;
- three source conflicts resolved;
- source conflicts excluded;
- unusable candidates;
- setup-qualified candidates;
- trade candidates;
- contracts selected;
- entries recorded;
- true no-trades;
- valid trades captured;
- missed valid trades;
- invalid trades allowed;
- unresolved cases;
- first blockers by field and funnel stage.

Answer plainly:

1. Which candidates moved forward?
2. Which candidates were excluded and why?
3. Which exact required fields still need outside data?
4. How much would that data cost?
5. How many candidates reached real trade testing?

## Next-task routing

Create exactly one next grouped task:

- grouped option-contract and fresh-quote testing when candidates reach
  `TRADE_CANDIDATE`;
- exact approval/download task when a validated paid-data request is required;
- grouped repair task when complete evidence proves a rule or harness defect;
- positive-entry expansion only after all current slots are resolved or closed.

Do not create another general governance task.

## Restrictions

Do not modify:

- frozen trading thresholds;
- production or live backend;
- `main.py`;
- Railway or deployment files;
- broker, account, or order code;
- credentials;
- `.env`.

Do not authenticate to Schwab.

Do not download paid data.

Do not claim profitability, proof, readiness, promotion, or live eligibility.

Do not commit or push.

## Required tests

Run:

1. direct safe checks;
2. execution-policy bypass when required;
3. data-source registry and resolver tests;
4. focused source-conflict tests;
5. focused required-field tests;
6. resolved candidate batch twice;
7. existing positive-trade funnel regression twice;
8. Ideal replay tests;
9. Clean Fast Break replay tests;
10. Continuation replay tests;
11. stage and session-boundary tests;
12. contract-selection and quote-freshness tests;
13. execution, context, and winner tests;
14. evidence validator;
15. package-to-intake bridge;
16. future-chat consistency tests;
17. `git diff --check`.

Remove generated `__pycache__` directories.

## Final summary

Return only:

- Baseline
- Fixed
- Blocked
- Next
- Tests
- Files changed
- External-data cases resolved
- Exact external-data requests remaining
- Source conflicts resolved
- Source conflicts excluded
- Candidate exclusions
- Setup-qualified total
- Trade-candidate total
- Contracts selected
- Entries recorded
- True no-trades
- Valid trades captured
- Missed valid trades
- Invalid trades allowed
- Unresolved cases
- Exact checked cost or `NOT_AVAILABLE`
- Five plain-English answers
- Exact next grouped task filename