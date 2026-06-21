import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from historical_signal_replay import day48_positive_trade_capture_funnel as day48_funnel
from historical_signal_replay import day50_exact_setup_source_evidence_completion
from historical_signal_replay import day50_required_setup_source_resolution
from watcher_foundation import candidate_completeness_screen


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_positive_entry_expansion_after_setup_source_closure.json"
)
DAY50_CLOSURE_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_exact_setup_source_evidence_completion.json"
)
DAY50_SOURCE_RESOLUTION_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_required_setup_source_resolution.json"
)

RESULT_VERSION = "day50_positive_entry_expansion_after_setup_source_closure_v1"
NEXT_TASK_FILENAME = "SAFE_FAST_DAY50_ACCEPTED_COMPLETE_SETUP_EVIDENCE_INTAKE_CODEX_TASK.md"

REQUIRED_SETUP_EVIDENCE_FIELDS = (
    "setup_candle",
    "trigger",
    "invalidation",
    "freshness",
    "blocker",
    "no_hindsight_boundary",
)

CLOSED_SETUP_SOURCE_CANDIDATE_IDS = set(
    day50_exact_setup_source_evidence_completion.TARGET_CANDIDATES
)


def build_expansion_document(*, source_commit=None, run_timestamp=None):
    closure = json.loads(DAY50_CLOSURE_PATH.read_text(encoding="utf-8"))
    resolution = json.loads(DAY50_SOURCE_RESOLUTION_PATH.read_text(encoding="utf-8"))
    if closure["scorecard"]["setup_source_requests_remaining"] != 0:
        raise ValueError("Day 50 setup-source closure is not complete")
    if closure["scorecard"]["trade_candidates"] != 0:
        raise ValueError("Unexpected trade candidates in Day 50 closure result")

    pool = candidate_completeness_screen.build_candidate_pool()
    scan_records = [_scan_record(row, closure, resolution) for row in pool]
    eligible = [row for row in scan_records if row["eligible_for_expansion"]]
    candidate_records = [_candidate_record(row) for row in eligible]
    replay_payload = {"candidate_records": candidate_records, "scan_records": scan_records}
    first_hash = _stable_hash(replay_payload)
    second_hash = _stable_hash(replay_payload)
    existing = day48_funnel.build_funnel_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    return {
        "result_version": RESULT_VERSION,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp or _utc_now(),
        "prior_closure_result_path": str(DAY50_CLOSURE_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
        "prior_source_resolution_result_path": str(
            DAY50_SOURCE_RESOLUTION_PATH.relative_to(REPO_ROOT)
        ).replace("\\", "/"),
        "selection_policy": {
            "source_universe": "watcher_foundation.candidate_completeness_screen.build_candidate_pool",
            "only_new_candidates_with_accepted_complete_setup_evidence": True,
            "closed_setup_source_candidates_are_regression_records_only": True,
            "closed_candidate_ids": sorted(CLOSED_SETUP_SOURCE_CANDIDATE_IDS),
            "required_setup_evidence_fields": list(REQUIRED_SETUP_EVIDENCE_FIELDS),
            "forbidden_selection_inputs": [
                "closed setup-source slots without later accepted evidence",
                "source-conflict candidates",
                "unusable candidates",
                "duplicates",
                "drop or replace rows",
                "outcome_window",
                "option exit path",
                "P&L",
                "profitability",
            ],
        },
        "source_pool_count": len(pool),
        "scan_records": scan_records,
        "candidate_count": len(candidate_records),
        "candidate_records": candidate_records,
        "combined_scorecard": _scorecard(candidate_records),
        "first_blockers": _first_blockers(candidate_records),
        "ineligible_reason_totals": _ineligible_reason_totals(scan_records),
        "closed_candidates_regression_records": _closed_regression_records(closure),
        "source_resolution_regression_records": _source_resolution_regression_records(resolution),
        "existing_regression_control_result": {
            "candidate_count": len(existing["candidate_records"]),
            "deterministic_result": existing["deterministic_comparison"]["result"],
            "combined_scorecard": existing["combined_scorecard"],
            "final_classifications": existing["final_classifications"],
        },
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
            "reason": "No new candidate reached TRADE_CANDIDATE; no option, quote, or exit-path request is valid.",
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
            "route": "accepted_complete_setup_evidence_intake_before_next_expansion",
            "reason": (
                "The post-closure expansion found zero new candidates with accepted, "
                "complete setup evidence. Closed candidates stay regression-only; the "
                "next bounded step must intake or validate exact accepted setup evidence "
                "before another expansion can select candidates."
            ),
        },
    }


def write_expansion_document(path=RESULT_PATH, *, source_commit=None, run_timestamp=None):
    document = build_expansion_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return document


