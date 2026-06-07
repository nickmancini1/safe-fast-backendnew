# SAFE-FAST Day 33 Project Handoff and Tier Runway

## Highest-priority active rule: profitability mandate and diagnosis loop

SAFE-FAST is not being built merely to test whether an idea might work. SAFE-FAST's required build target is a profitable trading plan. The goal is to make SAFE-FAST excellent at making money, not merely excellent at explaining charts.

Profitability is the required target, not a guaranteed claim. Profitability cannot be claimed until evidence proves it.

If SAFE-FAST is unprofitable, weak, not useful enough, unsuccessful in evidence, missing evidence, or inconclusive, that result is not an ending by itself. It is a mandatory diagnosis-and-fix trigger.

Every unsuccessful, weak, missing, or inconclusive result must identify:

- the affected setup type
- the affected symbol
- the missing or bad evidence
- whether the failure is in trigger, invalidation, freshness/final-signal, blocker handling, terminal outcome, timing, rule behavior, signal quality, evidence quality, selection stability, or trading usefulness
- the smallest next evidence-backed fix
- the replay/regression protection required before promotion

Preserved meanings:

- "Not useful enough" is not a final result. It is a repair signal.
- "Unprofitable" is not a stopping point. It is a diagnosis requirement.
- "Missing evidence" is not low confidence. It is a blocker that must be fixed or explicitly proven blocking.
- A weak result cannot be treated as an ending unless a hard blocker is proven and documented.
- A hard blocker means evidence proves a path cannot safely support the profitability target without fake proof, hindsight, unsafe assumptions, or live-money guessing.
- If one setup type, symbol, rule, signal, timing path, or evidence path fails, the project does not end automatically. The build must isolate the failure, diagnose it, and choose the smallest evidence-backed fix, narrowing path, removal path, or blocker documentation.
- The final profitable trading plan does not have to preserve every setup type, every symbol, or every original assumption. Anything that cannot support profitability must be fixed, narrowed, isolated, removed, or documented as a blocker.

### Biggest project risk

The biggest hidden danger is that SAFE-FAST could become excellent at explaining charts but not excellent at making money.

A chart can look clean after the fact and still be useless as a trade. A setup can be directionally right and still be too late, too small, too vague, too costly, or too hard to trade safely. The system can sound disciplined and still fail if the signal is late, invalidation is unclear, the exit is vague, or costs and timing delay erase the edge.

Every future task must ask whether it moves SAFE-FAST closer to a proven profitable trading plan, or merely makes the system sound smarter.

### Trading plan reality check

SAFE-FAST currently has a serious path, but it does not yet have a proven trading edge.

The current build is still primarily a recognition-and-discipline system trying to become a profitable trading plan. Recognition success is necessary, but it is not the same as trading profitability.

A system can correctly recognize Ideal, Clean Fast Break, and Continuation setups and still fail as a trading plan. It can be right too late. It can identify a real setup after most of the useful move is gone. It can be directionally right but have too little room after spread, slippage, timing delay, and costs. It can look good in historical review while being too late, too vague, or too expensive to trade safely. It can avoid bad trades but miss enough good trades that it is not useful.

It can overfit to clean historical winners if failed examples, blocked examples, tempting no-trades, late signals, missing-evidence examples, and wrong-winner examples are not included.

It can become unstable if Ideal, Clean Fast Break, and Continuation overlap without a stable winner/abstain rule.

It can behave differently across SPY, QQQ, IWM, and GLD, so symbol-specific weakness must be diagnosed instead of averaged away.

SAFE-FAST's strength is the discipline layer: setup type, trigger evidence, invalidation, blocker handling, freshness/final-signal handling, no-trade discipline, and separation of setup-time evidence from after-setup outcome. That discipline is valuable because it fights hope, hindsight, emotional trading, and vague chart confidence. But that discipline must eventually prove economic usefulness, not just cleaner explanations.

### Trading-usefulness gate

A setup should not count as a true success just because price eventually moved in the right direction.

A setup can only support the profitability target if:

- setup-time evidence was valid
- the signal was not stale
- invalidation was clear
- blockers were handled
- the setup was identified early enough to matter
- the move after signal had enough room to matter
- the outcome was strong enough after realistic timing/cost awareness
- no hindsight was used

Treat "too late" as a real failure:

- Correct idea, late signal is not a clean win.
- Correct setup, bad timing is not a clean win.
- Correct direction, not enough remaining room is not a clean win.
- A late system can look smart in review and still lose money.

Make "do nothing" a first-class result:

- A profitable trading plan is not only about finding trades.
- It must be good at avoiding bad trades.
- Historical evidence must include clean winners, failures, blocked setups, tempting no-trades, missing-evidence examples, late-signal examples, wrong-winner examples, and messy examples.

Make setup overlap strict:

- Ideal, Clean Fast Break, and Continuation may overlap.
- The plan needs stable rules for which setup wins, when to abstain, when a blocker overrides everything, when freshness expires, when invalidation kills the setup, and when mixed evidence means no action.
- Without this, SAFE-FAST can explain the same chart different ways later and become unstable.

Make symbol-specific diagnosis strict:

- SPY, QQQ, IWM, and GLD must not be averaged together too early.
- A setup may work on one symbol and fail on another.
- A failure must be diagnosed by setup type and symbol, such as IWM Continuation, GLD Ideal, QQQ Clean Fast Break, or SPY Ideal.
- Symbol-specific weakness must produce a fix, narrowing path, removal path, or blocker documentation.

### Execution mechanics and future broker path

SAFE-FAST must separate setup quality from execution quality.

A good setup signal is not a full trading-system win unless the actual signal-to-entry-to-exit path can be executed reliably.

The temporary split path may be tastytrade for data and signal observation and Charles Schwab for manual execution, but that split is only a measured bridge. Manual execution is allowed only as a measured test condition before any approved money stage.

Manual execution must measure:

- signal time
- setup type
- symbol
- underlying price at signal
- intended option contract
- option quote and spread at signal
- time the user sees the signal
- time Schwab is opened
- time order ticket is ready
- intended limit price
- whether the order would fill or did fill
- fill price if applicable
- whether the user chased
- whether the user skipped
- reason for skip
- exit rule
- actual or simulated exit
- whether failure came from setup quality or execution mechanics

If the signal is valid but manual Schwab execution is too slow, too wide, too confusing, or too inconsistent, that is a trading-usefulness problem.

If the option spread, fill quality, timing delay, or exit mechanics erase the edge, the setup cannot be counted as profitable.

The preferred future design is one broker for both signal validation and execution, if evidence supports it. Charles Schwab is the current preferred future broker candidate because the user is familiar with the platform and options permissions are there. tastytrade remains an alternate future path if permissions or preference change.

This rule does not authorize broker/API/order automation now. Any future Schwab or tastytrade integration must come only after historical proof and live-data shadow justify it, and only with explicit authorization.

No real-money stage may begin until the broker/execution path defines entry, invalidation, exit, spread limits, delay limits, no-chase rules, stop rules, cancel/skip rules, review rules, and failure definitions.

### Worked, failed, and missing-evidence meanings

A setup must not count as "worked" merely because price eventually moved in the right direction.

A setup can only support the profitability target if setup-time evidence was valid, invalidation was clear, blockers were handled, the signal was not stale, the signal was early enough to matter, and after-setup outcome evidence was strong enough.

