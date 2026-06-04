# SAFE-FAST Local Next-Step Plan After Setup Outcome Evidence Packet

## 1. Plain-English Purpose

SAFE-FAST can now build compact setup outcome evidence packets. The next small local build step should check whether those packets are complete enough for proof review before anyone tries to optimize rules, start watcher behavior, use controlled shadow data, or discuss live trade decisions.

The future evaluator should answer, in plain English, whether a packet is ready for lower-tier review, what evidence is missing, whether setup type and symbol are still separated, whether the diagnosis and next fix path are clear enough, whether a regression test is named, and whether the packet still preserves no-trade, no-live, no-shadow, and no-optimization boundaries.

This plan is local-only and docs-only. It does not start code work, live data, controlled shadow data, watcher loops, alerts, generated reports/logs, optimization, production work, or trade decisions.

## 2. Baseline and Day 33 Context

- **Baseline:** patch8.
- **Repo:** `safe-fast-backendnew`.
- **Branch:** `main`.
- **Current working day context:** Day 33.
- **Latest local setup outcome evidence packet milestone:** `239e642 Add setup outcome evidence packet builder`.
- **Work mode:** SAFE-FAST build work only, not live trade decisions.
- **Planning scope:** docs-only local next-step planning after the setup outcome evidence packet builder.
- **Highest priority:** viability proof before optimization.
- **Tier pressure:** use the current high-capability review window to make future lower-tier review compact, explicit, and bounded.

## 3. Current Fixed Foundation

- Replay/regression foundation is complete.
- Shadow review/export bundle foundation is complete.
- Day 60 input-contract validator is complete.
- Day 60 shadow session dry-run adapter is complete.
- Day 60 review/diagnostics packet builder is complete.
- Day 60 diagnostics readiness evaluator is complete.
- Day 60 outcome scoring contract validator is complete.
- Day 60 outcome scoring summary evaluator is complete.
- Day 60 outcome diagnostics evaluator is complete.
- Day 60 optimization readiness gate is complete.
- Historical outcome proof preflight validator is complete.
- Historical outcome proof summary evaluator is complete.
- Historical outcome diagnostics evaluator is complete.
- Historical optimization readiness gate is complete.
- Trading-plan discretion audit evaluator is complete.
- Discretion audit coverage evaluator is complete.
- Discretion audit inventory validator is complete.
- Discretion audit inventory-to-audit/coverage bridge gate is complete.
- Setup outcome proof evaluator is complete at `b878cae`.
- Setup outcome diagnostics evaluator is complete at `800f324`.
- Setup outcome evidence packet plan is complete at `aa51390`.
- Setup outcome evidence packet builder is complete at `239e642`.
- The evidence packet builder accepts only the in-memory setup outcome diagnostics summary, preserves watch-only/no-hindsight/no-trade/no-live/no-shadow/no-alert/no-file-write/no-broker/no-optimization/no-rule-change boundaries, emits compact packet items, keeps setup type and symbol separate, preserves missing/unavailable evidence, carries proof-limited reasons, includes next fix paths and regression-needed items, and makes no profitability or final viability claim.

## 4. What Is Still Unproven

- Final SAFE-FAST trading-plan viability is not proven.
- Actual historical success is not proven.
- Repeatability of successful setup outcomes is not proven.
- It is not yet proven whether compact packet output is complete enough for lower-tier proof review.
- It is not yet proven whether packet output always names missing evidence clearly enough.
- It is not yet proven whether packet output always keeps setup type separated from symbol in the readiness surface.
- It is not yet proven whether packet diagnoses are clear enough to support a bounded review decision.
- It is not yet proven whether packet next fix paths are specific enough to route work to the smallest responsible local contract, fixture, test, or planning layer.
- It is not yet proven whether every packet item names the regression test needed before broader changes.
- It is not yet proven whether a lower-tier reviewer can safely use the packet without reconstructing proof, diagnostics, and evidence-packet internals.
- Controlled shadow data has not started.
- Live data has not started.
- Alerts have not started.
- Generated reports/logs have not started.
- Broker/order/account/options/P&L behavior remains forbidden.
- Account sizing remains forbidden.
- Production readiness, Railway/deploy readiness, live backend readiness, live trade readiness, and live trade decisions remain forbidden and unproven.

## 5. Exact Next Implementation Step

Add one local-only in-memory setup outcome evidence packet readiness evaluator.

The future evaluator should accept only the in-memory summary from `build_setup_outcome_evidence_packet(...)` and return one in-memory readiness summary. It should not read files, fetch data, write files, generate reports/logs, start watcher behavior, change rules, optimize, or make trade decisions.

The readiness summary should answer:

- Is the packet complete enough to review?
- What evidence is missing?
- Is setup type still separated?
- Is symbol still separated?
- Is the diagnosis clear enough?
- Is the next fix path clear enough?
- Is a regression test named?
- Is this ready for lower-tier review?
- Is this still no-trade and no-optimization?

The evaluator should produce a clear readiness status such as `ready_for_lower_tier_review`, `needs_lower_tier_evidence_fix`, or `blocked_by_packet_contract_gap`. The exact names may follow local code style, but the output must distinguish complete review-ready packets from packets blocked by missing evidence, unclear diagnosis, unclear fix path, missing regression, merged setup/symbol grouping, rejected proof records, or boundary violations.

## 6. Allowed Files for That Future Step

- `watcher_foundation/setup_outcome_packet_readiness.py`
- `watcher_foundation/__init__.py`
- `tests/test_setup_outcome_packet_readiness.py`
- `SAFE_FAST_BUILD_STATE.md`

No other files are allowed for that future implementation step unless the user explicitly expands scope.

## 7. Forbidden Files / Systems

- `main.py`
- Trading engine logic
- Railway/deploy files
- Production or live backend integration
- Generated output paths
- Report/log writers
- Live data startup or fetching
- Controlled shadow data startup
- Watcher loops, schedulers, polling, daemons, or background workers
- Alert delivery systems
- Broker/order/account/options/P&L systems
- Account sizing or position sizing systems
- Secrets, `.env`, credentials, tokens, keys, or deployment settings
- Any code path that can make live trade decisions
- Any rule change or optimization before diagnostics and packet readiness prove what needs fixing

## 8. Required Tests for the Future Implementation Step

Add focused local unit tests in `tests/test_setup_outcome_packet_readiness.py` covering:

- Accepts only the in-memory setup outcome evidence packet summary shape.
- Requires `watch_only=True`, `setup_outcome_evidence_packet_only=True`, `setup_outcome_diagnostics_only=True`, `setup_outcome_proof_only=True`, `final_viability_proven=False`, `optimization_started=False`, and `no_rule_change_started=True`.
- Rejects summaries that started live data, controlled shadow data, alerts, file writes, broker/trade behavior, optimization, or rule changes.
- Confirms packet completeness only when each packet item has setup type, symbol, what setup appeared, what happened after setup, why it happened, evidence support, next fix path, regression needed, lower-tier handoff state, no-hindsight confirmation, and no-trade confirmation.
- Identifies missing evidence explicitly and keeps unavailable fields visible without fabrication.
- Confirms setup type remains separated from symbol in both packet items and grouped packet output.
- Fails readiness when setup type and symbol are merged, unavailable without explanation, or hidden in free-text.
- Fails readiness when diagnosis text is absent, shallow, vague, or unsupported by evidence.
- Fails readiness when next fix path is absent, vague, or not tied to an affected system area.
- Fails readiness when regression-needed is absent or not named.
- Marks rejected proof records and proof-limited packets as requiring lower-tier handoff.
- Preserves no-trade, no-rule-change, no-optimization, no-file-write, no-live-data, no-controlled-shadow-data, no-alert, and no-broker boundaries.
- Does not scan repo files, fetch data, start threads, invoke subprocesses, or write files/logs/reports.
- Rejects or quarantines broker/order/account/options/P&L/account-sizing/live-trade-decision fields.

Required validation commands for that future implementation:

- `python -m unittest discover -s tests -p test_setup_outcome_packet_readiness.py`
- `python -m unittest discover -s tests -p test_setup_outcome_evidence_packet.py`
- `python -m unittest discover -s tests -p test_setup_outcome_diagnostics.py`
- `python -m unittest discover -s tests -p test_setup_outcome_proof.py`
- `python -m unittest tests.test_watcher_foundation_scaffold`
- `git diff --check`

## 9. Required Build-State / Doc Updates for the Future Step

The future implementation must update `SAFE_FAST_BUILD_STATE.md` with:

- Implementation status for the local-only setup outcome evidence packet readiness evaluator.
- Baseline `patch8` and Day 33 context.
- Exact implementation file and test file.
- Focused packet readiness test result.
- Setup outcome evidence packet regression result.
- Setup outcome diagnostics regression result.
- Setup outcome proof regression result.
- Watcher-foundation scaffold regression result.
- `git diff --check` result.
- Preserved scope and no-go boundaries.
- Next local-only objective after the readiness evaluator.

Do not claim final viability, historical success, controlled shadow readiness, live readiness, production readiness, Railway readiness, live backend readiness, live trade readiness, or live trade decision readiness.

## 10. Viability Loop

Viability proof is the highest priority.

Detection alone is not enough. Outcome labels alone are not enough. Diagnostics alone are not enough. Evidence packets alone are not enough. The next step must check whether the packet is ready for proof review and whether the missing evidence and next fix path are explicit enough to route work.

Required viability loop:

detect -> score outcome -> diagnose deeply -> package evidence -> evaluate packet readiness -> analyze whole system -> decide fix path -> adjust rule/contract/test -> run regression -> review again

## 11. Diagnostics-Before-Optimization Rule

Diagnostics and packet readiness must come before optimization.

Shallow labels like failed setup, bad alert, weak signal, bad trade, or ready for review are not enough. Readiness must be tied to evidence completeness, missing evidence, setup type separation, symbol separation, diagnosis clarity, next fix path clarity, named regression coverage, lower-tier handoff requirement, and no-trade/no-optimization boundary preservation.

No threshold, ranking, trigger, invalidation, freshness, blocker/caution, workflow, or alert optimization may be proposed until diagnostic and packet-readiness output identifies an evidence-backed rule, contract, fixture, planning, or test gap.

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
- mark a packet ready without named evidence, diagnosis, fix path, and regression coverage

Setup recognition, trigger, invalidation, fresh/stale/spent, blocker/caution, ranking/focus, outcome scoring, diagnostics, evidence packaging, packet readiness, and user workflow should be rule-based.

## 13. Lower-Tier Handoff Requirement

If the readiness evaluator finds missing evidence, unclear setup type, unclear symbol, merged setup/symbol grouping, unclear diagnosis, vague next fix path, missing regression name, proof-limited records, rejected proof records, stale/freshness gaps, trigger/invalidation ambiguity, blocker/caution ambiguity, session-boundary ambiguity, workflow ambiguity, or boundary violations, the output must identify lower-tier handoff before any higher-tier optimization or live-readiness step.

Lower-tier handoff means the next fix path must go back to the smallest responsible local contract, fixture, test, or planning layer before changing broader watcher behavior. It must not skip directly to live data, alerts, trading, account sizing, production, or optimization.

The readiness output must be compact and explicit enough that lower-tier review can see the setup type, symbol, evidence, missing fields, diagnosis, fix path, named regression, and no-trade/no-optimization state without reconstructing the full evaluator internals.

## 14. Boundary Statement

This docs-only plan does not start code work, optimization, controlled shadow data, live data, watcher loops, alerts, generated reports/logs, broker/order/account/options/P&L, account sizing, production/Railway/live backend work, or live trade decisions.

This docs-only plan does not modify `main.py`, engine logic, watcher code, tests, Railway/deploy files, secrets, `.env` files, credentials, tokens, deployment settings, generated output paths, report/log writers, watcher loops, alert delivery, broker/order/account behavior, options behavior, option P&L, position sizing, account sizing, or live trade decision logic.

