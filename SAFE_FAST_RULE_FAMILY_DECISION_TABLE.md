# SAFE-FAST Rule Family Decision Table

## Scope

This table makes hard build-only decisions for the nine freshness/final-signal and blocker/caution rule families that block the seven strict Day 39 rows.

This is rule clarification, not proof review. It does not inspect outcomes, accept proof, claim profitability, authorize live data, authorize alerts, authorize broker/order/account work, or authorize changes to `main.py`.

Allowed decisions:

- `DEFINE_FROM_REPO_EVIDENCE`
- `SOURCE_DATA_INSUFFICIENT`
- `KILL_OR_NARROW_SETUP_SYMBOL_PATH`

Current intake-ready count: 0.

Proof accepted: NO.

Profitability claim made: NO.

## Decisions

| Rule family | Hard decision | Affected setup type | Affected symbols | Affected candidate IDs | Repo evidence checked | Exact reason | Intake-ready promotion meaning | Smallest next action | Blocks proof review |
|---|---|---|---|---|---|---|---|---|---|
| Clean Fast Break expiry | `SOURCE_DATA_INSUFFICIENT` | Clean Fast Break | QQQ, SPY | `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`; `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`; `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | `SAFE_FAST_DAY38_TOP_5_REPLAY_SETUP_TIME_FIELD_COMPLETION_REVIEW.md`; `SAFE_FAST_DAY38_SPY_QQQ_BATCH_CANDIDATE_EXPANSION_REVIEW.md`; `historical_signal_replay/reports/third_real_spy_clean_fast_break_replay_v1_signal_log.jsonl` | Repo rows show initial-break, higher-base, fresh-break, and spent lifecycle labels, but no accepted source-backed expiry rule defines when a Clean Fast Break signal has become stale or spent for intake promotion. | All affected Clean Fast Break rows remain blocked; `final_verdict=TRADE` cannot satisfy expiry. | Define a source-backed Clean Fast Break expiry rule with regression rows before any Clean Fast Break proof review. | YES |
| Clean Fast Break gap context | `SOURCE_DATA_INSUFFICIENT` | Clean Fast Break | QQQ | `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`; `historical_signal_replay/reports/first_real_qqq_clean_fast_break_replay_v1_signal_log.jsonl` | The QQQ source data has OHLCV plus unconfirmed context fields and the replay log has lifecycle labels, but no source-backed gap-context completeness field exists for the setup-time decision. | The QQQ gap Clean Fast Break row remains blocked from intake-ready. | Add source-backed gap-context evidence fields or keep QQQ gap Clean Fast Break out of proof review. | YES |
| Continuation next-session freshness | `KILL_OR_NARROW_SETUP_SYMBOL_PATH` | Continuation | QQQ | `QQQ-REAL-HISTORICAL-CONTINUATION-001` | `SAFE_FAST_DAY38_TOP_5_REPLAY_SETUP_TIME_FIELD_COMPLETION_REVIEW.md`; `historical_signal_replay/reports/first_real_qqq_continuation_replay_v1_signal_log.jsonl` | The repo records a 2026-04-30 15:30 Continuation trigger and a later spent row, but does not authorize next-session carry-forward freshness. The path is narrowed away from next-session Continuation entries until source-backed rules exist. | QQQ next-session Continuation is outside the narrowed Continuation path and cannot become intake-ready under current repo evidence. | Either source a tested next-session carry-forward rule or exclude next-session Continuation rows from the intake-ready path. | YES |
| Continuation session-boundary freshness | `KILL_OR_NARROW_SETUP_SYMBOL_PATH` | Continuation | QQQ, SPY | `QQQ-REAL-HISTORICAL-CONTINUATION-001`; `SPY-REAL-HISTORICAL-CONTINUATION-001` | `SAFE_FAST_ARCHITECT_CONTROL_AND_PROJECT_TIGHTENING.md`; `SAFE_FAST_DAY38_TOP_5_REPLAY_SETUP_TIME_PACKET.md` | Session-boundary handling is a documented blocker and no source-backed rule defines when Continuation signals survive the boundary. The setup-symbol path is narrowed to Continuation rows without session-boundary dependency. | Continuation rows with session-boundary dependency cannot become intake-ready; next-session rows are outside the narrowed path and same-session rows must still pass intrabar ordering plus complete context/caution gates. | Source and test Continuation session-boundary requirements before reviewing these rows as proof candidates. | YES |
| Ideal stale/spent expiry | `SOURCE_DATA_INSUFFICIENT` | Ideal | QQQ, SPY | `QQQ-REAL-HISTORICAL-IDEAL-001`; `SPY-REAL-HISTORICAL-IDEAL-001` | `SAFE_FAST_DAY38_TOP_5_REPLAY_SETUP_TIME_FIELD_COMPLETION_REVIEW.md`; `historical_signal_replay/reports/first_real_qqq_ideal_replay_v1_signal_log.jsonl`; `historical_signal_replay/reports/second_real_spy_ideal_replay_v1_signal_log.jsonl` | Ideal replay rows show triggers and later spent lifecycle states, but repo evidence does not define the accepted stale/spent expiry rule at setup time. | QQQ/SPY Ideal rows remain blocked from intake-ready. | Define and regression-test Ideal stale/spent expiry before Ideal proof review. | YES |
| Ideal fast-swing freshness | `KILL_OR_NARROW_SETUP_SYMBOL_PATH` | Ideal | QQQ | `QQQ-REAL-HISTORICAL-IDEAL-001` | `SAFE_FAST_DAY38_TOP_5_REPLAY_SETUP_TIME_FIELD_COMPLETION_REVIEW.md` | The QQQ Ideal packet leaves fast-swing hold freshness unfilled and no accepted rule says the fast-swing path remains actionable. The QQQ fast-swing Ideal path is narrowed out until it earns a source-backed rule. | QQQ fast-swing Ideal cannot become intake-ready under current evidence. | Either define tested fast-swing freshness or exclude fast-swing Ideal rows from the proof-review pool. | YES |
| Intrabar ordering | `KILL_OR_NARROW_SETUP_SYMBOL_PATH` | Continuation | SPY | `SPY-REAL-HISTORICAL-CONTINUATION-001` | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`; `SAFE_FAST_DAY38_TOP_5_REPLAY_SETUP_TIME_FIELD_COMPLETION_REVIEW.md` | Available SPY source is completed 1H OHLCV and cannot prove the order of trigger, pullback, and invalidation events inside the setup candles. The SPY Continuation intrabar-dependent path is narrowed out unless lower-timeframe evidence exists. | SPY Continuation intrabar-dependent rows are outside the narrowed path and cannot become intake-ready under current repo evidence. | Provide lower-timeframe source rows or exclude intrabar-dependent Continuation rows from proof review. | YES |
| Wide-risk / room threshold | `KILL_OR_NARROW_SETUP_SYMBOL_PATH` | Ideal | QQQ | `QQQ-REAL-HISTORICAL-IDEAL-001` | `SAFE_FAST_DAY38_TOP_5_REPLAY_SETUP_TIME_FIELD_COMPLETION_REVIEW.md`; `SAFE_FAST_DAY39_COMBINED_HANDOFF_AND_FAST_CANDIDATE_FUNNEL.md` | QQQ Ideal wide chart-risk and room are documented as unresolved trade-usefulness problems, and no accepted threshold defines enough room after risk and costs. The wide-risk QQQ Ideal path is narrowed out until thresholds exist. | QQQ wide-risk Ideal cannot become intake-ready under current evidence. | Define accepted room and wide-risk thresholds before restoring this path to proof review. | YES |
| Context/caution review | `SOURCE_DATA_INSUFFICIENT` | all | QQQ, SPY | `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`; `QQQ-REAL-HISTORICAL-CONTINUATION-001`; `QQQ-REAL-HISTORICAL-IDEAL-001`; `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`; `SPY-REAL-HISTORICAL-CONTINUATION-001`; `SPY-REAL-HISTORICAL-IDEAL-001`; `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`; `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`; `historical_signal_replay/reports/*.jsonl` used by the seven strict rows; `SAFE_FAST_ARCHITECT_CONTROL_AND_PROJECT_TIGHTENING.md` | Rows still carry unconfirmed 24H, macro, IV, event, room, headline, option, or execution context. Primary blocker null is source-backed as insufficient because blocker/caution must be complete and clean before intake-ready. | All seven rows remain blocked; primary blocker null alone and `final_verdict=TRADE` alone cannot promote. | Add complete source-backed context/caution review fields before any of the seven rows can enter proof review. | YES |

