# SAFE-FAST Day 41 Batch Restart QQQ Diagnosis And Candidate Plan

## Baseline

- Baseline task file states latest commit: `f4a8781 Fill QQQ CFB execution context evidence`.
- This is a docs and candidate-packet restart task only.
- Backtest authorized: NO.
- P&L calculated: NO.
- Proof accepted: NO.
- Profitability claimed: NO.
- Candidate readiness changed: NO.

## QQQ Diagnosis

`QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` should stay parked.

What passed:

- Gap context passed. The accepted QQQ CFB gap calculator filled `gap_context_status=clean`, `gap_context_as_of=2026-04-13T12:30:00-04:00`, and `gap_context_reviewed_before_signal=true`.
- Lifecycle/stale-spent passed. The accepted QQQ CFB lifecycle calculator and fixtures support the setup-time row as fresh and preserve later spent context as regression evidence only.
- Option context became `caution`. The selected top-ranked contract `QQQ   260427C00615000` / `instrument_id=1023411456` was listed before setup on Apr 13, was absent from the Apr 10 parent definitions, and passed setup-time-safe quote, spread, size, and trade-volume checks under the accepted narrow new-contract open-interest exception.

What failed:

- Execution context failed.
- Complete caution review failed by accepted precedence.
- Headline context remains `unknown`.

Why it failed:

- The selected quote `ts_event=2026-04-13T16:06:30.640301037Z` was compared with the setup boundary `2026-04-13T16:30:00Z`.
- The accepted execution-context calculator measured quote age as `1409.359699` seconds, about `23` minutes `29` seconds.
- The accepted rule classifies quote age over `5` minutes as `fail`, with rejection reason `quote_age_above_5_minutes`.
- Complete-caution precedence is `fail`, then `unknown`, then `caution`, then `clean`, so execution `fail` makes complete caution `fail`.

What this teaches the project:

- QQQ was useful, but not as a ready candidate. It proved the path from raw Databento fields to no-hindsight calculators, fixtures, and request-shaped evidence.
- The project should reuse the QQQ tooling in batches: gap context, lifecycle, context/caution aggregation, contract selection, new-contract open-interest exception, execution quote-age/spread/size/volume checks, and Databento OPRA normalization.
- A candidate can pass chart context and still fail at execution quality. The quote-age gate is not cosmetic; it is a hard no-trade diagnostic.
- The next useful work is not to keep widening or repairing this one QQQ contract. The useful next work is batch preflight across the remaining parked/replace candidates.

What should not be repeated:

- Do not keep reprocessing QQQ CFB as if another evidence fill can make the stale selected quote valid.
- Do not bypass the no-fallback rule after the selected/top-ranked contract fails a gate.
- Do not treat a source-backed option quote as a fill or a trade.
- Do not start a backtest, P&L calculation, proof claim, profitability claim, or readiness update from this QQQ evidence.
- Do not rebuild calculators that already exist; reuse them where their rule scope actually applies.

## Batch Candidate Table

