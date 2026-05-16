# QQQ First Real Historical Replay v1 Runner Output Validation Review

## Scope

- **Objective:** validate QQQ Ideal fixture runner inclusion/support.
- **Fixture:** `historical_signal_replay/fixtures/first_real_qqq_ideal_replay_v1_fixture.json`
- **Runner:** `historical_signal_replay/run_signal_replay.py`
- **Boundary:** signal/stage/lifecycle replay output only; no profitability, trade outcome backtesting for QQQ, option P&L, account sizing, broker/order/execution, auto-trading, watcher implementation, or live trade decisions.

## Runner support

- **QQQ Ideal fixture included:** yes
- **Runner code changed:** yes; `historical_signal_replay/run_signal_replay.py` now emits QQQ Ideal reports for this fixture only.
- **Generated reports changed:** yes; QQQ Ideal signal log, summary, and regression candidate files are emitted under `historical_signal_replay/reports/`.

## Generated reports

- `historical_signal_replay/reports/first_real_qqq_ideal_replay_v1_signal_log.jsonl`
- `historical_signal_replay/reports/first_real_qqq_ideal_replay_v1_summary.json`
- `historical_signal_replay/reports/first_real_qqq_ideal_replay_v1_regression_candidates.json`

## Validation results

- **Validation status:** PASS
- **QQQ Ideal signal log exists:** yes
- **QQQ Ideal signal log row count:** 6
- **QQQ Ideal summary `total_rows`:** 6
- **Symbol result:** PASS; `QQQ`
- **Setup family count result:** PASS; `Ideal: 6`
- **Stage count result:** PASS; `watching_ideal_impulse_context: 1`, `watching_ideal_pullback_retest_developing: 1`, `watching_ideal_retest_hold_unconfirmed: 1`, `ideal_retest_recovery_confirmation_candidate: 1`, `ideal_triggered_signal_stage_candidate: 1`, `ideal_follow_through_no_fresh_trigger: 1`
- **Lifecycle/stage sequence result:** PASS; `watching_ideal_impulse_context`, `watching_ideal_pullback_retest_developing`, `watching_ideal_retest_hold_unconfirmed`, `ideal_retest_recovery_confirmation_candidate`, `ideal_triggered_signal_stage_candidate`, `ideal_follow_through_no_fresh_trigger`
- **Boundary result:** PASS; generated QQQ reports remain signal/stage/lifecycle only and make no profitability, trade outcome backtesting, option P&L, account sizing, execution, auto-trading, watcher, or live trade decision claims.
- **Watcher remains deferred:** yes

## Summary counts

- **Final verdict counts:** `NO_TRADE: 4`, `PENDING: 1`, `TRADE: 1`
- **Blocker counts:** `no_retest_yet: 1`, `retest_developing: 1`, `retest_hold_unconfirmed: 1`, `awaiting_fresh_trigger: 1`, `prior_completed_ideal_trigger_spent: 1`
- **Caution counts:** `MACRO_UNCONFIRMED: 6`, `IV_UNCONFIRMED: 6`, `EVENT_UNCONFIRMED: 6`
- **Lifecycle change counts:** `state_changed: 6`, `trigger_changed: 3`, `blocker_changed: 6`
- **Meaningful alert candidate count:** 6

## Commands run

- `python -B historical_signal_replay/run_signal_replay.py` - PASS
- `python -m json.tool historical_signal_replay/fixtures/first_real_qqq_ideal_replay_v1_fixture.json` - PASS
- `python -B chart_trade_outcome_backtesting/validate_chart_outcome_fixtures.py` - PASS
- `python -B chart_trade_outcome_backtesting/run_chart_outcome_backtest.py` - PASS; existing chart runner executed, no QQQ chart outcome was added
- `python -B chart_trade_outcome_backtesting/summarize_chart_outcomes.py` - PASS
- `python -B replay/test_on_demand_stage_messages.py` - PASS
- `python -B replay/validate_fixtures.py` - PASS
- `python -B replay/run_replay.py` - PASS; 16/16 passed, `local_fixture_engine=16`, `placeholder_scaffold=0`
- All `replay/test_on_demand_*contract.py` files - PASS; 35 files passed locally

## Files intentionally not changed

- `main.py`
- `dxlink_candles.py`
- `historical_signal_replay/schemas/`
- Existing fixture contents
- Replay/on-demand tests
- Chart outcome calculation code
- Production/Railway files

## Next task

Review QQQ Ideal historical signal replay outputs as signal/stage/lifecycle evidence only, then choose the next bounded QQQ real historical replay coverage step without starting QQQ chart outcome calculation, option P&L, account sizing, watcher implementation, auto-trading, or live trade decisions.
