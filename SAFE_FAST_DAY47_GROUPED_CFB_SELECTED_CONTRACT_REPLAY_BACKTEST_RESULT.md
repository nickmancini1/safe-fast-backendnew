# SAFE-FAST Day 47 Grouped CFB Selected-Contract Replay Backtest Result

## Baseline

- Task file executed: `SAFE_FAST_DAY47_GROUPED_CFB_SELECTED_CONTRACT_REPLAY_BACKTEST_CODEX_TASK.md`.
- Starting branch observed locally: `main`.
- Starting HEAD observed locally: `723bce7 Record Day 47 grouped selected-contract evidence download`.
- Download-result baseline recorded by the task path: `5a818d8`.
- Required raw manifest read: `historical_signal_replay/source_data/external_option_data_drop/SPY_CFB_003_selected_contract_download_manifest.json`.
- Replay target: `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`.
- Grouped anchors preserved:
  - `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` remains the positive review-only anchor.
  - `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` is the selected-contract replay row under review.
  - `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` remains the stale-quote no-entry control.

## Raw Evidence Used

All raw files remain local-only and ignored.

| File | Role in this replay | Manifest rows | Replay use |
| --- | --- | ---: | --- |
| `historical_signal_replay/source_data/external_option_data_drop/SPY_CFB_003_selected_contract_tcbbo_open_to_signal.csv` | selected-contract setup-window quotes | 77 | Used to find the nearest setup-time-safe quote |
| `historical_signal_replay/source_data/external_option_data_drop/SPY_CFB_003_selected_contract_trades_open_to_signal.csv` | selected-contract setup-window trades | 77 | Inspected for setup-window support; not used as an entry fill |
| `historical_signal_replay/source_data/external_option_data_drop/SPY_CFB_003_selected_contract_statistics_signal_day.csv` | signal-day statistics/open-interest diagnosis | 88 | Inspected; no setup-time-safe statistics rows before the signal |
| `historical_signal_replay/source_data/external_option_data_drop/SPY_CFB_003_selected_contract_tcbbo_signal_to_1545_et.csv` | conditional exit-path quotes | 25 | Not used because no valid entry was found |
| `historical_signal_replay/source_data/external_option_data_drop/SPY_CFB_003_selected_contract_trades_signal_to_1545_et.csv` | conditional exit-path trades | 25 | Not used because no valid entry was found |

Validation facts preserved:

- Request shape used `raw_symbol=SPY   260429C00700000`.
- The failed local `instrument_id=1333784938` request was not substituted.
- Downloaded row-level Databento `instrument_id=1258293278` was used for the selected-contract evidence.
- Setup-window files and conditional exit-path files remained separate.

## Replay Result

The downloaded setup-window evidence changes the old `quote_after_signal` diagnosis for `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`.

- Prior starter quote: `2026-04-15T18:31:23.366609701Z`, after the `2026-04-15T18:30:00Z` signal.
- Downloaded setup-window nearest quote at or before signal: `2026-04-15T18:22:33.366710979Z`.
- Quote age at signal: about `446.633289` seconds, or about `7m 26.6s`.
- Quote fields: bid `7.63`, ask `7.66`, bid size `88`, ask size `40`.
- Accepted CFB quote-age gate: selected quotes older than `5` minutes are no-trade.
- New replay result for CFB 003: `no_trade_quote_age_above_5_minutes`.
- Valid entry under accepted CFB rules: NO.
- Conditional exit-path data used: NO, because entry remained invalid.

Grouped replay output:

| Candidate | Group role | Replay state | Primary reason | Entry/exit handling |
| --- | --- | --- | --- | --- |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | positive review-only anchor | `completed_review_only` / `completed_profit_target` | existing anchor result preserved | Existing entry `6.37`, adjusted exit `7.98`, adjusted result `+1.61`; not proof |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | selected-contract row under review | `no_trade` | `quote_age_above_5_minutes` | No valid entry; no exit-path replay |
| `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | stale-quote no-entry control | `no_trade` | `quote_age_above_5_minutes` | Existing stale-quote control preserved |

## Code/Test Change

- `historical_signal_replay/cfb_backtest_runner.py` now has a Day 47 replay helper that applies only the downloaded `SPY_CFB_003_selected_contract_tcbbo_open_to_signal.csv` setup-window quote evidence for CFB 003.
- Existing Day 46 runner behavior remains available separately.
- `tests/test_cfb_backtest_runner.py` covers the downloaded CFB 003 setup quote and verifies the changed blocker is `quote_age_above_5_minutes`, not `quote_after_signal`.

## Guardrails

- Databento downloaded: NO.
- More Databento data requested: NO.
- Raw Databento files changed: NO.
- `main.py` changed: NO.
- Railway/deploy, production, broker, order, account, credentials, `.env`, secrets, and live trading logic changed: NO.
- New proof accepted: NO.
- Profitability claimed: NO.
- Candidate marked ready: NO.
- Promotion decision made: NO.
- Intake-ready count changed: NO.
- Real trade chosen: NO.

## Tests

- `.\scripts\safe_fast_run_safe_checks.ps1`: BLOCKED by local PowerShell execution policy before the script ran.
- `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`: PASS, `3` checks.
- `python -m watcher_foundation.source_evidence_work_package_content_validator`: PASS, `9` passed requests, `0` failed requests, intake-ready `0`.
- `python -m watcher_foundation.source_evidence_package_to_intake_bridge`: PASS, `4` reconsideration-eligible candidates, intake-ready `0`, proof allowed `NO`.
- `python -m unittest discover -s tests -p "test_cfb_backtest_runner.py"`: PASS, `8` tests.
- `git --no-pager diff --check`: PASS with line-ending warnings only.

## Next

The mandatory queued audit remains next:

`SAFE_FAST_DAY47_TO_DAY90_CONSOLIDATED_AUDIT_AND_COMPLETION_PLAN_CODEX_TASK.md`
