# SAFE-FAST Next Chat Handoff - Start Here

## Start here

This is SAFE-FAST build and replay work.

Repo: `safe-fast-backendnew`.

Local Git is the source of truth. Read `SAFE_FAST_BUILD_STATE.md` before every Codex or code task. Run the startup-status script before assigning work. The user will not explain completed work again.

Run:

```powershell
Set-Location "C:\Users\nickm\Desktop\New folder\safe-fast-backendnew"
powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\safe_fast_new_chat_status.ps1"
```

## Current verified state

Project day and date: Day 51, 2026-06-22.

Current technical checkpoint: Day 50 raw-data positive-entry mapper-to-generation retry over the accepted SPY one-minute OHLCV setup-time packages.

Git status at Day 51 handoff-cleanup startup: dirty before this task. Pre-existing modified and untracked files are recorded in `SAFE_FAST_DAY51_REPO_HANDOFF_CLEANUP_RESULT.md`.

Pre-existing technical package: `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_ACCEPTED_SETUP_REPLAY_REGRESSION_CASES_RESULT.md`, `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_ACCEPTED_SETUP_REPLAY_MAPPER_CODEX_TASK.md`, `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_ACCEPTED_SETUP_REPLAY_PATH_DECISION_RESULT.md`, `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_ACCEPTED_SETUP_REPLAY_REGRESSION_CASES_CODEX_TASK.md`, `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_SETUP_TIME_REPLAY_MAPPING_RESULT.md`, `historical_signal_replay/results/day50_raw_data_positive_entry_setup_time_replay_mapping.json`, `historical_signal_replay/day50_raw_data_positive_entry_setup_time_replay_mapping.py`, `watcher_foundation/day50_raw_data_positive_entry_setup_time_replay_mapping_validator.py`, `tests/test_day50_raw_data_positive_entry_setup_time_replay_mapping.py`, `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_UNDERLYING_SETUP_TIME_COSTED_REQUEST_RESULT.md`, `historical_signal_replay/day50_raw_data_positive_entry_underlying_setup_time_request.py`, `historical_signal_replay/results/day50_raw_data_positive_entry_underlying_setup_time_costed_request.json`, and the updated raw-data generator package.

Exact active task: `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_MAPPER_TO_GENERATION_RETRY_CODEX_TASK.md`.

Active task exists: yes.

Exact active objective: complete the bounded Day 50 SPY mapper-to-generation retry and identify the smallest accepted repair needed before generated-candidate promotion.

Current funnel totals: raw opportunities mapped `3`; exact setup-time field packages established `3`; new generated candidates `0`; new setup-qualified candidates `0`; new trade candidates `0`; new selected contracts `0`; new eligible entries `0`; new recorded entries `0`; exact-generation-contract-required cases `3`; new exact-data-required cases `0`. Existing regression controls remain separate at `13` setup-qualified, `9` trade candidates, `5` selected contracts, `1` eligible entry, and `1` recorded entry.

Proven behavior: valid SPY one-minute OHLCV evidence exists and is chronological for the authorized March 16, 2026 session. The accepted mapper establishes three review-only setup-time field packages and all 17 accepted mapper regression cases pass. The mapper-to-generation retry processed Ideal, Clean Fast Break, and Continuation separately and stopped all three before `generated_candidate` because review-only packages are not accepted generation inputs.

Unproven behavior: no review-only mapper package is accepted as a generated candidate; no new setup-qualified candidate, trade candidate, selected contract, eligible entry, recorded entry, proof, profitability, readiness, promotion, paper eligibility, or live eligibility is established.

Schwab status: Schwab Trader API access remains pending approval/credential configuration unless a later repo result says otherwise. No Schwab authentication, token write, endpoint call, order, account, or fill action is part of the active task.

Exact next action: create `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_REVIEW_ONLY_PACKAGE_TO_CANDIDATE_CONTRACT_CODEX_TASK.md` only if the project wants to define and regression-test a bounded contract that can promote a review-only setup-time package into a generated candidate without weakening frozen rules.

## Current technical objective

The active technical task is the completed bounded mapper-to-generation retry. It processed only the accepted SPY March 16, 2026 raw one-minute OHLCV setup-time packages and preserved the accepted replay/regression cases and field boundaries for `setup_time_row`, `trigger`, `invalidation`, `freshness_final_signal_state`, `blocker_caution_review`, `session_boundary_behavior`, and `no_hindsight_boundary`.

