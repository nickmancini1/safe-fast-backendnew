# SAFE-FAST Day 41 QQQ CFB Contract Selection Decision

## Scope

Target candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Setup type: QQQ Clean Fast Break.

Signal/setup time: `2026-04-13T12:30:00-04:00`.

Baseline from task file: `869d0ef Record QQQ CFB selected contract policy blocker`.

This document defines the first conservative QQQ Clean Fast Break one-contract selection rule for later regression testing. It does not apply the rule to choose a real trade, backtest, calculate P&L, fill evidence, claim proof or profitability, mark QQQ ready, or change intake-ready status.

## Decision Result

First one-contract selection rule accepted for regression work: YES.

Real trade selected: NO.

Backtest authorized: NO.

P&L calculated: NO.

Evidence filled: NO.

QQQ candidate marked ready: NO.

Proof accepted: NO.

Profitability claimed: NO.

## Source Inputs Allowed

The first rule may use only setup-time-safe inputs already documented in the repo:

- candidate id `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`;
- symbol `QQQ`;
- setup type `Clean Fast Break`;
- setup time `2026-04-13T12:30:00-04:00`;
- trigger `613.67`;
- invalidation `609.58`;
- signal-day open `609.455`;
- Databento QQQ definitions for contract metadata;
- Databento TCBBO quote rows with `ts_event` at or before setup time;
- Databento statistics rows only under the timestamp rule below;
- normalized midpoint, spread, spread percent, bid size, ask size, and quote age from `historical_signal_replay/databento_opra_normalizer.py`.

Forbidden inputs:

- post-signal option quotes;
- future candles;
- future replay rows;
- outcome movement;
- fills;
- broker/order/account data;
- P&L;
- profitability;
- readiness.

## Reviewed Universe

The reviewed universe remains the policy accepted in `SAFE_FAST_DAY41_QQQ_CFB_SELECTED_CONTRACT_POLICY.md`:

- QQQ options listed on `2026-04-13`;
- expirations `2026-04-27` through `2026-05-13`, inclusive, when present in Databento definitions;
- strikes `590` through `640`, inclusive;
- valid definition metadata;
- valid TCBBO quote selected nearest at or before setup time by Databento `ts_event`.

Contracts outside that reviewed universe are rejected before ranking.

## Call/Put Side

First test side: long calls only.

Reason: the target Clean Fast Break trigger is an upside break level at `613.67`. The first test policy follows the break direction and does not inspect long puts, debit spreads, or both-side ranking.

This is a rule for regression testing only. It is not a bullish profitability claim and it does not authorize a fill or trade.

## Expiration Choice

First test expiration rule:

1. Compute calendar DTE from setup date `2026-04-13`.
2. Keep only reviewed-universe expirations with DTE greater than or equal to `14`.
3. Select the nearest available expiration by calendar date.
4. If the nearest target date is unavailable in Databento definitions, use the next later reviewed-universe expiration.
5. If no reviewed-universe expiration has DTE greater than or equal to `14`, abstain.

For the documented reviewed range, this means the rule ranks `2026-04-27` before later available expirations, but this document does not apply the rule to choose a target contract.

## Strike Choice

First test strike rule:

1. Use the Clean Fast Break trigger `613.67` as the strike reference.
2. For long calls, rank strikes at or above the trigger first.
3. Select the lowest available reviewed-universe call strike greater than or equal to the trigger.
4. If no strike greater than or equal to the trigger exists inside the reviewed universe, abstain.
5. Do not fall back to ITM calls below the trigger in the first test rule.

This keeps the first test rule side-aware and avoids using later outcome movement to decide moneyness.

## Moneyness Preference

First test moneyness preference: nearest out-of-the-money call relative to the trigger.

Reference price: trigger `613.67`.

Rejected alternatives for this first test rule:

- signal-day open as the strike reference;
- invalidation as the strike reference;
- nearest absolute ATM;
- first ITM;
- delta-based ranking, because Greeks are not available in the validated Databento files.

## One-Contract Ranking

Apply ranking in this exact order after reviewed-universe and eligibility filters:

1. side is call;
2. expiration is nearest available reviewed-universe expiration with DTE greater than or equal to `14`;
3. strike is the lowest call strike greater than or equal to trigger `613.67`;
4. selected TCBBO quote is nearest at or before setup time by `ts_event`;
5. quote passes the spread and liquidity gates below;
6. open-interest and volume requirements pass under the statistics timestamp rule below.

Tie-breakers:

- if duplicate rows exist for the same contract, select the quote with the latest `ts_event` at or before setup time;
- if duplicate quotes share the same `ts_event`, select the row with the earliest `ts_recv`;
- if duplicates remain indistinguishable, abstain rather than choose arbitrarily.

Rejected-contract fallback:

- if the top-ranked contract fails quote, spread, size, volume, open-interest, or timestamp gates, abstain;
- do not scan to the next expiration or strike after a ranked contract fails a gate in the first test rule.

## Maximum Spread

First test spread gate:

- absolute spread must be less than or equal to `0.15`;
- spread percent must be less than or equal to `2.00%`;
- midpoint must be positive;
- ask must be greater than bid;
- bid must be greater than or equal to zero.

