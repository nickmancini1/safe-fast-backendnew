# SAFE-FAST Technical Indicator and Evidence Component Inventory

## 1. Current conclusion

Status: PASS as a repo-backed docs-only inventory.

SAFE-FAST's current repo-backed indicator and evidence language is structure-first. The active logic and accepted local scaffolds confirm use of 1H 50 EMA, ATR distance/proximity, OHLCV/volume, trend/context labels, setup type, trigger, invalidation, blocker, freshness/stale/spent state, final verdict/final signal state, setup-time/no-hindsight boundaries, and terminal chart-outcome fields.

The repo does not support treating every common chart indicator as official SAFE-FAST logic. VWAP exists as a dxLink source/output field and as a planned caution indicator. Bollinger Bands exist in a planning doc only. SMA, MACD, RSI, relative volume, opening range, ORB, high of day, and low of day were not found outside the task prompt. Prior high appears in historical replay text as a level/context phrase, not as a standalone accepted indicator module.

This inventory does not authorize engine changes, live data, broker/order behavior, option P&L, account sizing, production work, generated reports, or live trade decisions.

## 2. Confirmed named technical indicators

| Term | Repo-backed status | Where found | Current use classification |
| --- | --- | --- | --- |
| 1H 50 EMA / EMA50 / EMA | CONFIRMED | `main.py`; `dxlink_candles.py`; `SAFE_FAST_LEVELS_AND_CONTEXT_INDICATORS_PLAN.md`; IWM/GLD review docs; replay tests | Active logic, source-data helper, tests, docs, and historical evidence reviews. Core structure/invalidation/extension reference. |
| ATR / 1H ATR(14) | CONFIRMED | `main.py`; `SAFE_FAST_LEVELS_AND_CONTEXT_INDICATORS_PLAN.md`; near-trigger trigger-card tests | Active logic and tests for distance/proximity context; planned as core structure reference in levels/context plan. |
| Volume / OHLCV | CONFIRMED | `main.py`; `dxlink_candles.py`; `historical_signal_replay` schemas/source CSVs/fixtures; `chart_trade_outcome_backtesting` schemas/fixtures/reports; IWM/GLD source validation reviews | Active data validation and evidence input; active chart-outcome candle field; volume climax/exhaustion appears in `main.py` as a caution/blocker-style evidence phrase. |
| VWAP | CONFIRMED BUT LIMITED | `dxlink_candles.py`; `SAFE_FAST_LEVELS_AND_CONTEXT_INDICATORS_PLAN.md` | Source/export field and docs-only planned intraday caution. Not confirmed as accepted setup decision logic. |
| Bollinger Bands | PLANNED ONLY | `SAFE_FAST_LEVELS_AND_CONTEXT_INDICATORS_PLAN.md` | Docs-only optional caution indicator. Not active logic, not accepted evidence, and not a hard blocker. |
| Trend / 24H trend/context | CONFIRMED | `main.py`; watcher/replay tests; `SAFE_FAST_LEVELS_AND_CONTEXT_INDICATORS_PLAN.md`; IWM/GLD review docs | Active context/evidence wording and tests; often unconfirmed in historical sample reviews when not source-backed. |
| Momentum | CONFIRMED AS GENERAL LANGUAGE ONLY | Broad docs/search results; not isolated as a named indicator module in active logic | Evidence/context language, not an accepted standalone technical indicator. |
| Prior high | LIMITED LEVEL CONTEXT | `historical_signal_replay` fixture text | Historical replay wording for completed trigger/reclaim context. Not confirmed as a standalone official indicator. |
| Prior low | NOT CONFIRMED | No repo hit outside prompt in the required search | Not accepted as an official term by this inventory. |
| SMA | NOT CONFIRMED | No repo hit outside prompt in the required search | Not accepted. |
| Moving average | NOT CONFIRMED AS TERM | No exact repo hit outside prompt in the required search | EMA is confirmed; generic moving average wording is not treated as official. |
| MACD | NOT CONFIRMED | No repo hit outside prompt in the required search | Not accepted. |
| RSI | NOT CONFIRMED | No repo hit outside prompt in the required search | Not accepted. |
| Relative volume | NOT CONFIRMED | No repo hit outside prompt in the required search | Not accepted. |
| Opening range / ORB | NOT CONFIRMED | No repo hit outside prompt in the required search | Not accepted. |
| High of day / low of day | NOT CONFIRMED | No repo hit outside prompt in the required search | Not accepted as named indicators. |

## 3. Confirmed SAFE-FAST evidence components

