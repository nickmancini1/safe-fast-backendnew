# SAFE-FAST Day 48 Actual Grouped Three-Family Replay Test Result

## Baseline

- Current task file executed: `SAFE_FAST_DAY48_ACTUAL_GROUPED_THREE_FAMILY_REPLAY_TEST_CODEX_TASK.md`.
- Baseline observed locally: branch `main`, HEAD `426a49f`.
- Local status before edits: clean except untracked task file `SAFE_FAST_DAY48_ACTUAL_GROUPED_THREE_FAMILY_REPLAY_TEST_CODEX_TASK.md`; git continued to report permission warnings for temp directories `tmp2i57tguu`, `tmpj8ei9a_f`, `tmpra392qh0`, and `tmpt2fw63vq`.
- This task superseded the queued governance-only repair-retirement task for this turn.
- This was build validation only, not live trade evaluation.

## Scope Executed

- Inventoried currently runnable local lifecycle replay fixtures across Ideal, Clean Fast Break, and Continuation.
- Included every runnable lifecycle fixture found for the three setup families: `12` total.
- Ran the complete grouped fixture batch twice in memory through a deterministic equality test.
- Ran the existing historical replay runner twice.
- Ran existing family-specific replay contracts, developing-stage contracts, session-boundary contracts, winner-stability tests, evidence validator, bridge, and preservation regressions.
- No data was downloaded.
- No trading behavior, live backend, `main.py`, Railway/deploy files, broker/order/account code, credentials, `.env`, frozen trading rule, or raw vendor file was changed.

## Candidate Results

