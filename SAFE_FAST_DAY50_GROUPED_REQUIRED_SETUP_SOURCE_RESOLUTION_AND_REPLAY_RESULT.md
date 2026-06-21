# SAFE-FAST Day 50 Grouped Required Setup-Source Resolution and Replay Result

## Baseline

- Branch: `main`.
- Starting commit: `a262237`.
- Starting status: clean except untracked `SAFE_FAST_DAY50_GROUPED_REQUIRED_SETUP_SOURCE_RESOLUTION_AND_REPLAY_CODEX_TASK.md` and known temp-directory permission warnings.
- Startup controls read first: `SAFE_FAST_BUILD_STATE.md`, canonical source registry, Day 50 registry and Schwab audit results, Day 49 setup-evidence and OHLCV results, Day 48 funnel result, dashboard, rule index, existing replay runners/calculators/fixtures/validators/tests, and ignored local source-data folders.
- No `main.py`, Railway/deploy files, broker/account/order code, credentials, `.env`, frozen trading thresholds, production/live backend, Schwab authentication, paid data download, or raw vendor download was changed.
- `SAFE_FAST_DB_AUTH` was not printed, saved, documented, or used because no remaining paid Databento request can supply SAFE-FAST setup labels.

## Fixed

- Added grouped Day 50 source resolver/replay builder: `historical_signal_replay/day50_required_setup_source_resolution.py`.
- Added machine-readable result: `historical_signal_replay/results/day50_required_setup_source_resolution.json`.
- Added focused tests: `tests/test_day50_required_setup_source_resolution.py`.
- Resolved the four external-data cases by source routing: existing local `DBEQ.BASIC / ohlcv-1h / raw_symbol` bars are raw input only; one-hour bars are not the remaining blocker. The remaining blocker is accepted SAFE-FAST setup-source evidence: setup-time row, trigger, invalidation, freshness/final-signal, blocker/caution, no-hindsight boundary, and session-boundary behavior.
- Resolved the three source conflicts by registry priority and closed them as `SOURCE_CONFLICT_EXCLUDED`.
- Preserved `GLD-REPLACEMENT-IDEAL-CANDIDATE-002` as `CANDIDATE_UNUSABLE` because no second exact GLD Ideal source window and row range is repo-backed.
- Reran all eight current slots twice through the funnel path. Both runs matched deterministically.

## Candidate Results

| Candidate | Final classification | Highest stage | First stage not reached | Exact blocker |
| --- | --- | --- | --- | --- |
| `GLD-REPLACEMENT-IDEAL-CANDIDATE-001` | `EXACT_EXTERNAL_DATA_REQUIRED` | `SETUP_DEVELOPING` | `SETUP_QUALIFIED` | accepted setup-time row/replay fixture absent |
| `SPY-SOURCE-WINDOW-CLEAN-FAST-BREAK-003` | `EXACT_EXTERNAL_DATA_REQUIRED` | `SETUP_DEVELOPING` | `SETUP_QUALIFIED` | accepted CFB setup-time replay fields absent |
| `IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001` | `EXACT_EXTERNAL_DATA_REQUIRED` | `SETUP_DEVELOPING` | `SETUP_QUALIFIED` | accepted Continuation setup-source fields absent |
| `IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002` | `EXACT_EXTERNAL_DATA_REQUIRED` | `SETUP_DEVELOPING` | `SETUP_QUALIFIED` | accepted session-boundary setup-source fields absent |
| `QQQ-SOURCE-WINDOW-CONTINUATION-002` | `SOURCE_CONFLICT_EXCLUDED` | `SETUP_DEVELOPING` | `SETUP_QUALIFIED` | fresh Continuation versus same rebound context unresolved by accepted chronological rule |
| `SPY-SOURCE-WINDOW-CONTINUATION-004` | `SOURCE_CONFLICT_EXCLUDED` | `SETUP_DEVELOPING` | `SETUP_QUALIFIED` | 2026-04-07 invalidation/recovery interpretation is not setup-time proof |
| `SPY-SOURCE-WINDOW-CONTINUATION-005` | `SOURCE_CONFLICT_EXCLUDED` | `SETUP_DEVELOPING` | `SETUP_QUALIFIED` | fresh/non-duplicate identity versus 2026-04-30 same-lifecycle follow-through unresolved |
| `GLD-REPLACEMENT-IDEAL-CANDIDATE-002` | `CANDIDATE_UNUSABLE` | `SETUP_DEVELOPING` | `SETUP_QUALIFIED` | no exact source window exists |

