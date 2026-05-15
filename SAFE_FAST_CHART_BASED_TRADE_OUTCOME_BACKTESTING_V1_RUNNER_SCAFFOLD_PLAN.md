# SAFE-FAST Chart-Based Trade Outcome Backtesting v1 Runner Scaffold Plan

## Planning Status

- **Planning status:** PASS
- **Baseline:** patch8
- **Latest local commit reviewed:** `959389a Add chart outcome tooling closeout review`
- **Scope:** docs-only planning review for the minimal chart-based trade outcome backtesting v1 runner scaffold.
- **Runner implementation started:** no
- **Outcome calculation started:** no

This plan defines the intended runner scaffold only. It does not implement the runner, calculate outcomes, change `main.py`, change schemas, change fixtures, change the historical replay runner, model option P&L, add account sizing, start watcher implementation, auto-trade, or make live trade decisions.

## Runner Purpose

The minimal v1 runner scaffold should provide a deterministic command boundary for chart-based trade outcome backtesting without yet performing outcome calculation.

The scaffold should eventually:

- load one chart outcome input fixture,
- validate it against `chart_outcome_backtesting/schemas/chart_outcome_backtest_input_v1.schema.json`,
- load the matching expected output fixture only as the v1 scaffold comparison target,
- validate the expected output against `chart_outcome_backtesting/schemas/chart_outcome_backtest_output_v1.schema.json`,
- verify referenced source artifacts exist,
- emit a clear scaffold-only PASS/FAIL result.

The scaffold must not infer trade outcomes until a later explicitly authorized implementation task.

## Allowed Inputs

Allowed v1 scaffold inputs:

- `chart_trade_outcome_backtesting/fixtures/first_spy_continuation_chart_outcome_input_v1.json`
- `chart_trade_outcome_backtesting/fixtures/first_spy_continuation_chart_outcome_expected_output_v1.json`
- `chart_trade_outcome_backtesting/schemas/chart_outcome_backtest_input_v1.schema.json`
- `chart_trade_outcome_backtesting/schemas/chart_outcome_backtest_output_v1.schema.json`
- `historical_signal_replay/reports/first_real_spy_continuation_replay_v1_signal_log.jsonl`
- `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`

Allowed symbol universe remains `SPY`, `QQQ`, `IWM`, and `GLD`, but the first scaffold should run only the existing SPY Continuation sample fixture. Allowed setup families remain `Ideal`, `Clean Fast Break`, and `Continuation`, but the first scaffold should not manufacture new candidates.

## Expected Outputs

Expected scaffold outputs:

- console PASS/FAIL status,
- validation errors when input or expected output schema validation fails,
- missing-artifact errors when referenced source files are absent,
- explicit confirmation that the run is scaffold-only,
- explicit confirmation that outcome calculation is not implemented.

The first scaffold should not create reports unless a later task explicitly authorizes report emission. If report emission is later added, reports must be chart-only and must not claim profitability, option performance, account suitability, execution realism, watcher readiness, or live trade permission.

## Sample Fixture Use

The scaffold should use the sample input fixture as the single source of candidate configuration:

- `candidate_id`: `first_spy_continuation_chart_outcome_v1`
- `symbol`: `SPY`
- `setup_family`: `Continuation`
- `source_row_name`: `triggered_signal_stage_candidate`
- `source_signal_timestamp`: `2026-04-30T12:30:00-04:00`
- `entry_candle_policy`: `next_eligible_candle_after_signal`
- `entry_price_policy`: `next_eligible_candle_open`

The expected output fixture should be used only as a scaffold validation target. It is not final backtest proof and must not be treated as a computed result until a later runner implementation task explicitly adds calculation logic.

## Real SPY Source Data Use

The scaffold should use `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` only for integrity and availability checks in v1 scaffold form.

Allowed scaffold checks:

- source CSV exists,
- source CSV contains SPY 1H RTH candles,
- source CSV contains the signal timestamp `2026-04-30T12:30:00-04:00`,
- source CSV contains lookahead-window timestamps referenced by the input fixture,
- unavailable context fields remain unconfirmed rather than inferred.

The scaffold must not scan the CSV to compute terminal outcome, MFE, MAE, gap cause, or performance until outcome calculation is explicitly authorized.

## Chart-Only Boundary

The runner scaffold is chart-only. It may validate or carry fields for:

- entry condition,
- invalidation condition,
- follow-through condition,
- failure condition,
- time-stop condition,
- max favorable move field shape,
- max adverse move field shape,
- same-day versus fast-swing classification field shape,
- headline and gap-risk context availability,
- no-hindsight audit fields.

It must not model:

- option P&L,
- option-spread pricing,
- Greeks,
- bid/ask behavior,
- fills or missed fills,
- slippage,
- broker/order execution,
- account sizing,
- account drawdown,
- watcher state mutation,
- auto-trading,
- live trade decisions.

## Entry-Condition Handling

The scaffold should validate that entry-condition fields exist and are schema-valid. It should confirm that the sample candidate uses a predeclared signal row with `final_verdict: TRADE`, `trigger_state: triggered`, and `entry_candle_policy: next_eligible_candle_after_signal`.