| Candidate identifier | Family | Evidence source | Chronological stage path | Session-boundary behavior | Result and exact reason | Winner-selection result | First/second run stability | Regression result | Remaining limitation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `first_real_gld_clean_fast_break_replay_v1_fixture` | Clean Fast Break | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv` | watching_clean_fast_break_base_rebuild_context -> watching_clean_fast_break_pre_reclaim_range_context -> watching_clean_fast_break_lower_base_before_reclaim -> clean_fast_break_initial_reclaim_candidate -> clean_fast_break_follow_through_extension_candidate -> clean_fast_break_pullback_hold_or_no_fresh_trigger_review | Multi-session carry/reset observed across 2026-04-29, 2026-05-01, 2026-05-05, 2026-05-06, 2026-05-07, 2026-05-08. | Final `NO_TRADE`; accepted-entry rows `0`; reason `fresh_or_spent_unconfirmed`. | Selects GLD Clean Fast Break fixture candidate; false Continuation/Ideal relabels rejected; news unconfirmed. | Stable / identical. | PASS. | Fixture-level only; no option execution, P&L, proof, or readiness. |
| `first_real_gld_continuation_replay_v1_fixture` | Continuation | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv` | watching_continuation_pullback_shelf_developing -> watching_continuation_elevated_shelf_no_trigger -> continuation_rebuild_below_trigger_candidate -> continuation_completed_break_candidate -> continuation_pullback_hold_or_stale_review -> continuation_extension_spent_or_no_fresh_trigger_review | Multi-session carry/reset observed across 2026-04-08, 2026-04-10, 2026-04-13, 2026-04-14, 2026-04-16, 2026-04-17. | Final `NO_TRADE`; accepted-entry rows `0`; reason `prior_completed_shelf_break_spent_TO_REVIEW`. | Selects GLD Continuation fixture candidate; false Ideal/CFB relabels rejected; news unconfirmed. | Stable / identical. | PASS. | Fixture-level only; no option execution, P&L, proof, or readiness. |
| `first_real_gld_ideal_replay_v1_fixture` | Ideal | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv` | watching_ideal_retest_low_context -> watching_ideal_base_after_retest_developing -> ideal_recovery_confirmation_candidate -> ideal_recovery_hold_candidate -> ideal_follow_through_extension_candidate -> ideal_pullback_hold_or_no_fresh_trigger_review | Multi-session carry/reset observed across 2026-05-04, 2026-05-05, 2026-05-06, 2026-05-07, 2026-05-08. | Final `NO_TRADE`; accepted-entry rows `0`; reason `fresh_or_spent_unconfirmed`. | Selects GLD Ideal fixture candidate; news unconfirmed. | Stable / identical. | PASS. | Fixture-level only; no option execution, P&L, proof, or readiness. |
| `first_real_iwm_clean_fast_break_replay_v1_fixture` | Clean Fast Break | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv` | watching_clean_fast_break_gap_impulse_context -> watching_clean_fast_break_tight_pause_context -> clean_fast_break_initial_break_candidate -> clean_fast_break_follow_through_confirming_context -> watching_higher_base_after_fast_break -> clean_fast_break_post_break_no_fresh_trigger | Multi-session carry/reset observed across 2026-04-08, 2026-04-10, 2026-04-13, 2026-04-16, 2026-04-17. | Final `NO_TRADE`; accepted-entry rows `0`; reason `fresh_or_spent_unconfirmed`. | Selects IWM Clean Fast Break fixture candidate; false Continuation relabel rejected. | Stable / identical. | PASS. | Fixture-level only; no option execution, P&L, proof, or readiness. |
| `first_real_iwm_continuation_replay_v1_fixture` | Continuation | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv` | watching_continuation_pullback_shelf_developing -> watching_continuation_shelf_retest_no_trigger -> continuation_recovery_above_shelf_candidate -> continuation_higher_base_rebuild_candidate -> continuation_triggered_signal_stage_candidate -> continuation_spent_or_follow_through_no_fresh_trigger | Multi-session carry/reset observed across 2026-04-20, 2026-04-21, 2026-04-22, 2026-04-24, 2026-04-30, 2026-05-01. | Final `NO_TRADE`; accepted-entry rows `0`; reason `prior_completed_shelf_break_spent_TO_REVIEW`. | Selects IWM Continuation fixture candidate; false Ideal/CFB relabels rejected. | Stable / identical. | PASS. | Fixture-level only; no option execution, P&L, proof, or readiness. |
| `first_real_iwm_ideal_replay_v1_fixture` | Ideal | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv` | watching_ideal_impulse_context -> watching_ideal_pullback_retest_developing -> watching_ideal_retest_hold_unconfirmed -> ideal_retest_recovery_confirmation_candidate -> ideal_triggered_signal_stage_candidate -> ideal_follow_through_no_fresh_trigger | Multi-session carry/reset observed across 2026-05-08, 2026-05-12, 2026-05-14. | Final `NO_TRADE`; accepted-entry rows `0`; reason `fresh_or_spent_unconfirmed`. | Selects IWM Ideal fixture candidate. | Stable / identical. | PASS. | Fixture-level only; no option execution, P&L, proof, or readiness. |
| `first_real_qqq_clean_fast_break_replay_v1_fixture` | Clean Fast Break | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv` | watching_clean_fast_break_gap_impulse_context -> watching_clean_fast_break_tight_pause_context -> clean_fast_break_initial_break_candidate -> clean_fast_break_follow_through_confirming_context -> watching_higher_base_after_fast_break -> clean_fast_break_post_break_no_fresh_trigger | Multi-session carry/reset observed across 2026-04-08, 2026-04-10, 2026-04-13, 2026-04-16, 2026-04-17. | Final `NO_TRADE`; accepted-entry row `2026-04-13T12:30:00-04:00`; reason `prior_completed_clean_fast_break_spent`. | Selects QQQ Clean Fast Break fixture candidate. | Stable / identical. | PASS. | Fixture-level only; stale quote/option execution prevents countable trade proof. |
| `first_real_qqq_continuation_replay_v1_fixture` | Continuation | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv` | watching_continuation_pullback_shelf_developing -> watching_continuation_shelf_retest_no_trigger -> continuation_recovery_above_shelf_candidate -> continuation_higher_base_rebuild_candidate -> continuation_triggered_signal_stage_candidate -> continuation_spent_or_follow_through_no_fresh_trigger | Multi-session carry/reset observed across 2026-04-20, 2026-04-21, 2026-04-22, 2026-04-24, 2026-04-30, 2026-05-01. | Final `NO_TRADE`; accepted-entry row `2026-04-30T15:30:00-04:00`; reason `prior_completed_shelf_break_spent`. | Selects QQQ Continuation fixture candidate. | Stable / identical. | PASS. | Fixture-level only; no option execution, P&L, proof, or readiness. |
| `first_real_qqq_ideal_replay_v1_fixture` | Ideal | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv` | watching_ideal_impulse_context -> watching_ideal_pullback_retest_developing -> watching_ideal_retest_hold_unconfirmed -> ideal_retest_recovery_confirmation_candidate -> ideal_triggered_signal_stage_candidate -> ideal_follow_through_no_fresh_trigger | Multi-session carry/reset observed across 2026-05-08, 2026-05-12, 2026-05-13, 2026-05-14. | Final `NO_TRADE`; accepted-entry row `2026-05-13T12:30:00-04:00`; reason `prior_completed_ideal_trigger_spent`. | Selects QQQ Ideal fixture candidate. | Stable / identical. | PASS. | Fixture-level only; no option execution, P&L, proof, or readiness. |
| `first_real_spy_continuation_replay_v1_fixture` | Continuation | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` | developing_pullback_shelf -> developing_shelf_no_trigger -> developing_shelf_no_trigger -> opening_probe_no_completed_approval -> triggered_signal_stage_candidate -> spent_or_follow_through_no_fresh_trigger | Multi-session carry/reset observed across 2026-04-28, 2026-04-29, 2026-04-30. | Final `NO_TRADE`; accepted-entry row `2026-04-30T12:30:00-04:00`; reason `prior_completed_shelf_break_spent`. | Selects SPY Continuation fixture candidate. | Stable / identical. | PASS. | Fixture-level only; no option execution, P&L, proof, or readiness. |
| `second_real_spy_ideal_replay_v1_fixture` | Ideal | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` | ideal_impulse_context -> ideal_pullback_retest_developing -> ideal_retest_hold_unconfirmed -> ideal_retest_recovery_confirmation_candidate -> ideal_triggered_signal_stage_candidate -> ideal_follow_through_no_fresh_trigger | Multi-session carry/reset observed across 2026-05-11, 2026-05-12, 2026-05-13. | Final `NO_TRADE`; accepted-entry row `2026-05-13T11:30:00-04:00`; reason `prior_completed_ideal_trigger_spent`. | Selects SPY Ideal fixture candidate. | Stable / identical. | PASS. | Fixture-level only; no option execution, P&L, proof, or readiness. |
| `third_real_spy_clean_fast_break_replay_v1_fixture` | Clean Fast Break | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` | clean_fast_break_tight_pause_context -> clean_fast_break_initial_break_candidate -> clean_fast_break_follow_through_confirming_context -> watching_higher_base_after_fast_break -> clean_fast_break_fresh_break_signal_candidate -> clean_fast_break_post_break_no_fresh_trigger | Multi-session carry/reset observed across 2026-04-10, 2026-04-13, 2026-04-15. | Final `NO_TRADE`; accepted-entry rows `2026-04-13T12:30:00-04:00` and `2026-04-15T14:30:00-04:00`; reason `prior_completed_clean_fast_break_spent`. | Selects SPY Clean Fast Break fixture candidate. | Stable / identical. | PASS. | Fixture-level only; CFB 003 remains no-trade from quote age above 5 minutes under selected-contract replay. |

