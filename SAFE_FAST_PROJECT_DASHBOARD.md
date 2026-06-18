# SAFE-FAST Project Dashboard

## Current Checkpoint

- Day 47 grouped CFB expansion/data-needed plan: `SAFE_FAST_DAY47_GROUPED_CFB_EXPANSION_DATA_NEEDED_PLAN.md` records the next planning package. It keeps `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` as one positive review-only CFB reference with entry `6.37`, adjusted exit `7.98`, and adjusted result `+1.61`; keeps `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` as the `quote_after_signal` no-entry control; and keeps `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` as the `quote_age_above_5_minutes` no-entry control. Ideal and Continuation candidates remain comparison/parking references until setup-family rule/evidence packages exist. Next task: `SAFE_FAST_DAY47_NEXT_GROUPED_DATA_NEEDED_COST_CHECK_CODEX_TASK.md`. No data was downloaded, no Databento request was made, no new backtest was run, no new P&L was calculated, and no proof/profitability/readiness/intake-ready change was claimed.
- Day 46 next grouped backtest batch decision: `SAFE_FAST_DAY46_NEXT_GROUPED_BACKTEST_BATCH_DECISION.md` records that the next grouped work is a Clean Fast Break expansion and data-needed planning package, not a new backtest run. The batch keeps `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` as one positive review-only reference with adjusted result `+1.61`, keeps `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` as the `quote_after_signal` no-trade control, and keeps `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` as the `quote_age_above_5_minutes` no-trade control. `SPY-REAL-HISTORICAL-IDEAL-001` is useful for later setup-family comparison but is not ready for a grouped backtest path because Ideal-specific gap/context, option/execution, entry/exit/cost/slippage, sample-size, and promotion rules remain incomplete. QQQ Ideal and both Continuation candidates stay parked until setup-family rule/evidence packages exist. No data was downloaded, no new P&L was calculated, no proof/profitability/readiness was claimed, and intake-ready status did not change.
- Day 46 handoff and next-chat start checkpoint: `SAFE_FAST_DAY46_NEXT_CHAT_HANDOFF_START_HERE.md` is now the plain-English starting point for the next chat, with `SAFE_FAST_DAY46_NEXT_CHAT_START_BLOCK.txt` as the copy/paste block. The handoff records that local git controls; latest known pre-handoff local HEAD was `59b2a03 Run first CFB backtest reference case` on `main`. It preserves the first CFB result: SPY CFB 002 hit the profit target with entry `6.37`, adjusted exit `7.98`, and adjusted result `+1.61`; SPY CFB 003 stayed out from quote-after-signal; QQQ CFB 001 stayed out from quote age above `5` minutes. The result is one useful positive reference plus two controls, not proof. The handoff also records plain-English communication, task-file-first PowerShell/Codex workflow, budget control, batching, Day 60 as a checkpoint, the final `$200` high-intensity sprint, the later `$20` tier transition, and the next grouped review/expansion task.
- Day 46 first backtest review and expansion plan: `SAFE_FAST_DAY46_FIRST_BACKTEST_REVIEW_AND_EXPANSION_PLAN.md` records the plain-English meaning of the first completed Clean Fast Break review-only result. `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` is useful as one positive reference: entry `6.37`, adjusted exit `7.98`, adjusted result `+1.61`, profit-target exit. It does not prove profitability, readiness, promotion, or a complete trading plan. `SAFE_FAST_DAY46_CANDIDATE_EXPANSION_PRIORITY_TABLE.md` ranks the next grouped work as more CFB examples first, Ideal comparison second, Continuation later only after setup-family rules/evidence exist, repair/no-trade controls preserved, and data-needed cases recorded before any cost-check request. `SAFE_FAST_DAY46_NEXT_GROUPED_BACKTEST_BATCH_TASK.md` defines the next grouped batch anchors: SPY CFB 002 positive reference, SPY CFB 003 quote-after-signal control, QQQ CFB 001 stale-quote control, SPY Ideal 001 only if ready enough, and Continuation candidates only if their rule/data state supports it. No data was downloaded, no new P&L was calculated, no proof/profitability/readiness was claimed, and intake-ready status did not change.
- Day 46 first CFB local backtest run with exit-path data: `historical_signal_replay/cfb_backtest_runner.py` now reads the new local selected-contract SPY CFB 002 TCBBO exit-path file and reruns the first Clean Fast Break path. The required local exit-path files exist. `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` completes as `completed_review_only` / `completed_profit_target`: entry time `2026-04-13T16:30:00+00:00`, entry ask `6.35`, accepted entry basis `6.37`, target threshold `7.9625`, stop threshold `5.4145`, exit time `2026-04-13T19:37:14.335714+00:00`, exit bid `8.00`, accepted exit basis `7.98`, gross result `+1.65`, and cost/slippage-adjusted result `+1.61`. `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` remains `no_trade` from `quote_after_signal`; `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` remains `no_trade` from `quote_age_above_5_minutes`. Review/result docs: `SAFE_FAST_DAY46_FIRST_CFB_BACKTEST_RUN_WITH_EXIT_PATH_REVIEW.md` and `SAFE_FAST_DAY46_FIRST_CFB_BACKTEST_RUN_WITH_EXIT_PATH_RESULT.md`. No Databento data was downloaded, no raw data was changed, no proof/profitability/promotion/readiness was claimed, and intake-ready status did not change.
- Day 46 first CFB local backtest run: `historical_signal_replay/cfb_backtest_runner.py` now runs the first authorized local Clean Fast Break backtest path from the exact prepared candidate rows, with focused tests in `tests/test_cfb_backtest_runner.py`. `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` enters the runner with selected contract `SPY   260427C00685000`, cost-adjusted entry basis `6.37`, profit target threshold `7.9625`, and option stop threshold `5.4145`, but the local starter data is not enough to complete the exit path through `15:45 ET`; result `blocked_missing_exit_path_data`, primary reason `selected_contract_tcbbo_bid_path_through_1545_et`, also missing `source_backed_underlying_invalidation_path_through_1545_et`. `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` remains `no_trade` from `quote_after_signal`; `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` remains `no_trade` from `quote_age_above_5_minutes`. Review/result docs: `SAFE_FAST_DAY46_FIRST_CFB_BACKTEST_RUN_REVIEW.md` and `SAFE_FAST_DAY46_FIRST_CFB_BACKTEST_RUN_RESULT.md`. No Databento data was downloaded, no raw data was changed, no P&L was calculated, no promotion/proof/profitability/readiness was claimed, and intake-ready status did not change.
- Day 45 CFB backtest-prep implementation: `historical_signal_replay/cfb_trade_rule_checker.py` now supports the accepted exact Clean Fast Break values from `historical_signal_replay/fixtures/cfb_exit_stop_cost_regression_fixtures.json` version `2`, while preserving the earlier grouped gate fixtures. `tests/test_cfb_trade_rule_checker.py` now covers `20` focused cases, including long-call entry, setup/option/execution pass gating, ask plus `0.02` entry basis, bid minus `0.02` exit basis, profit target, option premium stop, setup invalidation stop, `15:45 ET` time exit, zero-cost rejection, named failure reason, sample-size blocker below `20`, promotion blocker without positive expectancy review, and unsafe output refusal. `historical_signal_replay/cfb_backtest_prep_harness.py` prepares structure-only harness rows and explicitly refuses backtest and P&L calls. SPY CFB 002 is `entry_rule_ready_awaiting_backtest_harness`; SPY CFB 003 remains `no_trade` from `quote_after_signal`; QQQ CFB 001 remains `no_trade` from `quote_age_above_5_minutes`. No data was downloaded, no backtest was run, no P&L was calculated, no proof/profitability/readiness was claimed, and intake-ready status did not change.
- Day 45 CFB exact trade-rule values: `SAFE_FAST_DAY45_CFB_EXACT_TRADE_RULE_VALUES.md` accepts the first exact Clean Fast Break values for regression and later grouped backtest-prep implementation. Accepted values are long calls only; entry requires setup, option context, and execution context to pass; entry basis is setup-safe ask plus `0.02`; exit basis is bid minus `0.02`; first-pass exits use earliest of `+25%` profit target, `-15%` option premium stop, setup invalidation stop, or `15:45 ET` signal-day time exit; zero-cost fills are forbidden; failures need one primary named reason; promotion is blocked below `20` valid completed CFB examples and also requires accepted rules, passing replay/regression, and positive expectancy review after costs. `historical_signal_replay/fixtures/cfb_exit_stop_cost_regression_fixtures.json` is updated to value coverage. `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` is entry-rule-ready for later harness implementation only; `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` remains no-trade from `quote_after_signal`; `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` remains no-trade from `quote_age_above_5_minutes`. Backtest, P&L, proof, profitability, readiness, intake-ready status, evidence fills, raw data, and downloads remain unchanged.
- Day 45 CFB exit/stop/cost rule package: `SAFE_FAST_DAY45_CFB_EXIT_STOP_COST_RULE_PACKAGE.md` defines the first conservative remaining Clean Fast Break rule shape for exit, stop/invalidation translation, time exit, cost/slippage, failure diagnosis, sample size, and promotion. Only named failure diagnosis is accepted for first regression pass; exit, stop translation, time-exit values, cost/slippage numbers, sample-size thresholds, and promotion criteria still need human decisions before countable backtest results. `historical_signal_replay/fixtures/cfb_exit_stop_cost_regression_fixtures.json` records data-only blocker fixtures. `SAFE_FAST_DAY45_CFB_BACKTEST_GATE_DECISION.md` keeps `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` as the first CFB backtest-prep reference, but not backtest-ready: cheap starter data can test gate behavior and missing-rule blockers, while full-window Databento is deferred until exact rules, windows, cost check, and user approval exist. Backtest, P&L, proof, profitability, readiness, intake-ready status, evidence fills, and raw data remain unchanged.
- Day 45 CFB trade-rule checker implementation: `historical_signal_replay/cfb_trade_rule_checker.py` now implements the accepted first-pass grouped Clean Fast Break trade-rule gates from `historical_signal_replay/fixtures/cfb_trade_rule_regression_fixtures.json`, with focused tests in `tests/test_cfb_trade_rule_checker.py`. The checker returns `blocked_pre_backtest` for `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` because exit/cost/sample/promotion decisions remain missing while entry evidence is usable, returns `no_trade` with `quote_after_signal` for `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`, and returns `no_trade` with `quote_age_above_5_minutes` for `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`. Missing selected contract, missing entry quote, missing invalidation, missing exit rule, missing cost/slippage, missing failure diagnosis, missing sample-size gate, missing promotion gate, and forbidden P&L/proof/profitability/readiness fields are covered by tests. Backtest, P&L, proof, profitability, readiness, intake-ready status, and raw data remain unchanged.
- Day 45 CFB grouped trade-rule package: `SAFE_FAST_DAY45_CFB_GROUPED_TRADE_RULE_PACKAGE.md` defines the first conservative Clean Fast Break trade-rule package for regression/checker work only. `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` is the first backtest-prep reference after checker/tests and missing rule decisions; `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` is the quote-after-signal no-trade/repair reference; `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` is the stale-quote failed-execution reference. Accepted first-pass gates are setup-time-safe entry eligibility, selected-contract/no-fallback use, long-call ask entry basis, quote-after-signal rejection, stale-quote rejection, and named failure diagnosis. Exit, stop/invalidation translation, time exit, cost/slippage amounts, sample-size thresholds, and promotion criteria still need decisions before any countable backtest, P&L, proof, profitability, or readiness claim. Fixture file: `historical_signal_replay/fixtures/cfb_trade_rule_regression_fixtures.json`. Next grouped task: `SAFE_FAST_DAY45_CFB_NEXT_GROUPED_IMPLEMENTATION_TASK.md`.
- Day 45 grouped trade-plan readiness gate: `SAFE_FAST_DAY45_GROUPED_TRADE_PLAN_READINESS_GATE.md` records the grouped readiness result across all seven current candidates. Content validation is clean at `9` passed requests and `0` failed requests; the bridge marks `4` candidates reconsideration-eligible and `0` intake-ready. No candidate has a complete trade plan. `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` is the best first backtest-prep reference only after a grouped trade-rule package is accepted. QQQ CFB 001, SPY CFB 003, and SPY Ideal 001 belong in repair; QQQ Continuation 001, QQQ Ideal 001, and SPY Continuation 001 stay parked until setup-family evidence/rule packages are authorized. The next grouped task is `SAFE_FAST_DAY45_NEXT_GROUPED_BUILD_TASK.md`, which chooses a trade-rule package before any backtest-prep harness or full-window data approval package.
- Day 45 bounded final sprint control update: Day 60 is a progress checkpoint, not the finish line. The build target is a profitable trading plan, and the project will not cut corners to hit a date. The project also cannot run indefinitely. The next $200 month is the final high-intensity build sprint before moving toward the $20 tier. Work must stay batched, evidence-backed, cost-controlled, and focused on tested examples, comparison, trade-plan rules, and a clear decision package. Day 1 was May 3, 2026; June 16, 2026 was Day 45; Day 60 is July 1, 2026. Current repo docs after the SPY Ideal starter batch show evidence cleanup at `9` passed requests and `0` failed requests. Intake-ready remains controlled by the separate readiness gate, proof allowed remains `NO`, and trade-plan rules still need grouped readiness work.
- Current Day 41 SPY Ideal starter batch implementation/fill: `SAFE_FAST_DAY41_SPY_IDEAL_STARTER_BATCH_IMPLEMENT_AND_FILL_REVIEW.md` records the grouped starter-only rule and evidence fill for `SPY-REAL-HISTORICAL-IDEAL-001`. `SAFE_FAST_DAY41_SPY_IDEAL_STARTER_BATCH_RULE.md` accepts a conservative Ideal lifecycle rule and starter option/execution/context treatment for regression work only. SPY Ideal lifecycle is `fresh` at `2026-05-13T11:30:00-04:00` and later `spent` at `2026-05-13T14:30:00-04:00`. The top-ranked starter contract `SPY   260527C00745000` has only local quote/trade rows after setup, so option and execution context remain `unknown`; gap and headline also remain `unknown`; complete caution remains `unknown`. Content validation now has `9` passed requests and `0` failed requests; the bridge marks all four mapped parked candidates reconsideration-eligible, but intake-ready remains `0`, proof allowed remains `NO`, and no backtest/P&L/proof/readiness was claimed.
- Current Day 41 SPY CFB starter option/execution/context batch: `SAFE_FAST_DAY41_SPY_CFB_STARTER_OPTION_EXECUTION_CONTEXT_BATCH_REVIEW.md` records grouped starter-only rule application for `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` and `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`. `historical_signal_replay/cfb_contract_selector.py` now supports explicit fixture-level symbol/setup and optional OI-gate behavior while preserving QQQ defaults; `historical_signal_replay/context_caution_calculator.py` now supports fixture-level expected candidate identity while preserving QQQ defaults. SPY CFB 002 selects starter contract `SPY   260427C00685000` with `option_context_status=clean` and `execution_context_status=clean`; headline and complete caution remain `unknown`. SPY CFB 003 abstains because the top-ranked `SPY   260429C00700000` quote/trade row is post-signal, so option/execution/headline/complete caution remain `unknown`. Content validation now has `7` passed requests and `2` failed requests; QQQ CFB plus both SPY CFB candidates are reconsideration-eligible, but intake-ready remains `0`, proof allowed remains `NO`, and no backtest/P&L/proof/readiness was claimed.
- Current Day 41 SPY CFB lifecycle batch implementation/fill: `SAFE_FAST_DAY41_SPY_CFB_LIFECYCLE_BATCH_IMPLEMENT_AND_FILL_REVIEW.md` records grouped calculator/test implementation for `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` and `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`. `historical_signal_replay/cfb_lifecycle_calculator.py` now supports the accepted SPY lifecycle rule metadata while preserving QQQ fixtures; `tests/test_cfb_lifecycle_calculator.py` passes the existing `18` QQQ lifecycle fixtures and all `12` SPY lifecycle fixtures. Lifecycle-only work-package rows are filled for SPY CFB 002 initial-break expiry and SPY CFB 003 higher-base fresh-break expiry. Content validation now has `5` passed requests and `4` failed requests; SPY CFB 002 and 003 remain parked because complete context/caution fields are still missing. No raw data was changed, no backtest/P&L/proof/readiness was claimed, and intake-ready count remains `0`.
- Current Day 41 SPY CFB grouped rule/regression package: `SAFE_FAST_DAY41_SPY_CFB_GROUPED_RULE_REGRESSION_PACKAGE.md` accepts the first conservative SPY Clean Fast Break lifecycle rule for data-only regression work covering `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` initial-break lifecycle and `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` higher-base fresh-break lifecycle. Data-only fixtures were created at `historical_signal_replay/fixtures/spy_cfb_lifecycle_regression_fixtures.json`. QQQ CFB artifacts were used as structure only; QQQ contract, option-context, execution, proof, profitability, and readiness conclusions were not applied to SPY. This package does not fill evidence, backtest, choose a contract/trade, calculate P&L, claim proof/profitability, mark readiness, or change intake-ready status.
- Current Day 41 starter batch option inspection: `SAFE_FAST_DAY41_STARTER_BATCH_OPTION_INSPECTION.md` inspects the local cheap starter Databento files for `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`, `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`, `SPY-REAL-HISTORICAL-IDEAL-001`, `QQQ-REAL-HISTORICAL-CONTINUATION-001`, `QQQ-REAL-HISTORICAL-IDEAL-001`, and `SPY-REAL-HISTORICAL-CONTINUATION-001`. All six have option definitions, setup-window quotes, setup-window trades, and setup-time-safe `stat_type=9` open-interest rows for instruments seen in their starter quote/trade windows. Latest raw quote rows at or before setup are sub-second fresh for all six, and raw trade rows exist at or before setup for all six. This is raw starter inspection only: no QQQ-specific contract rules were applied to SPY, Ideal, or Continuation candidates; no evidence was filled; no backtest or P&L was run; no proof/profitability was claimed; and no candidate was marked ready. Routing is recorded in `SAFE_FAST_DAY41_STARTER_BATCH_RULE_AND_DATA_MATRIX.md`, and the next grouped task is `SAFE_FAST_DAY41_STARTER_BATCH_NEXT_GROUPED_TASK.md`.
- Current Day 41 cheap starter Databento batch validation: `SAFE_FAST_DAY41_CHEAP_STARTER_BATCH_VALIDATION.md` validates the local cheap starter manifest and nonempty candidate starter CSVs for `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`, `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`, `SPY-REAL-HISTORICAL-IDEAL-001`, `QQQ-REAL-HISTORICAL-CONTINUATION-001`, `QQQ-REAL-HISTORICAL-IDEAL-001`, and `SPY-REAL-HISTORICAL-CONTINUATION-001`. All six have definitions, statistics, 10-minute TCBBO quotes, and 10-minute trades. Starter data is enough to attempt first-pass option-universe, setup-time quote freshness, setup-time trade-volume, and setup-time statistics/open-interest inspection after setup-specific rule/regression authorization. It is not enough for full trade-plan proof; all six likely need full-window data later if entry/exit/backtest/proof work is authorized. No data was downloaded, no raw files were changed, no evidence was filled, no backtest or P&L was run, no proof/profitability was claimed, and no candidate was marked ready. Next steps are recorded in `SAFE_FAST_DAY41_CHEAP_STARTER_BATCH_NEXT_STEPS.md`.
- Current Day 41 SPY batch Databento cost-check result: `SAFE_FAST_DAY41_SPY_BATCH_DATABENTO_COST_CHECK_RESULT.md` covers `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`, `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`, and `SPY-REAL-HISTORICAL-IDEAL-001` in one grouped result. Databento `OPRA.PILLAR` metadata/cost-only calls were attempted for `definition`, `tcbbo`, `trades`, and `statistics`, but all Databento responses were blocked by the refused HTTPS proxy `127.0.0.1:9`, so estimated cost is `NOT_AVAILABLE_PROXY_BLOCKED`. No local SPY OPRA files exist; only QQQ OPRA files are local. The grouped Databento path stops until cost/source coverage can be confirmed from an environment with working HTTPS access. No Databento data was downloaded, no raw vendor files were written, no evidence was filled, no backtest or P&L was run, and no candidate was marked ready.
- Baseline commit for this SPY batch preflight task: `7d483ab Add batch restart plan after QQQ diagnosis`.
- Current Day 41 SPY batch preflight checkpoint: `SAFE_FAST_DAY41_SPY_BATCH_PREFLIGHT.md` inventories `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`, `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`, and `SPY-REAL-HISTORICAL-IDEAL-001` as evidence-shaped but still partial/missing. Local SPY source rows and replay signal rows exist, and all three candidate packets are updated with source row details, blockers, and data needs. `SAFE_FAST_DAY41_SPY_BATCH_DATABENTO_COST_CHECK_PLAN.md` defines a cost-check-only Databento `OPRA.PILLAR` plan for `definition`, `tcbbo`, `trades`, and `statistics` covering the two SPY CFB windows and optional SPY Ideal. `SAFE_FAST_DAY41_SPY_BATCH_NEXT_TASK.md` defines one grouped next task. No evidence was filled, no Databento data was downloaded, no backtest or P&L was run, and no candidate was marked ready.
- Baseline commit for this batch restart task: `f4a8781 Fill QQQ CFB execution context evidence`.
- Current Day 41 batch checkpoint: `SAFE_FAST_DAY41_BATCH_RESTART_QQQ_DIAGNOSIS_AND_CANDIDATE_PLAN.md` records the QQQ CFB diagnosis and batch candidate table, and `SAFE_FAST_DAY41_BATCH_NEXT_ACTIONS.md` defines the grouped next plan. QQQ CFB stays parked because gap context, lifecycle, and option context passed, but execution context failed on quote age above `5` minutes and complete caution failed by accepted precedence. Compact candidate packets now exist for the seven batch candidates: QQQ CFB, SPY CFB 002, SPY CFB 003, SPY Ideal, QQQ Continuation, QQQ Ideal, and SPY Continuation. The next grouped work should process SPY CFB 002 and SPY CFB 003 together, with SPY Ideal optionally included in the same SPY Databento cost-check pass. This checkpoint does not fill evidence, backtest, calculate P&L, claim proof/profitability, or mark any candidate ready.
- Baseline commit for this execution-context evidence fill task: `ed008eb Add QQQ CFB execution context calculator`.
- Current Day 41 checkpoint: QQQ Clean Fast Break contract selector now exists at `historical_signal_replay/cfb_contract_selector.py` with focused tests at `tests/test_cfb_contract_selector.py`. The selector still passes all `18` accepted contract-selection fixtures. Applied to the local Databento QQQ files in `SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_SELECTOR_EVIDENCE_REVIEW.md`, it initially abstained because the top-ranked `QQQ   260427C00615000` call had no setup-time-safe TCBBO quote and no fallback was allowed. `SAFE_FAST_DAY41_QQQ_CFB_TOP_CONTRACT_QUOTE_COVERAGE_AUDIT.md` confirmed the mapping to `instrument_id=1023411456` was consistent. `SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_RERUN_WITH_WIDER_QUOTES_REVIEW.md` cured the prior quote blocker with `28` setup-time-safe wider quote rows. `SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_RERUN_WITH_TRADES_STATS_REVIEW.md` cured the prior trade-volume blocker with `65` setup-time-safe contracts, but the new statistics file has `0` rows. `SAFE_FAST_DAY41_QQQ_CFB_TARGET_CONTRACT_LISTING_OI_AUDIT.md` confirms the target contract was listed before setup on Apr 13 (`ts_event=2026-04-13T12:00:00.445628903Z`), but was absent from the Apr 10 parent definitions (`target_matches=0`). `SAFE_FAST_DAY41_QQQ_CFB_NEW_CONTRACT_OI_EXCEPTION_RULE.md` accepts a narrow listing-aware exception for regression work, and `SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_NEW_CONTRACT_OI_EVIDENCE_FILL_REVIEW.md` records the bounded evidence fill to `option_context_status=caution`. `SAFE_FAST_DAY41_QQQ_CFB_EXECUTION_CONTEXT_RULE_DECISION.md` accepts the first conservative execution-context rule, `historical_signal_replay/fixtures/qqq_cfb_execution_context_regression_fixtures.json` records `13` data-only regression fixtures, and `historical_signal_replay/execution_context_calculator.py` implements the accepted rule with focused tests at `tests/test_execution_context_calculator.py`. `SAFE_FAST_DAY41_QQQ_CFB_EXECUTION_CONTEXT_EVIDENCE_FILL_REVIEW.md` records the bounded evidence fill: the known QQQ target execution fixture returns `execution_context_status=fail` because the selected quote is about `23` minutes `29` seconds old at setup, and accepted complete-caution precedence supports `complete_caution_review_status=fail`. Headline context remains `unknown`. This does not choose a real trade, backtest, calculate P&L, claim proof/profitability, or mark readiness.
- Proof accepted: NO.
- Profitability claim made: NO.
- Intake-ready count changed: NO.
- QQQ candidate ready: NO.
- Content validation result after context/caution fill: `3` passed requests, `6` failed requests.
- Bridge result after context/caution fill: QQQ reconsideration-eligible, intake-ready `NO`, proof allowed `NO`.

