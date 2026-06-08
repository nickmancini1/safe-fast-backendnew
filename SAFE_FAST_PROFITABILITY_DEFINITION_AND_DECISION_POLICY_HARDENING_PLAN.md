SAFE-FAST's ultimate goal is to build a profitable trading plan. Every build step must either prove that path, diagnose what blocks it, fix what blocks it, improve regression protection, improve evidence quality, improve transferability, or preserve a decision rule needed to reach that goal.

This file must be read by future chats before answering questions about project vagueness, profitability definition, usefulness gates, strategic improvement questions, owner self-questions, final scoring, UI readiness, execution reality, build-vs-docs discipline, or next strategic build direction.

## Build-vs-docs rule

Do not hide behind docs-only work once the blocker is understood.

If evidence is missing, the next task must do one of these:
- collect or source the missing evidence,
- build the local validator/helper needed to process it,
- document the exact blocker and move to the next evidence-backed fix.

Do not keep creating status documents that restate the same blocker.

Each task must move SAFE-FAST closer to:
- evidence,
- diagnosis,
- trading usefulness,
- regression protection,
- compact handoff readiness,
- or a defined profitability/decision-policy standard.

Docs-only work is allowed only when it preserves a required rule, closes an evidence review, records a real blocker, creates a decision contract, or prepares the next evidence-backed build step.

Docs-only work is not allowed when it merely repeats a blocker already understood.

## Current structural hardening needs

1. Profitable trading plan needs a hard definition.
- Define sample size, win rate, average win, average loss, R multiple, max drawdown, entry delay, spread/slippage assumptions, stale/spent rate, invalidation behavior, blocker impact, and whether the move had enough room to matter.

2. Useful enough needs numbers.
- Define early enough to matter, enough room to matter, and not useful enough.

3. Acceptance authority must be explicit.
- Define whether fields are accepted by human review, deterministic validator, replay output, worksheet rule, or a combined rule.

4. Fix/narrow/isolate/remove/blocker needs a decision tree.
- A weak setup or symbol must not survive because it was part of the original design.

5. Fresh/stale/spent needs setup-specific rules.
- Ideal, Clean Fast Break, and Continuation may require different timing/freshness standards.

6. Lower-tier handoff needs a gold-standard packet example.
- The project already requires fields, but future chats need one model example to copy.

7. UI display priority must be defined.
- The UI is not a trade recommendation screen. It must show mode, setup state, evidence, missing evidence, blockers, trigger/invalidation, freshness, outcome proof, diagnostics, next fix path, and regression protection before anything that could look like a trade suggestion.

8. Execution reality needs a later measurement contract.
- Before any tiny-money pilot, measure signal time, manual delay, quote/spread, fill quality, exit timing, and whether failure came from setup quality or execution.

9. Codex launch rules must stay top-level.
- Use only the known-working unelevated sandbox and no approval prompts.
- Do not use plain codex.
- Do not use default/elevated Windows sandbox.
- Do not use approval modes that pause for proceed/approval questions.

## Owner self-questions and default answers

Question: What is the actual goal?
Answer: To build a profitable trading plan. Not a watcher, not a chart explainer, not a pretty UI, not a bundle generator. Every step must move toward proof, diagnosis, regression protection, or repair.

Question: What would make me believe SAFE-FAST is actually improving?
Answer: More accepted historical examples, cleaner setup-time evidence, fewer missing fields, clearer trigger/invalidation/freshness decisions, better diagnosis of failures, and regression tests that stop old mistakes from coming back.

Question: What would make me believe SAFE-FAST is wasting time?
Answer: Repeating docs-only work without moving evidence forward, building generic infrastructure that does not help proof, adding UI before scoring rules are clear, or creating more gates without using the gates to diagnose real examples.

Question: What is the most dangerous false success?
Answer: Thinking recognition success means profitability. A setup is not successful just because the system labeled it correctly or price eventually moved in the right direction.

Question: What has to be measured before profitability can be claimed?
Answer: Sample size, win rate, average win, average loss, R multiple, max drawdown, entry delay, spread/slippage assumptions, stale/spent rate, invalidation behavior, blocker impact, and whether the move had enough room to matter.

Question: What is the biggest strategic risk?
Answer: Building a system that is good at explaining charts after the fact but not good at identifying useful setups early enough to support a profitable trading plan.

Question: What should happen when a setup type or symbol is weak?
Answer: It should not be defended emotionally. It should be fixed, narrowed, isolated, removed, or documented as blocked. Ideal, Clean Fast Break, Continuation, SPY, QQQ, IWM, and GLD each have to earn their place.

Question: What is the most important evidence question?
Answer: Did setup-time evidence exist before the move, with no hindsight? That means accepted setup identity, trigger, invalidation, freshness/final-signal, blocker/caution status, and later terminal outcome separation.

