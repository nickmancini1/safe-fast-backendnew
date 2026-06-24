# SAFE-FAST Next Chat Handoff - Start Here

<!-- SAFE_FAST_OPERATOR_TIME_PROTECTION_START -->
## MANDATORY OPERATOR-TIME PROTECTION

Every future chat must read and follow this rule before issuing commands.

Before any Codex run, network request, data request, download, broad test batch, repository-wide scan, or other potentially long-running or mutating command:

1. Perform a fast read-only preflight first.
2. Verify branch, HEAD, git status, exact input files, exact output path resolved from code or configuration, output parent directory, required environment-variable names, executable availability, and whether the requested result already exists.
3. Do not launch the long-running or mutating command until the preflight passes.
4. Keep requested pasteback to 3?6 decisive lines unless actual failure details are required.
5. Never claim success from an echoed label, variable, or previous chat statement. Verify the real process exit code, actual output-file existence, parseable output content, expected git changes, and final git status.
6. When a command fails, inspect its existing log and partial output first. Do not rerun it automatically.
7. Do not repeat completed tests, Codex work, downloads, cost requests, or data requests unless a specific verified evidence gap requires the rerun.
8. Use the smallest bounded command and smallest relevant test set.
9. Do not send giant command blocks when a short read-only check can resolve uncertainty.
10. A task is complete only when expected files are verified, required checks pass, the correct commit exists, and `git status --short` is empty.
11. Protect the operator?s time. After any failed assumption, diagnose it with a read-only check before attempting another operation.

This rule applies regardless of the current technical objective and supersedes any older workflow instruction that would cause unnecessary reruns or unverified long-running work.
<!-- SAFE_FAST_OPERATOR_TIME_PROTECTION_END -->

<!-- SAFE_FAST_MANDATORY_OPTION_BACKTEST_START -->
## CURRENT MANDATORY OBJECTIVE

Active task: `SAFE_FAST_EXISTING_SETUP_OPTION_EVIDENCE_END_TO_END_BACKTEST_CODEX_TASK.md`

Continue the accepted March 16, 2026 setup through deterministic contract selection, the complete allowed option-price window, entry, exit, costs, and net P&L.

Do not return to broad candidate hunting.

Use existing local evidence first, tastytrade second, and Databento for exact OPRA fallback.

Do not wait for Schwab.

A network/proxy failure is not proof that data is unavailable.

Future chats must continue this objective until committed evidence produces a costed result or one exact priced data request.

Latest current result: `SAFE_FAST_EXISTING_SETUP_OPTION_EVIDENCE_END_TO_END_BACKTEST_RESULT.md`.

Latest machine result: `historical_signal_replay/results/day52_existing_setup_option_evidence_end_to_end_backtest.json`.

Latest verified commit at task start: `37cda01 Make option-evidence backtest mandatory`.

Dirty status after this Codex task: `DIRTY` until operator commit. Modified tracked files: `SAFE_FAST_BUILD_STATE.md`, `SAFE_FAST_NEXT_CHAT_HANDOFF_START_HERE.md`, `SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt`, `SAFE_FAST_PROJECT_DASHBOARD.md`, `SAFE_FAST_PROJECT_RULE_INDEX.md`, `SAFE_FAST_DATA_SOURCE_REGISTRY.md`, and `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`. New untracked files: `SAFE_FAST_EXISTING_SETUP_OPTION_EVIDENCE_END_TO_END_BACKTEST_RESULT.md`, `historical_signal_replay/day52_existing_setup_option_evidence_end_to_end_backtest.py`, `historical_signal_replay/results/day52_existing_setup_option_evidence_end_to_end_backtest.json`, `watcher_foundation/day52_existing_setup_option_evidence_end_to_end_backtest_validator.py`, `tests/test_day52_existing_setup_option_evidence_end_to_end_backtest.py`, and `scripts/safe_fast_day52_existing_setup_databento_cost_request.py`.

Selected winner: `DAY52-SPY-2026-03-16-CLEAN-FAST-BREAK-20260316T133000Z-P39`.

