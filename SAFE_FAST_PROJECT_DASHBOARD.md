# SAFE-FAST Project Dashboard

## Current Checkpoint

- Baseline commit for this context/caution evidence fill task: `a61e734 Add QQQ CFB context caution calculator`.
- Current Day 41 checkpoint: QQQ Clean Fast Break context/caution work-package evidence is filled with calculator-backed blocker-preserving `unknown` statuses in `historical_signal_replay/source_data/richer_export_package_work/qqq_cfb_complete_context_caution_fields.jsonl`. It preserves blocker defaults from `SAFE_FAST_DAY41_QQQ_CFB_CONTEXT_CAUTION_MISSING_DECISIONS.md`: missing selected contract/reviewed universe keeps option context `unknown`, missing historical headline/no-headline source keeps headline context `unknown`, missing execution entry/fill rules keep execution context `unknown`, and complete caution review cannot pass with any required `unknown` component.
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

## Current Blockers

- QQQ Clean Fast Break complete context/caution fields are filled only as calculator-backed `unknown`; clean/caution/fail context labels remain blocked.
- Context/caution framework fixtures and missing-decision defaults are accepted, but option numeric thresholds, selected-contract/reviewed-universe policy, execution entry/fill/quote-age/spread/liquidity/slippage rules, and the historical headline/no-headline source/category policy remain blocked for clean/caution/fail evidence fills.
- Contract selection, entry, fill assumption, spread/liquidity limits, exit, stop/invalidation translation, time exit, cost/slippage, failure labels, sample-size requirement, and promotion gates remain undecided.
- Option-context, execution-context, headline-context, and complete-caution label rules remain undecided.
- No complete trade plan exists for any candidate.

## Next Single Action

Address the remaining trade-plan and clean/caution/fail decision blockers before any backtest or trade-plan evidence step: selected contract/reviewed universe, entry/fill rule, headline source/category mapping, execution thresholds, exit, stop, cost/slippage, sample size, and promotion gates.

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
- Lifecycle status: first QQQ CFB testing rule accepted; replay rows identify a fresh initial-break target, later spent follow-through, higher-base watch requiring a fresh completed breakout, and later spent/no-fresh-trigger context. Lifecycle regression rows added: YES. Lifecycle calculator created and tested: YES. Lifecycle evidence filled: YES.

## Remaining Project-Wide Rules

- Contract selection.
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
- No option contract selection is accepted.
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
