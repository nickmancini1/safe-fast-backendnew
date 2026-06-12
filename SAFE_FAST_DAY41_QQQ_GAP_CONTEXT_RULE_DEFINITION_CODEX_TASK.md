# SAFE-FAST Day 41 QQQ gap-context rule definition task

Repo:
- safe-fast-backendnew

Baseline:
- Branch: main
- HEAD: f0a4535 Record QQQ gap context rule gap

First action:
- Read SAFE_FAST_BUILD_STATE.md before touching anything else.

Goal:
- Define the no-hindsight QQQ Clean Fast Break gap-context rule.
- Do not fill evidence yet.
- Do not create trade proof.
- Do not mark QQQ ready.
- Do not touch live/engine/broker/order/account/Railway files.

Use these known raw values from the prior review:
- Candidate: QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001
- Signal time: 2026-04-13T12:30:00-04:00
- Previous close: 611.02
- Signal-day open: 609.455
- Candles available through 12:30 only

Task:
1. Read:
   - SAFE_FAST_BUILD_STATE.md
   - SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_RULE_GAP.md
   - SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_CALCULATION_REVIEW.md
   - SAFE_FAST_DAY41_TASTYTRADE_RAW_DATA_CAPABILITY_REVIEW.md
   - historical_signal_replay/source_data/richer_export_package_work/
2. Search repo for any existing gap-context language or similar rule.
3. Create exactly one rule document:
   - SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_RULE_DEFINITION.md
4. The rule document must define:
   - what gap_context_status can be
   - how previous close is chosen
   - how signal-day open is chosen
   - how the gap percent/direction is calculated
   - what counts as gap context clean / caution / fail / unknown
   - how gap_context_as_of is assigned
   - how gap_context_reviewed_before_signal is assigned
   - what data is allowed
   - what data is forbidden because it is after signal time
   - what happens when data is missing
   - exact regression cases needed before calculator work
5. If repo evidence is not enough to define thresholds honestly, say that clearly and create:
   - SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_THRESHOLD_GAP.md
6. Append a short status note to SAFE_FAST_BUILD_STATE.md.

Allowed writes:
- SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_RULE_DEFINITION_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_RULE_DEFINITION.md
- SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_THRESHOLD_GAP.md only if needed
- SAFE_FAST_BUILD_STATE.md

Do not write:
- calculator code
- tests
- evidence package files
- main.py
- live/engine files
- broker/order/account files
- Railway/deploy files
- .env or secrets

Final response:
Baseline:
Fixed:
Blocked:
Next:
Tests:
Files changed:
