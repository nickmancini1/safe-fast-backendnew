# SAFE-FAST Project Rule Index

## Accepted / Current

| Rule | Status | Current wording |
| --- | --- | --- |
| Profitability mandate | accepted/current | SAFE-FAST targets a profitable trading plan, but profitability cannot be claimed until evidence proves it. |
| Diagnosis loop | accepted/current | Weak, failed, unclear, missing, or unprofitable results require diagnosis and repair, not a declaration that the project is dead. |
| Missing evidence | accepted/current | Missing evidence is a blocker, not low confidence. |
| No-hindsight boundary | accepted/current | Setup-time labels and decisions must not use future candles, future replay rows, outcome evidence, fills, P&L, or profitability. |
| Recognition versus trade proof | accepted/current | Setup recognition is necessary but not sufficient for trade-plan proof. |
| Trade-plan completeness gate | accepted/current | Contract, side, expiration, strike, entry, fill, spread, liquidity, exit, stop, cost, slippage, and failure rules are required before counting results. |
| Vendor data role | accepted/current | Vendors provide raw fields; SAFE-FAST must calculate labels under accepted rules. |
| Raw Databento files | accepted/current | Raw QQQ OPRA files are local-only and must not be committed by this task. |
| Databento OPRA normalizer scope | accepted/current | The local Databento OPRA normalizer may parse, join, timestamp-normalize, select no-hindsight quotes, and derive quote inspection fields only; it must not infer fills, trade choice, P&L, proof, profitability, or readiness. |
| No proof / no profitability claim | accepted/current | Current docs must not claim proof, profitability, candidate readiness, or intake-ready status. |
| QQQ CFB rule decision package | accepted/current | `SAFE_FAST_DAY41_QQQ_CFB_RULE_DECISION_PACKAGE.md` is the current inventory of missing QQQ Clean Fast Break decisions before evidence fill or backtest; it does not accept unsupported rules. |
| QQQ CFB gap-context threshold fixture set | accepted/current | `SAFE_FAST_DAY41_QQQ_GAP_THRESHOLD_FIXTURE_DECISION.md` accepts the first QQQ Clean Fast Break gap-context regression fixture thresholds: `clean` when absolute gap percent is `<= 0.30%`, `caution` when `> 0.30%` and `<= 0.75%`, `fail` when `> 0.75%`, and `unknown` when required data or no-hindsight proof is missing. This is a test-fixture decision only, not proof or profitability. |
| QQQ CFB gap-context regression fixtures | accepted/current | `historical_signal_replay/fixtures/qqq_gap_context_regression_fixtures.json` records data-only regression fixtures for clean, caution lower boundary, caution upper boundary, fail, missing-input unknowns, future-data rejection, and the known `2026-04-13` QQQ target. The fixture file does not create calculator logic, fill evidence, authorize backtests, choose trades, calculate P&L, prove profitability, or mark readiness. |
| QQQ CFB gap-context calculator | accepted/current | `historical_signal_replay/gap_context_calculator.py` calculates gap amount, gap percent, direction, `gap_context_status`, `gap_context_as_of`, and `gap_context_reviewed_before_signal` from accepted QQQ CFB fixtures. It reports future source timestamps as rejected and refuses trade choice, P&L, proof, profitability, or readiness inference. |
| QQQ CFB gap-context evidence fill | accepted/current | `historical_signal_replay/source_data/richer_export_package_work/qqq_cfb_gap_context_completeness_fields_rule.jsonl` is filled for `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` with `gap_context_status=clean`, `gap_context_as_of=2026-04-13T12:30:00-04:00`, and `gap_context_reviewed_before_signal=true` from the accepted calculator and fixtures. This passes one work-package request only and does not authorize backtest, trade selection, P&L, proof, profitability, candidate readiness, or intake-ready status. |
| Project speed layer | accepted/current | `SAFE_FAST_PROJECT_DASHBOARD.md`, `SAFE_FAST_CODEX_TASK_TEMPLATES.md`, `scripts/safe_fast_run_safe_checks.ps1`, and `historical_signal_replay/candidate_packets/` are the current speed layer. Future chats should read build state, dashboard, rule index, templates, and candidate packets before repeating discovery, and should use the safe-check runner before and after code changes. |

## Missing / Needs Decision

