# SAFE-FAST Day 41 SPY Batch Preflight

## Baseline

- Task baseline states latest commit: `7d483ab Add batch restart plan after QQQ diagnosis`.
- This is a preflight and planning task only.
- Evidence filled: NO.
- Databento downloaded: NO.
- Backtest authorized: NO.
- P&L calculated: NO.
- Proof accepted: NO.
- Profitability claimed: NO.
- Candidate readiness changed: NO.

## Scope

Batch candidates:

- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`.
- `SPY-REAL-HISTORICAL-IDEAL-001`.

The two SPY Clean Fast Break candidates should be processed as a pair. `SPY-REAL-HISTORICAL-IDEAL-001` can share the same SPY Databento cost-check pass, but Ideal rule work must stay separate from Clean Fast Break lifecycle and contract-selection decisions.

## Candidate Inventory

| Candidate | Setup type | Symbol | Signal/setup time | Trigger/level | Invalidation | Existing source files | Existing evidence rows | Current evidence state | Current blockers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | Clean Fast Break | SPY | `2026-04-13T12:30:00-04:00` | `682.03` | `678.45` | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` line 138; `historical_signal_replay/reports/third_real_spy_clean_fast_break_replay_v1_signal_log.jsonl` lines 2-3 | `spy_cfb_002_initial_break_expiry_rule_regressions.jsonl`; `spy_cfb_002_complete_context_caution_fields.jsonl` | `partial_missing_required_evidence`; current rows contain `TASTYTRADE_DATA_NOT_AVAILABLE` blockers | SPY CFB initial-break lifecycle rule/regressions missing; option/headline/execution/complete-caution fields missing; SPY contract-selection/evidence authorization missing; entry/exit/cost/slippage and promotion gates missing |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | Clean Fast Break | SPY | `2026-04-15T14:30:00-04:00` | `698.65` | `694.2801` | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` line 154; `historical_signal_replay/reports/third_real_spy_clean_fast_break_replay_v1_signal_log.jsonl` lines 5-6 | `spy_cfb_003_higher_base_fresh_break_expiry_rule_regressions.jsonl`; `spy_cfb_003_complete_context_caution_fields.jsonl` | `partial_missing_required_evidence`; current rows contain `TASTYTRADE_DATA_NOT_AVAILABLE` blockers | SPY CFB higher-base fresh-break lifecycle rule/regressions missing; option/headline/execution/complete-caution fields missing; SPY contract-selection/evidence authorization missing; entry/exit/cost/slippage and promotion gates missing |
| `SPY-REAL-HISTORICAL-IDEAL-001` | Ideal | SPY | `2026-05-13T11:30:00-04:00` | `740.75` | `731.83` | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` line 291; `historical_signal_replay/reports/second_real_spy_ideal_replay_v1_signal_log.jsonl` lines 5-6 | `spy_ideal_stale_spent_expiry_rule_regressions.jsonl`; `spy_ideal_gap_headline_option_execution_complete_caution_fields.jsonl` | `partial_missing_required_evidence`; current rows contain `TASTYTRADE_DATA_NOT_AVAILABLE` blockers | SPY Ideal lifecycle rule/regressions missing; Ideal gap/headline/option/execution/complete-caution fields missing; Ideal contract-selection rule missing; entry/exit/cost/slippage and promotion gates missing |

## Local Source Row Check

