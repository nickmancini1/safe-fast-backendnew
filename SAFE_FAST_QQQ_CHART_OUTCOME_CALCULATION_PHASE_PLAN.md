# SAFE-FAST QQQ Chart Outcome Calculation Phase Plan

## Planning Status

- **Planning status:** PASS
- **Baseline:** patch8
- **Latest local commit reviewed:** `883762a Add QQQ post-closeout chart outcome decision review`
- **Scope:** docs-only QQQ chart outcome calculation phase plan for Ideal, Clean Fast Break, and Continuation.

This plan does not start QQQ chart outcome calculations, create chart outcome fixtures, change `main.py`, change schemas, change runner code, change chart outcome code, model option P&L, add account sizing, start watcher implementation, auto-trade, use live reads, or make live trade decisions.

## Reason QQQ Chart Outcomes Come Next

QQQ chart outcomes come next because QQQ now has completed three-setup real historical replay closeout for Ideal, Clean Fast Break, and Continuation. The SPY path already established the project sequence: complete real historical signal/stage/lifecycle replay evidence across the three setup families first, then move into chart-only outcome calculation. The broader chart outcome coverage plan also identifies QQQ as the minimum next-symbol target before IWM or GLD.

This phase remains a planning phase only. It authorizes the next bounded task to create the first QQQ Ideal chart outcome input/expected-output fixture and calculation, not to calculate all QQQ outcomes in this task.

## QQQ Replay Evidence Summary

- **QQQ three-setup closeout status:** PASS
- **Source data:** accepted QQQ `1h_rth` source CSV with 301 data rows from `2026-03-16T15:30:00-04:00` through `2026-05-15T14:30:00-04:00`
- **Source:** `dxlink_candles.get_1h_ema50_snapshot` as of `2026-05-15T18:48:44Z`
- **Ideal evidence:** PASS; 6 signal log rows, 6 summary rows, setup count `Ideal: 6`
- **Clean Fast Break evidence:** PASS; 6 signal log rows, 6 summary rows, setup count `Clean Fast Break: 6`
- **Continuation evidence:** PASS; 6 signal log rows, 6 summary rows, setup count `Continuation: 6`
- **Total QQQ signal/stage/lifecycle rows:** 18
- **Eligible chart outcome candidate rows:** one reviewed `TRADE` / `signal` / `triggered` row per setup family
- **No-hindsight replay boundary:** PASS; QQQ replay evidence remains signal/stage/lifecycle only and contains no future-row outcome labels, P&L, option data, account sizing, broker/order data, or chart outcome conclusions.

## Setup Families To Calculate

The QQQ chart outcome calculation phase should calculate these setup families in this order:

1. Ideal
2. Clean Fast Break
3. Continuation

Each family should start from its accepted QQQ historical signal replay row and should remain chart-only.

## Required QQQ Chart Outcome Fixture Files

Required input fixtures:

- `chart_trade_outcome_backtesting/fixtures/first_qqq_ideal_chart_outcome_input_v1.json`
- `chart_trade_outcome_backtesting/fixtures/first_qqq_clean_fast_break_chart_outcome_input_v1.json`
- `chart_trade_outcome_backtesting/fixtures/first_qqq_continuation_chart_outcome_input_v1.json`

Required expected output fixtures:

- `chart_trade_outcome_backtesting/fixtures/first_qqq_ideal_chart_outcome_expected_output_v1.json`
- `chart_trade_outcome_backtesting/fixtures/first_qqq_clean_fast_break_chart_outcome_expected_output_v1.json`
- `chart_trade_outcome_backtesting/fixtures/first_qqq_continuation_chart_outcome_expected_output_v1.json`

These files must not be created by this planning task.

## Required QQQ Chart Outcome Result Files

Required per-family result files:

- `chart_trade_outcome_backtesting/reports/first_qqq_ideal_chart_outcome_result_v1.json`
- `chart_trade_outcome_backtesting/reports/first_qqq_clean_fast_break_chart_outcome_result_v1.json`
- `chart_trade_outcome_backtesting/reports/first_qqq_continuation_chart_outcome_result_v1.json`

Required aggregate and closeout files:

- `chart_trade_outcome_backtesting/reports/qqq_three_setup_chart_outcome_summary_v1.json`
- `SAFE_FAST_QQQ_CHART_OUTCOME_CLOSEOUT_REVIEW.md`

These files must not be created by this planning task.

## Expected Calculation Order

1. QQQ Ideal
2. QQQ Clean Fast Break
3. QQQ Continuation
4. QQQ aggregate chart outcome summary
5. QQQ chart outcome closeout

Each step should be a separate bounded task unless a later task explicitly authorizes combining them.

## Entry Rule Source

The entry rule source is `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_CALCULATION_RULES_PLAN.md`.

For each QQQ candidate, entry eligibility must come from the accepted QQQ signal log row where:

- `symbol` is `QQQ`
- `setup_type` matches the target setup family
- `final_verdict` is `TRADE`
- `current_state` is `signal`
- `trigger_state` is `triggered`
- `primary_blocker` is null
- `trigger_level` is numeric
- `invalidation` is numeric
- `winner_selection_result.selected_setup_type` matches the target setup family

The default v1 entry timestamp is the next eligible QQQ 1H RTH candle after the eligible signal row timestamp. The default entry reference price is that next eligible candle open. This is a chart reference only, not a fill or execution claim.

## Invalidation Rule Source

The invalidation rule source is the accepted QQQ signal log row for the eligible candidate, using the `invalidation` value visible before future chart scanning.

