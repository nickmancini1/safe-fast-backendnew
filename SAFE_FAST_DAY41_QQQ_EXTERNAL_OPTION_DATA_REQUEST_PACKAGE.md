# SAFE-FAST Day 41 QQQ External Option Data Request Package

## Scope

Target candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Purpose: define the smallest external historical option-data request package needed to investigate the missing QQQ option/execution evidence without buying data, calling paid APIs, using credentials, writing ingestion code, filling evidence, or promoting the candidate.

This package is a request plan only. It does not prove option context, execution context, spread quality, fill quality, trade outcome, option P&L, or profitability.

## Candidate Details

| Field | Value |
| --- | --- |
| Candidate ID | `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` |
| Underlying symbol | `QQQ` |
| Setup type | `Clean Fast Break` |
| Signal date | `2026-04-13` |
| Signal/setup time | `2026-04-13T12:30:00-04:00` |
| Source session | `2026-04-13 regular session` |
| Source CSV | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv` |
| Source CSV row | line 132 |
| Replay log | `historical_signal_replay/reports/first_real_qqq_clean_fast_break_replay_v1_signal_log.jsonl` |
| Replay signal row | line 3 |
| Trigger level | `613.67` |
| Invalidation | `609.58` |
| Setup candle OHLCV | open `613.5`, high `614.8252`, low `612.57`, close `614.6`, volume `2010643.526251` |
| Option side already present | none found in candidate evidence |
| Target option expiration already present | none found in candidate evidence |
| Target option strike already present | none found in candidate evidence |
| Target option contract symbol already present | none found in candidate evidence |

Read-only local inventory found current on-demand option defaults of calls, 14-30 DTE, nearest 16 contracts, and 5-10 point debit-spread widths. Those defaults do not select a historical contract for this candidate. They only shape the external data request because the candidate itself does not contain a chosen expiration, strike, side, or option symbol.

## Exact Time Window Needed

Minimum historical option quote window:

- `2026-04-13T12:25:00-04:00` through `2026-04-13T12:35:00-04:00`.

Reason:

- The signal/setup time is exactly `2026-04-13T12:30:00-04:00`.
- The smallest useful option quote window must include the best quote at or immediately before the signal time and enough neighboring records to prove timestamp alignment, quote freshness, and spread stability.

Required chain metadata date:

- QQQ option chain metadata valid for `2026-04-13`.

Requested expiration range:

- Expirations from `2026-04-27` through `2026-05-13`, inclusive.

Reason:

- This is the 14-30 calendar-day window after the `2026-04-13` signal date, matching current read-only request-shaping defaults. If the vendor cannot filter by DTE, provide all QQQ expirations available on `2026-04-13` and Codex will filter after download.

Requested strike range:

- Minimum: QQQ strikes from `590` through `640`, inclusive, for both calls and puts.

Reason:

- Underlying was around `613.5` to `614.6` at signal time, trigger was `613.67`, and invalidation was `609.58`.
- The candidate lacks a chosen side and contract. The narrow strike band must still cover near-the-money contracts plus 5-10 point debit-spread pair candidates around the signal price and invalidation area.

If a vendor export is cheaper/easier only as a full chain snapshot, a full QQQ chain snapshot for the requested expirations at the requested time window is acceptable.

## Minimum Fields Needed

At the option-contract quote level:

- `underlying_symbol`
- `option_symbol` or OCC option identifier
- `quote_timestamp` with timezone or UTC offset
- `expiration_date`
- `strike_price`
- `option_type` or side, `C`/`P`
- `bid_price`
- `ask_price`
- `bid_size`
- `ask_size`
- `last_price` if available
- `mark_price` or midpoint if vendor supplies it
- `underlying_price` at quote time if vendor supplies it
- `data_vendor`
- `export_created_at` or file-generation timestamp, if available

At the chain metadata level:

- `underlying_symbol`
- `expiration_date`
- `days_to_expiration` if available
- `strike_price`
- `option_type`
- `option_symbol` or OCC option identifier
- settlement style / exercise style if available
- deliverable/multiplier if available

Codex validation can derive spread and midpoint from bid/ask if those derived fields are not present.

## Nice-To-Have Fields

- trade timestamp and trade price around the signal
- one-minute option OHLCV bars covering `2026-04-13T12:25:00-04:00` through `2026-04-13T12:35:00-04:00`
- option volume
- option open interest
- implied volatility
- delta, gamma, theta, vega
- exchange or venue
- quote condition flags
- NBBO indicator
- underlying NBBO or underlying trade price at quote time
- raw vendor symbol plus normalized OCC symbol

Nice-to-have fields are not a substitute for bid, ask, quote timestamp, expiration, strike, and option type.

## Databento-First Request Plan

Ask Databento for a historical QQQ options export with:

- Underlying: `QQQ`
- Date: `2026-04-13`
- Quote window: `2026-04-13T12:25:00-04:00` through `2026-04-13T12:35:00-04:00`
- Expirations: `2026-04-27` through `2026-05-13`, inclusive, or all QQQ expirations if DTE filtering is not supported at export time
- Strikes: `590` through `640`, inclusive, or full chain if strike filtering is not supported at export time
- Option types: calls and puts
- Data type: option quotes/NBBO if available, plus chain/security definition metadata
- Output: CSV, JSON, or ZIP containing CSV/JSON

Databento output should preserve exact timestamps and enough instrument metadata to map each quote row to expiration, strike, and option type. Do not request or include account, order, fill, broker, or real-money data.

## ThetaData Fallback Request Plan

If Databento cannot provide the package, ask ThetaData for the same bounded QQQ historical option package:

- Underlying: `QQQ`
- Date: `2026-04-13`
- Quote window: `2026-04-13T12:25:00-04:00` through `2026-04-13T12:35:00-04:00`
- Expirations: `2026-04-27` through `2026-05-13`, inclusive, or all QQQ expirations if easier
- Strikes: `590` through `640`, inclusive, or full chain if easier
- Option types: calls and puts
- Data type: historical option quote/NBBO rows plus chain/contract metadata
- Output: CSV, JSON, or ZIP containing CSV/JSON

The fallback package must still include quote timestamps, bid, ask, expiration, strike, option type, and option identifier. A daily end-of-day-only option file is not enough for this request.

## Accepted File Formats

Codex can accept these user-provided file types in the drop folder:

- `.csv`
- `.json`
- `.jsonl`
- `.zip` containing `.csv`, `.json`, or `.jsonl`

Preferred naming:

- `qqq_2026-04-13_1225-1235_option_quotes_databento.csv`
- `qqq_2026-04-13_chain_metadata_databento.csv`
- `qqq_2026-04-13_1225-1235_option_quotes_thetadata.csv`
- `qqq_2026-04-13_chain_metadata_thetadata.csv`

Exact filenames are not required, but filenames should include `QQQ`, `2026-04-13`, vendor name, and whether the file is quotes or chain metadata.

## Drop Location

Place downloaded files here:

```text
historical_signal_replay/source_data/external_option_data_drop/
```

Do not place credentials, API keys, account files, broker statements, orders, fills, or screenshots in this folder.

## Validation After Download

After files are placed in the drop folder, Codex should validate only the downloaded files and existing local evidence. The validation should not call vendor APIs, use credentials, buy data, write ingestion code, or edit evidence files unless a later task explicitly authorizes that.

Validation checklist:

1. Confirm every file is one of CSV, JSON, JSONL, or ZIP.
2. If ZIP files are present, inspect member names and reject unrelated or executable contents.
3. Confirm files are for `QQQ`, not SPY/IWM/GLD or another underlying.
4. Confirm the quote window covers `2026-04-13T12:25:00-04:00` through `2026-04-13T12:35:00-04:00`, or at minimum contains a valid quote at or immediately before `2026-04-13T12:30:00-04:00`.
5. Confirm chain metadata includes expiration, strike, option type, and option identifier.
6. Confirm quote rows include bid, ask, and quote timestamp.
7. Confirm expirations include the 14-30 DTE window from `2026-04-27` through `2026-05-13`, or document what is missing.
8. Confirm strikes include `590` through `640`, or document what is missing.
9. Compute simple derived fields for inspection only: midpoint, spread, spread percent, and nearest quote age relative to the signal timestamp.
10. Do not infer fills, P&L, profitability, or execution quality from quotes alone.
11. Do not mark `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` intake-ready from external files alone.

Expected validation output should be a docs-only review or local validation summary unless a later task authorizes code, tests, or evidence-file updates.

## What Still Cannot Be Proven After Files Arrive

Even if the option files arrive and validate structurally, they still cannot prove:

- SAFE-FAST `gap_context_status`, because QQQ CFB gap thresholds are not accepted yet.
- SAFE-FAST `gap_context_as_of` or `gap_context_reviewed_before_signal`, because those require an accepted no-hindsight gap-context rule and regressions.
- Clean Fast Break stale/spent expiry correctness, because that is a SAFE-FAST rule/regression artifact, not vendor option data.
- Actual fill quality, because historical quotes are not fills.
- Real account execution, order routing, slippage, partial fills, or cancel/replace behavior.
- Option P&L.
- Profitability.
- Candidate promotion or intake readiness.

The files can only support later review of whether historical option chain/quote/spread evidence existed around the QQQ signal time and whether the missing option/execution/caution fields can be evaluated under separate accepted SAFE-FAST rules.

## Current Status

External option data request package created: YES.

External data downloaded: NO.

Paid API called: NO.

Credentials used: NO.

Ingestion code written: NO.

Evidence files filled: NO.

QQQ candidate marked ready: NO.

Proof accepted: NO.

Profitability claimed: NO.
