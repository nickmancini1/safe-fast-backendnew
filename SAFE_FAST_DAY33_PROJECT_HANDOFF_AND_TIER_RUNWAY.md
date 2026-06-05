# SAFE-FAST Day 33 Project Handoff and Tier Runway

## Current update status

- Baseline: patch8.
- Current working day: Day 34.
- Day 33 status: historical context.
- Mode: build work only, not live trade chat.
- Repo: safe-fast-backendnew.
- Branch: main.
- Latest known local commit before current uncommitted work: c228cb1 Add GLD Continuation evidence fix plan.
- Latest known completed build commit before this handoff update: c228cb1 Add GLD Continuation evidence fix plan.
- Current uncommitted status: Day 34 GLD Continuation after-setup evidence implementation; changed files are `watcher_foundation/setup_outcome_historical_sample_path.py`, `tests/test_setup_outcome_historical_sample_path.py`, `SAFE_FAST_BUILD_STATE.md`, and this handoff file.
- Real local git status and git log are source of truth.
- This Day33-named file remains a living handoff document and records this Day 34 update.

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
- Day 33 is historical context for the current Day 34 plan/build-state updates.
- Day 28 file names are historical labels only.
- fc64232 is the latest Day 31 handoff/build-state checkpoint.
- 0d23423 is the Day 31 addendum milestone before that sync.
- 0e4a0c0 is a later intro-block replacement commit.
- Those are not conflicts.
- Sync commits are bookkeeping commits.

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

c228cb1 Add GLD Continuation evidence fix plan

Latest known local commit before current uncommitted work:

c228cb1 Add GLD Continuation evidence fix plan

Current Day 34 implementation status:

- Historical setup sample path planning is complete and committed at `73a27ba Add historical setup sample path plan`.
- Day 33 historical setup sample path runner is complete and committed at `6973581 Add historical setup sample path runner`.
- Controlled historical sample evidence set planning is complete and committed at `0910f54 Add controlled historical sample evidence set plan`.
- First controlled historical sample evidence set is complete and committed at `2ccc021 Add first controlled historical sample evidence set`.
- Controlled sample output review planning is complete and committed at `c880103 Add controlled sample review plan`.
- First controlled historical sample output review is complete and committed at `ba7374b Add controlled historical sample output review`.
- GLD Continuation evidence fix planning is complete and committed at `c228cb1 Add GLD Continuation evidence fix plan`.
- Current objective is Day 34 GLD Continuation after-setup evidence implementation after the controlled historical sample output review.
- Current plan file is `SAFE_FAST_LOCAL_NEXT_STEP_PLAN_AFTER_CONTROLLED_HISTORICAL_SAMPLE_OUTPUT_REVIEW.md`.
- Current changed files are limited to `watcher_foundation/setup_outcome_historical_sample_path.py`, `tests/test_setup_outcome_historical_sample_path.py`, `SAFE_FAST_BUILD_STATE.md`, and `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`; all are within the plan-allowed file set.
- Runner behavior: accepts caller-provided in-memory historical setup examples only, rejects file/report/log path, live-data, controlled-shadow, alert, broker/order/account/options/P&L/account-sizing, live-trade-decision, subprocess/thread/socket, watcher-loop, and `main.py` shaped inputs, runs proof -> diagnostics -> evidence packet -> packet readiness -> group review -> group review readiness -> historical bundle -> bundle readiness, preserves setup-time vs post-setup evidence separation, setup type, symbol, setup-type-plus-symbol pair separation, missing evidence, diagnostics, fix paths, regression needs, lower-tier review fields, and exact bundle-readiness missing review items.
- Sample evidence set behavior: exposes one worked `Ideal` / `SPY` setup, one failed `Clean Fast Break` / `QQQ` setup, and one now-reviewable `Continuation` / `GLD` setup through the existing runner; preserves setup type separation, symbol separation, setup-type-plus-symbol pair separation, setup-time versus after-setup evidence separation, diagnostics, fix paths, lower-tier summary, no-trade/watch-only, no-live-data, no-controlled-shadow, no-alert, no-broker, no-file-write, no-rule-change, and no-optimization boundaries.
- Review behavior: accepts caller-provided in-memory sample path output only, returns one in-memory review summary only, keeps worked, failed, and inconclusive samples separate, keeps setup type and symbol separate, checks no-hindsight boundaries, surfaces useful proof, weak proof, missing evidence, next fix paths, regression needs, lower-tier review material, and explicitly reports the GLD Continuation review status, and defensively copies returned data.
- Review result: the controlled output is useful but not final viability proof. The worked `Ideal` / `SPY` sample gives clear chart-behavior proof; the failed `Clean Fast Break` / `QQQ` sample gives useful diagnosis; the existing `Continuation` / `GLD` sample now has caller-provided after-setup evidence and became reviewable. Bundle readiness still shows tiny-sample/upstream review contract gaps and must not be treated as final lower-tier readiness.
- GLD Continuation status: `reviewable`; `gld_continuation_became_reviewable=True`; `gld_continuation_remains_inconclusive=False`; no final viability, profitability, historical success, optimization, or live trade claim.
- Next objective after this fix: narrow review of what the now-evidenced three-sample controlled set proves and still does not prove, before any broader sample expansion.
- Validation results: focused historical sample path PASS (`24` tests); bundle readiness PASS (`11`); proof review bundle PASS (`13`); review readiness PASS (`12`); review aggregator PASS (`11`); packet readiness PASS (`11`); evidence packet PASS (`12`); diagnostics PASS (`14`); proof PASS (`21`); watcher-foundation scaffold PASS (`6`); `git diff --check` PASS with LF-to-CRLF working-copy warnings only.
- Current implementation scope: local-only in-memory code/test/docs update; no `main.py`, no engine logic, no Railway/deploy, no live data, no controlled shadow data, no alerts, no broker/order/account/options/P&L, no account sizing, no generated reports/logs, no file writes by the runner/review, no rule change, no optimization, no final viability claim, no profitability claim, and no live trade decisions.

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

