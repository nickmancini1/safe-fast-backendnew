# Real Historical Replay v1 Data Expansion Plan

## Planning Status

Planning status: complete.

This is a docs-only plan for expanding Historical Signal Replay v1 from no-hindsight sample fixture shapes into real historical replay v1 data sequences. Real historical replay implementation has not started.

## Purpose

Real historical replay v1 should prove whether SAFE-FAST can walk forward through real historical RTH bar sequences and emit the correct signal, stage, lifecycle, blocker, caution, and duplicate-suppression states without hindsight.

The purpose is decision-support validation only. It is not profitability proof, trade outcome backtesting, option P&L modeling, account sizing, broker execution, production behavior, live trade decisioning, or Continuous Watcher implementation.

## What Historical Signal Replay v1 Already Proves

Historical Signal Replay v1 already proves the local replay foundation can:

- Validate input and output fixture shapes for the allowed universe: SPY, QQQ, IWM, and GLD.
- Represent the three allowed setup families: Ideal, Clean Fast Break, and Continuation.
- Emit signal/stage rows for the current fixture set.
- Emit summaries and regression candidate reports.
- Track Continuation lifecycle rows across developing, pending, triggered, and spent/no-fresh-trigger states.
- Track repeated unchanged states and mark duplicate-suppressed rows.
- Preserve the boundary that regression candidates are signal/stage/lifecycle metadata only.

## What Real Historical Replay v1 Must Prove Next

Real historical replay v1 must prove the same signal/stage/lifecycle behavior on real historical bar sequences:

- Bars are processed in timestamp order using only information available at each row timestamp.
- Setup identity remains stable for Ideal, Clean Fast Break, and Continuation through blockers and cautions.
- Developing states do not become triggers before the required trigger condition exists.
- Pending states remain pending until the required completed-candle or stage condition is met.
- Triggered states are emitted only when the historical row has enough no-hindsight evidence.
- Blocked/no-trade states surface the correct primary blocker.
- Spent or prior-session context does not become a fresh trigger.
- Repeated unchanged states are suppressible duplicates, while real state changes remain meaningful alert candidates.

## Allowed Universe

Real historical replay v1 data expansion is limited to:

- SPY
- QQQ
- IWM
- GLD

## Allowed Setup Families

Real historical replay v1 data expansion is limited to:

- Ideal
- Clean Fast Break
- Continuation

## Proposed First Historical Sequence Types

1. Ideal developing to valid trigger or blocked/no-trade state.
2. Clean Fast Break developing to valid trigger or blocked/no-trade state.
3. Continuation developing to pending/completed/spent lifecycle.
4. Repeated unchanged state sequence for duplicate suppression.
5. Session-boundary sequence where prior-session context must not become a fresh trigger.
6. Headline/elevated gap-risk note as context only, not trade outcome proof.

## Proposed Minimum Coverage Matrix

Minimum v1 coverage should document at least one planned sequence for each required coverage area below before expanding into larger historical windows.

| Coverage area | Minimum v1 requirement |
| --- | --- |
| SPY | At least one real historical sequence |
| QQQ | At least one real historical sequence |
| IWM | At least one real historical sequence |
| GLD | At least one real historical sequence |
| Ideal | At least one developing-to-trigger or developing-to-blocked sequence |
| Clean Fast Break | At least one developing-to-trigger or developing-to-blocked sequence |
| Continuation | At least one developing-to-pending-to-triggered-to-spent lifecycle sequence |
| Bullish/call-side where applicable | At least one applicable bullish sequence for each setup family where historical structure supports it |
| Bearish/put-side where applicable | At least one applicable bearish sequence for each setup family where historical structure supports it |
| Developing state | At least one row where setup is valid to watch but not ready |
| Pending state | At least one row where completed-candle or equivalent stage confirmation is still required |
| Triggered state | At least one row where the signal-stage trigger is valid without future bars |
| Blocked state | At least one row where setup identity remains but final verdict is NO_TRADE due to a blocker |
| Spent/no-fresh-trigger state | At least one row where prior trigger context is spent and cannot be treated as fresh |
| Repeated same-state suppressed state | At least one repeated unchanged observation with duplicate suppression |

## No-Hindsight Rules

