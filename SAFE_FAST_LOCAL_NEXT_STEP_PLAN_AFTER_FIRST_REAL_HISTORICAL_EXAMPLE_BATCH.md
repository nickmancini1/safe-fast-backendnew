# SAFE-FAST Local Next Step Plan After First Real Historical Example Batch

## 1. Plan Status

- **Status:** docs-only plan correction complete; ready for assistant review before commit.
- **Baseline:** patch8.
- **Day context:** Day 35.
- **Latest local commit before this correction:** `e03c792 Add real historical missing evidence inventory plan`.
- **Work mode:** build work only, not live trade chat.
- **Highest priority:** viability proof before optimization.
- **Purpose:** define the next smallest evidence-backed step after the first real historical example batch produced 2 worked examples and 2 missing-evidence examples.

## 2. Boundary Statement

This is a docs-only planning task.

No code, tests, `main.py`, engine logic, Railway/deploy files, production/live backend, live data, controlled shadow data, watcher loops, alerts, generated reports/logs, broker/order/account/options/P&L, account sizing, live trade decisions, secrets, environment files, GitHub writes, commits, rule changes, optimization, profitability claims, historical success claims, final viability claims, or production/live readiness claims are allowed.

## 3. Current First-Batch Result

The first real historical example batch contains exactly 4 local in-memory real historical examples:

- `Ideal` / `SPY`: worked chart/setup behavior.
- `Clean Fast Break` / `QQQ`: worked chart/setup behavior.
- `Continuation` / `IWM`: missing evidence / inconclusive.
- `Ideal` / `GLD`: missing evidence / inconclusive.

The system correctly did not fabricate proof. Profitability, final viability, actual historical success, live readiness, production readiness, and optimization remain unproven.

## 4. Exact Missing Evidence For IWM Continuation

IWM Continuation is source-backed as a real candidate example, but it is not accepted worked or failed proof.

Current candidate evidence:

- Fixture: `historical_signal_replay/fixtures/first_real_iwm_continuation_replay_v1_fixture.json`.
- Candidate row: `continuation_triggered_signal_stage_candidate`.
- Candidate timestamp: `2026-04-30T15:30:00-04:00`.
- Chart-only review: `SAFE_FAST_IWM_CONTINUATION_001_CHART_ONLY_OUTCOME_REVIEW.md`.
- Source movement evidence exists for `2026-05-01T09:30:00-04:00` through `2026-05-01T15:30:00-04:00`.

Exact missing accepted evidence:

- accepted final signal row with `final_verdict: TRADE`;
- accepted `trigger_state: triggered`;
- no primary blocker on the accepted row;
- numeric trigger level;
- exact trigger basis for the Continuation shelf break;
- numeric invalidation level;
- exact invalidation basis for the Continuation shelf/base;
- accepted fresh/stale/spent determination at the candidate signal-stage row;
- final blocker/caution priority after trigger-card review;
- session-boundary carry-forward decision if it affects trigger freshness;
- terminal outcome rule inputs, including chart risk denominator for R-based outcome scoring.

Existing repo-backed IWM facts do not satisfy those fields. The fixture explicitly keeps trigger level, invalidation, shelf/base, fresh/spent, session-boundary, macro, IV, event, and related context fields as `TO_REVIEW` / `UNCONFIRMED`, with `final_verdict: PENDING`, `trigger_state: completed_shelf_break_candidate_TO_REVIEW`, `primary_blocker: trigger_level_TO_REVIEW`, and null trigger/invalidation on the candidate row.

## 5. Exact Missing Evidence For GLD Ideal

GLD Ideal is source-backed as a real candidate example, but it is not accepted worked or failed proof.

Current candidate evidence:

- Fixture: `historical_signal_replay/fixtures/first_real_gld_ideal_replay_v1_fixture.json`.
- Candidate row: `ideal_recovery_confirmation_candidate`.
- Candidate timestamp: `2026-05-06T09:30:00-04:00`.
- Chart-only review: `SAFE_FAST_GLD_IDEAL_001_CHART_ONLY_OUTCOME_REVIEW.md`.
- Source movement evidence exists for rows 219-238, `2026-05-06T10:30:00-04:00` through `2026-05-08T15:30:00-04:00`.

