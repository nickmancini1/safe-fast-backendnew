# Third Real Historical Replay v1 Runner Output Validation Review

## Scope

- **Objective:** validate third-real SPY Clean Fast Break fixture runner inclusion/support.
- **Fixture:** `historical_signal_replay/fixtures/third_real_spy_clean_fast_break_replay_v1_fixture.json`
- **Runner:** `historical_signal_replay/run_signal_replay.py`
- **Boundary:** signal/stage/lifecycle replay output only; no profitability, trade outcome backtesting, option P&L, account sizing, broker/order/execution, auto-trading, or live trade decisions.

## Runner support

- **Third-real fixture included:** yes
- **Runner code changed:** yes; `historical_signal_replay/run_signal_replay.py` now emits third-real reports for this fixture only.
- **Generated reports changed:** yes; third-real signal log, summary, and regression candidate files are emitted under `historical_signal_replay/reports/`.

## Generated reports

- `historical_signal_replay/reports/third_real_spy_clean_fast_break_replay_v1_signal_log.jsonl`
- `historical_signal_replay/reports/third_real_spy_clean_fast_break_replay_v1_summary.json`
- `historical_signal_replay/reports/third_real_spy_clean_fast_break_replay_v1_regression_candidates.json`

## Validation results

- **Validation status:** PASS
- **Third-real signal log exists:** yes
- **Third-real signal log row count:** 6
- **Third-real summary `total_rows`:** 6
- **Symbol result:** PASS; `SPY`
- **Setup family count result:** PASS; `Clean Fast Break: 6`
- **Stage count result:** PASS; `clean_fast_break_tight_pause_context: 1`, `clean_fast_break_initial_break_candidate: 1`, `clean_fast_break_follow_through_confirming_context: 1`, `watching_higher_base_after_fast_break: 1`, `clean_fast_break_fresh_break_signal_candidate: 1`, `clean_fast_break_post_break_no_fresh_trigger: 1`
- **Lifecycle/stage sequence result:** PASS; `clean_fast_break_tight_pause_context`, `clean_fast_break_initial_break_candidate`, `clean_fast_break_follow_through_confirming_context`, `watching_higher_base_after_fast_break`, `clean_fast_break_fresh_break_signal_candidate`, `clean_fast_break_post_break_no_fresh_trigger`
- **Fixture row-name sequence result:** PASS; `watching_clean_fast_break_tight_pause_context`, `clean_fast_break_initial_break_candidate`, `clean_fast_break_follow_through_confirming_context`, `watching_higher_base_after_fast_break`, `clean_fast_break_fresh_break_signal_candidate`, `clean_fast_break_post_break_no_fresh_trigger`
- **Boundary result:** PASS; generated reports remain signal/stage/lifecycle only and make no profitability, trade outcome backtesting, option P&L, account sizing, execution, auto-trading, or live trade decision claims.

## Summary counts

- **Final verdict counts:** `NO_TRADE: 4`, `TRADE: 2`
- **Blocker counts:** `no_completed_break_yet: 1`, `fresh_completed_breakout_required: 1`, `prior_completed_clean_fast_break_spent: 2`
- **Caution counts:** `MACRO_UNCONFIRMED: 6`, `IV_UNCONFIRMED: 6`, `EVENT_UNCONFIRMED: 6`
- **Lifecycle change counts:** `state_changed: 6`, `trigger_changed: 5`, `blocker_changed: 6`
- **Meaningful alert candidate count:** 6

## Commands run

- `python -B historical_signal_replay/run_signal_replay.py` - PASS
- `python -m json.tool historical_signal_replay/fixtures/third_real_spy_clean_fast_break_replay_v1_fixture.json` - PASS
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
- Production/Railway files

## Next task

Choose the next bounded historical signal/stage/lifecycle replay validation step without starting trade outcome backtesting, option P&L, account sizing, watcher implementation, auto-trading, or live trade decisions.
