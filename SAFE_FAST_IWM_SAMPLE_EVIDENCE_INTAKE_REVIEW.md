# SAFE-FAST IWM Sample Evidence Intake Review

## Review Status

- Review status: PASS
- Baseline: patch8
- Repo: safe-fast-backendnew
- Branch: main
- Current pushed HEAD verified locally: `d202a33 Add missing-data trigger card surface contract`
- Work mode: build work only, no live trade decisions

## Purpose

This intake review resumes IWM historical sample collection/population by checking whether existing repo evidence can populate concrete IWM worksheet rows. It is docs/replay-prep only. It does not create fixtures, modify replay logic, modify schemas, change generated reports, touch `main.py`, touch Railway/production files, calculate option P&L, add account sizing, start auto-trading, start Continuous Watcher implementation, or make live trade decisions.

## Baseline And Conflict Check

- `SAFE_FAST_BUILD_STATE.md` was read first.
- `git status -sb` result before edits: `## main...origin/main`
- `git log --oneline -12` confirmed `d202a33 Add missing-data trigger card surface contract` at HEAD.
- Uncommitted changes before this task: none.
- Known non-conflict preserved: `SAFE_FAST_BUILD_STATE.md` may list `5d33edc` as the completed QQQ closeout milestone while local HEAD is newer.

