# SAFE-FAST Project Proof Pipeline

## Purpose

SAFE-FAST is still being turned from a setup-recognition system into a complete trade plan. Recognition success is required, but it is not proof of profitability.

This pipeline is project-wide. It applies to QQQ, SPY, IWM, GLD, and any setup type unless a later accepted rule narrows the project.

## Day 45 Bounded Sprint Rule

Day 60 is a progress checkpoint, not the finish line. The build target is a profitable trading plan, and the project will not cut corners to hit a date. The project also cannot run indefinitely. The next $200 month is the final high-intensity build sprint before moving toward the $20 tier.

The final sprint must stay batched, evidence-backed, cost-controlled, and focused on tested examples, comparison, trade-plan rules, and a clear decision package. Weak, failed, unclear, missing, or unprofitable results trigger diagnosis and repair; they are not forced into passing results.

## Pipeline

1. Raw data
   - Source-backed market, option, timestamp, context, and outcome inputs must exist.
   - Missing evidence is a blocker, not low confidence.
   - Raw vendor files do not by themselves prove a SAFE-FAST label or trade result.

2. Calculated labels
   - SAFE-FAST labels must be calculated from raw evidence or accepted rule artifacts.
   - Vendor data may provide fields such as bid, ask, timestamp, expiration, strike, volume, and open interest.
   - Vendor data must not be treated as providing SAFE-FAST labels unless the repo has a reviewed mapping rule.

3. Setup recognition
   - Setup type, symbol, setup candle, trigger, invalidation, freshness/final-signal state, blockers, and no-hindsight boundary must be explicit.
   - Favorable later price movement is not enough.

4. Stage transitions
   - The setup must have accepted rules for moving between watch, candidate, signal, spent, stale, invalidated, blocked, no-trade, and review states.
   - If stage-transition rules are missing or unclear, the candidate remains blocked.

5. Trade-plan completeness
   - A result cannot count unless the trade plan completeness gate is satisfied.
   - Contract, entry, exit, cost, slippage, liquidity, invalidation, stop, and failure rules must be fixed before counting the result.

6. Replay
   - Replay must use setup-time evidence only for setup-time decisions.
   - Future bars, future replay rows, outcome fields, fills, P&L, and profitability cannot backfill setup-time decisions.

7. Regression
   - Rules that affect labels, stage transitions, entries, exits, stale/spent status, or trade outcome must have regression cases before promotion.
   - Regression cases must include missing data, future-data rejection, boundary conditions, and wrong-symbol or wrong-setup contamination where relevant.

8. Evidence review
   - Evidence review must identify what is accepted, missing, partial, blocked, or invalid.
   - A passing structure check is not a passing content check.
   - A passing data-file validation is not a trade proof.

9. Failure diagnosis
   - Failed, weak, unclear, missing, or unprofitable results trigger diagnosis and repair.
   - Diagnosis must identify the affected setup type, symbol, layer, bad or missing evidence, smallest evidence-backed fix, and required regression protection.

10. Promotion decision
   - Promotion requires accepted evidence, passing regressions, complete trade-plan rules, and no-hindsight review.
   - Promotion can also mean narrowing, replacing, or removing a setup or symbol from the profitable plan.
   - No candidate is intake-ready from raw data or recognition alone.

11. Final sprint decision package
   - Before moving toward the $20 tier, the project needs a clear package stating what works, what failed, what needs repair, what data costs remain, strongest and weakest candidate families, accepted and missing rules, what can continue on the $20 tier, and what would require another serious spend or redesign.
   - Full-window data spending requires exact cost check and user approval before download.

## Current Project Status

Proof accepted: NO.

Profitability claimed: NO.

Current known state: repo docs after the SPY Ideal starter batch show work-package content validation at `9` passed requests and `0` failed requests. Intake-ready remains controlled by the separate readiness gate. SAFE-FAST still needs grouped trade-plan readiness, candidate comparison, cost-controlled data use, complete trade-plan rules, replay/regression evidence, and promotion review before any candidate can count.
