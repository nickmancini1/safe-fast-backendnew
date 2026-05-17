# SAFE-FAST Next Broader Coverage Decision Review

## Review Status

- Review status: PASS
- Baseline: patch8
- Repo: safe-fast-backendnew
- Branch: main
- Work mode: build work only, no live trade decisions

## Baseline Checked

`SAFE_FAST_BUILD_STATE.md` says:

- Latest completed milestone: QQQ chart outcome closeout review
- Current objective: decide next broader coverage phase after SPY + QQQ current-depth closeout, IWM vs GLD
- Continuous Watcher status: deferred
- Do-not-touch boundaries: do not touch Railway, production deploy files, old repo, auto-trading, or live-read/live-decision behavior; build work only and no live trade decisions.

## Repo State Checked

- Git status result: `## main...origin/main`
- Latest 5 commits:
  - `3faf90d Repair build-state header after QQQ closeout`
  - `5d33edc Add QQQ chart outcome closeout review`
  - `723a69f Add QQQ post-aggregate chart outcome decision review`
  - `ac1d046 Add QQQ aggregate chart outcome output validation`
  - `872906e Add QQQ chart outcome aggregate summary`
- Header repair commit present: yes, `3faf90d Repair build-state header after QQQ closeout`
- Blocker status: not a blocker. The header repair commit is docs-only state alignment after the completed QQQ closeout milestone; repo HEAD remains the source of truth and does not conflict with the completed milestone commit `5d33edc`.

## Fixed / Completed

- SPY: real historical replay closeout is complete across Continuation, Ideal, and Clean Fast Break; chart-only outcome v1 closeout is complete with three SPY setup-family samples and an aggregate summary.
- QQQ: real historical replay closeout is complete across Ideal, Clean Fast Break, and Continuation; chart-only outcome closeout is complete with three QQQ setup-family samples and an aggregate summary.
- Ideal: protected in on-demand recognition/stage contracts and covered in SPY and QQQ real replay plus chart-only outcome evidence.
- Clean Fast Break: protected in on-demand recognition/stage contracts and covered in SPY and QQQ real replay plus chart-only outcome evidence.
- Continuation: protected across stage, session-boundary, lifecycle, and duplicate-suppression fixture shapes; covered in SPY and QQQ real replay plus chart-only outcome evidence.
- Historical replay closeout: Historical Signal Replay v1 foundation is closed out; SPY and QQQ each have three-setup real historical replay closeouts.
- Chart-only outcome closeout: SPY chart-based trade outcome v1 is closed out; QQQ chart outcome phase is closed out.

## Still Unproven

- IWM broader coverage
- GLD broader coverage
- broader sample coverage beyond SPY/QQQ
- Continuous Watcher behavior
- duplicate alert suppression in real watcher operation
- shadow/live validation
- option P&L
- account sizing
- production readiness

## Decision

IWM first

## Evidence Supporting Decision

Repo evidence supports IWM first because the broader chart outcome coverage plan established the order as QQQ, then IWM, then GLD. QQQ is now complete at the current-depth replay and chart-only outcome closeout level, so the next item in that reviewed order is IWM.

The same plan says the order should stand unless later source-data validation or window-selection evidence shows that a symbol lacks enough valid no-hindsight setup windows. No IWM or GLD source-data, fixture, historical replay, or chart outcome artifacts exist in the repo yet, so there is no later repo evidence that overrides the planned order.

IWM also preserves the closest expansion path from the existing SPY and QQQ evidence because it remains an equity-index coverage target. The repo already completed SPY and QQQ as equity-index surfaces before GLD, and the exporter support lists both IWM and GLD as allowed symbols without giving GLD any stronger prepared artifact.

## Why Other Target Is Deferred

GLD is deferred because the reviewed broader coverage plan placed GLD after IWM, and no later repo evidence shows GLD has better source-data readiness, window selection, replay fixtures, chart outcomes, or validation artifacts. Starting GLD first would skip the documented IWM step without evidence.

## Boundary Check

- main.py changed: no
- engine logic changed: no
- replay runner changed: no
- schemas changed: no
- fixtures changed: no
- reports changed: no
- Railway touched: no
- production touched: no
- Continuous Watcher implementation started: no
- option P&L modeled: no
- account sizing added: no
- auto-trading added: no
- live trade decisions added: no

## Required Validation Before Future Expansion

Before future engine or replay expansion, validate source data and no-hindsight replay preparation for the selected target first. For IWM, the next expansion must begin with bounded planning and/or source-data validation, then reviewed window selection and replay fixture preparation before any chart outcome calculation. Any future engine or replay-runner behavior change requires replay/regression cases first and must stay outside `main.py`, schema, fixture, report, Railway, production, watcher, option P&L, account-sizing, and auto-trading changes unless a later bounded task explicitly authorizes them.

## Recommended Next Task

Begin IWM broader coverage planning/replay preparation as a docs-only or explicitly bounded source-data validation task. Do not change engine logic, start watcher implementation, model option P&L, add account sizing, or make live trade decisions.
