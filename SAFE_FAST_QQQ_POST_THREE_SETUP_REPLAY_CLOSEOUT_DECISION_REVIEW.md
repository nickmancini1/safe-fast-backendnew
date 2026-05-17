# SAFE-FAST QQQ Post-Three-Setup Replay Closeout Decision Review

## Decision Status

- **Decision status:** PASS
- **Baseline:** patch8
- **Latest local commit reviewed:** `9e3562f Add QQQ three-setup real historical replay closeout`
- **Scope:** docs-only decision review after QQQ three-setup real historical replay closeout.

This review does not start chart outcome calculations, create chart outcome fixtures, change `main.py`, change schemas, change runner code, change chart outcome code, model option P&L, add account sizing, start watcher implementation, auto-trade, use live reads, or make live trade decisions.

## Inspected Evidence

- `SAFE_FAST_BUILD_STATE.md`
- `historical_signal_replay/QQQ_THREE_SETUP_REAL_HISTORICAL_REPLAY_CLOSEOUT_REVIEW.md`
- `historical_signal_replay/QQQ_IDEAL_REPLAY_EVIDENCE_AND_NEXT_STEP_REVIEW.md`
- `historical_signal_replay/QQQ_CLEAN_FAST_BREAK_REPLAY_EVIDENCE_AND_NEXT_STEP_REVIEW.md`
- `historical_signal_replay/QQQ_CONTINUATION_REPLAY_EVIDENCE_AND_NEXT_STEP_REVIEW.md`
- `SAFE_FAST_BROADER_CHART_OUTCOME_BACKTESTING_COVERAGE_PLAN.md`
- `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_CLOSEOUT_REVIEW.md`
- `chart_trade_outcome_backtesting/reports/spy_three_setup_chart_outcome_summary_v1.json`

## Current QQQ Replay Closeout Position

- **QQQ three-setup closeout status:** PASS
- **Setup families closed out:** Ideal, Clean Fast Break, Continuation
- **QQQ Ideal replay evidence:** PASS; 6 signal log rows and 6 summary rows.
- **QQQ Clean Fast Break replay evidence:** PASS; 6 signal log rows and 6 summary rows.
- **QQQ Continuation replay evidence:** PASS; 6 signal log rows and 6 summary rows.
- **QQQ total signal/stage/lifecycle rows across three setup families:** 18
- **No-hindsight boundary:** PASS; QQQ replay evidence remains tied to reviewed QQQ source rows and signal/stage/lifecycle assertions only.
- **Chart outcome calculation started before this review:** no

## SPY Precedent

- **SPY chart outcome closeout status:** PASS
- **SPY setup families with chart outcomes:** Continuation, Ideal, Clean Fast Break
- **SPY validated chart outcome samples:** 3
- **SPY aggregate result:** 2 follow-through, 0 invalidated/failure, 1 time stop.
- **SPY boundary:** chart-only proof, not option P&L, not account sizing, not watcher readiness, and not profitability proof.

SPY established the current project pattern: complete three setup-family replay evidence first, then proceed into chart-only outcome calculation. QQQ now has the same three-setup replay closeout condition met at the signal/stage/lifecycle layer.

## Options Compared

### 1. Start QQQ Chart Outcome Calculation Phase

- **Decision:** choose next.
- **Reason:** QQQ now has completed real historical replay closeout for Ideal, Clean Fast Break, and Continuation. SPY already completed the same pattern before chart outcome calculations, and the broader chart outcome coverage plan identifies QQQ as the minimum next-symbol target before IWM or GLD.
- **Boundary:** this review chooses the next phase only; it does not start calculation or create fixtures.

### 2. Broaden Replay Coverage To IWM Before QQQ Chart Outcomes

- **Decision:** reject for now.
- **Reason:** IWM remains part of broader coverage, but QQQ is already closed out at the three-setup replay layer and is the documented minimum next-symbol target. Starting IWM replay first would defer the ready QQQ chart outcome phase without evidence that QQQ should be skipped.

### 3. Broaden Replay Coverage To GLD Before QQQ Chart Outcomes

- **Decision:** reject for now.
- **Reason:** GLD remains part of broader coverage after QQQ and IWM, but QQQ is already ready for the next bounded chart outcome planning phase. No inspected evidence supports moving GLD ahead of QQQ.

### 4. Move To Watcher Planning

- **Decision:** reject.
- **Reason:** watcher planning remains premature. The broader chart outcome coverage plan defers watcher planning until broader symbol chart outcome evidence is completed and reviewed. This task does not authorize watcher implementation, live reads, alert delivery, option P&L, account sizing, auto-trading, or production deployment.

## Decision

- **Chosen next phase:** plan QQQ chart outcome calculation phase for Ideal, Clean Fast Break, and Continuation.
- **Decision rule applied:** choose QQQ chart outcome calculation phase next because QQQ now has three-setup real historical replay closeout, and SPY already completed the same pattern before chart outcome calculations.
- **Decision status:** PASS

## Rejected Alternatives

- **Broaden replay coverage to IWM before QQQ chart outcomes:** rejected for now because QQQ is already the documented next-symbol target and has completed three-setup replay closeout.
- **Broaden replay coverage to GLD before QQQ chart outcomes:** rejected for now because GLD is later in the documented broader coverage order and QQQ is ready.
- **Move to watcher planning:** rejected because watcher planning remains deferred until broader chart outcome evidence is completed and reviewed.
- **Option/risk or account sizing:** rejected because this phase remains chart-only and does not model option P&L, full financial risk, or account sizing.

## Boundary Confirmation

- **Chart outcome calculation started:** no
- **Chart outcome fixtures created:** no
- **Option P&L modeled:** no
- **Account sizing added:** no
- **Watcher implementation started:** no
- **`main.py` changed:** no
- **Schemas changed:** no
- **Runner code changed:** no
- **Chart outcome code changed:** no

## Recommended Next Task

Plan QQQ chart outcome calculation phase for Ideal, Clean Fast Break, and Continuation, preserving the chart-only boundary and without modeling option P&L, adding account sizing, starting watcher implementation, changing `main.py`, changing schemas, changing runner code, or changing chart outcome code unless a later bounded task explicitly authorizes that work.
