# SAFE-FAST Day 48 Grouped Positive-Entry Expansion Result

## Baseline

- Current task file executed: `SAFE_FAST_DAY48_GROUPED_POSITIVE_ENTRY_EXPANSION_CODEX_TASK.md`.
- Baseline observed locally: branch `main`, HEAD `c287eae`.
- Local status before edits: clean except the known permission warnings for temp directories `tmp2i57tguu`, `tmpj8ei9a_f`, `tmpra392qh0`, and `tmpt2fw63vq`.
- This was grouped SAFE-FAST build testing and measurement, not live trade evaluation.
- No data was downloaded.
- No `main.py`, live/engine trading logic, Railway/deploy files, broker/order/account files, `.env`, secrets, raw vendor data, evidence fills, trade-selection code, P&L files, or generated live reports/logs were changed.

## Output Created

- Result document: `SAFE_FAST_DAY48_GROUPED_POSITIVE_ENTRY_EXPANSION_RESULT.md`.
- Setup-time-only missing-data request package: `historical_signal_replay/source_data/richer_export_package_work/day48_grouped_positive_entry_setup_time_request_manifest.json`.
- Exact next cost-check task: `SAFE_FAST_DAY48_GROUPED_POSITIVE_ENTRY_SETUP_TIME_REQUEST_COST_CHECK_CODEX_TASK.md`.

The machine-readable funnel artifact was rerun and validated, but not intentionally updated because no case was added or reclassified.

## Local Inventory Result

Existing local evidence did not add a new grouped positive-entry case.

- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` remains the current review-only captured valid-entry reference.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` reruns as a true no-trade from `quote_age_above_5_minutes`.
- `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` reruns as a true no-trade from `quote_age_above_5_minutes`.
- QQQ Continuation has local setup-time top-contract evidence, but the spread is `0.35`, above the accepted gate; no fallback is allowed.
- SPY Continuation has only a post-signal top-contract quote locally; setup-time TCBBO/trades remain missing.
- SPY Ideal has only post-signal top-contract starter rows locally; setup-time TCBBO/trades remain missing.
- QQQ Ideal, GLD, and IWM rows are not exact request candidates for this package because setup/rule prerequisites are missing or unresolved before selected-option evidence can be safely requested.

## Before Scorecards

| Scorecard | Found | Runnable | Setup developing | Setup qualified | Trade candidate | Contracts selected | Prices accepted | Entries eligible | Entries recorded | Exits evaluated | Valid trades captured | True no-trades | Missing data | Missed valid trades | Invalid trades allowed | Unresolved | Winners | Losers | Deterministic | Unstable |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Ideal | 4 | 4 | 4 | 4 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 2 | 0 | 0 | 4 | 0 |
| Clean Fast Break | 7 | 7 | 7 | 6 | 5 | 3 | 3 | 1 | 1 | 1 | 1 | 2 | 3 | 0 | 0 | 1 | 1 | 0 | 7 | 0 |
| Continuation | 4 | 4 | 4 | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 1 | 0 | 0 | 4 | 0 |
| Combined | 15 | 15 | 15 | 13 | 9 | 3 | 3 | 1 | 1 | 1 | 1 | 2 | 8 | 0 | 0 | 4 | 1 | 0 | 15 | 0 |

## After Scorecards

| Scorecard | Found | Runnable | Setup developing | Setup qualified | Trade candidate | Contracts selected | Prices accepted | Entries eligible | Entries recorded | Exits evaluated | Valid trades captured | True no-trades | Missing data | Missed valid trades | Invalid trades allowed | Unresolved | Winners | Losers | Deterministic | Unstable |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Ideal | 4 | 4 | 4 | 4 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 2 | 0 | 0 | 4 | 0 |
| Clean Fast Break | 7 | 7 | 7 | 6 | 5 | 3 | 3 | 1 | 1 | 1 | 1 | 2 | 3 | 0 | 0 | 1 | 1 | 0 | 7 | 0 |
| Continuation | 4 | 4 | 4 | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 1 | 0 | 0 | 4 | 0 |
| Combined | 15 | 15 | 15 | 13 | 9 | 3 | 3 | 1 | 1 | 1 | 1 | 2 | 8 | 0 | 0 | 4 | 1 | 0 | 15 | 0 |

