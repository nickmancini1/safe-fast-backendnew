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
| No proof / no profitability claim | accepted/current | Current docs must not claim proof, profitability, candidate readiness, or intake-ready status. |

## Missing / Needs Decision

| Rule | Status | Missing decision |
| --- | --- | --- |
| QQQ gap thresholds | missing/needs decision | Numeric clean/caution/fail thresholds for QQQ Clean Fast Break gap context. |
| Contract selection | missing/needs decision | Exact option side, expiration, strike, and contract-selection rule for each setup path. |
| Entry rule | missing/needs decision | Exact entry timing and quote/fill rule. |
| Exit rule | missing/needs decision | Exact profit exit, time exit, invalidation exit, and end-of-day handling. |
| Stale/spent rules | missing/needs decision | Setup-specific rules and regression fixtures for stale/spent lifecycle states. |
| Stage transitions | missing/needs decision | Project-wide state transitions among watch, candidate, signal, spent, stale, invalidated, blocked, no-trade, and review. |
| Sample-size requirements | missing/needs decision | Minimum accepted sample counts by setup type, symbol, and failure/no-trade category. |
| Promotion gates | missing/needs decision | Exact criteria for moving from evidence review to reconsideration-eligible, intake-ready, shadow planning, and later money stages. |
| Option-field label rules | missing/needs decision | Exact SAFE-FAST rules for turning Databento raw option, quote, spread, volume, open-interest, and liquidity inputs into `option_context_status`, `execution_context_status`, and `complete_caution_review_status`. |

## Pending Validation

| Rule or artifact | Status | Validation needed |
| --- | --- | --- |
| Databento QQQ OPRA validation | pending validation | Structural validation found definitions, bid/ask, timestamps, expirations, strikes, side, trade volume, and open interest/statistics. SAFE-FAST field mapping is documented, but code/tests and label rules remain missing. |
| Databento QQQ evidence field mapping | pending validation | `SAFE_FAST_DAY41_DATABENTO_QQQ_EVIDENCE_FIELD_MAPPING.md` maps validated Databento columns to raw option/liquidity inputs, but implementation tests and SAFE-FAST label rules are still missing. |
| Tastytrade historical option capability | pending validation | Existing local dxLink helpers provide underlying OHLCV only; historical option fields were not proven from current helpers. |
| QQQ gap-context calculator | pending validation | Calculator remains unauthorized until thresholds and regression cases are accepted. |
| Richer work-package requests | pending validation | Current content validation remains failed/partial; no request is accepted as proof. |

## Superseded

| Statement | Status | Current replacement |
| --- | --- | --- |
| `tastytrade is the raw-data source` as the active next-step framing | superseded | Tastytrade current helpers supplied underlying OHLCV only. Databento is now the likely validated historical option data source for QQQ, but mapping still needs validation. |
| `Before tastytrade proof` as the current next-chat blocker | superseded | Current baseline includes Databento QQQ download validation at `219be31`; next work is mapping validated option fields into SAFE-FAST evidence and trade-plan gates. |
| External option data downloaded: NO for the current repo state | superseded | Databento QQQ OPRA files are present locally and structurally validated, but remain local-only and uncommitted. |

## Conflicting / Needs Human Decision

| Item | Status | Decision needed |
| --- | --- | --- |
| Exact QQQ gap threshold label for `-0.2561%` | conflicting/needs human decision | Repo evidence permits measurement but not clean/caution/fail classification. |
| Whether current validated Databento fields are sufficient for every SAFE-FAST evidence field | conflicting/needs human decision | Mapping shows raw option/liquidity support only; SAFE-FAST label rules, contract selection, execution proof, and complete caution aggregation remain undecided. |
| How much failed/no-trade sample evidence is enough for promotion | conflicting/needs human decision | The project requires failures and no-trades, but sample-size gates are not fixed. |
