import csv
import hashlib
import json
import os
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from historical_signal_replay import day48_positive_trade_capture_funnel
from historical_signal_replay import day50_evidence_backed_positive_entry_testing_batch
from historical_signal_replay import (
    day50_raw_data_positive_entry_underlying_setup_time_request as day50_underlying,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_end_to_end_raw_data_positive_entry_generation.json"
)
MANIFEST_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "fixtures"
    / "day50_raw_data_positive_entry_candidate_manifest.json"
)

RESULT_VERSION = "day50_end_to_end_raw_data_positive_entry_generation_v1"
MANIFEST_VERSION = "day50_raw_data_positive_entry_candidate_manifest_v1"
NEXT_TASK_FILENAME = (
    "SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_SETUP_TIME_REPLAY_MAPPING_CODEX_TASK.md"
)

FUNNEL_STAGES = [
    "SETUP_DEVELOPING",
    "SETUP_QUALIFIED",
    "TRADE_CANDIDATE",
    "CONTRACT_SELECTED",
    "PRICE_ACCEPTABLE",
    "ENTRY_ELIGIBLE",
    "ENTRY_RECORDED",
    "EXIT_EVALUATED",
    "FINAL_OUTCOME",
]

SETUP_FAMILIES = ("Ideal", "Clean Fast Break", "Continuation")
CLASSIFICATIONS = (
    "VALID_TRADE_CAPTURED",
    "TRUE_NO_TRADE",
    "EXACT_DATA_REQUIRED",
    "MISSED_VALID_TRADE",
    "INVALID_TRADE_ALLOWED",
    "UNRESOLVED",
)

INCOMING_SOURCE_DIR = REPO_ROOT / "historical_signal_replay" / "source_data" / "incoming"
EXTERNAL_UNDERLYING_DIR = (
    REPO_ROOT / "historical_signal_replay" / "source_data" / "external_underlying_data_drop"
)
EXTERNAL_OPTION_DIR = (
    REPO_ROOT / "historical_signal_replay" / "source_data" / "external_option_data_drop"
)

MINIMUM_UNDERLYING_RESOLUTION = {
    "Ideal": "1m_rth_or_finer",
    "Clean Fast Break": "1m_rth_or_finer",
    "Continuation": "1m_rth_or_finer",
}