| Candidate | Setup type | Symbol | Known signal date/time | Data already in repo | Likely Databento data needed | Reusable calculators/tools | Batch evidence checks to attempt | Blocked by missing rules | Current disposition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | Clean Fast Break | QQQ | `2026-04-13T12:30:00-04:00` | Source CSV line 132, replay log lines 3-6, QQQ OPRA definitions/TCBBO/trades/statistics, accepted gap/lifecycle/context/option/execution evidence fills | None for the current selected contract unless an explicit new diagnostic task asks for broader market sampling | `gap_context_calculator.py`, `cfb_lifecycle_calculator.py`, `cfb_contract_selector.py`, `execution_context_calculator.py`, `context_caution_calculator.py`, Databento normalizer | None for readiness; record as failed execution case | Headline source policy, entry/exit/cost/slippage, sample-size, promotion gates | Parked, not ready |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | Clean Fast Break | SPY | `2026-04-15T14:30:00-04:00` | SPY source CSV line 154, replay log lines 5-6, work-package rows for higher-base lifecycle and context/caution with `TASTYTRADE_DATA_NOT_AVAILABLE` blockers | SPY OPRA definitions, TCBBO, trades, statistics/OI around setup; likely reviewed expiration/strike window around trigger `698.65` | QQQ CFB lifecycle and context/caution patterns may be adapted only after SPY CFB fixtures; Databento normalizer can be reused | Batch source row check, Databento availability/cost check, option quote/volume/OI preflight, missing lifecycle rule/regression check | SPY CFB higher-base lifecycle rule/regressions, SPY-specific gap thresholds if needed, contract-selection evidence authorization, headline policy, entry/exit/cost/slippage | Process now with SPY CFB 002 as a pair |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | Clean Fast Break | SPY | `2026-04-13T12:30:00-04:00` | SPY source CSV line 138, replay log lines 2-3, work-package rows for initial-break lifecycle and context/caution with `TASTYTRADE_DATA_NOT_AVAILABLE` blockers | SPY OPRA definitions, TCBBO, trades, statistics/OI around setup; likely reviewed expiration/strike window around trigger `682.03` | QQQ CFB lifecycle/context/contract/execution calculators as templates only; Databento normalizer can be reused | Batch source row check, Databento availability/cost check, option quote/volume/OI preflight, missing lifecycle rule/regression check | SPY CFB initial-break lifecycle rule/regressions, SPY-specific option/context rules, headline policy, entry/exit/cost/slippage | Process now with SPY CFB 003 as a pair |
| `SPY-REAL-HISTORICAL-IDEAL-001` | Ideal | SPY | `2026-05-13T11:30:00-04:00` | SPY source CSV line 291, replay log lines 5-6, work-package rows for Ideal lifecycle and context/caution with `TASTYTRADE_DATA_NOT_AVAILABLE` blockers | SPY OPRA definitions, TCBBO, trades, statistics/OI around setup; likely reviewed expiration/strike window around trigger `740.75` | Databento normalizer and context/caution aggregation vocabulary; QQQ CFB calculators are not directly reusable for Ideal lifecycle without Ideal fixtures | Batch source row check, Databento availability/cost check, option quote/volume/OI preflight, Ideal lifecycle rule-gap review | Ideal lifecycle rule/regressions, Ideal gap/context thresholds, Ideal contract-selection rule, headline policy, entry/exit/cost/slippage | Process after SPY CFB pair, or include in same SPY data-cost pass |
| `QQQ-REAL-HISTORICAL-CONTINUATION-001` | Continuation | QQQ | `2026-04-30T15:30:00-04:00` | QQQ Continuation replay log and summary; signal row has trigger `664.51`, invalidation `653.81`, later spent row on `2026-05-01T15:30:00-04:00`; no current richer work-package request found | QQQ OPRA definitions, TCBBO, trades, statistics/OI around signal if this path is promoted into evidence work | Databento normalizer and context/caution aggregation vocabulary only; Continuation-specific lifecycle/contract rules still need fixtures | Batch candidate-packet preflight, source/log identity check, data-needs estimate | Continuation lifecycle/stale-spent rule, Continuation contract-selection rule, gap/context/headline rules, entry/exit/cost/slippage | Park until a Continuation rule package is authorized |
| `QQQ-REAL-HISTORICAL-IDEAL-001` | Ideal | QQQ | `2026-05-13T12:30:00-04:00` | QQQ Ideal replay log and summary; signal row has trigger `714.59`, invalidation `696.66`, later spent row on `2026-05-14T11:30:00-04:00`; no current richer work-package request found | QQQ OPRA definitions, TCBBO, trades, statistics/OI around signal if this path is promoted into evidence work | Databento normalizer and context/caution aggregation vocabulary only; Ideal lifecycle/contract rules need fixtures | Batch candidate-packet preflight, source/log identity check, data-needs estimate | Ideal lifecycle/stale-spent rule, Ideal contract-selection rule, gap/context/headline rules, entry/exit/cost/slippage | Park until Ideal rule package is authorized |
| `SPY-REAL-HISTORICAL-CONTINUATION-001` | Continuation | SPY | `2026-04-30T12:30:00-04:00` | SPY Continuation replay log and summary; signal row has trigger `715.61`, invalidation `708.37`, later spent row on `2026-04-30T15:30:00-04:00`; no current richer work-package request found | SPY OPRA definitions, TCBBO, trades, statistics/OI around signal if this path is promoted into evidence work | Databento normalizer and context/caution aggregation vocabulary only; Continuation-specific lifecycle/contract rules still need fixtures | Batch candidate-packet preflight, source/log identity check, data-needs estimate | Continuation lifecycle/stale-spent rule, Continuation contract-selection rule, gap/context/headline rules, entry/exit/cost/slippage | Park until a Continuation rule package is authorized |

## Batch Restart Recommendation

Process the two SPY Clean Fast Break candidates together first:

- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`.

Reason:

- Both already have richer work-package rows.
- Both use the same symbol, setup family, source CSV, and replay log.
- Both are blocked on the same classes of missing evidence: SPY CFB lifecycle/regression artifacts and option/headline/execution/complete-caution fields.
- A single SPY Databento cost-check/preflight can cover both setup windows before any download or evidence fill is considered.

Secondary candidate:

- `SPY-REAL-HISTORICAL-IDEAL-001`, because it also uses the SPY source CSV and may be included in the same SPY Databento cost-check, but its Ideal-specific rules should not be mixed into CFB lifecycle decisions.

Candidates to keep parked for now:

- `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`, because execution context failed.
- `QQQ-REAL-HISTORICAL-CONTINUATION-001`, `QQQ-REAL-HISTORICAL-IDEAL-001`, and `SPY-REAL-HISTORICAL-CONTINUATION-001`, because they have replay artifacts but no current richer work-package request and lack accepted setup-specific rule packages.
