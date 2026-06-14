# SAFE-FAST Day 41 project speed layer task

Baseline:
- Latest commit before this task: 5ebc7cb Add QQQ gap context regression fixtures

First action:
- Read SAFE_FAST_BUILD_STATE.md first.

Goal:
- Add the project speed-and-efficiency layer.
- Make future chats move faster without lowering quality.
- Do not erase existing docs.
- Assess existing files first, then update only what makes sense.

Create:
- scripts/safe_fast_run_safe_checks.ps1
- SAFE_FAST_CODEX_TASK_TEMPLATES.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_DAY41_PROJECT_SPEED_LAYER_REVIEW.md
- historical_signal_replay/candidate_packets/README.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md

Update:
- SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_RULE_INDEX.md

The speed layer must include:

1. One safe-check runner
- Runs safe local checks only.
- Runs Databento OPRA normalizer tests if present.
- Validates JSON fixtures if present.
- Runs Python compile checks for helper modules if present.
- Skips missing checks clearly.
- Prints PASS / FAIL / SKIPPED summary.
- Does not touch live, broker, order, account, Railway, secrets, or raw data.

2. Reusable Codex task templates
Include templates for:
- data validation
- rule decision
- fixture creation
- calculator + tests
- evidence-field mapping
- regression
- dashboard update

3. Project dashboard
Must show:
- current checkpoint
- active objective
- completed breakthroughs
- current blockers
- next single action
- data-source status
- QQQ CFB status
- remaining project-wide rules
- what is not proven
- what must not be claimed

4. Candidate packets
Create a QQQ packet with:
- candidate id
- symbol
- setup type
- signal time
- previous close/open/gap
- Databento data status
- gap fixture status
- current blockers
- next needed rule/test
- no proof / no readiness status

5. Future-chat instructions
Future chats must know:
- read build state first
- then dashboard
- then rule index
- use task templates
- use safe-check runner before/after code changes
- use candidate packets
- do not restart old discovery if repo already records the answer
- answer the user directly in plain English
- no project-dead language; weak or failed results mean diagnose and repair

6. Review
Create a review that says:
- what was added
- what was already partly covered
- what was redundant
- what was clarified
- what was intentionally not deleted
- what future chats should read first

Allowed writes:
- SAFE_FAST_DAY41_PROJECT_SPEED_LAYER_CODEX_TASK.md
- SAFE_FAST_DAY41_PROJECT_SPEED_LAYER_REVIEW.md
- SAFE_FAST_CODEX_TASK_TEMPLATES.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- scripts/safe_fast_run_safe_checks.ps1
- historical_signal_replay/candidate_packets/README.md
- historical_signal_replay/candidate_packets/QQQ_REAL_HISTORICAL_CLEAN_FAST_BREAK_001.md
- SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_RULE_INDEX.md

Do not write:
- raw Databento CSV/DBN/manifest files
- evidence fills
- calculator code
- backtest code
- trade-selection code
- P&L
- main.py
- live/engine/broker/order/account/Railway files
- .env or secrets

Final response:
Baseline:
Fixed:
Blocked:
Next:
Tests:
Files changed:
