# SAFE-FAST Project Master Handoff

## Baseline

- **Current baseline:** `patch8`
- **Active objective:** validate lifecycle fixture shape and decide runner support, with Continuous Watcher foundation planning only
- **Latest completed commit:** `64576a5` - Add continuation lifecycle signal replay fixture
- **On-demand transition status:** READY WITH KNOWN LIMITS
- **Work mode:** docs/build-state and protected build work only unless explicitly expanded
- **Production status:** production readiness is not done
- **Deployment status:** no Railway, deploy, or production file work in this phase
- **Trading status:** no auto-trading; no live trade decisions

## Project Target

The final target is full SAFE-FAST automation with manual trade execution only.

That means the system may eventually automate scanning, setup recognition, lifecycle tracking, state-change alerts, context checks, and trade-plan preparation, but the human remains responsible for entering and managing trades manually. There must be no broker execution, no auto-order placement, and no auto-trading.

## Continuous Watcher Target

The planned automation target is **SAFE-FAST Continuous Watcher v1**:

- Watch-only
- No auto-trading
- Tracks Ideal, Clean Fast Break, and Continuation setups
- Preserves setup identity through blockers and cautions
- Tracks lifecycle changes over time
- Suppresses duplicate alert spam
- Alerts only on meaningful setup, stage, or risk-state changes
- Marks unavailable live fields as unconfirmed
- Requires replay/regression, shadow review, and serious backtesting before promotion

## Already Fixed / Protected

Patch8 has already fixed and protected a large part of on-demand recognition and stage correctness:

- Ideal setup identity survives blockers instead of being mislabeled as Clean Fast Break
- Clean Fast Break identity survives chop/noisy structure blockers
- Ideal identity survives chop/noisy structure blockers
- Winner selection stays deterministic across Ideal, Clean Fast Break, and Continuation candidates
- Spent or prior Continuation candidates are demoted behind fresh valid candidates
- Raw `NO_TRADE` winners cannot override screened `TRADE` candidates
- Stage messaging distinguishes fresh triggers from spent/prior breaks
- Intrabar Continuation breaks do not become completed-candle approval
- Market-closed completed triggers do not become live trades
- Prior-session, weekend, and holiday Continuation carry-forward cases are handled as spent context unless a fresh current-session break appears
- 24H countertrend context is surfaced as caution rather than a hard blocker
- High IV, event-day, and macro-event risk are surfaced as context/caution without destroying setup identity
- Soft extension and workable room can surface as cautions instead of automatic hard blockers
- Cramped room, wall-thesis failure, bad liquidity, missing invalidation, risk mismatch, existing position, and market-closed gates have protected user-facing priority
- ATH/open-air cases surface rebuilt-structure requirements instead of generic room/extension language
- Replay/regression contracts exist for the protected on-demand cases

## What Remains Unproven

The system is not yet proven viable for real manual trading. Remaining unproven areas include:

- Remaining on-demand setup recognition edge cases
- Remaining stage correctness edge cases
- Remaining session-boundary carry-forward edge cases
- Continuous lifecycle memory
- Alert suppression and no duplicate alert spam
- Shadow accuracy review
- Historical signal frequency and quality
- Trade outcome expectancy
- Options spread fill realism
- Drawdown and losing-streak behavior
- Small-account risk limits, especially for the `$1,500` account mode
- Production readiness

Replay/regression proves engine behavior against known cases. It does not prove profitability or live viability.

## Later Planned Account Modes

Account-mode and trade-style logic is planned later. It must not be added until on-demand setup recognition and stage correctness are stable and protected.

Planned account work includes:

- `$1,500` small-account safety mode
- Larger account modes with different sizing ceilings
- Trade-style rules that adapt to account size and risk tolerance
- Hard separation between planned invalidation risk and full debit exposure
- Manual execution only

## Later Planned Levels / Context Indicators

Levels and context indicators are planned later. They should not be added to engine behavior until recognition/stage correctness and the Continuous Watcher foundation are stable.

Planned context work includes:

- Key level ranking
- Nearby walls and first trouble area
- Market structure context
- Optional indicators as caution/context signals
- Indicator-driven hard blockers only when structurally justified

## Later Planned News / Headline Risk

News and headline risk handling is planned later. It must not invent unavailable data.

Planned news/headline work includes:

- Macro events
- Earnings and scheduled company events
- Material headlines
- Filings and regulatory events
- Immediate setup-window risk checks
- Unavailable data marked as unconfirmed

Most news should surface as caution/context. Hard blocks should be reserved for immediate and material risk to the setup, trade window, or hold thesis.

## Mandatory Viability Sequence

The required order is:

1. Finish on-demand setup recognition and stage correctness.
2. Close out on-demand behavior with targeted replay/regression coverage.
3. Build serious historical signal replay.
4. Build serious trade outcome backtesting.
5. Review shadow accuracy and risk behavior.
6. Only then consider proof-mode manual trading.
7. Later, build Continuous Watcher v1.
8. Later, add account modes, levels/context, and news/headline risk.

No auto-trading is allowed at any point.

## 22-Day Roadmap

### Days 1-4: On-Demand Closeout

- Find remaining recognition/stage failures one at a time
- Add replay/regression cases before engine behavior changes
- Preserve Ideal, Clean Fast Break, and Continuation identity through blockers
- Confirm user-facing stage language is specific and correct
- Keep `main.py` changes minimal and covered when engine changes are explicitly allowed

### Days 5-7: Closeout Regression Proof

- Run full local replay/regression
- Confirm fixture coverage is real and not placeholder scaffold
- Confirm no old repo, deploy, Railway, or production drift
- Update build state only with verified results

### Days 8-11: Historical Signal Replay v1

- Replay SPY, QQQ, IWM, and GLD bar by bar
- Emit on-demand-style setup states without hindsight
- Track setup type, stage, blockers, cautions, invalidation, and trigger status
- Measure signal frequency and setup/ticker distribution

### Days 12-16: Trade Outcome Backtest v1

- Convert qualifying historical signals into manual-trade-style outcome paths
- Model debit spreads, bid/ask, slippage, missed fills, target hits, invalidations, and full debit loss
- Report planned invalidation risk separately from full debit exposure
- Produce win rate, expectancy, drawdown, losing streak, and setup/ticker performance

### Days 17-19: Risk and Small-Account Review

- Stress test the `$1,500` account mode
- Treat full debit exposure as a hard account safety cap
- Compare planned-risk model, full-debit model, and stressed full-debit events
- Identify setups that are structurally valid but unsuitable for small-account sizing

### Days 20-22: Proof-Mode Manual Trading Readiness Review

- Review replay, backtest, and shadow-read evidence
- Decide whether proof-mode manual trading is justified
- Keep all execution manual
- Document remaining production blockers
- Do not promote to production or auto-trading

## Next Laptop Task Discipline

Next laptop tasks must stay narrow:

- Start from `patch8`
- Use the latest completed commit context: `64576a5`
- Validate lifecycle fixture shape and decide runner support
- Limit Continuous Watcher work to foundation planning only
- Do not start trade outcome backtesting implementation yet
- Do not make engine changes unless explicitly authorized and covered first
- Update build state with verified facts only
- Stop after the requested task

Do not touch Railway, deploy, production files, old repos, or auto-trading behavior.
