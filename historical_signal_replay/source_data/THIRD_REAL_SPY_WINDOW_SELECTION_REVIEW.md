# Third Real SPY Window Selection Review

## Selection Status

- **Status:** PASS
- **Baseline:** patch8
- **Latest local commit at selection time:** `c6a0430 Add second real SPY Ideal runner output validation`
- **Source CSV:** `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`
- **Symbol:** SPY
- **Timeframe:** 1h_rth
- **Selected timestamp range:** `2026-04-10T09:30:00-04:00` through `2026-04-15T15:30:00-04:00`
- **Selected row count:** 28
- **Avoided first selected window:** yes; did not reuse `2026-04-24T09:30:00-04:00` through `2026-04-30T15:30:00-04:00`
- **Avoided second selected window:** yes; did not reuse `2026-05-06T09:30:00-04:00` through `2026-05-13T14:30:00-04:00`
- **Likely setup family candidate:** Clean Fast Break

## Source Window Rationale

This bounded source-data window is selected as the third SPY candidate because it is the clearest unused Clean Fast Break candidate in the validated source CSV:

- `2026-04-10` forms a narrow pause after the prior upside session, with complete 1h RTH rows and a contained `678.45` to `682.03` range.
- `2026-04-13` breaks above the prior pause high, extends through `683.84`, and closes at `686.00` near the session high.
- `2026-04-14` gaps and continues higher, holding above the prior break area and extending into the `694` area.
- `2026-04-15` forms a tight higher-price base through midday, then breaks above `700` during the `14:30` row and holds near that level into the close.

The shape is suitable for future no-hindsight signal/stage/lifecycle fixture design because it contains a tight pre-break pause, a clean upside break, and bounded follow-through rows inside one non-overlapping source-data range. The selected setup family remains a candidate only and must be confirmed during future fixture design from row-by-row no-hindsight evidence.

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
- **Contract tests result:** PASS; all `replay/test_on_demand_*contract.py` files passed locally
- **Stage-message result:** PASS; `python -B replay/test_on_demand_stage_messages.py`
- **Fixture validation result:** PASS; `python -B replay/validate_fixtures.py`
- **Full replay result:** PASS; `python -B replay/run_replay.py` returned `16/16 passed`, `local_fixture_engine=16`, `placeholder_scaffold=0`

## Recommended Next Task

Design a third real historical replay v1 fixture from the selected SPY source-data window, preserving the source-data/no-hindsight boundary and staying signal/stage/lifecycle only.
