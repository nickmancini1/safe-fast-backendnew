# SAFE-FAST IWM/GLD Replacement Source Collection Worksheet

Project day: Day 36 working day
Repo baseline: patch8
Latest committed baseline before this worksheet: 039a7b1 Add IWM GLD new bounded source collection plan
Mode: build-only; not live trade chat

## Purpose

This docs-only worksheet starts the replacement source collection path for cleaner IWM Continuation and GLD Ideal candidates.

The current repo does not provide accepted setup-time proof for the existing IWM Continuation 001 or GLD Ideal 001 candidates.

This worksheet does not invent evidence, does not fake proof, does not use hindsight filling, and does not authorize live data, alerts, broker/order/account/options/P&L, account sizing, Railway, production, or live trade decisions.

## Required candidate IDs

- IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001
- IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002
- GLD-REPLACEMENT-IDEAL-CANDIDATE-001
- GLD-REPLACEMENT-IDEAL-CANDIDATE-002

## Collection status

Current status: source collection required.

The worksheet confirms the required candidate slots, acceptance fields, and no-hindsight intake requirements. It does not mark any replacement candidate accepted yet.

## Candidate intake table

| Candidate ID | Symbol | Setup type | Exact date/window | Setup-time row | Trigger candidate | Invalidation candidate | Freshness/final-signal | Blocker/caution status | Source status | Current decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001 | IWM | Continuation | TO COLLECT | MISSING | MISSING | MISSING | MISSING | MISSING | SOURCE NEEDED | missing-evidence/inconclusive |
| IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002 | IWM | Continuation | TO COLLECT | MISSING | MISSING | MISSING | MISSING | MISSING | SOURCE NEEDED | missing-evidence/inconclusive |
| GLD-REPLACEMENT-IDEAL-CANDIDATE-001 | GLD | Ideal | TO COLLECT | MISSING | MISSING | MISSING | MISSING | MISSING | SOURCE NEEDED | missing-evidence/inconclusive |
| GLD-REPLACEMENT-IDEAL-CANDIDATE-002 | GLD | Ideal | TO COLLECT | MISSING | MISSING | MISSING | MISSING | MISSING | SOURCE NEEDED | missing-evidence/inconclusive |

## Acceptance gate

A replacement candidate may proceed to acceptance review only if it has setup-time evidence for:

- exact setup-time signal timestamp
- accepted setup identity or rejected setup identity
- accepted final verdict or rejected verdict
- accepted trigger state
- accepted numeric trigger
- accepted trigger basis
- accepted numeric invalidation
- accepted invalidation basis
- accepted freshness/final-signal decision
- accepted blocker/caution decision
- unavailable fields explicitly named

## No-hindsight rule

The setup-time row must be selected before terminal outcome is reviewed.

After-setup movement cannot be used to choose the setup-time signal row.

If a candidate cannot provide setup-time evidence without hindsight, it stays missing-evidence/inconclusive.

## Current source review result

Existing repo source trails point back to known candidate/review material for IWM Continuation and GLD Ideal.

Those trails were already reviewed and found blocked at setup-time acceptance.

This worksheet therefore does not reuse IWM Continuation 001 or GLD Ideal 001 as replacement accepted candidates.

## Required source collection task

The next build step must collect or provide bounded source rows for the four replacement candidate IDs.

Each source row packet must include:

- source file or export reference
- symbol
- setup type
- date
- timeframe
- source window start
- source window end
- setup-time candidate row
- trigger candidate
- invalidation candidate
- freshness/final-signal candidate
- blocker/caution status
- unavailable context fields
- after-setup outcome window start and end, only for later use after setup-time evidence is frozen

## Smallest next evidence-backed fix

Create `SAFE_FAST_IWM_GLD_REPLACEMENT_SOURCE_ROW_REQUEST.md`.

That file must specify exactly what source rows or local exports are needed to populate the four replacement candidate slots.

It must not fetch live data.

It must not use broker data.

It must not create generated reports.

It must be a local source request / collection instruction only.

## Tests

Tests not run. Docs-only source collection worksheet.

Required validation:

- git diff --check
- clean post-commit status

## No-go boundaries preserved

- no main.py
- no engine logic
- no replay code
- no live data
- no watcher loops
- no alerts
- no broker/order/account/options/P&L
- no account sizing
- no Railway/deploy/production
- no generated reports/logs
- no live trade decisions

## Existing IWM source leads