| Evidence component | Repo-backed status | Where found | Current plan status |
| --- | --- | --- | --- |
| Setup family/type: Ideal, Clean Fast Break, Continuation | CONFIRMED | `main.py`; replay fixtures/tests; historical replay reports; IWM/GLD docs; build state | Active SAFE-FAST setup universe. |
| Trigger / trigger state / trigger card | CONFIRMED | `main.py`; `watcher_foundation/trigger_card.py`; `watcher_foundation/constants.py`; replay tests; trigger-card schema/review docs | Active output/evidence surface and current watcher-foundation contract. |
| Invalidation / invalidation level / 1H EMA invalidation | CONFIRMED | `main.py`; chart-outcome schemas/tooling; replay fixtures; IWM/GLD docs; account-mode plan | Active evidence component, but candidate-level values remain unavailable for some IWM/GLD chart-only reviews. |
| Blocker / primary blocker / caution | CONFIRMED | `main.py`; `watcher_foundation/diagnostics.py`; chart/replay schemas and fixtures; build-state sections | Active no-trade and diagnostic evidence component. |
| Freshness / fresh / stale / spent / no fresh trigger | CONFIRMED | `watcher_foundation/constants.py`; `watcher_foundation/diagnostics.py`; `watcher_foundation/trigger_card.py`; tests; replay reports | Active watcher/replay evidence component. |
| Final verdict / final signal | CONFIRMED | `replay/run_replay.py`; historical replay schemas/reports; chart-outcome inputs; docs | Active replay/evidence output. |
| Setup-time / no-hindsight boundary | CONFIRMED | build state; historical replay reviews; chart-only outcome reviews | Active evidence rule. Future candles may measure outcome only after setup evidence is frozen. |
| Terminal outcome / terminal condition | CONFIRMED | `chart_trade_outcome_backtesting` schemas/tooling/reports; chart-only reviews | Active chart-outcome/backtesting evidence component where generated chart-outcome inputs exist; unavailable for docs-only IWM/GLD chart-only reviews without accepted generated inputs. |
| Winner selection / selected setup type | CONFIRMED | chart-outcome input schema; chart-outcome fixtures; replay tests; watcher stable winner tests | Active stability component for overlapping setups. |
| Room / first wall / next pocket / support-resistance levels | CONFIRMED AS PLAN AND EVIDENCE LANGUAGE | `SAFE_FAST_LEVELS_AND_CONTEXT_INDICATORS_PLAN.md`; `main.py`; build state | Important planned/partially active evidence layer; level-ranking implementation is not authorized by this inventory. |
| 24H/daily, macro, IV, event, headline/news context | CONFIRMED AS EVIDENCE COMPONENTS, OFTEN UNCONFIRMED | `main.py`; IWM/GLD reviews; watcher/headline docs/tests | Active boundary/status fields, but often `UNCONFIRMED` unless source-backed. |
| Liquidity / spread quality / option/account risk | CONFIRMED AS FUTURE REQUIREMENT, NOT CURRENT PROOF | account-mode plan; build-state execution-mechanics section | Future trading-usefulness/execution evidence only; not current trade approval or P&L proof. |

## 4. Active vs planned vs stale/uncertain terms

Active or current-contract terms:

- 1H 50 EMA / EMA50.
- ATR distance/proximity.
- OHLCV and volume validation.
- Trend/24H context status.
- Ideal, Clean Fast Break, Continuation.
- Trigger, trigger state, trigger card, near-trigger, triggered, pending, stale, spent.
- Invalidation, blocker, caution, no-trade reason, final verdict.
- Setup-time/no-hindsight boundary.
- Terminal chart outcome where chart-outcome inputs are accepted.
- Winner selection / selected setup type.

Planned or secondary terms:

- VWAP as a secondary intraday caution and source/export field.
- Bollinger Bands as optional extension/exhaustion context only.
- VIX, TICK, ADX, breadth/advance-decline as optional context cautions in the levels/context plan.
- Support/resistance level ranking, room classification, first wall, next pocket, hidden levels.

Stale, uncertain, or not accepted by this inventory:

- SMA, MACD, RSI, relative volume, opening range, ORB, high of day, low of day: no repo source found outside the task prompt.
- Prior high: found as historical replay wording only; not accepted here as a standalone indicator.
- Generic momentum: repo language only unless tied to a specific accepted setup/evidence field.
- Any indicator not present in repo sources must remain unaccepted until a later source-backed design, test, and build-state update exists.

## 5. Source map

Major sources searched:

- `main.py`
- `dxlink_candles.py`
- `watcher_foundation/`
- `tests/`
- `replay/`
- `historical_signal_replay/`
- `chart_trade_outcome_backtesting/`
- `SAFE_FAST_LEVELS_AND_CONTEXT_INDICATORS_PLAN.md`
- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`
- IWM/GLD replay readiness, fixture specification, real historical replay, source validation, and chart-only outcome review docs.
- SPY/QQQ generated replay and chart-outcome fixtures/reports where present.

Minimum required search terms were checked:

- Confirmed in repo-backed sources: VWAP, EMA, ATR, volume, Bollinger, prior high, trend, momentum, trigger, invalidation, blocker, freshness, final signal/final verdict, Continuation, Clean Fast Break, Ideal, setup-time, terminal outcome.
- Not found outside the task prompt: SMA, moving average as exact phrase, MACD, RSI, relative volume, opening range, ORB, prior low, high of day, low of day.

## 6. Gaps and unresolved questions

- Whether VWAP should ever become an active caution field remains unresolved; current repo support is source/export plus planning only.
- Whether Bollinger Bands, VIX, TICK, ADX, or breadth should be implemented remains unresolved and must not be added all at once.
- Generic momentum should not be promoted to a standalone indicator without repo-backed rules and tests.
- Prior high/low, prior day high/low, shelf highs/lows, first wall, next pocket, and room classification need a separate level-mapping design and regression path before promotion.
- IWM/GLD docs-only chart outcomes still have missing generated-outcome prerequisites where trigger/invalidation/risk denominator/terminal conditions are not accepted.
- The inventory does not determine profitability and does not prove trade usefulness.

## 7. Smallest next evidence-backed fix

Do not add indicators yet. The smallest next evidence-backed fix is a bounded 1H/24H support-resistance and room-classification design/test plan, using existing repo language from `SAFE_FAST_LEVELS_AND_CONTEXT_INDICATORS_PLAN.md`, focused on level names, level-ranking enums, source fields, unavailable-field semantics, and no-trade/caution wording. That later task should remain local and docs/test scoped until approved, and must not touch broker/execution, option P&L, account sizing, production/deploy, or live trade decisions.
