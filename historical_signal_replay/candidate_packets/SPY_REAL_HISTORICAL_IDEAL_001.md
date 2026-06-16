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
- Backtest/P&L/proof/readiness: NO.

## Batch Plan

- Include in the same SPY Databento cost-check pass if bounded.
- Keep Ideal rule work separate from SPY CFB lifecycle decisions.
- Reuse Databento normalizer and context/caution aggregation vocabulary only after Ideal component rules are accepted.