A failed setup must explain what failed: trigger, invalidation, freshness, final signal, blocker, timing, wrong setup winner, symbol behavior, economic usefulness, or hindsight contamination.

Missing evidence is a blocker, not low confidence.

Inconclusive means the project does not yet have accepted evidence, not that the setup should be trusted.

### Setup and symbol survival rule

The goal is not loyalty to the original setup list. The goal is profitability under evidence.

Ideal, Clean Fast Break, Continuation, SPY, QQQ, IWM, and GLD must each earn their place.

A setup type or symbol does not need to survive unchanged if evidence says it hurts the plan.

Any weak setup-symbol combination must be fixed, narrowed, isolated, removed, or documented as a blocker.

Strong combinations must not be allowed to hide weak combinations.

The final trading plan may use only the combinations that prove useful.

### Where and when profitability is determined

Profitability is determined in stages.

Day 35 and the current IWM/GLD inventory do not determine profitability. They determine whether accepted evidence exists or is missing.

Day 54 does not determine profitability. It determines whether the compact handoff package is usable by the $20 tier.

Day 60 is the hard historical evidence checkpoint. It does not automatically prove profitability. It determines whether historical evidence is strong enough to plan live-data shadow, or whether exact blockers and next fixes must be named.

Before live-data shadow planning, the project must define historical trading-usefulness criteria. Those criteria must include signal timing, clear invalidation, blocker handling, terminal outcome, repeatability, whether the move was large enough to matter, and realistic awareness of spread, slippage, timing delay, and costs.

Historical trading usefulness must be judged from setup-time evidence and accepted after-setup outcome evidence. It must not use hindsight to justify entries.

Live-data shadow determines whether the system behaves usefully in real time with no trades, no alerts, no broker, no sizing, no money, and no live trade decisions.

Live-data shadow still does not prove actual-money profitability. It proves or disproves real-time usefulness and discipline.

Only after historical proof and live-data shadow both prove useful may a separate tiny-money pilot plan be created.

The tiny-money pilot plan must define actual profitability measurement before any dollars are used, including entry, invalidation, exit, risk limits, cost assumptions, stop rules, review rules, and what result counts as failure.

Actual-money profitability can only be judged from that explicitly approved tiny pilot or later approved stages. It cannot be claimed from recognition alone, historical chart appearance alone, or shadow alone.

### Future complete trading plan requirements

The future profitable trading plan eventually needs more than recognition:

- entry logic
- invalidation
- exit logic
- timing
- risk limits
- cost/spread/slippage awareness
- bad-market filters
- rules for doing nothing
- rules for stopping after bad behavior
- proof that the setup has enough room to matter

Before any money stage, the project must define:

- entry
- invalidation
- exit
- stop rules
- what counts as enough move
- what counts as failure
- when to stop trading after bad behavior
- how costs, spread, timing delay, and slippage are treated

Order of proof:

1. Can SAFE-FAST recognize the right setup while it is developing?
2. Can it avoid action when evidence is missing?
3. Can it pick the right setup type when setups overlap?
4. Can it identify invalidation before the outcome is known?
5. Can it produce signals early enough to matter?
6. Can the move after signal realistically beat costs and timing delay?
7. Can it define exits and stop rules without hindsight?
8. Can it repeat across SPY, QQQ, IWM, and GLD?
9. Can it survive live-data shadow with no trades?
10. Only then can a tiny-money pilot judge actual profitability.

### Architect operating rule

While architect-level guidance is being used, future chats must not passively follow narrow prompts if the project is drifting.

Future chats must call out hidden risks, vague goals, weak evidence, premature promotion, and anything that makes SAFE-FAST sound smarter without making it more profitable under evidence.

Future chats must preserve important corrections in the repo docs when the correction affects the project direction.

Future chats must keep the build moving toward evidence, diagnosis, trading usefulness, and profitability.

This does not authorize fake proof, live trading, engine changes without evidence and tests, or skipping the staged proof process.

### Architect questions future chats must preserve

Question: What is the biggest way this project could fool us?

Answer: SAFE-FAST could become excellent at explaining charts but not excellent at making money. The defense is the trading-usefulness gate, strict worked/failed meanings, failed examples, no-trade examples, and cost/timing awareness.

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

Answer: Day 60 fails if the project still cannot explain what is missing, mixes setup-time evidence with hindsight, lacks required symbol/setup coverage, uses vague worked/failed meanings, or cannot produce compact review material for the $20 tier.

Question: What is the most important next task after preserving this mandate?

Answer: Return to the docs-only IWM/GLD missing-evidence inventory. Determine whether accepted evidence already exists for IWM Continuation and GLD Ideal. If it does not exist, keep them missing-evidence/inconclusive and name the smallest evidence-backed fix.

Question: What should be refused even if there is impatience?

Answer: Do not start live data early, alerts early, broker/order/account work, sizing, Railway, production, engine patches off theory, fake historical proof, hindsight-filled examples, or claims that recognition success equals profitability.

Question: What is the clearest version of the whole project?

Answer: SAFE-FAST must become excellent at making money, but profitability cannot be claimed until evidence proves it. The build must move from historical recognition and discipline, to historical trading usefulness, to live-data shadow with no trades, to a separately approved tiny-money pilot, and only then to actual-money profitability judgment.

Question: What question should every future chat be forced to answer?

Answer: Is this task moving SAFE-FAST closer to a proven profitable trading plan, or is it only making the system sound smarter?

### Pro and $20 tier usage rule

Pro tier is for architecture, diagnosis, hard decisions, and preventing the project from becoming vague.

The $20 tier is for prepared continuation work.

The $20 tier should not be expected to rescue vague architecture, rediscover the project, or make major trading-plan decisions from scratch.

Day 54 is the first subscription decision checkpoint.

Day 54 must decide whether the handoff package is compact and clear enough for the $20 tier to continue.

Day 60 is the hard historical evidence checkpoint.

Do not buy another Pro month automatically.

Consider another Pro month only if the project still needs architect-level judgment to complete the historical evidence package, trading-usefulness gate, setup overlap rules, compact review packets, or Day 60 diagnosis.

If remaining work is mostly prepared execution, focused docs updates, compact review, or running already-defined Codex prompts, the $20 tier should be enough.

Use Pro for architecture, diagnosis, and hard decisions. Use $20 for prepared continuation work.

### Day 60 rule

Day 60 is not a quit/continue vibe check and not an automatic profitability claim. It must produce one of:

1. ready to plan live-data shadow
2. not ready with exact blockers and next fix
3. not useful enough yet with exact diagnosis and next fix

### Live-data shadow is not live trading

Live-data shadow means:

- no trades
- no broker
- no alerts
- no account sizing
- no money
- no live trade decisions
- no production/Railway/deploy unless explicitly authorized later

### This mandate does not authorize

This mandate does not authorize:

- fake proof
- hindsight filling
- skipping historical evidence
- live data before historical proof earns shadow planning
- real money before historical proof and shadow both prove useful
- changing the Day 35 / patch8 baseline

## Day 36 IWM Continuation 001 evidence packet review status

