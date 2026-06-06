# SAFE-FAST Local Next-Step Plan After Controlled Sample Coverage Review

## 1. Purpose

Plan the smallest next controlled sample gap after the controlled sample coverage review.

The coverage review showed that the current four-sample controlled set is useful at tiny-sample known-limits depth, but it no longer contains an active inconclusive or missing-evidence sample. The next step should restore that proof path before broader setup-type-plus-symbol pair expansion.

This is a docs-only plan. It does not start code work, tests, live data, controlled shadow data, watcher loops, alerts, generated reports/logs, broker/order/account/options/P&L, account sizing, optimization, production work, Railway/deploy work, or live trade decisions.

## 2. Day 34 Context

- **Baseline:** patch8.
- **Repo:** `safe-fast-backendnew`.
- **Branch:** `main`.
- **Current working day context:** Day 34.
- **Day 33 status:** historical context.
- **Latest commit before this plan:** `ca8b6a4 Add controlled sample coverage review`.
- **Work mode:** build work only, not live trade chat.
- **Highest priority:** viability proof before optimization.
- **Profitability status:** profitability and actual historical success are still unproven.
- **Current objective:** use the controlled sample coverage review to choose the next smallest evidence-backed controlled sample gap.

## 3. What The Coverage Review Showed

The controlled sample coverage review found:

- all four starting symbols are represented at least once: `GLD`, `IWM`, `QQQ`, and `SPY`
- all three setup types are represented at least once: `Clean Fast Break`, `Continuation`, and `Ideal`
- worked chart/setup behavior is represented
- failed chart/setup behavior with useful diagnosis is represented
- active inconclusive or missing-evidence coverage is not represented
- eight setup-type-plus-symbol pairs are still missing
- upstream bundle readiness still has tiny-sample and review-contract gaps
- the current set is useful for the next proof review at known-limits depth, but it is not final viability proof or final lower-tier readiness

## 4. What Is Represented Now

Current represented pairs:

- `Ideal` / `SPY`: worked chart/setup behavior.
- `Clean Fast Break` / `QQQ`: failed chart/setup behavior with useful diagnosis.
- `Continuation` / `GLD`: worked/reviewable chart/setup behavior.
- `Ideal` / `IWM`: worked/reviewable chart/setup behavior.

Current outcome coverage:

- worked: represented
- failed: represented
- inconclusive: absent
- missing evidence: absent

## 5. What Is Still Missing

Missing setup-type-plus-symbol pairs:

- `Clean Fast Break` / `SPY`
- `Continuation` / `SPY`
- `Ideal` / `QQQ`
- `Continuation` / `QQQ`
- `Clean Fast Break` / `IWM`
- `Continuation` / `IWM`
- `Ideal` / `GLD`
- `Clean Fast Break` / `GLD`

Missing outcome/contract coverage:

- one active inconclusive controlled sample
- one active missing-evidence controlled sample, or one sample that clearly exposes unavailable after-setup evidence
- proof that the review path still names exact unavailable fields without fabricating evidence
- proof that the next fix path and regression need remain explicit when evidence is incomplete
- final lower-tier bundle readiness

## 6. Smallest Next Evidence-Backed Gap

The smallest next evidence-backed gap is:

Add or preserve exactly one explicit inconclusive or missing-evidence controlled sample in the local in-memory controlled sample path.

Preferred smallest shape:

- one controlled sample only
- in-memory fixture input only
- no live data and no controlled shadow data
- no generated reports/logs
- setup-time evidence remains separate from after-setup evidence
- after-setup evidence is deliberately unavailable or incomplete in a source-backed way
- missing field names are explicit, such as `source_row_reference` or `post_setup_evidence`
- outcome remains `inconclusive`, `missing_evidence`, or `unavailable_evidence`
- review output must surface the sample as active missing-evidence/inconclusive coverage

## 7. Why This Gap Is Next

This gap is next because symbol coverage and setup-type coverage are already present at least once, and worked/failed behavior is already represented. Broad pair expansion would add width, but it would not prove that the chain can still handle unavailable evidence after GLD and IWM both became reviewable.

A single explicit inconclusive/missing-evidence sample is the smallest responsible next step because it tests the proof chain's most important safety behavior:

- do not fabricate missing after-setup evidence
- do not use future data to define the original setup
- do not turn incomplete evidence into a worked or failed claim
- do not optimize or change rules to hide the gap
- preserve exact missing field names
- name a next fix path and regression need

## 8. Future Implementation File Scope Allowed

If the user later approves implementation, allowed future file scope should be limited to:

- `watcher_foundation/setup_outcome_historical_sample_path.py`
- `tests/test_setup_outcome_historical_sample_path.py`
- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`

The future implementation should not touch `main.py`, engine logic, Railway/deploy files, production/live backend files, live-data paths, controlled-shadow paths, watcher loops, alerts, generated report/log writers, broker/order/account/options/P&L behavior, account sizing, secrets, env files, or GitHub.

## 9. Required Future Tests

If implementation is later approved, required tests should be focused and evidence-backed:

- assert the controlled sample set contains exactly one active inconclusive or missing-evidence sample
- assert worked and failed samples remain represented
- assert setup type, symbol, and setup-type-plus-symbol pair separation remain true
- assert setup-time evidence and after-setup evidence remain separated
- assert unavailable fields are explicit and not fabricated
- assert the review output exposes missing-evidence/inconclusive coverage
- assert the smallest next fix path prefers collecting or preserving missing after-setup evidence when that gap exists
- assert no final viability, profitability, historical success, live readiness, production readiness, rule-change, or optimization claim appears
- assert no file/network/subprocess/thread/live/broker side effects occur

Expected focused command for the future implementation step:

`python -m unittest discover -s tests -p test_setup_outcome_historical_sample_path.py`

Additional regression commands may be added only if the implementation touches shared proof-chain behavior. This docs-only plan does not run tests.

## 10. What Still Remains Unproven

Still unproven:

- final trading-plan viability
- profitability
- actual historical success
- broad setup-type-plus-symbol coverage
- final lower-tier readiness
- controlled shadow readiness
- live data readiness
- alert readiness
- generated report/log readiness
- broker/order execution
- option P&L
- account sizing
- production readiness
- Railway/deploy readiness
- live backend readiness
- live trade decisions

Worked or failed chart/setup behavior still does not mean profitable.

## 11. Validation For This Docs-Only Plan

Required validation for this docs-only task:

- do not run unit tests
- run `git diff --check`

The closeout should report files changed, plan summary, smallest next gap chosen, tests not run because docs-only, `git diff --check` result, git status, and whether the work is ready for assistant review before commit.

## 12. Boundary Statement

This plan is build-only documentation. It does not authorize code changes by itself.

No code changes, no tests changed, no `main.py`, no engine logic, no Railway/deploy, no production/live backend, no live data, no controlled shadow data, no watcher loops, no alerts, no generated reports/logs, no broker/order/account/options/P&L, no account sizing, no live trade decisions, no secrets or env files, no GitHub writes, and no commits are included in this task.
