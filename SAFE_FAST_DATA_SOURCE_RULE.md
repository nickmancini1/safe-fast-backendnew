# SAFE-FAST Data Source Rule

Purpose:
This file prevents future chats from guessing where data comes from or mixing vendor evidence with SAFE-FAST decisions.

Core rule:
Vendors provide raw evidence.
SAFE-FAST translates that evidence into setup labels, entry/exit decisions, P&L, exact rejections, and eligibility.

Data-source ownership:

Databento:
Databento supplies raw historical replay evidence.
Databento is the source for paid historical raw market evidence used in replay and backtesting.
Use it for approved raw option evidence such as quotes, trades, statistics, and other approved schemas.
A Databento request must be exact before it runs: contract, dataset, schemas, time windows, destination, cost state, approval state, and forbidden schemas.
No broad Databento download unless the sealed task explicitly approves it.
No paid Databento request unless cost and scope are approved first.

Tastytrade:
Tastytrade is part of the trading and candidate workflow where the repo or task says Tastytrade is the source.
Tastytrade/dxLink is candidate/trading workflow source only where the repo/task says so.
Do not silently replace Databento replay evidence with Tastytrade data.
Do not treat Tastytrade observations as SAFE-FAST proof until they are translated into exact SAFE-FAST setup rules and replayed where required.

Official agencies / ALFRED:
Official agencies / ALFRED supply macro and event facts.
Macro and event facts do not decide SAFE-FAST labels, entry, exit, P&L, profitability, paper eligibility, or live eligibility.

Schwab:
Schwab is future or potential broker/API work only.
Schwab is not active unless Nick explicitly approves it and the current task says Schwab is in scope.
No OAuth, token writes, account calls, broker mutation, orders, fills, live backend, or live trading unless explicitly approved.

SAFE-FAST:
SAFE-FAST owns setup labels and trade decisions.
SAFE-FAST owns labels, entry, exit, P&L, profitability, paper eligibility, and live eligibility.
SAFE-FAST must translate broad market data into exact setup definitions before a candidate can move to replay.
Vendors do not decide Ideal, Clean Fast Break, Continuation, entry, exit, P&L, profitability, paper eligibility, or live eligibility.
If SAFE-FAST is unprofitable, weak, missing evidence, or inconclusive, diagnose the exact cause and smallest evidence-backed fix.

Candidate data rule:
A candidate is not replay-ready just because it looks interesting.
Before replay, the task must state the candidate date, ticker, setup type, exact SAFE-FAST rule reason, contract or contract-selection rule, raw-data source, schemas, windows, cost/approval state, destination, expected replay output, and exact kill condition.

Market-context rule:
Broad market context can help propose a candidate, but it is not proof.
Useful context may include trend, volatility, volume, time of day, sector movement, news risk, liquidity, and indicator behavior.
That context must be translated into SAFE-FAST definitions before raw-data spend or replay.

Current Day 55 rule:
Current active Databento work is target-only SPY 670C evidence for `SPY   260330C00670000`, using:
`historical_signal_replay/results/day55_spy_670c_target_cost_only_request.json`.

Current Day 55 forbidden work:
No broad download.
No Schwab.
No Railway.
No live backend.
No live trading.
No profitability claim.
No paper/live eligibility claim.

Stop rule:
If a future chat cannot say which source owns the data, what SAFE-FAST must translate, and what exact proof will come back, it must not give a command.
