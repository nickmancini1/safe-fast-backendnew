# SAFE-FAST Rule Decision Survival Map

## Scope

This is the final Day 39 build-only survival map after applying the Continuation, Ideal, Clean Fast Break, intrabar ordering, and context/caution rule-family decisions.

This is not proof review. It does not accept proof, claim profitability, authorize live data, authorize alerts, authorize broker/order/account work, authorize Railway/deploy work, or authorize changes to `main.py`.

Proof accepted: NO.

Profitability claim made: NO.

Current intake-ready count: 0.

## Decision Coverage

All 9 rule-family decisions from `SAFE_FAST_RULE_FAMILY_DECISION_TABLE.md` are applied:

- Clean Fast Break expiry: `SOURCE_DATA_INSUFFICIENT`.
- Clean Fast Break gap context: `SOURCE_DATA_INSUFFICIENT`.
- Continuation next-session freshness: `KILL_OR_NARROW_SETUP_SYMBOL_PATH`.
- Continuation session-boundary freshness: `KILL_OR_NARROW_SETUP_SYMBOL_PATH`.
- Ideal stale/spent expiry: `SOURCE_DATA_INSUFFICIENT`.
- Ideal fast-swing freshness: `KILL_OR_NARROW_SETUP_SYMBOL_PATH`.
- Intrabar ordering: `KILL_OR_NARROW_SETUP_SYMBOL_PATH`.
- Wide-risk / room threshold: `KILL_OR_NARROW_SETUP_SYMBOL_PATH`.
- Context/caution review: `SOURCE_DATA_INSUFFICIENT`.

Decision counts:

- `DEFINE_FROM_REPO_EVIDENCE`: 0.
- `SOURCE_DATA_INSUFFICIENT`: 4.
- `KILL_OR_NARROW_SETUP_SYMBOL_PATH`: 5.

## Survival Summary

- Strict rows covered: 7.
- `active_blocked`: 4.
- `replace`: 3.
- `parked`: 0.
- `intake_ready`: 0.
- Proof allowed rows: 0.

## Survival Map

| Candidate ID | Symbol | Setup type | Current status | Blocking rule family | Rule decision applied | Exact reason | Next evidence fix | Proof allowed |
|---|---|---|---|---|---|---|---|---|
| `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | QQQ | Clean Fast Break | `active_blocked` | Clean Fast Break expiry; Clean Fast Break gap context; Context/caution review | `SOURCE_DATA_INSUFFICIENT`; `SOURCE_DATA_INSUFFICIENT`; `SOURCE_DATA_INSUFFICIENT` | Gap-context, Clean Fast Break expiry, and complete context/caution source-backed evidence are insufficient; `final_verdict=TRADE` and primary blocker null cannot promote. | Add source-backed QQQ gap-context evidence, define a tested Clean Fast Break expiry rule, and add complete context/caution review fields before proof review. | NO |
| `QQQ-REAL-HISTORICAL-CONTINUATION-001` | QQQ | Continuation | `replace` | Continuation next-session freshness; Continuation session-boundary freshness; Context/caution review | `KILL_OR_NARROW_SETUP_SYMBOL_PATH`; `KILL_OR_NARROW_SETUP_SYMBOL_PATH`; `SOURCE_DATA_INSUFFICIENT` | Next-session/session-boundary carry-forward freshness is outside the narrowed Continuation path and complete context/caution evidence is still insufficient. | Replace with same-session Continuation evidence or source and regression-test a next-session/session-boundary carry-forward rule plus complete context/caution fields. | NO |
| `QQQ-REAL-HISTORICAL-IDEAL-001` | QQQ | Ideal | `replace` | Ideal stale/spent expiry; Ideal fast-swing freshness; Wide-risk / room threshold; Context/caution review | `SOURCE_DATA_INSUFFICIENT`; `KILL_OR_NARROW_SETUP_SYMBOL_PATH`; `KILL_OR_NARROW_SETUP_SYMBOL_PATH`; `SOURCE_DATA_INSUFFICIENT` | Fast-swing/wide-risk Ideal is outside the narrowed Ideal path; stale/spent expiry, room/risk threshold, and complete context/caution evidence are not source-backed. | Replace with Ideal evidence inside the narrowed path or source and regression-test fast-swing freshness, stale/spent expiry, room/risk thresholds, and complete context/caution fields. | NO |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | SPY | Clean Fast Break | `active_blocked` | Clean Fast Break expiry; Context/caution review | `SOURCE_DATA_INSUFFICIENT`; `SOURCE_DATA_INSUFFICIENT` | Clean Fast Break higher-base/fresh-break expiry is not source-backed and complete context/caution review remains insufficient. | Define and regression-test Clean Fast Break higher-base/fresh-break expiry and add complete context/caution review fields before proof review. | NO |
| `SPY-REAL-HISTORICAL-CONTINUATION-001` | SPY | Continuation | `replace` | Continuation session-boundary freshness; Intrabar ordering; Context/caution review | `KILL_OR_NARROW_SETUP_SYMBOL_PATH`; `KILL_OR_NARROW_SETUP_SYMBOL_PATH`; `SOURCE_DATA_INSUFFICIENT` | Intrabar order-of-events inside completed 1H candles cannot be proven from current source rows, so this Continuation row is outside the narrowed path; complete context/caution evidence is also insufficient. | Replace with lower-timeframe/order-of-events evidence or exclude intrabar-dependent Continuation rows from proof review; add complete context/caution fields if restored. | NO |
| `SPY-REAL-HISTORICAL-IDEAL-001` | SPY | Ideal | `active_blocked` | Ideal stale/spent expiry; Context/caution review | `SOURCE_DATA_INSUFFICIENT`; `SOURCE_DATA_INSUFFICIENT` | Same-session Ideal remains eligible only after source-backed stale/spent expiry and complete context/caution evidence become clean; primary blocker null cannot promote. | Define and regression-test SPY Ideal stale/spent expiry and add complete context/caution review fields before proof review. | NO |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | SPY | Clean Fast Break | `active_blocked` | Clean Fast Break expiry; Context/caution review | `SOURCE_DATA_INSUFFICIENT`; `SOURCE_DATA_INSUFFICIENT` | Clean Fast Break initial-break expiry is not source-backed and complete context/caution review remains insufficient. | Define and regression-test Clean Fast Break initial-break expiry and add complete context/caution review fields before proof review. | NO |

## Next Evidence Fixes

- QQQ Clean Fast Break: source-backed QQQ gap-context evidence, tested Clean Fast Break expiry, and complete context/caution fields.
- SPY Clean Fast Break 003: tested higher-base/fresh-break expiry and complete context/caution fields.
- SPY Clean Fast Break 002: tested initial-break expiry and complete context/caution fields.
- SPY Ideal: tested stale/spent expiry and complete context/caution fields.
- QQQ Continuation replacement path: same-session evidence or tested next-session/session-boundary carry-forward rule plus complete context/caution fields.
- SPY Continuation replacement path: lower-timeframe/order-of-events evidence or exclusion of intrabar-dependent Continuation rows.
- QQQ Ideal replacement path: inside-path Ideal evidence or tested fast-swing freshness, stale/spent expiry, room/risk thresholds, and complete context/caution fields.

## Guardrail Result

No row can enter proof review from missing/source-insufficient rules, narrowed paths, `final_verdict=TRADE` alone, or primary blocker null alone.

Proof accepted: NO.

Profitability claim made: NO.
