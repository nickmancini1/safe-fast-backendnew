# SAFE-FAST Day 47 Grouped CFB Selected-Contract Download — Codex Task

## Authority and baseline

Read `SAFE_FAST_BUILD_STATE.md` before doing anything else.

Then read:

1. `SAFE_FAST_PROJECT_DASHBOARD.md`
2. `SAFE_FAST_PROJECT_RULE_INDEX.md`
3. `SAFE_FAST_DAY47_GROUPED_CFB_EXPANSION_DATA_NEEDED_PLAN.md`
4. `SAFE_FAST_DAY47_NEXT_GROUPED_DATA_NEEDED_COST_CHECK_RESULT.md`
5. The task that produced that result

Expected starting baseline:

- branch: `main`
- commit: `5a818d8`
- user approval: grouped selected-contract download approved
- approved checked total: `$0.002986669541`
- setup-window subtotal: `$0.002226263285`
- conditional exit-path subtotal: `$0.000760406256`

The successful checked request uses:

- dataset: `OPRA.PILLAR`
- symbology: `raw_symbol`
- selected contract: `SPY   260429C00700000`

The earlier `instrument_id=1333784938` request returned Databento
`422 symbology_invalid_request`. Do not substitute that failed request for the
working `raw_symbol` request.

## Active objective

Download only the already approved grouped selected-contract evidence defined
by the committed plan and cost-check result.

This is build/replay evidence work, not live trade evaluation.

Do not modify engine logic, the frozen baseline, production, Railway,
`main.py`, broker code, account code, order code, credentials, `.env`, or
deployment files.

## Preflight requirements

1. Verify branch and commit.
2. Permit only this task file as the expected pre-existing uncommitted file.
3. Stop if any unrelated tracked or untracked files exist.
4. Confirm the Databento credential is available without printing it.
5. Repeat the exact cost check immediately before download.
6. Proceed only when:
   - the request shape still matches the committed approved request; and
   - total checked cost is no more than `$0.01`.
7. If the request changes or exceeds `$0.01`, perform no download and report
   the blocker.
8. Never print, store in documentation, or commit an API key or secret.

## Exact download scope

Use the exact schemas, timestamps, timezones, setup window, and separated
conditional exit-path windows already defined by the committed plan and
cost-check result.

Required grouped evidence includes the approved setup-window requests for:

- `tcbbo`
- `trades`
- `statistics`

Keep conditional exit-path windows separate exactly as already planned.

Do not broaden:

- symbols
- contracts
- schemas
- time windows
- expirations
- candidate count
- setup families

Use existing project download utilities and the existing ignored local raw-data
location. Do not create a competing data layout when a canonical one already
exists.

Raw Databento data must remain local and ignored by git.

## Download validation and reproducibility

For every downloaded request, record without exposing secrets:

- dataset
- schema
- `raw_symbol`
- start and end timestamp
- timezone interpretation
- request purpose
- returned file path
- byte size
- record or row count when available
- SHA-256 checksum
- Databento request identifier when available
- checked cost immediately before download
- actual billed cost when available
- download timestamp
- missing, empty, delayed, or malformed-data findings

Verify that:

- expected files exist;
- setup and conditional exit windows remain separated;
- files are readable by existing project tooling;
- expected schemas are identifiable;
- raw files remain ignored and unstaged;
- no credential appears in output or tracked files.

Do not claim evidence is complete merely because a file exists. State any
coverage limitation explicitly.

## Required tracked outputs

Create one download-result document following current repository naming and
documentation conventions.

Update:

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_PROJECT_DASHBOARD.md`
- `SAFE_FAST_PROJECT_RULE_INDEX.md`

The three control files must agree on:

- exact baseline commit;
- what was downloaded;
- what was validated;
- what remains unproven;
- exact blocker, if any;
- one exact next task filename.

If the download succeeds, prepare one exact next task for grouped replay and
backtest of the downloaded selected-contract evidence. Reuse an existing
canonical task if one exists; otherwise create one task using the repository's
current Day 47 naming convention. Do not create competing next-task files.

## Mandatory queued audit and completion-plan consolidation

The user's full Day 47-to-Day 90 audit requirement must be preserved explicitly
in the repository and must not be lost in a future chat.

Find any existing canonical document or task covering this scope. Consolidate
into it rather than duplicating it. If no equivalent canonical task exists,
create:

`SAFE_FAST_DAY47_TO_DAY90_CONSOLIDATED_AUDIT_AND_COMPLETION_PLAN_CODEX_TASK.md`

Queue it as mandatory immediately after the current grouped data/replay path.

That future audit must inspect the full repo, remove redundancy and
contradictions, identify one canonical owner for every rule, and classify each
requirement as:

- defined
- partially defined
- missing
- contradictory
- proven by tests

Its mandatory scope includes every item below:

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
12. Falsifiable final outcomes:
    - paper-validation eligible
    - bounded repair
    - narrowed plan
    - redesign
13. Candidate-selection and hindsight bias.
14. Look-ahead and future-information leakage.
15. Deterministic option-contract selection at signal time.
16. Objective and reproducible setup labeling.
17. Missing-data and delayed-data behavior.
18. Replay-to-operational-engine equivalence.
19. Incremental developing-stage transition correctness.
20. Session-boundary carry-forward and reset behavior.
21. False-positive and false-negative no-trade measurement.
22. Realistic bid, ask, spread, quote-age, latency, slippage, size,
    partial-fill, target-touch, stop-touch, and same-interval ordering rules.
23. Market-regime, volatility, liquidity, time-of-day, weekday, symbol,
    expiration, accepted, rejected, ambiguous, winning, and losing coverage.
24. Overlapping signals, setup evolution, duplicate exposure, correlation,
    candidate precedence, and capital competition.
25. Maximum loss per trade, daily and weekly loss limits, drawdown shutdowns,
    consecutive-loss limits, concurrent-position limits, and de-risking rules.
26. Exact criteria for repairing, narrowing, replacing, or removing a family.
27. Exact criteria that invalidate a family.
28. One-command or otherwise repeatable replay and regression workflow.
29. Data-cost ledger and decision value for every purchase.
30. What can be maintained on the `$20` tier and what requires major spending.
31. A clear statement of what has actually been proven versus inferred.
32. Exact tests protecting each accepted behavior.
33. Full future-chat continuity and anti-restart controls.

Future-chat continuity must require every new chat to:

- verify local branch, commit, and status;
- read `SAFE_FAST_BUILD_STATE.md` first;
- read the canonical dashboard and rule index;
- identify the exact active objective and task;
- stop on file disagreement;
- continue the existing task without restarting discovery;
- never make the user explain completed work;
- never invent a new task when the repo already names one;
- report Baseline, Fixed, Blocked, Next, Tests, and Files Changed;
- detect stale commits, stale task references, duplicate task ownership, and
  contradictory control files automatically;
- preserve strict no-trade discipline;
- never confuse build work with live trade evaluation.

The audit must produce one consolidated prioritized completion plan, not
scattered essays or duplicate task files.

## Tests

Run all existing safe checks and both current evidence validators.

If direct PowerShell execution is blocked by local execution policy, use the
existing process-level bypass method and report both the direct result and the
successful bypass result accurately.

Run focused validation for any new manifest or documentation consistency logic.

Run `git diff --check`.

Do not commit or push.

## Final Codex summary

Return only a concise final summary containing:

- Baseline
- Fixed
- Blocked
- Next
- Tests
- Tracked files changed
- Ignored raw files downloaded
- Exact pre-download checked cost
- Actual billed cost, or `NOT_AVAILABLE`
- Exact next replay task filename
- Exact queued consolidated-audit task filename
