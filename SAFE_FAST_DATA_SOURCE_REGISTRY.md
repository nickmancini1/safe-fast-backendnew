# SAFE-FAST Data Source Registry

<!-- SAFE_FAST_OPRA_670C_RECOVERY_START -->
## CURRENT OPTION-EVIDENCE SOURCE STATE

- Existing local Databento `OPRA.PILLAR / definition` DBN verified.
- Raw DBN is local-only and must not be committed.
- DBN SHA-256: `2dfabeaae6eef16f752ef105daf8d469bf932d1e9ee11b7d560ff824bf24011f`.
- Definition records: `13472`.
- 669C is unlisted.
- Frozen-rule selected raw symbol: `SPY   260330C00670000`.
- Instrument ID: `1241515301`.
- Publisher ID: `30`.
- No second definition request is allowed.
- Current Databento credential variable: `SAFE_FAST_DB_AUTH`.
- Codex must not perform vendor calls.
- Normal local PowerShell handles credentials, cost checks, approvals, and downloads.
- Schwab is not required for this historical backtest.
- Raw vendors provide evidence; SAFE-FAST calculates its own labels and decisions.
<!-- SAFE_FAST_OPRA_670C_RECOVERY_END -->

Status: canonical as of Day 52 option-evidence request.

Machine-readable registry: `historical_signal_replay/config/safe_fast_data_source_registry.json`.

Read-only resolver: `watcher_foundation/safe_fast_data_source_resolver.py`.

This registry replaces ad hoc source wording in prior result files. Older manifests and result files remain historical evidence, but they are not the source-mapping authority.

## Rules

- Do not report vague `MISSING_DATA`. Report the exact field, source, dataset/schema/API/calculator, timestamp window, unavailable reason, blocking scope, and next action.
- SAFE-FAST setup labels come only from the frozen local SAFE-FAST rule engine.
- Databento is the primary historical options source: `OPRA.PILLAR`.
- Charles Schwab is the live broker and execution authority.
- Databento, tastytrade, and TradingView cannot override an actual Schwab fill.
- Do not average conflicting sources. A material disagreement is `SOURCE_CONFLICT`.
- Revised present-day macro values cannot silently replace historical-vintage values.
- TCBBO is supplemental trade-linked evidence and must not be the sole quote-freshness source.
- Optional context and review-only fields cannot block a technical setup label unless a frozen rule explicitly makes that field mandatory.

## Primary Source Map

| Field area | Primary source | Dataset, API, or calculator | Blocking rule |
| --- | --- | --- | --- |
| Historical underlying OHLCV | Databento | `DBEQ.BASIC / ohlcv-1h / raw_symbol` | Can block setup when required source bars are absent. |
| Setup labels | SAFE-FAST frozen local engine | setup/replay/lifecycle calculators | External vendors do not supply labels. |
| Option contract identity | Databento | `OPRA.PILLAR / definition` | Blocks trade eligibility if unresolved. |
| Option quote freshness | Databento | `OPRA.PILLAR / cmbp-1` | Blocks execution/trade eligibility if unresolved. |
| One-second quote fallback | Databento | `OPRA.PILLAR / cbbo-1s` | Review-only until explicitly validated. |
| Trade-linked quote context | Databento | `OPRA.PILLAR / tcbbo` | Supplemental only; not quote freshness by itself. |
| Option trades | Databento | `OPRA.PILLAR / trades` | Blocks when trade volume is required. |
| Volume/open interest/statistics | Databento | `OPRA.PILLAR / statistics` | Blocks when liquidity/OI is required and no accepted exception exists. |
| Live account/order/fill records | Schwab | Schwab Trader API read-only audit helper; live OAuth verification blocked until credentials exist | Schwab controls actual live fills. |
| Realized volatility | SAFE-FAST local calculation | underlying market-data calculator | Optional until frozen rule says otherwise. |
| Option IV/Greeks | SAFE-FAST local calculation | quote, underlying, strike, expiration, rate, dividend inputs | Optional until frozen rule says otherwise. |
| Official volatility indexes | Cboe | VIX/VIX9D, VXN, RVX, GVZ | Optional context unless a frozen rule makes it mandatory. |
| News/events/filings | Official issuer/agency source | SEC, Fed, BLS, BEA, Treasury, issuer IR | Official source controls conflicts. |
| Timestamped headlines | Benzinga when entitled | Benzinga headline API | Optional unless a frozen rule makes it mandatory. |
| Macro history | ALFRED | historical-vintage series values | Revised current values cannot replace vintages. |

