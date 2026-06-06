# SAFE-FAST Day 33 Project Handoff and Tier Runway

## Current update status

- Baseline: patch8.
- Current working day: Day 35.
- Day 33 status: historical context.
- Mode: build work only, not live trade chat.
- Repo: safe-fast-backendnew.
- Branch: main.
- Latest known local commit before current uncommitted work: e03c792 Add real historical missing evidence inventory plan.
- Latest known completed build commit before this handoff update: e03c792 Add real historical missing evidence inventory plan.
- Current uncommitted status: Day 35 docs-only plan correction; changed files should be limited to `SAFE_FAST_LOCAL_NEXT_STEP_PLAN_AFTER_FIRST_REAL_HISTORICAL_EXAMPLE_BATCH.md`, `SAFE_FAST_BUILD_STATE.md`, and this handoff file.
- Real local git status and git log are source of truth.
- This Day33-named file remains a living handoff document and records this Day 35 update.

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
- Current objective is creating the docs-only next-step plan after the first real historical example batch, focused on IWM Continuation and GLD Ideal missing accepted evidence.
- Current changed files should be limited to `SAFE_FAST_LOCAL_NEXT_STEP_PLAN_AFTER_FIRST_REAL_HISTORICAL_EXAMPLE_BATCH.md`, `SAFE_FAST_BUILD_STATE.md`, and `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`.
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

Assistant review of the Day 35 docs-only plan correction, then commit only expected files if accepted.

Current changed files should be limited to:

- `SAFE_FAST_LOCAL_NEXT_STEP_PLAN_AFTER_FIRST_REAL_HISTORICAL_EXAMPLE_BATCH.md`
- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`

Unfinished item:

Final viability, profitability, actual historical success, controlled shadow readiness, live readiness, production readiness, and Railway readiness remain unproven. The implemented first real historical batch covers only 4 of 12 setup-type-plus-symbol pairs. IWM Continuation and GLD Ideal remain missing-evidence/inconclusive until accepted trigger/invalidation/freshness evidence exists. Bundle readiness still has tiny-sample/upstream review contract gaps and must not be treated as final lower-tier readiness.

## Next-after-next objective

After assistant review and commit, create `SAFE_FAST_REAL_HISTORICAL_IWM_GLD_MISSING_EVIDENCE_INVENTORY.md` as a docs-only IWM/GLD missing-evidence inventory from existing repo sources only, without optimization, profitability claims, live data, alerts, broker behavior, generated reports/logs, or production work.

The next docs-only inventory task may edit only:

- `SAFE_FAST_REAL_HISTORICAL_IWM_GLD_MISSING_EVIDENCE_INVENTORY.md`
- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`

The inventory must decide separately whether IWM Continuation and GLD Ideal have accepted trigger/invalidation/freshness/final-signal proof already in the repo. If yes, plan the smallest later in-memory update and regression test. If no, preserve missing-evidence status and choose the next bounded real historical example without hiding remaining tiny-sample, missing-pair, real-history, or upstream bundle-readiness gaps.

The inventory must check existing repo sources only, must not invent evidence, and must answer whether accepted trigger, invalidation, freshness/final-signal, blocker, and terminal outcome evidence exists; where evidence exists, if it exists; what exact evidence remains missing for IWM Continuation and GLD Ideal; and the smallest next evidence-backed fix.

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
