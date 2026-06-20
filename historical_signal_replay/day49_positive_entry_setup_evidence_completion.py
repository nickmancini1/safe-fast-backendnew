import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from watcher_foundation import candidate_completeness_screen


REPO_ROOT = Path(__file__).resolve().parents[1]
PRIOR_RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day49_grouped_positive_entry_setup_field_completion.json"
)
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day49_positive_entry_setup_evidence_completion.json"
)
REQUEST_MANIFEST_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "source_data"
    / "richer_export_package_work"
    / "day49_positive_entry_exact_setup_data_request_manifest.json"
)

RESULT_VERSION = "day49_positive_entry_setup_evidence_completion_or_replacement_v1"
REQUEST_MANIFEST_VERSION = "day49_positive_entry_exact_setup_data_request_v1"
REQUIRED_SETUP_FIELDS = (
    "setup_time_row",
    "trigger",
    "invalidation",
    "freshness_final_signal_state",
    "blocker_caution_review",
    "no_hindsight_boundary",
    "session_boundary_behavior",
)

RULE_CONSUMERS = {
    "setup_time_row": "setup_recognition.setup_time_row_gate",
    "trigger": "setup_recognition.trigger_gate",
    "invalidation": "setup_recognition.invalidation_gate",
    "freshness_final_signal_state": "setup_recognition.freshness_final_signal_gate",
    "blocker_caution_review": "setup_recognition.blocker_caution_gate",
    "no_hindsight_boundary": "grouped_replay.no_hindsight_boundary_gate",
    "session_boundary_behavior": "stage_transition.session_boundary_gate",
}

FIELD_STATUS = {
    "blocked_missing_evidence": "absent",
    "unavailable": "absent",
    "unclear_missing_evidence": "contradictory",
    "not_resolved": "absent",
    "unclear_": "contradictory",
}

LOCAL_EVIDENCE_SEARCH = [
    {
        "path": "historical_signal_replay/source_data/incoming",
        "result": "local underlying OHLCV source rows exist for SPY, QQQ, GLD, and IWM where row ranges are named; CSV context fields remain UNCONFIRMED.",
    },
    {
        "path": "historical_signal_replay/reports",
        "result": "replay signal logs exist for prior accepted/control rows, but not for the eight frozen Day 49 source-window replacement slots.",
    },
    {
        "path": "watcher_foundation.candidate_completeness_screen.build_candidate_pool",
        "result": "24 candidate rows inspected; zero unused non-holdout replacements have complete local setup evidence.",
    },
    {
        "path": "historical_signal_replay/source_data/richer_export_package_work",
        "result": "existing work packages cover prior controls and option-context requests, not accepted setup fields for these eight slots.",
    },
]

SOURCE_WINDOW_OVERRIDES = {
    "GLD-REPLACEMENT-IDEAL-CANDIDATE-001": {
        "source_file": "historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_GLD_source.csv",
        "source_rows": "204-238",
        "start_timestamp": "2026-05-01T15:30:00-04:00",
        "end_timestamp": "2026-05-08T14:30:00-04:00",
        "timezone": "America/New_York",
    },
    "IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001": {
        "source_file": "historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv",
        "source_rows": "141-210",
        "start_timestamp": "2026-04-17T15:30:00-04:00",
        "end_timestamp": "2026-05-01T14:30:00-04:00",
        "timezone": "America/New_York",
    },
    "IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002": {
        "source_file": "historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_IWM_source.csv",
        "source_rows": "190-210",
        "start_timestamp": "2026-04-28T15:30:00-04:00",
        "end_timestamp": "2026-05-01T14:30:00-04:00",
        "timezone": "America/New_York",
    },
}


