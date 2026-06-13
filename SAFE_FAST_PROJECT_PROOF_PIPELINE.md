# SAFE-FAST Project Proof Pipeline

## Purpose

SAFE-FAST is still being turned from a setup-recognition system into a complete trade plan. Recognition success is required, but it is not proof of profitability.

This pipeline is project-wide. It applies to QQQ, SPY, IWM, GLD, and any setup type unless a later accepted rule narrows the project.

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

## Current Project Status

Proof accepted: NO.

Profitability claimed: NO.

Current known state: Databento QQQ OPRA files have been structurally validated for the requested QQQ option-data window, but SAFE-FAST still needs mapping rules, trade-plan completeness, replay/regression evidence, and promotion review before any candidate can count.
