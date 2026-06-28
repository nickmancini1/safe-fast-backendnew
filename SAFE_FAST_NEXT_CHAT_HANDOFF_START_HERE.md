<!-- SAFE_FAST_PRIORITY_DRIFT_GATE_BEGIN -->
## SAFE-FAST PRIORITY DRIFT GATE

This is the top red-flag gate. Every future chat must answer it before any baseline, explanation, or command.

Priority check: Am I efficiently working on the current priority task and not drifting?

Required answer format:
- Priority check: YES or NO.
- Current priority: one sentence.
- This step is: Substance or busy work.
- Why allowed: one sentence.
- If NO: stop and correct before giving a command.

Substance means the step directly moves SAFE-FAST toward one of: cost approval, vendor-ready request, contract selection, option evidence, entry/exit/P&L, exact rejection, exact blocker closure, or regression protection.

Busy work means another worksheet, task file, broad scan, handoff tweak, stale-output cleanup, or documentation update that does not unlock the current priority.

Hard rule: Busy work is forbidden unless current `git status --short` proves it physically blocks the priority task.

Top red flag: if the assistant cannot explain in one sentence how the next command advances the current priority, it must not give the command.

### Vertical execution gate

A substance command must complete the full vertical step whenever possible:

1. create or update the actual result,
2. run the required focused tests,
3. run `git diff --check`,
4. commit the expected files,
5. print the final decision, next action, latest commit, and clean status.

Do not split a substance step into repeated readback, summary, worksheet, or confirmation commands.

A read-only command is allowed only when it is a real hard gate:
- current Git status is unknown or dirty,
- a test failed and exact failure lines are needed,
- paid cost approval is needed,
- vendor/API auth is missing,
- vendor call approval is needed,
- script arguments are unknown and running the script would mutate files,
- current machine-readable result is missing or unparseable.

After one read-only gate command, the next response must either:
- run the next substance command,
- ask for operator approval on a paid/vendor action,
- or close the blocker exactly.

Top anti-drift rule: if the information already exists in the latest machine-readable result, do not ask for another readback just to summarize it. Use it to advance the priority step.
<!-- SAFE_FAST_PRIORITY_DRIFT_GATE_END -->


# SAFE-FAST Next Chat Handoff - Start Here

<!-- SAFE_FAST_SOURCE_TO_DECISION_OPERATING_LOOP_START -->
## MANDATORY SOURCE-TO-DECISION OPERATING LOOP

Read `SAFE_FAST_SOURCE_TO_DECISION_OPERATING_LOOP.md` before any task.

Required opening report: Baseline; Active objective; Raw-data source; SAFE-FAST translation required; Blocker category; Candidate state; Next executable step; Why this is the fastest safe path; Required tests; Commit proof.

One-active-objective rule: Do not replace, broaden, or abandon the active objective unless a completed result or hard blocker exists. A direction change must name the blocker category and smallest replacement action.

Blocker categories: `RAW_DATA_GAP`, `RULE_DEFINITION_GAP`, `CALCULATOR_OR_IMPLEMENTATION_GAP`, `CANDIDATE_QUALITY_GAP`, `ECONOMIC_EVIDENCE_GAP`, `REGRESSION_OR_PROOF_GAP`.

Source ownership: Databento supplies primary raw historical underlying and option evidence; tastytrade/dxLink is secondary raw data only; official agencies / ALFRED supply macro and event facts; Schwab is future live-data and broker/account/order authority after access approval. SAFE-FAST alone calculates setup identity, trigger, invalidation, freshness, stale/spent, blocker, stage, winner, no-trade, entry, exit, and profitability-related decisions. Vendors provide evidence; SAFE-FAST provides labels and decisions.

Candidate funnel: scan broad bounded pool; fast field screen; remove duplicates and known structural blockers; rank by completeness; deep-review strongest batch only; drop/replace weak candidates quickly; one-candidate work only when complete enough for economic proof.

