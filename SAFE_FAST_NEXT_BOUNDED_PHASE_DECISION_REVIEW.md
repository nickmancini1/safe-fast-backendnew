# SAFE-FAST Next Bounded Phase Decision Review

## Decision Status

- **Decision status:** PASS
- **Baseline:** patch8
- **Latest local commit reviewed:** `d417b01 Add SPY three-setup real historical replay closeout`
- **Current objective:** decide the next bounded phase after SPY three-setup real historical replay closeout.
- **Review scope:** docs-only phase decision review.

## Inputs Reviewed

- `SAFE_FAST_BUILD_STATE.md`
- `historical_signal_replay/REAL_HISTORICAL_REPLAY_V1_SPY_THREE_SETUP_CLOSEOUT_REVIEW.md`
- `historical_signal_replay/REAL_HISTORICAL_REPLAY_V1_DATA_EXPANSION_PLAN.md`
- `SAFE_FAST_ACCOUNT_MODE_AND_TRADE_STYLE_PLAN.md`
- `SAFE_FAST_PROJECT_MASTER_HANDOFF.md`

## Current State

The SPY three-setup real historical replay closeout passed. SPY now has real historical signal/stage/lifecycle coverage for all three allowed setup families:

- Continuation
- Ideal
- Clean Fast Break

The closeout also confirmed runner output validation for all three SPY fixtures and preserved the boundary that no trade outcome backtesting, option P&L, account sizing, watcher implementation, auto-trading, or live trade decisions were started.

## Options Compared

### 1. Add QQQ/IWM/GLD Real Historical Replay Coverage Next

- **Decision:** reject for the immediate next bounded phase.
- **Reason:** broader symbol coverage remains useful and should still happen before any broad performance claims, but it is not required before writing the first chart-based outcome methodology plan. The next step can define how outcomes will be measured using the completed SPY three-setup replay without implementing backtesting or claiming edge.
- **Boundary:** if selected later, this must remain signal/stage/lifecycle replay only unless separately authorized.

### 2. Start Chart-Based Trade Outcome Backtesting v1 Planning Next

- **Decision:** choose.
- **Reason:** SPY now has real replay coverage across Continuation, Ideal, and Clean Fast Break, which is enough to begin outcome methodology safely as a planning-only phase. The plan can define chart-based outcome rules, qualifying signal criteria, invalidation/target handling, no-hindsight rules, and reporting boundaries before any implementation, option P&L modeling, or account sizing exists.
- **Boundary:** this is planning only. It must not implement a backtester, model option P&L, size an account, generate performance claims, or alter engine behavior.

### 3. Start Continuous Watcher MVP Planning Next

- **Decision:** reject.
- **Reason:** the project handoff requires serious trade outcome backtesting before Continuous Watcher promotion work. Watcher implementation is explicitly not allowed before backtesting planning, and even watcher planning would be premature as the next phase while outcome methodology remains undefined.
- **Boundary:** Continuous Watcher work remains later, after replay, outcome methodology, backtesting evidence, shadow accuracy review, and risk review.

## Decision Rule Result

- **Rule applied:** If SPY three-setup replay is enough to begin outcome methodology safely, choose chart-based trade outcome backtesting v1 planning.
- **Result:** SPY three-setup replay is enough to begin outcome methodology planning safely because it covers all three setup families on one real symbol and has runner output validation.
- **Chosen next phase:** Chart-based trade outcome backtesting v1 planning.

## Rejected Alternatives

- **Next-symbol real historical replay coverage:** rejected as immediate next phase because broader QQQ/IWM/GLD signal coverage is valuable but not a blocker for planning outcome methodology.
- **Continuous Watcher MVP planning:** rejected because watcher work must not precede backtesting planning and evidence.

## Non-Changes

- **`main.py` changed:** no
- **Runner code changed:** no
- **Schemas changed:** no
- **Fixtures changed:** no
- **Reports changed:** no
- **Replay tests changed:** no
- **Backtesting implementation started:** no
- **Option P&L modeled:** no
- **Account sizing added:** no
- **Watcher implementation started:** no

## Next Task

Create a docs-only chart-based trade outcome backtesting v1 planning review. It should define methodology and boundaries only, using SPY three-setup replay as the starting evidence, without implementing backtesting, option P&L, account sizing, watcher behavior, auto-trading, live reads, or live trade decisions.
