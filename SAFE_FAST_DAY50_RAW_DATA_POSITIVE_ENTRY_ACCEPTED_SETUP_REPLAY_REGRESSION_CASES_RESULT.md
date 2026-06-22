# SAFE-FAST Day 50 Raw-Data Positive-Entry Accepted Setup Replay Regression Cases Result

## Scope

- Task executed: `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_ACCEPTED_SETUP_REPLAY_REGRESSION_CASES_CODEX_TASK.md`.
- Prior decision result: `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_ACCEPTED_SETUP_REPLAY_PATH_DECISION_RESULT.md`.
- Prior mapping result: `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_SETUP_TIME_REPLAY_MAPPING_RESULT.md`.
- Prior machine-readable mapping result: `historical_signal_replay/results/day50_raw_data_positive_entry_setup_time_replay_mapping.json`.
- Source evidence in scope: `historical_signal_replay/source_data/external_underlying_data_drop/SAFE_FAST_DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M.csv`.
- Request ID: `DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M`.
- Dataset/schema/stype: `DBEQ.BASIC / ohlcv-1m / raw_symbol`.
- Authorized window: `SPY`, `2026-03-16T09:30:00-04:00` through `2026-03-16T16:00:00-04:00`.
- Covered setup families: Ideal, Clean Fast Break, and Continuation for SPY on March 16, 2026 only.
- Result scope: planning/governance and regression definition only.

## Decision

The bounded replay/regression cases and accepted field boundaries required before implementation are now defined.

This result does not implement the raw OHLCV setup-label mapper, does not retry the three Day 50 SPY raw-data positive-entry opportunities, and does not request more data, option data, or exit-path data. Raw vendor OHLCV bars still cannot be treated as SAFE-FAST labels.

## Accepted Field Boundaries

Each future implementation must build a complete setup-time field package for one setup family at one decision timestamp. If any mandatory field is missing, ambiguous, outside scope, future-contaminated, wrong-symbol, wrong-window, duplicate-conflicted, or supplied only by a raw vendor label inference, the candidate remains blocked before `SETUP_QUALIFIED`.

| Field | Accepted source boundary | Timestamp boundary | Missing or ambiguous behavior | Blocking scope |
| --- | --- | --- | --- | --- |
| `setup_time_row` | May be derived only by an accepted SAFE-FAST setup-family replay/calculator path over the authorized SPY one-minute underlying rows. The row must identify one exact setup decision row for the family and must not come from a vendor-provided label. | Source rows used for the decision must have timestamps `<=` the setup decision timestamp and must be inside `2026-03-16T09:30:00-04:00` through `2026-03-16T16:00:00-04:00`. | Missing, multiple, non-SPY, out-of-window, non-chronological, duplicate-conflicted, or raw-label-only rows reject the field package. | Blocks setup and trade. |
| `trigger` | May be accepted only from a frozen SAFE-FAST trigger rule for the specific setup family after `setup_time_row` exists. A breakout, candle shape, raw high/low/open/close value, or later move is not a trigger unless the accepted rule names it. | Trigger inputs must be available no later than the setup decision timestamp. | Missing trigger, multiple competing triggers, trigger after the decision timestamp, or trigger inferred from later bars rejects the field package. | Blocks setup and trade. |
| `invalidation` | May be accepted only from a frozen SAFE-FAST invalidation rule for the setup family after `setup_time_row` exists. It must name the exact threshold/state used to block stale, failed, or invalidated setups. | Invalidation inputs must be available no later than the setup decision timestamp. | Missing invalidation, ambiguous invalidation, contradictory invalidation, or invalidation repaired from later bars rejects the field package. | Blocks setup and trade. |
| `freshness_final_signal_state` | May be accepted only from frozen SAFE-FAST lifecycle/stage-transition rules for the setup family, including setup identity, stage, trigger state, prior state when required, and row ordering. | Lifecycle inputs must be available no later than the setup decision timestamp. | Missing lifecycle state, stale/spent ambiguity, prior-state ambiguity, duplicate fresh signal, or final-signal state inferred from outcome bars rejects the field package. | Blocks setup and trade. |
| `blocker_caution_review` | May be accepted only from source-backed SAFE-FAST context/caution components or an existing frozen rule explicitly classifying a component as non-blocking for this setup-time decision. Optional context cannot silently block a technical setup label unless a frozen rule makes it mandatory. | Component inputs must be available no later than the setup decision timestamp, and official/news/macro inputs must use historical-vintage or timestamp-safe values when applicable. | Missing mandatory blocker/caution input rejects trade progression; missing optional context is recorded as non-blocking only when an existing frozen rule permits it. Raw bars cannot supply context/caution labels. | Blocks trade when mandatory; setup only if an existing frozen rule says so. |
| `session_boundary_behavior` | May be accepted only from SAFE-FAST session-boundary and lifecycle rules that define same-session reset, prior-session carry-forward, and next-session contamination behavior for the setup family. | Inputs must be limited to the authorized March 16, 2026 RTH session unless a frozen same-family rule explicitly allows a prior-session state input. | Prior-session contamination, wrong-session carry-forward, missing reset behavior, or cross-session ambiguity rejects the field package. | Blocks setup and trade. |
| `no_hindsight_boundary` | May be accepted only by replay fixtures/logs or calculator contracts proving the setup decision used no rows, labels, outcomes, fills, P&L, or favorable later movement after the decision timestamp. | The boundary is strict: bars after the decision timestamp may not affect setup identity, trigger, invalidation, freshness/final state, blocker/caution, or session behavior. | Any future bar, outcome, fill, P&L, target/stop result, or later favorable move used in setup labeling rejects the field package. | Blocks setup and trade. |