## Family Totals

| Family | Candidates found | Candidates runnable | Accepted-entry stage rows | Final no-trades | Ambiguous/pending cases | Passes | Failures | Blocked cases | Stable cases | Unstable cases |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Ideal | 4 | 4 | 2 | 4 | 4 | 4 | 0 | 4 | 4 | 0 |
| Clean Fast Break | 4 | 4 | 3 | 4 | 1 | 4 | 0 | 4 | 4 | 0 |
| Continuation | 4 | 4 | 2 | 4 | 3 | 4 | 0 | 4 | 4 | 0 |

## Aggregate Result

- Candidates found: `12`.
- Candidates runnable: `12`.
- Families runnable: Ideal, Clean Fast Break, Continuation.
- Grouped first-run result: PASS.
- Grouped second-run result: PASS.
- Deterministic equality result: PASS.
- Stage-transition result: PASS; all grouped fixtures preserve six-row chronological lifecycle paths and existing stage contract scripts pass.
- Session-boundary result: PASS; all grouped fixtures cover multi-session carry/reset behavior and existing session-boundary scripts pass.
- Winner-stability result: PASS; grouped fixture winner-selection fields are stable and existing stable-winner tests pass.
- Regression result: PASS for the validation surface run in this task.
- Unresolved cases: no runnable family failed to execute; all cases remain fixture-level validation and not countable trade proof.
- Missing coverage: no option execution/P&L/profitability validation for Ideal or Continuation; GLD/IWM rows remain shape-only candidates needing review; all grouped fixture candidates end as final `NO_TRADE`; no protected holdout was opened.

