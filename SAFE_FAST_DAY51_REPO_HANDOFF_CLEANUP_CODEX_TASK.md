# SAFE-FAST Day 51 Repo Handoff Cleanup — Codex Task

## Required startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then inspect:

1. Local branch, HEAD, and full Git status.
2. `SAFE_FAST_PROJECT_DASHBOARD.md`
3. `SAFE_FAST_PROJECT_RULE_INDEX.md`
4. `SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt`
5. Every handoff currently identified as current.
6. The newest technical result and task files referenced by the control files.
7. The current SPY one-minute replay-mapping package.
8. Existing future-chat consistency tests.

Local Git is the source of truth.

The expected technical direction is currently:

- Valid SPY one-minute OHLCV evidence exists.
- The current technical result concerns mapping that evidence into frozen
  SAFE-FAST setup fields.
- The likely next technical task is:
  `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_ACCEPTED_SETUP_REPLAY_PATH_DECISION_CODEX_TASK.md`

Verify all of that from the repo. Do not assume it when local files disagree.

Record every pre-existing modified or untracked file before making changes.

Preserve the complete pre-existing technical package.

Do not discard, restore, rewrite, stage, commit, or otherwise damage technical
work that already exists.

This task changes the repo handoff system only.

Do not modify trading rules, recognition logic, execution logic, production,
Railway, deployment, broker, account, order, credential, `.env`, or live files.

Do not commit or push.

## Objective

Build one permanent repo-contained handoff system with this workflow:

1. The user pastes one short block into a new chat.
2. The new chat asks the user to run one short repo-status script.
3. The script reports the current repo state and exact active task.
4. The new chat continues that task without asking the user to explain the
   project, workflow, Codex, PowerShell, or prior work.
5. The complete handoff remains in the repo.
6. Old handoffs remain historical and cannot be mistaken for current state.

## Canonical handoff files

Create or update exactly these canonical files:

1. `SAFE_FAST_NEXT_CHAT_HANDOFF_START_HERE.md`
2. `SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt`
3. `scripts/safe_fast_new_chat_status.ps1`
4. `tests/test_day51_next_chat_handoff_consistency.py`
5. `SAFE_FAST_DAY51_REPO_HANDOFF_CLEANUP_RESULT.md`

Update:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`

There must be exactly:

- one current full handoff;
- one current intro block;
- one startup-status script;
- one active technical task.

Stable current filenames:

- Full handoff:
  `SAFE_FAST_NEXT_CHAT_HANDOFF_START_HERE.md`
- User-paste block:
  `SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt`
- Startup script:
  `scripts/safe_fast_new_chat_status.ps1`

Day-numbered handoffs are historical snapshots.

Do not create a second competing current handoff.

Do not delete historical handoffs.

## Build-state current section

Add or update this exact delimited section in
`SAFE_FAST_BUILD_STATE.md`:

`<!-- SAFE_FAST_CURRENT_STATE_BEGIN -->`

and:

`<!-- SAFE_FAST_CURRENT_STATE_END -->`

Inside it, include one line for each field:

- `PROJECT_DAY:`
- `PROJECT_DATE:`
- `ACTIVE_OBJECTIVE:`
- `ACTIVE_TASK:`
- `ACTIVE_TASK_PURPOSE:`
- `PROVEN_SUMMARY:`
- `UNPROVEN_SUMMARY:`
- `CURRENT_FUNNEL_TOTALS:`
- `CURRENT_TECHNICAL_PACKAGE:`
- `CURRENT_TECHNICAL_RESULT:`
- `SCHWAB_STATUS:`
- `DATA_SOURCE_REGISTRY:`
- `NEXT_ACTION:`

Use the actual current repo state.

Do not hardcode branch or HEAD in this section. The startup script obtains them
directly from Git.

The named active task must exist.

## Full current handoff

Create or update:

`SAFE_FAST_NEXT_CHAT_HANDOFF_START_HERE.md`

It must contain these sections.

### Start here

State:

- This is SAFE-FAST build and replay work.
- Repo: `safe-fast-backendnew`.
- Local Git is the source of truth.
- Read `SAFE_FAST_BUILD_STATE.md` before every Codex or code task.
- Run the startup-status script before assigning work.
- The user will not explain completed work again.

### Current verified state

Using the repo, state:

- project day and date;
- current technical checkpoint;
- clean or dirty status at task startup;
- pre-existing technical package;
- exact active task;
- whether that task exists;
- exact active objective;
- current funnel totals;
- proven behavior;
- unproven behavior;
- Schwab status;
- exact next action.

Do not copy stale values from an older handoff.

### Current technical objective

Explain the current technical task in plain English.

When confirmed by the repo, explain that the task must:

- use the downloaded SPY one-minute bars;
- map those bars into the frozen SAFE-FAST setup fields;
- rerun the three SPY setup-family opportunities twice;
- report setup-qualified candidates, trade candidates, selected contracts,
  eligible entries, and recorded entries.

Use the actual repo task when it has advanced.

### Real progress measurement

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

### Communication contract

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
- explain “what is this?” in one sentence;
- state directly when the user pasted a command instead of its output;
- request only missing lines when output is partial;
- identify the exact failure when a command fails;
- continue from repo state without making the user repeat the project.

### PowerShell contract

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

### Codex contract

Standard launch:

`codex.cmd -c 'windows.sandbox="unelevated"' --sandbox workspace-write --ask-for-approval never "Read .\SAFE_FAST_BUILD_STATE.md first, then read and execute .\EXACT_TASK_FILE.md exactly."`

Add network access only for a required external cost check or approved
download.

Use hidden credential prompts.

Keep secrets out of output and tracked files.

### Data-source hierarchy

State:

- SAFE-FAST frozen local rules create Ideal, Clean Fast Break, and Continuation
  labels.
- Databento is the primary historical underlying and options source.
- OPRA `definition` supplies contract identity.
- OPRA `cmbp-1` supplies exact quote-update freshness.
- `cbbo-1s` is a validated fallback when one-second evidence is sufficient.
- TCBBO is supplemental and cannot alone establish quote freshness.
- Charles Schwab is the live broker and authority for account state, orders,
  order status, and fills.
- Schwab Trader API access is pending approval unless the repo shows it has
  advanced.
- Tastytrade is a secondary options and volatility check.
- TradingView is a manual chart and context check.
- ALFRED and official agencies supply historical macro and event evidence.
- `SAFE_FAST_DATA_SOURCE_REGISTRY.md` is the canonical source registry.

### Safety and positive-trade state

State the current repo totals for:

- valid trades captured;
- true no-trades;
- missing-data or exact-data-required cases;
- unresolved cases;
- missed valid trades;
- invalid trades allowed;
- winners;
- losers;
- readiness or promotion status.

State that safety rejection and positive-trade capture are equal build
objectives.

### Exact current task

Name the exact active task.

State:

- what it must implement;
- what measurable output it must produce;
- what output the user should paste after Codex runs.

## One-block intro file

Replace `SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt` with one short block that the user
can paste directly into a new chat.

The block must say:

- This is SAFE-FAST build work.
- The repo is the source of truth.
- The user will not explain the project again.
- Full handoff:
  `SAFE_FAST_NEXT_CHAT_HANDOFF_START_HERE.md`
- Build-state authority:
  `SAFE_FAST_BUILD_STATE.md`
- The active task comes from the repo.
- Communication uses plain English and one action at a time.
- The new chat's first response must ask the user to run exactly:

`Set-Location "C:\Users\nickm\Desktop\New folder\safe-fast-backendnew"`
`powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\safe_fast_new_chat_status.ps1"`

After the user returns that output, the new chat must:

1. state the actual baseline;
2. identify the exact active task;
3. give one action;
4. continue without restarting discovery;
5. avoid making the user explain completed work.

Keep this block concise and self-contained.

## Startup-status script

Create:

`scripts/safe_fast_new_chat_status.ps1`

