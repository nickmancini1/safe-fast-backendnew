# SAFE-FAST On-Demand Transition Readiness Review

## Current baseline

- **Baseline:** `patch8`
- **Active objective:** on-demand setup recognition and stage correctness
- **Latest completed commit:** `64e04b7 Protect put continuation trigger stage`
- **Review date:** 2026-05-10
- **Review scope:** docs and regression-readiness review only
- **Engine changes in this review:** none
- **`main.py` changed in this review:** no

## Review status

**READY WITH KNOWN LIMITS**

On-demand setup recognition and stage correctness are ready to move into the next phase of **Historical Signal Replay v1 planning** and **Continuous Watcher foundation planning**, but not into production, proof-mode manual trading, auto-trading, or trade outcome backtesting implementation.

## Exact reason for status

The known on-demand recognition and stage-correctness failure classes are now protected by targeted contracts, stage-message coverage, fixture validation, and full replay regression. The required local sweep passed:

- On-demand contract tests: all `replay/test_on_demand_*contract.py` files passed
- Stage-message contract: passed
- Fixture validation: passed
- Full replay regression: `16/16 passed | local_fixture_engine=16 | placeholder_scaffold=0`

The status is not full READY because replay/regression proves behavior only against known cases. It does not prove historical signal quality, lifecycle accuracy over time, alert suppression, options economics, drawdown behavior, small-account suitability, production readiness, or live viability.

## Fixed and protected areas

- Ideal identity survives blockers and chop/noisy structure cases.
- Clean Fast Break identity survives blockers, chop/noisy structure, and stale/spent Continuation context.
- Continuation identity and stage behavior are protected across developing, pending, spent, prior-session, weekend, holiday, and put-side shelf-break paths.
- Winner selection is protected across Ideal, Clean Fast Break, Continuation, stale/spent candidates, and raw `NO_TRADE` override risk.
- Intrabar shelf breaks do not become completed-candle approval.
- Completed triggers while the market is closed do not become live trades.
- Fresh current-session Continuation breaks are not suppressed by older spent prior-session breaks.
- User-facing stage surfaces humanize prior spent breaks, pending completed-candle approval, market-closed waits, next-bar hold failures, and ATH/open-air rebuilt-structure blockers.
- 24H countertrend, macro event risk, IV/event-day risk, soft extension, and workable/tight room can surface as cautions without destroying setup identity.
- Cramped room, wall-thesis failure, bad liquidity, missing invalidation, risk mismatch, existing open position, market closed, and time-gate blockers have protected priority.

## Remaining unproven areas

- Unknown on-demand recognition edge cases outside the current contract set.
- Unknown stage-correctness edge cases outside the current contract set.
- Historical bar-by-bar signal frequency and setup quality.
- Lifecycle memory across time.
- Duplicate alert suppression and meaningful state-change alerting.
- Shadow accuracy review.
- Options spread fill realism.
- Trade outcome expectancy.
- Drawdown and losing-streak behavior.
- Small-account safety for the `$1,500` account mode.
- Production readiness.

## Replay and regression evidence

- Contract files inspected: all existing `replay/test_on_demand_*contract.py` files.
- Stage-message test inspected and run: `replay/test_on_demand_stage_messages.py`.
- Fixture validation inspected and run: `replay/validate_fixtures.py`.
- Replay runner inspected and run: `replay/run_replay.py`.
- Regression workflow inspected: `.github/workflows/safe-fast-regression.yml`.
- Workflow coverage: contract sweep, stage-message contract, fixture validation, and replay regression.
- Local replay result: `16/16 passed | local_fixture_engine=16 | placeholder_scaffold=0`.

## Required next phase

The required next phase is **Historical Signal Replay v1 planning**, with **Continuous Watcher foundation planning** limited to interfaces, state snapshots, lifecycle fields, no-duplicate-alert rules, and watch-only constraints.

## Backtesting implementation decision

Trade outcome backtesting implementation should **not** start next.

Historical Signal Replay v1 must come first because the project still needs no-hindsight, bar-by-bar evidence that the engine recognizes setup type, stage, blockers, cautions, trigger state, invalidation, and setup lifecycle correctly over historical data. Trade outcome backtesting depends on that signal stream. Starting outcome backtesting before the historical signal replay layer would mix setup-recognition proof with profitability assumptions and could hide recognition or stage defects behind outcome scoring.

## Continuous Watcher decision

Continuous Watcher should **start only as foundation planning**, not production implementation.

Planning is appropriate now because on-demand output shape, stage states, and protected recognition behavior are stable enough to define watcher state snapshots and lifecycle transitions. Implementation should wait until Historical Signal Replay v1 defines the no-hindsight signal stream and exposes any additional regression candidates. The watcher must remain watch-only, with no broker execution and no live trade decisions.

## Hard no-go items

- Do not touch Railway.
- Do not touch deploy or production files.
- Do not add broker execution.
- Do not add auto-order placement.
- Do not add auto-trading.
- Do not make live trade decisions.

## Manual-trading-only final target

The final target remains SAFE-FAST automation with **manual trade execution only**. Automation may eventually support scanning, recognition, lifecycle tracking, alerts, context checks, and trade-plan preparation, but the human must remain responsible for trade entry and management.

## Risk-model reminder

Future historical reports and trade outcome backtests must keep these risk numbers separate:

- **Planned invalidation risk:** the expected managed loss if exiting at the planned 1H invalidation.
- **Full debit exposure:** the hard worst-case account risk if the debit spread goes to zero or cannot be exited.

These must not be blended. For the `$1,500` account mode, full debit exposure must remain a hard account safety cap.

## Repo-state note

`SAFE_FAST_PROJECT_MASTER_HANDOFF.md` still lists `b365947` as the latest completed commit, while local `git log` and the current task baseline identify `64e04b7 Protect put continuation trigger stage` as the latest completed commit. This review uses `64e04b7`.
