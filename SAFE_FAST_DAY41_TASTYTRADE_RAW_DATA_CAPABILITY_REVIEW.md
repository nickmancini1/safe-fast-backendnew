# SAFE-FAST Day 41 Tastytrade Raw Data Capability Review

## Baseline

- Branch baseline from required task file: `main`.
- Verified HEAD: `6f1fff4 Add Day 41 raw tastytrade handoff`.
- Working tree before changes had one untracked task file: `SAFE_FAST_DAY41_TASTYTRADE_RAW_DATA_CAPABILITY_CODEX_TASK.md`.
- Mode: build-only docs/capability review.
- No live trading, broker/order/account work, Railway/deploy work, production work, proof claim, profitability claim, option P&L, sizing, alerts, `main.py` edit, helper/source-code patch, evidence-file edit, `.env` write, or secret output was performed.

## Files inspected

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`
- `SAFE_FAST_DAY41_RAW_TASTYTRADE_NEXT_CHAT_HANDOFF.md`
- `SAFE_FAST_DAY41_TASTYTRADE_RAW_DATA_CAPABILITY_CODEX_TASK.md`
- `dxlink_candles.py`
- `historical_signal_replay/export_dxlink_source_csv.py`
- `historical_signal_replay/source_data/richer_export_package_work/`
- `historical_signal_replay/source_data/richer_export_package_work/qqq_cfb_gap_context_completeness_fields_rule.jsonl`
- `historical_signal_replay/source_data/richer_export_package_work/qqq_cfb_complete_context_caution_fields.jsonl`
- `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`
- `historical_signal_replay/reports/first_real_qqq_clean_fast_break_replay_v1_signal_log.jsonl`
- Latest git history for `6f1fff4 Add Day 41 raw tastytrade handoff`
- Read-only `main.py` snippets around option-chain and market-data helpers, for capability inventory only; no endpoint was called and no edit was made.

## Helpers found

- `dxlink_candles.py`
  - Fetches a tastytrade quote token using `/api-quote-tokens`.
  - Opens a dxLink websocket.
  - Subscribes to `Candle` feed events.
  - Uses candle symbol shape like `QQQ{=h,a=s,tho=true}` for 1-hour regular-session-aligned candles.
  - Parses candle fields: `eventSymbol`, `time`, `sequence`, `count`, `open`, `high`, `low`, `close`, `volume`, `vwap`, `bidVolume`, `askVolume`, `impVolatility`, `openInterest`.
  - Computes an EMA50 snapshot and returns `all_candles`.
- `historical_signal_replay/export_dxlink_source_csv.py`
  - Read-only exporter for tastytrade/dxLink RTH OHLCV candles.
  - Supports symbols `SPY`, `QQQ`, `IWM`, and `GLD`.
  - Has `--dry-run`, which validates local setup without network requests or file writes.
  - Writes source CSV rows with `open`, `high`, `low`, `close`, `volume`, `source`, `source_as_of`, and `data_vendor`.
- Existing `main.py` contains current/live option-chain and quote helpers:
  - `/option-chains/{symbol}`
  - `/market-data`
  - `/market-data/by-type` with `equity-option`
  - These were inspected only as local code inventory. They were not used because this task forbids broker/order/account work, live trade decisions, and helper/code changes; they also do not establish historical option quote availability for the April 2026 target window.

## Safe commands run

- `git --no-pager status --short`
- `git --no-pager log -1 --oneline`
- `git --no-pager show --name-only --oneline -1`
- `rg --files | rg "(tasty|dxlink|dx|source_evidence|richer_export_package_work|DAY41|TASTYTRADE|RAW_DATA)"`
- `rg -n "(option|chain|quote|bid|ask|spread|openInterest|open_interest|Option|Quote|Greeks|Trade|Summary|Candle)" -g "*.py" .`
- `rg -n "export_dxlink|dxlink_candles|get_1h_ema50|TT_CLIENT|api-quote-tokens|option-chains|market-metrics|equity-option" tests historical_signal_replay watcher_foundation -g "*.py"`
- `Get-ChildItem` / `Get-Content` read-only file inspections.
- Environment-variable presence check that printed only `present` / `missing`.
- `python -B .\historical_signal_replay\export_dxlink_source_csv.py --symbol QQQ --dry-run`
- `python -B -m watcher_foundation.source_evidence_work_package_content_validator`
- `python -B -m watcher_foundation.source_evidence_package_to_intake_bridge`
- `python -B -m watcher_foundation.source_evidence_package_intake --validate-work-package`

Notes:
- `rg` reported access-denied warnings for local temp directories `tmpra392qh0` and `tmpt2fw63vq`; this did not block discovery of repo helper files.
- The exporter dry run made no network request and wrote no file.
- Validators/bridge are local and safe; they were run.

## Environment variable presence check, present/missing only

- `TT_CLIENT_ID`: missing
- `TT_CLIENT_SECRET`: missing
- `TT_REDIRECT_URI`: missing
- `TT_REFRESH_TOKEN`: missing

The dry-run helper reported the same four variables missing. No values, tokens, secrets, refresh tokens, credentials, or `.env` contents were printed.

## Candidate metadata found for QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001

- Candidate ID: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`
- Symbol: `QQQ`
- Setup type: `Clean Fast Break`
- Evidence target: QQQ CFB gap context
- Work file: `historical_signal_replay/source_data/richer_export_package_work/qqq_cfb_gap_context_completeness_fields_rule.jsonl`
- Source file: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`
- Replay log: `historical_signal_replay/reports/first_real_qqq_clean_fast_break_replay_v1_signal_log.jsonl`
- Source row reference from work package: CSV line 132
- Replay log reference from work package: lines 3-4
- Known trigger: `613.67`
- Known invalidation: `609.58`
- Rule family: `Clean Fast Break gap context`
- Request ID: `qqq_cfb_gap_context_completeness_fields_rule`

## Signal timestamp or target window found

- Signal/setup candle timestamp: `2026-04-13T12:30:00-04:00`
- Source session: `2026-04-13 regular session`
- No-hindsight boundary carried by work package: setup-time row and replay log line 3 only; no future rows used for signal.
- Same-session follow-through/spent context is represented by replay log line 4 and must not be used to backfill setup-time gap context.

## Raw underlying candle capability

Current local tastytrade/dxLink helpers can fetch and export historical-style underlying RTH candles for QQQ around the target window, as shown by existing local source CSV rows marked:

- `source`: `dxlink_candles.get_1h_ema50_snapshot`
- `source_as_of`: `2026-05-15T18:48:44Z`
- `data_vendor`: `dxFeed via tastytrade dxLink`
- `timeframe`: `1h_rth`

The target row and surrounding rows are present in `first_real_historical_replay_v1_QQQ_source.csv`.

## Previous close / signal-day open capability

Current local source CSV rows are sufficient to identify the previous regular-session final 1h candle close and the signal-day opening 1h candle open, but only at the exported 1h RTH candle resolution.

- Previous regular-session final exported candle before signal day:
  - Timestamp: `2026-04-10T15:30:00-04:00`
  - Close: `611.02`
  - Source timestamp: `2026-05-15T18:48:44Z`
- Signal-day first exported RTH candle:
  - Timestamp: `2026-04-13T09:30:00-04:00`
  - Open: `609.455`
  - Source timestamp: `2026-05-15T18:48:44Z`

This supports raw gap calculation from available underlying candles. It does not by itself prove the SAFE-FAST labels `gap_context_status`, `gap_context_as_of`, or `gap_context_reviewed_before_signal`, because those labels must be calculated and recorded by SAFE-FAST from raw inputs under a defined rule.

## Intraday-through-signal-only capability

Current local source CSV rows can provide intraday 1h RTH bars through the signal time only:

- `2026-04-13T09:30:00-04:00`: open `609.455`, high `612.25`, low `608.11`, close `611.338`, volume `4001989.454556`
- `2026-04-13T10:30:00-04:00`: open `611.375`, high `612.88`, low `610.94`, close `611.7999`, volume `1862974.043705`
- `2026-04-13T11:30:00-04:00`: open `611.76`, high `613.76`, low `611.07`, close `613.49`, volume `1665431.815635`
- `2026-04-13T12:30:00-04:00`: open `613.5`, high `614.8252`, low `612.57`, close `614.6`, volume `2010643.526251`

Rows after `2026-04-13T12:30:00-04:00` exist locally but are not needed for setup-time gap context and must not be used for no-hindsight evidence fill.

## Historical option chain capability

Unavailable from the current allowed helpers.

- `dxlink_candles.py` does not fetch option chains.
- `export_dxlink_source_csv.py` does not fetch option chains.
- Read-only code inventory found current/live option-chain helper code in `main.py`, but that does not prove historical option-chain availability around `2026-04-13T12:30:00-04:00`, and this task does not allow using live app/broker-style endpoints to fill evidence.

Classification:
- Current helper: unavailable.
- Possibly available from tastytrade through another endpoint/helper: unproven from the local allowed helper surface; would require a separate safe data-only historical-option-chain helper or official/vendor-backed evidence.
- Not available from tastytrade historical access requiring another source: not proven by this local review.

## Historical option bid/ask quote capability

Unavailable from the current allowed helpers.

- `dxlink_candles.py` subscribes only to `Candle` events.
- `export_dxlink_source_csv.py` exports only underlying OHLCV and unconfirmed context fields.
- Read-only code inventory found current/live quote helpers in `main.py`, including `market-data/by-type` for `equity-option`, but this does not establish historical bid/ask quote availability for the target window.

Classification:
- Current helper: unavailable.
- Possibly available from tastytrade through another endpoint/helper: possible only if a safe historical quote endpoint/helper is proven separately.
- Not available from tastytrade historical access requiring another source: not proven by this local review.

## Spread and quote timestamp capability

Unavailable from the current allowed helpers for historical option evidence.

- Underlying candle rows have candle timestamps and `source_as_of`.
- The current exported CSV does not include option bid, option ask, option mid, option mark, option last, quote timestamp, per-leg spread, or spread timestamp fields.
- Existing `main.py` can calculate spread-related values from current quote payloads, but no historical option quote timestamp capability was proven from the allowed helpers.

Classification:
- Current helper: unavailable for historical options.
- Possibly available from tastytrade through another endpoint/helper: possible only if a safe historical option quote endpoint/helper is proven separately.
- Not available from tastytrade historical access requiring another source: not proven by this local review.

## Expiration / strike metadata capability

Unavailable from the current allowed helpers for the historical target window.

- `dxlink_candles.py` has no option-chain metadata fetch.
- `export_dxlink_source_csv.py` has no expiration or strike fields.
- Read-only code inventory found current/live option-chain parsing in `main.py` for `expiration-date`, `days-to-expiration`, `strike-price`, `option-type`, and option `symbol`, but that is not a historical evidence helper for this task.

Classification:
- Current helper: unavailable.
- Possibly available from tastytrade through another endpoint/helper: possible only if a safe data-only chain metadata helper is created and tested later.
- Not available from tastytrade historical access requiring another source: not proven by this local review.

## Option volume / open interest capability

Unavailable from the current allowed helpers for historical option contracts.

- `dxlink_candles.py` includes `openInterest`, `impVolatility`, `bidVolume`, and `askVolume` in the Candle event field list, but the current source CSV exporter does not preserve these fields.
- For the target evidence need, the current helper surface does not fetch historical option-contract volume or option-contract open interest around signal time.
- Underlying candle `volume` is available in the CSV; it is not option volume.

Classification:
- Current helper: unavailable for historical option contracts.
- Possibly available from tastytrade through another endpoint/helper: possible only if a safe option-chain/quote/metrics helper proves it.
- Not available from tastytrade historical access requiring another source: not proven by this local review.

## Exact raw fields found, with source timestamps if available

From `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`:

- Header fields: `symbol`, `timestamp`, `timezone`, `session_date`, `session_type`, `regular_session`, `timeframe`, `open`, `high`, `low`, `close`, `volume`, `source`, `source_as_of`, `data_vendor`, `context_24h_status`, `context_24h_as_of`, `macro_context_status`, `macro_context_as_of`, `iv_context_status`, `iv_context_as_of`, `event_context_status`, `event_context_as_of`, `notes`
- Previous-session final exported RTH candle:
  - `symbol`: `QQQ`
  - `timestamp`: `2026-04-10T15:30:00-04:00`
  - `open`: `611.31`
  - `high`: `611.31`
  - `low`: `610.46`
  - `close`: `611.02`
  - `volume`: `1882110.36406`
  - `source`: `dxlink_candles.get_1h_ema50_snapshot`
  - `source_as_of`: `2026-05-15T18:48:44Z`
  - `data_vendor`: `dxFeed via tastytrade dxLink`
- Signal-day open exported RTH candle:
  - `timestamp`: `2026-04-13T09:30:00-04:00`
  - `open`: `609.455`
  - `high`: `612.25`
  - `low`: `608.11`
  - `close`: `611.338`
  - `volume`: `4001989.454556`
  - `source_as_of`: `2026-05-15T18:48:44Z`
- Signal/setup candle:
  - `timestamp`: `2026-04-13T12:30:00-04:00`
  - `open`: `613.5`
  - `high`: `614.8252`
  - `low`: `612.57`
  - `close`: `614.6`
  - `volume`: `2010643.526251`
  - `source_as_of`: `2026-05-15T18:48:44Z`

From `historical_signal_replay/reports/first_real_qqq_clean_fast_break_replay_v1_signal_log.jsonl` setup-time signal row:

- `timestamp`: `2026-04-13T12:30:00-04:00`
- `symbol`: `QQQ`
- `setup_type`: `Clean Fast Break`
- `current_state`: `signal`
- `stage`: `clean_fast_break_initial_break_candidate`
- `trigger_state`: `triggered`
- `trigger_level`: `613.67`
- `invalidation`: `609.58`
- `context_24h`: `CONTEXT_24H_DAILY_UNCONFIRMED`
- `cautions_watchouts`: `MACRO_UNCONFIRMED`, `IV_UNCONFIRMED`, `EVENT_UNCONFIRMED`
- `primary_blocker`: null

## Missing fields

For QQQ CFB gap-context evidence:

- `gap_context_status`
- `gap_context_as_of`
- `gap_context_reviewed_before_signal`

For option/execution/caution context that may become relevant after gap context:

- historical option chain around signal time
- historical option bid
- historical option ask
- historical option quote timestamp
- historical option spread
- expiration metadata
- strike metadata
- option volume
- option open interest
- source timestamp proving option data was available before or at signal time

## Missing-field classification

| Field or capability | Classification | Reason |
| --- | --- | --- |
| `gap_context_status` | unavailable from current helper as a label; calculable by SAFE-FAST only after a rule uses raw candles | The raw previous close, signal-day open, and through-signal candles exist locally, but no current helper calculates/stores this SAFE-FAST label. |
| `gap_context_as_of` | unavailable from current helper as a label; calculable by SAFE-FAST only after a rule uses raw candles | Source rows have `source_as_of`, but no reviewed gap-context label timestamp exists. |
| `gap_context_reviewed_before_signal` | unavailable from current helper as a label; calculable by SAFE-FAST only after a no-hindsight rule uses raw candles | No current artifact records a completed pre-signal gap review. |
| Historical option chain | unavailable from current helper; possibly available through another endpoint/helper | Current allowed dxLink exporter is underlying-candle only. |
| Historical option bid/ask quotes | unavailable from current helper; possibly available through another endpoint/helper | Current allowed helper does not subscribe to option quote events or call a historical quote endpoint. |
| Spread and quote timestamps | unavailable from current helper; possibly available through another endpoint/helper | Requires historical option bid/ask plus timestamps; not present locally. |
| Expiration / strike metadata | unavailable from current helper; possibly available through another endpoint/helper | Current/live chain parser exists in `main.py`, but no safe historical helper exists. |
| Option volume / open interest | unavailable from current helper; possibly available through another endpoint/helper | Underlying candle volume exists; historical option volume/open interest is not present in the allowed helper output. |
| Fields requiring another data source | not proven by this local review | This review did not establish that tastytrade cannot provide historical option evidence; it established only that current allowed local helpers cannot. |

## Whether QQQ CFB gap-context evidence can be filled now

No.

The raw underlying candle rows needed to calculate a gap are present locally, but the required work-package fields are SAFE-FAST review labels:

- `gap_context_status`
- `gap_context_as_of`
- `gap_context_reviewed_before_signal`

Those labels are still missing from accepted source-backed evidence. Filling them directly from the current source CSV would be a fake label fill unless SAFE-FAST first defines and tests the gap-context calculation/review rule against raw candles with the no-hindsight boundary.

## Exact blocker and next evidence-backed source path

Blocker:
- Current allowed tastytrade/dxLink helpers provide local underlying 1h RTH OHLCV rows for QQQ, but they do not provide accepted SAFE-FAST gap-context label rows and do not provide historical option chain/quote/spread/timestamp evidence for the target window.

Next evidence-backed source path:
- Build a separate safe data-only gap-context calculation artifact from the existing raw underlying candles, with regression tests proving:
  - previous-session close is selected without hindsight,
  - signal-day open is selected correctly,
  - intraday bars are clipped through `2026-04-13T12:30:00-04:00`,
  - `gap_context_status`, `gap_context_as_of`, and `gap_context_reviewed_before_signal` are calculated deterministically,
  - future bars after signal time cannot affect the labels.
- Separately, investigate a safe data-only historical option-chain/quote helper or source-backed package for historical option bid/ask, quote timestamps, spread, expiration, strike, volume, and open interest. Do not use broker/order/account endpoints and do not edit live trading or `main.py` code for that work.

## Validator state

- Work-package structure validation: 9 files passed, 0 files failed.
- Work-package content validation: 0 passed requests, 9 failed requests, 9 partial rows, 0 header-only rows.
- Evidence-package-to-intake bridge: 0 reconsideration-eligible candidates.
- Intake-ready candidates: 0.
- Proof accepted: NO.
- Profitability claim made: NO.
