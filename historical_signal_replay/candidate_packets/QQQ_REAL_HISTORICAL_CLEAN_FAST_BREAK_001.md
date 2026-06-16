# QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001

## Batch Restart Status

- Current disposition: parked, not ready.
- Batch lesson: useful completed diagnostic case, not a candidate to keep grinding.
- Passed: gap context, stale/spent lifecycle, and option context under the accepted new-contract open-interest exception.
- Failed: execution context and complete caution review.
- Failure reason: selected quote `ts_event=2026-04-13T16:06:30.640301037Z` was about `23` minutes `29` seconds old at the `2026-04-13T16:30:00Z` setup boundary, so the accepted execution-context calculator returns `execution_context_status=fail` with `rejection_reason=quote_age_above_5_minutes`.
- Do not repeat: no fallback contract scan, no backtest, no P&L, no proof/profitability/readiness claim, and no further QQQ single-issue grind unless a later bounded task explicitly asks for a new diagnostic.

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
- Contract-selection selector: `historical_signal_replay/cfb_contract_selector.py`.
- Contract-selection selector tests: `tests/test_cfb_contract_selector.py`.
- Contract-selection selector review: `SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTOR_REVIEW.md`.
- Contract-selection selector status: implemented for regression work only; all `18` accepted fixtures pass.
- Option-context selector evidence review: `SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_SELECTOR_EVIDENCE_REVIEW.md`.
- Local Databento selector result: abstain. Top-ranked contract `QQQ   260427C00615000` expiring `2026-04-27` at strike `615` and call side has no TCBBO quote at or before `2026-04-13T12:30:00-04:00` in the local quote window. The accepted no-fallback rule prevents selecting another contract.
- Top-contract quote coverage audit: `SAFE_FAST_DAY41_QQQ_CFB_TOP_CONTRACT_QUOTE_COVERAGE_AUDIT.md`.
- Audit result: `QQQ   260427C00615000` maps consistently to `instrument_id=1023411456`; the local TCBBO file has `2` exact rows for that contract and both are after the setup boundary, beginning at `2026-04-13T16:31:13.931412942Z`. No symbol/instrument-id mismatch was found. The blocker is real inside the downloaded ten-minute window; a cost-checked single-contract wider TCBBO pull is the smallest possible follow-up if more data is authorized.
- Option-context rerun with wider quotes: `SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_RERUN_WITH_WIDER_QUOTES_REVIEW.md`.
- Wider top-contract quote result: `historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_top_contract_1023411456_tcbbo_0930_1230_et.csv` exists and contains `28` TCBBO rows for `instrument_id=1023411456`, all at or before setup time. The nearest at-or-before quote is `2026-04-13T16:06:30.640301037Z` with bid `7.76`, ask `7.80`, spread `0.04`, bid size `3`, and ask size `31`.
- Selector rerun result: the old quote timestamp blocker is cured, but the accepted selector still abstains because the top-ranked contract has `trade_volume_through_setup=0` from the existing trade file and no timestamp-safe same-contract open-interest/statistics row. No fallback is allowed.
- Option-context rerun with trades/statistics: `SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_RERUN_WITH_TRADES_STATS_REVIEW.md`.
- New top-contract trades/statistics result: `historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_top_contract_1023411456_trades_0930_1230_et.csv` exists and contains `28` trade rows for `instrument_id=1023411456`, all at or before setup time, with setup-time-safe trade volume `65`. `historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_top_contract_1023411456_statistics_0930_1230_et.csv` exists but contains `0` rows, so timestamp-safe same-contract open interest remains missing.
- Selector rerun with new trades/statistics result: the old trade-volume blocker is cured, but the accepted selector still abstains because the top-ranked contract has no timestamp-safe same-contract open-interest/statistics row. No fallback is allowed.
- Filled option-context status after trades/statistics selector rerun: `unknown`.
- Open-interest gate decision: `SAFE_FAST_DAY41_QQQ_CFB_OPEN_INTEREST_GATE_DECISION.md`.
- Open-interest gate result: same-contract setup-time-safe open interest remains required for the base QQQ CFB option-context rule; missing open interest is `unknown` and volume-only liquidity is not accepted as a pass. A later explicit human rule decision accepted the narrow new-contract OI exception for a newly listed selected contract with passing quote, spread, size, volume, no-future-data, and no-fallback gates.
- Open-interest source audit: `SAFE_FAST_DAY41_QQQ_CFB_OPEN_INTEREST_SOURCE_AUDIT.md`.
- Open-interest source audit result: current local QQQ OPRA files do not contain timestamp-safe same-contract open interest for `QQQ   260427C00615000` / `instrument_id=1023411456`. The full-day statistics file has `178,488` `stat_type=9` open-interest rows overall, but `0` same-contract open-interest rows; the same contract has `88` statistics rows, all after setup and none with `stat_type=9`; the targeted setup-window statistics file has `0` rows. The later new-contract OI exception handles this target as `caution`, not `clean`, because prior-day open interest cannot exist for the not-listed contract.
- Target contract listing / open-interest audit: `SAFE_FAST_DAY41_QQQ_CFB_TARGET_CONTRACT_LISTING_OI_AUDIT.md`.
- Target contract listing / open-interest audit result: Apr 13 definitions list `QQQ   260427C00615000` / `instrument_id=1023411456` at CSV line `10022` with `security_update_action=A` and `ts_event=2026-04-13T12:00:00.445628903Z`, before setup. The local Apr 10 parent definitions file has `10,212` rows and `0` matches for the target instrument, target symbol, or same `2026-04-27` call `615` contract shape. Prior-day same-contract open interest is unavailable from the current local prior-day definition source, which supports the accepted new-contract OI exception only as `caution`.
- New-contract open-interest exception rule: `SAFE_FAST_DAY41_QQQ_CFB_NEW_CONTRACT_OI_EXCEPTION_RULE.md`.
- New-contract open-interest exception result: accepted for regression work. If the already selected top-ranked contract was not listed on the prior trading day, prior-day same-contract open interest is not required, but the contract must be listed before setup and must still pass setup-time-safe quote, spread, spread-percent, bid-size, ask-size, trade-volume, no-future-data, and no-fallback checks. The exception result is `caution`, not `clean`, because open interest is unavailable.
- New-contract open-interest exception fixture file: `historical_signal_replay/fixtures/qqq_cfb_new_contract_oi_exception_regression_fixtures.json`.
- New-contract open-interest exception fixture review: `SAFE_FAST_DAY41_QQQ_CFB_NEW_CONTRACT_OI_EXCEPTION_FIXTURES_REVIEW.md`.
- New-contract open-interest exception regression fixtures added: YES, `13` data-only fixtures covering valid caution, listing-after-signal, prior-day-present missing OI, missing listing timestamp, missing quote, quote-after-signal, spread, spread-percent, bid-size, ask-size, trade-volume, no-fallback, and future-data rejection cases.
- New-contract open-interest exception selector review: `SAFE_FAST_DAY41_QQQ_CFB_NEW_CONTRACT_OI_EXCEPTION_SELECTOR_REVIEW.md`.
- New-contract open-interest exception selector result: implemented for regression work. The valid newly listed missing-OI fixture returns `option_context_status=caution`; the prior-day-present missing-OI, listing, quote, spread, size, trade-volume, no-fallback, and future-data fixtures remain rejected as `unknown`.
- Option-context new-contract OI evidence fill review: `SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_NEW_CONTRACT_OI_EVIDENCE_FILL_REVIEW.md`.
- Current recorded work-package fields are now `option_context_status=caution` under the accepted new-contract OI exception, `execution_context_status=fail` under the accepted execution-context calculator, `complete_caution_review_status=fail` under accepted precedence, and `headline_context_status=unknown`.
- Execution-context rule decision: `SAFE_FAST_DAY41_QQQ_CFB_EXECUTION_CONTEXT_RULE_DECISION.md`.
- Execution-context rule result: accepted for regression work. Quote age `<= 60` seconds is `clean`; quote age `> 60` seconds and `<= 5` minutes is `caution`; quote age `> 5` minutes, quote-after-signal, spread failure, missing/invalid bid/ask, missing/invalid size, missing setup-time-safe volume, or fallback is `fail`; missing source/rule proof is `unknown`.
- Execution-context fixture file: `historical_signal_replay/fixtures/qqq_cfb_execution_context_regression_fixtures.json`.
- Execution-context fixture review: `SAFE_FAST_DAY41_QQQ_CFB_EXECUTION_CONTEXT_FIXTURES_REVIEW.md`.
- Execution-context regression fixtures added: YES, `13` data-only fixtures covering clean quote age, caution quote age, fail quote too old, the known QQQ stale quote fail, quote-after-signal rejection, missing bid, missing ask, bad spread, missing size, missing volume, missing source data as `unknown`, no fallback, and forbidden P&L/proof/readiness field rejection.
- Execution-context calculator: `historical_signal_replay/execution_context_calculator.py`.
- Execution-context calculator tests: `tests/test_execution_context_calculator.py`.
- Execution-context calculator review: `SAFE_FAST_DAY41_QQQ_CFB_EXECUTION_CONTEXT_CALCULATOR_REVIEW.md`.
- Execution-context calculator result: implemented for regression work; all `13` accepted fixtures pass.
- Execution-context evidence fill review: `SAFE_FAST_DAY41_QQQ_CFB_EXECUTION_CONTEXT_EVIDENCE_FILL_REVIEW.md`.
- Target execution-context evidence: the selected quote at `2026-04-13T16:06:30.640301037Z` is about `23` minutes `29.359699` seconds old at the `2026-04-13T16:30:00Z` setup boundary, so the filled target result is `execution_context_status=fail` with `rejection_reason=quote_age_above_5_minutes`.
- Later-test fill basis: ask price only for long-call testing; target ask is `7.80`. No fill evidence, P&L, backtest, proof, profitability, readiness, or intake-ready change is authorized.
- One selected real trade remains unchosen. The accepted selector and evidence fill still do not authorize backtest, P&L, proof, profitability, or readiness.

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

