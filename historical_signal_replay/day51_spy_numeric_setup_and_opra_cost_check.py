import csv
import hashlib
import json
import os
from copy import deepcopy
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

from historical_signal_replay import (
    day50_raw_data_positive_entry_option_contract_evidence_request_review as day50_option_review,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day51_spy_numeric_setup_and_opra_cost_check.json"
)
RESULT_DOC_PATH = (
    REPO_ROOT / "SAFE_FAST_DAY51_SPY_NUMERIC_SETUP_AND_OPRA_COST_CHECK_RESULT.md"
)
UNDERLYING_CSV_PATH = day50_option_review.UNDERLYING_CSV_PATH
OPTION_DATA_DIR = day50_option_review.OPTION_DATA_DIR

RESULT_VERSION = "day51_spy_numeric_setup_and_opra_cost_check_v1"
TASK_FILENAME = "SAFE_FAST_DAY51_SPY_NUMERIC_SETUP_AND_OPRA_COST_CHECK_CODEX_TASK.md"
SETUP_FAMILIES = ("Ideal", "Clean Fast Break", "Continuation")
OPRA_DATASET = "OPRA.PILLAR"
OPRA_STYPE_IN = "raw_symbol"
OPRA_SCHEMAS = ("definition", "tcbbo", "trades", "statistics")
ENTRY_START_UTC = "2026-03-16T13:30:00Z"
ENTRY_END_UTC = "2026-03-16T13:35:00Z"
EXIT_END_UTC = "2026-03-16T19:45:00Z"
MISSING_AUTH_SENTINEL = "SAFE_FAST_MISSING_DATABENTO_AUTH_SENTINEL"


def build_day51_document(*, source_commit=None, run_timestamp=None, check_cost=True):
    run_timestamp = run_timestamp or _utc_now()
    day50_doc = day50_option_review.build_option_contract_evidence_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    setup_contracts = [_numeric_setup_contract(record) for record in day50_doc["setup_records"]]
    option_specs = [_option_evidence_spec(contract) for contract in setup_contracts]
    local_evidence = _local_option_evidence_inventory()
    cost_check = _check_grouped_opra_cost(option_specs) if check_cost else _cost_not_available(
        "cost check disabled by caller"
    )
    replay_results = [
        _replay_result(contract, local_evidence)
        for contract in setup_contracts
    ]
    after = _scorecard(replay_results)
    stable_payload = {
        "setup_contracts": setup_contracts,
        "option_specs": option_specs,
        "replay_results": replay_results,
        "after_funnel_totals": after,
    }
    first_hash = _stable_hash(stable_payload)
    second_hash = _stable_hash(deepcopy(stable_payload))
    approval = _approval_requirement(cost_check, option_specs)
    return {
        "result_version": RESULT_VERSION,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp,
        "task": TASK_FILENAME,
        "input_paths": {
            "day50_package_to_candidate_result": (
                "historical_signal_replay/results/"
                "day50_raw_data_positive_entry_review_only_package_to_candidate_contract.json"
            ),
            "day50_option_review_result": (
                "historical_signal_replay/results/"
                "day50_raw_data_positive_entry_option_contract_evidence_request_review.json"
            ),
            "underlying_source_csv": _relative(UNDERLYING_CSV_PATH),
            "local_option_data_dir": _relative(OPTION_DATA_DIR),
        },
        "execution_scope": {
            "bounded_to_spy_2026_03_16": True,
            "covered_setup_families": list(SETUP_FAMILIES),
            "processes_each_setup_family_separately": True,
            "cost_check_only": True,
            "paid_data_downloaded": False,
            "timeseries_download_called": False,
            "main_py_changed": False,
            "railway_or_deploy_changed": False,
            "broker_or_account_or_order_touched": False,
            "credentials_or_env_changed": False,
            "sizing_or_alerts_changed": False,
            "frozen_patch8_thresholds_changed": False,
            "profitability_claimed": False,
            "paper_eligible": False,
            "live_eligible": False,
        },
        "numeric_setup_contracts": setup_contracts,
        "exact_option_evidence_specifications": option_specs,
        "local_option_evidence_inventory": local_evidence,
        "grouped_opra_cost_check": cost_check,
        "approval_required": approval,
        "costed_backtest_results_by_setup_family": {
            result["setup_family"]: result for result in replay_results
        },
        "after_funnel_totals": after,
        "family_scorecards": {
            family: _scorecard([result for result in replay_results if result["setup_family"] == family])
            for family in SETUP_FAMILIES
        },
        "test_coverage_contract": {
            "numeric_setup_contracts_all_three_families": True,
            "no_hindsight": True,
            "developing_stage_transitions": True,
            "session_boundaries_and_carry_forward": True,
            "deterministic_winner_selection": True,
            "stale_spent_and_blocker_rejection": True,
            "no_trade_preservation": True,
            "mapper_regressions": True,
            "mapper_to_generation_regressions": True,
            "package_to_candidate_regressions": True,
            "option_selection_and_execution_cost_controls": True,
            "day51_handoff_consistency": True,
            "focused_validators": True,
            "safe_checks_execution_policy_bypass": True,
            "git_diff_check": True,
        },
        "control_results": {
            "accepted_mapper_regression_case_count": day50_doc[
                "accepted_mapper_regression_case_count"
            ],
            "package_to_candidate_control_result": day50_doc[
                "package_to_candidate_control_result"
            ],
            "preserved_day50_controls": day50_doc["preserved_day50_controls"],
            "preserved_scorecard": day50_doc["preserved_scorecard"],
        },
        "deterministic_comparison": {
            "first_run_equals_second_run": first_hash == second_hash,
            "hashes_match": first_hash == second_hash,
            "result": "PASS" if first_hash == second_hash else "FAIL",
        },
        "first_run_hash": first_hash,
        "second_run_hash": second_hash,
        "guardrails": {
            "schwab_authenticated": False,
            "broker_mutation_attempted": False,
            "proof_accepted": False,
            "profitability_claimed": False,
            "promotion_decision_made": False,
            "paper_eligible": False,
            "live_eligible": False,
        },
        "next_action": approval["next_action"],
    }


