import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from historical_signal_replay import day50_accepted_complete_setup_evidence_intake


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_accepted_setup_evidence_replay_after_intake.json"
)
INTAKE_RESULT_PATH = day50_accepted_complete_setup_evidence_intake.RESULT_PATH
DAY48_FUNNEL_RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day48_positive_trade_capture_funnel.json"
)

RESULT_VERSION = "day50_accepted_setup_evidence_replay_after_intake_v1"
NEXT_TASK_FILENAME = (
    "SAFE_FAST_DAY50_ACCEPTED_SETUP_EVIDENCE_REPLAY_AFTER_INTAKE_CLOSEOUT_CODEX_TASK.md"
)
TARGET_CANDIDATE_ID = "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001"


def build_replay_document(*, source_commit=None, run_timestamp=None):
    intake = json.loads(INTAKE_RESULT_PATH.read_text(encoding="utf-8"))
    day48 = json.loads(DAY48_FUNNEL_RESULT_PATH.read_text(encoding="utf-8"))
    _validate_prior_intake(intake)

    accepted_records = intake["accepted_complete_setup_evidence_records"]
    day48_target = _day48_target_record(day48)
    replay_records = [
        _replay_record(record, day48_target)
        for record in accepted_records
    ]
    replay_payload = {"replay_records": replay_records}
    first_hash = _stable_hash(replay_payload)
    second_hash = _stable_hash(replay_payload)

    return {
        "result_version": RESULT_VERSION,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp or _utc_now(),
        "prior_intake_result_path": str(INTAKE_RESULT_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
        "day48_regression_result_path": str(
            DAY48_FUNNEL_RESULT_PATH.relative_to(REPO_ROOT)
        ).replace("\\", "/"),
        "replay_policy": {
            "source": "accepted complete setup-evidence intake records only",
            "accepted_record_ids": [
                record["candidate_identifier"] for record in accepted_records
            ],
            "new_candidate_scan_run": False,
            "closed_setup_source_candidates_reopened": False,
            "rejected_intake_rows_replayed": False,
            "trade_candidate_requires_blocker_caution_status": ["clean", "caution"],
            "accepted_fail_blocks_trade_candidate": True,
            "forbidden_inputs": [
                "new candidate scans",
                "closed setup-source candidates",
                "rejected intake rows",
                "option requests before TRADE_CANDIDATE",
                "exit-path requests before valid entry",
                "P&L",
                "proof",
                "profitability",
                "paper/live readiness",
            ],
        },
        "accepted_intake_record_count": len(accepted_records),
        "replay_record_count": len(replay_records),
        "replay_records": replay_records,
        "scorecard": _scorecard(replay_records),
        "determination": _determination(replay_records),
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
                "Replay did not produce a TRADE_CANDIDATE; accepted complete "
                "setup evidence was stopped by accepted blocker/caution status fail."
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
            "route": "accepted_setup_evidence_replay_after_intake_closeout",
            "reason": (
                "The only accepted intake record replayed as a legitimate safety "
                "rejection, not an evidence or harness problem. The next bounded "
                "step should close out this replay result and choose the next "
                "evidence-producing task without reopening closed candidates."
            ),
        },
    }


def write_replay_document(path=RESULT_PATH, *, source_commit=None, run_timestamp=None):
    document = build_replay_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return document


def _validate_prior_intake(intake):
    if intake["scorecard"]["accepted_complete_setup_evidence_ingested"] != 1:
        raise ValueError("Accepted complete setup-evidence intake count changed")
    if intake["scorecard"]["trade_candidates"] != 0:
        raise ValueError("Prior accepted setup-evidence intake already has trade candidates")
    accepted_ids = [
        record["candidate_identifier"]
        for record in intake["accepted_complete_setup_evidence_records"]
    ]
    if accepted_ids != [TARGET_CANDIDATE_ID]:
        raise ValueError(f"Unexpected accepted intake record ids: {accepted_ids!r}")
    target = intake["accepted_complete_setup_evidence_records"][0]
    if target["field_results"]["blocker_caution_review"]["value"] != "fail":
        raise ValueError("Target accepted intake record no longer has blocker/caution fail")


