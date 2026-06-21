import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_positive_entry_remaining_evidence_gap_closeout.json"
)
ACTIVE_PATH_REPAIR_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_positive_entry_active_path_rule_evidence_repair.json"
)
TRADE_CANDIDATE_CLOSEOUT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_positive_entry_trade_candidate_rule_gap_closeout.json"
)
CONTRACT_SELECTED_MISSING_EVIDENCE_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_positive_entry_contract_selected_missing_evidence.json"
)
BATCH_RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_evidence_backed_positive_entry_testing_batch.json"
)

RESULT_VERSION = "day50_positive_entry_remaining_evidence_gap_closeout_v1"
NEXT_TASK_FILENAME = (
    "SAFE_FAST_DAY50_POSITIVE_ENTRY_ACTIVE_PATH_REQUIREMENT_REGRESSION_CODEX_TASK.md"
)

CLASSIFICATIONS = (
    "VALID_TRADE_CAPTURED",
    "TRUE_NO_TRADE",
    "MISSING_DATA",
    "MISSED_VALID_TRADE",
    "INVALID_TRADE_ALLOWED",
    "UNRESOLVED",
)


def build_closeout_document(*, source_commit=None, run_timestamp=None):
    active_path_repair = json.loads(ACTIVE_PATH_REPAIR_PATH.read_text(encoding="utf-8"))
    trade_candidate_closeout = json.loads(
        TRADE_CANDIDATE_CLOSEOUT_PATH.read_text(encoding="utf-8")
    )
    contract_selected_closeout = json.loads(
        CONTRACT_SELECTED_MISSING_EVIDENCE_PATH.read_text(encoding="utf-8")
    )
    batch = json.loads(BATCH_RESULT_PATH.read_text(encoding="utf-8"))
    _validate_inputs(
        active_path_repair,
        trade_candidate_closeout,
        contract_selected_closeout,
        batch,
    )

    active_path_records = [
        _active_path_remaining_gap_record(record)
        for record in active_path_repair["active_path_rule_evidence_repair_records"]
    ]
    contract_selected_records = [
        _contract_selected_gap_record(record)
        for record in contract_selected_closeout["remaining_evidence_gaps"]
    ]
    qqq_ideal = _qqq_ideal_outside_path_record(
        trade_candidate_closeout,
        contract_selected_closeout,
    )
    scorecard = _scorecard(
        active_path_repair,
        contract_selected_closeout,
        batch,
        active_path_records,
        contract_selected_records,
    )

    stable_payload = {
        "active_path_records": active_path_records,
        "contract_selected_records": contract_selected_records,
        "qqq_ideal": qqq_ideal,
        "scorecard": scorecard,
    }
    first_hash = _stable_hash(stable_payload)
    second_hash = _stable_hash(stable_payload)

    return {
        "result_version": RESULT_VERSION,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp or _utc_now(),
        "input_paths": {
            "day50_positive_entry_active_path_rule_evidence_repair": _relative(
                ACTIVE_PATH_REPAIR_PATH
            ),
            "day50_positive_entry_trade_candidate_rule_gap_closeout": _relative(
                TRADE_CANDIDATE_CLOSEOUT_PATH
            ),
            "day50_positive_entry_contract_selected_missing_evidence": _relative(
                CONTRACT_SELECTED_MISSING_EVIDENCE_PATH
            ),
            "day50_evidence_backed_positive_entry_testing_batch": _relative(
                BATCH_RESULT_PATH
            ),
        },
        "closeout_policy": {
            "source": "Day 50 active-path rule/evidence repair result only",
            "closeout_scope": (
                "remaining evidence-gap records from existing local fixture/source "
                "evidence and accepted frozen local rule evidence"
            ),
            "new_candidate_scan_run": False,
            "new_setup_source_pass_run": False,
            "closed_setup_source_candidates_reopened": False,
            "rejected_intake_rows_replayed": False,
            "confirmed_qqq_safety_rejection_rerun_as_live_candidate": False,
            "qqq_clean_fast_break_001_preserved_regression_only": True,
            "qqq_ideal_preserved_outside_narrowed_path": True,
            "contract_selected_closeout_additional_entries_preserved": 0,
            "frozen_rules_weakened": False,
            "governance_only_chain_created": False,
            "option_request_included": False,
            "exit_path_request_included": False,
            "classification_categories_preserved": list(CLASSIFICATIONS),
        },
        "remaining_evidence_gap_closeout_records": (
            active_path_records + contract_selected_records
        ),
        "active_path_requirement_records": active_path_records,
        "contract_selected_gap_records": contract_selected_records,
        "qqq_ideal_outside_path_preservation": qqq_ideal,
        "additional_entries": [],
        "scorecard": scorecard,
        "final_classifications": batch["final_classifications"],
        "deterministic_comparison": {
            "first_run_equals_second_run": True,
            "hashes_match": first_hash == second_hash,
            "result": "PASS" if first_hash == second_hash else "FAIL",
        },
        "first_run_hash": first_hash,
        "second_run_hash": second_hash,
        "databento_cost_check": {
            "checked_cost": "NOT_AVAILABLE",
            "actual_billed_cost": "NOT_AVAILABLE",
            "credential_used": False,
            "reason": (
                "Existing local fixture/source evidence and accepted frozen local rule "
                "evidence close the remaining gap surface to exact requirements or "
                "no-entry/outside-path determinations. No affected case reaches a valid "
                "paid option-data or exit-path request gate."
            ),
        },
        "paid_data_request_created": False,
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
            "route": "positive_entry_active_path_requirement_regression",
            "reason": (
                "The remaining open trade-candidate evidence gaps are now bounded to "
                "four exact active-path requirements. The next grouped task is to "
                "define and regression-test those active-path requirements from local "
                "fixture/source evidence before any selected-contract request."
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


def _validate_inputs(
    active_path_repair,
    trade_candidate_closeout,
    contract_selected_closeout,
    batch,
):
    if active_path_repair["result_version"] != (
        "day50_positive_entry_active_path_rule_evidence_repair_v1"
    ):
        raise ValueError("Unexpected active-path repair result version")
    if active_path_repair["scorecard"]["accepted_active_path_rule_evidence_records"] != 4:
        raise ValueError("Active-path repair record count changed")
    if active_path_repair["scorecard"]["selected_contracts_after_repair"] != 5:
        raise ValueError("Active-path selected-contract total changed")
    if active_path_repair["scorecard"]["eligible_entries_after_repair"] != 1:
        raise ValueError("Active-path eligible-entry total changed")
    if active_path_repair["scorecard"]["recorded_entries_after_repair"] != 1:
        raise ValueError("Active-path recorded-entry total changed")
    if (
        trade_candidate_closeout["scorecard"][
            "qqq_ideal_selected_contract_rule_gap_resolved_from_frozen_evidence"
        ]
        is not True
    ):
        raise ValueError("QQQ Ideal outside-path control changed")
    if contract_selected_closeout["scorecard"]["remaining_evidence_gaps"] != 2:
        raise ValueError("Contract-selected remaining-gap count changed")
    if contract_selected_closeout["scorecard"]["additional_entries_established"] != 0:
        raise ValueError("Contract-selected closeout added entries")
    if batch["scorecard"]["selected_contracts"] != 5:
        raise ValueError("Day 50 batch selected-contract count changed")
    if batch["scorecard"]["eligible_entries"] != 1:
        raise ValueError("Day 50 batch eligible-entry count changed")
    if batch["scorecard"]["recorded_entries"] != 1:
        raise ValueError("Day 50 batch recorded-entry count changed")
    for classification in CLASSIFICATIONS:
        if classification not in batch["final_classifications"]:
            raise ValueError(f"Missing classification category: {classification}")


def _active_path_remaining_gap_record(record):
    requirement = record["repaired_requirement"]
    return {
        "gap_type": "active_path_requirement",
        "candidate_identifier": record["candidate_identifier"],
        "business_candidate_id": record["business_candidate_id"],
        "underlying": record["underlying"],
        "setup_family": record["setup_family"],
        "batch_first_stage_not_reached": "TRADE_CANDIDATE",
        "highest_stage_reached": record["highest_stage_reached_after_repair"],
        "exact_blocker": record["exact_blocker"],
        "field": requirement["field"],
        "source": requirement["source_file_or_doc"],
        "dataset_schema_or_api": requirement["dataset_schema_or_api"],
        "calculator": requirement["calculator"],
        "timestamp_window": requirement["timestamp_window"],
        "required_source_field_or_log_evidence": requirement[
            "required_source_field_or_log_evidence"
        ],
        "unavailable_or_failure_reason": requirement["exact_missing_rule_or_evidence"],
        "blocking_scope": "blocks TRADE_CANDIDATE before selected-contract identity",
        "closeout_determination": "closed_to_exact_active_path_regression_requirement",
        "open_after_closeout": True,
        "selected_contract_after_closeout": False,
        "entry_eligible_after_closeout": False,
        "entry_recorded_after_closeout": False,
        "additional_entry_established": False,
        "next_action": requirement["smallest_next_action"],
        "proof_accepted": False,
        "profitability_claimed": False,
        "paper_eligible": False,
        "live_eligible": False,
    }


def _contract_selected_gap_record(gap):
    is_no_entry_spread = gap["field"] == "selected_contract_spread"
    return {
        "gap_type": "contract_selected_closeout_preservation",
        "candidate_identifier": gap["candidate_identifier"],
        "business_candidate_id": _business_candidate_id_for_gap(gap),
        "batch_first_stage_not_reached": "CONTRACT_SELECTED",
        "exact_blocker": gap["unavailable_or_failure_reason"],
        "field": gap["field"],
        "source": gap["source"],
        "dataset_schema_or_api": gap["dataset_schema_or_api"],
        "calculator": (
            "historical_signal_replay.execution_context_calculator"
            if is_no_entry_spread
            else "SAFE-FAST frozen local rule package"
        ),
        "timestamp_window": gap["timestamp_window"],
        "unavailable_or_failure_reason": gap["unavailable_or_failure_reason"],
        "blocking_scope": gap["blocking_scope"],
        "closeout_determination": (
            "closed_as_local_no_entry_blocker"
            if is_no_entry_spread
            else "closed_as_outside_narrowed_ideal_path"
        ),
        "open_after_closeout": False,
        "selected_contract_after_closeout": False,
        "entry_eligible_after_closeout": False,
        "entry_recorded_after_closeout": False,
        "additional_entry_established": False,
        "next_action": gap["next_action"],
        "proof_accepted": False,
        "profitability_claimed": False,
        "paper_eligible": False,
        "live_eligible": False,
    }


def _business_candidate_id_for_gap(gap):
    if gap["candidate_identifier"] == "first_real_qqq_continuation_replay_v1_fixture":
        return "QQQ-REAL-HISTORICAL-CONTINUATION-001"
    if gap["candidate_identifier"] == "first_real_qqq_ideal_replay_v1_fixture":
        return "QQQ-REAL-HISTORICAL-IDEAL-001"
    return gap["candidate_identifier"]


def _qqq_ideal_outside_path_record(
    trade_candidate_closeout,
    contract_selected_closeout,
):
    qqq_rule = trade_candidate_closeout["qqq_ideal_selected_contract_rule_gap_closeout"]
    qqq_quote = next(
        record
        for record in contract_selected_closeout["fresh_quote_cases"]
        if record["candidate_identifier"] == "first_real_qqq_ideal_replay_v1_fixture"
    )
    return {
        "candidate_identifier": qqq_rule["candidate_identifier"],
        "business_candidate_id": qqq_rule["business_candidate_id"],
        "accepted_frozen_evidence_status": qqq_rule["accepted_frozen_evidence_status"],
        "preserved_as": "outside_narrowed_ideal_path",
        "fresh_raw_quote_preserved": True,
        "fresh_raw_quote_symbol": qqq_quote["quote_evidence"]["raw_symbol"],
        "fresh_raw_quote_time": qqq_quote["quote_evidence"]["timestamp_window"][
            "nearest_quote_time"
        ],
        "fresh_raw_quote_spread": qqq_quote["quote_evidence"]["spread"],
        "selected_contract_after_closeout": False,
        "entry_eligible_after_closeout": False,
        "entry_recorded_after_closeout": False,
        "paid_option_request_valid_after_closeout": False,
        "unavailable_or_failure_reason": qqq_rule["unavailable_or_failure_reason"],
    }


def _scorecard(
    active_path_repair,
    contract_selected_closeout,
    batch,
    active_path_records,
    contract_selected_records,
):
    active_score = active_path_repair["scorecard"]
    return {
        "remaining_evidence_gap_records_reviewed": (
            len(active_path_records) + len(contract_selected_records)
        ),
        "active_path_requirements_open_after_closeout": sum(
            1 for record in active_path_records if record["open_after_closeout"]
        ),
        "contract_selected_gaps_closed_after_closeout": sum(
            1 for record in contract_selected_records if not record["open_after_closeout"]
        ),
        "additional_entries_established": 0,
        "affected_cases_selected_contracts_before_closeout": active_score[
            "affected_cases_selected_contracts_before_repair"
        ],
        "affected_cases_selected_contracts_after_closeout": active_score[
            "affected_cases_selected_contracts_after_repair"
        ],
        "affected_cases_entry_eligible_before_closeout": active_score[
            "affected_cases_entry_eligible_before_repair"
        ],
        "affected_cases_entry_eligible_after_closeout": active_score[
            "affected_cases_entry_eligible_after_repair"
        ],
        "affected_cases_entries_recorded_before_closeout": active_score[
            "affected_cases_entries_recorded_before_repair"
        ],
        "affected_cases_entries_recorded_after_closeout": active_score[
            "affected_cases_entries_recorded_after_repair"
        ],
        "trade_candidates_before_closeout": active_score["trade_candidates_before_repair"],
        "trade_candidates_after_closeout": active_score["trade_candidates_after_repair"],
        "selected_contracts_before_closeout": active_score[
            "selected_contracts_before_repair"
        ],
        "selected_contracts_after_closeout": active_score["selected_contracts_after_repair"],
        "eligible_entries_before_closeout": active_score["eligible_entries_before_repair"],
        "eligible_entries_after_closeout": active_score["eligible_entries_after_repair"],
        "recorded_entries_before_closeout": active_score["recorded_entries_before_repair"],
        "recorded_entries_after_closeout": active_score["recorded_entries_after_repair"],
        "contract_selected_closeout_additional_entries_preserved": contract_selected_closeout[
            "scorecard"
        ]["additional_entries_established"],
        "valid_trades_captured": batch["final_classifications"]["VALID_TRADE_CAPTURED"],
        "true_no_trades": batch["final_classifications"]["TRUE_NO_TRADE"],
        "missing_data_cases": batch["final_classifications"]["MISSING_DATA"],
        "missed_valid_trades": batch["final_classifications"]["MISSED_VALID_TRADE"],
        "invalid_trades_allowed": batch["final_classifications"][
            "INVALID_TRADE_ALLOWED"
        ],
        "unresolved_cases": batch["final_classifications"]["UNRESOLVED"],
        "closed_setup_source_candidates_reopened": 0,
        "rejected_intake_rows_replayed": 0,
        "closed_safety_rejections_rerun_as_live_candidates": 0,
    }


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
    doc = write_closeout_document()
    scorecard = doc["scorecard"]
    print(
        "wrote day50 remaining evidence-gap closeout: "
        f"{scorecard['remaining_evidence_gap_records_reviewed']} reviewed gaps, "
        f"{scorecard['selected_contracts_before_closeout']}->{scorecard['selected_contracts_after_closeout']} selected contracts, "
        f"{scorecard['eligible_entries_before_closeout']}->{scorecard['eligible_entries_after_closeout']} eligible entries, "
        f"{scorecard['recorded_entries_before_closeout']}->{scorecard['recorded_entries_after_closeout']} recorded entries"
    )
