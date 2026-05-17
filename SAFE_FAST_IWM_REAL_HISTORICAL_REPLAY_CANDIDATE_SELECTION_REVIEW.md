# SAFE-FAST IWM Real Historical Replay Candidate Selection Review

## Review Status

- Review status: PASS
- Baseline: patch8
- Repo: safe-fast-backendnew
- Branch: main
- Work mode: build work only, no live trade decisions

## Baseline Checked

`SAFE_FAST_BUILD_STATE.md` says:

- IWM-first decision: IWM is the selected next broader coverage target after completed SPY + QQQ current-depth closeout.
- Current objective: create IWM real historical replay candidate selection review.
- Latest committed planning/inventory status: `de6cf3b Add IWM broader coverage planning review` and `8b49ca6 Add IWM fixture replay candidate inventory` are present locally, and the inventory set this candidate selection review as the next task.
- Continuous Watcher deferral: Continuous Watcher remains deferred.
- No-touch boundaries: do not touch Railway, production deploy files, `main.py`, engine logic, replay runner logic, schemas, fixtures, generated reports, option P&L, account sizing, auto-trading, live trade decisions, or Continuous Watcher implementation in this docs/replay-prep task.

## Repo State Checked

- Git status result: `## main...origin/main [ahead 3]`
- Latest commits:
  - `8b49ca6 Add IWM fixture replay candidate inventory`
  - `de6cf3b Add IWM broader coverage planning review`
  - `5c1e564 Add next broader coverage decision review`
  - `3faf90d Repair build-state header after QQQ closeout`
  - `5d33edc Add QQQ chart outcome closeout review`
  - `723a69f Add QQQ post-aggregate chart outcome decision review`
  - `ac1d046 Add QQQ aggregate chart outcome output validation`
  - `872906e Add QQQ chart outcome aggregate summary`
  - `29fc799 Add QQQ Continuation chart outcome output validation`
  - `afb498f Add QQQ Continuation chart outcome calculation`
- `8b49ca6` present: yes.
- Conflicts found: none. Repo/build-state facts agree that patch8 is the frozen baseline, `safe-fast-backendnew` is the active repo, `main` is the branch, IWM is the next broader coverage target, GLD is deferred, and Continuous Watcher remains deferred.

## Purpose

This review selects or defines IWM real historical replay candidates. It does not prove IWM coverage yet. It defines the required candidate slots and evidence needed before later bounded fixture, replay, chart-only outcome, or aggregate closeout work can begin.

## Existing Evidence Reviewed

