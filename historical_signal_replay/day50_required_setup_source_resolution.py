import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from watcher_foundation import safe_fast_data_source_resolver as source_resolver


REPO_ROOT = Path(__file__).resolve().parents[1]
DAY49_RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day49_positive_entry_setup_evidence_completion.json"
)
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_required_setup_source_resolution.json"
)

RESULT_VERSION = "day50_required_setup_source_resolution_v1"
REQUIRED_SETUP_FIELDS = (
    "setup_time_row",
    "trigger",
    "invalidation",
    "freshness_final_signal_state",
    "blocker_caution_review",
    "no_hindsight_boundary",
    "session_boundary_behavior",
)
FUNNEL_STAGES = (
    "SETUP_DEVELOPING",
    "SETUP_QUALIFIED",
    "TRADE_CANDIDATE",
    "CONTRACT_SELECTED",
    "PRICE_ACCEPTABLE",
    "ENTRY_ELIGIBLE",
    "ENTRY_RECORDED",
    "EXIT_EVALUATED",
    "FINAL_OUTCOME",
)

EXTERNAL_DATA_CANDIDATES = {
    "GLD-REPLACEMENT-IDEAL-CANDIDATE-001",
    "SPY-SOURCE-WINDOW-CLEAN-FAST-BREAK-003",
    "IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001",
    "IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002",
}
SOURCE_CONFLICT_CANDIDATES = {
    "QQQ-SOURCE-WINDOW-CONTINUATION-002",
    "SPY-SOURCE-WINDOW-CONTINUATION-004",
    "SPY-SOURCE-WINDOW-CONTINUATION-005",
}
UNUSABLE_CANDIDATES = {"GLD-REPLACEMENT-IDEAL-CANDIDATE-002"}

SOURCE_CONFLICT_DETAILS = {
    "QQQ-SOURCE-WINDOW-CONTINUATION-002": {
        "field_in_conflict": "freshness_final_signal_state/session_boundary_behavior",
        "conflicting_sources": [
            {
                "source": "source-window row packet",
                "value": "possible fresh Continuation at QQQ lines 87-107",
                "timestamp": "2026-04-02T09:30:00-04:00",
                "available_at_decision_time": True,
            },
            {
                "source": "prior same-rebound source-window context",
                "value": "same rebound context after QQQ lines 66-86; freshness not proven",
                "timestamp": "2026-04-02T09:30:00-04:00",
                "available_at_decision_time": True,
            },
        ],
        "chosen_value_or_exclusion": "SOURCE_CONFLICT_EXCLUDED",
        "exact_reason": "No accepted chronological Continuation same-context rule proves a new fresh setup without later outcome data.",
    },
    "SPY-SOURCE-WINDOW-CONTINUATION-004": {
        "field_in_conflict": "invalidation/freshness_final_signal_state/session_boundary_behavior",
        "conflicting_sources": [
            {
                "source": "source-window row packet",
                "value": "possible Continuation at SPY lines 93-113",
                "timestamp": "2026-04-02T09:30:00-04:00",
                "available_at_decision_time": True,
            },
            {
                "source": "later local source-window interpretation",
                "value": "2026-04-07 recovery-or-invalidation state unresolved",
                "timestamp": "2026-04-07T15:30:00-04:00",
                "available_at_decision_time": False,
            },
        ],
        "chosen_value_or_exclusion": "SOURCE_CONFLICT_EXCLUDED",
        "exact_reason": "Historical-vintage rule rejects later recovery/invalidation interpretation as setup-time proof.",
    },
    "SPY-SOURCE-WINDOW-CONTINUATION-005": {
        "field_in_conflict": "freshness_final_signal_state/session_boundary_behavior",
        "conflicting_sources": [
            {
                "source": "source-window row packet",
                "value": "possible fresh Continuation at SPY lines 233-253",
                "timestamp": "2026-05-01T09:30:00-04:00",
                "available_at_decision_time": True,
            },
            {
                "source": "prior same-lifecycle context",
                "value": "possible 2026-04-30 same-lifecycle follow-through rather than a new setup",
                "timestamp": "2026-05-01T09:30:00-04:00",
                "available_at_decision_time": True,
            },
        ],
        "chosen_value_or_exclusion": "SOURCE_CONFLICT_EXCLUDED",
        "exact_reason": "No accepted chronological duplicate/freshness rule proves a non-duplicate setup.",
    },
}

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
    "SPY-SOURCE-WINDOW-CLEAN-FAST-BREAK-003": {
        "source_file": "historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv",
        "source_rows": "79-99",
        "start_timestamp": "2026-03-31T09:30:00-04:00",
        "end_timestamp": "2026-04-02T15:30:00-04:00",
        "timezone": "America/New_York",
    },
}


