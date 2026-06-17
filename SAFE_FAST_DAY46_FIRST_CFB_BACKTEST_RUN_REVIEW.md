# SAFE-FAST Day 46 First CFB Backtest Run Review

## Direct Answer

The first local Clean Fast Break backtest path was implemented and run against the three authorized candidates.

`SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` entered the runner and applied the accepted entry, target, stop, invalidation, time-exit, and slippage rules, but the local starter data is not enough to complete the exit path. The run stops with named missing data instead of guessing.

## Local Run Result

| Candidate | Local runner result | Named reason |
| --- | --- | --- |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | `blocked_missing_exit_path_data` | `selected_contract_tcbbo_bid_path_through_1545_et` |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | `no_trade` | `quote_after_signal` |
| `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | `no_trade` | `quote_age_above_5_minutes` |

## SPY CFB 002 Rule Application

- Selected contract: `SPY   260427C00685000`.
- Entry quote: `2026-04-13T16:29:04.514819033Z`.
- Entry basis: ask `6.35` plus `0.02` slippage = `6.37`.
- Profit target threshold: `7.9625` cost-adjusted option exit basis.
- Option stop threshold: `5.4145` cost-adjusted option exit basis.
- Exit basis rule: bid minus `0.02`.
- Time exit: `15:45 ET` on `2026-04-13`.

## Missing Exit-Path Data

Exact missing fields:

- `selected_contract_tcbbo_bid_path_through_1545_et`.
- `source_backed_underlying_invalidation_path_through_1545_et`.

Starter data is enough to verify entry and immediate local quote-path behavior only. It is not enough to complete target, stop, invalidation, or time-exit evaluation through `15:45 ET`.

## Cost-Check Request

Before any full-window download, run a Databento `OPRA.PILLAR` cost check for the selected contract only:

- Contract: `SPY   260427C00685000`.
- Instrument id: `1258293281`.
- Dataset/schema: `OPRA.PILLAR` TCBBO quotes.
- Window: `2026-04-13T16:30:00Z` through `2026-04-13T19:45:00Z`.
- Also confirm source-backed underlying invalidation-path coverage through `15:45 ET`.

No full-window data was downloaded in this task.

## Guardrails

- Local runner implemented: YES.
- Existing local data only: YES.
- Databento downloaded: NO.
- Raw Databento files changed: NO.
- Backtest path attempted locally: YES.
- Countable completed CFB example produced: NO.
- P&L calculated: NO.
- Promotion decision made: NO.
- Proof accepted: NO.
- Profitability claimed: NO.
- Candidate marked ready: NO.
- Intake-ready count changed: NO.
