# SAFE-FAST Chart-Based Trade Outcome Backtesting v1 Third Real Calculation Review

## Review Status

- **Calculation status:** PASS
- **Baseline:** patch8
- **Latest local commit before calculation:** `35a1249 Add post-second chart outcome decision review`
- **Scope:** third real chart-only outcome calculation for the SPY Clean Fast Break sample.

This calculation is chart-only. It uses underlying SPY 1H RTH source OHLCV rows, the eligible historical signal replay row, and predeclared calculation rules only. It does not model option P&L, account sizing, broker/order execution, watcher behavior, auto-trading, live reads, or live trade decisions.

## Source Artifacts

- **Rules plan:** `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_CALCULATION_RULES_PLAN.md`
- **Decision review:** `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_POST_SECOND_CALCULATION_DECISION_REVIEW.md`
- **Input fixture:** `chart_trade_outcome_backtesting/fixtures/third_spy_clean_fast_break_chart_outcome_input_v1.json`
- **Expected output fixture:** `chart_trade_outcome_backtesting/fixtures/third_spy_clean_fast_break_chart_outcome_expected_output_v1.json`
- **Report file:** `chart_trade_outcome_backtesting/reports/third_spy_clean_fast_break_chart_outcome_result_v1.json`
- **Replay signal log:** `historical_signal_replay/reports/third_real_spy_clean_fast_break_replay_v1_signal_log.jsonl`
- **Replay fixture:** `historical_signal_replay/fixtures/third_real_spy_clean_fast_break_replay_v1_fixture.json`
- **Source OHLCV:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`

## Eligible Signal Row

- **Symbol/setup:** SPY Clean Fast Break
- **Selected row:** `clean_fast_break_fresh_break_signal_candidate`
- **Source timestamp:** `2026-04-15T14:30:00-04:00`
- **Eligibility evidence:** `final_verdict: TRADE`, `current_state: signal`, `trigger_state: triggered`, `primary_blocker: null`, numeric trigger `698.65`, numeric invalidation `694.2801`, and `winner_selection_result.selected_setup_type: Clean Fast Break`.
- **Boundary note:** the earlier Clean Fast Break `TRADE` row is an initial-break candidate; this calculation uses the later signal-stage row for the third sample.

## Calculation Result

- **Entry result:** entry reached at `2026-04-15T15:30:00-04:00` using the next eligible 1H RTH candle open `699.995`.
- **Invalidation result:** copied pre-entry invalidation `694.2801`; not reached in the supported measurement window.
- **Follow-through/failure/time-stop result:** follow-through was not reached; invalidation/failure was not reached; same-day time stop applied at `2026-04-15T15:30:00-04:00` close `699.84`.
- **MFE result:** `0.285` points / `0.0407%` / `0.0499R`, from the real `2026-04-15T15:30:00-04:00` high `700.28`.
- **MAE result:** `0.735` points / `0.105%` / `0.1286R`, from the real `2026-04-15T15:30:00-04:00` low `699.26`.
- **Same-day/fast-swing classification:** `time_stop_same_day`.
- **Headline/gap-risk context:** preserved as unconfirmed/unavailable; chart gap recorded from real source candles with unknown cause.
- **Likely-risk vs full-risk notes:** preserved as chart-only notes; full risk is not modeled.

## Non-Changes

- **Option P&L modeled:** no
- **Account sizing added:** no
- **Broker/order execution modeled:** no
- **Watcher work started:** no
- **`main.py` changed:** no
- **Schemas changed:** no
- **Historical replay fixtures changed:** no
- **Historical replay runner changed:** no
- **Replay tests changed:** no
- **`dxlink_candles.py` changed:** no

## Validation

- **Chart fixture validation result:** PASS; `python -B chart_trade_outcome_backtesting/validate_chart_outcome_fixtures.py`
- **Chart runner result:** PASS; `python -B chart_trade_outcome_backtesting/run_chart_outcome_backtest.py`
- **Output JSON parse/schema validation result:** PASS; runner validated output schema and `python -m json.tool chart_trade_outcome_backtesting/reports/third_spy_clean_fast_break_chart_outcome_result_v1.json` parsed successfully

## Recommended Next Task

Validate third real chart outcome calculation output without modeling option P&L, adding account sizing, starting watcher work, changing `main.py`, changing schemas or historical replay fixtures, changing historical replay runners, auto-trading, live reads, or live trade decisions.
