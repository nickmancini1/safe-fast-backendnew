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
- First selected-contract policy doc: `SAFE_FAST_DAY41_QQQ_CFB_SELECTED_CONTRACT_POLICY.md`.
- Reviewed-universe policy accepted for regression work only: QQQ options listed on `2026-04-13`, expirations `2026-04-27` through `2026-05-13` when present, strikes `590` through `640`, both calls and puts retained while side is blocked, and valid Databento TCBBO quote nearest-at-or-before setup time by `ts_event`.
- Decision-needed doc: `SAFE_FAST_DAY41_QQQ_CFB_SELECTED_CONTRACT_POLICY_DECISION_NEEDED.md`.
- First contract-selection decision doc: `SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTION_DECISION.md`.
- First contract-selection still-blocked doc: `SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTION_DECISION_STILL_BLOCKED.md`.
- Contract-selection decision accepted for regression work only: long calls only; nearest reviewed-universe expiration with DTE at least `14`; lowest reviewed-universe call strike greater than or equal to trigger `613.67`; nearest OTM-by-trigger moneyness; quote nearest-at-or-before setup time by `ts_event`; maximum spread `0.15`; maximum spread percent `2.00%`; minimum bid size, ask size, through-setup trade volume, and open interest of `1`; strict statistics timestamp handling; missing-data abstain/unknown behavior; and no fallback scan after a top-ranked contract fails a gate.
- Contract-selection fixture file: `historical_signal_replay/fixtures/qqq_cfb_contract_selection_regression_fixtures.json`.
- Contract-selection fixture review: `SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTION_FIXTURES_REVIEW.md`.
- Contract-selection regression fixtures added: YES, covering valid selection, wrong side, DTE, expiration ranking, strike ranking, spread, spread percent, bid/ask, bid/ask size, volume, open interest, quote/statistics timestamp rejection, no fallback, and no-pass abstain cases.
- One selected real trade remains unchosen. The accepted rule still needs selector/calculator implementation before any evidence fill, backtest, P&L, proof, profitability, or readiness step.

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

- Option-context, execution-context, headline-context, and complete-caution clean/caution/fail labels are not decided.
- Reviewed option-universe, quote eligibility, the first one-contract selection rule, and contract-selection regression fixtures are accepted for regression work, but selector/calculator implementation, entry, fill, exit, stop/invalidation translation, time exit, costs/slippage, failure labels, sample-size requirements, and promotion gates are not decided or not implemented.

## Context/Caution Status

- Rule review doc: `SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_RULE.md`.
- Decision-needed doc: `SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_DECISION_NEEDED.md`.
- Framework decision doc: `SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_DECISION.md`.
- Still-blocked doc: `SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_DECISION_STILL_BLOCKED.md`.
- Regression fixture file: `historical_signal_replay/fixtures/qqq_cfb_context_caution_regression_fixtures.json`.
- Regression fixture review: `SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_REGRESSION_FIXTURES_REVIEW.md`.
- Blocked fixture doc: `SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_FIXTURES_BLOCKED.md`.
- Missing-decisions doc: `SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_MISSING_DECISIONS.md`.
- Calculator file: `historical_signal_replay/context_caution_calculator.py`.
- Calculator test file: `tests/test_context_caution_calculator.py`.
- Calculator review: `SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_CALCULATOR_REVIEW.md`.
- Work-package context/caution row: `historical_signal_replay/source_data/richer_export_package_work/qqq_cfb_complete_context_caution_fields.jsonl`.
- Content validator status for this request: passed after blocker-preserving `unknown` fill.
- Bridge status for this candidate: reconsideration-eligible, with intake-ready `NO` and proof allowed `NO`.
- Filled fields:
  - `option_context_status=unknown`.
  - `headline_context_status=unknown`.
  - `execution_context_status=unknown`.
  - `complete_caution_review_status=unknown`.
- Current rule result: first conservative framework accepted; blocker-preserving `unknown` evidence fill completed for the target row.
- Accepted framework: statuses `clean`, `caution`, `fail`, and `unknown`; setup-time source/timestamp rules; forbidden future-data behavior; missing-data behavior; and complete-caution aggregation precedence of `fail`, then `unknown`, then `caution`, then `clean`.
- Regression fixture status: data-only framework fixtures added for option, headline, and execution component statuses; complete-caution precedence; missing-data behavior; no-hindsight future-data rejection; wrong identity rejection; and forbidden fill/P&L/profitability/readiness rejection.
- Databento support: raw option, quote, spread, volume, and open-interest inputs are available for inspection, but no accepted label rule maps them to option or execution context status.
- Headline support: no source-confirmed headline/news/event feed is available for this historical row.
- Missing-decision defaults: no selected contract policy kept option context `unknown`; no source-confirmed historical headline/no-headline source keeps headline context `unknown`; no accepted execution entry/fill rule keeps execution context `unknown`; complete caution review cannot pass if any required component is `unknown`. The first reviewed-universe/eligibility policy is now accepted, but one-contract ranking and option thresholds remain blocked.
- Calculator status: created and tested against all 22 accepted framework fixtures. It classifies option, headline, execution, and complete-caution statuses, applies precedence `fail`, then `unknown`, then `caution`, then `clean`, rejects wrong identity and future/forbidden inputs, and refuses trade/P&L/proof/readiness inference.
- Aggregation support: precedence is accepted and calculator-backed. Complete caution is filled as `unknown` because option thresholds, selected-contract one-contract ranking, execution trade-plan rules, and headline source/category policy remain undecided for clean/caution/fail evidence fills.
- Selected-contract policy update: first reviewed-universe, quote-eligibility, one-contract selection rules, and contract-selection fixtures are accepted for regression work only. Complete caution remains `unknown` because contract-selection implementation, execution entry/fill rule, broader option-context labels, and headline source/category policy remain missing.

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

The QQQ CFB context/caution calculator now exists with focused tests against the accepted fixture file.

Current tested context/caution behavior:

- Classify option, headline, execution, and complete-caution statuses.
- Apply complete-caution precedence: `fail`, then `unknown`, then `caution`, then `clean`.
- Preserve blocker defaults so target option, headline, execution, and complete caution remain `unknown` without later accepted source/rule decisions.
- Reject wrong identity, future option/headline data, and forbidden fill/P&L/profitability/readiness fields.
- Refuse trade choice, P&L, proof, profitability, and readiness inference.

Context/caution evidence fill is completed only as blocker-preserving `unknown` statuses.

The QQQ CFB contract-selection regression fixture file now exists.

Current fixture coverage:

- valid selected contract;
- wrong side, DTE, strike, spread, spread percent, missing bid/ask, bid/ask size, volume, open interest, quote timestamp, and statistics timestamp rejection;
- nearest valid expiration and lowest strike greater than or equal to trigger selected;
- no fallback after a top-ranked contract fails;
- abstain when no contract passes.

Contract-selection selector/calculator implementation is still missing. No evidence fill, backtest, real trade choice, P&L, proof, profitability, or readiness is authorized from the fixture file alone.

## No Proof / No Readiness Status

- Gap-context evidence filled: YES.
- Lifecycle evidence filled: YES.
- All required QQQ CFB evidence filled: YES, only as request-shaped fields; complete caution remains `unknown`.
- Backtest authorized: NO.
- Trade chosen: NO.
- P&L calculated: NO.
- Proof accepted: NO.
- Profitability claim made: NO.
- Candidate ready: NO.
- Intake-ready count changed: NO.
