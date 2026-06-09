# SAFE-FAST IWM/GLD Setup-Time Review Row-Context Packets

Project day: Day 37
Current baseline commit: `3534497 Add IWM GLD setup-time review completion worksheet`
Mode: row-context evidence packet for setup-time review completion only

## Purpose And Boundary

This packet collects row-context evidence for review. It is not accepted proof and does not accept setup-time rows, trigger, invalidation, freshness, blockers, terminal outcomes, profitability, trade readiness, shadow readiness, live readiness, or production readiness.

- accepted_proof=false
- accepted_proof_count=0
- No live trading, live data, alerts, broker/order/account/options/P&L, account sizing, shadow, production, Railway, real money, or live trade decision is authorized.

## Source Files Used

- `SAFE_FAST_BUILD_STATE.md` latest Day 37 setup-time/request/completion/holding-period sections only
- `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md` top rules and latest Day 37 sections only
- `SAFE_FAST_IWM_GLD_SETUP_TIME_REVIEW_COMPLETION_WORKSHEET.md`
- `SAFE_FAST_IWM_GLD_SETUP_TIME_REVIEW_REQUEST_PACKETS.md`
- `SAFE_FAST_IWM_GLD_SOURCE_WINDOW_EXTRACTION_APPLICATION_REVIEW.md`
- `SAFE_FAST_REAL_HISTORICAL_IWM_GLD_MISSING_EVIDENCE_INVENTORY.md`
- `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv` rows 141-210 and 190-210 only
- `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv` rows 204-238 only

Worksheet file referenced: `SAFE_FAST_IWM_GLD_SETUP_TIME_REVIEW_COMPLETION_WORKSHEET.md`.

Request packet file referenced: `SAFE_FAST_IWM_GLD_SETUP_TIME_REVIEW_REQUEST_PACKETS.md`.

## Reviewer Warning

- Directionally favorable after-setup movement is not accepted proof.
- Trigger and invalidation must be setup-time accepted fields.
- Unavailable fields must be marked `UNAVAILABLE`.
- Missing evidence is a blocker, not low confidence.
- `ready_for_packet_build_review` is not accepted proof.

## IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001

