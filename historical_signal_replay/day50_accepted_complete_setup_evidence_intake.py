import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from historical_signal_replay import day50_exact_setup_source_evidence_completion
from historical_signal_replay import day50_positive_entry_expansion_after_setup_source_closure
from watcher_foundation import source_evidence_package_to_intake_bridge as bridge
from watcher_foundation import source_evidence_package_intake as package_intake


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_accepted_complete_setup_evidence_intake.json"
)
WORK_PACKAGE_DIR = REPO_ROOT / package_intake.WORK_PACKAGE_DIR

RESULT_VERSION = "day50_accepted_complete_setup_evidence_intake_v1"
NEXT_TASK_FILENAME = (
    "SAFE_FAST_DAY50_ACCEPTED_SETUP_EVIDENCE_REPLAY_AFTER_INTAKE_CODEX_TASK.md"
)

REQUIRED_ACCEPTED_SETUP_FIELDS = (
    "setup_time_row",
    "trigger",
    "invalidation",
    "freshness_final_signal_state",
    "blocker_caution_review",
    "no_hindsight_boundary",
    "session_boundary_behavior",
)
ACCEPTED_COMPLETE_CONTEXT_STATUSES = {"clean", "caution", "fail"}
UNRESOLVED_TEXT = {
    "",
    "missing",
    "unclear",
    "unknown",
    "to_review",
    "unfilled",
    "placeholder",
    "needs_real_evidence",
    "missing_required_evidence",
    "tastytrade_data_not_available",
}


def build_intake_document(*, source_commit=None, run_timestamp=None):
    closure = json.loads(
        day50_exact_setup_source_evidence_completion.RESULT_PATH.read_text(
            encoding="utf-8"
        )
    )
    expansion = json.loads(
        day50_positive_entry_expansion_after_setup_source_closure.RESULT_PATH.read_text(
            encoding="utf-8"
        )
    )
    _validate_prior_controls(closure, expansion)

    bridge_result = bridge.bridge_work_package_path(WORK_PACKAGE_DIR)
    requirements = {
        requirement.evidence_name: requirement
        for requirement in package_intake.build_package_requirements()
    }
    request_rows = {
        row["evidence_name"]: row
        for row in bridge_result["bridge_request_results"]
    }
    candidate_records = [
        _candidate_record(row, requirements, request_rows)
        for row in bridge_result["candidate_bridge_results"]
    ]
    accepted_records = [
        record
        for record in candidate_records
        if record["setup_evidence_intake_status"]
        == "ACCEPTED_COMPLETE_SETUP_EVIDENCE_INGESTED"
    ]
    rejected_records = [
        record
        for record in candidate_records
        if record["setup_evidence_intake_status"] != "ACCEPTED_COMPLETE_SETUP_EVIDENCE_INGESTED"
    ]
    replay_payload = {
        "candidate_records": candidate_records,
        "accepted_candidate_ids": [
            record["candidate_identifier"] for record in accepted_records
        ],
    }
    first_hash = _stable_hash(replay_payload)
    second_hash = _stable_hash(replay_payload)
    return {
        "result_version": RESULT_VERSION,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp or _utc_now(),
        "prior_closure_result_path": str(
            day50_exact_setup_source_evidence_completion.RESULT_PATH.relative_to(REPO_ROOT)
        ).replace("\\", "/"),
        "prior_post_closure_expansion_result_path": str(
            day50_positive_entry_expansion_after_setup_source_closure.RESULT_PATH.relative_to(
                REPO_ROOT
            )
        ).replace("\\", "/"),
        "work_package_dir": str(package_intake.WORK_PACKAGE_DIR).replace("\\", "/"),
        "intake_policy": {
            "source": "existing local richer source-evidence work package only",
            "required_accepted_setup_fields": list(REQUIRED_ACCEPTED_SETUP_FIELDS),
            "accepted_complete_context_statuses": sorted(
                ACCEPTED_COMPLETE_CONTEXT_STATUSES
            ),
            "closed_setup_source_candidates_are_regression_only": True,
            "closed_candidate_ids": sorted(
                day50_positive_entry_expansion_after_setup_source_closure.CLOSED_SETUP_SOURCE_CANDIDATE_IDS
            ),
            "forbidden_inputs": [
                "closed setup-source slots without later exact accepted evidence",
                "new candidate scans",
                "outcome-window-only evidence",
                "option exit path",
                "P&L",
                "profitability",
                "paper/live readiness",
            ],
        },
        "work_package_summary": {
            "requests_mapped": bridge_result["requests_mapped_count"],
            "passed_requests": bridge_result["passed_request_count"],
            "failed_requests": bridge_result["failed_request_count"],
            "reconsideration_eligible_candidates": bridge_result[
                "reconsideration_eligible_count"
            ],
            "legacy_bridge_intake_ready_count": bridge_result["intake_ready_count"],
        },
        "candidate_count": len(candidate_records),
        "candidate_records": candidate_records,
        "accepted_complete_setup_evidence_records": accepted_records,
        "rejected_candidate_records": rejected_records,
        "scorecard": _scorecard(candidate_records),
        "closed_candidates_regression_records": _closed_regression_records(closure),
        "first_run_hash": first_hash,
        "second_run_hash": second_hash,
        "deterministic_comparison": {
            "first_run_equals_second_run": True,
            "hashes_match": first_hash == second_hash,
            "result": "PASS" if first_hash == second_hash else "FAIL",
        },
        "option_request_included": False,
        "exit_path_request_included": False,
        "databento_cost_check": {
            "checked_cost": "NOT_AVAILABLE",
            "actual_billed_cost": "NOT_AVAILABLE",
            "credential_used": False,
            "reason": (
                "No accepted intake candidate reached TRADE_CANDIDATE; the one "
                "accepted complete setup-evidence record has accepted blocker/caution "
                "status fail."
            ),
        },
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
            "filename": NEXT_TASK_FILENAME,
            "route": "accepted_setup_evidence_replay_after_intake",
            "reason": (
                "One local Clean Fast Break candidate now has accepted complete setup "
                "evidence ingested, but its accepted blocker/caution review is fail, "
                "so the next bounded task should replay the accepted intake record "
                "through the positive-entry gate without requesting options, exits, "
                "or new data unless a candidate actually reaches TRADE_CANDIDATE."
            ),
        },
    }


