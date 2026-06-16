# SAFE-FAST Day 41 Cheap Starter Databento Batch Validation

## Scope

- Mode: batch validation only.
- Data source: local cheap starter Databento files in `historical_signal_replay/source_data/external_option_data_drop/`.
- Manifest: `historical_signal_replay/source_data/external_option_data_drop/SAFE_FAST_CHEAP_STARTER_DATABENTO_DOWNLOAD_MANIFEST.json`.
- Manifest exists: YES.
- Manifest created at UTC: `2026-06-16T13:10:51.013240+00:00`.
- Manifest mode: `cheap starter download only`.
- Manifest estimated cost: `12.136024817825998`.

## Guardrails

- Downloaded more data: NO.
- Used full-window data: NO.
- Filled evidence: NO.
- Backtested: NO.
- Calculated P&L: NO.
- Claimed proof or profitability: NO.
- Marked candidate ready: NO.
- Modified raw Databento files: NO.

## Expected Starter Files

Each requested candidate has all four expected starter CSV files:

- `definitions_full_day`
- `statistics_full_day`
- `tcbbo_signal_10min`
- `trades_signal_10min`

Each expected CSV is present and nonempty for all six candidates.

## Candidate Row Counts

| Candidate | Definitions rows | Statistics rows | 10-minute quote rows | 10-minute trade rows |
| --- | ---: | ---: | ---: | ---: |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | 13,390 | 1,056,976 | 53,730 | 53,730 |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | 13,422 | 1,070,272 | 26,724 | 26,724 |
| `SPY-REAL-HISTORICAL-IDEAL-001` | 13,604 | 1,068,996 | 23,940 | 23,940 |
| `QQQ-REAL-HISTORICAL-CONTINUATION-001` | 11,128 | 885,376 | 13,799 | 13,799 |
| `QQQ-REAL-HISTORICAL-IDEAL-001` | 11,628 | 914,920 | 20,106 | 20,106 |
| `SPY-REAL-HISTORICAL-CONTINUATION-001` | 12,970 | 1,027,476 | 13,598 | 13,598 |

## Starter Time Coverage

| Candidate | Definition `ts_event` range | Statistics `ts_event` range | Quote `ts_event` range | Trade `ts_event` range |
| --- | --- | --- | --- | --- |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | `2026-04-13T10:30:00.577278960Z` to `2026-04-13T12:00:00.230622119Z` | `2026-04-13T10:30:00.577278960Z` to `2026-04-13T21:44:59.097883480Z` | `2026-04-13T16:25:00.035333703Z` to `2026-04-13T16:34:59.990131064Z` | `2026-04-13T16:25:00.035333703Z` to `2026-04-13T16:34:59.990131064Z` |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | `2026-04-15T10:30:00.579636876Z` to `2026-04-15T12:00:01.601956692Z` | `2026-04-15T10:30:00.579636876Z` to `2026-04-15T21:36:29.946228992Z` | `2026-04-15T18:25:00.050479343Z` to `2026-04-15T18:34:59.969469890Z` | `2026-04-15T18:25:00.050479343Z` to `2026-04-15T18:34:59.969469890Z` |
| `SPY-REAL-HISTORICAL-IDEAL-001` | `2026-05-13T10:30:00.610948896Z` to `2026-05-13T12:00:01.821339663Z` | `2026-05-13T10:30:00.610948896Z` to `2026-05-13T21:45:10.132742912Z` | `2026-05-13T15:25:00.028542412Z` to `2026-05-13T15:34:59.970415863Z` | `2026-05-13T15:25:00.028542412Z` to `2026-05-13T15:34:59.970415863Z` |
| `QQQ-REAL-HISTORICAL-CONTINUATION-001` | `2026-04-30T10:30:00.586838787Z` to `2026-04-30T12:00:00.833003922Z` | `2026-04-30T10:30:00.586838787Z` to `2026-04-30T21:36:39.224011567Z` | `2026-04-30T19:25:00.120340449Z` to `2026-04-30T19:34:59.970326860Z` | `2026-04-30T19:25:00.120340449Z` to `2026-04-30T19:34:59.970326860Z` |
| `QQQ-REAL-HISTORICAL-IDEAL-001` | `2026-05-13T10:30:00.615468990Z` to `2026-05-13T12:00:01.265122635Z` | `2026-05-13T10:30:00.615468990Z` to `2026-05-13T21:45:10.085346624Z` | `2026-05-13T16:25:00.020374358Z` to `2026-05-13T16:34:59.991346641Z` | `2026-05-13T16:25:00.020374358Z` to `2026-05-13T16:34:59.991346641Z` |
| `SPY-REAL-HISTORICAL-CONTINUATION-001` | `2026-04-30T10:30:00.578534719Z` to `2026-04-30T12:00:01.925903443Z` | `2026-04-30T10:30:00.578534719Z` to `2026-04-30T21:36:39.802166195Z` | `2026-04-30T16:25:00.068100758Z` to `2026-04-30T16:34:59.987370274Z` | `2026-04-30T16:25:00.068100758Z` to `2026-04-30T16:34:59.987370274Z` |