- SAFE_FAST_ALL_SYMBOL_CURRENT_DEPTH_CLOSEOUT_REVIEW.md:48:| IWM / Continuation | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PARTIAL | PASS | PASS |
- SAFE_FAST_BROADER_CHART_OUTCOME_BACKTESTING_COVERAGE_PLAN.md:160:- QQQ, IWM, and GLD each have validated real historical replay coverage for Ideal, Clean Fast Break, and Continuation
- SAFE_FAST_BUILD_STATE.md:92:- A failure must be diagnosed by setup type and symbol, such as IWM Continuation, GLD Ideal, QQQ Clean Fast Break, or SPY Ideal.
- SAFE_FAST_BUILD_STATE.md:150:Ideal, Clean Fast Break, Continuation, SPY, QQQ, IWM, and GLD must each earn their place.
- SAFE_FAST_BUILD_STATE.md:271:Answer: Return to the docs-only IWM/GLD missing-evidence inventory. Determine whether accepted evidence already exists for IWM Continuation and GLD Ideal. If it does not exist, keep them missing-evidence/inconclusive and name the smallest evidence-backed fix.
- SAFE_FAST_BUILD_STATE.md:348:## Day 36 IWM Continuation 001 evidence packet review status
- SAFE_FAST_BUILD_STATE.md:352:- Result: IWM Continuation 001 remains missing-evidence/inconclusive.
- SAFE_FAST_BUILD_STATE.md:354:- Smallest next evidence-backed fix: create a bounded IWM Continuation accepted-signal-row review that decides whether an accepted signal timestamp, trigger, invalidation, freshness/final-signal, blocker/caution status, and terminal outcome can be accepted without hindsight.
- SAFE_FAST_BUILD_STATE.md:359:- Latest committed baseline before this status: df3fa06 Add IWM Continuation accepted signal row review.
- SAFE_FAST_BUILD_STATE.md:364:- Combined Day 36 evidence result: IWM Continuation 001 and GLD Ideal 001 both remain missing-evidence/inconclusive because neither has an accepted setup-time signal row.
- SAFE_FAST_BUILD_STATE.md:365:- Smallest next evidence-backed fix: choose the clearest bounded trigger/invalidation/freshness acceptance review between IWM Continuation and GLD Ideal; do not promote either setup unless accepted setup-time proof exists.
- SAFE_FAST_BUILD_STATE.md:386:- Smallest next evidence-backed fix: run IWM Continuation trigger / invalidation / freshness acceptance review.
- SAFE_FAST_BUILD_STATE.md:390:## Day 36 IWM Continuation 001 trigger / invalidation / freshness acceptance review status
- SAFE_FAST_BUILD_STATE.md:394:- Result: IWM Continuation 001 cannot accept trigger / invalidation / freshness proof from current repo evidence.
- SAFE_FAST_BUILD_STATE.md:395:- Status: IWM Continuation 001 remains missing-evidence/inconclusive.
- SAFE_FAST_BUILD_STATE.md:397:- Combined Day 36 evidence result: IWM Continuation 001 and GLD Ideal 001 both remain missing-evidence/inconclusive because neither has accepted setup-time proof.
- SAFE_FAST_BUILD_STATE.md:398:- Smallest next evidence-backed fix: stop trying to promote these two candidate examples unless explicitly requested; create a bounded real historical replacement-candidate selection review for a cleaner IWM Continuation or GLD Ideal example with complete setup-time fields.
- SAFE_FAST_BUILD_STATE.md:403:- Latest committed baseline before this status: c80bd9e Add IWM Continuation trigger invalidation freshness acceptance review.
- SAFE_FAST_BUILD_STATE.md:405:- Result: stop trying to promote the current IWM Continuation 001 and GLD Ideal 001 candidates unless explicitly requested later.
- SAFE_FAST_BUILD_STATE.md:421:## Day 36 IWM Continuation replacement candidate source selection worksheet status
- SAFE_FAST_BUILD_STATE.md:425:- Result: no acceptable IWM Continuation replacement candidate is accepted from current repo sources.
- SAFE_FAST_BUILD_STATE.md:426:- Combined Day 36 result: GLD Ideal replacement search is blocked and IWM Continuation replacement search is blocked.
- SAFE_FAST_BUILD_STATE.md:433:- Latest committed baseline before this status: d233511 Add IWM Continuation replacement candidate source selection worksheet.
- SAFE_FAST_BUILD_STATE.md:435:- Result: both current IWM Continuation and GLD Ideal replacement paths are blocked in current repo sources.
- SAFE_FAST_BUILD_STATE.md:437:- Purpose of next worksheet: collect cleaner bounded real historical candidates for IWM Continuation and GLD Ideal with complete setup-time fields.
- SAFE_FAST_BUILD_STATE.md:498:- **Latest completed build milestone:** Historical setup proof review bundle builder is complete and committed at `0dbae56 Add historical setup proof review bundle builder`; Day 33 project handoff and tier runway preservation is committed at `599d45f Add Day 33 project handoff and tier runway`; historical proof bundle readiness planning is committed at `bf431c2 Add historical proof bundle readiness plan`; historical proof bundle readiness gate is complete and committed at `7af3506 Add historical proof bundle readiness gate`; historical setup sample path planning is committed at `73a27ba Add historical setup sample path plan`; historical setup sample path runner is complete and committed at `6973581 Add historical setup sample path runner`; first controlled historical sample evidence set is complete and committed at `2ccc021 Add first controlled historical sample evidence set`; controlled sample review planning is committed at `c880103 Add controlled sample review plan`; controlled historical sample output review is complete and committed at `ba7374b Add controlled historical sample output review`; GLD Continuation evidence fix planning is complete and committed at `c228cb1 Add GLD Continuation evidence fix plan`; GLD Continuation after-setup evidence implementation is complete and committed at `eb6e5d0 Add GLD Continuation after-setup evidence`; IWM controlled sample expansion planning is complete and committed at `46b1e27 Add IWM controlled sample expansion plan`; IWM controlled sample evidence is complete and committed at `7cc424c Add IWM controlled sample evidence`; controlled sample coverage review planning is complete and committed at `d8ab7aa Add controlled sample coverage review plan`; Day 34 handoff timeline and evidence checkpoint is complete and committed at `7181645 Update Day 34 handoff timeline and evidence checkpoint`; controlled sample coverage review is complete and committed at `ca8b6a4 Add controlled sample coverage review`; controlled sample missing-evidence implementation planning is complete and committed at `ad21b40 Add controlled sample missing evidence plan`; controlled missing-evidence sample is complete and committed at `8527eff Add controlled missing-evidence sample`; controlled sample coverage review update is complete and committed at `bfad6d3 Update controlled sample coverage review`; first real historical example batch planning is complete and committed at `35b91bf Add first real historical example batch plan`; first real historical example batch implementation is complete and committed at `ba44d07 Add first real historical example batch`.
- SAFE_FAST_BUILD_STATE.md:507:- **Smallest next evidence-backed fix after this docs batch:** create or accept bounded real historical evidence packets for IWM Continuation and GLD Ideal first, because both remain missing-evidence/inconclusive; bounded 1H/24H support-resistance and room-classification design/test planning is only a later candidate if explicitly requested.
- SAFE_FAST_BUILD_STATE.md:671:- **Plain purpose:** preserve the existing worked `Ideal` / `SPY`, failed `Clean Fast Break` / `QQQ`, and worked/reviewable `Continuation` / `GLD` examples; add exactly one controlled `IWM` example; keep setup type, symbol, setup-type-plus-symbol pair, and no-hindsight separation; rerun the sample path and output review; report whether IWM becomes reviewable; report what the new sample teaches; and avoid profitability, historical success, final viability, live readiness, or production readiness claims.
- SAFE_FAST_BUILD_STATE.md:688:- **Implementation summary:** preserved the existing worked `Ideal` / `SPY` sample, failed `Clean Fast Break` / `QQQ` sample, and worked/reviewable `Continuation` / `GLD` sample; added exactly one controlled `Ideal` / `IWM` sample with setup-time evidence refs, after-setup evidence starting after detection, `source_row_reference`, `post_setup_evidence`, and `future_evidence_used_to_define_setup: False`; kept setup type, symbol, setup-type-plus-symbol pair, setup-time/after-setup, and no-hindsight separation; added output-review fields for IWM review status and what the IWM sample teaches.
- SAFE_FAST_BUILD_STATE.md:716:- **Known controlled sample coverage before future review:** represented symbols are SPY, QQQ, GLD, and IWM; represented setup types are Ideal, Clean Fast Break, and Continuation; represented pairs are `Ideal` / `SPY`, `Clean Fast Break` / `QQQ`, `Continuation` / `GLD`, and `Ideal` / `IWM`. The future review must verify this from actual controlled sample output.
- SAFE_FAST_BUILD_STATE.md:735:- **Coverage result:** represented symbols are `GLD`, `IWM`, `QQQ`, and `SPY`; represented setup types are `Clean Fast Break`, `Continuation`, and `Ideal`; represented pairs are `Ideal` / `SPY`, `Clean Fast Break` / `QQQ`, `Continuation` / `GLD`, and `Ideal` / `IWM`; missing pairs are `Clean Fast Break` / `SPY`, `Continuation` / `SPY`, `Ideal` / `QQQ`, `Continuation` / `QQQ`, `Clean Fast Break` / `IWM`, `Continuation` / `IWM`, `Ideal` / `GLD`, and `Clean Fast Break` / `GLD`.
- SAFE_FAST_BUILD_STATE.md:736:- **Outcome coverage result:** worked chart/setup behavior is represented by `Ideal` / `SPY`, `Continuation` / `GLD`, and `Ideal` / `IWM`; failed chart/setup behavior is represented by `Clean Fast Break` / `QQQ`; active inconclusive/missing-evidence coverage is not represented in the final four-sample controlled set.
- SAFE_FAST_BUILD_STATE.md:772:- **Implementation summary:** preserved the existing `Ideal` / `SPY` worked sample, `Clean Fast Break` / `QQQ` failed sample, `Continuation` / `GLD` worked/reviewable sample, and `Ideal` / `IWM` worked/reviewable sample; added exactly one explicit controlled missing-evidence sample as `Continuation` / `QQQ`. The new sample has setup-time candle/shelf evidence but deliberately omits after-setup `source_row_reference` and `post_setup_evidence`, keeps `future_evidence_used_to_define_setup=False`, remains local-only/in-memory, and is surfaced by the review as missing-evidence coverage instead of worked/failed proof.
- SAFE_FAST_BUILD_STATE.md:774:- **Output review rerun result:** worked samples `3`, failed samples `1`, inconclusive/missing-evidence samples `1`; represented symbols remain `SPY`, `IWM`, `QQQ`, and `GLD`; represented setup types remain `Ideal`, `Clean Fast Break`, and `Continuation`; represented pairs are `Ideal` / `SPY`, `Ideal` / `IWM`, `Clean Fast Break` / `QQQ`, `Continuation` / `GLD`, and `Continuation` / `QQQ`.
- SAFE_FAST_BUILD_STATE.md:793:- **Review conclusion:** controlled sample phase is complete enough to plan real historical examples, because `SPY`, `QQQ`, `IWM`, and `GLD` are represented; `Ideal`, `Clean Fast Break`, and `Continuation` are represented; worked, failed, and missing-evidence examples are represented; no-hindsight separation held; and setup type, symbol, and setup-type-plus-symbol pair separation held.
- SAFE_FAST_BUILD_STATE.md:808:- **First real historical batch definition:** exactly 4 real historical examples, one each for `SPY`, `QQQ`, `IWM`, and `GLD`; all three setup types represented; required first pairs are `Ideal` / `SPY`, `Clean Fast Break` / `QQQ`, `Continuation` / `IWM`, and `Ideal` / `GLD`.
- SAFE_FAST_BUILD_STATE.md:829:- **Implementation summary:** added `build_first_real_historical_example_batch()` and `FIRST_REAL_HISTORICAL_EXAMPLE_BATCH_ID` in the historical sample path module. The builder returns exactly four in-memory real historical examples: `Ideal` / `SPY`, `Clean Fast Break` / `QQQ`, `Continuation` / `IWM`, and `Ideal` / `GLD`. It uses source-backed fixture/report/review references, rejects controlled IDs/refs by test, keeps setup-time evidence separate from after-setup evidence, and preserves no-hindsight boundaries.
- SAFE_FAST_BUILD_STATE.md:830:- **Proof-chain run summary:** `records_processed=4`; `records_accepted=4`; `records_rejected=0`; represented symbols are `SPY`, `QQQ`, `IWM`, and `GLD`; represented setup types are `Ideal`, `Clean Fast Break`, and `Continuation`; represented pairs are `Ideal` / `SPY`, `Clean Fast Break` / `QQQ`, `Continuation` / `IWM`, and `Ideal` / `GLD`; outcome group counts are worked `2`, failed `0`, inconclusive `0`, pending `0`, stale `0`, invalidated `0`, missing evidence `2`.
- SAFE_FAST_BUILD_STATE.md:831:- **Outcome interpretation:** SPY Ideal and QQQ Clean Fast Break are source-backed worked chart/setup behavior examples. IWM Continuation and GLD Ideal are source-backed real candidate examples but remain missing-evidence/inconclusive because repo evidence does not prove accepted numeric trigger, numeric invalidation, and freshness/final signal fields. This is not a profitability, final viability, actual historical success, optimization, production readiness, live readiness, or live trade claim.
- SAFE_FAST_BUILD_STATE.md:838:- **Unfinished items:** final trading-plan viability, profitability, actual historical success, all 12 setup-type-plus-symbol pairs, failed real historical examples, repeated worked/failed patterns, repeated fix paths, lower-tier final readiness, controlled shadow readiness, live readiness, production readiness, Railway readiness, and live trade decision readiness remain unproven. IWM Continuation and GLD Ideal still require accepted trigger/invalidation/freshness evidence before they can be classified as worked or failed proof.
- SAFE_FAST_BUILD_STATE.md:852:- **Plan summary:** inspect existing repo evidence for IWM Continuation and GLD Ideal before any code change. The plan names exact missing accepted evidence: final accepted signal row, accepted triggered state, no primary blocker, numeric trigger, trigger basis, numeric invalidation, invalidation basis, freshness/final signal fields, blocker/caution priority, terminal outcome inputs, and chart risk denominator as applicable by setup.
- SAFE_FAST_BUILD_STATE.md:853:- **IWM Continuation evidence status:** repo contains source-backed candidate and post-candidate movement evidence, but the fixture/review keep the candidate as `PENDING`, `completed_shelf_break_candidate_TO_REVIEW`, `trigger_level_TO_REVIEW`, null trigger, null invalidation, fresh/spent `TO_REVIEW`, and related fields unconfirmed. This is not accepted worked/failed proof.
- SAFE_FAST_BUILD_STATE.md:857:- **Future inventory required answers:** what exact evidence is missing for IWM Continuation; what exact evidence is missing for GLD Ideal; whether accepted trigger evidence exists; whether accepted invalidation evidence exists; whether accepted freshness/final-signal evidence exists; whether accepted blocker evidence exists; whether accepted terminal outcome evidence exists; where evidence exists, if it exists; if evidence does not exist, keep the examples missing-evidence/inconclusive; smallest next evidence-backed fix.
- SAFE_FAST_BUILD_STATE.md:859:- **Future implementation gate:** do not change the historical sample path builder or tests for IWM/GLD until the inventory names exact accepted evidence fields and exact source references. If no accepted evidence exists, IWM Continuation and GLD Ideal must stay missing-evidence/inconclusive.
- SAFE_FAST_BUILD_STATE.md:5650:- **Core product function:** monitor SPY / QQQ / IWM / GLD for forming Ideal / Clean Fast Break / Continuation setups with trigger-card alerts
- SAFE_FAST_BUILD_STATE.md:5897:  - `IWM-WINDOW-CONTINUATION-001`
- SAFE_FAST_BUILD_STATE.md:5898:  - `IWM-WINDOW-STAGE-DEVELOPING-001`
- SAFE_FAST_BUILD_STATE.md:5899:  - `IWM-WINDOW-SESSION-BOUNDARY-001`
- SAFE_FAST_BUILD_STATE.md:5900:  - `IWM-WINDOW-WINNER-SELECTION-001`
- SAFE_FAST_BUILD_STATE.md:5928:  - `IWM-SAMPLE-CONTINUATION-001` from `IWM-WINDOW-CONTINUATION-001`
- SAFE_FAST_BUILD_STATE.md:5929:  - `IWM-SAMPLE-STAGE-DEVELOPING-001` from `IWM-WINDOW-STAGE-DEVELOPING-001`
- SAFE_FAST_BUILD_STATE.md:5930:  - `IWM-SAMPLE-SESSION-BOUNDARY-001` from `IWM-WINDOW-SESSION-BOUNDARY-001`
- SAFE_FAST_BUILD_STATE.md:5931:  - `IWM-SAMPLE-WINNER-SELECTION-001` from `IWM-WINDOW-WINNER-SELECTION-001`
- SAFE_FAST_BUILD_STATE.md:6190:- **Next task:** create IWM Continuation 001 replay readiness review
- SAFE_FAST_BUILD_STATE.md:6200:## IWM Sample Continuation 001 replay readiness review status
- SAFE_FAST_BUILD_STATE.md:6204:- **Sample ID:** `IWM-SAMPLE-CONTINUATION-001`
- SAFE_FAST_BUILD_STATE.md:6205:- **Window ID:** `IWM-WINDOW-CONTINUATION-001`
- SAFE_FAST_BUILD_STATE.md:6213:- **Next task:** create IWM Continuation 001 real historical replay review asset
- SAFE_FAST_BUILD_STATE.md:6226:## IWM Continuation 001 real historical replay review status
- SAFE_FAST_BUILD_STATE.md:6230:- **Sample ID:** `IWM-SAMPLE-CONTINUATION-001`
- SAFE_FAST_BUILD_STATE.md:6231:- **Window ID:** `IWM-WINDOW-CONTINUATION-001`
- SAFE_FAST_BUILD_STATE.md:6240:- **Next task:** create IWM Continuation 001 replay fixture specification review
- SAFE_FAST_BUILD_STATE.md:6253:## IWM Continuation 001 replay fixture specification review status
- SAFE_FAST_BUILD_STATE.md:6257:- **Sample ID:** `IWM-SAMPLE-CONTINUATION-001`
- SAFE_FAST_BUILD_STATE.md:6258:- **Window ID:** `IWM-WINDOW-CONTINUATION-001`
- SAFE_FAST_BUILD_STATE.md:6266:- **Next task:** create IWM Continuation 001 replay fixture JSON asset
- SAFE_FAST_BUILD_STATE.md:6279:## IWM Continuation 001 replay fixture JSON asset status
- SAFE_FAST_BUILD_STATE.md:6283:- **Sample ID:** `IWM-SAMPLE-CONTINUATION-001`
- SAFE_FAST_BUILD_STATE.md:6284:- **Window ID:** `IWM-WINDOW-CONTINUATION-001`
- SAFE_FAST_BUILD_STATE.md:6294:- **Next task:** validate IWM Continuation 001 replay fixture output
- SAFE_FAST_BUILD_STATE.md:6304:## IWM Continuation 001 replay fixture output validation status
- SAFE_FAST_BUILD_STATE.md:6309:- **Sample ID:** `IWM-SAMPLE-CONTINUATION-001`
- SAFE_FAST_BUILD_STATE.md:6310:- **Window ID:** `IWM-WINDOW-CONTINUATION-001`
- SAFE_FAST_BUILD_STATE.md:6334:- **IWM chart outcome inputs ready:** Ideal / Clean Fast Break / Continuation fixture output validations are PASS.
- SAFE_FAST_BUILD_STATE.md:6385:- **Next task:** create IWM Continuation 001 chart-only outcome review/calculation
- SAFE_FAST_BUILD_STATE.md:6398:## IWM Continuation 001 chart-only outcome review status
- SAFE_FAST_BUILD_STATE.md:6404:- **Sample ID:** `IWM-SAMPLE-CONTINUATION-001`
- SAFE_FAST_BUILD_STATE.md:6405:- **Window ID:** `IWM-WINDOW-CONTINUATION-001`
- SAFE_FAST_BUILD_STATE.md:6451:- **IWM replay fixture output validation coverage:** Ideal / Clean Fast Break / Continuation
- SAFE_FAST_BUILD_STATE.md:6452:- **IWM chart-only outcome coverage:** Ideal / Clean Fast Break / Continuation
- SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_CALCULATION_RULES_PLAN.md:194:- SPY has real replay signal coverage for Continuation, Ideal, and Clean Fast Break; QQQ, IWM, and GLD do not yet have equivalent local real replay closeout evidence.
- SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_RUNNER_SCAFFOLD_PLAN.md:40:Allowed symbol universe remains `SPY`, `QQQ`, `IWM`, and `GLD`, but the first scaffold should run only the existing SPY Continuation sample fixture. Allowed setup families remain `Ideal`, `Clean Fast Break`, and `Continuation`, but the first scaffold should not manufacture new candidates.
- SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_SCHEMA_DESIGN.md:74:The allowed v1 symbols are `SPY`, `QQQ`, `IWM`, and `GLD`. The allowed setup families are `Ideal`, `Clean Fast Break`, and `Continuation`.
- SAFE_FAST_CONTINUOUS_WATCHER_FOUNDATION_SHADOW_ARCHITECTURE_PLAN.md:26:The watcher target is a shadow/watch-only SAFE-FAST lifecycle monitor for SPY, QQQ, IWM, and GLD. It should track forming and changing Ideal, Clean Fast Break, and Continuation setups, produce trigger-card outputs, preserve stale/spent/no-fresh-trigger discipline, suppress duplicate same-state alerts, focus attention on the best current candidate, and create review artifacts for later shadow accuracy review.
- SAFE_FAST_CONTROLLED_SAMPLE_COVERAGE_REVIEW.md:74:- `Continuation` / `IWM`.
- SAFE_FAST_CONTROLLED_SAMPLE_COVERAGE_REVIEW.md:80:Worked chart/setup behavior is represented by `Ideal` / `SPY`, `Continuation` / `GLD`, and `Ideal` / `IWM`.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:92:- A failure must be diagnosed by setup type and symbol, such as IWM Continuation, GLD Ideal, QQQ Clean Fast Break, or SPY Ideal.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:150:Ideal, Clean Fast Break, Continuation, SPY, QQQ, IWM, and GLD must each earn their place.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:271:Answer: Return to the docs-only IWM/GLD missing-evidence inventory. Determine whether accepted evidence already exists for IWM Continuation and GLD Ideal. If it does not exist, keep them missing-evidence/inconclusive and name the smallest evidence-backed fix.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:338:## Day 36 IWM Continuation 001 evidence packet review status
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:342:- Result: IWM Continuation 001 remains missing-evidence/inconclusive.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:344:- Smallest next evidence-backed fix: create a bounded IWM Continuation accepted-signal-row review that decides whether an accepted signal timestamp, trigger, invalidation, freshness/final-signal, blocker/caution status, and terminal outcome can be accepted without hindsight.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:349:- Latest committed baseline before this status: df3fa06 Add IWM Continuation accepted signal row review.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:354:- Combined Day 36 evidence result: IWM Continuation 001 and GLD Ideal 001 both remain missing-evidence/inconclusive because neither has an accepted setup-time signal row.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:355:- Smallest next evidence-backed fix: choose the clearest bounded trigger/invalidation/freshness acceptance review between IWM Continuation and GLD Ideal; do not promote either setup unless accepted setup-time proof exists.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:376:- Smallest next evidence-backed fix: run IWM Continuation trigger / invalidation / freshness acceptance review.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:380:## Day 36 IWM Continuation 001 trigger / invalidation / freshness acceptance review status
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:384:- Result: IWM Continuation 001 cannot accept trigger / invalidation / freshness proof from current repo evidence.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:385:- Status: IWM Continuation 001 remains missing-evidence/inconclusive.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:387:- Combined Day 36 evidence result: IWM Continuation 001 and GLD Ideal 001 both remain missing-evidence/inconclusive because neither has accepted setup-time proof.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:388:- Smallest next evidence-backed fix: stop trying to promote these two candidate examples unless explicitly requested; create a bounded real historical replacement-candidate selection review for a cleaner IWM Continuation or GLD Ideal example with complete setup-time fields.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:393:- Latest committed baseline before this status: c80bd9e Add IWM Continuation trigger invalidation freshness acceptance review.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:395:- Result: stop trying to promote the current IWM Continuation 001 and GLD Ideal 001 candidates unless explicitly requested later.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:411:## Day 36 IWM Continuation replacement candidate source selection worksheet status
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:415:- Result: no acceptable IWM Continuation replacement candidate is accepted from current repo sources.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:416:- Combined Day 36 result: GLD Ideal replacement search is blocked and IWM Continuation replacement search is blocked.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:423:- Latest committed baseline before this status: d233511 Add IWM Continuation replacement candidate source selection worksheet.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:425:- Result: both current IWM Continuation and GLD Ideal replacement paths are blocked in current repo sources.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:427:- Purpose of next worksheet: collect cleaner bounded real historical candidates for IWM Continuation and GLD Ideal with complete setup-time fields.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:819:- Historical objective for that completed plan-correction block was creating the docs-only next-step plan after the first real historical example batch, focused on IWM Continuation and GLD Ideal missing accepted evidence.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:822:- Sample evidence set behavior: exposes one worked `Ideal` / `SPY` setup, one failed `Clean Fast Break` / `QQQ` setup, one reviewable `Continuation` / `GLD` setup, one reviewable `Ideal` / `IWM` setup, and exactly one explicit controlled missing-evidence `Continuation` / `QQQ` setup through the existing runner; preserves setup type separation, symbol separation, setup-type-plus-symbol pair separation, setup-time versus after-setup evidence separation, diagnostics, fix paths, lower-tier summary, no-trade/watch-only, no-live-data, no-controlled-shadow, no-alert, no-broker, no-file-write, no-rule-change, and no-optimization boundaries.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:823:- Review behavior: accepts caller-provided in-memory sample path output only, returns one in-memory review summary only, keeps worked, failed, and inconclusive samples separate, keeps setup type and symbol separate, checks no-hindsight boundaries, surfaces useful proof, weak proof, missing evidence, next fix paths, regression needs, lower-tier review material, explicitly reports the GLD Continuation review status and IWM review status / teaching, and defensively copies returned data.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:824:- Review result: the controlled output is useful but not final viability proof. The worked `Ideal` / `SPY` sample gives clear chart-behavior proof; the failed `Clean Fast Break` / `QQQ` sample gives useful diagnosis; the existing `Continuation` / `GLD` sample remains reviewable; the `Ideal` / `IWM` sample remains reviewable; the new `Continuation` / `QQQ` sample provides active missing-evidence coverage. Bundle readiness still shows tiny-sample/upstream review contract gaps and must not be treated as final lower-tier readiness.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:827:- Controlled sample implementation result: represented symbols are `GLD`, `IWM`, `QQQ`, and `SPY`; represented setup types are `Clean Fast Break`, `Continuation`, and `Ideal`; represented pairs are `Ideal` / `SPY`, `Clean Fast Break` / `QQQ`, `Continuation` / `GLD`, `Ideal` / `IWM`, and `Continuation` / `QQQ`.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:836:- Current coverage review conclusion: the controlled sample phase is complete enough to plan real historical examples. `SPY`, `QQQ`, `IWM`, and `GLD` are represented; `Ideal`, `Clean Fast Break`, and `Continuation` are represented; worked, failed, and missing-evidence examples are represented; no-hindsight separation held; setup type and symbol separation held.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:837:- Current plan summary: first batch should contain exactly 4 real historical examples, one each for `SPY`, `QQQ`, `IWM`, and `GLD`; all three setup types must be represented; required pairs are `Ideal` / `SPY`, `Clean Fast Break` / `QQQ`, `Continuation` / `IWM`, and `Ideal` / `GLD`.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:843:- Implementation result: `build_first_real_historical_example_batch()` returns exactly 4 local in-memory real historical examples: `Ideal` / `SPY`, `Clean Fast Break` / `QQQ`, `Continuation` / `IWM`, and `Ideal` / `GLD`.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:844:- Proof-chain run result: `records_processed=4`, `records_accepted=4`, `records_rejected=0`; represented symbols are `SPY`, `QQQ`, `IWM`, and `GLD`; represented setup types are `Ideal`, `Clean Fast Break`, and `Continuation`; represented pairs are `Ideal` / `SPY`, `Clean Fast Break` / `QQQ`, `Continuation` / `IWM`, and `Ideal` / `GLD`.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:846:- Interpretation: SPY Ideal and QQQ Clean Fast Break are source-backed worked chart/setup behavior examples. IWM Continuation and GLD Ideal are source-backed real candidate examples but remain missing-evidence/inconclusive because repo evidence does not prove accepted numeric trigger, numeric invalidation, and freshness/final signal fields.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:854:- Current plan summary: inspect existing repo evidence for IWM Continuation and GLD Ideal before any code change. The plan names the exact missing accepted evidence: accepted final signal row, accepted triggered state, no primary blocker, numeric trigger, trigger basis, numeric invalidation, invalidation basis, freshness/final signal fields, blocker/caution priority, terminal outcome inputs, and chart risk denominator as applicable by setup.

