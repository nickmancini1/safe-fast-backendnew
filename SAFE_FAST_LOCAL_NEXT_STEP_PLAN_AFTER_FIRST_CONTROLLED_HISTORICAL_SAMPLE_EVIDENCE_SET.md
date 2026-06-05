# SAFE-FAST Local Next-Step Plan After First Controlled Historical Sample Evidence Set

## 1. Plain Purpose

Plan the next build step after the first controlled local historical sample evidence set.

SAFE-FAST now has a tiny in-memory evidence set with one worked setup, one failed setup, and one missing-evidence/inconclusive setup. The next step should review whether that sample set actually tells us something useful before any broader sample expansion, rule change, optimization, controlled shadow work, live data, alerts, generated reports/logs, or production work.

This plan is docs-only. It does not start code work, tests, live data, controlled shadow data, watcher loops, alerts, generated reports/logs, broker/order/account/options/P&L, account sizing, optimization, production work, or live trade decisions.

## 2. Day 34 Context

- **Baseline:** patch8.
- **Repo:** `safe-fast-backendnew`.
- **Branch:** `main`.
- **Current working day context:** Day 34.
- **Day 33 status:** historical context.
- **Latest commit before this plan:** `2ccc021 Add first controlled historical sample evidence set`.
- **Work mode:** build work only, not live trade chat.
- **Highest priority:** viability proof before optimization.
- **Current objective:** plan the review step after the first controlled historical sample evidence set.
- **Profitability status:** profitability and historical success are still unproven.
- **Handoff rule:** `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md` remains a living handoff file and must track this Day 34 update, this plan file, and the next review objective.

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
- first controlled historical sample evidence set

The first controlled historical sample evidence set is complete and committed at `2ccc021 Add first controlled historical sample evidence set`.

The fixed foundation is local-only and in-memory. It accepts caller-provided historical setup examples, rejects file/report/log/live/shadow/alert/broker/account/options/P&L/account-sizing/trade-decision/watcher-loop shaped inputs, runs examples through the proof chain, preserves setup-time evidence and post-setup evidence separation, keeps setup type, symbol, and setup-type-plus-symbol pairs separate, exposes missing evidence, diagnostics, fix paths, regression needs, lower-tier review fields, and exact bundle-readiness missing review items, and returns one defensive-copy in-memory summary without profitability, final viability, rule-change, optimization, live-data, alert, broker, file-write, or trade-decision claims.

The controlled evidence set currently exposes:

- one worked `Ideal` / `SPY` setup
- one failed `Clean Fast Break` / `QQQ` setup
- one missing-evidence/inconclusive `Continuation` / `GLD` setup

## 4. What Is Still Unproven

- Final SAFE-FAST trading-plan viability is not proven.
- Profitability is not proven.
- Actual historical success is not proven.
- It is not yet proven that the first controlled evidence set produced clear proof.
- It is not yet proven that the failed example produced a useful diagnosis.
- It is not yet proven that the inconclusive example clearly showed what evidence was missing.
- It is not yet proven that the review output gives the smallest useful next fix path.
- It is not yet proven that lower-tier review can understand the resulting packet without raw logs or hidden repo context.
- Controlled shadow data, live data, alerts, generated reports/logs, broker/order/account/options/P&L behavior, account sizing, production readiness, Railway/deploy readiness, live backend readiness, live trade readiness, and live trade decisions remain forbidden and unproven.

## 5. Exact Next Implementation Step

Create a local-only review evaluator for the first controlled historical sample path output.

The future step should call the existing in-memory sample builder and runner, inspect the returned summary, and produce a compact in-memory review result answering:

- Did the worked example produce clear proof?
- Did the failed example produce a useful diagnosis?
- Did the inconclusive example clearly show what evidence was missing?
- Did the full chain preserve no-hindsight boundaries?
- Did it keep setup type and symbol separate?
- Did it keep setup-type-plus-symbol pair tracking separate?
- Did it produce clear next fix paths?
- Did it produce useful lower-tier review material?
- What is the smallest evidence-backed next fix path, contract gap, fixture gap, test gap, or docs gap?

The future implementation must not broaden the sample set by default. It should review the current evidence set first and only identify the next fix path. If the review finds that the sample set itself is too weak, that should be reported as a fixture or evidence gap, not hidden by expansion or tuning.

## 6. Allowed Files For That Future Step

Allowed future implementation files:

- `watcher_foundation/setup_outcome_historical_sample_path.py`
- `watcher_foundation/__init__.py`
- `tests/test_setup_outcome_historical_sample_path.py`
- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`

No other files are allowed for that future implementation step unless the user explicitly expands scope.

## 7. Required Tests For The Future Implementation Step

Add or update focused local unit tests in `tests/test_setup_outcome_historical_sample_path.py` covering:

- the review uses `build_first_controlled_historical_sample_evidence_set`
- the review uses `run_setup_outcome_historical_sample_path`
- the worked `Ideal` / `SPY` example is identified and judged for clear proof
- the failed `Clean Fast Break` / `QQQ` example is identified and judged for useful diagnosis
- the missing-evidence/inconclusive `Continuation` / `GLD` example is identified and judged for explicit missing evidence
- no-hindsight boundary preservation is checked from setup-time versus after-setup evidence
- setup type separation is checked
- symbol separation is checked
- setup-type-plus-symbol pair separation is checked
- next fix paths are surfaced without optimization
- lower-tier review material is compact and understandable
- worked/failed chart behavior does not become a profitability claim
- no-trade, no-live-data, no-controlled-shadow-data, no-alert, no-file-write, no-broker, no-rule-change, and no-optimization boundaries are preserved
- the review does not call `open`, network sockets, subprocesses, threads, report writers, alert systems, broker/order systems, or `main.py`

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

## 8. Required Build-State / Doc Updates For The Future Step

The future implementation must update `SAFE_FAST_BUILD_STATE.md` with:

- implementation status for the first controlled historical sample output review
- baseline `patch8` and Day 34 context, with Day 33 recorded as historical context
- latest commit before the task
- exact implementation file and test file
- focused historical sample path test result
- required proof-chain regression results
- watcher-foundation scaffold regression result
- `git diff --check` result
- preserved scope and no-go boundaries
- next local-only objective after the review

The future implementation must update `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md` with:

- latest commit after implementation
- current objective
- completed milestone
- next objective
- unfinished item
- changed active concerns, if any

Do not claim final viability, historical success, controlled shadow readiness, live readiness, production readiness, Railway readiness, live backend readiness, live trade readiness, or live trade decision readiness.

## 9. No-Hindsight Requirement

The future review must verify that setup-time evidence and post-setup outcome evidence stayed separate.

Allowed:

- use setup-time fields to describe why a setup appeared
- use later fields only to describe what happened after setup appearance
- mark missing or unavailable evidence explicitly
- reject or flag any review that backfills setup identity from outcome movement

Forbidden:

- backfill trigger validity from later candles
- backfill setup identity from outcome movement
- use post-setup outcome evidence to create the setup label
- change worked/failed status after the fact without explicit outcome evidence
- hide inconclusive or unavailable evidence
- convert chart behavior into profitability or trade readiness

## 10. Setup Type And Symbol Separation

The future review must treat setup type and symbol as separate fields.

Required separate tracking:

- setup type
- symbol
- setup-type-plus-symbol pair
- worked proof by setup type
- worked proof by symbol
- failed diagnosis by setup type
- failed diagnosis by symbol
- missing evidence by setup type
- missing evidence by symbol
- missing evidence by setup-type-plus-symbol pair

The review must not collapse `Ideal`, `Clean Fast Break`, `Continuation`, `SPY`, `QQQ`, `IWM`, and `GLD` into one combined score before separate review.

## 11. Diagnostics-Before-Optimization Rule

Diagnostics must come before optimization.

The future review must identify what the controlled set shows and what it does not show. It must surface what failed, what evidence was used, likely cause candidate, affected setup type, affected symbol, affected stage, trigger/invalidation/freshness relationship, blocker/caution relationship, ranking/focus issue, session-boundary issue, data-quality or missing-evidence issue, market-context issue, outcome-scoring issue, review/logging issue, user-facing workflow issue, next fix path, and regression test needed when those facts are available.

No threshold, ranking, trigger, invalidation, freshness, blocker/caution, workflow, alert, or rule optimization may be proposed from the review unless diagnostics identify an evidence-backed rule, contract, fixture, planning, or test gap.

## 12. Lower-Tier Handoff Requirement

The future review output must be compact enough for lower-tier review.

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

## 13. Six Active Concerns From The Handoff

### 1. Stop endless infrastructure before real evidence

The first controlled evidence set exists. The next step must review whether it gives useful evidence, not build more infrastructure or expand samples by default.

### 2. Define complete enough to trust

The review must say whether the current sample output is complete enough to inspect and, if not, exactly what is missing.

### 3. Protect no-hindsight boundaries

The review must verify that setup-time evidence, post-setup outcome evidence, missing evidence, and conclusions stayed separate.

### 4. Keep worked/failed separate from profitable

The review may discuss worked or failed chart/setup behavior only. It must not claim profitability or trade readiness.

### 5. Do not combine symbols or setup types too early

The review must keep `Ideal`, `Clean Fast Break`, `Continuation`, `SPY`, `QQQ`, `IWM`, `GLD`, and setup-type-plus-symbol pairs separate.

### 6. Avoid circular review packets

The review must inspect the actual sample path output. It must not trust the bundle only because an earlier gate said it was ready.

## 14. Boundary Statement

This docs-only plan does not start code work, tests, optimization, controlled shadow data, live data, watcher loops, alerts, generated reports/logs, broker/order/account/options/P&L, account sizing, production/Railway/live backend work, or live trade decisions.

This docs-only plan does not modify `main.py`, engine logic, watcher code, tests, Railway/deploy files, secrets, `.env` files, credentials, tokens, deployment settings, generated output paths, report/log writers, watcher loops, alert delivery, broker/order/account behavior, options behavior, option P&L, position sizing, account sizing, or live trade decision logic.
