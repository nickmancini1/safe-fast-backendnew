# SAFE-FAST Day 41 QQQ gap threshold decision package task

Baseline:
- Branch: main
- HEAD: ad716ef Record QQQ gap threshold decision needed

First action:
- Read SAFE_FAST_BUILD_STATE.md first.

Goal:
- Build the smallest useful decision package for QQQ gap thresholds.
- Do not guess thresholds.
- Do not write calculator code.
- Do not fill evidence.

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_THRESHOLD_DECISION_NEEDED.md
- SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_RULE_DEFINITION.md
- SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_CALCULATION_REVIEW.md
- SAFE_FAST_DAY41_TASTYTRADE_RAW_DATA_CAPABILITY_REVIEW.md
- historical_signal_replay/source_data/richer_export_package_work/
- any repo docs/tests mentioning Clean Fast Break, CFB, gap, threshold, clean, caution, fail, previous close, signal-day open

Task:
1. Find all repo examples that can help decide QQQ Clean Fast Break gap thresholds.
2. Calculate gap amount and gap percent only where previous close and signal-day open are present.
3. Create:
   - SAFE_FAST_DAY41_QQQ_GAP_THRESHOLD_DECISION_PACKAGE.md
4. Include:
   - examples found
   - usable examples
   - unusable examples
   - calculated gap amounts and percents
   - whether repo evidence supports numeric thresholds
   - if yes, list threshold options
   - if no, state exactly what sample/data is missing
   - exact regression fixtures needed next
5. Append a short status note to:
   - SAFE_FAST_BUILD_STATE.md

Allowed writes:
- SAFE_FAST_DAY41_QQQ_GAP_THRESHOLD_DECISION_PACKAGE_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_GAP_THRESHOLD_DECISION_PACKAGE.md
- SAFE_FAST_BUILD_STATE.md

Do not write:
- calculator code
- tests
- evidence files
- main.py
- live/engine/broker/order/account/Railway files
- .env or secrets

Final response:
Baseline:
Fixed:
Blocked:
Next:
Tests:
Files changed:
