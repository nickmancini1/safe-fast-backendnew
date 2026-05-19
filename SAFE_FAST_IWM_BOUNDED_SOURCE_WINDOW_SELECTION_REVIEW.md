# SAFE-FAST IWM Bounded Source-Window Selection Review

## Review Status

- Review status: PASS
- Baseline: patch8
- Repo: safe-fast-backendnew
- Branch: main
- Work mode: build work only, no live trade decisions

## Baseline Checked

- Current HEAD: `4fe8d43 Add IWM source CSV validation`
- IWM source CSV validation: PASS
- Trigger-card contracts complete for this phase: yes; the current source-window selection review can collect trigger-card fields and mark missing fields unconfirmed without requiring more trigger-card contract work first.
- IWM active target: yes; IWM remains the active broader coverage target.
- GLD deferred: yes.
- Continuous Watcher deferred: yes.
- SPY + QQQ closeout remains accepted: yes.

## Repo State Checked

- Git status result before edits: `## main...origin/main`
- Latest commits:
  - `4fe8d43 Add IWM source CSV validation`
  - `1237f14 Add IWM source CSV export blocked review`
  - `6cdeec3 Add IWM source CSV export request review`
  - `a8e597d Add IWM sample source extraction review`
  - `7d67095 Add IWM sample sourcing method review`
  - `be35e52 Add IWM sample evidence intake review`
  - `d202a33 Add missing-data trigger card surface contract`
  - `1318fa4 Add near-trigger early warning trigger card surface contract`
  - `1f6b5f1 Add blocked identifiable trigger card surface contract`
  - `7b46718 Add put-side trigger card surface contract`
  - `79fbe77 Add Clean Fast Break trigger card surface contract`
  - `8a1c4c4 Add Ideal trigger card surface contract`
- Conflicts found: none. The working tree was clean and synced with `origin/main` before this docs/replay-prep task.

## Source CSV Used

