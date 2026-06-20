# SAFE-FAST Day 49 Grouped Positive-Entry Setup-Time Download and Replay Result

## Baseline

- Current task file executed: `SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_SETUP_TIME_DOWNLOAD_AND_REPLAY_CODEX_TASK.md`.
- Baseline observed locally: branch `main`, HEAD `55527f0`.
- Local status before edits: expected untracked Day 49 task file only, plus known permission warnings for temp directories `tmp2i57tguu`, `tmpj8ei9a_f`, `tmpra392qh0`, and `tmpt2fw63vq`.
- This was SAFE-FAST build testing, not live trading.
- `SAFE_FAST_DB_AUTH` was used only in-process as the Databento credential. The credential was not printed, logged, documented, saved, or written to any file.

## Authorization And Cost

- Approved package: `historical_signal_replay/source_data/richer_export_package_work/day48_grouped_positive_entry_setup_time_request_manifest.json`.
- Manifest SHA-256 confirmed unchanged: `213dc93d2c08cd0653a78eb64c002b57673ab48a8a4f4b5ee727ff0c77b0f2bf`.
- Request count: `4`.
- Setup-time-only requests: `YES`.
- Exit-path requests downloaded: `NO`.
- Fresh checked total: `$0.000844895840`.
- Fresh checked total at or below `$0.01`: `YES`.
- Actual billed cost: `NOT_AVAILABLE`.

## Downloaded Raw Files

Raw files were stored only under the canonical ignored local data directory:

`historical_signal_replay/source_data/external_option_data_drop/`

Ignored raw files downloaded:

| Candidate | Schema | Raw symbol | UTC window | CSV rows | DBN bytes | DBN SHA-256 | Checked cost | Actual billed |
| --- | --- | --- | --- | ---: | ---: | --- | ---: | --- |
| `SPY-REAL-HISTORICAL-IDEAL-001` | `tcbbo` | `SPY   260527C00745000` | `2026-05-13T13:30:00Z` to `2026-05-13T15:30:00Z` | `22` | `1025` | `bbd161491628183d47dc8d6f471e07adc7b940563dc4ed5b0c5b72b28d407205` | `$0.000344216824` | `NOT_AVAILABLE` |
| `SPY-REAL-HISTORICAL-IDEAL-001` | `trades` | `SPY   260527C00745000` | `2026-05-13T13:30:00Z` to `2026-05-13T15:30:00Z` | `22` | `724` | `eaf0cd5113f22549c46f340f78eef1d7124d9a060a8cabcf0df56c2520dc2d80` | `$0.000275373459` | `NOT_AVAILABLE` |
| `SPY-REAL-HISTORICAL-CONTINUATION-001` | `tcbbo` | `SPY   260514C00720000` | `2026-04-30T13:30:00Z` to `2026-04-30T16:30:00Z` | `8` | `519` | `e4bfd3d341ccb83475b098b20fc058fdb64b09af2c76ab2476d6df048fab35c5` | `$0.000125169754` | `NOT_AVAILABLE` |
| `SPY-REAL-HISTORICAL-CONTINUATION-001` | `trades` | `SPY   260514C00720000` | `2026-04-30T13:30:00Z` to `2026-04-30T16:30:00Z` | `8` | `389` | `24c07ad8922318a248fe4148c60e49f71d822be4d7b606b4a519aa48b3b9b35e` | `$0.000100135803` | `NOT_AVAILABLE` |

Downloaded-file validation result: `PASS`; no empty, malformed, late, stale-window, or contradictory-symbol file problem was found. The ignored local download manifest is `historical_signal_replay/source_data/external_option_data_drop/SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_SETUP_TIME_DOWNLOAD_MANIFEST.json`.

## Replay Result

The complete grouped positive-trade funnel was rerun twice after validation. Both runs were deterministic:

- First run equals second run: `YES`.
- Hashes match: `YES`.
- Deterministic comparison: `PASS`.

Affected candidates:

| Candidate | Highest stage reached | First stage not reached | Exact blocker | Contract selection | Price acceptability | Entry eligibility | Entry recorded | Final classification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `second_real_spy_ideal_replay_v1_fixture` / `SPY-REAL-HISTORICAL-IDEAL-001` | `PRICE_ACCEPTABLE` | `ENTRY_ELIGIBLE` | `quote_age_above_5_minutes` | selected `SPY   260527C00745000` | `fail`, quote age `442.633927` seconds | blocked | not recorded | `TRUE_NO_TRADE` |
| `first_real_spy_continuation_replay_v1_fixture` / `SPY-REAL-HISTORICAL-CONTINUATION-001` | `PRICE_ACCEPTABLE` | `ENTRY_ELIGIBLE` | `quote_age_above_5_minutes` | selected `SPY   260514C00720000` | `fail`, quote age `3790.746258` seconds | blocked | not recorded | `TRUE_NO_TRADE` |

Exact missing-data cases changed:

- `second_real_spy_ideal_replay_v1_fixture`: changed from `MISSING_DATA` at `CONTRACT_SELECTED` / `missing_setup_time_selected_option_evidence` to `TRUE_NO_TRADE` at `ENTRY_ELIGIBLE` / `quote_age_above_5_minutes`.
- `first_real_spy_continuation_replay_v1_fixture`: changed from `MISSING_DATA` at `CONTRACT_SELECTED` / `missing_setup_time_selected_option_evidence` to `TRUE_NO_TRADE` at `ENTRY_ELIGIBLE` / `quote_age_above_5_minutes`.

No candidate changed to valid trade captured. No missed valid trade or invalid allowed trade was found. No exit path was downloaded, no P&L was calculated, and no winner or loser was added.

## Funnel Totals

| Metric | Before | After |
| --- | ---: | ---: |
| Valid trades captured | `1` | `1` |
| True no-trades | `2` | `4` |
| Missing-data cases | `8` | `6` |
| Missed valid trades | `0` | `0` |
| Invalid trades allowed | `0` | `0` |
| Unresolved cases | `4` | `4` |
| Winners | `1` | `1` |
| Losers | `0` | `0` |

First blocker by funnel stage:

| Stage | Before | After |
| --- | ---: | ---: |
| `SETUP_QUALIFIED` | `2` | `2` |
| `TRADE_CANDIDATE` | `4` | `4` |
| `CONTRACT_SELECTED` | `6` | `4` |
| `ENTRY_ELIGIBLE` | `2` | `4` |
| `NONE` | `1` | `1` |

After family totals:

| Family | Valid captured | True no-trades | Missing data | Missed valid | Invalid allowed | Unresolved | Winners | Losers |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Ideal | `0` | `1` | `1` | `0` | `0` | `2` | `0` | `0` |
| Clean Fast Break | `1` | `2` | `3` | `0` | `0` | `1` | `1` | `0` |
| Continuation | `0` | `1` | `2` | `0` | `0` | `1` | `0` | `0` |
| Combined | `1` | `4` | `6` | `0` | `0` | `4` | `1` | `0` |

## Five Owner Questions

1. Did SAFE-FAST recognize the setup before the move?
   - Yes for the grouped lifecycle candidates that reached setup or trade-candidate stages; recognition remains incomplete for shape-only and remaining missing-data rows.
2. Did it classify it as a possible trade?
   - Yes for accepted-entry-stage lifecycle rows and the three CFB selected-contract replay rows. Day 49 moved SPY Ideal 001 and SPY Continuation 001 through selected-contract evidence, but both stopped at entry eligibility.
3. Was a tradable option available at that exact time?
   - No countable tradable entry was available for the two newly downloaded cases because both selected-contract quotes were older than the frozen five-minute quote-age gate. SPY CFB 002 remains the only review-only captured valid entry with local entry and exit evidence.
4. Was rejection caused by a real safety rule or missing evidence?
   - Both remain present overall. The two Day 49 changed cases are real safety-rule rejections from `quote_age_above_5_minutes`; six cases still remain missing-data blockers and four remain unresolved.
5. How many valid trades were caught, missed, or incorrectly allowed?
   - Caught `1`; missed `0`; incorrectly allowed `0`.

## Final State

