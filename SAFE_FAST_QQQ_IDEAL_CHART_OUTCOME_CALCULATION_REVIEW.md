# SAFE-FAST QQQ Ideal Chart Outcome Calculation Review

## Review Status

- **Calculation status:** PASS
- **Baseline:** patch8
- **Latest local commit before calculation:** `a9c4a38 Add QQQ chart outcome calculation phase plan`
- **Sample used:** QQQ Ideal accepted historical signal replay row
- **Source signal log:** `historical_signal_replay/reports/first_real_qqq_ideal_replay_v1_signal_log.jsonl`
- **Source fixture:** `historical_signal_replay/fixtures/first_real_qqq_ideal_replay_v1_fixture.json`
- **Source CSV:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`
- **Input fixture:** `chart_trade_outcome_backtesting/fixtures/qqq_ideal_chart_outcome_input_v1.json`
- **Expected output fixture:** `chart_trade_outcome_backtesting/fixtures/qqq_ideal_chart_outcome_expected_output_v1.json`
- **Report file:** `chart_trade_outcome_backtesting/reports/qqq_ideal_chart_outcome_result_v1.json`

## Candidate

- **Symbol:** QQQ
- **Setup family:** Ideal
- **Eligible signal row:** `ideal_triggered_signal_stage_candidate`
- **Signal timestamp:** `2026-05-13T12:30:00-04:00`
- **Final verdict:** TRADE
- **Current state:** signal
- **Trigger state:** triggered
- **Primary blocker:** null
- **Trigger level:** 714.59
- **Copied invalidation:** 696.66
- **Winner selection result:** Ideal

## Calculation Result

- **Entry result:** entry reached at `2026-05-13T13:30:00-04:00`, reference price 714.79, using the next eligible 1H RTH candle open.
- **Invalidation result:** copied invalidation 696.66 was not reached before terminal follow-through.
- **Follow-through/failure/time-stop result:** follow-through reached at `2026-05-14T09:30:00-04:00` when the high reached 719.69, above the entry plus the predeclared 2.0 point favorable threshold.
- **Same-day/fast-swing classification:** fast_swing.
- **MFE result:** 4.9 points, 0.6855%, 0.2703 chart R at `2026-05-14T09:30:00-04:00`.
- **MAE result:** 1.115 points, 0.156%, 0.0615 chart R at `2026-05-13T13:30:00-04:00`.
- **Likely chart risk:** 18.13 points, 2.5364%, underlying-chart distance from entry reference to copied invalidation.
- **Headline/gap-risk context:** macro/IV/event unconfirmed, headline unavailable, chart gap detected up 0.14 points / 0.0196%; gap cause unknown.

## Boundary Result

PASS. This calculation is chart-only and uses real QQQ source OHLCV rows only. It does not fabricate prices or timestamps, does not recompute setup identity from future candles, and stops measurement at the first terminal condition.

- **Option P&L modeled:** no
- **Account sizing added:** no
- **Broker/order execution modeled:** no
- **Watcher work started:** no
- **`main.py` changed:** no
- **Schemas changed:** no
- **Historical replay fixtures changed:** no
- **Historical replay runner changed:** no

## Validation Results

- **Chart fixture validation:** PASS; `python -B chart_trade_outcome_backtesting/validate_chart_outcome_fixtures.py`
- **Chart runner:** PASS; `python -B chart_trade_outcome_backtesting/run_chart_outcome_backtest.py`
- **Output JSON validation:** PASS; `python -m json.tool chart_trade_outcome_backtesting/reports/qqq_ideal_chart_outcome_result_v1.json`
- **Historical signal replay:** PASS; `python -B historical_signal_replay/run_signal_replay.py`
- **Contract tests:** PASS; all 35 `replay/test_on_demand_*contract.py` files passed locally
- **Stage-message test:** PASS; `python -B replay/test_on_demand_stage_messages.py`
- **Fixture validation:** PASS; `python -B replay/validate_fixtures.py`
- **Full replay:** PASS; `python -B replay/run_replay.py` returned `16/16 passed`, `local_fixture_engine=16`, `placeholder_scaffold=0`

## Next Task

Validate QQQ Ideal chart outcome calculation output.
