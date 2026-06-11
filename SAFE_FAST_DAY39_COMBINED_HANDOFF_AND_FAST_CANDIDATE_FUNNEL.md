# SAFE-FAST Day 39 Combined Handoff and Fast Candidate Funnel

## Purpose

This file preserves the Day 39 takeover handoff plus the candidate-discovery speedup rule.

It exists so future chats can read the repo directly instead of depending on prior chat memory.

This is docs-only preservation.

It does not authorize live trading, live data, broker/order/account/options/P&L, account sizing, alerts, Railway, production, generated reports/logs, secrets, engine logic changes, `main.py`, or live trade decisions.

## Current working context

- Repo: safe-fast-backendnew
- Local path: C:\Users\nickm\Desktop\New folder\safe-fast-backendnew
- Branch: main
- Baseline: patch8
- Current working day: Day 39
- Build-only mode
- This is not live trade chat
- Latest verified commit before this preservation: 0f2fe9a Add Day 38 replacement source pool pass for bad added candidates
- Repo status before this preservation was expected clean

## First action for future chats

Do not assume this handoff is current until local git verifies it.

Future chats must ask the user to run:

Set-Location "C:\Users\nickm\Desktop\New folder\safe-fast-backendnew"
git --no-pager status --short
git --no-pager log -1 --oneline
git --no-pager log --oneline -20

Rules:

- Real local git status and git log are source of truth.
- If status is dirty, stop and identify dirty files.
- If latest commit disagrees with this handoff, stop and identify the conflict.
- Do not claim to have read files unless Codex/local commands actually read them.

## Repo package rule

The handoff package is in the repo.

Future chats cannot see prior chats or uploaded files unless the user pastes them.

Future chats must read repo files directly.

Required first repo reads:

1. SAFE_FAST_BUILD_STATE.md
2. SAFE_FAST_ARCHITECT_CONTROL_AND_PROJECT_TIGHTENING.md
3. SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md
4. SAFE_FAST_PROFITABILITY_DEFINITION_AND_DECISION_POLICY_HARDENING_PLAN.md when strategic/profitability decisions are involved
5. Latest Day 38 / Day 39 review files referenced by git log
6. Relevant watcher_foundation modules and tests for the active build task

Living handoff:

- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md is still the living handoff file.
- Day 33 in the filename is historical.
- Current working day is Day 39.
- SAFE_FAST_ARCHITECT_CONTROL_AND_PROJECT_TIGHTENING.md is durable project-control guidance for tightening the candidate funnel, preventing chart-explanation drift, and preserving the 24 architect Q&A.
- Current strict intake state remains: source-pool rows inspected 24; accepted intake count 6; intake-ready count 0; close-ready count 6; top blocker family is freshness/final-signal plus blocker/caution unresolved.

## Codex rule

Use the known-working unelevated Windows sandbox:

codex.cmd -c 'windows.sandbox="unelevated"' --sandbox workspace-write --ask-for-approval never

Codex failure recovery:

- If Codex shows WebSocket fallback, stream disconnect, os error 10055, or repeated backend transport failure, stop immediately.
- Do not retry the same task repeatedly.
- Restart the laptop.
- Reopen PowerShell.
- Set repo location again.
- Verify git status and git log.
- Resume only with a small bounded Codex task.
- Tiny Codex connectivity tests that do not use the unelevated sandbox are not valid tests of the user's working setup.

## Communication rules

- Speak in short, direct, normal English.
- Be concise.
- No filler.
- Do not think out loud.
- Do not make the user pull meaning out of project jargon.
- Human meaning first.
- Commands only when needed.
- Do not use copy blocks unless the user should paste them somewhere.
- Keep the build moving.
- If something is unclear, read the repo docs first.
- If a plan changes, say exactly what changed, why, what it affects, what it does not affect, and whether it must be preserved in the handoff.

## Hard project rule

SAFE-FAST is not being built merely to test whether an idea might work.

SAFE-FAST's required build target is a profitable trading plan.

Profitability is the target, not a guaranteed claim.

Profitability cannot be claimed until evidence proves it.