## Active Objective

Quality-over-deadline but bounded final sprint toward a profitable trading plan. Day 60 is a checkpoint/reporting date, not a forced finish line. The next $200 month is the final high-intensity build month before moving toward the $20 tier.

Next work: do not run the CFB harness until a later task explicitly authorizes a backtest run and any required data/cost scope. The current implementation can prepare structure-only harness rows for the three CFB references, but counted results, P&L, proof, profitability, readiness, and intake-ready changes remain blocked.

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
- QQQ CFB context/caution work-package request is filled with `option_context_status=caution` from the accepted new-contract OI exception, `headline_context_status=unknown`, `execution_context_status=fail` from the accepted execution-context calculator, and `complete_caution_review_status=fail` from accepted precedence. This is request-shaped evidence only, not proof, profitability, readiness, or a real trade choice.
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
- QQQ CFB execution-context regression fixtures exist at `historical_signal_replay/fixtures/qqq_cfb_execution_context_regression_fixtures.json` and cover clean quote age, caution quote age, fail quote too old, the known QQQ stale quote fail, quote-after-signal rejection, missing bid, missing ask, bad spread, missing size, missing volume, missing source data as `unknown`, no fallback, and forbidden P&L/proof/readiness field rejection.
- QQQ CFB execution-context calculator exists at `historical_signal_replay/execution_context_calculator.py` with focused fixture-driven tests at `tests/test_execution_context_calculator.py`; all `13` accepted execution-context fixtures pass, including the known QQQ stale quote fail.

