# Second Real SPY Window Selection Review

## Selection Status

- **Status:** PASS
- **Source CSV:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`
- **Symbol:** SPY
- **Timeframe:** 1h_rth
- **Selected timestamp range:** `2026-05-06T09:30:00-04:00` through `2026-05-13T14:30:00-04:00`
- **Selected row count:** 41
- **Avoided first selected window:** yes; did not reuse `2026-04-24T09:30:00-04:00` through `2026-04-30T15:30:00-04:00`
- **Likely setup family candidate:** Ideal

## Source Window Rationale

This bounded source-data window is selected as the second SPY candidate because it contains a cleaner trend-retest shape than the already-used first Continuation window:

- `2026-05-06` opens with a strong upward impulse and closes near the session high.
- `2026-05-07` through `2026-05-08` preserves higher-price structure while pausing below and around fresh highs.
- `2026-05-12` pulls back in a multi-bar sequence after the prior advance, then begins recovering into the close.
- `2026-05-13` extends the recovery into new highs within the available source rows.

The window is suitable for future no-hindsight signal/stage/lifecycle fixture design because it includes pre-retest impulse context, pullback/retest behavior, and post-retest recovery/follow-through inside one bounded source-data range.

## No-Hindsight Result

- **Result:** PASS
- The review uses only rows from the validated source CSV.
- The selected range is source-data only and does not add setup labels, trigger labels, blocker labels, lifecycle labels, trade outcomes, profit/loss, account sizing, option data, broker data, order data, execution data, or backtest conclusions.
- Any future fixture design from this window must evaluate each row using only market bars and context available at or before that row timestamp.

## Boundary Result

- **Result:** PASS
- No fixture was created.
- OHLCV data was not changed.
- No fabricated labels were added.
- Backtesting was not started.
- `main.py` was not changed.
- `dxlink_candles.py` was not changed.
- Runner code was not changed.
- Schemas were not changed.
- Generated reports were not intentionally changed by this selection review.

## Validation Result

- **Runner result:** PASS; `python -B historical_signal_replay/run_signal_replay.py`
- **Contract tests result:** PASS; all 35 `replay/test_on_demand_*contract.py` files passed locally
- **Stage-message result:** PASS; `python -B replay/test_on_demand_stage_messages.py`
- **Fixture validation result:** PASS; `python -B replay/validate_fixtures.py`
- **Full replay result:** PASS; `python -B replay/run_replay.py` returned `16/16 passed`, `local_fixture_engine=16`, `placeholder_scaffold=0`

## Recommended Next Task

Design a second real historical replay v1 fixture from the selected SPY source-data window, preserving the source-data/no-hindsight boundary and staying signal/stage/lifecycle only.