If SAFE-FAST is unprofitable, weak, not useful enough, unsuccessful in evidence, missing evidence, or inconclusive, that result is not an ending by itself. It is a mandatory diagnosis-and-fix trigger.

Every unsuccessful, weak, missing, or inconclusive result must identify:

- affected setup type
- affected symbol
- missing or bad evidence
- whether the failure is trigger, invalidation, freshness/final-signal, blocker handling, terminal outcome, timing, rule behavior, signal quality, evidence quality, selection stability, or trading usefulness
- smallest next evidence-backed fix
- replay/regression protection required before promotion

Preserved meanings:

- "Not useful enough" is not a final result. It is a repair signal.
- "Unprofitable" is not a stopping point. It is a diagnosis requirement.
- "Missing evidence" is not low confidence. It is a blocker.
- A weak result cannot be treated as an ending unless a hard blocker is proven and documented.
- Recognition success is not trading profitability.
- A setup must not count as worked just because price eventually moved in the right direction.
- SAFE-FAST must become excellent at making money, not merely excellent at explaining charts.
- The final profitable trading plan does not have to preserve every setup type, every symbol, or every original assumption.
- Anything that cannot support profitability must be fixed, narrowed, isolated, removed, or documented as a blocker.

## Trading-usefulness gate

A setup only supports the profitability target if:

- setup-time evidence was valid
- signal was not stale
- invalidation was clear
- blockers were handled
- setup was early enough to matter
- remaining move had enough room to matter
- outcome was strong enough after timing/cost awareness
- no hindsight was used

Treat "too late" as a real failure:

- Correct idea, late signal is not a clean win.
- Correct setup, bad timing is not a clean win.
- Correct direction, not enough remaining room is not a clean win.
- A late system can look smart in review and still lose money.

## Do-nothing rule

Doing nothing is a first-class result.

A profitable trading plan is not only about finding trades. It must avoid bad trades.

Historical evidence must include:

- clean winners
- failures
- blocked setups
- tempting no-trades
- missing-evidence examples
- late-signal examples
- wrong-winner examples
- messy examples

## Setup and symbol survival rule

Ideal, Clean Fast Break, Continuation, SPY, QQQ, IWM, and GLD must each earn their place.

A setup type or symbol does not need to survive unchanged if evidence says it hurts the plan.

Strong combinations must not hide weak combinations.

The final trading plan may use only the combinations that prove useful.

## Where profitability is determined

- Day 39 evidence work does not determine profitability.
- Day 54 determines whether the compact handoff package is usable by the $20 tier.
- Day 60 is the hard historical evidence checkpoint, not an automatic profitability claim.
- Live-data shadow comes only after historical proof earns shadow planning.
- Shadow means no trades, no broker, no alerts, no sizing, no money, no live trade decisions.
- Actual-money profitability can only be judged after a separate approved tiny-money pilot plan.
- No real-money stage starts automatically.

## Holding-period / trade-duration rule

SAFE-FAST does not yet have a final approved holding period.

Current intended framing:

- short-duration
- same-day to short swing
- likely intraday to 1-3 trading days depending on setup type and evidence
- not seconds/minutes scalping
- not multi-week investing
- no automatic overnight hold approved yet
- no automatic weekend hold approved yet

Exact hold rules must be defined by evidence before any money stage.

Do not target a number of trades per day.

Trade only when a full setup qualifies.

Hold from accepted trigger until one of these happens:

- setup works under accepted outcome rules
- setup invalidates
- signal becomes stale/spent
- blocker appears
- setup loses enough room to matter
- evidence-backed exit is reached
- manual execution delay ruins the setup
- option spread/decay/fill quality makes the trade no longer economically useful

Setup-specific current expectation:

- Ideal: likely shortest hold; should work soon after confirmation.
- Clean Fast Break: likely very short hold; if real, it should show strength quickly.
- Continuation: may allow the longest hold of the three, but still not open-ended and still subject to freshness, session-boundary, invalidation, and blocker rules.

Before any real-money stage, SAFE-FAST must define:

- maximum hold by setup type
- whether overnight holds are allowed
- whether Friday/weekend holds are allowed
- exit on invalidation
- exit on stale/spent signal
- exit on blocker
- exit on target/room exhaustion
- exit if manual execution delay ruins the setup
- option spread limits
- option decay/time-in-trade limits
- option fill-quality limits
- no-chase rules
- cancel/skip rules
- what counts as a trade-duration failure

## Execution mechanics / broker rule

SAFE-FAST must separate setup quality from execution quality.

A good setup signal is not a full trading-system win unless signal-to-entry-to-exit can be executed reliably.

Temporary split path may be tastytrade for data/signal observation and Charles Schwab for manual execution.

That split is only a measured bridge.

Preferred future design is one broker for both signal validation and execution if evidence supports it.

Charles Schwab is the current preferred future broker candidate because the user is familiar with it and options permissions are there.

tastytrade remains an alternate future path if permissions or preference change.

This does not authorize broker/API/order automation now.

Any future Schwab/tastytrade integration must come only after historical proof and live-data shadow justify it, and only with explicit authorization.

No real-money stage may begin until entry, invalidation, exit, spread limits, delay limits, no-chase rules, stop rules, cancel/skip rules, review rules, and failure definitions exist.

## Technical indicator rule

Repo-backed current terms:

- 1H 50 EMA / EMA50
- ATR
- OHLCV / volume
- trend/context
- setup type
- trigger
- invalidation
- blocker
- freshness/stale/spent
- final verdict/final signal
- setup-time/no-hindsight boundary
- terminal chart-outcome fields where inputs exist
- winner selection

Limited/planned/not accepted:

- VWAP is source/export/planning only unless later accepted.
- Bollinger Bands are planning only.
- SMA, MACD, RSI, relative volume, opening range, ORB, high of day, and low of day are not accepted current SAFE-FAST indicators.
- Do not add indicators without repo-backed design, tests, and build-state update.

## Current evidence state

- Pool expanded to 24 candidates.
- No proof accepted.
- No profitability claim.
- IWM/GLD remain missing-evidence/inconclusive unless exact accepted setup-time, trigger, invalidation, freshness, blocker, no-hindsight, and outcome proof exists.

## Day 38 result

- Full 20-candidate review was committed.
- Top 5 were reviewed.
- Top 5 remained blocked.
- Large SPY/QQQ source-pool expansion added 4 candidates.
- Added 4 were reviewed.
- Result: 2 blocked, 2 replace.
- Replacement source-pool pass found 3 cleaner-looking candidates but they were duplicates:
  - SPY-SOURCE-WINDOW-CONTINUATION-002
  - SPY-SOURCE-WINDOW-CONTINUATION-003
  - QQQ-SOURCE-WINDOW-CLEAN-FAST-BREAK-002
- Replacements added: 0.
- Latest verified commit from the prior handoff: 0f2fe9a Add Day 38 replacement source pool pass for bad added candidates.

## Latest 20 commits from prior verification

- 0f2fe9a Add Day 38 replacement source pool pass for bad added candidates
- e74ab27 Add Day 38 added 4 fixture-ready replay review
- 94c1741 Add Day 38 added 4 fixture-ready replay request
- 6040059 Add Day 38 added 4 row-by-row replay readiness review
- 4c320fa Add Day 38 added 4 replay readiness worksheet
- c21642e Add Day 38 large SPY QQQ source pool expansion pass
- f6cb08e Preserve Day 38 speed discipline rule
- 337f36c Add Day 38 QQQ blocker resolution review
- b81fe90 Add Day 38 QQQ replay readiness packet
- deb1234 Add Day 38 QQQ repeat path batch review
- dd517ea Add Day 38 QQQ repeat row packet
- d71adb7 Add Day 38 top 5 replay setup-time field completion review
- 0b0c5c5 Add Day 38 top 5 replay setup-time packet
- 9c9edb6 Add Day 38 kept candidates batch replay setup-time worksheet
- 18ce830 Add Day 38 full 20 candidate deep batch review
- c4d8f87 Add Day 38 top 5 candidates deep batch review
- 1b318fe Add Day 38 SPY source window Continuation 002 review
- e172ee1 Add Day 38 full 20 candidate batch worklist
- 1fc1766 Add Day 38 SPY QQQ source window candidate pass
- 9a110e2 Add Day 38 SPY QQQ batch candidate expansion review

