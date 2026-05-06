# SAFE-FAST Levels and Context Indicators Plan

## Purpose

SAFE-FAST should remain a structure-first system.

This layer should improve:
- support / resistance awareness
- room quality
- first wall detection
- next pocket detection
- hidden level warnings
- context cautions from market internals and indicators

This layer should not turn SAFE-FAST into indicator soup.

Core setup decisions still come from:
- Ideal
- Clean Fast Break
- Continuation
- 1H + 24H structure
- 1H 50 EMA
- room to next level
- valid trigger
- invalidation clarity
- liquidity / risk fit

Additional indicators should usually create cautions, not automatic blockers.

## Priority Order

### Priority 1 — Support / Resistance Mapping

This is the most important next layer.

SAFE-FAST needs better detection of:
- nearby resistance above long setups
- nearby support below short setups
- first wall
- next pocket
- hidden support / resistance
- magnet levels
- shelf high / shelf low
- prior breakout / reclaim areas
- prior rejection zones
- prior day high / low
- current week high / low
- major 24H levels

This should be built before secondary indicators like TICK, VIX, ADX, or Bollinger Bands.

## Timeframe Level Mapping

### 1H Levels

Use recent RTH 1H structure.

Suggested lookback:
- minimum: last 10 RTH sessions
- preferred: last 20-30 RTH sessions
- optional extended: last 40-60 RTH sessions when volatility regime requires it

1H levels should detect:
- recent swing highs
- recent swing lows
- shelf highs
- shelf lows
- breakout / reclaim areas
- repeated rejection zones
- repeated support zones
- prior day high / low
- current week high / low
- levels with multiple touches
- levels close enough to affect trade room

1H levels are used mainly for:
- entry quality
- clear room
- first wall
- next pocket
- trigger validation
- continuation shelf validation

### 24H Levels

Use broader daily structure.

Suggested lookback:
- minimum: last 3 months
- preferred: last 6 months
- optional extended: last 12 months for major levels

24H levels should detect:
- major swing highs
- major swing lows
- prior breakout zones
- prior failed breakout zones
- daily supply / resistance
- daily demand / support
- major reclaim / loss areas
- all-time high / open-air context when relevant

24H levels are used mainly for:
- major room context
- trend / supportive context
- hidden resistance / support
- whether a move is running into a bigger wall
- overnight / swing risk

## Level Ranking

Every detected level should be ranked.

Suggested ranking:
- MAJOR_LEVEL
- MODERATE_LEVEL
- MINOR_LEVEL
- MAGNET_LEVEL
- IGNORE

Ranking factors:
- timeframe: 24H levels rank above 1H levels
- recency
- number of touches
- reaction size
- whether level caused rejection
- whether level caused reclaim
- whether level aligns with shelf high / shelf low
- whether level aligns with prior day / week high / low
- whether level is close enough to affect trade room

## Room Classification

Room should not be binary only.

Use:
- ROOM_PASS
- ROOM_CAUTION
- ROOM_FAIL

### ROOM_PASS

Enough distance to next meaningful wall.
Trade has room to work toward target.

### ROOM_CAUTION

Room is workable but tight.
This should surface as caution.
It should not automatically block if setup, trigger, and structure are clean.

### ROOM_FAIL

Cramped room.
Next major wall is too close.
Trade requires hoping through a level.
Verdict should be NO TRADE.

## Indicator Roles

### Core Indicators / Structure References

These can influence trade gates:
- 1H 50 EMA
- 24H structure
- 1H ATR(14)
- room / first wall / next pocket
- shelf high / shelf low
- invalidation level
- extension state
- liquidity / spread quality
- IV acceptability

### Context / Caution Indicators

These should usually warn, not automatically block:
- VIX
- TICK
- advance-decline / ADV minus DECL
- VWAP
- ADX
- Bollinger Bands

## Specific Context Indicator Rules

### VIX

Use as market-risk context.

Possible outputs:
- VIX_NORMAL
- VIX_ELEVATED
- VIX_RISING_CAUTION
- VIX_SPIKE_RISK

VIX should not automatically block a clean setup unless combined with:
- major macro event
- weak structure
- bad liquidity
- high IV
- overnight hold risk

### TICK

Use as intraday breadth / pressure context.

Possible outputs:
- TICK_SUPPORTIVE
- TICK_MIXED
- TICK_WEAK_CAUTION
- TICK_EXTREME_EXHAUSTION_CAUTION

TICK should not override 1H structure.
It can help decide same-day timing.

### Advance-Decline / Breadth

Use as market participation context.

Possible outputs:
- BREADTH_SUPPORTIVE
- BREADTH_MIXED
- BREADTH_WEAK_CAUTION
- BREADTH_DIVERGENCE_CAUTION

Breadth weakness should caution long trades, not automatically block them.

### VWAP

Use as intraday location context.

Possible outputs:
- ABOVE_VWAP_SUPPORTIVE
- BELOW_VWAP_CAUTION
- VWAP_RECLAIM_PENDING
- VWAP_LOSS_CAUTION

VWAP should be secondary to 1H 50 EMA.
For same-day-only trades, VWAP can matter more.

### ADX

Use as regime / trend-strength context.

Possible outputs:
- TREND_STRENGTH_SUPPORTIVE
- LOW_TREND_CHOP_CAUTION
- STRONG_TREND_SUPPORTIVE
- EXHAUSTED_TREND_CAUTION

ADX should not decide setup type.

### Bollinger Bands

Use as extension / exhaustion context only.

Possible outputs:
- BAND_NORMAL
- UPPER_BAND_EXTENSION_CAUTION
- LOWER_BAND_EXTENSION_CAUTION
- BAND_SQUEEZE_CONTEXT
- BAND_WALK_CONTEXT

Bollinger Bands should not replace ATR / EMA extension logic.

## User-Facing Output

SAFE-FAST should eventually show:
- nearest 1H support
- nearest 1H resistance
- nearest 24H support
- nearest 24H resistance
- first wall
- next pocket
- room classification
- hidden level warning if present
- context cautions:
  - 24H countertrend
  - extension caution
  - room caution
  - VIX caution
  - breadth caution
  - VWAP caution
  - event risk

## Build Rule

Do not add all indicators at once.

Build order:
1. Design doc
2. Replay / contract tests for 1H and 24H level mapping
3. Level detection helper
4. Room classification tests
5. User-facing level output tests
6. Only then add optional context indicators
7. Indicators must be cautions first, not hard blockers

## Immediate Next Build Layer

The next build layer should be:

1H / 24H support-resistance mapping and level ranking.

This directly supports the existing SAFE-FAST rule:
"Clear room to the next major level is required."
