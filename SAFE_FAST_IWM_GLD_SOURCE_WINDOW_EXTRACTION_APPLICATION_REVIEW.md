# SAFE-FAST IWM/GLD Source Window Extraction Application Review

Project day: Day 36
Current baseline commit: `6865c6c Add replacement source row window extractor`
Mode: local docs/evidence review only

## Purpose

This review applies the existing source-window extractor to exact old local IWM/GLD source windows where exact row/window metadata is available.

This review does not update `SAFE_FAST_IWM_GLD_REPLACEMENT_SOURCE_ROW_PACKET.md`, does not create accepted proof, does not classify any replacement candidate as accepted, and does not make any trade decision.

## Tooling Used

- Extractor file used: `watcher_foundation/replacement_source_row_window_extractor.py`
- Extractor API used: `extract_replacement_source_row_window`
- CSV intake helper used: `watcher_foundation/replacement_source_row_csv_intake.py`
- CSV intake helper path used through extractor: `intake_replacement_source_row_csv_text`
- Population gate used: `watcher_foundation/replacement_source_row_packet_population.py`
- Population gate API used: `populate_replacement_source_row_packet_request`

## Source CSV Files Found

- `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv`: found
- `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv`: found

## Source Window Docs Inspected

- `SAFE_FAST_BUILD_STATE.md` latest Day 36 IWM/GLD replacement/source-window sections
- `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md` top rules and latest Day 36 sections
- `SAFE_FAST_IWM_GLD_REPLACEMENT_SOURCE_ROW_REQUEST.md`
- `SAFE_FAST_IWM_GLD_REPLACEMENT_SOURCE_ROW_PACKET.md`
- `SAFE_FAST_IWM_GLD_LOCAL_SOURCE_EXPORT_INSTRUCTION.md`
- `SAFE_FAST_IWM_GLD_LOCAL_SOURCE_ROW_PACKET_POPULATION_REVIEW.md`
- `SAFE_FAST_IWM_GLD_REPLACEMENT_SOURCE_ROW_POPULATION_GATE_APPLICATION_REVIEW.md`
- `SAFE_FAST_IWM_BOUNDED_SOURCE_WINDOW_SELECTION_REVIEW.md`
- `SAFE_FAST_GLD_BOUNDED_SOURCE_WINDOW_SELECTION_REVIEW.md`
- `watcher_foundation/replacement_source_row_window_extractor.py`
- `watcher_foundation/replacement_source_row_csv_intake.py`
- `watcher_foundation/replacement_source_row_packet_population.py`
- `tests/test_replacement_source_row_window_extractor.py`
- `tests/test_replacement_source_row_csv_intake.py`
- `tests/test_replacement_source_row_packet_population.py`

## Exact Windows Processed