def build_generation_document(*, source_commit=None, run_timestamp=None, check_cost=False):
    run_timestamp = run_timestamp or _utc_now()
    inventory = build_raw_data_inventory()
    prior_candidate_ids = _prior_candidate_identifiers()
    rejected_opportunities = _inspect_raw_opportunities(inventory, prior_candidate_ids)
    generated_candidates = []
    first_run = _run_full_trade_funnel(generated_candidates)
    second_run = _run_full_trade_funnel(generated_candidates)
    exact_data_request = _build_exact_underlying_request(inventory)
    acquisition_manifest = day50_underlying.load_download_manifest()
    if check_cost:
        exact_data_request["cost_check"] = _check_databento_cost(exact_data_request)
    else:
        exact_data_request["cost_check"] = _not_available_cost(
            "cost check skipped by deterministic unit-test path"
        )
    _apply_acquisition_status(exact_data_request, acquisition_manifest)

    manifest = _build_manifest(
        inventory=inventory,
        prior_candidate_ids=prior_candidate_ids,
        rejected_opportunities=rejected_opportunities,
        generated_candidates=generated_candidates,
        exact_data_request=exact_data_request,
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    first_hash = _stable_hash(_stable_generation_payload(manifest, first_run))
    second_hash = _stable_hash(_stable_generation_payload(manifest, second_run))
    day48_first = day48_positive_trade_capture_funnel.build_funnel_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    day48_second = day48_positive_trade_capture_funnel.build_funnel_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    day50_batch = day50_evidence_backed_positive_entry_testing_batch.build_batch_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )

    return {
        "result_version": RESULT_VERSION,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp,
        "input_paths": {
            "data_source_registry": "SAFE_FAST_DATA_SOURCE_REGISTRY.md",
            "proof_pipeline": "SAFE_FAST_PROJECT_PROOF_PIPELINE.md",
            "day50_active_path_requirement_regression": (
                "SAFE_FAST_DAY50_POSITIVE_ENTRY_ACTIVE_PATH_REQUIREMENT_REGRESSION_RESULT.md"
            ),
            "day50_evidence_backed_batch": (
                "SAFE_FAST_DAY50_EVIDENCE_BACKED_POSITIVE_ENTRY_TESTING_BATCH_RESULT.md"
            ),
            "day48_positive_trade_funnel": (
                "SAFE_FAST_DAY48_POSITIVE_TRADE_CAPTURE_AND_MISS_ANALYSIS_RESULT.md"
            ),
        },
        "generation_policy": {
            "source": "complete chronological local raw underlying evidence first",
            "protected_holdout_periods_excluded": True,
            "previously_measured_candidate_ids_excluded": sorted(prior_candidate_ids),
            "duplicate_signals_from_same_opportunity_excluded": True,
            "future_option_performance_used": False,
            "outcome_data_used_for_candidate_selection": False,
            "winners_and_losers_preserved_equally": True,
            "frozen_rules_changed": False,
            "main_py_changed": False,
            "railway_or_deploy_changed": False,
            "paid_data_downloaded": _acquired_without_problems(acquisition_manifest),
        },
        "raw_data_inventory": inventory,
        "minimum_underlying_data_requirements": _minimum_underlying_requirements(),
        "candidate_manifest_path": _relative(MANIFEST_PATH),
        "candidate_manifest": manifest,
        "full_trade_funnel_first_run": first_run,
        "full_trade_funnel_second_run": second_run,
        "deterministic_comparison": {
            "first_run_equals_second_run": first_run == second_run,
            "hashes_match": first_hash == second_hash,
            "result": "PASS" if first_hash == second_hash else "FAIL",
        },
        "first_run_hash": first_hash,
        "second_run_hash": second_hash,
        "exact_grouped_underlying_data_request": exact_data_request,
        "option_data_request": {
            "created": False,
            "reason": "No generated candidate reached TRADE_CANDIDATE.",
        },
        "exit_path_request": {
            "created": False,
            "reason": "No generated candidate reached ENTRY_RECORDED.",
        },
        "new_candidate_scorecard": _scorecard(generated_candidates),
        "family_scorecards": {
            family: _scorecard(
                [
                    candidate
                    for candidate in generated_candidates
                    if candidate["setup_family"] == family
                ]
            )
            for family in SETUP_FAMILIES
        },
        "raw_opportunities_inspected": len(rejected_opportunities),
        "rejected_raw_data_opportunities": rejected_opportunities,
        "existing_regression_result": {
            "day48_first_run": day48_first["combined_scorecard"],
            "day48_second_run": day48_second["combined_scorecard"],
            "day48_deterministic": (
                day48_first["deterministic_comparison"]["result"] == "PASS"
                and day48_second["deterministic_comparison"]["result"] == "PASS"
            ),
            "day50_evidence_backed_batch": day50_batch["scorecard"],
        },
        "underlying_setup_time_evidence_acquired_or_supplied": _acquired_without_problems(
            acquisition_manifest
        ),
        "underlying_setup_time_evidence_manifest": (
            _relative(
                EXTERNAL_UNDERLYING_DIR / day50_underlying.MANIFEST_FILENAME
            )
            if acquisition_manifest
            else None
        ),
        "concrete_completion_outcome": (
            "exact underlying setup-time evidence acquired and raw-data generator rerun"
            if _acquired_without_problems(acquisition_manifest)
            else (
                "one exact grouped, cost-checked raw-data request"
                if exact_data_request["cost_check"]["checked_cost"] != "NOT_AVAILABLE"
                else "one exact grouped raw-data request with cost NOT_AVAILABLE"
            )
        ),
        "databento_downloaded": _acquired_without_problems(acquisition_manifest),
        "schwab_authenticated": False,
        "broker_mutation_attempted": False,
        "proof_accepted": False,
        "profitability_claimed": False,
        "promotion_decision_made": False,
        "paper_eligible": False,
        "live_eligible": False,
        "next_task": {
            "filename": NEXT_TASK_FILENAME,
            "reason": (
                "Map the acquired one-minute SPY setup-time evidence through accepted "
                "SAFE-FAST replay/calculators to establish or reject exact setup-time "
                "row, trigger, invalidation, freshness, blocker/caution, session-boundary, "
                "and no-hindsight fields without changing frozen trading rules."
            ),
        },
    }