- Latest committed baseline before this status: 858a245 Add Day 35 evidence inventories and execution mechanics architecture.
- Review file: SAFE_FAST_IWM_CONTINUATION_001_EVIDENCE_PACKET_REVIEW.md.
- Result: IWM Continuation 001 remains missing-evidence/inconclusive.
- Reason: repo-backed source chain supports a candidate/review path, but accepted setup-time trigger, accepted invalidation, accepted freshness/final-signal, accepted blocker handling, and accepted terminal outcome evidence are still not proven.
- Smallest next evidence-backed fix: create a bounded IWM Continuation accepted-signal-row review that decides whether an accepted signal timestamp, trigger, invalidation, freshness/final-signal, blocker/caution status, and terminal outcome can be accepted without hindsight.
- Scope preserved: docs-only evidence review; no main.py, engine logic, replay code, live data, watcher loops, alerts, broker/order/account/options/P&L, account sizing, Railway/deploy/production, generated reports/logs, or live trade decisions.

## Day 36 GLD Ideal 001 accepted signal row review status

- Latest committed baseline before this status: df3fa06 Add IWM Continuation accepted signal row review.
- Review file: SAFE_FAST_GLD_IDEAL_001_ACCEPTED_SIGNAL_ROW_REVIEW.md.
- Result: GLD Ideal 001 does not have an accepted setup-time signal row.
- Status: GLD Ideal 001 remains missing-evidence/inconclusive.
- Reason: repo evidence supports a candidate/review chain, but accepted setup-time trigger, accepted invalidation, accepted freshness/final-signal, accepted blocker/caution handling, and accepted terminal outcome eligibility are still not proven.
- Combined Day 36 evidence result: IWM Continuation 001 and GLD Ideal 001 both remain missing-evidence/inconclusive because neither has an accepted setup-time signal row.
- Smallest next evidence-backed fix: choose the clearest bounded trigger/invalidation/freshness acceptance review between IWM Continuation and GLD Ideal; do not promote either setup unless accepted setup-time proof exists.
- Scope preserved: docs-only evidence review; no main.py, engine logic, replay code, live data, watcher loops, alerts, broker/order/account/options/P&L, account sizing, Railway/deploy/production, generated reports/logs, or live trade decisions.

## Day 36 GLD Ideal 001 trigger / invalidation / freshness acceptance review status

- Latest committed baseline before this status: 8044901 Add GLD Ideal accepted signal row review.
- Review file: SAFE_FAST_GLD_IDEAL_001_TRIGGER_INVALIDATION_FRESHNESS_ACCEPTANCE_REVIEW.md.
- Result: GLD Ideal 001 cannot accept trigger / invalidation / freshness proof from current repo evidence.
- Status: GLD Ideal 001 remains missing-evidence/inconclusive.
- Reason: no accepted setup-time signal row, no accepted numeric trigger, no accepted numeric invalidation, no accepted freshness/final-signal, unresolved blocker/caution status, and no terminal outcome eligibility before setup-time acceptance.
- Smallest next GLD-specific fix: create a bounded GLD Ideal setup-time row acceptance worksheet.
- Project-level next move: use GLD Ideal as the next worksheet candidate unless local source review proves IWM has clearer accepted setup-time rows.
- Scope preserved: docs-only evidence review; no main.py, engine logic, replay code, live data, watcher loops, alerts, broker/order/account/options/P&L, account sizing, Railway/deploy/production, generated reports/logs, or live trade decisions.

## Day 36 GLD Ideal 001 setup-time row acceptance worksheet status

- Latest committed baseline before this status: ff0f56d Add GLD Ideal trigger invalidation freshness acceptance review.
- Worksheet file: SAFE_FAST_GLD_IDEAL_001_SETUP_TIME_ROW_ACCEPTANCE_WORKSHEET.md.
- Result: GLD Ideal 001 cannot accept one setup-time row from current repo evidence.
- Status: GLD Ideal 001 remains missing-evidence/inconclusive.
- Reason: no accepted setup-time signal timestamp, accepted final verdict, accepted trigger state, accepted numeric trigger, accepted numeric invalidation, accepted freshness/final-signal, accepted blocker/caution status, or terminal outcome eligibility.
- Smallest next evidence-backed fix: run IWM Continuation trigger / invalidation / freshness acceptance review.
- Project-level rule: if IWM is also blocked at setup-time acceptance, stop trying to promote these two candidate examples and choose a cleaner bounded real historical example with complete setup-time fields.
- Scope preserved: docs-only worksheet; no main.py, engine logic, replay code, live data, watcher loops, alerts, broker/order/account/options/P&L, account sizing, Railway/deploy/production, generated reports/logs, or live trade decisions.

## Day 36 IWM Continuation 001 trigger / invalidation / freshness acceptance review status

- Latest committed baseline before this status: add70a4 Add GLD Ideal setup time row acceptance worksheet.
- Review file: SAFE_FAST_IWM_CONTINUATION_001_TRIGGER_INVALIDATION_FRESHNESS_ACCEPTANCE_REVIEW.md.
- Result: IWM Continuation 001 cannot accept trigger / invalidation / freshness proof from current repo evidence.
- Status: IWM Continuation 001 remains missing-evidence/inconclusive.
- Reason: no accepted setup-time signal row, no accepted numeric trigger, no accepted numeric invalidation, no accepted freshness/final-signal, unresolved blocker/caution status, and no terminal outcome eligibility before setup-time acceptance.
- Combined Day 36 evidence result: IWM Continuation 001 and GLD Ideal 001 both remain missing-evidence/inconclusive because neither has accepted setup-time proof.
- Smallest next evidence-backed fix: stop trying to promote these two candidate examples unless explicitly requested; create a bounded real historical replacement-candidate selection review for a cleaner IWM Continuation or GLD Ideal example with complete setup-time fields.
- Scope preserved: docs-only evidence review; no main.py, engine logic, replay code, live data, watcher loops, alerts, broker/order/account/options/P&L, account sizing, Railway/deploy/production, generated reports/logs, or live trade decisions.

## Day 36 IWM/GLD replacement candidate selection review status

- Latest committed baseline before this status: c80bd9e Add IWM Continuation trigger invalidation freshness acceptance review.
- Review file: SAFE_FAST_IWM_GLD_REPLACEMENT_CANDIDATE_SELECTION_REVIEW.md.
- Result: stop trying to promote the current IWM Continuation 001 and GLD Ideal 001 candidates unless explicitly requested later.
- Reason: both are blocked at setup-time acceptance and remain missing-evidence/inconclusive.
- Selected next evidence-backed move: create SAFE_FAST_GLD_IDEAL_REPLACEMENT_CANDIDATE_SOURCE_SELECTION_WORKSHEET.md.
- Target: find a cleaner GLD Ideal replacement candidate from existing repo sources only, or prove no acceptable GLD Ideal replacement candidate exists in current repo sources.
- Scope preserved: docs-only review; no main.py, engine logic, replay code, live data, watcher loops, alerts, broker/order/account/options/P&L, account sizing, Railway/deploy/production, generated reports/logs, or live trade decisions.

## Day 36 GLD Ideal replacement candidate source selection worksheet status

- Latest committed baseline before this status: c78a41c Add IWM GLD replacement candidate selection review.
- Worksheet file: SAFE_FAST_GLD_IDEAL_REPLACEMENT_CANDIDATE_SOURCE_SELECTION_WORKSHEET.md.
- Result: no acceptable GLD Ideal replacement candidate is accepted from current repo sources.
- Status: GLD Ideal remains blocked for the current Day 36 missing-evidence path.
- Reason: current repo source trail points back to GLD-WINDOW-IDEAL-001, and that candidate already failed setup-time row acceptance.
- Smallest next evidence-backed fix: create SAFE_FAST_IWM_CONTINUATION_REPLACEMENT_CANDIDATE_SOURCE_SELECTION_WORKSHEET.md.
- Scope preserved: docs-only worksheet; no main.py, engine logic, replay code, live data, watcher loops, alerts, broker/order/account/options/P&L, account sizing, Railway/deploy/production, generated reports/logs, or live trade decisions.