- Each replay row may use only bars and context available at or before that row timestamp.
- Future candles must not be used to decide setup identity, trigger state, blocker priority, or lifecycle state.
- Session context must be assigned from the row timestamp, not from later session knowledge.
- Headline, macro, IV, event, and gap-risk context must include `as_of` and source status when available.
- Unavailable context must be marked unconfirmed instead of inferred.
- A historical sequence may be labeled after selection for review, but row-level expected output must not rely on future outcome.
- The plan must not classify a later profitable move as proof that an earlier signal was valid.

## Data Requirements

Each real historical sequence should include:

- Symbol from the allowed universe.
- Timestamped RTH candles with open, high, low, close, and volume.
- Session calendar metadata with session date, type, timezone, and regular-session flag.
- 24H/daily context when available, or explicit unconfirmed status.
- Macro context when available, or explicit unconfirmed status.
- IV context when available, or explicit unconfirmed status.
- Event/headline/gap-risk context when available, or explicit unconfirmed status.
- Expected signal/stage/lifecycle output shape for each row.

## Timestamp And Session Requirements

- Use timezone-aware timestamps.
- Use `America/New_York` for RTH session interpretation.
- Preserve the actual bar timestamp cadence used by the source data.
- Keep session date separate from row timestamp.
- Mark regular, short, closed, or unknown sessions explicitly.
- Do not allow prior-session, weekend, or holiday carry-forward context to create a fresh current-session trigger.
- Session-boundary sequences must include enough rows to show prior context and the current-session decision point.

## Lifecycle Requirements

Real historical replay v1 should preserve:

- `first_seen`
- `last_seen`
- `prior_state`
- `current_state`
- `state_changed`
- `trigger_changed`
- `blocker_changed`
- `duplicate_alert_suppression_key`

Continuation lifecycle coverage should include developing, pending, triggered, and spent/no-fresh-trigger states. Ideal and Clean Fast Break sequences should include developing-to-trigger or developing-to-blocked/no-trade transitions where historical structure supports them.

## Duplicate And State-Change Requirements

- A meaningful alert candidate requires a real setup, trigger, or blocker state change.
- Repeated unchanged state rows should keep the same duplicate alert suppression key.
- Repeated unchanged state rows should set state, trigger, and blocker changes to false.
- Duplicate-suppressed rows must not imply a new trade decision.
- A changed blocker on the same setup should be treated as a meaningful state change, not a duplicate.

## Output And Report Requirements

Real historical replay v1 outputs should remain compatible with the existing signal replay output fields:

- Signal log rows.
- Summary counts.
- Regression candidate rows.
- Setup type counts.
- Final verdict counts.
- Blocker counts.
- Stage counts.
- Lifecycle change counts.
- Duplicate alert suppression key counts where applicable.
- Meaningful alert candidate counts where applicable.
- Duplicate-suppressed counts where applicable.

Reports must remain signal/stage/lifecycle reports only. They must not include win rate, expectancy, target hit, stop hit, option price, spread price, slippage, account risk, or P&L.

## Validation Requirements

Before accepting first real historical replay v1 data sequences:

- Validate schema JSON syntax.
- Validate fixture/data JSON syntax.
- Run the existing historical signal replay runner.
- Run all on-demand contract tests.
- Run the stage-message test.
- Run fixture validation.
- Run full replay regression.
- Confirm `main.py` is unchanged unless separately authorized.
- Confirm replay tests, schemas, existing fixtures, generated reports, deploy files, and production files were not changed by planning-only work.
- Confirm no trade outcome backtesting, option P&L modeling, account sizing, broker execution, auto-trading, live trade decisions, or Continuous Watcher implementation were started.

## Known Limits

- This plan does not implement real historical replay.
- This plan does not add data fixtures.
- This plan does not change the runner.
- This plan does not change schemas.
- This plan does not change metrics.
- This plan does not change replay tests.
- This plan does not prove profitability.
- This plan does not prove option contract performance.
- This plan does not prove account sizing.
- This plan does not prove production readiness.
- This plan does not implement Continuous Watcher behavior.
- Headline/elevated gap-risk coverage is context-only and does not prove trade outcomes.

## Signal/Stage/Lifecycle Boundary

Real historical replay v1 is signal/stage/lifecycle replay only.

It may prove that SAFE-FAST recognized a historical setup state, lifecycle transition, blocker, caution, or duplicate-suppression condition correctly at a point in time. It must not claim that a trade should have been taken, that the trade won or lost, that options would have filled, that an account could size the trade, or that a live/manual decision is justified.

## Recommended Next Task

Create the first real historical replay v1 fixture/data sequence while staying signal/stage/lifecycle only.