## Day 52 Existing-Setup Option Evidence Boundary

`SAFE_FAST_EXISTING_SETUP_OPTION_EVIDENCE_END_TO_END_BACKTEST_RESULT.md` is the current data-source boundary for the selected March 16, 2026 SPY economic winner. The selected winner is `DAY52-SPY-2026-03-16-CLEAN-FAST-BREAK-20260316T133000Z-P39`; Ideal and Continuation are suppressed duplicates and must not create separate economic trades.

Local evidence was checked first. No local March 16 SPY OPRA definition, quote, trade, or statistics evidence exists for the deterministic candidate contract shape. Tastytrade was checked second through the existing local helper path; that path proves underlying OHLCV export capability only and does not prove historical option bid/ask evidence. Databento is the fallback and is classified as `NETWORK_EXECUTION_BLOCKED` inside the Codex sandbox, not as market data `NOT_AVAILABLE`.

The deterministic candidate contract shape, pending OPRA definition confirmation, is `SPY   260330C00669000`, expiration `2026-03-30`, strike `669`, call. The accepted entry window is `2026-03-16T13:31:00Z` through `2026-03-16T13:36:00Z`; the accepted exit boundary is `2026-03-16T19:45:00Z`. The exact Databento request is `OPRA.PILLAR` `definition` for parent `SPY`, `cmbp-1` for primary quote freshness over the complete entry window, `tcbbo` for trade-linked quote context and bid path through the exit boundary, `trades` for trade volume/context, and `statistics` for open-interest/statistics evidence. The operator cost script is `scripts/safe_fast_day52_existing_setup_databento_cost_request.py`; expected output is `historical_signal_replay/results/day52_existing_setup_databento_cost_request_operator_output.json`.

Current stage is `EXACT_EVIDENCE_REQUEST`: no selected contract is confirmed, no eligible entry or recorded entry exists, no exit or net P&L is calculated, and profitability proof plus paper/live eligibility remain `NO`.

## Day 51 SPY Numeric Setup And OPRA Cost Boundary

`SAFE_FAST_DAY51_SPY_NUMERIC_SETUP_AND_OPRA_COST_CHECK_RESULT.md` is the current data-source boundary for the three setup-qualified SPY March 16, 2026 candidates. Frozen setup-time `DBEQ.BASIC / ohlcv-1m / raw_symbol` evidence establishes the setup timestamp, setup-minute OHLCV envelope, volume-weighted close, freshness deadline, no-hindsight boundary, and same-session behavior. It does not establish numeric trigger or invalidation thresholds because the accepted SAFE-FAST mapper does not bind the trigger/invalidation contracts to a numeric OHLCV field.

The exact OPRA specification is Databento `OPRA.PILLAR / definition`, `OPRA.PILLAR / tcbbo`, `OPRA.PILLAR / trades`, and `OPRA.PILLAR / statistics`, constrained to SPY parent definitions at setup time, nearest DTE >= 14 expiration `2026-03-30`, entry evidence from `2026-03-16T13:30:00Z` through `2026-03-16T13:35:00Z`, and conditional selected-contract exit evidence through `2026-03-16T19:45:00Z`. The local Databento metadata API path was attempted for `OPRA.PILLAR / definition` / `SPY` / `2026-03-16T13:30:00Z` to `2026-03-16T13:31:00Z`, but grouped cost is `NOT_AVAILABLE USD` because the HTTPS proxy connection to `127.0.0.1:9` was refused and no `SAFE_FAST_DB_AUTH` credential was configured. No paid download is authorized.

