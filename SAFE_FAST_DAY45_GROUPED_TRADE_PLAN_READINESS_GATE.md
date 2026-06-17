# SAFE-FAST Day 45 Grouped Trade-Plan Readiness Gate

## Bottom Line

No candidate is ready for a countable backtest or proof claim yet.

The evidence-package content gate is clean for the four mapped richer work-package candidates, but the trade-plan completeness gate is still open. The missing pieces are trade-plan rules: entry, fill, exit, stop/invalidation, time exit, cost/slippage, failure diagnosis, sample size, and promotion.

## Validator And Bridge Result

- Content validator command: `python -m watcher_foundation.source_evidence_work_package_content_validator`.
- Content validator result: `9` passed requests, `0` failed requests, `0` partial rows, `0` header-only rows.
- Bridge command: `python -m watcher_foundation.source_evidence_package_to_intake_bridge`.
- Bridge result: `4` reconsideration-eligible candidates, `0` intake-ready candidates, proof allowed `NO`.
- Reconsideration-eligible candidates: QQQ CFB 001, SPY CFB 002, SPY CFB 003, and SPY Ideal 001.
- Replacement/parked candidates not mapped by current richer work-package requests: QQQ Continuation 001, QQQ Ideal 001, and SPY Continuation 001.

## Candidate Readiness Status

| Candidate | Usable data state | Evidence state | Setup state | Option/quote state | Execution state | Current blocker | Route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | Local QQQ OPRA files exist and targeted wider quote/trade files exist for the selected top contract. | All three mapped work-package requests pass. | QQQ CFB gap and lifecycle are calculator-backed and filled. | Option context is `caution` under the new-contract OI exception. | `fail`; selected quote is about `23m 29s` old. | Execution-context failure plus missing complete trade-plan rules. | Repair batch, not first backtest batch. |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | Cheap starter SPY Databento files exist; full-window data not approved. | Lifecycle and context/caution requests pass. | SPY CFB initial break is lifecycle-backed as fresh at setup and later spent. | Starter selected contract `SPY   260427C00685000`; option context `clean`. | Starter execution context `clean`; quote age about `55.485181s`. | Headline is `unknown`; complete caution is `unknown`; trade-plan rules are missing. | First backtest-prep batch only after trade-rule package is accepted. |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | Cheap starter SPY Databento files exist; full-window data not approved. | Lifecycle and context/caution requests pass. | SPY CFB higher-base break is lifecycle-backed as fresh at setup. | Starter top-ranked contract has only post-signal local quote/trade row; option context `unknown`. | `unknown`. | No setup-time-safe selected quote under starter rule; headline and complete caution unknown; trade-plan rules missing. | Repair batch. |
| `SPY-REAL-HISTORICAL-IDEAL-001` | Cheap starter SPY Databento files exist; full-window data not approved. | Both mapped SPY Ideal requests pass. | Ideal lifecycle is fresh at setup and later spent under starter rule. | Top-ranked starter option row is post-signal; option context `unknown`. | `unknown`. | Ideal gap thresholds, headline policy, setup-time option/execution context, and trade-plan rules are missing. | Repair batch. |
| `QQQ-REAL-HISTORICAL-CONTINUATION-001` | Cheap starter Databento files exist and replay artifact exists. | No current richer work-package request. | Continuation-specific lifecycle not accepted. | Raw starter quote/trade/OI inspection exists only; no Continuation contract rule. | Not evaluated. | Needs Continuation evidence package and setup-family rules before option work. | Parking list. |
| `QQQ-REAL-HISTORICAL-IDEAL-001` | Cheap starter Databento files exist and replay artifact exists. | No current richer work-package request. | Ideal-specific lifecycle not accepted for this QQQ candidate. | Raw starter quote/trade/OI inspection exists only; no QQQ Ideal contract rule. | Not evaluated. | Needs Ideal evidence package and setup-family rules before option work. | Parking list. |
| `SPY-REAL-HISTORICAL-CONTINUATION-001` | Cheap starter Databento files exist and replay artifact exists. | No current richer work-package request. | Continuation-specific lifecycle not accepted. | Raw starter quote/trade/OI inspection exists only; no Continuation contract rule. | Not evaluated. | Needs Continuation evidence package and setup-family rules before option work. | Parking list. |

## First Batch Path

The best near-term path is not a backtest yet. It is a grouped trade-rule package with `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` as the first backtest-prep candidate and the other candidates held as repair or parking references.

Reason: SPY CFB 002 is the only current candidate with lifecycle complete, starter option context `clean`, and starter execution context `clean`. It still cannot be counted because headline/complete caution and trade-plan rules are missing.

## Repair Batch

- QQQ CFB 001: diagnose whether stale quote failure is a hard no-trade, a data-window issue, or a contract-rule issue. Do not fallback-scan without a new rule.
- SPY CFB 003: diagnose the post-signal top-ranked quote blocker and decide whether broader quote coverage or a stricter no-trade label is appropriate.
- SPY Ideal 001: define Ideal gap/context thresholds and investigate setup-time option/execution context before any backtest-prep claim.

## Parking List

- QQQ Continuation 001, QQQ Ideal 001, and SPY Continuation 001 stay parked.
- They have replay artifacts and starter option data, but they do not have request-shaped evidence packages or setup-family rule packages.

## Gate Decision

- Backtest authorized: NO.
- Trade chosen: NO.
- P&L calculated: NO.
- Proof accepted: NO.
- Profitability claimed: NO.
- Candidate marked ready: NO.
- Intake-ready count: `0`.

