# SAFE-FAST Day 41 Databento QQQ Download Validation

## Scope

Goal: validate the QQQ OPRA option files already present in `historical_signal_replay/source_data/external_option_data_drop/`.

No additional data was downloaded. No vendor API was called. No raw vendor file was edited. No evidence file was filled. No trade was chosen. No P&L was calculated. `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` was not marked ready.

## Baseline

| Field | Value |
| --- | --- |
| Branch | `main` |
| HEAD | `76ee698` |
| Candidate | `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` |
| Signal/setup time | `2026-04-13T12:30:00-04:00` |
| Requested quote window | `2026-04-13T12:25:00-04:00` through `2026-04-13T12:35:00-04:00` |
| UTC window equivalent | `2026-04-13T16:25:00Z` through `2026-04-13T16:35:00Z` |
| Signal-day open price for near-contract scan | `609.455` |

## Downloaded File Inventory

| File | Size bytes | Validation role |
| --- | ---: | --- |
| `QQQ_OPRA_2026-04-13_download_manifest.json` | 2,292 | download manifest |
| `QQQ_OPRA_definitions_full_day.csv` | 4,649,118 | option definitions / chain metadata |
| `QQQ_OPRA_definitions_full_day.dbn.zst` | 328,057 | raw DBN source for definitions |
| `QQQ_OPRA_statistics_full_day.csv` | 118,024,070 | full-day option statistics |
| `QQQ_OPRA_statistics_full_day.dbn.zst` | 3,747,829 | raw DBN source for statistics |
| `QQQ_OPRA_tcbbo_1225_1235_et.csv` | 4,616,967 | trade rows with consolidated best bid/offer fields |
| `QQQ_OPRA_tcbbo_1225_1235_et.dbn.zst` | 813,080 | raw DBN source for TCBBO |
| `QQQ_OPRA_trades_1225_1235_et.csv` | 3,867,578 | trade rows |
| `QQQ_OPRA_trades_1225_1235_et.dbn.zst` | 596,747 | raw DBN source for trades |

Downloaded QQQ_OPRA files exist: YES.

## CSV Headers And Row Counts

| CSV | Data rows | Header |
| --- | ---: | --- |
| `QQQ_OPRA_definitions_full_day.csv` | 10,244 | `ts_recv,ts_event,rtype,publisher_id,instrument_id,raw_symbol,security_update_action,instrument_class,min_price_increment,display_factor,expiration,activation,high_limit_price,low_limit_price,max_price_variation,unit_of_measure_qty,min_price_increment_amount,price_ratio,inst_attrib_value,underlying_id,raw_instrument_id,market_depth_implied,market_depth,market_segment_id,max_trade_vol,min_lot_size,min_lot_size_block,min_lot_size_round_lot,min_trade_vol,contract_multiplier,decay_quantity,original_contract_size,appl_id,maturity_year,decay_start_date,channel_id,currency,settl_currency,secsubtype,group,exchange,asset,cfi,security_type,unit_of_measure,underlying,strike_price_currency,strike_price,match_algorithm,main_fraction,price_display_format,sub_fraction,underlying_product,maturity_month,maturity_day,maturity_week,user_defined_instrument,contract_multiplier_unit,flow_schedule_type,tick_rule,leg_count,leg_index,leg_instrument_id,leg_raw_symbol,leg_instrument_class,leg_side,leg_price,leg_delta,leg_ratio_price_numerator,leg_ratio_price_denominator,leg_ratio_qty_numerator,leg_ratio_qty_denominator,leg_underlying_id,symbol` |
| `QQQ_OPRA_tcbbo_1225_1235_et.csv` | 28,388 | `ts_recv,ts_event,rtype,publisher_id,instrument_id,action,side,price,size,flags,ts_in_delta,bid_px_00,ask_px_00,bid_sz_00,ask_sz_00,bid_pb_00,ask_pb_00,symbol` |
| `QQQ_OPRA_trades_1225_1235_et.csv` | 28,388 | `ts_recv,ts_event,rtype,publisher_id,instrument_id,action,side,depth,price,size,flags,ts_in_delta,sequence,symbol` |
| `QQQ_OPRA_statistics_full_day.csv` | 809,952 | `ts_recv,ts_event,rtype,publisher_id,instrument_id,ts_ref,price,quantity,sequence,ts_in_delta,stat_type,channel_id,update_action,stat_flags,symbol` |

## Required Field Coverage

