# SAFE-FAST Day 41 Databento QQQ Evidence Field Mapping

## Scope

Target candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Goal: map the validated local Databento QQQ OPRA files to SAFE-FAST evidence-field requirements without filling evidence, choosing a trade, calculating P&L, or marking QQQ ready.

Baseline: `6f1eac1 Add project control consolidation audit`.

Raw Databento files inspected as local files only:

- `historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_definitions_full_day.csv`
- `historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_tcbbo_1225_1235_et.csv`
- `historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_trades_1225_1235_et.csv`
- `historical_signal_replay/source_data/external_option_data_drop/QQQ_OPRA_statistics_full_day.csv`

No vendor API was called. No raw data file was edited. No evidence file was filled.

## Candidate Evidence Fields

The QQQ work package contains three request groups for this candidate.

| Request file | SAFE-FAST fields required |
| --- | --- |
| `qqq_cfb_gap_context_completeness_fields_rule.jsonl` | `gap_context_status`, `gap_context_as_of`, `gap_context_reviewed_before_signal` |
| `qqq_cfb_stale_spent_expiry_rule_regressions.jsonl` | `clean_fast_break_stale_spent_expiry_rule`, `clean_fast_break_expiry_regression_rows` |
| `qqq_cfb_complete_context_caution_fields.jsonl` | `option_context_status`, `headline_context_status`, `execution_context_status`, `complete_caution_review_status` |

The common work-package fields already identify the candidate, symbol, setup type, signal time, trigger, invalidation, source row, replay row, and no-hindsight boundary. Databento does not replace those source/replay fields.

## Databento Column Mapping

| SAFE-FAST raw input or derived inspection field | Databento support | Databento source columns |
| --- | --- | --- |
| Underlying symbol | Supported | definitions `underlying`; OPRA symbol prefix in `symbol` / `raw_symbol` |
| Option contract identifier | Supported | definitions `symbol`, `raw_symbol`, `instrument_id`; TCBBO/trades/statistics `symbol`, `instrument_id` |
| Expiration date | Supported | definitions `expiration`; also parseable from OPRA/OCC-style `symbol` |
| Strike price | Supported | definitions `strike_price`; also parseable from OPRA/OCC-style `symbol` |
| Option side/type | Supported | definitions `instrument_class`; also parseable as `C` or `P` from OPRA/OCC-style `symbol` |
| Quote event timestamp | Supported | TCBBO `ts_event` |
| Quote receive timestamp | Supported | TCBBO `ts_recv` |
| Bid price | Supported | TCBBO `bid_px_00` |
| Ask price | Supported | TCBBO `ask_px_00` |
| Bid size | Supported | TCBBO `bid_sz_00` |
| Ask size | Supported | TCBBO `ask_sz_00` |
| Midpoint for inspection | Raw-supported, derived | `(bid_px_00 + ask_px_00) / 2` |
| Spread for inspection | Raw-supported, derived | `ask_px_00 - bid_px_00` |
| Spread percent for inspection | Raw-supported, derived | `(ask_px_00 - bid_px_00) / midpoint` when midpoint is positive |
| Quote age versus signal | Raw-supported, derived | signal time `2026-04-13T16:30:00Z` minus selected TCBBO `ts_event` |
| Trade timestamp | Supported | trades `ts_event`, `ts_recv` |
| Trade price | Supported | trades `price` |
| Trade size | Supported | trades `size` |
| Trade volume | Supported | trades `size`; statistics `quantity` where `stat_type` is Databento cleared volume |
| Open interest | Supported | statistics `quantity` where `stat_type` is Databento open interest |
| Statistics reference timestamp | Supported | statistics `ts_ref`, `ts_event`, `ts_recv` |
| Contract multiplier | Supported | definitions `contract_multiplier`, `original_contract_size` |
| Minimum tick / increment | Supported | definitions `min_price_increment`, `min_price_increment_amount`, `display_factor` |
| Exchange or venue-like source metadata | Partially supported | definitions `exchange`, `publisher_id`; quote rows `publisher_id` |
| Last price | Partially supported | trades `price` can provide trade prints, but Databento TCBBO file does not provide a separate quote-row last price field |
| Mark price | Not directly supplied | Derive midpoint only; do not treat midpoint as broker mark without an accepted rule |
| Underlying price at quote time | Not supplied by these OPRA files | Existing QQQ underlying source CSV has setup-time OHLCV separately; OPRA files do not include underlying quote/trade price |
| Implied volatility and Greeks | Not supplied by validated files | No IV, delta, gamma, theta, or vega columns found |
| Headline/news/event context | Not supplied by validated files | No headline, macro, event, or news columns found |
| Broker/account/order/fill fields | Not supplied and not allowed | No account, order, fill, broker routing, or P&L fields are present or needed for this mapping |

## SAFE-FAST Field Sufficiency

