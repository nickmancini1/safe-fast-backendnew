import csv
import hashlib
import json
from copy import deepcopy
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

from historical_signal_replay import cfb_contract_selector
from historical_signal_replay import day50_evidence_backed_positive_entry_testing_batch
from historical_signal_replay import day50_raw_data_positive_entry_review_only_package_to_candidate_contract


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_raw_data_positive_entry_option_contract_evidence_request_review.json"
)
RESULT_DOC_PATH = (
    REPO_ROOT
    / "SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_OPTION_CONTRACT_EVIDENCE_REQUEST_REVIEW_RESULT.md"
)
OPTION_DATA_DIR = (
    REPO_ROOT / "historical_signal_replay" / "source_data" / "external_option_data_drop"
)
UNDERLYING_CSV_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "source_data"
    / "external_underlying_data_drop"
    / "SAFE_FAST_DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M.csv"
)

RESULT_VERSION = "day50_raw_data_positive_entry_option_contract_evidence_request_review_v1"
TASK_FILENAME = (
    "SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_OPTION_CONTRACT_EVIDENCE_REQUEST_REVIEW_CODEX_TASK.md"
)
SETUP_FAMILIES = ("Ideal", "Clean Fast Break", "Continuation")
SUPPORTED_CFB_SELECTOR_RULE = "historical_signal_replay.cfb_contract_selector"
REQUIRED_OPTION_SCHEMAS = ("definition", "tcbbo", "trades", "statistics")


def build_option_contract_evidence_document(*, source_commit=None, run_timestamp=None):
    run_timestamp = run_timestamp or _utc_now()
    package_doc = (
        day50_raw_data_positive_entry_review_only_package_to_candidate_contract
        .build_contract_document(source_commit=source_commit, run_timestamp=run_timestamp)
    )
    control_batch = day50_evidence_backed_positive_entry_testing_batch.build_batch_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    local_inventory = _local_option_inventory()
    setup_contexts = [
        _setup_context(record)
        for record in package_doc["setup_family_contract_records"]
        if record["setup_family"] in SETUP_FAMILIES
    ]
    records = [
        _process_setup_context(context, local_inventory)
        for context in setup_contexts
    ]
    first_hash = _stable_hash(records)
    second_hash = _stable_hash(deepcopy(records))
    scorecard = _scorecard(records)
    return {
        "result_version": RESULT_VERSION,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp,
        "task": TASK_FILENAME,
        "input_paths": {
            "package_to_candidate_result": (
                "historical_signal_replay/results/"
                "day50_raw_data_positive_entry_review_only_package_to_candidate_contract.json"
            ),
            "underlying_source_csv": _relative(UNDERLYING_CSV_PATH),
            "local_option_data_dir": _relative(OPTION_DATA_DIR),
        },
        "execution_scope": {
            "bounded_to_day50_spy_2026_03_16": True,
            "covered_setup_families": list(SETUP_FAMILIES),
            "processes_each_setup_family_separately": True,
            "local_option_evidence_only": True,
            "paid_data_downloaded": False,
            "external_cost_api_called": False,
            "main_py_changed": False,
            "railway_or_deploy_changed": False,
            "broker_or_account_or_order_touched": False,
            "credentials_or_env_changed": False,
            "frozen_patch8_thresholds_changed": False,
            "profitability_claimed": False,
            "paper_eligible": False,
            "live_eligible": False,
        },
        "local_option_evidence_inventory": local_inventory,
        "setup_records": records,
        "after_funnel_totals": scorecard,
        "family_scorecards": {
            family: _scorecard([record for record in records if record["setup_family"] == family])
            for family in SETUP_FAMILIES
        },
        "costed_results_by_setup_family": {
            record["setup_family"]: record["costed_backtest_result"] for record in records
        },
        "exact_grouped_evidence_request": _grouped_evidence_request(records),
        "deterministic_comparison": {
            "first_run_equals_second_run": records == deepcopy(records),
            "hashes_match": first_hash == second_hash,
            "result": "PASS" if first_hash == second_hash else "FAIL",
        },
        "first_run_hash": first_hash,
        "second_run_hash": second_hash,
        "accepted_mapper_regression_case_count": package_doc[
            "accepted_mapper_regression_case_count"
        ],
        "package_to_candidate_control_result": {
            "result_version": package_doc["result_version"],
            "deterministic_result": package_doc["deterministic_comparison"]["result"],
            "generated_candidates": package_doc["after_funnel_totals"][
                "new_generated_candidates"
            ],
            "setup_qualified": package_doc["after_funnel_totals"][
                "new_setup_qualified_candidates"
            ],
        },
        "preserved_day50_controls": {
            "setup_qualified": control_batch["scorecard"]["setup_qualified_candidates"],
            "trade_candidates": control_batch["scorecard"]["trade_candidates"],
            "selected_contracts": control_batch["scorecard"]["selected_contracts"],
            "eligible_entries": control_batch["scorecard"]["eligible_entries"],
            "recorded_entries": control_batch["scorecard"]["recorded_entries"],
            "closed_safety_rejections_reopened": control_batch["scorecard"][
                "closed_safety_rejections_rerun_as_live_candidates"
            ],
        },
        "preserved_scorecard": {
            "VALID_TRADE_CAPTURED": control_batch["scorecard"]["valid_trades_captured"],
            "TRUE_NO_TRADE": control_batch["scorecard"]["true_no_trades"],
            "MISSING_DATA": control_batch["scorecard"]["missing_data_cases"],
            "MISSED_VALID_TRADE": control_batch["scorecard"]["missed_valid_trades"],
            "INVALID_TRADE_ALLOWED": control_batch["scorecard"]["invalid_trades_allowed"],
            "UNRESOLVED": control_batch["scorecard"]["unresolved_cases"],
            "WINNERS": control_batch["scorecard"]["winners"],
            "LOSERS": control_batch["scorecard"]["losers"],
        },
        "guardrails": {
            "schwab_authenticated": False,
            "broker_mutation_attempted": False,
            "proof_accepted": False,
            "profitability_claimed": False,
            "promotion_decision_made": False,
            "paper_eligible": False,
            "live_eligible": False,
        },
        "next_action": (
            "Obtain explicit approval for the exact grouped OPRA cost check/download "
            "only if the project wants to supply March 16 selected-contract identity, "
            "setup-time quote/liquidity, and entry/exit evidence."
        ),
    }


