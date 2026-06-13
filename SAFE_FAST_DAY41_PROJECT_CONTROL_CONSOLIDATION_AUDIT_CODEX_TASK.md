# SAFE-FAST Day 41 project control consolidation and ambiguity audit task

First action:
- Read SAFE_FAST_BUILD_STATE.md first.

Goal:
- Compile the project-wide clarifications from the phone discussion.
- Assess existing repo docs for redundancy, conflict, unclear wording, and superseded instructions.
- Do not blindly replace existing docs with new wording.
- Do not erase old statements just because newer chat text says something different.
- Explore validity first, then clarify what should be current.

Important current context:
- Local git output is source of truth.
- Latest known user-pasted repo state before this task:
  - HEAD was f460e91 Record QQQ external option data request package.
  - Databento QQQ raw files were downloaded into historical_signal_replay/source_data/external_option_data_drop/.
  - Databento validation task file may already exist.
  - Raw Databento files are local-only and should not be committed by this task.
- If HEAD differs, record the actual HEAD and continue only if the difference is explainable from local git history.
- If status is dirty only because of known Databento raw data files and task files, do not treat that as a conflict.
- Do not modify or delete raw downloaded data files.

Read and assess:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt
- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md
- all SAFE_FAST_DAY41*.md files
- all SAFE_FAST_*HANDOFF*.md files
- all SAFE_FAST_*GATE*.md files
- all SAFE_FAST_*RULE*.md files
- historical_signal_replay/source_data/richer_export_package_work/
- historical_signal_replay/source_data/external_option_data_drop/README.md
- Databento validation/download docs if present

Phone discussion to preserve and clarify:
1. The project is not allowed to be called dead.
   - Weak, failed, unclear, missing, or unprofitable results are diagnosis-and-repair triggers.
   - The plan can be narrowed, repaired, replaced, redesigned, or tightened.
   - The goal remains a profitable trading plan.
   - Remove or clarify wording that implies the whole project can be abandoned or called dead.

2. Full project proof pipeline:
   - raw data
   - calculated labels
   - setup recognition
   - stage transitions
   - trade-plan completeness
   - replay
   - regression
   - evidence review
   - failure diagnosis
   - promotion decision

3. Trade-plan completeness gate:
   A result cannot count unless the setup has:
   - exact option contract selection rule
   - side
   - expiration
   - strike
   - entry timing
   - fill assumption
   - bid/ask/mid/spread rule
   - volume/open-interest/liquidity minimums
   - exit rule
   - stop/invalidation rule
   - time exit or end-of-day rule if applicable
   - cost/slippage assumptions
   - failure conditions

4. Known unclear items to track:
   - QQQ gap thresholds
   - contract-selection rules
   - exact entry rule
   - exact exit rule
   - stale/spent rules by setup type
   - stage-transition rules
   - sample-size requirements
   - promotion gates
   - Databento file validation status
   - whether every needed option field maps cleanly into SAFE-FAST evidence fields

5. Project-level risk:
   - Do not prove a chart idea.
   - Prove a fully defined trade plan.
   - Recognition success is necessary but not profitability.
   - Missing evidence is a blocker, not low confidence.

6. Data-source clarification:
   - Tastytrade current helper path did not provide the required historical option fields.
   - Databento is the current likely source for the missing historical option data.
   - Do not overstate Databento until validation is complete.
   - Record Databento as likely/being validated, not guaranteed complete unless validation proves it.

7. User communication preference:
   - Direct answer first.
   - Yes/no/I do not know when that is the real answer.
   - Plain English.
   - No extra safety lectures.
   - No unnecessary recaps.
   - Commands only when useful.

8. Questions and answers to preserve:
   Create a direct Q&A section with these meanings:
   - Do we have a trade plan or a setup-recognition system?
     Answer: It is still being turned into a full trade plan; completeness gates are required.
   - What creates fake confidence?
     Answer: Counting results before contract, entry, exit, cost, and invalidation rules are fixed.
   - Do we likely have the raw data source?
     Answer: Databento likely provides the needed historical option data, but validation must confirm fields.
   - What happens if a backtest fails?
     Answer: Diagnose and repair the failing layer; do not call the project dead.
   - What happens if one setup type fails?
     Answer: Fix, narrow, replace, or remove that setup type from the profitable plan; the project continues.
   - What happens if data is missing?
     Answer: Identify the field, source it, change the proof path, or adjust the plan honestly.
   - What protects future chats from wasting time?
     Answer: Current baseline, exact fixed items, exact blockers, next single action, and repo proof file.

Task:
1. Create:
   - SAFE_FAST_PROJECT_CONTROL_CONSOLIDATION_AUDIT.md
2. Create or update:
   - SAFE_FAST_PROJECT_PROOF_PIPELINE.md
   - SAFE_FAST_TRADE_PLAN_COMPLETENESS_GATE.md
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_PROJECT_PHONE_QA_CLARIFICATIONS.md
3. Update:
   - SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt
   - SAFE_FAST_BUILD_STATE.md
4. The audit must include:
   - documents inspected
   - repeated/redundant themes
   - conflicting statements, if any
   - unclear statements, if any
   - superseded statements, if any
   - recommended current wording
   - what was updated
   - what was intentionally not changed
5. The rule index must classify each major rule as:
   - accepted/current
   - missing/needs decision
   - pending validation
   - superseded
   - conflicting/needs human decision
6. The proof pipeline and completeness gate must be project-wide, not QQQ-only.
7. Do not claim proof.
8. Do not claim profitability.
9. Do not mark any candidate ready.
10. Do not commit raw vendor data.

Allowed writes:
- SAFE_FAST_DAY41_PROJECT_CONTROL_CONSOLIDATION_AUDIT_CODEX_TASK.md
- SAFE_FAST_PROJECT_CONTROL_CONSOLIDATION_AUDIT.md
- SAFE_FAST_PROJECT_PROOF_PIPELINE.md
- SAFE_FAST_TRADE_PLAN_COMPLETENESS_GATE.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_PROJECT_PHONE_QA_CLARIFICATIONS.md
- SAFE_FAST_NEXT_CHAT_INTRO_BLOCK.txt
- SAFE_FAST_BUILD_STATE.md

Do not write:
- raw Databento CSV/DBN/manifest files
- evidence files
- calculator code
- tests
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