## Field Coverage

The starter files include the raw columns needed to attempt first-pass inspections:

- Definitions include `raw_symbol`, `instrument_id`, `underlying`, `expiration`, `strike_price`, `instrument_class`, and `security_update_action`.
- TCBBO includes `ts_event`, `instrument_id`, `bid_px_00`, `ask_px_00`, `bid_sz_00`, `ask_sz_00`, and `symbol`.
- Trades include `ts_event`, `instrument_id`, `price`, `size`, `sequence`, and `symbol`.
- Statistics includes `ts_event`, `instrument_id`, `stat_type`, `price`, `quantity`, `ts_ref`, and `symbol`.
- Statistics files include `stat_type=9` among the observed statistic types for every candidate.

## Starter-Only Usefulness

| Candidate | Option universe review | Setup-time quote freshness | Setup-time trade volume | Setup-time OI/statistics check | Starter-only next movement |
| --- | --- | --- | --- | --- | --- |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | Attemptable | Attemptable | Attemptable | Attemptable | Can move to starter-only option-data inspection after SPY CFB rule/regression authorization. |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | Attemptable | Attemptable | Attemptable | Attemptable | Can move to starter-only option-data inspection after SPY CFB rule/regression authorization. |
| `SPY-REAL-HISTORICAL-IDEAL-001` | Attemptable | Attemptable | Attemptable | Attemptable | Can move to starter-only option-data inspection after Ideal rule/regression authorization. |
| `QQQ-REAL-HISTORICAL-CONTINUATION-001` | Attemptable | Attemptable | Attemptable | Attemptable | Can move to starter-only option-data inspection after Continuation rule/evidence package authorization. |
| `QQQ-REAL-HISTORICAL-IDEAL-001` | Attemptable | Attemptable | Attemptable | Attemptable | Can move to starter-only option-data inspection after Ideal rule/evidence package authorization. |
| `SPY-REAL-HISTORICAL-CONTINUATION-001` | Attemptable | Attemptable | Attemptable | Attemptable | Can move to starter-only option-data inspection after Continuation rule/evidence package authorization. |

## Full-Window Data Likely Needed Later

The cheap starter data is enough for first-pass setup-window option inspection, not for full trade-plan proof. All six candidates likely need broader/full-window data later if the project authorizes:

- selected-contract quote path after the starter window;
- entry/fill/exit testing;
- invalidation or stop translation;
- time-exit or end-of-day handling;
- cost/slippage testing;
- backtest or sample-size validation;
- proof, profitability, readiness, or promotion review.

No full-window data was requested or downloaded in this task.

## Result

- Candidates that can move forward using starter data only for first-pass raw option inspection: all six listed candidates.
- Candidates that can be marked ready from starter data: none.
- Candidates with evidence filled from starter data: none.
- Candidates likely needing full-window data later for trade-plan proof: all six listed candidates.
- Safe-check command run: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`.
- Safe-check result: PASS, `3` checks.
