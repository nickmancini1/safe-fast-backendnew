# SAFE-FAST IWM/GLD Setup-Time Review Completion Worksheet

Project day: Day 37
Current baseline commit: `1736405 Preserve SAFE-FAST holding period rule`
Mode: fillable setup-time review completion worksheet only

## Purpose And Boundary

This worksheet is for completing setup-time review fields only from the existing setup-time review request packets.

This worksheet does not accept proof. `accepted_proof=false` and `accepted_proof_count=0`.

No live trading, live data, alerts, broker/order/account/options/P&L, account sizing, shadow, production, Railway, real money, or live trade decision is authorized.

Completed fields must later be processed through `watcher_foundation/replacement_source_row_setup_time_review_completion.py`.

`ready_for_packet_build_review` is not accepted proof.

## Reviewer Instructions

- `setup_time_source_row_number` must be inside `candidate_review_rows`.
- `after_setup_outcome_window_start` must be after `setup_time_source_row_number`.
- Trigger and invalidation must be accepted setup-time fields, not hindsight.
- Directionally favorable after-setup movement must not count as accepted setup-time proof.
- Unavailable fields must be explicitly marked `UNAVAILABLE`.
- Missing evidence is a blocker, not low confidence.
- If any required field is missing, the candidate remains `blocked_missing_evidence`.
- If all required fields are completed, the candidate may only become `ready_for_packet_build_review` after the completion helper and setup-time review gate pass.
- `ready_for_packet_build_review` is not accepted proof.

## Batch Baseline

- accepted_proof=false
- accepted_proof_count=0
- Three candidates are ready for setup-time review completion.
- `GLD-REPLACEMENT-IDEAL-CANDIDATE-002` remains unavailable.
- IWM Continuation and GLD Ideal remain missing-evidence/inconclusive until exact accepted proof exists.

## IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001

### Candidate Header

- candidate_id: `IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001`
- symbol: `IWM`
- setup_type: `Continuation`
- old_source_window_id: `IWM-WINDOW-CONTINUATION-001`
- old_source_sample_id: `IWM-SAMPLE-CONTINUATION-001`
- source_file_label: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv`
- row_start: 141
- row_end: 210
- candidate_review_rows: rows 141-210
- request_status: `ready_for_setup_time_review_request`
- completion_status: `TO_BE_COMPLETED`
- watch_only=true
- no_trade_decision=true
- accepted_proof=false

### Required Fields To Complete

- setup_time_source_row_number:
- setup_time_timestamp:
- setup_time_row_ohlcv:
- accepted_setup_identity:
- accepted_final_verdict:
- accepted_trigger_state:
- accepted_numeric_trigger:
- accepted_trigger_basis:
- accepted_numeric_invalidation:
- accepted_invalidation_basis:
- accepted_freshness_final_signal_decision:
- accepted_blocker_caution_decision:
- no_hindsight_boundary_statement:
- after_setup_outcome_window_start:
- after_setup_outcome_window_end:

### Lower-Tier Handoff

- what setup appeared:
- what happened after:
- evidence used:
- missing evidence:
- diagnosis:
- likely cause candidate:
- next fix path:
- regression needed:
- lower-tier handoff summary:

### Completion Checklist

- all required fields completed: yes/no
- no-hindsight boundary preserved: yes/no
- watch_only=true: yes/no
- no_trade_decision=true: yes/no
- accepted_proof=false: yes/no
- ready to run through completion intake helper: yes/no

## IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002

### Candidate Header

- candidate_id: `IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002`
- symbol: `IWM`
- setup_type: `Continuation`
- old_source_window_id: `IWM-WINDOW-SESSION-BOUNDARY-001`
- old_source_sample_id: `IWM-SAMPLE-SESSION-BOUNDARY-001`
- source_file_label: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv`
- row_start: 190
- row_end: 210
- candidate_review_rows: rows 190-210
- request_status: `ready_for_setup_time_review_request`
- completion_status: `TO_BE_COMPLETED`
- watch_only=true
- no_trade_decision=true
- accepted_proof=false

### Required Fields To Complete

- setup_time_source_row_number:
- setup_time_timestamp:
- setup_time_row_ohlcv:
- accepted_setup_identity:
- accepted_final_verdict:
- accepted_trigger_state:
- accepted_numeric_trigger:
- accepted_trigger_basis:
- accepted_numeric_invalidation:
- accepted_invalidation_basis:
- accepted_freshness_final_signal_decision:
- accepted_blocker_caution_decision:
- no_hindsight_boundary_statement:
- after_setup_outcome_window_start:
- after_setup_outcome_window_end:

### Lower-Tier Handoff

- what setup appeared:
- what happened after:
- evidence used:
- missing evidence:
- diagnosis:
- likely cause candidate:
- next fix path:
- regression needed:
- lower-tier handoff summary:

### Completion Checklist

- all required fields completed: yes/no
- no-hindsight boundary preserved: yes/no
- watch_only=true: yes/no
- no_trade_decision=true: yes/no
- accepted_proof=false: yes/no
- ready to run through completion intake helper: yes/no

