# SAFE-FAST Day 47 Promotion, Holdout, and Candidate-Freeze Rules Result

## Baseline

- Task file executed: `SAFE_FAST_DAY47_PROMOTION_HOLDOUT_AND_CANDIDATE_FREEZE_RULES_CODEX_TASK.md`.
- Result document: `SAFE_FAST_DAY47_PROMOTION_HOLDOUT_AND_CANDIDATE_FREEZE_RULES_RESULT.md`.
- Starting branch observed locally: `main`.
- Starting HEAD observed locally: `d23a343`.
- Local status before edits: clean except for the untracked current task file; git also reported permission warnings for temp directories `tmp2i57tguu`, `tmpj8ei9a_f`, `tmpra392qh0`, and `tmpt2fw63vq`.
- This was SAFE-FAST build-governance work only.

## Canonical Rule Document

`SAFE_FAST_PROJECT_PROOF_PIPELINE.md` is the exact canonical rule document for this package. It was updated instead of creating a duplicate authority because the consolidated audit named it as the proof and promotion pipeline owner.

## Fixed

- Defined the six-gate promotion ladder:
  - development evidence;
  - grouped replay eligibility;
  - regression acceptance;
  - protected-holdout evaluation;
  - controlled paper-validation eligibility;
  - paper-to-live review eligibility.
- Defined exactly four Day 90 outcomes:
  - `PAPER_VALIDATION_ELIGIBLE`;
  - `BOUNDED_REPAIR_REQUIRED`;
  - `NARROWED_PLAN`;
  - `REDESIGN_REQUIRED`.
- Defined exact sample-size and coverage minimums for Ideal, Clean Fast Break, and Continuation.
- Defined protected holdout manifest, exclusion, freeze, invalidation, replacement, and complete-reporting rules.
- Defined candidate and option-contract freeze rules requiring decision-time-only information and deterministic exclusion/tie-break records.
- Added compact operational decision tables.
- Updated canonical control files so they agree on the active objective, canonical rule document, current defined/unproven state, and next grouped task.
- Added focused consistency tests in `tests/test_day47_promotion_holdout_candidate_freeze_rules.py`.

## Exact Numerical Sample Contract

| Setup family | Accepted entries | Rejection/no-trade controls | Ambiguous or boundary cases | Winners | Losers | Protected holdout accepted entries | Protected holdout rejection/no-trade controls |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Ideal | 20 | 10 | 5 | 5 | 5 | 8 | 4 |
| Clean Fast Break | 20 | 10 | 5 | 5 | 5 | 8 | 4 |
| Continuation | 20 | 10 | 5 | 5 | 5 | 8 | 4 |

Coverage minimums per setup family:

| Coverage dimension | Exact minimum |
| --- | ---: |
| Major market regimes | 3 regimes: uptrend, downtrend, range/chop |
| Volatility conditions | 3 conditions: low, normal, high |
| Trend and chop | 2 trend examples and 2 chop examples beyond the major-regime count where separately labeled |
| Time-of-day periods | 3 periods: first 60 minutes, middle session, final 90 minutes |
| Weekdays | 5 weekdays, at least 2 examples each |
| Liquidity and spread conditions | 3 buckets: clean, caution, fail/reject |
| Symbols approved by plan | At least 2 approved symbols per active family unless a narrowed plan explicitly limits to 1 symbol with a rule-backed reason |
| Expirations approved by plan | At least 2 expiration buckets per active family: 14-21 DTE and 22-45 DTE, unless narrowed by accepted contract-selection rule |
| Developing-stage transitions | 5 examples covering watch, candidate, signal, spent/stale, and invalidated or blocked |
| Session-boundary cases | 3 cases: prior-session carry-forward, same-session reset, and next-session invalidation or block |

Clean Fast Break keeps the already accepted blocker below `20` valid completed CFB examples. The other numeric values are conservative governance assumptions and must be frozen before protected holdout evidence is opened.

## Why Accepted/Frozen Rules Changed

- Promotion gates changed from partially defined/missing to defined because the audit identified replay-to-paper and paper-to-live gates as missing and assigned the proof pipeline/rule index as canonical owners.
- Final outcomes changed from partially defined to exactly enumerated because the audit required falsifiable Day 90 outcomes and rejected open-ended continuation.
- Sample-size requirements changed from missing to defined because the audit required exact numerical coverage by family, outcome type, regime, volatility, time, weekday, liquidity/spread, symbol, expiration, stage transition, and session boundary.
- Protected holdout changed from missing to defined because the audit required untouched holdout selection, manifesting, anti-peeking, invalidation, replacement, and complete reporting before promotion-grade replay.
- Candidate and option-contract freeze changed from partially defined to defined because the audit required project-wide no-hindsight freeze records, deterministic exclusion reasons, and no retrospective best-contract selection.

## Still Unproven

- Profitability.
- Paper-validation eligibility.
- Live readiness.
- Stable winner selection.
- Portfolio-level behavior.
- Complete capital/risk plan.
- Holdout performance.
- Family repair, retirement, and invalidation thresholds.
- Replay-to-operational-engine equivalence.

## Next

Exact next grouped task filename: `SAFE_FAST_DAY47_CFB_EXECUTION_REALISM_RULES_CODEX_TASK.md`.

This next task follows the ordered audit plan and must define CFB execution realism before more countable results: latency, size, partial-fill, same-interval target/stop ordering, target-touch and stop-touch rules, while preserving current quote-age and no-fallback discipline.

## Guardrail Result

- `main.py` changed: NO.
- Railway/deploy, production, broker, order, account, credentials, `.env`, secrets changed: NO.
- Live trading logic changed: NO.
- Databento downloaded: NO.
- New backtest run: NO.
- New P&L calculated: NO.
- Proof/profitability/readiness/promotion/intake-ready claimed: NO.