## Summary

- `DEFINE_FROM_REPO_EVIDENCE`: 0 families.
- `SOURCE_DATA_INSUFFICIENT`: 4 families.
- `KILL_OR_NARROW_SETUP_SYMBOL_PATH`: 5 families.
- Intake-ready count: 0.
- Applied Clean Fast Break source-data insufficiency result: CFB rows remain blocked unless future source-backed expiry and gap-context rules exist.
- `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`: `blocked`; blocked by gap-context and CFB expiry source insufficiency.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`: `blocked`; blocked by CFB expiry and context/caution rule insufficiency.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`: `blocked`; blocked by CFB expiry and context/caution rule insufficiency.
- Applied context/caution source-data insufficiency result: rows needing complete context/caution review stay blocked unless future source-backed context/caution rules exist; primary blocker null alone cannot promote.
- `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`: `blocked`; still blocked by complete context/caution source-data insufficiency.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`: `blocked`; still blocked by complete context/caution source-data insufficiency.
- `SPY-REAL-HISTORICAL-IDEAL-001`: `blocked`; still blocked by complete context/caution source-data insufficiency.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`: `blocked`; still blocked by complete context/caution source-data insufficiency.
- Applied Continuation narrowing result: next-session/session-boundary-dependent Continuation cannot be intake-ready unless a future source-backed carry-forward rule exists.
- `QQQ-REAL-HISTORICAL-CONTINUATION-001`: `replace`; outside the narrowed Continuation path because next-session/session-boundary carry-forward remains unsupported.
- Applied intrabar ordering narrowing result: intrabar-dependent SPY Continuation cannot be intake-ready unless future lower-timeframe/order-of-events evidence exists.
- `SPY-REAL-HISTORICAL-CONTINUATION-001`: `replace`; outside the narrowed Continuation path because order-of-events inside completed 1H candles remains unsupported.
- Applied Ideal narrowing result: fast-swing / wide-risk Ideal cannot be intake-ready unless future source-backed rules define Ideal freshness expiry and room/risk thresholds.
- `QQQ-REAL-HISTORICAL-IDEAL-001`: `replace`; outside the narrowed Ideal path because fast-swing freshness and wide-risk/room threshold remain unsupported.
- `SPY-REAL-HISTORICAL-IDEAL-001`: `blocked`; same-session Ideal remains eligible only after stale/spent expiry and complete context/caution evidence become clean.
- Current source-pool counts after applying context/caution source-data insufficiency: accepted intake count 7; intake-ready count 0; blocked/drop/replace/duplicate counts 4/0/3/0; close-ready count 4.
- Proof accepted: NO.
- Profitability claim made: NO.

Recommended next action: do not deep-review proof. Source and regression-test complete context/caution review fields plus Clean Fast Break expiry and QQQ gap-context evidence, replace outside-path Continuation and Ideal rows with inside-path evidence or source and regression-test the missing carry-forward, intrabar order-of-events, fast-swing freshness, and room/risk threshold rules.