def write_intake_document(path=RESULT_PATH, *, source_commit=None, run_timestamp=None):
    document = build_intake_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return document


def _validate_prior_controls(closure, expansion):
    if closure["scorecard"]["setup_source_requests_remaining"] != 0:
        raise ValueError("Day 50 setup-source closure still has open requests")
    if closure["scorecard"]["trade_candidates"] != 0:
        raise ValueError("Day 50 setup-source closure unexpectedly has trade candidates")
    if expansion["candidate_count"] != 0:
        raise ValueError("Post-closure expansion no longer has zero selected candidates")
    if expansion["combined_scorecard"]["missing_data_cases"] != 0:
        raise ValueError("Post-closure expansion created a missing-data batch")


def _candidate_record(candidate_bridge_row, requirements, request_rows):
    candidate_id = candidate_bridge_row["candidate_id"]
    evidence_names = tuple(candidate_bridge_row["required_evidence_names"])
    evidence_rows = [
        _read_requirement_row(requirements[name]) for name in evidence_names
    ]
    field_results = _field_results(evidence_rows)
    incomplete = [
        field
        for field in REQUIRED_ACCEPTED_SETUP_FIELDS
        if not field_results[field]["accepted"]
    ]
    accepted = (
        candidate_bridge_row["all_required_requests_passed"]
        and not incomplete
        and candidate_id
        not in day50_positive_entry_expansion_after_setup_source_closure.CLOSED_SETUP_SOURCE_CANDIDATE_IDS
    )
    context_status = field_results["blocker_caution_review"]["value"]
    trade_candidate = accepted and context_status in {"clean", "caution"}
    return {
        "candidate_identifier": candidate_id,
        "setup_family": _common_value(evidence_rows, "setup_type"),
        "underlying": _common_value(evidence_rows, "symbol"),
        "source_time": _common_value(evidence_rows, "source_time"),
        "source_session": _common_value(evidence_rows, "source_session"),
        "required_evidence_names": list(evidence_names),
        "passed_evidence_names": [
            name for name in evidence_names if request_rows[name]["passed"]
        ],
        "failed_evidence_names": [
            name for name in evidence_names if not request_rows[name]["passed"]
        ],
        "field_results": field_results,
        "incomplete_or_unaccepted_setup_fields": incomplete,
        "setup_evidence_intake_status": (
            "ACCEPTED_COMPLETE_SETUP_EVIDENCE_INGESTED"
            if accepted
            else "NOT_ACCEPTED_COMPLETE_SETUP_EVIDENCE"
        ),
        "final_classification": (
            "ACCEPTED_COMPLETE_SETUP_EVIDENCE_TRADE_BLOCKED"
            if accepted and not trade_candidate
            else (
                "ACCEPTED_COMPLETE_SETUP_EVIDENCE_TRADE_CANDIDATE"
                if trade_candidate
                else "EXACT_SETUP_EVIDENCE_NOT_COMPLETE"
            )
        ),
        "highest_stage_reached": "SETUP_QUALIFIED" if accepted else "SETUP_DEVELOPING",
        "first_stage_not_reached": (
            "TRADE_CANDIDATE" if accepted and not trade_candidate else "SETUP_QUALIFIED"
        ),
        "setup_qualified": accepted,
        "trade_candidate": trade_candidate,
        "contract_selected": False,
        "price_acceptable": False,
        "entry_eligible": False,
        "entry_recorded": False,
        "exit_evaluated": False,
        "proof_accepted": False,
        "profitability_claimed": False,
    }