## Required Replay And Regression Cases

These cases must exist and pass before any raw one-minute OHLCV setup-replay mapper can be accepted for the Day 50 SPY retry.

| Case ID | Required coverage | Expected outcome before implementation |
| --- | --- | --- |
| `DAY50-SPY-IDEAL-POSITIVE-MAPPING` | Ideal setup-family field package for SPY March 16, 2026 using only authorized one-minute underlying rows and accepted SAFE-FAST rule paths. | One complete field package may be produced only if all seven accepted field boundaries are satisfied. |
| `DAY50-SPY-CFB-POSITIVE-MAPPING` | Clean Fast Break setup-family field package for SPY March 16, 2026 using only authorized one-minute underlying rows and accepted SAFE-FAST rule paths. | One complete field package may be produced only if all seven accepted field boundaries are satisfied. |
| `DAY50-SPY-CONTINUATION-POSITIVE-MAPPING` | Continuation setup-family field package for SPY March 16, 2026 using only authorized one-minute underlying rows and accepted SAFE-FAST rule paths. | One complete field package may be produced only if all seven accepted field boundaries are satisfied. |
| `DAY50-SPY-MISSING-SETUP-TIME-ROW` | Authorized rows exist but no exact setup decision row can be established. | Reject before `SETUP_QUALIFIED` with exact failed field `setup_time_row`. |
| `DAY50-SPY-MISSING-OR-AMBIGUOUS-TRIGGER` | Setup row exists but trigger is missing, conflicting, duplicated, or not rule-backed. | Reject before `SETUP_QUALIFIED` with exact failed field `trigger`. |
| `DAY50-SPY-MISSING-OR-AMBIGUOUS-INVALIDATION` | Setup row exists but invalidation state is missing, conflicting, or not rule-backed. | Reject before `SETUP_QUALIFIED` with exact failed field `invalidation`. |
| `DAY50-SPY-MISSING-FRESHNESS-FINAL-SIGNAL` | Setup row exists but freshness, stale/spent, prior-state, or final-signal state is missing or ambiguous. | Reject before `SETUP_QUALIFIED` with exact failed field `freshness_final_signal_state`. |
| `DAY50-SPY-MISSING-BLOCKER-CAUTION` | Mandatory blocker/caution source-backed component is missing, or optional context is treated as mandatory without a frozen rule. | Reject trade progression when mandatory, or record non-blocking optional status only when a frozen rule permits it. |
| `DAY50-SPY-SAME-SESSION-BOUNDARY` | Same-session behavior inside the March 16, 2026 RTH window, including reset and valid row ordering. | Accept only if same-session rule inputs are explicit and timestamp-safe. |
| `DAY50-SPY-PRIOR-SESSION-CONTAMINATION` | Prior-session carry-forward, next-session carry-forward, or cross-session state contaminates the March 16, 2026 decision. | Reject with exact failed field `session_boundary_behavior`. |
| `DAY50-SPY-NO-HINDSIGHT` | Bars after the setup decision timestamp are present but must not affect any setup-time label or field. | Reject any implementation that changes labels when future bars are present or removed. |
| `DAY50-SPY-WRONG-SYMBOL` | Non-SPY rows, mixed symbols, or symbol aliases contaminate the source package. | Reject with wrong-symbol source-scope failure before setup qualification. |
| `DAY50-SPY-WRONG-WINDOW` | Rows outside the authorized March 16, 2026 RTH window are required for the setup package without an accepted rule. | Reject with wrong-window source-scope failure before setup qualification. |
| `DAY50-SPY-DUPLICATE-HANDLING` | Duplicate rows, duplicate setup-family packages, or duplicate setup-time decisions appear for one family. | Deterministically reject or de-duplicate only under an accepted rule; no silent double counting. |
| `DAY50-SPY-RAW-VENDOR-LABEL-REJECTION` | Raw OHLCV candle patterns, trend, breakout, gap, shelf, or later favorable move are offered as direct SAFE-FAST labels. | Reject; vendor bars are evidence inputs only and do not supply setup labels. |
| `DAY50-SPY-DETERMINISM` | Same inputs and rule versions are run repeatedly. | Output field packages, rejection reasons, ordering, and hashes must match exactly. |
| `DAY50-SPY-CONTROL-PRESERVATION` | Existing Day 50 regression controls are present while the new raw-data mapping path is evaluated. | Preserve controls separately: `13` setup-qualified, `9` trade candidates, `5` selected contracts, `1` eligible entry, `1` recorded entry; no closed safety rejection is reopened. |

