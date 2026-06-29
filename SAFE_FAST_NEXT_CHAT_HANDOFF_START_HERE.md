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

Day 55 quote/trade/statistics evidence and target-mismatch replay:

- result doc: `SAFE_FAST_DAY55_SPY_670C_ENTRY_EXIT_PNL_EVALUATION_RESULT.md`
- machine result: `historical_signal_replay/results/day55_spy_670c_entry_exit_pnl_evaluation.json`
- current HEAD before uncommitted fix: `a91920b`
- approved/downloaded quote/trade/statistics evidence succeeded: `true`
- request count: `32`
- required schemas: `cmbp-1`, `tcbbo`, `trades`, and `statistics`
- forbidden schema: `definition`
- SPY 670C target: `SPY   260330C00670000`
- target present in Day 55 download manifest: `false`
- entry status: `NO_ENTRY_EXACT_REJECTION`
- first blocker: `target_contract_not_in_day55_download_manifest`
- old blocker audit trail: `open_interest_statistics_zero_rows` was not closed
- exit status: `EXIT_BLOCKED`
- gross P&L: `None`
- net P&L: `None`

Next path:

stop after the target-mismatch handoff fix unless a later explicit task chooses the next evidence action. Do not claim entry, exit, P&L, proof, or paper/live eligibility.

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

Active task: `SAFE_FAST_DAY55_TARGET_MISMATCH_HANDOFF_FIX_TASK.md`

Current objective: finish the uncommitted Day 55 target-mismatch handoff fix. Current HEAD before the uncommitted fix is `a91920b`. The approved/downloaded 32-request Day 55 Databento `OPRA.PILLAR` quote/trade/statistics evidence package succeeded, but it does not contain the SPY 670C replay target.

Do not return to broad candidate hunting.

Use the committed local Day 55 result first unless a later explicit task supersedes it.

Do not wait for Schwab.

A network/proxy failure is not proof that data is unavailable.

Future chats must start from the completed Day 55 target-mismatch exact rejection unless a later explicit task supersedes it.

Latest current result: `SAFE_FAST_DAY55_SPY_670C_ENTRY_EXIT_PNL_EVALUATION_RESULT.md`.

Latest machine result: `historical_signal_replay/results/day55_spy_670c_entry_exit_pnl_evaluation.json`.

Current HEAD before the uncommitted Day 55 target-mismatch fix: `a91920b`.

Dirty status for this task is expected until the operator reviews the uncommitted Day 55 target-mismatch handoff fix. Do not commit.

Selected winner: `DAY52-SPY-2026-03-16-CLEAN-FAST-BREAK-20260316T133000Z-P39`.

Contract-selection result: `CONTRACT_RESOLVED_FROM_EXISTING_LOCAL_DEFINITION_EVIDENCE`; rejected candidate is `SPY   260330C00669000` because it is unlisted; selected contract is `SPY   260330C00670000`, expiration `2026-03-30`, strike `670`, call, instrument ID `1241515301`, publisher ID `30`.

Tastytrade result: `FIELD_LIMITATION_BLOCKED`; local helper proves underlying OHLCV only, not historical option bid/ask.

Databento result: approved/downloaded quote/trade/statistics evidence succeeded for 32 requests; schemas are `cmbp-1`, `tcbbo`, `trades`, and `statistics`; `definition` is forbidden.

Stage reached: `NO_ENTRY_EXACT_REJECTION`.

Remaining blocker: `target_contract_not_in_day55_download_manifest`. The SPY 670C replay target is `SPY   260330C00670000`, and the downloaded Day 55 manifest does not contain it. The old blocker `open_interest_statistics_zero_rows` is preserved as not closed. Entry timestamp, entry price, exit, gross P&L, and net P&L are `None`.

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

Current technical checkpoint: Day 55 SPY 670C target-mismatch exact rejection after the approved/downloaded 32-request Databento `OPRA.PILLAR` quote/trade/statistics evidence package.

Latest verified commit at current option-evidence task start: `37cda01 Make option-evidence backtest mandatory`.

Current technical package: `SAFE_FAST_DAY55_SPY_670C_ENTRY_EXIT_PNL_EVALUATION_RESULT.md`, `historical_signal_replay/results/day55_spy_670c_entry_exit_pnl_evaluation.json`, `historical_signal_replay/day55_spy_670c_entry_exit_pnl_evaluation.py`, `watcher_foundation/day55_spy_670c_entry_exit_pnl_evaluation_validator.py`, and `tests/test_day55_spy_670c_entry_exit_pnl_evaluation.py`; Day 55 downloaded quote/trade/statistics manifest remains available.

Exact active task: `SAFE_FAST_DAY55_TARGET_MISMATCH_HANDOFF_FIX_TASK.md`.

Active task exists: yes.

Exact active objective: finish the uncommitted Day 55 target-mismatch handoff fix without committing.