Review the Day 34 GLD Continuation after-setup evidence implementation before commit, then commit only the plan-allowed changed files if accepted.

Current changed files:

- `watcher_foundation/setup_outcome_historical_sample_path.py`
- `tests/test_setup_outcome_historical_sample_path.py`
- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`

Current plan file:

SAFE_FAST_LOCAL_NEXT_STEP_PLAN_AFTER_CONTROLLED_HISTORICAL_SAMPLE_OUTPUT_REVIEW.md

Unfinished item:

The GLD Continuation after-setup evidence fill is implemented but uncommitted until assistant review and commit. Final viability, profitability, actual historical success, controlled shadow readiness, live readiness, production readiness, and Railway readiness remain unproven.

## Next-after-next objective

Create a narrow review of what the now-evidenced three-sample controlled set proves and still does not prove before broader sample expansion.

That follow-up must preserve the existing worked `Ideal` / `SPY` sample, failed `Clean Fast Break` / `QQQ` sample, and now-reviewable `Continuation` / `GLD` sample. It should ask whether the controlled local examples successfully tested the full chain:

setup appeared -> what happened after -> diagnosis -> packet -> packet readiness -> group review -> group readiness -> historical bundle -> bundle readiness

The first sample path output should remain small, explicit, and easy to inspect. Current result is that GLD Continuation became reviewable after caller-provided after-setup evidence was added. The next review must not broaden samples to hide remaining tiny-sample or upstream bundle-readiness gaps.

The review should answer:

- Can SAFE-FAST handle real-looking setup examples?
- Does the proof chain produce useful diagnostics?
- Does it preserve no-hindsight boundaries?
- Does it keep setup type and symbol separate?
- Does it identify missing evidence?
- Does it produce a review packet that a lower-tier chat can understand?

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
