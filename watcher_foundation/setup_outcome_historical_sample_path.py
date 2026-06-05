"""Local-only historical setup sample path runner.

This module accepts caller-provided in-memory historical setup examples only
and runs them through the existing setup outcome proof chain. It does not read
files, fetch data, write reports/logs, start shadow/live workflows, emit alerts,
call subprocesses, touch brokers/accounts/options/P&L, optimize rules, or make
trade decisions.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from watcher_foundation.setup_outcome_diagnostics import (
    evaluate_setup_outcome_diagnostics,
)
from watcher_foundation.setup_outcome_evidence_packet import (
    build_setup_outcome_evidence_packet,
)
from watcher_foundation.setup_outcome_packet_readiness import (
    evaluate_setup_outcome_packet_readiness,
)
from watcher_foundation.setup_outcome_proof import (
    FORBIDDEN_SETUP_OUTCOME_FIELD_NAMES,
    evaluate_setup_outcome_proof,
)
from watcher_foundation.setup_outcome_proof_review_bundle import (
    build_setup_outcome_proof_review_bundle,
)
from watcher_foundation.setup_outcome_proof_review_bundle_readiness import (
    evaluate_setup_outcome_proof_review_bundle_readiness,
)
from watcher_foundation.setup_outcome_review_aggregator import (
    SETUP_OUTCOME_REVIEW_OUTCOME_GROUPS,
    aggregate_setup_outcome_proof_review,
)
from watcher_foundation.setup_outcome_review_readiness import (
    evaluate_setup_outcome_review_readiness,
)


HISTORICAL_SAMPLE_PATH_RESULT_FIELDS = (
    "watch_only",
    "historical_setup_sample_path_only",
    "setup_outcome_proof_review_bundle_readiness_only",
    "setup_outcome_proof_review_bundle_only",
    "setup_outcome_review_readiness_only",
    "setup_outcome_review_aggregator_only",
    "setup_outcome_packet_readiness_only",
    "setup_outcome_evidence_packet_only",
    "setup_outcome_diagnostics_only",
    "setup_outcome_proof_only",
    "final_viability_proven",
    "profitability_claimed",
    "optimization_started",
    "no_rule_change_started",
    "records_processed",
    "records_accepted",
    "records_rejected",
    "setup_type_separated",
    "symbol_separated",
    "setup_type_symbol_pair_separated",
    "represented_setup_types",
    "represented_symbols",
    "represented_setup_type_symbol_pairs",
    "outcome_group_counts",
    "missing_evidence",
    "missing_evidence_by_setup_type",
    "missing_evidence_by_symbol",
    "missing_evidence_by_setup_type_symbol_pair",
    "diagnostics",
    "next_fix_paths",
    "regression_needs",
    "lower_tier_review_summary",
    "proof_chain",
    "bundle_readiness_result",
    "no_hindsight_boundary_preserved",
    "no_trade_boundary_preserved",
    "no_live_data_boundary_preserved",
    "no_controlled_shadow_boundary_preserved",
    "no_alert_boundary_preserved",
    "no_file_write_boundary_preserved",
    "no_broker_boundary_preserved",
    "no_optimization_boundary_preserved",
    "no_trade_or_optimization_boundary_preserved",
    "live_data_started",
    "controlled_shadow_data_started",
    "alerts_sent",
    "files_written",
    "broker_or_trade_behavior_enabled",
)

FIRST_CONTROLLED_HISTORICAL_SAMPLE_EVIDENCE_SET_ID = (
    "first_controlled_historical_sample_evidence_set_v1"
)

FORBIDDEN_HISTORICAL_SAMPLE_PATH_FIELD_NAMES = (
    FORBIDDEN_SETUP_OUTCOME_FIELD_NAMES
    | frozenset(
        {
            "alert",
            "alerts",
            "alert_delivery",
            "alert_path",
            "background_worker",
            "controlled_shadow",
            "controlled_shadow_data",
            "daemon",
            "data_fetch",
            "fetch_live_data",
            "file",
            "file_name",
            "file_path",
            "generated_log_path",
            "generated_report_path",
            "live_backend",
            "live_data",
            "live_data_input",
            "live_data_started",
            "live_trade",
            "live_trade_decision",
            "log_path",
            "main_py",
            "network",
            "output_file",
            "output_path",
            "poller",
            "raw_log_path",
            "report_path",
            "scheduler",
            "shadow_data",
            "socket",
            "subprocess",
            "thread",
            "watcher_loop",
            "write_path",
        }
    )
)


def build_first_controlled_historical_sample_evidence_set() -> list[dict[str, Any]]:
    """Return the first tiny caller-provided historical setup evidence set."""
    records = [
        _controlled_sample_record(
            proof_record_id="controlled-sample-ideal-spy-worked-001",
            source_record_id="controlled-source-spy-ideal-001",
            setup_id="controlled-ideal-spy-001",
            setup_type="Ideal",
            symbol="SPY",
            stage="near-trigger",
            detection_timestamp="2026-04-07T10:30:00-04:00",
            setup_evidence_refs=[
                "controlled-source-spy-ideal-001:setup-time-candle",
                "controlled-source-spy-ideal-001:setup-time-trigger-card",
            ],
            after_setup_evidence={
                "caller_provided": True,
                "start_timestamp": "2026-04-07T11:30:00-04:00",
                "end_timestamp": "2026-04-07T15:30:00-04:00",
                "source_row_reference": "controlled-source-spy-ideal-001:after-row-1",
                "post_setup_evidence": [
                    "controlled-source-spy-ideal-001:held-trigger-zone",
                    "controlled-source-spy-ideal-001:follow-through-before-close",
                ],
                "future_evidence_used_to_define_setup": False,
            },
            trigger_state="triggered",
            invalidation_state="valid_by_rule",
            freshness_state="fresh",
            blocker_caution_state="none",
            session_boundary_state="valid_by_rule",
            outcome_evidence_state="valid_by_rule",
            outcome_result_state="worked",
            evidence_refs=[
                "controlled-source-spy-ideal-001:setup-time-candle",
                "controlled-source-spy-ideal-001:after-row-1",
            ],
            unavailable_fields=[],
            next_fix_path=(
                "keep the controlled worked setup fixture as a regression for "
                "setup-time and after-setup separation"
            ),
        ),
        _controlled_sample_record(
            proof_record_id="controlled-sample-clean-fast-break-qqq-failed-001",
            source_record_id="controlled-source-qqq-clean-fast-break-001",
            setup_id="controlled-clean-fast-break-qqq-001",
            setup_type="Clean Fast Break",
            symbol="QQQ",
            stage="near-trigger",
            detection_timestamp="2026-04-10T10:30:00-04:00",
            setup_evidence_refs=[
                "controlled-source-qqq-clean-fast-break-001:setup-time-candle",
                "controlled-source-qqq-clean-fast-break-001:setup-time-reclaim",
            ],
            after_setup_evidence={
                "caller_provided": True,
                "start_timestamp": "2026-04-10T11:30:00-04:00",
                "end_timestamp": "2026-04-10T15:30:00-04:00",
                "source_row_reference": "controlled-source-qqq-clean-fast-break-001:after-row-1",
                "post_setup_evidence": [
                    "controlled-source-qqq-clean-fast-break-001:trigger-followed-by-reversal",
                    "controlled-source-qqq-clean-fast-break-001:failed-to-hold-reclaim",
                ],
                "future_evidence_used_to_define_setup": False,
            },
            trigger_state="triggered",
            invalidation_state="valid_by_rule",
            freshness_state="fresh",
            blocker_caution_state="none",
            session_boundary_state="valid_by_rule",
            outcome_evidence_state="valid_by_rule",
            outcome_result_state="failed",
            evidence_refs=[
                "controlled-source-qqq-clean-fast-break-001:setup-time-reclaim",
                "controlled-source-qqq-clean-fast-break-001:failed-to-hold-reclaim",
            ],
            unavailable_fields=[],
            next_fix_path=(
                "review outcome scoring evidence before changing any clean fast "
                "break rule or threshold"
            ),
        ),
        _controlled_sample_record(
            proof_record_id="controlled-sample-continuation-gld-missing-001",
            source_record_id="controlled-source-gld-continuation-001",
            setup_id="controlled-continuation-gld-001",
            setup_type="Continuation",
            symbol="GLD",
            stage="near-trigger",
            detection_timestamp="2026-04-15T09:30:00-04:00",
            setup_evidence_refs=[
                "controlled-source-gld-continuation-001:setup-time-candle",
                "controlled-source-gld-continuation-001:setup-time-shelf",
            ],
            after_setup_evidence={
                "caller_provided": True,
                "start_timestamp": "2026-04-15T10:30:00-04:00",
                "end_timestamp": "2026-04-15T15:30:00-04:00",
                "future_evidence_used_to_define_setup": False,
            },
            trigger_state="not_triggered",
            invalidation_state="valid_by_rule",
            freshness_state="fresh",
            blocker_caution_state="needs_review",
            session_boundary_state="needs_review",
            outcome_evidence_state="missing_evidence",
            outcome_result_state="inconclusive",
            evidence_refs=[
                "controlled-source-gld-continuation-001:setup-time-shelf",
            ],
            unavailable_fields=[
                _unavailable_sample_field(
                    "source_row_reference",
                    "after-setup source row reference was not provided",
                ),
                _unavailable_sample_field(
                    "post_setup_evidence",
                    "after-setup movement evidence was not provided",
                ),
            ],
            next_fix_path=(
                "collect or preserve missing GLD continuation after-setup evidence "
                "before any broader sample expansion"
            ),
        ),
    ]
    return deepcopy(records)


def run_setup_outcome_historical_sample_path(
    historical_setup_examples: list[dict[str, Any]],
) -> dict[str, Any]:
    """Run caller-provided in-memory historical setup examples through the chain."""
    if type(historical_setup_examples) is not list:
        raise TypeError("Historical setup examples must be a list")

    _reject_forbidden_sample_path_inputs(historical_setup_examples, path=())

    examples = deepcopy(historical_setup_examples)
    proof_summary = evaluate_setup_outcome_proof(examples)
    diagnostics_summary = evaluate_setup_outcome_diagnostics(proof_summary)
    evidence_packet_summary = build_setup_outcome_evidence_packet(diagnostics_summary)
    evidence_packet_summary = _carry_setup_identifiers(
        evidence_packet_summary,
        proof_summary,
    )
    packet_readiness_summary = evaluate_setup_outcome_packet_readiness(
        evidence_packet_summary
    )
    packet_readiness_summary = _carry_packet_outcome_statuses(
        packet_readiness_summary,
        evidence_packet_summary,
    )
    group_review_summary = aggregate_setup_outcome_proof_review(
        [packet_readiness_summary]
    )
    group_review_readiness_summary = evaluate_setup_outcome_review_readiness(
        group_review_summary
    )
    historical_proof_bundle_summary = build_setup_outcome_proof_review_bundle(
        [group_review_readiness_summary]
    )
    bundle_readiness_summary = evaluate_setup_outcome_proof_review_bundle_readiness(
        historical_proof_bundle_summary
    )

    result = {
        "watch_only": True,
        "historical_setup_sample_path_only": True,
        "setup_outcome_proof_review_bundle_readiness_only": True,
        "setup_outcome_proof_review_bundle_only": True,
        "setup_outcome_review_readiness_only": True,
        "setup_outcome_review_aggregator_only": True,
        "setup_outcome_packet_readiness_only": True,
        "setup_outcome_evidence_packet_only": True,
        "setup_outcome_diagnostics_only": True,
        "setup_outcome_proof_only": True,
        "final_viability_proven": False,
        "profitability_claimed": False,
        "optimization_started": False,
        "no_rule_change_started": True,
        "records_processed": proof_summary["records_processed"],
        "records_accepted": proof_summary["records_accepted"],
        "records_rejected": proof_summary["records_rejected"],
        "setup_type_separated": group_review_summary["setup_type_separated"],
        "symbol_separated": group_review_summary["symbol_separated"],
        "setup_type_symbol_pair_separated": bool(
            group_review_summary["represented_setup_type_symbol_pairs"]
        ),
        "represented_setup_types": deepcopy(
            group_review_summary["represented_setup_types"]
        ),
        "represented_symbols": deepcopy(group_review_summary["represented_symbols"]),
        "represented_setup_type_symbol_pairs": deepcopy(
            group_review_summary["represented_setup_type_symbol_pairs"]
        ),
        "outcome_group_counts": _outcome_group_counts(group_review_summary),
        "missing_evidence": deepcopy(bundle_readiness_summary["missing_evidence"]),
        "missing_evidence_by_setup_type": deepcopy(
            bundle_readiness_summary["missing_evidence_by_setup_type"]
        ),
        "missing_evidence_by_symbol": deepcopy(
            bundle_readiness_summary["missing_evidence_by_symbol"]
        ),
        "missing_evidence_by_setup_type_symbol_pair": deepcopy(
            bundle_readiness_summary[
                "missing_evidence_by_setup_type_symbol_pair"
            ]
        ),
        "diagnostics": _diagnostics_summary(diagnostics_summary),
        "next_fix_paths": _next_fix_paths(
            diagnostics_summary,
            group_review_summary,
            historical_proof_bundle_summary,
        ),
        "regression_needs": _regression_needs(
            evidence_packet_summary,
            group_review_summary,
            historical_proof_bundle_summary,
            bundle_readiness_summary,
        ),
        "lower_tier_review_summary": _lower_tier_review_summary(
            proof_summary,
            packet_readiness_summary,
            group_review_summary,
            group_review_readiness_summary,
            historical_proof_bundle_summary,
            bundle_readiness_summary,
        ),
        "proof_chain": {
            "setup_appeared": _setup_appeared_summary(proof_summary),
            "what_happened_after": _what_happened_after_summary(proof_summary),
            "diagnosis": deepcopy(diagnostics_summary),
            "evidence_packet": deepcopy(evidence_packet_summary),
            "packet_readiness": deepcopy(packet_readiness_summary),
            "group_review": deepcopy(group_review_summary),
            "group_review_readiness": deepcopy(group_review_readiness_summary),
            "historical_proof_bundle": deepcopy(historical_proof_bundle_summary),
            "bundle_readiness": deepcopy(bundle_readiness_summary),
        },
        "bundle_readiness_result": {
            "bundle_complete_enough_to_review": bundle_readiness_summary[
                "bundle_complete_enough_to_review"
            ],
            "ready_for_lower_tier_review": bundle_readiness_summary[
                "ready_for_lower_tier_review"
            ],
            "bundle_readiness_decision": bundle_readiness_summary[
                "bundle_readiness_decision"
            ],
            "exact_missing_review_items": deepcopy(
                bundle_readiness_summary["exact_missing_review_items"]
            ),
        },
        "no_hindsight_boundary_preserved": True,
        "no_trade_boundary_preserved": True,
        "no_live_data_boundary_preserved": True,
        "no_controlled_shadow_boundary_preserved": True,
        "no_alert_boundary_preserved": True,
        "no_file_write_boundary_preserved": True,
        "no_broker_boundary_preserved": True,
        "no_optimization_boundary_preserved": True,
        "no_trade_or_optimization_boundary_preserved": True,
        "live_data_started": False,
        "controlled_shadow_data_started": False,
        "alerts_sent": False,
        "files_written": False,
        "broker_or_trade_behavior_enabled": False,
    }
    return deepcopy(result)


def _controlled_sample_record(
    *,
    proof_record_id: str,
    source_record_id: str,
    setup_id: str,
    setup_type: str,
    symbol: str,
    stage: str,
    detection_timestamp: str,
    setup_evidence_refs: list[str],
    after_setup_evidence: dict[str, Any],
    trigger_state: str,
    invalidation_state: str,
    freshness_state: str,
    blocker_caution_state: str,
    session_boundary_state: str,
    outcome_evidence_state: str,
    outcome_result_state: str,
    evidence_refs: list[str],
    unavailable_fields: list[dict[str, Any]],
    next_fix_path: str,
) -> dict[str, Any]:
    return {
        "proof_record_id": proof_record_id,
        "source_record_id": source_record_id,
        "setup_id": setup_id,
        "setup_type": setup_type,
        "symbol": symbol,
        "timeframe": "1h_rth",
        "stage": stage,
        "detection_timestamp": detection_timestamp,
        "frozen_setup_identity": {
            "caller_provided": True,
            "frozen_before_outcome_scan": True,
            "setup_id": setup_id,
            "setup_type": setup_type,
            "symbol": symbol,
            "frozen_timestamp": detection_timestamp,
        },
        "setup_evidence_refs": deepcopy(setup_evidence_refs),
        "after_setup_evidence": deepcopy(after_setup_evidence),
        "trigger_state": trigger_state,
        "invalidation_state": invalidation_state,
        "freshness_state": freshness_state,
        "blocker_caution_state": blocker_caution_state,
        "session_boundary_state": session_boundary_state,
        "outcome_evidence_state": outcome_evidence_state,
        "outcome_result_state": outcome_result_state,
        "evidence_refs": deepcopy(evidence_refs),
        "unavailable_fields": deepcopy(unavailable_fields),
        "diagnostic_placeholders": {
            "next_fix_path": next_fix_path,
            "lower_tier_handoff": "review controlled local evidence only",
        },
        "no_hindsight_boundary": {
            "setup_identity_frozen_before_outcome_scan": True,
            "future_evidence_not_used_to_define_setup": True,
            "no_backfilled_outcome_labels": True,
        },
        "no_trade_boundary": {
            "no_trade": True,
            "no_broker": True,
            "no_order": True,
            "no_account_sizing": True,
            "no_option_pnl": True,
            "no_live_trade_decision": True,
            "broker_enabled": False,
            "orders_enabled": False,
            "account_sizing_enabled": False,
            "option_pnl_enabled": False,
            "live_trade_decision_enabled": False,
        },
        "watch_only": True,
    }


def _unavailable_sample_field(field_name: str, reason: str) -> dict[str, Any]:
    return {
        "field_name": field_name,
        "status": "missing_evidence",
        "reason": reason,
        "fabricated": False,
    }


def _carry_packet_outcome_statuses(
    packet_readiness_summary: Mapping[str, Any],
    evidence_packet_summary: Mapping[str, Any],
) -> dict[str, Any]:
    summary = deepcopy(dict(packet_readiness_summary))
    outcome_by_item_id = {
        item["packet_item_id"]: item["outcome_status"]
        for item in evidence_packet_summary["packet_items"]
        if type(item) is dict
        and type(item.get("packet_item_id")) is str
        and "outcome_status" in item
    }
    for item in summary["packet_items"]:
        if type(item) is dict and item.get("packet_item_id") in outcome_by_item_id:
            item["outcome_status"] = deepcopy(outcome_by_item_id[item["packet_item_id"]])
    for setup_type, symbols in summary["items_by_setup_type"].items():
        if type(symbols) is not dict:
            continue
        for symbol, items in symbols.items():
            if type(items) is not list:
                continue
            for item in items:
                if type(item) is dict and item.get("packet_item_id") in outcome_by_item_id:
                    item["outcome_status"] = deepcopy(
                        outcome_by_item_id[item["packet_item_id"]]
                    )
    return summary


def _carry_setup_identifiers(
    evidence_packet_summary: Mapping[str, Any],
    proof_summary: Mapping[str, Any],
) -> dict[str, Any]:
    summary = deepcopy(dict(evidence_packet_summary))
    setup_ids_by_item_id = {}
    for item, record in zip(summary["packet_items"], _accepted_records(proof_summary)):
        if type(item) is not dict:
            continue
        item_id = item.get("packet_item_id")
        if type(item_id) is str and type(record.get("setup_id")) is str:
            setup_ids_by_item_id[item_id] = record["setup_id"]
            item["setup_identifier"] = record["setup_id"]
            if type(item.get("what_setup_appeared")) is dict:
                item["what_setup_appeared"]["setup_identifier"] = record["setup_id"]
            _remove_missing_setup_identifier(item)
            if not item["missing_evidence"]:
                item["evidence_state"] = "evidence_supported"
                if item["lower_tier_handoff_required"] is True:
                    item["lower_tier_handoff_required"] = False
                    item["lower_tier_handoff_reason"] = (
                        "not required after preserving caller-provided setup identifier"
                    )

    summary["missing_evidence"] = [
        item
        for item in summary["missing_evidence"]
        if not (
            type(item) is dict
            and item.get("field_name") == "setup_identifier"
        )
    ]
    summary["lower_tier_handoff_items"] = [
        deepcopy(item)
        for item in summary["packet_items"]
        if type(item) is dict and item.get("lower_tier_handoff_required") is True
    ]
    summary["lower_tier_handoff_required"] = bool(
        summary["lower_tier_handoff_items"]
        or summary["missing_evidence"]
        or summary["proof_limited_records"]
        or summary["rejected_records"]
    )
    summary["packet_items_by_setup_type"] = _regroup_packet_items(
        summary["packet_items"]
    )
    return summary


def _remove_missing_setup_identifier(item: dict[str, Any]) -> None:
    missing = item.get("missing_evidence")
    if type(missing) is not list:
        return
    item["missing_evidence"] = [
        missing_item
        for missing_item in missing
        if not (
            type(missing_item) is dict
            and missing_item.get("field_name") == "setup_identifier"
        )
    ]


def _regroup_packet_items(
    packet_items: list[dict[str, Any]],
) -> dict[str, dict[str, list[dict[str, Any]]]]:
    grouped: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for item in packet_items:
        setup_type = item.get("setup_type") if type(item) is dict else None
        symbol = item.get("symbol") if type(item) is dict else None
        setup_type_key = setup_type if type(setup_type) is str and setup_type else "UNAVAILABLE_SETUP_TYPE"
        symbol_key = symbol if type(symbol) is str and symbol else "UNAVAILABLE_SYMBOL"
        grouped.setdefault(setup_type_key, {})
        grouped[setup_type_key].setdefault(symbol_key, [])
        grouped[setup_type_key][symbol_key].append(deepcopy(item))
    return grouped


def _diagnostics_summary(diagnostics_summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "record_id": deepcopy(finding["record_id"]),
            "diagnostic_category": deepcopy(finding["diagnostic_category"]),
            "outcome_status": deepcopy(finding["outcome_status"]),
            "affected_setup_type": deepcopy(finding["affected_setup_type"]),
            "affected_symbol": deepcopy(finding["affected_symbol"]),
            "affected_stage": deepcopy(finding["affected_stage"]),
            "what_happened": deepcopy(finding["what_happened"]),
            "evidence_used": deepcopy(finding["evidence_used"]),
            "unavailable_evidence": deepcopy(finding["unavailable_evidence"]),
            "likely_cause_candidates": deepcopy(finding["likely_cause_candidates"]),
            "next_fix_path": deepcopy(finding["next_fix_path"]),
            "regression_needed": deepcopy(finding["regression_needed"]),
            "lower_tier_handoff_required": finding[
                "lower_tier_handoff_required"
            ],
        }
        for finding in diagnostics_summary["diagnostic_findings"]
    ]


def _next_fix_paths(
    diagnostics_summary: Mapping[str, Any],
    group_review_summary: Mapping[str, Any],
    historical_proof_bundle_summary: Mapping[str, Any],
) -> list[str]:
    paths: list[str] = []
    for mapping in (
        diagnostics_summary["next_fix_paths"],
        group_review_summary["repeated_next_fix_paths"],
        historical_proof_bundle_summary["repeated_fix_paths"],
    ):
        for path in mapping:
            _append_unique(paths, path)
    return paths


def _regression_needs(
    evidence_packet_summary: Mapping[str, Any],
    group_review_summary: Mapping[str, Any],
    historical_proof_bundle_summary: Mapping[str, Any],
    bundle_readiness_summary: Mapping[str, Any],
) -> list[Any]:
    needs: list[Any] = []
    for regression in evidence_packet_summary["regression_needed"]:
        _append_unique(needs, regression)
    for regression in group_review_summary["regression_needed"]:
        _append_unique(needs, regression)
    for regression in historical_proof_bundle_summary["required_regression_tests"]:
        _append_unique(needs, regression)
    for regression in bundle_readiness_summary["required_regression_tests"]:
        _append_unique(needs, regression)
    for regression in bundle_readiness_summary["missing_regression_coverage"]:
        _append_unique(needs, regression)
    return needs


def _outcome_group_counts(group_review_summary: Mapping[str, Any]) -> dict[str, int]:
    return {
        group_name: len(group_review_summary["outcome_groups"][group_name])
        for group_name in SETUP_OUTCOME_REVIEW_OUTCOME_GROUPS
    }


def _lower_tier_review_summary(
    proof_summary: Mapping[str, Any],
    packet_readiness_summary: Mapping[str, Any],
    group_review_summary: Mapping[str, Any],
    group_review_readiness_summary: Mapping[str, Any],
    historical_proof_bundle_summary: Mapping[str, Any],
    bundle_readiness_summary: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "records_processed": proof_summary["records_processed"],
        "records_accepted": proof_summary["records_accepted"],
        "records_rejected": proof_summary["records_rejected"],
        "packet_readiness_status": packet_readiness_summary["readiness_status"],
        "group_review_decision": group_review_summary[
            "proof_continuation_decision"
        ],
        "group_review_readiness_decision": group_review_readiness_summary[
            "lower_tier_review_decision"
        ],
        "bundle_review_decision": historical_proof_bundle_summary[
            "bundle_review_decision"
        ],
        "bundle_readiness_decision": bundle_readiness_summary[
            "bundle_readiness_decision"
        ],
        "ready_for_lower_tier_review": bundle_readiness_summary[
            "ready_for_lower_tier_review"
        ],
        "exact_missing_review_items": deepcopy(
            bundle_readiness_summary["exact_missing_review_items"]
        ),
        "no_trade_watch_only": True,
        "no_live_data": True,
        "no_alerts": True,
        "no_broker": True,
        "no_file_write": True,
        "no_rule_change": True,
        "no_optimization": True,
        "final_viability_proven": False,
        "profitability_claimed": False,
    }


def _setup_appeared_summary(proof_summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    appeared = []
    for record in _accepted_records(proof_summary):
        appeared.append(
            {
                "proof_record_id": record["proof_record_id"],
                "setup_id": record["setup_id"],
                "setup_type": record["setup_type"],
                "symbol": record["symbol"],
                "setup_type_symbol_pair": {
                    "setup_type": record["setup_type"],
                    "symbol": record["symbol"],
                },
                "detection_timestamp": record["detection_timestamp"],
                "frozen_setup_identity": deepcopy(record["frozen_setup_identity"]),
                "setup_evidence_refs": deepcopy(record["setup_evidence_refs"]),
                "no_hindsight_boundary": deepcopy(record["no_hindsight_boundary"]),
            }
        )
    return appeared


def _what_happened_after_summary(
    proof_summary: Mapping[str, Any],
) -> list[dict[str, Any]]:
    happened = []
    for record in _accepted_records(proof_summary):
        happened.append(
            {
                "proof_record_id": record["proof_record_id"],
                "setup_id": record["setup_id"],
                "setup_type": record["setup_type"],
                "symbol": record["symbol"],
                "setup_type_symbol_pair": {
                    "setup_type": record["setup_type"],
                    "symbol": record["symbol"],
                },
                "after_setup_evidence": deepcopy(record["after_setup_evidence"]),
                "outcome_status": record["outcome_status"],
                "trigger_state": record["trigger_state"],
                "invalidation_state": record["invalidation_state"],
                "freshness_state": record["freshness_state"],
                "outcome_evidence_state": record["outcome_evidence_state"],
                "outcome_result_state": record["outcome_result_state"],
                "unavailable_fields": deepcopy(record["unavailable_fields"]),
            }
        )
    return happened


def _accepted_records(proof_summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    records = []
    for records_by_symbol in proof_summary["accepted_records_by_setup_type"].values():
        for symbol_records in records_by_symbol.values():
            records.extend(deepcopy(symbol_records))
    return records


def _append_unique(target: list[Any], value: Any) -> None:
    copied = deepcopy(value)
    if copied not in target:
        target.append(copied)


def _reject_forbidden_sample_path_inputs(value: Any, path: tuple[str, ...]) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            key_text = str(key)
            normalized_key = key_text.lower()
            if (
                normalized_key in FORBIDDEN_HISTORICAL_SAMPLE_PATH_FIELD_NAMES
                and not _is_preserved_no_trade_boundary_field(normalized_key, path)
            ):
                dotted_path = ".".join((*path, key_text))
                raise ValueError(f"Forbidden sample path field: {dotted_path}")
            _reject_forbidden_sample_path_inputs(nested_value, (*path, key_text))
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            _reject_forbidden_sample_path_inputs(nested_value, (*path, str(index)))
    elif isinstance(value, str):
        normalized_value = value.strip().lower().replace("\\", "/")
        if normalized_value.endswith("/main.py") or normalized_value == "main.py":
            dotted_path = ".".join(path) or "historical_setup_examples"
            raise ValueError(f"Forbidden sample path value: {dotted_path}")


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