If either spread metric is missing or exceeds the threshold, the contract is rejected for selection and the attempted selection result is `unknown/no-trade` for contract-selection regression purposes.

These thresholds are conservative test gates, not calibrated profitability thresholds.

## Minimum Volume And Open Interest

First test liquidity gate:

- bid size must be at least `1`;
- ask size must be at least `1`;
- same-contract trade volume through setup time must be at least `1` contract, using only trade rows with `ts_event` at or before setup time;
- same-contract open interest must be at least `1`, using only accepted open-interest statistics under the statistics timestamp rule below.

Missing trade volume, missing open interest, missing bid size, or missing ask size causes abstain/unknown, not clean.

## Quote Timestamp Rule

Accepted quote timestamp rule:

- use Databento TCBBO `ts_event` as event time;
- select the quote nearest at or before `2026-04-13T12:30:00-04:00`;
- reject quotes with `ts_event` after setup time;
- preserve `ts_recv` as metadata only;
- `ts_recv` cannot make a post-signal `ts_event` valid.

## Statistics Timestamp Rule

First test statistics timestamp rule:

- use Databento statistics only when `stat_type` maps to `cleared_volume` or `open_interest`;
- the statistics row must match the same option contract by `instrument_id` or symbol;
- the statistics row must have `ts_event` at or before setup time;
- if `ts_ref` is available, it must also be at or before setup time;
- if `ts_ref` is absent from the normalized row, the row may be used only when `ts_event` is at or before setup time;
- statistics rows after setup time are rejected even if they might represent prior-day or setup-day reference data.

This deliberately rejects potentially usable but timestamp-ambiguous statistics until a later rule accepts a less restrictive `ts_ref` policy.

## Missing-Data Behavior

Missing or unparseable required data causes abstain/unknown:

- wrong candidate id;
- wrong symbol;
- wrong setup type;
- missing trigger;
- missing definition metadata;
- missing reviewed-universe expiration or strike;
- missing selected quote;
- missing or invalid bid/ask;
- missing bid size or ask size;
- missing spread or spread percent;
- missing trade volume;
- missing open interest;
- missing or unsafe quote/statistics timestamp;
- duplicate indistinguishable top-ranked rows.

Missing data must not be treated as clean, pass, or proof.

## Rejected-Contract Behavior

Rejected contracts are excluded from selection and recorded as rejection reasons in later regression work.

Rejected-contract categories:

- outside reviewed universe;
- non-call side;
- expiration not top ranked;
- strike not top ranked;
- no valid quote at or before setup time;
- crossed, zero-midpoint, or unparseable quote;
- spread gate failed;
- liquidity gate failed;
- statistics timestamp gate failed;
- future or forbidden input detected.

Rejected top-ranked contract behavior for the first test rule: abstain. No fallback scan is allowed after a gate failure.

## Exact Regression Cases Needed Next

1. Long-call side is required; puts are rejected for first-rule selection.
2. Nearest reviewed-universe expiration with DTE at least `14` is selected.
3. Missing nearest expiration falls forward only to the next later reviewed-universe expiration.
4. No reviewed-universe expiration at or above `14` DTE causes abstain.
5. Long-call strike is the lowest reviewed-universe strike greater than or equal to trigger.
6. No strike greater than or equal to trigger causes abstain.
7. Signal-day open and invalidation do not alter strike ranking.
8. Delta/Greeks are ignored because validated Databento files do not supply them.
9. Quote nearest at or before setup time is selected by `ts_event`.
10. Post-signal quote is rejected even if `ts_recv` is before or near setup time.
11. Duplicate same-contract quote tie-breaker uses latest `ts_event`, then earliest `ts_recv`.
12. Indistinguishable duplicate quote rows cause abstain.
13. Absolute spread `0.15` passes and spread above `0.15` fails.
14. Spread percent `2.00%` passes and spread percent above `2.00%` fails.
15. Missing midpoint, missing spread, non-positive midpoint, crossed quote, or ask not greater than bid causes abstain.
16. Bid size and ask size of at least `1` pass; missing or zero size causes abstain.
17. Trade volume through setup time of at least `1` passes; missing or post-signal-only trade volume causes abstain.
18. Open interest of at least `1` passes only when timestamp-safe under the statistics rule.
19. Statistics rows with `ts_event` after setup time are rejected.
20. Statistics rows with `ts_ref` after setup time are rejected.
21. If top-ranked contract fails any gate, the rule abstains rather than selecting the next strike or expiration.
22. Wrong symbol, wrong setup, future candle, future replay row, fill, broker/order/account, outcome, P&L, profitability, and readiness inputs are rejected.

## Current QQQ Target Implication

This decision defines a future test-selection rule only.

It still cannot honestly produce:

- an executed trade;
- a fill;
- an exit;
- P&L;
- proof;
- profitability;
- readiness.

The rule must be implemented as regression fixtures and calculator logic before it can fill any evidence field or drive later trade-plan work.

## Result

First conservative QQQ CFB contract-selection rule accepted for regression work: YES.

Real trade selected: NO.

Evidence filled: NO.

Backtest authorized: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Intake-ready count changed: NO.

Proof accepted: NO.

Profitability claimed: NO.
