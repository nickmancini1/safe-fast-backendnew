# SAFE-FAST Day 41 QQQ gap-context threshold fixtures task

Repo:
- safe-fast-backendnew

Baseline:
- Branch: main
- HEAD: 25a77ac Define QQQ gap context rule shape

First action:
- Read SAFE_FAST_BUILD_STATE.md first.

Goal:
- Find or define the accepted QQQ Clean Fast Break gap-context threshold fixtures needed before calculator work.
- Do not write calculator code yet.
- Do not fill evidence yet.

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_RULE_DEFINITION.md
- SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_THRESHOLD_GAP.md
- SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_CALCULATION_REVIEW.md
- SAFE_FAST_DAY41_TASTYTRADE_RAW_DATA_CAPABILITY_REVIEW.md
- historical_signal_replay/source_data/richer_export_package_work/
- any existing tests/docs mentioning gap, context, clean, caution, fail, thresholds, Clean Fast Break, CFB

Task:
1. Search the repo for existing threshold rules or examples.
2. If accepted thresholds already exist, create:
   - SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_THRESHOLD_FIXTURES.md
   with exact clean/caution/fail/unknown threshold fixtures.
3. If accepted thresholds do not exist, do not invent them. Create:
   - SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_THRESHOLD_DECISION_NEEDED.md
   explaining exactly what decision is missing and what choices must be made.
4. Append a short status note to:
   - SAFE_FAST_BUILD_STATE.md

The fixture/decision doc must include:
- previous close fixture
- signal-day open fixture
- gap amount fixture
- gap percent fixture
- status expected
- as_of expected
- reviewed_before_signal expected
- missing-data case
- future-data rejection case
- exact regression cases needed next

Allowed writes:
- SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_THRESHOLD_FIXTURES_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_THRESHOLD_FIXTURES.md
- SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_THRESHOLD_DECISION_NEEDED.md
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
