# SAFE-FAST Chart-Based Trade Outcome Backtesting v1 Schema Design

## Schema Design Status

- **Schema design status:** PASS
- **Baseline:** patch8
- **Latest local commit reviewed:** `7b3a45d Add chart-based trade outcome backtesting v1 plan`
- **Scope:** docs-only schema design review for chart-based trade outcome backtesting v1.
- **Implementation status:** not started.

This design describes the intended input and output schema concepts only. It does not create schema files, implement backtesting, change runner behavior, change fixtures, change reports, model option P&L, add account sizing, start watcher behavior, auto-trade, or make live trade decisions.

## Input Schema Concept

The future input schema should describe one chart-outcome candidate derived from a qualifying historical signal/stage/lifecycle replay row plus the source candles needed to measure what happened after the candidate entry.

The input should be deterministic and auditable:

- it identifies the source replay artifact and exact signal row,
- it records the setup identity and lifecycle state available at signal time,
- it defines the entry, invalidation, follow-through, failure, and time-stop rules before any future candles are scanned,
- it includes only chart data and context fields available at or before the candidate creation timestamp,
- it carries unavailable macro, IV, event, headline, and 24H/daily context explicitly as unavailable or unconfirmed rather than inferred.

The default v1 concept is one candidate per qualifying signal row. Disqualified replay rows may be captured as skipped candidates in a later implementation, but the design should keep qualifying candidates and skipped rows distinct.

## Output Schema Concept

The future output schema should describe the measured chart-only outcome for one input candidate after applying the predeclared rules to future underlying candles.

The output should record:

- whether entry was reached,
- the first terminal condition,
- the terminal timestamp and terminal candle reference,
- max favorable move and max adverse move before the terminal condition,
- same-day versus fast-swing classification,
- no-hindsight audit evidence,
- unresolved or insufficient-lookahead status when source data ends before a valid terminal condition.

No output field should imply option-contract profitability, spread value, account return, trade execution quality, or broker/order behavior.

## Required Input Fields

Required input fields:

- `schema_version`
- `candidate_id`
- `source_replay_fixture`
- `source_signal_log`
- `source_summary`
- `source_row_name`
- `source_row_index`
- `source_signal_timestamp`
- `symbol`
- `timeframe`
- `session`
- `direction`
- `setup_family`
- `stage`
- `setup_state`
- `final_verdict`
- `trigger_state`
- `entry_condition`
- `invalidation_condition`
- `follow_through_condition`
- `failure_condition`
- `time_stop_condition`
- `available_context`
- `lookahead_window`
- `source_candle_window`
- `no_hindsight_audit`

The allowed v1 symbols are `SPY`, `QQQ`, `IWM`, and `GLD`. The allowed setup families are `Ideal`, `Clean Fast Break`, and `Continuation`.

## Required Output Fields

Required output fields:

- `schema_version`
- `candidate_id`
- `source_signal_timestamp`
- `entry_status`
- `entry_timestamp`
- `entry_reference_price`
- `terminal_outcome_type`
- `terminal_timestamp`
- `terminal_reference_price`
- `terminal_reason`
- `holding_period_candles`
- `holding_period_sessions`
- `same_day_fast_swing_classification`
- `max_favorable_move`
- `max_adverse_move`
- `chart_r_multiple`
- `likely_chart_risk`
- `full_risk_modeled`
- `option_pnl_modeled`
- `account_sizing_modeled`
- `headline_gap_risk_context`
- `no_hindsight_audit`
- `known_unavailable_context`

Valid terminal outcome types should include `follow_through`, `invalidated`, `time_stop`, `no_entry`, and `unresolved_insufficient_lookahead`.

## Setup Identity Fields

The schema should preserve the setup identity already emitted by historical signal replay:

- `symbol`
- `setup_family`
- `direction`
- `stage`
- `setup_state`
- `trigger_state`
- `trigger_level`
- `invalidation`
- `primary_blocker`
- `cautions_watchouts`
- `winner_selection_result.selected_setup_type`
- `duplicate_alert_suppression_key`

Setup identity must not be recomputed from future candles. Future candles can only measure outcome after the candidate is defined.