## Current Blockers

- QQQ Clean Fast Break context/caution fields now have `option_context_status=caution` for the accepted new-contract OI exception, `execution_context_status=fail` from the accepted execution-context calculator, `complete_caution_review_status=fail` by accepted precedence, and `headline_context_status=unknown`; broader headline and trade-plan labels remain blocked.
- QQQ CFB option context is recorded as `caution` only under the accepted new-contract open-interest exception for the top-ranked `QQQ   260427C00615000` contract. Execution context is recorded as `fail` because the selected quote is older than `5` minutes. Headline context remains `unknown`, and the candidate remains not ready.
- Context/caution framework fixtures, missing-decision defaults, the first reviewed option-universe/eligibility policy, selected-contract rule, new-contract OI option-context exception, and first execution quote-age/spread/size/volume rule are accepted, and bounded option/execution evidence fills are recorded. Entry/exit/cost/slippage rules, broader option-context thresholds, and the historical headline/no-headline source/category policy remain blocked for trade-plan proof or readiness.
- Contract-selection selector/calculator implementation now exists for regression work only. Evidence fill, entry, fill assumption, exit, stop/invalidation translation, time exit, cost/slippage, failure labels, sample-size requirement, and promotion gates remain undecided.
- Broader option-context, headline-context, and complete-caution label rules remain undecided. The first execution-context rule is accepted but not yet implemented or filled into evidence.
- No complete trade plan exists for any candidate.

