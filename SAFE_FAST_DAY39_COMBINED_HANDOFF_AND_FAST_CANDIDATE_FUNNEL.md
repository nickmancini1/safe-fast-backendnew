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
2. SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md
3. SAFE_FAST_PROFITABILITY_DEFINITION_AND_DECISION_POLICY_HARDENING_PLAN.md when strategic/profitability decisions are involved
4. Latest Day 38 / Day 39 review files referenced by git log
5. Relevant watcher_foundation modules and tests for the active build task

Living handoff:

- SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md is still the living handoff file.
- Day 33 in the filename is historical.
- Current working day is Day 39.

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
