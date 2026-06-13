# SAFE-FAST Day 41 Databento QQQ OPRA normalizer task

Baseline:
- Latest commit before this task: 7304497 Map QQQ Databento fields to evidence requirements

First action:
- Read SAFE_FAST_BUILD_STATE.md first.

Goal:
- Build a local Databento OPRA normalizer for the already-downloaded QQQ files.
- Add tests.
- Do not download more data.
- Do not fill evidence.
- Do not choose a trade.
- Do not calculate P&L.
- Do not mark QQQ ready.

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_DAY41_DATABENTO_QQQ_DOWNLOAD_VALIDATION.md
- SAFE_FAST_DAY41_DATABENTO_QQQ_EVIDENCE_FIELD_MAPPING.md
- SAFE_FAST_PROJECT_PROOF_PIPELINE.md
- SAFE_FAST_TRADE_PLAN_COMPLETENESS_GATE.md
- SAFE_FAST_PROJECT_RULE_INDEX.md
- historical_signal_replay/source_data/external_option_data_drop/README.md
- local QQQ_OPRA CSV files only if present

Task:
1. Create a read-only normalizer module:
   - historical_signal_replay/databento_opra_normalizer.py
2. Create tests:
   - tests/test_databento_opra_normalizer.py
3. The normalizer must support:
   - loading definitions, quotes, trades, and statistics CSVs
   - parsing Databento option symbols / instrument ids
   - joining quote/trade/stat rows to definitions
   - timestamp normalization
   - no-hindsight quote selection at or before signal time
   - bid/ask/spread calculation from quote rows
   - expiration, strike, side, volume, and open-interest/stat mapping when present
   - clear missing-field errors
   - refusal to infer fills, trade choice, P&L, proof, or readiness
4. Tests must cover:
   - symbol/instrument parsing
   - definition joins
   - quote timestamp selection that rejects post-signal rows
   - spread calculation
   - statistics interpretation
   - missing columns fail clearly
   - no fill/P&L/readiness inference
5. Create:
   - SAFE_FAST_DAY41_DATABENTO_QQQ_OPRA_NORMALIZER_REVIEW.md
6. Update:
   - SAFE_FAST_PROJECT_RULE_INDEX.md
   - SAFE_FAST_BUILD_STATE.md

Allowed writes:
- SAFE_FAST_DAY41_DATABENTO_QQQ_OPRA_NORMALIZER_CODEX_TASK.md
- SAFE_FAST_DAY41_DATABENTO_QQQ_OPRA_NORMALIZER_REVIEW.md
- historical_signal_replay/databento_opra_normalizer.py
- tests/test_databento_opra_normalizer.py
- SAFE_FAST_PROJECT_RULE_INDEX.md
- SAFE_FAST_BUILD_STATE.md

Do not write:
- raw data files
- evidence fills
- calculator gap labels
- trade selection
- P&L
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
