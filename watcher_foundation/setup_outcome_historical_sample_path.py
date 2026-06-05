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

HISTORICAL_SAMPLE_PATH_OUTPUT_REVIEW_RESULT_FIELDS = (
    "watch_only",
    "historical_sample_path_output_review_only",
    "accepted_in_memory_sample_path_output_only",
    "final_viability_proven",
    "profitability_claimed",
    "historical_success_claimed",
    "optimization_started",
    "no_rule_change_started",
    "worked_samples",
    "failed_samples",
    "inconclusive_samples",
    "worked_sample_clear_proof",
    "failed_sample_useful_diagnosis",
    "inconclusive_sample_missing_evidence_clear",
    "gld_continuation_review_status",
    "gld_continuation_became_reviewable",
    "gld_continuation_remains_inconclusive",
    "iwm_review_status",
    "iwm_became_reviewable",
    "iwm_remains_inconclusive",
    "iwm_sample_teaches",
    "useful_proof",
    "weak_proof",
    "missing_evidence",
    "missing_evidence_by_setup_type",
    "missing_evidence_by_symbol",
    "missing_evidence_by_setup_type_symbol_pair",
    "diagnostics",
    "next_fix_paths",
    "smallest_next_fix_path",
    "regression_needs",
    "lower_tier_review_summary",
    "no_hindsight_boundary_preserved",
    "setup_type_separated",
    "symbol_separated",
    "setup_type_symbol_pair_separated",
    "boundary_review",
    "result_useful_for_lower_tier_review",
    "review_conclusion",
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
            proof_record_id="controlled-sample-continuation-gld-evidenced-001",
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
                "source_row_reference": "controlled-source-gld-continuation-001:after-row-1",
                "post_setup_evidence": [
                    "controlled-source-gld-continuation-001:held-continuation-shelf",
                    "controlled-source-gld-continuation-001:follow-through-after-shelf-hold",
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
                "controlled-source-gld-continuation-001:setup-time-shelf",
                "controlled-source-gld-continuation-001:held-continuation-shelf",
            ],
            unavailable_fields=[],
            next_fix_path=(
                "review the now-evidenced three-sample controlled set before "
                "any broader sample expansion"
            ),
        ),
        _controlled_sample_record(
            proof_record_id="controlled-sample-ideal-iwm-worked-001",
            source_record_id="controlled-source-iwm-ideal-001",
            setup_id="controlled-ideal-iwm-001",
            setup_type="Ideal",
            symbol="IWM",
            stage="near-trigger",
            detection_timestamp="2026-04-16T10:30:00-04:00",
            setup_evidence_refs=[
                "controlled-source-iwm-ideal-001:setup-time-candle",
                "controlled-source-iwm-ideal-001:setup-time-trigger-card",
            ],
            after_setup_evidence={
                "caller_provided": True,
                "start_timestamp": "2026-04-16T11:30:00-04:00",
                "end_timestamp": "2026-04-16T15:30:00-04:00",
                "source_row_reference": "controlled-source-iwm-ideal-001:after-row-1",
                "post_setup_evidence": [
                    "controlled-source-iwm-ideal-001:held-trigger-zone",
                    "controlled-source-iwm-ideal-001:small-cap-follow-through",
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
                "controlled-source-iwm-ideal-001:setup-time-trigger-card",
                "controlled-source-iwm-ideal-001:small-cap-follow-through",
            ],
            unavailable_fields=[],
            next_fix_path=(
                "review the four-symbol controlled starting universe before "
                "any broader sample expansion"
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


def review_first_controlled_historical_sample_path_output() -> dict[str, Any]:
    """Build, run, and review the first controlled local sample output."""
    sample_path_output = run_setup_outcome_historical_sample_path(
        build_first_controlled_historical_sample_evidence_set()
    )
    return review_setup_outcome_historical_sample_path_output(sample_path_output)


def review_setup_outcome_historical_sample_path_output(
    sample_path_output: dict[str, Any],
) -> dict[str, Any]:
    """Review one caller-provided in-memory historical sample path output."""
    if type(sample_path_output) is not dict:
        raise TypeError("Historical sample path output must be a dict")

    output = deepcopy(sample_path_output)
    _validate_historical_sample_path_output(output)

    setup_by_id = _setup_appeared_by_id(output)
    happened_by_id = _what_happened_after_by_id(output)
    diagnostics_by_record_id = _diagnostics_by_record_id(output)

    worked_samples = _review_samples_for_statuses(
        setup_by_id,
        happened_by_id,
        diagnostics_by_record_id,
        {"worked"},
    )
    failed_samples = _review_samples_for_statuses(
        setup_by_id,
        happened_by_id,
        diagnostics_by_record_id,
        {"failed"},
    )
    inconclusive_samples = _review_samples_for_statuses(
        setup_by_id,
        happened_by_id,
        diagnostics_by_record_id,
        {"inconclusive", "missing_evidence", "unavailable_evidence"},
    )
    missing_evidence = _review_missing_evidence(output)
    boundary_review = _sample_path_output_boundary_review(
        output,
        setup_by_id,
        happened_by_id,
    )
    useful_proof = _useful_proof(worked_samples, failed_samples, inconclusive_samples)
    weak_proof = _weak_proof(output, worked_samples, failed_samples, inconclusive_samples)
    next_fix_paths = _review_next_fix_paths(output, missing_evidence, weak_proof)
    regression_needs = _review_regression_needs(output, weak_proof)
    gld_continuation_review_status = _gld_continuation_review_status(
        worked_samples,
        failed_samples,
        inconclusive_samples,
    )
    iwm_review_status = _iwm_review_status(
        worked_samples,
        failed_samples,
        inconclusive_samples,
    )

    result = {
        "watch_only": True,
        "historical_sample_path_output_review_only": True,
        "accepted_in_memory_sample_path_output_only": True,
        "final_viability_proven": False,
        "profitability_claimed": False,
        "historical_success_claimed": False,
        "optimization_started": False,
        "no_rule_change_started": True,
        "worked_samples": worked_samples,
        "failed_samples": failed_samples,
        "inconclusive_samples": inconclusive_samples,
        "worked_sample_clear_proof": _all_samples_have_clear_proof(worked_samples),
        "failed_sample_useful_diagnosis": _all_samples_have_useful_diagnosis(
            failed_samples
        ),
        "inconclusive_sample_missing_evidence_clear": (
            bool(inconclusive_samples)
            and _all_samples_have_missing_evidence(inconclusive_samples)
        ),
        "gld_continuation_review_status": gld_continuation_review_status,
        "gld_continuation_became_reviewable": (
            gld_continuation_review_status == "reviewable"
        ),
        "gld_continuation_remains_inconclusive": (
            gld_continuation_review_status == "inconclusive"
        ),
        "iwm_review_status": iwm_review_status,
        "iwm_became_reviewable": iwm_review_status == "reviewable",
        "iwm_remains_inconclusive": iwm_review_status == "inconclusive",
        "iwm_sample_teaches": _iwm_sample_teaches(
            iwm_review_status,
            worked_samples,
            failed_samples,
            inconclusive_samples,
        ),
        "useful_proof": useful_proof,
        "weak_proof": weak_proof,
        "missing_evidence": missing_evidence,
        "missing_evidence_by_setup_type": deepcopy(
            output["missing_evidence_by_setup_type"]
        ),
        "missing_evidence_by_symbol": deepcopy(output["missing_evidence_by_symbol"]),
        "missing_evidence_by_setup_type_symbol_pair": deepcopy(
            output["missing_evidence_by_setup_type_symbol_pair"]
        ),
        "diagnostics": deepcopy(output["diagnostics"]),
        "next_fix_paths": next_fix_paths,
        "smallest_next_fix_path": _smallest_next_fix_path(next_fix_paths),
        "regression_needs": regression_needs,
        "lower_tier_review_summary": _sample_path_output_lower_tier_review(
            output,
            worked_samples,
            failed_samples,
            inconclusive_samples,
            weak_proof,
        ),
        "no_hindsight_boundary_preserved": boundary_review[
            "no_hindsight_boundary_preserved"
        ],
        "setup_type_separated": output["setup_type_separated"],
        "symbol_separated": output["symbol_separated"],
        "setup_type_symbol_pair_separated": output[
            "setup_type_symbol_pair_separated"
        ],
        "boundary_review": boundary_review,
        "result_useful_for_lower_tier_review": _result_useful_for_lower_tier_review(
            worked_samples,
            failed_samples,
            inconclusive_samples,
            boundary_review,
            next_fix_paths,
        ),
        "review_conclusion": _sample_path_output_review_conclusion(
            worked_samples,
            failed_samples,
            inconclusive_samples,
            weak_proof,
            boundary_review,
            next_fix_paths,
        ),
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


def _validate_historical_sample_path_output(output: Mapping[str, Any]) -> None:
    missing = [
        field_name
        for field_name in HISTORICAL_SAMPLE_PATH_RESULT_FIELDS
        if field_name not in output
    ]
    if missing:
        raise ValueError(f"Missing historical sample path output fields: {missing}")
    if output["historical_setup_sample_path_only"] is not True:
        raise ValueError("Historical sample path output marker is missing")
    if output["watch_only"] is not True:
        raise ValueError("Historical sample path output must remain watch-only")


def _setup_appeared_by_id(output: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    appeared_by_id = {}
    for item in output["proof_chain"]["setup_appeared"]:
        setup_id = item.get("setup_id") if type(item) is dict else None
        if type(setup_id) is str:
            appeared_by_id[setup_id] = deepcopy(item)
    return appeared_by_id


def _what_happened_after_by_id(output: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    happened_by_id = {}
    for item in output["proof_chain"]["what_happened_after"]:
        setup_id = item.get("setup_id") if type(item) is dict else None
        if type(setup_id) is str:
            happened_by_id[setup_id] = deepcopy(item)
    return happened_by_id


def _diagnostics_by_record_id(output: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    diagnostics_by_id = {}
    for item in output["diagnostics"]:
        record_id = item.get("record_id") if type(item) is dict else None
        if type(record_id) is str:
            diagnostics_by_id[record_id] = deepcopy(item)
    return diagnostics_by_id


def _review_samples_for_statuses(
    setup_by_id: Mapping[str, dict[str, Any]],
    happened_by_id: Mapping[str, dict[str, Any]],
    diagnostics_by_record_id: Mapping[str, dict[str, Any]],
    statuses: set[str],
) -> list[dict[str, Any]]:
    samples = []
    for setup_id, happened in happened_by_id.items():
        outcome_status = _normalized_outcome_status(happened)
        if outcome_status not in statuses:
            continue
        appeared = setup_by_id.get(setup_id, {})
        diagnostic = diagnostics_by_record_id.get(happened["proof_record_id"], {})
        missing = _sample_missing_evidence(happened, diagnostic)
        samples.append(
            {
                "proof_record_id": happened["proof_record_id"],
                "setup_id": setup_id,
                "setup_type": happened["setup_type"],
                "symbol": happened["symbol"],
                "setup_type_symbol_pair": {
                    "setup_type": happened["setup_type"],
                    "symbol": happened["symbol"],
                },
                "outcome_status": happened["outcome_status"],
                "outcome_result_state": happened["outcome_result_state"],
                "setup_time_evidence_refs": deepcopy(
                    appeared.get("setup_evidence_refs", [])
                ),
                "after_setup_evidence": deepcopy(happened["after_setup_evidence"]),
                "diagnostic_category": deepcopy(
                    diagnostic.get("diagnostic_category")
                ),
                "diagnosis": deepcopy(diagnostic.get("what_happened")),
                "evidence_used": deepcopy(diagnostic.get("evidence_used", [])),
                "missing_evidence": missing,
                "next_fix_path": deepcopy(diagnostic.get("next_fix_path")),
                "regression_needed": deepcopy(diagnostic.get("regression_needed")),
                "clear_proof": _sample_has_clear_proof(happened, appeared, diagnostic),
                "useful_diagnosis": _sample_has_useful_diagnosis(diagnostic),
                "explicit_missing_evidence": bool(missing),
                "profitability_claimed": False,
            }
        )
    return deepcopy(samples)


def _normalized_outcome_status(happened: Mapping[str, Any]) -> str:
    if happened.get("outcome_evidence_state") in {
        "missing_evidence",
        "unavailable_evidence",
    }:
        return "missing_evidence"
    outcome_result_state = happened.get("outcome_result_state")
    if outcome_result_state in {
        "worked",
        "failed",
        "inconclusive",
        "pending",
        "stale",
        "invalidated",
    }:
        return outcome_result_state
    return str(outcome_result_state)


def _sample_missing_evidence(
    happened: Mapping[str, Any],
    diagnostic: Mapping[str, Any],
) -> list[Any]:
    missing = []
    for item in happened.get("unavailable_fields", []):
        _append_unique(missing, item)
    for item in diagnostic.get("unavailable_evidence", []):
        _append_unique(missing, item)
    after_setup_evidence = happened.get("after_setup_evidence", {})
    if type(after_setup_evidence) is dict:
        for field_name in ("source_row_reference", "post_setup_evidence"):
            if field_name not in after_setup_evidence:
                _append_unique(
                    missing,
                    {
                        "field_name": field_name,
                        "status": "missing_evidence",
                        "reason": f"after_setup_evidence did not include {field_name}",
                        "fabricated": False,
                    },
                )
    return missing


def _sample_has_clear_proof(
    happened: Mapping[str, Any],
    appeared: Mapping[str, Any],
    diagnostic: Mapping[str, Any],
) -> bool:
    after_setup_evidence = happened.get("after_setup_evidence", {})
    return bool(
        appeared.get("setup_evidence_refs")
        and type(after_setup_evidence) is dict
        and after_setup_evidence.get("post_setup_evidence")
        and happened.get("outcome_result_state") in {"worked", "failed"}
        and diagnostic.get("evidence_used")
        and not _sample_missing_evidence(happened, diagnostic)
    )


def _sample_has_useful_diagnosis(diagnostic: Mapping[str, Any]) -> bool:
    return bool(
        diagnostic.get("diagnostic_category")
        and diagnostic.get("what_happened")
        and diagnostic.get("evidence_used")
        and diagnostic.get("next_fix_path")
        and diagnostic.get("regression_needed")
    )


def _all_samples_have_clear_proof(samples: list[dict[str, Any]]) -> bool:
    return bool(samples) and all(sample["clear_proof"] for sample in samples)


def _all_samples_have_useful_diagnosis(samples: list[dict[str, Any]]) -> bool:
    return bool(samples) and all(sample["useful_diagnosis"] for sample in samples)


def _all_samples_have_missing_evidence(samples: list[dict[str, Any]]) -> bool:
    return bool(samples) and all(
        sample["explicit_missing_evidence"] for sample in samples
    )


def _gld_continuation_review_status(
    worked_samples: list[dict[str, Any]],
    failed_samples: list[dict[str, Any]],
    inconclusive_samples: list[dict[str, Any]],
) -> str:
    for sample in (*worked_samples, *failed_samples):
        if (
            sample["setup_type"] == "Continuation"
            and sample["symbol"] == "GLD"
            and sample["clear_proof"]
        ):
            return "reviewable"
    for sample in inconclusive_samples:
        if sample["setup_type"] == "Continuation" and sample["symbol"] == "GLD":
            return "inconclusive"
    return "not_present"


def _iwm_review_status(
    worked_samples: list[dict[str, Any]],
    failed_samples: list[dict[str, Any]],
    inconclusive_samples: list[dict[str, Any]],
) -> str:
    for sample in (*worked_samples, *failed_samples):
        if sample["symbol"] == "IWM" and sample["clear_proof"]:
            return "reviewable"
    for sample in inconclusive_samples:
        if sample["symbol"] == "IWM":
            return "inconclusive"
    return "not_present"


def _iwm_sample_teaches(
    iwm_review_status: str,
    worked_samples: list[dict[str, Any]],
    failed_samples: list[dict[str, Any]],
    inconclusive_samples: list[dict[str, Any]],
) -> dict[str, Any]:
    for sample in (*worked_samples, *failed_samples, *inconclusive_samples):
        if sample["symbol"] != "IWM":
            continue
        return {
            "review_status": iwm_review_status,
            "setup_type": sample["setup_type"],
            "symbol": sample["symbol"],
            "setup_type_symbol_pair": deepcopy(sample["setup_type_symbol_pair"]),
            "outcome_status": sample["outcome_status"],
            "teaches": (
                "the controlled local chain can carry one small-cap IWM "
                "example with setup-time evidence separated from after-setup "
                "evidence while keeping symbol and setup pair boundaries"
            ),
            "profitability_claimed": False,
            "final_viability_proven": False,
            "optimization_started": False,
        }
    return {
        "review_status": iwm_review_status,
        "teaches": "IWM is not present in the controlled local sample output",
        "profitability_claimed": False,
        "final_viability_proven": False,
        "optimization_started": False,
    }


def _review_missing_evidence(output: Mapping[str, Any]) -> list[Any]:
    missing = []
    for item in output["missing_evidence"]:
        _append_unique(missing, item)
    for item in output["bundle_readiness_result"]["exact_missing_review_items"]:
        _append_unique(missing, item)
    return missing


def _sample_path_output_boundary_review(
    output: Mapping[str, Any],
    setup_by_id: Mapping[str, dict[str, Any]],
    happened_by_id: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    no_hindsight = bool(
        output["no_hindsight_boundary_preserved"]
        and all("after_setup_evidence" not in item for item in setup_by_id.values())
        and all("frozen_setup_identity" not in item for item in happened_by_id.values())
        and all(
            happened.get("after_setup_evidence", {}).get(
                "future_evidence_used_to_define_setup"
            )
            is False
            for happened in happened_by_id.values()
            if type(happened.get("after_setup_evidence")) is dict
        )
    )
    return {
        "no_hindsight_boundary_preserved": no_hindsight,
        "no_trade_boundary_preserved": output["no_trade_boundary_preserved"],
        "no_live_data_boundary_preserved": output[
            "no_live_data_boundary_preserved"
        ],
        "no_controlled_shadow_boundary_preserved": output[
            "no_controlled_shadow_boundary_preserved"
        ],
        "no_alert_boundary_preserved": output["no_alert_boundary_preserved"],
        "no_file_write_boundary_preserved": output[
            "no_file_write_boundary_preserved"
        ],
        "no_broker_boundary_preserved": output["no_broker_boundary_preserved"],
        "no_optimization_boundary_preserved": output[
            "no_optimization_boundary_preserved"
        ],
        "no_rule_change_started": output["no_rule_change_started"],
        "live_data_started": output["live_data_started"],
        "controlled_shadow_data_started": output["controlled_shadow_data_started"],
        "alerts_sent": output["alerts_sent"],
        "files_written": output["files_written"],
        "broker_or_trade_behavior_enabled": output[
            "broker_or_trade_behavior_enabled"
        ],
        "profitability_claimed": output["profitability_claimed"],
        "final_viability_proven": output["final_viability_proven"],
    }


def _useful_proof(
    worked_samples: list[dict[str, Any]],
    failed_samples: list[dict[str, Any]],
    inconclusive_samples: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    proof_items = []
    for sample in worked_samples:
        if sample["clear_proof"]:
            proof_items.append(
                {
                    "proof_type": "worked_chart_behavior",
                    "setup_type": sample["setup_type"],
                    "symbol": sample["symbol"],
                    "setup_type_symbol_pair": sample["setup_type_symbol_pair"],
                    "reason": "setup-time and after-setup evidence were present and separated",
                }
            )
    for sample in failed_samples:
        if sample["clear_proof"] and sample["useful_diagnosis"]:
            proof_items.append(
                {
                    "proof_type": "failed_chart_behavior_with_diagnosis",
                    "setup_type": sample["setup_type"],
                    "symbol": sample["symbol"],
                    "setup_type_symbol_pair": sample["setup_type_symbol_pair"],
                    "reason": "failure had evidence, diagnosis, fix path, and regression need",
                }
            )
    for sample in inconclusive_samples:
        if sample["explicit_missing_evidence"]:
            proof_items.append(
                {
                    "proof_type": "missing_evidence_identified",
                    "setup_type": sample["setup_type"],
                    "symbol": sample["symbol"],
                    "setup_type_symbol_pair": sample["setup_type_symbol_pair"],
                    "reason": "inconclusive sample exposed exact unavailable evidence",
                }
            )
    return deepcopy(proof_items)


def _weak_proof(
    output: Mapping[str, Any],
    worked_samples: list[dict[str, Any]],
    failed_samples: list[dict[str, Any]],
    inconclusive_samples: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    weak = []
    if not _all_samples_have_clear_proof(worked_samples):
        weak.append(
            {
                "proof_gap": "worked_sample_clear_proof",
                "reason": "worked sample proof is absent or incomplete",
            }
        )
    if not _all_samples_have_useful_diagnosis(failed_samples):
        weak.append(
            {
                "proof_gap": "failed_sample_useful_diagnosis",
                "reason": "failed sample diagnosis is absent or incomplete",
            }
        )
    if inconclusive_samples and not _all_samples_have_missing_evidence(
        inconclusive_samples
    ):
        weak.append(
            {
                "proof_gap": "inconclusive_sample_missing_evidence",
                "reason": "inconclusive sample did not expose exact missing evidence",
            }
        )
    if output["bundle_readiness_result"]["ready_for_lower_tier_review"] is not True:
        weak.append(
            {
                "proof_gap": "bundle_readiness",
                "reason": output["bundle_readiness_result"][
                    "bundle_readiness_decision"
                ],
            }
        )
    return weak


def _review_next_fix_paths(
    output: Mapping[str, Any],
    missing_evidence: list[Any],
    weak_proof: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    fix_paths = []
    for path in output["next_fix_paths"]:
        _append_unique(
            fix_paths,
            {
                "path": path,
                "source": "sample_path_output",
                "optimization_allowed": False,
                "rule_change_allowed": False,
            },
        )
    if _has_after_setup_missing_evidence(missing_evidence):
        _append_unique(
            fix_paths,
            {
                "path": "collect_or_preserve_missing_after_setup_evidence",
                "source": "review_missing_evidence",
                "optimization_allowed": False,
                "rule_change_allowed": False,
            },
        )
    if weak_proof:
        _append_unique(
            fix_paths,
            {
                "path": "tighten_review_contract_or_fixture_before_expansion",
                "source": "review_weak_proof",
                "optimization_allowed": False,
                "rule_change_allowed": False,
            },
        )
    return fix_paths


def _has_after_setup_missing_evidence(missing_evidence: list[Any]) -> bool:
    for item in missing_evidence:
        if type(item) is not dict:
            continue
        if item.get("field_name") in {"source_row_reference", "post_setup_evidence"}:
            return True
    return False


def _smallest_next_fix_path(next_fix_paths: list[dict[str, Any]]) -> dict[str, Any]:
    for path in next_fix_paths:
        if path["path"] == "collect_or_preserve_missing_after_setup_evidence":
            return deepcopy(path)
    return deepcopy(next_fix_paths[0]) if next_fix_paths else {}


def _review_regression_needs(
    output: Mapping[str, Any],
    weak_proof: list[dict[str, Any]],
) -> list[Any]:
    regressions = []
    for item in output["regression_needs"]:
        _append_unique(regressions, item)
    for item in weak_proof:
        _append_unique(
            regressions,
            {
                "regression_gap": item["proof_gap"],
                "reason": item["reason"],
            },
        )
    return regressions


def _sample_path_output_lower_tier_review(
    output: Mapping[str, Any],
    worked_samples: list[dict[str, Any]],
    failed_samples: list[dict[str, Any]],
    inconclusive_samples: list[dict[str, Any]],
    weak_proof: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "records_processed": output["records_processed"],
        "records_accepted": output["records_accepted"],
        "records_rejected": output["records_rejected"],
        "worked_samples": deepcopy(worked_samples),
        "failed_samples": deepcopy(failed_samples),
        "inconclusive_samples": deepcopy(inconclusive_samples),
        "weak_proof": deepcopy(weak_proof),
        "bundle_readiness_result": deepcopy(output["bundle_readiness_result"]),
        "no_trade_watch_only": True,
        "no_live_data": True,
        "no_controlled_shadow_data": True,
        "no_alerts": True,
        "no_broker": True,
        "no_file_write": True,
        "no_rule_change": True,
        "no_optimization": True,
        "final_viability_proven": False,
        "profitability_claimed": False,
    }


def _result_useful_for_lower_tier_review(
    worked_samples: list[dict[str, Any]],
    failed_samples: list[dict[str, Any]],
    inconclusive_samples: list[dict[str, Any]],
    boundary_review: Mapping[str, Any],
    next_fix_paths: list[dict[str, Any]],
) -> bool:
    return bool(
        worked_samples
        and failed_samples
        and boundary_review["no_hindsight_boundary_preserved"]
        and next_fix_paths
    )


def _sample_path_output_review_conclusion(
    worked_samples: list[dict[str, Any]],
    failed_samples: list[dict[str, Any]],
    inconclusive_samples: list[dict[str, Any]],
    weak_proof: list[dict[str, Any]],
    boundary_review: Mapping[str, Any],
    next_fix_paths: list[dict[str, Any]],
) -> str:
    if (
        _all_samples_have_clear_proof(worked_samples)
        and _all_samples_have_useful_diagnosis(failed_samples)
        and (
            not inconclusive_samples
            or _all_samples_have_missing_evidence(inconclusive_samples)
        )
        and boundary_review["no_hindsight_boundary_preserved"]
        and next_fix_paths
    ):
        if weak_proof:
            return "useful_but_not_final_viability_proof"
        return "useful_controlled_review_ready_for_next_fix_path"
    return "not_enough_evidence_for_next_fix_path"


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
