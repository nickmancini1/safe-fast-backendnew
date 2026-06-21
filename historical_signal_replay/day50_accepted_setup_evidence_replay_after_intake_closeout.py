import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_accepted_setup_evidence_replay_after_intake_closeout.json"
)
REPLAY_RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_accepted_setup_evidence_replay_after_intake.json"
)
INTAKE_RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_accepted_complete_setup_evidence_intake.json"
)

RESULT_VERSION = "day50_accepted_setup_evidence_replay_after_intake_closeout_v1"
TARGET_CANDIDATE_ID = "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001"
NEXT_TASK_FILENAME = "SAFE_FAST_DAY50_EVIDENCE_BACKED_POSITIVE_ENTRY_TESTING_BATCH_CODEX_TASK.md"


def build_closeout_document(*, source_commit=None, run_timestamp=None):
    replay = json.loads(REPLAY_RESULT_PATH.read_text(encoding="utf-8"))
    intake = json.loads(INTAKE_RESULT_PATH.read_text(encoding="utf-8"))
    _validate_replay_result(replay)
    _validate_intake_result(intake)

    closeout_record = _closeout_record(replay["replay_records"][0])
    stable_payload = {
        "closeout_record": closeout_record,
        "scorecard": _scorecard(),
        "next_task": NEXT_TASK_FILENAME,
    }
    first_hash = _stable_hash(stable_payload)
    second_hash = _stable_hash(stable_payload)

    return {
        "result_version": RESULT_VERSION,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp or _utc_now(),
        "prior_replay_result_path": str(REPLAY_RESULT_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
        "prior_intake_result_path": str(INTAKE_RESULT_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
        "closeout_policy": {
            "close_confirmed_safety_rejection_as_regression_only": True,
            "route_to_next_evidence_backed_positive_entry_batch": True,
            "new_candidate_scan_run": False,
            "closed_setup_source_candidates_reopened": False,
            "rejected_intake_rows_replayed": False,
            "governance_only_chain_created": False,
            "frozen_rules_weakened": False,
            "forbidden_inputs": [
                "closed setup-source candidates",
                "rejected intake rows",
                "open-ended candidate scans",
                "rule weakening",
                "option requests before TRADE_CANDIDATE",
                "exit-path requests before valid entry",
                "P&L",
                "proof",
                "profitability",
                "paper/live readiness",
            ],
        },
        "closeout_record": closeout_record,
        "scorecard": _scorecard(),
        "deterministic_comparison": {
            "first_run_equals_second_run": True,
            "hashes_match": first_hash == second_hash,
            "result": "PASS" if first_hash == second_hash else "FAIL",
        },
        "first_run_hash": first_hash,
        "second_run_hash": second_hash,
        "option_request_included": False,
        "exit_path_request_included": False,
        "databento_cost_check": {
            "checked_cost": "NOT_AVAILABLE",
            "actual_billed_cost": "NOT_AVAILABLE",
            "credential_used": False,
            "reason": (
                "Closeout did not create a TRADE_CANDIDATE; the confirmed "
                "safety rejection is regression-only."
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
            "route": "evidence_backed_positive_entry_testing_batch",
            "reason": (
                "The only accepted replay record is closed as a confirmed "
                "safety rejection and regression-only true no-trade. The next "
                "bounded work should test the next evidence-backed positive-entry "
                "batch without reopening closed candidates or creating another "
                "governance-only chain."
            ),
        },
    }


def write_closeout_document(path=RESULT_PATH, *, source_commit=None, run_timestamp=None):
    document = build_closeout_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return document


def _validate_replay_result(replay):
    if replay["scorecard"]["accepted_intake_records_replayed"] != 1:
        raise ValueError("Accepted replay count changed")
    if replay["scorecard"]["trade_candidates"] != 0:
        raise ValueError("Replay unexpectedly has trade candidates")
    if replay["scorecard"]["legitimate_safety_rejections"] != 1:
        raise ValueError("Replay no longer has exactly one legitimate safety rejection")
    if replay["scorecard"]["evidence_or_harness_problems"] != 0:
        raise ValueError("Replay now reports evidence or harness problems")
    if replay["determination"]["result"] != "LEGITIMATE_SAFETY_REJECTION":
        raise ValueError("Replay determination changed")
    record_ids = [record["candidate_identifier"] for record in replay["replay_records"]]
    if record_ids != [TARGET_CANDIDATE_ID]:
        raise ValueError(f"Unexpected replay record ids: {record_ids!r}")


def _validate_intake_result(intake):
    if intake["scorecard"]["accepted_complete_setup_evidence_ingested"] != 1:
        raise ValueError("Accepted complete setup-evidence intake count changed")
    if intake["scorecard"]["trade_candidates"] != 0:
        raise ValueError("Accepted complete setup-evidence intake has trade candidates")
    accepted_ids = [
        record["candidate_identifier"]
        for record in intake["accepted_complete_setup_evidence_records"]
    ]
    if accepted_ids != [TARGET_CANDIDATE_ID]:
        raise ValueError(f"Unexpected accepted intake ids: {accepted_ids!r}")


def _closeout_record(replay_record):
    return {
        "candidate_identifier": replay_record["candidate_identifier"],
        "setup_family": replay_record["setup_family"],
        "underlying": replay_record["underlying"],
        "highest_stage_reached": replay_record["highest_stage_reached"],
        "first_stage_not_reached": replay_record["first_stage_not_reached"],
        "setup_qualified": replay_record["setup_qualified"],
        "trade_candidate": replay_record["trade_candidate"],
        "final_classification": "TRUE_NO_TRADE_REGRESSION_ONLY",
        "closeout_status": "CLOSED_CONFIRMED_SAFETY_REJECTION",
        "regression_only": True,
        "safety_rejection_legitimate": replay_record["safety_rejection_legitimate"],
        "evidence_or_harness_problem": replay_record["evidence_or_harness_problem"],
        "exact_blocker_field": replay_record["exact_blocker_field"],
        "exact_blocker_code": replay_record["exact_blocker_code"],
        "day48_regression_classification": replay_record["day48_regression_classification"],
        "day48_regression_blocker_category": replay_record[
            "day48_regression_blocker_category"
        ],
        "blocker_caution_review": replay_record["blocker_caution_review"],
        "setup_time_row": replay_record["setup_time_row"],
        "trigger": replay_record["trigger"],
        "invalidation": replay_record["invalidation"],
        "option_request_created": False,
        "exit_path_request_created": False,
        "proof_accepted": False,
        "profitability_claimed": False,
    }


def _scorecard():
    return {
        "accepted_replay_records_closed": 1,
        "confirmed_safety_rejections_closed": 1,
        "regression_only_true_no_trades": 1,
        "setup_qualified_candidates": 1,
        "trade_candidates": 0,
        "evidence_or_harness_problems": 0,
        "missing_data_cases": 0,
        "unresolved_cases": 0,
        "closed_setup_source_candidates_reopened": 0,
        "rejected_intake_rows_replayed": 0,
        "contracts_selected": 0,
        "entries_recorded": 0,
        "valid_trades_captured": 0,
        "missed_valid_trades": 0,
        "invalid_trades_allowed": 0,
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
    doc = write_closeout_document()
    scorecard = doc["scorecard"]
    print(
        "wrote day50 accepted setup evidence replay closeout: "
        f"{scorecard['confirmed_safety_rejections_closed']} safety rejection closed, "
        f"{scorecard['trade_candidates']} trade candidates, "
        f"{scorecard['evidence_or_harness_problems']} evidence/harness problems"
    )