## Evidence Reviewed

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_DAY60_PRODUCT_BUSINESS_HANDOFF_ADDENDUM.md`
- `SAFE_FAST_IWM_HISTORICAL_SAMPLE_COLLECTION_WORKSHEET.md`
- `SAFE_FAST_IWM_REAL_HISTORICAL_REPLAY_CANDIDATE_SELECTION_REVIEW.md`
- `SAFE_FAST_IWM_FIXTURE_REPLAY_CANDIDATE_INVENTORY.md`
- `SAFE_FAST_IWM_BROADER_COVERAGE_PLANNING_REVIEW.md`
- `SAFE_FAST_ON_DEMAND_TRIGGER_CARD_REQUIREMENT_REVIEW.md`
- `SAFE_FAST_ON_DEMAND_TRIGGER_CARD_SURFACE_CONTRACT_GAP_REVIEW.md`
- latest trigger-card contract statuses in `SAFE_FAST_BUILD_STATE.md`
- SPY/QQQ replay and chart outcome docs for sample-selection pattern
- repository files mentioning `IWM`

## Intake Finding

No concrete IWM chart windows/evidence were found in repo evidence.

Repo references to IWM are limited to allowed-symbol coverage, planning/deferral docs, candidate-slot requirements, trigger-card inheritance requirements, on-demand contract symbol-order references, and generic no-hindsight example shape artifacts.

The existing `historical_signal_replay/fixtures/no_hindsight_ideal_signal_replay_fixture.json` and matching `historical_signal_replay/reports/no_hindsight_sample_signal_log.jsonl` contain IWM-shaped Ideal sample data, but `historical_signal_replay/README.md` identifies these fixtures as no-hindsight example shapes only. Their winner-selection status is `shape_only_unimplemented`, and they are not backed by accepted IWM source CSV validation, bounded IWM window-selection review, fixture design from real IWM source rows, runner output validation, chart window review, or closeout evidence. They cannot populate concrete IWM worksheet rows without inventing sample provenance.

## Go / No-Go Decision

- Concrete IWM sample evidence in repo: no
- Worksheet population from existing repo evidence: NO-GO
- Actual IWM replay/fixture creation: NO-GO until concrete IWM sample windows are supplied
- Next practical input needed: concrete IWM chart windows/evidence for the worksheet slots
- Trigger-card requirement: trigger-card fields must be collected with each IWM sample
- Broader sequencing: the build should not move to GLD or Continuous Watcher implementation until IWM sample population is started or explicitly deferred

## Required Trigger-Card Fields Per Sample

Each concrete IWM sample must collect or explicitly mark unconfirmed:

- setup type
- direction
- stage
- trigger status
- trigger level or trigger zone
- candle/timeframe confirmation rule
- current distance to trigger when available
- early-warning or near-trigger threshold when available
- invalidation level or condition
- fresh/stale/spent condition
- next check or next alert condition
- blocker/caution relationship to trigger readiness

## Collection Checklist

| Required Sample Type | Historical Date / Window | Timeframe Context | Chart / Source Reference | Expected Setup Type | Expected Stage | Expected Trigger-Card Fields | Expected Blocker / Caution If Any | Expected Stale / Spent / Fresh Behavior | Notes For Replay / Review Creation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Ideal | REQUIRED | REQUIRED | REQUIRED | Ideal | REQUIRED | REQUIRED | REQUIRED or UNCONFIRMED | REQUIRED | preserve no-hindsight source rows; do not create fixture until source/window evidence is reviewed |
| Clean Fast Break | REQUIRED | REQUIRED | REQUIRED | Clean Fast Break | REQUIRED | REQUIRED | REQUIRED or UNCONFIRMED | REQUIRED | preserve no-hindsight source rows; do not create fixture until source/window evidence is reviewed |
| Continuation | REQUIRED | REQUIRED | REQUIRED | Continuation | REQUIRED | REQUIRED | REQUIRED or UNCONFIRMED | REQUIRED | include shelf/base lifecycle and completed-candle trigger path before fixture work |
| developing-stage correctness | REQUIRED | REQUIRED | REQUIRED | Ideal / Clean Fast Break / Continuation as evidenced | developing / watchable stage REQUIRED | REQUIRED | REQUIRED or UNCONFIRMED | REQUIRED | prove setup does not become trade-ready before trigger evidence exists |
| session-boundary carry-forward | REQUIRED | REQUIRED | REQUIRED | Continuation-focused unless evidence supports another setup | prior/current session stage REQUIRED | REQUIRED | REQUIRED or UNCONFIRMED | REQUIRED | include prior-session context, current-session context, and fresh-trigger decision |
| mixed setup / winner selection | REQUIRED | REQUIRED | REQUIRED | mixed setup candidates REQUIRED | REQUIRED | REQUIRED | REQUIRED or UNCONFIRMED | REQUIRED | include competing setup evidence and deterministic winner rationale |
| no-trade discipline | REQUIRED | REQUIRED | REQUIRED | setup identity REQUIRED | NO_TRADE or PENDING stage REQUIRED | REQUIRED | REQUIRED | REQUIRED | preserve setup identity while documenting why trade approval is blocked |
| chart-only outcome Ideal | REQUIRED after accepted Ideal replay row | REQUIRED | REQUIRED | Ideal | accepted replay trigger row REQUIRED | REQUIRED | REQUIRED or UNCONFIRMED | REQUIRED | blocked until IWM Ideal replay evidence exists; future rows used only for outcome measurement |
| chart-only outcome Clean Fast Break | REQUIRED after accepted Clean Fast Break replay row | REQUIRED | REQUIRED | Clean Fast Break | accepted replay trigger row REQUIRED | REQUIRED | REQUIRED or UNCONFIRMED | REQUIRED | blocked until IWM Clean Fast Break replay evidence exists; future rows used only for outcome measurement |
| chart-only outcome Continuation | REQUIRED after accepted Continuation replay row | REQUIRED | REQUIRED | Continuation | accepted replay trigger row REQUIRED | REQUIRED | REQUIRED or UNCONFIRMED | REQUIRED | blocked until IWM Continuation replay evidence exists; future rows used only for outcome measurement |

## Boundary Confirmation

- main.py changed: no
- Engine logic changed: no
- Replay runner changed: no
- Schemas changed: no
- Fixtures changed: no
- Reports changed: no
- Railway/production touched: no
- Live trade decisions added: no
- Option P&L added: no
- Account sizing added: no
- Auto-trading added: no
- Continuous Watcher implementation started: no

## What Remains Unproven

- IWM concrete sample population
- IWM source-data validation
- IWM bounded window selection
- IWM fixture/replay creation
- IWM replay output validation
- IWM chart-only outcome coverage
- IWM aggregate closeout
- GLD broader coverage
- Continuous Watcher behavior
- option P&L
- account sizing
- production readiness

## Recommended Next Task

Supply concrete IWM chart windows/evidence for the worksheet slots, including trigger-card fields for each sample.