The script must:

- locate the repo root from its own location;
- change to the repo root;
- print no more than 80 lines;
- print:
  - project day;
  - project date;
  - branch;
  - HEAD;
  - latest three commits;
  - exact clean or dirty status;
  - canonical handoff path;
  - canonical intro-block path;
  - active objective;
  - active task;
  - whether the active task exists;
  - proven summary;
  - unproven summary;
  - funnel totals;
  - current technical package;
  - current technical result;
  - Schwab status;
  - next action;
- read the delimited current-state section from
  `SAFE_FAST_BUILD_STATE.md`;
- report a clear conflict when a required field is missing;
- report a clear conflict when the active task is missing;
- avoid entire-document output;
- avoid secrets;
- exit nonzero on a genuine consistency conflict.

Use labels that a new chat can parse easily.

## Rule-index cleanup

Update `SAFE_FAST_PROJECT_RULE_INDEX.md` so it clearly identifies:

- current full handoff;
- current intro block;
- current startup script;
- current consistency test;
- current active task;
- historical handoff section.

Mark all older Day-numbered handoffs as historical.

For older handoff files still presented as current, add this one-line banner at
the top:

`SUPERSEDED: Read SAFE_FAST_NEXT_CHAT_HANDOFF_START_HERE.md`

Preserve their original historical content below the banner.

## Dashboard cleanup

Update `SAFE_FAST_PROJECT_DASHBOARD.md` with:

- active objective;
- active task;
- current technical result;
- current funnel totals;
- current handoff;
- current intro block;
- startup-status script;
- next action.

## Consistency tests

Create:

`tests/test_day51_next_chat_handoff_consistency.py`

It must verify:

1. The canonical handoff exists.
2. The canonical intro block exists.
3. The startup script exists.
4. The rule index names exactly one current handoff.
5. The rule index names exactly one current intro block.
6. Older handoffs are historical.
7. The intro block points to the full handoff.
8. The intro block points to the startup script.
9. The build-state current section contains every required field.
10. The active task exists.
11. Active-task references agree across build state, dashboard, rule index, and
    handoff.
12. The handoff contains the communication contract.
13. The handoff contains the PowerShell contract.
14. The handoff defines measurable progress.
15. The handoff contains the data-source hierarchy.
16. The handoff contains Schwab's current status.
17. The handoff states the current technical objective.
18. The startup script obtains branch and HEAD dynamically.
19. The startup script is bounded.
20. The current package contains no stale current-commit claim.

## Technical-package protection

Before editing, record every pre-existing changed file.

In the result document, separate:

- pre-existing technical package;
- handoff files changed by this task;
- generated caches;
- metadata-only rerun files.

Preserve the pending SPY replay-mapping package exactly.

Do not alter the current technical task.

## Required tests

Run:

1. `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_new_chat_status.ps1`
2. `python -B -m unittest discover -s tests -p "test_day51_next_chat_handoff_consistency.py"`
3. Existing future-chat consistency tests.
4. Existing source-registry tests.
5. Current SPY replay-mapping focused tests.
6. Evidence content validator.
7. Package-to-intake bridge.
8. Safe checks using the execution-policy bypass.
9. `git diff --check`.

Remove generated `__pycache__` directories.

## Result document

Create:

`SAFE_FAST_DAY51_REPO_HANDOFF_CLEANUP_RESULT.md`

Report:

- Baseline
- Branch and HEAD
- Pre-existing status
- Active objective
- Active task
- Canonical handoff
- Canonical intro block
- Startup script
- Superseded handoffs
- Funnel totals
- Proven behavior
- Unproven behavior
- Schwab status
- Files created
- Files updated
- Pre-existing technical package preserved
- Tests
- Exact next action

## Final summary

Return only:

- Baseline
- Fixed
- Blocked
- Next
- Tests
- Files changed
- Pre-existing technical package preserved
- Canonical handoff file
- Canonical intro block
- Startup-status script
- Active task
- Current funnel totals
- Exact next action