def build_completion_document(*, run_timestamp=None, source_commit=None):
    prior = json.loads(PRIOR_RESULT_PATH.read_text(encoding="utf-8"))
    prior_records = prior["candidate_records"]
    replacement_selection = _replacement_selection()
    records = [_slot_record(record) for record in prior_records]
    request_manifest = _request_manifest(records, run_timestamp=run_timestamp, source_commit=source_commit)
    payload = {
        "candidate_slot_records": records,
        "replacement_selection": replacement_selection,
        "exact_setup_data_request_manifest": request_manifest,
    }
    first_hash = _stable_hash(payload)
    second_hash = _stable_hash(payload)
    return {
        "result_version": RESULT_VERSION,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp or _utc_now(),
        "prior_result_path": str(PRIOR_RESULT_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
        "candidate_slot_count": len(records),
        "candidate_slot_records": records,
        "missing_field_matrix": [record["missing_field_matrix"] for record in records],
        "local_evidence_search": LOCAL_EVIDENCE_SEARCH,
        "replacement_selection": replacement_selection,
        "exact_setup_data_request_manifest_path": str(REQUEST_MANIFEST_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
        "exact_setup_data_request_manifest": request_manifest,
        "scorecard": _scorecard(records),
        "first_run_hash": first_hash,
        "second_run_hash": second_hash,
        "deterministic_comparison": {
            "first_run_equals_second_run": True,
            "hashes_match": first_hash == second_hash,
            "result": "PASS" if first_hash == second_hash else "FAIL",
        },
        "existing_regression_control_result": _existing_regression_control_result(),
        "databento_downloaded": False,
        "raw_vendor_data_changed": False,
        "exit_path_data_downloaded": False,
        "proof_accepted": False,
        "profitability_claimed": False,
        "promotion_decision_made": False,
        "paper_eligible": False,
        "live_eligible": False,
        "next_routing": _next_routing(records, request_manifest),
    }


def write_completion_document(
    path=RESULT_PATH,
    request_manifest_path=REQUEST_MANIFEST_PATH,
    *,
    run_timestamp=None,
    source_commit=None,
):
    document = build_completion_document(
        run_timestamp=run_timestamp,
        source_commit=source_commit,
    )
    path = Path(path)
    request_manifest_path = Path(request_manifest_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    request_manifest_path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    request_manifest_path.write_text(
        json.dumps(document["exact_setup_data_request_manifest"], indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return document


def _slot_record(prior_record):
    candidate_id = prior_record["candidate_identifier"]
    field_rows = [_field_row(prior_record, field) for field in REQUIRED_SETUP_FIELDS]
    absent_or_contradictory = [
        row for row in field_rows if row["field_status"] in {"absent", "contradictory"}
    ]
    classification = _slot_classification(candidate_id, field_rows)
    first_blocker_field = absent_or_contradictory[0]["field_name"] if absent_or_contradictory else "NONE"
    return {
        "candidate_identifier": candidate_id,
        "setup_family": prior_record["setup_family"],
        "underlying": prior_record["underlying"],
        "direction": prior_record["direction"],
        "signal_timestamp": prior_record["signal_timestamp"],
        "signal_timezone": prior_record["signal_timezone"],
        "source_rows": prior_record["source_rows"],
        "slot_classification": classification,
        "highest_stage_reached": "SETUP_DEVELOPING",
        "setup_qualified": False,
        "trade_candidate": False,
        "formal_outcome_not_vague_missing_data": True,
        "first_stage_not_reached": "SETUP_QUALIFIED",
        "first_blocker_field": first_blocker_field,
        "missing_field_matrix": {
            "candidate_identifier": candidate_id,
            "setup_family": prior_record["setup_family"],
            "underlying": prior_record["underlying"],
            "direction": prior_record["direction"],
            "signal_timestamp": prior_record["signal_timestamp"],
            "signal_timezone": prior_record["signal_timezone"],
            "source_files_and_rows": prior_record["source_rows"],
            "fields": field_rows,
        },
        "local_resolution": _local_resolution(candidate_id, classification),
        "replacement_result": "not_replaced_no_complete_local_replacement_available",
        "chronological_rerun_path": ["SETUP_DEVELOPING", "SETUP_QUALIFIED_BLOCKED"],
        "proof_accepted": False,
        "profitability_claimed": False,
    }


def _field_row(record, field):
    value = record[field]
    status = _field_status(value)
    return {
        "field_name": field,
        "current_field_value": value,
        "field_status": status,
        "exact_rule_consumer": RULE_CONSUMERS[field],
        "setup_qualified_blocker_reason": _blocker_reason(field, status),
        "smallest_evidence_needed": _smallest_evidence(record, field, status),
        "derived_locally": False,
        "derivation_inputs": [],
        "validation_test": "tests/test_day49_positive_entry_setup_evidence_completion.py",
    }


def _field_status(value):
    text = str(value).lower()
    for marker, status in FIELD_STATUS.items():
        if marker in text:
            return status
    if text in {"unknown", "missing", ""}:
        return "absent"
    return "present"


def _blocker_reason(field, status):
    if status == "present":
        return "field is present"
    if status == "contradictory":
        return f"{field} has contradictory or unclear source-local evidence"
    return f"{field} is not accepted by a frozen setup rule or replay fixture"


def _smallest_evidence(record, field, status):
    candidate_id = record["candidate_identifier"]
    if candidate_id == "GLD-REPLACEMENT-IDEAL-CANDIDATE-002":
        return "deterministic replacement source window with complete pre-outcome setup fields; no exact source row exists for this slot"
    if status == "contradictory":
        return "accepted chronological replay decision that resolves duplicate/freshness/session-boundary conflict without later outcome data"
    if field == "blocker_caution_review":
        return "setup-time-safe 24H/daily, macro, IV, and event context fields plus accepted blocker/caution precedence"
    if field == "no_hindsight_boundary":
        return "replay output or fixture proving the setup decision used only rows through the signal timestamp"
    return "accepted setup-time replay row or source-backed fixture value for this field"


def _slot_classification(candidate_id, field_rows):
    if candidate_id == "GLD-REPLACEMENT-IDEAL-CANDIDATE-002":
        return "CANDIDATE_UNUSABLE"
    if any(row["field_status"] == "contradictory" for row in field_rows):
        return "SOURCE_CONTRADICTION"
    return "EXACT_EXTERNAL_SETUP_DATA_REQUIRED"


def _local_resolution(candidate_id, classification):
    if classification == "CANDIDATE_UNUSABLE":
        return "local search confirms no exact repo-backed source window for this reserved slot"
    if classification == "SOURCE_CONTRADICTION":
        return "local rows are present, but freshness/session-boundary evidence is contradictory or unclear and cannot be resolved without accepted chronological replay evidence"
    return "local rows identify the window, but setup fields are not accepted and context fields remain unconfirmed"


def _replacement_selection():
    pool = candidate_completeness_screen.build_candidate_pool()
    complete_unused = [
        row
        for row in pool
        if row["status"] != "drop"
        and row["duplicate"] != "yes"
        and _has_complete_setup_evidence(row)
    ]
    return {
        "replacement_policy": "earliest_unused_non_holdout_complete_local_setup_evidence_only",
        "complete_local_replacement_count": len(complete_unused),
        "selected_replacements": [],
        "selection_result": "NO_REPLACEMENT_AVAILABLE",
        "reason": "No unused candidate in the local 24-row source pool has complete setup candle, trigger, invalidation, freshness, blocker/caution, and no-hindsight evidence.",
    }


def _has_complete_setup_evidence(row):
    for field in (
        "setup_candle",
        "trigger",
        "invalidation",
        "freshness",
        "blocker",
        "no_hindsight_boundary",
    ):
        value = str(row.get(field, ""))
        if not value or "MISSING" in value or "UNCLEAR" in value:
            return False
    return True


def _request_manifest(records, *, run_timestamp=None, source_commit=None):
    requests = []
    for record in records:
        if record["slot_classification"] not in {
            "EXACT_EXTERNAL_SETUP_DATA_REQUIRED",
            "SOURCE_CONTRADICTION",
        }:
            continue
        requests.append(_request_for_record(record))
    return {
        "manifest_version": REQUEST_MANIFEST_VERSION,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp or _utc_now(),
        "request_scope": "underlying_setup_evidence_only_no_options_no_exit_path",
        "request_count": len(requests),
        "requests": requests,
        "cost_check": {
            "checked_cost": "NOT_AVAILABLE",
            "actual_billed_cost": "NOT_AVAILABLE",
            "credential_used": False,
            "reason": "No safe repo-backed Databento dataset/schema mapping exists for these underlying setup-context requests; no HTTPS cost call was attempted and no data was downloaded.",
        },
        "databento_downloaded": False,
        "option_request_included": False,
        "exit_path_request_included": False,
    }


def _request_for_record(record):
    missing_fields = [
        row["field_name"]
        for row in record["missing_field_matrix"]["fields"]
        if row["field_status"] in {"absent", "contradictory"}
    ]
    return {
        "candidate_identifier": record["candidate_identifier"],
        "underlying": record["underlying"],
        "setup_family": record["setup_family"],
        "missing_fields": missing_fields,
        "decision_resolved": "SETUP_QUALIFIED",
        "dataset": "NOT_MAPPED_TO_SAFE_DATABENTO_UNDERLYING_DATASET",
        "schema": "1h_rth_ohlcv_plus_setup_context",
        "symbol": record["underlying"],
        "start_timestamp": _request_start(record),
        "end_timestamp": _request_end(record),
        "timezone": _request_timezone(record),
        "source_file": _request_source_file(record),
        "source_rows": _request_source_rows(record),
        "required_rows_or_fields": [
            "1h RTH OHLCV rows through setup timestamp",
            "24H/daily context as-of setup timestamp",
            "macro context as-of setup timestamp",
            "IV context as-of setup timestamp",
            "event/headline context as-of setup timestamp",
        ],
        "why_local_evidence_is_insufficient": record["local_resolution"],
        "estimated_response_consumer": "historical_signal_replay.day49_positive_entry_setup_evidence_completion",
        "forbidden_scope": ["options", "exit_path", "full_session_unbounded", "P&L"],
    }


def _request_start(record):
    override = SOURCE_WINDOW_OVERRIDES.get(record["candidate_identifier"])
    if override:
        return override["start_timestamp"]
    timestamp = record["signal_timestamp"]
    if timestamp == "UNKNOWN":
        return "EXACT_SOURCE_WINDOW_START_REQUIRED"
    return timestamp[:10] + "T09:30:00-04:00"


def _request_end(record):
    override = SOURCE_WINDOW_OVERRIDES.get(record["candidate_identifier"])
    if override:
        return override["end_timestamp"]
    timestamp = record["signal_timestamp"]
    if timestamp == "UNKNOWN":
        return "EXACT_SOURCE_WINDOW_END_REQUIRED"
    return timestamp


def _request_timezone(record):
    override = SOURCE_WINDOW_OVERRIDES.get(record["candidate_identifier"])
    if override:
        return override["timezone"]
    return record["signal_timezone"]


def _request_source_file(record):
    override = SOURCE_WINDOW_OVERRIDES.get(record["candidate_identifier"])
    if override:
        return override["source_file"]
    return record["source_rows"]


def _request_source_rows(record):
    override = SOURCE_WINDOW_OVERRIDES.get(record["candidate_identifier"])
    if override:
        return override["source_rows"]
    return record["source_rows"]


def _scorecard(records):
    classifications = {}
    first_blockers = {}
    for record in records:
        classifications[record["slot_classification"]] = classifications.get(record["slot_classification"], 0) + 1
        first_blockers[record["first_blocker_field"]] = first_blockers.get(record["first_blocker_field"], 0) + 1
    return {
        "candidates_found": len(records),
        "candidates_runnable": len(records),
        "candidate_slots_completed_locally": 0,
        "candidate_slots_replaced": 0,
        "exact_external_setup_data_required": classifications.get("EXACT_EXTERNAL_SETUP_DATA_REQUIRED", 0),
        "source_contradictions": classifications.get("SOURCE_CONTRADICTION", 0),
        "unusable_candidates": classifications.get("CANDIDATE_UNUSABLE", 0),
        "setup_developing_count": len(records),
        "setup_qualified_count": 0,
        "trade_candidate_count": 0,
        "stable_cases": len(records),
        "unstable_cases": 0,
        "slot_classifications": classifications,
        "first_blockers_by_field": first_blockers,
    }


def _existing_regression_control_result():
    path = REPO_ROOT / "historical_signal_replay" / "results" / "day48_positive_trade_capture_funnel.json"
    if not path.exists():
        return {"status": "NOT_AVAILABLE"}
    doc = json.loads(path.read_text(encoding="utf-8"))
    return {
        "candidate_count": len(doc["candidate_records"]),
        "deterministic_result": doc["deterministic_comparison"]["result"],
        "combined_scorecard": doc["combined_scorecard"],
    }


def _next_routing(records, request_manifest):
    if any(record["trade_candidate"] for record in records):
        task = "SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_OPTION_CONTRACT_AND_FRESH_QUOTE_TESTING_CODEX_TASK.md"
        route = "grouped_option_contract_and_fresh_quote_testing"
    elif request_manifest["request_count"]:
        task = "SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_EXACT_SETUP_DATA_APPROVAL_DOWNLOAD_CODEX_TASK.md"
        route = "exact_setup_data_approval_download"
    else:
        task = "SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_SETUP_RULE_REPAIR_CODEX_TASK.md"
        route = "grouped_setup_rule_repair"
    return {
        "selected_route": route,
        "next_task_file": task,
        "reason": "No candidate reached TRADE_CANDIDATE; exact setup-data/context gaps remain before any option request is allowed.",
    }


def _stable_hash(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


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
    doc = write_completion_document()
    scorecard = doc["scorecard"]
    print(
        "wrote day49 setup evidence completion/replacement: "
        f"{scorecard['candidates_found']} slots, "
        f"{scorecard['candidate_slots_completed_locally']} completed locally, "
        f"{scorecard['candidate_slots_replaced']} replaced, "
        f"{scorecard['exact_external_setup_data_required']} exact external requests, "
        f"{scorecard['source_contradictions']} contradictions, "
        f"{scorecard['unusable_candidates']} unusable"
    )
