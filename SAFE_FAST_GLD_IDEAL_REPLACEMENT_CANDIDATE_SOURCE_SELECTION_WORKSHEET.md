# SAFE-FAST GLD Ideal Replacement Candidate Source Selection Worksheet

Project day: Day 36 working day
Repo baseline: patch8
Latest committed baseline before this worksheet: c78a41c Add IWM GLD replacement candidate selection review
Mode: build-only; not live trade chat

## Purpose

This docs-only worksheet searches current repo sources for a cleaner GLD Ideal replacement candidate after GLD Ideal 001 failed setup-time row acceptance.

This worksheet does not invent evidence, does not fake proof, does not use hindsight filling, and does not authorize live data, alerts, broker/order/account/options/P&L, account sizing, Railway, production, or live trade decisions.

## Required decision

This worksheet must choose one of:

1. a cleaner GLD Ideal replacement candidate with enough setup-time fields to proceed;
2. no acceptable GLD Ideal replacement candidate exists in current repo sources;
3. GLD Ideal should stay blocked and IWM Continuation replacement search should become next.

## Decision

No acceptable GLD Ideal replacement candidate is accepted from current repo sources.

GLD Ideal stays blocked for the current Day 36 missing-evidence path.

The next evidence-backed move is IWM Continuation replacement candidate source selection.

## Reason

The current repo source trail points back to GLD-WINDOW-IDEAL-001 as the known GLD Ideal real historical candidate.

That candidate has already been reviewed and remains blocked:

- no accepted setup-time signal row
- no accepted final verdict
- no accepted trigger state
- no accepted numeric trigger
- no accepted numeric invalidation
- no accepted freshness/final-signal
- unresolved completed-candle-hold / setup-confirming uncertainty
- no terminal outcome eligibility before setup-time acceptance

No cleaner GLD Ideal replacement candidate is accepted by this worksheet.

## Source search summary

The search checked repo markdown for:

- GLD-WINDOW-IDEAL
- GLD Ideal
- Ideal GLD
- GLD-SAMPLE-IDEAL

Search hits are source leads only. They are not accepted evidence by themselves.

## Acceptance rule

A replacement candidate may not be chosen from chart movement.

A replacement candidate must have or be able to support, from setup-time evidence only:

- exact setup-time signal timestamp
- accepted setup identity
- accepted final verdict or clearly rejected verdict
- accepted trigger state
- accepted numeric trigger
- accepted trigger basis
- accepted numeric invalidation
- accepted invalidation basis
- accepted freshness/final-signal decision
- accepted blocker/caution decision
- terminal outcome eligibility only after setup-time evidence is frozen

## Outcome

Outcome selected: no acceptable GLD Ideal replacement candidate exists in current repo sources.

## Smallest next evidence-backed fix

Create `SAFE_FAST_IWM_CONTINUATION_REPLACEMENT_CANDIDATE_SOURCE_SELECTION_WORKSHEET.md`.

That worksheet must search existing repo sources only and choose one of:

1. a cleaner IWM Continuation replacement candidate with enough setup-time fields to proceed;
2. no acceptable IWM Continuation replacement candidate exists in current repo sources;
3. both current IWM/GLD replacement paths are blocked and a new bounded real historical source collection task is required.

## Tests

Tests not run. Docs-only source selection worksheet.

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