Contract-selection result: `BLOCKED_DEFINITION_EVIDENCE_MISSING`; deterministic candidate if OPRA definition confirms listing is `SPY   260330C00669000`, expiration `2026-03-30`, strike `669`, call.

Tastytrade result: `FIELD_LIMITATION_BLOCKED`; local helper proves underlying OHLCV only, not historical option bid/ask.

Databento result: `NETWORK_EXECUTION_BLOCKED`; run `python scripts/safe_fast_day52_existing_setup_databento_cost_request.py` from an operator environment with `SAFE_FAST_DB_AUTH` and working HTTPS.

Complete entry-window result: `BLOCKED_COMPLETE_OPTION_PRICE_WINDOW_MISSING`; accepted entry window is `2026-03-16T13:31:00Z` through `2026-03-16T13:36:00Z`; first valid option price is not established.

Stage reached: `EXACT_EVIDENCE_REQUEST`.

Remaining blocker: operator-run Databento cost output and then approved selected-contract OPRA definition/quote/trade/statistics evidence for the complete entry and exit windows.

Tests passed: focused Day 52 option-evidence tests; CFB selector/trade-rule/backtest tests; affected Day 50, Day 51, and Day 52 regressions; affected validators; `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`; `git diff --check`.

Profitability proof: `NO`.

Paper/live eligibility: `NO`.
<!-- SAFE_FAST_MANDATORY_OPTION_BACKTEST_END -->

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

Current technical checkpoint: Day 52 existing-setup option evidence request, with the accepted March 16 SPY Clean Fast Break selected winner advanced to an exact Databento priced-request blocker.

Latest verified commit at current option-evidence task start: `37cda01 Make option-evidence backtest mandatory`.

Current technical package: `SAFE_FAST_EXISTING_SETUP_OPTION_EVIDENCE_END_TO_END_BACKTEST_RESULT.md`, `historical_signal_replay/results/day52_existing_setup_option_evidence_end_to_end_backtest.json`, `historical_signal_replay/day52_existing_setup_option_evidence_end_to_end_backtest.py`, `watcher_foundation/day52_existing_setup_option_evidence_end_to_end_backtest_validator.py`, `tests/test_day52_existing_setup_option_evidence_end_to_end_backtest.py`, and `scripts/safe_fast_day52_existing_setup_databento_cost_request.py`; accepted layer-1 references remain `SAFE_FAST_DAY52_FAMILY_NUMERIC_BINDING_AND_PROMOTION_RESULT.md`, `historical_signal_replay/results/day52_family_numeric_binding_and_promotion.json`, `SAFE_FAST_DAY52_FULL_SESSION_RECOGNITION_MANIFEST_RESULT.md`, and `historical_signal_replay/results/day52_full_session_recognition_manifest.json`.

Exact active task: `SAFE_FAST_EXISTING_SETUP_OPTION_EVIDENCE_END_TO_END_BACKTEST_CODEX_TASK.md`.

Active task exists: yes.

Exact active objective: continue the accepted March 16, 2026 SPY selected winner through option evidence and end-to-end backtest completion, or stop only at one exact priced evidence request.

Current accepted full-session manifest result: sessions scanned `1`; rows scanned `751`; unique timestamps `390`; recognition records `2253`. Per setup family: rejected `389`, duplicate `361`, blocked by missing evidence `0`; Clean Fast Break selected winner `1`; Ideal suppressed `1`; Continuation suppressed `1`; setup-qualified layer-1 records `3`; recognition-layer executable `1`. Accepted numeric values established `6`; accepted numeric values unresolved `0`. Current provisional replay-only result remains separate: setup-qualified-under-provisional `3`, selected winner `1`, suppressed `2`, recognition-layer executable `1`, trade candidates `0`, selected contracts `0`, eligible entries `0`, recorded entries `0`; profitability proof `NO`; paper/live eligibility `NO`.

