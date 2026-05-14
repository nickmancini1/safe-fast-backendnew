# Second Real Historical Replay v1 Fixture Creation Review

## Scope

- **Baseline:** patch8
- **Latest local commit noted for this task:** `08458a1 Add second real historical replay fixture design`
- **Design review used:** `historical_signal_replay/SECOND_REAL_HISTORICAL_REPLAY_V1_FIXTURE_DESIGN_REVIEW.md`
- **Source CSV used:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`
- **Fixture created:** `historical_signal_replay/fixtures/second_real_spy_ideal_replay_v1_fixture.json`
- **Purpose:** create the second real historical replay v1 fixture from the approved Ideal design.

## Creation Status

- **Fixture creation status:** PASS
- **Supported fixture shape:** yes; lifecycle-style fixture rows with `input` and `expected_output_shape`
- **Reason:** the existing Historical Signal Replay v1 lifecycle fixture shape supports cumulative no-hindsight source rows and expected signal/stage/lifecycle output assertions without code or schema changes.

## Fixture Summary

- **Symbol:** SPY
- **Timeframe:** 1h_rth
- **Timestamp range:** 2026-05-06T09:30:00-04:00 through 2026-05-13T14:30:00-04:00
- **Setup family:** Ideal
- **Fixture row count:** 6
- **Source window row count:** 41

## Lifecycle / Stage Sequence Result

- **Lifecycle/stage sequence result:** PASS
1. `watching_ideal_impulse_context`
2. `watching_ideal_pullback_retest_developing`
3. `watching_ideal_retest_hold_unconfirmed`
4. `ideal_retest_recovery_confirmation_candidate`
5. `ideal_triggered_signal_stage_candidate`
6. `ideal_follow_through_no_fresh_trigger`

## No-Hindsight Result

- **No-hindsight result:** PASS
- Each fixture row includes only validated SPY source candles available at or before that row timestamp.
- Row 1 does not use the later 2026-05-12 pullback or 2026-05-13 trigger/follow-through.
- Rows 2 and 3 do not use later 2026-05-12 recovery bars or 2026-05-13 highs.
- Row 4 uses bars only through the 2026-05-12 close and does not use 2026-05-13 follow-through.
- Row 5 uses bars only through the completed 2026-05-13T11:30:00-04:00 bar.
- Row 6 acknowledges no fresh first trigger after follow-through without asserting profitability, option behavior, trade outcome, execution, or account-sizing conclusions.

## Boundary Result

- **Boundary result:** PASS
- **OHLCV changed:** no
- **Fabricated market data:** no
- **`main.py` changed:** no
- **`dxlink_candles.py` changed:** no
- **Runner code changed:** no
- **Schemas changed:** no
- **Replay tests changed:** no
- **Generated reports changed:** no
- **Backtesting started:** no
- **Option P&L modeled:** no
- **Account sizing added:** no
- **Broker/order/execution logic added:** no
- **Auto-trading added:** no

## Validation Commands

- `python -m json.tool historical_signal_replay/fixtures/second_real_spy_ideal_replay_v1_fixture.json`
- `python -m json.tool historical_signal_replay/schemas/signal_replay_input_v1.schema.json`
- `python -m json.tool historical_signal_replay/schemas/signal_replay_output_v1.schema.json`
- `python -B historical_signal_replay/run_signal_replay.py`
- `python -B replay/test_on_demand_stage_messages.py`
- `python -B replay/validate_fixtures.py`
- `python -B replay/run_replay.py`
- all `replay/test_on_demand_*contract.py` files

## Validation Status

- **Fixture JSON validation result:** PASS
- **Schema JSON validation result:** PASS
- **Source OHLCV integrity result:** PASS; fixture candles match the validated source CSV rows and each lifecycle row ends at its declared timestamp
- **Runner result:** PASS
- **Contract tests result:** PASS; all `replay/test_on_demand_*contract.py` files passed locally
- **Stage-message result:** PASS
- **Fixture validation result:** PASS
- **Full replay result:** PASS; 16/16 passed, `local_fixture_engine=16`, `placeholder_scaffold=0`

## Recommended Next Task

Validate second-real fixture content and decide separately whether runner report emission for the second-real fixture is desired, without starting backtesting, option P&L, account sizing, watcher implementation, auto-trading, or live trade decisions.
