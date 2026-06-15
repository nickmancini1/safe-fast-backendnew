# SAFE-FAST Day 41 QQQ CFB Open-Interest Gate Decision

## Scope

Target candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`.

Setup type: QQQ Clean Fast Break.

Signal/setup time: `2026-04-13T12:30:00-04:00` (`2026-04-13T16:30:00Z`).

Top-ranked contract: `QQQ   260427C00615000`.

Instrument id: `1023411456`.

Baseline from task file: `b6569f4 Rerun QQQ option context with trades statistics`.

This document decides the first QQQ CFB option-context open-interest gate after the wider quote and trades/statistics reruns. It does not fill evidence, change selector code, backtest, calculate P&L, choose a real trade, claim proof or profitability, mark QQQ ready, or change intake-ready status.

## Current Facts

The accepted selector still ranks the same top contract:

- contract: `QQQ   260427C00615000`;
- expiration: `2026-04-27`;
- strike: `615`;
- side: call;
- DTE: `14`;
- instrument id: `1023411456`.

The latest rerun facts are:

| Gate | Current result |
| --- | --- |
| Setup-time-safe quote | PASS. Wider top-contract TCBBO file has `28` setup-time-safe rows. |
| Nearest setup-time-safe quote | `2026-04-13T16:06:30.640301037Z`, bid `7.76`, ask `7.80`, spread `0.04`, bid size `3`, ask size `31`. |
| Spread | PASS, `0.04 <= 0.15`. |
| Spread percent | PASS, about `0.5141% <= 2.00%`. |
| Bid size | PASS, `3 >= 1`. |
| Ask size | PASS, `31 >= 1`. |
| Through-setup trade volume | PASS, `65 >= 1` from `28` setup-time-safe trade rows. |
| Setup-time-safe same-contract open interest | MISSING. The new top-contract statistics file has `0` rows. |

The existing selector result remains `abstain` with rejection reason `top_ranked_contract_failed_no_fallback`.

## Decision

Open-interest gate decision: keep same-contract setup-time-safe open interest required for the first QQQ CFB option-context rule.

Rule change accepted: NO.

Volume-only liquidity accepted for regression: NO.

`open_interest_status=unknown` allowed as a passing option-context substitute: NO.

Another source required before `option_context_status` can pass: YES.

The current QQQ case remains:

- `open_interest_status=unknown`;
- `option_context_status=unknown`;
- selector result `abstain`;
- no fallback to another strike or expiration.

## Rationale

The trade-plan completeness gate explicitly includes volume, open-interest, and liquidity minimums. The current accepted one-contract selector also requires same-contract open interest of at least `1` using timestamp-safe statistics. The latest evidence cures the quote and trade-volume blockers but does not supply any setup-time-safe open-interest row.

Treating missing open interest as clean, caution, or pass would weaken the accepted liquidity gate without a regression-backed human decision. Treating trade volume alone as sufficient would also change the rule from "volume and open interest" to "volume only"; no accepted fixture set or decision currently supports that change.

After-signal statistics remain forbidden. The existing full-day statistics rows for the top contract occur after setup time, and the new top-contract statistics file contains no rows. Neither can be used to fake or infer setup-time-safe open interest.

## Allowed Statuses

For this gate decision, the allowed open-interest component statuses are:

- `pass`: same-contract open interest is numeric, at least `1`, and supported by accepted timestamp-safe statistics for the selected contract.
- `fail`: same-contract open interest is numeric, timestamp-safe, and below `1`.
- `unknown`: same-contract open interest is missing, unparseable, not same-contract, timestamp-unsafe, or only available from a forbidden after-signal statistics row.

For the first QQQ CFB option-context rule, `unknown` does not pass the open-interest gate. It keeps option context blocked.

## Required Raw Inputs

Required raw inputs for an open-interest pass remain:

- exact option contract identity by `instrument_id` or symbol;
- Databento or other accepted source field that explicitly represents open interest;
- same-contract row matching `QQQ   260427C00615000` / `instrument_id=1023411456`;
- numeric open-interest value;
- statistics `ts_event` at or before `2026-04-13T16:30:00Z`;
- `ts_ref` at or before `2026-04-13T16:30:00Z` when `ts_ref` is present;
- no use of future candles, future replay rows, after-signal statistics, fills, P&L, proof, profitability, or readiness.

## Missing Open-Interest Behavior

If setup-time-safe same-contract open interest is missing:

- do not infer it from trade volume;
- do not infer it from quote size;
- do not infer it from nearby contracts;
- do not use after-signal statistics;
- do not fall back to another ranked contract after the top-ranked contract fails;
- classify the open-interest component as `unknown`;
- keep `option_context_status=unknown`.

## QQQ Case Classification

For `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`:

- quote gate: pass;
- spread gate: pass;
- spread-percent gate: pass;
- bid-size gate: pass;
- ask-size gate: pass;
- trade-volume gate: pass;
- open-interest gate: `unknown`;
- contract-selection status: `abstain`;
- option-context status: `unknown`.

This is a blocker-preserving classification only. It is not a trade choice, no-trade proof, failed trade, P&L result, profitability result, or readiness result.

## Regression Fixture Updates Needed

No selector change is accepted by this decision, so no immediate fixture update is required.

If a later task implements explicit open-interest component statuses while preserving the same gate, add regression fixtures for:

1. timestamp-safe open interest at `1` passes;
2. timestamp-safe open interest `0` fails;
3. missing open interest returns `unknown` and selector abstains;
4. header-only statistics file returns `unknown` and selector abstains;
5. after-signal `ts_event` statistics row is rejected;
6. after-signal `ts_ref` statistics row is rejected;
7. trade volume `65` does not override missing open interest;
8. quote size does not override missing open interest;
9. nearby-contract open interest does not satisfy same-contract open interest;
10. top-ranked open-interest failure still does not allow fallback selection.

If a later human decision changes the gate to volume-only or allows missing open interest as a passable caution, that later decision must define a separate fixture set before selector changes.

## Selector Changes Needed

Selector changes needed now: NONE.

The existing selector already enforces:

- minimum open interest `1`;
- timestamp-safe statistics;
- missing-data abstain;
- no fallback after top-ranked gate failure.

If a later task adds explicit `open_interest_status` reporting, it should be additive reporting only unless a new accepted rule changes the pass/fail behavior.

## Still Missing Source Or Human Decision

Exact missing source:

- a same-contract open-interest/statistics row for `QQQ   260427C00615000` / `instrument_id=1023411456`, with accepted timestamp fields at or before `2026-04-13T16:30:00Z`.

Alternative human decision needed if the source cannot be obtained:

- an explicit accepted rule, with regression fixtures first, that changes the first QQQ CFB option-context liquidity gate to volume-only or permits missing setup-time-safe open interest to classify as a non-passing `caution` or other status.

Until one of those exists, `option_context_status` cannot pass.

## Safety Boundaries

Evidence filled: NO.

Selector code changed: NO.

Backtest authorized: NO.

Real trade chosen: NO.

P&L calculated: NO.

QQQ candidate marked ready: NO.

Intake-ready count changed: NO.

Proof accepted: NO.

Profitability claimed: NO.

Raw Databento files changed: NO.
