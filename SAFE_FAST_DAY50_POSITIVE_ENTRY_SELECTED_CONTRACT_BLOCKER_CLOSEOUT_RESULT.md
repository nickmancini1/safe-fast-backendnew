# SAFE-FAST Day 50 Positive-Entry Selected-Contract Blocker Closeout Result

## Baseline

- Branch: `main`.
- Current task file executed: `SAFE_FAST_DAY50_POSITIVE_ENTRY_SELECTED_CONTRACT_BLOCKER_CLOSEOUT_CODEX_TASK.md`.
- Required startup files read first: `SAFE_FAST_BUILD_STATE.md`, Day 50 evidence-backed positive-entry batch result/JSON, accepted setup evidence replay-after-intake closeout result/JSON, Day 48 positive-trade funnel result/JSON, dashboard, rule index, and data-source registry.
- Source of truth: Day 50 evidence-backed positive-entry batch only.
- Confirmed QQQ safety rejection remained closed as regression-only and was not rerun as a live candidate.

## Fixed

- Added selected-contract blocker closeout builder: `historical_signal_replay/day50_positive_entry_selected_contract_blocker_closeout.py`.
- Added machine-readable closeout result: `historical_signal_replay/results/day50_positive_entry_selected_contract_blocker_closeout.json`.
- Added focused closeout tests: `tests/test_day50_positive_entry_selected_contract_blocker_closeout.py`.
- Created exact next grouped task: `SAFE_FAST_DAY50_POSITIVE_ENTRY_CONTRACT_SELECTED_MISSING_EVIDENCE_CODEX_TASK.md`.
- Updated control documents: `SAFE_FAST_BUILD_STATE.md`, `SAFE_FAST_PROJECT_DASHBOARD.md`, `SAFE_FAST_PROJECT_RULE_INDEX.md`, and `SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt`.

## Closeout Result

- Selected contracts in batch: `5`.
- Selected contracts that failed before entry: `4`.
- Affected cases rerun from existing local controls: `4`.
- Additional entries established: `0`.
- Affected cases entry-eligible after rerun: `0`.
- Affected cases entries recorded after rerun: `0`.
- Deterministic comparison: `PASS`; first and second hashes matched.

## Affected Selected Contracts

