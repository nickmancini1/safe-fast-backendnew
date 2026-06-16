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
- Backtest/P&L/proof/readiness: NO.

## Current Blockers

- `spy_ideal_stale_spent_expiry_rule_regressions.jsonl` is blocked because `spy_ideal_stale_spent_expiry_rule` and `spy_ideal_expiry_regression_rows` are missing SAFE-FAST artifacts.
- `spy_ideal_gap_headline_option_execution_complete_caution_fields.jsonl` is blocked because `gap_context_status`, `headline_context_status`, `option_context_status`, `execution_context_status`, and `complete_caution_review_status` are unavailable from local SPY dxLink and replay rows.
- Ideal gap/context thresholds and lifecycle rules are not accepted.
- Ideal contract-selection rules are not accepted.
- Headline/no-headline source policy is not accepted.
- Entry, fill, exit, stop/invalidation, time exit, cost, slippage, sample-size, and promotion gates are not accepted.

## Data Needs

- Underlying candles: local setup-time OHLCV row exists; accepted Ideal gap/lifecycle/context artifacts still needed.
- Option definitions: SPY OPRA signal-date and prior-trading-day definitions needed for contract identity/listing checks after Ideal reviewed-universe rules exist.
- Option quotes: SPY OPRA TCBBO from regular-session open through `2026-05-13T11:30:00-04:00` needed after an Ideal contract-selection rule exists.
- Option trades: same-contract setup-time-safe volume needed.
- Option statistics/open interest: same-contract setup-time-safe OI needed, unless a later Ideal-specific exception is accepted.
- Execution freshness: must be checked early after selected contract identity exists.

## Batch Plan

- Include in the same SPY Databento cost-check pass if bounded.
- Keep Ideal rule work separate from SPY CFB lifecycle decisions.
- Reuse Databento normalizer and context/caution aggregation vocabulary only after Ideal component rules are accepted.
- Do not apply QQQ CFB lifecycle, gap, or contract-selection rules to Ideal by assumption.
- Do not fill evidence, backtest, calculate P&L, claim proof/profitability, or mark readiness from this packet.
