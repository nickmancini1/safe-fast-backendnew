# SAFE-FAST Day 41 Raw Tastytrade Next Chat Handoff

## Baseline

SAFE-FAST Day 41 tastytrade raw data capability and first evidence fill.

Start from local git, not old pasted handoffs. The next chat must run:

```powershell
git --no-pager status --short
git --no-pager log -1 --oneline
git --no-pager branch --show-current
```

Do not trust pasted old handoffs over local git output.

Latest known local HEAD when this handoff was written: `46c0a92 Record tastytrade evidence availability check`.

Current branch when this handoff was written: `main`.

## Fixed

tastytrade is the raw-data source.

SAFE-FAST converts raw market and option data into trade-plan labels.

The next task is not asking whether tastytrade gives SAFE-FAST labels such as fresh/stale, expired/valid, context clean/blocked, gap context complete, CFB expiry, Ideal stale/spent, option context usable, execution context usable, or caution clean.

The next task is testing which raw fields tastytrade can provide so SAFE-FAST can calculate those labels itself.

## Blocked

Existing repo evidence is insufficient.

The current work package was prefilled from repo-known data.

Before tastytrade proof, the current work-package content validator result was:

- passed requests: 0.
- failed requests: 9.

tastytrade access was found.

Existing helper paths found:

- `dxlink_candles.py`.
- `historical_signal_replay/export_dxlink_source_csv.py`.

The first tastytrade evidence availability check found local dxLink/OHLCV-style data only. It did not satisfy the 9 richer evidence requests.

Current counts:

- Parked/source_data_insufficient count: 4.
- Replace count: 3.
- Intake-ready count: 0.
- Proof accepted: NO.
- Profitability claim made: NO.

## Why This Matters

The old pool was historical but incomplete.

The repo is now the validator, not the primary evidence source.

The next useful work must test tastytrade raw data capability for options, quotes, spreads, timestamps, and context inputs.

The next chat must not keep mining old repo examples.

## Next

First candidate target: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

First evidence target: QQQ CFB gap context.

Exact raw data needed:

- prior session close.
- signal-day open.
- intraday OHLC through signal time.
- quote timestamps.
- source timestamps proving data was available before or at signal.
- option chain/quote context around signal if available.
- spread/quote quality around signal if available.

SAFE-FAST labels to calculate from raw data:

- `gap_context_status`.
- `gap_context_as_of`.
- `gap_context_reviewed_before_signal`.
- `option_context_status`.
- `execution_context_status`.
- `caution_context_status`.

## Workflow

1. Verify repo state.
2. Read this Day 41 raw tastytrade handoff.
3. Locate tastytrade/dxLink helpers.
4. Run a safe data-only tastytrade capability test.
5. Do not print secrets.
6. Test raw data availability for underlying candles, option chain snapshot/history, option bid/ask quotes, spread, quote timestamps, volume/open interest if available, expiration/strike metadata, underlying price around signal, and data through signal time only.
7. Map raw fields to the 9 evidence requests.
8. Fill work-package files only with real tastytrade-backed raw evidence.
9. Run the content validator.
10. Run the evidence-package-to-intake bridge.
11. If a parked path has all required requests passing, mark it reconsideration-eligible only.
12. Intake-ready still requires later SAFE-FAST gates.
13. Proof remains NO.

## Command

The next chat first response must use this shape:

```text
Baseline:
Fixed:
Blocked:
Next:
Command:
```

It must not use long narrative. It must not use jargon without explaining it.

## User Workflow Rule

The assistant gives one task-file block.

The user pastes it into PowerShell.

The assistant waits.

The assistant gives one separate Codex launch line only after the task file is created.

Never put task creation and Codex launch in the same pasted block.

Never pass huge task text as a command-line argument. Use task files.

Local git output controls.

## Warnings

Do not use Yahoo.

Do not use public OHLC fallback.

Do not use broker/order/account actions.

Do not print secrets.

Do not claim proof.

Do not claim profitability.

Do not modify `main.py`, engine/live trading logic, Railway/deploy files, watcher loops, broker/order/account/options/P&L, alerts, sizing, secrets, `.env`, credentials, tokens, generated report/log files, or live-data paths.