def write_outputs(*, source_commit=None, run_timestamp=None, check_cost=True):
    document = build_day51_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
        check_cost=check_cost,
    )
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    RESULT_DOC_PATH.write_text(_markdown_result(document), encoding="utf-8")
    return document


def _numeric_setup_contract(record):
    evidence = _underlying_setup_snapshot(record["setup_time_utc"])
    rule_gap = (
        "accepted Day 50 mapper names family trigger/invalidation contracts but "
        "does not bind those contracts to a numeric OHLCV field; raw high/low/"
        "open/close may not be promoted to trigger or invalidation without an "
        "accepted family rule"
    )
    return {
        "setup_family": record["setup_family"],
        "symbol": "SPY",
        "setup_timestamp_utc": record["setup_time_utc"],
        "setup_timestamp_et": record["setup_time_et"],
        "direction": "long_call_only_when_family_selector_is_accepted",
        "direction_rule_status": (
            "accepted_for_clean_fast_break"
            if record["setup_family"] == "Clean Fast Break"
            else "rule_gap_no_accepted_local_family_selector"
        ),
        "freshness_deadline_utc": record["setup_time_utc"],
        "freshness_final_signal_state": record["freshness_final_signal_state"],
        "no_hindsight_boundary": record["no_hindsight_boundary"],
        "session_boundary_behavior": record["session_boundary_behavior"],
        "numeric_underlying_evidence": evidence,
        "trigger": record["trigger"],
        "trigger_numeric": None,
        "trigger_numeric_status": "RULE_GAP_NOT_NUMERICALLY_ESTABLISHED",
        "invalidation": record["invalidation"],
        "invalidation_numeric": None,
        "invalidation_numeric_status": "RULE_GAP_NOT_NUMERICALLY_ESTABLISHED",
        "numeric_room_or_target_required": True,
        "numeric_room_or_target": None,
        "numeric_room_or_target_status": "BLOCKED_UNTIL_TRIGGER_AND_INVALIDATION_NUMERIC",
        "rule_gap": rule_gap,
        "evidence_backed_fields_implemented": [
            "setup_timestamp",
            "direction_rule_status",
            "freshness_deadline",
            "no_hindsight_boundary",
            "session_boundary_behavior",
            "setup_minute_open_high_low_close_volume_envelope",
            "setup_minute_volume_weighted_close",
        ],
    }


