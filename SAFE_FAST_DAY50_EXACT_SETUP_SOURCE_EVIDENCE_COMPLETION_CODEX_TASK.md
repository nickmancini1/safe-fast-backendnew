# SAFE-FAST Day 50 Exact Setup-Source Evidence Completion

## Required startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DAY50_GROUPED_REQUIRED_SETUP_SOURCE_RESOLUTION_AND_REPLAY_RESULT.md`
2. `historical_signal_replay/results/day50_required_setup_source_resolution.json`
3. `SAFE_FAST_DATA_SOURCE_REGISTRY.md`
4. `historical_signal_replay/config/safe_fast_data_source_registry.json`
5. `SAFE_FAST_PROJECT_DASHBOARD.md`
6. `SAFE_FAST_PROJECT_RULE_INDEX.md`
7. Existing Ideal, Clean Fast Break, and Continuation replay runners, calculators, fixtures, validators, ignored local data, and regression tests.

Expected branch: `main`.
Expected starting status: clean except this task file and known temp-directory permission warnings.

If local Git or canonical control files disagree, stop and report the exact conflict.

## Objective

Complete or close the four remaining exact setup-source requests from Day 50:

- `GLD-REPLACEMENT-IDEAL-CANDIDATE-001`
- `SPY-SOURCE-WINDOW-CLEAN-FAST-BREAK-003`
- `IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001`
- `IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002`

Use only exact source-backed local replay output or reviewer-completed setup-source packets over the named source windows. Do not create another candidate batch.

## Required fields

For each candidate, resolve or formally close:

- `setup_time_row`
- `trigger`
- `invalidation`
- `freshness_final_signal_state`
- `blocker_caution_review`
- `no_hindsight_boundary`
- `session_boundary_behavior`

Optional macro/news/volatility context must be `CONTEXT_UNKNOWN` unless an existing frozen rule explicitly makes it mandatory.

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
Do not request option data before a candidate reaches `TRADE_CANDIDATE`.
Do not request exit data before a valid entry is established.
Do not claim profitability, proof, readiness, promotion, paper eligibility, or live eligibility.
Do not commit or push.

`SAFE_FAST_DB_AUTH` may be used only for cost checks if a valid paid-data request is created. Never print, save, document, or echo it.

## Required outputs

Create a result file and machine-readable JSON for this task.

Update:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`
- `SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt`

Create exactly one next grouped task based on the result:

- grouped option-contract and fresh-quote testing only if a candidate reaches `TRADE_CANDIDATE`;
- exact approval/download task only if a validated paid-data request is required;
- grouped repair task only if complete evidence proves a rule or harness defect;
- positive-entry expansion only after all current slots are resolved or closed.

## Required tests

Run focused setup-source tests, the Day 50 source-resolution test, the data-source registry tests, the resolved candidate replay twice, the Day 48 positive-trade funnel regression twice, relevant Ideal/CFB/Continuation/stage/session tests, contract-selection and quote-freshness tests, evidence validator, package-to-intake bridge, future-chat consistency tests, and `git diff --check`.