## GLD Ideal repo search hits

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
- SAFE_FAST_BUILD_STATE.md:477:- **Smallest next evidence-backed fix after this docs batch:** create or accept bounded real historical evidence packets for IWM Continuation and GLD Ideal first, because both remain missing-evidence/inconclusive; bounded 1H/24H support-resistance and room-classification design/test planning is only a later candidate if explicitly requested.
- SAFE_FAST_BUILD_STATE.md:531:- **Implementation summary:** added the local-only in-memory first controlled historical sample evidence set builder, exported it through `watcher_foundation`, and kept the existing historical sample path runner behavior unchanged. The sample set contains one worked `Ideal` / `SPY` setup, one failed `Clean Fast Break` / `QQQ` setup, and one missing-evidence/inconclusive `Continuation` / `GLD` setup. Each sample separates frozen setup-time identity/evidence from after-setup evidence and preserves setup type, symbol, and setup-type-plus-symbol pair tracking.
- SAFE_FAST_BUILD_STATE.md:598:- **Plain purpose:** plan the smallest next local-only implementation step that fills the missing `Continuation` / `GLD` after-setup evidence in the existing controlled sample set, while preserving the worked `Ideal` / `SPY` sample, preserving the failed `Clean Fast Break` / `QQQ` sample, keeping no-hindsight separation, keeping setup type and symbol separation, rerunning the sample path and output review, and showing whether GLD Continuation becomes reviewable or remains inconclusive.
- SAFE_FAST_BUILD_STATE.md:615:- **Implementation summary:** added caller-provided after-setup evidence to only the existing `Continuation` / `GLD` controlled sample, including `source_row_reference`, `post_setup_evidence`, and `future_evidence_used_to_define_setup: False`; preserved the worked `Ideal` / `SPY` sample; preserved the failed `Clean Fast Break` / `QQQ` sample; kept setup-time evidence separate from after-setup evidence; preserved no-hindsight, setup type, symbol, and setup-type-plus-symbol pair separation; and added explicit output-review fields reporting whether GLD Continuation became reviewable or remained inconclusive.
- SAFE_FAST_BUILD_STATE.md:616:- **GLD Continuation review result:** became reviewable. Explicit rerun showed `gld_continuation_review_status=reviewable`, `gld_continuation_became_reviewable=True`, `gld_continuation_remains_inconclusive=False`, worked samples `Ideal` / `SPY` and `Continuation` / `GLD`, failed sample `Clean Fast Break` / `QQQ`, no inconclusive samples, review conclusion `useful_but_not_final_viability_proof`, `profitability_claimed=False`, and `final_viability_proven=False`.
- SAFE_FAST_BUILD_STATE.md:641:- **Plain purpose:** preserve the existing worked `Ideal` / `SPY`, failed `Clean Fast Break` / `QQQ`, and worked/reviewable `Continuation` / `GLD` examples; add exactly one controlled `IWM` example; keep setup type, symbol, setup-type-plus-symbol pair, and no-hindsight separation; rerun the sample path and output review; report whether IWM becomes reviewable; report what the new sample teaches; and avoid profitability, historical success, final viability, live readiness, or production readiness claims.
- SAFE_FAST_BUILD_STATE.md:658:- **Implementation summary:** preserved the existing worked `Ideal` / `SPY` sample, failed `Clean Fast Break` / `QQQ` sample, and worked/reviewable `Continuation` / `GLD` sample; added exactly one controlled `Ideal` / `IWM` sample with setup-time evidence refs, after-setup evidence starting after detection, `source_row_reference`, `post_setup_evidence`, and `future_evidence_used_to_define_setup: False`; kept setup type, symbol, setup-type-plus-symbol pair, setup-time/after-setup, and no-hindsight separation; added output-review fields for IWM review status and what the IWM sample teaches.
- SAFE_FAST_BUILD_STATE.md:686:- **Known controlled sample coverage before future review:** represented symbols are SPY, QQQ, GLD, and IWM; represented setup types are Ideal, Clean Fast Break, and Continuation; represented pairs are `Ideal` / `SPY`, `Clean Fast Break` / `QQQ`, `Continuation` / `GLD`, and `Ideal` / `IWM`. The future review must verify this from actual controlled sample output.
- SAFE_FAST_BUILD_STATE.md:705:- **Coverage result:** represented symbols are `GLD`, `IWM`, `QQQ`, and `SPY`; represented setup types are `Clean Fast Break`, `Continuation`, and `Ideal`; represented pairs are `Ideal` / `SPY`, `Clean Fast Break` / `QQQ`, `Continuation` / `GLD`, and `Ideal` / `IWM`; missing pairs are `Clean Fast Break` / `SPY`, `Continuation` / `SPY`, `Ideal` / `QQQ`, `Continuation` / `QQQ`, `Clean Fast Break` / `IWM`, `Continuation` / `IWM`, `Ideal` / `GLD`, and `Clean Fast Break` / `GLD`.
- SAFE_FAST_BUILD_STATE.md:706:- **Outcome coverage result:** worked chart/setup behavior is represented by `Ideal` / `SPY`, `Continuation` / `GLD`, and `Ideal` / `IWM`; failed chart/setup behavior is represented by `Clean Fast Break` / `QQQ`; active inconclusive/missing-evidence coverage is not represented in the final four-sample controlled set.
- SAFE_FAST_BUILD_STATE.md:742:- **Implementation summary:** preserved the existing `Ideal` / `SPY` worked sample, `Clean Fast Break` / `QQQ` failed sample, `Continuation` / `GLD` worked/reviewable sample, and `Ideal` / `IWM` worked/reviewable sample; added exactly one explicit controlled missing-evidence sample as `Continuation` / `QQQ`. The new sample has setup-time candle/shelf evidence but deliberately omits after-setup `source_row_reference` and `post_setup_evidence`, keeps `future_evidence_used_to_define_setup=False`, remains local-only/in-memory, and is surfaced by the review as missing-evidence coverage instead of worked/failed proof.
- SAFE_FAST_BUILD_STATE.md:744:- **Output review rerun result:** worked samples `3`, failed samples `1`, inconclusive/missing-evidence samples `1`; represented symbols remain `SPY`, `IWM`, `QQQ`, and `GLD`; represented setup types remain `Ideal`, `Clean Fast Break`, and `Continuation`; represented pairs are `Ideal` / `SPY`, `Ideal` / `IWM`, `Clean Fast Break` / `QQQ`, `Continuation` / `GLD`, and `Continuation` / `QQQ`.
- SAFE_FAST_BUILD_STATE.md:763:- **Review conclusion:** controlled sample phase is complete enough to plan real historical examples, because `SPY`, `QQQ`, `IWM`, and `GLD` are represented; `Ideal`, `Clean Fast Break`, and `Continuation` are represented; worked, failed, and missing-evidence examples are represented; no-hindsight separation held; and setup type, symbol, and setup-type-plus-symbol pair separation held.
- SAFE_FAST_BUILD_STATE.md:778:- **First real historical batch definition:** exactly 4 real historical examples, one each for `SPY`, `QQQ`, `IWM`, and `GLD`; all three setup types represented; required first pairs are `Ideal` / `SPY`, `Clean Fast Break` / `QQQ`, `Continuation` / `IWM`, and `Ideal` / `GLD`.
- SAFE_FAST_BUILD_STATE.md:799:- **Implementation summary:** added `build_first_real_historical_example_batch()` and `FIRST_REAL_HISTORICAL_EXAMPLE_BATCH_ID` in the historical sample path module. The builder returns exactly four in-memory real historical examples: `Ideal` / `SPY`, `Clean Fast Break` / `QQQ`, `Continuation` / `IWM`, and `Ideal` / `GLD`. It uses source-backed fixture/report/review references, rejects controlled IDs/refs by test, keeps setup-time evidence separate from after-setup evidence, and preserves no-hindsight boundaries.
- SAFE_FAST_BUILD_STATE.md:800:- **Proof-chain run summary:** `records_processed=4`; `records_accepted=4`; `records_rejected=0`; represented symbols are `SPY`, `QQQ`, `IWM`, and `GLD`; represented setup types are `Ideal`, `Clean Fast Break`, and `Continuation`; represented pairs are `Ideal` / `SPY`, `Clean Fast Break` / `QQQ`, `Continuation` / `IWM`, and `Ideal` / `GLD`; outcome group counts are worked `2`, failed `0`, inconclusive `0`, pending `0`, stale `0`, invalidated `0`, missing evidence `2`.
- SAFE_FAST_BUILD_STATE.md:801:- **Outcome interpretation:** SPY Ideal and QQQ Clean Fast Break are source-backed worked chart/setup behavior examples. IWM Continuation and GLD Ideal are source-backed real candidate examples but remain missing-evidence/inconclusive because repo evidence does not prove accepted numeric trigger, numeric invalidation, and freshness/final signal fields. This is not a profitability, final viability, actual historical success, optimization, production readiness, live readiness, or live trade claim.
- SAFE_FAST_BUILD_STATE.md:808:- **Unfinished items:** final trading-plan viability, profitability, actual historical success, all 12 setup-type-plus-symbol pairs, failed real historical examples, repeated worked/failed patterns, repeated fix paths, lower-tier final readiness, controlled shadow readiness, live readiness, production readiness, Railway readiness, and live trade decision readiness remain unproven. IWM Continuation and GLD Ideal still require accepted trigger/invalidation/freshness evidence before they can be classified as worked or failed proof.
- SAFE_FAST_BUILD_STATE.md:822:- **Plan summary:** inspect existing repo evidence for IWM Continuation and GLD Ideal before any code change. The plan names exact missing accepted evidence: final accepted signal row, accepted triggered state, no primary blocker, numeric trigger, trigger basis, numeric invalidation, invalidation basis, freshness/final signal fields, blocker/caution priority, terminal outcome inputs, and chart risk denominator as applicable by setup.
- SAFE_FAST_BUILD_STATE.md:824:- **GLD Ideal evidence status:** repo contains source-backed candidate and post-candidate movement evidence, but the fixture/review keep the candidate as `PENDING`, `setup_confirming_TO_REVIEW`, `completed_candle_hold_unconfirmed`, null trigger, null invalidation, accepted signal row missing/unconfirmed, and freshness/final fields unconfirmed. This is not accepted worked/failed proof.
- SAFE_FAST_BUILD_STATE.md:827:- **Future inventory required answers:** what exact evidence is missing for IWM Continuation; what exact evidence is missing for GLD Ideal; whether accepted trigger evidence exists; whether accepted invalidation evidence exists; whether accepted freshness/final-signal evidence exists; whether accepted blocker evidence exists; whether accepted terminal outcome evidence exists; where evidence exists, if it exists; if evidence does not exist, keep the examples missing-evidence/inconclusive; smallest next evidence-backed fix.
- SAFE_FAST_BUILD_STATE.md:829:- **Future implementation gate:** do not change the historical sample path builder or tests for IWM/GLD until the inventory names exact accepted evidence fields and exact source references. If no accepted evidence exists, IWM Continuation and GLD Ideal must stay missing-evidence/inconclusive.
- SAFE_FAST_BUILD_STATE.md:5620:- **Core product function:** monitor SPY / QQQ / IWM / GLD for forming Ideal / Clean Fast Break / Continuation setups with trigger-card alerts
- SAFE_FAST_BUILD_STATE.md:6496:- **Selected Ideal candidate window:** `GLD-WINDOW-IDEAL-001`; rows 204-238; `2026-05-04T09:30:00-04:00` to `2026-05-08T15:30:00-04:00`; 35 rows.
- SAFE_FAST_BUILD_STATE.md:6524:- **Sample rows populated:** `GLD-SAMPLE-IDEAL-001`, `GLD-SAMPLE-CLEAN-FAST-BREAK-001`, `GLD-SAMPLE-CONTINUATION-001`
- SAFE_FAST_BUILD_STATE.md:6525:- **Ideal candidate worksheet row:** `GLD-SAMPLE-IDEAL-001`; source window `GLD-WINDOW-IDEAL-001`; rows 204-238; `2026-05-04T09:30:00-04:00` to `2026-05-08T15:30:00-04:00`; 35 rows; CANDIDATE / NEEDS REVIEW only.
- SAFE_FAST_BUILD_STATE.md:6530:- **Exact next task:** create GLD first setup replay readiness review from the populated worksheet, preferably `GLD-SAMPLE-IDEAL-001` first.
- SAFE_FAST_BUILD_STATE.md:6544:## GLD Ideal 001 replay readiness review status
- SAFE_FAST_BUILD_STATE.md:6548:- **Sample ID:** `GLD-SAMPLE-IDEAL-001`
- SAFE_FAST_BUILD_STATE.md:6549:- **Window ID:** `GLD-WINDOW-IDEAL-001`
- SAFE_FAST_BUILD_STATE.md:6563:- **Next task:** create GLD Ideal 001 real historical replay review asset.
- SAFE_FAST_BUILD_STATE.md:6564:- **GLD status:** active broader coverage target; first Ideal readiness review complete
- SAFE_FAST_BUILD_STATE.md:6575:## GLD Ideal 001 real historical replay review asset status
- SAFE_FAST_BUILD_STATE.md:6579:- **Sample ID:** `GLD-SAMPLE-IDEAL-001`
- SAFE_FAST_BUILD_STATE.md:6580:- **Window ID:** `GLD-WINDOW-IDEAL-001`
- SAFE_FAST_BUILD_STATE.md:6590:- **Review asset readiness result:** PASS; enough repo-backed expectations exist to create the GLD Ideal 001 replay fixture specification review next.
- SAFE_FAST_BUILD_STATE.md:6598:- **Next task:** create GLD Ideal 001 replay fixture specification review only.
- SAFE_FAST_BUILD_STATE.md:6599:- **GLD status:** active broader coverage target; first Ideal real historical replay review asset complete
- SAFE_FAST_BUILD_STATE.md:6610:## GLD Ideal 001 replay fixture specification review status
- SAFE_FAST_BUILD_STATE.md:6614:- **Sample ID:** `GLD-SAMPLE-IDEAL-001`
- SAFE_FAST_BUILD_STATE.md:6615:- **Window ID:** `GLD-WINDOW-IDEAL-001`
- SAFE_FAST_BUILD_STATE.md:6634:- **Next task:** create GLD Ideal 001 replay fixture JSON asset only.
- SAFE_FAST_BUILD_STATE.md:6635:- **GLD status:** active broader coverage target; first Ideal fixture specification review complete
- SAFE_FAST_BUILD_STATE.md:6646:## GLD Ideal 001 replay fixture asset status
- SAFE_FAST_BUILD_STATE.md:6650:- **Sample ID:** `GLD-SAMPLE-IDEAL-001`
- SAFE_FAST_BUILD_STATE.md:6651:- **Window ID:** `GLD-WINDOW-IDEAL-001`
- SAFE_FAST_BUILD_STATE.md:6671:- **Next task:** validate GLD Ideal 001 fixture output only; do not create chart outcomes, aggregate closeout, watcher work, option P&L, account sizing, production readiness, or live trade decisions.
- SAFE_FAST_BUILD_STATE.md:6673:## GLD Ideal 001 replay fixture output validation status
- SAFE_FAST_BUILD_STATE.md:6678:- **Sample ID:** `GLD-SAMPLE-IDEAL-001`
- SAFE_FAST_BUILD_STATE.md:6679:- **Window ID:** `GLD-WINDOW-IDEAL-001`
- SAFE_FAST_BUILD_STATE.md:6833:- **Validation status:** PASS; fixture JSON syntax, repo-native fixture validation, targeted lifecycle fixture validation, targeted input/output schema validation, targeted source-window consistency, GLD-only symbol preservation, `1h_rth` / `America/New_York` / `regular_session=true`, valid OHLCV, source/source-as-of/data-vendor preservation, false Continuation/Ideal relabel protection, and no-hindsight cumulative prefix handling all passed.
- SAFE_FAST_BUILD_STATE.md:6984:- **Validation status:** PASS; fixture JSON syntax, repo-native fixture validation, targeted lifecycle fixture validation, targeted input/output schema validation, targeted source-window consistency, GLD-only symbol preservation, `1h_rth` / `America/New_York` / `regular_session=true`, valid OHLCV, source/source-as-of/data-vendor preservation, false Ideal/Clean Fast Break relabel protection, and no-hindsight cumulative prefix handling all passed.
- SAFE_FAST_BUILD_STATE.md:7006:- **GLD chart outcome inputs ready:** Ideal 001, Clean Fast Break 001, and Continuation 001 fixture output validations are PASS.
- SAFE_FAST_BUILD_STATE.md:7007:- **Per-setup chart-only outcome order:** GLD Ideal 001, then GLD Clean Fast Break 001, then GLD Continuation 001.
- SAFE_FAST_BUILD_STATE.md:7023:- **Next task:** create GLD Ideal 001 chart-only outcome review only; do not create generated replay reports, generated chart outcome reports, aggregate summary, closeout, watcher work, option P&L, account sizing, production readiness, or live trade decisions.
- SAFE_FAST_BUILD_STATE.md:7025:## GLD Ideal 001 chart-only outcome review status
- SAFE_FAST_BUILD_STATE.md:7031:- **Sample ID:** `GLD-SAMPLE-IDEAL-001`
- SAFE_FAST_BUILD_STATE.md:7032:- **Window ID:** `GLD-WINDOW-IDEAL-001`
- SAFE_FAST_BUILD_STATE.md:7042:- **Same-day/fast-swing classification:** UNCONFIRMED; GLD Ideal 001 lacks accepted generated-outcome inputs.
- SAFE_FAST_BUILD_STATE.md:7167:- **What GLD now proves:** validated GLD source CSV evidence; current-depth Ideal, Clean Fast Break, and Continuation setup-family representation; accepted docs-only chart movement reviews for all three setup families; accepted aggregate summary/review; GLD current-depth broader coverage can close at known-limits depth before all-symbol current-depth closeout/readiness review.
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
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:395:- Result: stop trying to promote the current IWM Continuation 001 and GLD Ideal 001 candidates unless explicitly requested later.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:398:- Target: find a cleaner GLD Ideal replacement candidate from existing repo sources only, or prove no acceptable GLD Ideal replacement candidate exists in current repo sources.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:789:- Historical objective for that completed plan-correction block was creating the docs-only next-step plan after the first real historical example batch, focused on IWM Continuation and GLD Ideal missing accepted evidence.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:792:- Sample evidence set behavior: exposes one worked `Ideal` / `SPY` setup, one failed `Clean Fast Break` / `QQQ` setup, one reviewable `Continuation` / `GLD` setup, one reviewable `Ideal` / `IWM` setup, and exactly one explicit controlled missing-evidence `Continuation` / `QQQ` setup through the existing runner; preserves setup type separation, symbol separation, setup-type-plus-symbol pair separation, setup-time versus after-setup evidence separation, diagnostics, fix paths, lower-tier summary, no-trade/watch-only, no-live-data, no-controlled-shadow, no-alert, no-broker, no-file-write, no-rule-change, and no-optimization boundaries.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:794:- Review result: the controlled output is useful but not final viability proof. The worked `Ideal` / `SPY` sample gives clear chart-behavior proof; the failed `Clean Fast Break` / `QQQ` sample gives useful diagnosis; the existing `Continuation` / `GLD` sample remains reviewable; the `Ideal` / `IWM` sample remains reviewable; the new `Continuation` / `QQQ` sample provides active missing-evidence coverage. Bundle readiness still shows tiny-sample/upstream review contract gaps and must not be treated as final lower-tier readiness.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:797:- Controlled sample implementation result: represented symbols are `GLD`, `IWM`, `QQQ`, and `SPY`; represented setup types are `Clean Fast Break`, `Continuation`, and `Ideal`; represented pairs are `Ideal` / `SPY`, `Clean Fast Break` / `QQQ`, `Continuation` / `GLD`, `Ideal` / `IWM`, and `Continuation` / `QQQ`.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:806:- Current coverage review conclusion: the controlled sample phase is complete enough to plan real historical examples. `SPY`, `QQQ`, `IWM`, and `GLD` are represented; `Ideal`, `Clean Fast Break`, and `Continuation` are represented; worked, failed, and missing-evidence examples are represented; no-hindsight separation held; setup type and symbol separation held.
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md:807:- Current plan summary: first batch should contain exactly 4 real historical examples, one each for `SPY`, `QQQ`, `IWM`, and `GLD`; all three setup types must be represented; required pairs are `Ideal` / `SPY`, `Clean Fast Break` / `QQQ`, `Continuation` / `IWM`, and `Ideal` / `GLD`.

