# SAFE-FAST Day 47 Risk Capital Rules Result

## Baseline

- Task file executed: `SAFE_FAST_DAY47_RISK_CAPITAL_RULES_CODEX_TASK.md`.
- Result document: `SAFE_FAST_DAY47_RISK_CAPITAL_RULES_RESULT.md`.
- Starting branch observed locally: `main`.
- Starting HEAD observed locally: `92a9cbc`.
- Local status before edits: clean by `git status --short --branch` except git reported permission warnings for temp directories `tmp2i57tguu`, `tmpj8ei9a_f`, `tmpra392qh0`, and `tmpt2fw63vq`.
- This was SAFE-FAST build-governance and rule-definition work only.

## Canonical Rule Document

`SAFE_FAST_PROJECT_PROOF_PIPELINE.md` is the exact canonical rule document for this package. It was updated instead of creating a duplicate authority because the consolidated audit named the proof pipeline and rule index as the canonical owners for risk, promotion, paper-validation, and live-readiness gates.

## Fixed

- Defined conservative risk and capital rules for:
  - maximum loss per trade;
  - maximum daily loss;
  - maximum weekly loss;
  - drawdown shutdown;
  - consecutive-loss limits;
  - concurrent-position limits;
  - de-risking and stop-after-failure behavior;
  - position sizing placeholders for development replay, protected holdout, controlled paper-validation planning, and live-review eligibility;
  - capital competition among simultaneous candidates;
  - missing, partial, breached, contradictory, or unverifiable risk evidence.
- Preserved all frozen/accepted Clean Fast Break trading and execution-realism rules:
  - long calls only;
  - entry from ask plus `0.02`;
  - exit from bid minus `0.02`;
  - `+25%` target;
  - `-15%` option stop;
  - setup invalidation stop;
  - same-day `15:45 ET` time exit;
  - `5` minute quote-age failure;
  - no zero-cost fills;
  - one primary failure reason;
  - one-contract CFB countability;
  - no-fallback selected-contract discipline.
- Stated required evidence, required regression cases, automatic failure conditions, current replay-output effect, and no-proof boundary for every risk/capital rule.
- Updated canonical control files so they agree on the active objective, canonical rule document, current defined/unproven state, and next grouped task.
- Added focused consistency tests in `tests/test_day47_risk_capital_rules.py`.

## Rule Status Summary

| Rule area | Status |
| --- | --- |
| Maximum loss per trade | Accepted for replay and protected-holdout governance. |
| Maximum daily loss | Provisional governance for replay, holdout, and paper planning. |
| Maximum weekly loss | Provisional governance for replay, holdout, and paper planning. |
| Drawdown shutdown | Provisional governance. |
| Consecutive-loss limits | Provisional governance. |
| Concurrent-position limits | Accepted for replay and holdout governance until portfolio rules exist. |
| De-risking and stop-after-failure behavior | Provisional governance. |
| Development replay sizing placeholder | Accepted for governance/countability only: `1` option contract maximum. |
| Protected holdout sizing placeholder | Accepted for holdout governance only: same `1` contract placeholder frozen before reveal. |
| Controlled paper-validation sizing placeholder | Blocked until a later paper task maps the placeholder to paper account value and broker/platform constraints. |
| Live-review sizing placeholder | Blocked until completed paper logs, broker/order rollback plan, and explicit human approval exist. |
| Capital competition among simultaneous candidates | Provisional governance until the next portfolio-interaction package. |
| Missing, partial, breached, or unverifiable risk evidence | Accepted failure/default behavior. |

## Existing Replay Output Treatment

- Existing CFB replay outputs remain review-only unless rerun or reclassified under the promotion ladder, candidate/contract freeze rules, execution-realism rules, this risk/capital package, the sample contract, and later portfolio-interaction rules.
- SPY CFB 002 remains the positive review-only anchor. It is not invalidated by this package because first-pass CFB countability already uses one contract and the known option-stop threshold bounds per-trade replay risk. It still does not become proof, profitability, readiness, paper eligibility, or live readiness.
- SPY CFB 003 remains `no_trade` / `quote_age_above_5_minutes`.
- QQQ CFB 001 remains `no_trade` / `quote_age_above_5_minutes`.
- No existing replay output becomes countable because complete daily/weekly ledgers, drawdown curves, concurrency records, capital-slot precedence, and portfolio interaction rules do not yet exist.

## Why Accepted/Frozen Rules Changed

- Risk and capital rules changed from missing to defined because the consolidated audit required maximum loss, position sizing, portfolio exposure, shutdown, consecutive-loss, de-risking, and capital competition rules before paper validation or more countable results.
- Maximum loss per trade was accepted for replay and protected-holdout governance because the existing first-pass CFB model already has one-contract sizing, entry basis, option stop, setup invalidation, time exit, and zero-cost rejection. The rule still blocks any result missing stop, invalidation, sizing placeholder, or exit boundary.
- Daily loss, weekly loss, drawdown, consecutive-loss, de-risking, and capital competition values are provisional governance assumptions because no account-size, broker, margin, or live order plan is accepted. They must be regression-tested and frozen before protected holdout or paper-planning use.
- Concurrent-position countability was set to one open option position because the repo has no portfolio interaction, duplicate exposure, correlation, or precedence rules yet.
- No accepted/frozen CFB trading or execution-realism rule changed. The package explicitly preserved entry, exit, target, stop, time-exit, quote-age, no-fallback, cost/slippage, size, and failure-reason discipline.

## Still Unproven

- Profitability.
- Paper-validation eligibility.
- Live readiness.
- Portfolio-level behavior.
- Protected holdout performance.
- Stable winner selection.
- Family repair, retirement, and invalidation thresholds.
- Replay-to-operational-engine equivalence.
- Account-size, broker, margin, buying-power, and live order risk behavior.

## Next

Exact next grouped task filename: `SAFE_FAST_DAY47_PORTFOLIO_INTERACTION_RULES_CODEX_TASK.md`.

This next task follows the ordered audit plan and must define portfolio and setup-family interaction rules before data-cost ledger, grouped replay/regression, family invalidation, and the Day 90 decision package.

## Guardrail Result

- `main.py` changed: NO.
- Railway/deploy, production, broker, order, account, credentials, `.env`, secrets changed: NO.
- Live trading logic changed: NO.
- Databento downloaded: NO.
- New backtest run: NO.
- New P&L calculated: NO.
- Proof/profitability/readiness/promotion/intake-ready claimed: NO.
