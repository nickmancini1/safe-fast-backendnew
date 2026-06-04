"""Local-only setup outcome diagnostics evaluation.

This module accepts the in-memory setup outcome proof summary only and returns
one in-memory diagnostics summary. It does not fetch data, write files, start
shadow/live workflows, emit alerts, call subprocesses, touch brokers/accounts/
options/P&L, optimize rules, or make trade decisions.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from watcher_foundation.setup_outcome_proof import (
    FORBIDDEN_SETUP_OUTCOME_FIELD_NAMES,
    SETUP_OUTCOME_DIAGNOSTIC_FIX_PATHS,
    SETUP_OUTCOME_PROOF_RESULT_FIELDS,
    SETUP_OUTCOME_PROOF_STATUSES,
)


SETUP_OUTCOME_DIAGNOSTIC_FAILURE_CATEGORIES = (
    "setup_recognition_review",
    "trigger_card_review",
    "invalidation_review",
    "fresh_stale_spent_review",
    "blocker_caution_review",
    "session_boundary_review",
    "data_quality_or_missing_evidence",
    "outcome_scoring_review",
    "lower_tier_handoff_review",
)

SETUP_OUTCOME_DIAGNOSTICS_RESULT_FIELDS = (
    "watch_only",
    "setup_outcome_diagnostics_only",
    "setup_outcome_proof_only",
    "final_viability_proven",
    "optimization_started",
    "records_processed",
    "records_accepted",
    "records_rejected",
    "diagnostic_findings",
    "diagnostics_by_setup_type",
    "diagnostic_gap_counts",
    "likely_cause_candidates",
    "next_fix_paths",
    "unavailable_evidence",
    "rejected_records",
    "proof_limited_records",
    "no_hindsight_boundary_preserved",
    "no_trade_boundary_preserved",
    "no_rule_change_started",
    "live_data_started",
    "controlled_shadow_data_started",
    "alerts_sent",
    "files_written",
    "broker_or_trade_behavior_enabled",
)

_SUMMARY_REQUIRED_FIELDS = set(SETUP_OUTCOME_PROOF_RESULT_FIELDS)

_EXPECTED_TRUE_BOUNDARY_FIELDS = (
    "watch_only",
    "setup_outcome_proof_only",
    "no_hindsight_boundary_preserved",
    "no_trade_boundary_preserved",
)

_EXPECTED_FALSE_BOUNDARY_FIELDS = (
    "final_viability_proven",
    "optimization_started",
    "live_data_started",
    "controlled_shadow_data_started",
    "alerts_sent",
    "files_written",
    "broker_or_trade_behavior_enabled",
)

_OUTCOME_STATUS_TO_TEXT = {
    "triggered_worked": "trigger evidence was present and the caller-provided outcome result state was worked",
    "triggered_failed": "trigger evidence was present and the caller-provided outcome result state was failed",
    "triggered_inconclusive": "trigger evidence was present but the caller-provided outcome result state was inconclusive or still needs review",
    "stayed_valid_pending": "the setup remained valid and fresh without a trigger in the caller-provided evidence",
    "stale_without_trigger": "the setup became stale or spent before a trigger in the caller-provided evidence",
    "invalidated_before_trigger": "invalidation was observed before a trigger in the caller-provided evidence",
    "insufficient_evidence": "source-backed after-setup evidence was missing or unavailable",
}

_REGRESSION_BY_CATEGORY = {
    "setup_recognition_review": "add or keep a setup outcome diagnostics regression that preserves setup type, symbol, stage, and evidence references",
    "trigger_card_review": "add or keep a regression for trigger evidence, trigger timestamp or level, and no-hindsight trigger handling",
    "invalidation_review": "add or keep a regression for invalidation evidence before trigger and invalidation-level ambiguity",
    "fresh_stale_spent_review": "add or keep a regression for fresh, stale, and spent setup outcome transitions",
    "blocker_caution_review": "add or keep a regression for blocker/caution evidence affecting setup outcome diagnostics",
    "session_boundary_review": "add or keep a regression for session-boundary evidence and outcome-window handling",
    "data_quality_or_missing_evidence": "add or keep a regression that carries unavailable proof fields into missing-evidence diagnostics",
    "outcome_scoring_review": "add or keep a regression for triggered worked, failed, and inconclusive setup outcomes",
    "lower_tier_handoff_review": "add or keep a regression that preserves rejected proof reasons and requires lower-tier handoff",
}


def evaluate_setup_outcome_diagnostics(
    proof_summary: dict[str, Any],
) -> dict[str, Any]:
    """Return an in-memory setup outcome diagnostics summary."""
    if type(proof_summary) is not dict:
        raise TypeError(
            "Setup outcome diagnostics proof_summary must be a dict"
        )

    _validate_proof_summary(proof_summary)

    diagnostic_findings = []
    diagnostics_by_setup_type: dict[str, dict[str, list[dict[str, Any]]]] = {}
    unavailable_evidence = _collect_unavailable_evidence(proof_summary)

    for setup_type, records_by_symbol in proof_summary[
        "accepted_records_by_setup_type"
    ].items():
        if type(records_by_symbol) is not dict:
            raise TypeError(
                "Setup outcome diagnostics accepted_records_by_setup_type values "
                "must be dicts keyed by symbol"
            )
        diagnostics_by_setup_type.setdefault(str(setup_type), {})
        for symbol, records in records_by_symbol.items():
            if type(records) is not list:
                raise TypeError(
                    "Setup outcome diagnostics accepted symbol records must be lists"
                )
            diagnostics_by_setup_type[str(setup_type)].setdefault(str(symbol), [])
            for record in records:
                finding = _diagnostic_finding_for_record(record)
                diagnostic_findings.append(finding)
                diagnostics_by_setup_type[str(setup_type)][str(symbol)].append(
                    deepcopy(finding)
                )

    if proof_summary["rejected_records"]:
        diagnostic_findings.append(
            _rejected_records_finding(proof_summary["rejected_records"])
        )

    diagnostic_gap_counts = {
        category: 0 for category in SETUP_OUTCOME_DIAGNOSTIC_FAILURE_CATEGORIES
    }
    likely_cause_candidates = []
    next_fix_paths = {}
    for finding in diagnostic_findings:
        category = finding["diagnostic_category"]
        diagnostic_gap_counts[category] += 1
        likely_cause_candidates.extend(deepcopy(finding["likely_cause_candidates"]))
        next_fix_paths[category] = SETUP_OUTCOME_DIAGNOSTIC_FIX_PATHS[category]

    return {
        "watch_only": True,
        "setup_outcome_diagnostics_only": True,
        "setup_outcome_proof_only": True,
        "final_viability_proven": False,
        "optimization_started": False,
        "records_processed": proof_summary["records_processed"],
        "records_accepted": proof_summary["records_accepted"],
        "records_rejected": proof_summary["records_rejected"],
        "diagnostic_findings": deepcopy(diagnostic_findings),
        "diagnostics_by_setup_type": deepcopy(diagnostics_by_setup_type),
        "diagnostic_gap_counts": diagnostic_gap_counts,
        "likely_cause_candidates": likely_cause_candidates,
        "next_fix_paths": next_fix_paths,
        "unavailable_evidence": unavailable_evidence,
        "rejected_records": deepcopy(proof_summary["rejected_records"]),
        "proof_limited_records": deepcopy(proof_summary["proof_limited_records"]),
        "no_hindsight_boundary_preserved": True,
        "no_trade_boundary_preserved": True,
        "no_rule_change_started": True,
        "live_data_started": False,
        "controlled_shadow_data_started": False,
        "alerts_sent": False,
        "files_written": False,
        "broker_or_trade_behavior_enabled": False,
    }


def _validate_proof_summary(proof_summary: Mapping[str, Any]) -> None:
    _reject_forbidden_diagnostic_fields(proof_summary, path=())

    missing_fields = [
        field_name
        for field_name in SETUP_OUTCOME_PROOF_RESULT_FIELDS
        if field_name not in proof_summary
    ]
    if missing_fields:
        raise ValueError(
            "Missing required setup outcome proof summary fields: "
            + ", ".join(missing_fields)
        )

    for field_name in _EXPECTED_TRUE_BOUNDARY_FIELDS:
        if proof_summary[field_name] is not True:
            raise ValueError(
                f"Setup outcome diagnostics requires {field_name}=True"
            )
    for field_name in _EXPECTED_FALSE_BOUNDARY_FIELDS:
        if proof_summary[field_name] is not False:
            raise ValueError(
                f"Setup outcome diagnostics requires {field_name}=False"
            )

    if type(proof_summary["accepted_records_by_setup_type"]) is not dict:
        raise TypeError(
            "Setup outcome diagnostics accepted_records_by_setup_type must be a dict"
        )
    if type(proof_summary["rejected_records"]) is not list:
        raise TypeError("Setup outcome diagnostics rejected_records must be a list")
    if type(proof_summary["proof_limited_records"]) is not list:
        raise TypeError(
            "Setup outcome diagnostics proof_limited_records must be a list"
        )
    if type(proof_summary["outcome_status_counts"]) is not dict:
        raise TypeError(
            "Setup outcome diagnostics outcome_status_counts must be a dict"
        )
    if set(proof_summary["outcome_status_counts"]) != set(
        SETUP_OUTCOME_PROOF_STATUSES
    ):
        raise ValueError(
            "Setup outcome diagnostics outcome_status_counts must include every "
            "setup outcome proof status"
        )

    for records_by_symbol in proof_summary["accepted_records_by_setup_type"].values():
        if type(records_by_symbol) is not dict:
            raise TypeError(
                "Setup outcome diagnostics accepted_records_by_setup_type values "
                "must be dicts"
            )
        for records in records_by_symbol.values():
            if type(records) is not list:
                raise TypeError(
                    "Setup outcome diagnostics accepted record groups must be lists"
                )
            for index, record in enumerate(records):
                _validate_accepted_record_boundaries(record, index)


def _validate_accepted_record_boundaries(record: Any, index: int) -> None:
    if type(record) is not dict:
        raise TypeError(
            f"Setup outcome diagnostics accepted record {index} must be a dict"
        )
    if record.get("watch_only") is not True:
        raise ValueError(
            f"Setup outcome diagnostics accepted record {index} must preserve "
            "watch_only=True"
        )
    if record.get("outcome_status") not in SETUP_OUTCOME_PROOF_STATUSES:
        raise ValueError(
            f"Setup outcome diagnostics accepted record {index} has unsupported "
            "outcome_status"
        )
    _validate_no_trade_boundary(record.get("no_trade_boundary"), index)
    _validate_no_hindsight_boundary(record.get("no_hindsight_boundary"), index)


def _validate_no_trade_boundary(boundary: Any, index: int) -> None:
    if type(boundary) is not dict:
        raise TypeError(
            f"Setup outcome diagnostics accepted record {index}.no_trade_boundary "
            "must be a dict"
        )
    for field_name in (
        "no_trade",
        "no_broker",
        "no_order",
        "no_account_sizing",
        "no_option_pnl",
        "no_live_trade_decision",
    ):
        if boundary.get(field_name) is not True:
            raise ValueError(
                f"Setup outcome diagnostics accepted record {index}."
                f"no_trade_boundary must set {field_name}=True"
            )
    for field_name in (
        "broker_enabled",
        "orders_enabled",
        "account_sizing_enabled",
        "option_pnl_enabled",
        "live_trade_decision_enabled",
    ):
        if boundary.get(field_name) is not False:
            raise ValueError(
                f"Setup outcome diagnostics accepted record {index}."
                f"no_trade_boundary must set {field_name}=False"
            )


def _validate_no_hindsight_boundary(boundary: Any, index: int) -> None:
    if type(boundary) is not dict:
        raise TypeError(
            f"Setup outcome diagnostics accepted record {index}.no_hindsight_boundary "
            "must be a dict"
        )
    for field_name in (
        "setup_identity_frozen_before_outcome_scan",
        "future_evidence_not_used_to_define_setup",
        "no_backfilled_outcome_labels",
    ):
        if boundary.get(field_name) is not True:
            raise ValueError(
                f"Setup outcome diagnostics accepted record {index}."
                f"no_hindsight_boundary must set {field_name}=True"
            )


def _diagnostic_finding_for_record(record: Mapping[str, Any]) -> dict[str, Any]:
    proof_limited_fields = _proof_limited_fields(record)
    unavailable_items = _record_unavailable_items(record)
    category = _diagnostic_category(record, proof_limited_fields, unavailable_items)
    outcome_status = record["outcome_status"]
    evidence_used = _evidence_used(record)
    relationship = _relationship(record)
    lower_tier_handoff_required = _lower_tier_handoff_required(
        category,
        record,
        proof_limited_fields,
        unavailable_items,
    )

    return {
        "diagnostic_category": category,
        "record_id": record.get("proof_record_id", "UNAVAILABLE"),
        "outcome_status": outcome_status,
        "what_happened": _OUTCOME_STATUS_TO_TEXT[outcome_status],
        "evidence_supports": {
            "evidence_refs": deepcopy(evidence_used),
            "outcome_evidence_state": record.get("outcome_evidence_state"),
            "outcome_result_state": record.get("outcome_result_state"),
            "after_setup_evidence": deepcopy(record.get("after_setup_evidence", {})),
        },
        "affected_setup_type": record.get("setup_type", _unavailable_field("setup_type")),
        "affected_symbol": record.get("symbol", _unavailable_field("symbol")),
        "affected_stage": record.get("stage", _unavailable_field("stage")),
        "trigger_invalidation_freshness_relationship": relationship,
        "session_boundary_state": record.get("session_boundary_state"),
        "blocker_caution_state": record.get("blocker_caution_state"),
        "evidence_used": deepcopy(evidence_used),
        "unavailable_evidence": deepcopy(unavailable_items),
        "proof_limited_fields": deepcopy(proof_limited_fields),
        "likely_cause_candidates": [
            {
                "label": "candidate",
                "candidate": _candidate_text(category, outcome_status),
                "evidence_basis": {
                    "outcome_status": outcome_status,
                    "relationship": deepcopy(relationship),
                    "proof_limited_fields": deepcopy(proof_limited_fields),
                    "unavailable_evidence": deepcopy(unavailable_items),
                    "evidence_refs": deepcopy(evidence_used),
                },
            }
        ],
        "affected_system_area": category,
        "next_fix_path": SETUP_OUTCOME_DIAGNOSTIC_FIX_PATHS[category],
        "regression_needed": _REGRESSION_BY_CATEGORY[category],
        "lower_tier_handoff_required": lower_tier_handoff_required,
        "proof_limited_reason": _proof_limited_reason(
            proof_limited_fields,
            unavailable_items,
        ),
    }


def _diagnostic_category(
    record: Mapping[str, Any],
    proof_limited_fields: list[Any],
    unavailable_items: list[Any],
) -> str:
    outcome_status = record["outcome_status"]
    unavailable_names = _item_field_names(unavailable_items) | _item_field_names(
        proof_limited_fields
    )

    if outcome_status == "insufficient_evidence":
        return "data_quality_or_missing_evidence"
    if "source_row_reference" in unavailable_names or "post_setup_evidence" in unavailable_names:
        return "data_quality_or_missing_evidence"
    if "trigger_level" in unavailable_names or "trigger_timestamp" in unavailable_names:
        return "trigger_card_review"
    if (
        "invalidation_level" in unavailable_names
        or "invalidation_timestamp" in unavailable_names
        or outcome_status == "invalidated_before_trigger"
    ):
        return "invalidation_review"
    if outcome_status == "stale_without_trigger":
        return "fresh_stale_spent_review"
    if _normalized(record.get("blocker_caution_state")) == "blocked":
        return "blocker_caution_review"
    if _normalized(record.get("session_boundary_state")) in {"blocked", "needs_review"}:
        return "session_boundary_review"
    if outcome_status in {
        "triggered_worked",
        "triggered_failed",
        "triggered_inconclusive",
    }:
        return "outcome_scoring_review"
    return "setup_recognition_review"


def _candidate_text(category: str, outcome_status: str) -> str:
    category_text = category.replace("_", " ")
    outcome_text = outcome_status.replace("_", " ")
    return (
        f"candidate: {category_text} may explain or limit {outcome_text}; "
        "verify against the listed evidence before changing rules"
    )


def _lower_tier_handoff_required(
    category: str,
    record: Mapping[str, Any],
    proof_limited_fields: list[Any],
    unavailable_items: list[Any],
) -> bool:
    if category in {"data_quality_or_missing_evidence", "lower_tier_handoff_review"}:
        return True
    if proof_limited_fields or unavailable_items:
        return True
    if category in {"trigger_card_review", "invalidation_review", "fresh_stale_spent_review"}:
        return True
    if _normalized(record.get("blocker_caution_state")) in {"blocked", "needs_review"}:
        return True
    if _normalized(record.get("session_boundary_state")) in {"blocked", "needs_review"}:
        return True
    return False


def _collect_unavailable_evidence(proof_summary: Mapping[str, Any]) -> list[Any]:
    unavailable_evidence = []
    unavailable_evidence.extend(deepcopy(proof_summary["proof_limited_records"]))
    for records_by_symbol in proof_summary["accepted_records_by_setup_type"].values():
        if type(records_by_symbol) is dict:
            for records in records_by_symbol.values():
                if type(records) is list:
                    for record in records:
                        if type(record) is dict:
                            unavailable_evidence.extend(_record_unavailable_items(record))
    return unavailable_evidence


def _record_unavailable_items(record: Mapping[str, Any]) -> list[Any]:
    unavailable_items = []
    unavailable_fields = record.get("unavailable_fields")
    if type(unavailable_fields) is list:
        unavailable_items.extend(deepcopy(unavailable_fields))
    elif type(unavailable_fields) is dict:
        for field_name, item in unavailable_fields.items():
            copied_item = deepcopy(item) if type(item) is dict else {"value": item}
            copied_item["field_name"] = str(field_name)
            unavailable_items.append(copied_item)

    if not _evidence_used(record):
        unavailable_items.append(
            {
                "field_name": "evidence_refs",
                "status": "missing_evidence",
                "reason": "no evidence_refs were present for this diagnostic finding",
            }
        )
    return unavailable_items


def _proof_limited_fields(record: Mapping[str, Any]) -> list[Any]:
    fields = record.get("proof_limited_fields")
    if type(fields) is list:
        return deepcopy(fields)
    return []


def _proof_limited_reason(
    proof_limited_fields: list[Any],
    unavailable_items: list[Any],
) -> Any:
    if not proof_limited_fields and not unavailable_items:
        return "not proof-limited by the caller-provided setup outcome summary"
    return {
        "proof_limited_fields": deepcopy(proof_limited_fields),
        "unavailable_evidence": deepcopy(unavailable_items),
    }


def _evidence_used(record: Mapping[str, Any]) -> list[Any]:
    evidence_refs = record.get("evidence_refs")
    if type(evidence_refs) is list:
        return deepcopy(evidence_refs)
    return []


def _relationship(record: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "trigger_state": record.get("trigger_state", _unavailable_field("trigger_state")),
        "invalidation_state": record.get(
            "invalidation_state",
            _unavailable_field("invalidation_state"),
        ),
        "freshness_state": record.get(
            "freshness_state",
            _unavailable_field("freshness_state"),
        ),
        "blocker_caution_state": record.get(
            "blocker_caution_state",
            _unavailable_field("blocker_caution_state"),
        ),
        "session_boundary_state": record.get(
            "session_boundary_state",
            _unavailable_field("session_boundary_state"),
        ),
    }


def _rejected_records_finding(rejected_records: list[Any]) -> dict[str, Any]:
    return {
        "diagnostic_category": "lower_tier_handoff_review",
        "record_id": "SUMMARY",
        "outcome_status": "insufficient_evidence",
        "what_happened": "one or more setup outcome proof records were rejected before diagnostics could use them",
        "evidence_supports": {"rejected_records": deepcopy(rejected_records)},
        "affected_setup_type": _unavailable_field("setup_type"),
        "affected_symbol": _unavailable_field("symbol"),
        "affected_stage": _unavailable_field("stage"),
        "trigger_invalidation_freshness_relationship": {
            "trigger_state": _unavailable_field("trigger_state"),
            "invalidation_state": _unavailable_field("invalidation_state"),
            "freshness_state": _unavailable_field("freshness_state"),
            "blocker_caution_state": _unavailable_field("blocker_caution_state"),
            "session_boundary_state": _unavailable_field("session_boundary_state"),
        },
        "session_boundary_state": "unavailable_evidence",
        "blocker_caution_state": "unavailable_evidence",
        "evidence_used": deepcopy(rejected_records),
        "unavailable_evidence": [],
        "proof_limited_fields": [],
        "likely_cause_candidates": [
            {
                "label": "candidate",
                "candidate": "candidate: rejected setup outcome proof records need lower-tier contract or fixture review",
                "evidence_basis": deepcopy(rejected_records),
            }
        ],
        "affected_system_area": "lower_tier_handoff_review",
        "next_fix_path": SETUP_OUTCOME_DIAGNOSTIC_FIX_PATHS[
            "lower_tier_handoff_review"
        ],
        "regression_needed": _REGRESSION_BY_CATEGORY["lower_tier_handoff_review"],
        "lower_tier_handoff_required": True,
        "proof_limited_reason": "rejected setup outcome proof records cannot support diagnostics until lower-tier validation is fixed",
    }


def _item_field_names(items: list[Any]) -> set[str]:
    field_names = set()
    for item in items:
        if type(item) is dict and type(item.get("field_name")) is str:
            field_names.add(item["field_name"])
    return field_names


def _unavailable_field(field_name: str) -> dict[str, str]:
    return {
        "field_name": field_name,
        "status": "unavailable_evidence",
        "reason": "field not available in setup outcome diagnostics evidence",
    }


def _reject_forbidden_diagnostic_fields(value: Any, path: tuple[str, ...]) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            normalized_key = key_text.lower()
            if (
                normalized_key in FORBIDDEN_SETUP_OUTCOME_FIELD_NAMES
                and normalized_key not in _SUMMARY_REQUIRED_FIELDS
                and not _is_preserved_no_trade_boundary_field(normalized_key, path)
            ):
                dotted_path = ".".join((*path, key_text))
                raise ValueError(f"Forbidden execution/trade field: {dotted_path}")
            _reject_forbidden_diagnostic_fields(nested_value, (*path, key_text))
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            _reject_forbidden_diagnostic_fields(nested_value, (*path, str(index)))


def _is_preserved_no_trade_boundary_field(
    normalized_key: str,
    path: tuple[str, ...],
) -> bool:
    if not path or path[-1] != "no_trade_boundary":
        return False
    return normalized_key in {
        "broker_enabled",
        "orders_enabled",
        "account_sizing_enabled",
        "option_pnl_enabled",
        "live_trade_decision_enabled",
    }


def _normalized(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().lower().replace("-", "_").replace(" ", "_").replace("/", "_")
