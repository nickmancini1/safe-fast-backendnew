# SAFE-FAST Day 45 Next Grouped Build Task

## Chosen Path

Next grouped task: trade-rule package.

Do not start with a backtest-prep harness, candidate comparison expansion, full-window data approval package, or setup-family repair package. Those are useful later, but the current blocker is the missing trade-plan rule set.

## Baseline For Next Task

- Content validator: `9` passed requests, `0` failed requests.
- Bridge: `4` reconsideration-eligible candidates, `0` intake-ready candidates, proof allowed `NO`.
- Best first reference: `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`.
- Paired repair/failure references: `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` and `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.
- Parked replacement families: QQQ Continuation 001, QQQ Ideal 001, SPY Continuation 001.

## Task Goal

Create the first conservative grouped trade-rule package for Clean Fast Break backtest-prep readiness without running a backtest or downloading full-window data.

## Required Outputs

- Define candidate-level entry rule.
- Define selected-contract use rule for starter/backtest-prep scope.
- Define long-call fill price rule.
- Define exit rule.
- Define stop/invalidation rule.
- Define time exit rule.
- Define cost/slippage/spread rule.
- Define no-trade/failure diagnosis labels.
- Define minimum sample-size and promotion placeholders if final thresholds cannot be honestly accepted yet.
- Add regression cases before any implementation or evidence counting.

## Candidates To Use

- Primary reference: `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`.
- Paired no-trade/repair reference: `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`.
- Failed-execution reference: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

## Exclusions

- No backtest.
- No P&L.
- No full-window Databento download.
- No evidence fill unless a later task explicitly authorizes it.
- No `main.py`, trading logic, broker/order/account, Railway/deploy, `.env`, or secrets changes.

## Success Criteria

The next task succeeds if it produces a rule package that says exactly when a candidate enters, what option contract is used, how fill and exit prices are measured, when the setup is a no-trade, what costs/slippage apply, and what regression cases must pass before backtest-prep.