- Broader option-context, headline-context, and trade-plan proof labels are not decided.
- Open-interest gate decision is now listing-aware only for newly listed selected contracts: quote, spread, quote-size, and trade-volume gates pass for the top-ranked contract, and the target contract was listed before setup on Apr 13 but absent from local Apr 10 parent definitions. The narrow exception and selector fixtures classify the exception result as `caution`, not `clean`, and the work-package option-context field is filled as `caution`. Execution is filled as `fail` because the selected quote is older than `5` minutes, complete caution is filled as `fail` by precedence, and headline remains `unknown`.
- Reviewed option-universe, quote eligibility, the first one-contract selection rule, contract-selection regression fixtures, and selector/calculator implementation are accepted for regression work, but evidence fill, entry, fill, exit, stop/invalidation translation, time exit, costs/slippage, failure labels, sample-size requirements, and promotion gates are not decided or not implemented.

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
- Content validator status for this request: passed after bounded `execution_context_status=fail` and `complete_caution_review_status=fail` fill.
- Bridge status for this candidate: reconsideration-eligible, with intake-ready `NO` and proof allowed `NO`.
- Filled fields:
  - `option_context_status=caution`.
  - `headline_context_status=unknown`.
  - `execution_context_status=fail`.
  - `complete_caution_review_status=fail`.
