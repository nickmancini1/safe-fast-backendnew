# SAFE-FAST IWM Fixture / Replay Candidate Inventory

## Inventory Status

- Inventory status: PASS
- Baseline: patch8
- Repo: safe-fast-backendnew
- Branch: main
- Work mode: build work only, no live trade decisions

## Baseline Checked

`SAFE_FAST_BUILD_STATE.md` says:

- IWM-first decision: the next broader coverage decision review selected IWM first after SPY + QQQ closeout.
- Current objective: after this inventory update, create IWM real historical replay candidate selection review; before this task, the IWM planning review status set the next objective as creating this fixture/replay candidate inventory.
- Continuous Watcher deferral: Continuous Watcher remains deferred.
- No-touch boundaries: do not touch Railway, production deploy files, `main.py`, engine logic, replay runner logic, schemas, fixtures, generated reports, option P&L, account sizing, auto-trading, live trade decisions, or Continuous Watcher implementation in this docs/replay-prep task.

## Repo State Checked

- Git status result: `## main...origin/main [ahead 2]`
- Latest commits:
  - `de6cf3b Add IWM broader coverage planning review`
  - `5c1e564 Add next broader coverage decision review`
  - `3faf90d Repair build-state header after QQQ closeout`
  - `5d33edc Add QQQ chart outcome closeout review`
  - `723a69f Add QQQ post-aggregate chart outcome decision review`
  - `ac1d046 Add QQQ aggregate chart outcome output validation`
  - `872906e Add QQQ chart outcome aggregate summary`
  - `29fc799 Add QQQ Continuation chart outcome output validation`
- `de6cf3b` present: yes.
- Conflicts found: none. Working tree was clean before this task, and repo/build-state evidence agrees that patch8 is the frozen baseline, `safe-fast-backendnew` is the active repo, `main` is the branch, IWM is the selected next broader coverage target, GLD is deferred, and Continuous Watcher remains deferred. The stale top-level latest-completed-commit field was not updated with a guessed hash.

## Purpose

This inventory prepares IWM broader coverage. It does not prove IWM historical replay coverage, IWM chart-only outcome behavior, IWM aggregate closeout, profitability, live readiness, option performance, account sizing, watcher readiness, or production readiness.

The inventory defines what replay and review candidates must be selected before any actual IWM fixture JSON, replay output, chart outcome fixture, generated report, runner change, schema change, or engine change is authorized by a later bounded task.

## Existing Evidence Reviewed

