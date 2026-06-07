"""Local watch-only watcher foundation scaffold."""

from watcher_foundation.constants import (
    ACCEPTED_HEADLINE_NEWS_STATUSES,
    ACCEPTED_SETUP_TYPES,
    ACCEPTED_STAGES,
    ACCEPTED_TRIGGER_STATUSES,
    EXPLICIT_UNCONFIRMED_MARKERS,
    NEWS_UNCONFIRMED,
)
from watcher_foundation.batch_runner import (
    BATCH_RUNNER_RESULT_FIELDS,
    run_local_watcher_batch,
)
from watcher_foundation.day60_shadow_contract import (
    DAY60_SHADOW_CONTRACT_DIAGNOSTIC_PLACEHOLDER_FIELDS,
    DAY60_SHADOW_CONTRACT_REQUIRED_FIELDS,
    DAY60_SHADOW_CONTRACT_TRIGGER_CARD_REQUIRED_FIELDS,
    validate_day60_shadow_contract_batch,
    validate_day60_shadow_contract_row,
)
from watcher_foundation.day60_outcome_scoring_contract import (
    DAY60_OUTCOME_SCORING_CONTRACT_REQUIRED_FIELDS,
    DAY60_OUTCOME_SCORING_CONTRACT_REQUIRED_PROOF_FIELDS,
    DAY60_OUTCOME_SCORING_CONTRACT_RESULT_FIELDS,
    validate_day60_outcome_scoring_batch,
    validate_day60_outcome_scoring_row,
)
from watcher_foundation.day60_outcome_scoring_summary import (
    DAY60_OUTCOME_REVIEW_BUCKETS,
    DAY60_OUTCOME_SCORING_SUMMARY_RESULT_FIELDS,
    build_day60_outcome_scoring_summary,
)
from watcher_foundation.day60_outcome_diagnostics import (
    DAY60_OUTCOME_DIAGNOSTICS_RESULT_FIELDS,
    DAY60_OUTCOME_DIAGNOSTIC_FAILURE_CATEGORIES,
    DAY60_OUTCOME_DIAGNOSTIC_FIX_PATHS,
    evaluate_day60_outcome_diagnostics,
)
from watcher_foundation.day60_optimization_readiness import (
    DAY60_OPTIMIZATION_ALLOWED_SYSTEM_AREAS,
    DAY60_OPTIMIZATION_READINESS_REQUIRED_FIELDS,
    DAY60_OPTIMIZATION_READINESS_RESULT_FIELDS,
    evaluate_day60_optimization_readiness,
)
from watcher_foundation.discretion_audit import (
    DISCRETION_AUDIT_ALLOWED_HUMAN_DISCRETION,
    DISCRETION_AUDIT_AREAS,
    DISCRETION_AUDIT_RESULT_FIELDS,
    DISCRETION_AUDIT_VAGUE_PHRASES,
    audit_trading_plan_discretion,
)
from watcher_foundation.discretion_audit_coverage import (
    DISCRETION_AUDIT_COVERAGE_RESULT_FIELDS,
    DISCRETION_AUDIT_REQUIRED_COVERAGE_AREAS,
    evaluate_discretion_audit_coverage,
)
from watcher_foundation.discretion_audit_inventory import (
    DISCRETION_AUDIT_INVENTORY_ALLOWED_AREAS,
    DISCRETION_AUDIT_INVENTORY_REQUIRED_FIELDS,
    DISCRETION_AUDIT_INVENTORY_RESULT_FIELDS,
    validate_discretion_audit_inventory,
    validate_discretion_audit_inventory_item,
)
from watcher_foundation.discretion_audit_inventory_bridge import (
    DISCRETION_AUDIT_INVENTORY_BRIDGE_RESULT_FIELDS,
    evaluate_discretion_audit_inventory_bridge,
)
from watcher_foundation.historical_outcome_proof_preflight import (
    HISTORICAL_OUTCOME_PROOF_PREFLIGHT_REQUIRED_FIELDS,
    HISTORICAL_OUTCOME_PROOF_PREFLIGHT_RESULT_FIELDS,
    validate_historical_outcome_proof_batch,
    validate_historical_outcome_proof_row,
)
from watcher_foundation.historical_outcome_proof_summary import (
    HISTORICAL_OUTCOME_PROOF_SUMMARY_RESULT_FIELDS,
    build_historical_outcome_proof_summary,
)
from watcher_foundation.historical_outcome_diagnostics import (
    HISTORICAL_OUTCOME_DIAGNOSTICS_RESULT_FIELDS,
    HISTORICAL_OUTCOME_DIAGNOSTIC_FAILURE_CATEGORIES,
    HISTORICAL_OUTCOME_DIAGNOSTIC_FIX_PATHS,
    evaluate_historical_outcome_diagnostics,
)
from watcher_foundation.historical_optimization_readiness import (
    HISTORICAL_OPTIMIZATION_ALLOWED_SYSTEM_AREAS,
    HISTORICAL_OPTIMIZATION_READINESS_REQUIRED_FIELDS,
    HISTORICAL_OPTIMIZATION_READINESS_RESULT_FIELDS,
    evaluate_historical_optimization_readiness,
)
from watcher_foundation.setup_outcome_proof import (
    SETUP_OUTCOME_DIAGNOSTIC_FIX_PATHS,
    SETUP_OUTCOME_PROOF_REQUIRED_FIELDS,
    SETUP_OUTCOME_PROOF_RESULT_FIELDS,
    SETUP_OUTCOME_PROOF_STATUSES,
    evaluate_setup_outcome_proof,
    validate_setup_outcome_proof_record,
)
from watcher_foundation.setup_outcome_diagnostics import (
    SETUP_OUTCOME_DIAGNOSTICS_RESULT_FIELDS,
    SETUP_OUTCOME_DIAGNOSTIC_FAILURE_CATEGORIES,
    evaluate_setup_outcome_diagnostics,
)
from watcher_foundation.setup_outcome_evidence_packet import (
    SETUP_OUTCOME_EVIDENCE_PACKET_ITEM_FIELDS,
    SETUP_OUTCOME_EVIDENCE_PACKET_RESULT_FIELDS,
    build_setup_outcome_evidence_packet,
)
from watcher_foundation.setup_outcome_packet_readiness import (
    SETUP_OUTCOME_PACKET_READINESS_ITEM_FIELDS,
    SETUP_OUTCOME_PACKET_READINESS_RESULT_FIELDS,
    SETUP_OUTCOME_PACKET_READINESS_STATUSES,
    evaluate_setup_outcome_packet_readiness,
)
from watcher_foundation.setup_outcome_review_aggregator import (
    SETUP_OUTCOME_REVIEW_AGGREGATOR_DECISIONS,
    SETUP_OUTCOME_REVIEW_AGGREGATOR_RESULT_FIELDS,
    SETUP_OUTCOME_REVIEW_OUTCOME_GROUPS,
    aggregate_setup_outcome_proof_review,
)
from watcher_foundation.setup_outcome_review_readiness import (
    SETUP_OUTCOME_REVIEW_READINESS_DECISIONS,
    SETUP_OUTCOME_REVIEW_READINESS_RESULT_FIELDS,
    evaluate_setup_outcome_review_readiness,
)
from watcher_foundation.setup_outcome_proof_review_bundle import (
    SETUP_OUTCOME_PROOF_REVIEW_BUNDLE_DECISIONS,
    SETUP_OUTCOME_PROOF_REVIEW_BUNDLE_RESULT_FIELDS,
    build_setup_outcome_proof_review_bundle,
)
from watcher_foundation.setup_outcome_proof_review_bundle_readiness import (
    SETUP_OUTCOME_PROOF_REVIEW_BUNDLE_READINESS_DECISIONS,
    SETUP_OUTCOME_PROOF_REVIEW_BUNDLE_READINESS_RESULT_FIELDS,
    evaluate_setup_outcome_proof_review_bundle_readiness,
)
from watcher_foundation.setup_outcome_historical_sample_path import (
    FIRST_CONTROLLED_HISTORICAL_SAMPLE_EVIDENCE_SET_ID,
    HISTORICAL_SAMPLE_PATH_OUTPUT_REVIEW_RESULT_FIELDS,
    HISTORICAL_SAMPLE_PATH_RESULT_FIELDS,
    build_first_controlled_historical_sample_evidence_set,
    review_first_controlled_historical_sample_path_output,
    review_setup_outcome_historical_sample_path_output,
    run_setup_outcome_historical_sample_path,
)
from watcher_foundation.day60_shadow_review_packet import (
    DAY60_SHADOW_REVIEW_PACKET_DIAGNOSTIC_PLACEHOLDER_FIELDS,
    DAY60_SHADOW_REVIEW_PACKET_OUTCOME_PLACEHOLDER_FIELDS,
    DAY60_SHADOW_REVIEW_PACKET_RESULT_FIELDS,
    DAY60_SHADOW_REVIEW_PACKET_VIABILITY_PLACEHOLDER_FIELDS,
    build_day60_shadow_review_packet,
)
from watcher_foundation.day60_shadow_readiness import (
    DAY60_SHADOW_READINESS_REQUIRED_PROOF_FIELDS,
    DAY60_SHADOW_READINESS_RESULT_FIELDS,
    evaluate_day60_shadow_readiness,
)
from watcher_foundation.day60_shadow_session import (
    DAY60_SHADOW_SESSION_RESULT_FIELDS,
    run_day60_shadow_session_dry_run,
)
from watcher_foundation.diagnostics import (
    DIAGNOSTIC_REASON_CODE_GROUPS,
    build_diagnostics,
    create_diagnostics,
)
from watcher_foundation.duplicate_suppression import (
    DUPLICATE_SUPPRESSION_FINGERPRINT_VERSION,
    DUPLICATE_SUPPRESSION_KEY_FIELD_NAMES,
    MATERIAL_CHANGE_FLAGS_THAT_BREAK_SUPPRESSION,
    build_duplicate_suppression_key_fields,
    build_suppression_fingerprint,
    decide_duplicate_suppression,
)
from watcher_foundation.focus_ranking import FOCUS_RANK_BUCKETS, rank_focus_candidates
from watcher_foundation.headline_news import (
    REQUIRED_HEADLINE_NEWS_POLICY_FIELDS,
    VALID_SOURCE_STATUSES,
    create_headline_news_policy,
    evaluate_headline_news_policy,
)
from watcher_foundation.models import (
    WatchOnlyCandidateState,
    reject_forbidden_execution_fields,
)
from watcher_foundation.pipeline import PIPELINE_RESULT_FIELDS, run_local_watcher_pipeline
from watcher_foundation.replay_regression import (
    REPLAY_REGRESSION_RESULT_FIELDS,
    ReplayRegressionCase,
    run_local_replay_regression,
)
from watcher_foundation.state_tracker import WatcherTrackedState, update_watcher_state
from watcher_foundation.shadow_log import (
    ALLOWED_SHADOW_LOG_EVENT_TYPES,
    DEFAULT_REVIEW_LABEL,
    REQUIRED_SHADOW_LOG_FIELDS,
    SHADOW_LOG_SCHEMA_VERSION,
    append_shadow_log_line,
    create_shadow_log_record,
    serialize_shadow_log_line,
)
from watcher_foundation.shadow_review import (
    ALLOWED_SHADOW_REVIEW_LABELS,
    REQUIRED_SHADOW_REVIEW_FIELDS,
    SHADOW_REVIEW_EXPORT_BUNDLE_REQUIRED_FIELDS,
    SHADOW_REVIEW_EXPORT_BUNDLE_REVIEW_PACKAGE_REQUIRED_FIELDS,
    SHADOW_REVIEW_EXPORT_REQUIRED_FIELDS,
    SHADOW_REVIEW_WORKFLOW_SUMMARY_FIELDS,
    run_local_shadow_review_label_workflow,
    validate_shadow_review_export_bundle,
    validate_shadow_review_export_bundle_review_package,
    validate_shadow_review_export_shape,
    validate_shadow_review_label,
)
from watcher_foundation.trigger_card import (
    REQUIRED_TRIGGER_CARD_FIELDS,
    project_trigger_card,
)