What is fixed: the repo now has complete chronological accepted-mode layer-1 accounting for the SPY March 16, 2026 one-minute session, a binding audit proving legitimate shared setup-time row use, and accepted Candidate A numeric trigger/invalidation rules for Ideal, Clean Fast Break, and Continuation. Trigger is `668.360000000`; invalidation is `667.870000000`; setup timestamp is `2026-03-16T13:30:00Z`; source row index is `2` / publisher `39`. Validators and focused tests pass.

What remains unproven: no selected contract is confirmed, no complete entry quote window exists, no eligible entry, recorded entry, exit evaluation, net P&L, proof, profitability, readiness, paper eligibility, or live eligibility is established.

Exact remaining blocker: run the operator Databento cost script and obtain approved selected-contract OPRA `definition`, `cmbp-1`, `tcbbo`, `trades`, and `statistics` evidence for `SPY   260330C00669000` across the complete entry window and exit boundary. Network/proxy failure is `NETWORK_EXECUTION_BLOCKED`, not market-data unavailability.

Schwab status: Schwab Trader API access remains pending approval/credential configuration unless a later repo result says otherwise. No Schwab authentication, token write, endpoint call, order, account, or fill action is part of the active task.

Exact next task: continue the same option-evidence objective; use local evidence first, tastytrade second, Databento fallback; apply the existing timing rule to the complete quote window; do not broad-hunt candidates, do not create another provisional layer, do not wait for Schwab, and do not claim P&L until evidence is complete.

## Current technical objective

The active technical task is the existing-setup option evidence and end-to-end backtest path for the accepted March 16, 2026 SPY Clean Fast Break winner. It must continue from the selected winner, preserve duplicate suppression, apply the frozen Clean Fast Break contract and timing rules to the complete quote window, and finish with either entry/exit/net P&L or one exact priced evidence request.

The current result is `EXACT_EVIDENCE_REQUEST`. Contract selection is blocked by missing OPRA definition evidence, the complete entry quote window is missing, tastytrade is field-limited, and Databento network execution is blocked in the sandbox. It must not be read as selected-contract approval, eligible-entry approval, P&L, profitability proof, paper eligibility, or live eligibility.

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

Current repo totals: valid trades captured `1`; true no-trades `4`; missing-data or exact-data-required cases `10` in the preserved scorecard; Day 52 accepted mode has full-session layer-1 accounting with `3` setup-qualified records, `1` selected winner, `2` suppressed records, accepted numeric values established `6`, and unresolved numeric values `0`; Day 52 provisional mode remains separate with `3` setup-qualified-under-provisional records, `1` selected winner, and `2` suppressed records; unresolved cases `0`; missed valid trades `0`; invalid trades allowed `0`; winners `1`; losers `0`; profitability proof `NO`; paper/live eligibility `NO`.

Safety rejection and positive-trade capture are equal build objectives.

## Exact current task

Exact active task: `SAFE_FAST_EXISTING_SETUP_OPTION_EVIDENCE_END_TO_END_BACKTEST_CODEX_TASK.md`.

It applies the existing selected-winner, contract-selection, entry-window, exit, cost, and no-hindsight rules to the accepted SPY March 16, 2026 Clean Fast Break economic winner only.

Measurable output: exact evidence-request result showing selected winner `DAY52-SPY-2026-03-16-CLEAN-FAST-BREAK-20260316T133000Z-P39`, deterministic candidate contract shape `SPY   260330C00669000`, contract-selection status `BLOCKED_DEFINITION_EVIDENCE_MISSING`, complete entry-window status `BLOCKED_COMPLETE_OPTION_PRICE_WINDOW_MISSING`, tastytrade status `FIELD_LIMITATION_BLOCKED`, Databento status `NETWORK_EXECUTION_BLOCKED`, stage `EXACT_EVIDENCE_REQUEST`, profitability proof `NO`, paper/live eligibility `NO`, and no paid-data download, broker work, proof, readiness, paper, or live expansion.

After Codex runs, the user should paste Codex's `Baseline`, `Fixed`, `Blocked`, `Next`, `Tests`, and changed-files summary.
