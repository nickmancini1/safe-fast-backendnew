# SAFE-FAST Local Next-Step Plan After Setup Outcome Diagnostics

## 1. Plain-English Purpose

SAFE-FAST can now explain what happened after a setup and why. The next small build step should turn that explanation into a compact local review packet that a lower-tier reviewer can inspect without reopening the whole diagnostic chain.

The packet should show what setup appeared, what happened after it appeared, why it worked, failed, stayed pending, went stale, was invalidated, or lacked evidence, what evidence supports that conclusion, what is missing, what fix path is next, and what regression test is needed. Setup type and symbol must stay separate.

This plan is local-only and docs-only. It does not start live trade chat, live data, controlled shadow data, watcher loops, alerts, generated reports/logs, optimization, production work, or trade decisions.

## 2. Baseline and Day 33 Context

- **Baseline:** patch8.
- **Repo:** `safe-fast-backendnew`.
- **Branch:** `main`.
- **Current working day context:** Day 33.
- **Latest local setup outcome diagnostics milestone:** `800f324 Add setup outcome diagnostics evaluator`.
- **Work mode:** SAFE-FAST build work only, not live trade decisions.
- **Planning scope:** docs-only local next-step planning after the setup outcome diagnostics evaluator.
- **Highest priority:** prove whether SAFE-FAST can become a viable trading plan under no-hindsight review.

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
- The diagnostics evaluator accepts only the in-memory setup outcome proof summary, preserves watch-only/no-hindsight/no-trade/no-live/no-shadow/no-alert/no-file-write/no-broker/no-optimization boundaries, separates diagnostics by setup type and symbol, and emits evidence-backed what-happened text, likely cause candidates, next fix paths, lower-tier handoff flags, proof-limited reasons, and regression-needed fields.

## 4. What Is Still Unproven

- Final SAFE-FAST trading-plan viability is not proven.
- Actual historical success is not proven.
- Repeatability of successful setup outcomes is not proven.
- It is not yet proven whether setup failures are caused by setup recognition, trigger evidence, trigger level/zone ambiguity, invalidation ambiguity, stale/fresh/spent handling, blocker/caution handling, session boundary handling, missing evidence, outcome scoring gaps, workflow ambiguity, or lower-tier contract gaps.
- It is not yet proven whether the diagnostic findings are compact enough for reliable lower-tier review.
- It is not yet proven whether the next fix path should be a rule/contract/test adjustment, a fixture/evidence gap, or a lower-tier handoff.
- Controlled shadow data has not started.
- Live data has not started.
- Alerts have not started.
- Generated reports/logs have not started.
- Broker/order/account/options/P&L behavior remains forbidden.
- Account sizing remains forbidden.
- Production readiness, Railway/deploy readiness, live backend readiness, live trade readiness, and live trade decisions remain forbidden and unproven.

## 5. Exact Next Implementation Step

Add one local-only in-memory setup outcome evidence packet builder.

The future builder should accept the in-memory summary from `evaluate_setup_outcome_diagnostics(...)` and return one compact in-memory evidence packet summary. It should not read files, fetch data, write files, generate reports/logs, start watcher behavior, change rules, optimize, or make trade decisions.

Each packet item should include:

- setup type
- symbol
- setup identifier when available
- what setup appeared
- what happened after it appeared
- why it worked, failed, stayed pending, went stale, was invalidated, or lacked evidence
- evidence references and after-setup evidence used
- unavailable or missing evidence
- proof-limited reason
- likely cause candidates
- affected system area
- next fix path
- required regression test
- lower-tier handoff requirement
- no-hindsight/no-trade boundary confirmation

The packet should be compact enough for lower-tier review while preserving enough evidence to prevent hidden discretion or fabricated conclusions.

## 6. Allowed Files for That Future Step

- `watcher_foundation/setup_outcome_evidence_packet.py`
- `watcher_foundation/__init__.py`
- `tests/test_setup_outcome_evidence_packet.py`
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
- Any rule change or optimization before diagnostics prove what needs fixing

## 8. Required Tests for the Future Implementation Step

Add focused local unit tests in `tests/test_setup_outcome_evidence_packet.py` covering:

- Accepts only the in-memory setup outcome diagnostics summary shape.
- Requires `watch_only=True`, `setup_outcome_diagnostics_only=True`, `setup_outcome_proof_only=True`, `final_viability_proven=False`, `optimization_started=False`, and `no_rule_change_started=True`.
- Rejects summaries that started live data, controlled shadow data, alerts, file writes, broker/trade behavior, optimization, or rule changes.
- Preserves setup type and symbol as separate packet grouping keys.
- Emits one compact packet item per accepted diagnostic finding.
- Preserves rejected proof reasons as lower-tier handoff packet evidence.
- Includes what setup appeared, what happened after it appeared, why it happened, evidence support, missing evidence, next fix path, regression needed, and lower-tier handoff flag.
- Carries proof-limited reason and unavailable evidence without fabricating values.
- Preserves triggered worked, triggered failed, triggered inconclusive, stayed valid pending, stale without trigger, invalidated before trigger, and insufficient evidence cases.
- Rejects shallow packet conclusions without evidence.
- Preserves no-trade, no-rule-change, no-optimization, no-file-write, no-live-data, no-controlled-shadow-data, no-alert, and no-broker boundaries.
- Does not scan repo files, fetch data, start threads, invoke subprocesses, or write files/logs/reports.
- Rejects or quarantines broker/order/account/options/P&L/account-sizing/live-trade-decision fields.

Required validation commands for that future implementation:

- `python -m unittest discover -s tests -p test_setup_outcome_evidence_packet.py`
- `python -m unittest discover -s tests -p test_setup_outcome_diagnostics.py`
- `python -m unittest discover -s tests -p test_setup_outcome_proof.py`
- `python -m unittest discover -s tests -p test_day60_outcome_diagnostics.py`
- `python -m unittest discover -s tests -p test_historical_outcome_diagnostics.py`
- `python -m unittest tests.test_watcher_foundation_scaffold`
- `git diff --check`

## 9. Required Build-State / Doc Updates for the Future Step

The future implementation must update `SAFE_FAST_BUILD_STATE.md` with:

- Implementation status for the local-only setup outcome evidence packet builder.
- Baseline `patch8` and Day 33 context.
- Exact implementation file and test file.
- Focused evidence packet test result.
- Setup outcome diagnostics regression result.
- Setup outcome proof regression result.
- Day 60 outcome diagnostics regression result.
- Historical outcome diagnostics regression result.
- Watcher-foundation scaffold regression result.
- `git diff --check` result.
- Preserved scope and no-go boundaries.
- Next local-only objective after the evidence packet builder.

Do not claim final viability, historical success, controlled shadow readiness, live readiness, production readiness, Railway readiness, live backend readiness, live trade readiness, or live trade decision readiness.

## 10. Viability Loop

Viability proof is the highest priority.

Detection alone is not enough. Outcome labels alone are not enough. Diagnostics alone are not enough. The next step must make the diagnostic evidence compact enough to review, compare, and route to the smallest responsible fix path.

Required viability loop:

detect -> score outcome -> diagnose deeply -> package evidence -> analyze whole system -> decide fix path -> adjust rule/contract/test -> run regression -> review again

## 11. Diagnostics-Before-Optimization Rule

Diagnostics and evidence packaging must come before optimization.

Shallow labels like failed setup, bad alert, weak signal, or bad trade are not enough. The packet must preserve evidence, likely cause, affected setup type, affected symbol when available, affected stage, trigger/invalidation/freshness relationship, affected system area, next fix path, required regression test, and lower-tier handoff requirement.

No threshold, ranking, trigger, invalidation, freshness, blocker/caution, or workflow optimization may be proposed until diagnostic output identifies an evidence-backed rule, contract, fixture, or test gap.

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

Setup recognition, trigger, invalidation, fresh/stale/spent, blocker/caution, ranking/focus, outcome scoring, diagnostics, evidence packaging, and user workflow should be rule-based.

## 13. Lower-Tier Handoff Requirement

If the evidence packet shows insufficient evidence, stale setup handling gaps, trigger/invalidation ambiguity, blocker/caution ambiguity, session-boundary ambiguity, diagnostics gaps, workflow ambiguity, or rejected proof records, the output must identify whether lower-tier handoff is required before any higher-tier optimization or live-readiness step.

Lower-tier handoff means the next fix path must go back to the smallest responsible local contract, fixture, test, or planning layer before changing broader watcher behavior. It must not skip directly to live data, alerts, trading, account sizing, production, or optimization.

The packet must be compact and explicit enough that lower-tier review can see the setup type, symbol, evidence, missing fields, fix path, and regression need without reconstructing the full evaluator internals.

## 14. Boundary Statement

This docs-only plan does not start code work, optimization, controlled shadow data, live data, watcher loops, alerts, generated reports/logs, broker/order/account/options/P&L, account sizing, production/Railway/live backend work, or live trade decisions.

This docs-only plan does not modify `main.py`, engine logic, watcher code, tests, Railway/deploy files, secrets, `.env` files, credentials, tokens, deployment settings, generated output paths, report/log writers, watcher loops, alert delivery, broker/order/account behavior, options behavior, option P&L, position sizing, account sizing, or live trade decision logic.
