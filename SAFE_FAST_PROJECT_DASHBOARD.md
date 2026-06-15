# SAFE-FAST Project Dashboard

## Current Checkpoint

- Baseline commit for this new-contract open-interest exception fixtures task: `63a4748 Accept QQQ CFB new contract OI exception rule`.
- Current Day 41 checkpoint: QQQ Clean Fast Break contract selector now exists at `historical_signal_replay/cfb_contract_selector.py` with focused tests at `tests/test_cfb_contract_selector.py`. The selector passes all `18` accepted contract-selection fixtures. Applied to the local Databento QQQ files in `SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_SELECTOR_EVIDENCE_REVIEW.md`, it initially abstained because the top-ranked `QQQ   260427C00615000` call had no setup-time-safe TCBBO quote and no fallback was allowed. `SAFE_FAST_DAY41_QQQ_CFB_TOP_CONTRACT_QUOTE_COVERAGE_AUDIT.md` confirmed the mapping to `instrument_id=1023411456` was consistent. `SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_RERUN_WITH_WIDER_QUOTES_REVIEW.md` cured the prior quote blocker with `28` setup-time-safe wider quote rows. `SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_RERUN_WITH_TRADES_STATS_REVIEW.md` cured the prior trade-volume blocker with `65` setup-time-safe contracts, but the new statistics file has `0` rows. `SAFE_FAST_DAY41_QQQ_CFB_OPEN_INTEREST_GATE_DECISION.md` kept same-contract setup-time-safe open interest required for the first QQQ CFB option-context rule. `SAFE_FAST_DAY41_QQQ_CFB_OPEN_INTEREST_SOURCE_AUDIT.md` confirms the current local QQQ OPRA files do not contain timestamp-safe same-contract open interest. `SAFE_FAST_DAY41_QQQ_CFB_TARGET_CONTRACT_LISTING_OI_AUDIT.md` confirms the target contract was listed before setup on Apr 13 (`ts_event=2026-04-13T12:00:00.445628903Z`), but was absent from the Apr 10 parent definitions (`target_matches=0`). `SAFE_FAST_DAY41_QQQ_CFB_NEW_CONTRACT_OI_EXCEPTION_RULE.md` accepts a narrow listing-aware exception for regression work: a newly listed selected contract may satisfy the open-interest component as `caution`, not `clean`, only when it was not listed on the prior trading day and all setup-time quote, spread, size, volume, timestamp, no-future-data, and no-fallback checks pass. `historical_signal_replay/fixtures/qqq_cfb_new_contract_oi_exception_regression_fixtures.json` now records `13` data-only regression fixtures for that exception. For the target QQQ contract, the expected option-context result after selector/rule implementation remains `caution`; current evidence files and selector code remain unchanged, so recorded `option_context_status` remains `unknown`. This does not choose a real trade, backtest, calculate P&L, claim proof/profitability, or mark readiness.
- Proof accepted: NO.
- Profitability claim made: NO.
- Intake-ready count changed: NO.
- QQQ candidate ready: NO.
- Content validation result after context/caution fill: `3` passed requests, `6` failed requests.
- Bridge result after context/caution fill: QQQ reconsideration-eligible, intake-ready `NO`, proof allowed `NO`.

## Active Objective

Turn the current QQQ Clean Fast Break path from documented raw inputs and fixture decisions into tested, no-hindsight calculators and later complete trade-plan evidence. The immediate next work should be the smallest authorized rule/test step, not broad rediscovery.

## Completed Breakthroughs

- Project-wide proof pipeline and trade-plan completeness gate are documented.
- Databento QQQ OPRA files are locally present and structurally validated, but raw vendor files remain local-only.
- Databento OPRA normalizer exists with focused tests and supports read-only local parsing, joins, timestamps, quote selection, and spread/liquidity inspection fields.
- QQQ Clean Fast Break rule-decision package inventories the missing decisions before evidence fill or backtest.
- First QQQ Clean Fast Break gap-context threshold fixture set is accepted for regression work:
  - `clean`: absolute gap percent `<= 0.30%`.
  - `caution`: absolute gap percent `> 0.30%` and `<= 0.75%`.
  - `fail`: absolute gap percent `> 0.75%`.
  - `unknown`: missing or unproven required inputs, source/session identity, symbol match, timestamp parsing, no-hindsight clipping, or threshold metadata.
