# SAFE-FAST Day 48 Grouped Positive-Entry Setup-Time Request Cost Check Result

## Baseline

- Current task file executed: `SAFE_FAST_DAY48_GROUPED_POSITIVE_ENTRY_SETUP_TIME_REQUEST_COST_CHECK_CODEX_TASK.md`.
- Baseline observed locally: branch `main`, HEAD `d1eb1e9`.
- Local git status before edits: `main...origin/main [ahead 226]`, with the existing permission warnings for temp directories `tmp2i57tguu`, `tmpj8ei9a_f`, `tmpra392qh0`, and `tmpt2fw63vq`.
- Required startup files were read before action:
  - `SAFE_FAST_BUILD_STATE.md`
  - `SAFE_FAST_DAY48_GROUPED_POSITIVE_ENTRY_EXPANSION_RESULT.md`
  - `historical_signal_replay/source_data/richer_export_package_work/day48_grouped_positive_entry_setup_time_request_manifest.json`
  - `SAFE_FAST_DAY48_POSITIVE_TRADE_CAPTURE_AND_MISS_ANALYSIS_RESULT.md`
  - `historical_signal_replay/results/day48_positive_trade_capture_funnel.json`
  - `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`
  - `SAFE_FAST_PROJECT_DASHBOARD.md`
  - `SAFE_FAST_PROJECT_RULE_INDEX.md`

## Manifest Validation

- Manifest path: `historical_signal_replay/source_data/richer_export_package_work/day48_grouped_positive_entry_setup_time_request_manifest.json`.
- Manifest validation result: `PASS`.
- Request count: `4`.
- All requests are setup-time-only: `YES`.
- Conditional exit-path requests present: `NO`.
- Scope controls preserved:
  - QQQ, GLD, IWM requests: `NO`.
  - Alternate contracts or expirations: `NO`.
  - Broader symbols or broader windows: `NO`.
  - Statistics or definitions requests: `NO`.
  - Conditional exit-path requests: `NO`.

## Credential And Tooling Availability

- `SAFE_FAST_DB_AUTH`: present.
- Internal `DATABENTO_API_KEY` mapping for this run: used in-process only from `SAFE_FAST_DB_AUTH`.
- `DATABENTO_API_KEY` original environment variable: not present before the in-process mapping.
- Local `databento` Python package: available.
- Safe cost-check path: available via Databento `metadata.get_cost`.
- Credential value printed, logged, documented, or saved: `NO`.

## Cost Check Result

Vendor metadata/cost request made: `YES`.

No data download was requested or performed. Only Databento metadata cost estimates were requested.

| Request | Schema | Raw symbol | UTC start | UTC end | Checked cost |
| --- | --- | --- | --- | --- | ---: |
| `SPY-REAL-HISTORICAL-IDEAL-001-SETUP-TCBBO-RAW-SYMBOL-OPEN-TO-SIGNAL` | `tcbbo` | `SPY   260527C00745000` | `2026-05-13T13:30:00Z` | `2026-05-13T15:30:00Z` | `$0.000344216824` |
| `SPY-REAL-HISTORICAL-IDEAL-001-SETUP-TRADES-RAW-SYMBOL-OPEN-TO-SIGNAL` | `trades` | `SPY   260527C00745000` | `2026-05-13T13:30:00Z` | `2026-05-13T15:30:00Z` | `$0.000275373459` |
| `SPY-REAL-HISTORICAL-CONTINUATION-001-SETUP-TCBBO-RAW-SYMBOL-OPEN-TO-SIGNAL` | `tcbbo` | `SPY   260514C00720000` | `2026-04-30T13:30:00Z` | `2026-04-30T16:30:00Z` | `$0.000125169754` |
| `SPY-REAL-HISTORICAL-CONTINUATION-001-SETUP-TRADES-RAW-SYMBOL-OPEN-TO-SIGNAL` | `trades` | `SPY   260514C00720000` | `2026-04-30T13:30:00Z` | `2026-04-30T16:30:00Z` | `$0.000100135803` |

Grouped checked total: `$0.000844895840`.

Schema subtotals:

| Schema | Checked cost |
| --- | ---: |
| `tcbbo` | `$0.000469386578` |
| `trades` | `$0.000375509262` |

Candidate subtotals:

| Candidate | Checked cost |
| --- | ---: |
| `SPY-REAL-HISTORICAL-IDEAL-001` | `$0.000619590283` |
| `SPY-REAL-HISTORICAL-CONTINUATION-001` | `$0.000225305557` |

## No-Download And Approval Boundary

- Databento downloaded: `NO`.
- Raw vendor data changed: `NO`.
- Positive-trade funnel artifact changed: `NO`.
- Download authorized: `NO`.
- Purchase approval inferred: `NO`.
- Download approval inferred: `NO`.
- Download task created: `NO`.
- Repair task created: `NO`.

## Final State

- New backtest run: `NO`.
- New P&L calculated: `NO`.
- Promotion decision made: `NO`.
- Real trade chosen: `NO`.
- Candidate marked ready: `NO`.
- Intake-ready count changed: `NO`.
- Proof accepted: `NO`.
- Profitability claim made: `NO`.
- No `main.py`, live/engine trading logic, Railway/deploy files, broker/order/account files, `.env`, secrets, raw vendor data, evidence fills, trade-selection code, P&L files, or generated live reports/logs were changed.

## Checks Run

- `.\scripts\safe_fast_run_safe_checks.ps1`: BLOCKED by local PowerShell execution policy before the script ran.
- `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`: PASS, `3` checks plus `9` discovered tests.
- `python -B -m unittest discover -s tests -p "test_day48_positive_trade_capture_funnel.py"`: PASS, `4` tests.
- `python -B -m watcher_foundation.day48_positive_trade_capture_funnel_validator`: PASS.
- `python -B -m watcher_foundation.source_evidence_work_package_content_validator`: PASS, `9` passed requests, `0` failed requests, intake-ready `0`.
- `python -B -m watcher_foundation.source_evidence_package_to_intake_bridge`: PASS, `4` reconsideration-eligible candidates, intake-ready `0`, proof allowed `NO`.
- Bounded `__pycache__` cleanup command over `tests`, `watcher_foundation`, `historical_signal_replay`, and `replay`: BLOCKED by local command policy before it ran.
- Bounded `__pycache__` inspection over `tests`, `watcher_foundation`, `historical_signal_replay`, and `replay`: PASS, `0` directories found.
- `git --no-pager diff --check`: PASS.

## Next

The grouped setup-time request package has a checked cost, but this task does not authorize purchase or download. Stop here unless a later explicit task approves a download for the exact checked request scope.
