# SPY-REAL-HISTORICAL-CONTINUATION-001

## Identity

- Candidate id: `SPY-REAL-HISTORICAL-CONTINUATION-001`.
- Symbol: `SPY`.
- Setup type: Continuation.
- Signal/setup time: `2026-04-30T12:30:00-04:00`.
- Trigger: `715.61`.
- Invalidation: `708.37`.

## Repo Evidence

- Replay log: `historical_signal_replay/reports/first_real_spy_continuation_replay_v1_signal_log.jsonl`.
- Replay summary: `historical_signal_replay/reports/first_real_spy_continuation_replay_v1_summary.json`.
- Signal row: completed SPY Continuation trigger-stage candidate at `2026-04-30T12:30:00-04:00`.
- Later lifecycle row: spent/no-fresh-trigger context at `2026-04-30T15:30:00-04:00`.
- Current richer work-package request: none found.

## Current Status

- Replay artifact exists, but current request-shaped evidence package does not include this candidate.
- Continuation-specific lifecycle, contract-selection, option-context, headline, execution, entry, exit, cost, slippage, sample-size, and promotion rules are not accepted for this candidate.
- Backtest/P&L/proof/readiness: NO.

## Cheap Starter Databento Validation

- Validation doc: `SAFE_FAST_DAY41_CHEAP_STARTER_BATCH_VALIDATION.md`.
- Manifest: `historical_signal_replay/source_data/external_option_data_drop/SAFE_FAST_CHEAP_STARTER_DATABENTO_DOWNLOAD_MANIFEST.json`.
- Starter files present: definitions, statistics, 10-minute TCBBO quotes, and 10-minute trades.
- Row counts: definitions `12,970`, statistics `1,027,476`, quotes `13,598`, trades `13,598`.
- Starter-only checks now attemptable after Continuation rule authorization: option universe review, setup-time quote freshness, setup-time trade volume, and setup-time open-interest/statistics availability.
- Full-window data likely remains needed later for entry/exit/backtest/proof work.
- Evidence filled, backtest, P&L, proof, profitability, readiness: NO.

## Batch Plan

- Park until a Continuation rule/evidence package is explicitly authorized.
- If later authorized, start with source/log identity and no-hindsight lifecycle fixture work before option data pulls.
