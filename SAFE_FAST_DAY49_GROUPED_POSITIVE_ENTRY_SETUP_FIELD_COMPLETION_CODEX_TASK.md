# SAFE-FAST Day 49 Grouped Positive-Entry Setup-Field Completion - Codex Task

## Startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_CANDIDATE_EXPANSION_RESULT.md`
2. `historical_signal_replay/fixtures/day49_positive_entry_candidate_expansion_manifest.json`
3. `historical_signal_replay/results/day49_positive_entry_candidate_expansion.json`
4. `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`
5. `SAFE_FAST_PROJECT_DASHBOARD.md`
6. `SAFE_FAST_PROJECT_RULE_INDEX.md`

Expected branch: `main`.
Expected status: clean except this task file.

If local Git or canonical control files disagree, stop and identify the exact conflict.

## Objective

Complete a grouped local setup-field review for the eight Day 49 frozen development candidates.

Do not inspect option outcomes, do not download data, and do not create an option setup-time cost check unless a candidate first reaches `TRADE_CANDIDATE` from local setup-time evidence.

## Frozen Candidates

Use exactly the candidates frozen in:

`historical_signal_replay/fixtures/day49_positive_entry_candidate_expansion_manifest.json`

Do not add replacements in this task.

## Required Work

For each frozen candidate, use existing local source rows, signal logs, and packet/replay helpers to fill or explicitly block:

- setup-time row;
- trigger;
- invalidation;
- freshness/final-signal state;
- blocker/caution review;
- no-hindsight boundary;
- session-boundary behavior;
- whether the setup reaches `SETUP_QUALIFIED`;
- whether it reaches `TRADE_CANDIDATE`.

Classify missing fields as missing data, not true no-trades.

## Restrictions

Do not modify production/live backend, `main.py`, Railway/deploy files, broker/order/account code, credentials, `.env`, frozen trading rules, accepted thresholds, raw vendor data, or exit-path data.

Do not download data.

Do not claim proof, profitability, readiness, promotion, paper eligibility, live eligibility, or a real trade choice.

## Required Result

Create a result document named:

`SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_SETUP_FIELD_COMPLETION_RESULT.md`

Update build state, dashboard, rule index, and current handoff files only if active state changes.

## Next Routing

Create exactly one next grouped task based on evidence:

- exact grouped setup-time option cost check only if one or more candidates reach `TRADE_CANDIDATE` and local option evidence remains missing;
- grouped safety repair only if a real invalid allowed trade is found;
- grouped repair only if a missed valid trade is proven;
- another deterministic candidate batch only if the frozen candidate set is exhausted and unused candidates remain.

## Required Tests

Run focused setup-field completion tests, the Day 49 candidate expansion validator, the existing positive-trade funnel regression batch, relevant family/stage/session tests, evidence validator, package-to-intake bridge, future-chat consistency tests, and `git diff --check`.
