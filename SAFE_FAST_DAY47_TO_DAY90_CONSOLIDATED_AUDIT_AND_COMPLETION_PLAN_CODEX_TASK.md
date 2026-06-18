# SAFE-FAST Day 47 To Day 90 Consolidated Audit And Completion Plan Codex Task

## Authority

This task is mandatory immediately after the current grouped data/replay path.

Read `SAFE_FAST_BUILD_STATE.md` before doing anything else.

Then read:

1. `SAFE_FAST_PROJECT_DASHBOARD.md`
2. `SAFE_FAST_PROJECT_RULE_INDEX.md`
3. the latest grouped CFB data/replay result documents
4. existing handoff, dashboard, rule, proof, promotion, evidence, and candidate documents needed to audit ownership and contradictions

## Objective

Inspect the full repo, remove redundancy and contradictions, identify one canonical owner for every rule, and produce one consolidated prioritized completion plan.

Do not create scattered essays or duplicate task ownership.

## Mandatory classifications

For every audited requirement, classify the current repo state as one of:

- `defined`
- `partially_defined`
- `missing`
- `contradictory`
- `proven_by_tests`

## Mandatory scope

The audit must cover:

1. Numerical profitability contract.
2. Replay-to-paper and paper-to-live promotion gates.
3. Protected untouched holdout evidence.
4. Deterministic conservative options execution model.
5. Capital allocation and complete risk plan.
6. Evidence-sample coverage contract.
7. Repair-cycle limits and setup-family retirement rules.
8. Exact data and result reproducibility.
9. Economically sound stable-winner selection.
10. Day 90 operational and decision package.
11. Portfolio-level and setup-family interaction testing.
12. Falsifiable final outcomes: paper-validation eligible, bounded repair, narrowed plan, redesign.
13. Candidate-selection and hindsight bias.
14. Look-ahead and future-information leakage.
15. Deterministic option-contract selection at signal time.
16. Objective and reproducible setup labeling.
17. Missing-data and delayed-data behavior.
18. Replay-to-operational-engine equivalence.
19. Incremental developing-stage transition correctness.
20. Session-boundary carry-forward and reset behavior.
21. False-positive and false-negative no-trade measurement.
22. Realistic bid, ask, spread, quote-age, latency, slippage, size, partial-fill, target-touch, stop-touch, and same-interval ordering rules.
23. Market-regime, volatility, liquidity, time-of-day, weekday, symbol, expiration, accepted, rejected, ambiguous, winning, and losing coverage.
24. Overlapping signals, setup evolution, duplicate exposure, correlation, candidate precedence, and capital competition.
25. Maximum loss per trade, daily and weekly loss limits, drawdown shutdowns, consecutive-loss limits, concurrent-position limits, and de-risking rules.
26. Exact criteria for repairing, narrowing, replacing, or removing a family.
27. Exact criteria that invalidate a family.
28. One-command or otherwise repeatable replay and regression workflow.
29. Data-cost ledger and decision value for every purchase.
30. What can be maintained on the `$20` tier and what requires major spending.
31. A clear statement of what has actually been proven versus inferred.
32. Exact tests protecting each accepted behavior.
33. Full future-chat continuity and anti-restart controls.

## Future-chat continuity requirements

The audit must require every new chat to:

- verify local branch, commit, and status;
- read `SAFE_FAST_BUILD_STATE.md` first;
- read the canonical dashboard and rule index;
- identify the exact active objective and task;
- stop on file disagreement;
- continue the existing task without restarting discovery;
- never make the user explain completed work;
- never invent a new task when the repo already names one;
- report Baseline, Fixed, Blocked, Next, Tests, and Files Changed;
- detect stale commits, stale task references, duplicate task ownership, and contradictory control files automatically;
- preserve strict no-trade discipline;
- never confuse build work with live trade evaluation.

## Guardrails

- Do not modify `main.py`.
- Do not touch Railway, production, broker, order, account, credentials, `.env`, or secrets.
- Do not patch live trading logic.
- Do not download Databento data.
- Do not run new backtests unless a latest grouped replay task explicitly requires a read-only result check.
- Do not claim proof, profitability, readiness, promotion, or intake-ready status unless existing accepted evidence and tests already prove it.

## Required output

Create one consolidated audit and prioritized completion-plan result document using the repository naming convention.

Update:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`

The result must name one canonical owner for each rule area, list contradictions to resolve, name duplicate or superseded docs, and produce one ordered completion plan from Day 47 through Day 90.

## Tests

Run:

1. `.\scripts\safe_fast_run_safe_checks.ps1`
2. If direct PowerShell execution is blocked, rerun with `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`
3. `python -m watcher_foundation.source_evidence_work_package_content_validator`
4. `python -m watcher_foundation.source_evidence_package_to_intake_bridge`
5. focused documentation consistency checks added by this task
6. `git diff --check`

Do not commit or push.

## Final response format

Return:

- Baseline
- Fixed
- Blocked
- Next
- Tests
- Files changed