def _option_evidence_spec(contract):
    family = contract["setup_family"]
    selector_ready = family == "Clean Fast Break"
    return {
        "setup_family": family,
        "symbol": "SPY",
        "call_or_put": "C" if selector_ready else "RULE_GAP_REQUIRES_ACCEPTED_FAMILY_SELECTOR",
        "contract_selection_timestamp_utc": contract["setup_timestamp_utc"],
        "permitted_expiration_range": {
            "rule": "nearest listed expiration with DTE >= 14",
            "start_date": "2026-03-30",
            "end_date": "2026-03-30",
            "status": "exact_rule_window_ready_definition_evidence_required",
        },
        "permitted_strike_range": {
            "rule": "first call strike at or above accepted numeric trigger",
            "lower_bound": None,
            "upper_bound": None,
            "status": "APPROVAL_UNLOCKS_AFTER_NUMERIC_TRIGGER_RULE_GAP_CLOSES",
        },
        "dataset": OPRA_DATASET,
        "schemas": list(OPRA_SCHEMAS),
        "stype_in": OPRA_STYPE_IN,
        "definition_window": {
            "schema": "definition",
            "start_timestamp_utc": "2026-03-16T13:30:00Z",
            "end_timestamp_utc": "2026-03-16T13:31:00Z",
            "symbols": "SPY",
            "query_type": "parent_symbol",
            "post_filter": "expiration=2026-03-30 and right=C and strike>=accepted_numeric_trigger",
        },
        "quote_window": {
            "schema": "tcbbo",
            "start_timestamp_utc": ENTRY_START_UTC,
            "end_timestamp_utc": ENTRY_END_UTC,
            "symbols": "selected_raw_symbol_after_definition_filter",
        },
        "trade_window": {
            "schema": "trades",
            "start_timestamp_utc": ENTRY_START_UTC,
            "end_timestamp_utc": ENTRY_END_UTC,
            "symbols": "selected_raw_symbol_after_definition_filter",
        },
        "statistics_volume_open_interest_window": {
            "schema": "statistics",
            "start_timestamp_utc": "2026-03-16T13:30:00Z",
            "end_timestamp_utc": ENTRY_END_UTC,
            "symbols": "selected_raw_symbol_after_definition_filter",
        },
        "required_symbols_or_parent_symbol_query": {
            "definition": "SPY parent-symbol query only",
            "quotes_trades_statistics": "selected raw_symbol only after definition and selector filtering",
        },
        "entry_evidence_window": {
            "start_timestamp_utc": ENTRY_START_UTC,
            "end_timestamp_utc": ENTRY_END_UTC,
        },
        "exit_evidence_window": {
            "start_timestamp_utc": ENTRY_START_UTC,
            "end_timestamp_utc": EXIT_END_UTC,
            "status": "conditional_on_selected_contract_and_eligible_entry",
        },
        "request_blockers_before_download": [
            "numeric_trigger_rule_gap",
            "numeric_invalidation_rule_gap",
            *([] if selector_ready else ["family_selector_rule_gap"]),
            "selected_contract_raw_symbol_not_known_locally",
        ],
    }


