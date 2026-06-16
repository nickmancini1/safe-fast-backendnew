# SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003

## Identity

- Candidate id: `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`.
- Symbol: `SPY`.
- Setup type: Clean Fast Break.
- Signal/setup time: `2026-04-15T14:30:00-04:00`.
- Trigger: `698.65`.
- Invalidation: `694.2801`.

## Repo Evidence

- Source CSV: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`, line 154.
- Replay log: `historical_signal_replay/reports/third_real_spy_clean_fast_break_replay_v1_signal_log.jsonl`, line 5.
- Later lifecycle context: replay log line 6 marks prior completed Clean Fast Break spent after the 14:30 break.
- Work-package rows exist:
  - `historical_signal_replay/source_data/richer_export_package_work/spy_cfb_003_higher_base_fresh_break_expiry_rule_regressions.jsonl`.
  - `historical_signal_replay/source_data/richer_export_package_work/spy_cfb_003_complete_context_caution_fields.jsonl`.

## Current Status

- Current work-package status: partial/missing required evidence.
- Tastytrade/dxLink local source provides underlying OHLCV and unconfirmed macro/IV/event fields only.
- Option context, headline context, execution context, and complete caution fields are not source-backed in the current local dxLink export.
- Accepted SPY CFB higher-base fresh-break lifecycle rule/regression package is still missing.
- Source row details: line 154 has `open=698.49`, `high=700.03`, `low=698.48`, `close=700.01`, `volume=4401495.310274`, source_as_of `2026-05-13T18:43:00Z`.
- Replay row details: line 5 is `clean_fast_break_fresh_break_signal_candidate`, `trigger_state=triggered`, `final_verdict=TRADE`, and explicitly lifecycle fixture only.
- Later lifecycle row: line 6 is spent context after the 14:30 break and must not be used as setup-time signal evidence.
- Grouped Databento cost-check result: `SAFE_FAST_DAY41_SPY_BATCH_DATABENTO_COST_CHECK_RESULT.md`; `OPRA.PILLAR` cost estimate is `NOT_AVAILABLE_PROXY_BLOCKED`, and no local SPY OPRA files exist.
- Backtest/P&L/proof/readiness: NO.

## Current Blockers

- `spy_cfb_003_higher_base_fresh_break_expiry_rule_regressions.jsonl` is blocked because `clean_fast_break_higher_base_fresh_break_expiry_rule` and `higher_base_fresh_break_expiry_regression_rows` are missing SAFE-FAST artifacts.
- `spy_cfb_003_complete_context_caution_fields.jsonl` is blocked because `option_context_status`, `headline_context_status`, `execution_context_status`, and `complete_caution_review_status` are unavailable from local SPY dxLink and replay rows.
- SPY CFB contract-selection rules and evidence authorization are not accepted.
- Headline/no-headline source policy is not accepted.
- Entry, fill, exit, stop/invalidation, time exit, cost, slippage, sample-size, and promotion gates are not accepted.

## Cheap Starter Databento Validation

- Validation doc: `SAFE_FAST_DAY41_CHEAP_STARTER_BATCH_VALIDATION.md`.
- Manifest: `historical_signal_replay/source_data/external_option_data_drop/SAFE_FAST_CHEAP_STARTER_DATABENTO_DOWNLOAD_MANIFEST.json`.
- Starter files present: definitions, statistics, 10-minute TCBBO quotes, and 10-minute trades.
- Row counts: definitions `13,422`, statistics `1,070,272`, quotes `26,724`, trades `26,724`.
- Starter-only checks now attemptable after rule authorization: option universe review, setup-time quote freshness, setup-time trade volume, and setup-time open-interest/statistics availability.
- Full-window data likely remains needed later for entry/exit/backtest/proof work.
- Evidence filled, backtest, P&L, proof, profitability, readiness: NO.

## Starter Batch Option Inspection

- Inspection doc: `SAFE_FAST_DAY41_STARTER_BATCH_OPTION_INSPECTION.md`.
- Rule/data matrix: `SAFE_FAST_DAY41_STARTER_BATCH_RULE_AND_DATA_MATRIX.md`.
- Definitions exist: YES, `13,422` rows, `36` expirations.
- Setup-window quotes exist: YES, `26,724` rows; `9,067` at or before setup.
- Quote freshness: latest raw quote at/before setup `2026-04-15T18:29:59.973562Z`, about `0.026438` seconds before setup.
- Setup-window trades exist: YES, `26,724` rows; `9,067` at or before setup; setup-time-safe summed size `104,943`.
- Same-contract or usable statistics/open-interest exists for raw inspection: YES, `29,412` setup-time-safe `stat_type=9` rows across `1,634` quote/trade-window instruments.
- Starter data alone appears enough to continue: YES for first-pass raw option inspection after SPY CFB higher-base rule/regression authorization; NO for evidence fill, trade choice, proof, or readiness.
- Full-window data may be needed later: YES, for entry/fill/exit, full quote path, stop/invalidation, time exit, cost/slippage, sample-size, and proof work.
- Next grouped task: SPY CFB grouped rule/regression package with `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`.

## Data Needs

- Underlying candles: local setup-time OHLCV row exists; accepted SPY CFB higher-base lifecycle/regression artifacts still needed.
- Option definitions: SPY OPRA signal-date and prior-trading-day definitions needed for contract identity/listing checks.
- Option quotes: SPY OPRA TCBBO from regular-session open through `2026-04-15T14:30:00-04:00` needed after a reviewed-universe rule exists.
- Option trades: same-contract setup-time-safe volume needed.
- Option statistics/open interest: same-contract setup-time-safe OI needed, unless a later explicit exception is accepted.
- Execution freshness: must be checked early after selected contract identity exists.

## Batch Plan

- Process in the first SPY CFB batch with `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`.
- Cost-check SPY OPRA definitions, TCBBO, trades, and statistics/OI around the setup window before any data pull: attempted and proxy-blocked; rerun from a working HTTPS environment before any SPY OPRA download.
- Reuse the Databento normalizer for read-only inspection if SPY OPRA data is later authorized.
- Use QQQ CFB calculators only as implementation patterns until SPY CFB rules and fixtures are accepted.
- Do not fill evidence, backtest, calculate P&L, claim proof/profitability, or mark readiness from this packet.
