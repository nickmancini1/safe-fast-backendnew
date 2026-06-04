# SAFE-FAST Local Next-Step Plan After Setup Outcome Review Aggregator

## 1. Plain-English Purpose

SAFE-FAST can now review groups of setup outcome packet readiness summaries. The next small local build step should check whether that group review is complete enough to trust for proof work before any optimization, watcher expansion, live data, alerts, or trading-related work.

The future readiness gate should answer whether the aggregate review is usable for proof review, which setup types and symbols still need more evidence, whether failures and repeated fix paths are clear, whether named regression tests exist, whether proof gaps still block review, whether lower-tier review is required, and whether the packet remains no-trade and not optimization.

This plan is local-only and docs-only. It does not start code work, live data, controlled shadow data, watcher loops, alerts, generated reports/logs, optimization, production work, or trade decisions.

## 2. Day 33 Context

- **Baseline:** patch8.
- **Repo:** `safe-fast-backendnew`.
- **Branch:** `main`.
- **Current working day context:** Day 33.
- **Latest local commit provided for this task:** `44c4b73 Add setup outcome proof review aggregator`.
- **Work mode:** SAFE-FAST build work only, not live trade decisions.
- **Planning scope:** docs-only local next-step planning after the setup outcome proof review aggregator.
- **Highest priority:** viability proof before optimization.
- **Tier pressure:** use the current $200 window to make proof review explicit, compact, transferable, and lower-tier handoff friendly.

## 3. Current Fixed Foundation

- Replay/regression foundation is complete.
- Shadow review/export bundle foundation is complete.
- Day 60 input-contract, diagnostics, outcome scoring, outcome diagnostics, and optimization readiness layers are complete.
- Historical outcome proof, summary, diagnostics, and optimization readiness layers are complete.
- Trading-plan discretion audit, coverage, inventory, and bridge-gate layers are complete.
- Setup outcome proof evaluator is complete at `b878cae`.
- Setup outcome diagnostics evaluator is complete at `800f324`.
- Setup outcome evidence packet builder is complete at `239e642`.
- Setup outcome packet readiness evaluator is complete at `ca55023`.
- Setup outcome proof review aggregator is complete at `44c4b73`.
- The review aggregator accepts only caller-provided in-memory setup outcome packet readiness summaries, preserves setup type and symbol separation, groups worked/failed/inconclusive/pending/stale/invalidated/missing-evidence outcomes when carried, identifies missing evidence, readiness gaps, repeated fix paths, repeated regression needs, proof gaps, rejected/proof-limited records, lower-tier handoff needs, and proof-continuation decisions.
- No live data, controlled shadow data, watcher loops, alerts, generated reports/logs, broker/order/account/options/P&L, account sizing, production/Railway/live backend work, or live trade decisions are active.

## 4. What Is Still Unproven

- Final SAFE-FAST trading-plan viability is not proven.
- Actual historical success is not proven.
- Repeatability of successful setup outcomes is not proven.
- It is not yet proven whether the group review is complete enough to trust for proof work.
- It is not yet proven which setup types still need more evidence.
- It is not yet proven which symbols still need more evidence.
- It is not yet proven whether failures are diagnosed clearly enough for responsible repair.
- It is not yet proven whether repeated fix paths are clear enough to send to the smallest lower-tier contract, fixture, test, or planning layer.
- It is not yet proven whether named regression tests cover every proof-blocking gap.
- It is not yet proven whether proof gaps are still blocking review.
- It is not yet proven whether the aggregate review is ready for lower-tier review.
- Controlled shadow data, live data, alerts, generated reports/logs, broker/order/account/options/P&L behavior, account sizing, production readiness, Railway/deploy readiness, live backend readiness, live trade readiness, and live trade decisions remain forbidden and unproven.

## 5. Exact Next Implementation Step

Add one local-only in-memory setup outcome proof review readiness gate.

The future gate should accept only one caller-provided in-memory summary from `aggregate_setup_outcome_proof_review(...)` and return one in-memory readiness decision summary. It should not read files, fetch data, write files, generate reports/logs, start watcher behavior, change rules, optimize, or make trade decisions.

The readiness summary should answer:

- Is the group review complete enough to use for proof work?
- Which reviewed packet summaries are included?
- Which setup types are represented, and which still need more evidence?
- Which symbols are represented, and which still need more evidence?
- Are worked, failed, inconclusive, pending, stale, invalidated, and missing-evidence groups explicit enough?
- Are failures diagnosed clearly enough?
- Are repeated fix paths clear and lower-tier specific?
- Are regression tests named?
- Are proof gaps still blocking review?
- Is the packet ready for lower-tier review?
- Is this still no-trade and not optimization?

The output should keep setup type and symbol as separate fields and separate grouping keys. It may summarize missing evidence by setup type, by symbol, and by setup-type-plus-symbol pairing, but it must not merge setup identity and symbol identity into free text.

## 6. Allowed Files for That Future Step

- `watcher_foundation/setup_outcome_review_readiness.py`
- `watcher_foundation/__init__.py`
- `tests/test_setup_outcome_review_readiness.py`
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
- Any rule change or optimization before diagnostics, packet readiness, aggregate review, and review-readiness gating identify an evidence-backed gap

## 8. Required Tests for the Future Implementation Step

Add focused local unit tests in `tests/test_setup_outcome_review_readiness.py` covering:

- Accepts only one in-memory setup outcome proof review aggregate summary.
- Requires `watch_only=True`, `setup_outcome_review_aggregator_only=True`, `setup_outcome_packet_readiness_only=True`, `setup_outcome_evidence_packet_only=True`, `setup_outcome_diagnostics_only=True`, `setup_outcome_proof_only=True`, `final_viability_proven=False`, `optimization_started=False`, and `no_rule_change_started=True`.
- Rejects inputs that started live data, controlled shadow data, alerts, file writes, broker/trade behavior, optimization, or rule changes.
- Preserves reviewed packet identifiers or explicit unavailable identifiers without fabricating them.
- Preserves setup type and symbol separation in readiness output.
- Identifies setup types needing more evidence from missing evidence, proof gaps, readiness gaps, proof-limited records, rejected records, or absent outcome coverage.
- Identifies symbols needing more evidence from missing evidence, proof gaps, readiness gaps, proof-limited records, rejected records, or absent outcome coverage.
- Requires explicit outcome groups for worked, failed, inconclusive, pending, stale, invalidated, and missing-evidence outcomes.
- Requires failures to carry clear diagnostic or readiness-gap context before proof review can be trusted.
- Requires repeated fix paths to be named, specific, and lower-tier oriented.
- Requires named regression coverage before broader changes.
- Marks proof gaps as blocking when they remain unresolved.
- Emits a lower-tier review decision such as `ready_for_lower_tier_review`, `needs_more_evidence_before_lower_tier_review`, or `blocked_by_review_contract_gap`.
- Preserves no-trade, no-rule-change, no-optimization, no-file-write, no-live-data, no-controlled-shadow-data, no-alert, and no-broker boundaries.
- Does not scan repo files, fetch data, start threads, invoke subprocesses, or write files/logs/reports.
- Rejects or quarantines broker/order/account/options/P&L/account-sizing/live-trade-decision fields.

Required validation commands for that future implementation:

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

- Implementation status for the local-only setup outcome proof review readiness gate.
- Baseline `patch8` and Day 33 context.
- Exact implementation file and test file.
- Focused review readiness gate test result.
- Setup outcome review aggregator regression result.
- Setup outcome packet readiness regression result.
- Setup outcome evidence packet regression result.
- Setup outcome diagnostics regression result.
- Setup outcome proof regression result.
- Watcher-foundation scaffold regression result.
- `git diff --check` result.
- Preserved scope and no-go boundaries.
- Next local-only objective after the readiness gate.

Do not claim final viability, historical success, controlled shadow readiness, live readiness, production readiness, Railway readiness, live backend readiness, live trade readiness, or live trade decision readiness.

## 10. Viability Loop

Viability proof is the highest priority.

Detection alone is not enough. Outcome labels alone are not enough. Diagnostics alone are not enough. Evidence packets alone are not enough. Packet readiness alone is not enough. Aggregate review alone is not enough. The next step must gate the aggregate review for proof-readiness so missing setup-type, symbol, diagnosis, fix-path, regression, lower-tier handoff, and proof-gap patterns are explicit before any optimization.

Required viability loop:

detect -> score outcome -> diagnose deeply -> package evidence -> evaluate packet readiness -> aggregate ready packet review -> gate aggregate review readiness -> analyze whole system -> decide fix path -> adjust rule/contract/test -> run regression -> review again

## 11. Diagnostics-Before-Optimization Rule

Diagnostics, evidence packets, packet readiness, aggregate review, and review-readiness gating must come before optimization.

Shallow labels like good setup, bad setup, bad alert, weak signal, failed trade, enough proof, or ready for review are not enough. Review-readiness gating must be tied to evidence completeness, missing evidence by setup type and symbol, diagnosis clarity, repeated fix path clarity, named regression coverage, unresolved proof gaps, lower-tier handoff requirement, and no-trade/no-optimization boundary preservation.

No threshold, ranking, trigger, invalidation, freshness, blocker/caution, workflow, or alert optimization may be proposed until the readiness gate identifies an evidence-backed rule, contract, fixture, planning, or test gap.

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
- mark group review ready without named evidence, setup type, symbol, diagnosis, fix path, regression coverage, lower-tier handoff state, and proof-gap status

Setup recognition, trigger, invalidation, fresh/stale/spent, blocker/caution, ranking/focus, outcome scoring, diagnostics, evidence packaging, packet readiness, aggregate review, review-readiness gating, and user workflow should be rule-based.

## 13. Lower-Tier Handoff Requirement

If the readiness gate finds missing evidence, setup types needing more evidence, symbols needing more evidence, unclear setup type, unclear symbol, merged setup/symbol grouping, unclear diagnosis, vague next fix path, missing regression name, unresolved proof gaps, proof-limited records, rejected proof records, stale/freshness gaps, trigger/invalidation ambiguity, blocker/caution ambiguity, session-boundary ambiguity, workflow ambiguity, readiness contract gaps, aggregate review contract gaps, or boundary violations, the output must identify lower-tier handoff before any higher-tier optimization or live-readiness step.

Lower-tier handoff means the next fix path must go back to the smallest responsible local contract, fixture, test, or planning layer before changing broader watcher behavior. It must not skip directly to live data, alerts, trading, account sizing, production, or optimization.

The readiness output must be compact and explicit enough that lower-tier review can see reviewed packets, setup types, symbols, outcome groups, evidence gaps, repeated fix paths, named regressions, proof gaps, and no-trade/no-optimization state without reconstructing the full aggregator internals.

## 14. Boundary Statement

This docs-only plan does not start code work, optimization, controlled shadow data, live data, watcher loops, alerts, generated reports/logs, broker/order/account/options/P&L, account sizing, production/Railway/live backend work, or live trade decisions.

This docs-only plan does not modify `main.py`, engine logic, watcher code, tests, Railway/deploy files, secrets, `.env` files, credentials, tokens, deployment settings, generated output paths, report/log writers, watcher loops, alert delivery, broker/order/account behavior, options behavior, option P&L, position sizing, account sizing, or live trade decision logic.
