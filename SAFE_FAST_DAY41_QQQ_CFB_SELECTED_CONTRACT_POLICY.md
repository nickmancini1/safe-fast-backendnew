# SAFE-FAST Day 41 QQQ CFB Selected-Contract Policy

## Scope

Target candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Setup type: QQQ Clean Fast Break.

Signal/setup time: `2026-04-13T12:30:00-04:00`.

Baseline from task file: `809bd5e Fill QQQ CFB context caution evidence`.

This document defines the first conservative QQQ Clean Fast Break reviewed option-universe and selected-contract eligibility policy. It does not choose a real trade, backtest, calculate P&L, fill evidence, claim proof or profitability, mark QQQ ready, or change intake-ready status.

## Decision Result

First reviewed option-universe policy accepted: YES, for regression fixture work only.

One selected contract chosen: NO.

Reason: repo evidence supports a bounded, source-backed Databento QQQ OPRA contract universe and no-hindsight quote inspection, but does not yet support an honest call/put direction decision, exact one-contract ranking rule, numeric spread cap, or volume/open-interest thresholds.

Evidence fill authorized: NO.

Backtest authorized: NO.

Trade chosen: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Proof accepted: NO.

Profitability claimed: NO.

## Source Inputs

The policy may use only already-validated local Databento QQQ OPRA inspection fields and existing candidate metadata:

- candidate id `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`;
- symbol `QQQ`;
- setup type `Clean Fast Break`;
- setup time `2026-04-13T12:30:00-04:00`;
- trigger `613.67`;
- invalidation `609.58`;
- signal-day open `609.455`;
- Databento definitions for QQQ option contract metadata;
- Databento TCBBO quote rows for bid, ask, bid size, ask size, `ts_event`, and `ts_recv`;
- Databento trade/statistics rows only as timestamp-safe inspection inputs;
- `historical_signal_replay/databento_opra_normalizer.py` for read-only parsing, timestamp normalization, joins, quote selection, and spread/liquidity inspection.

Raw Databento files remain local-only and must not be modified or committed by this policy work.

## Reviewed Option Universe

The first reviewed universe is a bounded inspection universe, not a trade selection:

- underlying: QQQ only;
- source date: `2026-04-13`;
- expiration range: listed QQQ expirations from `2026-04-27` through `2026-05-13`, inclusive, when present in Databento definitions;
- strike range: QQQ strikes `590` through `640`, inclusive;
- side coverage: both calls and puts remain reviewable because the call/put trade-direction decision is still blocked;
- required definition metadata: contract symbol, instrument id or symbol join key, expiration, strike, side, and underlying;
- required quote metadata: at least one valid TCBBO quote selected by `ts_event` nearest at or before setup time for the contract.

Contracts outside this universe are rejected for the first QQQ CFB contract-policy regression path.

The absence of `2026-05-13` from the downloaded Databento definitions is treated as source availability, not as a chosen fallback. Listed expirations inside the inclusive range remain reviewable; missing expirations are unavailable.

## Selected-Contract Eligibility

A contract is eligible for later one-contract selection only if all of the following are true:

1. It belongs to the reviewed option universe above.
2. It has source-backed definition metadata matching QQQ, expiration, side, and strike.
3. It has a selected quote with `ts_event` at or before `2026-04-13T12:30:00-04:00`.
4. The selected quote has parseable bid, ask, bid size, and ask size.
5. Bid is greater than or equal to zero, ask is greater than bid, midpoint is positive, and spread and spread percent are calculable.
6. It does not require any post-signal quote, future candle, future replay row, outcome move, fill, P&L, profitability, or readiness input.

This eligibility filter does not rank eligible contracts and does not pick a trade.

## Call/Put Side Rule

Call/put selected side is still blocked.

Human decision needed: define whether QQQ Clean Fast Break selected-contract work should inspect long calls only, long puts only, both sides with a predeclared ranking rule, debit spreads, or an abstain/no-trade path.

Until that decision is accepted:

- both calls and puts may be retained in the reviewed universe;
- no single contract may be selected;
- `option_context_status` and `execution_context_status` cannot become clean/caution/fail from side-dependent logic.

## Expiration Selection Rule

Reviewed-universe expiration rule accepted for regression work:

- include listed QQQ expirations from `2026-04-27` through `2026-05-13`, inclusive;
- reject contracts with expirations before `2026-04-27` or after `2026-05-13`;
- reject requested expirations absent from Databento definitions as unavailable, not failed.

One-expiration selection is still blocked.

Human decision needed: define whether to select the nearest available expiration, a fixed target DTE, the first weekly/monthly after a threshold, or a ranked fallback when the target expiration is missing.

## Strike Selection Rule

Reviewed-universe strike rule accepted for regression work:

- include strikes from `590` through `640`, inclusive;
- reject strikes outside that range.

One-strike selection is still blocked.

Human decision needed: define the reference price and ranking rule for one selected strike, such as nearest to signal-day open, nearest to trigger, first ITM/ATM/OTM strike by side, fixed delta when available, or another predeclared method.

## Moneyness / ATM / ITM / OTM Rule

Moneyness may be calculated for inspection only from the source-backed reference values:

- signal-day open: `609.455`;
- trigger: `613.67`;
- invalidation: `609.58`.

No accepted policy yet chooses which reference value controls moneyness or whether the selected contract must be ATM, ITM, or OTM.

