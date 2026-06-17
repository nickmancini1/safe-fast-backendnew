# SAFE-FAST Day 45 bounded final sprint update task

Baseline:
- Latest commit before this task: 2654e08 Fill SPY Ideal starter evidence batch

First action:
- Read SAFE_FAST_BUILD_STATE.md first.
- Then read SAFE_FAST_PROJECT_DASHBOARD.md.
- Then read SAFE_FAST_PROJECT_RULE_INDEX.md.
- Then read SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt.
- Then read SAFE_FAST_PROJECT_PROOF_PIPELINE.md.
- Then read SAFE_FAST_TRADE_PLAN_COMPLETENESS_GATE.md.

Goal:
- Make the Day 45 user directive explicit and impossible for future chats to miss.
- This is a repo-control update.
- The build must be done correctly.
- The build must also be bounded.
- Day 60 is a progress checkpoint, not a forced finish.
- The next $200 month is the final high-intensity build sprint before moving toward the $20 tier.
- Future work must stay batched.
- Future chats must use plain English.

User directive to preserve:
- Day 1 is May 3, 2026.
- June 16, 2026 was Day 45.
- Day 60 is July 1, 2026.
- Day 61 is after the Day 60 checkpoint.
- Do not cut corners because the calendar is tight.
- Do not let the project run indefinitely.
- Use the time needed for more tested examples and better comparison.
- The target remains a profitable trading plan.
- Weak, failed, missing, unclear, or unprofitable results trigger diagnosis and repair.
- The next $200 month must produce a clear decision package before moving toward the $20 tier.

Plain-English front-door wording future chats must see near the top:
"Day 60 is a progress checkpoint, not the finish line. The build target is a profitable trading plan, and we will not cut corners to hit a date. This project also cannot run indefinitely. The next $200 month is the final high-intensity build sprint before moving toward the $20 tier. Work must stay batched, evidence-backed, cost-controlled, and focused on tested examples, comparison, trade-plan rules, and a clear decision package."

Create:
- SAFE_FAST_DAY45_BOUNDED_FINAL_SPRINT_UPDATE.md
- SAFE_FAST_DAY45_200_TO_20_TIER_TRANSITION_PLAN.md

Update:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt
- SAFE_FAST_PROJECT_PROOF_PIPELINE.md
- SAFE_FAST_TRADE_PLAN_COMPLETENESS_GATE.md

The Day 45 update must include:
1. Timeline:
   - Day 1: May 3, 2026
   - June 16, 2026: Day 45
   - Day 60: July 1, 2026
   - Day 60 is a checkpoint/reporting date

2. Quality rule:
   - No corner-cutting because of the calendar
   - More tested examples and better comparison are allowed when needed
   - Weak or failed results trigger diagnosis and repair
   - Do not force weak results into passes

3. Boundary rule:
   - The project cannot run indefinitely
   - The next $200 month is the final high-intensity build sprint
   - The sprint must produce a decision package
   - After that, the repo must be organized enough for $20-tier continuation, maintenance, or slower follow-up

4. Final sprint mission:
   - grouped candidate testing
   - candidate comparison
   - entry rule package
   - exit rule package
   - stop/invalidation rule package
   - cost/slippage rule package
   - failure diagnosis
   - backtest-prep or backtest batch
   - budget/cost summary
   - clear handoff to lower tier

5. Decision package required before $20 tier:
   - what works
   - what failed
   - what needs repair
   - what data costs remain
   - strongest candidate families
   - weakest candidate families
   - accepted rules
   - missing rules
   - what can continue on $20 tier
   - what would require another serious spend or redesign

6. Batching rule:
   - Batching/grouped progress is already the rule
   - Future chats must follow it
   - Use grouped candidate passes, grouped rule packages, grouped validation, grouped data cost checks, and grouped comparison
   - Avoid one-field loops unless a real blocker makes batching unsafe

7. Cost-control rule:
   - Cheap starter data first
   - Full-window Databento data only after exact cost check and user approval
   - No broad data download from guesses
   - Known warning: SPY 3-candidate full-window cost check was about $72.36
   - Full-window data may be useful, but it must be approved by price, not assumed

8. Communication rule:
   - Plain English
   - Direct answer first
   - No filler
   - Avoid repeated "not/not/not" framing in user-facing summaries
   - Explain meaning, cost, timeline, and next action clearly

9. Current build position:
   - Evidence cleanup reached 9 passed / 0 failed after the SPY Ideal batch if current repo confirms it
   - Intake-ready is controlled by the separate readiness gate
   - Trade-plan rules still need grouped readiness work
   - Next work should be grouped trade-plan readiness and candidate comparison

The $200-to-$20 transition plan must include:
- What must be finished during the final high-intensity month
- What can be safely handed to the $20 tier
- What cannot be left vague
- What budget decisions must be made before more data spending
- What the final sprint success output looks like

Update the next-chat intro so this appears near the top, before older Day 41 language.

Update the dashboard so the active objective becomes:
- Quality-over-deadline but bounded final sprint toward a profitable trading plan
- Day 60 is checkpoint/reporting
- Next $200 month is the final high-intensity build month
- Next work: grouped trade-plan readiness, candidate comparison, cost-controlled data use, and decision package

Run:
- powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1

Allowed writes:
- SAFE_FAST_DAY45_BOUNDED_FINAL_SPRINT_UPDATE_CODEX_TASK.md
- SAFE_FAST_DAY45_BOUNDED_FINAL_SPRINT_UPDATE.md
- SAFE_FAST_DAY45_200_TO_20_TIER_TRANSITION_PLAN.md
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_PROJECT_DASHBOARD.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt
- SAFE_FAST_PROJECT_PROOF_PIPELINE.md
- SAFE_FAST_TRADE_PLAN_COMPLETENESS_GATE.md

Do not write:
- raw Databento files
- evidence fills
- backtest code
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