| Candidate ID | Old source window ID | Old source sample ID | Source file | Row start | Row end | Source rows found |
| --- | --- | --- | --- | ---: | ---: | ---: |
| `IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001` | `IWM-WINDOW-CONTINUATION-001` | `IWM-SAMPLE-CONTINUATION-001` | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv` | 141 | 210 | 70 |
| `IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002` | `IWM-WINDOW-SESSION-BOUNDARY-001` | `IWM-SAMPLE-SESSION-BOUNDARY-001` | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv` | 190 | 210 | 21 |
| `GLD-REPLACEMENT-IDEAL-CANDIDATE-001` | `GLD-WINDOW-IDEAL-001` | `GLD-SAMPLE-IDEAL-001` | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv` | 204 | 238 | 35 |

Additional exact old IWM window considered but not assigned as the primary seed for a reserved candidate: `IWM-WINDOW-STAGE-DEVELOPING-001`, derived from documented timestamps as rows 148-175. It remains developing/mixed candidate material only.

No second repo-documented GLD Ideal candidate window with an exact row range was found in the targeted docs.

## Candidate Reviews

### IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001

- candidate_id: `IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001`
- symbol: `IWM`
- setup_type: `Continuation`
- old_source_window_id: `IWM-WINDOW-CONTINUATION-001`
- old_source_sample_id: `IWM-SAMPLE-CONTINUATION-001`
- source_file: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv`
- row_start: 141
- row_end: 210
- extraction_status: `source_window_extracted`
- csv_intake_status: `blocked_missing_evidence`
- population_status: `blocked_missing_evidence`
- readiness_status: `missing_evidence_inconclusive`
- source_rows_found: 70
- packet_built: `true`
- evidence_used: old IWM local source CSV rows 141-210; old window/sample metadata from targeted repo docs; extractor output only
- missing_evidence: accepted setup-time source row; accepted trigger evidence; accepted invalidation evidence; accepted freshness/final-signal evidence; accepted blocker/caution evidence; accepted terminal outcome evidence
- rejected_reasons: `missing_required_fields`
- diagnosis: old IWM Continuation source rows can seed future packet work, but they do not include accepted setup-time proof or accepted trigger/invalidation/freshness/blocker/terminal evidence
- likely_cause_candidate: old source CSV contains OHLCV/session/context rows, not accepted replacement packet fields
- next_fix_path: perform bounded row-by-row setup-time evidence review before any acceptance review; do not use after-setup movement to choose proof
- regression_needed: preserve coverage that extracted old windows without accepted evidence remain blocked or inconclusive
- lower_tier_handoff_summary: use rows 141-210 as seed material only; no accepted replacement proof exists for this reserved candidate
- watch_only=true
- no_trade_decision=true
- accepted_proof=false

### IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002

- candidate_id: `IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002`
- symbol: `IWM`
- setup_type: `Continuation`
- old_source_window_id: `IWM-WINDOW-SESSION-BOUNDARY-001`
- old_source_sample_id: `IWM-SAMPLE-SESSION-BOUNDARY-001`
- source_file: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv`
- row_start: 190
- row_end: 210
- extraction_status: `source_window_extracted`
- csv_intake_status: `blocked_missing_evidence`
- population_status: `blocked_missing_evidence`
- readiness_status: `missing_evidence_inconclusive`
- source_rows_found: 21
- packet_built: `true`
- evidence_used: old IWM local source CSV rows 190-210; old session-boundary window/sample metadata from targeted repo docs; extractor output only
- missing_evidence: accepted setup-time source row; accepted trigger evidence; accepted invalidation evidence; accepted freshness/final-signal evidence; accepted blocker/caution evidence; accepted terminal outcome evidence
- rejected_reasons: `missing_required_fields`
- diagnosis: old IWM session-boundary rows can seed future packet work, but session-boundary freshness and accepted Continuation proof remain unconfirmed
- likely_cause_candidate: old source CSV contains bounded OHLCV rows, not accepted session-boundary trigger/freshness proof
- next_fix_path: run bounded row-by-row session-boundary freshness and trigger/invalidation review before any acceptance review
- regression_needed: preserve coverage that session-boundary source rows do not become trade-ready proof without accepted fields
- lower_tier_handoff_summary: use rows 190-210 as seed material only; no accepted replacement proof exists for this reserved candidate
- watch_only=true
- no_trade_decision=true
- accepted_proof=false

### GLD-REPLACEMENT-IDEAL-CANDIDATE-001

- candidate_id: `GLD-REPLACEMENT-IDEAL-CANDIDATE-001`
- symbol: `GLD`
- setup_type: `Ideal`
- old_source_window_id: `GLD-WINDOW-IDEAL-001`
- old_source_sample_id: `GLD-SAMPLE-IDEAL-001`
- source_file: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv`
- row_start: 204
- row_end: 238
- extraction_status: `source_window_extracted`
- csv_intake_status: `blocked_missing_evidence`
- population_status: `blocked_missing_evidence`
- readiness_status: `missing_evidence_inconclusive`
- source_rows_found: 35
- packet_built: `true`
- evidence_used: old GLD local source CSV rows 204-238; old window/sample metadata from targeted repo docs; extractor output only
- missing_evidence: accepted setup-time source row; accepted trigger evidence; accepted invalidation evidence; accepted freshness/final-signal evidence; accepted blocker/caution evidence; accepted terminal outcome evidence
- rejected_reasons: `missing_required_fields`
- diagnosis: old GLD Ideal source rows can seed future packet work, but they do not include accepted setup-time proof or accepted Ideal trigger/invalidation/freshness/blocker/terminal evidence
- likely_cause_candidate: old GLD source CSV contains OHLCV/session/context rows, not accepted replacement packet fields
- next_fix_path: perform bounded GLD Ideal row-by-row setup-time evidence review before any acceptance review
- regression_needed: preserve coverage that extracted old GLD Ideal windows without accepted evidence remain blocked or inconclusive
- lower_tier_handoff_summary: use rows 204-238 as seed material only; no accepted replacement proof exists for this reserved candidate
- watch_only=true
- no_trade_decision=true
- accepted_proof=false