## Next Single Action

The cheap starter Databento batch validation, starter option inspection, SPY CFB grouped lifecycle/context fills, and SPY Ideal starter lifecycle/context fills are complete for the four mapped richer work-package parked candidates. The next single action, if explicitly authorized later, is blocker diagnosis for remaining unknown context components or setup-specific rule work for remaining Ideal/Continuation replacement candidates. Do not download full-window data, backtest, calculate P&L, claim proof/profitability, or mark readiness from the starter-only fills.

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
- Evidence status: gap-context request, stale/spent/expiry lifecycle request, and context/caution request pass content validation; option context is `caution`, headline remains `unknown`, execution is `fail`, complete caution is `fail`, and QQQ is not proof or ready.
- Context/caution fixture status: framework fixture package added; threshold/source boundary fixtures remain blocked by missing human decisions.
- Context/caution calculator status: created and tested against all 22 accepted framework fixtures; target option context is filled as `caution`, execution context is filled as `fail`, complete caution is filled as `fail` by precedence, and headline context remains `unknown`.
- Execution-context rule status: first conservative rule accepted, implemented, and filled into the QQQ context/caution work-package row. Quote age `<= 60` seconds is `clean`, quote age `> 60` seconds and `<= 5` minutes is `caution`, quote age `> 5` minutes or quote/spread/size/volume/no-fallback failure is `fail`, and missing source/rule proof is `unknown`. Data-only execution-context regression fixtures exist at `historical_signal_replay/fixtures/qqq_cfb_execution_context_regression_fixtures.json` with `13` cases, and `historical_signal_replay/execution_context_calculator.py` passes them through `tests/test_execution_context_calculator.py`. Later long-call testing uses ask price only as the fill basis. The target quote at `2026-04-13T16:06:30.640301037Z` is about `23` minutes `29` seconds old at setup, so the filled target execution status is `fail` with `rejection_reason=quote_age_above_5_minutes`.
- Selected-contract policy status: first reviewed-universe and quote-eligibility policy accepted for regression work only.
- Contract-selection decision status: first one-contract rule accepted for regression work only. The rule is long calls only, nearest reviewed-universe expiration at least `14` DTE, lowest reviewed-universe call strike greater than or equal to trigger `613.67`, nearest OTM-by-trigger moneyness, strict quote/statistics timestamp handling, maximum spread `0.15`, maximum spread percent `2.00%`, minimum bid size/ask size/trade volume/open interest of `1`, abstain/unknown missing-data behavior, and no fallback after a gate failure. Regression fixtures and selector/calculator implementation now exist and pass all accepted fixture cases, but the rule has not filled evidence or been applied to choose a real trade.
- Option-context selector evidence status: local Databento application attempted. The initial ten-minute quote file had no setup-time-safe quote for top-ranked contract `QQQ   260427C00615000` expiring `2026-04-27` at strike `615`. The wider top-contract TCBBO rerun finds setup-time-safe quotes for `instrument_id=1023411456`. The new top-contract trades/statistics rerun finds setup-time-safe trade volume `65`, curing the trade-volume gate, but the new statistics file contains no rows and cannot satisfy timestamp-safe same-contract open interest under the base selector. `SAFE_FAST_DAY41_QQQ_CFB_NEW_CONTRACT_OI_EXCEPTION_RULE.md` accepts a narrow new-contract exception as `caution` when prior-day open interest cannot exist because the selected contract was not listed on the prior trading day and all other gates pass. `historical_signal_replay/fixtures/qqq_cfb_new_contract_oi_exception_regression_fixtures.json` records the data-only regression fixtures, and `SAFE_FAST_DAY41_QQQ_CFB_NEW_CONTRACT_OI_EXCEPTION_SELECTOR_REVIEW.md` records selector implementation passing all `13` exception fixtures. `SAFE_FAST_DAY41_QQQ_CFB_OPTION_CONTEXT_NEW_CONTRACT_OI_EVIDENCE_FILL_REVIEW.md` records the work-package evidence fill to `option_context_status=caution`; `SAFE_FAST_DAY41_QQQ_CFB_EXECUTION_CONTEXT_EVIDENCE_FILL_REVIEW.md` records the work-package evidence fill to `execution_context_status=fail` and `complete_caution_review_status=fail`; headline remains `unknown`.
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