- `SAFE_FAST_BUILD_STATE.md`: confirms patch8, active repo/branch, IWM-first direction, current objective, Continuous Watcher deferral, and no-touch boundaries.
- `SAFE_FAST_IWM_FIXTURE_REPLAY_CANDIDATE_INVENTORY.md`: states that no concrete IWM historical sample dates or candle windows were found and defines the needed IWM candidate categories.
- `SAFE_FAST_IWM_BROADER_COVERAGE_PLANNING_REVIEW.md`: selects IWM as the next broader coverage target and requires candidate inventory/replay preparation before source-data, fixture, replay, or chart outcome work.
- `SAFE_FAST_NEXT_BROADER_COVERAGE_DECISION_REVIEW.md`: documents the IWM-first decision after SPY + QQQ closeout and defers GLD because no later source-data or window-selection evidence overrides IWM.
- `SAFE_FAST_PROJECT_MASTER_HANDOFF.md`: defines the manual-trading-only target, no auto-trading boundary, protected setup identities, session-boundary behavior, winner-selection behavior, and bar-by-bar replay expectation for SPY / QQQ / IWM / GLD.
- `SAFE_FAST_ON_DEMAND_CLOSEOUT_PLAN.md`: defines the setup recognition, stage correctness, session-boundary, winner-selection, no-trade, blocker, and user-facing behavior that IWM replay candidates must preserve.
- `SAFE_FAST_BACKTESTING_PLAN.md`: includes IWM in the allowed universe and requires no-hindsight historical signal replay before trade outcome backtesting.
- `historical_signal_replay/`: provides the existing signal/stage/lifecycle replay boundary, fixture/report pattern, source-data intake requirements, SPY/QQQ window-selection pattern, and replay output validation pattern.
- SPY historical replay docs: show the accepted SPY pattern for Continuation, Ideal, and Clean Fast Break source windows, fixtures, signal logs, summaries, validation reviews, and three-setup closeout.
- QQQ historical replay docs: show the accepted QQQ pattern for Ideal, Clean Fast Break, and Continuation source windows, fixtures, signal logs, summaries, evidence reviews, and three-setup closeout.
- SPY chart outcome docs: show the chart-only outcome calculation, validation, aggregate summary, and closeout pattern after real replay evidence exists.
- QQQ chart outcome docs: show the per-setup chart-only outcome calculation/output validation, aggregate summary validation, and QQQ chart outcome closeout pattern.
- Aggregate closeout docs: show that aggregate closeout follows per-setup replay and chart-only outcome validation, not candidate selection.
- Output validation docs: require JSON/schema/count/source-row validation and preserve no-option-P&L, no-account-sizing, no-live-decision boundaries.
- Transition readiness docs: confirm protected on-demand behavior is ready with known limits, not proof of IWM historical signal quality, watcher readiness, or production readiness.
- Files containing `IWM`: show allowed-symbol, planning, deferral, and candidate-inventory references, but no concrete IWM source CSV, fixture JSON, replay output, chart outcome result, or historical sample date/window.
- Files containing `GLD`: show allowed-symbol and deferral references, but no stronger GLD source-data, window-selection, replay, chart outcome, or closeout artifact that overrides IWM-first.
- Files containing `Ideal`, `Clean Fast Break`, `Continuation`, `session-boundary`, `winner-selection`, `no-trade`, `stage correctness`, `chart outcome`, and `aggregate closeout`: confirm the required setup families, edge categories, output boundaries, and SPY/QQQ artifact pattern for IWM.

## Concrete IWM Sample Evidence Found

- Concrete IWM sample dates/windows found in repo evidence: no
- No concrete IWM chart windows are currently present in repo evidence.
- This review therefore selects required candidate slots and required evidence, not invented historical dates.

## Candidate Selection Method

IWM candidate selection must cover:

- Ideal recognition
- Clean Fast Break recognition
- Continuation recognition
- developing-stage correctness
- session-boundary carry-forward
- stable winner selection
- no-trade discipline
- chart-only outcome readiness
- aggregate closeout readiness

## Selected IWM Historical Replay Candidate Slots

