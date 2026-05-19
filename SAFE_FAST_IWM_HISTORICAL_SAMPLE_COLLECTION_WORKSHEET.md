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
- Current objective: populate IWM historical sample collection worksheet from bounded source-window selection.
- Latest IWM bounded source-window selection status: `SAFE_FAST_IWM_BOUNDED_SOURCE_WINDOW_SELECTION_REVIEW.md` passed and selected ten bounded IWM source windows from the validated dxLink 1H RTH source CSV.
- Concrete sample status: bounded IWM source windows are now present as CANDIDATE / NEEDS REVIEW rows; fixture creation status remains NO-GO until row-by-row review confirms final setup identity, stage, trigger, invalidation, blockers, cautions, and replay readiness.
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
- `SAFE_FAST_IWM_BOUNDED_SOURCE_WINDOW_SELECTION_REVIEW.md`: provides ten bounded IWM dxLink 1H RTH source windows selected from `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv`; all labels remain CANDIDATE / NEEDS REVIEW.
- `SAFE_FAST_IWM_SOURCE_CSV_VALIDATION_REVIEW.md`: validates the IWM source CSV, row count, source range, and 1H RTH source-data basis used by the bounded source-window review.
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
- Files containing `IWM`: show allowed-symbol, planning, deferral, candidate-slot references, the validated IWM source CSV, and the bounded source-window selection review; no IWM fixture JSON, replay output, chart outcome result, or final accepted replay sample exists yet.
- Files containing `Ideal`, `Clean Fast Break`, `Continuation`, `stage`, `session-boundary`, `winner-selection`, `no-trade`, `chart outcome`, and `aggregate closeout`: confirm the required setup families, edge categories, output boundaries, and SPY/QQQ artifact pattern for IWM.

## Concrete IWM Sample Status

- Concrete IWM sample dates/windows currently available in repo evidence: yes, as bounded source-window CANDIDATE / NEEDS REVIEW rows from `SAFE_FAST_IWM_BOUNDED_SOURCE_WINDOW_SELECTION_REVIEW.md`.
- Final accepted IWM setup proof currently available in repo evidence: no.
- Actual IWM fixture/replay creation remains NO-GO until row-by-row review confirms setup identity, stage, trigger, invalidation, blockers, cautions, and replay readiness.

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