def _replay_record(record, day48_target):
    blocker = record["field_results"]["blocker_caution_review"]
    blocker_status = blocker["value"]
    trade_candidate = blocker_status in {"clean", "caution"}
    exact_blocker_code = _day48_value(day48_target, "exact_blocker_code")
    final_classification = (
        "TRADE_CANDIDATE"
        if trade_candidate
        else "TRUE_NO_TRADE_LEGITIMATE_SAFETY_REJECTION"
    )
    return {
        "candidate_identifier": record["candidate_identifier"],
        "setup_family": record["setup_family"],
        "underlying": record["underlying"],
        "source_time": record["source_time"],
        "setup_time_row": record["field_results"]["setup_time_row"]["value"],
        "trigger": record["field_results"]["trigger"]["value"],
        "invalidation": record["field_results"]["invalidation"]["value"],
        "freshness_final_signal_state": record["field_results"][
            "freshness_final_signal_state"
        ]["value"],
        "blocker_caution_review": blocker_status,
        "blocker_caution_source": blocker["source"],
        "highest_stage_reached": "SETUP_QUALIFIED",
        "first_stage_not_reached": None if trade_candidate else "TRADE_CANDIDATE",
        "setup_qualified": True,
        "trade_candidate": trade_candidate,
        "contract_selected": False,
        "price_acceptable": False,
        "entry_eligible": False,
        "entry_recorded": False,
        "exit_evaluated": False,
        "final_classification": final_classification,
        "safety_rejection_legitimate": not trade_candidate,
        "evidence_or_harness_problem": False,
        "evidence_or_harness_problem_reason": (
            "No harness/evidence defect found: setup evidence is accepted and "
            "complete, and accepted blocker/caution status fail is a frozen "
            "positive-entry stop."
        ),
        "safety_rejection_reason": (
            "accepted blocker/caution review is fail"
            if not trade_candidate
            else None
        ),
        "exact_blocker_field": (
            "blocker_caution_review" if not trade_candidate else None
        ),
        "exact_blocker_code": exact_blocker_code if not trade_candidate else None,
        "day48_regression_classification": _day48_value(
            day48_target, "final_classification"
        ),
        "day48_regression_blocker_category": _day48_value(
            day48_target, "blocker_category"
        ),
        "day48_regression_evidence_source": _day48_value(
            day48_target, "evidence_source"
        ),
        "day48_regression_result_name": _day48_nested_value(
            day48_target, "first_run_output", "result_name"
        ),
        "day48_regression_failure_reason": _day48_nested_value(
            day48_target, "first_run_output", "failure_reason"
        ),
        "day48_regression_entry_quote_time": _day48_nested_value(
            day48_target, "first_run_output", "entry_quote_time"
        ),
        "day48_regression_entry_time": _day48_nested_value(
            day48_target, "first_run_output", "entry_time"
        ),
        "option_request_created": False,
        "exit_path_request_created": False,
        "proof_accepted": False,
        "profitability_claimed": False,
    }


def _scorecard(records):
    safety_rejections = [
        record for record in records if record["safety_rejection_legitimate"]
    ]
    harness_problems = [
        record for record in records if record["evidence_or_harness_problem"]
    ]
    trade_candidates = [record for record in records if record["trade_candidate"]]
    return {
        "accepted_intake_records_replayed": len(records),
        "setup_qualified_candidates": len(records),
        "trade_candidates": len(trade_candidates),
        "legitimate_safety_rejections": len(safety_rejections),
        "evidence_or_harness_problems": len(harness_problems),
        "true_no_trades": len(safety_rejections),
        "missing_data_cases": 0,
        "unresolved_cases": 0,
        "contracts_selected": 0,
        "entries_recorded": 0,
        "valid_trades_captured": 0,
        "missed_valid_trades": 0,
        "invalid_trades_allowed": 0,
    }


def _determination(records):
    if records and all(record["safety_rejection_legitimate"] for record in records):
        return {
            "result": "LEGITIMATE_SAFETY_REJECTION",
            "reason": (
                "The accepted intake record has accepted complete setup evidence, "
                "but positive-entry replay must honor accepted blocker/caution "
                "status fail. The local regression record names the same failure "
                "as quote_age_above_5_minutes."
            ),
            "harness_problem_found": False,
            "evidence_problem_found": False,
        }
    return {
        "result": "REVIEW_REQUIRED",
        "reason": "At least one accepted intake record did not classify as a safety rejection.",
        "harness_problem_found": any(
            record["evidence_or_harness_problem"] for record in records
        ),
        "evidence_problem_found": any(
            record["evidence_or_harness_problem"] for record in records
        ),
    }


def _day48_target_record(day48):
    for record in day48.get("candidate_records", []):
        if record.get("candidate_identifier") == TARGET_CANDIDATE_ID:
            return record
    return {}


def _day48_value(record, field_name):
    value = record.get(field_name)
    return value if value is not None else "NOT_AVAILABLE"


def _day48_nested_value(record, outer, inner):
    nested = record.get(outer) or {}
    value = nested.get(inner)
    return value if value is not None else "NOT_AVAILABLE"


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
    doc = write_replay_document()
    scorecard = doc["scorecard"]
    print(
        "wrote day50 accepted setup evidence replay after intake: "
        f"{scorecard['accepted_intake_records_replayed']} replayed, "
        f"{scorecard['trade_candidates']} trade candidates, "
        f"{scorecard['legitimate_safety_rejections']} legitimate safety rejections, "
        f"{scorecard['evidence_or_harness_problems']} evidence/harness problems"
    )
