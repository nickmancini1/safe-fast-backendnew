# SAFE-FAST Day 41 QQQ CFB Stale/Spent Expiry Decision

## Scope

Candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Symbol/setup: QQQ / Clean Fast Break.

Setup/signal time: `2026-04-13T12:30:00-04:00`.

Baseline: `07ea738 Record QQQ CFB stale spent expiry decision needed`.

This is a lifecycle-rule decision for testing only. It does not fill evidence, add regression rows, backtest, choose a trade, calculate P&L, mark QQQ ready, accept proof, or claim profitability.

## Accepted First Rule

The first usable QQQ Clean Fast Break lifecycle rule is same-candle initial-break freshness with spent-state preservation and explicit higher-base refresh requirements.

The rule is intentionally conservative:

- an initial-break signal is fresh only at the completed signal candle decision timestamp;
- the same trigger path cannot remain fresh after that timestamp;
- a completed break or follow-through consumes the trigger path and makes later reuse spent;
- a later higher base may create a new eligible path only when it has a source-backed new trigger, new invalidation, and fresh completed breakout;
- missing lifecycle inputs produce `unknown`, not an inferred fresh/stale/spent/expired state.

## State Definitions

`fresh`: the decision timestamp is exactly the source-backed completed QQQ Clean Fast Break initial-break signal candle, the row has matching symbol/setup identity, a trigger and invalidation are present, the trigger state is `triggered`, and no prior completed break has already consumed that trigger path at or before the decision timestamp.

`stale`: a QQQ Clean Fast Break watch or candidate path has a source-backed trigger/invalidation context but does not have a completed breakout at the decision timestamp. Stale is a no-trade/watch-only lifecycle state until a fresh completed breakout is source-backed. A stale path must not be promoted by proximity to trigger.

`spent`: a QQQ Clean Fast Break trigger path has already produced a completed initial break, follow-through context, or explicit prior-completed-break blocker. The same trigger path cannot be reused as a fresh signal.

`expired`: a previously fresh initial-break signal is reviewed at any timestamp after its exact signal candle decision timestamp and is not classified as spent by higher-precedence spent evidence. Expired means the first-rule freshness window has closed.

`unknown`: required lifecycle data or rule metadata is missing, ambiguous, wrong-symbol, wrong-setup, malformed, or contaminated by future data. Unknown cannot pass evidence validation.

## Timing Decisions

Freshness window: exact signal candle decision timestamp only. For the target candidate, the known fresh regression target is `2026-04-13T12:30:00-04:00`.

Stale timing: a watch or candidate path without a completed breakout is stale at each review timestamp until a completed breakout occurs or the path is replaced by a new accepted setup path. For QQQ CFB, trigger proximity without `trigger_state=triggered` is not fresh.

Spent behavior: after a completed initial break or follow-through is source-backed, later rows that reuse the same trigger path are spent. Same-session follow-through does not refresh the initial signal.

Expiry clock: the expiry clock starts at the initial-break signal decision timestamp. The boundary is inclusive only at the exact signal candle timestamp. Any later timestamp is outside the freshness window and is expired unless spent has higher precedence.

Higher-base refresh behavior: a later higher-base watch is not fresh by itself. It can become fresh only at a later completed breakout decision timestamp when all of these are source-backed before or at that timestamp:

- a new higher-base stage;
- a new trigger level;
- a new invalidation level;
- a completed breakout with `trigger_state=triggered`;
- no prior completed break has already consumed that new trigger path.

## State Precedence

Apply states in this order:

1. `unknown` when required identity, timestamp, trigger, invalidation, stage, trigger state, prior-state, or lifecycle-rule metadata is missing or invalid.
2. `spent` when the same trigger path has already completed or a row carries source-backed prior-completed-break/follow-through/spent evidence.
3. `fresh` when the current decision timestamp is exactly the completed initial-break or accepted higher-base breakout timestamp.
4. `expired` when a previously fresh initial-break timestamp is reviewed after the freshness boundary and no spent evidence applies.
5. `stale` when a watch/candidate path exists but has not completed a fresh breakout at the decision timestamp.

Blocked or invalidated rows are not upgraded to fresh. If blocker/invalidation handling is needed but the accepted metadata is missing, the lifecycle state is `unknown` for evidence-fill purposes.

## Missing-Data Behavior

Return `unknown` when any required field is missing or ambiguous:

- symbol;
- setup type;
- decision timestamp;
- setup or stage identity;
- trigger state;
- trigger level;
- invalidation level;
- prior state or prior completed-break marker needed to detect spent;
- accepted lifecycle rule metadata;
- source-backed row ordering.

Wrong symbol, wrong setup type, malformed timestamp, duplicated ambiguous rows, or no-hindsight boundary ambiguity also produce `unknown`.

## Future-Data Rejection

Lifecycle decisions may use only rows and fields at or before the decision timestamp.

The rule must reject:

- future candles;
- future replay rows;
- later follow-through rows when deciding earlier freshness;
- outcome evidence;
- option data;
- fills;
- P&L;
- profitability;
- readiness or promotion labels.

For the target candidate, the `2026-04-13T15:30:00-04:00` spent row must not be used to decide freshness at `2026-04-13T12:30:00-04:00`; it is only a later spent regression case.

## Required Regression Fixture Cases

Before lifecycle evidence fill, add data-only regression fixtures for:

- target fresh initial-break signal at `2026-04-13T12:30:00-04:00`;
- same-session follow-through at `2026-04-13T15:30:00-04:00` classified `spent`, not fresh;
- higher-base watch at `2026-04-16T13:30:00-04:00` classified stale/watch-only until a fresh completed breakout exists;
- prior completed break/no-fresh-trigger at `2026-04-17T15:30:00-04:00` classified `spent`;
- boundary case where exact signal timestamp is `fresh` and the next later review timestamp is not fresh;
- expired case for a previously fresh signal reviewed after its exact signal timestamp without spent evidence;
- missing trigger, missing invalidation, missing timestamp, missing setup stage, missing prior-state data, wrong symbol, and wrong setup type producing `unknown`;
- future replay row rejection;
- future candle rejection;
- option/fill/P&L/profitability/readiness fields ignored;
- precedence case where spent and expired could both apply, with `spent` winning;
- precedence case where missing required data forces `unknown`.

## Target Row Interpretation

- Replay line 3, `2026-04-13T12:30:00-04:00`: fresh initial-break regression target.
- Replay line 4, `2026-04-13T15:30:00-04:00`: spent same-session follow-through regression target.
- Replay line 5, `2026-04-16T13:30:00-04:00`: stale/watch-only higher-base context until a fresh completed breakout exists.
- Replay line 6, `2026-04-17T15:30:00-04:00`: spent prior-completed-break/no-fresh-trigger regression target.

## Current Result

Accepted lifecycle rule: YES, for first QQQ CFB testing only.

Lifecycle regression rows added: NO.

Evidence filled: NO.

Backtest authorized: NO.

Trade chosen: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Proof accepted: NO.

Profitability claimed: NO.