- candidate_id: `IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001`
- symbol: `IWM`
- setup_type: `Continuation`
- source_file_label: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv`
- old_source_window_id: `IWM-WINDOW-CONTINUATION-001`
- old_source_sample_id: `IWM-SAMPLE-CONTINUATION-001`
- row_start: 141
- row_end: 210
- candidate_review_rows: rows 141-210
- setup_time_review_request_status: `ready_for_setup_time_review_request`
- completion_status: `TO_BE_COMPLETED`
- watch_only=true
- no_trade_decision=true
- accepted_proof=false

### Required Fields Still To Complete

- setup_time_source_row_number: `UNAVAILABLE`
- setup_time_timestamp: `UNAVAILABLE`
- setup_time_row_ohlcv: `UNAVAILABLE`
- accepted_setup_identity: `UNAVAILABLE`
- accepted_final_verdict: `UNAVAILABLE`
- accepted_trigger_state: `UNAVAILABLE`
- accepted_numeric_trigger: `UNAVAILABLE`
- accepted_trigger_basis: `UNAVAILABLE`
- accepted_numeric_invalidation: `UNAVAILABLE`
- accepted_invalidation_basis: `UNAVAILABLE`
- accepted_freshness_final_signal_decision: `UNAVAILABLE`
- accepted_blocker_caution_decision: `UNAVAILABLE`
- no_hindsight_boundary_statement: `UNAVAILABLE`
- after_setup_outcome_window_start: `UNAVAILABLE`
- after_setup_outcome_window_end: `UNAVAILABLE`

### Row-Context Table

| source_row_number | timestamp | open | high | low | close | volume | symbol | timezone | session_date | session_type | regular_session | timeframe | source | source_as_of | data_vendor | context_24h_status | context_24h_as_of | macro_context_status | macro_context_as_of | iv_context_status | iv_context_as_of | event_context_status | event_context_as_of | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 141 | 2026-04-20T09:30:00-04:00 | 274.64 | 276.66 | 274.53 | 276.435 | 1627381.0 | IWM | America/New_York | 2026-04-20 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 142 | 2026-04-20T10:30:00-04:00 | 276.43 | 277.08 | 275.45 | 276.965 | 1735195.823861 | IWM | America/New_York | 2026-04-20 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 143 | 2026-04-20T11:30:00-04:00 | 276.93 | 277.3007 | 276.45 | 276.5 | 713535.0 | IWM | America/New_York | 2026-04-20 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 144 | 2026-04-20T12:30:00-04:00 | 276.51 | 277.035 | 276.225 | 276.75 | 892944.0 | IWM | America/New_York | 2026-04-20 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 145 | 2026-04-20T13:30:00-04:00 | 276.795 | 277.17 | 276.32 | 277.03 | 745645.646347 | IWM | America/New_York | 2026-04-20 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 146 | 2026-04-20T14:30:00-04:00 | 277.1 | 277.665 | 276.93 | 277.27 | 1228079.0 | IWM | America/New_York | 2026-04-20 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 147 | 2026-04-20T15:30:00-04:00 | 277.265 | 277.42 | 276.99 | 277.34 | 1018987.0 | IWM | America/New_York | 2026-04-20 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 148 | 2026-04-21T09:30:00-04:00 | 278.16 | 279.79 | 277.54 | 279.62 | 1498240.10513 | IWM | America/New_York | 2026-04-21 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 149 | 2026-04-21T10:30:00-04:00 | 279.63 | 279.77 | 275.99 | 276.305 | 2079668.888324 | IWM | America/New_York | 2026-04-21 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 150 | 2026-04-21T11:30:00-04:00 | 276.3 | 276.79 | 275.72 | 275.95 | 1299760.0 | IWM | America/New_York | 2026-04-21 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 151 | 2026-04-21T12:30:00-04:00 | 275.93 | 276.29 | 274.26 | 274.72 | 1198775.0 | IWM | America/New_York | 2026-04-21 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 152 | 2026-04-21T13:30:00-04:00 | 274.72 | 276.31 | 274.3 | 274.71 | 1250923.0 | IWM | America/New_York | 2026-04-21 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 153 | 2026-04-21T14:30:00-04:00 | 274.7 | 276.54 | 274.7 | 276.435 | 1536840.0 | IWM | America/New_York | 2026-04-21 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 154 | 2026-04-21T15:30:00-04:00 | 276.42 | 276.5 | 273.76 | 274.53 | 2206925.0 | IWM | America/New_York | 2026-04-21 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 155 | 2026-04-22T09:30:00-04:00 | 277.61 | 278.01 | 276.505 | 276.63 | 1883261.58897 | IWM | America/New_York | 2026-04-22 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 156 | 2026-04-22T10:30:00-04:00 | 276.61 | 276.92 | 275.94 | 276.4 | 1022374.82389 | IWM | America/New_York | 2026-04-22 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 157 | 2026-04-22T11:30:00-04:00 | 276.395 | 276.65 | 275.3914 | 275.51 | 774298.0 | IWM | America/New_York | 2026-04-22 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 158 | 2026-04-22T12:30:00-04:00 | 275.5 | 275.9 | 274.9 | 275.89 | 1006681.0 | IWM | America/New_York | 2026-04-22 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 159 | 2026-04-22T13:30:00-04:00 | 275.9 | 276.03 | 275.31 | 275.52 | 554494.0 | IWM | America/New_York | 2026-04-22 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 160 | 2026-04-22T14:30:00-04:00 | 275.53 | 276.08 | 275.33 | 276.03 | 612106.0 | IWM | America/New_York | 2026-04-22 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 161 | 2026-04-22T15:30:00-04:00 | 276.03 | 276.56 | 275.72 | 276.48 | 670929.0 | IWM | America/New_York | 2026-04-22 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 162 | 2026-04-23T09:30:00-04:00 | 276.74 | 277.54 | 275.77 | 276.87 | 1921775.0 | IWM | America/New_York | 2026-04-23 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 163 | 2026-04-23T10:30:00-04:00 | 276.86 | 277.86 | 276.74 | 277.42 | 957606.0 | IWM | America/New_York | 2026-04-23 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 164 | 2026-04-23T11:30:00-04:00 | 277.45 | 277.69 | 276.35 | 276.515 | 723566.0 | IWM | America/New_York | 2026-04-23 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 165 | 2026-04-23T12:30:00-04:00 | 276.54 | 276.95 | 273.67 | 273.83 | 1971164.0 | IWM | America/New_York | 2026-04-23 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 166 | 2026-04-23T13:30:00-04:00 | 273.8 | 275.57 | 271.96 | 275.55 | 2867679.0 | IWM | America/New_York | 2026-04-23 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 167 | 2026-04-23T14:30:00-04:00 | 275.555 | 275.8 | 274.48 | 275.12 | 966722.0 | IWM | America/New_York | 2026-04-23 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 168 | 2026-04-23T15:30:00-04:00 | 275.08 | 275.75 | 274.43 | 275.53 | 795622.0 | IWM | America/New_York | 2026-04-23 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 169 | 2026-04-24T09:30:00-04:00 | 276.67 | 277.29 | 274.2354 | 275.755 | 2004110.0 | IWM | America/New_York | 2026-04-24 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 170 | 2026-04-24T10:30:00-04:00 | 275.79 | 276.48 | 275.618 | 276.3 | 660480.0 | IWM | America/New_York | 2026-04-24 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 171 | 2026-04-24T11:30:00-04:00 | 276.31 | 278.13 | 276.15 | 277.35 | 1769360.101587 | IWM | America/New_York | 2026-04-24 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 172 | 2026-04-24T12:30:00-04:00 | 277.38 | 277.74 | 276.89 | 277.18 | 576808.0 | IWM | America/New_York | 2026-04-24 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 173 | 2026-04-24T13:30:00-04:00 | 277.158 | 277.74 | 276.78 | 276.94 | 798103.074974 | IWM | America/New_York | 2026-04-24 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 174 | 2026-04-24T14:30:00-04:00 | 276.94 | 277.27 | 276.63 | 276.8179 | 822579.0 | IWM | America/New_York | 2026-04-24 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 175 | 2026-04-24T15:30:00-04:00 | 276.77 | 277.01 | 276.3 | 276.64 | 834904.559301 | IWM | America/New_York | 2026-04-24 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 176 | 2026-04-27T09:30:00-04:00 | 276.83 | 278.24 | 276.25 | 276.78 | 2000931.0 | IWM | America/New_York | 2026-04-27 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 177 | 2026-04-27T10:30:00-04:00 | 276.77 | 277.61 | 276.26 | 276.49 | 806403.774881 | IWM | America/New_York | 2026-04-27 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 178 | 2026-04-27T11:30:00-04:00 | 276.5 | 277.05 | 276.42 | 276.66 | 367927.0 | IWM | America/New_York | 2026-04-27 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 179 | 2026-04-27T12:30:00-04:00 | 276.675 | 277.0 | 276.45 | 276.945 | 355166.0 | IWM | America/New_York | 2026-04-27 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 180 | 2026-04-27T13:30:00-04:00 | 276.91 | 277.19 | 276.43 | 276.74 | 548413.0 | IWM | America/New_York | 2026-04-27 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 181 | 2026-04-27T14:30:00-04:00 | 276.73 | 277.135 | 276.64 | 276.9499 | 603657.0 | IWM | America/New_York | 2026-04-27 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 182 | 2026-04-27T15:30:00-04:00 | 276.93 | 277.15 | 276.74 | 277.1 | 817767.0 | IWM | America/New_York | 2026-04-27 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 183 | 2026-04-28T09:30:00-04:00 | 276.04 | 276.97 | 273.74 | 273.79 | 2152984.0 | IWM | America/New_York | 2026-04-28 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 184 | 2026-04-28T10:30:00-04:00 | 273.78 | 274.17 | 272.915 | 273.55 | 1432584.595872 | IWM | America/New_York | 2026-04-28 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 185 | 2026-04-28T11:30:00-04:00 | 273.56 | 273.695 | 273.09 | 273.56 | 715553.0 | IWM | America/New_York | 2026-04-28 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 186 | 2026-04-28T12:30:00-04:00 | 273.54 | 273.7255 | 273.11 | 273.455 | 435928.0 | IWM | America/New_York | 2026-04-28 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 187 | 2026-04-28T13:30:00-04:00 | 273.45 | 273.95 | 273.42 | 273.86 | 512361.0 | IWM | America/New_York | 2026-04-28 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 188 | 2026-04-28T14:30:00-04:00 | 273.86 | 274.12 | 273.47 | 273.485 | 1044809.0 | IWM | America/New_York | 2026-04-28 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 189 | 2026-04-28T15:30:00-04:00 | 273.48 | 273.97 | 273.27 | 273.92 | 999391.0 | IWM | America/New_York | 2026-04-28 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 190 | 2026-04-29T09:30:00-04:00 | 273.92 | 274.38 | 272.51 | 273.105 | 1578364.58579 | IWM | America/New_York | 2026-04-29 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 191 | 2026-04-29T10:30:00-04:00 | 273.08 | 273.5 | 272.02 | 272.41 | 1063150.830347 | IWM | America/New_York | 2026-04-29 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 192 | 2026-04-29T11:30:00-04:00 | 272.41 | 272.5 | 271.06 | 271.27 | 1949852.0 | IWM | America/New_York | 2026-04-29 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 193 | 2026-04-29T12:30:00-04:00 | 271.25 | 271.54 | 270.85 | 271.38 | 802697.0 | IWM | America/New_York | 2026-04-29 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 194 | 2026-04-29T13:30:00-04:00 | 271.41 | 271.87 | 270.41 | 270.83 | 899334.662642 | IWM | America/New_York | 2026-04-29 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 195 | 2026-04-29T14:30:00-04:00 | 270.86 | 272.02 | 270.37 | 271.53 | 1081930.0 | IWM | America/New_York | 2026-04-29 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 196 | 2026-04-29T15:30:00-04:00 | 271.51 | 272.16 | 271.13 | 272.07 | 1323900.0 | IWM | America/New_York | 2026-04-29 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 197 | 2026-04-30T09:30:00-04:00 | 273.13 | 274.19 | 272.44 | 274.19 | 2106451.0 | IWM | America/New_York | 2026-04-30 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 198 | 2026-04-30T10:30:00-04:00 | 274.12 | 276.11 | 273.9 | 276.0121 | 1227417.606375 | IWM | America/New_York | 2026-04-30 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 199 | 2026-04-30T11:30:00-04:00 | 276.02 | 276.27 | 275.48 | 276.25 | 874646.0 | IWM | America/New_York | 2026-04-30 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 200 | 2026-04-30T12:30:00-04:00 | 276.255 | 276.61 | 275.985 | 276.61 | 634600.0 | IWM | America/New_York | 2026-04-30 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 201 | 2026-04-30T13:30:00-04:00 | 276.61 | 277.34 | 276.61 | 277.29 | 738711.995886 | IWM | America/New_York | 2026-04-30 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 202 | 2026-04-30T14:30:00-04:00 | 277.31 | 277.96 | 277.215 | 277.76 | 1148054.0 | IWM | America/New_York | 2026-04-30 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 203 | 2026-04-30T15:30:00-04:00 | 277.76 | 278.22 | 277.565 | 277.92 | 1380866.0 | IWM | America/New_York | 2026-04-30 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 204 | 2026-05-01T09:30:00-04:00 | 278.66 | 279.52 | 276.58 | 278.99 | 3310047.630359 | IWM | America/New_York | 2026-05-01 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 205 | 2026-05-01T10:30:00-04:00 | 279.0 | 279.0 | 277.845 | 278.63 | 1171394.753966 | IWM | America/New_York | 2026-05-01 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 206 | 2026-05-01T11:30:00-04:00 | 278.625 | 279.36 | 278.44 | 278.56 | 1216393.0 | IWM | America/New_York | 2026-05-01 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 207 | 2026-05-01T12:30:00-04:00 | 278.505 | 279.45 | 278.24 | 279.43 | 715233.69271 | IWM | America/New_York | 2026-05-01 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 208 | 2026-05-01T13:30:00-04:00 | 279.42 | 279.69 | 278.93 | 279.55 | 646164.04331 | IWM | America/New_York | 2026-05-01 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 209 | 2026-05-01T14:30:00-04:00 | 279.53 | 279.81 | 278.92 | 279.63 | 820141.0 | IWM | America/New_York | 2026-05-01 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 210 | 2026-05-01T15:30:00-04:00 | 279.64 | 279.68 | 279.175 | 279.3 | 1096393.52851 | IWM | America/New_York | 2026-05-01 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |

## IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002

- candidate_id: `IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002`
- symbol: `IWM`
- setup_type: `Continuation`
- source_file_label: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv`
- old_source_window_id: `IWM-WINDOW-SESSION-BOUNDARY-001`
- old_source_sample_id: `IWM-SAMPLE-SESSION-BOUNDARY-001`
- row_start: 190
- row_end: 210
- candidate_review_rows: rows 190-210
- setup_time_review_request_status: `ready_for_setup_time_review_request`
- completion_status: `TO_BE_COMPLETED`
- watch_only=true
- no_trade_decision=true
- accepted_proof=false