| SAFE-FAST field | Databento can support from validated files? | Mapping result |
| --- | --- | --- |
| `gap_context_status` | No | Requires QQQ Clean Fast Break gap thresholds and a SAFE-FAST gap-context rule. Databento option files do not classify the underlying gap. |
| `gap_context_as_of` | No | Requires the accepted no-hindsight gap-context rule over underlying source candles. Databento OPRA files do not define this label. |
| `gap_context_reviewed_before_signal` | No | Requires regression proof that no future candle, future replay row, or outcome evidence affected the label. Databento OPRA files do not prove this. |
| `clean_fast_break_stale_spent_expiry_rule` | No | This is a SAFE-FAST lifecycle rule artifact, not vendor market data. |
| `clean_fast_break_expiry_regression_rows` | No | This is a SAFE-FAST regression artifact, not vendor market data. |
| `option_context_status` | Raw-data supported, not label-supported | Databento supports option chain, quote, spread, size, volume, and open-interest inputs. SAFE-FAST still needs an accepted option-context rule to turn those inputs into a status. |
| `headline_context_status` | No | The validated OPRA files contain no headline, macro, news, or event feed. |
| `execution_context_status` | Raw-data supported, not label-supported | Databento supports historical quote/trade inputs around the signal, but not fills. SAFE-FAST still needs entry timing, quote selection, fill assumption, spread, slippage, and failure rules. |
| `complete_caution_review_status` | Partially raw-data supported, not label-supported | Databento can inform the option/liquidity/execution slice only. Gap, headline, lifecycle, and complete caution aggregation rules remain missing. |

## Trade-Plan Gate Mapping

Databento can support later trade-plan review only at the raw option-data layer.

| Trade-plan completeness field | Databento support | Blocker |
| --- | --- | --- |
| Exact option contract selection rule | Partially supports available contracts | SAFE-FAST has not chosen side, expiration, strike, DTE, debit-spread width, or ranking rule for this candidate. |
| Side | Raw chain supports calls and puts | SAFE-FAST has not selected long call, long put, spread direction, or abstain rule. |
| Expiration | Raw chain supports expirations found in the files | SAFE-FAST has not selected expiration or fallback behavior when requested dates are absent. |
| Strike | Raw chain supports strikes found in the files | SAFE-FAST has not selected strike selection or spread-leg rules. |
| Entry timing | Quote timestamps support a nearest-at-or-before-signal lookup | SAFE-FAST has not accepted the entry timing rule. |
| Fill assumption | Quotes support bid/ask/mid inspection | Quotes are not fills; fill rule remains missing. |
| Bid/ask/mid/spread rule | Raw-supported | Accepted spread and midpoint rules remain missing. |
| Volume, open interest, liquidity minimums | Raw-supported | Minimum thresholds remain missing. |
| Exit rule | Not supported | Databento window is signal-centered only and no SAFE-FAST exit rule is accepted. |
| Stop or invalidation rule | Underlying invalidation is known from repo evidence | Option exit/stop translation is not accepted. |
| Time exit or EOD rule | Not supported by current bounded quote window | Rule and data window requirements remain missing. |
| Cost and slippage assumptions | Raw quote spread can inform later assumptions | Assumptions are not accepted. |
| Failure conditions | Not supplied by vendor | SAFE-FAST must define failure conditions. |

## Raw-Supported But Not Label-Supported

These areas have enough Databento structure to justify a later parser/normalizer, but they cannot be filled as SAFE-FAST statuses yet:

- Contract inventory for QQQ options on `2026-04-13`.
- Expiration, strike, side, and contract metadata.
- Bid, ask, bid size, ask size, quote timestamps, and quote age around `2026-04-13T12:30:00-04:00`.
- Derived midpoint, spread, and spread percent for inspection.
- Trade prints around the quote window.
- Cleared volume and open-interest statistics where the Databento `stat_type` mapping is applied.
- Liquidity review inputs for later `option_context_status` and `execution_context_status`.

## Still Unsupported

The validated Databento files do not support:

- `gap_context_status`, `gap_context_as_of`, or `gap_context_reviewed_before_signal`.
- QQQ Clean Fast Break numeric clean/caution/fail gap thresholds.
- Clean Fast Break stale/spent lifecycle rule text.
- Clean Fast Break expiry regression rows.
- Headline, macro, IV/event, or news context.
- Actual order routing, fills, account execution, partial fills, cancels, replacements, slippage, or P&L.
- Profitability.
- Candidate promotion, reconsideration eligibility, or intake readiness.

## Minimum Next Code And Tests

No code or tests were written in this task. The minimum next authorized implementation should be data-only and evidence-preserving:

1. Add a read-only Databento QQQ OPRA normalizer for local CSV files.
2. Parse OPRA/OCC-style symbols into underlying, expiration, side, and strike, and cross-check against definitions.
3. Join TCBBO, trades, statistics, and definitions by `instrument_id` and/or `symbol`.
4. Select the nearest quote at or before `2026-04-13T12:30:00-04:00` without using later rows for setup-time labels.
5. Derive inspection fields only: midpoint, spread, spread percent, quote age, trade counts/volume, and open interest.
6. Keep output as a mapping/inspection artifact, not an evidence fill, until SAFE-FAST label rules are accepted.
7. Add tests for symbol parsing, timestamp timezone handling, no-hindsight quote selection, definition joins, missing statistics, stat-type interpretation, and refusal to infer fills/P&L/profitability.

## Result

Databento QQQ OPRA files can support raw option, quote, trade, spread, volume, open-interest, and liquidity inputs for the QQQ Clean Fast Break candidate.

They cannot by themselves support SAFE-FAST labels, gap thresholds, lifecycle rules, regression artifacts, headline context, contract selection, execution proof, fills, P&L, profitability, or readiness.

Evidence filled: NO.

Trade chosen: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Proof accepted: NO.

Profitability claimed: NO.