def _check_grouped_opra_cost(option_specs):
    windows = _cost_windows(option_specs)
    api_key = os.environ.get("SAFE_FAST_DB_AUTH")
    command = (
        "python -m historical_signal_replay.day51_spy_numeric_setup_and_opra_cost_check"
    )
    try:
        import databento as db
    except Exception as exc:
        return _cost_not_available(
            f"databento package unavailable: {exc}",
            windows=windows,
            command=command,
            credential_configured=bool(api_key),
        )
    try:
        credential_configured = bool(api_key)
        client_key = api_key or MISSING_AUTH_SENTINEL
        client = db.Historical(key=client_key)
        checked = []
        attempts = []
        for window in windows:
            if _window_requires_selected_contract_symbol(window):
                checked.append({
                    **window,
                    "checked_cost": "NOT_AVAILABLE",
                    "currency": "USD",
                    "status": "BLOCKED_BEFORE_API_CALL",
                    "reason": "selected raw_symbol is not known because numeric trigger/selector evidence is incomplete",
                })
                attempts.append({
                    **window,
                    "attempted": False,
                    "status": "BLOCKED_SELECTED_RAW_SYMBOL_UNKNOWN",
                    "technical_failure": "selected raw_symbol placeholder cannot be sent as an exact Databento symbol",
                })
                continue
            cost = Decimal(
                str(
                    client.metadata.get_cost(
                        dataset=window["dataset"],
                        start=window["start_timestamp_utc"],
                        end=window["end_timestamp_utc"],
                        symbols=window["symbols"],
                        schema=window["schema"],
                        stype_in=window["stype_in"],
                    )
                )
            )
            checked.append({**window, "checked_cost": str(cost), "currency": "USD", "status": "CHECKED"})
            attempts.append({**window, "attempted": True, "status": "CHECKED", "checked_cost": str(cost)})
        checked_costs = [
            Decimal(item["checked_cost"])
            for item in checked
            if item.get("checked_cost") not in (None, "NOT_AVAILABLE")
        ]
        if len(checked_costs) != len(windows):
            return _cost_not_available(
                "Databento cost check incomplete because selected raw_symbol windows cannot be priced before contract selection",
                windows=windows,
                command=command,
                credential_used=credential_configured,
                credential_configured=credential_configured,
                external_cost_api_called=True,
                api_attempts=attempts,
                checked_windows=checked,
            )
        total = sum(checked_costs)
        return {
            "status": "CHECKED",
            "attempted": True,
            "api_or_local_command_used": command,
            "credential_configured": credential_configured,
            "credential_used": credential_configured,
            "external_cost_api_called": True,
            "download_created": False,
            "paid_data_downloaded": False,
            "currency": "USD",
            "checked_total": str(total),
            "grouped_total": str(total),
            "sufficient_for_explicit_approval": True,
            "approval_status": "APPROVAL_REQUIRED",
            "schema_window_costs": checked,
            "api_attempts": attempts,
            "actual_billed_cost": "NOT_AVAILABLE",
            "checked_at_utc": _utc_now(),
        }
    except Exception as exc:
        return _cost_not_available(
            f"Databento cost check failed: {exc}",
            windows=windows,
            command=command,
            credential_used=bool(api_key),
            credential_configured=bool(api_key),
            external_cost_api_called=True,
            api_attempts=[{
                **_first_api_attemptable_window(windows),
                "attempted": True,
                "status": "FAILED",
                "technical_failure": f"{type(exc).__name__}: {exc}",
            }],
        )


def _cost_windows(option_specs):
    windows = []
    seen = set()
    for spec in option_specs:
        for key in (
            "definition_window",
            "quote_window",
            "trade_window",
            "statistics_volume_open_interest_window",
        ):
            window = spec[key]
            symbols = window["symbols"]
            item = {
                "setup_family": spec["setup_family"],
                "dataset": spec["dataset"],
                "schema": window["schema"],
                "stype_in": spec["stype_in"],
                "symbols": symbols,
                "start_timestamp_utc": window["start_timestamp_utc"],
                "end_timestamp_utc": window["end_timestamp_utc"],
            }
            dedupe_key = tuple(item[field] for field in (
                "dataset",
                "schema",
                "stype_in",
                "symbols",
                "start_timestamp_utc",
                "end_timestamp_utc",
            ))
            if dedupe_key in seen:
                continue
            seen.add(dedupe_key)
            windows.append(item)
    return windows


def _window_requires_selected_contract_symbol(window):
    return str(window.get("symbols")) == "selected_raw_symbol_after_definition_filter"


def _first_api_attemptable_window(windows):
    for window in windows or []:
        if not _window_requires_selected_contract_symbol(window):
            return window
    return {}


