# SAFE-FAST Local Next-Step Plan After GLD Continuation Evidence Fix

## 1. Purpose

Plan the next controlled local sample expansion after the GLD Continuation after-setup evidence fix.

The current controlled sample set now has:

- worked `Ideal` / `SPY`
- failed `Clean Fast Break` / `QQQ`
- worked and reviewable `Continuation` / `GLD`

The obvious starting-universe gap is that `IWM` is not represented in the controlled local sample set. The next build step should preserve the existing SPY, QQQ, and GLD examples, add exactly one controlled `IWM` example, rerun the local sample path and output review, and report whether IWM becomes reviewable and what the expanded sample teaches.

This plan is docs-only. It does not start code work, tests, live data, controlled shadow data, watcher loops, alerts, generated reports/logs, broker/order/account/options/P&L, account sizing, optimization, production work, or live trade decisions.

## 2. Day 34 Context

- **Baseline:** patch8.
- **Repo:** `safe-fast-backendnew`.
- **Branch:** `main`.
- **Current working day context:** Day 34.
- **Day 33 status:** historical context.
- **Latest commit before this plan:** `eb6e5d0 Add GLD Continuation after-setup evidence`.
- **Work mode:** build work only, not live trade chat.
- **Highest priority:** viability proof before optimization.
- **Profitability status:** profitability and historical success are still unproven.
- **Current objective:** plan one controlled local sample expansion so the starting universe is not missing IWM.

## 3. Fixed Inputs To Preserve

The future implementation must preserve these existing controlled examples:

- `Ideal` / `SPY`: worked sample with setup-time and after-setup evidence.
- `Clean Fast Break` / `QQQ`: failed sample with useful diagnosis.
- `Continuation` / `GLD`: worked/reviewable sample after the GLD evidence fix.

The future implementation must not rewrite these samples to make the expanded set look stronger. Existing worked, failed, and reviewable statuses must remain visible as separate chart/setup behavior outcomes, not profitability evidence.

## 4. Exact Next Implementation Step

Add one controlled local `IWM` example to the first controlled historical sample evidence set.

The future implementation should:

- preserve the existing SPY, QQQ, and GLD examples unchanged unless a narrow compatibility adjustment is required
- add exactly one controlled `IWM` example
- keep setup type separation
- keep symbol separation
- keep setup-type-plus-symbol pair separation
- keep setup-time evidence separate from after-setup evidence
- keep `future_evidence_used_to_define_setup: False`
- keep the sample set local-only and in-memory
- run the sample path through the existing proof chain
- rerun the sample output review
- report whether IWM becomes reviewable or remains inconclusive
- report what the new IWM sample teaches
- avoid any profitability, historical success, final viability, live readiness, or production readiness claim

The IWM setup type should remain explicit. Do not use the new IWM sample to blend setup types or hide weakness in any existing SPY, QQQ, or GLD example.

## 5. IWM Evidence Shape

The future IWM example should include, at minimum:

- `setup_id`
- `setup_type`
- `symbol: IWM`
- `detection_timestamp`
- setup-time identity/evidence refs
- after-setup evidence that starts after the detection timestamp
- `source_row_reference`
- `post_setup_evidence`
- `future_evidence_used_to_define_setup: False`
- explicit outcome state: worked, failed, or inconclusive
- diagnostic/fix-path material sufficient for review

The IWM sample may be worked, failed, or inconclusive. The important requirement is that the review can say what the example teaches without turning it into a profitability or final viability claim.

## 6. No-Hindsight Requirement

Allowed:

- setup-time evidence describes why the IWM setup appeared
- after-setup evidence describes only what happened after setup appearance
- the output review decides whether IWM is reviewable
- missing or unavailable IWM evidence remains explicit if IWM is not reviewable

Forbidden:

- backfill IWM setup identity from later movement
- backfill trigger validity from future candles
- use post-setup movement to choose or relabel the setup type
- combine IWM with SPY, QQQ, or GLD to hide sample weakness
- convert worked/failed chart behavior into profitability, trade readiness, or live decision language

## 7. Allowed Files For The Future Implementation Step

Allowed future implementation files:

- `watcher_foundation/setup_outcome_historical_sample_path.py`
- `watcher_foundation/__init__.py`
- `tests/test_setup_outcome_historical_sample_path.py`
- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`

No other files are allowed for that future implementation step unless the user explicitly expands scope.

## 8. Required Tests For The Future Implementation Step

Add or update focused local unit tests in `tests/test_setup_outcome_historical_sample_path.py` covering:

- existing `Ideal` / `SPY` remains present and reviewable
- existing `Clean Fast Break` / `QQQ` remains present and reviewable as a useful failure diagnosis
- existing `Continuation` / `GLD` remains present and reviewable
- new `IWM` sample is present
- IWM setup type and symbol are represented separately
- IWM setup-time evidence remains separate from IWM after-setup evidence
- IWM future evidence is not used to define the setup
- setup-type-plus-symbol pair separation includes the new IWM pair
- the sample path still runs fully in memory
- the output review reports whether IWM becomes reviewable or remains inconclusive
- the output review reports what the new sample teaches
- no final viability, profitability, historical success, optimization, live-data, controlled-shadow, alert, file-write, broker, account, option P&L, account sizing, or live trade decision behavior appears

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

## 9. Required Build-State / Handoff Updates For The Future Step

The future implementation must update `SAFE_FAST_BUILD_STATE.md` with:

- implementation status for the one-sample IWM expansion
- baseline `patch8` and Day 34 context, with Day 33 recorded as historical context
- latest commit before the task
- exact implementation and test files changed
- focused sample path test result
- required proof-chain regression results
- watcher-foundation scaffold regression result
- `git diff --check` result
- whether IWM became reviewable or remained inconclusive
- what the expanded controlled sample set teaches
- preserved scope and no-go boundaries
- next local-only objective after the IWM expansion

The future implementation must update `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md` with:

- latest commit before/after implementation
- current objective
- completed milestone
- next objective
- unresolved concerns
- strict no-go boundaries

Do not claim final viability, historical success, profitability, controlled shadow readiness, live readiness, production readiness, Railway readiness, live backend readiness, live trade readiness, or live trade decision readiness.

## 10. Decision Rule After The Future Step

The future output review should make one of these states explicit:

- `IWM` became reviewable because setup-time evidence and after-setup evidence are both present and separated.
- `IWM` remains inconclusive because the added evidence is missing, weak, unavailable, or violates no-hindsight separation.

If IWM becomes reviewable, the next objective may be a narrow review of what the four-symbol controlled starting universe now proves and still does not prove.

If IWM remains inconclusive, the next objective must stay focused on the exact remaining IWM evidence, contract, fixture, or regression gap. Do not broaden samples to hide the unresolved IWM weakness.

## 11. Boundary Statement

This docs-only plan does not start code work, tests, optimization, controlled shadow data, live data, watcher loops, alerts, generated reports/logs, broker/order/account/options/P&L, account sizing, production/Railway/live backend work, or live trade decisions.

This docs-only plan does not modify `main.py`, engine logic, watcher code, tests, Railway/deploy files, secrets, `.env` files, credentials, tokens, deployment settings, generated output paths, report/log writers, watcher loops, alert delivery, broker/order/account behavior, options behavior, option P&L, position sizing, account sizing, or live trade decision logic.