## Stage and Lifecycle Fields

Stage and lifecycle input fields should include:

- `current_state`
- `prior_state`
- `first_seen`
- `last_seen`
- `state_changed`
- `trigger_changed`
- `blocker_changed`
- `final_verdict`
- `human_next_step`

The future backtester should only treat rows with eligible signal-stage semantics as entry candidates. Rows that are watching, developing, pending, spent, blocked, or no-trade context should not become outcome entries unless the schema explicitly classifies them as skipped or disqualified rows.

## Entry Condition Fields

Entry condition fields should include:

- `entry_trigger_type`
- `entry_trigger_level`
- `entry_reference_source`
- `entry_signal_timestamp`
- `entry_eligibility_rule`
- `entry_candle_policy`
- `entry_price_policy`
- `entry_confirmation_required`
- `entry_confirmation_basis`

The v1 default should be `next_eligible_candle_after_signal` for outcome measurement unless a future schema file explicitly supports completed same-candle trigger handling. This policy must be recorded on every candidate so later implementation does not silently change entry timing.

## Invalidation Fields

Invalidation fields should include:

- `invalidation_type`
- `invalidation_level`
- `invalidation_reference_source`
- `invalidation_rule`
- `invalidation_touch_or_close_policy`
- `invalidation_known_at_entry`
- `likely_chart_risk_points`
- `likely_chart_risk_percent`

Invalidation must be known at entry and must not be moved using future candle behavior. The schema should allow setup-specific invalidation references such as 1H 50 EMA loss, shelf/base failure, retest-hold failure, breakout-hold failure, and break back through the thesis level.

## Follow-Through Fields

Follow-through fields should include:

- `follow_through_type`
- `follow_through_threshold`
- `follow_through_threshold_basis`
- `follow_through_touch_or_close_policy`
- `follow_through_required_before_time_stop`
- `first_trouble_area`
- `continuation_objective`

The follow-through threshold must be predeclared. It cannot be selected after viewing future candles.

## Failure Fields

Failure fields should include:

- `failure_type`
- `failure_rule`
- `failure_level`
- `failure_touch_or_close_policy`
- `hold_failure_required`
- `hard_blocker_failure_policy`

Failure should be reported separately from raw adverse movement. Example failure types include `invalidation_hit`, `trigger_hold_failed`, `thesis_level_reversed`, `no_meaningful_move_before_time_stop`, and `hard_chart_blocker_before_follow_through`.

## Time-Stop Fields

Time-stop fields should include:

- `time_stop_type`
- `max_hold_candles`
- `max_hold_sessions`
- `entry_session_close_policy`
- `overnight_carry_policy`
- `fast_swing_max_sessions`
- `source_end_policy`

The v1 concept should support same-day time stops and fast-swing time stops. If source data ends before the declared time-stop window can complete, the output should be `unresolved_insufficient_lookahead`, not a fabricated win, loss, or time stop.

## Max Favorable Move Fields

Max favorable move fields should include:

- `mfe_points`
- `mfe_percent`
- `mfe_chart_r`
- `mfe_timestamp`
- `mfe_candle_index`
- `mfe_candles_after_entry`
- `mfe_before_terminal_condition`

MFE measures only underlying-chart movement before the first terminal condition. It must not imply option delta, spread value, or dollar P&L.

## Max Adverse Move Fields

Max adverse move fields should include:

- `mae_points`
- `mae_percent`
- `mae_chart_r`
- `mae_timestamp`
- `mae_candle_index`
- `mae_candles_after_entry`
- `mae_before_terminal_condition`

MAE measures only underlying-chart movement before the first terminal condition. It should be used to evaluate whether the planned chart invalidation was realistic, not to estimate account drawdown.

## Same-Day vs Fast-Swing Fields

Same-day and fast-swing fields should include:

- `hold_classification`
- `entry_session_date`
- `terminal_session_date`
- `same_session_terminal`
- `overnight_carried`
- `sessions_held`
- `same_day_time_stop_applied`
- `fast_swing_time_stop_applied`

