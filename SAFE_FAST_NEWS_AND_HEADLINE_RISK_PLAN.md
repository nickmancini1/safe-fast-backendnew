# SAFE-FAST News and Headline Risk Plan

## Status

Planned future risk layer.

This is a plan document only. Do not add engine behavior yet.

## Purpose

SAFE-FAST may later add a news and headline risk layer.

This layer must not replace the setup model.

SAFE-FAST remains:

1. Setup first.
2. Stage second.
3. Structure / risk / news context third.
4. Trade style last.

News is a risk layer, not a signal engine.

Do not create headline-chasing behavior.

## Risk levels

Future news/headline risk levels:

- `NEWS_CLEAR`
- `NEWS_CAUTION`
- `NEWS_BLOCK`
- `NEWS_UNCONFIRMED`

Default rule:

Most news should create caution, not a hard blocker.

Hard block only when the news directly threatens:

- the setup
- the trade window
- the intended hold window
- overnight gap risk
- liquidity / execution safety
- event-driven invalidation risk

If data is unavailable, do not invent it. Mark it `NEWS_UNCONFIRMED`.

## Scheduled macro events

Track planned macro events including:

- FOMC rate decision
- FOMC press conference
- Fed minutes
- Fed speakers
- CPI
- PPI
- PCE inflation
- NFP / unemployment
- Jobless claims
- JOLTS
- ISM / PMI
- Retail sales
- GDP
- Treasury auctions

Rules:

- Major macro today may become `NEWS_BLOCK` if structure is not pristine.
- Major macro today is usually at least `NEWS_CAUTION`.
- Major macro tomorrow creates overnight caution.
- Event-day IV creates caution or block depending on structure, liquidity, and trade window.
- Do not invent macro data if unavailable. Use `NEWS_UNCONFIRMED`.

Examples:

- FOMC decision in 30 minutes: likely `NEWS_BLOCK`.
- CPI tomorrow morning: `NEWS_CAUTION`, overnight not approved.
- Fed speaker during trade window: usually `NEWS_CAUTION`, unless immediate and market-moving.
- Treasury auction during weak structure/rate-sensitive symbol: possible `NEWS_CAUTION` or `NEWS_BLOCK`.

## Earnings and mega-cap events

SAFE-FAST trades only:

- SPY
- QQQ
- IWM
- GLD

Even so, mega-cap earnings can move index ETFs.

Track especially for SPY / QQQ:

- NVDA
- AAPL
- MSFT
- AMZN
- GOOGL
- META
- TSLA
- major semiconductor names
- major banks

Rules:

- Mega-cap earnings same day or next morning = caution.
- Earnings after close = overnight caution.
- Earnings directly affecting QQQ/SPY components = caution unless combined with other risk.
- Do not hard-block a clean setup from earnings alone unless risk is immediate and material.
- Multiple large component events clustered together may raise risk.
- If earnings data is unavailable, mark `NEWS_UNCONFIRMED`.

Examples:

- NVDA earnings after close while holding QQQ overnight: `NEWS_CAUTION`, possibly `NO_OVERNIGHT`.
- AAPL/MSFT same week during weak SPY structure: `NEWS_CAUTION`.
- Huge surprise from a top-weighted component during active setup window: possible `NEWS_BLOCK`.

## SEC filings / corporate shock events

Possible sources later:

- SEC 8-K
- earnings release
- guidance cut
- CEO/CFO resignation
- M&A
- bankruptcy risk
- SEC investigation
- material agreement
- major lawsuit / regulatory action
- offering / dilution

Rules:

- For index ETFs, corporate shock events are usually caution.
- For huge component shock events, raise to `NEWS_BLOCK` only if the affected company is large enough to move the ETF and the timing directly threatens the trade.
- Isolated small-cap corporate filings should not affect SPY/QQQ/IWM/GLD unless market-wide contagion risk exists.
- If filing/news source is unavailable, mark `NEWS_UNCONFIRMED`.

Examples:

- Top QQQ component guidance cut premarket: `NEWS_CAUTION` or `NEWS_BLOCK` depending on severity and setup quality.
- CEO resignation at a small non-index component: likely `NEWS_CLEAR` for SAFE-FAST ETF purposes.
- Major bank shock affecting financial sector and SPY/IWM risk: possible `NEWS_BLOCK`.

## Market-wide headline risk

Track:

- war / geopolitical escalation
- tariffs
- sanctions
- election shock
- government shutdown
- banking stress
- credit event
- debt ceiling
- oil shock
- major cyberattack
- major exchange / broker outage
- unexpected Fed comments
- emergency central bank action

Rules:

- Market-wide shock = `NEWS_CAUTION` by default.
- `NEWS_BLOCK` only if immediate, unresolved, and likely to create gap/headline risk during the intended hold window.
- Headline risk should not replace setup logic.
- Headline risk should not create trades.
- Headline risk may reduce allowed trade style from overnight to same-day-only or watch-only.

Examples:

- Active geopolitical escalation before close: `NEWS_CAUTION`, overnight caution.
- Emergency central bank action during session: possible `NEWS_BLOCK`.
- Broker/exchange outage affecting execution: possible `NEWS_BLOCK`.
- Government shutdown headline with no immediate market reaction: likely `NEWS_CAUTION`.

## ETF-specific news context

### SPY / QQQ

