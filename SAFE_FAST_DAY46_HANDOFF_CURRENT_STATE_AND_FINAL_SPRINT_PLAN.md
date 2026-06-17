# SAFE-FAST Day 46 Current State And Final Sprint Plan

## Baseline

Local git controls. Latest known local HEAD before this handoff commit was `59b2a03 Run first CFB backtest reference case` on `main`.

This handoff follows the Day 46 first CFB backtest review/expansion work already present locally.

## Current State In Plain English

SAFE-FAST has one useful positive Clean Fast Break reference and two useful rejection controls.

The positive reference:

- Candidate: `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`.
- Result: completed profit target.
- Entry basis: `6.37`.
- Adjusted exit basis: `7.98`.
- Cost/slippage-adjusted result: `+1.61`.
- Meaning: useful positive reference, not proof.

The controls:

- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`: stayed out because the quote came after the signal.
- `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`: stayed out because the quote was older than 5 minutes.

Current project state:

- Evidence cleanup reached `9` passed requests and `0` failed requests after the SPY Ideal batch.
- Intake-ready remains `0`.
- No candidate is ready.
- No real trade is chosen.
- No proof or profitability is accepted.
- The next work is grouped comparison and expansion, not one-example grinding.

## What The First CFB Result Means

The result says the first SPY CFB positive reference can survive the accepted first-pass entry, exit, cost/slippage, and named-result path using local selected-contract exit-path data.

It does not say the strategy works. One profitable example is not enough. The value is that the repo now has a concrete positive anchor to compare against no-trade controls and future CFB, Ideal, and Continuation examples.

## Final Sprint Rule

Day 60 is July 1, 2026. It is a checkpoint and reporting date, not a forced finish.

The build must be correct, and the project must also be bounded. The next `$200` month is the final high-intensity build sprint before moving toward the `$20` tier. That sprint must produce a decision package.

The decision package must cover:

- what works
- what failed
- what needs repair
- remaining data costs
- strongest candidate families
- weakest candidate families
- accepted rules
- missing rules
- what can continue on the `$20` tier
- what would require another serious spend or redesign

## Batch-First Work Plan

Batching remains mandatory. Future work should use:

- grouped candidate passes
- grouped rule packages
- grouped validation
- grouped cost checks
- grouped comparison
- batched blocker diagnosis when possible

Avoid one-field loops unless a real blocker makes batching unsafe.

## Budget Control

- Cheap starter data first.
- Full-window Databento data only after exact cost check and user approval.
- No broad data downloads from guesses.
- Known warning: the SPY 3-candidate full-window cost check was about `$72.36`.
- Raw vendor files stay local-only and ignored.

## Recommended Next Grouped Task

The next grouped task should:

1. Review the first CFB backtest result.
2. Build a grouped expansion plan.
3. Compare `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`, `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`, and `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.
4. Decide the next batch across CFB, Ideal, and Continuation.
5. Use `SAFE_FAST_DAY46_FIRST_BACKTEST_REVIEW_AND_EXPANSION_PLAN_CODEX_TASK.md` if present, or create a fresh grouped review/expansion task if local git says it is missing.

## Do Not Do In This Handoff

- Do not download data.
- Do not run new backtests.
- Do not calculate new P&L.
- Do not change P&L files.
- Do not touch `main.py`.
- Do not touch live, engine, broker, order, account, Railway, `.env`, secrets, raw Databento files, or evidence fills.
