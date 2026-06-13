# SAFE-FAST Day 41 QQQ external option data request package task

Baseline:
- Branch: main
- HEAD: 0707543 Record QQQ gap threshold decision package

First action:
- Read SAFE_FAST_BUILD_STATE.md first.

Goal:
- Build the exact smallest data request package for the missing QQQ historical option evidence.
- Do not buy data.
- Do not call paid APIs.
- Do not use credentials.
- Do not write ingestion code yet.

Read:
- SAFE_FAST_BUILD_STATE.md
- SAFE_FAST_DAY41_TASTYTRADE_RAW_DATA_CAPABILITY_REVIEW.md
- SAFE_FAST_DAY41_QQQ_GAP_THRESHOLD_DECISION_PACKAGE.md
- SAFE_FAST_DAY41_QQQ_GAP_CONTEXT_CALCULATION_REVIEW.md
- historical_signal_replay/source_data/richer_export_package_work/
- any QQQ Clean Fast Break candidate files

Task:
1. Find the exact QQQ candidate details:
   - candidate id
   - signal date
   - signal time
   - underlying symbol
   - any target option expiration/strike/side already present
   - if no strike/expiration exists, say that clearly
2. Create:
   - SAFE_FAST_DAY41_QQQ_EXTERNAL_OPTION_DATA_REQUEST_PACKAGE.md
3. The package must include:
   - exact time window needed
   - minimum fields needed
   - nice-to-have fields
   - Databento-first request plan
   - ThetaData fallback request plan
   - what file formats we can accept from the user: CSV, JSON, ZIP
   - where the user should place downloaded files in the repo
   - how Codex should validate the files after download
   - what still cannot be proven even after the files arrive
4. Create the target drop folder only if it does not exist:
   - historical_signal_replay/source_data/external_option_data_drop/
5. Add a README in that folder:
   - historical_signal_replay/source_data/external_option_data_drop/README.md
   explaining exactly what files to put there.
6. Append a short status note to:
   - SAFE_FAST_BUILD_STATE.md

Allowed writes:
- SAFE_FAST_DAY41_QQQ_EXTERNAL_OPTION_DATA_REQUEST_PACKAGE_CODEX_TASK.md
- SAFE_FAST_DAY41_QQQ_EXTERNAL_OPTION_DATA_REQUEST_PACKAGE.md
- historical_signal_replay/source_data/external_option_data_drop/README.md
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