## Day 36 IWM Continuation replacement candidate source selection worksheet status

- Latest committed baseline before this status: c8339d9 Add GLD Ideal replacement candidate source selection worksheet.
- Worksheet file: SAFE_FAST_IWM_CONTINUATION_REPLACEMENT_CANDIDATE_SOURCE_SELECTION_WORKSHEET.md.
- Result: no acceptable IWM Continuation replacement candidate is accepted from current repo sources.
- Combined Day 36 result: GLD Ideal replacement search is blocked and IWM Continuation replacement search is blocked.
- Reason: current repo source trails provide candidate/review material only; accepted setup-time trigger, invalidation, freshness/final-signal, blocker/caution status, and terminal eligibility are not available for a cleaner replacement candidate.
- Smallest next evidence-backed fix: create SAFE_FAST_IWM_GLD_NEW_BOUNDED_SOURCE_COLLECTION_PLAN.md.
- Scope preserved: docs-only worksheet; no main.py, engine logic, replay code, live data, watcher loops, alerts, broker/order/account/options/P&L, account sizing, Railway/deploy/production, generated reports/logs, or live trade decisions.

## Day 36 IWM/GLD new bounded source collection plan status

- Latest committed baseline before this status: d233511 Add IWM Continuation replacement candidate source selection worksheet.
- Plan file: SAFE_FAST_IWM_GLD_NEW_BOUNDED_SOURCE_COLLECTION_PLAN.md.
- Result: both current IWM Continuation and GLD Ideal replacement paths are blocked in current repo sources.
- Next build step: create SAFE_FAST_IWM_GLD_REPLACEMENT_SOURCE_COLLECTION_WORKSHEET.md.
- Purpose of next worksheet: collect cleaner bounded real historical candidates for IWM Continuation and GLD Ideal with complete setup-time fields.
- Candidate IDs reserved: IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001, IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002, GLD-REPLACEMENT-IDEAL-CANDIDATE-001, GLD-REPLACEMENT-IDEAL-CANDIDATE-002.
- Scope preserved: docs-only plan; no main.py, engine logic, replay code, live data, watcher loops, alerts, broker/order/account/options/P&L, account sizing, Railway/deploy/production, generated reports/logs, or live trade decisions.

## Day 36 IWM/GLD replacement source collection worksheet status

- Latest committed baseline before this status: 039a7b1 Add IWM GLD new bounded source collection plan.
- Worksheet file: SAFE_FAST_IWM_GLD_REPLACEMENT_SOURCE_COLLECTION_WORKSHEET.md.
- Result: replacement candidate slots are defined but not populated with accepted source rows.
- Status: source collection required for IWM Continuation and GLD Ideal replacement candidates.
- Candidate IDs reserved: IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001, IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002, GLD-REPLACEMENT-IDEAL-CANDIDATE-001, GLD-REPLACEMENT-IDEAL-CANDIDATE-002.
- Smallest next evidence-backed fix: create SAFE_FAST_IWM_GLD_REPLACEMENT_SOURCE_ROW_REQUEST.md.
- Scope preserved: docs-only worksheet; no main.py, engine logic, replay code, live data, watcher loops, alerts, broker/order/account/options/P&L, account sizing, Railway/deploy/production, generated reports/logs, or live trade decisions.

## Day 36 IWM/GLD replacement source row request status

- Latest committed baseline before this status: 7e69635 Add IWM GLD replacement source collection worksheet.
- Request file: SAFE_FAST_IWM_GLD_REPLACEMENT_SOURCE_ROW_REQUEST.md.
- Result: exact local source row requirements are defined for two IWM Continuation replacement candidates and two GLD Ideal replacement candidates.
- Next build step: create SAFE_FAST_IWM_GLD_REPLACEMENT_SOURCE_ROW_PACKET.md.
- Purpose of next packet: populate the four replacement candidate IDs with local historical 1H RTH source rows, or explicitly mark them unavailable.
- Scope preserved: docs-only source row request; no main.py, engine logic, replay code, live data, watcher loops, alerts, broker/order/account/options/P&L, account sizing, Railway/deploy/production, generated reports/logs, or live trade decisions.

## Day 36 IWM/GLD replacement source row packet status

- Latest committed baseline before this status: 0f0c519 Add IWM GLD replacement source row request.
- Packet file: SAFE_FAST_IWM_GLD_REPLACEMENT_SOURCE_ROW_PACKET.md.
- Result: no replacement candidate slot is ready for acceptance review yet.
- Status: all four replacement slots remain missing-evidence/inconclusive because complete setup-time source row packets are unavailable.
- Smallest next evidence-backed fix: create SAFE_FAST_IWM_GLD_LOCAL_SOURCE_EXPORT_INSTRUCTION.md.
- Purpose of next instruction: specify the exact bounded historical 1H RTH rows needed to populate IWM Continuation and GLD Ideal replacement candidates.
- Scope preserved: docs-only packet; no main.py, engine logic, replay code, live data, watcher loops, alerts, broker/order/account/options/P&L, account sizing, Railway/deploy/production, generated reports/logs, or live trade decisions.

## Current update status

- Baseline: patch8.
- Current working day: Day 35.
- Day 33 status: historical context.
- Mode: build work only, not live trade chat.
- Repo: safe-fast-backendnew.
- Branch: main.
- Latest known local commit before current uncommitted work: 3189fd2 Preserve profitability mandate and trading-usefulness architecture.
- Latest known completed build commit before this handoff update: 3189fd2 Preserve profitability mandate and trading-usefulness architecture.
- Current uncommitted status: Day 35 combined docs-only batch pending assistant review and commit. Changed files should be limited to `SAFE_FAST_REAL_HISTORICAL_IWM_GLD_MISSING_EVIDENCE_INVENTORY.md`, `SAFE_FAST_TECHNICAL_INDICATOR_AND_EVIDENCE_COMPONENT_INVENTORY.md`, `SAFE_FAST_BUILD_STATE.md`, and this handoff file.
- Real local git status and git log are source of truth.
- This Day33-named file remains a living handoff document and records this Day 35 update.
- Execution mechanics architecture status: preserved as a docs-only rule after the IWM/GLD inventory path; this does not authorize broker/API/order automation, live trading, order execution, option P&L, account sizing, or production work.
- Technical indicator inventory status: started and completed in `SAFE_FAST_TECHNICAL_INDICATOR_AND_EVIDENCE_COMPONENT_INVENTORY.md`; official indicator and evidence-component lists must be repo-backed, not guessed.
- Inventory boundary: this does not authorize new indicators, engine logic, broker integration, order automation, option P&L, account sizing, production work, or live trade decisions.

## Update protocol

Update this file whenever any of these change:

- current working day
- latest local commit
- current objective
- completed milestone
- proof chain status
- tier/runway status
- no-go boundaries
- active risks
- unresolved concerns
- next objective
- next-after-next objective
- instructions future chats must not forget

Future chats must not make the user re-explain this context.

## Repo and checkpoint handling