- Current rule result: first conservative framework accepted; bounded option-context and execution-context evidence fills completed for the target row.
- Accepted framework: statuses `clean`, `caution`, `fail`, and `unknown`; setup-time source/timestamp rules; forbidden future-data behavior; missing-data behavior; and complete-caution aggregation precedence of `fail`, then `unknown`, then `caution`, then `clean`.
- Regression fixture status: data-only framework fixtures added for option, headline, and execution component statuses; complete-caution precedence; missing-data behavior; no-hindsight future-data rejection; wrong identity rejection; and forbidden fill/P&L/profitability/readiness rejection.
- Databento support: raw option, quote, spread, volume, and open-interest inputs are available for inspection. The first execution-context quote-age/spread/size/volume rule, fixtures, calculator, and bounded target evidence fill are accepted.
- Headline support: no source-confirmed headline/news/event feed is available for this historical row.
- Missing-decision defaults: no source-confirmed historical headline/no-headline source keeps headline context `unknown`. Earlier missing option/execution defaults are superseded for this target row by the accepted new-contract OI exception and accepted execution-context evidence fill.
- Calculator status: created and tested against all 22 accepted framework fixtures. It classifies option, headline, execution, and complete-caution statuses, applies precedence `fail`, then `unknown`, then `caution`, then `clean`, rejects wrong identity and future/forbidden inputs, and refuses trade/P&L/proof/readiness inference.
- Aggregation support: precedence is accepted and calculator-backed. Complete caution is filled as `fail` because the accepted execution-context calculator returns `fail`, and fail beats unknown, caution, and clean. Headline source/category policy remains unresolved and `headline_context_status` remains `unknown`.
- Selected-contract policy update: first reviewed-universe, quote-eligibility, one-contract selection rules, contract-selection fixtures, and contract-selection selector are accepted for regression work only. Complete caution is now `fail` because the selected quote fails the accepted execution quote-age rule.
- Option-context selector evidence update: the selector was applied to local Databento QQQ OPRA files and initially abstained on the top-ranked contract because no setup-time-safe quote was available. The wider quote rerun found setup-time-safe quotes. The new trades/statistics rerun found setup-time-safe trade volume `65`, curing the trade-volume gate. The new-contract OI exception selector returns `caution` for the accepted newly listed missing-OI case, and the work-package option-context field is now filled as `caution`; execution and complete caution are filled as `fail`; headline remains `unknown`.
- Top-contract quote coverage audit update: the exact top contract mapping is consistent, and local ten-minute TCBBO/trade rows for the contract exist only after signal time. The wider quote rerun cures the quote-only blocker and the new trades file cures the trade-volume blocker without filling evidence or changing the accepted selector rule. Timestamp-safe same-contract open interest remains missing.

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
- Preserve blocker defaults unless later accepted source/rule decisions support a target-row fill.
- Reject wrong identity, future option/headline data, and forbidden fill/P&L/profitability/readiness fields.
- Refuse trade choice, P&L, proof, profitability, and readiness inference.