Day 45 grouped readiness gate documents these gaps in `SAFE_FAST_DAY45_TRADE_RULE_GAP_PACKAGE.md`; the next grouped task is to define the first conservative trade-rule package before backtest-prep.

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

## Day 46 handoff correction: prompt discipline and Codex transport failure

This correction exists because a new chat mishandled the Day 46 handoff and produced a bad first Codex attempt.

Future chats must follow this exactly:

1. Do not invent generic task files such as TASK_DAY46_GROUPED_BACKTEST_BATCH_REVIEW.md.

2. Use the task files already committed in the repo unless local git proves they are missing.

3. After checkpoint 239692f Add Day 46 first backtest expansion plan, the expected next grouped task is:
   SAFE_FAST_DAY46_NEXT_GROUPED_BACKTEST_BATCH_TASK.md

4. If that file exists, launch Codex with exactly this command:

   codex.cmd -c 'windows.sandbox="unelevated"' --sandbox workspace-write --ask-for-approval never "Read and execute .\SAFE_FAST_DAY46_NEXT_GROUPED_BACKTEST_BATCH_TASK.md exactly."

5. If the expected task file does not exist, create a proper SAFE_FAST_..._CODEX_TASK.md task file first.

6. Do not pass a huge task prompt directly into Codex as command-line text.