## Best available next work from prior handoff

Run one batch setup-time replay review for already-counted cleaner candidates:

- SPY-SOURCE-WINDOW-CONTINUATION-002, lines 156-169
- QQQ-SOURCE-WINDOW-CLEAN-FAST-BREAK-002, lines 66-86

Do both together.

For each candidate, review:

- exact setup candle
- trigger
- failure level / invalidation
- freshness
- blocker
- outcome
- no-hindsight check
- missing fields
- keep / block / drop / replace
- fastest next action

If both remain blocked:

- stop drilling them
- expand the source pool again

## Candidate-discovery speedup rule

The last few days have gone too slowly.

The problem is not the proof standard. The proof standard is correct.

The problem is that the workflow has spent too much time deep-reviewing weak or already-known-blocked candidates instead of using a faster funnel.

Do not start with deep proof review.

Start with a fast screen that classifies candidates into four buckets:

1. ready for deep review
2. blocked but maybe fixable
3. duplicate / already counted
4. drop / replace

Only bucket 1 gets deep review.

## Candidate completeness screen

A candidate should not get deep review unless it already has:

- exact setup candle
- trigger
- invalidation / failure level
- freshness or final-signal status
- blocker/caution status
- no-hindsight boundary
- outcome window
- source row reference

If those are missing, mark the candidate blocked fast and replace it.

Day 39 runnable helper now exists for this screen:

- Helper: `watcher_foundation/candidate_completeness_screen.py`
- Tests: `tests/test_candidate_completeness_screen.py`
- Command: `python -B -m watcher_foundation.candidate_completeness_screen`
- Current helper result: 24 candidates represented; ready 0; blocked 20; replace 3; drop 1.
- The helper prints the ranked table to stdout only and creates no generated report/log file.
- Missing evidence remains blocked, not low confidence.
- Duplicate, drop, and replace rows are not promoted.
- No proof was accepted.
- No profitability claim was made.

## Strict source-pool intake helper

Day 39 now also has a strict source-pool intake helper:

- Helper: `watcher_foundation/candidate_source_pool_intake.py`
- Tests: `tests/test_candidate_source_pool_intake.py`
- Command: `python -B -m watcher_foundation.candidate_source_pool_intake`

Why this handoff changed:

- The workflow now separates the 24-candidate completeness screen from strict source-pool intake.
- The intake helper rejects chart-shape-only rows and rows without repo-backed setup candle, trigger, invalidation, no-hindsight boundary, and outcome input.
- The helper prints to stdout only and creates no generated report/log file.
- Current intake result after Ideal narrowing: source-pool rows inspected 60; accepted intake count 7; intake-ready count 0; blocked/drop/replace/duplicate counts 5/0/2/0; close-ready count 5.
- Current intake result after applying Clean Fast Break source-data insufficiency decisions: source-pool rows inspected 60; accepted intake count 7; intake-ready count 0; blocked/drop/replace/duplicate counts 5/0/2/0; close-ready count 5.
- Current intake result after applying intrabar ordering narrowing: source-pool rows inspected 60; accepted intake count 7; intake-ready count 0; blocked/drop/replace/duplicate counts 4/0/3/0; close-ready count 4.
- Current intake result after applying context/caution source-data insufficiency: source-pool rows inspected 60; accepted intake count 7; intake-ready count 0; blocked/drop/replace/duplicate counts 4/0/3/0; close-ready count 4.
- `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` remains `blocked` by gap-context and CFB expiry source insufficiency.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` remains `blocked` by CFB expiry and context/caution rule insufficiency.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` remains `blocked` by CFB expiry and context/caution rule insufficiency.
- Context/caution review is now applied as `SOURCE_DATA_INSUFFICIENT`: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`, `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`, `SPY-REAL-HISTORICAL-IDEAL-001`, and `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` stay blocked unless future source-backed context/caution rules exist.
- `QQQ-REAL-HISTORICAL-CONTINUATION-001` is `replace` because it is next-session/session-boundary-dependent and outside the narrowed Continuation path without a source-backed carry-forward rule.
- `SPY-REAL-HISTORICAL-CONTINUATION-001` is `replace` because it is intrabar-ordering-dependent and outside the narrowed Continuation path without lower-timeframe/order-of-events evidence.
- `QQQ-REAL-HISTORICAL-IDEAL-001` is `replace` because it is fast-swing/wide-risk-dependent and outside the narrowed Ideal path without source-backed freshness and room/risk threshold rules.
- `SPY-REAL-HISTORICAL-IDEAL-001` remains `blocked`; same-session Ideal may remain eligible only if stale/spent expiry and complete context/caution gates become clean.
- Top remaining blocker family: freshness/final-signal plus blocker/caution unresolved.
- Current exact blocker: local docs/data support only 7 strict source-backed candidates, not 20-50 strict candidates, and two accepted rows are outside narrowed setup paths.
- No proof was accepted.
- No profitability claim was made.

## Rule-family decision table

Day 39 now has a hard decision table for the nine freshness/final-signal and blocker/caution rule families that block the seven strict rows:

- Decision table: `SAFE_FAST_RULE_FAMILY_DECISION_TABLE.md`
- This is rule clarification only.
- It is not proof review.
- It does not accept proof.
- It does not claim profitability.
- Current rule-family result: `DEFINE_FROM_REPO_EVIDENCE` 0, `SOURCE_DATA_INSUFFICIENT` 4, `KILL_OR_NARROW_SETUP_SYMBOL_PATH` 5.
- Current intake-ready count remains 0.
- Applied Clean Fast Break source-data insufficiency: Clean Fast Break rows cannot become intake-ready unless future source-backed expiry and gap-context rules exist.
- Applied Continuation narrowing: cross-session / next-session Continuation cannot become intake-ready unless a future source-backed carry-forward rule exists.
- Applied Ideal narrowing: fast-swing / wide-risk Ideal cannot become intake-ready unless future source-backed rules define Ideal freshness expiry and room/risk thresholds.
- Applied intrabar ordering narrowing: SPY Continuation cannot become intake-ready while it depends on unresolved order-of-events inside completed 1H candles.
- Applied context/caution source-data insufficiency: rows needing complete context/caution review cannot become intake-ready from primary blocker null alone.

## Rule-decision survival map

Day 39 now has the final rule-decision survival map after applying Continuation, Ideal, Clean Fast Break, intrabar ordering, and context/caution decisions:

- Survival map: `SAFE_FAST_RULE_DECISION_SURVIVAL_MAP.md`.
- Strict rows covered: 7.
- All 9 rule-family decisions are applied.
- `active_blocked`: 4.
- `replace`: 3.
- `parked`: 0.
- `intake_ready`: 0.
- Proof allowed rows: 0.
- `QQQ-REAL-HISTORICAL-CONTINUATION-001`: `replace`.
- `QQQ-REAL-HISTORICAL-IDEAL-001`: `replace`.
- `SPY-REAL-HISTORICAL-CONTINUATION-001`: `replace`.
- `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`: `active_blocked`.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`: `active_blocked`.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`: `active_blocked`.
- `SPY-REAL-HISTORICAL-IDEAL-001`: `active_blocked`.
- Active blocked next evidence fixes: source-backed QQQ gap-context evidence; Clean Fast Break expiry rules; SPY Ideal stale/spent expiry; complete context/caution review fields.
- Replacement next evidence fixes: same-session Continuation evidence or tested carry-forward rule; lower-timeframe/order-of-events Continuation evidence; inside-path Ideal evidence or tested fast-swing freshness plus room/risk thresholds.
- Rule-gate CLI now prints the survival summary.
- Source-pool intake CLI now prints survival active_blocked/replace/parked/intake_ready counts.
- No proof was accepted.
- No profitability claim was made.

## Active-path evidence requirements

Day 39 now has the active-path evidence requirement table for the four `active_blocked` rows:

- Requirement table: `SAFE_FAST_ACTIVE_PATH_EVIDENCE_REQUIREMENTS.md`.
- Active rows covered: 4.
- Requirement rows: 9.
- `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`: missing source-backed QQQ gap-context evidence, tested Clean Fast Break stale/spent expiry, and complete context/caution fields.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`: missing tested higher-base/fresh-break expiry and complete context/caution fields.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`: missing tested initial-break expiry and complete context/caution fields.
- `SPY-REAL-HISTORICAL-IDEAL-001`: missing tested SPY Ideal stale/spent expiry and complete context/caution fields.
- Current repo has enough data for each active row: NO.
- Proof allowed rows: 0.
- Rule-gate CLI now prints active-path evidence requirements.
- Source-pool intake CLI now prints active-path coverage, proof-allowed count, and current repo data availability by active row.
- Proof accepted: NO.
- Profitability claim made: NO.

## QQQ Clean Fast Break survival action

- Candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.
- Survival action applied: YES.
- Status: `active_blocked`.
- Exact missing evidence:
  - source-backed QQQ gap-context completeness field/rule.
  - tested Clean Fast Break stale/spent expiry rule.
  - complete source-backed context/caution review fields.
- Clean rule evidence found: none.
- Accepted intake count: 7.
- Intake-ready count: 0.
- Survival counts remain `active_blocked` 4, `replace` 3, `parked` 0, `intake_ready` 0.
- Proof accepted: NO.
- Profitability claim made: NO.

## SPY Clean Fast Break 003 survival action

- Candidate: `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`.
- Survival action applied: YES.
- Status: `active_blocked`.
- Repo-backed clean rule evidence found: none.
- Exact missing evidence:
  - tested Clean Fast Break higher-base/fresh-break expiry rule.
  - complete source-backed context/caution review fields.
- Applied result: SPY Clean Fast Break 003 cannot promote through missing higher-base/fresh-break expiry or incomplete context/caution.
- Accepted intake count: 7.
- Intake-ready count: 0.
- Survival counts remain `active_blocked` 4, `replace` 3, `parked` 0, `intake_ready` 0.
- Proof accepted: NO.
- Profitability claim made: NO.

## SPY Clean Fast Break 002 survival action

- Candidate: `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`.
- Survival action applied: YES.
- Status: `active_blocked`.
- Repo-backed clean rule evidence found: none.
- Exact missing evidence:
  - tested Clean Fast Break initial-break expiry rule.
  - complete source-backed context/caution review fields.
- Evidence inspected:
  - `historical_signal_replay/reports/third_real_spy_clean_fast_break_replay_v1_signal_log.jsonl` line 2: completed 2026-04-13 12:30 initial-break signal-stage candidate, `final_verdict=TRADE`, `trigger_state=triggered`, `trigger_level=682.03`, `invalidation=678.45`, `primary_blocker=null`.
  - `historical_signal_replay/reports/third_real_spy_clean_fast_break_replay_v1_signal_log.jsonl` line 3: same-session follow-through/spent lifecycle context, not an accepted setup-time expiry rule.
  - `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` line 138: setup-time source row for the 2026-04-13 12:30 signal.
- Applied result: SPY Clean Fast Break 002 cannot promote through missing initial-break expiry or incomplete context/caution.
- Accepted intake count: 7.
- Intake-ready count: 0.
- Survival counts remain `active_blocked` 4, `replace` 3, `parked` 0, `intake_ready` 0.
- Proof accepted: NO.
- Profitability claim made: NO.

## SPY Ideal survival action

- Candidate: `SPY-REAL-HISTORICAL-IDEAL-001`.
- Survival action applied: YES.
- Status: `active_blocked`.
- Repo-backed clean rule evidence found: none.
- Exact missing evidence:
  - tested SPY Ideal stale/spent expiry rule.
  - complete source-backed context/caution review fields.
- Evidence inspected:
  - `historical_signal_replay/reports/second_real_spy_ideal_replay_v1_signal_log.jsonl` line 5: completed 2026-05-13 11:30 same-session Ideal signal-stage candidate, `final_verdict=TRADE`, `trigger_state=triggered`, `trigger_level=740.75`, `invalidation=731.83`, `primary_blocker=null`.
  - `historical_signal_replay/reports/second_real_spy_ideal_replay_v1_signal_log.jsonl` line 6: later spent lifecycle row, not an accepted setup-time stale/spent expiry rule.
  - `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` line 291: setup-time source row for the 2026-05-13 11:30 signal.
- Applied result: SPY Ideal cannot promote through missing same-session Ideal stale/spent expiry or incomplete context/caution.
- Accepted intake count: 7.
- Intake-ready count: 0.
- Survival counts remain `active_blocked` 4, `replace` 3, `parked` 0, `intake_ready` 0.
- Proof accepted: NO.
- Profitability claim made: NO.

## Faster workflow

Use this order:

1. Large source pool pass
   - Pull 20-50 possible candidates at once.
   - Do not prove them yet.

2. Fast completeness screen
   - Check whether required fields exist.
   - No narrative review yet.
   - No candidate gets promoted because it looks good.

3. Rank by completeness
   - Highest priority goes to candidates with exact setup-time row, clear trigger, clear invalidation, clear freshness, clean blocker status, and clean outcome window.

4. Deep review only the best batch
   - Review 5-10 candidates at a time.
   - Judge each separately.
   - Keep, block, drop, or replace.

5. Stop drilling weak candidates
   - One blocked result is enough if the blocker is structural.
   - Do not keep re-reviewing the same missing evidence.

6. Expand pool if needed
   - If the batch does not produce enough ready candidates, expand the source pool again.

## Candidate completeness score

Future chats should use existing repo tooling to create or apply a candidate completeness score before deep review.

Minimum completeness fields:

- setup-time row present
- trigger present
- invalidation present
- freshness/final-signal present
- blocker/caution present
- no-hindsight boundary present
- outcome window present
- not duplicate
- not already blocked
- not mixed/ambiguous setup identity

Only candidates above threshold should get deep review.

## Safety does not require slowness

Quality and safety are protected by rules, not by slowness.

Keep these fixed:

- no live data
- no broker
- no alerts
- no Railway/production
- no option P&L
- no account sizing
- no proof claim
- no profitability claim
- no hindsight
- no missing evidence treated as low confidence
- no candidate promoted without exact setup-time proof

## Practical next-chat recommendation

Do not continue with slow one-candidate narrative documents.

Run a batch candidate completeness screen over the 24-candidate pool, produce a ranked table, then deep-review only the top 5-10 candidates that pass minimum setup-time completeness.

The table should include:

- candidate ID
- symbol
- setup type
- source lines
- setup candle
- trigger
- invalidation
- freshness
- blocker
- outcome window
- duplicate yes/no
- status: ready / blocked / drop / replace
- reason
- next action

The goal is not to review more words.

The goal is to find candidates that can actually survive proof.

## Build-vs-docs rule

Do not hide behind docs-only work once the blocker is understood.

If evidence is missing, either collect/source the missing evidence, build the local validator/helper needed to process it, or document the exact blocker and move to the next evidence-backed fix.

Do not keep creating status documents that restate the same blocker.

Each task must move SAFE-FAST closer to evidence, diagnosis, trading usefulness, regression protection, or compact handoff readiness.

## Workflow

- Use local PowerShell and Codex only.
- No direct GitHub writes.
- No GitHub blobs.
- No GitHub edit/write tools.
- Assistant gives one complete PowerShell/Codex block when work is needed.
- User pastes it into PowerShell.
- Codex runs locally using the unelevated sandbox.
- User sends output back.
- Assistant reviews output before commit.
- Guarded commits only.
- Do not push unless explicitly asked.

## No-go rules

- no main.py
- no engine logic unless explicitly evidence-backed and tested
- no live data
- no live trading
- no controlled shadow unless explicitly authorized later
- no watcher loops
- no alerts
- no broker/order/account/options/P&L
- no account sizing
- no Railway/production/deploy
- no generated reports/logs unless explicitly authorized
- no secrets, .env, credentials, tokens, or deployment settings
- no live trade decisions
- no profitability claims
- no fake proof
- no hindsight filling

## Future-chat start requirement

Future chats must start by verifying repo state, then reading the repo docs directly.

Do not rely on this file alone.

Read the repo.