## Exact Negative Case Requirements

- Missing-data cases must report the exact missing field, source, dataset/schema/API/calculator, timestamp window, unavailable reason, blocking scope, and next action.
- Wrong-symbol cases must fail when any non-SPY or mixed-symbol row is required to form a field package.
- Wrong-window cases must fail when rows outside `2026-03-16T09:30:00-04:00` through `2026-03-16T16:00:00-04:00` are required without an accepted rule.
- No-hindsight cases must prove that bars after the setup decision timestamp cannot affect setup labels, stage state, blocker/caution state, or acceptance.
- Duplicate cases must prevent duplicate setup-family packages, duplicate setup-time rows, duplicate field packages, and silent double counting.
- Raw-vendor-label rejection cases must prove raw OHLCV values alone do not supply `setup_time_row`, `trigger`, `invalidation`, lifecycle/freshness, blocker/caution, session-boundary, or no-hindsight labels.

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

## Non-Goals And Forbidden Inferences

- Mapper implemented: `NO`.
- Day 50 SPY raw-data positive-entry opportunities retried: `NO`.
- Additional data requested: `NO`.
- Option data requested: `NO`.
- Exit-path data requested: `NO`.
- Raw vendor bars treated as SAFE-FAST labels: `NO`.
- Raw candle, trend, breakout, gap, shelf, or later favorable move treated as a SAFE-FAST setup label: `NO`.
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

Create and run `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_ACCEPTED_SETUP_REPLAY_MAPPER_CODEX_TASK.md`.

The next task may implement the bounded raw one-minute OHLCV setup-replay mapper only against the accepted field boundaries and replay/regression cases defined here. It must remain limited to Ideal, Clean Fast Break, and Continuation for SPY on March 16, 2026. It must not request more data, request option data, request exit-path data, infer labels directly from raw vendor bars, weaken frozen rules, touch `main.py` or Railway/deploy files, touch broker/order/account/credential paths, or claim proof, profitability, readiness, promotion, paper eligibility, or live eligibility.