### Required Fields Still To Complete

- setup_time_source_row_number: `UNAVAILABLE`
- setup_time_timestamp: `UNAVAILABLE`
- setup_time_row_ohlcv: `UNAVAILABLE`
- accepted_setup_identity: `UNAVAILABLE`
- accepted_final_verdict: `UNAVAILABLE`
- accepted_trigger_state: `UNAVAILABLE`
- accepted_numeric_trigger: `UNAVAILABLE`
- accepted_trigger_basis: `UNAVAILABLE`
- accepted_numeric_invalidation: `UNAVAILABLE`
- accepted_invalidation_basis: `UNAVAILABLE`
- accepted_freshness_final_signal_decision: `UNAVAILABLE`
- accepted_blocker_caution_decision: `UNAVAILABLE`
- no_hindsight_boundary_statement: `UNAVAILABLE`
- after_setup_outcome_window_start: `UNAVAILABLE`
- after_setup_outcome_window_end: `UNAVAILABLE`

### Row-Context Table

| source_row_number | timestamp | open | high | low | close | volume | symbol | timezone | session_date | session_type | regular_session | timeframe | source | source_as_of | data_vendor | context_24h_status | context_24h_as_of | macro_context_status | macro_context_as_of | iv_context_status | iv_context_as_of | event_context_status | event_context_as_of | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 190 | 2026-04-29T09:30:00-04:00 | 273.92 | 274.38 | 272.51 | 273.105 | 1578364.58579 | IWM | America/New_York | 2026-04-29 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 191 | 2026-04-29T10:30:00-04:00 | 273.08 | 273.5 | 272.02 | 272.41 | 1063150.830347 | IWM | America/New_York | 2026-04-29 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 192 | 2026-04-29T11:30:00-04:00 | 272.41 | 272.5 | 271.06 | 271.27 | 1949852.0 | IWM | America/New_York | 2026-04-29 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 193 | 2026-04-29T12:30:00-04:00 | 271.25 | 271.54 | 270.85 | 271.38 | 802697.0 | IWM | America/New_York | 2026-04-29 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 194 | 2026-04-29T13:30:00-04:00 | 271.41 | 271.87 | 270.41 | 270.83 | 899334.662642 | IWM | America/New_York | 2026-04-29 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 195 | 2026-04-29T14:30:00-04:00 | 270.86 | 272.02 | 270.37 | 271.53 | 1081930.0 | IWM | America/New_York | 2026-04-29 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 196 | 2026-04-29T15:30:00-04:00 | 271.51 | 272.16 | 271.13 | 272.07 | 1323900.0 | IWM | America/New_York | 2026-04-29 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 197 | 2026-04-30T09:30:00-04:00 | 273.13 | 274.19 | 272.44 | 274.19 | 2106451.0 | IWM | America/New_York | 2026-04-30 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 198 | 2026-04-30T10:30:00-04:00 | 274.12 | 276.11 | 273.9 | 276.0121 | 1227417.606375 | IWM | America/New_York | 2026-04-30 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 199 | 2026-04-30T11:30:00-04:00 | 276.02 | 276.27 | 275.48 | 276.25 | 874646.0 | IWM | America/New_York | 2026-04-30 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 200 | 2026-04-30T12:30:00-04:00 | 276.255 | 276.61 | 275.985 | 276.61 | 634600.0 | IWM | America/New_York | 2026-04-30 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 201 | 2026-04-30T13:30:00-04:00 | 276.61 | 277.34 | 276.61 | 277.29 | 738711.995886 | IWM | America/New_York | 2026-04-30 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 202 | 2026-04-30T14:30:00-04:00 | 277.31 | 277.96 | 277.215 | 277.76 | 1148054.0 | IWM | America/New_York | 2026-04-30 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 203 | 2026-04-30T15:30:00-04:00 | 277.76 | 278.22 | 277.565 | 277.92 | 1380866.0 | IWM | America/New_York | 2026-04-30 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 204 | 2026-05-01T09:30:00-04:00 | 278.66 | 279.52 | 276.58 | 278.99 | 3310047.630359 | IWM | America/New_York | 2026-05-01 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 205 | 2026-05-01T10:30:00-04:00 | 279.0 | 279.0 | 277.845 | 278.63 | 1171394.753966 | IWM | America/New_York | 2026-05-01 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 206 | 2026-05-01T11:30:00-04:00 | 278.625 | 279.36 | 278.44 | 278.56 | 1216393.0 | IWM | America/New_York | 2026-05-01 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 207 | 2026-05-01T12:30:00-04:00 | 278.505 | 279.45 | 278.24 | 279.43 | 715233.69271 | IWM | America/New_York | 2026-05-01 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 208 | 2026-05-01T13:30:00-04:00 | 279.42 | 279.69 | 278.93 | 279.55 | 646164.04331 | IWM | America/New_York | 2026-05-01 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 209 | 2026-05-01T14:30:00-04:00 | 279.53 | 279.81 | 278.92 | 279.63 | 820141.0 | IWM | America/New_York | 2026-05-01 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 210 | 2026-05-01T15:30:00-04:00 | 279.64 | 279.68 | 279.175 | 279.3 | 1096393.52851 | IWM | America/New_York | 2026-05-01 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-19T01:47:01Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |

## GLD-REPLACEMENT-IDEAL-CANDIDATE-001

- candidate_id: `GLD-REPLACEMENT-IDEAL-CANDIDATE-001`
- symbol: `GLD`
- setup_type: `Ideal`
- source_file_label: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv`
- old_source_window_id: `GLD-WINDOW-IDEAL-001`
- old_source_sample_id: `GLD-SAMPLE-IDEAL-001`
- row_start: 204
- row_end: 238
- candidate_review_rows: rows 204-238
- setup_time_review_request_status: `ready_for_setup_time_review_request`
- completion_status: `TO_BE_COMPLETED`
- watch_only=true
- no_trade_decision=true
- accepted_proof=false

### Required Fields Still To Complete

- setup_time_source_row_number: `UNAVAILABLE`
- setup_time_timestamp: `UNAVAILABLE`
- setup_time_row_ohlcv: `UNAVAILABLE`
- accepted_setup_identity: `UNAVAILABLE`
- accepted_final_verdict: `UNAVAILABLE`
- accepted_trigger_state: `UNAVAILABLE`
- accepted_numeric_trigger: `UNAVAILABLE`
- accepted_trigger_basis: `UNAVAILABLE`
- accepted_numeric_invalidation: `UNAVAILABLE`
- accepted_invalidation_basis: `UNAVAILABLE`
- accepted_freshness_final_signal_decision: `UNAVAILABLE`
- accepted_blocker_caution_decision: `UNAVAILABLE`
- no_hindsight_boundary_statement: `UNAVAILABLE`
- after_setup_outcome_window_start: `UNAVAILABLE`
- after_setup_outcome_window_end: `UNAVAILABLE`

### Row-Context Table

| source_row_number | timestamp | open | high | low | close | volume | symbol | timezone | session_date | session_type | regular_session | timeframe | source | source_as_of | data_vendor | context_24h_status | context_24h_as_of | macro_context_status | macro_context_as_of | iv_context_status | iv_context_as_of | event_context_status | event_context_as_of | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 204 | 2026-05-04T09:30:00-04:00 | 418.815 | 420.74 | 418.08 | 419.72 | 430985.090472 | GLD | America/New_York | 2026-05-04 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 205 | 2026-05-04T10:30:00-04:00 | 419.64 | 420.86 | 414.38 | 416.63 | 613033.570865 | GLD | America/New_York | 2026-05-04 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 206 | 2026-05-04T11:30:00-04:00 | 416.68 | 417.15 | 413.2801 | 414.53 | 589998.757526 | GLD | America/New_York | 2026-05-04 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 207 | 2026-05-04T12:30:00-04:00 | 414.53 | 416.1 | 413.89 | 415.44 | 207653.936085 | GLD | America/New_York | 2026-05-04 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 208 | 2026-05-04T13:30:00-04:00 | 415.43 | 415.73 | 414.12 | 414.3 | 218519.441049 | GLD | America/New_York | 2026-05-04 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 209 | 2026-05-04T14:30:00-04:00 | 414.3 | 415.56 | 414.2201 | 415.29 | 311658.66152 | GLD | America/New_York | 2026-05-04 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 210 | 2026-05-04T15:30:00-04:00 | 415.3 | 415.74 | 414.57 | 414.73 | 285589.540037 | GLD | America/New_York | 2026-05-04 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 211 | 2026-05-05T09:30:00-04:00 | 420.24 | 421.13 | 419.1803 | 420.98 | 578570.345855 | GLD | America/New_York | 2026-05-05 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 212 | 2026-05-05T10:30:00-04:00 | 420.96 | 421.07 | 420.07 | 420.41 | 250312.0 | GLD | America/New_York | 2026-05-05 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 213 | 2026-05-05T11:30:00-04:00 | 420.41 | 420.57 | 418.3 | 418.64 | 195803.244263 | GLD | America/New_York | 2026-05-05 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 214 | 2026-05-05T12:30:00-04:00 | 418.65 | 418.92 | 418.06 | 418.5201 | 140914.0 | GLD | America/New_York | 2026-05-05 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 215 | 2026-05-05T13:30:00-04:00 | 418.58 | 419.1692 | 418.285 | 418.9 | 123810.186921 | GLD | America/New_York | 2026-05-05 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 216 | 2026-05-05T14:30:00-04:00 | 418.91 | 419.23 | 418.25 | 418.355 | 140663.0 | GLD | America/New_York | 2026-05-05 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 217 | 2026-05-05T15:30:00-04:00 | 418.3886 | 418.58 | 417.905 | 418.17 | 163277.28564 | GLD | America/New_York | 2026-05-05 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 218 | 2026-05-06T09:30:00-04:00 | 430.1 | 433.19 | 429.73 | 432.06 | 833615.481746 | GLD | America/New_York | 2026-05-06 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 219 | 2026-05-06T10:30:00-04:00 | 432.095 | 432.87 | 430.89 | 431.0865 | 434695.898501 | GLD | America/New_York | 2026-05-06 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 220 | 2026-05-06T11:30:00-04:00 | 431.1 | 431.27 | 429.785 | 430.42 | 398647.528166 | GLD | America/New_York | 2026-05-06 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 221 | 2026-05-06T12:30:00-04:00 | 430.45 | 430.78 | 429.64 | 429.98 | 168583.17282 | GLD | America/New_York | 2026-05-06 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 222 | 2026-05-06T13:30:00-04:00 | 429.955 | 430.66 | 429.6 | 430.48 | 174548.11866 | GLD | America/New_York | 2026-05-06 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 223 | 2026-05-06T14:30:00-04:00 | 430.37 | 431.53 | 430.145 | 431.385 | 227109.639953 | GLD | America/New_York | 2026-05-06 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 224 | 2026-05-06T15:30:00-04:00 | 431.37 | 431.455 | 430.6 | 430.6973 | 411368.52916 | GLD | America/New_York | 2026-05-06 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 225 | 2026-05-07T09:30:00-04:00 | 435.61 | 436.93 | 434.9 | 436.745 | 537395.108778 | GLD | America/New_York | 2026-05-07 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 226 | 2026-05-07T10:30:00-04:00 | 436.72 | 437.42 | 434.83 | 435.12 | 385866.981088 | GLD | America/New_York | 2026-05-07 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 227 | 2026-05-07T11:30:00-04:00 | 435.22 | 435.8399 | 431.81 | 433.305 | 433902.906344 | GLD | America/New_York | 2026-05-07 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 228 | 2026-05-07T12:30:00-04:00 | 433.22 | 433.385 | 430.27 | 431.333 | 292997.0 | GLD | America/New_York | 2026-05-07 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 229 | 2026-05-07T13:30:00-04:00 | 431.29 | 432.67 | 430.79 | 432.65 | 255211.832793 | GLD | America/New_York | 2026-05-07 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 230 | 2026-05-07T14:30:00-04:00 | 432.67 | 432.94 | 431.065 | 431.91 | 223066.475633 | GLD | America/New_York | 2026-05-07 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 231 | 2026-05-07T15:30:00-04:00 | 431.93 | 432.53 | 431.68 | 431.7 | 158472.82766 | GLD | America/New_York | 2026-05-07 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 232 | 2026-05-08T09:30:00-04:00 | 434.07 | 436.2 | 433.13 | 433.25 | 737713.464471 | GLD | America/New_York | 2026-05-08 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 233 | 2026-05-08T10:30:00-04:00 | 433.28 | 433.925 | 431.9026 | 432.6999 | 356084.694377 | GLD | America/New_York | 2026-05-08 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 234 | 2026-05-08T11:30:00-04:00 | 432.7499 | 433.23 | 431.74 | 433.21 | 213010.019534 | GLD | America/New_York | 2026-05-08 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 235 | 2026-05-08T12:30:00-04:00 | 433.24 | 433.59 | 432.635 | 433.49 | 152965.68583 | GLD | America/New_York | 2026-05-08 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 236 | 2026-05-08T13:30:00-04:00 | 433.48 | 434.205 | 433.33 | 433.98 | 146791.117522 | GLD | America/New_York | 2026-05-08 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 237 | 2026-05-08T14:30:00-04:00 | 433.95 | 433.9999 | 433.44 | 433.77 | 150154.207274 | GLD | America/New_York | 2026-05-08 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |
| 238 | 2026-05-08T15:30:00-04:00 | 433.762 | 434.08 | 433.5809 | 433.795 | 175738.015447 | GLD | America/New_York | 2026-05-08 | regular | true | 1h_rth | dxlink_candles.get_1h_ema50_snapshot | 2026-05-20T16:25:45Z | dxFeed via tastytrade dxLink | CONTEXT_24H_DAILY_UNCONFIRMED |  | MACRO_UNCONFIRMED |  | IV_UNCONFIRMED |  | EVENT_UNCONFIRMED |  | OHLCV returned by dxLink; unavailable context fields UNCONFIRMED. |

## GLD-REPLACEMENT-IDEAL-CANDIDATE-002 Unavailable Section

- candidate_id: `GLD-REPLACEMENT-IDEAL-CANDIDATE-002`
- symbol: `GLD`
- setup_type: `Ideal`
- old_source_window_id: `UNAVAILABLE`
- old_source_sample_id: `UNAVAILABLE`
- source_file_label: `UNAVAILABLE`
- row_start: `UNAVAILABLE`
- row_end: `UNAVAILABLE`
- candidate_review_rows: `UNAVAILABLE`
- setup_time_review_request_status: `unavailable`
- completion_status: `UNAVAILABLE`
- watch_only=true
- no_trade_decision=true
- accepted_proof=false

Exact second GLD Ideal source window/range remains unavailable unless future repo-backed evidence supplies it. This packet does not create fake row ranges.

## Packet Conclusion

This row-context packet was created for the three ready setup-time review worksheet candidates only. It does not create accepted proof. `accepted_proof_count=0` remains preserved. IWM Continuation and GLD Ideal remain missing-evidence/inconclusive until exact accepted proof exists.
