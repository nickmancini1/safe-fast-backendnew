# SAFE-FAST Day 50 Positive-Entry Active-Path Rule Evidence Repair Result

## Baseline

- Branch: `main`.
- Current task file executed: `SAFE_FAST_DAY50_POSITIVE_ENTRY_ACTIVE_PATH_RULE_EVIDENCE_REPAIR_CODEX_TASK.md`.
- Required startup files read first: `SAFE_FAST_BUILD_STATE.md`, Day 50 trade-candidate rule-gap closeout result/JSON, Day 50 contract-selected missing-evidence result/JSON, rule-family decision table, rule decision survival map, data-source registry, dashboard, and rule index.
- Source of truth: Day 50 positive-entry trade-candidate rule-gap closeout only.
- Targeted group: first stage not reached `TRADE_CANDIDATE`.
- QQQ Clean Fast Break 001 was preserved as regression-only and was not rerun as a live candidate.
- QQQ Ideal was preserved as `replace` / outside the narrowed Ideal path.
- The contract-selected missing-evidence closeout remained preserved with `0` additional entries.

## Fixed

- Added bounded active-path repair builder: `historical_signal_replay/day50_positive_entry_active_path_rule_evidence_repair.py`.
- Added machine-readable repair result: `historical_signal_replay/results/day50_positive_entry_active_path_rule_evidence_repair.json`.
- Added focused repair tests: `tests/test_day50_positive_entry_active_path_rule_evidence_repair.py`.
- Created exact next grouped task: `SAFE_FAST_DAY50_POSITIVE_ENTRY_REMAINING_EVIDENCE_GAP_CLOSEOUT_CODEX_TASK.md`.
- Updated control documents: `SAFE_FAST_BUILD_STATE.md`, `SAFE_FAST_PROJECT_DASHBOARD.md`, `SAFE_FAST_PROJECT_RULE_INDEX.md`, and `SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt`.

## Repair Result

- Affected `TRADE_CANDIDATE` active-path cases repaired into exact evidence-requirement records: `4`.
- Accepted active-path rule/evidence records created: `4`.
- Affected cases selected contracts before repair: `0`.
- Affected cases selected contracts after repair: `0`.
- Affected cases entry-eligible before repair: `0`.
- Affected cases entry-eligible after repair: `0`.
- Affected cases entries recorded before repair: `0`.
- Affected cases entries recorded after repair: `0`.
- Additional entries established: `0`.
- Deterministic comparison: `PASS`; first and second hashes matched.

## Before And After Batch Totals

| Metric | Before repair | After repair |
| --- | ---: | ---: |
| Trade candidates | `9` | `9` |
| Selected contracts | `5` | `5` |
| Eligible entries | `1` | `1` |
| Recorded entries | `1` | `1` |

## Repaired Active-Path Evidence Records

| Candidate | Exact blocker | Field/source/dataset/calculator/window | Repair result |
| --- | --- | --- | --- |
| `first_real_gld_clean_fast_break_replay_v1_fixture` | `fresh_or_spent_unconfirmed` | `freshness_final_signal_state`; `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv`; SAFE-FAST local grouped lifecycle fixture / `signal_replay_input_v1` and `signal_replay_output_v1`; `historical_signal_replay.day48_positive_trade_capture_funnel`; `2026-05-08T15:30:00-04:00`. | Exact active-path requirement record created for a tested GLD Clean Fast Break fresh/spent rule; still blocks `TRADE_CANDIDATE`. |
| `first_real_gld_ideal_replay_v1_fixture` | `fresh_or_spent_unconfirmed` | `freshness_final_signal_state`; `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv`; SAFE-FAST local grouped lifecycle fixture / `signal_replay_input_v1` and `signal_replay_output_v1`; `historical_signal_replay.day48_positive_trade_capture_funnel`; `2026-05-08T15:30:00-04:00`. | Exact active-path requirement record created for a tested GLD Ideal fresh/spent rule; still blocks `TRADE_CANDIDATE`. |
| `first_real_iwm_continuation_replay_v1_fixture` | `prior_completed_shelf_break_spent_TO_REVIEW` | `prior_completed_shelf_break_spent_state`; `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv`; SAFE-FAST local grouped lifecycle fixture / `signal_replay_input_v1` and `signal_replay_output_v1`; `historical_signal_replay.day48_positive_trade_capture_funnel`; `2026-05-01T15:30:00-04:00`. | Exact active-path requirement record created for IWM Continuation shelf-break spent/session-boundary freshness; still blocks `TRADE_CANDIDATE`. |
| `first_real_iwm_ideal_replay_v1_fixture` | `fresh_or_spent_unconfirmed` | `freshness_final_signal_state`; `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv`; SAFE-FAST local grouped lifecycle fixture / `signal_replay_input_v1` and `signal_replay_output_v1`; `historical_signal_replay.day48_positive_trade_capture_funnel`; `2026-05-14T15:30:00-04:00`. | Exact active-path requirement record created for a tested IWM Ideal fresh/spent rule; still blocks `TRADE_CANDIDATE`. |

## Scorecard