__all__ = [
    "ACCEPTED_HEADLINE_NEWS_STATUSES",
    "ACCEPTED_SETUP_TYPES",
    "ACCEPTED_STAGES",
    "ACCEPTED_TRIGGER_STATUSES",
    "ALLOWED_SHADOW_LOG_EVENT_TYPES",
    "ALLOWED_SHADOW_REVIEW_LABELS",
    "BATCH_RUNNER_RESULT_FIELDS",
    "DAY60_OUTCOME_SCORING_CONTRACT_REQUIRED_FIELDS",
    "DAY60_OUTCOME_SCORING_CONTRACT_REQUIRED_PROOF_FIELDS",
    "DAY60_OUTCOME_SCORING_CONTRACT_RESULT_FIELDS",
    "DAY60_OUTCOME_REVIEW_BUCKETS",
    "DAY60_OUTCOME_SCORING_SUMMARY_RESULT_FIELDS",
    "DAY60_OUTCOME_DIAGNOSTICS_RESULT_FIELDS",
    "DAY60_OUTCOME_DIAGNOSTIC_FAILURE_CATEGORIES",
    "DAY60_OUTCOME_DIAGNOSTIC_FIX_PATHS",
    "DAY60_OPTIMIZATION_ALLOWED_SYSTEM_AREAS",
    "DAY60_OPTIMIZATION_READINESS_REQUIRED_FIELDS",
    "DAY60_OPTIMIZATION_READINESS_RESULT_FIELDS",
    "DAY60_SHADOW_CONTRACT_DIAGNOSTIC_PLACEHOLDER_FIELDS",
    "DAY60_SHADOW_CONTRACT_REQUIRED_FIELDS",
    "DAY60_SHADOW_CONTRACT_TRIGGER_CARD_REQUIRED_FIELDS",
    "DAY60_SHADOW_REVIEW_PACKET_DIAGNOSTIC_PLACEHOLDER_FIELDS",
    "DAY60_SHADOW_REVIEW_PACKET_OUTCOME_PLACEHOLDER_FIELDS",
    "DAY60_SHADOW_REVIEW_PACKET_RESULT_FIELDS",
    "DAY60_SHADOW_REVIEW_PACKET_VIABILITY_PLACEHOLDER_FIELDS",
    "DAY60_SHADOW_READINESS_REQUIRED_PROOF_FIELDS",
    "DAY60_SHADOW_READINESS_RESULT_FIELDS",
    "DAY60_SHADOW_SESSION_RESULT_FIELDS",
    "DEFAULT_REVIEW_LABEL",
    "DISCRETION_AUDIT_ALLOWED_HUMAN_DISCRETION",
    "DISCRETION_AUDIT_AREAS",
    "DISCRETION_AUDIT_COVERAGE_RESULT_FIELDS",
    "DISCRETION_AUDIT_INVENTORY_ALLOWED_AREAS",
    "DISCRETION_AUDIT_INVENTORY_BRIDGE_RESULT_FIELDS",
    "DISCRETION_AUDIT_INVENTORY_REQUIRED_FIELDS",
    "DISCRETION_AUDIT_INVENTORY_RESULT_FIELDS",
    "DISCRETION_AUDIT_REQUIRED_COVERAGE_AREAS",
    "DISCRETION_AUDIT_RESULT_FIELDS",
    "DISCRETION_AUDIT_VAGUE_PHRASES",
    "DIAGNOSTIC_REASON_CODE_GROUPS",
    "DUPLICATE_SUPPRESSION_FINGERPRINT_VERSION",
    "DUPLICATE_SUPPRESSION_KEY_FIELD_NAMES",
    "EXPLICIT_UNCONFIRMED_MARKERS",
    "FIRST_CONTROLLED_HISTORICAL_SAMPLE_EVIDENCE_SET_ID",
    "FOCUS_RANK_BUCKETS",
    "HISTORICAL_OUTCOME_PROOF_PREFLIGHT_REQUIRED_FIELDS",
    "HISTORICAL_OUTCOME_PROOF_PREFLIGHT_RESULT_FIELDS",
    "HISTORICAL_OUTCOME_PROOF_SUMMARY_RESULT_FIELDS",
    "HISTORICAL_OUTCOME_DIAGNOSTICS_RESULT_FIELDS",
    "HISTORICAL_OUTCOME_DIAGNOSTIC_FAILURE_CATEGORIES",
    "HISTORICAL_OUTCOME_DIAGNOSTIC_FIX_PATHS",
    "HISTORICAL_OPTIMIZATION_ALLOWED_SYSTEM_AREAS",
    "HISTORICAL_SAMPLE_PATH_OUTPUT_REVIEW_RESULT_FIELDS",
    "HISTORICAL_SAMPLE_PATH_RESULT_FIELDS",
    "HISTORICAL_OPTIMIZATION_READINESS_REQUIRED_FIELDS",
    "HISTORICAL_OPTIMIZATION_READINESS_RESULT_FIELDS",
    "SETUP_OUTCOME_DIAGNOSTIC_FIX_PATHS",
    "SETUP_OUTCOME_DIAGNOSTICS_RESULT_FIELDS",
    "SETUP_OUTCOME_DIAGNOSTIC_FAILURE_CATEGORIES",
    "SETUP_OUTCOME_EVIDENCE_PACKET_ITEM_FIELDS",
    "SETUP_OUTCOME_EVIDENCE_PACKET_RESULT_FIELDS",
    "SETUP_OUTCOME_PACKET_READINESS_ITEM_FIELDS",
    "SETUP_OUTCOME_PACKET_READINESS_RESULT_FIELDS",
    "SETUP_OUTCOME_PACKET_READINESS_STATUSES",
    "SETUP_OUTCOME_PROOF_REQUIRED_FIELDS",
    "SETUP_OUTCOME_PROOF_REVIEW_BUNDLE_DECISIONS",
    "SETUP_OUTCOME_PROOF_REVIEW_BUNDLE_READINESS_DECISIONS",
    "SETUP_OUTCOME_PROOF_REVIEW_BUNDLE_READINESS_RESULT_FIELDS",
    "SETUP_OUTCOME_PROOF_REVIEW_BUNDLE_RESULT_FIELDS",
    "SETUP_OUTCOME_PROOF_RESULT_FIELDS",
    "SETUP_OUTCOME_PROOF_STATUSES",
    "SETUP_OUTCOME_REVIEW_AGGREGATOR_DECISIONS",
    "SETUP_OUTCOME_REVIEW_AGGREGATOR_RESULT_FIELDS",
    "SETUP_OUTCOME_REVIEW_OUTCOME_GROUPS",
    "SETUP_OUTCOME_REVIEW_READINESS_DECISIONS",
    "SETUP_OUTCOME_REVIEW_READINESS_RESULT_FIELDS",
    "MATERIAL_CHANGE_FLAGS_THAT_BREAK_SUPPRESSION",
    "NEWS_UNCONFIRMED",
    "PIPELINE_RESULT_FIELDS",
    "REQUIRED_SHADOW_LOG_FIELDS",
    "REQUIRED_SHADOW_REVIEW_FIELDS",
    "SHADOW_REVIEW_EXPORT_BUNDLE_REQUIRED_FIELDS",
    "SHADOW_REVIEW_EXPORT_BUNDLE_REVIEW_PACKAGE_REQUIRED_FIELDS",
    "SHADOW_REVIEW_EXPORT_REQUIRED_FIELDS",
    "SHADOW_REVIEW_WORKFLOW_SUMMARY_FIELDS",
    "REQUIRED_HEADLINE_NEWS_POLICY_FIELDS",
    "REQUIRED_TRIGGER_CARD_FIELDS",
    "REPLAY_REGRESSION_RESULT_FIELDS",
    "SHADOW_LOG_SCHEMA_VERSION",
    "VALID_SOURCE_STATUSES",
    "ReplayRegressionCase",
    "WatchOnlyCandidateState",
    "WatcherTrackedState",
    "append_shadow_log_line",
    "audit_trading_plan_discretion",
    "build_diagnostics",
    "build_day60_shadow_review_packet",
    "build_day60_outcome_scoring_summary",
    "build_historical_outcome_proof_summary",
    "build_first_controlled_historical_sample_evidence_set",
    "build_setup_outcome_evidence_packet",
    "build_setup_outcome_proof_review_bundle",
    "build_duplicate_suppression_key_fields",
    "build_suppression_fingerprint",
    "create_diagnostics",
    "create_headline_news_policy",
    "create_shadow_log_record",
    "decide_duplicate_suppression",
    "evaluate_headline_news_policy",
    "evaluate_day60_shadow_readiness",
    "evaluate_day60_outcome_diagnostics",
    "evaluate_day60_optimization_readiness",
    "evaluate_historical_outcome_diagnostics",
    "evaluate_historical_optimization_readiness",
    "evaluate_setup_outcome_proof",
    "evaluate_setup_outcome_diagnostics",
    "evaluate_setup_outcome_packet_readiness",
    "aggregate_setup_outcome_proof_review",
    "evaluate_setup_outcome_review_readiness",
    "evaluate_setup_outcome_proof_review_bundle_readiness",
    "evaluate_discretion_audit_coverage",
    "evaluate_discretion_audit_inventory_bridge",
    "project_trigger_card",
    "rank_focus_candidates",
    "reject_forbidden_execution_fields",
    "review_first_controlled_historical_sample_path_output",
    "review_setup_outcome_historical_sample_path_output",
    "run_local_replay_regression",
    "run_day60_shadow_session_dry_run",
    "run_setup_outcome_historical_sample_path",
    "run_local_shadow_review_label_workflow",
    "run_local_watcher_batch",
    "run_local_watcher_pipeline",
    "serialize_shadow_log_line",
    "update_watcher_state",
    "validate_day60_outcome_scoring_batch",
    "validate_day60_outcome_scoring_row",
    "validate_day60_shadow_contract_batch",
    "validate_day60_shadow_contract_row",
    "validate_discretion_audit_inventory",
    "validate_discretion_audit_inventory_item",
    "validate_historical_outcome_proof_batch",
    "validate_historical_outcome_proof_row",
    "validate_setup_outcome_proof_record",
    "validate_shadow_review_export_bundle",
    "validate_shadow_review_export_bundle_review_package",
    "validate_shadow_review_export_shape",
    "validate_shadow_review_label",
]

from .replacement_source_row_packet import validate_replacement_source_row_packet, validate_replacement_source_row_packet_batch

from .replacement_source_row_packet_template import build_replacement_source_row_packet_template, build_all_replacement_source_row_packet_templates, classify_source_row_packet
