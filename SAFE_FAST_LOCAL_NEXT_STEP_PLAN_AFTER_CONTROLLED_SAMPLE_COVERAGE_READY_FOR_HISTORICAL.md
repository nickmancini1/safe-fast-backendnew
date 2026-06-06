# SAFE-FAST Local Next Step Plan After Controlled Sample Coverage Ready For Historical

## 1. Plan Status

- **Status:** docs-only planning complete; ready for assistant review before commit.
- **Baseline:** patch8.
- **Day context:** Day 35.
- **Latest local commit before this task:** `bfad6d3 Update controlled sample coverage review`.
- **Work mode:** build work only, not live trade chat.
- **Highest priority:** viability proof before optimization.
- **Purpose:** define the first small real historical example batch after controlled sample coverage became complete enough to plan real historical examples.

## 2. Boundary Statement

This plan is for real historical examples only.

It is not live data, not controlled shadow data, not trading, not profitability proof, not a watcher loop, not alerts, not generated reports/logs, not broker/order/account/options/P&L, not account sizing, not production/Railway/live backend work, and not live trade decisions.

No `main.py`, engine logic, tests, Railway/deploy files, secrets, environment files, GitHub writes, commits, live data, controlled shadow data, watcher loops, alerts, generated reports/logs, broker/account/order behavior, option P&L, account sizing, optimization, rule changes, or production/live backend paths are allowed in this docs-only planning task.

## 3. What Counts As A Real Historical Example

A real historical example is one caller-provided in-memory setup example derived from a real past market chart/source record, for one symbol, one setup type, and one specific setup timestamp/window.

Each example must include:

- a stable `proof_record_id`, `source_record_id`, and `setup_id`;
- one of the starting symbols: `SPY`, `QQQ`, `IWM`, or `GLD`;
- one setup type: `Ideal`, `Clean Fast Break`, or `Continuation`;
- setup-time evidence references that existed at or before the setup appeared;
- after-setup evidence references from candles/rows after the setup appeared;
- an explicit no-hindsight boundary showing future evidence did not define the original setup;
- an outcome evidence state and outcome result state from the chart/setup proof layer only;
- missing evidence entries when source-backed after-setup evidence is unavailable;
- diagnostics, next fix path, and regression need when the outcome is failed, inconclusive, unavailable, stale, invalidated, or missing evidence.

A real historical example must not be synthetic controlled fixture data. It may be manually selected and manually encoded for the first batch, but its evidence references must point to real past market source rows/windows, not invented controlled sample rows.

## 4. First Small Batch Size

The first batch should contain exactly **4 real historical examples**.

Reason:

- small enough to inspect line by line;
- wide enough to include all four starting symbols once;
- narrow enough to avoid pretending that all 12 setup-type-plus-symbol pairs are covered;
- sufficient to prove whether the existing proof chain can carry real historical examples before broader expansion.

No combined score, aggregate viability score, profitability score, or optimization decision should be produced from this first batch.

## 5. Symbols Included First

The first batch must include exactly one example for each starting symbol:

- `SPY`
- `QQQ`
- `IWM`
- `GLD`

Each symbol must stay separately reviewable. Do not combine symbol results into a single conclusion.

## 6. Setup Types Included First

The first batch must include all three setup types at least once:

- `Ideal`
- `Clean Fast Break`
- `Continuation`

Required first-batch pair layout:

- `Ideal` / `SPY`
- `Clean Fast Break` / `QQQ`
- `Continuation` / `IWM`
- `Ideal` / `GLD`

Why this layout:

- keeps `SPY`, `QQQ`, `IWM`, and `GLD` represented in the first real historical batch;
- keeps all three setup types represented;
- deliberately starts filling controlled-pair gaps without trying to cover all gaps at once;
- gives GLD a first real historical `Ideal` example instead of only continuation coverage;
- gives IWM a real historical `Continuation` example instead of only ideal coverage.