No-documentation-loop rule: no new review/plan/status/handoff merely restating a known blocker. Documentation is allowed only when it establishes a decision, closes contradiction, defines a testable contract, records a completed result, repairs canonical handoff, or enables the immediate executable step.

PowerShell / Codex freeze recovery: if waiting for hidden input, enter it. If not waiting for input and output stops, press Ctrl+C once. Do not rerun. Inspect exit status, logs, partial files, checkpoint manifest, sizes, hashes, parseability, Git status, and whether the step already completed. Rerun only for a specific verified missing or failed result. Never repeat paid requests, completed vendor schemas, Codex tasks, test batches, or downloads merely because terminal output was quiet.

Build/test/commit rule: focused tests; affected regressions; validators; safe checks; `git diff --check`; exact commit when authorized; empty git status when authorized. Uncommitted accepted work is unfinished work.

Red-flag stop conditions: same blocker repeated twice; more data proposed when rule/implementation is missing; one candidate repeatedly reviewed without advancing; more documentation than evidence/code/tests/economic results; canonical docs contradict machine-readable results; active objective cannot be explained in one sentence.

Progress metrics: complete economic replays; valid entries; exact rejections/no-trades; exits and net P&L; blockers permanently closed; candidates screened versus promoted; tests passed; clean commits.

Final question: Is this task moving SAFE-FAST closer to a tested profitable trading plan, or only making it sound more sophisticated?
<!-- SAFE_FAST_SOURCE_TO_DECISION_OPERATING_LOOP_END -->

<!-- SAFE_FAST_OPRA_670C_RECOVERY_START -->
## CURRENT DAY 55 SPY 670C RESULT

Read:

1. `SAFE_FAST_OPRA_670C_RECOVERY_HANDOFF_START_HERE.md`
2. `SAFE_FAST_OPRA_670C_RECOVERY_CODEX_TASK.md`
3. `historical_signal_replay/results/day52_spy_opra_contract_resolution.json`
4. `SAFE_FAST_DAY52_SPY_OPRA_670C_CONTRACT_RESOLUTION_RESULT.md`

Verified result:

- raw definition DBN remains local-only
- 669C is unlisted
- frozen-rule selected contract is `SPY   260330C00670000`
- instrument ID is `1241515301`
- publisher ID is `30`
- do not redownload definitions

Day 55 local evaluation:

- result doc: `SAFE_FAST_DAY55_SPY_670C_ENTRY_EXIT_PNL_EVALUATION_RESULT.md`
- machine result: `historical_signal_replay/results/day55_spy_670c_entry_exit_pnl_evaluation.json`
- entry result: `NO_ENTRY_EXACT_REJECTION`
- first blocker: `open_interest_statistics_zero_rows`
- exit result: `EXIT_BLOCKED`
- gross P&L: `None`
- net P&L: `None`
- complete end-to-end backtest: `NO`

Next path:

operator review of the exact no-entry result. Do not request more data under the completed Day 55 task unless a later explicit task authorizes it.

Profitability proof: `NO`.

Paper/live eligibility: `NO`.
<!-- SAFE_FAST_OPRA_670C_RECOVERY_END -->

<!-- SAFE_FAST_OPERATOR_TIME_PROTECTION_START -->
## MANDATORY OPERATOR-TIME PROTECTION

Every future chat must read and follow this rule before issuing commands.

If PowerShell stops progressing, press Ctrl+C once. Do not rerun. First inspect logs, partial files, output, manifest, and Git status.

Expanded freeze-recovery rule:

1. First determine whether PowerShell is waiting for hidden input.
2. If not, press Ctrl+C once.
3. Do not assume success or failure.
4. Inspect process status, logs, partial files, output, manifest, sizes, hashes, parseability, and Git status.
5. Rerun only for a specific verified missing or failed result.
6. Never repeat a paid request or completed schema merely because output was quiet.

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

Active task: `NONE_PENDING_OPERATOR_REVIEW`

Cleanup completed at `3210251`: the mandatory source-to-decision / anti-rabbit-hole operating contract is installed. Preserve the accepted March 16, 2026 SPY 670C exact no-entry result. Current objective: operator review chooses the next fastest safe economic replay path; no active code/Codex task is authorized yet.

