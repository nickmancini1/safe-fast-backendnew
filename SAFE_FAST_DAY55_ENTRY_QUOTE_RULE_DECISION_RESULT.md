# SAFE-FAST Day 55 Entry Quote Rule Decision Result

## Baseline

- Active replay surface: `historical_signal_replay/day55_ready_downloaded_contracts_replay.py`.
- Existing Day 55 ready-downloaded replay behavior evaluates the earliest `cmbp-1` quote inside the accepted entry window.
- SPY 707C evidence pattern under review: first quote spread `0.18`; later same-window quote spread `0.15`.

## Rule Decision

- Rule decision: `RULE_DEFINITION_GAP`.
- Preserved replay behavior until an explicit rule is accepted: `first quote only`.
- Entry is not newly allowed from a later valid quote inside the accepted entry window.

## Existing Docs Basis

- `SAFE_FAST_PROJECT_RULE_INDEX.md` still lists the entry rule as `missing/needs decision`.
- `SAFE_FAST_DAY41_QQQ_CFB_EXECUTION_CONTEXT_RULE_DECISION.md` defines spread, quote-age, size, volume, and no-fallback gates for a selected setup-time-safe quote, but it does not define whether Day 55 economic replay may skip a failed first entry-window quote and use a later passing quote.
- Because the docs do not define this exact first-quote-vs-later-valid entry-window rule, the safe decision is to mark `RULE_DEFINITION_GAP` and regression-protect the current first-quote-only behavior.

## Regression Protection

- Added focused regression: `tests/test_day55_ready_downloaded_contracts_replay.py::Day55ReadyDownloadedContractsReplayTests::test_entry_rule_gap_preserves_first_quote_only_spread_rejection`.
- The regression builds a synthetic SPY 707C entry window where quote 1 fails spread `0.18` and quote 2 passes spread `0.15`.
- Expected result remains `NO_ENTRY_EXACT_REJECTION` with first blocker `spread_above_0_15`; no entry timestamp, entry price, exit, P&L, proof, or paper/live eligibility is created.

## Guardrails

- No vendor download.
- No Schwab.
- No Railway/deploy.
- No live backend.
- No `main.py` change.
- No profitability, proof, paper/live eligibility, broker/account/order/fill, credential, or `.env` change.
