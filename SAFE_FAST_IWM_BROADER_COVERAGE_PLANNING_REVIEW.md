# SAFE-FAST IWM Broader Coverage Planning Review

## Review Status

- Review status: PASS
- Baseline: patch8
- Repo: safe-fast-backendnew
- Branch: main
- Work mode: build work only, no live trade decisions

## Baseline Checked

`SAFE_FAST_BUILD_STATE.md` says:

- Completed SPY/QQQ closeout: SPY and QQQ current-depth work is complete. SPY has three-setup real historical replay closeout and chart-only outcome closeout. QQQ has three-setup real historical replay closeout and QQQ chart outcome closeout.
- IWM-first decision: the next broader coverage decision review selected IWM first after SPY + QQQ closeout.
- Continuous Watcher deferral: Continuous Watcher remains deferred.
- Do-not-touch boundaries: do not touch Railway, production deploy files, `main.py`, engine logic, replay runner logic, schemas, fixtures, generated reports, option P&L, account sizing, auto-trading, live trade decisions, or Continuous Watcher implementation in this docs-only task.

## Repo State Checked

- Git status result after Phase 1: `## main...origin/main [ahead 1]`
- Latest commits:
  - `5c1e564 Add next broader coverage decision review`
  - `3faf90d Repair build-state header after QQQ closeout`
  - `5d33edc Add QQQ chart outcome closeout review`
  - `723a69f Add QQQ post-aggregate chart outcome decision review`
  - `ac1d046 Add QQQ aggregate chart outcome output validation`
  - `872906e Add QQQ chart outcome aggregate summary`
  - `29fc799 Add QQQ Continuation chart outcome output validation`
  - `afb498f Add QQQ Continuation chart outcome calculation`
- Prior decision review committed: yes, `5c1e564 Add next broader coverage decision review`
- Conflicts: none. The working tree was clean after Phase 1, and the local ahead state is the expected prior docs-only decision commit.

## Why IWM Is The Next Target

IWM is next because the reviewed broader coverage plan established the symbol order as QQQ, then IWM, then GLD. SPY and QQQ now both have current-depth closeout evidence, and the prior decision review selected IWM first because no later repo evidence overrides that order.

Repo evidence supports following the SPY/QQQ pattern before GLD. SPY and QQQ have accepted real historical source data, setup-family replay windows, fixture/replay output validation, chart-only outcome reviews, aggregate summaries, and closeouts. IWM has no equivalent source-data, fixture, replay, chart outcome, or aggregate closeout artifacts yet, and GLD has no stronger prepared artifact. The exporter allows both IWM and GLD, but the documented order defers GLD until after IWM unless IWM source/window evidence later fails.

## Scope For IWM Broader Coverage

The IWM phase is planning/replay preparation only. It should prepare IWM coverage across:

- Ideal
- Clean Fast Break
- Continuation
- stage correctness
- session-boundary carry-forward
- winner-selection stability
- no-trade discipline

This phase should identify the replay-preparation path and candidate inventory needed before any fixture creation, source-data pull, chart outcome calculation, engine change, schema change, or report generation is authorized by a later bounded task.

## Required IWM Replay/Review Assets

The next IWM work should follow the SPY/QQQ artifact pattern where applicable:

- IWM fixture/replay candidate inventory
- IWM real historical replay planning
- IWM source-data validation review for a real 1H RTH source CSV
- IWM setup-type coverage plan across Ideal / Clean Fast Break / Continuation
- IWM no-hindsight window-selection reviews for candidate setup-family windows
- IWM fixture design reviews for selected setup-family windows
- IWM fixture creation reviews after fixture creation is explicitly authorized
- IWM runner output validation reviews for replay outputs
- IWM three-setup real historical replay closeout review
- IWM chart-only outcome review plan
- IWM chart-only outcome calculation/output validation reviews after replay closeout and later explicit authorization
- IWM aggregate summary and aggregate output validation plan
- IWM aggregate closeout review plan
- IWM output validation plan covering JSON validity, expected counts, setup-family coverage, no-hindsight boundaries, and non-goal boundaries

## Explicit Non-Goals

- no engine patching
- no live trading
- no Railway
- no production
- no Continuous Watcher implementation
- no option P&L
- no account sizing
- no auto-trading

## What Remains Unproven

- IWM historical replay coverage
- IWM chart-only outcome coverage
- IWM aggregate closeout
- GLD broader coverage
- broader sample coverage beyond SPY/QQQ/IWM
- Continuous Watcher behavior
- real duplicate suppression
- shadow/live validation
- option P&L
- account sizing
- production readiness

## Recommended Next Task

Create IWM broader coverage fixture/replay candidate inventory.