## Funnel Totals

| Metric | Before | After |
| --- | ---: | ---: |
| Valid trades captured | 1 | 1 |
| True no-trades | 2 | 2 |
| Missing-data cases | 8 | 8 |
| Missed valid trades | 0 | 0 |
| Invalid trades allowed | 0 | 0 |
| Unresolved cases | 4 | 4 |
| Winners | 1 | 1 |
| Losers | 0 | 0 |

## First Blockers By Stage

| First blocker stage | Count | Families affected | Common cause | Local evidence can resolve? | External data required? | Smallest safe next action |
| --- | ---: | --- | --- | --- | --- | --- |
| `SETUP_QUALIFIED` | 2 | Continuation, Clean Fast Break | spent/freshness not proven enough for qualification | no | no | Add grouped local fixture evidence before any data request. |
| `TRADE_CANDIDATE` | 4 | Clean Fast Break, Ideal, Continuation | fresh/spent or pending status unresolved | no | no | Add grouped local fixture evidence before any data request. |
| `CONTRACT_SELECTED` | 6 | Clean Fast Break, Ideal, Continuation | missing setup-time selected-option evidence | no for current local evidence | yes for exact SPY Ideal and SPY Continuation setup-time rows | Cost-check the setup-time-only request package; do not request exit paths until a valid entry exists. |
| `ENTRY_ELIGIBLE` | 2 | Clean Fast Break | `quote_age_above_5_minutes` | yes | no | Preserve frozen quote-age rejection controls in regression. |
| none | 1 | Clean Fast Break | completed review-only valid entry | n/a | no | Keep SPY CFB 002 as review-only positive-entry reference; do not claim proof. |

## Request Package

Because no additional local positive-entry expansion was possible, the smallest exact grouped missing-data request package was created for setup-time fields only:

`historical_signal_replay/source_data/richer_export_package_work/day48_grouped_positive_entry_setup_time_request_manifest.json`

Included requests:

- SPY Ideal 001 top-ranked raw symbol `SPY   260527C00745000`, `tcbbo`, open through signal.
- SPY Ideal 001 top-ranked raw symbol `SPY   260527C00745000`, `trades`, open through signal.
- SPY Continuation 001 top-ranked raw symbol `SPY   260514C00720000`, `tcbbo`, open through signal.
- SPY Continuation 001 top-ranked raw symbol `SPY   260514C00720000`, `trades`, open through signal.

Not included: conditional exit-path evidence, QQQ Continuation, QQQ Ideal, GLD, IWM, alternate contracts, broader symbols, broader windows, definitions, statistics, cost check, or download.

## Five Owner Questions

1. Did SAFE-FAST recognize the setup before the move?
   - Yes for grouped lifecycle candidates that reached setup or trade-candidate stages. Recognition remains incomplete for shape-only and missing-data rows.
2. Did it classify the setup as a possible trade?
   - Yes for accepted-entry-stage lifecycle rows and the three CFB selected-contract replay rows. Accepted-entry stage is not an executed trade.
3. Was a tradable option available at that exact time?
   - Only `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` currently has local selected-contract entry and exit evidence sufficient for a review-only captured valid entry. SPY Ideal and SPY Continuation need setup-time selected raw-symbol quote/trade evidence; QQQ Continuation fails spread locally; the two CFB controls fail quote age.
4. Was rejection caused by a real safety rule or missing evidence?
   - Both. Two CFB controls are true no-trades from the frozen quote-age safety rule. Eight cases remain missing-data blockers. Four remain unresolved and separate.