7. Do not create random task names.

8. Do not make the user correct the prompt format.

Correct PowerShell/Codex workflow:

Step 1:
Give the user one PowerShell block that writes the task file.

Step 2:
Stop.

Step 3:
After the user confirms the task file exists, give the Codex launch line separately.

Step 4:
User pastes Codex final output.

Step 5:
Review output and give guarded commit commands.

Correct startup check for the next chat:

   Set-Location "C:\Users\nickm\Desktop\New folder\safe-fast-backendnew"
   git --no-pager branch --show-current
   git --no-pager log -1 --oneline
   git --no-pager status --short

Expected checkpoint:
   main
   239692f Add Day 46 first backtest expansion plan
   clean status

If Codex shows WebSocket fallback failure, HTTPS fallback failure, backend-api/codex/responses 404, or repeated reconnect failure:

- Say plainly: Codex connection failed; repo is not the problem.
- Stop retrying the same Codex run.
- Ask only for git branch/log/status.
- Do not create new project tasks while Codex transport is failing.
- Do not tell the user to delete the chat as the first solution.

Plain English current state:

- First real CFB backtest reference ran.
- SPY CFB 002 hit the profit target.
- Adjusted result was +1.61.
- SPY CFB 003 stayed out because quote came after the signal.
- QQQ CFB 001 stayed out because quote was too old.
- Next work is grouped expansion/comparison.
- Do not grind one example.
- Do not invent new task names.

Next intended work:

Use SAFE_FAST_DAY46_NEXT_GROUPED_BACKTEST_BATCH_TASK.md if present.
If missing, create a fresh SAFE_FAST_DAY46_... grouped review/expansion task file first.
Keep batching.
Keep cost control.
Use plain English.

## End Day 46 handoff correction

