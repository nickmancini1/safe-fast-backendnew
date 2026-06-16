# SAFE-FAST Day 41 Batch Next Actions

## Guardrails

- Do not backtest.
- Do not calculate P&L.
- Do not claim proof, profitability, readiness, or a chosen trade.
- Do not modify `main.py`, live/engine trading logic, broker/order/account files, Railway/deploy files, `.env`, secrets, or raw Databento files.
- Reuse existing tools where their accepted rule scope applies.

## Grouped Plan

### 1. Batch Data-Needs Check

Check the seven candidate packets and split candidates into:

- already evidence-shaped in the richer work package;
- replay-only with no current richer work-package request;
- parked because a completed calculator-backed failure already exists.

Initial grouping:

- Evidence-shaped now: `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`, `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`, `SPY-REAL-HISTORICAL-IDEAL-001`.
- Replay-only parked: `QQQ-REAL-HISTORICAL-CONTINUATION-001`, `QQQ-REAL-HISTORICAL-IDEAL-001`, `SPY-REAL-HISTORICAL-CONTINUATION-001`.
- Completed failure parked: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

### 2. Batch Databento Cost-Check Plan

Create one cost-check package for SPY before any data pull:

- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`: setup `2026-04-13T12:30:00-04:00`, trigger `682.03`.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`: setup `2026-04-15T14:30:00-04:00`, trigger `698.65`.
- Optional same pass: `SPY-REAL-HISTORICAL-IDEAL-001`, setup `2026-05-13T11:30:00-04:00`, trigger `740.75`.

Request-shape to cost-check only:

- OPRA definitions for the signal date and prior trading day where open-interest/listing proof may matter.
- TCBBO quote window from regular-session open through setup, narrowed by symbol, expiration range, and strike band after a reviewed-universe rule exists.
- Trades from regular-session open through setup for same-contract volume.
- Statistics/open-interest source where available before setup.

No vendor API call or raw file write is authorized by this next-actions doc.

### 3. Batch Evidence-Preflight Plan

Before filling evidence, run a preflight that answers for each candidate:

- Is the source CSV row present?
- Is the replay log signal row present?
- Is trigger/invalidation present?
- Is the setup-time no-hindsight boundary explicit?
- Does a setup-specific lifecycle rule exist?
- Does a setup-specific contract-selection rule exist?
- Are option quote, trade, and statistics fields locally available or only requested?
- Are headline/no-headline fields source-backed?

Expected result: SPY CFB candidates should expose shared missing lifecycle and context/caution blockers; QQQ CFB should remain parked as execution fail.

### 4. Batch Calculator Reuse Plan

Reuse directly:

- `historical_signal_replay/databento_opra_normalizer.py` for read-only OPRA parsing and quote/trade/statistics inspection.
- `historical_signal_replay/context_caution_calculator.py` for aggregation precedence only where accepted component statuses exist.
- `historical_signal_replay/execution_context_calculator.py` for selected-contract quote-age/spread/size/volume checks only after a selected contract is defined.

Reuse as templates, not direct authority:

- `historical_signal_replay/gap_context_calculator.py` for SPY only after SPY-specific or setup-general gap thresholds are accepted.
- `historical_signal_replay/cfb_lifecycle_calculator.py` for SPY CFB only after SPY CFB fixtures/decision docs are created or a project-wide CFB lifecycle rule is accepted.
- `historical_signal_replay/cfb_contract_selector.py` for SPY only after reviewed-universe, expiration, strike, side, liquidity, open-interest, and no-fallback rules are accepted for SPY CFB.

Do not reuse QQQ-specific thresholds as if they prove SPY or Ideal behavior.

### 5. Batch Rule-Gap List

Current rule gaps:

- SPY CFB initial-break lifecycle rule/regression rows.
- SPY CFB higher-base fresh-break lifecycle rule/regression rows.
- SPY Ideal stale/spent lifecycle rule/regression rows.
- Continuation lifecycle and stale/spent rule package for QQQ/SPY.
- Ideal contract-selection rules.
- SPY CFB contract-selection evidence authorization and any SPY-specific reviewed-universe parameters.
- Historical headline/no-headline source and category policy.
- Entry rule, fill assumption, exit rule, stop/invalidation translation, time exit, cost/slippage assumptions, failure labels, sample-size requirements, and promotion gates.

### 6. Next 2-3 Candidates To Process Together

Process together first:

- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`.

Include in the same data-cost pass if cheap and bounded:

- `SPY-REAL-HISTORICAL-IDEAL-001`.

Keep parked:

- `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`, because execution context failed.
- `QQQ-REAL-HISTORICAL-CONTINUATION-001`, `QQQ-REAL-HISTORICAL-IDEAL-001`, and `SPY-REAL-HISTORICAL-CONTINUATION-001`, because replay artifacts exist but accepted evidence package/rule paths are not ready.
