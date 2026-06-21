# SAFE-FAST Day 50 Positive-Entry Active-Path Requirement Regression Result

## Baseline

- Branch: `main`.
- Current task file executed: `SAFE_FAST_DAY50_POSITIVE_ENTRY_ACTIVE_PATH_REQUIREMENT_REGRESSION_CODEX_TASK.md`.
- Required startup files read first: `SAFE_FAST_BUILD_STATE.md`, Day 50 remaining evidence-gap closeout result/JSON, Day 50 active-path rule/evidence repair result/JSON, data-source registry, dashboard, and rule index.
- Source of truth: Day 50 remaining evidence-gap closeout result only.
- Open group tested: exactly the four active-path requirements that still blocked `TRADE_CANDIDATE` before selected-contract identity.
- QQQ Clean Fast Break 001 was preserved as `TRUE_NO_TRADE_REGRESSION_ONLY` and was not rerun as a live candidate.
- QQQ Ideal was preserved as `replace` / outside the narrowed Ideal path.
- Contract-selected closeout remained preserved with `0` additional entries.

## Fixed

- Added bounded active-path requirement regression builder: `historical_signal_replay/day50_positive_entry_active_path_requirement_regression.py`.
- Added machine-readable regression result: `historical_signal_replay/results/day50_positive_entry_active_path_requirement_regression.json`.
- Added focused regression tests: `tests/test_day50_positive_entry_active_path_requirement_regression.py`.
- Created exact next grouped task: `SAFE_FAST_DAY50_POSITIVE_ENTRY_CLOSED_REQUIREMENT_SCORECARD_RECONCILIATION_CODEX_TASK.md`.
- Updated control documents: `SAFE_FAST_BUILD_STATE.md`, `SAFE_FAST_PROJECT_DASHBOARD.md`, `SAFE_FAST_PROJECT_RULE_INDEX.md`, and `SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt`.

## Regression Result

- Active-path requirements tested: `4`.
- Advanced to `TRADE_CANDIDATE`: `0`.
- Permanently closed with exact failed requirement: `4`.
- Active-path requirements open after regression: `0`.
- Additional entries established: `0`.
- Affected active-path cases selected contracts before/after regression: `0` / `0`.
- Affected active-path cases eligible entries before/after regression: `0` / `0`.
- Affected active-path cases recorded entries before/after regression: `0` / `0`.
- Batch trade candidates before/after regression: `9` / `9`.
- Batch selected contracts before/after regression: `5` / `5`.
- Batch eligible entries before/after regression: `1` / `1`.
- Batch recorded entries before/after regression: `1` / `1`.
- Paid-data request created: `NO`.
- Databento downloaded: `NO`.
- Deterministic comparison: `PASS`; first and second hashes matched.

## Tested Active-Path Requirements

| Candidate | Result | Exact failed requirement | Field/source/dataset/calculator/window |
| --- | --- | --- | --- |
| `first_real_gld_clean_fast_break_replay_v1_fixture` | Permanently closed; did not advance to `TRADE_CANDIDATE`. | `freshness_final_signal_state` remained `fresh_or_spent_unconfirmed`; no accepted Clean Fast Break fresh/spent active-path rule advances the case. | `freshness_final_signal_state`; `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv`; SAFE-FAST local grouped lifecycle fixture / `signal_replay_input_v1` and `signal_replay_output_v1`; `historical_signal_replay.day48_positive_trade_capture_funnel`; `2026-05-08T15:30:00-04:00`. |
| `first_real_gld_ideal_replay_v1_fixture` | Permanently closed; did not advance to `TRADE_CANDIDATE`. | `freshness_final_signal_state` remained `fresh_or_spent_unconfirmed`; no accepted Ideal fresh/spent active-path rule advances the case. | `freshness_final_signal_state`; `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv`; SAFE-FAST local grouped lifecycle fixture / `signal_replay_input_v1` and `signal_replay_output_v1`; `historical_signal_replay.day48_positive_trade_capture_funnel`; `2026-05-08T15:30:00-04:00`. |
| `first_real_iwm_continuation_replay_v1_fixture` | Permanently closed; did not advance to `TRADE_CANDIDATE`. | `prior_completed_shelf_break_spent_state` remained `prior_completed_shelf_break_spent_TO_REVIEW`; no accepted session-boundary freshness rule advances the case. | `prior_completed_shelf_break_spent_state`; `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv`; SAFE-FAST local grouped lifecycle fixture / `signal_replay_input_v1` and `signal_replay_output_v1`; `historical_signal_replay.day48_positive_trade_capture_funnel`; `2026-05-01T15:30:00-04:00`. |
| `first_real_iwm_ideal_replay_v1_fixture` | Permanently closed; did not advance to `TRADE_CANDIDATE`. | `freshness_final_signal_state` remained `fresh_or_spent_unconfirmed`; no accepted Ideal fresh/spent active-path rule advances the case. | `freshness_final_signal_state`; `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv`; SAFE-FAST local grouped lifecycle fixture / `signal_replay_input_v1` and `signal_replay_output_v1`; `historical_signal_replay.day48_positive_trade_capture_funnel`; `2026-05-14T15:30:00-04:00`. |

## Scorecard

- Before regression: `VALID_TRADE_CAPTURED=1`, `TRUE_NO_TRADE=4`, `MISSING_DATA=6`, `MISSED_VALID_TRADE=0`, `INVALID_TRADE_ALLOWED=0`, and `UNRESOLVED=4`.
- After regression: `VALID_TRADE_CAPTURED=1`, `TRUE_NO_TRADE=4`, `MISSING_DATA=10`, `MISSED_VALID_TRADE=0`, `INVALID_TRADE_ALLOWED=0`, and `UNRESOLVED=0`.
- Additional entries: `0`.
- Closed safety rejections rerun as live candidates: `0`.
- Closed setup-source candidates reopened: `0`.
- Rejected intake rows replayed: `0`.

## Cost And Scope

- Checked cost: `NOT_AVAILABLE`.
- Actual billed cost: `NOT_AVAILABLE`.
- Credential used: `NO`.
- Reason: all four tested active-path requirements close before selected-contract identity from existing local fixture/source evidence. No case reaches a paid option-data or exit-path request gate.
- Option request included: `NO`.
- Exit-path request included: `NO`.
- Schwab authenticated: `NO`.
- Broker/order/account mutation attempted: `NO`.

No paid-data request was created, no cost check was needed, and no data was downloaded.

## Guardrails

No `main.py`, trading logic, Railway/deploy files, broker/account/order code, credentials, `.env`, frozen thresholds, production/live backend, Schwab authentication, data download, option request, exit-path request, proof, profitability claim, readiness claim, promotion, paper eligibility, or live eligibility was changed or created.

## Next

Exact next grouped task: `SAFE_FAST_DAY50_POSITIVE_ENTRY_CLOSED_REQUIREMENT_SCORECARD_RECONCILIATION_CODEX_TASK.md`.

Reason: the four open active-path requirements are now permanently closed with exact failed requirements and no added trade candidates. The next bounded group is scorecard/control reconciliation only.

## Tests

- `python -B -m unittest discover -s tests -p "test_day50_positive_entry_active_path_requirement_regression.py"`: PASS, `8` tests.
- `python -B -m historical_signal_replay.day50_positive_entry_active_path_requirement_regression`: PASS, wrote `4` tested, `0` advanced, `4` permanently closed, `9->9` trade candidates, `5->5` selected contracts, `1->1` eligible entries, `1->1` recorded entries.
