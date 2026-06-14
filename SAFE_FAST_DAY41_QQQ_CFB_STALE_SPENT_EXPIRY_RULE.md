# SAFE-FAST Day 41 QQQ CFB Stale/Spent Expiry Rule

## Scope

Candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Symbol/setup: QQQ / Clean Fast Break.

Setup/signal time: `2026-04-13T12:30:00-04:00`.

Baseline: `17d433e Fill QQQ CFB gap context evidence`.

This is a rule-definition review only. It does not fill evidence, add regression rows, backtest, choose a trade, calculate P&L, mark QQQ ready, accept proof, or claim profitability.

## Existing Repo Language Found

Current source artifacts show lifecycle labels but not an accepted reusable stale/spent/expiry rule:

- `SAFE_FAST_RULE_FAMILY_DECISION_TABLE.md` marks `Clean Fast Break expiry` as `SOURCE_DATA_INSUFFICIENT`.
- `historical_signal_replay/source_data/richer_export_package_work/qqq_cfb_stale_spent_expiry_rule_regressions.jsonl` requests `clean_fast_break_stale_spent_expiry_rule` and `clean_fast_break_expiry_regression_rows`, and both are unresolved.
- `historical_signal_replay/reports/first_real_qqq_clean_fast_break_replay_v1_signal_log.jsonl` line 3 records the target setup as `current_state=signal`, `setup_state=initial_break_candidate`, `stage=clean_fast_break_initial_break_candidate`, `trigger_state=triggered`, and `final_verdict=TRADE`.
- The same QQQ log line 4 records later same-session follow-through as `current_state=spent`, `setup_state=follow_through_context`, `stage=clean_fast_break_follow_through_confirming_context`, `trigger_state=follow_through`, and `primary_blocker=prior_completed_clean_fast_break_spent`.
- Line 5 records a later higher-base watch state with `primary_blocker=fresh_completed_breakout_required`.
- Line 6 records a later post-break state as `current_state=spent`, `setup_state=spent`, `stage=clean_fast_break_post_break_no_fresh_trigger`, `trigger_state=spent`, and `primary_blocker=prior_completed_clean_fast_break_spent`.

These labels are useful regression targets, but they do not by themselves define a complete accepted rule.

## Current Rule Status

An honest accepted QQQ Clean Fast Break stale/spent/expiry rule is still not fully defined from repo evidence.

The repo supports these bounded observations for the target sample:

- The `2026-04-13T12:30:00-04:00` QQQ row is a setup-time initial-break signal candidate.
- The later `2026-04-13T15:30:00-04:00` row is same-session follow-through context and is marked spent, not a fresh new trigger.
- A later higher-base watch can exist only as a watch state until a fresh completed breakout is source-backed.
- A later post-break/no-fresh-trigger row remains spent and cannot reuse the prior completed break as a fresh signal.

The repo does not yet define these required reusable decisions:

- exact stale timing for an untriggered or delayed QQQ CFB setup;
- exact expiry timing for an initial-break signal;
- whether expiry is same-candle, next-candle, same-session, session-boundary, or higher-base dependent;
- whether a higher-base continuation can refresh the setup and under what trigger/invalidation source;
- precedence between fresh, stale, spent, invalidated, blocked, and expired states.

## Required Rule Shape

The accepted future rule must explicitly define the following fields before evidence fill or backtest:

- `fresh`: the setup is still eligible at the decision timestamp because a source-backed QQQ Clean Fast Break trigger path exists, the trigger/invalidation are current, required context gates are not missing, and no prior completed break has already consumed that trigger path.
- `stale`: the setup shape exists but is no longer eligible at the decision timestamp because the allowed freshness window or required confirmation window has passed without a fresh completed breakout. The exact timing is not decided.
- `spent`: the setup has already produced a completed break or follow-through lifecycle state, so the prior trigger path cannot be reused as a new fresh signal unless a new accepted higher-base/fresh-break rule creates a new trigger path.
- `expired`: the setup is no longer eligible for promotion or trade-plan counting under the accepted CFB expiry rule. The exact expiry clock is not decided.
- `decision_timestamp`: the candle or review timestamp at which the lifecycle decision is made.
- `allowed_data`: QQQ source rows, trigger/invalidation, setup stage, blocker/context fields, and lifecycle rows at or before the decision timestamp only.
- `forbidden_future_data`: future candles, future replay rows, later follow-through, outcome evidence, option data, fills, P&L, profitability, and readiness must not backfill the setup-time lifecycle decision.
- `missing_data`: if trigger, invalidation, setup stage, source timestamp, symbol/setup identity, or accepted lifecycle rule metadata is missing, the lifecycle result must be `unknown` or blocked and cannot pass content validation.

## Current Target Interpretation

For this candidate, line 3 can be used as a future regression target for a fresh initial-break candidate only after the stale/spent/expiry rule is accepted.

Line 4 can be used as a future regression target for a spent same-session follow-through state.

Line 5 can be used as a future regression target for a higher-base watch state requiring a fresh completed breakout.

Line 6 can be used as a future regression target for a prior completed break remaining spent.

These are not evidence fills and do not mark the candidate ready.

## Regression Fixture Cases Needed Next

Before any lifecycle evidence fill, add regression cases for:

- QQQ initial-break signal at `2026-04-13T12:30:00-04:00` classified fresh under the accepted rule.
- QQQ same-session follow-through at `2026-04-13T15:30:00-04:00` classified spent, not fresh.
- QQQ higher-base watch at `2026-04-16T13:30:00-04:00` blocked until a fresh completed breakout exists.
- QQQ post-break/no-fresh-trigger at `2026-04-17T15:30:00-04:00` classified spent.
- Missing trigger, missing invalidation, missing source timestamp, wrong symbol, and wrong setup type produce `unknown` or blocked.
- Future replay rows after the decision timestamp cannot affect the decision.
- Outcome, option quote, fill, P&L, profitability, or readiness fields cannot affect the decision.
- Boundary case for the exact stale/expiry clock once that clock is decided.
- Precedence case where invalidated, blocked, spent, stale, and expired signals compete.

## Current Result

Accepted lifecycle rule: NO.

Decision-needed doc created: YES, `SAFE_FAST_DAY41_QQQ_CFB_STALE_SPENT_EXPIRY_DECISION_NEEDED.md`.

Evidence filled: NO.

Backtest authorized: NO.

Trade chosen: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Proof accepted: NO.

Profitability claimed: NO.
