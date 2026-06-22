# SAFE-FAST Day 50 Raw-Data Positive-Entry Mapper-to-Generation Retry Result

## Scope

- Task executed: `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_MAPPER_TO_GENERATION_RETRY_CODEX_TASK.md`.
- Machine-readable result: `historical_signal_replay/results/day50_raw_data_positive_entry_mapper_to_generation_retry.json`.
- Bridge: `historical_signal_replay/day50_raw_data_positive_entry_mapper_to_generation_retry.py`.
- Covered setup families: Ideal, Clean Fast Break, and Continuation for SPY on `2026-03-16` only.
- Frozen source evidence: `DBEQ.BASIC / ohlcv-1m / raw_symbol`.

## Retry Outcome

- Ideal: mapped package reached; stopped before `generated_candidate` on `accepted_mapper_package_review_only_not_generation_input`.
- Clean Fast Break: mapped package reached; stopped before `generated_candidate` on `accepted_mapper_package_review_only_not_generation_input`.
- Continuation: mapped package reached; stopped before `generated_candidate` on `accepted_mapper_package_review_only_not_generation_input`.

No setup reached trade-candidate or selected-contract status, so no local costed entry/exit replay was available to run and no option or exit-path evidence request was created.

## Funnel Totals

- Before retry: `3` exact setup-time field packages, `0` generated candidates, `0` setup-qualified, `0` trade candidates, `0` selected contracts, `0` eligible entries, `0` recorded entries.
- After retry: `3` exact setup-time field packages, `0` generated candidates, `0` setup-qualified, `0` trade candidates, `0` selected contracts, `0` eligible entries, `0` recorded entries.
- Exact generation-contract-required cases: `3`.

## Controls And Guardrails

- Accepted mapper regression cases passed in input package: `17`.
- Preserved controls: `13` setup-qualified, `9` trade candidates, `5` selected contracts, `1` eligible entry, `1` recorded entry.
- Determinism: `PASS`.
- No raw vendor bars were treated as SAFE-FAST labels.
- No thresholds were loosened; no missing fields, option evidence, or exit evidence were invented.
- No `main.py`, Railway/deploy, production/live, broker/order/account, credential, `.env`, paid-data download, proof, profitability, paper, or live scope was changed.

## Exact Next Substantive Action

Create `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_REVIEW_ONLY_PACKAGE_TO_CANDIDATE_CONTRACT_CODEX_TASK.md` only if the project wants to define and regression-test a bounded contract that can promote a review-only setup-time package into a generated candidate.
