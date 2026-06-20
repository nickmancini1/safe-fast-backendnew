# SAFE-FAST Day 49 Grouped Positive-Entry Setup-Time Download and Replay

## Startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DAY48_GROUPED_POSITIVE_ENTRY_SETUP_TIME_REQUEST_COST_CHECK_RESULT.md`
2. `SAFE_FAST_DAY48_GROUPED_POSITIVE_ENTRY_EXPANSION_RESULT.md`
3. `SAFE_FAST_DAY48_POSITIVE_TRADE_CAPTURE_AND_MISS_ANALYSIS_RESULT.md`
4. `historical_signal_replay/source_data/richer_export_package_work/day48_grouped_positive_entry_setup_time_request_manifest.json`
5. `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`
6. `SAFE_FAST_PROJECT_DASHBOARD.md`
7. `SAFE_FAST_PROJECT_RULE_INDEX.md`
8. Existing three-family replay, funnel, validator, execution, contract,
   context, session, stage-transition, and winner-selection tests

Expected branch: `main`
Expected commit: `55527f0`
Expected status: only this task file is untracked.

Stop only for a real repo conflict.

This is build testing, not live trading.

## Authorization

The exact four-request setup-time package was checked at:

`$0.000844895840`

The exact setup-time download is authorized.

No exit-path download is authorized.

Do not broaden candidates, contracts, symbols, schemas, dates, or time windows.

## Objective

1. Recheck the exact four-request cost.
2. Confirm the manifest is unchanged.
3. Confirm the fresh total is no more than `$0.01`.
4. Download only those four setup-time requests.
5. Validate every downloaded file.
6. Immediately rerun the grouped positive-trade funnel across Ideal, Clean Fast
   Break, and Continuation twice.
7. Compare both runs for deterministic equality.
8. Report exactly which missing-data cases changed.

Do not stop after the download when validation succeeds.

## Credential handling

`SAFE_FAST_DB_AUTH` contains the Databento credential for this run.

Use it internally without printing, logging, documenting, or saving it.

Never write the credential to a file.

## Download limits

Download only requests from:

`historical_signal_replay/source_data/richer_export_package_work/day48_grouped_positive_entry_setup_time_request_manifest.json`

Requirements:

- exactly four setup-time requests;
- no exit-path requests;
- fresh checked total at or below `$0.01`;
- raw data stored only in the canonical ignored local data directory;
- raw data must remain untracked and unstaged.

Record for every request:

- candidate;
- schema;
- symbol;
- start and end times;
- returned path;
- byte and row count;
- SHA-256 checksum;
- checked cost;
- actual billed cost when available;
- empty, malformed, late, stale, or contradictory evidence.

## Replay and funnel analysis

After validation, rerun the complete grouped positive-trade funnel twice.

For every affected candidate, report:

- highest stage reached;
- first stage not reached;
- exact blocker;
- contract-selection result;
- price-acceptability result;
- entry-eligibility result;
- entry-recorded result;
- final classification.

Allowed final classifications:

- `VALID_TRADE_CAPTURED`
- `TRUE_NO_TRADE`
- `MISSING_DATA`
- `MISSED_VALID_TRADE`
- `INVALID_TRADE_ALLOWED`
- `UNRESOLVED`

Never classify missing evidence as a true no-trade.

Do not manufacture a contract, quote, fill, entry, exit, winner, or loser.

Do not change frozen trading rules or safety thresholds to produce a trade.

## Required result

Create:

`SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_SETUP_TIME_DOWNLOAD_AND_REPLAY_RESULT.md`

Update when required:

- positive-trade funnel JSON;
- funnel builder or validator;
- focused tests;
- `SAFE_FAST_BUILD_STATE.md`;
- `SAFE_FAST_PROJECT_DASHBOARD.md`;
- `SAFE_FAST_PROJECT_RULE_INDEX.md`;
- current future-chat handoff files.

Show before-and-after totals for:

- valid trades captured;
- true no-trades;
- missing-data cases;
- missed valid trades;
- invalid trades allowed;
- unresolved cases;
- winners;
- losers;
- first blocker by funnel stage.

Answer plainly:

1. Did SAFE-FAST recognize the setup before the move?
2. Did it classify it as a possible trade?
3. Was a tradable option available at that exact time?
4. Was rejection caused by a real safety rule or missing evidence?
5. How many valid trades were caught, missed, or incorrectly allowed?

## Restrictions

Do not modify production, live backend, `main.py`, Railway, deployment,
broker, account, order, credential, or `.env` files.

Do not download exit data.

Do not calculate P&L without a valid entry.

Do not claim profitability, proof, readiness, promotion, or live eligibility.

Do not commit or push.

## Tests

Run:

- direct safe checks and the execution-policy bypass when required;
- manifest and downloaded-file validation;
- positive-trade funnel tests and validator;
- all Ideal, Clean Fast Break, and Continuation replay tests;
- grouped Day 48 tests;
- lifecycle, stage, session, contract, execution, context, and winner tests;
- the complete grouped funnel twice;
- future-chat consistency tests;
- evidence validator;
- intake bridge;
- `git diff --check`.

Remove generated `__pycache__` directories.

## Next task

Create exactly one evidence-driven grouped next task:

- exit-path cost check only for newly proven valid entries;
- positive-entry expansion if coverage remains thin;
- repair task for a proven missed valid trade;
- safety repair for an invalid trade allowed;
- smallest missing-data request only when evidence remains unavailable.

Do not create another governance-only chain.

## Final summary

Return only:

- Baseline
- Fixed
- Blocked
- Next
- Tests
- Files changed
- Ignored raw files downloaded
- Fresh checked cost
- Actual billed cost or `NOT_AVAILABLE`
- Before funnel totals
- After funnel totals
- Valid trades captured
- True no-trades
- Missing-data cases
- Missed valid trades
- Invalid trades allowed
- Unresolved cases
- Winners
- Losers
- Five owner questions and answers
- Exact next grouped task filename