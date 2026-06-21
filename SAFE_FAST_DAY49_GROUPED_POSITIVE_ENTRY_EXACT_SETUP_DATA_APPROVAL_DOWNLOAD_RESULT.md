# SAFE-FAST Day 49 Grouped Positive-Entry Exact Setup-Data Approval/Download Result

## Scope

- Current task file executed: `SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_EXACT_SETUP_DATA_APPROVAL_DOWNLOAD_CODEX_TASK.md`.
- Required startup files were read first: `SAFE_FAST_BUILD_STATE.md`, the Day 49 setup-evidence result, the Day 49 setup-evidence JSON, the exact setup-data request manifest, `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`, `SAFE_FAST_PROJECT_DASHBOARD.md`, and `SAFE_FAST_PROJECT_RULE_INDEX.md`.
- User approval in this run was limited to the exact previously cost-checked OHLCV subset: `DBEQ.BASIC` / `ohlcv-1h` / `raw_symbol`, manifest symbols only (`GLD`, `SPY`, `QQQ`, `IWM`), fresh-cost ceiling `$0.01`.
- No option, exit-path, macro, event, headline, IV, setup-label, P&L, broker/account/order, `.env`, credential, `main.py`, Railway/deploy, or frozen-threshold data/code was requested or changed.
- `SAFE_FAST_DB_AUTH` was used only in-process for Databento metadata and timeseries calls. The credential was not printed, logged, documented, saved, or written to a file.

## Mapping Result

Safe Databento mapping exists for the underlying 1h OHLCV subset only:

- Dataset: `DBEQ.BASIC`
- Schema: `ohlcv-1h`
- Symbol type: `raw_symbol`
- Symbols: manifest `symbol` values only (`GLD`, `SPY`, `QQQ`, `IWM`)
- Scope: underlying hourly OHLCV bars only

The full setup-context request remains not fully mapped because OHLCV does not provide SAFE-FAST setup labels, trigger/invalidation decisions, blocker/caution decisions, macro context, IV context, event/headline context, or no-hindsight replay decisions.

## Cost And Download

Strict manifest timestamps had four zero-length windows, so the accepted Databento end-exclusive repair was used: keep each manifest start timestamp unchanged and advance each manifest end timestamp by one hour.

Fresh checked total: `$0.002040266989`

Authorized ceiling: `$0.01`

Actual billed cost: `NOT_AVAILABLE`

Download manifest: `historical_signal_replay/source_data/external_underlying_data_drop/SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_OHLCV_DOWNLOAD_MANIFEST.json`

Raw vendor files were written only under ignored `historical_signal_replay/source_data/external_underlying_data_drop/`.

| Candidate | Symbol | Checked cost | Rows | Validation |
| --- | --- | ---: | ---: | --- |
| `GLD-REPLACEMENT-IDEAL-CANDIDATE-001` | `GLD` | `$0.000496506691` | `119` | PASS |
| `SPY-SOURCE-WINDOW-CLEAN-FAST-BREAK-003` | `SPY` | `$0.000012516975` | `3` | PASS |
| `QQQ-SOURCE-WINDOW-CONTINUATION-002` | `QQQ` | `$0.000012516975` | `3` | PASS |
| `SPY-SOURCE-WINDOW-CONTINUATION-004` | `SPY` | `$0.000012516975` | `3` | PASS |
| `SPY-SOURCE-WINDOW-CONTINUATION-005` | `SPY` | `$0.000012516975` | `3` | PASS |
| `IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001` | `IWM` | `$0.001155734062` | `277` | PASS |
| `IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002` | `IWM` | `$0.000337958336` | `81` | PASS |

## Replay Result

The affected Day 49 candidate replay surfaces were rerun immediately after validation:

- `python -B -m historical_signal_replay.day49_grouped_positive_entry_setup_field_completion`: PASS, `8` candidates, `0` setup-qualified, `0` trade candidates, `8` missing-data cases.
- `python -B -m historical_signal_replay.day49_positive_entry_setup_evidence_completion`: PASS, `8` slots, `0` completed locally, `0` replaced, `4` exact external requests, `3` contradictions, `1` unusable.
- `python -B -m historical_signal_replay.day48_positive_trade_capture_funnel`: PASS, `15` candidates, `1` valid captured, `4` true no-trades, `6` missing-data cases.

Replay effect: unchanged. OHLCV validates the limited underlying bar subset, but it does not resolve setup-time row acceptance, trigger, invalidation, freshness/final-signal, blocker/caution, macro/IV/event/headline context, or no-hindsight boundaries.

## Status

- Safe exact setup-data dataset/schema mapping exists: `YES`, for OHLCV subset only.
- OHLCV subset download approved and completed: `YES`.
- Full setup-context approval/download ready: `NO`.
- Option request included: `NO`.
- Exit-path request included: `NO`.
- Macro/event/headline/IV/setup-label request included: `NO`.
- Proof accepted: `NO`.
- Profitability claimed: `NO`.
- Promotion/readiness/paper/live decision made: `NO`.
- New P&L calculated: `NO`.

## Exact Next Grouped Task

`SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_SETUP_DATA_REQUEST_SHAPE_REPAIR_CODEX_TASK.md`

Reason: the approved OHLCV subset was downloaded and validated, but the full setup-context request still needs grouped repair for non-OHLCV context fields before the affected candidates can move beyond setup-evidence blockers.