- Day 31 is historical context.
- Day 33 is historical context.
- Day 34 is historical context for the current Day 35 implementation/build-state updates.
- Day 35 is the current working day.
- Day 28 file names are historical labels only.
- fc64232 is the latest Day 31 handoff/build-state checkpoint.
- 0d23423 is the Day 31 addendum milestone before that sync.
- 0e4a0c0 is a later intro-block replacement commit.
- Those are not conflicts.
- Sync commits are bookkeeping commits.

## Day 34 Phone Clarifications

### Fixed timeline

- Today is Day 34.
- Day 54 is the target for the $20-tier handoff package to be usable.
- Day 60 is the hard evidence checkpoint.
- There is no Day 90 planning target unless the user explicitly changes the tier plan.

### Day 34 to Day 60 plan

- Day 34 to Day 38: finish controlled sample coverage review.
- Day 39 to Day 45: start real historical examples.
- Day 46 to Day 53: expand real historical examples across symbols and setup types.
- Day 54: $20-tier handoff package must be usable.
- Day 54 to Day 60: prepare the Day 60 evidence decision package.
- Day 60: decide whether historical proof earns shadow planning, exact blockers remain, or the current version needs diagnosis/fix path.

Day 60 is not a profitability claim and not live trading.

By Day 60, SAFE-FAST must produce one of these:

- ready to plan live-data shadow
- not ready, with exact blockers
- not useful enough yet, with exact diagnosis and fix path

"Not useful enough is not an ending. It is a diagnosis trigger."

If the minimum historical evidence package is not complete by Day 60, it is a blocker, not "low confidence."

### Minimum Day 60 historical evidence package

- real historical examples have started
- SPY, QQQ, IWM, and GLD are represented
- Ideal, Clean Fast Break, and Continuation are represented
- each example separates setup-time evidence from after-setup evidence
- the system can say worked, failed, or missing evidence
- the system can explain why
- the system can name the next fix path
- the system can produce compact review material for the $20 tier

## Workflow

Use local PowerShell and Codex only.

Do not write directly to GitHub.
Do not create GitHub blobs.
Do not use GitHub edit/write tools.

Standard workflow:

1. Assistant gives one complete PowerShell block.
2. User pastes it into PowerShell.
3. Codex runs locally with the unelevated sandbox.
4. User sends the output back.
5. Assistant reviews files changed, scope, tests, git diff --check, and git status.
6. Assistant gives a guarded commit block.
7. Commit only expected files.
8. Do not push unless the user explicitly asks.

Codex command:

codex.cmd -c 'windows.sandbox="unelevated"' --sandbox workspace-write --ask-for-approval never

## Communication rule

The user wants direct normal English.

Do not add filler.
Do not narrate internal thinking.
Do not say “plain English.”
Do not use copy blocks unless the user should paste them somewhere.
Say what matters, what changed, what is next, and what is still unproven.

## Tier and runway context

The user is currently back on the $200 tier.

The project must assume the user will be on the $20 tier in about 30 days.

The current $200 tier window is the heavy-build window.

Do not plan around Day 90.

The lower-tier handoff must be ready before the current $200 window ends.

Future chats must not soften this into “maybe” or treat Day 90 as a planning target unless the user explicitly changes the tier plan.

Use the current $200 window for:

- hard reasoning
- repo review
- Codex task design
- proof structure
- diagnostics
- regression discipline
- handoff protection
- lower-tier transferability

The future $20 tier is for:

- compact evidence review
- small Codex tasks
- documentation updates
- focused diagnostics review
- small patches

The $20 tier role is:

- $20 tier reviews compact packets
- $20 tier helps with small Codex prompts
- $20 tier helps update docs
- $20 tier does nple coverage review

The $20 tier is not:

- the live-data engine
- a raw log processor
- a giant repo rediscovery tool
- a production supervisor
- a live trading assistant

## Ultimate goal

The goal is not to finish a watcher.

The goal is to prove whether SAFE-FAST can become a profitable trading plan.

Detection alone is not enough.
A watcher alone is not enough.
A clean codebase alone is not enough.

SAFE-FAST must eventually answer:

- What setup appeared?
- What happened after it appeared?
- Did it work, fail, stay pending, go stale, get invalidated, or lack evidence?
- Why did that likely happen?
- What evidence supports that?
- What is missing?
- What must be fixed next?
- What regression test protects the fix?
- Is the plan proving viable or not?

If the plan is not proving viable, the system must diagnose why.
If diagnostics show a fixable path, pursue that path aggressively.
If diagnostics show the plan is not viable, say that honestly.
Do not hide failure with tuning.

## Required viability loop

detect -> score outcome -> diagnose deeply -> analyze whole system -> decide fix path -> adjust rule/contract/test -> run regression -> review again

## Diagnostics rule

Diagnostics must identify:

- what failed
- evidence used
- likely cause candidate
- affected setup type
- affected symbol
- affected stage
- trigger/invalidation/freshness relationship
- blocker/caution relationship
- ranking/focus issue
- session-boundary issue
- data-quality or missing-evidence issue
- market-context issue
- outcome-scoring issue
- review/logging issue
- user-facing workflow issue
- next fix path
- regression test needed

Do not accept shallow labels like:

- failed setup
- bad alert
- weak signal
- bad trade
- looked wrong
- market was bad

## Optimization rule

Do not optimize blindly.
Do not change rules because something feels wrong.
Do not tune based on vibes.

Optimization requires:

- evidence
- diagnosed failure category
- targeted fix path
- regression test path
- preserved no-trade boundary

If diagnostics show a fixable path, pursue it.
If diagnostics show the plan is not viable, say that honestly.

## Discretion rule

The signal layer must become as rule-based as possible.

Rule-based areas:

- setup recognition
- trigger
- invalidation
- fresh/stale/spent
- blocker/caution
- ranking/focus
- outcome scoring
- diagnostics
- user workflow

Human discretion may exist only as:

- no-trade veto
- review note
- safety pause

Human discretion must not:

- create a signal
- approve a trade
- override missing proof
- move triggers
- hide failures
- change outcome after the fact

Ambiguous cases should be labeled:

- inconclusive
- unavailable_evidence
- needs_review

## Starting universe

Starting symbols:

- SPY
- QQQ
- IWM
- GLD

Why:

- SPY: broad market behavior
- QQQ: tech/growth-heavy behavior
- IWM: small-cap behavior
- GLD: gold / non-equity behavior

Each symbol must be judged separately.

Do not expand the universe until these four are reviewed separately.

## Setup types

SAFE-FAST must evaluate these separately:

- Ideal
- Clean Fast Break
- Continuation

Do not combine setup types too early.

Each setup type must be reviewable on its own.

## Worked or failed does not mean profitable

For now, “worked” means the chart/setup behavior matched the plan expectation.

It does not mean profitable.

Profitability comes later.

Later layers must handle:

- entry quality
- risk
- invalidation behavior
- timing
- trade management
- option fills
- spreads
- IV
- expiration
- P&L
- account sizing

Those are not the first proof layer.

## Current fixed proof chain

Recently built proof chain:

- discretion audit inventory bridge gate
- setup outcome proof evaluator
- setup outcome diagnostics evaluator
- setup outcome evidence packet builder
- setup outcome evidence packet readiness evaluator
- setup outcome proof review aggregator
- setup outcome proof review readiness gate
- historical setup proof review bundle builder
- historical setup proof review bundle readiness gate
- historical setup sample path runner
- first controlled historical sample evidence set
- first controlled historical sample output review

Latest known completed build commit before current uncommitted work:

e03c792 Add real historical missing evidence inventory plan

Latest known local commit before current uncommitted work:

