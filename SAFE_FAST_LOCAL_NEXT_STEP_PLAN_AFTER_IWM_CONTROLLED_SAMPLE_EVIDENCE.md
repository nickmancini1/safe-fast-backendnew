# SAFE-FAST Local Next-Step Plan After IWM Controlled Sample Evidence

## 1. Purpose

Plan the next docs-only controlled sample coverage review after the IWM controlled sample expansion.

The current controlled sample set now includes:

- worked `Ideal` / `SPY`
- failed `Clean Fast Break` / `QQQ`
- worked/reviewable `Continuation` / `GLD`
- worked/reviewable `Ideal` / `IWM`

The next build step should review what this four-symbol controlled starting universe proves, what it does not prove, which setup-type-plus-symbol pairs are represented, which pairs are still missing, whether outcome coverage is broad enough for the next proof review, and the smallest evidence-backed gap to fix next.

This plan is docs-only. It does not start code work, tests, live data, controlled shadow data, watcher loops, alerts, generated reports/logs, broker/order/account/options/P&L, account sizing, optimization, production work, or live trade decisions.

## 2. Day 34 Context

- **Baseline:** patch8.
- **Repo:** `safe-fast-backendnew`.
- **Branch:** `main`.
- **Current working day context:** Day 34.
- **Day 33 status:** historical context.
- **Latest commit before this plan:** `7cc424c Add IWM controlled sample evidence`.
- **Work mode:** build work only, not live trade chat.
- **Highest priority:** viability proof before optimization.
- **Profitability status:** profitability and historical success are still unproven.
- **Current objective:** plan the next controlled sample coverage review after IWM became represented and reviewable.

## 3. Fixed Inputs To Review

The future review must use the current controlled sample set as the fixed input:

- `Ideal` / `SPY`: worked chart/setup behavior sample.
- `Clean Fast Break` / `QQQ`: failed chart/setup behavior sample with useful diagnosis.
- `Continuation` / `GLD`: worked/reviewable chart/setup behavior sample after the GLD evidence fix.
- `Ideal` / `IWM`: worked/reviewable chart/setup behavior sample after the IWM expansion.

The future review must not rewrite samples, add samples, change setup labels, change outcomes, optimize rules, or combine symbols/setup types to hide gaps.

## 4. Exact Next Review Step

Create a narrow controlled sample coverage review.

The future review should answer:

- Which symbols are represented?
- Which setup types are represented?
- Which setup-type-plus-symbol pairs are represented?
- Which setup-type-plus-symbol pairs are still missing?
- Does the sample set cover worked, failed, and inconclusive or missing-evidence cases?
- Is the sample set useful enough for the next proof review?
- What is the smallest next evidence-backed gap to fix?

The review should stay local-only and evidence-backed. It should inspect the current sample path output and output review shape, not live data, generated reports, controlled shadow data, broker/account data, or production paths.

## 5. Expected Coverage Matrix

Starting symbols:

- `SPY`
- `QQQ`
- `IWM`
- `GLD`

Setup types:

- `Ideal`
- `Clean Fast Break`
- `Continuation`

Currently represented pairs:

- `Ideal` / `SPY`
- `Clean Fast Break` / `QQQ`
- `Continuation` / `GLD`
- `Ideal` / `IWM`

Currently missing pairs:

- `Clean Fast Break` / `SPY`
- `Continuation` / `SPY`
- `Ideal` / `QQQ`
- `Continuation` / `QQQ`
- `Clean Fast Break` / `IWM`
- `Continuation` / `IWM`
- `Ideal` / `GLD`
- `Clean Fast Break` / `GLD`

The future review should verify this matrix from the actual controlled sample output rather than treating this plan as proof.

## 6. Outcome Coverage Questions

The future review should preserve this distinction:

- Worked chart/setup behavior is represented by `Ideal` / `SPY`, `Continuation` / `GLD`, and `Ideal` / `IWM`.
- Failed chart/setup behavior is represented by `Clean Fast Break` / `QQQ`.
- Inconclusive or missing-evidence coverage is not currently represented in the final four-sample controlled set after GLD and IWM became reviewable.

The review should decide whether the lack of an active inconclusive/missing-evidence sample is acceptable for the next proof review, or whether the smallest next gap is to add or preserve one explicit missing-evidence/inconclusive sample before broader coverage.

## 7. Usefulness Decision Rule

The future review should classify the sample set as one of:

- useful for next proof review at tiny-sample known-limits depth
- useful but missing explicit inconclusive/missing-evidence coverage
- not useful enough because setup-type, symbol, pair, outcome, no-hindsight, diagnostic, or lower-tier review material is incomplete

The review must not claim final viability, historical success, profitability, optimization readiness, controlled shadow readiness, live readiness, production readiness, Railway readiness, or live trade readiness.

## 8. Smallest Next Gap Rule

The future review must name one smallest next evidence-backed gap.

Candidate gap types include:

- missing active inconclusive/missing-evidence coverage in the controlled sample set
- missing setup-type-plus-symbol pair coverage
- weak or missing diagnosis for a failed sample
- weak lower-tier review summary
- upstream bundle-readiness contract gap at tiny-sample depth

The chosen gap must be based on the current controlled sample output, not preference, tuning, or broad expansion pressure.

## 9. Allowed Files For The Future Review Step

Allowed future review files:

- one new docs-only review file, name to be chosen by the next task
- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`

No code, tests, fixtures, runner changes, generated reports/logs, live-data files, controlled-shadow files, `main.py`, engine logic, Railway/deploy files, secrets, or env files are allowed unless the user explicitly expands scope.

## 10. Validation For The Future Review Step

The future step is docs-only unless explicitly changed by the user.

Required validation:

- do not run unit tests
- run `git diff --check`

The future closeout should report files changed, whether only allowed docs files changed, plan/review summary, tests not run because docs-only, `git diff --check` result, git status, and whether the work is ready for assistant review before commit.

## 11. Boundary Statement

This docs-only plan does not start code work, tests, optimization, controlled shadow data, live data, watcher loops, alerts, generated reports/logs, broker/order/account/options/P&L, account sizing, production/Railway/live backend work, or live trade decisions.

This docs-only plan does not modify `main.py`, engine logic, watcher code, tests, Railway/deploy files, secrets, `.env` files, credentials, tokens, deployment settings, generated output paths, report/log writers, watcher loops, alert delivery, broker/order/account behavior, options behavior, option P&L, position sizing, account sizing, or live trade decision logic.
