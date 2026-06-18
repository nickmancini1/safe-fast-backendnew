# SAFE-FAST Day 47 Next Grouped Data-Needed Cost-Check Result

## Scope

- Task file executed: `SAFE_FAST_DAY47_NEXT_GROUPED_DATA_NEEDED_COST_CHECK_CODEX_TASK.md`.
- Baseline: `SAFE_FAST_DAY47_GROUPED_CFB_EXPANSION_DATA_NEEDED_PLAN.md`.
- Mode: grouped data-needed cost-check documentation only.
- Dataset target: Databento `OPRA.PILLAR`.
- Databento data downloaded: NO.
- Raw vendor files written: NO.
- New backtest run: NO.
- New P&L calculated: NO.
- Proof, profitability, readiness, promotion, or intake-ready change: NO.

## Grouped Candidates Covered

| Candidate | Role in this grouped task | Current data state | Day 47 cost-check routing |
| --- | --- | --- | --- |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | Positive CFB review-only anchor | Selected contract `SPY   260427C00685000`, `instrument_id=1258293281`; local selected-contract entry and exit-path review already exists; result remains `completed_profit_target`, adjusted result `+1.61` | No new Databento request needed for its current anchor role |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | `quote_after_signal` no-entry control and next narrow CFB data-needed candidate | Top-ranked starter contract `SPY   260429C00700000`, `instrument_id=1333784938`; local quote/trade row is after setup | Exact selected-contract setup-window and conditional exit-path cost check identified; fresh cost call blocked before price returned |
| `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | `quote_age_above_5_minutes` no-entry control | Selected contract `QQQ   260427C00615000`, `instrument_id=1023411456`; local targeted TCBBO/trades/statistics/definition diagnostics already preserve stale-quote result | No fallback scan and no new Databento request needed for its current control role |
| `SPY-REAL-HISTORICAL-IDEAL-001` | Deferred Ideal comparison reference | Starter lifecycle/context evidence exists, but Ideal-specific trade-plan rules remain incomplete | Parked; no CFB cost-check request |
| `QQQ-REAL-HISTORICAL-IDEAL-001` | Parked Ideal comparison reference | Replay and starter option data exist; no current richer request or accepted QQQ Ideal rule path | Parked; no CFB cost-check request |
| `SPY-REAL-HISTORICAL-CONTINUATION-001` | Parked Continuation comparison reference | Replay and starter option data exist; no accepted Continuation rule path | Parked; no CFB cost-check request |
| `QQQ-REAL-HISTORICAL-CONTINUATION-001` | Parked Continuation comparison reference | Replay and starter option data exist; no accepted Continuation rule path | Parked; no CFB cost-check request |

## Additional Local CFB Rows

Local replay review found the same usable CFB signal anchors already represented by the grouped packet:

- `QQQ` initial-break signal at `2026-04-13T12:30:00-04:00`.
- `SPY` initial-break signal at `2026-04-13T12:30:00-04:00`.
- `SPY` higher-base fresh-break signal at `2026-04-15T14:30:00-04:00`.

Other local CFB replay rows are watch, follow-through, spent, or no-fresh-trigger context rows. They are not additional ready completed CFB backtest rows under the current rule state.

## Exact Databento Requests Identified

Parent-symbol discovery needs are currently separated from selected-contract needs:

- Parent-symbol discovery: none required for the current three CFB anchors because selected contracts and instrument IDs are already recorded for the current roles.
- Future parent-symbol discovery: if a later task adds new CFB rows without selected contract identity, cost-check `definition`, `tcbbo`, `trades`, and `statistics` using parent/root `SPY` or `QQQ` first, then narrow to selected instrument IDs after contract identity is accepted.
- Selected-contract request for the current next data-needed row: `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`, `instrument_id=1333784938`.

| Candidate | Request | Dataset | Schema | Symbol / instrument | `stype_in` | UTC start | UTC end | Setup vs full exit path |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | selected-contract setup quotes, open to signal | `OPRA.PILLAR` | `tcbbo` | `1333784938` | `instrument_id` | `2026-04-15T13:30:00Z` | `2026-04-15T18:30:00Z` | setup-window |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | selected-contract setup trades, open to signal | `OPRA.PILLAR` | `trades` | `1333784938` | `instrument_id` | `2026-04-15T13:30:00Z` | `2026-04-15T18:30:00Z` | setup-window |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | selected-contract signal-day statistics/open-interest diagnosis | `OPRA.PILLAR` | `statistics` | `1333784938` | `instrument_id` | `2026-04-15T04:00:00Z` | `2026-04-16T04:00:00Z` | setup-window support |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | selected-contract TCBBO path if entry becomes valid later | `OPRA.PILLAR` | `tcbbo` | `1333784938` | `instrument_id` | `2026-04-15T18:30:00Z` | `2026-04-15T19:45:00Z` | full exit-path candidate |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | selected-contract trades path if entry becomes valid later | `OPRA.PILLAR` | `trades` | `1333784938` | `instrument_id` | `2026-04-15T18:30:00Z` | `2026-04-15T19:45:00Z` | full exit-path candidate |

## Cost-Check Attempt

Local access facts:

- `DATABENTO_API_KEY`: present; key value not printed or written.
- Python `databento` package: installed.
- Python `databento` version: `0.79.0`.

The fresh cost-only call attempted:

```text
metadata.get_cost(
  dataset="OPRA.PILLAR",
  schema="tcbbo",
  symbols=1333784938,
  stype_in="instrument_id",
  start="2026-04-15T13:30:00Z",
  end="2026-04-15T18:30:00Z"
)
```

Result:

```text
ProxyError HTTPSConnectionPool(host='hist.databento.com', port=443): Max retries exceeded with url: /v0/metadata.get_cost (Caused by ProxyError('Unable to connect to proxy', NewConnectionError("HTTPSConnection(host='127.0.0.1', port=9): Failed to establish a new connection: [WinError 10061] No connection could be made because the target machine actively refused it")))
```

Because the first Databento metadata cost call failed before a Databento response, the remaining identified calls were not attempted.

## Checked Price

- Fresh Day 47 checked price: `NOT_AVAILABLE_PROXY_BLOCKED`.
- Exact Databento price returned in this task: none.
- Prior reference only: `SAFE_FAST_DAY41_SPY_BATCH_DATABENTO_DIRECT_COST_CHECK_RESULT.md` recorded a broader SPY three-candidate parent-symbol total of `$72.355630`; that is not the fresh Day 47 grouped CFB selected-contract checked price.

## Approval And Download Decision

- User approval required before any download: YES.
- Reason: no fresh checked price was returned, and this task does not include approval to download.
- Download performed: NO.
- Raw Databento files changed: NO.

## Data Still Missing After Cost Check

- Fresh Databento cost for the selected-contract `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` setup-window request.
- If cost is acceptable and a later task authorizes download, selected-contract `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` setup-time-safe TCBBO, trades, and statistics/open-interest coverage.
- Conditional only if entry becomes valid later: selected-contract `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` TCBBO and trades path from signal through `15:45 ET`.
- Historical headline/no-headline source policy and complete caution rules remain missing for promotion-grade review.
- Additional valid completed CFB examples remain below the minimum `20` completed-example blocker.

## Next Recommended Action

Rerun the same cost-only selected-contract Databento check from an environment where HTTPS access to `hist.databento.com` is not routed through the refused `127.0.0.1:9` proxy. Do not download data until a fresh exact price is returned and the user explicitly approves any full-window download.