Context/caution evidence fill is completed for the target row with `option_context_status=caution`, `headline_context_status=unknown`, `execution_context_status=fail`, and `complete_caution_review_status=fail`.

The QQQ CFB contract-selection regression fixture file and selector now exist.

Current fixture coverage:

- valid selected contract;
- wrong side, DTE, strike, spread, spread percent, missing bid/ask, bid/ask size, volume, open interest, quote timestamp, and statistics timestamp rejection;
- nearest valid expiration and lowest strike greater than or equal to trigger selected;
- no fallback after a top-ranked contract fails;
- abstain when no contract passes.

Contract-selection selector/calculator implementation now exists and passes all `18` accepted fixtures. No evidence fill, backtest, real trade choice, P&L, proof, profitability, or readiness is authorized from the fixture file or selector alone.

## No Proof / No Readiness Status

- Gap-context evidence filled: YES.
- Lifecycle evidence filled: YES.
- QQQ CFB work-package requests pass content validation after this evidence fill; option context is `caution`, headline context is `unknown`, execution context is `fail`, and complete caution is `fail`. This remains request-shaped evidence only.
- Backtest authorized: NO.
- Trade chosen: NO.
- P&L calculated: NO.
- Proof accepted: NO.
- Profitability claim made: NO.
- Candidate ready: NO.
- Intake-ready count changed: NO.