Invalidation must not be moved, widened, tightened, recalculated, or optimized from future candles. For bullish QQQ rows, invalidation is reached when a future candle low touches or crosses the copied invalidation level before follow-through or time stop.

## Follow-Through, Failure, And Time-Stop Rules

Follow-through, failure, and time-stop rules must use `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_CALCULATION_RULES_PLAN.md` as the source of truth.

- **Follow-through:** use the predeclared candidate `follow_through_condition`, such as a numeric favorable-points threshold and touch/close policy. The threshold must be declared before scanning future candles.
- **Failure:** default failure is chart invalidation reached before follow-through or time stop. Same-candle follow-through/invalidation ambiguity uses conservative ordering: invalidation wins.
- **Time stop:** use the predeclared `time_stop_condition` and `lookahead_window`. If source data ends before the declared window can complete, the output must be unresolved/insufficient-lookahead, not fabricated.

## MFE And MAE Requirements

Each QQQ chart outcome output must include chart-only MFE and MAE:

- points
- percent
- chart R when likely chart risk is positive and known
- timestamp
- candle index
- candles after entry
- confirmation that MFE/MAE use no candles after the first terminal condition

For bullish QQQ rows, MFE is measured from entry reference price to the maximum high through the first terminal candle. MAE is measured from entry reference price to the minimum low through the first terminal candle. These values must not imply option delta, option spread value, account drawdown, or dollar P&L.

## Same-Day And Fast-Swing Classification Requirements

Each QQQ output must classify the terminal condition as same-day or fast-swing chart behavior:

- same-session follow-through: `same_day`
- same-session invalidation: `invalidated_same_day`
- same-session time stop: `time_stop_same_day`
- post-entry-session follow-through inside the declared window: `fast_swing`
- post-entry-session invalidation inside the declared window: `invalidated_fast_swing`
- post-entry-session time stop inside the declared window: `time_stop_fast_swing`

This classification is chart context only. It does not authorize live trading, overnight carrying, option modeling, or account sizing.

## Headline And Gap-Risk Handling

Chart gaps may be measured from QQQ candles when a regular-session open differs from the prior available RTH close. Gap direction, points, and percent may be recorded from chart data.

Gap cause must not be inferred from price action. Macro, IV, event, 24H/daily, and headline context must remain unavailable or unconfirmed unless a reviewed source artifact explicitly supplies that context. Headline/gap-risk fields are context only and must not become live trade permission.

## Likely Risk Vs Full-Risk Note

Likely chart risk is the underlying-chart distance between entry reference price and copied invalidation reference price.

Likely chart risk is not full financial risk. Full risk remains out of scope and must not be modeled. The QQQ phase must exclude option debit, spread width, Greeks, bid/ask behavior, fill quality, slippage, commissions, gap-through-invalidation losses, assignment/exercise behavior, account sizing, buying power, and broker execution.

## No-Hindsight Rules

The QQQ calculation phase must enforce these no-hindsight rules:

- Use only accepted QQQ replay/source artifacts to identify candidate rows.
- Do not recompute setup identity from future candles.
- Copy trigger level, invalidation, blockers, cautions, setup family, and source timestamp from source artifacts or predeclared input.
- Freeze entry, invalidation, follow-through, failure, time-stop, MFE, MAE, and classification rules before scanning future candles.
- Use future candles only after the candidate is frozen.
- Stop scanning at the first terminal condition.
- Use conservative ordering when 1H OHLCV cannot prove intrabar sequence.
- Mark missing headline, macro, IV, event, 24H/daily, option, account, and broker context as unavailable or unconfirmed.
- Do not use manual overrides in v1 real calculation.

## Chart-Only Boundary

QQQ chart outcome calculation is limited to underlying-chart behavior after qualifying historical signal replay rows.

It may measure entry reference, copied invalidation, follow-through, invalidation/failure, time stop, MFE, MAE, same-day/fast-swing classification, chart gap context, and no-hindsight audit fields.

It must not model option P&L, option-spread pricing, Greeks, option chains, bid/ask behavior, fills, missed fills, slippage, commissions, account sizing, account drawdown, buying power, broker/order execution, watcher state mutation, auto-trading, live reads, live alerts, or live trade decisions.

## Known Limits

- This is a docs-only plan.
- QQQ chart outcome calculation has not started.
- QQQ chart outcome fixtures have not been created.
- QQQ currently has one eligible signal-stage candidate per setup family, not the broader minimum of three samples per setup family.
- Existing QQQ replay outputs are signal/stage/lifecycle evidence only, not profitability or chart outcome proof.
- Current source artifacts are 1H RTH candles, not tick data or intrabar sequencing.
- Same-candle terminal ordering cannot be known from 1H OHLCV and must use conservative ordering.
- Macro, IV, event, headline, 24H/daily, option, account, and broker context remain unavailable or unconfirmed unless a reviewed source supplies them.
- Chart outcomes will not prove option profitability, account safety, watcher readiness, production readiness, or live trade readiness.

## Non-Changes

- **Chart outcome calculation started:** no
- **Chart outcome fixtures created:** no
- **Option P&L modeled:** no
- **Account sizing added:** no
- **Watcher implementation started:** no
- **`main.py` changed:** no
- **Schemas changed:** no
- **Runner code changed:** no
- **Chart outcome code changed:** no

## Recommended Next Task

Create QQQ Ideal chart outcome input/expected output fixture and calculation, using the accepted QQQ Ideal signal-stage row and the v1 chart-only calculation rules. Do not model option P&L, add account sizing, start watcher implementation, change `main.py`, change schemas, change runner code, or broaden beyond the QQQ Ideal chart outcome unless explicitly authorized.
