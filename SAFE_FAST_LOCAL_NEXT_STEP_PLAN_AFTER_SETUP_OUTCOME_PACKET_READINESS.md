# SAFE-FAST Local Next-Step Plan After Setup Outcome Packet Readiness

## 1. Plain-English Purpose

SAFE-FAST can now build setup outcome evidence packets and evaluate whether those packets are ready for review. The next small local build step should review a group of ready packet outputs together, while keeping setup type and symbol separate, so the system can see repeated worked/failed/missing-evidence patterns before any optimization.

The future aggregator should answer which ready packets are being reviewed, which setup types and symbols are represented, what worked, what failed, what lacked evidence, which fix paths repeat, which regression tests are needed, whether there is enough proof to continue review, and whether the work remains no-trade and not an optimization step.

This plan is local-only and docs-only. It does not start code work, live data, controlled shadow data, watcher loops, alerts, generated reports/logs, optimization, production work, or trade decisions.

## 2. Day 33 Context

- **Baseline:** patch8.
- **Repo:** `safe-fast-backendnew`.
- **Branch:** `main`.
- **Current working day context:** Day 33.
- **Latest local commit provided for this task:** `ca55023 Add setup outcome packet readiness evaluator`.
- **Work mode:** SAFE-FAST build work only, not live trade decisions.
- **Planning scope:** docs-only local next-step planning after the setup outcome packet readiness evaluator.
- **Highest priority:** viability proof before optimization.
- **Tier pressure:** use the current high-capability review window to make proof review compact, explicit, transferable, and lower-tier handoff friendly.

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
- The readiness evaluator accepts only in-memory setup outcome evidence packet summaries, preserves setup type and symbol separation, identifies missing evidence, unclear diagnosis, unclear next fix path, missing regression, rejected/proof-limited records, lower-tier handoff needs, and no-trade/no-live/no-shadow/no-alert/no-file-write/no-broker/no-optimization boundaries.
- No live data, controlled shadow data, watcher loops, alerts, generated reports/logs, broker/order/account/options/P&L, account sizing, production/Railway/live backend work, or live trade decisions are active.

## 4. What Is Still Unproven

- Final SAFE-FAST trading-plan viability is not proven.
- Actual historical success is not proven.
- Repeatability of successful setup outcomes is not proven.
- It is not yet proven whether a group of ready packets shows enough evidence to continue proof review.
- It is not yet proven which setup types are represented across ready packets.
- It is not yet proven which symbols are represented across ready packets.
- It is not yet proven whether worked, failed, inconclusive, stale, invalidated, pending, and insufficient-evidence outcomes repeat by setup type without being merged into symbol behavior.
- It is not yet proven whether repeated fix paths point to setup recognition, trigger/invalidation, freshness, blocker/caution, session boundary, outcome scoring, data quality, packet contract, or lower-tier handoff gaps.
- It is not yet proven which regression tests are needed before any rule, contract, fixture, or workflow change.
- Controlled shadow data, live data, alerts, generated reports/logs, broker/order/account/options/P&L behavior, account sizing, production readiness, Railway/deploy readiness, live backend readiness, live trade readiness, and live trade decisions remain forbidden and unproven.

## 5. Exact Next Implementation Step

Add one local-only in-memory setup outcome proof review aggregator.

The future aggregator should accept only a caller-provided list of in-memory summaries from `evaluate_setup_outcome_packet_readiness(...)` and return one in-memory aggregate review summary. It should not read files, fetch data, write files, generate reports/logs, start watcher behavior, change rules, optimize, or make trade decisions.

The aggregate summary should answer:

- Which ready packet summaries are being reviewed?
- Which setup types are represented?
- Which symbols are represented?
- What worked?
- What failed?
- What stayed pending, became stale, invalidated before trigger, or stayed inconclusive?
- What lacked evidence?
- Which readiness gaps repeat?
- Which next fix paths repeat?
- Which regression tests are needed?
- Is there enough proof to continue review, or is more evidence needed?
- Is lower-tier handoff required before broader changes?
- Is this still no-trade and not an optimization step?

The output should keep setup type and symbol as separate fields and separate grouping keys. It may summarize by setup type, by symbol, and by setup-type-plus-symbol pairing, but it must not merge setup identity and symbol identity into free text.

## 6. Allowed Files for That Future Step

- `watcher_foundation/setup_outcome_review_aggregator.py`
- `watcher_foundation/__init__.py`
- `tests/test_setup_outcome_review_aggregator.py`
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
- Any rule change or optimization before diagnostics, packet readiness, and aggregate review identify an evidence-backed gap

## 8. Required Tests for the Future Implementation Step

Add focused local unit tests in `tests/test_setup_outcome_review_aggregator.py` covering:

- Accepts only a list of in-memory setup outcome packet readiness summaries.
- Requires each input to preserve `watch_only=True`, `setup_outcome_packet_readiness_only=True`, `setup_outcome_evidence_packet_only=True`, `setup_outcome_diagnostics_only=True`, `setup_outcome_proof_only=True`, `final_viability_proven=False`, `optimization_started=False`, and `no_rule_change_started=True`.
- Rejects inputs that started live data, controlled shadow data, alerts, file writes, broker/trade behavior, optimization, or rule changes.
- Lists the reviewed packet identifiers or explicit unavailable identifiers without fabricating them.
- Preserves setup type and symbol separation in aggregate output.
- Summarizes represented setup types and represented symbols independently.
- Summarizes worked, failed, inconclusive, pending, stale, invalidated, and insufficient-evidence outcomes when present in packet/readiness items.
- Carries missing evidence and readiness gaps without hiding unavailable fields.
- Counts repeated next fix paths without converting them into optimization instructions.
- Collects regression-needed entries and requires named regression coverage before broader changes.
- Requires lower-tier handoff when readiness gaps, missing evidence, proof-limited records, rejected records, unclear setup/symbol identity, or boundary violations are present.
- Emits a proof-continuation decision such as `continue_review_with_ready_packets`, `needs_more_evidence_before_review`, or `blocked_by_readiness_contract_gap`.
- Preserves no-trade, no-rule-change, no-optimization, no-file-write, no-live-data, no-controlled-shadow-data, no-alert, and no-broker boundaries.
- Does not scan repo files, fetch data, start threads, invoke subprocesses, or write files/logs/reports.
- Rejects or quarantines broker/order/account/options/P&L/account-sizing/live-trade-decision fields.

Required validation commands for that future implementation:

- `python -m unittest discover -s tests -p test_setup_outcome_review_aggregator.py`
- `python -m unittest discover -s tests -p test_setup_outcome_packet_readiness.py`
- `python -m unittest discover -s tests -p test_setup_outcome_evidence_packet.py`
- `python -m unittest discover -s tests -p test_setup_outcome_diagnostics.py`
- `python -m unittest discover -s tests -p test_setup_outcome_proof.py`
- `python -m unittest tests.test_watcher_foundation_scaffold`
- `git diff --check`

## 9. Required Build-State / Doc Updates for the Future Step

The future implementation must update `SAFE_FAST_BUILD_STATE.md` with:

- Implementation status for the local-only setup outcome proof review aggregator.
- Baseline `patch8` and Day 33 context.
- Exact implementation file and test file.
- Focused review aggregator test result.
- Setup outcome packet readiness regression result.
- Setup outcome evidence packet regression result.
- Setup outcome diagnostics regression result.
- Setup outcome proof regression result.
- Watcher-foundation scaffold regression result.
- `git diff --check` result.
- Preserved scope and no-go boundaries.
- Next local-only objective after the aggregator.

Do not claim final viability, historical success, controlled shadow readiness, live readiness, production readiness, Railway readiness, live backend readiness, live trade readiness, or live trade decision readiness.

## 10. Viability Loop

Viability proof is the highest priority.

Detection alone is not enough. Outcome labels alone are not enough. Diagnostics alone are not enough. Evidence packets alone are not enough. Packet readiness alone is not enough. The next step must aggregate ready packet review evidence so repeated setup-type, symbol, missing-evidence, and fix-path patterns can be seen before any optimization.

Required viability loop:

detect -> score outcome -> diagnose deeply -> package evidence -> evaluate packet readiness -> aggregate ready packet review -> analyze whole system -> decide fix path -> adjust rule/contract/test -> run regression -> review again

## 11. Diagnostics-Before-Optimization Rule

Diagnostics, evidence packets, packet readiness, and aggregate review must come before optimization.

Shallow labels like good setup, bad setup, bad alert, weak signal, failed trade, or enough proof are not enough. Aggregate review must be tied to evidence completeness, missing evidence, setup type separation, symbol separation, diagnosis clarity, next fix path clarity, named regression coverage, lower-tier handoff requirement, and no-trade/no-optimization boundary preservation.

No threshold, ranking, trigger, invalidation, freshness, blocker/caution, workflow, or alert optimization may be proposed until aggregate review identifies an evidence-backed rule, contract, fixture, planning, or test gap.

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
- mark aggregate proof sufficient without named evidence, setup type, symbol, diagnosis, fix path, and regression coverage

Setup recognition, trigger, invalidation, fresh/stale/spent, blocker/caution, ranking/focus, outcome scoring, diagnostics, evidence packaging, packet readiness, aggregate review, and user workflow should be rule-based.

## 13. Lower-Tier Handoff Requirement

If the aggregator finds missing evidence, unclear setup type, unclear symbol, merged setup/symbol grouping, unclear diagnosis, vague next fix path, missing regression name, proof-limited records, rejected proof records, stale/freshness gaps, trigger/invalidation ambiguity, blocker/caution ambiguity, session-boundary ambiguity, workflow ambiguity, readiness contract gaps, or boundary violations, the output must identify lower-tier handoff before any higher-tier optimization or live-readiness step.

Lower-tier handoff means the next fix path must go back to the smallest responsible local contract, fixture, test, or planning layer before changing broader watcher behavior. It must not skip directly to live data, alerts, trading, account sizing, production, or optimization.

The aggregate output must be compact and explicit enough that lower-tier review can see reviewed packets, setup types, symbols, outcomes, evidence gaps, repeated fix paths, named regressions, and no-trade/no-optimization state without reconstructing the full evaluator internals.

## 14. Boundary Statement

This docs-only plan does not start code work, optimization, controlled shadow data, live data, watcher loops, alerts, generated reports/logs, broker/order/account/options/P&L, account sizing, production/Railway/live backend work, or live trade decisions.

This docs-only plan does not modify `main.py`, engine logic, watcher code, tests, Railway/deploy files, secrets, `.env` files, credentials, tokens, deployment settings, generated output paths, report/log writers, watcher loops, alert delivery, broker/order/account behavior, options behavior, option P&L, position sizing, account sizing, or live trade decision logic.