| Rule | Status | Missing decision |
| --- | --- | --- |
| QQQ gap threshold validation beyond first fixture | missing/needs decision | The first QQQ CFB gap-context test fixture thresholds are accepted for regression work, but profitable-plan calibration, sample-size validation, and promotion-grade threshold review remain undecided. |
| Contract selection | missing/needs decision | Exact option side, expiration, strike, and contract-selection rule for each setup path. |
| Entry rule | missing/needs decision | Exact entry timing and quote/fill rule. |
| Exit rule | missing/needs decision | Exact profit exit, time exit, invalidation exit, and end-of-day handling. |
| Stale/spent rules | missing/needs decision | Setup-specific rules and regression fixtures for stale/spent lifecycle states. |
| Stage transitions | missing/needs decision | Project-wide state transitions among watch, candidate, signal, spent, stale, invalidated, blocked, no-trade, and review. |
| Sample-size requirements | missing/needs decision | Minimum accepted sample counts by setup type, symbol, and failure/no-trade category. |
| Promotion gates | missing/needs decision | Exact criteria for moving from evidence review to reconsideration-eligible, intake-ready, shadow planning, and later money stages. |
| Option-field label rules | missing/needs decision | Exact SAFE-FAST rules for turning Databento raw option, quote, spread, volume, open-interest, and liquidity inputs into `option_context_status`, `execution_context_status`, and `complete_caution_review_status`. |
| QQQ CFB trade-plan rule set | missing/needs decision | Exact QQQ Clean Fast Break contract selection, entry, fill, spread/liquidity limits, exit, stop/invalidation translation, time exit, cost/slippage, failure labels, sample-size requirement, and promotion gate. |
| QQQ CFB headline and caution aggregation | missing/needs decision | Exact source requirement and label logic for headline context and complete caution review, including no-data behavior and precedence. |

## Pending Validation

| Rule or artifact | Status | Validation needed |
| --- | --- | --- |
| Databento QQQ OPRA validation | pending validation | Structural validation found definitions, bid/ask, timestamps, expirations, strikes, side, trade volume, and open interest/statistics. SAFE-FAST field mapping is documented, but code/tests and label rules remain missing. |
| Databento QQQ evidence field mapping | pending validation | `SAFE_FAST_DAY41_DATABENTO_QQQ_EVIDENCE_FIELD_MAPPING.md` maps validated Databento columns to raw option/liquidity inputs, and the local normalizer now has focused tests. SAFE-FAST label rules remain missing. |
| Databento QQQ OPRA normalizer | pending validation | `historical_signal_replay/databento_opra_normalizer.py` and `tests/test_databento_opra_normalizer.py` support local read-only raw OPRA normalization, joins, no-hindsight quote selection, spread inspection, statistics mapping, and refusal to infer fills/P&L/readiness. |
| QQQ CFB rule decision package | pending validation | `SAFE_FAST_DAY41_QQQ_CFB_RULE_DECISION_PACKAGE.md` lists the smallest ordered path from raw data to valid backtest, but the listed decisions, tests, evidence fills, and backtest path remain unimplemented. |
| Tastytrade historical option capability | pending validation | Existing local dxLink helpers provide underlying OHLCV only; historical option fields were not proven from current helpers. |
| QQQ gap-context calculator evidence use | pending validation | The calculator output is now filled into the QQQ CFB gap-context work-package request and that one request passes content validation. It still does not authorize backtest, trade selection, P&L, proof, profitability, or readiness. |
| Richer work-package requests | pending validation | Current content validation has `1` passed request and `8` failed requests. No request is accepted as proof, and no candidate is reconsideration-eligible or intake-ready. |

## Superseded

| Statement | Status | Current replacement |
| --- | --- | --- |
| `tastytrade is the raw-data source` as the active next-step framing | superseded | Tastytrade current helpers supplied underlying OHLCV only. Databento is now the likely validated historical option data source for QQQ, but mapping still needs validation. |
| `Before tastytrade proof` as the current next-chat blocker | superseded | Current baseline includes Databento QQQ download validation at `219be31`; next work is mapping validated option fields into SAFE-FAST evidence and trade-plan gates. |
| External option data downloaded: NO for the current repo state | superseded | Databento QQQ OPRA files are present locally and structurally validated, but remain local-only and uncommitted. |

## Conflicting / Needs Human Decision

| Item | Status | Decision needed |
| --- | --- | --- |
| Promotion-grade QQQ gap threshold label for `-0.2561%` | conflicting/needs human decision | The first regression fixture labels the measured `-0.2561%` QQQ CFB gap as `clean`, but promotion-grade proof, profitability calibration, and sample-backed validation remain undecided. |
| Whether current validated Databento fields are sufficient for every SAFE-FAST evidence field | conflicting/needs human decision | Mapping shows raw option/liquidity support only; SAFE-FAST label rules, contract selection, execution proof, and complete caution aggregation remain undecided. |
| How much failed/no-trade sample evidence is enough for promotion | conflicting/needs human decision | The project requires failures and no-trades, but sample-size gates are not fixed. |