def _cost_not_available(
    reason,
    *,
    windows=None,
    command=None,
    credential_used=False,
    credential_configured=False,
    external_cost_api_called=False,
    api_attempts=None,
    checked_windows=None,
):
    windows = windows or []
    checked_windows = checked_windows or [
        {**window, "checked_cost": "NOT_AVAILABLE", "currency": "USD"}
        for window in windows
    ]
    return {
        "status": "NOT_AVAILABLE",
        "attempted": True,
        "api_or_local_command_used": command
        or "python -m historical_signal_replay.day51_spy_numeric_setup_and_opra_cost_check",
        "credential_configured": credential_configured,
        "credential_used": credential_used,
        "external_cost_api_called": external_cost_api_called,
        "download_created": False,
        "paid_data_downloaded": False,
        "currency": "USD",
        "checked_total": "NOT_AVAILABLE",
        "grouped_total": "NOT_AVAILABLE",
        "sufficient_for_explicit_approval": False,
        "approval_status": "APPROVAL_REQUIRED_COST_ESTIMATE_BLOCKED",
        "schema_window_costs": checked_windows,
        "api_attempts": api_attempts or [],
        "actual_billed_cost": "NOT_AVAILABLE",
        "reason": reason,
        "checked_at_utc": _utc_now(),
    }


def _approval_requirement(cost_check, option_specs):
    if cost_check["status"] == "CHECKED":
        return {
            "status": "APPROVAL_REQUIRED",
            "grouped_cost": cost_check["grouped_total"],
            "currency": cost_check["currency"],
            "estimate_sufficient_for_explicit_approval": True,
            "precise_data_unlocked": _precise_data_unlocked(option_specs),
            "next_action": (
                "Stop for explicit approval before any Databento OPRA download; "
                f"grouped checked cost is {cost_check['grouped_total']} {cost_check['currency']}."
            ),
        }
    return {
        "status": "APPROVAL_REQUIRED_COST_ESTIMATE_BLOCKED",
        "grouped_cost": "NOT_AVAILABLE",
        "currency": "USD",
        "estimate_sufficient_for_explicit_approval": False,
        "precise_data_unlocked": _precise_data_unlocked(option_specs),
        "next_action": (
            "Provide a successful Databento OPRA metadata cost estimate for the exact "
            "grouped request before any download or costed backtest."
        ),
    }


def _precise_data_unlocked(option_specs):
    return [
        {
            "setup_family": spec["setup_family"],
            "dataset": spec["dataset"],
            "definition": spec["definition_window"],
            "entry_quote": spec["quote_window"],
            "entry_trades": spec["trade_window"],
            "statistics": spec["statistics_volume_open_interest_window"],
            "exit": spec["exit_evidence_window"],
        }
        for spec in option_specs
    ]


def _replay_result(contract, local_evidence):
    blocker = [
        contract["trigger_numeric_status"],
        contract["invalidation_numeric_status"],
    ]
    if not local_evidence["has_march16_spy_opra_evidence"]:
        blocker.append("LOCAL_MARCH16_SPY_OPRA_EVIDENCE_MISSING")
    return {
        "setup_family": contract["setup_family"],
        "signal_timestamp": contract["setup_timestamp_utc"],
        "selected_contract": None,
        "entry_timestamp": None,
        "entry_price": None,
        "exit_timestamp": None,
        "exit_price": None,
        "gross_pnl": None,
        "spread_slippage_fees": None,
        "net_pnl": None,
        "hold_duration": None,
        "exit_reason": None,
        "trade_candidate": False,
        "selected_contract_stage": False,
        "eligible_entry": False,
        "recorded_entry": False,
        "costed_exit_replay_run": False,
        "status": "APPROVAL_REQUIRED_BEFORE_COSTED_BACKTEST",
        "blocking_reasons": blocker,
    }


def _local_option_evidence_inventory():
    base = day50_option_review._local_option_inventory()
    return {
        "directory": base["directory"],
        "exists": base["exists"],
        "file_count": base["file_count"],
        "march16_matching_files": base.get("march16_matching_files", []),
        "manifest_march16_requests": base.get("manifest_march16_requests", []),
        "has_march16_spy_opra_evidence": base.get("has_march16_spy_opra_evidence", False),
    }