Exact missing accepted evidence:

- accepted final signal row with `final_verdict: TRADE`;
- accepted `trigger_state: triggered`;
- no primary blocker on the accepted row;
- completed-candle approval state;
- numeric trigger level;
- exact trigger basis for the Ideal recovery/confirmation setup;
- numeric invalidation level;
- exact invalidation basis;
- accepted fresh/stale/spent determination after recovery/hold/follow-through review;
- final blocker/caution priority after trigger-card review;
- terminal follow-through/failure/time-stop rule inputs;
- chart risk denominator for R-based MFE/MAE and outcome scoring.

Existing repo-backed GLD facts do not satisfy those fields. The fixture and chart-only review explicitly keep accepted signal row, trigger level, invalidation, completed-candle approval, final trigger state, blocker priority, and fresh/stale/spent determination unconfirmed. The candidate/reference row has `final_verdict: PENDING`, `trigger_state: setup_confirming_TO_REVIEW`, `primary_blocker: completed_candle_hold_unconfirmed`, and null trigger/invalidation.

## 6. Does The Repo Already Contain The Missing Evidence?

Current answer: not as accepted proof.

The repo contains useful source-backed candidate and post-candidate movement evidence for both examples:

- source CSV windows;
- lifecycle fixtures;
- fixture validation reviews;
- chart-only outcome reviews;
- explicit no-hindsight boundaries;
- explicit `TO_REVIEW`, `UNCONFIRMED`, null, and blocker fields.

The repo does not currently contain accepted SPY/QQQ-style generated-outcome prerequisites for IWM Continuation or GLD Ideal. Candidate rows and review-limited movement are not the same as accepted final signal rows with numeric trigger, numeric invalidation, freshness/final signal fields, and terminal outcome inputs.

## 7. If Evidence Is Found Later, How To Add It Without Hindsight

Only add evidence if a later bounded task can point to repo-backed, pre-outcome or at-signal evidence that existed at the setup timestamp or accepted signal timestamp.

Allowed evidence sources for a future implementation step:

- existing fixture rows or replay output rows that already contain accepted final signal fields;
- existing generated replay summaries/reports that already contain accepted signal rows and numeric trigger/invalidation fields;
- existing source CSV rows only for OHLCV context, not for inventing trigger labels after the fact;
- existing docs/reviews only when they cite the exact source row and field values.

No-hindsight rules:

- do not use later favorable or adverse price movement to choose trigger or invalidation;
- do not convert `PENDING`, `TO_REVIEW`, null, or `UNCONFIRMED` into accepted proof without a source-backed row;
- do not infer freshness from post-candidate success;
- do not backfill blocker removal from the later chart path;
- preserve setup-time evidence separately from after-setup evidence;
- leave `future_evidence_used_to_define_setup=False`.

If accepted evidence is found, the future code change should update only the relevant in-memory example fields and tests, with evidence references naming the exact source row/report path. The example should then be classified based on the accepted evidence and after-setup evidence, not based on whether the chart later looked favorable.

## 8. If Evidence Is Not Found

If accepted evidence is not found, both examples must remain missing-evidence/inconclusive.

Required behavior:

- keep `outcome_evidence_state` as `unavailable_evidence` or `missing_evidence`;
- keep `outcome_result_state` as `inconclusive`;
- keep unavailable fields explicit;
- preserve IWM Continuation missing fields separately from GLD Ideal missing fields;
- do not promote either example to worked, failed, stale, invalidated, or pending proof;
- keep next fix paths focused on evidence collection/validation, not optimization.

## 9. Next Smallest Evidence-Backed Fix

The next smallest evidence-backed fix is a docs-only evidence inventory for the two missing examples before any code change.

Future task shape:

- exact inventory file: `SAFE_FAST_REAL_HISTORICAL_IWM_GLD_MISSING_EVIDENCE_INVENTORY.md`;
- allowed future inventory edits only:
  - `SAFE_FAST_REAL_HISTORICAL_IWM_GLD_MISSING_EVIDENCE_INVENTORY.md`;
  - `SAFE_FAST_BUILD_STATE.md`;
  - `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`;
- inspect only existing repo sources for IWM Continuation and GLD Ideal;
- do not invent evidence;
- answer what exact evidence is missing for IWM Continuation;
- answer what exact evidence is missing for GLD Ideal;
- answer whether accepted trigger evidence exists;
- answer whether accepted invalidation evidence exists;
- answer whether accepted freshness/final-signal evidence exists;
- answer whether accepted blocker evidence exists;
- answer whether accepted terminal outcome evidence exists;
- answer where evidence exists, if it exists;
- if evidence does not exist, keep the examples missing-evidence/inconclusive;
- name the smallest next evidence-backed fix;
- list every candidate row and any accepted row candidate;
- record whether each required field is present, null, `TO_REVIEW`, `UNCONFIRMED`, or absent;
- decide separately for IWM Continuation and GLD Ideal whether accepted proof exists in the repo;
- if proof exists, plan the smallest later in-memory sample update and regression test;
- if proof does not exist, preserve missing-evidence status and plan the next bounded real historical example instead of forcing these two through.

The planned inventory file, if later approved, should be docs-only and should not modify fixtures, code, tests, reports, source CSVs, generated outputs, `main.py`, engine logic, Railway/deploy files, live data paths, broker/order/account/options/P&L, account sizing, optimization logic, production files, or GitHub.

## 10. Future Implementation Gate

Do not change `watcher_foundation/setup_outcome_historical_sample_path.py` or tests for IWM/GLD until a review names exact accepted evidence fields and exact source references.

Future implementation is allowed only if the inventory proves accepted evidence exists. Then the implementation must be limited to:

- `watcher_foundation/setup_outcome_historical_sample_path.py`;
- `tests/test_setup_outcome_historical_sample_path.py`;
- `SAFE_FAST_BUILD_STATE.md`;
- `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`.

Required future tests if implementation is approved:

- IWM/GLD remain missing evidence when accepted fields are unavailable;
- any promoted example cites exact accepted source evidence;
- no-hindsight separation remains intact;
- worked/failed classification is based on accepted setup fields plus after-setup evidence;
- no profitability, final viability, historical success, live readiness, production readiness, optimization, rule-change, generated-report, or side-effect claim appears.

## 11. Still Unproven

This plan does not prove:

- final trading-plan viability;
- profitability;
- actual historical success;
- all 12 setup-type-plus-symbol pairs;
- failed real historical examples;
- repeated worked/failed patterns;
- repeated fix paths;
- lower-tier final readiness;
- controlled shadow readiness;
- live data readiness;
- alerts;
- generated reports/logs;
- broker/order/account behavior;
- option P&L;
- account sizing;
- production/Railway/live backend readiness;
- live trade decisions.

## 12. Next Objective After This Plan

If this corrected plan is accepted and committed, create `SAFE_FAST_REAL_HISTORICAL_IWM_GLD_MISSING_EVIDENCE_INVENTORY.md` as a docs-only IWM/GLD missing-evidence inventory from existing repo sources only.

The next docs-only inventory task may edit only `SAFE_FAST_REAL_HISTORICAL_IWM_GLD_MISSING_EVIDENCE_INVENTORY.md`, `SAFE_FAST_BUILD_STATE.md`, and `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`.

Do not run tests for that docs-only inventory unless explicitly requested. Do not change code, tests, fixtures, source CSVs, reports, generated outputs, watcher behavior, live data paths, broker behavior, optimization logic, production files, or `main.py`. Check existing repo sources only, do not invent evidence, and keep IWM Continuation and GLD Ideal missing-evidence/inconclusive unless accepted evidence exists in the repo.
