# SAFE-FAST Local Next-Step Plan After Setup Outcome Proof Review Bundle Readiness

## 1. Plain Purpose

Plan the small local historical sample path.

SAFE-FAST now has the proof chain through historical proof bundle readiness. The next build step should run a small caller-provided, in-memory set of historical setup examples through that chain so the project can see whether the chain actually helps judge setup behavior.

The intended future path is:

setup appeared -> what happened after -> diagnosis -> evidence packet -> packet readiness -> group review -> group review readiness -> historical proof bundle -> bundle readiness

This plan is docs-only. It does not start code work, tests, live data, controlled shadow data, watcher loops, alerts, generated reports/logs, broker/order/account/options/P&L, account sizing, optimization, production work, or live trade decisions.

## 2. Day 33 Context

- **Baseline:** patch8.
- **Repo:** `safe-fast-backendnew`.
- **Branch:** `main`.
- **Current working day context:** Day 33.
- **Latest local commit before this plan:** `7af3506 Add historical proof bundle readiness gate`.
- **Work mode:** build work only, not live trade chat.
- **Highest priority:** viability proof before optimization.
- **Tier pressure:** the current $200 window must prepare the project for $20-tier continuation in about 30 days.
- **Planning scope:** docs-only local next-step plan after the historical setup proof review bundle readiness gate.
- **Handoff rule:** `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md` must track this objective, this plan file, and the unfinished item to build the small local historical sample path next.

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

The latest gate is committed at `7af3506 Add historical proof bundle readiness gate`.

The fixed foundation is local-only and in-memory. It accepts caller-provided proof objects, preserves no-trade/no-live/no-alert/no-broker/no-file-write/no-rule-change/no-optimization boundaries, keeps setup type and symbol separate, carries setup-type-plus-symbol pair evidence, exposes missing evidence and proof gaps, and produces lower-tier review decisions without claiming final viability or profitability.

## 4. What Is Still Unproven

- Final SAFE-FAST trading-plan viability is not proven.
- Profitability is not proven.
- Actual historical success is not proven.
- The chain has not yet been exercised on a small controlled local historical setup sample path.
- It is not yet proven whether the proof chain produces useful diagnostics on concrete historical examples.
- It is not yet proven whether the chain can preserve no-hindsight boundaries while carrying both setup-appeared evidence and post-setup outcome evidence.
- It is not yet proven whether lower-tier review can understand the resulting packet without raw logs or hidden repo context.
- Controlled shadow data, live data, alerts, generated reports/logs, broker/order/account/options/P&L behavior, account sizing, production readiness, Railway/deploy readiness, live backend readiness, live trade readiness, and live trade decisions remain forbidden and unproven.

## 5. Exact Next Implementation Step

Build a local-only in-memory historical setup sample path runner.

The future runner should accept a small caller-provided set of historical setup examples and pass them through:

- setup appeared
- what happened after
- diagnosis
- evidence packet
- packet readiness
- group review
- group review readiness
- historical proof bundle
- bundle readiness

The runner should return one in-memory result that exposes the full path and final bundle-readiness result. It must not read live data, fetch data, write files, generate reports/logs, start watcher behavior, change rules, optimize, or make trade decisions.

The first implementation should be small, explicit, and inspectable. It should prove whether the chain can handle real-looking examples before any broader sample expansion or optimization work.

## 6. Allowed Files for That Future Step

Allowed future implementation files:

- `watcher_foundation/setup_outcome_historical_sample_path.py`
- `watcher_foundation/__init__.py`
- `tests/test_setup_outcome_historical_sample_path.py`
- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`

No other files are allowed for that future implementation step unless the user explicitly expands scope.

## 7. Forbidden Files / Systems

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

## 8. Required Tests for the Future Implementation Step

Add focused local unit tests in `tests/test_setup_outcome_historical_sample_path.py` covering:

- accepts only caller-provided in-memory historical setup examples
- rejects file paths, generated report/log paths, live-data inputs, controlled-shadow inputs, alerts, broker/order/account/options/P&L/account-sizing fields, and live-trade-decision fields
- preserves no-hindsight separation between what was known when the setup appeared and what happened after it appeared
- keeps setup type and symbol separate
- keeps setup-type-plus-symbol pairs separate
- passes examples through proof, diagnostics, evidence packet, packet readiness, group review, group review readiness, historical bundle, and bundle readiness
- returns a compact lower-tier-reviewable in-memory summary
- identifies missing evidence instead of fabricating proof
- carries worked, failed, inconclusive, pending, stale, invalidated, and missing-evidence outcomes without treating worked/failed as profitable
- preserves no-trade, no-live-data, no-controlled-shadow-data, no-alert, no-file-write, no-broker, no-rule-change, and no-optimization boundaries
- does not call `open`, network sockets, subprocesses, threads, report writers, alert systems, broker/order systems, or `main.py`

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

## 9. Required Build-State / Doc Updates for the Future Step

The future implementation must update `SAFE_FAST_BUILD_STATE.md` with:

- implementation status for the local-only historical setup sample path runner
- baseline `patch8` and Day 33 context
- exact implementation file and test file
- focused historical sample path test result
- required proof-chain regression results
- watcher-foundation scaffold regression result
- `git diff --check` result
- preserved scope and no-go boundaries
- next local-only objective after the sample path runner

The future implementation must update `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md` with:

- latest commit after implementation
- current objective
- completed milestone
- next objective
- unfinished item
- changed active concerns, if any

Do not claim final viability, historical success, controlled shadow readiness, live readiness, production readiness, Railway readiness, live backend readiness, live trade readiness, or live trade decision readiness.

## 10. Viability Loop

Viability proof is the highest priority.

Required viability loop:

detect -> score outcome -> diagnose deeply -> analyze whole system -> decide fix path -> adjust rule/contract/test -> run regression -> review again

For the future sample path runner, this means the examples must not stop at detection. They must carry setup-appeared evidence, post-setup outcome evidence, diagnostics, packet evidence, readiness decisions, review aggregation, bundle readiness, missing evidence, next fix path, and regression needs.

## 11. Diagnostics-Before-Optimization Rule

Diagnostics must come before optimization.

The sample path must expose what failed, what evidence was used, likely cause candidate, affected setup type, affected symbol, affected stage, trigger/invalidation/freshness relationship, blocker/caution relationship, ranking/focus issue, session-boundary issue, data-quality or missing-evidence issue, market-context issue, outcome-scoring issue, review/logging issue, user-facing workflow issue, next fix path, and regression test needed when those facts are available.

No threshold, ranking, trigger, invalidation, freshness, blocker/caution, workflow, or alert optimization may be proposed from the sample path unless diagnostics identify an evidence-backed rule, contract, fixture, planning, or test gap.

## 12. Discretion Rule

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
- mark the sample path reviewable without readiness-gate support

Setup recognition, trigger, invalidation, fresh/stale/spent, blocker/caution, ranking/focus, outcome scoring, diagnostics, evidence packaging, packet readiness, aggregate review, review-readiness gating, bundle review, bundle readiness, and user workflow should be rule-based.

## 13. Lower-Tier Handoff Requirement

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

## 14. Six Active Concerns From Day 33 Handoff

### 1. Stop endless infrastructure before real evidence

After the historical proof bundle readiness gate, move to a small local historical sample path. The future runner must use a small controlled set of local historical setup examples and run them through the full chain from setup appeared to bundle readiness.

### 2. Define complete enough to trust

The existing readiness gate makes this strict. The sample path must preserve setup type separation, symbol separation, setup-type-plus-symbol pair tracking, evidence references, missing evidence, worked patterns, failed patterns, repeated fix paths, regression tests, proof gaps, no-trade boundary, no optimization claim, and lower-tier review summary.

### 3. Protect no-hindsight boundaries

Every sample must separate what was known when the setup appeared, what happened after the setup appeared, outcome evidence, missing evidence, and review conclusion. If later information is used to justify the original setup, the proof is invalid.

### 4. Keep worked/failed separate from profitable

The current proof layer judges chart/setup behavior only. Profitability is a later layer. The sample path must not claim profitability from worked/failed setup behavior.

### 5. Do not combine symbols or setup types too early

Every sample path result must preserve separation by Ideal, Clean Fast Break, Continuation, SPY, QQQ, IWM, GLD, and setup-type-plus-symbol pair. A combined score can come later only after the pieces are proven separately.

### 6. Avoid circular review packets

A bundle cannot be trusted just because an earlier gate said it was ready. The sample path must carry enough detail to review what setup appeared, what happened after, evidence used, missing evidence, diagnosis, likely cause candidate, next fix path, regression needed, and lower-tier handoff summary.

## 15. No-Hindsight Requirement

The sample path must keep setup-time evidence and post-setup outcome evidence separate.

Allowed:

- use setup-time fields to describe why a setup appeared
- use later fields only to describe what happened after setup appearance
- mark missing or unavailable evidence explicitly

Forbidden:

- backfill trigger validity from later candles
- backfill setup identity from outcome movement
- change worked/failed status after the fact without explicit outcome evidence
- hide inconclusive or unavailable evidence
- convert chart behavior into profitability or trade readiness

## 16. Setup Type And Symbol Separation

The future runner must treat setup type and symbol as separate fields.

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

The runner must not collapse Ideal, Clean Fast Break, Continuation, SPY, QQQ, IWM, and GLD into one combined score before separate review.

## 17. Boundary Statement

This docs-only plan does not start code work, tests, optimization, controlled shadow data, live data, watcher loops, alerts, generated reports/logs, broker/order/account/options/P&L, account sizing, production/Railway/live backend work, or live trade decisions.

This docs-only plan does not modify `main.py`, engine logic, watcher code, tests, Railway/deploy files, secrets, `.env` files, credentials, tokens, deployment settings, generated output paths, report/log writers, watcher loops, alert delivery, broker/order/account behavior, options behavior, option P&L, position sizing, account sizing, or live trade decision logic.
