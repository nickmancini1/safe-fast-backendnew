# SAFE-FAST Day 41 Starter Batch Option Inspection

## Scope

- Mode: read-only local starter Databento inspection.
- Data source: `historical_signal_replay/source_data/external_option_data_drop/`.
- Manifest: `historical_signal_replay/source_data/external_option_data_drop/SAFE_FAST_CHEAP_STARTER_DATABENTO_DOWNLOAD_MANIFEST.json`.
- Candidates inspected:
  - `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`
  - `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`
  - `SPY-REAL-HISTORICAL-IDEAL-001`
  - `QQQ-REAL-HISTORICAL-CONTINUATION-001`
  - `QQQ-REAL-HISTORICAL-IDEAL-001`
  - `SPY-REAL-HISTORICAL-CONTINUATION-001`

## Guardrails

- Downloaded more data: NO.
- Used full-window data: NO.
- Filled evidence: NO.
- Backtested: NO.
- Calculated P&L: NO.
- Claimed proof or profitability: NO.
- Marked candidate ready: NO.
- Modified raw Databento files: NO.
- Applied QQQ-specific contract rules blindly to SPY, Ideal, or Continuation: NO.

## Inspection Method

For each candidate, the inspection used only:

- `definitions_full_day`
- `statistics_full_day`
- `tcbbo_signal_10min`
- `trades_signal_10min`

The setup boundary came from the candidate packet. Quote freshness means the latest raw `tcbbo` `ts_event` at or before the setup boundary across the starter window, not a selected contract. Trade activity means raw rows and summed `size` at or before the setup boundary across the starter window, not a fill or entry assumption. Statistics/open-interest availability means `stat_type=9` rows for instruments that appeared in the candidate's starter quote or trade windows, at or before the setup boundary, not an accepted selected-contract evidence fill.

## Batch Result

All six candidates have starter data that is sufficient for first-pass raw option inspection after setup-specific rule/regression authorization. None can be moved to evidence fill, backtest, proof, profitability, or readiness from this inspection alone.

| Candidate | Definitions exist | Setup-window quotes exist | Setup-window trades exist | Same-contract or usable statistics/OI exists | Quote freshness around signal | Trade activity around signal | Starter data alone enough to continue | Full-window data may be needed later |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | YES: `13,390` definitions, `13,390` instruments, `36` expirations. | YES: `53,730` quote rows, `1,735` instruments; `28,629` rows at/before setup. | YES: `53,730` trade rows, `1,735` instruments; `28,629` rows at/before setup. | YES: `30,456` setup-time-safe `stat_type=9` rows across `1,692` quote/trade-window instruments. | Latest at/before setup: `2026-04-13T16:29:59.990518Z`, age about `0.009482` seconds; `11,557` rows within 60 seconds before setup. | Setup-time-safe summed size `276,562`; last 60 seconds summed size `112,441`; latest trade row age about `0.009482` seconds. | YES for raw starter inspection after SPY CFB rule/regression authorization; NO for evidence fill or trade choice. | YES, likely needed for entry, exit, full quote path, stop/invalidation, time exit, costs, slippage, sample-size, and proof work. |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | YES: `13,422` definitions, `13,422` instruments, `36` expirations. | YES: `26,724` quote rows, `1,672` instruments; `9,067` rows at/before setup. | YES: `26,724` trade rows, `1,672` instruments; `9,067` rows at/before setup. | YES: `29,412` setup-time-safe `stat_type=9` rows across `1,634` quote/trade-window instruments. | Latest at/before setup: `2026-04-15T18:29:59.973562Z`, age about `0.026438` seconds; `1,366` rows within 60 seconds before setup. | Setup-time-safe summed size `104,943`; last 60 seconds summed size `9,653`; latest trade row age about `0.026438` seconds. | YES for raw starter inspection after SPY CFB higher-base rule/regression authorization; NO for evidence fill or trade choice. | YES, likely needed for entry, exit, full quote path, stop/invalidation, time exit, costs, slippage, sample-size, and proof work. |
| `SPY-REAL-HISTORICAL-IDEAL-001` | YES: `13,604` definitions, `13,604` instruments, `37` expirations. | YES: `23,940` quote rows, `1,144` instruments; `10,302` rows at/before setup. | YES: `23,940` trade rows, `1,144` instruments; `10,302` rows at/before setup. | YES: `19,926` setup-time-safe `stat_type=9` rows across `1,107` quote/trade-window instruments. | Latest at/before setup: `2026-05-13T15:29:59.996749Z`, age about `0.003251` seconds; `1,303` rows within 60 seconds before setup. | Setup-time-safe summed size `125,354`; last 60 seconds summed size `9,394`; latest trade row age about `0.003251` seconds. | YES for raw starter inspection after Ideal rule/regression authorization; NO for evidence fill or trade choice. | YES, likely needed for entry, exit, full quote path, stop/invalidation, time exit, costs, slippage, sample-size, and proof work. |
| `QQQ-REAL-HISTORICAL-CONTINUATION-001` | YES: `11,128` definitions, `11,128` instruments, `35` expirations. | YES: `13,799` quote rows, `1,305` instruments; `6,229` rows at/before setup. | YES: `13,799` trade rows, `1,305` instruments; `6,229` rows at/before setup. | YES: `22,932` setup-time-safe `stat_type=9` rows across `1,274` quote/trade-window instruments. | Latest at/before setup: `2026-04-30T19:29:59.750843Z`, age about `0.249157` seconds; `1,432` rows within 60 seconds before setup. | Setup-time-safe summed size `57,129`; last 60 seconds summed size `11,069`; latest trade row age about `0.249157` seconds. | YES for raw starter inspection after Continuation rule/evidence package authorization; NO for evidence fill or trade choice. | YES, likely needed for entry, exit, full quote path, stop/invalidation, time exit, costs, slippage, sample-size, and proof work. |
| `QQQ-REAL-HISTORICAL-IDEAL-001` | YES: `11,628` definitions, `11,628` instruments, `34` expirations. | YES: `20,106` quote rows, `1,263` instruments; `11,916` rows at/before setup. | YES: `20,106` trade rows, `1,263` instruments; `11,916` rows at/before setup. | YES: `21,366` setup-time-safe `stat_type=9` rows across `1,187` quote/trade-window instruments. | Latest at/before setup: `2026-05-13T16:29:59.824325Z`, age about `0.175675` seconds; `1,825` rows within 60 seconds before setup. | Setup-time-safe summed size `95,652`; last 60 seconds summed size `12,586`; latest trade row age about `0.175675` seconds. | YES for raw starter inspection after Ideal rule/evidence package authorization; NO for evidence fill or trade choice. | YES, likely needed for entry, exit, full quote path, stop/invalidation, time exit, costs, slippage, sample-size, and proof work. |
| `SPY-REAL-HISTORICAL-CONTINUATION-001` | YES: `12,970` definitions, `12,970` instruments, `36` expirations. | YES: `13,598` quote rows, `1,110` instruments; `6,819` rows at/before setup. | YES: `13,598` trade rows, `1,110` instruments; `6,819` rows at/before setup. | YES: `19,656` setup-time-safe `stat_type=9` rows across `1,092` quote/trade-window instruments. | Latest at/before setup: `2026-04-30T16:29:59.959534Z`, age about `0.040466` seconds; `1,299` rows within 60 seconds before setup. | Setup-time-safe summed size `62,783`; last 60 seconds summed size `12,862`; latest trade row age about `0.040466` seconds. | YES for raw starter inspection after Continuation rule/evidence package authorization; NO for evidence fill or trade choice. | YES, likely needed for entry, exit, full quote path, stop/invalidation, time exit, costs, slippage, sample-size, and proof work. |

