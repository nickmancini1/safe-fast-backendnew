# SAFE-FAST Day 50 Data-Source Registry and Schwab Queue — Codex Task

## Required startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_EXACT_SETUP_DATA_APPROVAL_DOWNLOAD_RESULT.md`
2. `SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_SETUP_EVIDENCE_COMPLETION_OR_REPLACEMENT_RESULT.md`
3. `SAFE_FAST_DAY48_POSITIVE_TRADE_CAPTURE_AND_MISS_ANALYSIS_RESULT.md`
4. `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`
5. `SAFE_FAST_PROJECT_DASHBOARD.md`
6. `SAFE_FAST_PROJECT_RULE_INDEX.md`
7. Current future-chat handoff files identified by the rule index
8. Existing market-data manifests, field consumers, calculators, replay runners,
   validators, and tests

Expected branch: `main`
Expected starting commit: `4fac2e6`
Expected status: clean except this task file.

If local Git and the canonical files disagree, stop and report the exact
conflict.

This is SAFE-FAST build infrastructure work.

Do not modify frozen trading behavior.

Do not download data.

Do not authenticate to Schwab during this task.

## Active objective

End the vague missing-data loop by assigning every required SAFE-FAST field to
an exact source, calculation, fallback, timestamp rule, and unavailable-data
behavior.

Also create the exact next task for a read-only Charles Schwab authentication
and capability audit.

Schwab is the user's likely production broker and the authority for live account
state, submitted orders, order status, and actual fills.

Schwab must not automatically replace Databento for historical backtesting
unless the capability audit proves equivalent historical coverage.

## Required canonical files

Create or consolidate into:

1. `SAFE_FAST_DATA_SOURCE_REGISTRY.md`
2. `historical_signal_replay/config/safe_fast_data_source_registry.json`
3. `watcher_foundation/safe_fast_data_source_resolver.py`
4. `tests/test_safe_fast_data_source_registry.py`
5. `SAFE_FAST_DAY50_DATA_SOURCE_REGISTRY_AND_SCHWAB_QUEUE_RESULT.md`

Create the configuration directory when necessary.

Do not create competing source registries when a canonical equivalent already
exists. Consolidate and mark superseded files clearly.

## Required source hierarchy

### Historical underlying market data

Primary:

- Databento equity datasets and schemas already validated by the repo.
- Current validated example: `DBEQ.BASIC / ohlcv-1h / raw_symbol`.

Secondary:

- Schwab price-history capability, only after the read-only audit verifies its
  exact range, granularity, timestamps, adjustment behavior, and reproducibility.
- TradingView chart export or visual review is manual secondary evidence only.

### Historical options data

Primary:

- Databento `OPRA.PILLAR`.

Required schema mapping:

- contract identity, strike, expiration, option type: `definition`;
- exact quote updates and quote age: `cmbp-1`;
- one-second quote fallback when explicitly validated: `cbbo-1s`;
- option trades: `trades`;
- volume, open interest, and statistics: `statistics`;
- `tcbbo` is supplemental trade-linked evidence and must not be the sole quote-
  freshness source.

Secondary verification:

- Schwab option-chain and quote data after read-only capability validation;
- tastytrade option-chain, quote, spread, liquidity, implied-volatility, and
  Greek checks when available.

Do not average conflicting sources.

A material disagreement becomes `SOURCE_CONFLICT`.

### Live trading and execution records

Primary authority:

- Charles Schwab.

Schwab controls:

- live account balances;
- buying power;
- positions;
- live quotes used for Schwab decisions;
- submitted orders;
- order acknowledgements;
- order status;
- cancellations;
- fills;
- commissions and execution records.

Databento, tastytrade, and TradingView cannot override an actual Schwab fill.

### Volatility

Calculated locally by SAFE-FAST:

- realized volatility from underlying market data;
- option implied volatility and Greeks from option quote, underlying price,
  strike, expiration, interest-rate input, and dividend input when all required
  inputs are present.