## 7. Setup-Time Versus After-Setup Evidence Separation

Each future implementation record must keep setup-time evidence separate from after-setup evidence.

Setup-time evidence may include only:

- source row/window identifiers available at detection time;
- candle state at or before the setup timestamp;
- trigger/freshness/blocker/session fields known at setup time;
- evidence refs that do not depend on future outcome movement.

After-setup evidence may include only:

- later candle/row references;
- post-setup movement behavior;
- hold/fail/stale/invalidated/missing-evidence observations;
- outcome evidence used to classify what happened after the setup appeared.

The future implementation must not copy after-setup evidence into the setup-appeared object, and must not copy frozen setup identity into the what-happened-after object in a way that blurs the no-hindsight boundary.

## 8. No-Hindsight Review Protection

The first real historical batch is invalid if future candles are used to define the original setup.

The future implementation must preserve:

- `frozen_setup_identity` before outcome scan;
- `future_evidence_used_to_define_setup=False`;
- no backfilled trigger labels, setup labels, invalidation levels, freshness states, or blocker states from later candles;
- explicit missing-evidence fields instead of invented source rows;
- separate review of setup appeared, what happened after, diagnostics, missing evidence, fix path, and regression need.

If the source evidence cannot prove what was known at setup time, the example must be labeled missing evidence or unavailable evidence. It must not be promoted to worked or failed proof.

## 9. Future Implementation Files Allowed

If later explicitly approved, future implementation should be limited to:

- `watcher_foundation/setup_outcome_historical_sample_path.py`
- `tests/test_setup_outcome_historical_sample_path.py`
- `SAFE_FAST_BUILD_STATE.md`
- `SAFE_FAST_DAY33_PROJECT_HANDOFF_AND_TIER_RUNWAY.md`

No other files should be changed unless a later task explicitly expands scope.

## 10. Future Tests Required

The future implementation tests must prove the first real historical batch can run through the existing proof chain:

- builder returns exactly 4 real historical examples;
- examples include exactly `SPY`, `QQQ`, `IWM`, and `GLD`;
- examples include `Ideal`, `Clean Fast Break`, and `Continuation`;
- required first-batch pairs are present;
- examples are not controlled sample IDs or controlled source refs;
- setup-time evidence and after-setup evidence remain separated;
- no-hindsight boundary is preserved;
- missing or unavailable real evidence is surfaced without fabrication;
- runner output preserves setup type, symbol, and setup-type-plus-symbol pair separation;
- proof chain still runs through proof, diagnostics, evidence packet, packet readiness, group review, group review readiness, historical proof bundle, and bundle readiness;
- review output keeps worked, failed, inconclusive, missing-evidence, stale, pending, and invalidated states separate when present;
- lower-tier review summary remains compact and no-trade/watch-only;
- no file/network/subprocess/thread/live/broker side effects occur;
- final viability, profitability, historical success, live readiness, production readiness, optimization, and rule-change claims remain false.

## 11. Still Unproven

This first real historical batch plan still does not prove:

- final trading-plan viability;
- profitability;
- actual historical success;
- all 12 setup-type-plus-symbol pairs;
- repeated worked/failed patterns;
- repeated fix paths;
- lower-tier final readiness;
- controlled shadow readiness;
- live data readiness;
- alerts;
- generated reports/logs;
- broker/order/account behavior;
- option P&L;
- account sizing;
- production/Railway/live backend readiness;
- live trade decisions.

The first batch is only the next viability-proof step: prove the existing local proof chain can carry a small set of real past market examples while preserving evidence boundaries and naming exact gaps.

## 12. Next Objective After This Plan

If this plan is accepted and committed, implement the first real historical example batch locally and in memory only, using the existing proof chain and the file limits above.

Do not expand into live data, controlled shadow, watcher loops, alerts, broker behavior, generated reports/logs, optimization, rule changes, production work, or profitability claims.