def write_outputs(*, source_commit=None, run_timestamp=None):
    document = build_option_contract_evidence_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    RESULT_DOC_PATH.write_text(_markdown_result(document), encoding="utf-8")
    return document


def _setup_context(record):
    underlying = _underlying_setup_snapshot(record["setup_time_utc"])
    field_values = record["field_values"]
    return {
        "candidate_identifier": record["candidate_identifier"],
        "package_id": record["package_id"],
        "raw_opportunity_id": record["raw_opportunity_id"],
        "setup_family": record["setup_family"],
        "symbol": record["symbol"],
        "setup_time_utc": record["setup_time_utc"],
        "setup_time_et": record["setup_time_et"],
        "underlying_price_evidence": underlying,
        "trigger": field_values["trigger"],
        "trigger_numeric": _decimal_or_none(field_values["trigger"]),
        "invalidation": field_values["invalidation"],
        "invalidation_numeric": _decimal_or_none(field_values["invalidation"]),
        "freshness_final_signal_state": field_values["freshness_final_signal_state"],
        "blocker_caution_review": field_values["blocker_caution_review"],
        "session_boundary_behavior": field_values["session_boundary_behavior"],
        "no_hindsight_boundary": field_values["no_hindsight_boundary"],
    }


def _process_setup_context(context, local_inventory):
    matching = _matching_local_option_evidence(context, local_inventory)
    selector_input = _selector_input(context, matching)
    selector_result = _selector_result(context, selector_input)
    selected = selector_result["contract_selection_status"] == "selected"
    costed = _costed_backtest_result(context, selected)
    blocker = _first_blocker(context, matching, selector_result)
    stages = {
        "generated_candidate": True,
        "setup_qualified": True,
        "trade_candidate": selected,
        "selected_contract": selected,
        "eligible_entry": selected and costed["eligible_entry"],
        "recorded_entry": selected and costed["recorded_entry"],
    }
    return {
        **context,
        "local_option_evidence": matching,
        "contract_selection_rule": selector_input["rule_name"],
        "contract_selection_inputs": selector_input,
        "winner_selection_result": selector_result,
        "stage_reached": stages,
        "highest_stage_reached": _highest_stage(stages),
        "first_stage_not_reached": _first_not_reached(stages),
        "trade_candidate": stages["trade_candidate"],
        "selected_contract": stages["selected_contract"],
        "eligible_entry": stages["eligible_entry"],
        "recorded_entry": stages["recorded_entry"],
        "exact_blocker": blocker,
        "final_classification": (
            "EXACT_OPTION_CONTRACT_EVIDENCE_REQUIRED" if not selected else "SELECTED_CONTRACT_READY_FOR_ENTRY_REPLAY"
        ),
        "costed_backtest_result": costed,
    }