Official market-volatility sources:

- Cboe VIX and VIX9D for SPY context;
- Cboe VXN for QQQ context;
- Cboe RVX for IWM context;
- Cboe GVZ for GLD context.

Secondary verification:

- Schwab and tastytrade displayed implied volatility and Greeks.

The registry must distinguish calculated volatility, vendor-displayed
volatility, and official volatility indexes.

### News, filings, and scheduled events

Official primary sources:

- SEC EDGAR for filings;
- Federal Reserve for FOMC and Federal Reserve releases;
- Bureau of Labor Statistics for CPI, PPI, employment, unemployment, and JOLTS;
- Bureau of Economic Analysis for GDP, PCE, income, and spending;
- United States Treasury for official Treasury data;
- issuer investor-relations releases when company-specific events matter.

Timestamped headline API:

- Benzinga API when entitlement and credentials are available.

Secondary/manual verification:

- Schwab news;
- TradingView news and economic calendar.

Official releases control when a headline provider conflicts with the issuing
agency.

### Macro history

Primary historical-vintage source:

- ALFRED for values as they were known on the candidate date.

Supporting sources:

- FRED;
- the issuing agency's official release;
- Federal Reserve;
- BLS;
- BEA;
- Treasury.

Do not silently use revised present-day macro values for historical decisions.

### SAFE-FAST setup labels

Sole authority:

- SAFE-FAST's frozen local rule engine.

External vendors do not supply:

- Ideal;
- Clean Fast Break;
- Continuation;
- developing-stage transitions;
- setup qualification;
- trade-candidate labels.

The registry must map every setup label to:

- exact local calculator or rule consumer;
- required input fields;
- rule version;
- timestamp rule;
- missing-input behavior.

## Required field classification

Every field must be marked as exactly one of:

- `REQUIRED_FOR_SETUP_LABEL`
- `REQUIRED_FOR_TRADE_ELIGIBILITY`
- `REQUIRED_FOR_EXECUTION`
- `REQUIRED_FOR_EXIT`
- `OPTIONAL_CONTEXT`
- `REVIEW_ONLY`

A missing `OPTIONAL_CONTEXT` or `REVIEW_ONLY` field must not block a technical
setup label or trade unless an existing frozen rule explicitly makes it
mandatory.

Do not alter a frozen rule while performing this classification.

When the repo disagrees about whether a field is required, report the exact
conflict and assign no silent default.

## Required registry fields

Every registry entry must include:

- field identifier;
- plain-English meaning;
- requirement class;
- setup families that consume it;
- exact primary source;
- dataset, schema, API, series, endpoint, or local calculator;
- exact secondary source;
- live authority;
- historical authority;
- timestamp and timezone rule;
- historical-vintage rule;
- credential requirement;
- entitlement requirement;
- cost-check requirement;
- local cache location;
- consumer module;
- validation test;
- fallback behavior;
- unavailable-data classification;
- source-conflict behavior;
- whether the field may block setup qualification;
- whether the field may block trade eligibility.

Do not leave `TBD`, `UNKNOWN_SOURCE`, `sufficient source`, or similar vague
language.

When a source cannot yet be proven, use a precise state such as:

- `SOURCE_CAPABILITY_AUDIT_REQUIRED`
- `CREDENTIAL_NOT_CONFIGURED`
- `ENTITLEMENT_NOT_CONFIRMED`
- `SOURCE_UNAVAILABLE_CANDIDATE_EXCLUDED`

## Resolver behavior

Implement a read-only source resolver that:

1. accepts a field identifier and decision timestamp;
2. returns the named source plan;
3. identifies the exact consumer and requirement class;
4. states whether the field may block the current decision;
5. returns the precise next action when data is unavailable;
6. never contacts a vendor or downloads data by itself;
7. never reads or stores secrets.

No future task may report only `MISSING_DATA`.

It must report:

