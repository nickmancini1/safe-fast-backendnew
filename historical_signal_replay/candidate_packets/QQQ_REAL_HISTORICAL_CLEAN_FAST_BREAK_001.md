# QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001

## Identity

- Candidate id: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.
- Symbol: `QQQ`.
- Setup type: Clean Fast Break.
- Signal/setup time: `2026-04-13T12:30:00-04:00`.
- Trigger: `613.67`.
- Invalidation: `609.58`.

## Gap Inputs

- Previous regular-session close: `611.02`.
- Previous close timestamp: `2026-04-10T15:30:00-04:00`.
- Signal-day open: `609.455`.
- Signal-day open timestamp: `2026-04-13T09:30:00-04:00`.
- Gap amount: `-1.565`.
- Gap percent: about `-0.2561%`.
- Direction: down.
- Expected latest allowed source time after regression proof: `2026-04-13T12:30:00-04:00`.
- Filled gap-context status: `clean`.
- Filled gap-context as-of: `2026-04-13T12:30:00-04:00`.
- Filled reviewed-before-signal: `true`.

## Databento Data Status

- QQQ OPRA raw files are locally present and structurally validated.
- Definitions, bid/ask quotes, quote timestamps, expiration, strike, side, trades/volume, and open interest/statistics are available for inspection.
- `historical_signal_replay/databento_opra_normalizer.py` exists for read-only normalization and quote inspection support.
- Databento raw data does not by itself decide contract selection, entry, fill, exit, P&L, proof, profitability, or readiness.

## Gap Fixture Status

- Fixture file: `historical_signal_replay/fixtures/qqq_gap_context_regression_fixtures.json`.
- Calculator file: `historical_signal_replay/gap_context_calculator.py`.
- Calculator test file: `tests/test_gap_context_calculator.py`.
- Accepted first QQQ CFB threshold fixture set:
  - `clean`: absolute gap percent `<= 0.30%`.
  - `caution`: absolute gap percent `> 0.30%` and `<= 0.75%`.
  - `fail`: absolute gap percent `> 0.75%`.
  - `unknown`: required data, source/session identity, symbol match, timestamp parsing, no-hindsight clipping, or threshold fixture metadata missing/ambiguous/unproven.
- Known target calculator fixture status: `clean`, with no-hindsight future-data rejection covered by focused tests.
- Work-package gap-context evidence row: filled in `historical_signal_replay/source_data/richer_export_package_work/qqq_cfb_gap_context_completeness_fields_rule.jsonl`.
- Content validator status for this request: passed.

## Current Blockers

- Option-context, execution-context, headline-context, and complete-caution labels are not decided.
- Contract selection, entry, fill, spread/liquidity, exit, stop/invalidation translation, time exit, costs/slippage, failure labels, sample-size requirements, and promotion gates are not decided.

## Context/Caution Status

- Rule review doc: `SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_RULE.md`.
- Decision-needed doc: `SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_DECISION_NEEDED.md`.
- Work-package context/caution row: `historical_signal_replay/source_data/richer_export_package_work/qqq_cfb_complete_context_caution_fields.jsonl`.
- Content validator status for this request: failed.
- Missing fields:
  - `option_context_status`.
  - `headline_context_status`.
  - `execution_context_status`.
  - `complete_caution_review_status`.
- Current rule result: no accepted honest QQQ CFB complete context/caution rule exists yet.
- Databento support: raw option, quote, spread, volume, and open-interest inputs are available for inspection, but no accepted label rule maps them to option or execution context status.
- Headline support: no source-confirmed headline/news/event feed is available for this historical row.
- Aggregation support: complete caution aggregation is not accepted because option, execution, headline, missing-data, timestamp, and precedence rules remain undecided.

## Stale/Spent Expiry Status

