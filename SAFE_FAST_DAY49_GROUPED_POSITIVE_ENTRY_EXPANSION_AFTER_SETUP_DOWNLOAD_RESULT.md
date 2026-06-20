# SAFE-FAST Day 49 Grouped Positive-Entry Expansion After Setup Download Result

## Baseline

- Current task file executed: `SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_EXPANSION_AFTER_SETUP_DOWNLOAD_CODEX_TASK.md`.
- This was SAFE-FAST build testing, not live trading.
- No production, live backend, `main.py`, Railway, deployment, broker, account, order, credential, or `.env` files were modified.
- `SAFE_FAST_DB_AUTH` was not used. No Databento cost call was made and no data was downloaded.
- Local quote-update evidence was checked first, using existing ignored local files and committed funnel, fixture, candidate-packet, manifest, and rule artifacts.

## Objective Result

The grouped quote-freshness and eligible-contract sweep found no new valid positive entry and no losing valid-entry example from current local evidence.

The smallest safe next path is not a data download. It is a grouped local replacement/expansion sweep for candidates that can reach selected-contract review without already being stale, no-fallback blocked, outside the narrowed path, or blocked before trade-candidate status.

## Grouped Candidate Inventory Reviewed

The current funnel inventory remains `15` review-only records:

| Group | Count | Result |
| --- | ---: | --- |
| Grouped lifecycle fixtures | `12` | `6` missing-data, `4` unresolved, `2` true no-trade after Day 49 setup-time evidence |
| CFB selected-contract replay rows | `3` | `1` valid captured winner reference, `2` stale-quote true no-trade controls |
| Combined | `15` | `1` valid captured, `4` true no-trades, `6` missing-data, `4` unresolved |

## Quote-Freshness And Eligible-Contract Sweep

| Candidate or record | Local evidence checked | Sweep result |
| --- | --- | --- |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | Existing CFB selected-contract replay output | Preserved as the only review-only positive winner reference; no new entry or P&L was created. |
| `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | Existing local top-contract quote/trade/statistics evidence and selected-contract replay output | Preserved as `TRUE_NO_TRADE`; selected quote at `2026-04-13T16:06:30.640301Z` is about `1409.359699` seconds old at signal, so it fails `quote_age_above_5_minutes`. |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | Existing selected-contract setup-window download manifest and CFB replay output | Preserved as `TRUE_NO_TRADE`; nearest setup-time-safe quote at `2026-04-15T18:22:33.366710Z` is about `446.633289` seconds old, so it fails `quote_age_above_5_minutes`. |
| `SPY-REAL-HISTORICAL-IDEAL-001` / `second_real_spy_ideal_replay_v1_fixture` | Day 49 setup-time raw-symbol quote/trade manifest and helper evidence | Preserved as `TRUE_NO_TRADE`; selected quote at `2026-05-13T15:22:37.366073Z`, trade volume `45`, spread `0.03`, quote age `442.633927` seconds, fail `quote_age_above_5_minutes`. |
| `SPY-REAL-HISTORICAL-CONTINUATION-001` / `first_real_spy_continuation_replay_v1_fixture` | Day 49 setup-time raw-symbol quote/trade manifest and helper evidence | Preserved as `TRUE_NO_TRADE`; selected quote at `2026-04-30T15:26:49.253742Z`, trade volume `15`, spread `0.01`, quote age `3790.746258` seconds, fail `quote_age_above_5_minutes`. |
| `QQQ-REAL-HISTORICAL-CONTINUATION-001` / `first_real_qqq_continuation_replay_v1_fixture` | Existing local starter option files and Day 48 Continuation option-context evidence package | No positive entry found; local setup-time-safe top-ranked quote exists, but spread `0.35` fails the accepted `0.15` spread cap and no fallback is allowed. |
| `QQQ-REAL-HISTORICAL-IDEAL-001` / `first_real_qqq_ideal_replay_v1_fixture` | Candidate packet, starter files, and rule gate state | No exact positive-entry request is justified; QQQ Ideal remains outside the narrowed path until Ideal lifecycle/freshness, room/risk, context, contract-selection, entry, exit, cost, and slippage rules exist. |
| GLD and IWM lifecycle fixtures | Funnel records and freshness/blocker state | No selected-contract sweep is justified yet; these remain blocked before selected-option evidence by setup qualification or unresolved fresh/spent state. |

## Before/After Funnel Totals

The funnel was rerun after the sweep. No classification changed.

| Metric | Before sweep | After sweep |
| --- | ---: | ---: |
| Candidates found/runnable | `15` / `15` | `15` / `15` |
| Contracts selected | `5` | `5` |
| Prices accepted | `5` | `5` |
| Entries eligible | `1` | `1` |
| Entries recorded | `1` | `1` |
| Exits evaluated | `1` | `1` |
| Valid trades captured | `1` | `1` |
| True no-trades | `4` | `4` |
| Missing-data cases | `6` | `6` |
| Unresolved cases | `4` | `4` |
| Missed valid trades | `0` | `0` |
| Invalid trades allowed | `0` | `0` |
| Winners | `1` | `1` |
| Losers | `0` | `0` |

First blockers by funnel stage remain:

| Stage | Count |
| --- | ---: |
| `SETUP_QUALIFIED` | `2` |
| `TRADE_CANDIDATE` | `4` |
| `CONTRACT_SELECTED` | `4` |
| `ENTRY_ELIGIBLE` | `4` |
| `NONE` | `1` |

## Positive-Entry Candidates Found

- New positive-entry candidates found: `0`.
- New valid losing entries found: `0`.
- Existing positive winner reference preserved: `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`.
- No exit-path data was downloaded or used for any newly eligible candidate because no newly eligible candidate exists.

## True No-Trade Controls Preserved

The sweep preserved all four current true no-trade controls:

- `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`: stale quote, `quote_age_above_5_minutes`.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`: stale quote, `quote_age_above_5_minutes`.
- `SPY-REAL-HISTORICAL-IDEAL-001`: stale quote, `quote_age_above_5_minutes`.
- `SPY-REAL-HISTORICAL-CONTINUATION-001`: stale quote, `quote_age_above_5_minutes`.

