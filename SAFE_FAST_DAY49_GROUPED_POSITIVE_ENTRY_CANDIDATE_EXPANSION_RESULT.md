# SAFE-FAST Day 49 Grouped Positive-Entry Candidate Expansion Result

## Baseline

- Current task file executed: `SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_CANDIDATE_EXPANSION_CODEX_TASK.md`.
- Baseline observed locally: branch `main`, HEAD `46ab96e`, with only the untracked task file and known temp-directory permission warnings.
- This was SAFE-FAST build testing, not live trading.
- No production/live backend, `main.py`, Railway/deploy, broker, account, order, credential, `.env`, frozen trading-rule, accepted-threshold, raw vendor, or exit-path files were modified.
- No Databento data was downloaded. No purchase approval was inferred.

## Output Created

- Frozen development manifest: `historical_signal_replay/fixtures/day49_positive_entry_candidate_expansion_manifest.json`.
- Machine-readable expansion result: `historical_signal_replay/results/day49_positive_entry_candidate_expansion.json`.
- Expansion builder: `historical_signal_replay/day49_positive_entry_candidate_expansion.py`.
- Focused validator: `watcher_foundation/day49_positive_entry_candidate_expansion_validator.py`.
- Focused tests: `tests/test_day49_positive_entry_candidate_expansion.py`.
- Exact next grouped task: `SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_SETUP_FIELD_COMPLETION_CODEX_TASK.md`.

## Candidate Freeze

The selection used the existing 24-row local candidate completeness screen as the pre-outcome source universe. Existing measured 15-candidate funnel controls, current positive/rejection controls, duplicate source-window rows, dropped rows, and protected holdout rows were excluded before selection.

Frozen new development candidates:

| Family | Candidate count | Candidate ids |
| --- | ---: | --- |
| Ideal | `2` | `GLD-REPLACEMENT-IDEAL-CANDIDATE-001`, `GLD-REPLACEMENT-IDEAL-CANDIDATE-002` |
| Clean Fast Break | `1` | `SPY-SOURCE-WINDOW-CLEAN-FAST-BREAK-003` |
| Continuation | `5` | `IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001`, `IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002`, `SPY-SOURCE-WINDOW-CONTINUATION-004`, `QQQ-SOURCE-WINDOW-CONTINUATION-002`, `SPY-SOURCE-WINDOW-CONTINUATION-005` |
| Combined | `8` | all selected candidates above |

Selection was deterministic and outcome-blind:

- Deterministic selection result: `PASS`.
- First run hash equals second run hash: `YES`.
- Protected holdout candidates selected: `0`.
- Outcome/profit fields were not used for selection.

## New-Candidate Funnel Totals

| Scorecard | Found | Runnable | Setup developing | Setup qualified | Trade candidate | Contracts selected | Prices accepted | Entries eligible | Entries recorded | Exits evaluated | Valid captured | True no-trades | Missing data | Missed valid | Invalid allowed | Unresolved | Winners | Losers | Stable | Unstable |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Ideal | `2` | `2` | `2` | `0` | `0` | `0` | `0` | `0` | `0` | `0` | `0` | `0` | `2` | `0` | `0` | `0` | `0` | `0` | `2` | `0` |
| Clean Fast Break | `1` | `1` | `1` | `0` | `0` | `0` | `0` | `0` | `0` | `0` | `0` | `0` | `1` | `0` | `0` | `0` | `0` | `0` | `1` | `0` |
| Continuation | `5` | `5` | `5` | `0` | `0` | `0` | `0` | `0` | `0` | `0` | `0` | `0` | `5` | `0` | `0` | `0` | `0` | `0` | `5` | `0` |
| Combined | `8` | `8` | `8` | `0` | `0` | `0` | `0` | `0` | `0` | `0` | `0` | `0` | `8` | `0` | `0` | `0` | `0` | `0` | `8` | `0` |

First blockers by stage:

| Stage | Count | Cause |
| --- | ---: | --- |
| `SETUP_QUALIFIED` | `8` | Missing or unresolved setup-time replay fields: setup candle, trigger, invalidation, freshness/final-signal, blocker/caution, or no-hindsight boundary. |

Conversion rates:

- `SETUP_DEVELOPING` to `SETUP_QUALIFIED`: `0.0`.
- Later stage conversion rates: `NOT_APPLICABLE` because no new candidate reached `SETUP_QUALIFIED`.

## Existing Regression-Control Result

The existing 15-candidate positive-trade funnel reran as regression control and remained deterministic:

- Existing candidates found/runnable: `15` / `15`.
- Existing valid trades captured: `1`.
- Existing true no-trades: `4`.
- Existing missing-data cases: `6`.
- Existing missed valid trades: `0`.
- Existing invalid trades allowed: `0`.
- Existing unresolved cases: `4`.
- Existing winners/losers: `1` / `0`.
- Existing deterministic result: `PASS`.

## Cost And Request Decision

- Exact checked cost: `NOT_AVAILABLE`.
- Actual billed cost: `NOT_AVAILABLE`.
- Setup-time request created: `NO`.
- Reason: no new frozen candidate reached `TRADE_CANDIDATE`, so no bounded option-contract set or setup-time quote request is justified.
- CMBP-1 request shape: `NOT_APPLICABLE`.
- CBBO-1s request shape: `NOT_APPLICABLE`.
- Exit-path cost-check task created: `NO`, because no new valid entry was established.

## Five Owner Questions

1. Did SAFE-FAST recognize the new setups before the move?
   - No. The new frozen development candidates do not yet have enough local setup-time replay fields to be recognized before the move.
2. How many became possible trades?
   - `0`.
3. How many had a tradable option at that exact time?
   - `0`; no new candidate reached the option-contract stage.
4. How many were rejected by a real safety rule versus missing evidence?
   - `0` were rejected by a real safety rule; `8` are missing-evidence cases.
5. How many valid trades were caught, missed, or incorrectly allowed?
   - Caught `0`; missed `0`; incorrectly allowed `0`.

## Final State

- New valid trades captured: `0`.
- New true no-trades: `0`.
- New missing-data cases: `8`.
- New missed valid trades: `0`.
- New invalid trades allowed: `0`.
- New unresolved cases: `0`.
- New winners: `0`.
- New losers: `0`.
- Databento downloaded: `NO`.
- Raw vendor data changed: `NO`.
- New P&L calculated: `NO`.
- Proof accepted: `NO`.
- Profitability claimed: `NO`.
- Promotion/readiness/paper/live decision made: `NO`.

Exact next grouped task filename:

`SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_SETUP_FIELD_COMPLETION_CODEX_TASK.md`

## Checks Run

- `.\scripts\safe_fast_run_safe_checks.ps1`: BLOCKED by local PowerShell execution policy before the script ran.
- `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`: PASS, `3` checks plus `9` discovered tests.
- `python -B -m unittest discover -s tests -p "test_day49_positive_entry_candidate_expansion.py"`: PASS, `5` tests.
- `python -B -m watcher_foundation.day49_positive_entry_candidate_expansion_validator`: PASS.
- `python -B -m historical_signal_replay.day49_positive_entry_candidate_expansion`: PASS twice, wrote `8` new candidates, `0` trade candidates, `0` valid captured, `8` missing-data cases.
- `python -B -m historical_signal_replay.day48_positive_trade_capture_funnel`: PASS twice, wrote `15` candidates, `1` valid captured, `4` true no-trades, `6` missing-data cases.
- `python -B -m unittest discover -s tests -p "test_day48_positive_trade_capture_funnel.py"`: PASS, `4` tests.
- `python -B -m unittest discover -s tests -p "test_day49_grouped_positive_entry_setup_time.py"`: PASS, `2` tests.
- `python -B -m unittest discover -s tests -p "test_day48_positive_trade_handoff_consistency.py"`: PASS after control-file update, `3` tests.
- `python -B -m unittest discover -s tests -p "test_day48_actual_grouped_three_family_replay.py"`: PASS, `2` tests.
- `python -B -m unittest discover -s tests -p "test_day48_grouped_three_family_coverage_expansion.py"`: PASS, `3` tests.
- `python -B -m unittest discover -s tests -p "test_day48_continuation_starter_coverage.py"`: PASS, `3` tests.
- `python -B -m unittest discover -s tests -p "test_day48_grouped_three_family_expansion_after_continuation.py"`: PASS, `3` tests.
- `python -B -m unittest discover -s tests -p "test_cfb_contract_selector.py"`: PASS, `17` tests.
- `python -B -m unittest discover -s tests -p "test_execution_context_calculator.py"`: PASS, `10` tests.
- `python -B -m unittest discover -s tests -p "test_context_caution_calculator.py"`: PASS, `12` tests.
- `python -B -m unittest discover -s tests -p "test_watcher_stable_winner_selection_replay.py"`: PASS, `8` tests.
- `python -B -m unittest discover -s tests -p "test_cfb_backtest_runner.py"`: PASS, `8` tests.
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
- Bounded `__pycache__` inspection over `tests`, `watcher_foundation`, `historical_signal_replay`, and `replay`: `0` directories found.
- `git --no-pager diff --check`: PASS with line-ending warnings only for edited Markdown/text/Python files.
