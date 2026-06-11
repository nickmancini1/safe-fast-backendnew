# SAFE-FAST Active-Path Evidence Requirements

## Scope

This build-only table defines the exact missing evidence and final parked action for the four rows that were previously `active_blocked` in `SAFE_FAST_RULE_DECISION_SURVIVAL_MAP.md`.

This is not proof review. It does not accept proof, claim profitability, authorize live data, authorize alerts, authorize broker/order/account work, authorize Railway/deploy work, or authorize changes to `main.py`.

Proof accepted: NO.

Profitability claim made: NO.

Current intake-ready count: 0.

## Summary

- Active rows covered: 4.
- Requirement rows: 9.
- Current repo has enough data for any active row: NO.
- Proof allowed rows: 0.
- Applied action if missing: `parked/source_data_insufficient`.
- Final active_blocked count: 0.
- Final parked/source_data_insufficient count: 4.

## Requirement Table

| Candidate ID | Symbol | Setup type | Exact missing rule/evidence | Required source field or log evidence | Exact local source file or doc that should contain it | Current repo has enough data | Action if missing | Smallest next action | Proof allowed |
|---|---|---|---|---|---|---|---|---|---|
| `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | QQQ | Clean Fast Break | source-backed QQQ gap-context completeness field/rule | setup-time `gap_context` completeness field, or replay-log evidence proving gap context was reviewed before the signal | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`; `historical_signal_replay/reports/first_real_qqq_clean_fast_break_replay_v1_signal_log.jsonl` | NO | `parked/source_data_insufficient` | Add source-backed QQQ gap-context completeness evidence before any QQQ Clean Fast Break proof review. | NO |
| `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | QQQ | Clean Fast Break | tested Clean Fast Break stale/spent expiry rule | accepted setup-time expiry rule plus regression rows distinguishing fresh, stale, and spent Clean Fast Break signals | `SAFE_FAST_RULE_FAMILY_DECISION_TABLE.md`; `historical_signal_replay/reports/first_real_qqq_clean_fast_break_replay_v1_signal_log.jsonl`; `tests/test_candidate_freshness_blocker_rule_gate.py` | NO | `parked/source_data_insufficient` | Define and regression-test Clean Fast Break stale/spent expiry before promotion. | NO |
| `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001` | QQQ | Clean Fast Break | complete source-backed context/caution review fields | complete 24H, macro, IV, event, room, option, headline, execution, and caution review fields at setup time | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`; `SAFE_FAST_ARCHITECT_CONTROL_AND_PROJECT_TIGHTENING.md` | NO | `parked/source_data_insufficient` | Add complete source-backed context/caution fields; primary blocker null is not enough. | NO |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | SPY | Clean Fast Break | tested Clean Fast Break higher-base/fresh-break expiry rule | accepted setup-time expiry rule covering higher-base/fresh-break signals, with line 5 fresh signal and line 6 later spent lifecycle treated as regression evidence | `historical_signal_replay/reports/third_real_spy_clean_fast_break_replay_v1_signal_log.jsonl`; `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv`; `tests/test_candidate_freshness_blocker_rule_gate.py` | NO | `parked/source_data_insufficient` | Define and regression-test higher-base/fresh-break expiry before promotion. | NO |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003` | SPY | Clean Fast Break | complete source-backed context/caution review fields | complete 24H, macro, IV, event, room, option, headline, execution, and caution review fields for the 2026-04-15 14:30 setup-time row | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` line 154; `historical_signal_replay/reports/third_real_spy_clean_fast_break_replay_v1_signal_log.jsonl` line 5 | NO | `parked/source_data_insufficient` | Repair source/context fields for the 2026-04-15 14:30 setup-time row. | NO |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | SPY | Clean Fast Break | tested Clean Fast Break initial-break expiry rule | accepted setup-time expiry rule covering initial-break signals, with line 2 signal-stage and line 3 follow-through/spent lifecycle treated as regression evidence | `historical_signal_replay/reports/third_real_spy_clean_fast_break_replay_v1_signal_log.jsonl`; `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` line 138; `tests/test_candidate_freshness_blocker_rule_gate.py` | NO | `parked/source_data_insufficient` | Define and regression-test Clean Fast Break initial-break expiry before promotion. | NO |
| `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002` | SPY | Clean Fast Break | complete source-backed context/caution review fields | complete 24H, macro, IV, event, room, option, headline, execution, and caution review fields for the 2026-04-13 12:30 setup-time row | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` line 138; `historical_signal_replay/reports/third_real_spy_clean_fast_break_replay_v1_signal_log.jsonl` line 2 | NO | `parked/source_data_insufficient` | Repair source/context fields for the 2026-04-13 12:30 setup-time row. | NO |
| `SPY-REAL-HISTORICAL-IDEAL-001` | SPY | Ideal | tested SPY Ideal stale/spent expiry rule | accepted setup-time stale/spent expiry rule covering same-session SPY Ideal, with line 5 triggered signal and line 6 later spent lifecycle as regression evidence | `historical_signal_replay/reports/second_real_spy_ideal_replay_v1_signal_log.jsonl`; `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` line 291; `tests/test_candidate_freshness_blocker_rule_gate.py` | NO | `parked/source_data_insufficient` | Define and regression-test SPY Ideal stale/spent expiry before promotion. | NO |
| `SPY-REAL-HISTORICAL-IDEAL-001` | SPY | Ideal | complete source-backed context/caution review fields | complete gap, headline, room, 24H, macro, IV, event, option, execution, and caution review fields for the 2026-05-13 11:30 setup-time row | `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv` line 291; `historical_signal_replay/reports/second_real_spy_ideal_replay_v1_signal_log.jsonl` line 5 | NO | `parked/source_data_insufficient` | Repair source/context fields for the 2026-05-13 11:30 Ideal setup-time row. | NO |

## Row Results

- `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`: final action `parked/source_data_insufficient`; current repo has enough data: NO; proof allowed: NO.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003`: final action `parked/source_data_insufficient`; current repo has enough data: NO; proof allowed: NO.
- `SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002`: final action `parked/source_data_insufficient`; current repo has enough data: NO; proof allowed: NO.
- `SPY-REAL-HISTORICAL-IDEAL-001`: final action `parked/source_data_insufficient`; current repo has enough data: NO; proof allowed: NO.

## Guardrail Result

No formerly active row can enter proof review while its active-path evidence requirements are unmet. All four formerly active rows are parked/source_data_insufficient.

Proof accepted: NO.

Profitability claim made: NO.