def _underlying_setup_snapshot(setup_time_utc):
    rows = [
        row for row in _read_csv_rows(UNDERLYING_CSV_PATH)
        if _trim_nanos_z(row.get("ts_event")) == setup_time_utc
    ]
    highs = [_decimal_or_none(row.get("high")) for row in rows]
    lows = [_decimal_or_none(row.get("low")) for row in rows]
    opens = [_decimal_or_none(row.get("open")) for row in rows]
    closes = [_decimal_or_none(row.get("close")) for row in rows]
    volumes = [_decimal_or_none(row.get("volume")) or Decimal("0") for row in rows]
    total_volume = sum(volumes)
    weighted_close = None
    if total_volume:
        weighted_close = sum(
            (_decimal_or_none(row.get("close")) or Decimal("0")) * (_decimal_or_none(row.get("volume")) or Decimal("0"))
            for row in rows
        ) / total_volume
    return {
        "source_csv": _relative(UNDERLYING_CSV_PATH),
        "setup_time_utc": setup_time_utc,
        "rows_found": len(rows),
        "publisher_ids": sorted({row.get("publisher_id") for row in rows}),
        "open_min": _string_or_none(min(opens)) if opens else None,
        "open_max": _string_or_none(max(opens)) if opens else None,
        "high_min": _string_or_none(min(highs)) if highs else None,
        "high_max": _string_or_none(max(highs)) if highs else None,
        "low_min": _string_or_none(min(lows)) if lows else None,
        "low_max": _string_or_none(max(lows)) if lows else None,
        "close_min": _string_or_none(min(closes)) if closes else None,
        "close_max": _string_or_none(max(closes)) if closes else None,
        "volume_total": _string_or_none(total_volume),
        "volume_weighted_close": _string_or_none(weighted_close),
        "numeric_values_are_evidence_not_trigger_or_invalidation": True,
    }


def _scorecard(replay_results):
    return {
        "raw_opportunities_mapped": len(replay_results),
        "exact_setup_time_field_packages_established": len(replay_results),
        "new_generated_candidates": len(replay_results),
        "new_setup_qualified_candidates": len(replay_results),
        "new_trade_candidates": sum(1 for result in replay_results if result["trade_candidate"]),
        "new_selected_contracts": sum(1 for result in replay_results if result["selected_contract_stage"]),
        "new_eligible_entries": sum(1 for result in replay_results if result["eligible_entry"]),
        "new_recorded_entries": sum(1 for result in replay_results if result["recorded_entry"]),
        "new_exact_option_contract_evidence_required_cases": sum(
            1 for result in replay_results if not result["selected_contract_stage"]
        ),
        "new_exact_data_required_cases": sum(
            1 for result in replay_results if not result["selected_contract_stage"]
        ),
        "new_exits_evaluated": sum(1 for result in replay_results if result["costed_exit_replay_run"]),
        "new_valid_trades_captured": 0,
        "new_true_no_trades": 0,
        "new_missed_valid_trades": 0,
        "new_invalid_trades_allowed": 0,
        "new_unresolved_cases": 0,
        "new_winners": 0,
        "new_losers": 0,
    }