- Databento downloaded: `YES`, only the four authorized setup-time requests.
- Exit-path downloaded: `NO`.
- Raw vendor data changed: `YES`, ignored local raw DBN/CSV files only.
- Positive-trade funnel artifact updated: `YES`.
- New backtest run: grouped positive-trade funnel rerun only; no new exit/P&L backtest.
- New P&L calculated: `NO`.
- Promotion decision made: `NO`.
- Real trade chosen: `NO`.
- Candidate marked ready: `NO`.
- Intake-ready count changed: `NO`.
- Proof accepted: `NO`.
- Profitability claim made: `NO`.

Exact next grouped task:

`SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_EXPANSION_AFTER_SETUP_DOWNLOAD_CODEX_TASK.md`

## Checks Run

- `.\scripts\safe_fast_run_safe_checks.ps1`: BLOCKED by local PowerShell execution policy before the script ran.
- `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`: PASS, `3` checks plus `9` discovered tests.
- `python -B -m historical_signal_replay.day49_grouped_positive_entry_setup_time`: PASS, downloaded `4` setup-time requests at fresh checked total `$0.000844895840`.
- `python -B -m historical_signal_replay.day48_positive_trade_capture_funnel`: PASS twice after validation, wrote `15` candidates, `1` valid captured, `4` true no-trades, `6` missing-data cases.
- `python -B -m watcher_foundation.day48_positive_trade_capture_funnel_validator`: PASS.
- `python -B -m unittest discover -s tests -p "test_day49_grouped_positive_entry_setup_time.py"`: PASS, `2` tests.
- `python -B -m unittest discover -s tests -p "test_day48_positive_trade_capture_funnel.py"`: PASS, `4` tests.
- `python -B -m unittest discover -s tests -p "test_day48_positive_trade_handoff_consistency.py"`: PASS, `3` tests.
- `python -B -m unittest discover -s tests -p "test_day48_actual_grouped_three_family_replay.py"`: PASS, `2` tests.
- `python -B -m unittest discover -s tests -p "test_day48_grouped_three_family_coverage_expansion.py"`: PASS, `3` tests.
- `python -B -m unittest discover -s tests -p "test_day48_continuation_starter_coverage.py"`: PASS, `3` tests.
- `python -B -m unittest discover -s tests -p "test_day48_grouped_three_family_expansion_after_continuation.py"`: PASS, `3` tests.
- `python -B -m unittest discover -s tests -p "test_cfb_backtest_runner.py"`: PASS, `8` tests.
- `python -B -m unittest discover -s tests -p "test_cfb_contract_selector.py"`: PASS, `17` tests.
- `python -B -m unittest discover -s tests -p "test_execution_context_calculator.py"`: PASS, `10` tests.
- `python -B -m unittest discover -s tests -p "test_context_caution_calculator.py"`: PASS, `12` tests.
- `python -B -m unittest discover -s tests -p "test_watcher_stable_winner_selection_replay.py"`: PASS, `8` tests.
- Direct script execution for `replay/test_on_demand_*ideal*.py`: PASS, `3` files.
- Direct script execution for `replay/test_on_demand_*clean_fast_break*.py`: PASS, `3` files.
- Direct script execution for `replay/test_on_demand_*continuation*.py`: PASS, `6` files.
- Direct script execution for `replay/test_on_demand_*stage*.py`: PASS, `6` files.
- Direct script execution for `replay/test_on_demand_session_boundary*.py`: PASS, `5` files.
- `python -B .\replay\test_on_demand_winner_selection_contract.py`: PASS.
- `python -B .\historical_signal_replay\run_signal_replay.py`: PASS.
- `python -B -m watcher_foundation.source_evidence_work_package_content_validator`: PASS, `9` passed requests, `0` failed requests, intake-ready `0`.
- `python -B -m watcher_foundation.source_evidence_package_to_intake_bridge`: PASS, `4` reconsideration-eligible candidates, intake-ready `0`, proof allowed `NO`.
- `python -B -m unittest discover -s tests -p "test_day47_to_day90_audit_consistency.py"`: PASS, `2` tests.
- Bounded `__pycache__` cleanup over `tests`, `watcher_foundation`, `historical_signal_replay`, and `replay`: PowerShell cleanup BLOCKED by local command policy; Python fallback cleanup removed generated `historical_signal_replay\__pycache__`; final inspection found `0` generated cache directories.
- `git --no-pager diff --check`: PASS with line-ending warnings only.