- `SAFE_FAST_BUILD_STATE.md`: confirms patch8, active repo/branch, IWM-first direction, current IWM planning status, Continuous Watcher deferral, and no-touch boundaries.
- `SAFE_FAST_IWM_BROADER_COVERAGE_PLANNING_REVIEW.md`: selects IWM as the next broader coverage target and requires an IWM fixture/replay candidate inventory before source-data, fixture, replay, or chart outcome work.
- `SAFE_FAST_NEXT_BROADER_COVERAGE_DECISION_REVIEW.md`: documents the IWM-first decision after SPY + QQQ closeout and defers GLD absent stronger evidence.
- `SAFE_FAST_PROJECT_MASTER_HANDOFF.md`: records the manual-trading-only final target, no auto-trading boundary, and broader viability sequence, including historical replay and trade outcome review before proof-mode readiness.
- `SAFE_FAST_ON_DEMAND_CLOSEOUT_PLAN.md`: defines protected setup recognition, stage correctness, session-boundary, blocker, and user-facing gates that IWM candidate selection must preserve.
- `SAFE_FAST_BACKTESTING_PLAN.md`: requires no-hindsight historical signal replay before trade outcome backtesting and includes SPY, QQQ, IWM, and GLD in the test universe.
- `historical_signal_replay/README.md`: defines the signal/stage/lifecycle replay boundary and existing fixture/output concepts.
- `historical_signal_replay/REAL_HISTORICAL_REPLAY_V1_SPY_THREE_SETUP_CLOSEOUT_REVIEW.md`: provides the SPY pattern for source validation, setup-family window selection, fixture/output validation, and three-setup closeout.
- `historical_signal_replay/QQQ_THREE_SETUP_REAL_HISTORICAL_REPLAY_CLOSEOUT_REVIEW.md`: provides the QQQ pattern for Ideal, Clean Fast Break, and Continuation replay coverage and closeout.
- `historical_signal_replay/REAL_HISTORICAL_REPLAY_V1_DATA_EXPANSION_PLAN.md`: defines allowed symbols, allowed setup families, no-hindsight rules, lifecycle requirements, and minimum coverage matrix for IWM/GLD expansion.
- `historical_signal_replay/SOURCE_HISTORICAL_DATA_INTAKE_SPEC.md`: defines required source-data fields and the rule against fabricated timestamps, OHLCV, setup labels, blocker labels, or outcomes.
- `SAFE_FAST_BROADER_CHART_OUTCOME_BACKTESTING_COVERAGE_PLAN.md`: establishes the broader coverage order QQQ, then IWM, then GLD, and requires real historical replay before chart outcome calculation.
- `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_CLOSEOUT_REVIEW.md`: confirms chart-only outcome boundaries and notes IWM and GLD still lack equivalent chart outcome closeout evidence.
- `SAFE_FAST_QQQ_CHART_OUTCOME_CLOSEOUT_REVIEW.md`: provides the next-symbol closeout pattern for per-setup chart-only outcomes plus aggregate summary.
- `SAFE_FAST_QQQ_CHART_OUTCOME_AGGREGATE_SUMMARY_OUTPUT_VALIDATION_REVIEW.md`: provides the aggregate output validation pattern.
- `SAFE_FAST_ON_DEMAND_TRANSITION_READINESS_REVIEW.md`: confirms protected on-demand behavior is ready with known limits, not proof of historical signal quality, watcher readiness, or live viability.
- Repository search for `IWM`: found allowed-symbol and planning references, plus on-demand contract symbol-order references, but no concrete IWM source CSV, IWM fixture JSON, IWM replay output, IWM chart outcome result, or IWM historical sample dates.
- Repository search for `GLD`: found allowed-symbol and deferral references, but no stronger GLD source-data, window-selection, fixture, replay, chart outcome, or closeout artifact that overrides IWM-first.
- Repository search for `fixture`, `replay candidate`, `chart outcome`, `closeout`, `aggregate`, `Ideal`, `Clean Fast Break`, and `Continuation`: confirms the SPY/QQQ artifact pattern and candidate categories needed for IWM.

## IWM Candidate Inventory Summary

No concrete IWM historical sample dates or IWM candle windows were found in repo evidence. The candidates below are required candidate categories, not selected dates or completed fixtures.

