# SAFE-FAST Local Next-Step Plan After Setup Outcome Review Readiness

## 1. Plain-English Purpose

SAFE-FAST can now check whether a grouped setup outcome proof review is complete enough to trust for proof work. The next small local build step should package readiness-gated group reviews into one historical setup proof review bundle.

The future bundle builder should answer which ready group reviews are included, which setup types and symbols are represented, what evidence is still missing, what worked across reviewed groups, what failed across reviewed groups, which fix paths repeat, which regression tests are needed, whether the bundle is ready for lower-tier review, and whether the bundle remains proof review only, not trading and not optimization.

This plan is local-only and docs-only. It does not start code work, live data, controlled shadow data, watcher loops, alerts, generated reports/logs, optimization, production work, or trade decisions.

## 2. Day 33 Context

- **Baseline:** patch8.
- **Repo:** `safe-fast-backendnew`.
- **Branch:** `main`.
- **Current working day context:** Day 33.
- **Latest local commit provided for this task:** `51fb006 Add setup outcome proof review readiness gate`.
- **Work mode:** SAFE-FAST build work only, not live trade decisions.
- **Planning scope:** docs-only local next-step planning after the setup outcome proof review readiness gate.
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
- Setup outcome proof review readiness gate is complete at `51fb006`.
- The readiness gate accepts only one caller-provided in-memory aggregate review summary, preserves reviewed packets and unavailable packet identifiers, keeps setup type and symbol separate, identifies setup types, symbols, and setup-type-plus-symbol pairs needing more evidence, checks explicit outcome groups, flags unclear diagnoses, unclear repeated fix paths, missing regression coverage, unresolved proof gaps, and lower-tier review decisions.
- No live data, controlled shadow data, watcher loops, alerts, generated reports/logs, broker/order/account/options/P&L, account sizing, production/Railway/live backend work, or live trade decisions are active.

## 4. What Is Still Unproven

- Final SAFE-FAST trading-plan viability is not proven.
- Actual historical success is not proven.
- Repeatability of successful setup outcomes across a historical bundle is not proven.
- It is not yet proven which readiness-gated group reviews should be included in one historical proof review bundle.
- It is not yet proven which setup types are sufficiently represented across bundled group reviews.
- It is not yet proven which symbols are sufficiently represented across bundled group reviews.
- It is not yet proven what evidence remains missing across the whole bundle.
- It is not yet proven what worked repeatedly across reviewed groups.
- It is not yet proven what failed repeatedly across reviewed groups.
- It is not yet proven which lower-tier fix paths repeat across group reviews.
- It is not yet proven which regression tests are needed at bundle level before any broader change.
- It is not yet proven whether a bundled historical proof review is ready for lower-tier review.
- Controlled shadow data, live data, alerts, generated reports/logs, broker/order/account/options/P&L behavior, account sizing, production readiness, Railway/deploy readiness, live backend readiness, live trade readiness, and live trade decisions remain forbidden and unproven.

## 5. Exact Next Implementation Step

Add one local-only in-memory historical setup proof review bundle builder.

The future builder should accept only caller-provided readiness summaries from `evaluate_setup_outcome_review_readiness(...)` and return one in-memory bundle summary. It should not read files, fetch data, write files, generate reports/logs, start watcher behavior, change rules, optimize, or make trade decisions.

The bundle summary should answer:

- Which ready group reviews are included?
- Which setup types are represented?
- Which symbols are represented?
- Which setup-type-plus-symbol pairs are represented?
- What evidence is still missing?
- What worked across the reviewed groups?
- What failed across the reviewed groups?
- Which inconclusive, pending, stale, invalidated, or missing-evidence patterns remain?
- Which fix paths repeat?
- Which regression tests are needed?
- Which proof gaps still block bundle review?
- Is lower-tier handoff required?
- Is this bundle ready for lower-tier review?
- Is this still proof review, not trading and not optimization?

The output should keep setup type and symbol as separate fields and grouping keys. It may summarize bundle-level gaps by setup type, by symbol, and by setup-type-plus-symbol pairing, but it must not merge setup identity and symbol identity into free text.

## 6. Allowed Files for That Future Step

- `watcher_foundation/setup_outcome_proof_review_bundle.py`
- `watcher_foundation/__init__.py`
- `tests/test_setup_outcome_proof_review_bundle.py`
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
- Any rule change or optimization before diagnostics, packet readiness, aggregate review, review-readiness gating, and bundle review identify an evidence-backed gap

## 8. Required Tests for the Future Implementation Step

Add focused local unit tests in `tests/test_setup_outcome_proof_review_bundle.py` covering:

- Accepts only a list of in-memory setup outcome proof review readiness summaries.
- Requires `watch_only=True`, `setup_outcome_review_readiness_only=True`, `setup_outcome_review_aggregator_only=True`, `setup_outcome_packet_readiness_only=True`, `setup_outcome_evidence_packet_only=True`, `setup_outcome_diagnostics_only=True`, `setup_outcome_proof_only=True`, `final_viability_proven=False`, `optimization_started=False`, and `no_rule_change_started=True`.
- Rejects inputs that started live data, controlled shadow data, alerts, file writes, broker/trade behavior, optimization, or rule changes.
- Includes only readiness summaries that are complete enough for proof work or clearly marks excluded/not-ready summaries without fabricating readiness.
- Lists included group reviews and preserves reviewed packet identifiers or explicit unavailable identifiers.
- Preserves setup type, symbol, and setup-type-plus-symbol separation across the bundle.
- Aggregates worked and failed groups across included reviews without claiming profitability or final viability.
- Carries inconclusive, pending, stale, invalidated, and missing-evidence groups explicitly.
- Aggregates missing evidence by setup type, symbol, and setup-type-plus-symbol pair.
- Counts repeated fix paths and repeated regression needs.
- Requires named regression coverage for proof-blocking bundle gaps.
- Emits lower-tier handoff items when evidence, diagnosis, fix-path, regression, contract, setup type, symbol, or boundary gaps remain.
- Emits a bundle review decision such as `ready_for_lower_tier_review`, `needs_more_evidence_before_lower_tier_review`, or `blocked_by_bundle_contract_gap`.
- Preserves no-trade, no-rule-change, no-optimization, no-file-write, no-live-data, no-controlled-shadow-data, no-alert, and no-broker boundaries.
- Does not scan repo files, fetch data, start threads, invoke subprocesses, or write files/logs/reports.
- Rejects or quarantines broker/order/account/options/P&L/account-sizing/live-trade-decision fields.

Required validation commands for that future implementation:

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

- Implementation status for the local-only historical setup proof review bundle builder.
- Baseline `patch8` and Day 33 context.
- Exact implementation file and test file.
- Focused proof review bundle test result.
- Setup outcome review readiness regression result.
- Setup outcome review aggregator regression result.
- Setup outcome packet readiness regression result.
- Setup outcome evidence packet regression result.
- Setup outcome diagnostics regression result.
- Setup outcome proof regression result.
- Watcher-foundation scaffold regression result.
- `git diff --check` result.
- Preserved scope and no-go boundaries.
- Next local-only objective after the bundle builder.

Do not claim final viability, historical success, controlled shadow readiness, live readiness, production readiness, Railway readiness, live backend readiness, live trade readiness, or live trade decision readiness.

## 10. Viability Loop

Viability proof is the highest priority.

Detection alone is not enough. Outcome labels alone are not enough. Diagnostics alone are not enough. Evidence packets alone are not enough. Packet readiness alone is not enough. Aggregate review alone is not enough. Review-readiness gating alone is not enough. The next step must bundle readiness-gated group reviews so repeated worked/failed/missing-evidence/fix-path/regression patterns are explicit before any optimization.

Required viability loop:

detect -> score outcome -> diagnose deeply -> package evidence -> evaluate packet readiness -> aggregate ready packet review -> gate aggregate review readiness -> bundle historical proof review -> analyze whole system -> decide fix path -> adjust rule/contract/test -> run regression -> review again

## 11. Diagnostics-Before-Optimization Rule

Diagnostics, evidence packets, packet readiness, aggregate review, review-readiness gating, and bundle review must come before optimization.

Shallow labels like good setup, bad setup, bad alert, weak signal, failed trade, enough proof, ready for review, or bundle ready are not enough. Bundle review must be tied to included group reviews, setup type representation, symbol representation, missing evidence, worked/failed patterns, repeated fix paths, named regression coverage, unresolved proof gaps, lower-tier handoff requirement, and no-trade/no-optimization boundary preservation.

No threshold, ranking, trigger, invalidation, freshness, blocker/caution, workflow, or alert optimization may be proposed until the bundle builder identifies an evidence-backed rule, contract, fixture, planning, or test gap.

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
- include a group review in a bundle without readiness-gate support
- mark a bundle ready without named included reviews, setup types, symbols, evidence gaps, worked/failed patterns, fix paths, regression coverage, lower-tier handoff state, and proof-gap status

Setup recognition, trigger, invalidation, fresh/stale/spent, blocker/caution, ranking/focus, outcome scoring, diagnostics, evidence packaging, packet readiness, aggregate review, review-readiness gating, bundle review, and user workflow should be rule-based.

## 13. Lower-Tier Handoff Requirement

If the bundle builder finds missing evidence, setup types needing more evidence, symbols needing more evidence, unclear setup type, unclear symbol, merged setup/symbol grouping, unclear diagnosis, vague next fix path, missing regression name, unresolved proof gaps, proof-limited records, rejected proof records, stale/freshness gaps, trigger/invalidation ambiguity, blocker/caution ambiguity, session-boundary ambiguity, workflow ambiguity, readiness contract gaps, aggregate review contract gaps, bundle contract gaps, or boundary violations, the output must identify lower-tier handoff before any higher-tier optimization or live-readiness step.

Lower-tier handoff means the next fix path must go back to the smallest responsible local contract, fixture, test, or planning layer before changing broader watcher behavior. It must not skip directly to live data, alerts, trading, account sizing, production, or optimization.

The bundle output must be compact and explicit enough that lower-tier review can see included group reviews, setup types, symbols, outcome groups, evidence gaps, repeated fix paths, named regressions, proof gaps, and no-trade/no-optimization state without reconstructing every upstream readiness summary.

## 14. Boundary Statement

This docs-only plan does not start code work, optimization, controlled shadow data, live data, watcher loops, alerts, generated reports/logs, broker/order/account/options/P&L, account sizing, production/Railway/live backend work, or live trade decisions.

This docs-only plan does not modify `main.py`, engine logic, watcher code, tests, Railway/deploy files, secrets, `.env` files, credentials, tokens, deployment settings, generated output paths, report/log writers, watcher loops, alert delivery, broker/order/account behavior, options behavior, option P&L, position sizing, account sizing, or live trade decision logic.