| Candidate | Local underlying candle evidence | Replay signal evidence | Future/later lifecycle row |
| --- | --- | --- | --- |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | Source line 138: 1h RTH candle `open=681.38`, `high=682.82`, `low=680.71`, `close=682.48`, `volume=3307087.642277`, source `dxlink_candles.get_1h_ema50_snapshot`, source_as_of `2026-05-13T18:43:00Z`, vendor `dxFeed via tastytrade dxLink` | Replay line 2: `current_state=signal`, `stage=clean_fast_break_initial_break_candidate`, `trigger_state=triggered`, `final_verdict=TRADE`, but explicitly lifecycle fixture only | Replay line 3: later same-session follow-through/spent context; not valid setup-time evidence for the signal row |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | Source line 154: 1h RTH candle `open=698.49`, `high=700.03`, `low=698.48`, `close=700.01`, `volume=4401495.310274`, source `dxlink_candles.get_1h_ema50_snapshot`, source_as_of `2026-05-13T18:43:00Z`, vendor `dxFeed via tastytrade dxLink` | Replay line 5: `current_state=signal`, `stage=clean_fast_break_fresh_break_signal_candidate`, `trigger_state=triggered`, `final_verdict=TRADE`, but explicitly lifecycle fixture only | Replay line 6: later spent context after the 14:30 break; not valid setup-time evidence for the signal row |
| `SPY-REAL-HISTORICAL-IDEAL-001` | Source line 291: 1h RTH candle `open=739.27`, `high=741.98`, `low=738.9451`, `close=741.725`, `volume=1914842.373732`, source `dxlink_candles.get_1h_ema50_snapshot`, source_as_of `2026-05-13T18:43:00Z`, vendor `dxFeed via tastytrade dxLink` | Replay line 5: `current_state=signal`, `stage=ideal_triggered_signal_stage_candidate`, `trigger_state=triggered`, `final_verdict=TRADE`, but explicitly lifecycle fixture only | Replay line 6: later Ideal spent context; not valid setup-time evidence for the signal row |

## Existing Evidence Rows

| Candidate | Lifecycle/expiry row | Context/caution row | Current passed/failed state |
| --- | --- | --- | --- |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | `spy_cfb_002_initial_break_expiry_rule_regressions.jsonl` says `clean_fast_break_initial_break_expiry_rule` and `initial_break_expiry_regression_rows` are SAFE-FAST artifacts not provided by local tastytrade/dxLink OHLCV | `spy_cfb_002_complete_context_caution_fields.jsonl` says option, headline, execution, and complete caution statuses are not present in local SPY dxLink source or replay log | Not passed; both rows remain partial/missing required evidence |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | `spy_cfb_003_higher_base_fresh_break_expiry_rule_regressions.jsonl` says `clean_fast_break_higher_base_fresh_break_expiry_rule` and `higher_base_fresh_break_expiry_regression_rows` are SAFE-FAST artifacts not provided by local tastytrade/dxLink OHLCV | `spy_cfb_003_complete_context_caution_fields.jsonl` says option, headline, execution, and complete caution statuses are not present in local SPY dxLink source or replay log | Not passed; both rows remain partial/missing required evidence |
| `SPY-REAL-HISTORICAL-IDEAL-001` | `spy_ideal_stale_spent_expiry_rule_regressions.jsonl` says `spy_ideal_stale_spent_expiry_rule` and `spy_ideal_expiry_regression_rows` are SAFE-FAST artifacts not provided by local tastytrade/dxLink OHLCV | `spy_ideal_gap_headline_option_execution_complete_caution_fields.jsonl` says gap, headline, option, execution, and complete caution statuses are not present in local SPY dxLink source or replay log | Not passed; both rows remain partial/missing required evidence |

## Batch Data-Needs Table

| Candidate | Underlying candles needed | Option definitions needed | Option quotes needed | Option trades needed | Option statistics/OI needed | Headline/context source needed | Execution quote freshness needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | Local SPY 1h RTH row exists; lifecycle regressions still need accepted SPY CFB rule artifacts | SPY OPRA definitions for signal date and prior trading day for listing/contract identity | SPY OPRA TCBBO from regular-session open through `2026-04-13T12:30:00-04:00`, narrowed after reviewed-universe rule | Same-contract trades through setup for setup-time-safe volume | Same-contract statistics/open-interest at or before setup, or explicit listing-aware exception if accepted later | Source-confirmed headline/no-headline and macro/event policy; local rows are unconfirmed only | Required after selected contract exists; QQQ lesson says quote age must be checked early and stale quotes must fail |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | Local SPY 1h RTH row exists; lifecycle regressions still need accepted SPY CFB higher-base rule artifacts | SPY OPRA definitions for signal date and prior trading day for listing/contract identity | SPY OPRA TCBBO from regular-session open through `2026-04-15T14:30:00-04:00`, narrowed after reviewed-universe rule | Same-contract trades through setup for setup-time-safe volume | Same-contract statistics/open-interest at or before setup, or explicit listing-aware exception if accepted later | Source-confirmed headline/no-headline and macro/event policy; local rows are unconfirmed only | Required after selected contract exists; check selected-contract quote age before writing broad rule work |
| `SPY-REAL-HISTORICAL-IDEAL-001` | Local SPY 1h RTH row exists; Ideal gap/lifecycle status needs Ideal-specific accepted rules | SPY OPRA definitions for signal date and prior trading day for listing/contract identity | SPY OPRA TCBBO from regular-session open through `2026-05-13T11:30:00-04:00`, narrowed after Ideal reviewed-universe rule | Same-contract trades through setup for setup-time-safe volume | Same-contract statistics/open-interest at or before setup, or Ideal-specific exception if accepted later | Source-confirmed headline/no-headline and Ideal context policy; local rows are unconfirmed only | Required after Ideal selected contract exists; do not apply QQQ CFB contract rules by assumption |