| Candidate ID | Setup Type | Purpose | Required Evidence | Expected Replay/Review Asset | Status |
| --- | --- | --- | --- | --- | --- |
| IWM-Ideal-Recognition | Ideal | Verify Ideal recognition on IWM without relabeling under blockers/chop/context | Real IWM 1H RTH candidate window, no-hindsight row review, expected Ideal identity/stage/blocker behavior | IWM Ideal candidate selection review, then fixture design/replay review if authorized | Needed; no concrete IWM sample in repo |
| IWM-Clean-Fast-Break-Recognition | Clean Fast Break | Verify Clean Fast Break recognition and no false Continuation relabel | Real IWM 1H RTH candidate window showing tight pause/fast-break structure and expected non-Continuation identity | IWM Clean Fast Break candidate selection review, then fixture design/replay review if authorized | Needed; no concrete IWM sample in repo |
| IWM-Continuation-Recognition | Continuation | Verify shelf/base recognition and developing Continuation lifecycle | Real IWM 1H RTH shelf/base candidate window with developing, pending/triggered, and spent/no-fresh-trigger review points where available | IWM Continuation candidate selection review, then fixture design/replay review if authorized | Needed; no concrete IWM sample in repo |
| IWM-Stage-Developing | mixed/all | Verify developing setup stage messaging and no premature trade-ready state | IWM rows where setup is watchable but not trigger-ready, with expected stage/verdict/blocker/caution notes | IWM stage edge review tied to selected candidate windows | Needed; no concrete IWM sample in repo |
| IWM-Session-Boundary | Continuation-focused | Verify prior-session carry-forward does not become a fresh current-session trigger | IWM rows spanning prior/current session context, with session date, prior break context, and fresh-trigger decision evidence | IWM session-boundary candidate review | Needed; no concrete IWM sample in repo |
| IWM-Winner-Selection | mixed/all | Verify stable winner selection across Ideal / Clean Fast Break / Continuation | IWM or mixed visible setup candidates where selection must remain deterministic and not prefer stale/spent context over fresh valid context | IWM winner-selection edge review | Needed; no concrete IWM sample in repo |
| IWM-No-Trade-Discipline | mixed/all | Verify blockers/cautions preserve no-trade discipline and setup identity | IWM rows with expected blockers/cautions, final verdict NO_TRADE or PENDING where appropriate, and identity preserved | IWM no-trade discipline review | Needed; no concrete IWM sample in repo |
| IWM-Chart-Only-Outcome-Ideal | Ideal | Chart-only outcome review candidate | Accepted IWM Ideal replay signal-stage row, copied invalidation/trigger context, and future chart rows for chart-only measurement | IWM Ideal chart outcome calculation/output validation review after replay passes | Blocked until IWM Ideal replay candidate is accepted |
| IWM-Chart-Only-Outcome-Clean-Fast-Break | Clean Fast Break | Chart-only outcome review candidate | Accepted IWM Clean Fast Break replay signal-stage row, copied invalidation/trigger context, and future chart rows for chart-only measurement | IWM Clean Fast Break chart outcome calculation/output validation review after replay passes | Blocked until IWM Clean Fast Break replay candidate is accepted |
| IWM-Chart-Only-Outcome-Continuation | Continuation | Chart-only outcome review candidate | Accepted IWM Continuation replay signal-stage row, copied invalidation/trigger context, and future chart rows for chart-only measurement | IWM Continuation chart outcome calculation/output validation review after replay passes | Blocked until IWM Continuation replay candidate is accepted |
| IWM-Aggregate-Closeout | all | Aggregate closeout after per-setup reviews are complete | Validated IWM Ideal, Clean Fast Break, and Continuation replay/outcome evidence with source files and validation reviews | IWM aggregate summary/output validation and IWM closeout review | Blocked until per-setup replay and chart-only outcome reviews are complete |

## Required Concrete Inputs Before Fixture Creation

- Candidate chart windows or historical sample references.
- Setup type label for each candidate.
- Expected stage/verdict/blocker/caution behavior.
- Expected no-trade/trigger behavior.
- Session date context where relevant.
- Chart-only outcome review notes where relevant.

## Proposed IWM Asset Creation Order

1. IWM real historical replay candidate selection
2. IWM Ideal replay/review asset
3. IWM Clean Fast Break replay/review asset
4. IWM Continuation replay/review asset
5. IWM stage/session/winner/no-trade edge review
6. IWM chart-only outcome per setup type
7. IWM aggregate closeout review

## Explicit Non-Goals

- no engine patching
- no live trading
- no Railway
- no production
- no Continuous Watcher implementation
- no option P&L
- no account sizing
- no auto-trading
- no fixture JSON created in this task
- no generated reports changed in this task

## What Remains Unproven

- IWM historical replay coverage
- IWM chart-only outcome coverage
- IWM aggregate closeout
- GLD broader coverage
- broader samples beyond SPY/QQQ/IWM
- Continuous Watcher behavior
- real duplicate suppression
- shadow/live validation
- option P&L
- account sizing
- production readiness

## Recommended Next Task

Create IWM real historical replay candidate selection review.