| Candidate | Family | Underlying | Selected contract | First blocker stage | Exact blocker | Classification |
| --- | --- | --- | --- | --- | --- | --- |
| `first_real_spy_continuation_replay_v1_fixture` | Continuation | SPY | `SPY   260514C00720000` | `ENTRY_ELIGIBLE` | `quote_age_above_5_minutes` | `TRUE_NO_TRADE` |
| `second_real_spy_ideal_replay_v1_fixture` | Ideal | SPY | `SPY   260527C00745000` | `ENTRY_ELIGIBLE` | `quote_age_above_5_minutes` | `TRUE_NO_TRADE` |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | Clean Fast Break | SPY | selected-contract replay row | `ENTRY_ELIGIBLE` | `quote_age_above_5_minutes` | `TRUE_NO_TRADE` |
| `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | Clean Fast Break | QQQ | selected-contract replay row | `ENTRY_ELIGIBLE` | `quote_age_above_5_minutes` | `TRUE_NO_TRADE_REGRESSION_ONLY` |

## Exact Blocker Details

- Blocking field: `option_quote_freshness`.
- Source: Databento historical options via existing local selected-contract evidence.
- Dataset/schema/API/calculator: Databento `OPRA.PILLAR` quote freshness through local replay and `historical_signal_replay.execution_context_calculator` / `historical_signal_replay.cfb_backtest_runner`.
- Frozen failure rule: quote age above `5` minutes blocks `ENTRY_ELIGIBLE` and `ENTRY_RECORDED`.
- SPY Continuation quote-age evidence: `3790.746258` seconds, selected contract `SPY   260514C00720000`.
- SPY Ideal quote-age evidence: `442.633927` seconds, selected contract `SPY   260527C00745000`.
- SPY CFB 003 timestamp evidence: entry time `2026-04-15T18:30:00+00:00`, selected quote time `2026-04-15T18:22:33.366710+00:00`.
- QQQ CFB 001 timestamp evidence: entry time `2026-04-13T16:30:00+00:00`, selected quote time `2026-04-13T16:06:30.640301+00:00`; preserved only as regression-only true no-trade.

## Scorecard

- `VALID_TRADE_CAPTURED`: `1`.
- `TRUE_NO_TRADE`: `4`.
- `MISSING_DATA`: `6`.
- `MISSED_VALID_TRADE`: `0`.
- `INVALID_TRADE_ALLOWED`: `0`.
- `UNRESOLVED`: `4`.
- Regression-only closed safety rejections: `1`.
- Closed safety rejections rerun as live candidates: `0`.
- Closed setup-source candidates reopened: `0`.
- Rejected intake rows replayed: `0`.

## Cost And Scope

- Checked cost: `NOT_AVAILABLE`.
- Actual billed cost: `NOT_AVAILABLE`.
- Credential used: `NO`.
- Databento downloaded: `NO`.
- Raw vendor data changed: `NO`.
- Option request included: `NO`.
- Exit-path request included: `NO`.
- Schwab authenticated: `NO`.
- Broker/order/account mutation attempted: `NO`.

No paid-data request was created because the affected selected contracts already have local selected-contract evidence and all four fail before entry on the frozen quote-age gate.

## Guardrails

No `main.py`, trading logic, Railway/deploy files, broker/account/order code, credentials, `.env`, frozen thresholds, production/live backend, Schwab authentication, data download, option request, exit-path request, proof, profitability claim, readiness claim, promotion, paper eligibility, or live eligibility was changed or created.

## Next

Exact next grouped task: `SAFE_FAST_DAY50_POSITIVE_ENTRY_CONTRACT_SELECTED_MISSING_EVIDENCE_CODEX_TASK.md`.

Reason: this closeout established `0` additional entries from selected contracts that failed before entry. The remaining bounded positive-entry surface is the Day 50 batch's `CONTRACT_SELECTED` blocker group with exact `missing_setup_time_selected_option_evidence`.

## Tests

- `python -B -m unittest discover -s tests -p "test_day50_positive_entry_selected_contract_blocker_closeout.py"`: PASS, `6` tests.
- `python -B -m historical_signal_replay.day50_positive_entry_selected_contract_blocker_closeout`: PASS, wrote `4` failed before entry, `4` affected cases rerun, `0` additional entries established.
- `python -B -m unittest discover -s tests -p "test_day50_evidence_backed_positive_entry_testing_batch.py"`: PASS, `7` tests.
- `python -B -m historical_signal_replay.day50_evidence_backed_positive_entry_testing_batch`: PASS, wrote `13` setup-qualified, `9` trade candidates, `5` selected contracts, `1` eligible entry, `1` recorded entry.
- `python -B -m unittest discover -s tests -p "test_day50_accepted_setup_evidence_replay_after_intake_closeout.py"`: PASS, `7` tests.
- `python -B -m historical_signal_replay.day50_accepted_setup_evidence_replay_after_intake_closeout`: PASS, wrote `1` safety rejection closed, `0` trade candidates, `0` evidence/harness problems.
- `python -B -m unittest discover -s tests -p "test_day50_accepted_setup_evidence_replay_after_intake.py"`: PASS, `7` tests.
- `python -B -m historical_signal_replay.day50_accepted_setup_evidence_replay_after_intake`: PASS, wrote `1` replayed, `0` trade candidates, `1` legitimate safety rejection, `0` evidence/harness problems.
- `python -B -m unittest discover -s tests -p "test_day50_accepted_complete_setup_evidence_intake.py"`: PASS, `7` tests.
- `python -B -m historical_signal_replay.day50_accepted_complete_setup_evidence_intake`: PASS, wrote `1` accepted, `0` trade candidates, `1` blocked by accepted caution fail.
- `python -B -m unittest discover -s tests -p "test_day50_positive_entry_expansion_after_setup_source_closure.py"`: PASS, `6` tests.
- `python -B -m historical_signal_replay.day50_positive_entry_expansion_after_setup_source_closure`: PASS, wrote `0` eligible new candidates, `0` trade candidates, `0` valid captured.
- `python -B -m unittest discover -s tests -p "test_day50_exact_setup_source_evidence_completion.py"`: PASS, `5` tests.
- `python -B -m historical_signal_replay.day50_exact_setup_source_evidence_completion`: PASS, wrote `4` reviewed, `4` closed, `0` trade candidates.
- `python -B -m unittest discover -s tests -p "test_day50_required_setup_source_resolution.py"`: PASS, `5` tests.
- `python -B -m historical_signal_replay.day50_required_setup_source_resolution`: PASS, wrote `4` exact requests, `3` source conflicts excluded, `0` trade candidates.
- `python -B -m unittest discover -s tests -p "test_safe_fast_data_source_registry.py"`: PASS, `10` tests.
- `python -B -m historical_signal_replay.day48_positive_trade_capture_funnel`: PASS twice, each wrote `15` candidates, `1` valid captured, `4` true no-trades, `6` missing-data cases.
- `python -B -m unittest discover -s tests -p "test_day48_positive_trade_capture_funnel.py"`: PASS, `4` tests.
- Relevant positive-entry/family/stage/session tests: PASS for `test_day49_positive_entry_candidate_expansion.py`, `test_day49_grouped_positive_entry_setup_field_completion.py`, `test_day49_grouped_positive_entry_setup_time.py`, `test_day48_actual_grouped_three_family_replay.py`, `test_day48_continuation_starter_coverage.py`, `test_day48_grouped_three_family_coverage_expansion.py`, and `test_day48_grouped_three_family_expansion_after_continuation.py`.
- Relevant contract/quote/context tests: PASS for `test_cfb_contract_selector.py`, `test_cfb_lifecycle_calculator.py`, `test_execution_context_calculator.py`, and `test_context_caution_calculator.py`.
- Evidence and bridge tests: PASS for `watcher_foundation.day49_positive_entry_setup_evidence_completion_validator`, `watcher_foundation.source_evidence_work_package_content_validator`, `watcher_foundation.source_evidence_package_to_intake_bridge`, `watcher_foundation.source_evidence_gap_scanner`, `test_day49_positive_entry_setup_evidence_completion.py`, `test_source_evidence_work_package_content_validator.py`, `test_source_evidence_package_to_intake_bridge.py`, `test_source_evidence_package_intake.py`, `test_source_evidence_acquisition_validator.py`, and `test_source_evidence_gap_scanner.py`.
- Direct on-demand Ideal/CFB/Continuation/stage/session scripts: PASS, `23` files.
- Future-chat consistency tests: PASS for `test_day48_positive_trade_handoff_consistency.py` and `test_day47_to_day90_audit_consistency.py`.
- `git --no-pager diff --check`: PASS, with normal CRLF warnings only.
