# SAFE-FAST Day 50 Data-Source Registry and Schwab Queue Result

## Baseline

- Branch: `main`.
- Starting commit: `4fac2e6`.
- Starting status: clean except untracked `SAFE_FAST_DAY50_DATA_SOURCE_REGISTRY_AND_SCHWAB_QUEUE_CODEX_TASK.md` and known temp-directory permission warnings.
- Scope: SAFE-FAST build infrastructure only.
- No `main.py`, Railway/deploy files, frozen trading behavior, broker order-submission code, credentials, `.env`, raw market data, or production/live backend files were modified.
- No Schwab authentication was attempted.
- No data was downloaded.

## Fixed

- Created canonical registry document: `SAFE_FAST_DATA_SOURCE_REGISTRY.md`.
- Created machine-readable registry: `historical_signal_replay/config/safe_fast_data_source_registry.json`.
- Created read-only resolver: `watcher_foundation/safe_fast_data_source_resolver.py`.
- Created focused registry/resolver/control tests: `tests/test_safe_fast_data_source_registry.py`.
- Created exact next Schwab task: `SAFE_FAST_DAY50_SCHWAB_READ_ONLY_AUTH_AND_CAPABILITY_AUDIT_CODEX_TASK.md`.
- Updated control and future-chat files to point at the canonical registry and forbid vague `MISSING_DATA`.

## Blocked

- Schwab capabilities remain unaudited until the read-only OAuth/capability task runs.
- Schwab must not replace Databento historical backtesting sources unless that audit proves equivalent historical coverage, timestamp behavior, adjustment behavior, reproducibility, and entitlement access.
- The current eight Day 49 candidates remain unqualified; their blockers are now mapped to exact fields and next actions.

## Source Authorities

- Historical underlying data: Databento `DBEQ.BASIC / ohlcv-1h / raw_symbol`.
- Historical options data: Databento `OPRA.PILLAR`.
- Live broker/account/order/fill authority: Charles Schwab.
- Volatility: SAFE-FAST calculated realized volatility and calculated option IV/Greeks when inputs exist; Cboe VIX/VIX9D, VXN, RVX, and GVZ for official index context.
- News/events: SEC EDGAR, Federal Reserve, BLS, BEA, Treasury, issuer IR; Benzinga only when timestamped API entitlement and credentials exist.
- Macro history: ALFRED for historical vintages, with FRED and issuing agencies as supporting sources.
- Setup labels: SAFE-FAST frozen local rule engine only.

## Current Blockers Mapped

- `GLD-REPLACEMENT-IDEAL-CANDIDATE-001`: exact setup fields required; OHLCV did not resolve SAFE-FAST label decisions.
- `GLD-REPLACEMENT-IDEAL-CANDIDATE-002`: no exact second GLD Ideal source window; candidate should be excluded unless a deterministic source window appears.
- `SPY-SOURCE-WINDOW-CLEAN-FAST-BREAK-003`: exact CFB setup-time replay/calculator evidence required.
- `SPY-SOURCE-WINDOW-CONTINUATION-004`: `SOURCE_CONFLICT` around freshness and 2026-04-07 invalidation/recovery.
- `SPY-SOURCE-WINDOW-CONTINUATION-005`: `SOURCE_CONFLICT` around fresh/non-duplicate identity after 2026-04-30.
- `QQQ-SOURCE-WINDOW-CONTINUATION-002`: `SOURCE_CONFLICT` around fresh Continuation versus same rebound context.
- `IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001`: exact setup fields required; OHLCV did not resolve accepted Continuation decisions.
- `IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002`: exact session-boundary setup fields required; OHLCV did not resolve accepted Continuation decisions.

Optional context removed as a silent setup blocker: realized volatility, option IV/Greeks, official volatility indexes, timestamped headlines, macro context, and official event context. These remain optional or review-only unless a frozen rule explicitly makes one mandatory.

## Next

Exact next task: `SAFE_FAST_DAY50_SCHWAB_READ_ONLY_AUTH_AND_CAPABILITY_AUDIT_CODEX_TASK.md`.

Do not run another incomplete candidate batch. Do not buy more data before exact field/source/cost routing.

## Tests

- `.\scripts\safe_fast_run_safe_checks.ps1`: BLOCKED by local PowerShell execution policy before the script ran.
- `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\safe_fast_run_safe_checks.ps1`: PASS, `3` checks.
- `python -B -m unittest discover -s tests -p "test_safe_fast_data_source_registry.py"`: PASS, `10` tests.
- `python -B -m watcher_foundation.safe_fast_data_source_resolver`: PASS, read-only resolver smoke output produced with `vendor_contacted=false` and `secrets_read=false`.
- `python -B -m watcher_foundation.source_evidence_work_package_content_validator`: PASS, `9` passed requests, `0` failed requests, intake-ready `0`.
- `python -B -m watcher_foundation.source_evidence_package_to_intake_bridge`: PASS, `9` passed requests, `4` reconsideration-eligible candidates, intake-ready `0`.
- `python -B -m unittest discover -s tests -p "test_day49_grouped_positive_entry_setup_field_completion.py"`: PASS, `6` tests.
- `python -B -m unittest discover -s tests -p "test_day49_positive_entry_setup_evidence_completion.py"`: PASS, `5` tests.
- `python -B -m unittest discover -s tests -p "test_day48_positive_trade_handoff_consistency.py"`: PASS, `3` tests.
- `python -B -m unittest discover -s tests -p "test_databento_opra_normalizer.py"`: PASS, `9` tests.
- `python -B -m unittest discover -s tests -p "test_execution_context_calculator.py"`: PASS, `10` tests.
- `python -B -m unittest discover -s tests -p "test_context_caution_calculator.py"`: PASS, `12` tests.
- Bounded `__pycache__` inspection over `tests`, `watcher_foundation`, `historical_signal_replay`, and `replay`: `0` directories found.
- `git --no-pager diff --check`: PASS with line-ending warnings only.
