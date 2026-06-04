"""Local-only setup outcome proof evaluation.

This module accepts caller-provided in-memory setup outcome proof records only.
It does not fetch data, write files, start shadow/live workflows, emit alerts,
call subprocesses, touch brokers/accounts/options/P&L, or make trade decisions.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from watcher_foundation.constants import (
    ACCEPTED_SETUP_TYPES,
    ACCEPTED_STAGES,
    FORBIDDEN_EXECUTION_FIELD_NAMES,
)
from watcher_foundation.day60_outcome_scoring_contract import (
    FABRICATED_PROOF_MARKERS,
)


SETUP_OUTCOME_PROOF_REQUIRED_FIELDS = (
    "proof_record_id",
    "source_record_id",
    "setup_id",
    "setup_type",
    "symbol",
    "timeframe",
    "stage",
    "detection_timestamp",
    "frozen_setup_identity",
    "setup_evidence_refs",
    "after_setup_evidence",
    "trigger_state",
    "invalidation_state",
    "freshness_state",
    "blocker_caution_state",
    "session_boundary_state",
    "outcome_evidence_state",
    "outcome_result_state",
    "evidence_refs",
    "unavailable_fields",
    "diagnostic_placeholders",
    "no_hindsight_boundary",
    "no_trade_boundary",
    "watch_only",
)

SETUP_OUTCOME_PROOF_STATUSES = (
    "triggered_worked",
    "triggered_failed",
    "triggered_inconclusive",
    "stayed_valid_pending",
    "stale_without_trigger",
    "invalidated_before_trigger",
    "insufficient_evidence",
)

SETUP_OUTCOME_RULE_STATES = (
    "valid_by_rule",
    "missing_evidence",
    "inconclusive",
    "unavailable_evidence",
    "blocked",
    "stale",
    "spent",
    "invalidated",
    "needs_review",
    "triggered",
    "not_triggered",
    "worked",
    "failed",
    "pending",
    "fresh",
    "rebuilding",
    "prior_session",
    "none",
)

SETUP_OUTCOME_PROOF_RESULT_FIELDS = (
    "watch_only",
    "setup_outcome_proof_only",
    "final_viability_proven",
    "optimization_started",
    "records_processed",
    "records_accepted",
    "records_rejected",
    "accepted_records_by_setup_type",
    "rejected_records",
    "outcome_status_counts",
    "proof_limited_records",
    "diagnostic_findings",
    "next_fix_paths",
    "no_hindsight_boundary_preserved",
    "no_trade_boundary_preserved",
    "live_data_started",
    "controlled_shadow_data_started",
    "alerts_sent",
    "files_written",
    "broker_or_trade_behavior_enabled",
)

SETUP_OUTCOME_DIAGNOSTIC_FIX_PATHS = {
    "setup_recognition_review": "review frozen setup identity and setup evidence references",
    "trigger_card_review": "review trigger evidence and trigger-state contract",
    "invalidation_review": "review invalidation evidence before any rule change",
    "fresh_stale_spent_review": "review freshness, stale, and spent-state evidence",
    "blocker_caution_review": "review blocker and caution evidence against outcome evidence",
    "session_boundary_review": "review session-boundary and outcome-window evidence",
    "data_quality_or_missing_evidence": "collect or preserve missing source-backed setup outcome evidence",
    "outcome_scoring_review": "review setup outcome labels, terminal evidence, and tests",
    "lower_tier_handoff_review": "return to the smallest responsible local contract, fixture, or test before optimization",
}

PROOF_LIMITING_FIELDS = (
    "trigger_level",
    "invalidation_level",
    "trigger_timestamp",
    "invalidation_timestamp",
    "source_row_reference",
    "post_setup_evidence",
    "freshness_state",
)

VAGUE_OUTCOME_LABELS = (
    "good",
    "bad",
    "weak",
    "strong",
    "success",
    "failure",
    "worked ok",
    "failed setup",
    "bad trade",
)

FORBIDDEN_SETUP_OUTCOME_FIELD_NAMES = (
    FORBIDDEN_EXECUTION_FIELD_NAMES
    | frozenset(
        {
            "approved_trade",
            "approved_trades",
            "auto_trade",
            "auto_trading",
            "broker_call",
            "broker_order",
            "buy",
            "live_trade",
            "live_trade_approval",
            "live_trade_decision",
            "option_pnl",
            "options",
            "order",
            "orders",
            "p&l",
            "p_and_l",
            "p_l",
            "pl",
            "sell",
            "trade",
            "trade_approval",
            "trade_decision",
            "trade_decisions",
        }
    )
)


def evaluate_setup_outcome_proof(
    records: list[dict[str, Any]],
) -> dict[str, Any]:
    """Evaluate caller-provided setup outcome proof records in memory."""
    if type(records) is not list:
        raise TypeError("Setup outcome proof records must be a list")

    accepted_records_by_setup_type: dict[str, dict[str, list[dict[str, Any]]]] = {}
    rejected_records = []
    proof_limited_records = []
    diagnostic_findings = []
    outcome_status_counts = {status: 0 for status in SETUP_OUTCOME_PROOF_STATUSES}

    for index, record in enumerate(records):
        record_id = _extract_record_id(record)
        try:
            accepted_record = validate_setup_outcome_proof_record(record)
        except (TypeError, ValueError) as exc:
            rejected_records.append(
                {
                    "index": index,
                    "record_id": record_id,
                    "reason": str(exc),
                }
            )
            continue

        outcome_status = _classify_outcome_status(accepted_record)
        proof_limited_fields = _proof_limited_fields(accepted_record)
        diagnostic = _build_diagnostic_finding(
            accepted_record,
            outcome_status,
            proof_limited_fields,
        )
        accepted_record["outcome_status"] = outcome_status
        accepted_record["proof_limited"] = bool(proof_limited_fields)
        accepted_record["proof_limited_fields"] = proof_limited_fields
        accepted_record["diagnostic_finding"] = deepcopy(diagnostic)

        accepted_records_by_setup_type.setdefault(accepted_record["setup_type"], {})
        accepted_records_by_setup_type[accepted_record["setup_type"]].setdefault(
            accepted_record["symbol"], []
        )
        accepted_records_by_setup_type[accepted_record["setup_type"]][
            accepted_record["symbol"]
        ].append(deepcopy(accepted_record))
        outcome_status_counts[outcome_status] += 1
        diagnostic_findings.append(diagnostic)

        if proof_limited_fields:
            proof_limited_records.append(
                {
                    "record_id": accepted_record["proof_record_id"],
                    "setup_type": accepted_record["setup_type"],
                    "symbol": accepted_record["symbol"],
                    "proof_limited_fields": deepcopy(proof_limited_fields),
                    "outcome_status": outcome_status,
                }
            )

    next_fix_paths = {
        finding["diagnostic_category"]: SETUP_OUTCOME_DIAGNOSTIC_FIX_PATHS[
            finding["diagnostic_category"]
        ]
        for finding in diagnostic_findings
    }
    if rejected_records:
        diagnostic_findings.append(_rejected_records_finding(rejected_records))
        next_fix_paths["lower_tier_handoff_review"] = SETUP_OUTCOME_DIAGNOSTIC_FIX_PATHS[
            "lower_tier_handoff_review"
        ]

    return {
        "watch_only": True,
        "setup_outcome_proof_only": True,
        "final_viability_proven": False,
        "optimization_started": False,
        "records_processed": len(records),
        "records_accepted": sum(
            len(symbol_records)
            for setup_records in accepted_records_by_setup_type.values()
            for symbol_records in setup_records.values()
        ),
        "records_rejected": len(rejected_records),
        "accepted_records_by_setup_type": deepcopy(accepted_records_by_setup_type),
        "rejected_records": deepcopy(rejected_records),
        "outcome_status_counts": outcome_status_counts,
        "proof_limited_records": deepcopy(proof_limited_records),
        "diagnostic_findings": deepcopy(diagnostic_findings),
        "next_fix_paths": next_fix_paths,
        "no_hindsight_boundary_preserved": True,
        "no_trade_boundary_preserved": True,
        "live_data_started": False,
        "controlled_shadow_data_started": False,
        "alerts_sent": False,
        "files_written": False,
        "broker_or_trade_behavior_enabled": False,
    }


def validate_setup_outcome_proof_record(record: dict[str, Any]) -> dict[str, Any]:
    """Return a defensive copy of a valid setup outcome proof record."""
    if type(record) is not dict:
        raise TypeError("Setup outcome proof record must be a dict")

    _reject_forbidden_setup_outcome_fields(record, path=())
    _reject_fabricated_proof_values(record, path=())
    _reject_vague_labels(record, path=())

    missing_fields = [
        field_name for field_name in SETUP_OUTCOME_PROOF_REQUIRED_FIELDS if field_name not in record
    ]
    if missing_fields:
        raise ValueError(
            "Missing required setup outcome proof fields: "
            + ", ".join(missing_fields)
        )

    for field_name in (
        "proof_record_id",
        "source_record_id",
        "setup_id",
        "setup_type",
        "symbol",
        "timeframe",
        "stage",
        "detection_timestamp",
    ):
        _require_string(record, field_name)

    if record["setup_type"] not in ACCEPTED_SETUP_TYPES:
        raise ValueError(f"Unsupported setup_type: {record['setup_type']}")
    if record["stage"] not in ACCEPTED_STAGES:
        raise ValueError(f"Unsupported stage: {record['stage']}")
    if record["watch_only"] is not True:
        raise ValueError("Setup outcome proof records must preserve watch_only=True")

    _validate_frozen_setup_identity(record)
    _validate_after_setup_evidence(record)
    _validate_list_of_strings(record["setup_evidence_refs"], "setup_evidence_refs")
    _validate_list_of_strings(record["evidence_refs"], "evidence_refs")
    _validate_unavailable_fields(record["unavailable_fields"])
    _validate_state(record["trigger_state"], "trigger_state")
    _validate_state(record["invalidation_state"], "invalidation_state")
    _validate_state(record["freshness_state"], "freshness_state")
    _validate_state(record["blocker_caution_state"], "blocker_caution_state")
    _validate_state(record["session_boundary_state"], "session_boundary_state")
    _validate_state(record["outcome_evidence_state"], "outcome_evidence_state")
    _validate_state(record["outcome_result_state"], "outcome_result_state")
    _validate_diagnostic_placeholders(record["diagnostic_placeholders"])
    _validate_no_hindsight_boundary(record["no_hindsight_boundary"])
    _validate_no_trade_boundary(record["no_trade_boundary"])

    return deepcopy(dict(record))


def _classify_outcome_status(record: Mapping[str, Any]) -> str:
    trigger_state = _normalized(record["trigger_state"])
    invalidation_state = _normalized(record["invalidation_state"])
    freshness_state = _normalized(record["freshness_state"])
    outcome_evidence_state = _normalized(record["outcome_evidence_state"])
    outcome_result_state = _normalized(record["outcome_result_state"])

    unavailable_field_names = _unavailable_field_names(record["unavailable_fields"])
    if (
        outcome_evidence_state in {"missing_evidence", "unavailable_evidence"}
        or "post_setup_evidence" in unavailable_field_names
        or "source_row_reference" in unavailable_field_names
    ):
        return "insufficient_evidence"
    if invalidation_state == "invalidated" and trigger_state != "triggered":
        return "invalidated_before_trigger"
    if freshness_state in {"stale", "spent"} and trigger_state != "triggered":
        return "stale_without_trigger"
    if trigger_state == "triggered" and outcome_result_state == "worked":
        return "triggered_worked"
    if trigger_state == "triggered" and outcome_result_state == "failed":
        return "triggered_failed"
    if trigger_state == "triggered" and outcome_result_state in {
        "inconclusive",
        "needs_review",
        "pending",
        "missing_evidence",
        "unavailable_evidence",
    }:
        return "triggered_inconclusive"
    if (
        trigger_state in {"not_triggered", "pending", "needs_review"}
        and invalidation_state in {"valid_by_rule", "none", "pending"}
        and freshness_state in {"valid_by_rule", "fresh", "rebuilding", "prior_session"}
    ):
        return "stayed_valid_pending"
    return "insufficient_evidence"


def _proof_limited_fields(record: Mapping[str, Any]) -> list[dict[str, Any]]:
    unavailable_names = _unavailable_field_names(record["unavailable_fields"])
    limiting_fields = []
    for field_name in PROOF_LIMITING_FIELDS:
        if field_name in unavailable_names:
            limiting_fields.append(
                {
                    "field_name": field_name,
                    "state": "unavailable_evidence",
                    "reason": _unavailable_reason(record["unavailable_fields"], field_name),
                }
            )

    after_setup_evidence = record["after_setup_evidence"]
    for field_name in ("source_row_reference", "post_setup_evidence"):
        if field_name not in after_setup_evidence:
            limiting_fields.append(
                {
                    "field_name": field_name,
                    "state": "missing_evidence",
                    "reason": "after_setup_evidence did not include this field",
                }
            )
    return limiting_fields


def _build_diagnostic_finding(
    record: Mapping[str, Any],
    outcome_status: str,
    proof_limited_fields: list[dict[str, Any]],
) -> dict[str, Any]:
    category = _diagnostic_category(outcome_status, record, proof_limited_fields)
    return {
        "diagnostic_category": category,
        "record_id": record["proof_record_id"],
        "outcome_status": outcome_status,
        "affected_setup_type": record["setup_type"],
        "affected_symbol": record["symbol"],
        "affected_stage": record["stage"],
        "trigger_invalidation_freshness_relationship": {
            "trigger_state": record["trigger_state"],
            "invalidation_state": record["invalidation_state"],
            "freshness_state": record["freshness_state"],
            "session_boundary_state": record["session_boundary_state"],
        },
        "evidence_used": deepcopy(record["evidence_refs"]),
        "unavailable_evidence": deepcopy(record["unavailable_fields"]),
        "proof_limited_fields": deepcopy(proof_limited_fields),
        "likely_cause_candidates": [
            {
                "label": "candidate",
                "candidate": _candidate_text(category, outcome_status),
                "evidence_basis": {
                    "outcome_status": outcome_status,
                    "proof_limited_fields": deepcopy(proof_limited_fields),
                    "evidence_refs": deepcopy(record["evidence_refs"]),
                },
            }
        ],
        "next_fix_path": SETUP_OUTCOME_DIAGNOSTIC_FIX_PATHS[category],
        "lower_tier_handoff_required": category
        in {"data_quality_or_missing_evidence", "lower_tier_handoff_review"},
    }


def _diagnostic_category(
    outcome_status: str,
    record: Mapping[str, Any],
    proof_limited_fields: list[dict[str, Any]],
) -> str:
    if proof_limited_fields or outcome_status == "insufficient_evidence":
        return "data_quality_or_missing_evidence"
    if outcome_status == "invalidated_before_trigger":
        return "invalidation_review"
    if outcome_status == "stale_without_trigger":
        return "fresh_stale_spent_review"
    if outcome_status == "triggered_failed":
        return "outcome_scoring_review"
    if outcome_status == "triggered_inconclusive":
        return "outcome_scoring_review"
    if _normalized(record["blocker_caution_state"]) == "blocked":
        return "blocker_caution_review"
    if _normalized(record["session_boundary_state"]) in {"blocked", "needs_review"}:
        return "session_boundary_review"
    return "setup_recognition_review"


def _candidate_text(category: str, outcome_status: str) -> str:
    return (
        "candidate: "
        + category.replace("_", " ")
        + f" may need review for outcome status {outcome_status}"
    )


def _rejected_records_finding(rejected_records: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "diagnostic_category": "lower_tier_handoff_review",
        "record_id": "SUMMARY",
        "outcome_status": "insufficient_evidence",
        "affected_setup_type": {
            "field_name": "setup_type",
            "status": "unavailable_evidence",
            "reason": "rejected record summary",
        },
        "affected_symbol": {
            "field_name": "symbol",
            "status": "unavailable_evidence",
            "reason": "rejected record summary",
        },
        "affected_stage": {
            "field_name": "stage",
            "status": "unavailable_evidence",
            "reason": "rejected record summary",
        },
        "trigger_invalidation_freshness_relationship": {
            "trigger_state": "unavailable_evidence",
            "invalidation_state": "unavailable_evidence",
            "freshness_state": "unavailable_evidence",
            "session_boundary_state": "unavailable_evidence",
        },
        "evidence_used": deepcopy(rejected_records),
        "unavailable_evidence": [],
        "proof_limited_fields": [],
        "likely_cause_candidates": [
            {
                "label": "candidate",
                "candidate": "candidate: rejected setup outcome proof records need lower-tier contract review",
                "evidence_basis": deepcopy(rejected_records),
            }
        ],
        "next_fix_path": SETUP_OUTCOME_DIAGNOSTIC_FIX_PATHS[
            "lower_tier_handoff_review"
        ],
        "lower_tier_handoff_required": True,
    }


def _validate_frozen_setup_identity(record: Mapping[str, Any]) -> None:
    identity = record["frozen_setup_identity"]
    if type(identity) is not dict:
        raise TypeError("Setup outcome proof frozen_setup_identity must be a dict")
    if identity.get("caller_provided") is not True:
        raise ValueError(
            "Setup outcome proof frozen_setup_identity must set caller_provided=True"
        )
    if identity.get("frozen_before_outcome_scan") is not True:
        raise ValueError(
            "Setup outcome proof requires frozen setup identity before outcome scan"
        )
    if identity.get("setup_id") != record["setup_id"]:
        raise ValueError("Setup outcome proof frozen_setup_identity setup_id mismatch")
    if identity.get("setup_type") != record["setup_type"]:
        raise ValueError(
            "Setup outcome proof frozen_setup_identity setup_type mismatch"
        )
    if identity.get("symbol") != record["symbol"]:
        raise ValueError("Setup outcome proof frozen_setup_identity symbol mismatch")
    frozen_timestamp = identity.get("frozen_timestamp")
    if type(frozen_timestamp) is not str or not frozen_timestamp:
        raise ValueError(
            "Setup outcome proof frozen_setup_identity must include frozen_timestamp"
        )
    if frozen_timestamp > record["detection_timestamp"]:
        raise ValueError(
            "Setup outcome proof frozen_setup_identity must not be frozen after detection_timestamp"
        )


def _validate_after_setup_evidence(record: Mapping[str, Any]) -> None:
    evidence = record["after_setup_evidence"]
    if type(evidence) is not dict:
        raise TypeError("Setup outcome proof after_setup_evidence must be a dict")
    if evidence.get("caller_provided") is not True:
        raise ValueError(
            "Setup outcome proof after_setup_evidence must set caller_provided=True"
        )
    if evidence.get("future_evidence_used_to_define_setup") is True:
        raise ValueError(
            "Setup outcome proof must not use future evidence to define the original setup"
        )
    start_timestamp = evidence.get("start_timestamp")
    if type(start_timestamp) is not str or not start_timestamp:
        raise ValueError(
            "Setup outcome proof after_setup_evidence must include start_timestamp"
        )
    if start_timestamp < record["detection_timestamp"]:
        raise ValueError(
            "Setup outcome proof after_setup_evidence must start after detection_timestamp"
        )


def _validate_state(value: Any, field_name: str) -> None:
    if type(value) is not str or not value:
        raise TypeError(f"Setup outcome proof {field_name} must be a non-empty string")
    if _normalized(value) not in SETUP_OUTCOME_RULE_STATES:
        raise ValueError(f"Unsupported {field_name}: {value}")


def _validate_diagnostic_placeholders(placeholders: Any) -> None:
    if type(placeholders) is not dict:
        raise TypeError("Setup outcome proof diagnostic_placeholders must be a dict")
    if type(placeholders.get("next_fix_path")) is not str or not placeholders.get(
        "next_fix_path"
    ):
        raise ValueError(
            "Setup outcome proof diagnostic_placeholders must include next_fix_path"
        )


def _validate_no_hindsight_boundary(boundary: Any) -> None:
    if type(boundary) is not dict:
        raise TypeError("Setup outcome proof no_hindsight_boundary must be a dict")
    for field_name in (
        "setup_identity_frozen_before_outcome_scan",
        "future_evidence_not_used_to_define_setup",
        "no_backfilled_outcome_labels",
    ):
        if boundary.get(field_name) is not True:
            raise ValueError(
                f"Setup outcome proof no_hindsight_boundary must set {field_name}=True"
            )


def _validate_no_trade_boundary(boundary: Any) -> None:
    if type(boundary) is not dict:
        raise TypeError("Setup outcome proof no_trade_boundary must be a dict")
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
                f"Setup outcome proof no_trade_boundary must set {field_name}=True"
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
                f"Setup outcome proof no_trade_boundary must set {field_name}=False"
            )


def _validate_unavailable_fields(unavailable_fields: Any) -> None:
    if type(unavailable_fields) not in {list, dict}:
        raise TypeError("Setup outcome proof unavailable_fields must be a list or dict")
    for field_name, item in _iter_unavailable_items(unavailable_fields):
        if type(field_name) is not str or not field_name:
            raise ValueError(
                "Setup outcome proof unavailable_fields must name fields explicitly"
            )
        if type(item) is not dict:
            raise TypeError(
                f"Setup outcome proof unavailable_fields[{field_name}] must be a dict"
            )
        if item.get("status") not in {"missing_evidence", "unavailable_evidence"}:
            raise ValueError(
                f"Setup outcome proof unavailable_fields[{field_name}] status "
                "must be missing_evidence or unavailable_evidence"
            )
        if type(item.get("reason")) is not str or not item.get("reason"):
            raise ValueError(
                f"Setup outcome proof unavailable_fields[{field_name}] must include reason"
            )
        if item.get("fabricated") is not False:
            raise ValueError(
                f"Setup outcome proof unavailable_fields[{field_name}] must set fabricated=False"
            )


def _validate_list_of_strings(value: Any, field_name: str) -> None:
    if type(value) is not list:
        raise TypeError(f"Setup outcome proof {field_name} must be a list")
    if not value:
        raise ValueError(f"Setup outcome proof {field_name} must be non-empty")
    for index, item in enumerate(value):
        if type(item) is not str or not item:
            raise TypeError(
                f"Setup outcome proof {field_name}[{index}] must be a non-empty string"
            )


def _require_string(record: Mapping[str, Any], field_name: str) -> None:
    if type(record[field_name]) is not str:
        raise TypeError(f"Setup outcome proof {field_name} must be a string")
    if not record[field_name]:
        raise ValueError(f"Setup outcome proof {field_name} must not be empty")


def _unavailable_field_names(unavailable_fields: Any) -> set[str]:
    return {
        field_name
        for field_name, item in _iter_unavailable_items(unavailable_fields)
        if type(item) is dict
        and item.get("status") in {"missing_evidence", "unavailable_evidence"}
    }


def _unavailable_reason(unavailable_fields: Any, target_field_name: str) -> str:
    for field_name, item in _iter_unavailable_items(unavailable_fields):
        if field_name == target_field_name and type(item) is dict:
            return str(item.get("reason", "caller marked evidence unavailable"))
    return "caller marked evidence unavailable"


def _iter_unavailable_items(unavailable_fields: Any) -> list[tuple[str, Any]]:
    if type(unavailable_fields) is dict:
        return [(str(field_name), item) for field_name, item in unavailable_fields.items()]
    items = []
    for index, item in enumerate(unavailable_fields):
        if type(item) is not dict:
            raise TypeError(
                f"Setup outcome proof unavailable_fields[{index}] must be a dict"
            )
        field_name = item.get("field_name")
        if type(field_name) is not str or not field_name:
            raise ValueError(
                f"Setup outcome proof unavailable_fields[{index}] must include field_name"
            )
        items.append((field_name, item))
    return items


def _reject_fabricated_proof_values(value: Any, path: tuple[str, ...]) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            if key_text.lower() == "fabricated" and nested_value is True:
                dotted_path = ".".join((*path, key_text))
                raise ValueError(f"Fabricated proof value rejected: {dotted_path}")
            _reject_fabricated_proof_values(nested_value, (*path, key_text))
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            _reject_fabricated_proof_values(nested_value, (*path, str(index)))
    elif isinstance(value, str):
        normalized_value = value.upper()
        for marker in FABRICATED_PROOF_MARKERS:
            if marker in normalized_value:
                dotted_path = ".".join(path) or "record"
                raise ValueError(
                    f"Fabricated proof marker rejected at {dotted_path}: {marker}"
                )


def _reject_forbidden_setup_outcome_fields(value: Any, path: tuple[str, ...]) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            normalized_key = key_text.lower()
            if (
                normalized_key in FORBIDDEN_SETUP_OUTCOME_FIELD_NAMES
                and not _is_preserved_no_trade_boundary_field(normalized_key, path)
            ):
                dotted_path = ".".join((*path, key_text))
                raise ValueError(f"Forbidden execution/trade field: {dotted_path}")
            _reject_forbidden_setup_outcome_fields(nested_value, (*path, key_text))
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            _reject_forbidden_setup_outcome_fields(nested_value, (*path, str(index)))


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


def _reject_vague_labels(value: Any, path: tuple[str, ...]) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            _reject_vague_labels(nested_value, (*path, str(key)))
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            _reject_vague_labels(nested_value, (*path, str(index)))
    elif isinstance(value, str):
        normalized_value = _normalized(value)
        if normalized_value in {_normalized(label) for label in VAGUE_OUTCOME_LABELS}:
            dotted_path = ".".join(path) or "record"
            raise ValueError(f"Vague setup outcome label rejected at {dotted_path}")


def _extract_record_id(record: Any) -> str:
    if isinstance(record, Mapping) and "proof_record_id" in record:
        return str(record["proof_record_id"])
    return "UNAVAILABLE"


def _normalized(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().lower().replace("-", "_").replace(" ", "_").replace("/", "_")
