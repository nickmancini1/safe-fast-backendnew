# SAFE-FAST Local Next-Step Plan After Controlled Historical Sample Output Review

## 1. Plain Purpose

Plan the next build step after the controlled historical sample output review.

The review showed that the current controlled sample output is useful but not final viability proof. The worked `Ideal` / `SPY` sample is reviewable, the failed `Clean Fast Break` / `QQQ` sample is reviewable as a useful failure diagnosis, and the `Continuation` / `GLD` sample remains inconclusive because it lacks after-setup evidence.

The next build step should fill that smallest evidence gap only: add after-setup evidence for the existing `Continuation` / `GLD` controlled sample, rerun the local in-memory sample path and output review, and show whether that GLD sample becomes reviewable or remains inconclusive.

This plan is docs-only. It does not start code work, tests, live data, controlled shadow data, watcher loops, alerts, generated reports/logs, broker/order/account/options/P&L, account sizing, optimization, production work, or live trade decisions.

## 2. Day 34 Context

- **Baseline:** patch8.
- **Repo:** `safe-fast-backendnew`.
- **Branch:** `main`.
- **Current working day context:** Day 34.
- **Day 33 status:** historical context.
- **Latest commit before this plan:** `ba7374b Add controlled historical sample output review`.
- **Work mode:** build work only, not live trade chat.
- **Highest priority:** viability proof before optimization.
- **Current objective:** plan the smallest next build step after the controlled historical sample output review.
- **Profitability status:** profitability and historical success are still unproven.
- **Handoff rule:** `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md` remains a living handoff file and must track this Day 34 update, this plan file, and the next GLD Continuation evidence-fill objective.

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
- first controlled historical sample output review

The controlled sample output review is complete and committed at `ba7374b Add controlled historical sample output review`.

The review result is:

- `Ideal` / `SPY`: worked sample, clear chart-behavior proof, preserve unchanged.
- `Clean Fast Break` / `QQQ`: failed sample, useful diagnosis, preserve unchanged.
- `Continuation` / `GLD`: inconclusive sample, missing after-setup evidence, improve next.

The current review result is useful but not final viability proof. It does not prove profitability, historical success, controlled shadow readiness, live readiness, production readiness, or live trade readiness.

## 4. Exact Next Implementation Step

Update the first controlled historical sample evidence set so the existing `Continuation` / `GLD` sample includes caller-provided after-setup evidence.

The future implementation should:

- preserve the existing worked `Ideal` / `SPY` sample
- preserve the existing failed `Clean Fast Break` / `QQQ` sample
- improve only the existing `Continuation` / `GLD` sample
- add after-setup evidence for GLD without changing the setup identity from future movement
- keep setup-time evidence separate from after-setup evidence
- keep setup type separation
- keep symbol separation
- keep setup-type-plus-symbol pair separation
- keep the sample set local-only and in-memory
- rerun the sample path through the existing proof chain
- rerun the sample output review
- report whether GLD Continuation becomes reviewable or remains inconclusive

The future implementation should not broaden the sample set by default. The task is to test whether the smallest identified evidence gap can be closed before expanding into more samples.

## 5. Expected GLD Evidence Shape

The GLD sample should keep its existing setup-time identity and setup-time evidence.

The future after-setup evidence should add, at minimum:

- `source_row_reference`
- `post_setup_evidence`
- timestamps that start after the setup detection timestamp
- `future_evidence_used_to_define_setup: False`
- caller-provided/local-only markers consistent with the existing controlled samples

The future evidence must be chart/setup behavior evidence only. It must not add entry quality, option fills, spreads, IV, expiration, P&L, account sizing, broker/order execution, live trade decisions, or profitability claims.

## 6. No-Hindsight Requirement

The future implementation must preserve no-hindsight separation.

Allowed:

- setup-time evidence describes why the `Continuation` / `GLD` setup appeared
- after-setup evidence describes only what happened after setup appearance
- missing or unavailable evidence remains explicit if GLD is still not reviewable
- the output review decides whether the GLD sample has enough evidence to review

Forbidden:

- backfill trigger validity from later candles
- backfill setup identity from outcome movement
- use post-setup movement to create or change the setup label
- change the SPY or QQQ samples to make bundle readiness look better
- hide inconclusive or unavailable evidence
- convert chart behavior into profitability, trade readiness, or live decision language

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

- the existing `Ideal` / `SPY` worked sample remains present and reviewable
- the existing `Clean Fast Break` / `QQQ` failed sample remains present and reviewable as a useful diagnosis
- the existing `Continuation` / `GLD` sample now carries after-setup evidence
- GLD setup-time evidence remains separate from GLD after-setup evidence
- GLD future evidence is not used to define the setup
- setup type separation remains true
- symbol separation remains true
- setup-type-plus-symbol pair separation remains true
- the sample path still runs fully in memory
- the output review reruns against the updated controlled sample
- the review explicitly reports whether GLD Continuation becomes reviewable or remains inconclusive
- worked/failed/reviewable chart behavior does not become a profitability claim
- no-trade, no-live-data, no-controlled-shadow-data, no-alert, no-file-write, no-broker, no-rule-change, and no-optimization boundaries are preserved
- the implementation does not call `open`, network sockets, subprocesses, threads, report writers, alert systems, broker/order systems, or `main.py`

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

- implementation status for the GLD Continuation after-setup evidence fill
- baseline `patch8` and Day 34 context, with Day 33 recorded as historical context
- latest commit before the task
- exact implementation file and test file
- focused historical sample path test result
- required proof-chain regression results
- watcher-foundation scaffold regression result
- `git diff --check` result
- whether GLD Continuation became reviewable or remained inconclusive
- preserved scope and no-go boundaries
- next local-only objective after the GLD evidence fill

The future implementation must update `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md` with:

- latest commit after implementation
- current objective
- completed milestone
- next objective
- unfinished item
- changed active concerns, if any

Do not claim final viability, historical success, profitability, controlled shadow readiness, live readiness, production readiness, Railway readiness, live backend readiness, live trade readiness, or live trade decision readiness.

## 10. Decision Rule After The Future Step

The future output review should make one of these states explicit:

- `Continuation` / `GLD` became reviewable because setup-time evidence and after-setup evidence are both present and separated.
- `Continuation` / `GLD` remains inconclusive because the added evidence is still missing, weak, unavailable, or violates no-hindsight separation.

If GLD becomes reviewable, the next objective may be a narrow review of what the three-sample controlled set now proves and still does not prove.

If GLD remains inconclusive, the next objective must stay focused on the exact remaining evidence, contract, fixture, or regression gap. Do not broaden samples to hide the unresolved GLD weakness.

## 11. Boundary Statement

This docs-only plan does not start code work, tests, optimization, controlled shadow data, live data, watcher loops, alerts, generated reports/logs, broker/order/account/options/P&L, account sizing, production/Railway/live backend work, or live trade decisions.

This docs-only plan does not modify `main.py`, engine logic, watcher code, tests, Railway/deploy files, secrets, `.env` files, credentials, tokens, deployment settings, generated output paths, report/log writers, watcher loops, alert delivery, broker/order/account behavior, options behavior, option P&L, position sizing, account sizing, or live trade decision logic.