- exact field;
- exact source;
- exact dataset/schema/API/calculator;
- exact timestamp window;
- exact reason unavailable;
- whether it blocks setup, trade, execution, exit, or only optional context;
- exact next action.

## Schwab read-only task

Create exactly:

`SAFE_FAST_DAY50_SCHWAB_READ_ONLY_AUTH_AND_CAPABILITY_AUDIT_CODEX_TASK.md`

Its required scope must include:

1. Audit official Schwab Trader API requirements and existing repo support.
2. Implement OAuth authentication and token renewal in read-only mode.
3. Store tokens outside Git and outside tracked repo files.
4. Never print or document client secrets, access tokens, or refresh tokens.
5. Verify account-list access.
6. Verify balances, buying power, positions, and transaction-history access.
7. Verify quote access.
8. Verify option-chain access.
9. Verify price-history access.
10. Determine historical range, granularity, timestamp semantics, adjustments,
    option-history availability, rate limits, and entitlement limits.
11. Read existing order and fill records when safely available.
12. Do not submit, replace, cancel, or preview an order.
13. Do not call an order-submission endpoint.
14. Compare bounded identical timestamps against Databento.
15. Compare bounded option-chain fields against tastytrade when available.
16. State which historical fields Schwab can replace, supplement, or cannot
    provide.
17. Define a future local Schwab market-data archive for forward replay.
18. Add focused tests and documentation.
19. Update the source registry and future-chat handoffs.
20. Keep production, Railway, live backend, and trading logic untouched.

The Schwab task must require explicit user action only when Schwab's OAuth
browser authorization is actually needed.

## Current candidate blockers

Audit the current eight-candidate setup-field package against the registry.

For every blocker, state:

- exact field;
- proper source;
- whether the field is truly required;
- whether OHLCV should have resolved it;
- why the downloaded OHLCV did or did not resolve it;
- whether local calculation is possible;
- whether a separate official/news/macro source is needed;
- whether the candidate should be excluded instead of remaining indefinitely
  unresolved.

Do not run another incomplete candidate batch.

Do not buy more data during this task.

## Control files and future chats

Update:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`
- `SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt`
- current canonical handoff and next-chat files named by the rule index

Future-chat files must:

- point to the canonical source registry;
- forbid vague `MISSING_DATA`;
- name Schwab as the live broker and execution authority;
- name Databento as the primary historical options source;
- keep setup labels inside SAFE-FAST;
- distinguish required fields from optional context;
- name the exact active task;
- preserve grouped work;
- prevent another incomplete-candidate loop.

## Required tests

Run:

1. direct safe checks;
2. execution-policy bypass if required;
3. registry JSON schema and completeness tests;
4. resolver tests;
5. tests that every currently required field has an exact source;
6. tests that setup labels map only to SAFE-FAST;
7. tests that options history maps primarily to Databento;
8. tests that live Schwab fills remain authoritative;
9. tests that revised macro data cannot silently replace historical vintages;
10. tests that TCBBO alone cannot establish quote freshness;
11. tests that optional context cannot silently block a setup;
12. control-file and future-chat consistency tests;
13. evidence validator;
14. package-to-intake bridge;
15. `git diff --check`.

Remove generated `__pycache__` directories.

Do not commit or push.

## Restrictions

Do not modify:

- frozen trading behavior;
- production or live backend;
- `main.py`;
- Railway or deployment files;
- broker order-submission code;
- account or order behavior;
- credentials;
- `.env`;
- raw market data.

Do not authenticate to Schwab in this task.

Do not download market data.

Do not claim profitability, proof, readiness, promotion, or live eligibility.

## Final summary

Return only:

- Baseline
- Fixed
- Blocked
- Next
- Tests
- Files changed
- Canonical registry files
- Historical options source
- Live broker authority
- Volatility sources
- News and event sources
- Macro sources
- Setup-label source
- Current blockers mapped
- Optional fields removed as blockers
- Exact Schwab task filename
- Exact next task filename