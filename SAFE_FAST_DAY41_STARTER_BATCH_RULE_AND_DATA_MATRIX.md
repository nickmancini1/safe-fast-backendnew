# SAFE-FAST Day 41 Starter Batch Rule and Data Matrix

## Scope

This matrix routes the six remaining candidates after read-only starter Databento inspection. It does not authorize downloads, evidence fills, backtests, P&L, proof, profitability, or readiness.

## Matrix

| Candidate | Setup family | Process now with starter data | Needs setup-specific rule first | Needs full-window data later | Parked for now | Replace candidate still needs new rule path |
| --- | --- | --- | --- | --- | --- | --- |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | Clean Fast Break, SPY initial break | YES, but only as raw starter inspection after SPY CFB rule/regression authorization. | YES: SPY CFB initial-break lifecycle/regressions, SPY CFB contract-selection, option/headline/execution/context rules. | YES: likely for selected-contract quote path, entry/fill/exit, stop/invalidation, time exit, costs, slippage, sample-size, and proof. | NO once SPY CFB rule work is authorized; otherwise parked. | NO. |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | Clean Fast Break, SPY higher-base fresh break | YES, but only as raw starter inspection after SPY CFB higher-base rule/regression authorization. | YES: SPY CFB higher-base lifecycle/regressions, SPY CFB contract-selection, option/headline/execution/context rules. | YES: likely for selected-contract quote path, entry/fill/exit, stop/invalidation, time exit, costs, slippage, sample-size, and proof. | NO once SPY CFB rule work is authorized; otherwise parked. | NO. |
| `SPY-REAL-HISTORICAL-IDEAL-001` | Ideal, SPY | YES, but only as raw starter inspection after Ideal rule/regression authorization. | YES: Ideal lifecycle/gap/context and Ideal contract-selection rules. | YES: likely for selected-contract quote path, entry/fill/exit, stop/invalidation, time exit, costs, slippage, sample-size, and proof. | YES until Ideal package is authorized. | NO. |
| `QQQ-REAL-HISTORICAL-CONTINUATION-001` | Continuation, QQQ | YES, but only as raw starter inspection after Continuation evidence/rule package authorization. | YES: Continuation lifecycle/context/contract-selection rules and request-shaped evidence package. | YES: likely for selected-contract quote path, entry/fill/exit, stop/invalidation, time exit, costs, slippage, sample-size, and proof. | YES until Continuation package is authorized. | YES: current candidate lacks a richer work-package path and needs a new Continuation rule/evidence path before replacement processing. |
| `QQQ-REAL-HISTORICAL-IDEAL-001` | Ideal, QQQ | YES, but only as raw starter inspection after Ideal rule/evidence package authorization. | YES: Ideal lifecycle/gap/context and Ideal contract-selection rules. | YES: likely for selected-contract quote path, entry/fill/exit, stop/invalidation, time exit, costs, slippage, sample-size, and proof. | YES until Ideal package is authorized. | YES: current candidate lacks a richer work-package path and needs a new Ideal rule/evidence path before replacement processing. |
| `SPY-REAL-HISTORICAL-CONTINUATION-001` | Continuation, SPY | YES, but only as raw starter inspection after Continuation evidence/rule package authorization. | YES: Continuation lifecycle/context/contract-selection rules and request-shaped evidence package. | YES: likely for selected-contract quote path, entry/fill/exit, stop/invalidation, time exit, costs, slippage, sample-size, and proof. | YES until Continuation package is authorized. | YES: current candidate lacks a richer work-package path and needs a new Continuation rule/evidence path before replacement processing. |

## Recommended Grouping

1. First grouped rule path: SPY Clean Fast Break.
   - Pair `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` and `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`.
   - Build SPY CFB lifecycle/regression decisions for initial break and higher-base fresh break.
   - Then run starter-only raw option inspection using the already local files.

2. Second grouped rule path: Ideal.
   - Pair `SPY-REAL-HISTORICAL-IDEAL-001` and `QQQ-REAL-HISTORICAL-IDEAL-001`.
   - Define Ideal lifecycle/gap/context and contract-selection rules before raw option inspection is interpreted.

3. Third grouped rule path: Continuation.
   - Pair `QQQ-REAL-HISTORICAL-CONTINUATION-001` and `SPY-REAL-HISTORICAL-CONTINUATION-001`.
   - Create request-shaped evidence path plus Continuation lifecycle and contract-selection rules before raw option inspection is interpreted.

## Stop Conditions

- Do not fill evidence from this matrix.
- Do not select a real contract or trade.
- Do not calculate P&L.
- Do not claim proof, profitability, or readiness.
- Do not download full-window data until a later explicit task authorizes the reason and scope.