5. How many valid trades were caught, missed, or incorrectly allowed?
   - Caught `1`; missed `0`; incorrectly allowed `0`.

## Checks Run

- `.\scripts\safe_fast_run_safe_checks.ps1`: BLOCKED by local PowerShell execution policy before the script ran.
- `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`: PASS, `3` checks plus `9` discovered tests.
- `python -B -m historical_signal_replay.day48_positive_trade_capture_funnel`: PASS, wrote `15` candidates, `1` valid captured, `2` true no-trades, `8` missing-data cases.
- `python -B -m watcher_foundation.day48_positive_trade_capture_funnel_validator`: PASS.
- `python -B -m unittest discover -s tests -p "test_day48_positive_trade_capture_funnel.py"`: PASS, `4` tests.
- `python -B -m unittest discover -s tests -p "test_cfb_backtest_runner.py"`: PASS, `8` tests.
- Direct script execution for `replay/test_on_demand_*ideal*.py`: PASS, `3` files.
- Direct script execution for `replay/test_on_demand_*clean_fast_break*.py`: PASS, `3` files.
- Direct script execution for `replay/test_on_demand_*continuation*.py`: PASS, `6` files.
- `python -B -m unittest discover -s tests -p "test_day48_actual_grouped_three_family_replay.py"`: PASS, `2` tests.
- `python -B -m unittest discover -s tests -p "test_day48_grouped_three_family_coverage_expansion.py"`: PASS, `3` tests.
- `python -B -m unittest discover -s tests -p "test_day48_continuation_starter_coverage.py"`: PASS, `3` tests.
- `python -B -m unittest discover -s tests -p "test_day48_grouped_three_family_expansion_after_continuation.py"`: PASS, `3` tests.
- Direct script execution for `replay/test_on_demand_*stage*.py`: PASS, `6` files.
- Direct script execution for `replay/test_on_demand_session_boundary*.py`: PASS, `5` files.
- `python -B -m unittest discover -s tests -p "test_cfb_contract_selector.py"`: PASS, `17` tests.
- `python -B -m unittest discover -s tests -p "test_execution_context_calculator.py"`: PASS, `10` tests.
- `python -B -m unittest discover -s tests -p "test_context_caution_calculator.py"`: PASS, `12` tests.
- `python -B -m unittest discover -s tests -p "test_watcher_stable_winner_selection_replay.py"`: PASS, `8` tests.
- `python -B -m watcher_foundation.source_evidence_work_package_content_validator`: PASS, `9` passed requests, `0` failed requests, intake-ready `0`.
- `python -B -m watcher_foundation.source_evidence_package_to_intake_bridge`: PASS, `4` reconsideration-eligible candidates, intake-ready `0`, proof allowed `NO`.
- `python -m json.tool historical_signal_replay/source_data/richer_export_package_work/day48_grouped_positive_entry_setup_time_request_manifest.json`: PASS.
- Bounded `__pycache__` cleanup over `tests`, `watcher_foundation`, `historical_signal_replay`, and `replay`: BLOCKED by local command policy before it ran.
- Bounded `__pycache__` inspection over `tests`, `watcher_foundation`, `historical_signal_replay`, and `replay`: PASS, `0` directories found.
- `git --no-pager diff --check`: PASS with the existing line-ending warning for `historical_signal_replay/results/day48_positive_trade_capture_funnel.json`.

## Final Status

- Databento downloaded: NO.
- New backtest run: NO.
- New P&L calculated: NO.
- Promotion decision made: NO.
- Real trade chosen: NO.
- Candidate marked ready: NO.
- Intake-ready count changed: NO.
- Proof accepted: NO.
- Profitability claim made: NO.

Exact next grouped task:

`SAFE_FAST_DAY48_GROUPED_POSITIVE_ENTRY_SETUP_TIME_REQUEST_COST_CHECK_CODEX_TASK.md`