The current result must not be read as candidate-generation approval. A later bounded task would need to define and regression-test a review-only-package-to-generated-candidate contract before any of the three packages can advance.

## Real progress measurement

A task counts as measurable progress when it produces at least one of:

- a new setup-qualified candidate;
- a new trade candidate;
- a new selected contract;
- a new eligible entry;
- a new recorded entry;
- a proven missed valid trade;
- a proven invalid trade allowed;
- a permanently closed blocker with an exact reason and regression test;
- an exact cost-checked request that directly resolves the active blocker.

Every testing batch must report before-and-after funnel totals.

## Communication contract

The next chat must:

- answer the user's direct question first;
- state the action it is taking;
- use plain English;
- explain technical terms immediately;
- give one next action;
- provide one complete PowerShell block when needed;
- request only the smallest output required;
- use brief `Baseline`, `Fixed`, `Blocked`, `Next`, and `Command` sections;
- use one short paragraph when the user is on a phone;
- explain "what is this?" in one sentence;
- state directly when the user pasted a command instead of its output;
- request only missing lines when output is partial;
- identify the exact failure when a command fails;
- continue from repo state without making the user repeat the project.

## PowerShell contract

Every PowerShell response must:

- contain one complete block;
- use exact paths;
- stage exact files only;
- avoid `git add .`;
- run `git diff --check`;
- request only necessary output.

Task creation and Codex launch remain separate steps:

1. Create or update the task.
2. Confirm it exists.
3. Launch Codex in the next interaction.
4. Review Codex's final summary.
5. Inspect exact changed files.
6. Commit the exact validated package.
7. Continue the single evidence-driven next task.

The next chat must not send duplicate commands or competing actions.

## Codex contract

Standard launch:

`codex.cmd -c 'windows.sandbox="unelevated"' --sandbox workspace-write --ask-for-approval never "Read .\SAFE_FAST_BUILD_STATE.md first, then read and execute .\EXACT_TASK_FILE.md exactly."`

Add network access only for a required external cost check or approved download.

Use hidden credential prompts.

Keep secrets out of output and tracked files.

## Data-source hierarchy

- SAFE-FAST frozen local rules create Ideal, Clean Fast Break, and Continuation labels.
- Databento is the primary historical underlying and options source.
- OPRA `definition` supplies contract identity.
- OPRA `cmbp-1` supplies exact quote-update freshness.
- `cbbo-1s` is a validated fallback when one-second evidence is sufficient.
- TCBBO is supplemental and cannot alone establish quote freshness.
- Charles Schwab is the live broker and authority for account state, orders, order status, and fills.
- Schwab Trader API access is pending approval unless the repo shows it has advanced.
- Tastytrade is a secondary options and volatility check.
- TradingView is a manual chart and context check.
- ALFRED and official agencies supply historical macro and event evidence.
- `SAFE_FAST_DATA_SOURCE_REGISTRY.md` is the canonical source registry.

## Safety and positive-trade state

Current repo totals: valid trades captured `1`; true no-trades `4`; missing-data or exact-data-required cases `10` in the preserved scorecard plus `3` new exact-data-required SPY mapping cases; unresolved cases `0`; missed valid trades `0`; invalid trades allowed `0`; winners `1`; losers `0`; readiness or promotion status `not proven and not authorized`.

Safety rejection and positive-trade capture are equal build objectives.

## Exact current task

Exact active task: `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_MAPPER_TO_GENERATION_RETRY_CODEX_TASK.md`.

It retried only the bounded raw one-minute underlying OHLCV evidence setup-time packages through the existing historical generation boundary. Covered scope is SPY March 16, 2026 only, with Ideal, Clean Fast Break, and Continuation setup families.

Measurable output: a bounded retry result showing `3` mapped packages, `0` generated candidates, exact blocker `accepted_mapper_package_review_only_not_generation_input`, deterministic comparison, preserved control totals, and no data, option, exit-path, proof, readiness, paper, or live expansion.

After Codex runs, the user should paste Codex's `Baseline`, `Fixed`, `Blocked`, `Next`, `Tests`, and changed-files summary.
