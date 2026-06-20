# SAFE-FAST Day 49 Grouped Positive-Entry Next Deterministic Candidate Batch - Codex Task

## Startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_SETUP_FIELD_COMPLETION_RESULT.md`
2. `historical_signal_replay/results/day49_grouped_positive_entry_setup_field_completion.json`
3. `historical_signal_replay/fixtures/day49_positive_entry_candidate_expansion_manifest.json`
4. `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`
5. `SAFE_FAST_PROJECT_DASHBOARD.md`
6. `SAFE_FAST_PROJECT_RULE_INDEX.md`

Expected branch: `main`.
Expected status: clean except this task file.

If local Git or canonical control files disagree, stop and identify the exact conflict.

## Objective

Run one deterministic, outcome-blind candidate-batch routing pass after the frozen Day 49 setup-field completion exhausted all eight candidates at `SETUP_QUALIFIED`.

The pass must determine whether any unused, non-protected, non-duplicate, non-dropped, non-control development candidates remain in current local repo evidence. If none remain, document that the current local positive-entry candidate pool is exhausted and route to the smallest bounded evidence-collection or source-row repair task.

## Restrictions

Do not inspect option outcomes.

Do not download data.

Do not create an option setup-time cost check unless a newly selected candidate first reaches `TRADE_CANDIDATE` from accepted local setup-time evidence.

Do not modify production/live backend, `main.py`, Railway/deploy files, broker/order/account code, credentials, `.env`, frozen trading rules, accepted thresholds, raw vendor data, or exit-path data.

Do not claim proof, profitability, readiness, promotion, paper eligibility, live eligibility, or a real trade choice.

## Required Work

- Preserve the eight Day 49 setup-field completion rows as missing-data controls.
- Reuse existing local source rows, candidate screens, packet/replay helpers, and current control docs only.
- Exclude protected holdout rows, existing measured funnel controls, current positive/rejection controls, duplicate source-window signals, dropped rows, and the eight exhausted Day 49 frozen candidates.
- If selecting any new candidates, freeze the selection in a machine-readable manifest and keep selection deterministic and outcome-blind.
- If no eligible unused candidates remain, create a result document that says so plainly and names the smallest bounded next evidence task.

## Required Result

Create a result document named:

`SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_NEXT_DETERMINISTIC_CANDIDATE_BATCH_RESULT.md`

Update build state, dashboard, rule index, and current handoff files only if active state changes.

## Required Tests

Run focused deterministic candidate-batch tests, the Day 49 setup-field completion tests, the Day 49 candidate expansion validator, the existing positive-trade funnel regression batch, relevant family/stage/session tests, evidence validator, package-to-intake bridge, future-chat consistency tests, and `git diff --check`.