Question: What is the most important repair question?
Answer: When something fails, what failed exactly: trigger, invalidation, freshness, blocker handling, timing, setup quality, evidence quality, winner selection, session carry-forward, or execution reality?

Question: What should the UI eventually help me decide?
Answer: Not buy or sell. It should show setup state, evidence, missing evidence, blockers, freshness, invalidation, historical proof, diagnostics, next fix path, regression protection, and current mode.

Question: What should the project avoid adding too early?
Answer: Broker work, live data, alerts, order automation, option P&L, account sizing, Railway, production, or UI trade-call behavior before historical proof and scoring rules justify it.

Question: What question should every future chat ask before suggesting a next step?
Answer: Does this step directly improve evidence, diagnosis, regression protection, profitability definition, usefulness scoring, or lower-tier transferability?

## Prior-chat architect questions and answers that must carry forward

Question: What is the biggest way this project could fool us?
Answer: SAFE-FAST could become excellent at explaining charts but not excellent at making money. The defense is the trading-usefulness gate, strict worked/failed meanings, failed examples, no-trade examples, timing/cost awareness, and refusing to treat directionally correct late signals as wins.

Question: What exactly must be true before SAFE-FAST is trusted more?
Answer: It must recognize developing setups, avoid action when evidence is missing, separate setup-time evidence from after-setup evidence, handle blockers, identify invalidation, avoid hindsight, signal early enough to matter, show enough movement after signal to matter, repeat across symbols and setup types, and survive live-data shadow with no trades.

Question: Could one setup type be hurting the whole plan?
Answer: Yes. Ideal, Clean Fast Break, and Continuation should not all be protected just because they are part of the original design. A failing setup type must be diagnosed, narrowed, fixed, isolated, removed, or documented as a blocker.

Question: Could one symbol be hurting the whole plan?
Answer: Yes. SPY, QQQ, IWM, and GLD must not be averaged together too early. Symbol-specific weakness must be diagnosed instead of hidden by stronger symbols.

Question: Does every setup and symbol need to be profitable?
Answer: No. Every setup and symbol must be explainable, but the final profitable trading plan can choose only the combinations that prove useful.

Question: What should happen when something fails?
Answer: Failure must produce a repair map. It must identify what failed, which setup type and symbol were affected, what evidence was missing or bad, and the smallest next evidence-backed fix.

Question: What would make Day 60 a success?
Answer: Day 60 succeeds if it produces a clear evidence-backed decision: ready to plan live-data shadow, not ready with exact blockers and next fix, or not useful enough yet with exact diagnosis and next fix.

Question: What would make Day 60 a failure?
Answer: Day 60 fails if the project still cannot explain what is missing, mixes setup-time evidence with hindsight, lacks required symbol/setup coverage, uses vague worked/failed meanings, or cannot produce compact review material for the lower tier.

Question: What should be refused even if there is impatience?
Answer: Do not start live data early, alerts early, broker/order/account work, sizing, Railway, production, engine patches off theory, fake historical proof, hindsight-filled examples, or claims that recognition success equals profitability.

Question: What is the clearest version of the whole project?
Answer: SAFE-FAST must become excellent at making money, but profitability cannot be claimed until evidence proves it. The build must move from historical recognition and discipline, to historical trading usefulness, to live-data shadow with no trades, to a separately approved tiny-money pilot, and only then to actual-money profitability judgment.

Question: What question should every future chat be forced to answer?
Answer: Is this task moving SAFE-FAST closer to a proven profitable trading plan, or is it only making the system sound smarter?

Current application of those answers:
The original immediate post-mandate task was IWM/GLD missing-evidence inventory. That inventory has now been created. IWM Continuation and GLD Ideal remain missing-evidence/inconclusive. Current work has moved into replacement source row packet tooling and recovery of replacement_source_row_packet_builder.py, subject to real local git status and latest commit.

## Implementation runway

Step 1:
Create this preservation file and update build state plus handoff.

Step 2:
Build a profitability definition contract. It should define the required numbers and fields before profitability can be judged.

Step 3:
Build a usefulness gate. It should check early enough, enough room, freshness, trigger/invalidation clarity, blocker handling, and realistic timing/cost awareness.

Step 4:
Build a decision policy gate. It should classify weak or failed results as fix, narrow, isolate, remove, or blocker.

Step 5:
Build setup-specific freshness/stale/spent rules for Ideal, Clean Fast Break, and Continuation.

Step 6:
Create a gold-standard lower-tier evidence packet example.

Step 7:
Define UI priority rules so the UI never becomes a trade recommendation screen.

Step 8:
Define execution-reality measurement before any pilot.

Step 9:
Only after historical proof earns it, plan live-data shadow. Shadow means no trades, no broker, no alerts, no sizing, no money, and no live trade decisions.
