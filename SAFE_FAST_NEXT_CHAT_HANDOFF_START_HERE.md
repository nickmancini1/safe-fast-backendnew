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

Project day and date: Day 52, 2026-06-23.

Current technical checkpoint: Day 52 replay-only numeric rule candidate layer, kept separate from the accepted unresolved numeric trigger/invalidation blockers.

Latest verified commit at Day 52 task start: `e20c67167b05bd981f040eda3308f288867c01e7`.

Current technical package: `SAFE_FAST_DAY52_REPLAY_ONLY_NUMERIC_RULE_CANDIDATES_RESULT.md`, `historical_signal_replay/results/day52_replay_only_numeric_rule_candidates.json`, `historical_signal_replay/results/day52_replay_only_numeric_rule_candidates_manifest.json`, `historical_signal_replay/results/day52_replay_only_numeric_rule_candidates_setup_time_review.json`, `historical_signal_replay/day52_replay_only_numeric_rule_candidates.py`, `watcher_foundation/day52_replay_only_numeric_rule_candidates_validator.py`, `tests/test_day52_replay_only_numeric_rule_candidates.py`, plus accepted references `SAFE_FAST_DAY52_NUMERIC_TRIGGER_INVALIDATION_RESULT.md`, `historical_signal_replay/results/day52_numeric_trigger_invalidation.json`, `SAFE_FAST_DAY52_FULL_SESSION_RECOGNITION_MANIFEST_RESULT.md`, `historical_signal_replay/results/day52_full_session_recognition_manifest.json`, and `historical_signal_replay/results/day52_full_session_setup_time_review.json`.

Exact active task: `SAFE_FAST_DAY52_REPLAY_ONLY_NUMERIC_RULE_CANDIDATES_CODEX_TASK.md`.

Active task exists: yes.

Exact active objective: resolve the remaining family-specific numeric trigger and invalidation rule gaps before any setup-qualified full-session recognition claim or OPRA/economic work.

Current accepted full-session manifest result: sessions scanned `1`; rows scanned `751`; unique timestamps `390`; recognition records `2253`. Per setup family: rejected `389`, duplicate `361`, blocked by missing evidence `1`, setup-qualified `0`, selected winner `0`, suppressed `0`, developing at session end `0`, recognition-layer executable `0`. Accepted numeric values established `0`; accepted numeric values unresolved `6`. Current provisional replay-only result: setup-qualified-under-provisional `3`, selected winner `1`, suppressed `2`, recognition-layer executable `1`, trade candidates `0`, selected contracts `0`, eligible entries `0`, recorded entries `0`; profitability proof `NO`; paper/live eligibility `NO`.

What is fixed: the repo now has complete chronological accepted-mode layer-1 accounting for the SPY March 16, 2026 one-minute session, exact family-field accepted numeric blockers, and a separate deterministic `PROVISIONAL_REPLAY_ONLY` candidate layer. Candidate A setup-bar range produces trigger `668.360000000` and invalidation `667.870000000` for Ideal, Clean Fast Break, and Continuation from the primary setup-time row. Candidate B and Candidate C are explicitly blocked by missing accepted structure-boundary and named-level fields. Validators and focused tests pass.

What remains unproven: accepted full-session setup-qualified recognition is still blocked because no accepted local rule promotes Candidate A, B, or C into a frozen family trigger/invalidation contract. The provisional values are research evidence only, not accepted numeric rules. No accepted numeric trigger, accepted numeric invalidation, trade candidate, selected contract, eligible entry, recorded entry, OPRA layer, costed backtest, exit evaluation, net P&L, proof, profitability, readiness, promotion, paper eligibility, or live eligibility is established.

Exact remaining blockers: `NUMERIC_RULE_UNRESOLVED_IDEAL_TRIGGER`, `NUMERIC_RULE_UNRESOLVED_IDEAL_INVALIDATION`, `NUMERIC_RULE_UNRESOLVED_CLEAN_FAST_BREAK_TRIGGER`, `NUMERIC_RULE_UNRESOLVED_CLEAN_FAST_BREAK_INVALIDATION`, `NUMERIC_RULE_UNRESOLVED_CONTINUATION_TRIGGER`, and `NUMERIC_RULE_UNRESOLVED_CONTINUATION_INVALIDATION`. OPRA remains separate layer-2/layer-3 economic evidence and was not used or downloaded.

Schwab status: Schwab Trader API access remains pending approval/credential configuration unless a later repo result says otherwise. No Schwab authentication, token write, endpoint call, order, account, or fill action is part of the active task.

Exact next task: decide whether to promote, revise, or reject the `PROVISIONAL_REPLAY_ONLY` setup-bar range candidate for each family with explicit accepted-rule regression cases before any accepted setup-qualified full-session recognition claim or OPRA/economic work.

## Current technical objective

The active technical task is the completed Day 52 replay-only numeric candidate layer. It processed the complete SPY March 16, 2026 raw one-minute underlying OHLCV session and preserved accepted replay/regression boundaries while adding separate provisional Candidate A setup-bar range values.

The current result is deterministic recognition/lifecycle accounting plus provisional research evidence only. It must not be read as accepted setup-qualified approval, trade-candidate approval, selected-contract approval, or profitability evidence. Explicit family-specific numeric trigger/invalidation promotion rules are required before any accepted setup-qualified full-session recognition claim; OPRA and costs remain later economic layers.

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

Current repo totals: valid trades captured `1`; true no-trades `4`; missing-data or exact-data-required cases `10` in the preserved scorecard; Day 52 accepted mode has full-session recognition accounting with `3` known setup-time records blocked by six exact family-field numeric rule blockers; Day 52 provisional mode has `3` setup-qualified-under-provisional records, `1` selected winner, and `2` suppressed records; unresolved cases `0`; missed valid trades `0`; invalid trades allowed `0`; winners `1`; losers `0`; profitability proof `NO`; paper/live eligibility `NO`.

Safety rejection and positive-trade capture are equal build objectives.

## Exact current task

Exact active task: `SAFE_FAST_DAY52_REPLAY_ONLY_NUMERIC_RULE_CANDIDATES_CODEX_TASK.md`.

It defined and implemented deterministic replay-only numeric rule candidates for the complete-session underlying recognition manifest. Covered scope is SPY March 16, 2026 only, with Ideal, Clean Fast Break, and Continuation setup families.

Measurable output: a provisional numeric result and provisional full-session manifest showing `1` session, `751` rows, `2253` recognition records, Candidate A values trigger `668.360000000` and invalidation `667.870000000` for all three families, Candidate B/C exact missing-field blockers, deterministic comparison, setup-time review field exclusion, strict no-trade behavior, profitability proof `NO`, paper/live eligibility `NO`, and no paid-data download, OPRA/economic work, proof, readiness, paper, or live expansion.

After Codex runs, the user should paste Codex's `Baseline`, `Fixed`, `Blocked`, `Next`, `Tests`, and changed-files summary.