| Sample Slot ID | Source Window ID | Candidate Type | Historical Date / Window | Timeframe Context | Source / Chart Reference | Expected Setup Type | Direction | Candidate Stage | Trigger-Card Fields To Review | Missing / Unconfirmed Fields | Blocker / Caution Questions | Fresh / Stale / Spent Question | Fixture / Replay Readiness | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IWM-SAMPLE-IDEAL-001 | IWM-WINDOW-IDEAL-001 | real historical replay CANDIDATE | `2026-05-05T09:30:00-04:00` to `2026-05-14T15:30:00-04:00` | IWM dxLink 1H RTH, 56 source rows, `America/New_York` | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv`; bounded review says upside context from `282.57` close on 2026-05-05 into `286.81` close on 2026-05-06, pullback/retest through 2026-05-12 with `278.29` window low, recovery into 2026-05-14 with `285.655` high. | Ideal CANDIDATE / NEEDS REVIEW | bullish/call-side candidate if later review confirms | pullback/retest into recovery CANDIDATE | trigger zone TO REVIEW: recovery through 2026-05-13/2026-05-14 `283.56` to `285.655`; candle/timeframe rule TO REVIEW: completed 1H RTH recovery/hold; invalidation area TO REVIEW: retest low zone near `278.29` if accepted. | Final Ideal identity UNCONFIRMED; EMA/trend context UNCONFIRMED; 24H/daily context UNCONFIRMED; macro/IV/event context UNCONFIRMED; exact trigger/invalidation UNCONFIRMED; final verdict/blockers/cautions UNCONFIRMED. | soft extension after prior highs TO REVIEW; unavailable 24H/macro/IV/event context TO REVIEW. | TO REVIEW whether 2026-05-14 remains fresh or already extended. | READY FOR WORKSHEET; NOT READY FOR FIXTURE until row-by-row review. | Candidate only; no final Ideal proof claimed. |
| IWM-SAMPLE-CLEAN-FAST-BREAK-001 | IWM-WINDOW-CLEAN-FAST-BREAK-001 | real historical replay CANDIDATE | `2026-04-08T09:30:00-04:00` to `2026-04-17T15:30:00-04:00` | IWM dxLink 1H RTH, 56 source rows, `America/New_York` | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv`; bounded review says compact pause around `258.43` to `262.90` on 2026-04-08 through 2026-04-10, upside break on 2026-04-13 reaching `265.36`, follow-through through 2026-04-17 reaching `277.63`. | Clean Fast Break CANDIDATE / NEEDS REVIEW | bullish/call-side candidate if later review confirms | tight pause into upside break and follow-through CANDIDATE | trigger zone TO REVIEW: break/hold above 2026-04-10/2026-04-09 pause highs near `262.75` to `262.90`; candle/timeframe rule TO REVIEW: completed 1H RTH break above compact range; invalidation area TO REVIEW: pause low zone near `260.03` to `260.34` if accepted. | Final Clean Fast Break identity UNCONFIRMED; exact trigger/invalidation UNCONFIRMED; completed-candle approval state UNCONFIRMED; blockers/cautions UNCONFIRMED; 24H/daily/macro/IV/event context UNCONFIRMED. | gap/extension TO REVIEW; missing higher-timeframe context TO REVIEW. | TO REVIEW whether 2026-04-14 to 2026-04-17 rows are spent/follow-through. | READY FOR WORKSHEET; NOT READY FOR FIXTURE until row-by-row review. | Candidate only; no final fast-break proof claimed. |
| IWM-SAMPLE-CONTINUATION-001 | IWM-WINDOW-CONTINUATION-001 | real historical replay CANDIDATE | `2026-04-20T09:30:00-04:00` to `2026-05-01T15:30:00-04:00` | IWM dxLink 1H RTH, 70 source rows, `America/New_York` | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv`; bounded review says prior upside move, higher-price consolidation around `274` to `279`, dip/rebuild through 2026-04-28 and 2026-04-29 with `270.37` low, recovery/break through 2026-04-30 and 2026-05-01 with `279.81` high. | Continuation CANDIDATE / NEEDS REVIEW | bullish/call-side candidate if later review confirms | shelf/base, pullback, rebuild, potential completed break CANDIDATE | trigger zone TO REVIEW: recovery above 2026-04-29 high `274.38`, then hold/reclaim of 2026-04-30 to 2026-05-01 `278` to `279.81`; candle/timeframe rule TO REVIEW: completed 1H RTH shelf break/hold; invalidation area TO REVIEW: shelf/rebuild low near `270.37` or nearer structure low if accepted. | Final Continuation identity UNCONFIRMED; shelf definition UNCONFIRMED; trigger basis/state UNCONFIRMED; exact invalidation UNCONFIRMED; blockers/cautions UNCONFIRMED; unavailable context fields UNCONFIRMED. | prior impulse TO REVIEW; extension TO REVIEW; missing context TO REVIEW. | TO REVIEW whether 2026-04-30 break becomes spent by 2026-05-01. | READY FOR WORKSHEET; NOT READY FOR FIXTURE until row-by-row review. | Candidate only; selected for lifecycle utility. |
| IWM-SAMPLE-STAGE-DEVELOPING-001 | IWM-WINDOW-STAGE-DEVELOPING-001 | developing-stage correctness CANDIDATE | `2026-04-21T09:30:00-04:00` to `2026-04-24T15:30:00-04:00` | IWM dxLink 1H RTH, 28 source rows, `America/New_York` | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv`; bounded review says push to `279.79`, pullback to `271.96` on 2026-04-23, rebuild into 2026-04-24 without a final fixture label. | developing Continuation or mixed CANDIDATE / NEEDS REVIEW | bullish/call-side candidate if later review confirms | developing/rebuild; not assumed trade-ready | trigger zone TO REVIEW: reclaim/hold near `277.86` to `278.13`; candle/timeframe rule TO REVIEW: completed 1H RTH reclaim/hold after pullback; invalidation area TO REVIEW: candidate low near `271.96` if accepted. | Final stage UNCONFIRMED; exact setup identity UNCONFIRMED; exact trigger/invalidation UNCONFIRMED; final verdict UNCONFIRMED; blocker priority UNCONFIRMED; 24H/daily/macro/IV/event context UNCONFIRMED. | no proven hold TO REVIEW; noisy pullback TO REVIEW; missing higher-timeframe context TO REVIEW. | TO REVIEW whether 2026-04-24 rebuild is fresh or still unconfirmed. | READY FOR WORKSHEET; NOT READY FOR FIXTURE until row-by-row review. | Selected to review that developing setups do not become prematurely trade-ready. |
| IWM-SAMPLE-SESSION-BOUNDARY-001 | IWM-WINDOW-SESSION-BOUNDARY-001 | session-boundary carry-forward CANDIDATE | `2026-04-29T09:30:00-04:00` to `2026-05-01T15:30:00-04:00` | IWM dxLink 1H RTH, 21 source rows, `America/New_York` | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv`; bounded review says 2026-04-29 decline/rebuild from `274.38` high to `270.37` low, 2026-04-30 reclaim and close at `277.92`, and 2026-05-01 continuation attempt with `279.81` high. | Continuation CANDIDATE / NEEDS REVIEW | bullish/call-side candidate if later review confirms | prior-session reclaim into next-session carry-forward CANDIDATE | trigger zone TO REVIEW: 2026-04-30 reclaim above `274.38` and 2026-05-01 hold/extension above `278` to `279.81`; candle/timeframe rule TO REVIEW: completed 1H RTH break and next-session freshness check; invalidation area TO REVIEW: 2026-04-29/2026-04-30 rebuild lows near `270.37` to `272.44` if accepted. | Final shelf trigger basis UNCONFIRMED; prior-session spent/fresh decision UNCONFIRMED; exact trigger/invalidation UNCONFIRMED; final stage/verdict UNCONFIRMED; unavailable context fields UNCONFIRMED. | carry-forward freshness TO REVIEW; no fresh current-session trigger TO REVIEW. | TO REVIEW whether 2026-04-30 is prior-session spent context on 2026-05-01. | READY FOR WORKSHEET; NOT READY FOR FIXTURE until row-by-row review. | Source data supports a candidate; final session-boundary proof remains unconfirmed. |
| IWM-SAMPLE-WINNER-SELECTION-001 | IWM-WINDOW-WINNER-SELECTION-001 | mixed setup winner-selection CANDIDATE | `2026-05-05T09:30:00-04:00` to `2026-05-14T15:30:00-04:00` | IWM dxLink 1H RTH, 56 source rows, `America/New_York` | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv`; bounded review says the same bounded window has prior impulse, pullback/retest, recovery, and possible continuation/rebuild interpretations. | Ideal / Continuation mixed CANDIDATE / NEEDS REVIEW | bullish/call-side candidate if later review confirms | competing retest/recovery versus continuation/rebuild CANDIDATE | trigger zone TO REVIEW: `283.56` to `285.655` recovery area; candle/timeframe rule TO REVIEW: completed 1H RTH confirmation for the winning candidate; invalidation area TO REVIEW: `278.29` pullback low zone if accepted. | Final competing candidates UNCONFIRMED; deterministic winner rationale UNCONFIRMED; exact trigger card for winner UNCONFIRMED; blockers/cautions UNCONFIRMED; final verdict UNCONFIRMED; 24H/daily/macro/IV/event context UNCONFIRMED. | overlapping setup identities TO REVIEW; extension TO REVIEW; unavailable context TO REVIEW. | TO REVIEW whether any prior continuation context is stale/spent versus fresh Ideal. | READY FOR WORKSHEET; NOT READY FOR FIXTURE until row-by-row review. | Selected as CANDIDATE / NEEDS REVIEW because source shape alone cannot prove final winner selection. |
| IWM-SAMPLE-NO-TRADE-DISCIPLINE-001 | IWM-WINDOW-NO-TRADE-DISCIPLINE-001 | no-trade discipline CANDIDATE | `2026-05-14T09:30:00-04:00` to `2026-05-18T15:30:00-04:00` | IWM dxLink 1H RTH, 21 source rows, `America/New_York` | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv`; bounded review says failure/rollover after 2026-05-14 high `285.655`, 2026-05-15 gap/down session, and 2026-05-18 lower low to `273.94`. | stale/blocked mixed CANDIDATE / NEEDS REVIEW | long-side caution/no-trade candidate; put-side direction UNCONFIRMED | failed follow-through or stale/spent prior long context CANDIDATE | trigger zone TO REVIEW: no fresh long trigger unless recovery above broken `280` to `284` areas is confirmed; candle/timeframe rule TO REVIEW: completed 1H RTH recovery needed before any fresh long; invalidation area UNCONFIRMED. | Final setup identity UNCONFIRMED; whether put-side candidate exists UNCONFIRMED; exact trigger/invalidation UNCONFIRMED; final NO_TRADE/PENDING verdict UNCONFIRMED; blocker priority UNCONFIRMED; 24H/daily/macro/IV/event context UNCONFIRMED. | failed recovery TO REVIEW; broken structure TO REVIEW; missing context TO REVIEW. | TO REVIEW whether 2026-05-14 long context is spent by 2026-05-15/2026-05-18. | READY FOR WORKSHEET; NOT READY FOR FIXTURE until row-by-row review. | Selected for discipline review, not for live bearish trade decision. |
| IWM-SAMPLE-CHART-OUTCOME-IDEAL-001 | IWM-WINDOW-CHART-OUTCOME-IDEAL-001 | chart-only outcome CANDIDATE | `2026-05-12T09:30:00-04:00` to `2026-05-18T15:30:00-04:00` | IWM dxLink 1H RTH, 35 source rows, `America/New_York` | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv`; bounded review says 2026-05-12 retest/recovery candidate, 2026-05-13/2026-05-14 recovery/high area, and later 2026-05-15/2026-05-18 downside rows for possible future chart-only outcome review after replay acceptance. | Ideal chart-only outcome CANDIDATE / NEEDS REVIEW | bullish/call-side candidate if replay later accepts it | replay-derived trigger/outcome measurement CANDIDATE | trigger zone TO REVIEW only after accepted replay signal, likely in `283.56` to `285.655` area if confirmed; candle/timeframe rule TO REVIEW: copied from accepted replay trigger; invalidation area TO REVIEW: copied from accepted replay. | Accepted replay signal row UNCONFIRMED; final trigger/invalidation UNCONFIRMED; chart-only calculation rule inputs UNCONFIRMED; final setup proof UNCONFIRMED. | chart-only outcome must not be computed before replay acceptance. | copied from replay; currently UNCONFIRMED. | READY FOR WORKSHEET AS OUTCOME CANDIDATE; BLOCKED FOR OUTCOME until replay passes. | No chart outcome calculated in this task. |
| IWM-SAMPLE-CHART-OUTCOME-CLEAN-FAST-BREAK-001 | IWM-WINDOW-CHART-OUTCOME-CLEAN-FAST-BREAK-001 | chart-only outcome CANDIDATE | `2026-04-10T09:30:00-04:00` to `2026-04-20T15:30:00-04:00` | IWM dxLink 1H RTH, 49 source rows, `America/New_York` | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv`; bounded review says compact 2026-04-10 pause, 2026-04-13 break through the pause area, and subsequent 2026-04-14 to 2026-04-20 follow-through rows. | Clean Fast Break chart-only outcome CANDIDATE / NEEDS REVIEW | bullish/call-side candidate if replay later accepts it | replay-derived trigger/outcome measurement CANDIDATE | trigger zone TO REVIEW only after accepted replay signal, likely around `262.75` to `262.90` pause-high area if confirmed; candle/timeframe rule TO REVIEW: copied from accepted replay trigger; invalidation area TO REVIEW: copied from accepted replay. | Accepted replay signal row UNCONFIRMED; final trigger/invalidation UNCONFIRMED; chart-only calculation rule inputs UNCONFIRMED; final setup proof UNCONFIRMED. | chart-only outcome must not be computed before replay acceptance. | copied from replay; currently UNCONFIRMED. | READY FOR WORKSHEET AS OUTCOME CANDIDATE; BLOCKED FOR OUTCOME until replay passes. | No chart outcome calculated in this task. |
| IWM-SAMPLE-CHART-OUTCOME-CONTINUATION-001 | IWM-WINDOW-CHART-OUTCOME-CONTINUATION-001 | chart-only outcome CANDIDATE | `2026-04-28T09:30:00-04:00` to `2026-05-05T15:30:00-04:00` | IWM dxLink 1H RTH, 42 source rows, `America/New_York` | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv`; bounded review says 2026-04-28/2026-04-29 dip and shelf/rebuild, 2026-04-30 reclaim, 2026-05-01 follow-through, and 2026-05-04/2026-05-05 later rows. | Continuation chart-only outcome CANDIDATE / NEEDS REVIEW | bullish/call-side candidate if replay later accepts it | replay-derived continuation trigger/outcome measurement CANDIDATE | trigger zone TO REVIEW only after accepted replay signal, likely around `274.38`, `278.22`, or `279.81` depending on row-by-row review; candle/timeframe rule TO REVIEW: copied from accepted replay trigger; invalidation area TO REVIEW: copied from accepted replay. | Accepted replay signal row UNCONFIRMED; final trigger/invalidation UNCONFIRMED; chart-only calculation rule inputs UNCONFIRMED; final setup proof UNCONFIRMED. | chart-only outcome must not be computed before replay acceptance. | copied from replay; currently UNCONFIRMED. | READY FOR WORKSHEET AS OUTCOME CANDIDATE; BLOCKED FOR OUTCOME until replay passes. | No chart outcome calculated in this task. |

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

Create the first IWM row-by-row replay readiness review from the populated worksheet, starting with `IWM-SAMPLE-IDEAL-001`, without creating fixtures until the row is validated.