## Exact External Requests Remaining

Scope: exact setup-source evidence only. No option data, no exit-path data, no outcome-window data.

| Candidate | Source window | Required fields |
| --- | --- | --- |
| `GLD-REPLACEMENT-IDEAL-CANDIDATE-001` | GLD rows `204-238`, `2026-05-01T15:30:00-04:00` to `2026-05-08T14:30:00-04:00` | setup-time row, trigger, invalidation, freshness/final-signal, blocker/caution, no-hindsight, session-boundary |
| `SPY-SOURCE-WINDOW-CLEAN-FAST-BREAK-003` | SPY rows `79-99`, `2026-03-31T09:30:00-04:00` to `2026-04-02T15:30:00-04:00` | same required setup-source fields |
| `IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001` | IWM rows `141-210`, `2026-04-17T15:30:00-04:00` to `2026-05-01T14:30:00-04:00` | same required setup-source fields |
| `IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002` | IWM rows `190-210`, `2026-04-28T15:30:00-04:00` to `2026-05-01T14:30:00-04:00` | same required setup-source fields |

Checked cost: `NOT_AVAILABLE`. Reason: no paid vendor dataset/schema can supply SAFE-FAST setup labels, trigger, invalidation, freshness, or no-hindsight decisions; existing OHLCV is already local and no download was requested.

## Totals

- External-data cases resolved by source routing: `4`.
- External-data cases completed locally: `0`.
- External-data cases still requiring exact setup-source requests: `4`.
- Source conflicts resolved: `3`.
- Source conflicts excluded: `3`.
- Unusable candidates: `1`.
- Setup-qualified candidates: `0`.
- Trade candidates: `0`.
- Contracts selected: `0`.
- Entries recorded: `0`.
- True no-trades: `0`.
- Valid trades captured: `0`.
- Missed valid trades: `0`.
- Invalid trades allowed: `0`.
- Unresolved cases: `0`.
- First blockers by field: `setup_time_row=8`.
- First blockers by funnel stage: `SETUP_QUALIFIED=8`.

## Plain-English Answers

1. Which candidates moved forward? None reached setup-qualified or trade-candidate status.
2. Which candidates were excluded and why? The three Continuation source-conflict rows were excluded because accepted chronological replay rules do not resolve their freshness/session-boundary conflicts; `GLD-REPLACEMENT-IDEAL-CANDIDATE-002` remains unusable because no exact source window exists.
3. Which exact required fields still need outside data? The four remaining candidates need accepted setup-time row, trigger, invalidation, freshness/final-signal, blocker/caution, no-hindsight boundary, and session-boundary behavior.
4. How much would that data cost? `NOT_AVAILABLE`; this is not a Databento paid-data request shape.
5. How many candidates reached real trade testing? `0`.

## Next

Exact next grouped task: `SAFE_FAST_DAY50_EXACT_SETUP_SOURCE_EVIDENCE_COMPLETION_CODEX_TASK.md`.

Reason: no slot reached `TRADE_CANDIDATE`; option-contract and quote-freshness testing is not allowed until exact setup-source evidence moves at least one current candidate forward.

## Tests

- `python -B -m unittest discover -s tests -p "test_day50_required_setup_source_resolution.py"`: PASS, `5` tests.
- `python -B -m historical_signal_replay.day50_required_setup_source_resolution`: PASS, wrote `4` exact setup-source requests, `3` source conflicts excluded, `0` trade candidates.
