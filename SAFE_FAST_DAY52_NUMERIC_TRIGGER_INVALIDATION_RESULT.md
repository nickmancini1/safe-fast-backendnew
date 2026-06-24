# SAFE-FAST Day 52 Numeric Trigger and Invalidation Result

## Scope

- Task executed: `SAFE_FAST_DAY52_FAMILY_NUMERIC_BINDING_AND_PROMOTION_CODEX_TASK.md`.
- Machine-readable result: `historical_signal_replay/results/day52_numeric_trigger_invalidation.json`.
- Implementation: `historical_signal_replay/day52_numeric_trigger_invalidation.py`.
- Covered setup families: Ideal, Clean Fast Break, and Continuation for SPY on `2026-03-16`.

## Result

Candidate A setup-bar range is promoted separately for each family after binding audit.
The constructors bind trigger to the setup-time high and invalidation to the setup-time low for the bullish accepted packages.

- Ideal: trigger `668.360000000` (PROMOTE_CANDIDATE_A), invalidation `667.870000000` (CANDIDATE_A_SETUP_BAR_RANGE); setup-qualified allowed `True`.
- Clean Fast Break: trigger `668.360000000` (PROMOTE_CANDIDATE_A), invalidation `667.870000000` (CANDIDATE_A_SETUP_BAR_RANGE); setup-qualified allowed `True`.
- Continuation: trigger `668.360000000` (PROMOTE_CANDIDATE_A), invalidation `667.870000000` (CANDIDATE_A_SETUP_BAR_RANGE); setup-qualified allowed `True`.

## Guardrails

No OPRA evidence, option selection, entry, exit, P&L, proof, profitability, paper/live eligibility, `main.py`, Railway/deploy, broker/account/order/fill/alert, credential, `.env`, sizing, or frozen `patch8` threshold change was made.
