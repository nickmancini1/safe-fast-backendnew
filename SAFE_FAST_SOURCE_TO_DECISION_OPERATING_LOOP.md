<!-- SAFE_FAST_PRIORITY_DRIFT_GATE_BEGIN -->
## SAFE-FAST PRIORITY DRIFT GATE

This is the top red-flag gate. Every future chat must answer it before any baseline, explanation, or command.

Priority check: Am I efficiently working on the current priority task and not drifting?

Required answer format:
- Priority check: YES or NO.
- Current priority: one sentence.
- This step is: Substance or busy work.
- Why allowed: one sentence.
- If NO: stop and correct before giving a command.

Substance means the step directly moves SAFE-FAST toward one of: cost approval, vendor-ready request, contract selection, option evidence, entry/exit/P&L, exact rejection, exact blocker closure, or regression protection.

Busy work means another worksheet, task file, broad scan, handoff tweak, stale-output cleanup, or documentation update that does not unlock the current priority.

Hard rule: Busy work is forbidden unless current `git status --short` proves it physically blocks the priority task.

Top red flag: if the assistant cannot explain in one sentence how the next command advances the current priority, it must not give the command.
<!-- SAFE_FAST_PRIORITY_DRIFT_GATE_END -->


# SAFE-FAST Source-To-Decision Operating Loop

This is the mandatory source-to-decision and anti-rabbit-hole operating contract for every SAFE-FAST chat.

## Required Opening Report

Required opening report:

Every new chat or resumed task must begin from repo state and report:

- Baseline: branch, HEAD, git status, current build-state checkpoint.
- Active objective: the one current objective from `SAFE_FAST_BUILD_STATE.md`.
- Raw-data source: exact source, dataset/schema/API, file, timestamp window, and credential boundary if relevant.
- SAFE-FAST translation required: what SAFE-FAST must calculate from raw evidence.
- Blocker category: one category from the list below.
- Candidate state: funnel location and whether the candidate is strong enough for deeper work.
- Next executable step: the smallest command, edit, validator, test, or review that advances the active objective.
- Why this is the fastest safe path: one concrete sentence tied to evidence, code, tests, or economic result.
- Required tests: focused tests, affected regressions, validators, safe checks, and diff check.
- Commit proof: exact commit when committing is authorized; otherwise state that uncommitted accepted work is unfinished.

## One Active Objective

Do not replace, broaden, or abandon the active objective unless a completed result or hard blocker exists.

A direction change must name the blocker category and the smallest replacement action. Do not use open-ended "move forward" behavior.

## Blocker Categories

- `RAW_DATA_GAP`
- `RULE_DEFINITION_GAP`
- `CALCULATOR_OR_IMPLEMENTATION_GAP`
- `CANDIDATE_QUALITY_GAP`
- `ECONOMIC_EVIDENCE_GAP`
- `REGRESSION_OR_PROOF_GAP`

## Source Ownership

- Databento supplies primary raw historical underlying and option evidence.
- tastytrade/dxLink is secondary raw data only.
- official agencies / ALFRED supply macro and event facts.
- Schwab is future live-data and broker/account/order authority after access approval.
- SAFE-FAST alone calculates setup identity, trigger, invalidation, freshness, stale/spent, blocker, stage, winner, no-trade, entry, exit, and profitability-related decisions.
- Vendors provide evidence; SAFE-FAST provides labels and decisions.

## Candidate Funnel

Use this order:

1. Scan a broad bounded pool.
2. Run a fast field screen.
3. Remove duplicates and known structural blockers.
4. Rank by completeness.
5. Deep-review the strongest batch only.
6. Drop or replace weak candidates quickly.
7. Do one-candidate work only when the candidate is complete enough for economic proof.

## No Documentation Loop

No-documentation-loop rule: no new review, plan, status, or handoff may merely restate a known blocker.

Do not create a new review, plan, status, or handoff merely restating a known blocker.

Documentation is allowed only when it establishes a decision, closes a contradiction, defines a testable contract, records a completed result, repairs canonical handoff, or enables the immediate executable step.

## PowerShell / Codex Freeze Recovery

If waiting for hidden input, enter it.

If not waiting for input and output stops, press Ctrl+C once. Do not rerun.

Inspect exit status, logs, partial files, checkpoint manifest, sizes, hashes, parseability, Git status, and whether the step already completed.

Rerun only for a specific verified missing or failed result.

Never repeat paid requests, completed vendor schemas, Codex tasks, test batches, or downloads merely because terminal output was quiet.

## Build, Test, Commit

Required completion path when edits are authorized:

- focused tests;
- affected regressions;
- validators;
- safe checks;
- `git diff --check`;
- exact commit when commit is authorized;
- empty git status when commit is authorized.

Uncommitted accepted work is unfinished work.

## Red-Flag Stop Conditions

Stop and diagnose when:

- the same blocker repeats twice;
- more data is proposed when a rule or implementation is missing;
- one candidate is repeatedly reviewed without advancing;
- there is more documentation than evidence, code, tests, or economic results;
- canonical docs contradict machine-readable results;
- the active objective cannot be explained in one sentence.

## Progress Metrics

Measure progress with:

- complete economic replays;
- valid entries;
- exact rejections/no-trades;
- exits and net P&L;
- blockers permanently closed;
- candidates screened versus promoted;
- tests passed;
- clean commits.

## Final Question

Is this task moving SAFE-FAST closer to a tested profitable trading plan, or only making it sound more sophisticated?