- Rule review doc: `SAFE_FAST_DAY41_QQQ_CFB_STALE_SPENT_EXPIRY_RULE.md`.
- Decision-needed doc: `SAFE_FAST_DAY41_QQQ_CFB_STALE_SPENT_EXPIRY_DECISION_NEEDED.md`.
- Replay line 3: initial-break signal candidate at `2026-04-13T12:30:00-04:00`.
- Replay line 4: later same-session follow-through marked spent at `2026-04-13T15:30:00-04:00`.
- Replay line 5: higher-base watch requires a fresh completed breakout at `2026-04-16T13:30:00-04:00`.
- Replay line 6: prior completed break remains spent/no-fresh-trigger at `2026-04-17T15:30:00-04:00`.
- Decision doc: `SAFE_FAST_DAY41_QQQ_CFB_STALE_SPENT_EXPIRY_DECISION.md`.
- Lifecycle fixture file: `historical_signal_replay/fixtures/qqq_cfb_lifecycle_regression_fixtures.json`.
- Lifecycle fixture review: `SAFE_FAST_DAY41_QQQ_CFB_LIFECYCLE_REGRESSION_FIXTURES_REVIEW.md`.
- Lifecycle calculator: `historical_signal_replay/cfb_lifecycle_calculator.py`.
- Lifecycle calculator tests: `tests/test_cfb_lifecycle_calculator.py`.
- Lifecycle calculator review: `SAFE_FAST_DAY41_QQQ_CFB_LIFECYCLE_CALCULATOR_REVIEW.md`.
- Lifecycle evidence fill review: `SAFE_FAST_DAY41_QQQ_CFB_LIFECYCLE_EVIDENCE_FILL_REVIEW.md`.
- Work-package lifecycle evidence row: filled in `historical_signal_replay/source_data/richer_export_package_work/qqq_cfb_stale_spent_expiry_rule_regressions.jsonl`.
- Content validator status for this request: passed.
- Accepted first lifecycle rule: YES, for testing only.
- Freshness window: exact completed initial-break signal candle decision timestamp only.
- Spent behavior: a completed break or follow-through consumes the trigger path; later reuse of the same trigger path is spent.
- Higher-base refresh behavior: a later higher base is not fresh unless a new source-backed trigger, invalidation, and completed breakout exist.
- Missing-data and future-data behavior: missing or ambiguous required lifecycle fields produce `unknown`; future rows, option data, fills, P&L, profitability, and readiness cannot affect setup-time lifecycle state.
- Lifecycle regression rows added: YES.
- Lifecycle calculator created and tested: YES; all 18 accepted fixtures pass.
- Lifecycle evidence filled: YES.

## Next Needed Rule/Test

The QQQ Clean Fast Break gap-context calculator now exists with focused tests against the accepted fixture file.

Current tested behavior:

- Calculate raw gap amount and percent from source-backed previous close and signal-day open.
- Classify by the accepted fixture threshold set.
- Return `unknown` for missing/ambiguous required inputs.
- Prove no-hindsight behavior by ignoring future candles and replay future rows after `2026-04-13T12:30:00-04:00`.
- Preserve `gap_context_as_of` as the latest allowed candle timestamp used by the rule, not the later export timestamp.

The QQQ CFB lifecycle calculator now exists with focused tests against the accepted fixture file.

Current tested lifecycle behavior:

- Classify `fresh`, `stale`, `spent`, `expired`, and `unknown`.
- Preserve `lifecycle_as_of` and `reviewed_before_signal`.
- Return explicit rejection reasons for missing required data and ignored future/forbidden inputs.
- Prove no-hindsight behavior by ignoring future candles, future replay rows, option/fill/P&L/profitability/readiness fields.
- Apply accepted state precedence and higher-base refresh rules.

The next useful step is a focused QQQ CFB complete context/caution decision and regression fixture task, only when explicitly authorized.

## No Proof / No Readiness Status

- Gap-context evidence filled: YES.
- Lifecycle evidence filled: YES.
- All required QQQ CFB evidence filled: NO.
- Backtest authorized: NO.
- Trade chosen: NO.
- P&L calculated: NO.
- Proof accepted: NO.
- Profitability claim made: NO.
- Candidate ready: NO.
- Intake-ready count changed: NO.