## Day 50 Raw One-Minute Underlying Setup-Replay Mapping Boundary

`SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_OPTION_CONTRACT_EVIDENCE_REQUEST_REVIEW_RESULT.md` is the current option-evidence boundary for the three setup-qualified SPY March 16, 2026 candidates. It inspected existing local option files/manifests under `historical_signal_replay/source_data/external_option_data_drop` and found no March 16 SPY OPRA `definition`, `tcbbo`, `trades`, or `statistics` evidence. The frozen setup trigger and invalidation fields remain accepted contract labels, not numeric option-selection values. Therefore no local selected contract, eligible entry, recorded entry, costed backtest, or net P&L is established.

The exact grouped request now requires Databento `OPRA.PILLAR / definition`, `OPRA.PILLAR / tcbbo`, `OPRA.PILLAR / trades`, `OPRA.PILLAR / statistics`, selected-contract quote path through `15:45 ET`, and numeric trigger/invalidation repair before full net-P&L can be calculated. Exact local cost is `NOT_AVAILABLE` because no external Databento cost API call or paid download was authorized or run.

`SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_REVIEW_ONLY_PACKAGE_TO_CANDIDATE_CONTRACT_RESULT.md` confirms the next boundary after accepted mapping: the three SPY setup-time field packages satisfy the bounded contract for generated-candidate and setup-qualified status, but do not satisfy the trade-candidate contract. The bounded contract processed Ideal, Clean Fast Break, and Continuation separately and stopped each before `trade_candidate` with blocker `selected_contract_option_evidence_missing`.

Option contract evidence is now the smallest named blocker for these three setup-qualified SPY candidates. The grouped request is for selected-contract identity, selected-contract quote freshness, selected-contract liquidity, and entry execution context. Required sources are Databento `OPRA.PILLAR / definition`, an accepted OPRA quote-freshness source such as `cmbp-1`, `OPRA.PILLAR / trades`, and `OPRA.PILLAR / statistics`. The requested setup-time window is `2026-03-16T09:30:00-04:00` through `2026-03-16T09:35:00-04:00`. The contract result does not authorize a cost check or paid-data download by itself.

`SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_MAPPER_TO_GENERATION_RETRY_RESULT.md` remains the historical retry boundary showing that, before the contract existed, the same three packages stopped before `generated_candidate` with blocker `accepted_mapper_package_review_only_not_generation_input`.

`SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_ACCEPTED_SETUP_REPLAY_PATH_DECISION_RESULT.md` decides that a bounded accepted setup-replay mapping path should be created before retrying the Day 50 SPY raw-data positive-entry opportunities, but replay/regression cases and accepted field boundaries must be defined first.

`SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_ACCEPTED_SETUP_REPLAY_REGRESSION_CASES_RESULT.md` now defines the accepted field boundaries and required replay/regression cases before implementation. The only current source evidence is the acquired SPY `DBEQ.BASIC / ohlcv-1m / raw_symbol` file for `2026-03-16`. The bounded path may cover only Ideal, Clean Fast Break, and Continuation setup families for that SPY session, and only the fields `setup_time_row`, `trigger`, `invalidation`, `freshness_final_signal_state`, `blocker_caution_review`, `session_boundary_behavior`, and `no_hindsight_boundary`.

The registry rule remains unchanged: raw vendor OHLCV bars do not supply SAFE-FAST labels. Any implementation must satisfy accepted replay/regression cases for positive per-family mapping, missing-field rejection, same-session and prior-session boundary behavior, no-hindsight rejection, wrong-symbol/wrong-window rejection, duplicate handling, raw-vendor-label rejection, determinism, and control preservation.

