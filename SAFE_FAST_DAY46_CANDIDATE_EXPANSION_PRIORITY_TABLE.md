# SAFE-FAST Day 46 Candidate Expansion Priority Table

## Ranking

| Rank | Workstream | Candidates | Why next | Current blocker | Next grouped action |
| --- | --- | --- | --- | --- | --- |
| 1 | More Clean Fast Break examples | Start with `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`, `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`, and `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`; add more CFB examples only through a grouped task | CFB now has one completed positive reference and two named no-trade controls | One positive result is not enough; more completed valid CFB examples are needed before sample or expectancy review | Build a grouped CFB batch that keeps the positive reference and no-trade controls together |
| 2 | Ideal examples | `SPY-REAL-HISTORICAL-IDEAL-001`, then `QQQ-REAL-HISTORICAL-IDEAL-001` only after Ideal rule/evidence authorization | Ideal is the next setup-family comparison path and has starter evidence for SPY | Ideal gap/context thresholds, setup-time option/execution rules, entry/exit/cost rules, and promotion gates are incomplete | Prepare Ideal comparison only if the next task can keep it grouped and rule-backed |
| 3 | Continuation examples | `SPY-REAL-HISTORICAL-CONTINUATION-001`, `QQQ-REAL-HISTORICAL-CONTINUATION-001` | Continuation may be useful for family comparison after CFB/Ideal, but is less ready now | Continuation-specific lifecycle, request-shaped evidence, contract-selection, context, and trade-plan rules are missing | Park until a Continuation rule/evidence package is explicitly authorized |
| 4 | Repair/no-trade examples | `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`, `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | Failed/no-trade examples protect the process from overfitting to SPY CFB 002 | They are not backtest candidates under current rules; they are controls and diagnostics | Keep them in grouped validation so quote-after-signal and stale-quote rejection stay enforced |
| 5 | Data-needed examples | Continuation candidates, QQQ Ideal, and any future CFB examples missing complete source/exit paths | These may become useful later, but current missing-rule or missing-data state prevents countable work | More data requires grouped cost check and user approval; raw downloads are not allowed here | Record exact data/rule needs before any later cost-check request |

## Expansion Rule

The next expansion should add comparison breadth before chasing another single result. A batch is preferred over a one-candidate loop unless a named blocker makes batching unsafe.

## Non-Goals

- No data download.
- No new P&L calculation.
- No proof or profitability claim.
- No readiness mark.
- No intake-ready change.