e03c792 Add real historical missing evidence inventory plan

Current Day 35 next-step plan after first real historical example batch status:

- Historical setup sample path planning is complete and committed at `73a27ba Add historical setup sample path plan`.
- Day 33 historical setup sample path runner is complete and committed at `6973581 Add historical setup sample path runner`.
- Controlled historical sample evidence set planning is complete and committed at `0910f54 Add controlled historical sample evidence set plan`.
- First controlled historical sample evidence set is complete and committed at `2ccc021 Add first controlled historical sample evidence set`.
- Controlled sample output review planning is complete and committed at `c880103 Add controlled sample review plan`.
- First controlled historical sample output review is complete and committed at `ba7374b Add controlled historical sample output review`.
- GLD Continuation evidence fix planning is complete and committed at `c228cb1 Add GLD Continuation evidence fix plan`.
- GLD Continuation after-setup evidence implementation is complete and committed at `eb6e5d0 Add GLD Continuation after-setup evidence`.
- IWM controlled sample expansion planning is complete and committed at `46b1e27 Add IWM controlled sample expansion plan`.
- IWM controlled sample evidence implementation is complete and committed at `7cc424c Add IWM controlled sample evidence`.
- Controlled sample coverage review planning is complete and committed at `d8ab7aa Add controlled sample coverage review plan`.
- Day 34 handoff timeline and evidence checkpoint is complete and committed at `7181645 Update Day 34 handoff timeline and evidence checkpoint`.
- Controlled sample coverage review is complete and committed at `ca8b6a4 Add controlled sample coverage review`.
- Controlled sample missing-evidence implementation planning is complete and committed at `ad21b40 Add controlled sample missing evidence plan`.
- Controlled missing-evidence sample implementation is complete and committed at `8527eff Add controlled missing-evidence sample`.
- Controlled sample coverage review update is complete and committed at `bfad6d3 Update controlled sample coverage review`.
- First real historical example batch planning is complete and committed at `35b91bf Add first real historical example batch plan`.
- First real historical example batch implementation is complete and committed at `ba44d07 Add first real historical example batch`.
- Historical objective for that completed plan-correction block was creating the docs-only next-step plan after the first real historical example batch, focused on IWM Continuation and GLD Ideal missing accepted evidence.
- Historical changed files for that completed block were limited to `SAFE_FAST_LOCAL_NEXT_STEP_PLAN_AFTER_FIRST_REAL_HISTORICAL_EXAMPLE_BATCH.md`, `SAFE_FAST_BUILD_STATE.md`, and `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`.
- Runner behavior: accepts caller-provided in-memory historical setup examples only, rejects file/report/log path, live-data, controlled-shadow, alert, broker/order/account/options/P&L/account-sizing, live-trade-decision, subprocess/thread/socket, watcher-loop, and `main.py` shaped inputs, runs proof -> diagnostics -> evidence packet -> packet readiness -> group review -> group review readiness -> historical bundle -> bundle readiness, preserves setup-time vs post-setup evidence separation, setup type, symbol, setup-type-plus-symbol pair separation, missing evidence, diagnostics, fix paths, regression needs, lower-tier review fields, and exact bundle-readiness missing review items.
- Sample evidence set behavior: exposes one worked `Ideal` / `SPY` setup, one failed `Clean Fast Break` / `QQQ` setup, one reviewable `Continuation` / `GLD` setup, one reviewable `Ideal` / `IWM` setup, and exactly one explicit controlled missing-evidence `Continuation` / `QQQ` setup through the existing runner; preserves setup type separation, symbol separation, setup-type-plus-symbol pair separation, setup-time versus after-setup evidence separation, diagnostics, fix paths, lower-tier summary, no-trade/watch-only, no-live-data, no-controlled-shadow, no-alert, no-broker, no-file-write, no-rule-change, and no-optimization boundaries.
- Review behavior: accepts caller-provided in-memory sample path output only, returns one in-memory review summary only, keeps worked, failed, and inconclusive samples separate, keeps setup type and symbol separate, checks no-hindsight boundaries, surfaces useful proof, weak proof, missing evidence, next fix paths, regression needs, lower-tier review material, explicitly reports the GLD Continuation review status and IWM review status / teaching, and defensively copies returned data.
- Review result: the controlled output is useful but not final viability proof. The worked `Ideal` / `SPY` sample gives clear chart-behavior proof; the failed `Clean Fast Break` / `QQQ` sample gives useful diagnosis; the existing `Continuation` / `GLD` sample remains reviewable; the `Ideal` / `IWM` sample remains reviewable; the new `Continuation` / `QQQ` sample provides active missing-evidence coverage. Bundle readiness still shows tiny-sample/upstream review contract gaps and must not be treated as final lower-tier readiness.
- GLD Continuation status: `reviewable`; `gld_continuation_became_reviewable=True`; `gld_continuation_remains_inconclusive=False`; no final viability, profitability, historical success, optimization, or live trade claim.
- IWM status: `reviewable`; `iwm_became_reviewable=True`; `iwm_remains_inconclusive=False`; the new sample teaches that the controlled local chain can carry one small-cap IWM example with setup-time evidence separated from after-setup evidence while keeping symbol and setup pair boundaries.
- Controlled sample implementation result: represented symbols are `GLD`, `IWM`, `QQQ`, and `SPY`; represented setup types are `Clean Fast Break`, `Continuation`, and `Ideal`; represented pairs are `Ideal` / `SPY`, `Clean Fast Break` / `QQQ`, `Continuation` / `GLD`, `Ideal` / `IWM`, and `Continuation` / `QQQ`.
- Outcome coverage result: worked chart/setup behavior is represented, failed chart/setup behavior is represented, and active missing-evidence coverage is now represented exactly once.
- Missing-evidence coverage present: yes; `controlled-sample-continuation-qqq-missing-evidence-001` has setup-time evidence but missing after-setup `source_row_reference` and `post_setup_evidence`.
- What the missing-evidence sample teaches: the chain can preserve setup-time evidence, keep missing after-setup evidence scoped to the `Continuation` / `QQQ` pair, diagnose the gap as `data_quality_or_missing_evidence`, avoid fabricating evidence, and name `collect_or_preserve_missing_after_setup_evidence` as the smallest next fix path without optimization or rule changes.
- Focused validation result: `python -m unittest discover -s tests -p test_setup_outcome_historical_sample_path.py` PASS (`27` tests).
- Controlled sample path and output review rerun: PASS; `records_processed=5`, `records_accepted=5`, `records_rejected=0`; worked `3`, failed `1`, missing evidence `1`; `review_conclusion=useful_but_not_final_viability_proof`; no final viability, profitability, historical success, or optimization claim.
- git diff whitespace check: PASS with `git diff --check` (exit 0; LF-to-CRLF working-copy warnings for `SAFE_FAST_BUILD_STATE.md`, `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`, `tests/test_setup_outcome_historical_sample_path.py`, and `watcher_foundation/setup_outcome_historical_sample_path.py` only).
- Prior Day 34 docs-only coverage review validation: unit tests not run because the plan said do not run unit tests for that docs-only step; `git diff --check` PASS (exit 0; LF-to-CRLF working-copy warnings for `SAFE_FAST_BUILD_STATE.md` and `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md` only); new review file checked with `git diff --no-index --check -- NUL SAFE_FAST_CONTROLLED_SAMPLE_COVERAGE_REVIEW.md` and no whitespace errors were reported.
- Prior Day 34 docs-only missing-evidence plan validation: unit tests not run because that task was docs-only; `git diff --check` PASS (exit 0; LF-to-CRLF working-copy warnings for `SAFE_FAST_BUILD_STATE.md` and `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md` only); new plan file checked with `git diff --no-index --check -- NUL SAFE_FAST_LOCAL_NEXT_STEP_PLAN_AFTER_CONTROLLED_SAMPLE_COVERAGE_REVIEW.md` and no whitespace errors were reported.
- Current coverage review conclusion: the controlled sample phase is complete enough to plan real historical examples. `SPY`, `QQQ`, `IWM`, and `GLD` are represented; `Ideal`, `Clean Fast Break`, and `Continuation` are represented; worked, failed, and missing-evidence examples are represented; no-hindsight separation held; setup type and symbol separation held.
- Current plan summary: first batch should contain exactly 4 real historical examples, one each for `SPY`, `QQQ`, `IWM`, and `GLD`; all three setup types must be represented; required pairs are `Ideal` / `SPY`, `Clean Fast Break` / `QQQ`, `Continuation` / `IWM`, and `Ideal` / `GLD`.
- Real historical example definition: one caller-provided in-memory setup example derived from a real past market chart/source record for one symbol, one setup type, and one setup timestamp/window, with setup-time evidence separated from after-setup evidence and no future candles used to define the original setup.
- Future implementation files, if later explicitly approved, should be limited to `watcher_foundation/setup_outcome_historical_sample_path.py`, `tests/test_setup_outcome_historical_sample_path.py`, `SAFE_FAST_BUILD_STATE.md`, and `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`.
- Future tests must prove the 4-example real historical batch runs through the existing proof chain; preserves symbol/setup/pair separation; rejects controlled IDs/refs for the real batch; preserves no-hindsight and setup-time versus after-setup separation; surfaces missing evidence without fabrication; and preserves no side effects or viability/profitability/live/production/optimization/rule-change claims.
- Real historical source evidence exists: yes, for the required first-batch pairs, with different proof depth by pair.
- Source evidence used: `historical_signal_replay/fixtures/second_real_spy_ideal_replay_v1_fixture.json`; `historical_signal_replay/reports/second_real_spy_ideal_replay_v1_summary.json`; `historical_signal_replay/fixtures/first_real_qqq_clean_fast_break_replay_v1_fixture.json`; `historical_signal_replay/reports/first_real_qqq_clean_fast_break_replay_v1_summary.json`; `historical_signal_replay/fixtures/first_real_iwm_continuation_replay_v1_fixture.json`; `SAFE_FAST_IWM_CONTINUATION_001_CHART_ONLY_OUTCOME_REVIEW.md`; `historical_signal_replay/fixtures/first_real_gld_ideal_replay_v1_fixture.json`; `SAFE_FAST_GLD_IDEAL_001_CHART_ONLY_OUTCOME_REVIEW.md`; and corresponding SPY, QQQ, IWM, and GLD source CSV refs under `historical_signal_replay/source_data/incoming/`.
- Implementation result: `build_first_real_historical_example_batch()` returns exactly 4 local in-memory real historical examples: `Ideal` / `SPY`, `Clean Fast Break` / `QQQ`, `Continuation` / `IWM`, and `Ideal` / `GLD`.
- Proof-chain run result: `records_processed=4`, `records_accepted=4`, `records_rejected=0`; represented symbols are `SPY`, `QQQ`, `IWM`, and `GLD`; represented setup types are `Ideal`, `Clean Fast Break`, and `Continuation`; represented pairs are `Ideal` / `SPY`, `Clean Fast Break` / `QQQ`, `Continuation` / `IWM`, and `Ideal` / `GLD`.
- Outcome group result: worked `2`, failed `0`, inconclusive `0`, pending `0`, stale `0`, invalidated `0`, missing evidence `2`.
- Interpretation: SPY Ideal and QQQ Clean Fast Break are source-backed worked chart/setup behavior examples. IWM Continuation and GLD Ideal are source-backed real candidate examples but remain missing-evidence/inconclusive because repo evidence does not prove accepted numeric trigger, numeric invalidation, and freshness/final signal fields.
- Review output result: `review_conclusion=not_enough_evidence_for_next_fix_path`; worked samples `2`; failed samples `0`; inconclusive/missing-evidence samples `2`; `historical_success_claimed=False`; `final_viability_proven=False`; `profitability_claimed=False`; `optimization_started=False`.
- Focused validation result: `python -m unittest discover -s tests -p test_setup_outcome_historical_sample_path.py` PASS (`32` tests).
- Manual in-memory proof-chain validation result: PASS; the batch ran through `run_setup_outcome_historical_sample_path(...)` and `review_setup_outcome_historical_sample_path_output(...)` with no file/network/subprocess/thread/live/broker side effects.
- git diff whitespace check: PASS with `git diff --check` (exit 0; LF-to-CRLF working-copy warnings for `SAFE_FAST_BUILD_STATE.md`, `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`, `tests/test_setup_outcome_historical_sample_path.py`, `watcher_foundation/__init__.py`, and `watcher_foundation/setup_outcome_historical_sample_path.py` only).
- Current next-step plan file: `SAFE_FAST_LOCAL_NEXT_STEP_PLAN_AFTER_FIRST_REAL_HISTORICAL_EXAMPLE_BATCH.md`.
- Current Day 35 plan correction: the previous plan lacked a concrete inventory filename, so this correction names the exact future inventory file and allowed future docs-only edit scope.
- Exact future inventory file: `SAFE_FAST_REAL_HISTORICAL_IWM_GLD_MISSING_EVIDENCE_INVENTORY.md`.
- Current plan summary: inspect existing repo evidence for IWM Continuation and GLD Ideal before any code change. The plan names the exact missing accepted evidence: accepted final signal row, accepted triggered state, no primary blocker, numeric trigger, trigger basis, numeric invalidation, invalidation basis, freshness/final signal fields, blocker/caution priority, terminal outcome inputs, and chart risk denominator as applicable by setup.
- IWM Continuation evidence status: repo contains source-backed candidate and post-candidate movement evidence, but the candidate remains `PENDING`, `completed_shelf_break_candidate_TO_REVIEW`, blocked by `trigger_level_TO_REVIEW`, with null trigger/invalidation and fresh/spent status still `TO_REVIEW`. It must remain missing-evidence/inconclusive unless exact accepted proof is found.
- GLD Ideal evidence status: repo contains source-backed candidate and post-candidate movement evidence, but the candidate remains `PENDING`, `setup_confirming_TO_REVIEW`, blocked by `completed_candle_hold_unconfirmed`, with null trigger/invalidation and accepted signal/freshness/final fields unconfirmed. It must remain missing-evidence/inconclusive unless exact accepted proof is found.
- Smallest next evidence-backed gap: create `SAFE_FAST_REAL_HISTORICAL_IWM_GLD_MISSING_EVIDENCE_INVENTORY.md` as a docs-only IWM/GLD missing-evidence inventory from existing repo sources only; list every candidate/accepted-row possibility and whether each required field is present, null, `TO_REVIEW`, `UNCONFIRMED`, or absent.
- Allowed edits for the future docs-only inventory task: `SAFE_FAST_REAL_HISTORICAL_IWM_GLD_MISSING_EVIDENCE_INVENTORY.md`; `SAFE_FAST_BUILD_STATE.md`; `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`.
- Future inventory evidence boundary: check existing repo sources only and do not invent evidence.
- Future inventory required answers: what exact evidence is missing for IWM Continuation; what exact evidence is missing for GLD Ideal; whether accepted trigger evidence exists; whether accepted invalidation evidence exists; whether accepted freshness/final-signal evidence exists; whether accepted blocker evidence exists; whether accepted terminal outcome evidence exists; where evidence exists, if it exists; if evidence does not exist, keep the examples missing-evidence/inconclusive; smallest next evidence-backed fix.
- Validation for this docs-only task: unit tests not run per instruction; `git diff --check` PASS (exit 0; LF-to-CRLF working-copy warnings for `SAFE_FAST_BUILD_STATE.md` and `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md` only). New plan file checked with `git diff --no-index --check -- NUL SAFE_FAST_LOCAL_NEXT_STEP_PLAN_AFTER_FIRST_REAL_HISTORICAL_EXAMPLE_BATCH.md`; no whitespace errors were reported, with the expected file-difference exit and LF-to-CRLF warning only.
- Validation for this Day 35 plan correction: tests not run because docs-only; `git diff --check` PASS (exit 0; LF-to-CRLF working-copy warnings for `SAFE_FAST_BUILD_STATE.md`, `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`, and `SAFE_FAST_LOCAL_NEXT_STEP_PLAN_AFTER_FIRST_REAL_HISTORICAL_EXAMPLE_BATCH.md` only).
- Current task scope: docs only; no code changes, no tests changed, no `main.py`, no engine logic, no Railway/deploy, no live data, no controlled shadow data, no alerts, no broker/order/account/options/P&L, no account sizing, no generated reports/logs, no rule change, no optimization, no final viability claim, no historical success claim, no profitability claim, and no live trade decisions.