Human decision needed: define the moneyness reference and side-aware ATM/ITM/OTM preference before a selected contract can be chosen.

## Minimum Bid/Ask Data Requirement

Minimum bid/ask data requirement accepted for eligibility:

- selected TCBBO quote must be nearest at or before setup time by `ts_event`;
- `bid_px_00`, `ask_px_00`, `bid_sz_00`, and `ask_sz_00` must be present and parseable;
- ask must be greater than bid;
- midpoint, spread, and spread percent must be calculable;
- quote source references must preserve contract symbol or instrument id and quote timestamp.

Missing or invalid bid/ask data rejects the contract from eligibility and leaves the component status `unknown` unless a later accepted fail rule explicitly classifies it as fail.

## Maximum Spread Rule

Numeric maximum spread and maximum spread-percent thresholds are still blocked.

Eligibility requires only that spread and spread percent are calculable from a valid non-crossed quote. It does not classify the quote as clean, caution, or fail.

Human decision needed: define hard-block and caution thresholds for absolute spread and/or spread percent, including whether thresholds vary by option price, expiration, or moneyness.

## Minimum Volume / Open-Interest Rule

Numeric minimum volume, trade-count, bid/ask-size, and open-interest thresholds are still blocked.

Eligibility may preserve source-backed trade, cleared-volume, and open-interest inspection fields only when their timestamp/reference rule is no-hindsight safe.

Human decision needed: define:

- whether trade rows, cleared volume, open interest, bid size, and ask size are required;
- minimum thresholds for each required field;
- timestamp/reference handling for statistics rows, especially when `ts_event` or `ts_ref` is after the setup time;
- whether missing liquidity statistics are `unknown`, `caution`, `fail`, or rejection-only.

## Quote Timestamp / No-Hindsight Rule

Accepted no-hindsight quote rule for eligibility:

- use Databento TCBBO `ts_event`, not `ts_recv`, as the event-time boundary;
- selected quote must be the nearest quote at or before `2026-04-13T12:30:00-04:00`;
- quotes with `ts_event` after setup time are rejected for setup-time eligibility;
- `ts_recv` may be preserved as receive-time metadata but cannot make a post-signal `ts_event` valid;
- future candles, future replay rows, outcome movement, fills, broker/order/account data, P&L, profitability, and readiness must not affect contract eligibility.

Statistics rows require a later accepted timestamp/reference rule before they can drive clean/caution/fail labels.

## Missing-Data Behavior

Missing candidate identity, wrong symbol, wrong setup type, missing definition metadata, missing quote, missing bid/ask, missing quote timestamp, missing selected-contract side rule, missing one-contract ranking rule, missing spread threshold, missing liquidity threshold, or missing no-hindsight proof returns `unknown` for the affected option/execution component.

Missing data must not be treated as clean.

## Rejected-Contract Behavior

A contract is rejected from the reviewed universe or eligibility set when it has:

- wrong underlying;
- wrong setup/candidate identity;
- expiration outside the accepted reviewed-universe range;
- strike outside the accepted reviewed-universe range;
- missing or unparseable definition metadata;
- no valid quote at or before setup time;
- crossed or non-positive quote state that prevents midpoint/spread inspection;
- post-signal quote used as the only quote;
- forbidden future/outcome/fill/P&L/profitability/readiness input.

Rejected contracts cannot be used to select a trade or improve option/execution context. Rejection of one contract does not choose a different contract unless a later ranking and fallback rule is accepted.

## Exact Regression Cases Needed Next

1. Target reviewed-universe construction includes only QQQ definitions with expirations `2026-04-27` through `2026-05-13` and strikes `590` through `640`.
2. Missing `2026-05-13` expiration is treated as unavailable source coverage, not as a selected-contract failure.
3. Contracts outside expiration range are rejected.
4. Contracts outside strike range are rejected.
5. Calls and puts remain in the reviewed universe while side decision is blocked.
6. Missing side decision prevents one selected contract.
7. Valid quote nearest at or before setup time is eligible for inspection.
8. Post-signal quote is rejected for setup-time eligibility.
9. Missing quote returns `unknown`.
10. Missing or unparseable bid/ask/bid-size/ask-size returns `unknown`.
11. Crossed or non-positive quote state rejects eligibility.
12. Spread and spread percent are calculated but do not produce clean/caution/fail without numeric thresholds.
13. Volume/open-interest fields are preserved for inspection but do not produce clean/caution/fail without timestamp and threshold decisions.
14. Missing one-contract ranking rule prevents trade choice.
15. Wrong symbol, wrong setup, future candle, future replay row, fill, broker/order/account, outcome, P&L, profitability, and readiness inputs are rejected.

## Current QQQ Target Implication

For `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`, this policy can support a future reviewed-universe regression fixture package.

It still cannot honestly produce:

- one selected option contract;
- option-context clean/caution/fail;
- execution-context clean/caution/fail;
- a fill;
- a trade result;
- P&L;
- proof;
- profitability;
- readiness.

## Result

Reviewed option-universe policy accepted for regression work: YES.

Selected-contract eligibility filter accepted for regression work: YES.

One selected contract chosen: NO.

Evidence filled: NO.

Backtest authorized: NO.

Trade chosen: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Intake-ready count changed: NO.

Proof accepted: NO.

Profitability claimed: NO.
