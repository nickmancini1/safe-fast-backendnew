# Real Historical Replay v1 SPY Three-Setup Closeout Review

## Closeout Status

- **Closeout status:** PASS
- **Baseline:** patch8
- **Latest local commit reviewed:** `5410a7d Add third real SPY Clean Fast Break runner output validation`
- **Scope:** docs-only closeout of SPY real historical replay v1 coverage across Continuation, Ideal, and Clean Fast Break.

This closeout confirms that SPY real historical replay v1 now has real source-data coverage, fixture creation, and runner output validation for all three setup families. It remains signal/stage/lifecycle replay only.

## Source Data Summary

- **Source data file:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`
- **Source validation review:** `historical_signal_replay/source_data/FIRST_REAL_SOURCE_HISTORICAL_DATA_VALIDATION_REVIEW.md`
- **Source validation status:** PASS
- **Symbol:** SPY
- **Timeframe:** 1h_rth
- **Total source row count:** 293
- **Source timestamp range:** 2026-03-16T09:30:00-04:00 through 2026-05-13T14:30:00-04:00
- **Source:** `dxlink_candles.get_1h_ema50_snapshot`
- **Source as-of:** 2026-05-13T18:43:00Z
- **Data vendor:** dxFeed via tastytrade dxLink

The source CSV passed header, symbol, timestamp/session, OHLCV, source/as-of, unavailable-context, no-outcome, and no-after-the-fact-label checks.

## Continuation Fixture/Output Result

- **Result:** PASS
- **Window review:** `historical_signal_replay/source_data/FIRST_REAL_SPY_WINDOW_SELECTION_REVIEW.md`
- **Fixture file:** `historical_signal_replay/fixtures/first_real_spy_continuation_replay_v1_fixture.json`
- **Runner output review:** `historical_signal_replay/FIRST_REAL_HISTORICAL_REPLAY_V1_RUNNER_OUTPUT_VALIDATION_REVIEW.md`
- **Source window:** 2026-04-24T09:30:00-04:00 through 2026-04-30T15:30:00-04:00
- **Source window row count:** 35
- **Fixture row count:** 6
- **Signal log row count:** 6
- **Summary total rows:** 6
- **Setup family count:** `Continuation: 6`
- **Stage counts:** `developing_pullback_shelf: 1`, `developing_shelf_no_trigger: 2`, `opening_probe_no_completed_approval: 1`, `triggered_signal_stage_candidate: 1`, `spent_or_follow_through_no_fresh_trigger: 1`
- **Runner output validation:** PASS

## Ideal Fixture/Output Result

- **Result:** PASS
- **Window review:** `historical_signal_replay/source_data/SECOND_REAL_SPY_WINDOW_SELECTION_REVIEW.md`
- **Fixture file:** `historical_signal_replay/fixtures/second_real_spy_ideal_replay_v1_fixture.json`
- **Runner output review:** `historical_signal_replay/SECOND_REAL_HISTORICAL_REPLAY_V1_RUNNER_OUTPUT_VALIDATION_REVIEW.md`
- **Source window:** 2026-05-06T09:30:00-04:00 through 2026-05-13T14:30:00-04:00
- **Source window row count:** 41
- **Fixture row count:** 6
- **Signal log row count:** 6
- **Summary total rows:** 6
- **Setup family count:** `Ideal: 6`
- **Stage counts:** `ideal_impulse_context: 1`, `ideal_pullback_retest_developing: 1`, `ideal_retest_hold_unconfirmed: 1`, `ideal_retest_recovery_confirmation_candidate: 1`, `ideal_triggered_signal_stage_candidate: 1`, `ideal_follow_through_no_fresh_trigger: 1`
- **Runner output validation:** PASS

## Clean Fast Break Fixture/Output Result

- **Result:** PASS
- **Window review:** `historical_signal_replay/source_data/THIRD_REAL_SPY_WINDOW_SELECTION_REVIEW.md`
- **Fixture file:** `historical_signal_replay/fixtures/third_real_spy_clean_fast_break_replay_v1_fixture.json`
- **Runner output review:** `historical_signal_replay/THIRD_REAL_HISTORICAL_REPLAY_V1_RUNNER_OUTPUT_VALIDATION_REVIEW.md`
- **Source window:** 2026-04-10T09:30:00-04:00 through 2026-04-15T15:30:00-04:00
- **Source window row count:** 28
- **Fixture row count:** 6
- **Signal log row count:** 6
- **Summary total rows:** 6
- **Setup family count:** `Clean Fast Break: 6`
- **Stage counts:** `clean_fast_break_tight_pause_context: 1`, `clean_fast_break_initial_break_candidate: 1`, `clean_fast_break_follow_through_confirming_context: 1`, `watching_higher_base_after_fast_break: 1`, `clean_fast_break_fresh_break_signal_candidate: 1`, `clean_fast_break_post_break_no_fresh_trigger: 1`
- **Runner output validation:** PASS

## Row Counts

- **Validated source CSV rows:** 293
- **Continuation selected source rows:** 35
- **Ideal selected source rows:** 41
- **Clean Fast Break selected source rows:** 28
- **Total selected source-window rows across three setup families:** 104
- **Continuation fixture rows / output rows:** 6 / 6
- **Ideal fixture rows / output rows:** 6 / 6
- **Clean Fast Break fixture rows / output rows:** 6 / 6
- **Total real SPY fixture rows / output rows across three setup families:** 18 / 18

## Coverage Results

- **Setup-family coverage result:** PASS; Continuation, Ideal, and Clean Fast Break each have selected real SPY source windows, created replay fixtures, generated signal logs, generated summaries, generated regression candidate files, and runner output validation.
- **No-hindsight result:** PASS; each source-window selection and fixture review states that rows use only validated SPY source candles available at or before that row timestamp, with no future-row labels, trade outcomes, P&L, option data, account sizing, broker/order/execution, or backtest conclusions.
- **Signal/stage/lifecycle boundary result:** PASS; the created fixtures and generated reports remain signal/stage/lifecycle artifacts only and do not claim profitability, trade outcome backtesting, option P&L, account sizing, execution, auto-trading, or live trade decisions.

## Known Limits

- The three fixtures validate selected SPY historical signal/stage/lifecycle paths only; they do not validate all possible SPY market regimes.
- 24H/daily, macro, IV, and event context remain unavailable/unconfirmed in the source CSV.
- The generated regression candidate files are review artifacts, not promoted replay regression tests by this closeout.
- Runner output validation confirms report emission and expected counts/sequences for the three fixtures; it does not prove alert production readiness or continuous lifecycle memory.
- No trade outcomes, fills, slippage, option chain behavior, P&L, or position sizing are modeled.

## What This Proves

- A real validated SPY 1h RTH source CSV is available and accepted for historical signal/stage/lifecycle replay v1 work.
- Non-overlapping real SPY source windows were selected for Continuation, Ideal, and Clean Fast Break setup-family coverage.
- Each setup family has a six-row fixture built from real source candles with no-hindsight row boundaries.
- The runner emits signal log, summary, and regression candidate outputs for all three real SPY fixtures.
- Output summaries confirm expected setup-family counts, stage counts, lifecycle sequences, and row counts for all three setup families.

## What This Does Not Prove

- It does not prove profitability or expected trade outcomes.
- It does not model option P&L, contract selection, Greeks, liquidity, slippage, fills, or broker execution.
- It does not add account sizing or risk allocation.
- It does not implement a watcher, alert delivery, auto-trading, live reads, or live trade decisions.
- It does not modify engine behavior or prove production readiness.

## Non-Changes

- **`main.py` changed:** no
- **`dxlink_candles.py` changed:** no
- **Runner code changed:** no
- **Schemas changed:** no
- **Fixture contents changed:** no
- **Generated reports changed:** no
- **Replay tests changed:** no
- **Backtesting started:** no
- **Option P&L modeled:** no
- **Account sizing added:** no

## Recommended Next Task

Decide the next bounded phase after SPY three-setup real historical replay closeout, staying signal/stage/lifecycle only unless a separate task explicitly authorizes a different phase.