The scaffold should not decide whether a new row qualifies for entry and should not recompute entry timing from future candles.

## Invalidation Handling

The scaffold should validate that invalidation is present, known at entry, and chart-only. For the first sample, invalidation is copied from the replay row as `708.37`.

The scaffold should not evaluate whether future candles touched or closed through invalidation until outcome calculation is authorized.

## Follow-Through Handling

The scaffold should validate that follow-through rules are present and predeclared. For the first sample, the expected fixture uses a 2.0 point favorable touch threshold as sample/scaffold context only.

The scaffold should not decide whether follow-through occurred and should not select thresholds after reading future candles.

## Failure Handling

The scaffold should validate that failure rules are present and chart-only. Failure types should remain limited to schema-defined chart failures such as invalidation hit, trigger hold failure, thesis reversal, no meaningful move before time stop, or hard chart blocker before follow-through.

The scaffold should not classify a candidate as failed until outcome calculation is authorized.

## Time-Stop Handling

The scaffold should validate the declared time-stop policy:

- `time_stop_type`: `same_day_or_fast_swing`
- `max_hold_candles`: `14`
- `max_hold_sessions`: `3`
- `source_end_policy`: `unresolved_insufficient_lookahead`

The scaffold should not apply a time stop or choose terminal status from candle behavior until outcome calculation is authorized.

## Max Favorable Move Handling

The scaffold should validate max favorable move field shape in the expected output fixture only.

It must not compute MFE from real candles yet. It must not infer option delta, spread value, dollar P&L, or account return from MFE fields.

## Max Adverse Move Handling

The scaffold should validate max adverse move field shape in the expected output fixture only.

It must not compute MAE from real candles yet. It must not treat MAE as account drawdown, full option risk, or broker execution proof.

## Same-Day vs Fast-Swing Classification

The scaffold should validate that the expected output fixture carries a schema-valid hold classification. For the current sample, that classification is `same_day`.

The scaffold should not classify new outcomes or convert overnight carry into live trading permission. Same-day and fast-swing remain chart-analysis labels only.

## Headline and Gap-Risk Handling

The scaffold should preserve headline and gap-risk fields as availability/context fields. Current SPY source data marks 24H/daily, macro, IV, and event context as unconfirmed, and headline context is unavailable.

Chart gaps may be carried from fixtures, but the scaffold must not infer a gap cause from candles. Missing news, macro, IV, or event context must remain unavailable or unconfirmed.

## Likely Risk vs Full-Risk Notes

The scaffold should preserve the distinction between likely chart risk and full financial risk.

Likely chart risk may exist as fixture data based on the underlying-chart distance from entry reference to invalidation. Full risk is not modeled and must remain outside v1 scaffold scope, including option debit, spread pricing, slippage, liquidity, assignment, and account drawdown.

## No-Hindsight Rules

The scaffold should enforce these no-hindsight boundaries at validation time:

- setup identity is copied from source artifacts or fixture input,
- entry, invalidation, follow-through, failure, and time-stop rules exist before future candle measurement,
- future candle fields in the fixture are treated as fixture content, not as a basis for recomputing setup identity,
- expected output is compared only as a fixture target, not as proof of computed backtest behavior,
- missing context remains unavailable or unconfirmed,
- manual overrides remain disallowed.

## Validation Requirements

Before closeout of the runner scaffold planning task, run:

- `python -B chart_trade_outcome_backtesting/validate_chart_outcome_fixtures.py`
- `python -B historical_signal_replay/run_signal_replay.py`
- all `replay/test_on_demand_*contract.py` files
- `python -B replay/test_on_demand_stage_messages.py`
- `python -B replay/validate_fixtures.py`
- `python -B replay/run_replay.py`

Future runner scaffold implementation validation should include those same checks plus the new scaffold command once it exists.

## Known Limits

- This is a docs-only planning review.
- No runner exists yet.
- No outcome calculation is implemented.
- The existing expected output fixture is a sample/scaffold target, not final backtest proof.
- Only the first SPY Continuation chart outcome sample is available.
- QQQ, IWM, and GLD do not yet have equivalent chart outcome sample fixtures.
- Current real source data lacks confirmed 24H/daily, macro, IV, event, and headline context.
- Chart outcome does not equal option outcome.
- Likely chart risk does not equal full account or option-spread risk.
- Same-day and fast-swing labels are not live trade permissions.
- v1 scaffold does not prove watcher readiness, proof-mode readiness, production readiness, or account safety.

## Non-Changes

- **`main.py` changed:** no
- **Schemas changed:** no
- **Fixtures changed:** no
- **Historical replay runner changed:** no
- **Runner implementation started:** no
- **Outcome calculation started:** no
- **Option P&L modeled:** no
- **Account sizing added:** no
- **Watcher implementation started:** no

## Recommended Next Task

Create the minimal chart-based trade outcome backtesting v1 runner scaffold, limited to schema validation, sample fixture loading, source artifact existence checks, and scaffold-only PASS/FAIL reporting. Do not implement outcome calculation, model option P&L, add account sizing, change `main.py`, change schemas or fixtures, change the historical replay runner, or start watcher implementation.
