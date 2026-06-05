# SAFE-FAST Local Next-Step Plan After Setup Outcome Historical Sample Path

## 1. Plain Purpose

Plan the first controlled local historical sample evidence set.

SAFE-FAST can now run caller-provided in-memory historical setup examples through the proof chain. The next build step should define a tiny, inspectable, local-only fixture/evidence set that tests whether the chain is useful on concrete examples before any broader sample expansion, optimization, controlled shadow work, live data, alerts, or reports.

The evidence set should include at least:

- one worked setup
- one failed setup
- one missing-evidence or inconclusive setup
- setup type separation
- symbol separation
- no-hindsight separation between what was known at setup time and what happened after

This plan is docs-only. It does not start code work, tests, live data, controlled shadow data, watcher loops, alerts, generated reports/logs, broker/order/account/options/P&L, account sizing, optimization, production work, or live trade decisions.

## 2. Day 34 Context

- **Baseline:** patch8.
- **Repo:** `safe-fast-backendnew`.
- **Branch:** `main`.
- **Current working day context:** Day 34.
- **Day 33 status:** historical context.
- **Latest local commit before this plan:** `6973581 Add historical setup sample path runner`.
- **Latest completed commit before this plan:** `6973581 Add historical setup sample path runner`.
- **Work mode:** build work only, not live trade chat.
- **Highest priority:** viability proof before optimization.
- **Tier pressure:** the current $200 window must prepare the project for $20-tier continuation in about 30 days.
- **Planning scope:** docs-only local next-step plan after the historical setup sample path runner.
- **Current objective:** plan the first controlled historical sample evidence set.
- **Handoff rule:** `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md` remains a living handoff file and must track this Day 34 update, this objective, this plan file, and the unfinished item to build the first controlled historical sample evidence set next.

## 3. Current Fixed Foundation

The current fixed proof chain is:

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

The historical setup sample path runner is complete and committed at `6973581 Add historical setup sample path runner`.

The fixed foundation is local-only and in-memory. It accepts caller-provided historical setup examples, rejects file/report/log/live/shadow/alert/broker/account/options/P&L/account-sizing/trade-decision/watcher-loop shaped inputs, runs examples through the proof chain, preserves setup-time evidence and post-setup evidence separation, keeps setup type, symbol, and setup-type-plus-symbol pairs separate, exposes missing evidence, diagnostics, fix paths, regression needs, lower-tier review fields, and exact bundle-readiness missing review items, and returns one defensive-copy in-memory summary without profitability, final viability, rule-change, optimization, live-data, alert, broker, file-write, or trade-decision claims.

## 4. What Is Still Unproven

- Final SAFE-FAST trading-plan viability is not proven.
- Profitability is not proven.
- Actual historical success is not proven.
- It is not yet proven whether the runner output is useful on a first controlled historical sample evidence set.
- It is not yet proven whether a tiny evidence fixture can expose worked, failed, and missing-evidence or inconclusive behavior clearly enough for review.
- It is not yet proven whether the current chain gives useful diagnostics, fix paths, and regression needs from concrete historical examples.
- It is not yet proven whether lower-tier review can understand the resulting packet without raw logs or hidden repo context.
- Controlled shadow data, live data, alerts, generated reports/logs, broker/order/account/options/P&L behavior, account sizing, production readiness, Railway/deploy readiness, live backend readiness, live trade readiness, and live trade decisions remain forbidden and unproven.

## 5. Exact Next Implementation Step

Build a local-only in-memory historical setup sample fixture/evidence set and focused tests around the existing sample path runner.

The future fixture should provide a tiny caller-provided set of historical setup examples that the runner can pass through:

- setup appeared
- what happened after
- diagnosis
- evidence packet
- packet readiness
- group review
- group review readiness
- historical proof bundle
- bundle readiness

The first implementation should be small enough to inspect manually. It should not fetch data, read files, write files, generate reports/logs, start watcher behavior, create alerts, change rules, optimize thresholds, or make trade decisions.

The output review question is not "is this profitable?" The output review question is whether the proof chain handles the first concrete historical sample evidence set well enough to expose evidence, missing evidence, diagnostics, next fix paths, and regression needs.

## 6. Exact Sample Categories Needed

The fixture/evidence set must include these categories:

- **Worked setup:** a setup where setup-time evidence is complete enough and post-setup chart/setup behavior matches the plan expectation.
- **Failed setup:** a setup where setup-time evidence is present but post-setup chart/setup behavior fails, invalidates, or otherwise does not match the plan expectation.
- **Missing-evidence or inconclusive setup:** a setup where the chain must explicitly report missing or unavailable evidence, or mark the result inconclusive, instead of fabricating a worked or failed conclusion.
- **Setup type separation:** at least two setup types must appear, selected from Ideal, Clean Fast Break, and Continuation.
- **Symbol separation:** at least two starting symbols must appear, selected from SPY, QQQ, IWM, and GLD.
- **Setup-type-plus-symbol pair separation:** the fixture must preserve pair-level tracking so results do not collapse into one combined score.
- **No-hindsight setup-time evidence:** each example must freeze what was known when the setup appeared.
- **No-hindsight post-setup evidence:** each example must separately describe what happened after setup appearance and must not use later outcome movement to justify the original setup identity.

The fixture should prefer the fewest examples that cover these categories clearly. A likely minimum is three records, but the future implementation may add one extra record only if needed to keep setup type and symbol separation clear without making the fixture hard to inspect.

## 7. Allowed Files for That Future Step

Allowed future implementation files:

- `watcher_foundation/setup_outcome_historical_sample_path.py`
- `watcher_foundation/__init__.py`
- `tests/test_setup_outcome_historical_sample_path.py`
- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`

No other files are allowed for that future implementation step unless the user explicitly expands scope.

## 8. Forbidden Files / Systems

- `main.py`
- trading engine logic
- Railway/deploy files
- production or live backend integration
- generated output paths
- report/log writers
- live data startup or fetching
- controlled shadow data startup
- watcher loops, schedulers, polling, daemons, or background workers
- alert delivery systems
- broker/order/account/options/P&L systems
- account sizing or position sizing systems
- secrets, `.env`, credentials, tokens, keys, or deployment settings
- any code path that can make live trade decisions
- any rule change or optimization before diagnostics identify an evidence-backed gap

## 9. Required Tests for the Future Implementation Step

Add or update focused local unit tests in `tests/test_setup_outcome_historical_sample_path.py` covering:

- the first controlled sample evidence set runs through the existing historical sample path runner
- at least one worked setup is represented
- at least one failed setup is represented
- at least one missing-evidence or inconclusive setup is represented
- setup type separation is preserved
- symbol separation is preserved
- setup-type-plus-symbol pair separation is preserved
- setup-time evidence and post-setup evidence remain separate
- future outcome evidence is not used to define the setup identity
- missing evidence is listed instead of fabricated
- lower-tier review summary remains compact and understandable
- worked/failed chart behavior does not become a profitability claim
- no-trade, no-live-data, no-controlled-shadow-data, no-alert, no-file-write, no-broker, no-rule-change, and no-optimization boundaries are preserved
- the fixture does not call `open`, network sockets, subprocesses, threads, report writers, alert systems, broker/order systems, or `main.py`

Required validation commands for that future implementation:

- `python -m unittest discover -s tests -p test_setup_outcome_historical_sample_path.py`
- `python -m unittest discover -s tests -p test_setup_outcome_proof_review_bundle_readiness.py`
- `python -m unittest discover -s tests -p test_setup_outcome_proof_review_bundle.py`
- `python -m unittest discover -s tests -p test_setup_outcome_review_readiness.py`
- `python -m unittest discover -s tests -p test_setup_outcome_review_aggregator.py`
- `python -m unittest discover -s tests -p test_setup_outcome_packet_readiness.py`
- `python -m unittest discover -s tests -p test_setup_outcome_evidence_packet.py`
- `python -m unittest discover -s tests -p test_setup_outcome_diagnostics.py`
- `python -m unittest discover -s tests -p test_setup_outcome_proof.py`
- `python -m unittest tests.test_watcher_foundation_scaffold`
- `git diff --check`

## 10. Required Build-State / Doc Updates for the Future Step

The future implementation must update `SAFE_FAST_BUILD_STATE.md` with:

- implementation status for the first controlled historical sample evidence set
- baseline `patch8` and Day 34 context, with Day 33 recorded as historical context
- exact implementation file and test file
- focused historical sample path test result
- required proof-chain regression results
- watcher-foundation scaffold regression result
- `git diff --check` result
- preserved scope and no-go boundaries
- next local-only objective after the first controlled sample evidence set

The future implementation must update `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md` with:

- latest commit after implementation
- current objective
- completed milestone
- next objective
- unfinished item
- changed active concerns, if any

Do not claim final viability, historical success, controlled shadow readiness, live readiness, production readiness, Railway readiness, live backend readiness, live trade readiness, or live trade decision readiness.

## 11. Viability Loop

Viability proof is the highest priority.

Required viability loop:

detect -> score outcome -> diagnose deeply -> analyze whole system -> decide fix path -> adjust rule/contract/test -> run regression -> review again

For the future evidence set, this means the examples must not stop at detection. They must carry setup-appeared evidence, post-setup outcome evidence, diagnostics, packet evidence, readiness decisions, review aggregation, bundle readiness, missing evidence, next fix path, and regression needs.

## 12. Diagnostics-Before-Optimization Rule

Diagnostics must come before optimization.

The sample evidence set must expose what failed, what evidence was used, likely cause candidate, affected setup type, affected symbol, affected stage, trigger/invalidation/freshness relationship, blocker/caution relationship, ranking/focus issue, session-boundary issue, data-quality or missing-evidence issue, market-context issue, outcome-scoring issue, review/logging issue, user-facing workflow issue, next fix path, and regression test needed when those facts are available.

No threshold, ranking, trigger, invalidation, freshness, blocker/caution, workflow, alert, or rule optimization may be proposed from the sample evidence set unless diagnostics identify an evidence-backed rule, contract, fixture, planning, or test gap.

## 13. Discretion Rule

Human discretion may exist only as:

- no-trade veto
- review note
- safety pause

Human discretion must never:

- create a signal
- approve a trade
- override missing proof
- move triggers
- hide failures
- change outcome after the fact
- merge setup type and symbol evidence
- mark the sample evidence set reviewable without readiness-gate support

Setup recognition, trigger, invalidation, fresh/stale/spent, blocker/caution, ranking/focus, outcome scoring, diagnostics, evidence packaging, packet readiness, aggregate review, review-readiness gating, bundle review, bundle readiness, and user workflow should be rule-based.

## 14. Lower-Tier Handoff Requirement

The future sample path output must be compact enough for lower-tier review.

It should show:

- what setup appeared
- what was known at setup time
- what happened after setup appearance
- setup type
- symbol
- setup-type-plus-symbol pair
- outcome group
- diagnosis
- evidence packet result
- packet readiness result
- group review result
- group review readiness result
- historical bundle result
- bundle readiness result
- missing evidence
- next fix path
- regression needed
- no-trade/no-live/no-optimization boundary state

A lower-tier chat should not need giant raw logs, hidden repo context, live data, generated reports, or production systems to understand the packet.

## 15. Six Active Concerns From Day 33 Historical Handoff

### 1. Stop endless infrastructure before real evidence

The project has built enough proof machinery to start testing real evidence shape. The next step is the first tiny controlled historical sample evidence set, run through the existing historical sample path runner. This is local controlled evidence work, not live data.

### 2. Define complete enough to trust

The evidence set must preserve setup type separation, symbol separation, setup-type-plus-symbol pair tracking, evidence references, missing evidence, worked patterns, failed patterns, repeated fix paths where available, regression tests, proof gaps, no-trade boundary, no optimization claim, and lower-tier review summary.

### 3. Protect no-hindsight boundaries

Every sample must separate what was known when the setup appeared, what happened after the setup appeared, outcome evidence, missing evidence, and review conclusion. If later information is used to justify the original signal, the proof is invalid.

### 4. Keep worked/failed separate from profitable

The current proof layer judges chart/setup behavior only. Profitability is a later layer. The evidence set must not claim profitability from worked/failed setup behavior.

### 5. Do not combine symbols or setup types too early

Every sample path result must preserve separation by Ideal, Clean Fast Break, Continuation, SPY, QQQ, IWM, GLD, and setup-type-plus-symbol pair. A combined score can come later only after the pieces are proven separately.

### 6. Avoid circular review packets

A bundle cannot be trusted just because an earlier gate said it was ready. The evidence set must carry enough detail to review what setup appeared, what happened after, evidence used, missing evidence, diagnosis, likely cause candidate, next fix path, regression needed, and lower-tier handoff summary.

## 16. No-Hindsight Requirement

The sample evidence set must keep setup-time evidence and post-setup outcome evidence separate.

Allowed:

- use setup-time fields to describe why a setup appeared
- use later fields only to describe what happened after setup appearance
- mark missing or unavailable evidence explicitly

Forbidden:

- backfill trigger validity from later candles
- backfill setup identity from outcome movement
- use post-setup outcome evidence to create the setup label
- change worked/failed status after the fact without explicit outcome evidence
- hide inconclusive or unavailable evidence
- convert chart behavior into profitability or trade readiness

## 17. Setup Type And Symbol Separation

The future evidence set must treat setup type and symbol as separate fields.

Required separate tracking:

- setup type
- symbol
- setup-type-plus-symbol pair
- outcome group by setup type
- outcome group by symbol
- outcome group by setup-type-plus-symbol pair
- missing evidence by setup type
- missing evidence by symbol
- missing evidence by setup-type-plus-symbol pair

The evidence set must not collapse Ideal, Clean Fast Break, Continuation, SPY, QQQ, IWM, and GLD into one combined score before separate review.

## 18. Boundary Statement

This docs-only plan does not start code work, tests, optimization, controlled shadow data, live data, watcher loops, alerts, generated reports/logs, broker/order/account/options/P&L, account sizing, production/Railway/live backend work, or live trade decisions.

This docs-only plan does not modify `main.py`, engine logic, watcher code, tests, Railway/deploy files, secrets, `.env` files, credentials, tokens, deployment settings, generated output paths, report/log writers, watcher loops, alert delivery, broker/order/account behavior, options behavior, option P&L, position sizing, account sizing, or live trade decision logic.
