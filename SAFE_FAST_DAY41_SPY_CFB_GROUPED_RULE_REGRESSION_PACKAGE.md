# SAFE-FAST Day 41 SPY CFB Grouped Rule/Regression Package

## Scope

- Candidates:
  - `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`
  - `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`
- Symbol/setup family: SPY / Clean Fast Break.
- Task mode: grouped lifecycle rule/regression authorization only.
- Starter Databento files remain read-only starter inputs for later raw inspection.

## Guardrails

- Downloaded more data: NO.
- Used full-window data: NO.
- Filled evidence: NO.
- Backtested: NO.
- Calculated P&L: NO.
- Claimed proof or profitability: NO.
- Marked any candidate ready: NO.
- Modified raw Databento files: NO.
- Modified `main.py`, live/engine trading logic, broker/order/account code, Railway/deploy files, `.env`, secrets, or generated live reports/logs: NO.

## Inputs Reviewed

- Build state: `SAFE_FAST_BUILD_STATE.md`.
- Dashboard: `SAFE_FAST_PROJECT_DASHBOARD.md`.
- Rule index: `SAFE_FAST_PROJECT_RULE_INDEX.md`.
- Starter inspection: `SAFE_FAST_DAY41_STARTER_BATCH_OPTION_INSPECTION.md`.
- Candidate packets:
  - `historical_signal_replay/candidate_packets/SPY_REAL_HISTORICAL_CLEAN_FAST_BREAK_002.md`
  - `historical_signal_replay/candidate_packets/SPY_REAL_HISTORICAL_CLEAN_FAST_BREAK_003.md`
- SPY source CSV:
  - `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`
- SPY replay log:
  - `historical_signal_replay/reports/third_real_spy_clean_fast_break_replay_v1_signal_log.jsonl`
- QQQ CFB lifecycle artifacts, as structure only:
  - `SAFE_FAST_DAY41_QQQ_CFB_STALE_SPENT_EXPIRY_DECISION.md`
  - `historical_signal_replay/fixtures/qqq_cfb_lifecycle_regression_fixtures.json`

## What Can Be Reused From QQQ CFB

The following can be reused as implementation and documentation structure only:

- status vocabulary: `fresh`, `stale`, `spent`, `expired`, `unknown`;
- no-hindsight boundary shape;
- state precedence shape;
- missing-data behavior shape;
- future-data rejection shape;
- data-only fixture file structure.

The following cannot be reused blindly:

- QQQ candidate identity;
- QQQ trigger/invalidation values;
- QQQ replay-line interpretations;
- QQQ option-contract selection rules;
- QQQ open-interest exception behavior;
- QQQ execution quote-age evidence result;
- any proof, profitability, readiness, or trade-plan conclusion.

## Accepted First SPY CFB Lifecycle Rule

The first SPY Clean Fast Break lifecycle rule is accepted for data-only regression work.

The rule covers two SPY CFB lifecycle shapes:

- initial-break lifecycle for `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`;
- higher-base fresh-break lifecycle for `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`.

The rule is conservative:

- a completed SPY Clean Fast Break signal is `fresh` only at the exact source-backed completed signal candle decision timestamp;
- the same trigger path cannot remain fresh after that timestamp;
- a completed break, follow-through context, or explicit prior-completed-break blocker consumes the trigger path and makes later reuse `spent`;
- a higher-base path is watch-only `stale` until a source-backed new trigger, new invalidation, and completed breakout exist at or before the decision timestamp;
- missing identity, timestamp, trigger, invalidation, stage, trigger-state, prior-state, rule metadata, or no-hindsight proof returns `unknown`;
- a previously fresh signal reviewed later without spent evidence is `expired`;
- future candles, later replay rows, option data, fills, P&L, proof, profitability, and readiness are forbidden lifecycle inputs.

## State Definitions

`fresh`: exact completed SPY Clean Fast Break initial-break or accepted higher-base fresh-break signal candle timestamp, with matching SPY/Clean Fast Break identity, trigger, invalidation, `trigger_state=triggered`, source-backed row ordering, and no prior completed break consuming that trigger path.

`stale`: SPY Clean Fast Break watch/candidate path with source-backed trigger/invalidation context but no completed breakout at the decision timestamp.

`spent`: the same trigger path already produced a completed break, follow-through context, or explicit prior-completed-break blocker.

`expired`: a previously fresh SPY Clean Fast Break signal reviewed after the exact signal candle timestamp when no higher-precedence spent evidence applies.

`unknown`: required lifecycle data, rule metadata, identity, row ordering, or no-hindsight proof is missing, invalid, ambiguous, wrong-symbol, wrong-setup, malformed, or future-contaminated.

## State Precedence

Apply lifecycle states in this order:

1. `unknown`
2. `spent`
3. `fresh`
4. `expired`
5. `stale`

## Target Row Interpretation

`SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`:

- source CSV line 138 is the setup-time OHLCV row at `2026-04-13T12:30:00-04:00`;
- replay log line 2 is the fresh initial-break signal candidate at `2026-04-13T12:30:00-04:00`;
- replay log line 3 is later same-session follow-through/spent context and must not be used to decide setup-time freshness.

`SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`:

- source CSV line 154 is the setup-time OHLCV row at `2026-04-15T14:30:00-04:00`;
- replay log line 4 is the higher-base watch context at `2026-04-15T11:30:00-04:00`;
- replay log line 5 is the fresh higher-base signal candidate at `2026-04-15T14:30:00-04:00`;
- replay log line 6 is later spent context and must not be used to decide setup-time freshness.

## Data-Only Regression Fixtures

Fixture file created:

- `historical_signal_replay/fixtures/spy_cfb_lifecycle_regression_fixtures.json`

Fixture coverage:

- SPY CFB 002 fresh initial break at setup time;
- SPY CFB 002 same-session follow-through classified `spent`;
- SPY CFB 002 later review of a previously fresh signal classified `expired` when no spent evidence applies;
- SPY CFB 003 higher-base watch classified `stale`;
- SPY CFB 003 higher-base completed fresh break at setup time;
- SPY CFB 003 later spent context;
- missing trigger and missing invalidation as `unknown`;
- wrong symbol and wrong setup as `unknown`;
- future replay row rejection;
- option/fill/P&L/proof/profitability/readiness rejection.

## What This Authorizes

- SPY CFB lifecycle regression fixture work for the two grouped candidates.
- Later implementation of a lifecycle calculator against the accepted SPY fixture file, if explicitly requested.
- Later read-only raw starter option inspection for SPY CFB after the lifecycle package exists.

## What This Does Not Authorize

- Evidence fill.
- Contract selection as a real trade.
- Entry, fill, exit, stop/invalidation, time exit, cost, slippage, sample-size, or promotion rules.
- Backtest.
- P&L.
- Proof.
- Profitability.
- Candidate readiness.
- Intake-ready status changes.

## Result

SPY CFB grouped lifecycle rule accepted for data-only regression work: YES.

Data-only regression fixtures created: YES.

Evidence filled: NO.

Raw starter option inspection performed in this task: NO.

Proof accepted: NO.

Profitability claimed: NO.
