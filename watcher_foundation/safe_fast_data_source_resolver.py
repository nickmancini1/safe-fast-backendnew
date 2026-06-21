import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "config"
    / "safe_fast_data_source_registry.json"
)


class DataSourceResolverError(ValueError):
    pass


def load_registry(path=REGISTRY_PATH):
    path = Path(path)
    return json.loads(path.read_text(encoding="utf-8"))


def registry_entries(path=REGISTRY_PATH):
    registry = load_registry(path)
    return {entry["field_identifier"]: entry for entry in registry["entries"]}


def resolve_field_source(field_identifier, decision_timestamp, *, registry_path=REGISTRY_PATH):
    if not field_identifier:
        raise DataSourceResolverError("field_identifier is required")
    if not decision_timestamp:
        raise DataSourceResolverError("decision_timestamp is required")

    entries = registry_entries(registry_path)
    try:
        entry = entries[field_identifier]
    except KeyError as exc:
        raise DataSourceResolverError(f"Unknown SAFE-FAST field identifier: {field_identifier}") from exc

    block_targets = []
    if entry["may_block_setup_qualification"]:
        block_targets.append("setup")
    if entry["may_block_trade_eligibility"]:
        block_targets.append("trade")
    if entry["requirement_class"] == "REQUIRED_FOR_EXECUTION":
        block_targets.append("execution")
    if entry["requirement_class"] == "REQUIRED_FOR_EXIT":
        block_targets.append("exit")
    if not block_targets:
        block_targets.append("optional_context_or_review_only")

    return {
        "field_identifier": entry["field_identifier"],
        "decision_timestamp": decision_timestamp,
        "requirement_class": entry["requirement_class"],
        "consumer_module": entry["consumer_module"],
        "primary_source": entry["primary_source"],
        "dataset_schema_api_series_endpoint_or_calculator": entry[
            "dataset_schema_api_series_endpoint_or_calculator"
        ],
        "secondary_source": entry["secondary_source"],
        "live_authority": entry["live_authority"],
        "historical_authority": entry["historical_authority"],
        "timestamp_window": _timestamp_window(entry, decision_timestamp),
        "timestamp_timezone_rule": entry["timestamp_timezone_rule"],
        "historical_vintage_rule": entry["historical_vintage_rule"],
        "credential_requirement": entry["credential_requirement"],
        "entitlement_requirement": entry["entitlement_requirement"],
        "cost_check_requirement": entry["cost_check_requirement"],
        "local_cache_location": entry["local_cache_location"],
        "validation_test": entry["validation_test"],
        "may_block_current_decision": (
            entry["may_block_setup_qualification"]
            or entry["may_block_trade_eligibility"]
            or entry["requirement_class"] in {"REQUIRED_FOR_EXECUTION", "REQUIRED_FOR_EXIT"}
        ),
        "blocking_targets": block_targets,
        "fallback_behavior": entry["fallback_behavior"],
        "unavailable_data_classification": entry["unavailable_data_classification"],
        "source_conflict_behavior": entry["source_conflict_behavior"],
        "unavailable_next_action": _unavailable_next_action(entry),
        "vendor_contacted": False,
        "secrets_read": False,
    }


def resolve_unavailable_field(field_identifier, decision_timestamp, reason, *, registry_path=REGISTRY_PATH):
    plan = resolve_field_source(
        field_identifier,
        decision_timestamp,
        registry_path=registry_path,
    )
    plan["reason_unavailable"] = reason
    plan["missing_data_label_allowed"] = False
    plan["required_report_fields"] = {
        "exact_field": plan["field_identifier"],
        "exact_source": plan["primary_source"],
        "exact_dataset_schema_api_calculator": plan[
            "dataset_schema_api_series_endpoint_or_calculator"
        ],
        "exact_timestamp_window": plan["timestamp_window"],
        "exact_reason_unavailable": reason,
        "blocks": plan["blocking_targets"],
        "exact_next_action": plan["unavailable_next_action"],
    }
    return plan


def _timestamp_window(entry, decision_timestamp):
    if entry["field_identifier"] in {
        "setup_time_row",
        "trigger",
        "invalidation",
        "freshness_final_signal_state",
        "blocker_caution_review",
        "no_hindsight_boundary",
        "session_boundary_behavior",
        "option_contract_definition",
        "option_quote_freshness_cmbp1",
        "option_quote_fallback_cbbo1s",
        "option_tcbbo_trade_linked_context",
        "option_trades",
        "option_statistics_volume_open_interest",
    }:
        return f"source timestamps <= {decision_timestamp}"
    if entry["field_identifier"] == "underlying_ohlcv_1h":
        return f"1h bar window ending no later than {decision_timestamp}; vendor request end is exclusive"
    return f"as-of {decision_timestamp}"


def _unavailable_next_action(entry):
    classification = entry["unavailable_data_classification"]
    if classification == "SOURCE_UNAVAILABLE_CANDIDATE_EXCLUDED":
        return "exclude candidate or complete exact source-backed setup evidence before rerun"
    if classification == "CREDENTIAL_NOT_CONFIGURED":
        return "run explicit read-only credential/capability audit task; do not read secrets in resolver"
    if classification == "ENTITLEMENT_NOT_CONFIRMED":
        return "verify entitlement and run exact cost check before any data request"
    if classification == "SOURCE_CAPABILITY_AUDIT_REQUIRED":
        return "perform bounded source capability audit and update registry before using source"
    return "stop and record exact unavailable-data classification"


if __name__ == "__main__":
    plan = resolve_field_source("setup_time_row", "2026-05-01T15:30:00-04:00")
    print(json.dumps(plan, indent=2, sort_keys=True))
