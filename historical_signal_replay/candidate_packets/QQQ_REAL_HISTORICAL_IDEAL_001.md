# QQQ-REAL-HISTORICAL-IDEAL-001

## Identity

- Candidate id: `QQQ-REAL-HISTORICAL-IDEAL-001`.
- Symbol: `QQQ`.
- Setup type: Ideal.
- Signal/setup time: `2026-05-13T12:30:00-04:00`.
- Trigger: `714.59`.
- Invalidation: `696.66`.

## Repo Evidence

- Replay log: `historical_signal_replay/reports/first_real_qqq_ideal_replay_v1_signal_log.jsonl`.
- Replay summary: `historical_signal_replay/reports/first_real_qqq_ideal_replay_v1_summary.json`.
- Signal row: completed QQQ Ideal trigger-stage candidate at `2026-05-13T12:30:00-04:00`.
- Later lifecycle row: spent/no-fresh-trigger context at `2026-05-14T11:30:00-04:00`.
- Current richer work-package request: none found.

## Current Status

- Replay artifact exists, but current request-shaped evidence package does not include this candidate.
- Ideal-specific lifecycle, contract-selection, option-context, headline, execution, entry, exit, cost, slippage, sample-size, and promotion rules are not accepted for this candidate.
- Backtest/P&L/proof/readiness: NO.

## Cheap Starter Databento Validation

- Validation doc: `SAFE_FAST_DAY41_CHEAP_STARTER_BATCH_VALIDATION.md`.
- Manifest: `historical_signal_replay/source_data/external_option_data_drop/SAFE_FAST_CHEAP_STARTER_DATABENTO_DOWNLOAD_MANIFEST.json`.
- Starter files present: definitions, statistics, 10-minute TCBBO quotes, and 10-minute trades.
- Row counts: definitions `11,628`, statistics `914,920`, quotes `20,106`, trades `20,106`.
- Starter-only checks now attemptable after Ideal rule authorization: option universe review, setup-time quote freshness, setup-time trade volume, and setup-time open-interest/statistics availability.
- Full-window data likely remains needed later for entry/exit/backtest/proof work.
- Evidence filled, backtest, P&L, proof, profitability, readiness: NO.

## Batch Plan

- Park until an Ideal rule/evidence package is explicitly authorized.
- If later authorized, start with source/log identity and Ideal lifecycle fixture work before option data pulls.