## Still unproven

Still not proven:

- final trading-plan viability
- profitability
- actual historical success
- controlled shadow data
- live data
- alerts
- generated reports/logs
- trading success
- broker/order execution
- option P&L
- account sizing
- production readiness
- Railway/deploy readiness
- live backend readiness
- live trade decisions

Do not claim any of these are proven.

## Strict no-go boundaries

No main.py.
No engine logic.
No live data.
No controlled shadow data unless explicitly authorized later.
No watcher loops.
No alerts.
No generated reports/logs unless explicitly authorized later.
No broker/order/account/options/P&L.
No account sizing.
No production/Railway/deploy.
No live backend.
No live trade decisions.
No secrets.
No .env files.
No credentials.
No tokens.
No deployment settings.
No direct GitHub writes.

## Six active concerns to solve

These are active build requirements, not side notes.

### 1. Stop endless infrastructure before real evidence

Concern:

The project has built a lot of proof machinery. It cannot keep building containers forever without real examples.

Required response:

After the historical proof bundle readiness gate, move toward a small local historical sample path.

The system must run a small controlled set of local historical setup examples through this chain:

setup appeared -> what happened after -> diagnosis -> evidence packet -> packet readiness -> group review -> group review readiness -> historical proof bundle -> bundle readiness

This is local controlled evidence work, not live data.