## GLD-REPLACEMENT-IDEAL-CANDIDATE-001

### Candidate Header

- candidate_id: `GLD-REPLACEMENT-IDEAL-CANDIDATE-001`
- symbol: `GLD`
- setup_type: `Ideal`
- old_source_window_id: `GLD-WINDOW-IDEAL-001`
- old_source_sample_id: `GLD-SAMPLE-IDEAL-001`
- source_file_label: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv`
- row_start: 204
- row_end: 238
- candidate_review_rows: rows 204-238
- request_status: `ready_for_setup_time_review_request`
- completion_status: `TO_BE_COMPLETED`
- watch_only=true
- no_trade_decision=true
- accepted_proof=false

### Required Fields To Complete

- setup_time_source_row_number:
- setup_time_timestamp:
- setup_time_row_ohlcv:
- accepted_setup_identity:
- accepted_final_verdict:
- accepted_trigger_state:
- accepted_numeric_trigger:
- accepted_trigger_basis:
- accepted_numeric_invalidation:
- accepted_invalidation_basis:
- accepted_freshness_final_signal_decision:
- accepted_blocker_caution_decision:
- no_hindsight_boundary_statement:
- after_setup_outcome_window_start:
- after_setup_outcome_window_end:

### Lower-Tier Handoff

- what setup appeared:
- what happened after:
- evidence used:
- missing evidence:
- diagnosis:
- likely cause candidate:
- next fix path:
- regression needed:
- lower-tier handoff summary:

### Completion Checklist

- all required fields completed: yes/no
- no-hindsight boundary preserved: yes/no
- watch_only=true: yes/no
- no_trade_decision=true: yes/no
- accepted_proof=false: yes/no
- ready to run through completion intake helper: yes/no

## GLD-REPLACEMENT-IDEAL-CANDIDATE-002

### Candidate Header

- candidate_id: `GLD-REPLACEMENT-IDEAL-CANDIDATE-002`
- symbol: `GLD`
- setup_type: `Ideal`
- old_source_window_id: `UNAVAILABLE`
- old_source_sample_id: `UNAVAILABLE`
- source_file_label: `UNAVAILABLE`
- row_start: `UNAVAILABLE`
- row_end: `UNAVAILABLE`
- candidate_review_rows: `UNAVAILABLE`
- request_status: `unavailable`
- completion_status: `UNAVAILABLE`
- watch_only=true
- no_trade_decision=true
- accepted_proof=false

Exact second GLD Ideal window/range is unavailable unless future repo-backed evidence supplies it. This worksheet does not create fake row ranges.

### Required Fields To Complete

- setup_time_source_row_number: `UNAVAILABLE`
- setup_time_timestamp: `UNAVAILABLE`
- setup_time_row_ohlcv: `UNAVAILABLE`
- accepted_setup_identity: `UNAVAILABLE`
- accepted_final_verdict: `UNAVAILABLE`
- accepted_trigger_state: `UNAVAILABLE`
- accepted_numeric_trigger: `UNAVAILABLE`
- accepted_trigger_basis: `UNAVAILABLE`
- accepted_numeric_invalidation: `UNAVAILABLE`
- accepted_invalidation_basis: `UNAVAILABLE`
- accepted_freshness_final_signal_decision: `UNAVAILABLE`
- accepted_blocker_caution_decision: `UNAVAILABLE`
- no_hindsight_boundary_statement: `UNAVAILABLE`
- after_setup_outcome_window_start: `UNAVAILABLE`
- after_setup_outcome_window_end: `UNAVAILABLE`

### Lower-Tier Handoff

- what setup appeared: `UNAVAILABLE`
- what happened after: `UNAVAILABLE`
- evidence used: targeted request packet and extraction reviews found no second exact GLD Ideal source window.
- missing evidence: second exact GLD Ideal source window/range and all setup-time review completion fields.
- diagnosis: no setup-time review completion can begin for this reserved slot until exact source-window evidence exists.
- likely cause candidate: repo-backed old GLD Ideal evidence provides only `GLD-WINDOW-IDEAL-001`.
- next fix path: collect or identify a second exact bounded GLD Ideal 1H RTH source window with setup-time review fields.
- regression needed: preserve coverage that unavailable second GLD Ideal slots remain unavailable.
- lower-tier handoff summary: no lower-tier setup-time completion work can begin until exact repo-backed source-window evidence exists.

### Completion Checklist

- all required fields completed: no
- no-hindsight boundary preserved: yes
- watch_only=true: yes
- no_trade_decision=true: yes
- accepted_proof=false: yes
- ready to run through completion intake helper: no

## Worksheet Conclusion

This worksheet prepares evidence collection only. It does not accept setup-time rows, trigger, invalidation, freshness, blockers, terminal outcomes, profitability, trade readiness, live/shadow readiness, or production readiness.

The three available candidates may be filled and then processed through `watcher_foundation/replacement_source_row_setup_time_review_completion.py`. `GLD-REPLACEMENT-IDEAL-CANDIDATE-002` remains unavailable until future repo-backed evidence supplies an exact second GLD Ideal source window and row range.