These controls must stay in regression/sample accounting and must not be replaced by favorable examples.

## Missing-Data Cases Remaining

Six records remain `MISSING_DATA`:

| Record | First stage not reached | Exact blocker | Sweep decision |
| --- | --- | --- | --- |
| `first_real_gld_continuation_replay_v1_fixture` | `SETUP_QUALIFIED` | `prior_completed_shelf_break_spent_TO_REVIEW` | Needs local lifecycle/freshness evidence before option data. |
| `first_real_iwm_clean_fast_break_replay_v1_fixture` | `SETUP_QUALIFIED` | `fresh_or_spent_unconfirmed` | Needs local lifecycle/freshness evidence before option data. |
| `first_real_qqq_clean_fast_break_replay_v1_fixture` | `CONTRACT_SELECTED` | `missing_setup_time_selected_option_evidence` | Matching business candidate already has separate selected-contract stale-quote no-trade evidence; no new request needed. |
| `first_real_qqq_continuation_replay_v1_fixture` | `CONTRACT_SELECTED` | `missing_setup_time_selected_option_evidence` | Local evidence already shows top-ranked contract fails spread/no-fallback; no new request needed. |
| `first_real_qqq_ideal_replay_v1_fixture` | `CONTRACT_SELECTED` | `missing_setup_time_selected_option_evidence` | Outside narrowed Ideal path until setup-family rules exist; no exact request now. |
| `third_real_spy_clean_fast_break_replay_v1_fixture` | `CONTRACT_SELECTED` | `missing_setup_time_selected_option_evidence` | Matching business candidate already has separate selected-contract stale-quote no-trade evidence; no new request needed. |

## Unresolved Cases Remaining

Four records remain `UNRESOLVED`:

