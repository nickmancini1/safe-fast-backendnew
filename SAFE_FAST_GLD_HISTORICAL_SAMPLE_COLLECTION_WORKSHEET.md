# SAFE-FAST GLD Historical Sample Collection Worksheet

## Worksheet Status

- Worksheet status: PASS
- Baseline: patch8
- Repo: safe-fast-backendnew
- Branch: main
- Work mode: build work only, no live trade decisions

## Baseline Checked

`SAFE_FAST_BUILD_STATE.md` says:

- GLD is the active broader coverage target after completed SPY / QQQ / IWM current-depth closeout.
- Current objective: GLD historical sample worksheet population or GLD first setup replay readiness review from selected bounded candidate windows.
- Latest GLD bounded source-window selection status: `SAFE_FAST_GLD_BOUNDED_SOURCE_WINDOW_SELECTION_REVIEW.md` passed and selected three bounded GLD source windows from the validated dxLink 1H RTH source CSV.
- Concrete GLD sample status: bounded GLD source windows are now present as CANDIDATE / NEEDS REVIEW rows; fixture creation status remains NO-GO until row-by-row review confirms setup identity, stage, trigger, invalidation, blockers, cautions, and replay readiness.
- Continuous Watcher deferral: Continuous Watcher remains deferred.
- No-touch boundaries: do not touch Railway, production deploy files, `main.py`, engine logic, replay runner logic, schemas, fixtures, generated reports, option P&L, account sizing, auto-trading, live trade decisions, or Continuous Watcher implementation in this docs/replay-prep task.

## Repo State Checked

- Git status result: `## main...origin/main`
- Latest commits:
  - `00d52ff Fix latest completed commit after GLD window selection`
  - `43e9d42 Add GLD bounded source-window selection review`
  - `0ee8545 Fix latest completed commit after GLD source CSV validation`
  - `3a95868 Sync build state after GLD source CSV validation`
  - `f7fbdfc Validate GLD source CSV`
  - `eb20d20 Add GLD source CSV validation blocked review`
- Conflicts found: none. The worktree was clean before this docs/worksheet task.

## Purpose

This worksheet exists to collect concrete GLD historical sample windows before fixture/replay creation can begin. It is a collection aid only. It does not create GLD fixture JSON, modify replay logic, produce generated reports, calculate chart outcomes, create aggregate closeout, model option P&L, add account sizing, or make live-trade conclusions.

## Existing Evidence Reviewed

- `SAFE_FAST_BUILD_STATE.md`: confirms patch8, active repo/branch, GLD active broader coverage target, current worksheet/replay-readiness objective, Continuous Watcher deferral, and no-touch boundaries.
- `SAFE_FAST_GLD_SOURCE_CSV_VALIDATION_REVIEW.md`: validates the GLD source CSV, 290-row count, `2026-03-23T09:30:00-04:00` to `2026-05-20T11:30:00-04:00` source range, dxLink 1H RTH source-data basis, source/vendor/as-of metadata, and unavailable context field handling.
- `SAFE_FAST_GLD_BOUNDED_SOURCE_WINDOW_SELECTION_REVIEW.md`: provides three bounded GLD dxLink 1H RTH source windows selected from `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv`; all labels remain CANDIDATE / NEEDS REVIEW.
- `SAFE_FAST_IWM_HISTORICAL_SAMPLE_COLLECTION_WORKSHEET.md`: provides the closest existing worksheet naming, structure, and provisional candidate-label style.
- `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv`: validated source CSV used for row ranges, timestamp spans, row counts, and source-observation facts only.

## Concrete GLD Sample Status

- Concrete GLD sample dates/windows currently available in repo evidence: yes, as bounded source-window CANDIDATE / NEEDS REVIEW rows from `SAFE_FAST_GLD_BOUNDED_SOURCE_WINDOW_SELECTION_REVIEW.md`.
- Final accepted GLD setup proof currently available in repo evidence: no.
- Actual GLD fixture/replay creation remains NO-GO until row-by-row review confirms setup identity, stage, trigger, invalidation, blockers, cautions, and replay readiness.