## Tool Reuse Assessment

Can be reused immediately as read-only/preflight concepts:

- `historical_signal_replay/databento_opra_normalizer.py` for local OPRA parsing and quote/trade/statistics inspection if SPY OPRA files later exist or are explicitly authorized.
- `historical_signal_replay/context_caution_calculator.py` for aggregation precedence only after accepted component statuses exist.
- `historical_signal_replay/execution_context_calculator.py` for quote-age/spread/size/volume checks only after a selected contract is defined.

Can be reused only as implementation templates until rules are accepted:

- `historical_signal_replay/gap_context_calculator.py` for SPY only after SPY/setup-specific gap thresholds are accepted.
- `historical_signal_replay/cfb_lifecycle_calculator.py` for SPY CFB only after SPY CFB initial-break and higher-base fixture decisions exist, or after a project-wide CFB lifecycle rule is accepted.
- `historical_signal_replay/cfb_contract_selector.py` for SPY only after SPY CFB or Ideal reviewed-universe, side, expiration, strike, quote, trade, OI, and no-fallback rules are accepted.

Must not be assumed:

- QQQ CFB gap thresholds prove SPY or Ideal gap context.
- QQQ CFB lifecycle fixtures prove SPY CFB lifecycle without an accepted cross-symbol rule.
- QQQ CFB contract-selection rules prove Ideal contract selection.
- A quote row is a fill, a trade choice, proof, profitability, or readiness.

## Immediate Local Checks vs Databento Needs

Can be attempted from local repo state now:

- Confirm each source CSV row exists.
- Confirm each replay signal row exists.
- Confirm trigger and invalidation values.
- Confirm work-package row presence and current partial/missing status.
- Draft SPY CFB lifecycle decision/regression needs.
- Draft Ideal lifecycle and context rule gaps.

Needs Databento cost-check or later authorized data pull:

- SPY OPRA definition coverage.
- SPY selected-contract quote coverage.
- SPY same-contract trade-volume coverage.
- SPY same-contract statistics/open-interest coverage.
- Selected-contract quote freshness.

Needs human/rule decision before evidence fill or selection:

- SPY CFB initial-break lifecycle rule/regression rows.
- SPY CFB higher-base fresh-break lifecycle rule/regression rows.
- SPY Ideal stale/spent lifecycle rule/regression rows.
- SPY CFB and Ideal contract-selection rules.
- Headline/no-headline source policy.
- Entry, fill, exit, stop/invalidation, time exit, costs, slippage, failure labels, sample-size requirements, and promotion gates.

## Preflight Result

The three SPY candidates are evidence-shaped, but none is ready for evidence fill. Local source and replay rows are present, while the current work-package rows still fail because local tastytrade/dxLink rows contain only underlying OHLCV and unconfirmed macro/IV/event context, not accepted SAFE-FAST lifecycle artifacts or option/headline/execution component statuses.

The next useful grouped action is a SPY Databento cost-check package covering the two CFB candidates and optionally the Ideal candidate. No raw data should be downloaded until a later task explicitly authorizes it.