- `first_real_gld_clean_fast_break_replay_v1_fixture`: `fresh_or_spent_unconfirmed`.
- `first_real_gld_ideal_replay_v1_fixture`: `fresh_or_spent_unconfirmed`.
- `first_real_iwm_continuation_replay_v1_fixture`: `prior_completed_shelf_break_spent_TO_REVIEW`.
- `first_real_iwm_ideal_replay_v1_fixture`: `fresh_or_spent_unconfirmed`.

These need grouped local fixture/source evidence before any selected-contract request package.

## Cost-Check Package Decision

New exact cost-check package needed now: `NO`.

Reason: current local evidence already answers the live contract-selected blockers that can be answered safely:

- QQQ CFB and SPY CFB 003 are stale-quote controls.
- QQQ Continuation fails local spread/no-fallback.
- SPY Ideal and SPY Continuation were answered by the approved Day 49 setup-time download and are stale-quote controls.
- QQQ Ideal and the GLD/IWM rows are not exact selected-contract request candidates under current rules.

A later cost-check package may become justified only after a grouped local replacement-candidate sweep identifies candidates that reach trade-candidate status, have exact deterministic selected contracts, and are not already blocked by local quote freshness, spread, no-fallback, or narrowed-path rules.

## Final State

- Databento downloaded: `NO`.
- Databento cost check made: `NO`.
- Exit-path downloaded: `NO`.
- Raw vendor data changed: `NO`.
- Positive-trade funnel artifact rerun: `YES`, no classification change.
- New backtest run: grouped positive-trade funnel rerun only; no new exit/P&L backtest.
- New P&L calculated: `NO`.
- Promotion decision made: `NO`.
- Real trade chosen: `NO`.
- Candidate marked ready: `NO`.
- Intake-ready count changed: `NO`.
- Proof accepted: `NO`.
- Profitability claim made: `NO`.

Exact next grouped task filename:

`SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_LOCAL_REPLACEMENT_CANDIDATE_SWEEP_CODEX_TASK.md`

## Checks Run

- `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`: PASS, `3` checks plus `9` discovered tests.
- `python -B -m historical_signal_replay.day48_positive_trade_capture_funnel`: PASS, wrote `15` candidates, `1` valid captured, `4` true no-trades, `6` missing-data cases.
- `python -B -m watcher_foundation.day48_positive_trade_capture_funnel_validator`: PASS.
- `python -B -m unittest discover -s tests -p "test_day48_positive_trade_capture_funnel.py"`: PASS, `4` tests.
- `python -B -m unittest discover -s tests -p "test_day49_grouped_positive_entry_setup_time.py"`: PASS, `2` tests.
- `python -B -m unittest discover -s tests -p "test_day48_positive_trade_handoff_consistency.py"`: PASS, `3` tests.
- `python -B -m unittest discover -s tests -p "test_day48_actual_grouped_three_family_replay.py"`: PASS, `2` tests.
- `python -B -m unittest discover -s tests -p "test_day48_grouped_three_family_coverage_expansion.py"`: PASS, `3` tests.
- `python -B -m unittest discover -s tests -p "test_day48_continuation_starter_coverage.py"`: PASS, `3` tests.
- `python -B -m unittest discover -s tests -p "test_day48_grouped_three_family_expansion_after_continuation.py"`: PASS, `3` tests.
- `python -B -m unittest discover -s tests -p "test_cfb_backtest_runner.py"`: PASS, `8` tests.
- `python -B -m unittest discover -s tests -p "test_execution_context_calculator.py"`: PASS, `10` tests.
- `python -B -m unittest discover -s tests -p "test_cfb_contract_selector.py"`: PASS, `17` tests.
- `python -B -m watcher_foundation.source_evidence_work_package_content_validator`: PASS, `9` passed requests, `0` failed requests, intake-ready `0`.
- `python -B -m watcher_foundation.source_evidence_package_to_intake_bridge`: PASS, `4` reconsideration-eligible candidates, intake-ready `0`, proof allowed `NO`.
- Bounded `__pycache__` inspection over `tests`, `watcher_foundation`, `historical_signal_replay`, and `replay`: `0` directories found.
- `git --no-pager diff --check`: PASS.