Do not return to broad candidate hunting.

Use the committed local Day 55 result first unless a later explicit task supersedes it.

Do not wait for Schwab.

A network/proxy failure is not proof that data is unavailable.

Future chats must start from the Day 55 exact no-entry result unless a later explicit task supersedes it.

Latest current result: `SAFE_FAST_DAY55_SPY_670C_ENTRY_EXIT_PNL_EVALUATION_RESULT.md`.

Latest machine result: `historical_signal_replay/results/day55_spy_670c_entry_exit_pnl_evaluation.json`.

Latest verified commit at task start: `37cda01 Make option-evidence backtest mandatory`.

Dirty status after the Day 55 canonical workflow cleanup task: `DIRTY` until operator review/commit. Modified tracked files include `SAFE_FAST_BUILD_STATE.md`, `SAFE_FAST_NEXT_CHAT_HANDOFF_START_HERE.md`, `SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt`, `SAFE_FAST_PROJECT_DASHBOARD.md`, `SAFE_FAST_PROJECT_RULE_INDEX.md`, `scripts/safe_fast_new_chat_status.ps1`, and `tests/test_day51_next_chat_handoff_consistency.py`. New file: `SAFE_FAST_SOURCE_TO_DECISION_OPERATING_LOOP.md`. The task file `NONE_PENDING_OPERATOR_REVIEW` remains the expected preexisting untracked task file.

Selected winner: `DAY52-SPY-2026-03-16-CLEAN-FAST-BREAK-20260316T133000Z-P39`.

Contract-selection result: `CONTRACT_RESOLVED_FROM_EXISTING_LOCAL_DEFINITION_EVIDENCE`; rejected candidate is `SPY   260330C00669000` because it is unlisted; selected contract is `SPY   260330C00670000`, expiration `2026-03-30`, strike `670`, call, instrument ID `1241515301`, publisher ID `30`.

Tastytrade result: `FIELD_LIMITATION_BLOCKED`; local helper proves underlying OHLCV only, not historical option bid/ask.

Databento result: local manifest is `SUCCESS`; completed/reused schemas are `cmbp-1`, `tcbbo`, `trades`, and `statistics`; no `definition` request is needed.

Complete entry-window result: quotes are present and inspected; first quote at `2026-03-16T13:31:00.010890Z` has bid `9.970000000`, ask `10.040000000`, spread `0.070000000`, and valid displayed sizes.

Stage reached: `NO_ENTRY_EXACT_REJECTION`.

Remaining blocker: `open_interest_statistics_zero_rows`; statistics has zero rows, so the accepted open-interest rule blocks entry. Exit and net P&L are blocked.

Tests passed: focused SPY 670C downloader tests; focused Day 52 option-evidence tests; Databento OPRA normalizer tests; Day 52 option-evidence validator; `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`; `git diff --check`.

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

Project day and date: Day 55, 2026-06-26.

Current technical checkpoint: Day 55 local selected-contract economic evaluation, with the accepted March 16 SPY Clean Fast Break selected winner stopped at exact no-entry blocker `open_interest_statistics_zero_rows`.

Latest verified commit at current option-evidence task start: `37cda01 Make option-evidence backtest mandatory`.

Current technical package: `SAFE_FAST_DAY55_SPY_670C_ENTRY_EXIT_PNL_EVALUATION_RESULT.md`, `historical_signal_replay/results/day55_spy_670c_entry_exit_pnl_evaluation.json`, `historical_signal_replay/day55_spy_670c_entry_exit_pnl_evaluation.py`, `watcher_foundation/day55_spy_670c_entry_exit_pnl_evaluation_validator.py`, and `tests/test_day55_spy_670c_entry_exit_pnl_evaluation.py`; accepted layer-1 and Day 52 input references remain available.

Exact active task: `NONE_PENDING_OPERATOR_REVIEW`.

Active task exists: yes.