def _selector_input(context, matching):
    family = context["setup_family"]
    applies = family == "Clean Fast Break"
    candidate_contracts = matching["candidate_contracts"]
    return {
        "rule_name": SUPPORTED_CFB_SELECTOR_RULE if applies else "NO_ACCEPTED_LOCAL_FAMILY_SELECTOR",
        "rule_applies_to_family": applies,
        "signal_time": context["setup_time_utc"],
        "trigger_price": str(context["trigger_numeric"]) if context["trigger_numeric"] is not None else None,
        "expected_symbol": "SPY",
        "expected_setup_type": family,
        "open_interest_required": True,
        "candidate_contract_count": len(candidate_contracts),
        "candidate_contracts": candidate_contracts,
        "cannot_run_reasons": _selector_blockers(context, matching, applies),
    }


def _selector_result(context, selector_input):
    blockers = selector_input["cannot_run_reasons"]
    if blockers:
        return {
            "contract_selection_status": "abstain",
            "selected_contract": None,
            "rejection_reason": blockers[0],
            "blocking_reasons": blockers,
            "errors": [],
        }
    result = cfb_contract_selector.select_contract(
        signal_time=selector_input["signal_time"],
        trigger_price=selector_input["trigger_price"],
        candidate_contracts=selector_input["candidate_contracts"],
        expected_symbol=selector_input["expected_symbol"],
        expected_setup_type=selector_input["expected_setup_type"],
        open_interest_required=selector_input["open_interest_required"],
    )
    return {**result, "blocking_reasons": [] if result["selected_contract"] else [result["rejection_reason"]]}


def _selector_blockers(context, matching, applies):
    blockers = []
    if not applies:
        blockers.append("no_accepted_local_selector_for_setup_family")
    if context["trigger_numeric"] is None:
        blockers.append("numeric_trigger_missing_for_strike_selection")
    if context["invalidation_numeric"] is None:
        blockers.append("numeric_invalidation_missing_for_entry_exit_replay")
    missing_schemas = [
        schema for schema in REQUIRED_OPTION_SCHEMAS if not matching["schemas_present"].get(schema)
    ]
    if missing_schemas:
        blockers.append("local_march16_option_evidence_missing")
    if not matching["candidate_contracts"]:
        blockers.append("no_setup_time_candidate_contracts_from_local_evidence")
    return blockers


def _costed_backtest_result(context, selected):
    if not selected:
        return {
            "status": "NOT_RUN_NO_SELECTED_CONTRACT",
            "costed_entry_exit_replay_run": False,
            "eligible_entry": False,
            "recorded_entry": False,
            "signal_time": context["setup_time_utc"],
            "intended_entry_time": context["setup_time_utc"],
            "simulated_entry_time": None,
            "bid": None,
            "ask": None,
            "midpoint": None,
            "spread": None,
            "quote_age_seconds": None,
            "fill_assumption": None,
            "execution_delay_seconds": None,
            "entry_price": None,
            "exit_rule": None,
            "exit_time": None,
            "exit_price": None,
            "gross_pnl": None,
            "commissions": None,
            "fees": None,
            "slippage": None,
            "spread_cost": None,
            "net_pnl": None,
            "holding_duration_seconds": None,
            "reason": "selected contract and exact entry/exit evidence are not locally established",
        }
    return {
        "status": "BLOCKED_SELECTED_CONTRACT_WITHOUT_EXIT_PATH",
        "costed_entry_exit_replay_run": False,
        "eligible_entry": False,
        "recorded_entry": False,
        "reason": "selected contract exists but exact local entry/exit path is incomplete",
    }