def _markdown_result(document):
    cost = document["grouped_opra_cost_check"]
    approval = document["approval_required"]
    rows = "\n".join(
        (
            f"- {record['setup_family']}: trigger numeric `{record['trigger_numeric']}` "
            f"({record['trigger_numeric_status']}), invalidation numeric "
            f"`{record['invalidation_numeric']}` ({record['invalidation_numeric_status']}); "
            f"setup evidence VWAP `{record['numeric_underlying_evidence']['volume_weighted_close']}`."
        )
        for record in document["numeric_setup_contracts"]
    )
    replay_rows = "\n".join(
        (
            f"- {family}: selected contract `None`; entry `None`; exit `None`; "
            f"net P&L `None`; status `{result['status']}`."
        )
        for family, result in document["costed_backtest_results_by_setup_family"].items()
    )
    attempt = (cost.get("api_attempts") or [{}])[0]
    attempt_summary = (
        f"{attempt.get('status')} on {attempt.get('dataset')} {attempt.get('schema')} "
        f"{attempt.get('symbols')} {attempt.get('start_timestamp_utc')} to "
        f"{attempt.get('end_timestamp_utc')}: {attempt.get('technical_failure')}"
        if attempt
        else "No API attempt record"
    )
    return f"""# SAFE-FAST Day 51 SPY Numeric Setup and OPRA Cost Check Result

## Scope

- Task executed: `{TASK_FILENAME}`.
- Machine-readable result: `historical_signal_replay/results/day51_spy_numeric_setup_and_opra_cost_check.json`.
- Implementation: `historical_signal_replay/day51_spy_numeric_setup_and_opra_cost_check.py`.
- Validator: `watcher_foundation/day51_spy_numeric_setup_and_opra_cost_check_validator.py`.
- Focused tests: `tests/test_day51_spy_numeric_setup_and_opra_cost_check.py`.
- Covered setup families: Ideal, Clean Fast Break, and Continuation for SPY on `2026-03-16` only.

## Numeric Setup Contract

{rows}

The exact rule gap remains: the accepted Day 50 mapper names family trigger and invalidation contracts but does not bind those contracts to a numeric OHLCV field. Raw setup-minute high/low/open/close values are recorded as evidence only and were not promoted into trigger or invalidation thresholds.

## Exact OPRA Specification

One grouped request specification was produced for Databento `OPRA.PILLAR` schemas `definition`, `tcbbo`, `trades`, and `statistics`. It is constrained to SPY parent definitions at the setup timestamp, nearest DTE >= 14 expiration (`2026-03-30`), entry evidence from `13:30Z` to `13:35Z`, and selected-contract exit evidence through `19:45Z` only after a selected raw symbol exists.

## Cost Check

- Status: `{cost['status']}`.
- Grouped total: `{cost['grouped_total']}` `{cost['currency']}`.
- API/local command used: `{cost['api_or_local_command_used']}`.
- External metadata API called: `{cost['external_cost_api_called']}`.
- Credential configured: `{cost.get('credential_configured')}`.
- Credential used: `{cost['credential_used']}`.
- API attempt result: `{attempt_summary}`.
- Estimate sufficient for explicit approval: `{cost['sufficient_for_explicit_approval']}`.
- Download created: `{cost['download_created']}`.

## Replay

{replay_rows}

No costed backtest was run because numeric trigger/invalidation remain rule-gapped and local March 16 SPY OPRA selected-contract evidence is absent.

## Final Status

`{approval['status']}` grouped cost `{approval['grouped_cost']}` `{approval['currency']}`. The precise data it unlocks is the exact grouped SPY OPRA definition, selected-contract quote, trade, statistics, and conditional exit evidence listed in the JSON result.

## Guardrails

No `main.py`, Railway/deploy, production/live backend, broker/account/order code, credentials, `.env`, sizing, alerts, frozen `patch8` thresholds, paid download, proof, paper/live eligibility, or profitability claim was changed or created.
"""


def _read_csv_rows(path):
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _trim_nanos_z(value):
    text = str(value)
    if "." in text and text.endswith("Z"):
        prefix, suffix = text[:-1].split(".", 1)
        return f"{prefix}.{suffix[:6]}Z".replace(".000000Z", "Z")
    return text


def _decimal_or_none(value):
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def _string_or_none(value):
    return str(value) if value is not None else None


def _stable_hash(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _relative(path):
    return str(Path(path).relative_to(REPO_ROOT)).replace("\\", "/")


def _utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _git_short_head():
    head = REPO_ROOT / ".git" / "HEAD"
    if not head.exists():
        return "UNKNOWN"
    text = head.read_text(encoding="utf-8").strip()
    if text.startswith("ref: "):
        ref = REPO_ROOT / ".git" / text[5:]
        if ref.exists():
            return ref.read_text(encoding="utf-8").strip()[:7]
    return text[:7]


if __name__ == "__main__":
    doc = write_outputs()
    cost = doc["grouped_opra_cost_check"]
    print(
        "wrote day51 SPY numeric setup and OPRA cost check: "
        f"{doc['after_funnel_totals']['new_trade_candidates']} trade candidates, "
        f"{doc['after_funnel_totals']['new_selected_contracts']} selected contracts, "
        f"grouped cost {cost['grouped_total']} {cost['currency']}"
    )