## Setup Family Rule Work Needed

### Clean Fast Break

- Needed for `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` and `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`.
- Do not apply the QQQ CFB contract selector or QQQ lifecycle thresholds to SPY by assumption.
- Required first work:
  - SPY CFB initial-break lifecycle rule/regression package for CFB 002.
  - SPY CFB higher-base fresh-break lifecycle rule/regression package for CFB 003.
  - SPY CFB reviewed-universe and contract-selection rule authorization.
  - SPY CFB option-context, execution-context, headline-context, and complete-caution component rules.
  - Later trade-plan rules: entry, fill, exit, stop/invalidation, time exit, cost, slippage, sample size, and promotion gates.

### Ideal

- Needed for `SPY-REAL-HISTORICAL-IDEAL-001` and `QQQ-REAL-HISTORICAL-IDEAL-001`.
- Do not apply QQQ CFB gap, lifecycle, or contract-selection rules to Ideal candidates.
- Required first work:
  - Ideal setup identity and lifecycle rule/regression package.
  - Ideal gap/context decision if the Ideal evidence shape requires it.
  - Ideal reviewed-universe and contract-selection rule authorization by symbol/setup.
  - Ideal option-context, execution-context, headline-context, and complete-caution component rules.
  - Later trade-plan rules: entry, fill, exit, stop/invalidation, time exit, cost, slippage, sample size, and promotion gates.

### Continuation

- Needed for `QQQ-REAL-HISTORICAL-CONTINUATION-001` and `SPY-REAL-HISTORICAL-CONTINUATION-001`.
- Do not infer Continuation rules from CFB or Ideal.
- Required first work:
  - Continuation evidence-package shape, since current richer work-package rows are not present for these candidates.
  - Continuation setup identity and lifecycle rule/regression package.
  - Continuation reviewed-universe and contract-selection rule authorization by symbol/setup.
  - Continuation option-context, execution-context, headline-context, and complete-caution component rules.
  - Later trade-plan rules: entry, fill, exit, stop/invalidation, time exit, cost, slippage, sample size, and promotion gates.

## Conclusion

Starter data quality is not the immediate blocker for first-pass raw option inspection. The immediate blockers are setup-family-specific rule/regression authorization and evidence-package shape. All six candidates remain not ready and not proven.

## Safe Checks

- Command: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`.
- Result: PASS, `3` checks.