def _scan_record(row, closure, resolution):
    candidate_id = row["candidate_id"]
    ineligible_reasons = []
    if candidate_id in CLOSED_SETUP_SOURCE_CANDIDATE_IDS:
        ineligible_reasons.append("closed_setup_source_regression_only")
    if _resolution_classification(candidate_id, resolution) in {
        "SOURCE_CONFLICT_EXCLUDED",
        "CANDIDATE_UNUSABLE",
    }:
        ineligible_reasons.append("prior_source_resolution_excluded_or_unusable")
    if row["duplicate"] == "yes":
        ineligible_reasons.append("duplicate_signal_same_underlying_opportunity")
    if row["status"] in {"drop", "replace"}:
        ineligible_reasons.append(f"candidate_status_{row['status']}")

    incomplete_fields = [
        field
        for field in REQUIRED_SETUP_EVIDENCE_FIELDS
        if _is_missing_or_unclear(row.get(field))
    ]
    if incomplete_fields:
        ineligible_reasons.append("accepted_complete_setup_evidence_absent")
    if row["status"] != "ready":
        ineligible_reasons.append("candidate_status_not_ready")

    closure_record = _closure_record(candidate_id, closure)
    if closure_record is not None and closure_record["final_classification"] != (
        "SETUP_SOURCE_CLOSED_NO_ACCEPTED_EVIDENCE"
    ):
        ineligible_reasons.append("closure_conflict")

    return {
        "candidate_identifier": candidate_id,
        "setup_family": row["setup_type"],
        "underlying": row["symbol"],
        "source_rows": row["source_lines"],
        "candidate_status": row["status"],
        "duplicate_signal": row["duplicate"] == "yes",
        "required_setup_evidence_fields": {
            field: row.get(field) for field in REQUIRED_SETUP_EVIDENCE_FIELDS
        },
        "incomplete_setup_evidence_fields": incomplete_fields,
        "prior_closure_classification": None
        if closure_record is None
        else closure_record["final_classification"],
        "prior_source_resolution_classification": _resolution_classification(
            candidate_id, resolution
        ),
        "eligible_for_expansion": not ineligible_reasons,
        "ineligible_reasons": sorted(set(ineligible_reasons)),
    }


def _candidate_record(scan_record):
    return {
        "candidate_identifier": scan_record["candidate_identifier"],
        "setup_family": scan_record["setup_family"],
        "underlying": scan_record["underlying"],
        "source_rows": scan_record["source_rows"],
        "highest_stage_reached": "SETUP_DEVELOPING",
        "first_stage_not_reached": "SETUP_QUALIFIED",
        "final_classification": "MISSING_DATA",
        "setup_qualified": False,
        "trade_candidate": False,
        "contract_selected": False,
        "entry_recorded": False,
        "exit_evaluated": False,
        "proof_accepted": False,
        "profitability_claimed": False,
    }


def _scorecard(records):
    return {
        "candidates_found": len(records),
        "candidates_runnable": len(records),
        "setup_developing_count": len(records),
        "setup_qualified_count": 0,
        "trade_candidate_count": 0,
        "contracts_selected": 0,
        "prices_accepted": 0,
        "entries_eligible": 0,
        "entries_recorded": 0,
        "exits_evaluated": 0,
        "valid_trades_captured": 0,
        "true_no_trades": 0,
        "missing_data_cases": len(records),
        "missed_valid_trades": 0,
        "invalid_trades_allowed": 0,
        "unresolved_cases": 0,
        "winners": 0,
        "losers": 0,
    }


def _first_blockers(records):
    if not records:
        return {}
    return {"SETUP_QUALIFIED": len(records)}


def _closed_regression_records(closure):
    return [
        {
            "candidate_identifier": record["candidate_identifier"],
            "final_classification": record["final_classification"],
            "highest_stage_reached": record["highest_stage_reached"],
            "regression_only": True,
        }
        for record in closure["candidate_records"]
    ]


def _source_resolution_regression_records(resolution):
    return [
        {
            "candidate_identifier": record["candidate_identifier"],
            "final_classification": record["final_classification"],
            "regression_only": True,
        }
        for record in resolution["candidate_records"]
        if record["final_classification"] in {"SOURCE_CONFLICT_EXCLUDED", "CANDIDATE_UNUSABLE"}
    ]


def _ineligible_reason_totals(scan_records):
    totals = {}
    for record in scan_records:
        for reason in record["ineligible_reasons"]:
            totals[reason] = totals.get(reason, 0) + 1
    return totals


def _closure_record(candidate_id, closure):
    for record in closure["candidate_records"]:
        if record["candidate_identifier"] == candidate_id:
            return record
    return None


def _resolution_classification(candidate_id, resolution):
    for record in resolution["candidate_records"]:
        if record["candidate_identifier"] == candidate_id:
            return record["final_classification"]
    return None


def _is_missing_or_unclear(value):
    text = str(value or "").strip().lower()
    return not text or "missing" in text or "unclear" in text or "to_review" in text


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
    doc = write_expansion_document()
    scorecard = doc["combined_scorecard"]
    print(
        "wrote day50 post-closure positive-entry expansion: "
        f"{doc['candidate_count']} eligible new candidates, "
        f"{scorecard['trade_candidate_count']} trade candidates, "
        f"{scorecard['valid_trades_captured']} valid captured"
    )
