# SAFE-FAST Day 41 SPY CFB Starter Option/Execution/Context Batch Review

## Scope

- Task file: `SAFE_FAST_DAY41_SPY_CFB_STARTER_OPTION_EXECUTION_CONTEXT_BATCH_CODEX_TASK.md`.
- Baseline stated by task file: `a6b5daa Fill SPY CFB lifecycle evidence batch`.
- Candidates processed together:
  - `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`
  - `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`
- Data used: cheap starter Databento files only.
- Downloaded more data: NO.
- Used full-window data: NO.
- Backtested: NO.
- Calculated P&L: NO.
- Claimed proof/profitability/readiness: NO.

## Accepted Starter Rule Application

The existing QQQ CFB rule structure was reused only as the CFB-family default where no repo conflict was found:

- Long calls only.
- Nearest reviewed expiration with DTE `>= 14`.
- Lowest call strike at or above the candidate trigger.
- Nearest TCBBO quote at or before signal time by `ts_event`.
- Spread cap `0.15`.
- Spread percent cap `2.00%`.
- Bid size `>= 1`.
- Ask size `>= 1`.
- Setup-time-safe same-contract trade volume `>= 1`.
- Open interest `>= 1` only if setup-time-safe same-contract open interest exists in the starter data.
- No fallback if the top-ranked contract fails.
- Execution quote freshness:
  - `clean` when quote age is `<= 60` seconds.
  - `caution` when quote age is `> 60` seconds and `<= 5` minutes.
  - `fail` when quote age is `> 5` minutes.
- No future data, no fill/P&L/proof/readiness inference.

## Candidate Results

### SPY CFB 002

- Signal time: `2026-04-13T12:30:00-04:00` / `2026-04-13T16:30:00Z`.
- Trigger: `682.03`.
- Top-ranked starter contract: `SPY   260427C00685000`, `instrument_id=1258293281`.
- Expiration: `2026-04-27`, DTE `14`.
- Strike: `685`.
- Selected quote: `2026-04-13T16:29:04.514819033Z`.
- Bid/ask: `6.33` / `6.35`.
- Spread: `0.02`.
- Spread percent: about `0.3155%`.
- Bid/ask size: `123` / `12`.
- Setup-time-safe same-contract trade volume: `12`.
- Setup-time-safe same-contract `stat_type=9` OI row: not found; not evaluated under the SPY starter rule wording.
- Contract-selection result: selected.
- Option context: `clean`.
- Execution context: `clean`, quote age `55.485181` seconds.
- Headline context: `unknown`.
- Complete caution review: `unknown` because headline context is still unknown.

### SPY CFB 003

- Signal time: `2026-04-15T14:30:00-04:00` / `2026-04-15T18:30:00Z`.
- Trigger: `698.65`.
- Top-ranked starter contract: `SPY   260429C00700000`, `instrument_id=1333784938`.
- Expiration: `2026-04-29`, DTE `14`.
- Strike: `700`.
- Local starter quote/trade row for top-ranked contract: `2026-04-15T18:31:23.366609701Z`, after signal.
- Contract-selection result: abstain, `quote_ts_event_after_signal`.
- Option context: `unknown`.
- Execution context: `unknown`, no selected setup-time-safe quote.
- Headline context: `unknown`.
- Complete caution review: `unknown`.

## Fixtures And Calculators

- Added `historical_signal_replay/fixtures/spy_cfb_contract_selection_regression_fixtures.json`.
- Added `historical_signal_replay/fixtures/spy_cfb_execution_context_regression_fixtures.json`.
- Added `historical_signal_replay/fixtures/spy_cfb_context_caution_regression_fixtures.json`.
- Extended `historical_signal_replay/cfb_contract_selector.py` with an explicit `open_interest_required` fixture parameter. The default remains strict for existing QQQ fixtures.
- Extended `historical_signal_replay/context_caution_calculator.py` so fixtures can declare expected candidate identity. QQQ defaults remain unchanged.
- Updated tests:
  - `tests/test_cfb_contract_selector.py`
  - `tests/test_execution_context_calculator.py`
  - `tests/test_context_caution_calculator.py`

## Evidence Fill

Filled only SPY CFB context/caution rows:

- `historical_signal_replay/source_data/richer_export_package_work/spy_cfb_002_complete_context_caution_fields.jsonl`
- `historical_signal_replay/source_data/richer_export_package_work/spy_cfb_003_complete_context_caution_fields.jsonl`

Unrelated evidence fields were not changed.

## Validation

- `python -m unittest tests.test_cfb_contract_selector`: PASS, `15` tests.
- `python -m unittest tests.test_execution_context_calculator`: PASS, `8` tests.
- `python -m unittest tests.test_context_caution_calculator`: PASS, `10` tests.
- `python -m watcher_foundation.source_evidence_work_package_content_validator`: PASS command; `7` passed requests, `2` failed requests, `2` partial rows, `0` header-only rows.
- `python -m watcher_foundation.source_evidence_package_to_intake_bridge`: PASS command; `3` reconsideration-eligible candidates, intake-ready `0`, proof allowed `NO`.

## Remaining Blockers

- SPY CFB 002: headline context remains `unknown`; complete caution remains `unknown`; no entry/fill/exit/cost/slippage/sample-size/promotion rules are accepted.
- SPY CFB 003: option context, headline context, execution context, and complete caution remain `unknown` from starter data; no setup-time-safe top-contract quote exists in the local starter window.
- SPY Ideal still has the only failed work-package requests.
- No candidate is ready.
- No proof or profitability is claimed.
