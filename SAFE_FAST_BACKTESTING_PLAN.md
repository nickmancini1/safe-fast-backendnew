# SAFE-FAST Backtesting Plan

## Purpose

Replay/regression proves engine behavior. It does not prove profitability.

The SAFE-FAST viability proof needs two separate historical phases after on-demand closeout and before proof-mode manual trading:

1. **Historical signal replay v1**
2. **Trade outcome backtest v1**

Both phases must be no-hindsight, bar-by-bar, and limited to manual-trading proof. No auto-trading is allowed.

## Test Universe

Initial historical work must cover:

- `SPY`
- `QQQ`
- `IWM`
- `GLD`

These tickers should be evaluated separately and together so the reports can show setup/ticker performance instead of hiding weak areas in an aggregate result.

## Phase 1: Historical Signal Replay v1

Historical signal replay answers whether the engine recognizes the right setup and stage at the right time. It does not score profitability.

Required behavior:

- Replay historical bars in chronological order
- Use only information available at each bar
- Emit on-demand-style state snapshots
- Preserve Ideal, Clean Fast Break, and Continuation identity
- Record blockers, cautions, stage, trigger state, invalidation, target context, and no-trade reason
- Track when a setup appears, matures, fails, becomes spent, or remains pending
- Exclude hindsight labels from engine decisions

Outputs:

- Signal counts by ticker
- Signal counts by setup type
- Trade-ready vs pending vs no-trade distribution
- Blocker/caution distribution
- Stage correctness review samples
- Regression candidates for any incorrect recognition or stage behavior

## Phase 2: Trade Outcome Backtest v1

Trade outcome backtest answers whether recognized setups have acceptable manual-trading economics under realistic constraints.

Required behavior:

- Convert qualifying historical replay signals into simulated manual trade plans
- Evaluate outcomes bar by bar after signal time
- Use no future data when deciding entry, exit, invalidation, or target handling
- Separate setup recognition from trade outcome scoring
- Model missed trades when the required fill is unrealistic
- Record whether targets, invalidation, timeout, or full debit loss occurred

## No-Hindsight Bar-By-Bar Rules

The backtest must obey these rules:

- No using future candles to approve a setup
- No using the eventual high/low to choose a better entry
- No using final outcome to choose spread width or target
- No retroactive invalidation movement
- No assuming fills inside the bid/ask spread without a fill model
- No deleting losing signals because later context looked unfavorable
- No upgrading a setup after it fails unless a new historical bar creates a new valid setup

## Options Spread Realism

The first trade outcome backtest must model debit spreads realistically enough to avoid fake expectancy.

Required modeling:

- Debit spreads, not naked directional exposure
- Bid/ask spread at entry and exit
- Slippage assumptions
- Missed fills
- Spread width constraints
- Expiration selection assumptions
- Liquidity filters
- Maximum debit per trade
- Target fill realism
- Invalidation exit fill realism

The report must clearly label assumptions that are estimated or unavailable.

## Risk Model

The risk model must separate two different risk numbers:

1. **Planned invalidation risk**
2. **Full debit exposure**

### Planned Invalidation Risk

Planned invalidation risk is the expected managed loss if exiting at the 1H invalidation.

This is the trade-plan risk used to judge whether the setup has a reasonable manual exit thesis. It depends on the planned invalidation, expected option-spread value near invalidation, bid/ask, slippage, and whether the exit is realistically available.

### Full Debit Exposure

Full debit exposure is the hard worst-case account risk.

This is the maximum loss if the debit spread goes to zero or cannot be exited before full loss. It must be treated as real account risk, even when the planned invalidation exit is expected to happen earlier.

For the `$1,500` account, full debit exposure must act as a hard account safety cap.

## Required Reports

Every trade outcome report must show:

- Planned-risk model results
- Full-debit model results
- Stressed full-debit events
- Win rate
- Expectancy
- Drawdown
- Losing streak
- Setup performance
- Ticker performance
- Setup/ticker performance
- Target hit distribution
- Invalidation exit distribution
- Missed-fill rate
- Average bid/ask cost
- Slippage sensitivity

The planned-risk model and full-debit model must never be blended into one number.

## Core Metrics

Required metrics:

- Win rate
- Expectancy
- Maximum drawdown
- Average drawdown
- Losing streak
- Setup performance
- Ticker performance
- Setup/ticker performance
- Target hit distribution
- Average win
- Average planned invalidation loss
- Average full debit loss
- Missed-fill rate
- Slippage sensitivity

## Small Account Safety

The `$1,500` account requires stricter reporting:

- Full debit exposure is a hard account safety cap
- Planned invalidation risk is not enough by itself
- A trade can be valid structurally but still fail small-account safety
- Reports must show how many trades pass structure but fail full-debit account limits
- Reports must show drawdown under planned-risk and full-debit assumptions
- Stressed full-debit events must be shown explicitly

## Promotion Gates

Proof-mode manual trading cannot be considered until:

- On-demand closeout is complete
- Historical signal replay v1 is complete
- Trade outcome backtest v1 is complete
- Reports separate planned invalidation risk from full debit exposure
- SPY, QQQ, IWM, and GLD have ticker-specific results
- Debit-spread realism is included
- Small-account full-debit safety is reviewed
- No auto-trading has been added

Backtesting can justify further research or proof-mode manual trading. It cannot justify auto-trading.