### GLD-REPLACEMENT-IDEAL-CANDIDATE-002

- candidate_id: `GLD-REPLACEMENT-IDEAL-CANDIDATE-002`
- symbol: `GLD`
- setup_type: `Ideal`
- old_source_window_id: unavailable
- old_source_sample_id: unavailable
- source_file: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv`
- row_start: unavailable
- row_end: unavailable
- extraction_status: `unavailable`
- csv_intake_status: `not_run`
- population_status: `unavailable`
- readiness_status: `missing_evidence_inconclusive`
- source_rows_found: 0
- packet_built: `false`
- evidence_used: targeted docs found only `GLD-WINDOW-IDEAL-001` as an exact old GLD Ideal candidate window
- missing_evidence: second exact GLD Ideal source window; accepted setup-time source row; accepted trigger evidence; accepted invalidation evidence; accepted freshness/final-signal evidence; accepted blocker/caution evidence; accepted terminal outcome evidence
- rejected_reasons: none
- diagnosis: no second exact old GLD Ideal window exists in the targeted repo docs, so this reserved candidate remains unavailable
- likely_cause_candidate: old repo docs selected one GLD Ideal candidate window only
- next_fix_path: collect or identify a second bounded GLD Ideal historical 1H RTH window with exact row range and setup-time evidence fields
- regression_needed: preserve coverage that unavailable second GLD Ideal slot remains inconclusive
- lower_tier_handoff_summary: this slot still needs exact source-window evidence before extractor/intake/gate application
- watch_only=true
- no_trade_decision=true
- accepted_proof=false

## Batch Summary

- total: 4
- source_window_extracted: 3
- candidate_seed_ready: 0
- blocked_missing_evidence: 3
- unavailable: 1
- rejected: 0
- accepted_proof_count=0

## Final Conclusion

Three old local source windows can seed a future replacement packet path: `IWM-WINDOW-CONTINUATION-001`, `IWM-WINDOW-SESSION-BOUNDARY-001`, and `GLD-WINDOW-IDEAL-001`.

Those old windows are old sample/window IDs, not exact reserved replacement candidate proofs. They are seed material only. No candidate became `candidate_seed_ready` or `ready_for_packet_build_review` because accepted setup-time trigger, invalidation, freshness/final-signal, blocker/caution, and terminal outcome proof remains missing.

`GLD-REPLACEMENT-IDEAL-CANDIDATE-002` remains unavailable because no second exact old GLD Ideal source window was found in the targeted docs.

The three processed candidates are `blocked_missing_evidence`. No accepted proof was created, `accepted_proof_count=0`, and every candidate remains `watch_only=true` and `no_trade_decision=true`.

IWM Continuation and GLD Ideal remain missing-evidence/inconclusive unless exact accepted proof exists.

Smallest next evidence-backed fix: run a bounded row-by-row setup-time evidence review on the extracted old windows, starting with the clearest extracted IWM Continuation or GLD Ideal seed, and require accepted trigger, invalidation, freshness/final-signal, blocker/caution, and terminal-outcome evidence before any acceptance review.