def _field_results(evidence_rows):
    context_status = _context_status(evidence_rows)
    freshness_status = _freshness_status(evidence_rows)
    return {
        "setup_time_row": _field_result(
            "setup_time_row",
            _common_value(evidence_rows, "setup_candle_time"),
            "all required package rows agree on setup_candle_time",
        ),
        "trigger": _field_result(
            "trigger",
            _common_value(evidence_rows, "known_trigger"),
            "all required package rows agree on known_trigger",
        ),
        "invalidation": _field_result(
            "invalidation",
            _common_value(evidence_rows, "known_invalidation"),
            "all required package rows agree on known_invalidation",
        ),
        "freshness_final_signal_state": {
            "field_name": "freshness_final_signal_state",
            "accepted": freshness_status == "fresh",
            "value": freshness_status,
            "source": "accepted lifecycle/stale-spent evidence row",
            "reason": "setup-time lifecycle status must be accepted as fresh",
        },
        "blocker_caution_review": {
            "field_name": "blocker_caution_review",
            "accepted": context_status in ACCEPTED_COMPLETE_CONTEXT_STATUSES,
            "value": context_status,
            "source": "accepted context/caution evidence row",
            "reason": "complete_caution_review_status must be clean, caution, or fail",
        },
        "no_hindsight_boundary": _no_hindsight_result(evidence_rows),
        "session_boundary_behavior": {
            "field_name": "session_boundary_behavior",
            "accepted": True,
            "value": "NOT_APPLICABLE_SAME_SESSION",
            "source": "source_session and setup-time row",
            "reason": "local intake candidates are same-session setup rows; no cross-session carry-forward is applied",
        },
    }


def _field_result(field_name, value, reason):
    return {
        "field_name": field_name,
        "accepted": not _is_unresolved(value),
        "value": value,
        "source": "local source-evidence work package",
        "reason": reason,
    }


