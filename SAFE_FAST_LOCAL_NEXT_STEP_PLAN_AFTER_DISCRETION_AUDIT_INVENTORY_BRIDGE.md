# SAFE-FAST Local Next-Step Plan After Discretion Audit Inventory Bridge

## 1. Baseline and Day 32 Context

- **Baseline:** patch8.
- **Repo:** `safe-fast-backendnew`.
- **Branch:** `main`.
- **Current working day context:** Day 32.
- **Work mode:** SAFE-FAST build work only, not live trade chat.
- **Latest committed build step:** `a6b0d60 Add discretion audit inventory bridge gate`.
- **Day 31 status:** historical context only.
- **Day 28 file names:** historical labels only.
- **Planning scope:** docs-only local planning after the discretion audit inventory bridge gate.

## 2. Current Fixed Foundation

- Replay/regression foundation is complete.
- Shadow review/export bundle foundation is complete.
- Day 60 local input-contract validator is complete.
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
- Discretion audit inventory-to-audit/coverage bridge gate is complete at `a6b0d60`.
- The bridge validates caller-provided inventory, converts accepted items into existing audit input, runs existing audit/coverage evaluators under watch-only boundaries, and returns one in-memory readiness/audit/coverage summary.
- Strict Day 28 and Day 31 docs remain historical context; Day 32 is the current working context.

## 3. What Is Still Unproven

- Final SAFE-FAST trading-plan viability is not proven.
- Actual historical success is not proven.
- The system does not yet locally connect detected setup records to normalized post-setup outcome scoring and diagnostics.
- It is not yet proven what happens after a setup appears: whether it triggers, stays valid, becomes stale, gets invalidated, works, fails, or lacks enough evidence.
- It is not yet proven which setup failures are rule failures, evidence gaps, stale/freshness failures, trigger/invalidation problems, diagnostics gaps, or lower-tier handoff issues.
- Controlled shadow data has not started.
- Live data has not started.
- Alerts have not started.
- Generated reports/logs have not started.
- Broker/order/account/options/P&L behavior remains forbidden.
- Account sizing remains forbidden.
- Production readiness, Railway/deploy readiness, live backend readiness, live trade readiness, and live trade decisions remain forbidden and unproven.

## 4. Active Objective

Pick exactly one next local-only implementation step that moves SAFE-FAST closer to proving whether the trading plan works:

**A local-only setup outcome proof contract evaluator.**

The future step should connect caller-provided detected setup records to caller-provided post-setup evidence and produce in-memory outcome scoring plus diagnostics. It must answer, for each setup: what happened after detection, what outcome category is supported by evidence, what is missing, and what fix path should be reviewed next.

## 5. Exact Next Implementation Step

Add a local-only in-memory module that evaluates setup outcome proof records.

The future evaluator must:

- Accept caller-provided in-memory setup outcome proof records only.
- Require a frozen detected setup identity before any post-setup outcome scan.
- Preserve no-hindsight ordering between setup evidence and later outcome evidence.
- Classify each setup into exactly one evidence-backed outcome status:
  - `triggered_worked`
  - `triggered_failed`
  - `triggered_inconclusive`
  - `stayed_valid_pending`
  - `stale_without_trigger`
  - `invalidated_before_trigger`
  - `insufficient_evidence`
- Preserve trigger, invalidation, freshness/staleness, blocker/caution, ranking/focus, outcome scoring, diagnostics, and user workflow fields as caller-provided evidence only.
- Produce in-memory diagnostics that identify evidence, likely cause, affected setup type, affected symbol when available, affected stage, trigger/invalidation/freshness relationship, affected system area, next fix path, and lower-tier handoff need.
- Mark records as proof-limited when trigger level, invalidation level, timing, source row reference, or post-setup evidence is missing.
- Avoid any optimization recommendation unless diagnostics first identify an evidence-backed rule/contract/test gap.
- Return one in-memory summary only; no files, logs, reports, live data, alerts, watcher loops, or trade decisions.

## 6. Allowed Files for That Future Step

- `watcher_foundation/setup_outcome_proof.py`
- `watcher_foundation/__init__.py`
- `tests/test_setup_outcome_proof.py`
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

Add focused local unit tests in `tests/test_setup_outcome_proof.py` covering:

- Accepts caller-provided in-memory setup outcome proof records only.
- Requires frozen setup identity before post-setup outcome evidence.
- Preserves no-hindsight ordering and rejects future evidence used to define the original setup.
- Classifies `triggered_worked`.
- Classifies `triggered_failed`.
- Classifies `triggered_inconclusive`.
- Classifies `stayed_valid_pending`.
- Classifies `stale_without_trigger`.
- Classifies `invalidated_before_trigger`.
- Classifies `insufficient_evidence`.
- Marks proof-limited records when trigger/invalidation/freshness/source-row evidence is missing.
- Emits diagnostics with evidence, likely cause, affected setup type, symbol when available, stage, trigger/invalidation/freshness relationship, system area, next fix path, and lower-tier handoff need.
- Preserves no-trade, no-rule-change, no-optimization, no-file-write, no-live-data, no-controlled-shadow-data, no-alert, and no-broker boundaries.
- Does not scan repo files, fetch data, start threads, invoke subprocesses, or write files/logs/reports.
- Rejects or quarantines broker/order/account/options/P&L/account-sizing/live-trade-decision fields.

Required validation commands for that future implementation:

- `python -m unittest discover -s tests -p test_setup_outcome_proof.py`
- `python -m unittest discover -s tests -p test_discretion_audit_inventory_bridge.py`
- `python -m unittest tests.test_watcher_foundation_scaffold`
- `git diff --check`

## 9. Required Build-State / Doc Updates for the Future Step

The future implementation must update `SAFE_FAST_BUILD_STATE.md` with:

- Implementation status for the local-only setup outcome proof contract evaluator.
- Baseline `patch8` and Day 32 context.
- Exact implementation file and test file.
- Focused test result.
- Bridge regression result.
- Watcher-foundation scaffold regression result.
- `git diff --check` result.
- Preserved scope and no-go boundaries.
- Next local-only objective after outcome proof evaluation.

Do not claim final viability, historical success, controlled shadow readiness, live readiness, production readiness, Railway readiness, live backend readiness, live trade readiness, or live trade decision readiness.

## 10. No-Go Boundaries

- No `main.py`.
- No engine logic.
- No Railway/deploy files.
- No production or live backend work.
- No live data.
- No controlled shadow data.
- No watcher loops.
- No alerts.
- No generated reports/logs.
- No broker/order/account/options/P&L.
- No account sizing.
- No live trade decisions.
- No secrets, `.env`, credentials, tokens, or deployment settings.
- No rule changes.
- No optimization before diagnostics.
- No hidden repo-file audit automation.
- No generated outcome reports.

## 11. Viability Loop

Viability proof is the highest priority.

Detection alone is not enough. A watcher alone is not enough. The next step must start proving what happened after a setup appeared before SAFE-FAST can decide whether the trading plan works.

Required viability loop:

detect -> score outcome -> diagnose deeply -> analyze whole system -> decide fix path -> adjust rule/contract/test -> run regression -> review again

## 12. Diagnostics-Before-Optimization Rule

Diagnostics must come before optimization.

Shallow labels like failed setup, bad alert, weak signal, or bad trade are not enough. Diagnostics must identify evidence, likely cause, affected setup type, affected symbol when available, affected stage, trigger/invalidation/freshness relationship, affected system area, next fix path, and whether lower-tier handoff is required.

No threshold, ranking, trigger, invalidation, freshness, blocker/caution, or workflow optimization may be proposed until the diagnostic output identifies an evidence-backed rule, contract, or test gap.

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

Setup recognition, trigger, invalidation, fresh/stale/spent, blocker/caution, ranking/focus, outcome scoring, diagnostics, and user workflow should be rule-based.

## 14. Lower-Tier Handoff Requirement

If the outcome proof evaluator finds insufficient evidence, stale setup handling gaps, trigger/invalidation ambiguity, diagnostics gaps, or workflow ambiguity, the output must identify whether the issue requires lower-tier handoff before any higher-tier optimization or live-readiness step.

Lower-tier handoff means the next fix path must go back to the smallest responsible local contract, fixture, test, or planning layer before changing broader watcher behavior. It must not skip directly to live data, alerts, trading, account sizing, production, or optimization.

## 15. Boundary Statement

This docs-only plan does not start code work, optimization, controlled shadow data, live data, watcher loops, alerts, generated reports/logs, broker/order/account/options/P&L, account sizing, production/Railway/live backend work, or live trade decisions.

This docs-only plan does not modify `main.py`, engine logic, watcher code, tests, Railway/deploy files, secrets, `.env` files, credentials, tokens, deployment settings, generated output paths, report/log writers, watcher loops, alert delivery, broker/order/account behavior, options behavior, option P&L, position sizing, account sizing, or live trade decision logic.