- `VALID_TRADE_CAPTURED`: `1`.
- `TRUE_NO_TRADE`: `4`.
- `MISSING_DATA`: `6`.
- `MISSED_VALID_TRADE`: `0`.
- `INVALID_TRADE_ALLOWED`: `0`.
- `UNRESOLVED`: `4`.
- Additional entries: `0`.
- Closed safety rejections rerun as live candidates: `0`.
- Closed setup-source candidates reopened: `0`.
- Rejected intake rows replayed: `0`.

## Cost And Scope

- Checked cost: `NOT_AVAILABLE`.
- Actual billed cost: `NOT_AVAILABLE`.
- Credential used: `NO`.
- Reason: the repair names active-path rule/evidence requirements from existing local fixture/source evidence. No affected case reaches selected-contract identity, and no paid option or exit request is valid.
- Option request included: `NO`.
- Exit-path request included: `NO`.
- Schwab authenticated: `NO`.
- Broker/order/account mutation attempted: `NO`.

No paid-data request was created, no cost check was needed, and no data was downloaded.

## Guardrails

No `main.py`, trading logic, Railway/deploy files, broker/account/order code, credentials, `.env`, frozen thresholds, production/live backend, Schwab authentication, data download, option request, exit-path request, proof, profitability claim, readiness claim, promotion, paper eligibility, or live eligibility was changed or created.

## Next

Exact next grouped task: `SAFE_FAST_DAY50_POSITIVE_ENTRY_REMAINING_EVIDENCE_GAP_CLOSEOUT_CODEX_TASK.md`.

Reason: the active-path evidence records are now explicit for the affected `TRADE_CANDIDATE` blockers, but no additional selected contracts or entries were established. The next bounded group is remaining evidence-gap closeout without scans, downloads, or rule weakening.

## Tests

- `python -B -m unittest discover -s tests -p "test_day50_positive_entry_active_path_rule_evidence_repair.py"`: PASS, `9` tests.
- `python -B -m historical_signal_replay.day50_positive_entry_active_path_rule_evidence_repair`: PASS, wrote `4` repaired cases, `9->9` trade candidates, `5->5` selected contracts, `1->1` eligible entries, `1->1` recorded entries.
- `python -B -m unittest discover -s tests -p "test_day50_positive_entry_trade_candidate_rule_gap_closeout.py"`: PASS, `7` tests.
- `python -B -m historical_signal_replay.day50_positive_entry_trade_candidate_rule_gap_closeout`: PASS, wrote `4` affected cases, `5` selected contracts, `1` eligible entry, `1` recorded entry, `0` additional entries.
- `python -B -m unittest discover -s tests -p "test_day50_positive_entry_contract_selected_missing_evidence.py"`: PASS, `7` tests.
- `python -B -m historical_signal_replay.day50_positive_entry_contract_selected_missing_evidence`: PASS, wrote `2` fresh quote cases, `1` stale case, `0` additional entries.
- `python -B -m unittest discover -s tests -p "test_day50_positive_entry_selected_contract_blocker_closeout.py"`: PASS, `6` tests.
- `python -B -m historical_signal_replay.day50_positive_entry_selected_contract_blocker_closeout`: PASS, wrote `4` failed before entry, `4` affected cases rerun, `0` additional entries established.
- `python -B -m unittest discover -s tests -p "test_day50_evidence_backed_positive_entry_testing_batch.py"`: PASS, `7` tests.
- `python -B -m historical_signal_replay.day50_evidence_backed_positive_entry_testing_batch`: PASS, wrote `13` setup-qualified, `9` trade candidates, `5` selected contracts, `1` eligible entry, `1` recorded entry.
- Required Day 50 dependency tests/builders: PASS for accepted setup evidence replay-after-intake closeout, accepted setup evidence replay-after-intake, accepted complete setup evidence intake, post-closure expansion, exact setup-source closure, source-resolution, and data-source registry.
- Day 48 positive-trade funnel regression: PASS twice, each wrote `15` candidates, `1` valid captured, `4` true no-trades, `6` missing-data cases.
- Relevant positive-entry/family/stage/session tests: PASS for Day 49 positive-entry candidate expansion, Day 49 setup-field completion, Day 49 setup-time, Day 48 actual grouped three-family replay, Continuation starter coverage, Continuation option-context request validator, grouped three-family coverage expansion, grouped three-family expansion after Continuation, and candidate freshness blocker rule gate.
- Contract-selection and quote-freshness tests: PASS for CFB contract selector, CFB lifecycle calculator, execution context calculator, and context caution calculator.
- Evidence and bridge checks: PASS for `watcher_foundation.day49_positive_entry_setup_evidence_completion_validator`, `watcher_foundation.source_evidence_work_package_content_validator`, `watcher_foundation.source_evidence_package_to_intake_bridge`, `watcher_foundation.source_evidence_gap_scanner`, `test_day49_positive_entry_setup_evidence_completion.py`, `test_source_evidence_work_package_content_validator.py`, `test_source_evidence_package_to_intake_bridge.py`, `test_source_evidence_package_intake.py`, `test_source_evidence_acquisition_validator.py`, and `test_source_evidence_gap_scanner.py`.
- Future-chat consistency tests: PASS for `test_day48_positive_trade_handoff_consistency.py` and `test_day47_to_day90_audit_consistency.py`.
- `git --no-pager diff --check`: PASS, with normal CRLF warnings only.