## Checks Run

- `.\scripts\safe_fast_run_safe_checks.ps1`: BLOCKED by local PowerShell execution policy before the script ran.
- `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`: PASS, `3` checks, plus `9` discovered tests.
- `python -B -m unittest discover -s tests -p "test_day48_actual_grouped_three_family_replay.py"`: PASS, `2` tests.
- `python -B .\historical_signal_replay\run_signal_replay.py`: PASS, run once.
- `python -B .\historical_signal_replay\run_signal_replay.py`: PASS, run twice.
- Direct script execution for `replay/test_on_demand_*ideal*.py`: PASS, `3` files, `0` failed.
- Direct script execution for `replay/test_on_demand_*clean_fast_break*.py`: PASS, `3` files, `0` failed.
- Direct script execution for `replay/test_on_demand_*continuation*.py`: PASS, `6` files, `0` failed.
- Direct script execution for `replay/test_on_demand_*stage*.py`: PASS, `6` files, `0` failed.
- Direct script execution for `replay/test_on_demand_session_boundary*.py`: PASS, `5` files, `0` failed.
- `python -B -m unittest discover -s tests -p "test_watcher_stable_winner_selection_replay.py"`: PASS, `8` tests.
- `python -B .\replay\test_on_demand_winner_selection_contract.py`: PASS.
- `python -B -m watcher_foundation.source_evidence_work_package_content_validator`: PASS, `9` passed requests, `0` failed requests, intake-ready `0`.
- `python -B -m watcher_foundation.source_evidence_package_to_intake_bridge`: PASS, `4` reconsideration-eligible candidates, intake-ready `0`, proof allowed `NO`.
- `python -B -m unittest discover -s tests -p "test_watcher_replay*.py"`: PASS, `42` tests.
- `python -B -m unittest discover -s tests -p "test_day47_grouped_replay_regression_rules.py"`: PASS, `5` tests.
- `python -B -m unittest discover -s tests -p "test_candidate_freshness_blocker*.py"`: PASS, `56` tests.
- Bounded `__pycache__` cleanup over `tests`, `watcher_foundation`, `historical_signal_replay`, and `replay`: `0` directories removed.
- `git --no-pager diff --check`: PASS.

## Final State

- Databento downloaded: NO.
- New backtest run: NO.
- New P&L calculated: NO.
- Promotion decision made: NO.
- Real trade chosen: NO.
- Candidate marked ready: NO.
- Intake-ready count changed: NO.
- Proof accepted: NO.
- Profitability claim made: NO.
- Main/live/engine/deploy/broker/order/account/secrets/raw vendor data changed: NO.

## Next Task Determination

Actual test evidence shows grouped execution works and is deterministic, but coverage is thin: all runnable grouped lifecycle candidates are fixture-level, all final outcomes are `NO_TRADE`, and Ideal/Continuation still lack option-execution/P&L validation. The next task is grouped expansion, not repair and not cost check.

Exact next grouped task filename:

`SAFE_FAST_DAY48_GROUPED_THREE_FAMILY_COVERAGE_EXPANSION_CODEX_TASK.md`
