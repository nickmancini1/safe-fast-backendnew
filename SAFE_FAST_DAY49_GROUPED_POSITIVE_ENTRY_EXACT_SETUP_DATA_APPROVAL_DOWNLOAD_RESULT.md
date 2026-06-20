# SAFE-FAST Day 49 Grouped Positive-Entry Exact Setup-Data Approval/Download Result

## Scope

- Current task file executed: `SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_EXACT_SETUP_DATA_APPROVAL_DOWNLOAD_CODEX_TASK.md`.
- Required startup files were read first: `SAFE_FAST_BUILD_STATE.md`, the Day 49 setup-evidence result, the Day 49 setup-evidence JSON, the exact setup-data request manifest, `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`, `SAFE_FAST_PROJECT_DASHBOARD.md`, and `SAFE_FAST_PROJECT_RULE_INDEX.md`.
- This was a metadata/cost-check and request-shape review only.
- No data was downloaded.
- No option request, exit-path request, unrestricted full-session request, backtest, P&L calculation, proof acceptance, profitability claim, readiness decision, promotion decision, paper/live decision, real trade choice, `main.py`, Railway/deploy file, broker/account/order code, `.env`, credential file, frozen threshold, or raw vendor file was changed.
- `SAFE_FAST_DB_AUTH` was used only in-process for Databento metadata calls. The credential was not printed, logged, documented, saved, or written to a file.

## Mapping Result

Safe cost-checkable Databento mapping exists for the 1h underlying OHLCV subset only:

- Dataset: `DBEQ.BASIC`
- Schema: `ohlcv-1h`
- Symbol type: `raw_symbol`
- Symbols: manifest `symbol` values only (`GLD`, `SPY`, `QQQ`, `IWM`)
- Scope: underlying hourly OHLCV bars only, no options, no exit path, no P&L

The full manifest request shape is not fully mapped to a safe Databento schema because it asks for:

- `1h RTH OHLCV rows through setup timestamp`
- `24H/daily context as-of setup timestamp`
- `macro context as-of setup timestamp`
- `IV context as-of setup timestamp`
- `event/headline context as-of setup timestamp`

The Databento mapping above covers the OHLCV portion only. It does not provide SAFE-FAST setup labels, trigger/invalidation decisions, blocker/caution decisions, macro context, IV context, event/headline context, or no-hindsight replay decisions. Those fields still require grouped setup-rule/request-shape repair or a separate accepted source mapping before the full setup-context request can be treated as complete.

## Cost Check

Strict manifest timestamps were first tested against Databento metadata. Four request rows have `start_timestamp == end_timestamp`; Databento rejected those strict zero-length windows with `422 data_time_range_start_on_or_after_end`.

For cost-check purposes only, the exact Databento end-exclusive window repair was applied: keep each manifest start timestamp unchanged and advance each manifest end timestamp by one hour so the requested setup bar can be included by `ohlcv-1h`.

Checked total: `$0.002040266989`

Actual billed cost: `NOT_AVAILABLE`

No download was attempted.

| Candidate | Dataset | Schema | Symbol | Start UTC | End UTC exclusive | Checked cost |
| --- | --- | --- | --- | --- | --- | ---: |
| `GLD-REPLACEMENT-IDEAL-CANDIDATE-001` | `DBEQ.BASIC` | `ohlcv-1h` | `GLD` | `2026-05-01T19:30:00Z` | `2026-05-08T19:30:00Z` | `$0.000496506691` |
| `SPY-SOURCE-WINDOW-CLEAN-FAST-BREAK-003` | `DBEQ.BASIC` | `ohlcv-1h` | `SPY` | `2026-03-31T13:30:00Z` | `2026-03-31T14:30:00Z` | `$0.000012516975` |
| `QQQ-SOURCE-WINDOW-CONTINUATION-002` | `DBEQ.BASIC` | `ohlcv-1h` | `QQQ` | `2026-04-02T13:30:00Z` | `2026-04-02T14:30:00Z` | `$0.000012516975` |
| `SPY-SOURCE-WINDOW-CONTINUATION-004` | `DBEQ.BASIC` | `ohlcv-1h` | `SPY` | `2026-04-02T13:30:00Z` | `2026-04-02T14:30:00Z` | `$0.000012516975` |
| `SPY-SOURCE-WINDOW-CONTINUATION-005` | `DBEQ.BASIC` | `ohlcv-1h` | `SPY` | `2026-05-01T13:30:00Z` | `2026-05-01T14:30:00Z` | `$0.000012516975` |
| `IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001` | `DBEQ.BASIC` | `ohlcv-1h` | `IWM` | `2026-04-17T19:30:00Z` | `2026-05-01T19:30:00Z` | `$0.001155734062` |
| `IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002` | `DBEQ.BASIC` | `ohlcv-1h` | `IWM` | `2026-04-28T19:30:00Z` | `2026-05-01T19:30:00Z` | `$0.000337958336` |

## Approval And Download Status

- Approval status: blocked.
- Download status: blocked.
- Reason: no purchase/download approval exists, and the full setup-context request shape is not fully mapped beyond the OHLCV subset.
- Ready for user approval: only the limited OHLCV-subset request shape could be presented for approval after the user explicitly accepts the end-exclusive one-hour repair and the fact that macro/IV/event/headline/setup-label fields remain unresolved.
- Not ready for approval as a full setup-context package until grouped setup-rule/request-shape repair defines accepted sources for the non-OHLCV context fields.

## No-Proof Boundary

- Proof accepted: `NO`
- Profitability claimed: `NO`
- Promotion/readiness/paper/live decision made: `NO`
- New P&L calculated: `NO`
- Databento downloaded: `NO`
- Raw vendor data changed: `NO`
- Option request included: `NO`
- Exit-path request included: `NO`

## Exact Next Grouped Task

`SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_SETUP_DATA_REQUEST_SHAPE_REPAIR_CODEX_TASK.md`

Reason: the OHLCV subset has a safe metadata-cost mapping, but the full setup-context request still needs grouped repair for non-OHLCV context fields and the Databento end-exclusive timestamp shape before any approval/download task can be valid.
