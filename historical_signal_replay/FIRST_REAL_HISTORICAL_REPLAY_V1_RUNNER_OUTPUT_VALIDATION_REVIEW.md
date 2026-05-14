# First Real Historical Replay v1 Runner Output Validation Review

## Scope

- **Objective:** validate first-real SPY Continuation fixture runner inclusion/support.
- **Fixture:** `historical_signal_replay/fixtures/first_real_spy_continuation_replay_v1_fixture.json`
- **Runner:** `historical_signal_replay/run_signal_replay.py`
- **Boundary:** signal/stage/lifecycle replay output only; no profitability, trade outcome backtesting, option P&L, account sizing, broker/order/execution, auto-trading, or live trade decisions.

## Runner support

- **First-real fixture included:** yes
- **Runner code changed:** yes; `historical_signal_replay/run_signal_replay.py` now emits first-real reports for this fixture only.
- **Generated reports changed:** yes; first-real signal log, summary, and regression candidate files are emitted under `historical_signal_replay/reports/`.

## Generated reports

- `historical_signal_replay/reports/first_real_spy_continuation_replay_v1_signal_log.jsonl`
- `historical_signal_replay/reports/first_real_spy_continuation_replay_v1_summary.json`
- `historical_signal_replay/reports/first_real_spy_continuation_replay_v1_regression_candidates.json`

## Validation results

- **Validation status:** PASS
- **First-real signal log exists:** yes
- **First-real signal log row count:** 6
- **First-real summary `total_rows`:** 6
- **Symbol result:** PASS; `SPY`
- **Setup family count result:** PASS; `Continuation: 6`
- **Stage count result:** PASS; `developing_pullback_shelf: 1`, `developing_shelf_no_trigger: 2`, `opening_probe_no_completed_approval: 1`, `triggered_signal_stage_candidate: 1`, `spent_or_follow_through_no_fresh_trigger: 1`
- **Lifecycle/stage sequence result:** PASS; `developing_pullback_shelf`, `developing_shelf_no_trigger`, `developing_shelf_no_trigger`, `opening_probe_no_completed_approval`, `triggered_signal_stage_candidate`, `spent_or_follow_through_no_fresh_trigger`
- **Fixture row-name sequence result:** PASS; `watching_developing_pullback_shelf`, `watching_developing_shelf_no_trigger`, `watching_developing_repeated_same_state`, `opening_probe_no_completed_approval`, `triggered_signal_stage_candidate`, `spent_or_follow_through_no_fresh_trigger`
- **Boundary result:** PASS; generated reports remain signal/stage/lifecycle only and make no profitability, backtesting, option P&L, account sizing, execution, auto-trading, or live trade decision claims.

## Summary counts

- **Final verdict counts:** `NO_TRADE: 4`, `PENDING: 1`, `TRADE: 1`
- **Blocker counts:** `no_valid_trigger: 3`, `completed_candle_approval_required: 1`, `prior_completed_shelf_break_spent: 1`
- **Caution counts:** `MACRO_UNCONFIRMED: 6`, `IV_UNCONFIRMED: 6`, `EVENT_UNCONFIRMED: 6`
- **Lifecycle change counts:** `state_changed: 5`, `trigger_changed: 3`, `blocker_changed: 4`
- **Meaningful alert candidate count:** 5

## Commands run

- `python -B historical_signal_replay/run_signal_replay.py` - PASS
- `python -m json.tool historical_signal_replay/fixtures/first_real_spy_continuation_replay_v1_fixture.json` - PASS
- `python -B replay/test_on_demand_stage_messages.py` - PASS
- `python -B replay/validate_fixtures.py` - PASS
- `python -B replay/run_replay.py` - PASS; 16/16 passed, `local_fixture_engine=16`, `placeholder_scaffold=0`
- All `replay/test_on_demand_*contract.py` files - PASS

## Files intentionally not changed

- `main.py`
- `dxlink_candles.py`
- `historical_signal_replay/schemas/`
- Existing fixture contents
- Replay/on-demand tests
- Production/Railway files

## Next task

Decide the next bounded real historical signal/stage/lifecycle replay validation step without starting trade outcome backtesting, option P&L, account sizing, watcher implementation, auto-trading, or live trade decisions.