## Existing GLD source leads

- SAFE_FAST_ALL_SYMBOL_CURRENT_DEPTH_CLOSEOUT_REVIEW.md:49:| GLD / Ideal | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PARTIAL | PASS | PASS |
- SAFE_FAST_BROADER_CHART_OUTCOME_BACKTESTING_COVERAGE_PLAN.md:160:- QQQ, IWM, and GLD each have validated real historical replay coverage for Ideal, Clean Fast Break, and Continuation
- SAFE_FAST_BUILD_STATE.md:92:- A failure must be diagnosed by setup type and symbol, such as IWM Continuation, GLD Ideal, QQQ Clean Fast Break, or SPY Ideal.
- SAFE_FAST_BUILD_STATE.md:150:Ideal, Clean Fast Break, Continuation, SPY, QQQ, IWM, and GLD must each earn their place.
- SAFE_FAST_BUILD_STATE.md:271:Answer: Return to the docs-only IWM/GLD missing-evidence inventory. Determine whether accepted evidence already exists for IWM Continuation and GLD Ideal. If it does not exist, keep them missing-evidence/inconclusive and name the smallest evidence-backed fix.
- SAFE_FAST_BUILD_STATE.md:357:## Day 36 GLD Ideal 001 accepted signal row review status
- SAFE_FAST_BUILD_STATE.md:361:- Result: GLD Ideal 001 does not have an accepted setup-time signal row.
- SAFE_FAST_BUILD_STATE.md:362:- Status: GLD Ideal 001 remains missing-evidence/inconclusive.
- SAFE_FAST_BUILD_STATE.md:364:- Combined Day 36 evidence result: IWM Continuation 001 and GLD Ideal 001 both remain missing-evidence/inconclusive because neither has an accepted setup-time signal row.
- SAFE_FAST_BUILD_STATE.md:365:- Smallest next evidence-backed fix: choose the clearest bounded trigger/invalidation/freshness acceptance review between IWM Continuation and GLD Ideal; do not promote either setup unless accepted setup-time proof exists.
- SAFE_FAST_BUILD_STATE.md:368:## Day 36 GLD Ideal 001 trigger / invalidation / freshness acceptance review status
- SAFE_FAST_BUILD_STATE.md:370:- Latest committed baseline before this status: 8044901 Add GLD Ideal accepted signal row review.
- SAFE_FAST_BUILD_STATE.md:372:- Result: GLD Ideal 001 cannot accept trigger / invalidation / freshness proof from current repo evidence.
- SAFE_FAST_BUILD_STATE.md:373:- Status: GLD Ideal 001 remains missing-evidence/inconclusive.
- SAFE_FAST_BUILD_STATE.md:375:- Smallest next GLD-specific fix: create a bounded GLD Ideal setup-time row acceptance worksheet.
- SAFE_FAST_BUILD_STATE.md:376:- Project-level next move: use GLD Ideal as the next worksheet candidate unless local source review proves IWM has clearer accepted setup-time rows.
- SAFE_FAST_BUILD_STATE.md:379:## Day 36 GLD Ideal 001 setup-time row acceptance worksheet status
- SAFE_FAST_BUILD_STATE.md:381:- Latest committed baseline before this status: ff0f56d Add GLD Ideal trigger invalidation freshness acceptance review.
- SAFE_FAST_BUILD_STATE.md:383:- Result: GLD Ideal 001 cannot accept one setup-time row from current repo evidence.
- SAFE_FAST_BUILD_STATE.md:384:- Status: GLD Ideal 001 remains missing-evidence/inconclusive.
- SAFE_FAST_BUILD_STATE.md:392:- Latest committed baseline before this status: add70a4 Add GLD Ideal setup time row acceptance worksheet.
- SAFE_FAST_BUILD_STATE.md:397:- Combined Day 36 evidence result: IWM Continuation 001 and GLD Ideal 001 both remain missing-evidence/inconclusive because neither has accepted setup-time proof.
- SAFE_FAST_BUILD_STATE.md:398:- Smallest next evidence-backed fix: stop trying to promote these two candidate examples unless explicitly requested; create a bounded real historical replacement-candidate selection review for a cleaner IWM Continuation or GLD Ideal example with complete setup-time fields.
- SAFE_FAST_BUILD_STATE.md:405:- Result: stop trying to promote the current IWM Continuation 001 and GLD Ideal 001 candidates unless explicitly requested later.
- SAFE_FAST_BUILD_STATE.md:408:- Target: find a cleaner GLD Ideal replacement candidate from existing repo sources only, or prove no acceptable GLD Ideal replacement candidate exists in current repo sources.
- SAFE_FAST_BUILD_STATE.md:411:## Day 36 GLD Ideal replacement candidate source selection worksheet status
- SAFE_FAST_BUILD_STATE.md:415:- Result: no acceptable GLD Ideal replacement candidate is accepted from current repo sources.
- SAFE_FAST_BUILD_STATE.md:416:- Status: GLD Ideal remains blocked for the current Day 36 missing-evidence path.
- SAFE_FAST_BUILD_STATE.md:417:- Reason: current repo source trail points back to GLD-WINDOW-IDEAL-001, and that candidate already failed setup-time row acceptance.
- SAFE_FAST_BUILD_STATE.md:423:- Latest committed baseline before this status: c8339d9 Add GLD Ideal replacement candidate source selection worksheet.
- SAFE_FAST_BUILD_STATE.md:426:- Combined Day 36 result: GLD Ideal replacement search is blocked and IWM Continuation replacement search is blocked.
- SAFE_FAST_BUILD_STATE.md:435:- Result: both current IWM Continuation and GLD Ideal replacement paths are blocked in current repo sources.
- SAFE_FAST_BUILD_STATE.md:437:- Purpose of next worksheet: collect cleaner bounded real historical candidates for IWM Continuation and GLD Ideal with complete setup-time fields.
- SAFE_FAST_BUILD_STATE.md:507:- **Smallest next evidence-backed fix after this docs batch:** create or accept bounded real historical evidence packets for IWM Continuation and GLD Ideal first, because both remain missing-evidence/inconclusive; bounded 1H/24H support-resistance and room-classification design/test planning is only a later candidate if explicitly requested.
- SAFE_FAST_BUILD_STATE.md:561:- **Implementation summary:** added the local-only in-memory first controlled historical sample evidence set builder, exported it through `watcher_foundation`, and kept the existing historical sample path runner behavior unchanged. The sample set contains one worked `Ideal` / `SPY` setup, one failed `Clean Fast Break` / `QQQ` setup, and one missing-evidence/inconclusive `Continuation` / `GLD` setup. Each sample separates frozen setup-time identity/evidence from after-setup evidence and preserves setup type, symbol, and setup-type-plus-symbol pair tracking.
- SAFE_FAST_BUILD_STATE.md:628:- **Plain purpose:** plan the smallest next local-only implementation step that fills the missing `Continuation` / `GLD` after-setup evidence in the existing controlled sample set, while preserving the worked `Ideal` / `SPY` sample, preserving the failed `Clean Fast Break` / `QQQ` sample, keeping no-hindsight separation, keeping setup type and symbol separation, rerunning the sample path and output review, and showing whether GLD Continuation becomes reviewable or remains inconclusive.
- SAFE_FAST_BUILD_STATE.md:645:- **Implementation summary:** added caller-provided after-setup evidence to only the existing `Continuation` / `GLD` controlled sample, including `source_row_reference`, `post_setup_evidence`, and `future_evidence_used_to_define_setup: False`; preserved the worked `Ideal` / `SPY` sample; preserved the failed `Clean Fast Break` / `QQQ` sample; kept setup-time evidence separate from after-setup evidence; preserved no-hindsight, setup type, symbol, and setup-type-plus-symbol pair separation; and added explicit output-review fields reporting whether GLD Continuation became reviewable or remained inconclusive.
- SAFE_FAST_BUILD_STATE.md:646:- **GLD Continuation review result:** became reviewable. Explicit rerun showed `gld_continuation_review_status=reviewable`, `gld_continuation_became_reviewable=True`, `gld_continuation_remains_inconclusive=False`, worked samples `Ideal` / `SPY` and `Continuation` / `GLD`, failed sample `Clean Fast Break` / `QQQ`, no inconclusive samples, review conclusion `useful_but_not_final_viability_proof`, `profitability_claimed=False`, and `final_viability_proven=False`.
- SAFE_FAST_BUILD_STATE.md:671:- **Plain purpose:** preserve the existing worked `Ideal` / `SPY`, failed `Clean Fast Break` / `QQQ`, and worked/reviewable `Continuation` / `GLD` examples; add exactly one controlled `IWM` example; keep setup type, symbol, setup-type-plus-symbol pair, and no-hindsight separation; rerun the sample path and output review; report whether IWM becomes reviewable; report what the new sample teaches; and avoid profitability, historical success, final viability, live readiness, or production readiness claims.
- SAFE_FAST_BUILD_STATE.md:688:- **Implementation summary:** preserved the existing worked `Ideal` / `SPY` sample, failed `Clean Fast Break` / `QQQ` sample, and worked/reviewable `Continuation` / `GLD` sample; added exactly one controlled `Ideal` / `IWM` sample with setup-time evidence refs, after-setup evidence starting after detection, `source_row_reference`, `post_setup_evidence`, and `future_evidence_used_to_define_setup: False`; kept setup type, symbol, setup-type-plus-symbol pair, setup-time/after-setup, and no-hindsight separation; added output-review fields for IWM review status and what the IWM sample teaches.
- SAFE_FAST_BUILD_STATE.md:716:- **Known controlled sample coverage before future review:** represented symbols are SPY, QQQ, GLD, and IWM; represented setup types are Ideal, Clean Fast Break, and Continuation; represented pairs are `Ideal` / `SPY`, `Clean Fast Break` / `QQQ`, `Continuation` / `GLD`, and `Ideal` / `IWM`. The future review must verify this from actual controlled sample output.
- SAFE_FAST_BUILD_STATE.md:735:- **Coverage result:** represented symbols are `GLD`, `IWM`, `QQQ`, and `SPY`; represented setup types are `Clean Fast Break`, `Continuation`, and `Ideal`; represented pairs are `Ideal` / `SPY`, `Clean Fast Break` / `QQQ`, `Continuation` / `GLD`, and `Ideal` / `IWM`; missing pairs are `Clean Fast Break` / `SPY`, `Continuation` / `SPY`, `Ideal` / `QQQ`, `Continuation` / `QQQ`, `Clean Fast Break` / `IWM`, `Continuation` / `IWM`, `Ideal` / `GLD`, and `Clean Fast Break` / `GLD`.
- SAFE_FAST_BUILD_STATE.md:736:- **Outcome coverage result:** worked chart/setup behavior is represented by `Ideal` / `SPY`, `Continuation` / `GLD`, and `Ideal` / `IWM`; failed chart/setup behavior is represented by `Clean Fast Break` / `QQQ`; active inconclusive/missing-evidence coverage is not represented in the final four-sample controlled set.
- SAFE_FAST_BUILD_STATE.md:772:- **Implementation summary:** preserved the existing `Ideal` / `SPY` worked sample, `Clean Fast Break` / `QQQ` failed sample, `Continuation` / `GLD` worked/reviewable sample, and `Ideal` / `IWM` worked/reviewable sample; added exactly one explicit controlled missing-evidence sample as `Continuation` / `QQQ`. The new sample has setup-time candle/shelf evidence but deliberately omits after-setup `source_row_reference` and `post_setup_evidence`, keeps `future_evidence_used_to_define_setup=False`, remains local-only/in-memory, and is surfaced by the review as missing-evidence coverage instead of worked/failed proof.
- SAFE_FAST_BUILD_STATE.md:774:- **Output review rerun result:** worked samples `3`, failed samples `1`, inconclusive/missing-evidence samples `1`; represented symbols remain `SPY`, `IWM`, `QQQ`, and `GLD`; represented setup types remain `Ideal`, `Clean Fast Break`, and `Continuation`; represented pairs are `Ideal` / `SPY`, `Ideal` / `IWM`, `Clean Fast Break` / `QQQ`, `Continuation` / `GLD`, and `Continuation` / `QQQ`.
- SAFE_FAST_BUILD_STATE.md:793:- **Review conclusion:** controlled sample phase is complete enough to plan real historical examples, because `SPY`, `QQQ`, `IWM`, and `GLD` are represented; `Ideal`, `Clean Fast Break`, and `Continuation` are represented; worked, failed, and missing-evidence examples are represented; no-hindsight separation held; and setup type, symbol, and setup-type-plus-symbol pair separation held.
- SAFE_FAST_BUILD_STATE.md:808:- **First real historical batch definition:** exactly 4 real historical examples, one each for `SPY`, `QQQ`, `IWM`, and `GLD`; all three setup types represented; required first pairs are `Ideal` / `SPY`, `Clean Fast Break` / `QQQ`, `Continuation` / `IWM`, and `Ideal` / `GLD`.
- SAFE_FAST_BUILD_STATE.md:829:- **Implementation summary:** added `build_first_real_historical_example_batch()` and `FIRST_REAL_HISTORICAL_EXAMPLE_BATCH_ID` in the historical sample path module. The builder returns exactly four in-memory real historical examples: `Ideal` / `SPY`, `Clean Fast Break` / `QQQ`, `Continuation` / `IWM`, and `Ideal` / `GLD`. It uses source-backed fixture/report/review references, rejects controlled IDs/refs by test, keeps setup-time evidence separate from after-setup evidence, and preserves no-hindsight boundaries.
- SAFE_FAST_BUILD_STATE.md:830:- **Proof-chain run summary:** `records_processed=4`; `records_accepted=4`; `records_rejected=0`; represented symbols are `SPY`, `QQQ`, `IWM`, and `GLD`; represented setup types are `Ideal`, `Clean Fast Break`, and `Continuation`; represented pairs are `Ideal` / `SPY`, `Clean Fast Break` / `QQQ`, `Continuation` / `IWM`, and `Ideal` / `GLD`; outcome group counts are worked `2`, failed `0`, inconclusive `0`, pending `0`, stale `0`, invalidated `0`, missing evidence `2`.
- SAFE_FAST_BUILD_STATE.md:831:- **Outcome interpretation:** SPY Ideal and QQQ Clean Fast Break are source-backed worked chart/setup behavior examples. IWM Continuation and GLD Ideal are source-backed real candidate examples but remain missing-evidence/inconclusive because repo evidence does not prove accepted numeric trigger, numeric invalidation, and freshness/final signal fields. This is not a profitability, final viability, actual historical success, optimization, production readiness, live readiness, or live trade claim.
- SAFE_FAST_BUILD_STATE.md:838:- **Unfinished items:** final trading-plan viability, profitability, actual historical success, all 12 setup-type-plus-symbol pairs, failed real historical examples, repeated worked/failed patterns, repeated fix paths, lower-tier final readiness, controlled shadow readiness, live readiness, production readiness, Railway readiness, and live trade decision readiness remain unproven. IWM Continuation and GLD Ideal still require accepted trigger/invalidation/freshness evidence before they can be classified as worked or failed proof.
- SAFE_FAST_BUILD_STATE.md:852:- **Plan summary:** inspect existing repo evidence for IWM Continuation and GLD Ideal before any code change. The plan names exact missing accepted evidence: final accepted signal row, accepted triggered state, no primary blocker, numeric trigger, trigger basis, numeric invalidation, invalidation basis, freshness/final signal fields, blocker/caution priority, terminal outcome inputs, and chart risk denominator as applicable by setup.
- SAFE_FAST_BUILD_STATE.md:854:- **GLD Ideal evidence status:** repo contains source-backed candidate and post-candidate movement evidence, but the fixture/review keep the candidate as `PENDING`, `setup_confirming_TO_REVIEW`, `completed_candle_hold_unconfirmed`, null trigger, null invalidation, accepted signal row missing/unconfirmed, and freshness/final fields unconfirmed. This is not accepted worked/failed proof.
- SAFE_FAST_BUILD_STATE.md:857:- **Future inventory required answers:** what exact evidence is missing for IWM Continuation; what exact evidence is missing for GLD Ideal; whether accepted trigger evidence exists; whether accepted invalidation evidence exists; whether accepted freshness/final-signal evidence exists; whether accepted blocker evidence exists; whether accepted terminal outcome evidence exists; where evidence exists, if it exists; if evidence does not exist, keep the examples missing-evidence/inconclusive; smallest next evidence-backed fix.
- SAFE_FAST_BUILD_STATE.md:859:- **Future implementation gate:** do not change the historical sample path builder or tests for IWM/GLD until the inventory names exact accepted evidence fields and exact source references. If no accepted evidence exists, IWM Continuation and GLD Ideal must stay missing-evidence/inconclusive.
- SAFE_FAST_BUILD_STATE.md:5650:- **Core product function:** monitor SPY / QQQ / IWM / GLD for forming Ideal / Clean Fast Break / Continuation setups with trigger-card alerts
- SAFE_FAST_BUILD_STATE.md:6526:- **Selected Ideal candidate window:** `GLD-WINDOW-IDEAL-001`; rows 204-238; `2026-05-04T09:30:00-04:00` to `2026-05-08T15:30:00-04:00`; 35 rows.
- SAFE_FAST_BUILD_STATE.md:6554:- **Sample rows populated:** `GLD-SAMPLE-IDEAL-001`, `GLD-SAMPLE-CLEAN-FAST-BREAK-001`, `GLD-SAMPLE-CONTINUATION-001`
- SAFE_FAST_BUILD_STATE.md:6555:- **Ideal candidate worksheet row:** `GLD-SAMPLE-IDEAL-001`; source window `GLD-WINDOW-IDEAL-001`; rows 204-238; `2026-05-04T09:30:00-04:00` to `2026-05-08T15:30:00-04:00`; 35 rows; CANDIDATE / NEEDS REVIEW only.
- SAFE_FAST_BUILD_STATE.md:6560:- **Exact next task:** create GLD first setup replay readiness review from the populated worksheet, preferably `GLD-SAMPLE-IDEAL-001` first.
- SAFE_FAST_BUILD_STATE.md:6574:## GLD Ideal 001 replay readiness review status
- SAFE_FAST_BUILD_STATE.md:6578:- **Sample ID:** `GLD-SAMPLE-IDEAL-001`
- SAFE_FAST_BUILD_STATE.md:6579:- **Window ID:** `GLD-WINDOW-IDEAL-001`
- SAFE_FAST_BUILD_STATE.md:6593:- **Next task:** create GLD Ideal 001 real historical replay review asset.
- SAFE_FAST_BUILD_STATE.md:6594:- **GLD status:** active broader coverage target; first Ideal readiness review complete
- SAFE_FAST_BUILD_STATE.md:6605:## GLD Ideal 001 real historical replay review asset status
- SAFE_FAST_BUILD_STATE.md:6609:- **Sample ID:** `GLD-SAMPLE-IDEAL-001`
- SAFE_FAST_BUILD_STATE.md:6610:- **Window ID:** `GLD-WINDOW-IDEAL-001`
- SAFE_FAST_BUILD_STATE.md:6620:- **Review asset readiness result:** PASS; enough repo-backed expectations exist to create the GLD Ideal 001 replay fixture specification review next.
- SAFE_FAST_BUILD_STATE.md:6628:- **Next task:** create GLD Ideal 001 replay fixture specification review only.
- SAFE_FAST_BUILD_STATE.md:6629:- **GLD status:** active broader coverage target; first Ideal real historical replay review asset complete
- SAFE_FAST_BUILD_STATE.md:6640:## GLD Ideal 001 replay fixture specification review status
- SAFE_FAST_BUILD_STATE.md:6644:- **Sample ID:** `GLD-SAMPLE-IDEAL-001`
- SAFE_FAST_BUILD_STATE.md:6645:- **Window ID:** `GLD-WINDOW-IDEAL-001`
- SAFE_FAST_BUILD_STATE.md:6664:- **Next task:** create GLD Ideal 001 replay fixture JSON asset only.
- SAFE_FAST_BUILD_STATE.md:6665:- **GLD status:** active broader coverage target; first Ideal fixture specification review complete
- SAFE_FAST_BUILD_STATE.md:6676:## GLD Ideal 001 replay fixture asset status
- SAFE_FAST_BUILD_STATE.md:6680:- **Sample ID:** `GLD-SAMPLE-IDEAL-001`
- SAFE_FAST_BUILD_STATE.md:6681:- **Window ID:** `GLD-WINDOW-IDEAL-001`
- SAFE_FAST_BUILD_STATE.md:6701:- **Next task:** validate GLD Ideal 001 fixture output only; do not create chart outcomes, aggregate closeout, watcher work, option P&L, account sizing, production readiness, or live trade decisions.
- SAFE_FAST_BUILD_STATE.md:6703:## GLD Ideal 001 replay fixture output validation status
- SAFE_FAST_BUILD_STATE.md:6708:- **Sample ID:** `GLD-SAMPLE-IDEAL-001`
- SAFE_FAST_BUILD_STATE.md:6709:- **Window ID:** `GLD-WINDOW-IDEAL-001`
- SAFE_FAST_BUILD_STATE.md:6863:- **Validation status:** PASS; fixture JSON syntax, repo-native fixture validation, targeted lifecycle fixture validation, targeted input/output schema validation, targeted source-window consistency, GLD-only symbol preservation, `1h_rth` / `America/New_York` / `regular_session=true`, valid OHLCV, source/source-as-of/data-vendor preservation, false Continuation/Ideal relabel protection, and no-hindsight cumulative prefix handling all passed.
- SAFE_FAST_BUILD_STATE.md:7014:- **Validation status:** PASS; fixture JSON syntax, repo-native fixture validation, targeted lifecycle fixture validation, targeted input/output schema validation, targeted source-window consistency, GLD-only symbol preservation, `1h_rth` / `America/New_York` / `regular_session=true`, valid OHLCV, source/source-as-of/data-vendor preservation, false Ideal/Clean Fast Break relabel protection, and no-hindsight cumulative prefix handling all passed.
- SAFE_FAST_BUILD_STATE.md:7036:- **GLD chart outcome inputs ready:** Ideal 001, Clean Fast Break 001, and Continuation 001 fixture output validations are PASS.
- SAFE_FAST_BUILD_STATE.md:7037:- **Per-setup chart-only outcome order:** GLD Ideal 001, then GLD Clean Fast Break 001, then GLD Continuation 001.
- SAFE_FAST_BUILD_STATE.md:7053:- **Next task:** create GLD Ideal 001 chart-only outcome review only; do not create generated replay reports, generated chart outcome reports, aggregate summary, closeout, watcher work, option P&L, account sizing, production readiness, or live trade decisions.
- SAFE_FAST_BUILD_STATE.md:7055:## GLD Ideal 001 chart-only outcome review status
- SAFE_FAST_BUILD_STATE.md:7061:- **Sample ID:** `GLD-SAMPLE-IDEAL-001`
- SAFE_FAST_BUILD_STATE.md:7062:- **Window ID:** `GLD-WINDOW-IDEAL-001`
- SAFE_FAST_BUILD_STATE.md:7072:- **Same-day/fast-swing classification:** UNCONFIRMED; GLD Ideal 001 lacks accepted generated-outcome inputs.
- SAFE_FAST_BUILD_STATE.md:7197:- **What GLD now proves:** validated GLD source CSV evidence; current-depth Ideal, Clean Fast Break, and Continuation setup-family representation; accepted docs-only chart movement reviews for all three setup families; accepted aggregate summary/review; GLD current-depth broader coverage can close at known-limits depth before all-symbol current-depth closeout/readiness review.
- SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_CALCULATION_RULES_PLAN.md:194:- SPY has real replay signal coverage for Continuation, Ideal, and Clean Fast Break; QQQ, IWM, and GLD do not yet have equivalent local real replay closeout evidence.
- SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_RUNNER_SCAFFOLD_PLAN.md:40:Allowed symbol universe remains `SPY`, `QQQ`, `IWM`, and `GLD`, but the first scaffold should run only the existing SPY Continuation sample fixture. Allowed setup families remain `Ideal`, `Clean Fast Break`, and `Continuation`, but the first scaffold should not manufacture new candidates.
- SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_SCHEMA_DESIGN.md:74:The allowed v1 symbols are `SPY`, `QQQ`, `IWM`, and `GLD`. The allowed setup families are `Ideal`, `Clean Fast Break`, and `Continuation`.
- SAFE_FAST_CONTINUOUS_WATCHER_FOUNDATION_SHADOW_ARCHITECTURE_PLAN.md:26:The watcher target is a shadow/watch-only SAFE-FAST lifecycle monitor for SPY, QQQ, IWM, and GLD. It should track forming and changing Ideal, Clean Fast Break, and Continuation setups, produce trigger-card outputs, preserve stale/spent/no-fresh-trigger discipline, suppress duplicate same-state alerts, focus attention on the best current candidate, and create review artifacts for later shadow accuracy review.
- SAFE_FAST_CONTROLLED_SAMPLE_COVERAGE_REVIEW.md:75:- `Ideal` / `GLD`.
- SAFE_FAST_CONTROLLED_SAMPLE_COVERAGE_REVIEW.md:80:Worked chart/setup behavior is represented by `Ideal` / `SPY`, `Continuation` / `GLD`, and `Ideal` / `IWM`.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:92:- A failure must be diagnosed by setup type and symbol, such as IWM Continuation, GLD Ideal, QQQ Clean Fast Break, or SPY Ideal.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:150:Ideal, Clean Fast Break, Continuation, SPY, QQQ, IWM, and GLD must each earn their place.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:271:Answer: Return to the docs-only IWM/GLD missing-evidence inventory. Determine whether accepted evidence already exists for IWM Continuation and GLD Ideal. If it does not exist, keep them missing-evidence/inconclusive and name the smallest evidence-backed fix.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:347:## Day 36 GLD Ideal 001 accepted signal row review status
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:351:- Result: GLD Ideal 001 does not have an accepted setup-time signal row.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:352:- Status: GLD Ideal 001 remains missing-evidence/inconclusive.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:354:- Combined Day 36 evidence result: IWM Continuation 001 and GLD Ideal 001 both remain missing-evidence/inconclusive because neither has an accepted setup-time signal row.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:355:- Smallest next evidence-backed fix: choose the clearest bounded trigger/invalidation/freshness acceptance review between IWM Continuation and GLD Ideal; do not promote either setup unless accepted setup-time proof exists.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:358:## Day 36 GLD Ideal 001 trigger / invalidation / freshness acceptance review status
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:360:- Latest committed baseline before this status: 8044901 Add GLD Ideal accepted signal row review.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:362:- Result: GLD Ideal 001 cannot accept trigger / invalidation / freshness proof from current repo evidence.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:363:- Status: GLD Ideal 001 remains missing-evidence/inconclusive.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:365:- Smallest next GLD-specific fix: create a bounded GLD Ideal setup-time row acceptance worksheet.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:366:- Project-level next move: use GLD Ideal as the next worksheet candidate unless local source review proves IWM has clearer accepted setup-time rows.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:369:## Day 36 GLD Ideal 001 setup-time row acceptance worksheet status
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:371:- Latest committed baseline before this status: ff0f56d Add GLD Ideal trigger invalidation freshness acceptance review.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:373:- Result: GLD Ideal 001 cannot accept one setup-time row from current repo evidence.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:374:- Status: GLD Ideal 001 remains missing-evidence/inconclusive.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:382:- Latest committed baseline before this status: add70a4 Add GLD Ideal setup time row acceptance worksheet.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:387:- Combined Day 36 evidence result: IWM Continuation 001 and GLD Ideal 001 both remain missing-evidence/inconclusive because neither has accepted setup-time proof.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:388:- Smallest next evidence-backed fix: stop trying to promote these two candidate examples unless explicitly requested; create a bounded real historical replacement-candidate selection review for a cleaner IWM Continuation or GLD Ideal example with complete setup-time fields.
