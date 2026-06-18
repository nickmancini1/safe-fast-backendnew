# SAFE-FAST Day 47 CFB Execution Realism Rules Result

## Baseline

- Task file executed: `SAFE_FAST_DAY47_CFB_EXECUTION_REALISM_RULES_CODEX_TASK.md`.
- Result document: `SAFE_FAST_DAY47_CFB_EXECUTION_REALISM_RULES_RESULT.md`.
- Starting branch observed locally: `main`.
- Starting HEAD observed locally: `613d253`.
- Local status before edits: clean by `git status --short --branch` except git reported permission warnings for temp directories `tmp2i57tguu`, `tmpj8ei9a_f`, `tmpra392qh0`, and `tmpt2fw63vq`.
- This was SAFE-FAST build-governance and rule-definition work only.

## Canonical Rule Document

`SAFE_FAST_PROJECT_PROOF_PIPELINE.md` is the exact canonical rule document for this package. It was updated instead of creating a duplicate authority because the consolidated audit and prior Day 47 package named it as the proof and promotion pipeline owner.

## Fixed

- Defined conservative Clean Fast Break execution-realism countability rules for:
  - signal-to-decision latency;
  - usable quote age;
  - one-contract order size and minimum quote size;
  - partial-fill blocking;
  - target-touch recognition;
  - stop-touch and setup-invalidation recognition;
  - same-interval target/stop ordering;
  - bid/ask/spread handling beyond the Day 45 first-pass values;
  - no-fallback selected-contract discipline;
  - missing, delayed, crossed, locked, zero, negative, wrong-symbol, wrong-instrument, unparsable, or malformed quote behavior.
- Preserved the accepted Day 45 first-pass CFB values:
  - long calls only;
  - entry from ask plus `0.02`;
  - exit from bid minus `0.02`;
  - `+25%` target;
  - `-15%` option stop;
  - setup invalidation stop;
  - same-day `15:45 ET` time exit;
  - no zero-cost fills;
  - one primary failure reason;
  - no promotion below `20` valid completed CFB examples.
- Preserved the current `5` minute stale-quote failure rule. QQQ CFB 001 and SPY CFB 003 remain no-trade controls with primary reason `quote_age_above_5_minutes` unless a later regression-backed rule explicitly narrows that behavior.
- Preserved no-fallback selected-contract discipline. A stale, missing, malformed, or failed top-ranked selected contract requires abstain/no-trade with one primary reason; the replay cannot scan to a later or better-performing contract.
- Stated required evidence, required regression cases, automatic failure conditions, current replay-output effect, and no-proof boundary for every accepted execution-realism rule.
- Updated canonical control files so they agree on the active objective, canonical rule document, current defined/unproven state, and next grouped task.
- Added focused consistency tests in `tests/test_day47_cfb_execution_realism_rules.py`.

## Rule Status Summary

| Rule area | Status |
| --- | --- |
| Signal-to-decision latency | Accepted for CFB countability governance. |
| Usable quote age | Accepted and frozen; quote age above `5` minutes fails. |
| Order size and minimum quote size | Accepted for first CFB countability pass; only `1` contract is countable. |
| Partial-fill behavior | Accepted as blocked-by-default for countable replay without exact fill evidence. |
| Target-touch recognition | Accepted for first CFB countability pass from selected-contract bid minus `0.02`. |
| Stop-touch recognition | Accepted for first CFB countability pass from selected-contract bid minus `0.02`; setup invalidation needs source-backed underlying evidence and option bid exit quote. |
| Same-interval target/stop ordering | Accepted conservative rule; earliest timestamp wins, same timestamp or unresolved interval is stop-first or ambiguous/review-only. |
| Bid/ask/spread handling | Accepted for first CFB countability pass with positive non-crossed quotes, entry ask plus `0.02`, exit bid minus `0.02`, entry spread no more than `0.15`, and entry spread percent no more than `2.00%` unless later regression-backed rule changes it. |
| No-fallback selected-contract discipline | Accepted and frozen. |
| Missing, delayed, crossed, locked, zero, or malformed quote behavior | Accepted failure/default behavior. |

## Existing Replay Output Treatment

- Existing CFB replay outputs remain review-only unless rerun or reclassified under this execution-realism package, candidate/contract freeze rules, sample contract rules, and later risk/capital rules.
- SPY CFB 002 remains the positive review-only anchor. It is not invalidated by this package because its known entry quote is setup-time-safe, positive bid/ask, sized for one contract, and compatible with the first-pass size rule. It still does not become proof, profitability, readiness, paper eligibility, or live readiness.
- SPY CFB 003 remains `no_trade` / `quote_age_above_5_minutes`.
- QQQ CFB 001 remains `no_trade` / `quote_age_above_5_minutes`.

## Why Accepted/Frozen Rules Changed

- CFB execution realism changed from missing to defined because the consolidated audit required latency, size, partial-fill, target/stop touch, same-interval ordering, bid/ask/spread, quote-age, no-fallback, and bad-quote behavior before more countable CFB results.
- The `5` minute quote-age failure rule did not change. It was explicitly preserved to prevent hindsight repair of stale-quote controls.
- No-fallback selected-contract discipline did not change. It was explicitly preserved to prevent retrospective best-contract selection.
- Day 45 entry, exit, target, stop, time-exit, cost/slippage, zero-cost, primary-reason, sample-size, and promotion blockers did not change. They were restated as dependencies so the new execution-realism section cannot be mistaken for proof or readiness.
- Spread and size requirements were made explicit for countability because the audit identified execution realism as incomplete. They do not retroactively promote or invalidate review-only outputs.
- Partial fills were blocked by default because the repo has no exact fill-log rule or evidence.

## Still Unproven

- Profitability.
- Paper-validation eligibility.
- Live readiness.
- Complete risk and capital plan.
- Portfolio-level behavior.
- Protected holdout performance.
- Stable winner selection.
- Family repair, retirement, and invalidation thresholds.
- Replay-to-operational-engine equivalence.

## Next

Exact next grouped task filename: `SAFE_FAST_DAY47_RISK_CAPITAL_RULES_CODEX_TASK.md`.

This next task follows the ordered audit plan and must define capital allocation and risk-plan rules before portfolio interaction, data-cost ledger, grouped replay/regression, family invalidation, and the Day 90 decision package.

## Guardrail Result

- `main.py` changed: NO.
- Railway/deploy, production, broker, order, account, credentials, `.env`, secrets changed: NO.
- Live trading logic changed: NO.
- Databento downloaded: NO.
- New backtest run: NO.
- New P&L calculated: NO.
- Proof/profitability/readiness/promotion/intake-ready claimed: NO.
