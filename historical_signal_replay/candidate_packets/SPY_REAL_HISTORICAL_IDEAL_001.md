# SPY-REAL-HISTORICAL-IDEAL-001

## Identity

- Candidate id: `SPY-REAL-HISTORICAL-IDEAL-001`.
- Symbol: `SPY`.
- Setup type: Ideal.
- Signal/setup time: `2026-05-13T11:30:00-04:00`.
- Trigger: `740.75`.
- Invalidation: `731.83`.

## Repo Evidence

- Source CSV: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`, line 291.
- Replay log: `historical_signal_replay/reports/second_real_spy_ideal_replay_v1_signal_log.jsonl`, line 5.
- Later lifecycle context: replay log line 6 marks prior completed Ideal trigger spent.
- Work-package rows exist:
  - `historical_signal_replay/source_data/richer_export_package_work/spy_ideal_stale_spent_expiry_rule_regressions.jsonl`.
  - `historical_signal_replay/source_data/richer_export_package_work/spy_ideal_gap_headline_option_execution_complete_caution_fields.jsonl`.

## Current Status

- Current work-package status: partial/missing required evidence.
- Tastytrade/dxLink local source provides underlying OHLCV and unconfirmed macro/IV/event fields only.
- Gap, headline, option, execution, and complete caution fields are not source-backed in the current local dxLink export.
- Accepted SPY Ideal lifecycle rule/regression package is still missing.
- Source row details: line 291 has `open=739.27`, `high=741.98`, `low=738.9451`, `close=741.725`, `volume=1914842.373732`, source_as_of `2026-05-13T18:43:00Z`.
- Replay row details: line 5 is `ideal_triggered_signal_stage_candidate`, `trigger_state=triggered`, `final_verdict=TRADE`, and explicitly lifecycle fixture only.
- Later lifecycle row: line 6 is spent context after follow-through and must not be used as setup-time signal evidence.
- Grouped Databento cost-check result: `SAFE_FAST_DAY41_SPY_BATCH_DATABENTO_COST_CHECK_RESULT.md`; `OPRA.PILLAR` cost estimate is `NOT_AVAILABLE_PROXY_BLOCKED`, and no local SPY OPRA files exist.
- Backtest/P&L/proof/readiness: NO.

## Current Blockers

- `spy_ideal_stale_spent_expiry_rule_regressions.jsonl` is blocked because `spy_ideal_stale_spent_expiry_rule` and `spy_ideal_expiry_regression_rows` are missing SAFE-FAST artifacts.
- `spy_ideal_gap_headline_option_execution_complete_caution_fields.jsonl` is blocked because `gap_context_status`, `headline_context_status`, `option_context_status`, `execution_context_status`, and `complete_caution_review_status` are unavailable from local SPY dxLink and replay rows.
- Ideal gap/context thresholds and lifecycle rules are not accepted.
- Ideal contract-selection rules are not accepted.
- Headline/no-headline source policy is not accepted.
- Entry, fill, exit, stop/invalidation, time exit, cost, slippage, sample-size, and promotion gates are not accepted.

## Cheap Starter Databento Validation

- Validation doc: `SAFE_FAST_DAY41_CHEAP_STARTER_BATCH_VALIDATION.md`.
- Manifest: `historical_signal_replay/source_data/external_option_data_drop/SAFE_FAST_CHEAP_STARTER_DATABENTO_DOWNLOAD_MANIFEST.json`.
- Starter files present: definitions, statistics, 10-minute TCBBO quotes, and 10-minute trades.
- Row counts: definitions `13,604`, statistics `1,068,996`, quotes `23,940`, trades `23,940`.
- Starter-only checks now attemptable after Ideal rule authorization: option universe review, setup-time quote freshness, setup-time trade volume, and setup-time open-interest/statistics availability.
- Full-window data likely remains needed later for entry/exit/backtest/proof work.
- Evidence filled, backtest, P&L, proof, profitability, readiness: NO.

## Starter Batch Option Inspection

- Inspection doc: `SAFE_FAST_DAY41_STARTER_BATCH_OPTION_INSPECTION.md`.
- Rule/data matrix: `SAFE_FAST_DAY41_STARTER_BATCH_RULE_AND_DATA_MATRIX.md`.
- Definitions exist: YES, `13,604` rows, `37` expirations.
- Setup-window quotes exist: YES, `23,940` rows; `10,302` at or before setup.
- Quote freshness: latest raw quote at/before setup `2026-05-13T15:29:59.996749Z`, about `0.003251` seconds before setup.
- Setup-window trades exist: YES, `23,940` rows; `10,302` at or before setup; setup-time-safe summed size `125,354`.
- Same-contract or usable statistics/open-interest exists for raw inspection: YES, `19,926` setup-time-safe `stat_type=9` rows across `1,107` quote/trade-window instruments.
- Starter data alone appears enough to continue: YES for first-pass raw option inspection after Ideal rule/regression authorization; NO for evidence fill, trade choice, proof, or readiness.
- Full-window data may be needed later: YES, for entry/fill/exit, full quote path, stop/invalidation, time exit, cost/slippage, sample-size, and proof work.
- Next grouped task after SPY CFB: Ideal setup-family rule/evidence package with `QQQ-REAL-HISTORICAL-IDEAL-001`.

## Data Needs

- Underlying candles: local setup-time OHLCV row exists; accepted Ideal gap/lifecycle/context artifacts still needed.
- Option definitions: SPY OPRA signal-date and prior-trading-day definitions needed for contract identity/listing checks after Ideal reviewed-universe rules exist.
- Option quotes: SPY OPRA TCBBO from regular-session open through `2026-05-13T11:30:00-04:00` needed after an Ideal contract-selection rule exists.
- Option trades: same-contract setup-time-safe volume needed.
- Option statistics/open interest: same-contract setup-time-safe OI needed, unless a later Ideal-specific exception is accepted.
- Execution freshness: must be checked early after selected contract identity exists.

## Batch Plan

- Include in the same SPY Databento cost-check pass if bounded.
- Grouped cost-check was attempted and proxy-blocked; rerun from a working HTTPS environment before any SPY OPRA download.
- Keep Ideal rule work separate from SPY CFB lifecycle decisions.
- Reuse Databento normalizer and context/caution aggregation vocabulary only after Ideal component rules are accepted.
- Do not apply QQQ CFB lifecycle, gap, or contract-selection rules to Ideal by assumption.
- Do not fill evidence, backtest, calculate P&L, claim proof/profitability, or mark readiness from this packet.
