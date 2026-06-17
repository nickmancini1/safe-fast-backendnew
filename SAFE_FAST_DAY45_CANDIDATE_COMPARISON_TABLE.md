# SAFE-FAST Day 45 Candidate Comparison Table

## Family Summary

| Setup family | Candidates | Current strength | Current weakness | Sprint route |
| --- | --- | --- | --- | --- |
| Clean Fast Break | QQQ CFB 001, SPY CFB 002, SPY CFB 003 | Most developed family. QQQ has gap/lifecycle/context evidence. SPY 002/003 have grouped lifecycle and starter context fills. | QQQ execution failed. SPY 003 option/execution unknown. SPY 002 still lacks headline/complete caution and trade-plan rules. | Use SPY CFB 002 as first trade-rule/backtest-prep reference; keep QQQ CFB and SPY CFB 003 in repair. |
| Ideal | SPY Ideal 001, QQQ Ideal 001 | SPY Ideal has lifecycle/context request-shaped evidence. QQQ Ideal has replay artifact and starter data. | Ideal gap thresholds, context rules, contract rules, and trade-plan rules are not accepted broadly. SPY Ideal option/execution remain unknown. | Repair package before any backtest-prep. |
| Continuation | QQQ Continuation 001, SPY Continuation 001 | Replay artifacts and starter option data exist. | No current richer work-package requests and no accepted Continuation setup-family rules. | Parking list until a Continuation rule/evidence package is authorized. |

## Candidate Ranking For Next Work

| Rank | Candidate | Why | Route |
| --- | --- | --- | --- |
| 1 | `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | Best current starter evidence: lifecycle complete, option context clean, execution context clean. | First trade-rule/backtest-prep reference after rules are accepted. |
| 2 | `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | Most complete QQQ evidence chain and useful failed execution case. | Repair/failure-diagnosis reference, not backtest-ready. |
| 3 | `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | Lifecycle complete and same setup family as SPY CFB 002. | Repair option/quote blocker. |
| 4 | `SPY-REAL-HISTORICAL-IDEAL-001` | SPY Ideal lifecycle and context requests pass. | Repair Ideal-specific context/option/entry rules. |
| 5 | `QQQ-REAL-HISTORICAL-IDEAL-001` | Replay and starter data exist. | Park until Ideal package is authorized. |
| 6 | `QQQ-REAL-HISTORICAL-CONTINUATION-001` | Replay and starter data exist. | Park until Continuation package is authorized. |
| 7 | `SPY-REAL-HISTORICAL-CONTINUATION-001` | Replay and starter data exist. | Park until Continuation package is authorized. |

## Trade-Plan Readiness Comparison

| Candidate | Evidence clean? | Setup rule accepted? | Contract/option usable? | Execution usable? | Trade-plan complete? | Readiness result |
| --- | --- | --- | --- | --- | --- | --- |
| QQQ CFB 001 | YES | YES for QQQ CFB | Caution | Fail | NO | Repair |
| SPY CFB 002 | YES | YES for SPY CFB | Clean starter context | Clean starter context | NO | First backtest-prep reference after rules |
| SPY CFB 003 | YES | YES for SPY CFB | Unknown | Unknown | NO | Repair |
| SPY Ideal 001 | YES | YES for SPY Ideal starter lifecycle | Unknown | Unknown | NO | Repair |
| QQQ Continuation 001 | NO current request | NO | Raw starter only | Not evaluated | NO | Park |
| QQQ Ideal 001 | NO current request | NO | Raw starter only | Not evaluated | NO | Park |
| SPY Continuation 001 | NO current request | NO | Raw starter only | Not evaluated | NO | Park |

## Plain-English Decision

Clean Fast Break is the strongest family because it has the most accepted rules, fixtures, calculators, and evidence fills. The best narrow reference is SPY CFB 002.

Ideal is second because SPY Ideal now has request-shaped lifecycle/context evidence, but its option/execution and gap/context rules remain too incomplete.

Continuation is last because it has replay and starter data but no current evidence package or accepted setup-family rules.