### 2. Define complete enough to trust

Concern:

“Complete enough to trust” can become vague.

Required response:

The readiness gate now makes it strict.

A historical proof bundle should only be reviewable if it has:

- setup type separation
- symbol separation
- setup-type-plus-symbol pair tracking
- evidence references
- missing evidence listed
- worked patterns
- failed patterns
- repeated fix paths
- regression tests named
- proof gaps shown
- no-trade boundary preserved
- no optimization claim
- lower-tier review summary

If not complete, the system must say exactly what is missing.

### 3. Protect no-hindsight boundaries

Concern:

Historical proof becomes fake if later outcome data is used to justify the original setup.

Required response:

Every proof object must separate:

- what was known when the setup appeared
- what happened after the setup appeared
- outcome evidence
- missing evidence
- review conclusion

If later information is used to justify the original signal, the proof is invalid.

### 4. Keep worked/failed separate from profitable

Concern:

A setup can work on the chart but still not be profitable.

Required response:

Current proof layer judges chart/setup behavior only.
Profitability is a later layer.

Do not claim profitability from worked/failed setup behavior.

### 5. Do not combine symbols or setup types too early

Concern:

Combined scores can hide weak parts.

Required response:

Every proof review must preserve separation by:

- Ideal
- Clean Fast Break
- Continuation
- SPY
- QQQ
- IWM
- GLD
- setup-type-plus-symbol pair

A combined score can come later only after the pieces are proven separately.

### 6. Avoid circular review packets

Concern:

A bundle cannot be trusted just because an earlier gate said it was ready.

Required response:

Every bundle must carry enough detail to review:

- what setup appeared
- what happened after
- evidence used
- missing evidence
- diagnosis
- likely cause candidate
- next fix path
- regression needed
- lower-tier handoff summary

A lower-tier chat should not need giant raw logs or hidden repo context to understand the packet.

## Next objective

After this combined docs-only batch is committed, the next evidence-backed objective is to create or accept bounded real historical evidence packets for IWM Continuation and GLD Ideal, preserving missing-evidence/inconclusive status until accepted proof exists.

Current changed files should be limited to:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`
- `SAFE_FAST_TECHNICAL_INDICATOR_AND_EVIDENCE_COMPONENT_INVENTORY.md`

Unfinished item:

Final viability, profitability, actual historical success, controlled shadow readiness, live readiness, production readiness, and Railway readiness remain unproven. The implemented first real historical batch covers only 4 of 12 setup-type-plus-symbol pairs. IWM Continuation and GLD Ideal remain missing-evidence/inconclusive until accepted trigger/invalidation/freshness evidence exists. Bundle readiness still has tiny-sample/upstream review contract gaps and must not be treated as final lower-tier readiness.

## Next-after-next objective

After the next bounded IWM/GLD evidence packet work is accepted, reassess the smallest evidence-backed fix. A bounded 1H/24H support-resistance and room-classification design/test plan remains only a later candidate if explicitly requested. Do not mix that with broker integration, order automation, option P&L, account sizing, production work, or live trade decisions.

## Final UI direction

The final UI is not a trade recommendation screen.

It should not simply say “buy” or “trade this.”

It must show:

- setup state
- evidence
- missing evidence
- blockers
- no-trade / watch-only / shadow / pilot / blocked status
- historical outcome proof
- diagnostics
- next fix path
- regression protection
- current mode

Modes should be separate:

- local/replay review
- historical proof review
- controlled shadow review
- live-data shadow review
- pilot review, only later if authorized

Proof layers should stay separate by:

- setup type
- symbol
- stage
- market condition
- trigger status
- blocker/caution status
- freshness state
- session-boundary state

No combined score until the parts are proven separately.

Use rule/evidence language:

- valid by rule
- missing evidence
- inconclusive
- unavailable evidence
- blocked
- stale
- spent
- invalidated
- needs review

Avoid vague language:

- looks good
- strong setup
- weak signal
- probably valid
- maybe tradable

The UI should eventually include:

- diagnostics workbench
- optimization gate
- discretion audit panel
- lower-tier handoff/review mode
- compact evidence packet export

## Final success condition

The finish line is not:

“The watcher works.”

The finish line is:

SAFE-FAST proves a viable trading-plan path, or it produces diagnostics strong enough to show exactly why it is not viable yet and what must be fixed next.

Do not drift into endless build work without proof.

Every next step must move toward evidence, diagnostics, regression protection, or lower-tier transferability.