Exact active objective: operator review chooses the next fastest safe economic replay path while preserving the Day 55 SPY 670C exact no-entry result.

Current accepted full-session manifest result: sessions scanned `1`; rows scanned `751`; unique timestamps `390`; recognition records `2253`. Per setup family: rejected `389`, duplicate `361`, blocked by missing evidence `0`; Clean Fast Break selected winner `1`; Ideal suppressed `1`; Continuation suppressed `1`; setup-qualified layer-1 records `3`; recognition-layer executable `1`. Accepted numeric values established `6`; accepted numeric values unresolved `0`. Current provisional replay-only result remains separate: setup-qualified-under-provisional `3`, selected winner `1`, suppressed `2`, recognition-layer executable `1`, trade candidates `0`, selected contracts `0`, eligible entries `0`, recorded entries `0`; profitability proof `NO`; paper/live eligibility `NO`.

What is fixed: the repo now has complete chronological accepted-mode layer-1 accounting for the SPY March 16, 2026 one-minute session, a binding audit proving legitimate shared setup-time row use, and accepted Candidate A numeric trigger/invalidation rules for Ideal, Clean Fast Break, and Continuation. Trigger is `668.360000000`; invalidation is `667.870000000`; setup timestamp is `2026-03-16T13:30:00Z`; source row index is `2` / publisher `39`. Validators and focused tests pass.

What remains unproven: no valid entry, recorded entry, exit evaluation, gross P&L, net P&L, proof, profitability, readiness, paper eligibility, or live eligibility is established.

Exact remaining blocker: `open_interest_statistics_zero_rows`. The local Day 55 manifest is `SUCCESS`, selected-contract identity matches, entry-window quotes and trade volume are present, but statistics/OI has zero rows, so the accepted open-interest rule blocks entry. Do not request `definition`; committed definition evidence already rejected 669C and selected 670C.

Schwab status: Schwab Trader API access remains pending approval/credential configuration unless a later repo result says otherwise. No Schwab authentication, token write, endpoint call, order, account, or fill action is part of the active task.

Exact next task: operator decision only. Do not broad-hunt candidates, do not create another provisional layer, do not wait for Schwab, and do not claim P&L, profitability, paper eligibility, or live eligibility.

## Current technical objective

The active technical objective is operator review to choose the next fastest safe economic replay path while preserving the bounded local Day 55 SPY 670C selected-contract economic evaluation result.

The current result is `NO_ENTRY_EXACT_REJECTION`. Contract selection is resolved from committed local definition evidence: 669C is unlisted and selected contract `SPY   260330C00670000` matches instrument ID `1241515301` / publisher ID `30`. Entry-window quotes and trade volume are present, but statistics/OI has zero rows, so the accepted open-interest rule blocks entry with `open_interest_statistics_zero_rows`. Exit, gross P&L, and net P&L remain blocked. This must not be read as valid entry, P&L, profitability proof, paper eligibility, or live eligibility.

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

Exact active task: `NONE_PENDING_OPERATOR_REVIEW`.

Cleanup completed at `3210251`; do not recreate the completed task file. The current task state is operator review only, with no active code/Codex task authorized yet.

Measurable output: result doc `SAFE_FAST_DAY55_SPY_670C_ENTRY_EXIT_PNL_EVALUATION_RESULT.md` and machine result `historical_signal_replay/results/day55_spy_670c_entry_exit_pnl_evaluation.json` record selected winner `DAY52-SPY-2026-03-16-CLEAN-FAST-BREAK-20260316T133000Z-P39`, selected contract `SPY   260330C00670000`, entry result `NO_ENTRY_EXACT_REJECTION`, first blocker `open_interest_statistics_zero_rows`, exit result `EXIT_BLOCKED`, gross P&L `None`, net P&L `None`, complete end-to-end backtest `NO`, profitability proof `NO`, paper/live eligibility `NO`, and no vendor call, broker work, proof, readiness, paper, or live expansion.

After Codex runs, the user should paste Codex's `Baseline`, `Fixed`, `Blocked`, `Next`, `Tests`, and changed-files summary.