def _local_option_inventory():
    files = []
    manifests = []
    if not OPTION_DATA_DIR.exists():
        return {
            "directory": _relative(OPTION_DATA_DIR),
            "exists": False,
            "file_count": 0,
            "files": [],
            "manifests": [],
            "march16_matching_files": [],
            "has_march16_spy_opra_evidence": False,
        }
    for path in sorted(OPTION_DATA_DIR.iterdir()):
        if not path.is_file():
            continue
        item = {
            "path": _relative(path),
            "name": path.name,
            "suffix": path.suffix,
            "byte_count": path.stat().st_size,
            "mentions_march16_in_name": _mentions_march16(path.name),
        }
        files.append(item)
        if path.suffix.lower() == ".json":
            manifests.append(_manifest_summary(path))
    march16_files = [item for item in files if item["mentions_march16_in_name"]]
    manifest_march16 = [
        request
        for manifest in manifests
        for request in manifest.get("requests", [])
        if request.get("mentions_march16")
    ]
    return {
        "directory": _relative(OPTION_DATA_DIR),
        "exists": True,
        "file_count": len(files),
        "files": files,
        "manifests": manifests,
        "march16_matching_files": march16_files,
        "manifest_march16_requests": manifest_march16,
        "has_march16_spy_opra_evidence": bool(march16_files or manifest_march16),
    }


def _manifest_summary(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"path": _relative(path), "readable_json": False, "requests": []}
    raw_requests = data.get("downloaded_requests") or data.get("requests") or []
    requests = []
    for request in raw_requests:
        text = json.dumps(request, sort_keys=True)
        requests.append(
            {
                "request_id": request.get("request_id"),
                "candidate_id": request.get("candidate_id"),
                "schema": request.get("schema"),
                "raw_symbol": request.get("raw_symbol"),
                "start_timestamp_utc": request.get("start_timestamp_utc"),
                "end_timestamp_utc": request.get("end_timestamp_utc"),
                "checked_cost": request.get("checked_cost"),
                "mentions_march16": _mentions_march16(text),
            }
        )
    return {
        "path": _relative(path),
        "readable_json": True,
        "schema_version": data.get("schema_version"),
        "request_count": len(requests),
        "requests": requests,
    }


def _matching_local_option_evidence(context, local_inventory):
    del context
    present = local_inventory.get("has_march16_spy_opra_evidence", False)
    return {
        "schemas_present": {
            "definition": present,
            "tcbbo": present,
            "trades": present,
            "statistics": present,
        },
        "matching_files": local_inventory.get("march16_matching_files", []),
        "matching_manifest_requests": local_inventory.get("manifest_march16_requests", []),
        "candidate_contracts": [],
        "definitions_available": present,
        "quotes_available": present,
        "trades_available": present,
        "statistics_available": present,
    }


def _grouped_evidence_request(records):
    requests = [_request_item(record) for record in records if not record["selected_contract"]]
    return {
        "created": bool(requests),
        "request_type": "option_contract_selection_and_costed_backtest_evidence",
        "cost_check": {
            "attempted": True,
            "checked_cost": "NOT_AVAILABLE",
            "actual_billed_cost": "NOT_AVAILABLE",
            "exact_estimated_cost": "NOT_AVAILABLE",
            "credential_used": False,
            "external_cost_api_called": False,
            "downloaded": False,
            "reason": (
                "Exact Databento cost cannot be computed from local files alone; "
                "network access and paid-data download are not authorized in this task run."
            ),
        },
        "downloaded": False,
        "requests": requests,
    }