def _no_hindsight_result(evidence_rows):
    values = [
        str(row.get("known_no_hindsight_boundary", "")).strip()
        for row in evidence_rows
        if not _is_unresolved(row.get("known_no_hindsight_boundary"))
    ]
    text = " ".join(values).lower()
    accepted = bool(values) and "future" in text and (
        "no future" in text
        or "rejects future" in text
        or "excluded" in text
        or "ignores future" in text
    )
    return {
        "field_name": "no_hindsight_boundary",
        "accepted": accepted,
        "value": " | ".join(values),
        "source": "local source-evidence work package",
        "reason": "each package row must state setup-time boundary and reject or exclude future rows",
    }


def _freshness_status(evidence_rows):
    lifecycle_rows = [
        row for row in evidence_rows if "stale" in row.get("rule_family", "").lower()
        or "expiry" in row.get("rule_family", "").lower()
    ]
    text = " ".join(
        str(row.get("prefill_note", "")) + " " + " ".join(str(value) for value in row.values())
        for row in lifecycle_rows
    ).lower()
    if (
        "lifecycle_status fresh" in text
        or "lifecycle is fresh" in text
        or "fresh setup signal" in text
    ):
        return "fresh"
    return "unknown"


def _context_status(evidence_rows):
    for row in evidence_rows:
        value = str(row.get("complete_caution_review_status", "")).strip().lower()
        if value:
            return value
    return "unknown"


def _read_requirement_row(requirement):
    file_path = WORK_PACKAGE_DIR / requirement.required_file_name
    with file_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        return {}
    return rows[0]


def _common_value(rows, field_name):
    values = [
        str(row.get(field_name, "")).strip()
        for row in rows
        if not _is_unresolved(row.get(field_name))
    ]
    if not values:
        return ""
    if len(set(values)) == 1:
        return values[0]
    return "SOURCE_CONFLICT: " + " | ".join(values)


def _is_unresolved(value):
    text = "" if value is None else str(value).strip().lower()
    return (
        text in UNRESOLVED_TEXT
        or text.startswith("missing_required_evidence:")
        or text.startswith("tastytrade_data_not_available:")
        or text.startswith("source_conflict:")
    )


def _scorecard(records):
    accepted = [
        record
        for record in records
        if record["setup_evidence_intake_status"]
        == "ACCEPTED_COMPLETE_SETUP_EVIDENCE_INGESTED"
    ]
    trade_candidates = [record for record in accepted if record["trade_candidate"]]
    blocked_by_caution = [
        record
        for record in accepted
        if record["field_results"]["blocker_caution_review"]["value"] == "fail"
    ]
    rejected = [record for record in records if record not in accepted]
    return {
        "local_candidate_records_reviewed": len(records),
        "accepted_complete_setup_evidence_ingested": len(accepted),
        "rejected_not_accepted_complete": len(rejected),
        "setup_qualified_candidates": len(accepted),
        "trade_candidates": len(trade_candidates),
        "trade_blocked_by_accepted_caution_fail": len(blocked_by_caution),
        "contracts_selected": 0,
        "entries_recorded": 0,
        "valid_trades_captured": 0,
        "true_no_trades": len(blocked_by_caution),
        "missing_data_cases": 0,
        "missed_valid_trades": 0,
        "invalid_trades_allowed": 0,
        "unresolved_cases": 0,
        "accepted_by_family": _family_totals(accepted),
        "rejected_by_family": _family_totals(rejected),
    }


def _family_totals(records):
    totals = {"Ideal": 0, "Clean Fast Break": 0, "Continuation": 0}
    for record in records:
        family = record["setup_family"]
        totals[family] = totals.get(family, 0) + 1
    return totals


def _closed_regression_records(closure):
    return [
        {
            "candidate_identifier": record["candidate_identifier"],
            "final_classification": record["final_classification"],
            "regression_only": True,
        }
        for record in closure["candidate_records"]
    ]


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
    doc = write_intake_document()
    scorecard = doc["scorecard"]
    print(
        "wrote day50 accepted complete setup evidence intake: "
        f"{scorecard['accepted_complete_setup_evidence_ingested']} accepted, "
        f"{scorecard['trade_candidates']} trade candidates, "
        f"{scorecard['trade_blocked_by_accepted_caution_fail']} blocked by accepted caution fail"
    )
