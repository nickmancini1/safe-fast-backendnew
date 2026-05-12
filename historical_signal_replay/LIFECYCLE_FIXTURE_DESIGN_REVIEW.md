# Historical Signal Replay v1 Lifecycle Fixture Design Review

## Decision

Recommend the first lifecycle fixture as a multi-row **Continuation lifecycle** fixture.

This is a design-only decision for Historical Signal Replay v1. It does not create lifecycle fixture implementation, runner code, schema changes, production behavior, auto-trading behavior, live trade decisions, trade outcome backtesting, option P&L modeling, or account sizing.

## Current State

- Three-fixture signal replay support passed.
- Historical Signal Replay v1 currently represents all three setup types:
  - Continuation
  - Clean Fast Break
  - Ideal
- Current replay coverage proves single-row signal/stage output across the represented setup types.
- Lifecycle behavior over multiple timestamps is not yet proven.

## Why Lifecycle Is Next

Lifecycle fixture coverage is the next useful Historical Signal Replay v1 expansion because it proves state transitions over time instead of only proving isolated signal rows.

This prepares the Continuous Watcher foundation by defining the minimum row sequence and fields needed for watch-only lifecycle memory. It also helps shape duplicate alert suppression design before any continuous watcher implementation exists.

The lifecycle fixture should stay signal/stage focused. It should answer whether the same setup progresses through expected states over time, not whether a trade would have made money.

## Recommended First Lifecycle Fixture

The first lifecycle fixture should be a multi-row **Continuation lifecycle** fixture.

Continuation is the recommended first lifecycle because its expected path naturally exercises the watcher foundation:

- developing structure before confirmation
- pending completed-candle approval after an intrabar or incomplete trigger condition
- triggered or signal-stage state once the trigger condition is confirmed
- spent / no fresh trigger state after the meaningful trigger window has passed

That progression is more useful for lifecycle and duplicate alert suppression design than adding another isolated setup-type fixture.

## Required Lifecycle Rows

The first Continuation lifecycle fixture should include rows representing:

1. `watching` / `developing`
2. `pending_completed_candle_approval`
3. `triggered` or `signal_stage`
4. `spent` / `no fresh trigger`

The row sequence should be no-hindsight: each row should only use information available at that timestamp.

## Required Fields To Verify Per Row

Each lifecycle row should verify:

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

## Duplicate Alert Suppression Expectation

Repeated rows with the same meaningful lifecycle state should not create a new meaningful alert.

State, trigger, or blocker changes should be alert candidates. The lifecycle fixture should make those changes explicit enough that future Continuous Watcher work can distinguish meaningful changes from repeated same-state observations.

## Boundaries

- No trade outcome backtesting.
- No option P&L.
- No account sizing.
- No production behavior.
- No auto-trading.
- No live trade decisions.

## Next Task

Add lifecycle runner support for the validated multi-row lifecycle fixture shape only.