Allowed hold classifications should include `same_day`, `fast_swing`, `time_stop_same_day`, `time_stop_fast_swing`, `invalidated_same_day`, `invalidated_fast_swing`, and `unresolved_insufficient_lookahead`.

## Headline and Gap-Risk Context Fields

Headline and gap-risk context fields should include:

- `macro_context_status`
- `iv_context_status`
- `event_context_status`
- `headline_context_status`
- `gap_detected_from_chart`
- `gap_direction`
- `gap_points`
- `gap_percent`
- `gap_cause_known`
- `gap_cause_source`

Current replay artifacts include unconfirmed macro, IV, and event cautions. The schema should preserve those as unavailable or unconfirmed. Chart gaps may be measured from candles, but gap cause must not be invented.

## Likely Risk vs Full-Risk Notes

The schema should distinguish likely chart risk from full financial risk:

- likely chart risk is the distance from entry reference price to planned invalidation,
- chart R is based on likely chart risk,
- full debit risk, option spread behavior, liquidity, slippage, assignment, and account drawdown are out of scope.

The output may set `full_risk_modeled: false`, `option_pnl_modeled: false`, and `account_sizing_modeled: false` for every v1 record.

## No-Hindsight Rules

No-hindsight rules:

- Entry eligibility uses only replay state and candle data available at or before the signal timestamp.
- Setup identity, stage, trigger level, invalidation level, blockers, cautions, and available context are copied from source artifacts or predeclared candidate input.
- Entry, invalidation, follow-through, failure, and time-stop rules are defined before scanning future candles.
- Future candles are used only to measure post-entry chart behavior.
- Outcome classification stops at the first terminal condition.
- Source-data end produces `unresolved_insufficient_lookahead` when a terminal condition cannot be proven.
- Missing macro, IV, event, headline, 24H, or daily context is marked unavailable or unconfirmed.
- Manual overrides, if ever permitted, require explicit override reason, timestamp, author/source, and the pre-override value.

## Chart-Only Boundary

The v1 schema is chart-only. It may describe underlying candle movement, chart entry references, invalidation references, follow-through thresholds, failure rules, time stops, MFE, MAE, and same-day versus fast-swing classifications.

It must not model or infer:

- option P&L,
- option-spread pricing,
- Greeks,
- bid/ask behavior,
- fill quality,
- slippage,
- broker execution,
- order routing,
- account sizing,
- account drawdown,
- live trade permission.

## Excluded Fields

Explicitly excluded fields:

- option contract symbol,
- option strike,
- option expiration,
- option delta,
- option debit,
- option spread value,
- option P&L,
- position size,
- contracts,
- account balance,
- buying power,
- percent of account risked,
- broker order id,
- fill price,
- partial fills,
- slippage,
- commission,
- live alert routing,
- watcher state mutation.

## Known Limits

- This is a design review only; no schema files are created in this task.
- SPY has three-setup real historical replay coverage; QQQ, IWM, and GLD do not yet have equivalent local real replay closeout evidence.
- Current real replay artifacts are 1H RTH signal/stage/lifecycle artifacts, not trade outcome artifacts.
- 24H/daily, macro, IV, event, and headline context are unavailable or unconfirmed in the current SPY source artifacts.
- Chart gap cause cannot be inferred from candles alone.
- Same-day and fast-swing labels are analysis classifications, not live trade permissions.
- Chart outcome does not equal option outcome.
- Likely chart risk does not equal full account or option-spread risk.
- v1 does not prove production readiness, watcher readiness, proof-mode trading readiness, or account safety.

## Non-Changes

- **`main.py` changed:** no
- **Runner code changed:** no
- **Existing schemas changed:** no
- **Fixtures changed:** no
- **Reports changed:** no
- **Backtesting implementation started:** no
- **Option P&L modeled:** no
- **Account sizing added:** no
- **Watcher implementation started:** no

## Recommended Next Task

Create chart-based trade outcome backtesting v1 schema files only, using this design as the source of truth, without implementing backtesting, modeling option P&L, adding account sizing, changing `main.py`, changing runner behavior, modifying fixtures, modifying reports, or starting watcher implementation.