- CSV path: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv`
- Row count: 287
- First timestamp: `2026-03-20T09:30:00-04:00`
- Last timestamp: `2026-05-18T15:30:00-04:00`
- Timeframe/session: `1h_rth`, regular RTH rows, `America/New_York`
- Validation status: PASS in `SAFE_FAST_IWM_SOURCE_CSV_VALIDATION_REVIEW.md`

## Selection Method

The windows below were selected from validated IWM dxLink 1H RTH source CSV rows only. The selection follows the SPY/QQQ pattern: use contiguous bounded source rows, choose visible candidate setup-family shapes, keep labels provisional, document trigger-card fields to review, and defer fixture design, replay execution, generated reports, and chart-only outcome proof.

This is source-window selection only. These windows are candidate inputs for later row-by-row fixture/replay review. They do not prove final setup classification, final trigger validity, trade outcome quality, option P&L, account sizing, watcher readiness, production readiness, or live trade decisions.

## Selected Candidate Windows

| Window ID | Candidate Type | Setup Type | Direction | Start Timestamp | End Timestamp | Source Evidence Summary | Trigger-Card Fields To Review | Missing / Unconfirmed Fields | Fixture/Replay Readiness | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IWM-WINDOW-IDEAL-001 | real historical replay candidate | Ideal CANDIDATE | bullish/call-side candidate | `2026-05-05T09:30:00-04:00` | `2026-05-14T15:30:00-04:00` | 56 rows. Source window shows upside context from `282.57` close on 2026-05-05 into `286.81` close on 2026-05-06, pullback/retest behavior through 2026-05-12 with `278.29` window low, and recovery into 2026-05-14 with `285.655` high. | Expected setup type: Ideal CANDIDATE; direction: bullish if later review confirms; candidate stage: pullback/retest into recovery; trigger zone to review: recovery through the 2026-05-13/2026-05-14 `283.56` to `285.655` area; candle/timeframe rule: completed 1H RTH recovery/hold; invalidation area: retest low zone near `278.29` if later review accepts it; fresh/stale/spent question: whether 2026-05-14 remains fresh or already extended; blocker/caution questions: soft extension after prior highs, unavailable 24H/macro/IV/event context. | Final Ideal identity, EMA/trend context, 24H/daily context, macro, IV, event context, exact trigger level, exact invalidation, final verdict, blockers/cautions. | READY FOR WORKSHEET; NOT READY FOR FIXTURE until row-by-row review. | Candidate only; no final Ideal proof claimed. |
| IWM-WINDOW-CLEAN-FAST-BREAK-001 | real historical replay candidate | Clean Fast Break CANDIDATE | bullish/call-side candidate | `2026-04-08T09:30:00-04:00` | `2026-04-17T15:30:00-04:00` | 56 rows. Source window shows compact pause around the `258.43` to `262.90` area on 2026-04-08 through 2026-04-10, upside break through the pause area on 2026-04-13 reaching `265.36`, and follow-through through 2026-04-17 reaching `277.63`. | Expected setup type: Clean Fast Break CANDIDATE; direction: bullish if later review confirms; candidate stage: tight pause into upside break and follow-through; trigger zone to review: break/hold above the 2026-04-10/2026-04-09 pause highs near `262.75` to `262.90`; candle/timeframe rule: completed 1H RTH break above compact range; invalidation area: pause low zone near `260.03` to `260.34` if later review accepts it; fresh/stale/spent question: whether later 2026-04-14 to 2026-04-17 rows are spent/follow-through; blocker/caution questions: gap/extension and missing higher-timeframe context. | Final Clean Fast Break identity, exact trigger, exact invalidation, completed-candle approval state, blockers/cautions, 24H/daily context, macro, IV, event context. | READY FOR WORKSHEET; NOT READY FOR FIXTURE until row-by-row review. | Candidate only; no final fast-break proof claimed. |
| IWM-WINDOW-CONTINUATION-001 | real historical replay candidate | Continuation CANDIDATE | bullish/call-side candidate | `2026-04-20T09:30:00-04:00` | `2026-05-01T15:30:00-04:00` | 70 rows. Source window follows the prior upside move, then shows higher-price consolidation around `274` to `279`, a dip/rebuild through 2026-04-28 and 2026-04-29 with `270.37` low, and recovery/break behavior through 2026-04-30 and 2026-05-01 with `279.81` high. | Expected setup type: Continuation CANDIDATE; direction: bullish if later review confirms; candidate stage: shelf/base, pullback, rebuild, potential completed break; trigger zone to review: recovery above 2026-04-29 high `274.38`, then hold/reclaim of 2026-04-30 to 2026-05-01 `278` to `279.81` area; candle/timeframe rule: completed 1H RTH shelf break/hold; invalidation area: shelf/rebuild low near `270.37` or nearer structure low if later review accepts it; fresh/stale/spent question: whether 2026-04-30 break becomes spent by 2026-05-01; blocker/caution questions: prior impulse, extension, missing context. | Final Continuation identity, shelf definition, trigger basis, exact trigger state, exact invalidation, fresh/spent determination, blockers/cautions, unavailable context fields. | READY FOR WORKSHEET; NOT READY FOR FIXTURE until row-by-row review. | Candidate only; selected for lifecycle utility. |
| IWM-WINDOW-STAGE-DEVELOPING-001 | developing-stage correctness candidate | Continuation / mixed CANDIDATE | bullish/call-side candidate if confirmed | `2026-04-21T09:30:00-04:00` | `2026-04-24T15:30:00-04:00` | 28 rows. Source window starts with a push to `279.79`, then pulls back to `271.96` on 2026-04-23 and rebuilds into 2026-04-24 without a final fixture label. This gives a bounded candidate for developing, rebuilding, pending, or blocked-stage review. | Expected setup type: developing Continuation or mixed CANDIDATE; direction: bullish if later review confirms; candidate stage: developing/rebuild, not assumed trade-ready; trigger zone to review: reclaim/hold near `277.86` to `278.13`; candle/timeframe rule: completed 1H RTH reclaim/hold after pullback; invalidation area: candidate low near `271.96` if later review accepts it; fresh/stale/spent question: whether the 2026-04-24 rebuild is fresh or still unconfirmed; blocker/caution questions: no proven hold, noisy pullback, missing higher-timeframe context. | Final stage, exact setup identity, exact trigger, exact invalidation, final verdict, blocker priority, 24H/daily, macro, IV, event context. | READY FOR WORKSHEET; NOT READY FOR FIXTURE until row-by-row review. | Selected to review that developing setups do not become prematurely trade-ready. |
| IWM-WINDOW-SESSION-BOUNDARY-001 | session-boundary carry-forward candidate | Continuation CANDIDATE | bullish/call-side candidate if confirmed | `2026-04-29T09:30:00-04:00` | `2026-05-01T15:30:00-04:00` | 21 rows. Source window spans a 2026-04-29 decline/rebuild from `274.38` high to `270.37` low, a 2026-04-30 reclaim and close at `277.92`, and a 2026-05-01 continuation attempt with `279.81` high. | Expected setup type: Continuation CANDIDATE; direction: bullish if later review confirms; candidate stage: prior-session reclaim into next-session carry-forward; trigger zone to review: 2026-04-30 reclaim above `274.38` and 2026-05-01 hold/extension above `278` to `279.81`; candle/timeframe rule: completed 1H RTH break and next-session freshness check; invalidation area: 2026-04-29/2026-04-30 rebuild lows near `270.37` to `272.44` if later review accepts them; fresh/stale/spent question: whether 2026-04-30 is prior-session spent context on 2026-05-01; blocker/caution questions: carry-forward freshness and no fresh current-session trigger. | Final shelf trigger basis, prior-session spent/fresh decision, exact trigger, exact invalidation, final stage/verdict, unavailable context fields. | READY FOR WORKSHEET; NOT READY FOR FIXTURE until row-by-row review. | Source data supports a candidate; final session-boundary proof remains unconfirmed. |
| IWM-WINDOW-WINNER-SELECTION-001 | mixed/winner-selection candidate | Ideal / Continuation mixed CANDIDATE | bullish/call-side candidate if confirmed | `2026-05-05T09:30:00-04:00` | `2026-05-14T15:30:00-04:00` | 56 rows. The same bounded window has prior impulse, pullback/retest, recovery, and possible continuation/rebuild interpretations. This makes it useful for reviewing deterministic winner selection if multiple candidate identities compete. | Expected setup type: mixed CANDIDATE; direction: bullish if later review confirms; candidate stage: competing retest/recovery versus continuation/rebuild; trigger zone to review: `283.56` to `285.655` recovery area; candle/timeframe rule: completed 1H RTH confirmation for the winning candidate; invalidation area: `278.29` pullback low zone if accepted; fresh/stale/spent question: whether any prior continuation context is stale/spent versus fresh Ideal; blocker/caution questions: overlapping setup identities, extension, unavailable context. | Final competing candidates, deterministic winner rationale, exact trigger card for winner, blockers/cautions, final verdict, 24H/daily, macro, IV, event context. | READY FOR WORKSHEET; NOT READY FOR FIXTURE until row-by-row review. | Selected as CANDIDATE / NEEDS REVIEW because source shape alone cannot prove final winner selection. |
| IWM-WINDOW-NO-TRADE-DISCIPLINE-001 | no-trade discipline candidate | mixed/all CANDIDATE | bearish/defensive context for long-side discipline; put-side unconfirmed | `2026-05-14T09:30:00-04:00` | `2026-05-18T15:30:00-04:00` | 21 rows. Source window shows failure/rollover after 2026-05-14 high `285.655`, with 2026-05-15 gap/down session and 2026-05-18 lower low to `273.94`. This supports a no-trade/stale-long discipline candidate without claiming put-side setup proof. | Expected setup type: stale/blocked mixed CANDIDATE; direction: long-side caution/no-trade candidate, put-side direction unconfirmed; candidate stage: failed follow-through or stale/spent prior long context; trigger zone to review: no fresh long trigger unless recovery above broken `280` to `284` areas is confirmed; candle/timeframe rule: completed 1H RTH recovery needed before any fresh long; invalidation area: unconfirmed; fresh/stale/spent question: whether 2026-05-14 long context is spent by 2026-05-15/2026-05-18; blocker/caution questions: failed recovery, broken structure, missing context. | Final setup identity, whether put-side candidate exists, exact trigger/invalidation, final NO_TRADE/PENDING verdict, blocker priority, 24H/daily, macro, IV, event context. | READY FOR WORKSHEET; NOT READY FOR FIXTURE until row-by-row review. | Selected for discipline review, not for live bearish trade decision. |
| IWM-WINDOW-CHART-OUTCOME-IDEAL-001 | chart-only outcome candidate window | Ideal CANDIDATE | bullish/call-side candidate if replay later accepts it | `2026-05-12T09:30:00-04:00` | `2026-05-18T15:30:00-04:00` | 35 rows. Source window contains the 2026-05-12 retest/recovery candidate, 2026-05-13/2026-05-14 recovery/high area, and later 2026-05-15/2026-05-18 downside rows for possible future chart-only outcome review after replay acceptance. | Expected setup type: Ideal chart-only outcome CANDIDATE; direction: bullish if accepted by replay; candidate stage: replay-derived trigger/outcome measurement candidate; trigger zone to review: replay-accepted Ideal trigger only, likely in `283.56` to `285.655` area if confirmed; candle/timeframe rule: copied from accepted replay trigger; invalidation area: copied from accepted replay; fresh/stale/spent question: copied from replay; blocker/caution questions: chart-only outcome must not be computed before replay acceptance. | Accepted replay signal row, final trigger, final invalidation, chart-only calculation rule inputs, final setup proof. | READY FOR WORKSHEET AS OUTCOME CANDIDATE; BLOCKED FOR OUTCOME until replay passes. | No chart outcome calculated in this task. |
| IWM-WINDOW-CHART-OUTCOME-CLEAN-FAST-BREAK-001 | chart-only outcome candidate window | Clean Fast Break CANDIDATE | bullish/call-side candidate if replay later accepts it | `2026-04-10T09:30:00-04:00` | `2026-04-20T15:30:00-04:00` | 49 rows. Source window includes the compact 2026-04-10 pause, the 2026-04-13 break through the pause area, and subsequent 2026-04-14 to 2026-04-20 follow-through rows. | Expected setup type: Clean Fast Break chart-only outcome CANDIDATE; direction: bullish if accepted by replay; candidate stage: replay-derived trigger/outcome measurement candidate; trigger zone to review: replay-accepted fast-break trigger only, likely around the `262.75` to `262.90` pause-high area if confirmed; candle/timeframe rule: copied from accepted replay trigger; invalidation area: copied from accepted replay; fresh/stale/spent question: copied from replay; blocker/caution questions: chart-only outcome must not be computed before replay acceptance. | Accepted replay signal row, final trigger, final invalidation, chart-only calculation rule inputs, final setup proof. | READY FOR WORKSHEET AS OUTCOME CANDIDATE; BLOCKED FOR OUTCOME until replay passes. | No chart outcome calculated in this task. |
| IWM-WINDOW-CHART-OUTCOME-CONTINUATION-001 | chart-only outcome candidate window | Continuation CANDIDATE | bullish/call-side candidate if replay later accepts it | `2026-04-28T09:30:00-04:00` | `2026-05-05T15:30:00-04:00` | 42 rows. Source window includes the 2026-04-28/2026-04-29 dip and shelf/rebuild, 2026-04-30 reclaim, 2026-05-01 follow-through, and 2026-05-04/2026-05-05 later rows. | Expected setup type: Continuation chart-only outcome CANDIDATE; direction: bullish if accepted by replay; candidate stage: replay-derived continuation trigger/outcome measurement candidate; trigger zone to review: replay-accepted shelf/reclaim trigger only, likely around `274.38`, `278.22`, or `279.81` depending on row-by-row review; candle/timeframe rule: copied from accepted replay trigger; invalidation area: copied from accepted replay; fresh/stale/spent question: copied from replay; blocker/caution questions: chart-only outcome must not be computed before replay acceptance. | Accepted replay signal row, final trigger, final invalidation, chart-only calculation rule inputs, final setup proof. | READY FOR WORKSHEET AS OUTCOME CANDIDATE; BLOCKED FOR OUTCOME until replay passes. | No chart outcome calculated in this task. |

## Window Selection Result

PASS. Enough bounded candidate windows were selected from the validated IWM source CSV to begin the first IWM replay/review asset preparation path. All labels remain CANDIDATE / NEEDS REVIEW until later row-by-row fixture/replay design confirms setup identity, stage, trigger, invalidation, blockers, cautions, and replay readiness.

## Worksheet Population Decision

`SAFE_FAST_IWM_HISTORICAL_SAMPLE_COLLECTION_WORKSHEET.md` can now be populated from the selected bounded windows.

Worksheet population is not performed in this task. The next task is to populate the IWM historical sample collection worksheet from bounded source-window selection.

## Next Task

Populate IWM historical sample collection worksheet from bounded source-window selection.

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

## What Remains Unproven

- IWM worksheet population
- IWM real historical replay assets
- IWM fixture creation/execution
- IWM chart-only outcomes
- IWM aggregate closeout
- GLD broader coverage
- Continuous Watcher behavior
- alert suppression
- shadow/live validation
- option P&L
- account sizing
- production readiness