| Candidate ID | Setup Type | Selection Role | Concrete Sample Status | Required Evidence Before Fixture/Replay Creation | Expected Assertion Focus | Next Asset |
| --- | --- | --- | --- | --- | --- | --- |
| IWM-HIST-IDEAL-001 | Ideal | first IWM Ideal real historical replay candidate | NEEDS_CONCRETE_SAMPLE | specific IWM historical date/window, 1H RTH source rows, expected Ideal identity/stage/verdict/blocker/caution notes, no-hindsight row review | Ideal identity survives blockers/chop/context without false Clean Fast Break or Continuation relabel | IWM Ideal real historical replay review asset |
| IWM-HIST-CLEAN-FAST-BREAK-001 | Clean Fast Break | first IWM Clean Fast Break real historical replay candidate | NEEDS_CONCRETE_SAMPLE | specific IWM historical date/window, 1H RTH source rows, expected Clean Fast Break identity/stage/verdict/blocker/caution notes, no-hindsight row review | Clean Fast Break identity survives blockers/chop/context without false Continuation relabel | IWM Clean Fast Break real historical replay review asset |
| IWM-HIST-CONTINUATION-001 | Continuation | first IWM Continuation real historical replay candidate | NEEDS_CONCRETE_SAMPLE | specific IWM historical date/window, 1H RTH source rows, expected Continuation shelf/base identity, developing/pending/completed trigger notes, no-hindsight row review | shelf/base recognition, developing lifecycle, pending/completed trigger discipline | IWM Continuation real historical replay review asset |
| IWM-HIST-STAGE-DEVELOPING-001 | mixed/all | IWM developing-stage correctness candidate | NEEDS_CONCRETE_SAMPLE | IWM rows where setup is watchable but not trade-ready, with expected stage, verdict, blocker/caution, and user-facing reason notes | developing setup does not prematurely become trade-ready and surfaces correct stage reason | IWM stage/session/winner/no-trade edge review |
| IWM-HIST-SESSION-BOUNDARY-001 | Continuation-focused | IWM prior-session carry-forward candidate | NEEDS_CONCRETE_SAMPLE | IWM rows spanning prior/current session context, session-date evidence, prior break context, and fresh/current-session trigger decision notes | prior-session break remains spent/context unless fresh current-session break occurs | IWM stage/session/winner/no-trade edge review |
| IWM-HIST-WINNER-SELECTION-001 | mixed/all | IWM mixed setup winner-selection candidate | NEEDS_CONCRETE_SAMPLE | IWM rows with competing Ideal / Clean Fast Break / Continuation candidates and expected deterministic winner rationale | deterministic winner selection across Ideal / Clean Fast Break / Continuation without stale/spent setup winning incorrectly | IWM stage/session/winner/no-trade edge review |
| IWM-HIST-NO-TRADE-DISCIPLINE-001 | mixed/all | IWM no-trade discipline candidate | NEEDS_CONCRETE_SAMPLE | IWM rows with blockers/cautions, expected preserved setup identity, expected NO_TRADE or PENDING verdict, and trigger/no-trigger notes | blockers/cautions preserve setup identity and prevent live trade approval when required | IWM stage/session/winner/no-trade edge review |
| IWM-HIST-CHART-OUTCOME-IDEAL-001 | Ideal | IWM Ideal chart-only outcome candidate | NEEDS_CONCRETE_SAMPLE | accepted IWM Ideal replay signal-stage row, copied invalidation/trigger context, future source rows for chart-only measurement, and chart-only outcome notes | chart-only outcome review readiness, not option P&L | IWM Ideal chart-only outcome review |
| IWM-HIST-CHART-OUTCOME-CLEAN-FAST-BREAK-001 | Clean Fast Break | IWM Clean Fast Break chart-only outcome candidate | NEEDS_CONCRETE_SAMPLE | accepted IWM Clean Fast Break replay signal-stage row, copied invalidation/trigger context, future source rows for chart-only measurement, and chart-only outcome notes | chart-only outcome review readiness, not option P&L | IWM Clean Fast Break chart-only outcome review |
| IWM-HIST-CHART-OUTCOME-CONTINUATION-001 | Continuation | IWM Continuation chart-only outcome candidate | NEEDS_CONCRETE_SAMPLE | accepted IWM Continuation replay signal-stage row, copied invalidation/trigger context, future source rows for chart-only measurement, and chart-only outcome notes | chart-only outcome review readiness, not option P&L | IWM Continuation chart-only outcome review |
| IWM-HIST-AGGREGATE-CLOSEOUT-001 | all | IWM aggregate closeout candidate | NEEDS_CONCRETE_SAMPLE | completed per-setup IWM replay/review evidence and completed per-setup chart-only outcome reviews with validation results | only after per-setup IWM replay/review and chart-only outcome reviews are complete | IWM aggregate closeout review |

## Required Inputs Before Fixture Creation

- specific historical date/window
- symbol/timeframe context
- setup type label
- expected setup identity
- expected stage
- expected verdict
- expected blockers/cautions
- expected no-trade/trigger behavior
- session-date context for carry-forward cases
- chart-only outcome notes where relevant

## Go / No-Go For Actual IWM Fixture Creation

Actual IWM fixture creation cannot begin now.

- Fixture creation status: NO-GO
- Reason: concrete IWM samples are not present in repo evidence. Fixture creation remains blocked until sample collection is complete and reviewed.

## Recommended Asset Creation Order

1. IWM historical sample collection worksheet if concrete samples are missing
2. IWM Ideal real historical replay review asset
3. IWM Clean Fast Break real historical replay review asset
4. IWM Continuation real historical replay review asset
5. IWM stage/session/winner/no-trade edge review
6. IWM chart-only outcome reviews by setup type
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
- IWM fixture execution
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

Create IWM historical sample collection worksheet.
