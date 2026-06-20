# SAFE-FAST Day 49 Grouped Positive-Entry Exact Setup-Data Approval or Repair Task

## Required startup

Read `SAFE_FAST_BUILD_STATE.md` first.

Then read:

1. `SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_SETUP_EVIDENCE_COMPLETION_OR_REPLACEMENT_RESULT.md`
2. `historical_signal_replay/results/day49_positive_entry_setup_evidence_completion.json`
3. `historical_signal_replay/source_data/richer_export_package_work/day49_positive_entry_exact_setup_data_request_manifest.json`
4. `SAFE_FAST_PROJECT_PROOF_PIPELINE.md`
5. `SAFE_FAST_PROJECT_DASHBOARD.md`
6. `SAFE_FAST_PROJECT_RULE_INDEX.md`

## Objective

Resolve the exact setup-data request blocker without creating another candidate batch.

Do one of these:

- map the request manifest to a safe exact dataset/schema and run a cost check only, with no download; or
- prove the request cannot be safely mapped and route to grouped setup-rule/request-shape repair.

Do not request option data. Do not request exit-path data. Do not download data. Do not touch `main.py`, Railway/deploy files, broker/account/order code, credentials, `.env`, or frozen trading thresholds.

## Required output

Create one result document and update the build state/dashboard/rule index.

The result must report:

- whether a safe exact setup-data dataset/schema mapping exists;
- checked cost or exact reason cost is unavailable;
- whether approval/download is blocked or ready for user approval;
- no proof/profitability/readiness/promotion claim;
- exact next grouped task.
