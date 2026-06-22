# SAFE-FAST Day 50 Raw-Data Positive-Entry Accepted Setup Replay Path Decision Result

## Scope

- Task executed: `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_ACCEPTED_SETUP_REPLAY_PATH_DECISION_CODEX_TASK.md`.
- Prior technical result: `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_SETUP_TIME_REPLAY_MAPPING_RESULT.md`.
- Prior machine-readable result: `historical_signal_replay/results/day50_raw_data_positive_entry_setup_time_replay_mapping.json`.
- Source evidence in scope: `historical_signal_replay/source_data/external_underlying_data_drop/SAFE_FAST_DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M.csv`.
- Request ID: `DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M`.
- Dataset/schema/stype: `DBEQ.BASIC / ohlcv-1m / raw_symbol`.
- Authorized window: `SPY`, `2026-03-16T09:30:00-04:00` through `2026-03-16T16:00:00-04:00`.
- Decision scope: planning/governance only.

## Decision

A bounded accepted SAFE-FAST setup-replay mapping path should be created before retrying the three Day 50 SPY raw-data positive-entry opportunities, but not as a direct implementation task.

The next task must first define replay/regression cases and accepted field boundaries. Only after those cases are accepted may a later implementation task map raw one-minute underlying OHLCV evidence into SAFE-FAST setup-time fields.

This decision is needed because the prior mapping result proved valid one-minute SPY OHLCV evidence exists, but all three setup-family opportunities remain blocked by `accepted_setup_time_replay_mapping_path_absent`. Raw vendor OHLCV bars still cannot be treated as SAFE-FAST labels.

## Covered Setup Families

The proposed bounded path may cover only these setup families for the Day 50 SPY raw-data positive-entry retry:

| Setup family | Covered symbol/window | Current blocker |
| --- | --- | --- |
| Ideal | SPY, March 16, 2026 RTH one-minute underlying bars | `accepted_setup_time_replay_mapping_path_absent` |
| Clean Fast Break | SPY, March 16, 2026 RTH one-minute underlying bars | `accepted_setup_time_replay_mapping_path_absent` |
| Continuation | SPY, March 16, 2026 RTH one-minute underlying bars | `accepted_setup_time_replay_mapping_path_absent` |

No other symbols, dates, setup families, option data, exit paths, proof, readiness, paper eligibility, or live eligibility are covered.

## Covered Fields

The proposed bounded path may define only these setup-time fields:

- `setup_time_row`
- `trigger`
- `invalidation`
- `freshness_final_signal_state`
- `blocker_caution_review`
- `session_boundary_behavior`
- `no_hindsight_boundary`

Each field must name its source input, accepted calculator or rule path, timestamp boundary, missing-data behavior, and setup/trade blocking scope before implementation.

## Required Replay And Regression Cases

Before implementation, the next task must define replay/regression cases covering:

- Positive SPY Ideal mapping case from the March 16, 2026 one-minute OHLCV evidence.
- Positive SPY Clean Fast Break mapping case from the March 16, 2026 one-minute OHLCV evidence.
- Positive SPY Continuation mapping case from the March 16, 2026 one-minute OHLCV evidence.
- Missing `setup_time_row` rejection.
- Missing or ambiguous `trigger` rejection.
- Missing or ambiguous `invalidation` rejection.
- Missing `freshness_final_signal_state` rejection.
- Missing `blocker_caution_review` source-backed component rejection or explicit non-blocking classification when allowed by an existing frozen rule.
- Session-boundary case covering same-session behavior.
- Session-boundary case covering carry-forward or prior-session contamination rejection.
- No-hindsight case proving bars after the decision timestamp cannot affect setup labels.
- Wrong-symbol contamination rejection.
- Wrong-window contamination rejection.
- Duplicate setup-family or duplicate row handling.
- Raw-vendor-label rejection proving raw OHLCV values alone do not supply SAFE-FAST labels.
- Determinism case proving repeated runs produce identical field packages and classifications.
- Control preservation case proving existing Day 50 regression controls remain separate and unchanged.

The next task must keep these cases at replay/regression definition scope unless it explicitly accepts the field boundaries and still avoids implementing the mapper.

## Non-Goals And Forbidden Inferences

- Do not request more data.
- Do not request option data.
- Do not request exit-path data.
- Do not infer SAFE-FAST labels directly from raw vendor bars.
- Do not treat a raw OHLCV candle, trend, breakout, gap, shelf, or later favorable move as a SAFE-FAST setup label without an accepted frozen rule path.
- Do not implement a raw OHLCV setup-label mapper before replay/regression cases and field boundaries are accepted.
- Do not weaken frozen trading rules.
- Do not reopen closed safety rejections or preserved controls.
- Do not claim proof, profitability, readiness, promotion, paper eligibility, or live eligibility.
- Do not touch `main.py`, Railway/deploy files, production/live backend, broker/order/account code, credentials, or `.env`.

## Preserved Funnel Totals

- Raw opportunities mapped: `3`.
- Exact setup-time field packages established: `0`.
- New generated candidates: `0`.
- New setup-qualified candidates: `0`.
- New trade candidates: `0`.
- New selected contracts: `0`.
- New eligible entries: `0`.
- New recorded entries: `0`.
- New exact-data-required cases: `3`.
- Preserved controls: `13` setup-qualified, `9` trade candidates, `5` selected contracts, `1` eligible entry, `1` recorded entry.
- Scorecard preserved: `VALID_TRADE_CAPTURED=1`, `TRUE_NO_TRADE=4`, `MISSING_DATA=10`, `MISSED_VALID_TRADE=0`, `INVALID_TRADE_ALLOWED=0`, `UNRESOLVED=0`, `WINNERS=1`, `LOSERS=0`.

## Guardrails

- Raw vendor bars treated as SAFE-FAST labels: `NO`.
- Mapper implemented: `NO`.
- Additional data requested: `NO`.
- Option data requested: `NO`.
- Exit-path data requested: `NO`.
- Frozen trading rules changed: `NO`.
- `main.py` changed: `NO`.
- Railway/deploy files changed: `NO`.
- Production/live backend changed: `NO`.
- Broker/order/account code changed: `NO`.
- Credentials or `.env` changed: `NO`.
- Schwab authentication performed: `NO`.
- Broker mutation attempted: `NO`.
- Proof accepted: `NO`.
- Profitability claimed: `NO`.
- Promotion decision made: `NO`.
- Paper eligibility claimed: `NO`.
- Live eligibility claimed: `NO`.

## Exact Next Task

Create and run `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_ACCEPTED_SETUP_REPLAY_REGRESSION_CASES_CODEX_TASK.md`.

The next task must define the bounded replay/regression cases and accepted field boundaries for the proposed raw one-minute OHLCV setup-replay mapping path. It must not implement the mapper, retry the SPY opportunities, request data, request options, request exit paths, or make any proof/readiness claim.
