# SAFE-FAST Day 41 QQQ Gap-Context Calculation Review

## Baseline

- Verified branch baseline: `main`.
- Verified HEAD: `0f3d706 Record Day 41 tastytrade raw data capability review`.
- Working tree before changes had the untracked task file `SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_CALCULATION_CODEX_TASK.md`.
- Git status emitted access-denied warnings for local temp folders `tmpra392qh0` and `tmpt2fw63vq`; this did not block the requested repo checks.

## Files Inspected

- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_DAY41_TASTYTRADE_RAW_DATA_CAPABILITY_REVIEW.md`
- `SAFE_FAST_DAY41_RAW_TASTYTRADE_NEXT_CHAT_HANDOFF.md`
- `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`
- `SAFE_FAST_RULE_FAMILY_DECISION_TABLE.md`
- `SAFE_FAST_CHART_BASED_TRADE_OUTCOME_BACKTESTING_V1_CALCULATION_RULES_PLAN.md`
- `SAFE_FAST_QQQ_CHART_OUTCOME_CALCULATION_PHASE_PLAN.md`
- `historical_signal_replay/source_data/richer_export_package_work/`
- `historical_signal_replay/source_data/richer_export_package_work/qqq_cfb_gap_context_completeness_fields_rule.jsonl`
- `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`
- `historical_signal_replay/reports/first_real_qqq_clean_fast_break_replay_v1_signal_log.jsonl`
- `watcher_foundation/candidate_freshness_blocker_rule_gate.py`
- `tests/test_candidate_freshness_blocker_rule_gate.py`

## Candidate Time

- Candidate: `QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001`
- Symbol: `QQQ`
- Setup type: `Clean Fast Break`
- Signal/setup candle time: `2026-04-13T12:30:00-04:00`
- Replay signal row: `historical_signal_replay/reports/first_real_qqq_clean_fast_break_replay_v1_signal_log.jsonl`, line 3
- Source CSV setup row: `historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv`, line 132

## Raw Candle Inputs

The existing QQQ CSV contains the raw candle inputs requested by the task:

| Input | Source row | Value |
|---|---:|---|
| Previous regular-session final exported close | CSV line 128, `2026-04-10T15:30:00-04:00` | `611.02` |
| Signal-day open | CSV line 129, `2026-04-13T09:30:00-04:00` | `609.455` |
| Through-signal candles | CSV lines 129-132 | available through `2026-04-13T12:30:00-04:00` |
| First post-signal candle | CSV line 133 | excluded from setup-time gap context |
| Source timestamp | CSV lines 128-132 | `2026-05-15T18:48:44Z` |

The raw gap can be measured as `-1.565` points, approximately `-0.2561%`, from signal-day open minus previous exported RTH close. That measurement is not an accepted SAFE-FAST gap-context label.

## Rule Search

The repo has chart-gap measurement language, but no accepted rule for the required labels:

- Chart calculation plans allow measuring chart gaps from candles.
- The rule gate and decision table still mark QQQ Clean Fast Break gap context as `SOURCE_DATA_INSUFFICIENT`.
- The richer work-package row still contains unresolved `TASTYTRADE_DATA_NOT_AVAILABLE` values for `gap_context_status`, `gap_context_as_of`, and `gap_context_reviewed_before_signal`.

No clear rule was found that defines:

- accepted `gap_context_status` values,
- how raw gap size/direction maps to status,
- whether through-signal candles change the status,
- which timestamp becomes `gap_context_as_of`,
- or how to evaluate `gap_context_reviewed_before_signal` when `source_as_of` is after the historical signal.

## Decision

No calculator or tests were created because the task explicitly says not to invent a rule if no clear repo rule exists.

Created `SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_RULE_GAP.md` to document the exact missing rule.

## Status

- QQQ CFB gap-context evidence filled: NO.
- QQQ candidate marked ready: NO.
- Intake-ready count changed: NO.
- Proof accepted: NO.
- Profitability claim made: NO.
- `main.py`, engine/live trading files, Railway/deploy files, broker/order/account files, evidence package files, `.env`, secrets, and generated live reports/logs changed: NO.

## Next

Define a source-backed, no-hindsight QQQ Clean Fast Break gap-context rule with accepted status values, timestamp semantics, and regression cases. Only after that rule exists should a small data-only calculator be created.