## Minimum Required GLD Sample Coverage

Before GLD replay/fixture creation can begin, minimum sample coverage for this current-depth broader coverage pass includes:

- at least one Ideal candidate
- at least one Clean Fast Break candidate
- at least one Continuation candidate

Put-side setup-family candidates and no-trade discipline windows remain unconfirmed / not selected in the bounded source-window selection review.

## Sample Collection Worksheet

| Sample Slot ID | Source Window ID | Candidate Type | Historical Date / Window | Timeframe Context | Source / Chart Reference | Expected Setup Type | Direction | Candidate Stage | Trigger-Card Fields To Review | Missing / Unconfirmed Fields | Blocker / Caution Questions | Fresh / Stale / Spent Question | Fixture / Replay Readiness | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GLD-SAMPLE-IDEAL-001 | GLD-WINDOW-IDEAL-001 | real historical replay CANDIDATE | rows 204-238; `2026-05-04T09:30:00-04:00` to `2026-05-08T15:30:00-04:00` | GLD dxLink 1H RTH, 35 source rows, `America/New_York` | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv`; bounded review says low/retest area on 2026-05-04 near `413.2801`, 2026-05-05 base with `417.9050` to `421.1300` range, recovery through 2026-05-06/2026-05-07 into `437.4200` window high, and 2026-05-08 pullback rows. CSV source observations: first open `418.815`, final close `433.795`, window high `437.42`, window low `413.2801`. | Ideal CANDIDATE / NEEDS REVIEW | bullish/call-side candidate if later review confirms | pullback/retest into recovery CANDIDATE | trigger zone TO REVIEW: recovery through the 2026-05-06/2026-05-07 `433.1900` to `437.4200` area; candle/timeframe rule TO REVIEW: completed 1H RTH recovery/hold; invalidation area TO REVIEW: 2026-05-04 low zone near `413.2801` if accepted. | Final Ideal identity UNCONFIRMED; EMA/trend context UNCONFIRMED; 24H/daily context UNCONFIRMED; macro/IV/event context UNCONFIRMED; exact trigger/invalidation UNCONFIRMED; final stage/verdict/blockers/cautions UNCONFIRMED. | unavailable 24H/macro/IV/event context TO REVIEW; possible extension after recovery TO REVIEW. | TO REVIEW whether the 2026-05-07 recovery is fresh or already extended by later rows. | READY FOR WORKSHEET; NOT READY FOR FIXTURE until row-by-row review. | Candidate only; no final Ideal proof claimed. |
| GLD-SAMPLE-CLEAN-FAST-BREAK-001 | GLD-WINDOW-CLEAN-FAST-BREAK-001 | real historical replay CANDIDATE | rows 183-238; `2026-04-29T09:30:00-04:00` to `2026-05-08T15:30:00-04:00` | GLD dxLink 1H RTH, 56 source rows, `America/New_York` | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv`; bounded review says lower-price base/rebuild from 2026-04-29 through 2026-05-05 with a `413.2801` window low, then 2026-05-06 gap/reclaim and 2026-05-07 push to `437.4200`, followed by 2026-05-08 pullback context. CSV source observations: first open `416.74`, final close `433.795`, window high `437.42`, window low `413.2801`. | Clean Fast Break CANDIDATE / NEEDS REVIEW | bullish/call-side candidate if later review confirms | base/rebuild into fast upside reclaim CANDIDATE | trigger zone TO REVIEW: 2026-05-06 break/reclaim above prior `425.4500` to `427.9200` area and later hold toward `433.1900`; candle/timeframe rule TO REVIEW: completed 1H RTH break/hold above compact range; invalidation area TO REVIEW: base low zone near `413.2801` or nearer structure low if accepted. | Final Clean Fast Break identity UNCONFIRMED; exact trigger/invalidation UNCONFIRMED; completed-candle approval state UNCONFIRMED; blockers/cautions UNCONFIRMED; 24H/daily/macro/IV/event context UNCONFIRMED. | gap/extension TO REVIEW; missing higher-timeframe context TO REVIEW. | TO REVIEW whether 2026-05-07/2026-05-08 rows are follow-through or spent. | READY FOR WORKSHEET; NOT READY FOR FIXTURE until row-by-row review. | Candidate only; overlaps the Ideal candidate window, so final family separation remains unconfirmed. |
| GLD-SAMPLE-CONTINUATION-001 | GLD-WINDOW-CONTINUATION-001 | real historical replay CANDIDATE | rows 78-133; `2026-04-08T09:30:00-04:00` to `2026-04-17T15:30:00-04:00` | GLD dxLink 1H RTH, 56 source rows, `America/New_York` | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv`; bounded review says elevated consolidation around the `431.31` to `440.9050` area from 2026-04-08 through 2026-04-13, recovery/push on 2026-04-14 to `445.1800`, and later 2026-04-17 extension to `448.7000` window high. CSV source observations: first open `440.12`, final close `445.88`, window high `448.7`, window low `431.31`. | Continuation CANDIDATE / NEEDS REVIEW | bullish/call-side candidate if later review confirms | elevated shelf/base into potential completed break and follow-through CANDIDATE | trigger zone TO REVIEW: break/hold above the 2026-04-08 through 2026-04-10 `440.9050` area and later 2026-04-14/2026-04-17 continuation behavior; candle/timeframe rule TO REVIEW: completed 1H RTH shelf break/hold; invalidation area TO REVIEW: shelf/rebuild low near `431.31` or nearer structure low if accepted. | Final Continuation identity UNCONFIRMED; shelf definition UNCONFIRMED; trigger basis/state UNCONFIRMED; exact invalidation UNCONFIRMED; fresh/spent determination UNCONFIRMED; blockers/cautions UNCONFIRMED; unavailable context fields UNCONFIRMED. | prior impulse TO REVIEW; extension TO REVIEW; missing context TO REVIEW. | TO REVIEW whether the 2026-04-14 push is fresh or spent by 2026-04-17. | READY FOR WORKSHEET; NOT READY FOR FIXTURE until row-by-row review. | Candidate only; final session/stage treatment remains unconfirmed. |

## Evidence Needed Per Sample

Each sample must collect the following before it can become a fixture/replay asset:

- historical date/window
- symbol/timeframe context
- source row references
- setup label as CANDIDATE / NEEDS REVIEW
- expected setup identity to review
- expected stage to review
- expected blockers/cautions to review
- expected trigger/no-trade behavior to review
- missing context fields and unavailable higher-timeframe data

## Fixture Creation Gate

- Fixture creation status: NO-GO until at least the required concrete sample evidence is reviewed row by row.
- No fixture JSON should be created from worksheet candidate rows.
- Worksheet candidate rows may guide collection only.

## Proposed Next Workflow

1. Create GLD Ideal 001 row-by-row replay readiness review from this worksheet.
2. Create GLD Ideal 001 real historical replay review asset only if the row-by-row readiness review passes.
3. Repeat the same readiness path for GLD Clean Fast Break 001 and GLD Continuation 001.

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
- no replay reports created in this task
- no chart outcomes created in this task
- no aggregate closeout created in this task
- no invented sample dates, setup labels, trigger labels, chart outcomes, or trade facts

## What Remains Unproven

- GLD replay-readiness proof
- GLD final setup identity
- GLD exact trigger/invalidation behavior
- GLD fixture execution
- GLD chart-only outcomes
- GLD aggregate closeout
- Continuous Watcher behavior
- alert suppression
- shadow/live validation
- option P&L
- account sizing
- production readiness

## Recommended Next Task

Create the first GLD row-by-row replay readiness review from the populated worksheet, starting with `GLD-SAMPLE-IDEAL-001`, without creating fixtures until the row is validated.