| Requirement | Result |
| --- | --- |
| Option definitions / chain | YES. `QQQ_OPRA_definitions_full_day.csv` has 10,244 unique QQQ option symbols. |
| Bid | YES. `QQQ_OPRA_tcbbo_1225_1235_et.csv` has `bid_px_00`. |
| Ask | YES. `QQQ_OPRA_tcbbo_1225_1235_et.csv` has `ask_px_00`. |
| Quote timestamp | YES. TCBBO rows have `ts_event` and `ts_recv`. |
| Spread-calculable fields | YES. Spread is calculable from `ask_px_00 - bid_px_00` for inspection only. |
| Expiration | YES in definitions as `expiration`; also parseable from QQQ OPRA symbols in quote/trade/statistics rows. |
| Strike | YES in definitions as `strike_price`; also parseable from QQQ OPRA symbols in quote/trade/statistics rows. |
| Option side | YES in definitions as `instrument_class`; also parseable as `C` or `P` from QQQ OPRA symbols. |
| Trade volume | YES. Trade rows include `size`; statistics include `quantity` with `stat_type` values including `6` (`CLEARED_VOLUME` in the installed Databento enum). |
| Open interest / statistics | YES. Statistics file is present; `stat_type` includes `9` (`OPEN_INTEREST` in the installed Databento enum), with 178,488 rows. |

Important limitation: TCBBO, trade, and statistics rows do not expose separate `expiration`, `strike`, or option-side columns. Those fields are available by parsing the QQQ OPRA/OCC-style `symbol`, for example `QQQ   260501C00610000` means expiration `2026-05-01`, call, strike `610`.

## Window Coverage

| File | Earliest `ts_event` | Latest `ts_event` | Window result |
| --- | --- | --- | --- |
| `QQQ_OPRA_tcbbo_1225_1235_et.csv` | `2026-04-13T16:25:00.075927844Z` | `2026-04-13T16:34:59.886770236Z` | Covers the requested ten-minute ET window as an end-exclusive export through just before `12:35:00 ET`. |
| `QQQ_OPRA_trades_1225_1235_et.csv` | `2026-04-13T16:25:00.075927844Z` | `2026-04-13T16:34:59.886770236Z` | Covers the requested ten-minute ET window as an end-exclusive export through just before `12:35:00 ET`. |
| `QQQ_OPRA_definitions_full_day.csv` | `2026-04-13T10:30:00.573512487Z` | not needed for quote window | Full-day definitions file present for the date. |
| `QQQ_OPRA_statistics_full_day.csv` | `2026-04-13T10:30:00.573512487Z` | `2026-04-13T21:44:58.355950532Z` | Full-day statistics file present for the date. |

Timestamp window covers `2026-04-13 12:25-12:35 ET`: YES for the TCBBO/trades export interval; no row exists exactly at `12:35:00 ET`.

## Expiration And Strike Coverage

Definitions coverage:

- Unique definition symbols: 10,244.
- Expiration range: `2026-04-13` through `2028-12-15`.
- Strike range: `174.78` through `950`.
- Calls: 5,122 symbols.
- Puts: 5,122 symbols.
- Requested expiration range symbols (`2026-04-27` through `2026-05-13`): 1,118.
- Requested strike range symbols (`590` through `640`): 2,128.
- Requested expiration plus strike range symbols: 280.

TCBBO quote coverage:

- Quote rows: 28,388.
- Unique quoted symbols: 1,324.
- Quoted expiration range: `2026-04-13` through `2028-12-15`.
- Quoted strike range: `205` through `920`.
- Requested expiration range quote rows: 541.
- Requested strike range quote rows: 26,924.
- Requested expiration plus strike range quote rows: 375.

Expirations found inside the requested `2026-04-27` through `2026-05-13` range:

| Expiration | Definition symbols | TCBBO rows | TCBBO symbols | TCBBO min strike | TCBBO max strike |
| --- | ---: | ---: | ---: | ---: | ---: |
| `2026-04-27` | 60 | 61 | 20 | 555 | 650 |
| `2026-04-30` | 316 | 150 | 57 | 445 | 660 |
| `2026-05-01` | 342 | 184 | 60 | 505 | 665 |
| `2026-05-08` | 400 | 146 | 57 | 470 | 680 |

No `2026-05-13` expiration appeared in the downloaded QQQ definitions or quote rows. This appears to be an availability/listing result in the downloaded files, not a SAFE-FAST contract decision.

## Contracts Near Signal-Day Open Price 609.455

Near-contract scan rule used for validation only: QQQ contracts with strikes within 1.0 point of `609.455`.

Definitions near `609.455` inside the requested expiration range:

| Expiration | Contracts found |
| --- | --- |
| `2026-04-27` | `QQQ   260427C00610000`, `QQQ   260427P00610000` |
| `2026-04-30` | `QQQ   260430C00609000`, `QQQ   260430P00609000`, `QQQ   260430C00610000`, `QQQ   260430P00610000` |
| `2026-05-01` | `QQQ   260501C00609000`, `QQQ   260501P00609000`, `QQQ   260501C00610000`, `QQQ   260501P00610000` |
| `2026-05-08` | `QQQ   260508C00609000`, `QQQ   260508P00609000`, `QQQ   260508C00610000`, `QQQ   260508P00610000` |

TCBBO near-contract rows inside the requested expiration range:

| Symbol | Rows | Expiration | Side | Strike | First `ts_event` | Last `ts_event` | First bid | First ask | First spread |
| --- | ---: | --- | --- | ---: | --- | --- | ---: | ---: | ---: |
| `QQQ   260427C00610000` | 2 | `2026-04-27` | C | 610 | `2026-04-13T16:31:11.951379332Z` | `2026-04-13T16:31:13.931412942Z` | 11.62 | 11.75 | 0.13 |
| `QQQ   260427P00610000` | 5 | `2026-04-27` | P | 610 | `2026-04-13T16:29:20.551383589Z` | `2026-04-13T16:33:28.554792286Z` | 7.27 | 7.34 | 0.07 |
| `QQQ   260430P00609000` | 1 | `2026-04-30` | P | 609 | `2026-04-13T16:28:11.238771402Z` | `2026-04-13T16:28:11.238771402Z` | 8.82 | 8.88 | 0.06 |
| `QQQ   260430C00610000` | 4 | `2026-04-30` | C | 610 | `2026-04-13T16:26:21.787707102Z` | `2026-04-13T16:26:22.932874347Z` | 13.12 | 13.22 | 0.10 |
| `QQQ   260430P00610000` | 5 | `2026-04-30` | P | 610 | `2026-04-13T16:25:02.550533010Z` | `2026-04-13T16:33:45.893818777Z` | 9.23 | 9.29 | 0.06 |
| `QQQ   260501C00609000` | 1 | `2026-05-01` | C | 609 | `2026-04-13T16:29:06.707410049Z` | `2026-04-13T16:29:06.707410049Z` | 14.58 | 14.71 | 0.13 |
| `QQQ   260501P00609000` | 4 | `2026-05-01` | P | 609 | `2026-04-13T16:25:30.990268734Z` | `2026-04-13T16:29:21.382502868Z` | 9.22 | 9.24 | 0.02 |
| `QQQ   260501C00610000` | 6 | `2026-05-01` | C | 610 | `2026-04-13T16:27:00.625942516Z` | `2026-04-13T16:33:19.098206867Z` | 13.51 | 13.60 | 0.09 |
| `QQQ   260501P00610000` | 5 | `2026-05-01` | P | 610 | `2026-04-13T16:25:04.350947041Z` | `2026-04-13T16:30:35.526368580Z` | 9.58 | 9.65 | 0.07 |
| `QQQ   260508C00610000` | 1 | `2026-05-08` | C | 610 | `2026-04-13T16:31:39.464453623Z` | `2026-04-13T16:31:39.464453623Z` | 15.95 | 16.06 | 0.11 |
| `QQQ   260508P00610000` | 12 | `2026-05-08` | P | 610 | `2026-04-13T16:25:31.327970684Z` | `2026-04-13T16:30:48.869723967Z` | 11.10 | 11.11 | 0.01 |

This near-contract list is an inventory only. It does not choose a trade, contract, spread, entry, exit, fill, or P&L path.

## Validation Result

Downloaded files exist: YES.

File names and sizes recorded: YES.

CSV headers and row counts recorded: YES.

Bid, ask, timestamp, spread-calculable quote fields found: YES.

Definitions/chain metadata found: YES.

Expiration, strike, and side found: YES, directly in definitions and parseable from symbols in quote/trade/statistics rows.

Trade volume fields found: YES.

Open interest/statistics found: YES, via statistics `stat_type` `9` (`OPEN_INTEREST`).

Timestamp window coverage confirmed: YES for the requested ten-minute export interval, with no exact row at the exclusive end boundary.

Contracts near QQQ signal-day open price `609.455` identified: YES.

Evidence filled: NO.

Trade chosen: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Proof accepted: NO.

Profitability claim made: NO.

## Next

The smallest next step is not evidence promotion. A later explicitly authorized task would need to define how to map these validated option rows into SAFE-FAST option/execution/caution evidence fields, while preserving no-hindsight boundaries and without inferring fills or profitability from quotes alone.