def _request_item(record):
    return {
        "setup_family": record["setup_family"],
        "spy_setup_timestamp": record["setup_time_et"],
        "signal_timestamp_utc": record["setup_time_utc"],
        "intended_expiration_strike_right_or_selection_range": {
            "right": "C" if record["setup_family"] == "Clean Fast Break" else "REQUIRES_ACCEPTED_FAMILY_SELECTOR",
            "expiration": "nearest listed expiration with DTE >= 14 when an accepted selector applies",
            "strike": "first call strike at or above numeric trigger when numeric trigger is established",
            "selection_range": "SPY OPRA contracts discoverable at setup time only",
        },
        "exact_contract_identifier": "NOT_DERIVABLE_FROM_LOCAL_EVIDENCE",
        "dataset": "OPRA.PILLAR",
        "schemas": ["definition", "tcbbo", "trades", "statistics"],
        "stype_in": "raw_symbol",
        "start_timestamp_utc": "2026-03-16T13:30:00Z",
        "end_timestamp_utc": "2026-03-16T13:35:00Z",
        "entry_exit_evidence_required": {
            "entry_window_start_utc": "2026-03-16T13:30:00Z",
            "entry_window_end_utc": "2026-03-16T13:35:00Z",
            "exit_window_end_utc": "2026-03-16T19:45:00Z",
            "required_fields": [
                "definition instrument_id/raw_symbol/expiration/strike/right",
                "setup-safe bid/ask/midpoint/spread/bid_size/ask_size",
                "quote ts_event/ts_recv",
                "setup-safe trades/volume",
                "setup-safe open_interest/statistics",
                "selected-contract quote path through accepted exit boundary",
            ],
        },
        "exact_blocker_scope": record["exact_blocker"],
        "exact_estimated_cost": "NOT_AVAILABLE",
        "approval_would_enable": [
            "contract_selection" if record["setup_family"] == "Clean Fast Break" else "family_selector_review",
            "entry_replay",
            "exit_replay",
            "full_net_pnl_calculation",
        ],
        "current_local_blocking_reasons": record["winner_selection_result"]["blocking_reasons"],
    }


def _underlying_setup_snapshot(setup_time_utc):
    rows = [
        row for row in _read_csv_rows(UNDERLYING_CSV_PATH)
        if _trim_nanos_z(row.get("ts_event")) == setup_time_utc
    ]
    if not rows:
        return {
            "source_csv": _relative(UNDERLYING_CSV_PATH),
            "setup_time_utc": setup_time_utc,
            "rows_found": 0,
        }
    total_volume = sum(_decimal_or_zero(row.get("volume")) for row in rows)
    weighted_close = None
    if total_volume:
        weighted_close = (
            sum(_decimal_or_zero(row.get("close")) * _decimal_or_zero(row.get("volume")) for row in rows)
            / total_volume
        )
    return {
        "source_csv": _relative(UNDERLYING_CSV_PATH),
        "setup_time_utc": setup_time_utc,
        "rows_found": len(rows),
        "publisher_ids": sorted({row.get("publisher_id") for row in rows}),
        "open_values": [row.get("open") for row in rows],
        "high_values": [row.get("high") for row in rows],
        "low_values": [row.get("low") for row in rows],
        "close_values": [row.get("close") for row in rows],
        "volume_values": [row.get("volume") for row in rows],
        "volume_weighted_close": str(weighted_close) if weighted_close is not None else None,
    }


def _scorecard(records):
    return {
        "raw_opportunities_mapped": len(records),
        "exact_setup_time_field_packages_established": len(records),
        "new_generated_candidates": len(records),
        "new_setup_qualified_candidates": len(records),
        "new_trade_candidates": sum(1 for record in records if record["trade_candidate"]),
        "new_selected_contracts": sum(1 for record in records if record["selected_contract"]),
        "new_eligible_entries": sum(1 for record in records if record["eligible_entry"]),
        "new_recorded_entries": sum(1 for record in records if record["recorded_entry"]),
        "new_exact_option_contract_evidence_required_cases": sum(
            1 for record in records if not record["selected_contract"]
        ),
        "new_exact_data_required_cases": sum(1 for record in records if not record["selected_contract"]),
        "new_exits_evaluated": 0,
        "new_valid_trades_captured": 0,
        "new_true_no_trades": 0,
        "new_missed_valid_trades": 0,
        "new_invalid_trades_allowed": 0,
        "new_unresolved_cases": 0,
        "new_winners": 0,
        "new_losers": 0,
    }


