# SAFE-FAST Day 48 Positive-Trade Capture and Miss Analysis Result

## Baseline

- Current task file executed: `SAFE_FAST_DAY48_POSITIVE_TRADE_CAPTURE_AND_MISS_ANALYSIS_CODEX_TASK.md`.
- Baseline observed locally: branch `main`, HEAD `6b90016`.
- Local status before edits: clean except untracked task file `SAFE_FAST_DAY48_POSITIVE_TRADE_CAPTURE_AND_MISS_ANALYSIS_CODEX_TASK.md`; git continued to report permission warnings for temp directories `tmp2i57tguu`, `tmpj8ei9a_f`, `tmpra392qh0`, and `tmpt2fw63vq`.
- This was actual SAFE-FAST build testing and measurement, not live trade evaluation.
- No data was downloaded.
- No `main.py`, live/engine trading logic, Railway/deploy files, broker/order/account files, `.env`, secrets, raw vendor data, evidence fills, trade-selection code, P&L files, or generated live reports/logs were changed.

## Output Created

- Machine-readable funnel result: `historical_signal_replay/results/day48_positive_trade_capture_funnel.json`.
- Funnel builder: `historical_signal_replay/day48_positive_trade_capture_funnel.py`.
- Focused validator: `watcher_foundation/day48_positive_trade_capture_funnel_validator.py`.
- Focused tests: `tests/test_day48_positive_trade_capture_funnel.py`.

The funnel includes the existing `12` grouped lifecycle fixture candidates plus the `3` Clean Fast Break selected-contract replay rows from the current review-only CFB path.

## Four Scorecards

| Scorecard | Found | Runnable | Setup developing | Setup qualified | Trade candidate | Contracts selected | Prices accepted | Entries eligible | Entries recorded | Exits evaluated | Valid trades captured | True no-trades | Missing data | Missed valid trades | Invalid trades allowed | Unresolved | Winners | Losers | Deterministic | Unstable |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Ideal | 4 | 4 | 4 | 4 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 2 | 0 | 0 | 4 | 0 |
| Clean Fast Break | 7 | 7 | 7 | 6 | 5 | 3 | 3 | 1 | 1 | 1 | 1 | 2 | 3 | 0 | 0 | 1 | 1 | 0 | 7 | 0 |
| Continuation | 4 | 4 | 4 | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 1 | 0 | 0 | 4 | 0 |
| Combined | 15 | 15 | 15 | 13 | 9 | 3 | 3 | 1 | 1 | 1 | 1 | 2 | 8 | 0 | 0 | 4 | 1 | 0 | 15 | 0 |

## Candidate-Level Funnel Table