Current accepted full-session manifest result: sessions scanned `1`; rows scanned `751`; unique timestamps `390`; recognition records `2253`. Per setup family: rejected `389`, duplicate `361`, blocked by missing evidence `0`; Clean Fast Break selected winner `1`; Ideal suppressed `1`; Continuation suppressed `1`; setup-qualified layer-1 records `3`; recognition-layer executable `1`. Accepted numeric values established `6`; accepted numeric values unresolved `0`. Current provisional replay-only result remains separate: setup-qualified-under-provisional `3`, selected winner `1`, suppressed `2`, recognition-layer executable `1`, trade candidates `0`, selected contracts `0`, eligible entries `0`, recorded entries `0`; profitability proof `NO`; paper/live eligibility `NO`.

What is fixed: the repo now has complete chronological accepted-mode layer-1 accounting for the SPY March 16, 2026 one-minute session, a binding audit proving legitimate shared setup-time row use, and accepted Candidate A numeric trigger/invalidation rules for Ideal, Clean Fast Break, and Continuation. Trigger is `668.360000000`; invalidation is `667.870000000`; setup timestamp is `2026-03-16T13:30:00Z`; source row index is `2` / publisher `39`. Validators and focused tests pass.

What remains unproven: no valid entry, recorded entry, exit evaluation, gross P&L, net P&L, proof, profitability, readiness, paper eligibility, or live eligibility is established.

Exact remaining blocker: `target_contract_not_in_day55_download_manifest`. Do not request `definition`; preserve that `open_interest_statistics_zero_rows` was not closed.

Schwab status: Schwab Trader API access remains pending approval/credential configuration unless a later repo result says otherwise. No Schwab authentication, token write, endpoint call, order, account, or fill action is part of the active task.

Exact next task: stop after the target-mismatch handoff fix unless a later explicit task is provided. Do not broad-hunt candidates, create another provisional layer, wait for Schwab, or claim entry/exit/P&L, profitability, paper eligibility, or live eligibility.

## Current technical objective

The active technical objective is the Day 55 SPY 670C target-mismatch exact rejection after approved/downloaded quote/trade/statistics evidence.

The current result is `NO_ENTRY_EXACT_REJECTION` with first blocker `target_contract_not_in_day55_download_manifest`. The approved/downloaded package contains 32 Databento `OPRA.PILLAR` quote/trade/statistics requests, but not the SPY 670C target `SPY   260330C00670000`. This must not be read as valid entry, exit, P&L, profitability proof, paper eligibility, or live eligibility.

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

Exact active task: `SAFE_FAST_DAY55_TARGET_MISMATCH_HANDOFF_FIX_TASK.md`.

Current HEAD before the uncommitted fix is `a91920b`. The current task state is the Day 55 target-mismatch handoff fix; do not commit.

Measurable output: result doc `SAFE_FAST_DAY55_SPY_670C_ENTRY_EXIT_PNL_EVALUATION_RESULT.md` and machine result `historical_signal_replay/results/day55_spy_670c_entry_exit_pnl_evaluation.json` record entry status `NO_ENTRY_EXACT_REJECTION`, first blocker `target_contract_not_in_day55_download_manifest`, target `SPY   260330C00670000`, target present in Day 55 download manifest `false`, old blocker `open_interest_statistics_zero_rows` not closed, exit status `EXIT_BLOCKED`, gross P&L `None`, net P&L `None`, profitability proof `NO`, paper/live eligibility `NO`, and no broker work, proof, readiness, paper, or live expansion.

After Codex runs, the user should paste Codex's `Baseline`, `Fixed`, `Blocked`, `Next`, `Tests`, and changed-files summary.
## Day 55 SPY 670C target-mismatch replay status

- Result: `historical_signal_replay/results/day55_spy_670c_entry_exit_pnl_evaluation.json`.
- Summary: `SAFE_FAST_DAY55_SPY_670C_ENTRY_EXIT_PNL_EVALUATION_RESULT.md`.
- Test: `tests/test_day55_spy_670c_entry_exit_pnl_evaluation.py`.
- Validator: `watcher_foundation/day55_spy_670c_entry_exit_pnl_evaluation_validator.py`.
- Current HEAD before uncommitted fix: `a91920b`.
- Decision: `NO_ENTRY_EXACT_REJECTION`.
- Request count: `32`.
- Required schemas: `cmbp-1`, `tcbbo`, `trades`, and `statistics`.
- Forbidden schema: `definition`.
- Approved/downloaded evidence succeeded: `true`.
- SPY 670C target: `SPY   260330C00670000`.
- Target present in Day 55 download manifest: `false`.
- First blocker: `target_contract_not_in_day55_download_manifest`.
- Old blocker audit trail: `open_interest_statistics_zero_rows` was not closed.
- Entry status: `NO_ENTRY_EXACT_REJECTION`.
- Exit status: `EXIT_BLOCKED`.
- Gross P&L: `None`.
- Net P&L: `None`.
- Profitability proof: `NO`.
- Paper/live eligibility: `NO`.
- Next action: stop after this handoff fix unless a later explicit task is provided; no entry/exit/P&L claim.