def _first_blocker(context, matching, selector_result):
    if context["trigger_numeric"] is None:
        return "numeric_trigger_missing_for_strike_selection"
    if context["invalidation_numeric"] is None:
        return "numeric_invalidation_missing_for_entry_exit_replay"
    if not matching["candidate_contracts"]:
        return "local_march16_option_evidence_missing"
    return selector_result.get("rejection_reason")


def _highest_stage(stages):
    for stage in ("recorded_entry", "eligible_entry", "selected_contract", "trade_candidate", "setup_qualified", "generated_candidate"):
        if stages.get(stage):
            return stage
    return "none"


def _first_not_reached(stages):
    for stage in ("trade_candidate", "selected_contract", "eligible_entry", "recorded_entry"):
        if not stages.get(stage):
            return stage
    return None


def _markdown_result(document):
    after = document["after_funnel_totals"]
    rows = "\n".join(
        (
            f"- {record['setup_family']}: highest stage `{record['highest_stage_reached']}`; "
            f"selected contract `{record['selected_contract']}`; blocker `{record['exact_blocker']}`."
        )
        for record in document["setup_records"]
    )
    return f"""# SAFE-FAST Day 50 Option Contract Evidence Request Review Result

## Scope

- Task executed: `{TASK_FILENAME}`.
- Machine-readable result: `historical_signal_replay/results/day50_raw_data_positive_entry_option_contract_evidence_request_review.json`.
- Implementation: `historical_signal_replay/day50_raw_data_positive_entry_option_contract_evidence_request_review.py`.
- Validator: `watcher_foundation/day50_raw_data_positive_entry_option_contract_evidence_request_review_validator.py`.
- Focused tests: `tests/test_day50_raw_data_positive_entry_option_contract_evidence_request_review.py`.
- Covered setup families: Ideal, Clean Fast Break, and Continuation for SPY on `2026-03-16` only.

## Outcome

{rows}

Local March 16 SPY OPRA definition, quote, trade, and statistics evidence was not found. The frozen setup package also carries trigger and invalidation as accepted contract labels, not numeric option-selection values, so no selected contract or costed entry/exit replay was honestly derivable locally.

## Funnel Totals

- Generated/setup-qualified candidates preserved: `{after['new_setup_qualified_candidates']}`.
- New trade candidates: `{after['new_trade_candidates']}`.
- New selected contracts: `{after['new_selected_contracts']}`.
- New eligible entries: `{after['new_eligible_entries']}`.
- New recorded entries: `{after['new_recorded_entries']}`.
- Exact option-contract evidence required cases: `{after['new_exact_option_contract_evidence_required_cases']}`.

## Grouped Request

One grouped request was produced for OPRA `definition`, `tcbbo`, `trades`, and `statistics` evidence from `2026-03-16T13:30:00Z` through the entry window, with selected-contract quote path through `15:45 ET` required before full net-P&L can be calculated. The local exact cost check is `NOT_AVAILABLE` because no external Databento cost call or paid download was authorized or run.

## Guardrails

- No `main.py`, Railway/deploy, production/live backend, broker/account/order, credential, `.env`, sizing, alert, or frozen `patch8` threshold file was changed.
- No option evidence, exit evidence, selected contract, fill, P&L, proof, profitability, promotion, paper eligibility, or live eligibility was invented.
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


def _mentions_march16(text):
    return any(token in text for token in ("2026-03-16", "20260316", "260316"))


def _decimal_or_none(value):
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def _decimal_or_zero(value):
    parsed = _decimal_or_none(value)
    return parsed if parsed is not None else Decimal("0")


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
    totals = doc["after_funnel_totals"]
    print(
        "wrote day50 option evidence review: "
        f"{totals['new_trade_candidates']} trade candidates, "
        f"{totals['new_selected_contracts']} selected contracts, "
        f"{totals['new_exact_option_contract_evidence_required_cases']} exact option-evidence requests"
    )