| Candidate | Family | Underlying | Highest stage | First stage not reached | Blocker | Classification | Winner/loser |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | Clean Fast Break | SPY | `FINAL_OUTCOME` | none | none | `VALID_TRADE_CAPTURED` | winner |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | Clean Fast Break | SPY | `PRICE_ACCEPTABLE` | `ENTRY_ELIGIBLE` | `quote_age_above_5_minutes` | `TRUE_NO_TRADE` | none |
| `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | Clean Fast Break | QQQ | `PRICE_ACCEPTABLE` | `ENTRY_ELIGIBLE` | `quote_age_above_5_minutes` | `TRUE_NO_TRADE` | none |
| `first_real_gld_clean_fast_break_replay_v1_fixture` | Clean Fast Break | GLD | `SETUP_QUALIFIED` | `TRADE_CANDIDATE` | `fresh_or_spent_unconfirmed` | `UNRESOLVED` | none |
| `first_real_iwm_clean_fast_break_replay_v1_fixture` | Clean Fast Break | IWM | `SETUP_DEVELOPING` | `SETUP_QUALIFIED` | `fresh_or_spent_unconfirmed` | `MISSING_DATA` | none |
| `first_real_qqq_clean_fast_break_replay_v1_fixture` | Clean Fast Break | QQQ | `TRADE_CANDIDATE` | `CONTRACT_SELECTED` | `missing_setup_time_selected_option_evidence` | `MISSING_DATA` | none |
| `third_real_spy_clean_fast_break_replay_v1_fixture` | Clean Fast Break | SPY | `TRADE_CANDIDATE` | `CONTRACT_SELECTED` | `missing_setup_time_selected_option_evidence` | `MISSING_DATA` | none |
| `first_real_gld_ideal_replay_v1_fixture` | Ideal | GLD | `SETUP_QUALIFIED` | `TRADE_CANDIDATE` | `fresh_or_spent_unconfirmed` | `UNRESOLVED` | none |
| `first_real_iwm_ideal_replay_v1_fixture` | Ideal | IWM | `SETUP_QUALIFIED` | `TRADE_CANDIDATE` | `fresh_or_spent_unconfirmed` | `UNRESOLVED` | none |
| `first_real_qqq_ideal_replay_v1_fixture` | Ideal | QQQ | `TRADE_CANDIDATE` | `CONTRACT_SELECTED` | `missing_setup_time_selected_option_evidence` | `MISSING_DATA` | none |
| `second_real_spy_ideal_replay_v1_fixture` | Ideal | SPY | `TRADE_CANDIDATE` | `CONTRACT_SELECTED` | `missing_setup_time_selected_option_evidence` | `MISSING_DATA` | none |
| `first_real_gld_continuation_replay_v1_fixture` | Continuation | GLD | `SETUP_DEVELOPING` | `SETUP_QUALIFIED` | `prior_completed_shelf_break_spent_TO_REVIEW` | `MISSING_DATA` | none |
| `first_real_iwm_continuation_replay_v1_fixture` | Continuation | IWM | `SETUP_QUALIFIED` | `TRADE_CANDIDATE` | `prior_completed_shelf_break_spent_TO_REVIEW` | `UNRESOLVED` | none |
| `first_real_qqq_continuation_replay_v1_fixture` | Continuation | QQQ | `TRADE_CANDIDATE` | `CONTRACT_SELECTED` | `missing_setup_time_selected_option_evidence` | `MISSING_DATA` | none |
| `first_real_spy_continuation_replay_v1_fixture` | Continuation | SPY | `TRADE_CANDIDATE` | `CONTRACT_SELECTED` | `missing_setup_time_selected_option_evidence` | `MISSING_DATA` | none |

## First-Blocker Analysis

| First blocker stage | Count | Families affected | Common cause | Cause type | Local evidence can resolve? | External data required? | Smallest safe next action |
| --- | ---: | --- | --- | --- | --- | --- | --- |
| `SETUP_QUALIFIED` | 2 | Continuation, Clean Fast Break | spent/freshness not proven enough for qualification | missing or unresolved local setup evidence | no | no | Add grouped local fixture evidence before any data request. |
| `TRADE_CANDIDATE` | 4 | Clean Fast Break, Ideal, Continuation | fresh/spent or pending status unresolved | unresolved setup-stage evidence | no | no | Add grouped local fixture evidence before any data request. |
| `CONTRACT_SELECTED` | 6 | Clean Fast Break, Ideal, Continuation | setup-time selected-option evidence missing | missing data | no | yes for some candidates | Build grouped positive-entry expansion first; create exact missing-data cost checks only for named setup-time fields after local evidence is exhausted. |
| `ENTRY_ELIGIBLE` | 2 | Clean Fast Break | selected quote older than frozen 5-minute gate | correct safety behavior | yes | no | Preserve frozen stale-quote rejection controls in regression. |
| none | 1 | Clean Fast Break | SPY CFB 002 completed review-only positive entry | captured valid entry reference, not proof | n/a | no | Use as positive-entry expansion reference without claiming proof. |

## Totals

- Valid trades captured: `1`.
- True no-trades: `2`.
- Missing-data cases: `8`.
- Missed valid trades: `0`.
- Invalid trades allowed: `0`.
- Unresolved cases: `4`.
- Winners: `1`.
- Losers: `0`.
- Deterministic cases: `15`.
- Unstable cases: `0`.

The captured trade is `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`, using the existing review-only CFB selected-contract path: entry basis `6.37`, adjusted exit basis `7.98`, adjusted result `+1.61`, profit-target exit. This remains not proof, not profitability, not readiness, and not promotion.

## Sample Contract Progress

| Requirement | Current | Required |
| --- | ---: | ---: |
| Accepted entries | 1 | 20 |
| Rejection/no-trade controls | 2 | 10 |
| Ambiguous/boundary cases | 4 | 5 |
| Winners | 1 | 5 |
| Losers | 0 | 5 |
| Protected holdout accepted entries | 0 | 8 |
| Protected holdout rejection/no-trade controls | 0 | 4 |

SAFE-FAST is far below the canonical sample contract. The current evidence is useful development evidence only.

## Five Owner Questions

1. Did SAFE-FAST recognize the setup before the move?
   - Yes for the grouped lifecycle candidates that reached setup or trade-candidate stages; recognition is still incomplete for shape-only and missing-data rows.
2. Did it classify the setup as a possible trade?
   - Yes for accepted-entry-stage lifecycle rows and the three CFB selected-contract replay rows. An accepted-entry-stage row is not an executed trade.
3. Was a tradable option available at that exact time?
   - Only `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` currently has local selected-contract entry and exit evidence sufficient for a review-only captured valid entry. Other rows are blocked by stale quote, future quote, wide spread, unresolved setup state, or missing setup-time selected-option evidence.
4. Was rejection caused by a real safety rule or by missing evidence?
   - Both. Two CFB controls are true no-trades from the frozen quote-age safety rule. Eight cases are missing-data blockers. Four remain unresolved and are not hidden inside no-trade totals.
5. How many valid trades were caught, missed, or incorrectly allowed?
   - Caught `1`; missed `0`; incorrectly allowed `0`.

## Exact Evidence-Backed Next Action

Create one grouped positive-entry expansion task:

`SAFE_FAST_DAY48_GROUPED_POSITIVE_ENTRY_EXPANSION_CODEX_TASK.md`

Reason: the funnel works and separates captured trades, true no-trades, missing data, missed valid trades, invalid allowed trades, and unresolved cases, but valid-entry coverage is only `1` and there are no losing valid-entry examples. The next task must expand positive-entry coverage in grouped batches while rerunning the stale-quote no-trade controls and the full three-family regression suite.

Do not download data in that task unless it creates an exact grouped missing-data request and later receives a checked cost plus user approval. Do not claim proof, profitability, readiness, promotion, paper eligibility, or live eligibility.

## Checks Run

- `.\scripts\safe_fast_run_safe_checks.ps1`: BLOCKED by local PowerShell execution policy before the script ran.
- `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`: PASS, `3` checks plus `9` discovered tests.
- `python -B -m historical_signal_replay.day48_positive_trade_capture_funnel`: PASS, wrote `15` candidates, `1` valid captured, `2` true no-trades, `8` missing-data cases.
- `python -B -m watcher_foundation.day48_positive_trade_capture_funnel_validator`: PASS.
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
- Direct script execution for `replay/test_on_demand_*ideal*.py`: PASS, `3` files.
- Direct script execution for `replay/test_on_demand_*clean_fast_break*.py`: PASS, `3` files.
- Direct script execution for `replay/test_on_demand_*continuation*.py`: PASS, `6` files.
- Direct script execution for `replay/test_on_demand_*stage*.py`: PASS, `6` files.
- Direct script execution for `replay/test_on_demand_session_boundary*.py`: PASS, `5` files.
- `python -B -m unittest discover -s tests -p "test_watcher_stable_winner_selection_replay.py"`: PASS, `8` tests.
- `python -B .\replay\test_on_demand_winner_selection_contract.py`: PASS.
- `python -B .\historical_signal_replay\run_signal_replay.py`: PASS.
- `python -B -m watcher_foundation.source_evidence_work_package_content_validator`: PASS, `9` passed requests, `0` failed requests, intake-ready `0`.
- `python -B -m watcher_foundation.source_evidence_package_to_intake_bridge`: PASS, `4` reconsideration-eligible candidates, intake-ready `0`, proof allowed `NO`.
- `python -B -m unittest discover -s tests -p "test_day47_to_day90_audit_consistency.py"`: PASS, `2` tests.
- Bounded `__pycache__` inspection over `tests`, `watcher_foundation`, `historical_signal_replay`, and `replay`: `0` directories found.
- `git --no-pager diff --check`: PASS with line-ending warnings only for edited Markdown/text files.
