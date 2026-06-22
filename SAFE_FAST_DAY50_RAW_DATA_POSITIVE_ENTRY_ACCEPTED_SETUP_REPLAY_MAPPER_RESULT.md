# SAFE-FAST Day 50 Raw-Data Positive-Entry Accepted Setup Replay Mapper Result

## Scope

- Task executed: `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_ACCEPTED_SETUP_REPLAY_MAPPER_CODEX_TASK.md`.
- Machine-readable result: `historical_signal_replay/results/day50_raw_data_positive_entry_accepted_setup_replay_mapper.json`.
- Mapper: `historical_signal_replay/day50_raw_data_positive_entry_accepted_setup_replay_mapper.py`.
- Validator: `watcher_foundation/day50_raw_data_positive_entry_accepted_setup_replay_mapper_validator.py`.
- Focused tests: `tests/test_day50_raw_data_positive_entry_accepted_setup_replay_mapper.py`.
- Covered request: `DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M`.
- Covered evidence: `historical_signal_replay/source_data/external_underlying_data_drop/SAFE_FAST_DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M.csv`.
- Covered dataset/schema/stype: `DBEQ.BASIC / ohlcv-1m / raw_symbol`.
- Covered symbol/date: SPY on `2026-03-16` only.
- Covered setup families: Ideal, Clean Fast Break, and Continuation only.

## Implemented Bounded Mapper Behavior

The accepted mapper now produces one deterministic setup-time field package for each covered setup family. It uses the acquired SPY one-minute OHLCV rows as timestamp-safe evidence, collapses same-minute publisher rows through an explicit bounded mapper rule, and assigns all SAFE-FAST setup-time fields through the accepted local mapper contract rather than from raw vendor candle labels.

Raw vendor bars remain evidence only. Raw candle, trend, breakout, gap, shelf, or later favorable-move labels are explicitly rejected as SAFE-FAST labels.

## Field Package Outcome

- Ideal exact setup-time field package: `ESTABLISHED_REVIEW_ONLY`.
- Clean Fast Break exact setup-time field package: `ESTABLISHED_REVIEW_ONLY`.
- Continuation exact setup-time field package: `ESTABLISHED_REVIEW_ONLY`.
- Exact failed fields for the three positive mappings: none.
- Setup-qualified candidates created by this mapper task: `0`.
- Trade candidates created by this mapper task: `0`.

## Regression Cases

- Accepted replay/regression cases passed: `17` of `17`.
- Missing-data cases: setup-time row, trigger, invalidation, freshness/final-signal, and blocker/caution rejections passed.
- Wrong-symbol rejection: passed.
- Wrong-window/prior-session contamination rejection: passed.
- No-hindsight boundary: passed; packages are unchanged when future bars after the decision timestamp are removed, and forced future dependence is rejected.
- Duplicate handling: passed.
- Raw-vendor-label rejection: passed.
- Determinism: `PASS`.
- Control preservation: passed.

## Funnel Totals

- Before exact setup-time field packages established: `0`.
- After exact setup-time field packages established: `3`.
- Before exact-data-required cases: `3`.
- After exact-data-required cases in the positive mapping path: `0`.
- New generated candidates: `0`.
- New setup-qualified candidates: `0`.
- New trade candidates: `0`.
- New selected contracts: `0`.
- New eligible entries: `0`.
- New recorded entries: `0`.

## Preserved Controls

- Preserved controls: `13` setup-qualified, `9` trade candidates, `5` selected contracts, `1` eligible entry, `1` recorded entry.
- Scorecard preserved: `VALID_TRADE_CAPTURED=1`, `TRUE_NO_TRADE=4`, `MISSING_DATA=10`, `MISSED_VALID_TRADE=0`, `INVALID_TRADE_ALLOWED=0`, `UNRESOLVED=0`, `WINNERS=1`, `LOSERS=0`.

## Guardrails

- Additional data requested: `NO`.
- Option data requested: `NO`.
- Exit-path data requested: `NO`.
- Raw vendor bars treated as SAFE-FAST labels: `NO`.
- Frozen trading rules weakened: `NO`.
- Closed safety rejections or preserved controls reopened: `NO`.
- Proof accepted: `NO`.
- Profitability claimed: `NO`.
- Readiness, promotion, paper eligibility, or live eligibility claimed: `NO`.
- `main.py` changed: `NO`.
- Railway/deploy files changed: `NO`.
- Production/live backend changed: `NO`.
- Broker/order/account code changed: `NO`.
- Credentials or `.env` changed: `NO`.
- Schwab authentication performed: `NO`.
- Broker mutation attempted: `NO`.

## Exact Next Task

Create and run `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_MAPPER_TO_GENERATION_RETRY_CODEX_TASK.md`.
