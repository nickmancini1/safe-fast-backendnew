# SAFE-FAST IWM Historical Sample Collection Worksheet

## Worksheet Status

- Worksheet status: PASS
- Baseline: patch8
- Repo: safe-fast-backendnew
- Branch: main
- Work mode: build work only, no live trade decisions

## Baseline Checked

`SAFE_FAST_BUILD_STATE.md` says:

- IWM-first decision: IWM is the selected next broader coverage target after completed SPY + QQQ current-depth closeout.
- Current objective: create IWM historical sample collection worksheet.
- Latest IWM candidate selection status: `SAFE_FAST_IWM_REAL_HISTORICAL_REPLAY_CANDIDATE_SELECTION_REVIEW.md` passed and selected required IWM candidate slots, but did not find concrete IWM sample evidence.
- Concrete sample status: concrete IWM sample evidence found: no; fixture creation status remains NO-GO because no concrete IWM historical sample windows are present in repo evidence.
- Continuous Watcher deferral: Continuous Watcher remains deferred.
- No-touch boundaries: do not touch Railway, production deploy files, `main.py`, engine logic, replay runner logic, schemas, fixtures, generated reports, option P&L, account sizing, auto-trading, live trade decisions, or Continuous Watcher implementation in this docs/replay-prep task.

## Repo State Checked

- Git status result: `## main...origin/main [ahead 4]`
- Latest commits:
  - `1ff5daf Add IWM historical replay candidate selection review`
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
  - `fc21fd3 Add QQQ Clean Fast Break chart outcome output validation`
- `1ff5daf` present: yes.
- Conflicts found: none. Repo/build-state facts agree that patch8 is the frozen baseline, `safe-fast-backendnew` is the active repo, `main` is the branch, IWM is the next broader coverage target, concrete IWM sample evidence is not yet present, GLD is deferred, and Continuous Watcher remains deferred.

## Purpose

This worksheet exists to collect concrete IWM historical sample windows before fixture/replay creation can begin. It is a collection aid only. It does not create IWM fixture JSON, modify replay logic, produce generated reports, calculate chart outcomes, or make live-trade conclusions.

## Existing Evidence Reviewed

- `SAFE_FAST_BUILD_STATE.md`: confirms patch8, active repo/branch, IWM-first direction, current worksheet objective, concrete sample NO-GO status, Continuous Watcher deferral, and no-touch boundaries.
- `SAFE_FAST_IWM_REAL_HISTORICAL_REPLAY_CANDIDATE_SELECTION_REVIEW.md`: confirms required IWM candidate slots and states no concrete IWM historical sample dates/windows were found in repo evidence.
- `SAFE_FAST_IWM_FIXTURE_REPLAY_CANDIDATE_INVENTORY.md`: defines the IWM inventory scope across Ideal, Clean Fast Break, Continuation, stage correctness, session-boundary, winner-selection, no-trade discipline, chart-only outcome, and aggregate closeout; states all IWM slots need concrete samples.
- `SAFE_FAST_IWM_BROADER_COVERAGE_PLANNING_REVIEW.md`: selects IWM as the next broader coverage target and keeps IWM work in planning/replay preparation before any source-data, fixture, replay, chart outcome, schema, or engine change.
- `SAFE_FAST_NEXT_BROADER_COVERAGE_DECISION_REVIEW.md`: documents the IWM-first decision after SPY + QQQ closeout and defers GLD because no later IWM/GLD source-data or window-selection evidence overrides IWM.
- `SAFE_FAST_PROJECT_MASTER_HANDOFF.md`: defines the manual-trading-only target, no auto-trading boundary, protected setup identities, session-boundary behavior, winner-selection behavior, and bar-by-bar replay expectation for SPY / QQQ / IWM / GLD.
- `SAFE_FAST_ON_DEMAND_CLOSEOUT_PLAN.md`: defines protected setup recognition, stage correctness, session-boundary carry-forward, winner selection, no-trade discipline, blocker/caution, and user-facing behavior expected of later IWM samples.
- `SAFE_FAST_BACKTESTING_PLAN.md`: includes IWM in the allowed universe and requires no-hindsight historical signal replay before trade outcome backtesting.
- `historical_signal_replay/`: shows the existing signal/stage/lifecycle replay boundary, fixture/report pattern, source-data intake requirements, SPY/QQQ window-selection pattern, runner output validation pattern, and no-hindsight rules.
- SPY historical replay docs: show the accepted SPY pattern for Continuation, Ideal, and Clean Fast Break source windows, fixtures, signal logs, summaries, validation reviews, and three-setup closeout.
- QQQ historical replay docs: show the accepted QQQ pattern for Ideal, Clean Fast Break, and Continuation source windows, fixtures, signal logs, summaries, evidence reviews, and three-setup closeout.
- SPY chart outcome docs: show the chart-only outcome calculation, validation, aggregate summary, and closeout pattern after real replay evidence exists.
- QQQ chart outcome docs: show the per-setup chart-only outcome calculation/output validation, aggregate summary validation, and QQQ chart outcome closeout pattern.
- Aggregate closeout docs: show that aggregate closeout follows per-setup replay and chart-only outcome validation, not candidate selection.
- Output validation docs: require JSON/schema/count/source-row validation and preserve no-option-P&L, no-account-sizing, no-live-decision boundaries.
- Transition readiness docs: confirm protected on-demand behavior is ready with known limits, not proof of IWM historical signal quality, watcher readiness, or production readiness.
- Files containing `IWM`: show allowed-symbol, planning, deferral, and candidate-slot references, but no concrete IWM source CSV, fixture JSON, replay output, chart outcome result, or historical sample date/window.
- Files containing `Ideal`, `Clean Fast Break`, `Continuation`, `stage`, `session-boundary`, `winner-selection`, `no-trade`, `chart outcome`, and `aggregate closeout`: confirm the required setup families, edge categories, output boundaries, and SPY/QQQ artifact pattern for IWM.