- QQQ gap-context regression fixtures exist at `historical_signal_replay/fixtures/qqq_gap_context_regression_fixtures.json`.
- QQQ gap-context calculator exists at `historical_signal_replay/gap_context_calculator.py` with focused fixture-driven tests at `tests/test_gap_context_calculator.py`.
- QQQ CFB gap-context work-package request now passes content validation with `gap_context_status`, `gap_context_as_of`, and `gap_context_reviewed_before_signal` filled for `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.
- QQQ CFB stale/spent expiry review records the current replay lifecycle labels in `SAFE_FAST_DAY41_QQQ_CFB_STALE_SPENT_EXPIRY_RULE.md`.
- QQQ CFB stale/spent expiry first testing decision is accepted in `SAFE_FAST_DAY41_QQQ_CFB_STALE_SPENT_EXPIRY_DECISION.md`: same-candle initial-break freshness, spent preservation after completed break/follow-through, higher-base refresh only with new source-backed trigger/invalidation and completed breakout, explicit stale/expired/unknown behavior, state precedence, missing-data behavior, future-data rejection, and required regression fixture cases.
- QQQ CFB lifecycle regression fixtures exist at `historical_signal_replay/fixtures/qqq_cfb_lifecycle_regression_fixtures.json` and cover fresh, stale, spent, expired, unknown, missing-data, future-data rejection, higher-base refresh allowed/rejected, and precedence cases.
- QQQ CFB lifecycle calculator exists at `historical_signal_replay/cfb_lifecycle_calculator.py` with focused fixture-driven tests at `tests/test_cfb_lifecycle_calculator.py`; all 18 accepted lifecycle fixtures pass.
- QQQ CFB stale/spent/expiry work-package request now passes content validation with the accepted lifecycle rule and regression rows filled from the decision doc, fixture file, and calculator.
- QQQ CFB context/caution rule review exists at `SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_RULE.md` and the exact missing decision is documented at `SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_DECISION_NEEDED.md`.
- QQQ CFB context/caution regression fixtures exist at `historical_signal_replay/fixtures/qqq_cfb_context_caution_regression_fixtures.json` and cover framework-level component statuses, complete-caution precedence, missing-data behavior, future-data rejection, wrong identity rejection, and forbidden fill/P&L/profitability/readiness rejection. Threshold/source boundary fixtures that would require missing human decisions are documented as blocked in `SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_FIXTURES_BLOCKED.md`.
- QQQ CFB context/caution missing-decision defaults are accepted at `SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_MISSING_DECISIONS.md`: option, headline, and execution remain `unknown` when their source/rule prerequisites are missing, and `unknown` blocks complete caution review.
- QQQ CFB context/caution calculator exists at `historical_signal_replay/context_caution_calculator.py` with focused fixture-driven tests at `tests/test_context_caution_calculator.py`; all 22 accepted context/caution fixtures pass.
- QQQ CFB context/caution work-package request is filled with `option_context_status=unknown`, `headline_context_status=unknown`, `execution_context_status=unknown`, and `complete_caution_review_status=unknown` from the accepted missing-decision defaults and calculator. This is blocker-preserving evidence, not a clean/caution/fail pass.
- QQQ CFB first selected-contract policy exists at `SAFE_FAST_DAY41_QQQ_CFB_SELECTED_CONTRACT_POLICY.md`: reviewed universe is QQQ options listed on `2026-04-13` with expirations `2026-04-27` through `2026-05-13`, strikes `590` through `640`, both calls and puts retained while side was still blocked, and eligible quotes selected nearest-at-or-before `2026-04-13T12:30:00-04:00` by Databento `ts_event`. `SAFE_FAST_DAY41_QQQ_CFB_SELECTED_CONTRACT_POLICY_DECISION_NEEDED.md` records the now-superseded blocker list that led to the first contract-selection decision.
- QQQ CFB first contract-selection decision exists at `SAFE_FAST_DAY41_QQQ_CFB_CONTRACT_SELECTION_DECISION.md`: long calls only, nearest reviewed-universe expiration with DTE at least `14`, lowest reviewed-universe call strike greater than or equal to trigger `613.67`, nearest OTM-by-trigger moneyness, quote nearest-at-or-before setup by `ts_event`, maximum spread `0.15`, maximum spread percent `2.00%`, minimum bid size/ask size/trade volume/open interest of `1`, strict statistics timestamp handling, abstain/unknown missing-data behavior, and no fallback scan after a top-ranked contract fails a gate.
- QQQ CFB contract-selection regression fixtures exist at `historical_signal_replay/fixtures/qqq_cfb_contract_selection_regression_fixtures.json` and cover valid selection, wrong side, DTE, expiration ranking, strike ranking, spread, spread percent, bid/ask, bid/ask size, volume, open interest, quote/statistics timestamp rejection, no fallback, and no-pass abstain cases.
- QQQ CFB contract selector exists at `historical_signal_replay/cfb_contract_selector.py` with focused fixture-driven tests at `tests/test_cfb_contract_selector.py`; all `18` accepted contract-selection fixtures pass.
- QQQ CFB option-context selector evidence review exists at `SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_SELECTOR_EVIDENCE_REVIEW.md`. The initial local Databento application did not select exactly one eligible contract because the top-ranked `QQQ   260427C00615000` call lacked a TCBBO quote at or before setup time; the no-fallback rule preserved `option_context_status=unknown`.
- QQQ CFB top-contract quote coverage audit exists at `SAFE_FAST_DAY41_QQQ_CFB_TOP_CONTRACT_QUOTE_COVERAGE_AUDIT.md`. The audit maps `QQQ   260427C00615000` to `instrument_id=1023411456`, finds `2` local TCBBO rows and `2` local trade rows for that exact contract, all after the signal, and finds no symbol/instrument-id mismatch. The local blocker is real inside the downloaded ten-minute window; the audit cannot prove no earlier same-day quote exists before the local TCBBO window starts.
- QQQ CFB option-context rerun with wider quotes exists at `SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_RERUN_WITH_WIDER_QUOTES_REVIEW.md`. The wider top-contract TCBBO file contains `28` setup-time-safe rows for `instrument_id=1023411456`, with nearest at-or-before quote `2026-04-13T16:06:30.640301037Z`, bid `7.76`, ask `7.80`, spread `0.04`, bid size `3`, and ask size `31`. The accepted selector still abstains because the top-ranked contract has no through-setup trade volume in the existing trade file and no timestamp-safe same-contract open-interest/statistics row; `option_context_status` remains `unknown`.
- QQQ CFB option-context rerun with trades/statistics exists at `SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_RERUN_WITH_TRADES_STATS_REVIEW.md`. The new top-contract trades file contains `28` setup-time-safe rows for `instrument_id=1023411456` and setup-time-safe trade volume `65`, curing the trade-volume blocker. The new statistics file contains `0` rows, so timestamp-safe same-contract open interest remains missing; the accepted selector still abstains with no fallback and `option_context_status` remains `unknown`.
- QQQ CFB target contract listing / open-interest audit exists at `SAFE_FAST_DAY41_QQQ_CFB_TARGET_CONTRACT_LISTING_OI_AUDIT.md`. The Apr 13 definition row for `QQQ   260427C00615000` / `instrument_id=1023411456` is line `10022`, `security_update_action=A`, with `ts_event=2026-04-13T12:00:00.445628903Z`, before the setup boundary. The Apr 10 parent definitions file exists with `10,212` rows and has `0` matches for the target instrument, target symbol, or same `2026-04-27` call `615` contract shape. The audit keeps the open-interest gate unchanged and records the exact human decision still needed: keep blocking newly listed contracts without setup-time-safe same-contract open interest, or explicitly accept a listing-aware exception with regression fixtures.
- QQQ CFB new-contract open-interest exception rule exists at `SAFE_FAST_DAY41_QQQ_CFB_NEW_CONTRACT_OI_EXCEPTION_RULE.md`. The accepted narrow exception says prior-day same-contract open interest is not required when the selected contract was not listed on the prior trading day, but listing before setup, setup-time-safe quote, spread, spread percent, bid size, ask size, trade volume, no future data, and no fallback are still required. The exception result is `caution`, not `clean`; the expected QQQ option-context result after regression fixtures and selector/rule implementation is `caution`.
- QQQ CFB new-contract open-interest exception regression fixtures exist at `historical_signal_replay/fixtures/qqq_cfb_new_contract_oi_exception_regression_fixtures.json` and cover the valid `caution` case plus listing-after-signal, prior-day-present missing OI, missing listing timestamp, missing quote, quote-after-signal, spread, spread-percent, bid-size, ask-size, trade-volume, no-fallback, and future-data rejection cases.

## Current Blockers

- QQQ Clean Fast Break complete context/caution fields are filled only as calculator-backed and selector-backed `unknown`; clean/caution/fail context labels remain blocked.
- QQQ CFB option context remains recorded as `unknown` because evidence files and selector code were not changed. A new narrow listing-aware exception and regression fixtures are accepted, but selector/rule implementation is still needed before the expected target result can move to `caution`.
- Context/caution framework fixtures, missing-decision defaults, and the first reviewed option-universe/eligibility policy are accepted, but one selected contract, option numeric thresholds, execution entry/fill/quote-age/spread/liquidity/slippage rules, and the historical headline/no-headline source/category policy remain blocked for clean/caution/fail evidence fills.
- Contract-selection selector/calculator implementation now exists for regression work only. Evidence fill, entry, fill assumption, exit, stop/invalidation translation, time exit, cost/slippage, failure labels, sample-size requirement, and promotion gates remain undecided.
- Option-context, execution-context, headline-context, and complete-caution label rules remain undecided.
- No complete trade plan exists for any candidate.

## Next Single Action

Use the implemented selector only as a regression-protected contract-selection rule. The next bounded option-context step is selector/rule implementation against the accepted new-contract open-interest exception fixtures, or separately acquire a timestamp-safe same-contract open-interest source for `instrument_id=1023411456` / `QQQ   260427C00615000`. Any next step must still avoid backtest, evidence fill, P&L, proof, profitability, readiness, or trade-plan result counting unless separately authorized.

## Data-Source Status

- Tastytrade/dxLink local helpers: underlying OHLCV only for current validated use; they did not satisfy historical option-field needs.
- Databento QQQ OPRA raw files: local, structurally validated for definitions, bid/ask quotes, timestamps, expiration, strike, side, trades/volume, and open interest/statistics.
- Databento OPRA normalizer: local read-only helper exists and has focused tests.
- Raw Databento CSV/DBN/manifest files: must not be committed or modified by speed-layer or rule/calculator tasks unless explicitly authorized.

## QQQ CFB Status

- Candidate id: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.
- Symbol: `QQQ`.
- Setup type: Clean Fast Break.
- Signal/setup time: `2026-04-13T12:30:00-04:00`.
- Previous regular-session close: `611.02`.
- Signal-day open: `609.455`.
- Gap amount: `-1.565`.
- Gap percent: about `-0.2561%`.
- Direction: down.
- Calculator fixture status under first QQQ CFB threshold set: `clean` with no-hindsight future-data rejection covered by focused tests.
- Evidence status: gap-context request, stale/spent/expiry lifecycle request, and context/caution request pass content validation; context/caution remains four blocker-preserving `unknown` statuses; QQQ is not proof and not ready.
- Context/caution fixture status: framework fixture package added; threshold/source boundary fixtures remain blocked by missing human decisions.
- Context/caution calculator status: created and tested against all 22 accepted framework fixtures; target option, headline, execution, and complete caution statuses are filled as blocker-preserving `unknown` unless later source/rule decisions are accepted.
- Selected-contract policy status: first reviewed-universe and quote-eligibility policy accepted for regression work only.
- Contract-selection decision status: first one-contract rule accepted for regression work only. The rule is long calls only, nearest reviewed-universe expiration at least `14` DTE, lowest reviewed-universe call strike greater than or equal to trigger `613.67`, nearest OTM-by-trigger moneyness, strict quote/statistics timestamp handling, maximum spread `0.15`, maximum spread percent `2.00%`, minimum bid size/ask size/trade volume/open interest of `1`, abstain/unknown missing-data behavior, and no fallback after a gate failure. Regression fixtures and selector/calculator implementation now exist and pass all accepted fixture cases, but the rule has not filled evidence or been applied to choose a real trade.
- Option-context selector evidence status: local Databento application attempted. The initial ten-minute quote file had no setup-time-safe quote for top-ranked contract `QQQ   260427C00615000` expiring `2026-04-27` at strike `615`. The wider top-contract TCBBO rerun finds setup-time-safe quotes for `instrument_id=1023411456`. The new top-contract trades/statistics rerun finds setup-time-safe trade volume `65`, curing the trade-volume gate, but the new statistics file contains no rows and cannot satisfy timestamp-safe same-contract open interest. `SAFE_FAST_DAY41_QQQ_CFB_OPEN_INTEREST_GATE_DECISION.md` kept setup-time-safe same-contract open interest required and rejected volume-only liquidity. `SAFE_FAST_DAY41_QQQ_CFB_NEW_CONTRACT_OI_EXCEPTION_RULE.md` accepts a narrow new-contract exception as `caution` when prior-day open interest cannot exist because the selected contract was not listed on the prior trading day and all other gates pass, and `historical_signal_replay/fixtures/qqq_cfb_new_contract_oi_exception_regression_fixtures.json` now records the data-only regression fixtures. Current `option_context_status` remains `unknown` until selector/rule implementation is completed.
- Top-contract quote coverage audit status: exact mapping is consistent for `instrument_id=1023411456`; exact local ten-minute TCBBO rows for the top contract begin at `2026-04-13T16:31:13.931412942Z`, after the `2026-04-13T16:30:00Z` setup boundary. The wider top-contract quote file now cures the quote timestamp blocker, and the new top-contract trades file cures the trade-volume blocker, but timestamp-safe statistics/open-interest remains missing.
- Lifecycle status: first QQQ CFB testing rule accepted; replay rows identify a fresh initial-break target, later spent follow-through, higher-base watch requiring a fresh completed breakout, and later spent/no-fresh-trigger context. Lifecycle regression rows added: YES. Lifecycle calculator created and tested: YES. Lifecycle evidence filled: YES.

## Remaining Project-Wide Rules

- Contract-selection evidence fill using the selector, only if explicitly authorized.
- Entry rule.
- Fill assumption.
- Spread and liquidity limits.
- Exit rule.
- Stop/invalidation translation.
- Time exit and end-of-day handling.
- Cost and slippage assumptions.
- Stale/spent lifecycle rules by setup type.
- Stage transitions and precedence.
- Headline-context labels.
- Option-context labels.
- Execution-context labels.
- Complete-caution aggregation.
- Failure/no-trade diagnosis labels.
- Sample-size requirements.
- Promotion gates.

## What Is Not Proven

- No profitable trading plan is proven.
- No backtest is authorized from the current QQQ gap fixtures alone.
- No option contract has been selected as a real trade.
- No entry or exit rule is accepted.
- No fill, slippage, cost, or P&L assumption is accepted.
- No candidate is ready for intake, shadow planning, live action, broker/order activity, or money stages.

## What Must Not Be Claimed

- Do not claim proof.
- Do not claim profitability.
- Do not claim readiness.
- Do not claim a chosen trade.
- Do not claim P&L.
- Do not call the project dead. Weak, failed, unclear, missing, or unprofitable results mean diagnose and repair.

## Future-Chat Speed Path

1. Read `SAFE_FAST_BUILD_STATE.md`.
2. Read this dashboard.
3. Read `SAFE_FAST_PROJECT_RULE_INDEX.md`.
4. Read the relevant candidate packet in `historical_signal_replay/candidate_packets/`.
5. Use `SAFE_FAST_CODEX_TASK_TEMPLATES.md` for the next bounded task.
6. Run `.\scripts\safe_fast_run_safe_checks.ps1` before and after code changes.
7. Do not restart old discovery when the repo already records the answer.
8. Answer the user directly in plain English.