def write_generation_outputs(*, check_cost=True):
    document = build_generation_document(check_cost=check_cost)
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    MANIFEST_PATH.write_text(
        json.dumps(document["candidate_manifest"], indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return document


def build_raw_data_inventory():
    underlying_files = []
    for path in sorted(INCOMING_SOURCE_DIR.glob("*_source.csv")):
        underlying_files.append(_inventory_incoming_source(path))
    for path in sorted(EXTERNAL_UNDERLYING_DIR.glob("*.csv")):
        underlying_files.append(_inventory_databento_underlying_csv(path))

    option_manifests = [
        _inventory_manifest(path, "ignored_local_option_manifest")
        for path in sorted(EXTERNAL_OPTION_DIR.glob("*manifest*.json"))
    ]
    underlying_manifests = [
        _inventory_manifest(path, "ignored_local_underlying_manifest")
        for path in sorted(EXTERNAL_UNDERLYING_DIR.glob("*manifest*.json"))
    ]
    return {
        "inventory_status": "complete_local_tracked_and_ignored_inventory",
        "underlying_files": underlying_files,
        "underlying_manifests": underlying_manifests,
        "option_manifests": option_manifests,
        "ignored_local_raw_data_included": True,
        "local_raw_vendor_data_modified": False,
    }


def _inventory_incoming_source(path):
    rows = _read_csv_rows(path)
    timestamps = [row["timestamp"] for row in rows]
    symbol = rows[0]["symbol"] if rows else _symbol_from_name(path.name)
    timeframe = rows[0].get("timeframe") if rows else "UNKNOWN"
    complete = _chronological(timestamps) and all(
        row.get("symbol") == symbol
        and row.get("regular_session") == "true"
        and row.get("timezone") == "America/New_York"
        for row in rows
    )
    return {
        "path": _relative(path),
        "tracked_or_ignored": "tracked",
        "source": rows[0].get("source") if rows else "UNKNOWN",
        "dataset": "dxFeed via tastytrade dxLink",
        "schema": "first_real_historical_replay_v1_source_template",
        "symbol": symbol,
        "bar_or_event_resolution": timeframe,
        "timestamp_start": timestamps[0] if timestamps else None,
        "timestamp_end": timestamps[-1] if timestamps else None,
        "timezone": "America/New_York",
        "session_coverage": "regular_session_rth_only",
        "row_count": len(rows),
        "complete_chronological_rows": complete,
        "candidate_families_evaluable": list(SETUP_FAMILIES),
        "supports_exact_setup_trigger": False,
        "supports_invalidation": False,
        "supports_freshness_final_signal_state": False,
        "supports_session_boundary_evaluation": False,
        "limitation": (
            "1h_rth bars support context only; frozen setup trigger, invalidation, "
            "freshness/final-signal state, prior structure, blocker/caution, and "
            "session-boundary behavior require accepted finer setup-time replay rows."
        ),
    }


def _inventory_databento_underlying_csv(path):
    rows = _read_csv_rows(path)
    timestamps = [row["ts_event"] for row in rows]
    symbol = rows[0]["symbol"] if rows else _symbol_from_name(path.name)
    complete = _chronological(timestamps) and all(row.get("symbol") == symbol for row in rows)
    is_day50_setup_time = day50_underlying.REQUEST_ID in path.name
    schema = "ohlcv-1m" if is_day50_setup_time else "ohlcv-1h"
    resolution = "1m" if is_day50_setup_time else "1h"
    limitation = (
        "Exact one-minute underlying setup-time evidence is present for the authorized "
        "SPY session, but raw OHLCV rows alone do not name the accepted SAFE-FAST "
        "setup-time row, trigger, invalidation, freshness/final-signal state, "
        "blocker/caution state, session-boundary behavior, or no-hindsight boundary."
        if is_day50_setup_time
        else (
            "Downloaded one-hour OHLCV did not resolve accepted SAFE-FAST setup labels "
            "or setup-time trigger/invalidation/freshness decisions."
        )
    )
    return {
        "path": _relative(path),
        "tracked_or_ignored": "ignored_local_raw_data",
        "source": "Databento",
        "dataset": "DBEQ.BASIC",
        "schema": schema,
        "symbol": symbol,
        "bar_or_event_resolution": resolution,
        "timestamp_start": timestamps[0] if timestamps else None,
        "timestamp_end": timestamps[-1] if timestamps else None,
        "timezone": "UTC",
        "session_coverage": "downloaded_request_window",
        "row_count": len(rows),
        "complete_chronological_rows": complete,
        "candidate_families_evaluable": list(SETUP_FAMILIES),
        "supports_exact_underlying_setup_time_evidence": is_day50_setup_time,
        "supports_exact_setup_trigger": False,
        "supports_invalidation": False,
        "supports_freshness_final_signal_state": False,
        "supports_session_boundary_evaluation": False,
        "limitation": limitation,
    }


def _inventory_manifest(path, kind):
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        payload = {}
    return {
        "path": _relative(path),
        "tracked_or_ignored": "ignored_local_raw_data",
        "kind": kind,
        "schema_version": payload.get("schema_version") or payload.get("manifest_version"),
        "dataset": _manifest_dataset(payload),
        "request_count": len(payload.get("downloaded_requests", []))
        or len(payload.get("requests", [])),
        "actual_billed_cost": payload.get("actual_billed_cost", "NOT_AVAILABLE"),
        "checked_total": (
            payload.get("fresh_cost_check", {}).get("checked_total")
            or payload.get("checked_total")
            or "NOT_AVAILABLE"
        ),
    }


def _minimum_underlying_requirements():
    rows = []
    for family in SETUP_FAMILIES:
        rows.extend(
            [
                _requirement(family, "setup development", "underlying_ohlcv_1m"),
                _requirement(family, "setup decision row", "setup_time_row"),
                _requirement(family, "trigger", "trigger"),
                _requirement(family, "invalidation", "invalidation"),
                _requirement(
                    family,
                    "freshness or spent state",
                    "freshness_final_signal_state",
                ),
                _requirement(
                    family,
                    "final-signal state",
                    "freshness_final_signal_state",
                ),
                _requirement(
                    family,
                    "prior completed structure",
                    (
                        "prior_completed_shelf_break_spent_state"
                        if family == "Continuation"
                        else "freshness_final_signal_state"
                    ),
                ),
                _requirement(family, "blocker and caution state", "blocker_caution_review"),
                _requirement(
                    family,
                    "session-boundary behavior",
                    "session_boundary_behavior",
                ),
                _requirement(family, "no-hindsight boundary", "no_hindsight_boundary"),
            ]
        )
    return rows


def _requirement(family, decision, field_identifier):
    return {
        "setup_family": family,
        "decision": decision,
        "minimum_resolution": MINIMUM_UNDERLYING_RESOLUTION[family],
        "field_identifier": field_identifier,
        "primary_source": (
            "SAFE-FAST frozen local engine over source-backed underlying rows"
        ),
        "dataset_schema_or_calculator": _field_source(field_identifier),
        "blocking_scope": "blocks setup or trade eligibility when unavailable",
    }


def _field_source(field_identifier):
    mapping = {
        "underlying_ohlcv_1m": "Databento DBEQ.BASIC / ohlcv-1m / raw_symbol",
        "setup_time_row": "historical_signal_replay.signal_replay",
        "trigger": "setup_recognition.trigger_gate",
        "invalidation": "setup_recognition.invalidation_gate",
        "freshness_final_signal_state": "setup-family lifecycle calculators",
        "prior_completed_shelf_break_spent_state": "Continuation lifecycle/session-boundary gate",
        "blocker_caution_review": "historical_signal_replay.context_caution_calculator",
        "session_boundary_behavior": "stage_transition.session_boundary_gate",
        "no_hindsight_boundary": "historical_signal_replay.run_signal_replay",
    }
    return mapping[field_identifier]


def _inspect_raw_opportunities(inventory, prior_candidate_ids):
    opportunities = []
    for source in inventory["underlying_files"]:
        if not source["complete_chronological_rows"]:
            continue
        for family in SETUP_FAMILIES:
            opportunity_id = _opportunity_id(source, family)
            if opportunity_id in prior_candidate_ids:
                continue
            opportunities.append(_rejected_opportunity(source, family, opportunity_id))
    return opportunities


def _rejected_opportunity(source, family, opportunity_id):
    has_setup_time_evidence = source.get("supports_exact_underlying_setup_time_evidence")
    return {
        "raw_opportunity_id": opportunity_id,
        "source_path": source["path"],
        "setup_family": family,
        "symbol": source["symbol"],
        "timestamp_start": source["timestamp_start"],
        "timestamp_end": source["timestamp_end"],
        "candidate_generated": False,
        "exclusion_reason": (
            "setup_time_replay_mapping_not_established"
            if has_setup_time_evidence
            else "underlying_resolution_insufficient_for_exact_setup_trigger"
        ),
        "exact_failed_fields": [
            "setup_time_row",
            "trigger",
            "invalidation",
            "freshness_final_signal_state",
            "blocker_caution_review",
            "session_boundary_behavior",
            "no_hindsight_boundary",
        ],
        "required_source": (
            "SAFE-FAST frozen local replay/calculators over acquired Databento "
            "DBEQ.BASIC / ohlcv-1m / raw_symbol evidence"
            if has_setup_time_evidence
            else (
                "Databento DBEQ.BASIC / ohlcv-1m / raw_symbol plus "
                "SAFE-FAST frozen local replay/calculators"
            )
        ),
        "local_evidence_status": source["limitation"],
        "underlying_setup_time_evidence_supplied": bool(has_setup_time_evidence),
    }


def _build_exact_underlying_request(inventory):
    earliest = min(
        (
            item
            for item in inventory["underlying_files"]
            if item["tracked_or_ignored"] == "tracked"
            and item["complete_chronological_rows"]
            and item["symbol"] == "SPY"
        ),
        key=lambda item: item["timestamp_start"],
    )
    session_date = earliest["timestamp_start"][:10]
    request = {
        "created": True,
        "request_type": "underlying_setup_time_data",
        "request_id": "DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M",
        "symbols": ["SPY"],
        "windows": [
            {
                "symbol": "SPY",
                "start_timestamp": f"{session_date}T09:30:00-04:00",
                "end_timestamp": f"{session_date}T16:00:00-04:00",
                "timezone": "America/New_York",
                "subtotal_scope": "one earliest unused full RTH development session",
            }
        ],
        "dataset": "DBEQ.BASIC",
        "schema": "ohlcv-1m",
        "stype_in": "raw_symbol",
        "required_resolution": "1 minute RTH bars",
        "field_consumers": [
            "setup_time_row",
            "trigger",
            "invalidation",
            "freshness_final_signal_state",
            "prior_completed_structure",
            "blocker_caution_review",
            "session_boundary_behavior",
            "no_hindsight_boundary",
        ],
        "setup_family_decisions_resolved": list(SETUP_FAMILIES),
        "forbidden_scope": [
            "option data",
            "exit-path data",
            "macro data",
            "headline data",
            "IV/Greeks",
            "fills",
            "P&L",
            "live broker decisions",
        ],
        "downloaded": False,
    }
    return request


def _apply_acquisition_status(request, acquisition_manifest):
    if not acquisition_manifest:
        request["downloaded"] = False
        request["evidence_acquired_or_supplied"] = False
        request["actual_billed_cost"] = "NOT_AVAILABLE"
        return
    downloaded = acquisition_manifest.get("downloaded_request", {})
    request["downloaded"] = not acquisition_manifest.get("problems")
    request["evidence_acquired_or_supplied"] = request["downloaded"]
    request["download_manifest_path"] = _relative(
        EXTERNAL_UNDERLYING_DIR / day50_underlying.MANIFEST_FILENAME
    )
    request["downloaded_csv_path"] = downloaded.get("csv_path")
    request["downloaded_row_count"] = downloaded.get("row_count")
    request["actual_billed_cost"] = acquisition_manifest.get(
        "actual_billed_cost", "NOT_AVAILABLE"
    )
    if "cost_check" in request:
        request["cost_check"]["actual_billed_cost"] = request["actual_billed_cost"]
        request["cost_check"]["download_created"] = request["downloaded"]


def _acquired_without_problems(acquisition_manifest):
    return bool(acquisition_manifest) and not acquisition_manifest.get("problems")


def _check_databento_cost(request):
    api_key = os.environ.get("SAFE_FAST_DB_AUTH")
    if not api_key:
        return _not_available_cost("SAFE_FAST_DB_AUTH is not configured")
    try:
        import databento as db
    except Exception as exc:
        return _not_available_cost(f"databento package unavailable: {exc}")

    try:
        client = db.Historical(key=api_key)
        checked = []
        for window in request["windows"]:
            cost = Decimal(
                str(
                    client.metadata.get_cost(
                        dataset=request["dataset"],
                        start=window["start_timestamp"],
                        end=window["end_timestamp"],
                        symbols=window["symbol"],
                        schema=request["schema"],
                        stype_in=request["stype_in"],
                    )
                )
            )
            checked.append({**window, "checked_cost": str(cost)})
        total = sum(Decimal(item["checked_cost"]) for item in checked)
        return {
            "checked_cost": str(total),
            "checked_at_utc": _utc_now(),
            "credential_used": True,
            "download_created": False,
            "actual_billed_cost": "NOT_AVAILABLE",
            "subtotal_by_symbol_and_window": checked,
        }
    except Exception as exc:
        return _not_available_cost(f"Databento cost check failed: {exc}")


def _not_available_cost(reason):
    return {
        "checked_cost": "NOT_AVAILABLE",
        "checked_at_utc": _utc_now(),
        "credential_used": False,
        "download_created": False,
        "actual_billed_cost": "NOT_AVAILABLE",
        "reason": reason,
        "subtotal_by_symbol_and_window": [],
    }


def _build_manifest(
    *,
    inventory,
    prior_candidate_ids,
    rejected_opportunities,
    generated_candidates,
    exact_data_request,
    source_commit,
    run_timestamp,
):
    return {
        "manifest_version": MANIFEST_VERSION,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp,
        "candidate_count": len(generated_candidates),
        "candidate_records": generated_candidates,
        "prior_candidate_ids_excluded": sorted(prior_candidate_ids),
        "raw_data_inventory_summary": {
            "underlying_file_count": len(inventory["underlying_files"]),
            "underlying_manifest_count": len(inventory["underlying_manifests"]),
            "option_manifest_count": len(inventory["option_manifests"]),
        },
        "rejected_raw_data_opportunities": rejected_opportunities,
        "exact_grouped_underlying_data_request": exact_data_request,
    }


def _run_full_trade_funnel(candidates):
    records = []
    for candidate in candidates:
        records.append(
            {
                "candidate_identifier": candidate["candidate_identifier"],
                "setup_family": candidate["setup_family"],
                "symbol": candidate["symbol"],
                "highest_stage_reached": candidate["highest_stage_reached"],
                "first_stage_not_reached": candidate["first_stage_not_reached"],
                "exact_blocker": candidate["exact_blocker"],
                "final_classification": candidate["final_classification"],
            }
        )
    return {
        "candidate_records": records,
        "scorecard": _scorecard(records),
    }


def _scorecard(records):
    return {
        "candidates_generated": len(records),
        "setup_qualified_candidates": _stage_count(records, "SETUP_QUALIFIED"),
        "trade_candidates": _stage_count(records, "TRADE_CANDIDATE"),
        "selected_contracts": _stage_count(records, "CONTRACT_SELECTED"),
        "prices_accepted": _stage_count(records, "PRICE_ACCEPTABLE"),
        "eligible_entries": _stage_count(records, "ENTRY_ELIGIBLE"),
        "recorded_entries": _stage_count(records, "ENTRY_RECORDED"),
        "exits_evaluated": _stage_count(records, "EXIT_EVALUATED"),
        "valid_trades_captured": _classification_count(records, "VALID_TRADE_CAPTURED"),
        "true_no_trades": _classification_count(records, "TRUE_NO_TRADE"),
        "exact_data_required_cases": _classification_count(records, "EXACT_DATA_REQUIRED"),
        "missed_valid_trades": _classification_count(records, "MISSED_VALID_TRADE"),
        "invalid_trades_allowed": _classification_count(records, "INVALID_TRADE_ALLOWED"),
        "unresolved_cases": _classification_count(records, "UNRESOLVED"),
        "winners": sum(1 for record in records if record.get("winner_or_loser") == "winner"),
        "losers": sum(1 for record in records if record.get("winner_or_loser") == "loser"),
        "first_blockers_by_stage": _first_blockers(records),
    }


def _stage_count(records, stage):
    return sum(
        1
        for record in records
        if stage in record.get("funnel_stage_path", [])
        or record.get("highest_stage_reached") == stage
    )


def _classification_count(records, classification):
    return sum(1 for record in records if record.get("final_classification") == classification)


def _first_blockers(records):
    grouped = {}
    for record in records:
        stage = record.get("first_stage_not_reached") or "NONE"
        grouped[stage] = grouped.get(stage, 0) + 1
    return grouped


def _prior_candidate_identifiers():
    batch = day50_evidence_backed_positive_entry_testing_batch.build_batch_document(
        source_commit="inventory",
        run_timestamp="2026-06-21T00:00:00Z",
    )
    return {record["candidate_identifier"] for record in batch["candidate_records"]}


def _stable_generation_payload(manifest, funnel):
    return {
        "candidate_records": manifest["candidate_records"],
        "rejected_raw_data_opportunities": manifest["rejected_raw_data_opportunities"],
        "funnel": funnel,
    }


def _opportunity_id(source, family):
    family_part = family.upper().replace(" ", "-")
    return (
        f"DAY50-RAW-{source['symbol']}-{family_part}-"
        f"{source['timestamp_start']}-{source['timestamp_end']}"
    )


def _read_csv_rows(path):
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _chronological(timestamps):
    return timestamps == sorted(timestamps)


def _symbol_from_name(name):
    for symbol in ("SPY", "QQQ", "IWM", "GLD"):
        if symbol in name:
            return symbol
    return "UNKNOWN"


def _manifest_dataset(payload):
    if "authorized_scope" in payload:
        return payload["authorized_scope"].get("dataset")
    if "dataset" in payload:
        return payload.get("dataset")
    requests = payload.get("downloaded_requests") or payload.get("requests") or []
    if requests:
        return requests[0].get("dataset")
    return None


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
    doc = write_generation_outputs(check_cost=True)
    scorecard = doc["new_candidate_scorecard"]
    cost = doc["exact_grouped_underlying_data_request"]["cost_check"]["checked_cost"]
    print(
        "wrote day50 raw-data positive-entry generation: "
        f"{doc['raw_opportunities_inspected']} raw opportunities inspected, "
        f"{scorecard['setup_qualified_candidates']} setup-qualified, "
        f"{scorecard['trade_candidates']} trade candidates, "
        f"{scorecard['selected_contracts']} selected contracts, "
        f"{scorecard['eligible_entries']} eligible entries, "
        f"{scorecard['recorded_entries']} recorded entries, "
        f"checked cost {cost}"
    )