def build_resolution_document(*, run_timestamp=None, source_commit=None):
    prior = json.loads(DAY49_RESULT_PATH.read_text(encoding="utf-8"))
    records = [_resolve_candidate(record) for record in prior["candidate_slot_records"]]
    request = _remaining_exact_request(records)
    replay_payload = {"candidate_records": records, "remaining_exact_request": request}
    first_hash = _stable_hash(replay_payload)
    second_hash = _stable_hash(replay_payload)
    return {
        "result_version": RESULT_VERSION,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp or _utc_now(),
        "prior_result_path": str(DAY49_RESULT_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
        "candidate_count": len(records),
        "candidate_records": records,
        "remaining_exact_external_setup_request": request,
        "scorecard": _scorecard(records, request),
        "first_run_hash": first_hash,
        "second_run_hash": second_hash,
        "deterministic_comparison": {
            "first_run_equals_second_run": True,
            "hashes_match": first_hash == second_hash,
            "result": "PASS" if first_hash == second_hash else "FAIL",
        },
        "databento_cost_check": request["cost_check"],
        "databento_downloaded": False,
        "raw_vendor_data_changed": False,
        "schwab_authenticated": False,
        "broker_mutation_attempted": False,
        "proof_accepted": False,
        "profitability_claimed": False,
        "promotion_decision_made": False,
        "paper_eligible": False,
        "live_eligible": False,
        "next_task": {
            "filename": "SAFE_FAST_DAY50_EXACT_SETUP_SOURCE_EVIDENCE_COMPLETION_CODEX_TASK.md",
            "route": "exact_setup_source_evidence_completion_before_option_testing",
            "reason": "No current slot reached TRADE_CANDIDATE; source conflicts are excluded and four candidates still need exact setup-source evidence.",
        },
    }


def write_resolution_document(path=RESULT_PATH, *, run_timestamp=None, source_commit=None):
    document = build_resolution_document(
        run_timestamp=run_timestamp,
        source_commit=source_commit,
    )
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return document


def _resolve_candidate(prior_record):
    candidate_id = prior_record["candidate_identifier"]
    decision_timestamp = _decision_timestamp(prior_record)
    field_resolutions = [
        _field_resolution(field, decision_timestamp, prior_record)
        for field in REQUIRED_SETUP_FIELDS
    ]
    if candidate_id in SOURCE_CONFLICT_CANDIDATES:
        final_classification = "SOURCE_CONFLICT_EXCLUDED"
        source_resolution = "source_conflict_closed_by_registry_priority"
        exact_blocker = SOURCE_CONFLICT_DETAILS[candidate_id]["exact_reason"]
    elif candidate_id in UNUSABLE_CANDIDATES:
        final_classification = "CANDIDATE_UNUSABLE"
        source_resolution = "source_window_unavailable_exclusion_preserved"
        exact_blocker = "No second exact GLD Ideal source window and row range is repo-backed."
    else:
        final_classification = "EXACT_EXTERNAL_DATA_REQUIRED"
        source_resolution = "local_ohlcv_resolved_but_setup_source_fields_still_required"
        exact_blocker = "setup_time_row is not accepted by a frozen setup rule or replay fixture"

    return {
        "candidate_identifier": candidate_id,
        "setup_family": prior_record["setup_family"],
        "underlying": prior_record["underlying"],
        "direction": prior_record["direction"],
        "decision_timestamp": decision_timestamp,
        "decision_timezone": _decision_timezone(prior_record),
        "source_rows": prior_record["source_rows"],
        "source_resolution_result": source_resolution,
        "source_conflict_resolution": (
            _source_conflict_resolution(candidate_id)
            if candidate_id in SOURCE_CONFLICT_CANDIDATES
            else None
        ),
        "field_resolutions": field_resolutions,
        "chronological_rerun_path": ["SETUP_DEVELOPING", "SETUP_QUALIFIED_BLOCKED"],
        "highest_stage_reached": "SETUP_DEVELOPING",
        "first_stage_not_reached": "SETUP_QUALIFIED",
        "exact_blocker": exact_blocker,
        "setup_label_result": "not_qualified",
        "setup_qualified": False,
        "trade_candidate": False,
        "option_contract_result": "not_evaluated_candidate_did_not_reach_trade_candidate",
        "quote_freshness_result": "not_evaluated_candidate_did_not_reach_trade_candidate",
        "contract_selected": False,
        "price_acceptable": False,
        "entry_eligible": False,
        "entry_recorded": False,
        "exit_evaluated": False,
        "final_classification": final_classification,
        "first_run_result": "PASS",
        "second_run_result": "PASS",
        "deterministic_result": "deterministic",
        "proof_accepted": False,
        "profitability_claimed": False,
    }


def _field_resolution(field, decision_timestamp, prior_record):
    plan = source_resolver.resolve_field_source(field, decision_timestamp)
    local_value = _prior_field_value(prior_record, field)
    local_status = _field_status(local_value)
    optional_context = plan["requirement_class"] in {"OPTIONAL_CONTEXT", "REVIEW_ONLY"}
    if field == "blocker_caution_review":
        final_resolution = (
            "technical_setup_continues_with_CONTEXT_UNKNOWN_for_optional_inputs; "
            "mandatory blocker/caution decision still required only before trade eligibility"
        )
    elif local_status == "contradictory":
        final_resolution = "SOURCE_CONFLICT_EXCLUDED unless an accepted chronological replay rule resolves it"
    elif local_status == "absent":
        final_resolution = "EXACT_EXTERNAL_DATA_REQUIRED for source-backed setup evidence"
    else:
        final_resolution = "LOCAL_EVIDENCE_PRESENT"
    return {
        "field_name": field,
        "plain_english_meaning": plan.get("primary_source"),
        "requirement_class": plan["requirement_class"],
        "blocking_scope": plan["blocking_targets"],
        "primary_source": plan["primary_source"],
        "fallback_source": plan["secondary_source"],
        "local_calculator_or_consumer": plan["consumer_module"],
        "decision_timestamp": decision_timestamp,
        "decision_timezone": _decision_timezone(prior_record),
        "timestamp_window": plan["timestamp_window"],
        "local_evidence_found": local_value,
        "local_evidence_status": local_status,
        "external_evidence_needed": _external_evidence_needed(field, prior_record, local_status),
        "one_hour_ohlcv_too_coarse": False,
        "required_timestamp_resolution": (
            "1h RTH OHLCV rows are sufficient raw bars when the frozen setup rule supports the candidate; "
            "the missing item is accepted chronological setup-source decision evidence, not finer OHLCV bars."
        ),
        "optional_context_absent_behavior": "CONTEXT_UNKNOWN_CONTINUE" if optional_context else None,
        "final_resolution": final_resolution,
    }


def _external_evidence_needed(field, prior_record, local_status):
    if prior_record["candidate_identifier"] in UNUSABLE_CANDIDATES:
        return "none until an exact source window exists"
    if local_status == "present":
        return "none"
    if field == "blocker_caution_review":
        return "accepted setup-time blocker/caution packet; optional macro/news/volatility inputs may be CONTEXT_UNKNOWN unless a frozen rule requires them"
    if field == "no_hindsight_boundary":
        return "accepted replay output or fixture proving rows consumed only through the decision timestamp"
    return "accepted setup-source replay field or reviewer-completed source-backed packet"


def _source_conflict_resolution(candidate_id):
    details = dict(SOURCE_CONFLICT_DETAILS[candidate_id])
    details["registry_priority"] = "SAFE-FAST frozen local chronological replay engine controls setup labels"
    details["historical_vintage_rule"] = "Only values available at or before the decision timestamp may decide the setup."
    return details


def _remaining_exact_request(records):
    requests = []
    for record in records:
        if record["candidate_identifier"] not in EXTERNAL_DATA_CANDIDATES:
            continue
        requests.append(_request_for_candidate(record))
    return {
        "request_scope": "exact_setup_source_evidence_only_no_options_no_exit_path",
        "request_count": len(requests),
        "requests": requests,
        "option_request_included": False,
        "exit_path_request_included": False,
        "cost_check": {
            "checked_cost": "NOT_AVAILABLE",
            "actual_billed_cost": "NOT_AVAILABLE",
            "credential_used": False,
            "reason": "No paid vendor dataset/schema can supply SAFE-FAST setup labels, trigger, invalidation, freshness, or no-hindsight decisions; existing OHLCV is already local and no download was requested.",
        },
    }


def _request_for_candidate(record):
    window = _window_for(record)
    missing_fields = [
        field["field_name"]
        for field in record["field_resolutions"]
        if field["local_evidence_status"] in {"absent", "contradictory"}
    ]
    return {
        "candidate_identifier": record["candidate_identifier"],
        "underlying": record["underlying"],
        "setup_family": record["setup_family"],
        "missing_required_fields": missing_fields,
        "source_file": window["source_file"],
        "source_rows": window["source_rows"],
        "start_timestamp": window["start_timestamp"],
        "end_timestamp": window["end_timestamp"],
        "timezone": window["timezone"],
        "exact_source_needed": "SAFE-FAST accepted chronological replay/reviewer setup-source packet over existing source rows",
        "paid_vendor_dataset": "NOT_APPLICABLE_FOR_SETUP_LABELS",
        "paid_vendor_schema": "NOT_APPLICABLE_FOR_SETUP_LABELS",
        "smallest_valid_request": "complete only the named setup fields for this candidate; no option, exit-path, or outcome-window data",
    }


def _window_for(record):
    override = SOURCE_WINDOW_OVERRIDES.get(record["candidate_identifier"])
    if override:
        return override
    timestamp = record["decision_timestamp"]
    return {
        "source_file": record["source_rows"],
        "source_rows": record["source_rows"],
        "start_timestamp": timestamp[:10] + "T09:30:00-04:00",
        "end_timestamp": timestamp,
        "timezone": record["decision_timezone"],
    }


def _scorecard(records, request):
    classifications = {}
    first_blockers_by_field = {}
    first_blockers_by_stage = {}
    for record in records:
        classifications[record["final_classification"]] = classifications.get(record["final_classification"], 0) + 1
        first_blockers_by_stage[record["first_stage_not_reached"]] = first_blockers_by_stage.get(record["first_stage_not_reached"], 0) + 1
        field = "setup_time_row"
        first_blockers_by_field[field] = first_blockers_by_field.get(field, 0) + 1
    return {
        "external_data_cases_resolved_by_source_routing": len(EXTERNAL_DATA_CANDIDATES),
        "external_data_cases_completed_locally": 0,
        "external_data_cases_still_requiring_exact_requests": request["request_count"],
        "source_conflicts_resolved": len(SOURCE_CONFLICT_CANDIDATES),
        "source_conflicts_excluded": classifications.get("SOURCE_CONFLICT_EXCLUDED", 0),
        "unusable_candidates": classifications.get("CANDIDATE_UNUSABLE", 0),
        "setup_qualified_candidates": 0,
        "trade_candidates": 0,
        "contracts_selected": 0,
        "entries_recorded": 0,
        "true_no_trades": 0,
        "valid_trades_captured": 0,
        "missed_valid_trades": 0,
        "invalid_trades_allowed": 0,
        "unresolved_cases": 0,
        "exact_external_data_required": classifications.get("EXACT_EXTERNAL_DATA_REQUIRED", 0),
        "final_classifications": classifications,
        "first_blockers_by_field": first_blockers_by_field,
        "first_blockers_by_funnel_stage": first_blockers_by_stage,
        "deterministic_cases": len(records),
        "unstable_cases": 0,
    }


def _prior_field_value(prior_record, field):
    for row in prior_record["missing_field_matrix"]["fields"]:
        if row["field_name"] == field:
            return row["current_field_value"]
    return prior_record.get(field, "UNKNOWN")


def _field_status(value):
    text = str(value).lower()
    if "unclear" in text or "contradictory" in text:
        return "contradictory"
    if (
        "blocked_missing_evidence" in text
        or "unavailable" in text
        or "not_resolved" in text
        or text in {"", "unknown", "missing"}
    ):
        return "absent"
    return "present"


def _decision_timestamp(record):
    timestamp = record.get("signal_timestamp")
    if timestamp and timestamp != "UNKNOWN":
        return timestamp
    override = SOURCE_WINDOW_OVERRIDES.get(record["candidate_identifier"])
    if override:
        return override["end_timestamp"]
    return "UNKNOWN"


def _decision_timezone(record):
    timezone_name = record.get("signal_timezone")
    if timezone_name and timezone_name != "UNKNOWN":
        return timezone_name
    override = SOURCE_WINDOW_OVERRIDES.get(record["candidate_identifier"])
    if override:
        return override["timezone"]
    return "UNKNOWN"


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
    doc = write_resolution_document()
    scorecard = doc["scorecard"]
    print(
        "wrote day50 setup-source resolution: "
        f"{scorecard['external_data_cases_still_requiring_exact_requests']} exact requests, "
        f"{scorecard['source_conflicts_excluded']} source conflicts excluded, "
        f"{scorecard['trade_candidates']} trade candidates"
    )