## Concrete IWM Sample Status

- Concrete IWM sample dates/windows currently available in repo evidence: no
- No concrete IWM chart windows are currently present in repo evidence.
- Actual IWM fixture/replay creation remains NO-GO until sample rows are populated with concrete chart evidence.

## Minimum Required IWM Sample Coverage

Before IWM replay/fixture creation can begin, minimum sample coverage must include:

- at least one Ideal candidate
- at least one Clean Fast Break candidate
- at least one Continuation candidate
- at least one developing-stage correctness candidate
- at least one session-boundary carry-forward candidate
- at least one mixed setup / winner-selection candidate
- at least one no-trade discipline candidate
- chart-only outcome candidates for Ideal / Clean Fast Break / Continuation
- aggregate closeout only after per-setup review assets are complete

## Sample Collection Worksheet

| Sample Slot ID | Candidate Type | Setup Type | Required Concrete Evidence | Historical Date / Window | Timeframe Context | Source / Chart Reference | Expected Setup Identity | Expected Stage | Expected Verdict | Expected Blockers | Expected Cautions | Expected Trigger / No-Trade Behavior | Session Boundary Context | Chart-Only Outcome Notes | Fixture/Replay Readiness | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IWM-SAMPLE-IDEAL-001 | real historical replay | Ideal | historical date/window; IWM 1H RTH chart/source evidence; expected identity/stage/verdict/blocker/caution notes | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | NOT READY | Placeholder row for later concrete evidence collection only |
| IWM-SAMPLE-CLEAN-FAST-BREAK-001 | real historical replay | Clean Fast Break | historical date/window; IWM 1H RTH chart/source evidence; expected identity/stage/verdict/blocker/caution notes | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | NOT READY | Placeholder row for later concrete evidence collection only |
| IWM-SAMPLE-CONTINUATION-001 | real historical replay | Continuation | historical date/window; IWM 1H RTH chart/source evidence; shelf/base lifecycle and trigger-state notes | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | NOT READY | Placeholder row for later concrete evidence collection only |
| IWM-SAMPLE-STAGE-DEVELOPING-001 | stage correctness | mixed/all | historical date/window; setup is watchable but not trade-ready; expected developing-stage evidence | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | NOT READY | Placeholder row for later concrete evidence collection only |
| IWM-SAMPLE-SESSION-BOUNDARY-001 | session-boundary carry-forward | Continuation-focused | historical date/window spanning prior/current session context; prior break and fresh-trigger evidence | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | NOT READY | Placeholder row for later concrete evidence collection only |
| IWM-SAMPLE-WINNER-SELECTION-001 | mixed setup winner selection | mixed/all | historical date/window with competing setup candidates and deterministic winner rationale | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | NOT READY | Placeholder row for later concrete evidence collection only |
| IWM-SAMPLE-NO-TRADE-DISCIPLINE-001 | no-trade discipline | mixed/all | historical date/window with blockers/cautions, preserved identity, and expected NO_TRADE or PENDING behavior | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | NOT READY | Placeholder row for later concrete evidence collection only |
| IWM-SAMPLE-CHART-OUTCOME-IDEAL-001 | chart-only outcome | Ideal | accepted IWM Ideal replay row plus copied trigger/invalidation context and future chart rows for outcome measurement | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | NOT READY | Blocked until IWM Ideal replay evidence exists |
| IWM-SAMPLE-CHART-OUTCOME-CLEAN-FAST-BREAK-001 | chart-only outcome | Clean Fast Break | accepted IWM Clean Fast Break replay row plus copied trigger/invalidation context and future chart rows for outcome measurement | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | NOT READY | Blocked until IWM Clean Fast Break replay evidence exists |
| IWM-SAMPLE-CHART-OUTCOME-CONTINUATION-001 | chart-only outcome | Continuation | accepted IWM Continuation replay row plus copied trigger/invalidation context and future chart rows for outcome measurement | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | TO COLLECT | NOT READY | Blocked until IWM Continuation replay evidence exists |

## Evidence Needed Per Sample

Each sample must collect the following before it can become a fixture/replay asset:

- historical date/window
- symbol/timeframe context
- chart or source reference
- setup label
- expected setup identity
- expected stage
- expected verdict
- expected blockers/cautions
- expected trigger/no-trade behavior
- session-date context where relevant
- chart-only outcome notes where relevant

## Fixture Creation Gate

- Fixture creation status: NO-GO until at least the required concrete sample evidence is collected.
- No fixture JSON should be created from placeholder rows.
- Placeholder rows may guide collection only.

## Proposed Next Workflow

1. Populate this worksheet with concrete IWM chart windows/evidence.
2. Validate that each row has enough evidence for replay/review creation.
3. Create IWM Ideal real historical replay review asset first.
4. Create IWM Clean Fast Break real historical replay review asset.
5. Create IWM Continuation real historical replay review asset.
6. Create IWM stage/session/winner/no-trade edge review assets.
7. Create IWM chart-only outcome reviews.
8. Create IWM aggregate closeout review.

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
- no invented sample dates or chart facts

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

Populate IWM historical sample collection worksheet with concrete chart windows/evidence.
