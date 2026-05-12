# Repeated-State Duplicate Suppression Fixture Design Review

## Decision

Recommend the first repeated-state duplicate suppression fixture as a **Continuation lifecycle repeated-state** fixture.

This is a design-only decision for Historical Signal Replay v1. It does not create the repeated-state fixture, change runner behavior, change schemas, change replay tests, change signal replay code, touch `main.py`, generate reports, start trade outcome backtesting, model option P&L, add account sizing, add auto-trading, or make live trade decisions.

## Current State

- Three-fixture signal replay support passed.
- Historical Signal Replay v1 represents all three setup types:
  - Continuation
  - Clean Fast Break
  - Ideal
- A Continuation lifecycle fixture exists.
- Lifecycle runner support exists.
- Lifecycle runner output validation passed.

## Why Repeated-State Duplicate Suppression Is Next

The current Continuation lifecycle fixture proves meaningful state changes across the watcher foundation lifecycle:

- `watching_developing`
- `pending_completed_candle_approval`
- `triggered_signal_stage`
- `spent_no_fresh_trigger`

It does not yet prove that repeated same-state observations are suppressed. That proof is required before Continuous Watcher alert behavior because a watcher must avoid treating unchanged observations as new meaningful alerts.

The repeated-state fixture should stay no-hindsight and signal/stage focused. It should prove alert suppression behavior only, not profitability or trade outcomes.

## Recommended First Repeated-State Fixture

The first repeated-state duplicate suppression fixture should be a **Continuation repeated-state duplicate suppression fixture**.

Continuation is the recommended first repeated-state fixture because the existing lifecycle fixture already proves its meaningful state progression. Duplicating each lifecycle state with a repeated same-state observation is the smallest useful next step for proving suppression behavior before Continuous Watcher implementation.

## Required Repeated-State Rows

The fixture should include 8 rows:

1. `watching_developing` first observation
2. `watching_developing` repeated same-state observation
3. `pending_completed_candle_approval` first observation
4. `pending_completed_candle_approval` repeated same-state observation
5. `triggered_signal_stage` first observation
6. `triggered_signal_stage` repeated same-state observation
7. `spent_no_fresh_trigger` first observation
8. `spent_no_fresh_trigger` repeated same-state observation

## Expected Suppression Behavior

- The first observation of a state can be a meaningful alert candidate.
- A repeated same-state observation with the same `duplicate_alert_suppression_key` should not be a new meaningful alert candidate.
- Rows with `state_changed: false`, `trigger_changed: false`, and `blocker_changed: false` should produce no new meaningful alert.
- `duplicate_alert_suppression_key` should remain the same for repeated same-state rows.

## Required Fields To Verify Per Row

Each row should verify:

- `timestamp`
- `symbol`
- `setup_type`
- `setup_state`
- `stage`
- `trigger_state`
- `trigger_level`
- `invalidation`
- `final_verdict`
- `primary_blocker`
- `human_next_step`
- `first_seen`
- `last_seen`
- `state_changed`
- `prior_state`
- `current_state`
- `trigger_changed`
- `blocker_changed`
- `duplicate_alert_suppression_key`
- `meaningful_alert_candidate`
- `duplicate_suppressed`

## Expected Summary Metrics

- `total_rows`: 8
- `unique_duplicate_alert_suppression_keys`: 4
- `meaningful_alert_candidate_count`: 4
- `duplicate_suppressed_count`: 4

## Boundaries

- No trade outcome backtesting.
- No option P&L.
- No account sizing.
- No production.
- No auto-trading.
- No live trade decisions.

## Next Task

Validate repeated-state duplicate suppression fixture shape and decide runner support.