Most relevant:

- mega-cap earnings
- Fed / rates
- CPI / PCE / NFP
- Treasury yields
- AI / semiconductor headlines
- banking stress

Rules:

- Mega-cap concentration matters.
- Rate-sensitive events matter.
- AI/semiconductor headlines can affect QQQ heavily.
- Banking stress can affect SPY and broad risk appetite.

### IWM

Most relevant:

- rates
- credit stress
- regional banks
- small-cap breadth
- dollar / liquidity conditions
- economic growth data

Rules:

- IWM is more sensitive to credit stress and regional banks.
- Weak breadth plus credit stress can raise risk.
- Rate shocks can affect small-cap risk appetite.

### GLD

Most relevant:

- real yields
- dollar strength
- Fed policy
- inflation data
- geopolitical risk
- central bank gold headlines

Rules:

- GLD news risk should account for rates, real yields, dollar, and geopolitical shock.
- Inflation / Fed data can be caution or block depending on timing.
- Geopolitical risk can support GLD but still increase gap/headline risk.

## Future user-facing output fields

Eventually SAFE-FAST should expose:

```json
{
  "news_risk_level": "NEWS_CLEAR | NEWS_CAUTION | NEWS_BLOCK | NEWS_UNCONFIRMED",
  "news_risk_reason": "short plain-English reason",
  "scheduled_event_risk": "clear | caution | block | unconfirmed",
  "earnings_risk": "clear | caution | block | unconfirmed",
  "headline_risk": "clear | caution | block | unconfirmed",
  "overnight_news_permission": "NO_OVERNIGHT | OVERNIGHT_CAUTION | OVERNIGHT_ALLOWED | UNCONFIRMED"
}
```

Possible trade-style interaction:

- `WATCH_ONLY`
- `SAME_DAY_ONLY`
- `FAST_SWING_ALLOWED`
- `OVERNIGHT_ALLOWED`
- `NO_TRADE`

News should not decide setup type or stage.

## Example user-facing outputs

### Caution example

```text
Setup: Continuation
Stage: Pending Trigger
News risk: CAUTION
Reason: CPI tomorrow morning; overnight hold not approved.
Trade style: SAME_DAY_ONLY or WATCH_ONLY.
```

### Hard block example

```text
Setup: Ideal
Stage: Valid
News risk: BLOCK
Reason: FOMC decision in 30 minutes.
Action: NO TRADE.
```

### Unconfirmed example

```text
Setup: Clean Fast Break
Stage: Developing
News risk: UNCONFIRMED
Reason: News/calendar data unavailable; do not assume clear.
Action: WATCH_ONLY until context is confirmed.
```

## Build order

Build in this order only after on-demand recognition/stage correctness is stable enough:

1. Create this plan document.
2. Add contract tests for:
   - `NEWS_CLEAR`
   - `NEWS_CAUTION`
   - `NEWS_BLOCK`
   - `NEWS_UNCONFIRMED`
3. Add scheduled macro event logic first.
4. Add earnings calendar logic second.
5. Add SEC filing / 8-K logic third.
6. Add general headline risk last.
7. Add user-facing output surface.
8. Keep news mostly as caution, not hard blocker.
9. Do not let news replace setup/stage logic.

## Contract test targets

Future tests should protect:

- clear calendar context returns `NEWS_CLEAR`
- unavailable calendar/news context returns `NEWS_UNCONFIRMED`
- major macro today returns `NEWS_CAUTION` or `NEWS_BLOCK` depending on timing/structure
- major macro tomorrow returns overnight caution
- high IV/event-day context does not erase setup identity
- mega-cap earnings create caution for SPY/QQQ
- earnings after close creates overnight caution
- market-wide unresolved shock can create `NEWS_BLOCK`
- normal headlines do not block a clean setup by themselves
- news cannot convert a bad setup into a trade
- news cannot replace setup/stage logic
- user-facing response shows news reason clearly

## Hard-block policy

Only use `NEWS_BLOCK` when the risk is immediate and material.

Examples of possible hard block:

- FOMC decision or press conference inside intended trade window
- CPI/NFP minutes before entry
- emergency central bank action
- active exchange/broker outage
- severe geopolitical escalation during intended hold window
- major component shock large enough to directly threaten SPY/QQQ trade
- event-day IV plus weak structure/liquidity

## Caution policy

Use `NEWS_CAUTION` for most news risk.

Examples:

- CPI tomorrow
- FOMC later this week
- Fed speaker today
- mega-cap earnings after close
- headline risk not yet resolved
- elevated IV without direct setup threat
- sector-specific headline that may affect ETF but is not immediate

## Unconfirmed policy

Use `NEWS_UNCONFIRMED` when data is missing.

Rules:

- Do not invent calendar data.
- Do not invent earnings dates.
- Do not invent SEC filings.
- Do not invent headline context.
- If a tool/source is unavailable, mark unconfirmed.
- Unconfirmed can force watch-only if the intended hold depends on news clarity.

## SAFE-FAST principle

Setup first.

Stage second.

Structure / risk / news context third.

Trade style last.

News is a risk layer, not a signal engine.

Do not create headline-chasing behavior.

Do not let news override a bad setup into a trade.

Do not let news erase setup identity.

Do not add engine behavior until this plan has tests and the on-demand setup/stage foundation is stable.