## Unique GLD-WINDOW-IDEAL source hits

- SAFE_FAST_BUILD_STATE.md:6496:- **Selected Ideal candidate window:** `GLD-WINDOW-IDEAL-001`; rows 204-238; `2026-05-04T09:30:00-04:00` to `2026-05-08T15:30:00-04:00`; 35 rows.
- SAFE_FAST_BUILD_STATE.md:6525:- **Ideal candidate worksheet row:** `GLD-SAMPLE-IDEAL-001`; source window `GLD-WINDOW-IDEAL-001`; rows 204-238; `2026-05-04T09:30:00-04:00` to `2026-05-08T15:30:00-04:00`; 35 rows; CANDIDATE / NEEDS REVIEW only.
- SAFE_FAST_BUILD_STATE.md:6549:- **Window ID:** `GLD-WINDOW-IDEAL-001`
- SAFE_FAST_BUILD_STATE.md:6580:- **Window ID:** `GLD-WINDOW-IDEAL-001`
- SAFE_FAST_BUILD_STATE.md:6615:- **Window ID:** `GLD-WINDOW-IDEAL-001`
- SAFE_FAST_BUILD_STATE.md:6651:- **Window ID:** `GLD-WINDOW-IDEAL-001`
- SAFE_FAST_BUILD_STATE.md:6679:- **Window ID:** `GLD-WINDOW-IDEAL-001`
- SAFE_FAST_BUILD_STATE.md:7032:- **Window ID:** `GLD-WINDOW-IDEAL-001`
- SAFE_FAST_GLD_BOUNDED_SOURCE_WINDOW_SELECTION_REVIEW.md:54:| GLD-WINDOW-IDEAL-001 | real historical replay candidate | Ideal CANDIDATE | bullish/call-side candidate if later review confirms | 204-238 | `2026-05-04T09:30:00-04:00` | `2026-05-08T15:30:00-04:00` | 35 | Source window shows a low/retest area on 2026-05-04 near `413.2801`, a 2026-05-05 base with `417.9050` to `421.1300` range, and recovery through 2026-05-06/2026-05-07 into a `437.4200` window high before 2026-05-08 pullback rows. | Expected setup type: Ideal CANDIDATE only; direction: bullish if later row-by-row review confirms; candidate stage: pullback/retest into recovery; trigger zone to review: recovery through the 2026-05-06/2026-05-07 `433.1900` to `437.4200` area; candle/timeframe rule: completed 1H RTH recovery/hold; invalidation area: 2026-05-04 low zone near `413.2801` if later review accepts it; fresh/stale/spent question: whether the 2026-05-07 recovery is fresh or already extended; blocker/caution questions: unavailable 24H/macro/IV/event context. | Final Ideal identity, trend/EMA context, exact trigger, exact invalidation, final stage/verdict, blockers/cautions, 24H/daily, macro, IV, event context. | READY FOR WORKSHEET; NOT READY FOR FIXTURE until row-by-row review. | Candidate only; selected because the bounded source rows show retest/recovery shape, not validated setup proof. |
- SAFE_FAST_GLD_CHART_ONLY_OUTCOME_PHASE_PLANNING_REVIEW.md:59:| GLD Ideal 001 | `SAFE_FAST_GLD_IDEAL_001_REPLAY_FIXTURE_OUTPUT_VALIDATION_REVIEW.md` | `GLD-SAMPLE-IDEAL-001` | `GLD-WINDOW-IDEAL-001` | rows 204-238 | `2026-05-04T09:30:00-04:00` to `2026-05-08T15:30:00-04:00` | 35 | PASS; `Ideal: 6`, `NO_TRADE: 3`, `PENDING: 3` |
- SAFE_FAST_GLD_HISTORICAL_SAMPLE_COLLECTION_WORKSHEET.md:66:| GLD-SAMPLE-IDEAL-001 | GLD-WINDOW-IDEAL-001 | real historical replay CANDIDATE | rows 204-238; `2026-05-04T09:30:00-04:00` to `2026-05-08T15:30:00-04:00` | GLD dxLink 1H RTH, 35 source rows, `America/New_York` | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv`; bounded review says low/retest area on 2026-05-04 near `413.2801`, 2026-05-05 base with `417.9050` to `421.1300` range, recovery through 2026-05-06/2026-05-07 into `437.4200` window high, and 2026-05-08 pullback rows. CSV source observations: first open `418.815`, final close `433.795`, window high `437.42`, window low `413.2801`. | Ideal CANDIDATE / NEEDS REVIEW | bullish/call-side candidate if later review confirms | pullback/retest into recovery CANDIDATE | trigger zone TO REVIEW: recovery through the 2026-05-06/2026-05-07 `433.1900` to `437.4200` area; candle/timeframe rule TO REVIEW: completed 1H RTH recovery/hold; invalidation area TO REVIEW: 2026-05-04 low zone near `413.2801` if accepted. | Final Ideal identity UNCONFIRMED; EMA/trend context UNCONFIRMED; 24H/daily context UNCONFIRMED; macro/IV/event context UNCONFIRMED; exact trigger/invalidation UNCONFIRMED; final stage/verdict/blockers/cautions UNCONFIRMED. | unavailable 24H/macro/IV/event context TO REVIEW; possible extension after recovery TO REVIEW. | TO REVIEW whether the 2026-05-07 recovery is fresh or already extended by later rows. | READY FOR WORKSHEET; NOT READY FOR FIXTURE until row-by-row review. | Candidate only; no final Ideal proof claimed. |
- SAFE_FAST_GLD_IDEAL_001_CHART_ONLY_OUTCOME_REVIEW.md:62:- Window ID: `GLD-WINDOW-IDEAL-001`
- SAFE_FAST_GLD_IDEAL_001_REAL_HISTORICAL_REPLAY_REVIEW.md:38:- Window ID: `GLD-WINDOW-IDEAL-001`
- SAFE_FAST_GLD_IDEAL_001_REPLAY_FIXTURE_OUTPUT_VALIDATION_REVIEW.md:43:- Window ID: `GLD-WINDOW-IDEAL-001`
- SAFE_FAST_GLD_IDEAL_001_REPLAY_FIXTURE_SPECIFICATION_REVIEW.md:46:- Window ID: `GLD-WINDOW-IDEAL-001`
- SAFE_FAST_GLD_IDEAL_001_REPLAY_READINESS_REVIEW.md:37:- Mapped window ID: `GLD-WINDOW-IDEAL-001`
- SAFE_FAST_GLD_IDEAL_001_SETUP_TIME_ROW_ACCEPTANCE_WORKSHEET.md:32:- Source window: GLD-WINDOW-IDEAL-001
- SAFE_FAST_REAL_HISTORICAL_IWM_GLD_MISSING_EVIDENCE_INVENTORY.md:167:- SAFE_FAST_BUILD_STATE.md:6433:- **Selected Ideal candidate window:** `GLD-WINDOW-IDEAL-001`; rows 204-238; `2026-05-04T09:30:00-04:00` to `2026-05-08T15:30:00-04:00`; 35 rows.
- SAFE_FAST_REAL_HISTORICAL_IWM_GLD_MISSING_EVIDENCE_INVENTORY.md:168:- SAFE_FAST_BUILD_STATE.md:6462:- **Ideal candidate worksheet row:** `GLD-SAMPLE-IDEAL-001`; source window `GLD-WINDOW-IDEAL-001`; rows 204-238; `2026-05-04T09:30:00-04:00` to `2026-05-08T15:30:00-04:00`; 35 rows; CANDIDATE / NEEDS REVIEW only.
- SAFE_FAST_REAL_HISTORICAL_IWM_GLD_MISSING_EVIDENCE_INVENTORY.md:215:- SAFE_FAST_GLD_BOUNDED_SOURCE_WINDOW_SELECTION_REVIEW.md:54:| GLD-WINDOW-IDEAL-001 | real historical replay candidate | Ideal CANDIDATE | bullish/call-side candidate if later review confirms | 204-238 | `2026-05-04T09:30:00-04:00` | `2026-05-08T15:30:00-04:00` | 35 | Source window shows a low/retest area on 2026-05-04 near `413.2801`, a 2026-05-05 base with `417.9050` to `421.1300` range, and recovery through 2026-05-06/2026-05-07 into a `437.4200` window high before 2026-05-08 pullback rows. | Expected setup type: Ideal CANDIDATE only; direction: bullish if later row-by-row review confirms; candidate stage: pullback/retest into recovery; trigger zone to review: recovery through the 2026-05-06/2026-05-07 `433.1900` to `437.4200` area; candle/timeframe rule: completed 1H RTH recovery/hold; invalidation area: 2026-05-04 low zone near `413.2801` if later review accepts it; fresh/stale/spent question: whether the 2026-05-07 recovery is fresh or already extended; blocker/caution questions: unavailable 24H/macro/IV/event context. | Final Ideal identity, trend/EMA context, exact trigger, exact invalidation, final stage/verdict, blockers/cautions, 24H/daily, macro, IV, event context. | READY FOR WORKSHEET; NOT READY FOR FIXTURE until row-by-row review. | Candidate only; selected because the bounded source rows show retest/recovery shape, not validated setup proof. |
- SAFE_FAST_REAL_HISTORICAL_IWM_GLD_MISSING_EVIDENCE_INVENTORY.md:218:- SAFE_FAST_GLD_CHART_ONLY_OUTCOME_PHASE_PLANNING_REVIEW.md:59:| GLD Ideal 001 | `SAFE_FAST_GLD_IDEAL_001_REPLAY_FIXTURE_OUTPUT_VALIDATION_REVIEW.md` | `GLD-SAMPLE-IDEAL-001` | `GLD-WINDOW-IDEAL-001` | rows 204-238 | `2026-05-04T09:30:00-04:00` to `2026-05-08T15:30:00-04:00` | 35 | PASS; `Ideal: 6`, `NO_TRADE: 3`, `PENDING: 3` |
- SAFE_FAST_REAL_HISTORICAL_IWM_GLD_MISSING_EVIDENCE_INVENTORY.md:464:- SAFE_FAST_GLD_CHART_ONLY_OUTCOME_PHASE_PLANNING_REVIEW.md:59:| GLD Ideal 001 | `SAFE_FAST_GLD_IDEAL_001_REPLAY_FIXTURE_OUTPUT_VALIDATION_REVIEW.md` | `GLD-SAMPLE-IDEAL-001` | `GLD-WINDOW-IDEAL-001` | rows 204-238 | `2026-05-04T09:30:00-04:00` to `2026-05-08T15:30:00-04:00` | 35 | PASS; `Ideal: 6`, `NO_TRADE: 3`, `PENDING: 3` |