## Current Eight Candidate Blockers

The Day 49 OHLCV download did not resolve the eight-candidate blocker package. OHLCV gives raw hourly bars only. It does not accept a SAFE-FAST setup-time row, trigger, invalidation, freshness/final-signal state, blocker/caution decision, no-hindsight boundary, or session-boundary behavior.

| Candidate | Exact blocker fields | Proper source | Current action |
| --- | --- | --- | --- |
| `GLD-REPLACEMENT-IDEAL-CANDIDATE-001` | setup row, trigger, invalidation, freshness, blocker/caution, no-hindsight, session boundary | SAFE-FAST local replay/review over exact rows; official/news/macro only for blocker/caution | `EXACT_EXTERNAL_SETUP_DATA_REQUIRED` |
| `GLD-REPLACEMENT-IDEAL-CANDIDATE-002` | all setup fields | no exact source window exists | `SOURCE_UNAVAILABLE_CANDIDATE_EXCLUDED` |
| `SPY-SOURCE-WINDOW-CLEAN-FAST-BREAK-003` | all setup fields | SAFE-FAST CFB replay/calculator | `EXACT_EXTERNAL_SETUP_DATA_REQUIRED` |
| `SPY-SOURCE-WINDOW-CONTINUATION-004` | freshness, invalidation/recovery, and setup fields | SAFE-FAST Continuation lifecycle/session-boundary rule | `SOURCE_CONFLICT` |
| `SPY-SOURCE-WINDOW-CONTINUATION-005` | freshness/non-duplicate and setup fields | SAFE-FAST Continuation duplicate/freshness rule | `SOURCE_CONFLICT` |
| `QQQ-SOURCE-WINDOW-CONTINUATION-002` | freshness/same-rebound context and setup fields | SAFE-FAST Continuation same-context rule | `SOURCE_CONFLICT` |
| `IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001` | setup row, trigger, invalidation, freshness, blocker/caution, no-hindsight, session boundary | SAFE-FAST local replay/review over exact rows | `EXACT_EXTERNAL_SETUP_DATA_REQUIRED` |
| `IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002` | session-boundary setup row and all setup fields | SAFE-FAST local replay/review over exact rows | `EXACT_EXTERNAL_SETUP_DATA_REQUIRED` |

Optional context removed as a silent blocker: realized volatility, option IV/Greeks, official volatility index context, timestamped headlines, macro context, and official event context. These can block trade eligibility only if an existing frozen rule explicitly makes that specific context mandatory.

## Resolver Contract

`watcher_foundation.safe_fast_data_source_resolver.resolve_field_source(field_identifier, decision_timestamp)` returns:

- exact field identifier;
- exact source plan;
- exact dataset/schema/API/calculator;
- exact consumer and requirement class;
- timestamp window;
- whether the field may block setup, trade, execution, exit, or only optional context;
- fallback and source-conflict behavior;
- exact unavailable-data next action.

The resolver never contacts a vendor, never downloads data, and never reads or stores secrets.

## Schwab Read-Only Audit Status

`watcher_foundation.schwab_read_only_audit` defines the isolated read-only OAuth/token and capability audit path. It uses Schwab official `api.schwabapi.com` endpoints only, blocks token storage inside the repo, redacts tokens from outputs, and allow-lists only GET requests for accounts, positions, balances/account detail, transactions, existing orders, quotes, option chains, and price history.

Live verification is still blocked because `SCHWAB_CLIENT_ID` or `SCHWAB_APP_KEY`, `SCHWAB_CLIENT_SECRET` or `SCHWAB_APP_SECRET`, and `SCHWAB_REDIRECT_URI` are not configured in this environment. No Schwab OAuth browser authorization was requested, no token was written, no authenticated Schwab endpoint was called, and no order preview/submission/replacement/cancellation endpoint is allowed.
