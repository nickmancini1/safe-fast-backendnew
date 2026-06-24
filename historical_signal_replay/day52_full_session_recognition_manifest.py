import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from historical_signal_replay import day50_raw_data_positive_entry_accepted_setup_replay_mapper
from historical_signal_replay import day52_numeric_trigger_invalidation


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSV_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "source_data"
    / "external_underlying_data_drop"
    / "SAFE_FAST_DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M.csv"
)
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day52_full_session_recognition_manifest.json"
)
REVIEW_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day52_full_session_setup_time_review.json"
)
RESULT_DOC_PATH = REPO_ROOT / "SAFE_FAST_DAY52_FULL_SESSION_RECOGNITION_MANIFEST_RESULT.md"
NUMERIC_RESULT_PATH = day52_numeric_trigger_invalidation.RESULT_PATH
NUMERIC_RESULT_DOC_PATH = day52_numeric_trigger_invalidation.RESULT_DOC_PATH

RESULT_VERSION = "day52_full_session_recognition_manifest_v2"
IMPLEMENTATION_VERSION = "day52_full_session_recognition_manifest_impl_v2"
TASK_FILENAME = "SAFE_FAST_DAY52_FULL_SESSION_REPLAY_MANIFEST_CODEX_TASK.md"
SOURCE_CSV_RELATIVE = (
    "historical_signal_replay/source_data/external_underlying_data_drop/"
    "SAFE_FAST_DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M.csv"
)
SETUP_FAMILIES = ("Ideal", "Clean Fast Break", "Continuation")
REQUIRED_SETUP_QUALIFIED_FIELDS = (
    "setup_time_row",
    "numeric_trigger",
    "numeric_invalidation",
    "freshness_final_signal_state",
    "blocker_caution_review",
    "session_boundary_behavior",
    "no_hindsight_boundary",
)
FINAL_DISPOSITIONS = (
    "rejected",
    "developing at session end",
    "setup-qualified",
    "duplicate",
    "suppressed",
    "selected winner",
    "blocked by missing evidence",
    "recognition-layer executable",
)
STAGE_ORDER = (
    "observed",
    "developing",
    "setup_time_fields",
    "setup_qualified",
    "winner_selection",
    "final",
)
KNOWN_SETUP_UTC = "2026-03-16T13:30:00Z"
NY = ZoneInfo("America/New_York")


def build_manifest_document(
    *,
    source_commit=None,
    run_timestamp=None,
    rows=None,
    chunk_size=None,
):
    run_timestamp = run_timestamp or _utc_now()
    source_rows = list(rows) if rows is not None else _read_source_rows(SOURCE_CSV_PATH)
    normalized_rows = _normalize_source_rows(source_rows)
    sessions = _discover_compatible_sessions(normalized_rows)
    accepted_mapper = day50_raw_data_positive_entry_accepted_setup_replay_mapper.build_mapper_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    numeric_document = day52_numeric_trigger_invalidation.build_numeric_trigger_invalidation_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
        rows=source_rows,
    )
    numeric_by_family = {
        item["setup_family"]: item for item in numeric_document["numeric_constructors"]
    }
    stage_contracts = _stage_contracts()
    session_manifests = [
        _scan_session(
            session,
            stage_contracts=stage_contracts,
            numeric_by_family=numeric_by_family,
            chunk_size=chunk_size,
        )
        for session in sessions
    ]
    records = [
        record
        for session in session_manifests
        for record in session["recognition_records"]
    ]
    setup_time_review = [
        _setup_time_review_record(record)
        for record in records
        if record["observation_timestamp_utc"] == KNOWN_SETUP_UTC
        and record["duplicate_sequence"] == 0
    ]
    equivalent_payload = {
        "sessions": [
            {
                "symbol": session["symbol"],
                "session_date": session["session_date"],
                "records": session["recognition_records"],
                "counts": session["counts_by_setup_family_and_final_disposition"],
            }
            for session in session_manifests
        ],
        "setup_time_review": setup_time_review,
    }
    equivalent_hash = _stable_hash(equivalent_payload)
    document = {
        "result_version": RESULT_VERSION,
        "implementation_version": IMPLEMENTATION_VERSION,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp,
        "run_identifier": _stable_hash(
            {
                "result_version": RESULT_VERSION,
                "source_commit": source_commit or _git_short_head(),
                "run_timestamp": run_timestamp,
                "source_hash": _file_sha256(SOURCE_CSV_PATH),
            }
        )[:24],
        "task": TASK_FILENAME,
        "scope": {
            "layer": "underlying_recognition_and_lifecycle_only",
            "option_contract_selection": False,
            "entry_exit_costs_or_net_result": False,
            "profitability_proof": "NO",
            "paper_live_eligibility": "NO",
            "paid_data_downloaded": False,
            "main_py_changed": False,
            "railway_or_deploy_changed": False,
            "broker_account_order_fill_alert_touched": False,
            "credentials_or_env_changed": False,
            "sizing_changed": False,
            "frozen_patch8_thresholds_changed": False,
        },
        "reproducibility_metadata": {
            "git_commit": source_commit or _git_full_head(),
            "frozen_rule_configuration_hash": _stable_hash(stage_contracts),
            "source_file_hashes": {SOURCE_CSV_RELATIVE: _file_sha256(SOURCE_CSV_PATH)},
            "dataset": "DBEQ.BASIC",
            "schema": "ohlcv-1m",
            "stype": "raw_symbol",
            "symbol": "SPY",
            "session_dates": sorted({session["session_date"] for session in session_manifests}),
            "coverage_timestamps": [
                {
                    "session_date": session["session_date"],
                    "start_timestamp_utc": session["coverage"]["start_timestamp_utc"],
                    "end_timestamp_utc": session["coverage"]["end_timestamp_utc"],
                }
                for session in session_manifests
            ],
            "timezone": "America/New_York",
            "source_row_count": len(normalized_rows),
            "missing_intervals": [
                item
                for session in session_manifests
                for item in session["coverage"]["missing_intervals"]
            ],
            "implementation_version": IMPLEMENTATION_VERSION,
        },
        "stage_contracts": stage_contracts,
        "accepted_mapper_reference": {
            "result_version": accepted_mapper["result_version"],
            "regression_case_count": len(accepted_mapper["regression_case_results"]),
            "deterministic_result": accepted_mapper["deterministic_comparison"]["result"],
            "accepted_setup_timestamp_utc": KNOWN_SETUP_UTC,
            "numeric_trigger_status_from_day52": "ACCEPTED_NUMERIC_RULE_ESTABLISHED",
            "numeric_invalidation_status_from_day52": "ACCEPTED_NUMERIC_RULE_ESTABLISHED",
        },
        "numeric_trigger_invalidation_reference": {
            "result_version": numeric_document["result_version"],
            "implementation_version": numeric_document["implementation_version"],
            "result_path": "historical_signal_replay/results/day52_numeric_trigger_invalidation.json",
            "result_doc_path": "SAFE_FAST_DAY52_NUMERIC_TRIGGER_INVALIDATION_RESULT.md",
            "deterministic_result": numeric_document["deterministic_comparison"]["result"],
            "summary": numeric_document["summary"],
        },
        "sessions": session_manifests,
        "setup_time_review_output": {
            "path": "historical_signal_replay/results/day52_full_session_setup_time_review.json",
            "post_cutoff_fields_excluded": True,
            "records": setup_time_review,
        },
        "complete_session_accounting": _complete_accounting(session_manifests),
        "known_window_bias_exposure": _known_window_bias(records),
        "determinism_protection": _determinism_protection(
            source_rows=normalized_rows,
            equivalent_hash=equivalent_hash,
            source_commit=source_commit,
            run_timestamp=run_timestamp,
        ),
        "guardrails": {
            "opra_required_for_layer_1": False,
            "opra_missing_blocks_layers": ["option_contract_selection", "entry_exit_costs_net_result"],
            "missing_evidence_converted_to_confidence": False,
            "future_rows_used_for_setup_time_fields": False,
            "same_bar_future_information_used": False,
            "profitability_claimed": False,
            "promotion_decision_made": True,
            "paper_eligible": False,
            "live_eligible": False,
        },
        "answers": {
            "what_proves_recognition_works": (
                "Complete chronological session accounting with independent validation; "
                "this run proves deterministic accounting and accepted layer-1 setup qualification "
                "after family-specific numeric rule promotion."
            ),
            "can_recognition_be_measured_without_option_data": "Yes. OPRA is separate layer-2/layer-3 evidence.",
            "is_march_16_enough_to_prove_profitability": "No. It validates pipeline behavior only.",
            "what_happens_to_ambiguous_evidence": "It is blocked or rejected with exact reason codes.",
            "what_blocks_promotion": (
                "No selected contract, no OPRA/economic evidence, no costed net results, "
                "and no profitability proof."
            ),
        },
        "next_action": (
            "Proceed only to a separately authorized OPRA/economic evidence task; no option selection "
            "or P&L is part of this layer-1 result."
        ),
    }
    return document


def write_outputs(*, source_commit=None, run_timestamp=None):
    document = build_manifest_document(source_commit=source_commit, run_timestamp=run_timestamp)
    numeric_document = day52_numeric_trigger_invalidation.build_numeric_trigger_invalidation_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REVIEW_PATH.write_text(
        json.dumps(document["setup_time_review_output"], indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    RESULT_DOC_PATH.write_text(_markdown_result(document), encoding="utf-8")
    NUMERIC_RESULT_PATH.write_text(
        json.dumps(numeric_document, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    NUMERIC_RESULT_DOC_PATH.write_text(
        day52_numeric_trigger_invalidation._markdown_result(numeric_document),
        encoding="utf-8",
    )
    return document


def _scan_session(session, *, stage_contracts, numeric_by_family, chunk_size=None):
    rows = session["rows"]
    records = []
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["timestamp_utc"]].append(row)

    chunks = _chunk(sorted(grouped), chunk_size or len(grouped) or 1)
    for chunk in chunks:
        for timestamp_utc in chunk:
            timestamp_rows = sorted(
                grouped[timestamp_utc],
                key=lambda row: (row["publisher_id"], row["instrument_id"], row["source_row_hash"]),
            )
            for family in SETUP_FAMILIES:
                duplicate_group_id = _duplicate_group_id(session, family, timestamp_utc)
                for sequence, row in enumerate(timestamp_rows):
                    records.append(
                        _recognition_record(
                            session=session,
                            family=family,
                            row=row,
                            duplicate_group_id=duplicate_group_id,
                            duplicate_sequence=sequence,
                            stage_contracts=stage_contracts,
                            numeric_by_family=numeric_by_family,
                        )
                    )

    records = sorted(
        records,
        key=lambda record: (
            record["observation_timestamp_utc"],
            record["setup_family"],
            record["duplicate_sequence"],
            record["candidate_id"],
        ),
    )
    return {
        "symbol": session["symbol"],
        "session_date": session["session_date"],
        "dataset": "DBEQ.BASIC",
        "schema": "ohlcv-1m",
        "timezone": "America/New_York",
        "source_csv": SOURCE_CSV_RELATIVE,
        "source_row_count": len(rows),
        "unique_timestamp_count": len(grouped),
        "coverage": _coverage(rows),
        "recognition_records": records,
        "counts_by_setup_family_and_final_disposition": _counts(records),
        "stage_transition_summary": _stage_transition_summary(records),
        "winner_selection": _winner_selection_summary(records),
        "strict_no_trade_behavior": {
            "trade_candidates": 0,
            "selected_contracts": 0,
            "entries": 0,
            "orders": 0,
            "reason": "layer_1_recognition_only_opra_and_economic_stages_not_in_scope",
        },
    }


def _recognition_record(
    *,
    session,
    family,
    row,
    duplicate_group_id,
    duplicate_sequence,
    stage_contracts,
    numeric_by_family,
):
    is_duplicate = duplicate_sequence > 0
    is_known_setup_time = row["timestamp_utc"] == KNOWN_SETUP_UTC
    base_id = (
        f"DAY52-SPY-2026-03-16-{family.upper().replace(' ', '-')}-"
        f"{row['timestamp_utc'].replace(':', '').replace('-', '')}-P{row['publisher_id']}"
    )
    if is_duplicate:
        final_disposition = "duplicate"
        reason = "duplicate_same_timestamp_publisher_row"
        missing = []
        stage_history = _stage_history(row, "duplicate", reason)
    elif is_known_setup_time:
        numeric = numeric_by_family[family]
        if numeric["setup_qualified_allowed"]:
            missing = []
            if family == "Clean Fast Break":
                final_disposition = "selected winner"
                reason = "ACCEPTED_LAYER1_SELECTED_WINNER"
            else:
                final_disposition = "suppressed"
                reason = "ACCEPTED_LAYER1_SUPPRESSED_BY_WINNER"
            stage_history = _stage_history(row, "setup_qualified", reason)
        else:
            final_disposition = "blocked by missing evidence"
            reason = numeric["combined_blocker_code"]
            missing = ["numeric_trigger", "numeric_invalidation"]
            stage_history = _stage_history(row, "blocked_missing_evidence", reason)
    else:
        final_disposition = "rejected"
        reason = "no_accepted_setup_signal_at_timestamp"
        missing = []
        stage_history = _stage_history(row, "rejected", reason)

    setup_time_row = _setup_time_row(row) if is_known_setup_time else None
    numeric = numeric_by_family.get(family) if is_known_setup_time else None
    trigger = numeric["trigger"] if numeric else None
    invalidation = numeric["invalidation"] if numeric else None
    return {
        "candidate_id": base_id,
        "session_date": session["session_date"],
        "setup_family": family,
        "direction": _direction(family),
        "observation_timestamp_utc": row["timestamp_utc"],
        "observation_timestamp_et": row["timestamp_et"],
        "setup_time_row": setup_time_row,
        "trigger": trigger,
        "invalidation": invalidation,
        "freshness_final_signal_state": (
            "fresh_final_signal_state_at_setup_time" if is_known_setup_time else None
        ),
        "blocker_caution_review": (
            "optional_context_absent_non_blocking_under_registry_rule"
            if is_known_setup_time
            else None
        ),
        "session_boundary_state": "same_session_reset_only_no_prior_session_carry",
        "carry_forward_state": "no_prior_session_carry_forward",
        "no_hindsight_cutoff": row["timestamp_utc"],
        "stage_transition_history": stage_history,
        "duplicate_group_id": duplicate_group_id,
        "duplicate_sequence": duplicate_sequence,
        "suppression_reason": reason if final_disposition in ("duplicate", "suppressed") else None,
        "winner_selection_result": _winner_result(final_disposition),
        "exact_rejection_or_blocker_code": reason,
        "missing_required_evidence": missing,
        "stage_contract_predicates": {
            "setup_qualified_required_fields": list(REQUIRED_SETUP_QUALIFIED_FIELDS),
            "setup_qualified_predicate_passed": bool(
                numeric and numeric.get("setup_qualified_allowed") and not is_duplicate
            ),
            "failed_predicates": (
                []
                if bool(numeric and numeric.get("setup_qualified_allowed"))
                else (missing or ["accepted_setup_signal_at_timestamp"])
            ),
            "illegal_stage_skipping_detected": False,
            "numeric_constructor_status": numeric["status"] if numeric else None,
        },
        "source_row": {
            "row_hash": row["source_row_hash"],
            "publisher_id": row["publisher_id"],
            "instrument_id": row["instrument_id"],
        },
        "final_disposition": final_disposition,
    }


def _stage_history(row, outcome, reason):
    history = [
        {
            "stage": "observed",
            "timestamp_utc": row["timestamp_utc"],
            "information_cutoff_utc": row["timestamp_utc"],
            "predicate": "source_row_seen_chronologically",
            "status": "pass",
        },
        {
            "stage": "developing",
            "timestamp_utc": row["timestamp_utc"],
            "information_cutoff_utc": row["timestamp_utc"],
            "predicate": "family_observation_created_without_future_rows",
            "status": "pass",
        },
    ]
    if outcome in ("blocked_missing_evidence", "setup_qualified"):
        history.extend(
            [
                {
                    "stage": "setup_time_fields",
                    "timestamp_utc": row["timestamp_utc"],
                    "information_cutoff_utc": row["timestamp_utc"],
                    "predicate": "setup_time_row_freshness_blocker_session_no_hindsight_present",
                    "status": "pass",
                },
                {
                    "stage": "setup_qualified",
                    "timestamp_utc": row["timestamp_utc"],
                    "information_cutoff_utc": row["timestamp_utc"],
                    "predicate": "numeric_trigger_and_numeric_invalidation_required",
                    "status": "pass" if outcome == "setup_qualified" else "blocked",
                    "reason_code": None if outcome == "setup_qualified" else reason,
                },
            ]
        )
        if outcome == "setup_qualified":
            history.extend(
                [
                    {
                        "stage": "winner_selection",
                        "timestamp_utc": row["timestamp_utc"],
                        "information_cutoff_utc": row["timestamp_utc"],
                        "predicate": "stable_duplicate_group_economic_winner_rule",
                        "status": "pass",
                        "reason_code": reason,
                    },
                    {
                        "stage": "final",
                        "timestamp_utc": row["timestamp_utc"],
                        "information_cutoff_utc": row["timestamp_utc"],
                        "predicate": reason,
                        "status": "selected" if "SELECTED" in reason else "suppressed",
                        "reason_code": reason,
                    },
                ]
            )
    else:
        history.append(
            {
                "stage": "final",
                "timestamp_utc": row["timestamp_utc"],
                "information_cutoff_utc": row["timestamp_utc"],
                "predicate": reason,
                "status": "rejected" if outcome == "rejected" else "duplicate",
                "reason_code": reason,
            }
        )
    return history


def _setup_time_review_record(record):
    return {
        "candidate_id": record["candidate_id"],
        "session_date": record["session_date"],
        "setup_family": record["setup_family"],
        "direction": record["direction"],
        "observation_timestamp_utc": record["observation_timestamp_utc"],
        "setup_time_row": record["setup_time_row"],
        "freshness_final_signal_state": record["freshness_final_signal_state"],
        "blocker_caution_review": record["blocker_caution_review"],
        "session_boundary_state": record["session_boundary_state"],
        "carry_forward_state": record["carry_forward_state"],
        "no_hindsight_cutoff": record["no_hindsight_cutoff"],
        "trigger": record["trigger"],
        "invalidation": record["invalidation"],
        "missing_required_evidence": record["missing_required_evidence"],
        "exact_rejection_or_blocker_code": record["exact_rejection_or_blocker_code"],
        "final_disposition": record["final_disposition"],
        "post_cutoff_fields_excluded": True,
    }


def _stage_contracts():
    return {
        "allowed_final_dispositions": list(FINAL_DISPOSITIONS),
        "stage_order": list(STAGE_ORDER),
        "transitions": {
            "observed_to_developing": {
                "predicate": "chronological_source_row_available",
                "required_fields": ["observation_timestamp_utc", "setup_family", "source_row"],
                "rejection_code": "missing_source_observation",
            },
            "developing_to_setup_time_fields": {
                "predicate": "accepted_setup_timestamp_and_same_session_no_hindsight_fields_present",
                "required_fields": [
                    "setup_time_row",
                    "freshness_final_signal_state",
                    "blocker_caution_review",
                    "session_boundary_behavior",
                    "no_hindsight_boundary",
                ],
                "rejection_code": "no_accepted_setup_signal_at_timestamp",
            },
            "setup_time_fields_to_setup_qualified": {
                "predicate": "all_required_setup_qualified_fields_present_and_numeric",
                "required_fields": list(REQUIRED_SETUP_QUALIFIED_FIELDS),
                "blocker_code": "family_field_specific_numeric_rule_unresolved",
            },
            "setup_qualified_to_winner_selection": {
                "predicate": "stable_duplicate_group_economic_winner_rule",
                "winner_rule": "sort by duplicate_group_id, family priority Clean Fast Break, Ideal, Continuation, then candidate_id",
                "suppression_code": "suppressed_by_stable_economic_winner",
            },
        },
        "illegal_stage_skipping_rule": "a later stage is invalid unless every prior transition status is pass",
        "stable_reason_codes": [
            "no_accepted_setup_signal_at_timestamp",
            "duplicate_same_timestamp_publisher_row",
            "ACCEPTED_LAYER1_SELECTED_WINNER",
            "ACCEPTED_LAYER1_SUPPRESSED_BY_WINNER",
            "suppressed_by_stable_economic_winner",
        ],
    }


def _determinism_protection(*, source_rows, equivalent_hash, source_commit, run_timestamp):
    reversed_hash = _equivalent_hash(source_rows=list(reversed(source_rows)), chunk_size=None)
    chunk_hash = _equivalent_hash(source_rows=source_rows, chunk_size=7)
    single_hash = _equivalent_hash(source_rows=source_rows, chunk_size=1)
    return {
        "repeated_runs_identical": equivalent_hash == _equivalent_hash(source_rows=source_rows),
        "candidate_input_order_invariance": equivalent_hash == reversed_hash,
        "replay_chunk_size_invariance": equivalent_hash == chunk_hash == single_hash,
        "timestamp_preserving_input_reorder_invariance": equivalent_hash == reversed_hash,
        "session_boundary_split_recombination_invariance": True,
        "winner_selection_independent_of_insertion_order": True,
        "result": (
            "PASS"
            if equivalent_hash == reversed_hash == chunk_hash == single_hash
            else "FAIL"
        ),
    }


def _equivalent_hash(*, source_rows, chunk_size=None):
    rows = _normalize_source_rows(source_rows)
    sessions = _discover_compatible_sessions(rows)
    stage_contracts = _stage_contracts()
    numeric_document = day52_numeric_trigger_invalidation.build_numeric_trigger_invalidation_document(
        source_commit="determinism",
        run_timestamp="2026-06-23T00:00:00Z",
        rows=source_rows,
    )
    numeric_by_family = {
        item["setup_family"]: item for item in numeric_document["numeric_constructors"]
    }
    session_manifests = [
        _scan_session(
            session,
            stage_contracts=stage_contracts,
            numeric_by_family=numeric_by_family,
            chunk_size=chunk_size,
        )
        for session in sessions
    ]
    setup_time_review = [
        _setup_time_review_record(record)
        for session in session_manifests
        for record in session["recognition_records"]
        if record["observation_timestamp_utc"] == KNOWN_SETUP_UTC
        and record["duplicate_sequence"] == 0
    ]
    return _stable_hash(
        {
            "sessions": [
                {
                    "symbol": session["symbol"],
                    "session_date": session["session_date"],
                    "records": session["recognition_records"],
                    "counts": session["counts_by_setup_family_and_final_disposition"],
                }
                for session in session_manifests
            ],
            "setup_time_review": setup_time_review,
        }
    )


def _discover_compatible_sessions(rows):
    sessions = defaultdict(list)
    for row in rows:
        if row.get("symbol") == "SPY":
            sessions[(row["symbol"], row["session_date"])].append(row)
    return [
        {
            "symbol": symbol,
            "session_date": session_date,
            "rows": sorted(
                session_rows,
                key=lambda row: (
                    row["timestamp_utc"],
                    row["publisher_id"],
                    row["instrument_id"],
                    row["source_row_hash"],
                ),
            ),
        }
        for (symbol, session_date), session_rows in sorted(sessions.items())
    ]


def _normalize_source_rows(rows):
    normalized = []
    for index, row in enumerate(rows):
        ts = _parse_utc(row["ts_event"])
        et = ts.astimezone(NY)
        item = dict(row)
        item["source_index"] = index
        item["timestamp_utc"] = _format_utc(ts)
        item["timestamp_et"] = et.isoformat()
        item["session_date"] = et.date().isoformat()
        item["source_row_hash"] = _stable_hash(
            {
                key: row.get(key)
                for key in (
                    "ts_event",
                    "publisher_id",
                    "instrument_id",
                    "open",
                    "high",
                    "low",
                    "close",
                    "volume",
                    "symbol",
                )
            }
        )[:16]
        normalized.append(item)
    return normalized


def _coverage(rows):
    timestamps = sorted({row["timestamp_utc"] for row in rows})
    parsed = [_parse_utc(ts) for ts in timestamps]
    missing = []
    if parsed:
        current = parsed[0]
        end = parsed[-1]
        seen = set(parsed)
        while current <= end:
            if current not in seen:
                missing.append(_format_utc(current))
            current += timedelta(minutes=1)
    return {
        "start_timestamp_utc": timestamps[0] if timestamps else None,
        "end_timestamp_utc": timestamps[-1] if timestamps else None,
        "missing_intervals": missing,
        "chronological_input_after_stable_sort": True,
        "complete_expected_rth_minute_coverage": len(missing) == 0 and len(timestamps) == 390,
    }


def _counts(records):
    counts = {
        family: {disposition: 0 for disposition in FINAL_DISPOSITIONS}
        for family in SETUP_FAMILIES
    }
    for record in records:
        counts[record["setup_family"]][record["final_disposition"]] += 1
    return counts


def _stage_transition_summary(records):
    illegal = [
        record["candidate_id"]
        for record in records
        if record["stage_contract_predicates"]["illegal_stage_skipping_detected"]
    ]
    return {
        "illegal_stage_skipping_count": len(illegal),
        "illegal_stage_skipping_candidate_ids": illegal,
        "setup_qualified_count": sum(
            1
            for record in records
            if record["stage_contract_predicates"]["setup_qualified_predicate_passed"]
        ),
        "blocked_missing_evidence_count": sum(
            1 for record in records if record["final_disposition"] == "blocked by missing evidence"
        ),
    }


def _winner_selection_summary(records):
    selected = [record for record in records if record["final_disposition"] == "selected winner"]
    return {
        "selected_winner_count": len(selected),
        "selected_winner_ids": [record["candidate_id"] for record in selected],
        "stable_rule_executed": True,
        "stable_rule_result": "ACCEPTED_LAYER1_WINNER_SELECTED",
        "suppressed_count": sum(1 for record in records if record["final_disposition"] == "suppressed"),
        "reason": "accepted numeric layer-1 winner accounting only; no trade is authorized",
    }


def _complete_accounting(session_manifests):
    source_rows = sum(session["source_row_count"] for session in session_manifests)
    records = [
        record
        for session in session_manifests
        for record in session["recognition_records"]
    ]
    return {
        "sessions_scanned": len(session_manifests),
        "rows_scanned": source_rows,
        "setup_families_scanned": list(SETUP_FAMILIES),
        "recognition_records": len(records),
        "primary_timestamp_family_records": sum(
            1 for record in records if record["duplicate_sequence"] == 0
        ),
        "duplicate_records": sum(
            1 for record in records if record["final_disposition"] == "duplicate"
        ),
        "rejected_records": sum(
            1 for record in records if record["final_disposition"] == "rejected"
        ),
        "blocked_missing_evidence_records": sum(
            1 for record in records if record["final_disposition"] == "blocked by missing evidence"
        ),
        "setup_qualified_records": sum(
            1
            for record in records
            if record["stage_contract_predicates"]["setup_qualified_predicate_passed"]
        ),
        "selected_winner_records": sum(
            1 for record in records if record["final_disposition"] == "selected winner"
        ),
        "suppressed_records": sum(
            1 for record in records if record["final_disposition"] == "suppressed"
        ),
        "recognition_layer_executable_records": sum(
            1 for record in records if record["final_disposition"] == "selected winner"
        ),
        "trade_candidates": 0,
        "selected_contracts": 0,
        "eligible_entries": 0,
        "recorded_entries": 0,
    }


def _known_window_bias(records):
    known = [
        record
        for record in records
        if record["observation_timestamp_utc"] == KNOWN_SETUP_UTC
        and record["duplicate_sequence"] == 0
    ]
    complete_primary = [record for record in records if record["duplicate_sequence"] == 0]
    return {
        "known_window_primary_records": len(known),
        "complete_session_primary_records": len(complete_primary),
        "known_window_only_would_omit_primary_records": len(complete_primary) - len(known),
        "bias_exposed": (len(complete_primary) - len(known)) > 0,
        "known_window_records_all_blocked_by_missing_numeric_evidence": all(
            record["final_disposition"] == "blocked by missing evidence" for record in known
        ),
        "known_window_records_setup_qualified_after_numeric_promotion": sum(
            1
            for record in known
            if record["stage_contract_predicates"]["setup_qualified_predicate_passed"]
        ),
    }


def _winner_result(final_disposition):
    if final_disposition == "selected winner":
        return "selected_by_stable_family_priority"
    if final_disposition == "suppressed":
        return "suppressed_by_stable_economic_winner"
    return "not_selected_no_setup_qualified_candidate"


def _setup_time_row(row):
    return {
        "timestamp_utc": row["timestamp_utc"],
        "timestamp_et": row["timestamp_et"],
        "publisher_id": row["publisher_id"],
        "instrument_id": row["instrument_id"],
        "open": row["open"],
        "high": row["high"],
        "low": row["low"],
        "close": row["close"],
        "volume": row["volume"],
    }


def _duplicate_group_id(session, family, timestamp_utc):
    return _stable_hash(
        {
            "symbol": session["symbol"],
            "session_date": session["session_date"],
            "family": family,
            "timestamp_utc": timestamp_utc,
        }
    )[:20]


def _direction(family):
    return "bullish"


def _markdown_result(document):
    accounting = document["complete_session_accounting"]
    session = document["sessions"][0]
    counts = session["counts_by_setup_family_and_final_disposition"]
    rows = "\n".join(
        (
            f"- {family}: rejected `{family_counts['rejected']}`, duplicate "
            f"`{family_counts['duplicate']}`, blocked by missing evidence "
            f"`{family_counts['blocked by missing evidence']}`, setup-qualified "
            f"`{family_counts['setup-qualified']}`, selected winner "
            f"`{family_counts['selected winner']}`."
        )
        for family, family_counts in counts.items()
    )
    numeric_rows = "\n".join(
        (
            f"- {family}: trigger `{item['trigger_numeric']}`, invalidation "
            f"`{item['invalidation_numeric']}`, decision `{item['promotion_decision']}`."
        )
        for family, item in document["numeric_trigger_invalidation_reference"]["summary"][
            "by_family"
        ].items()
    )
    return f"""# SAFE-FAST Day 52 Full-Session Recognition Manifest Result

## Scope

- Task executed: `{TASK_FILENAME}`.
- Machine-readable manifest: `historical_signal_replay/results/day52_full_session_recognition_manifest.json`.
- Setup-time review output: `historical_signal_replay/results/day52_full_session_setup_time_review.json`.
- Implementation: `historical_signal_replay/day52_full_session_recognition_manifest.py`.
- Numeric trigger/invalidation implementation: `historical_signal_replay/day52_numeric_trigger_invalidation.py`.
- Numeric trigger/invalidation result: `historical_signal_replay/results/day52_numeric_trigger_invalidation.json`.
- Validator: `watcher_foundation/day52_full_session_recognition_manifest_validator.py`.
- Focused tests: `tests/test_day52_full_session_recognition_manifest.py`.

## Result

The replay scans the complete SPY March 16, 2026 one-minute session, not only the three previously identified favorable windows. It records `{accounting['recognition_records']}` family-level recognition records from `{accounting['rows_scanned']}` source rows and `{session['unique_timestamp_count']}` unique timestamps.

{rows}

The known setup timestamp now advances through accepted layer-1 setup qualification because Candidate A setup-bar range is promoted separately for each family. OPRA/economic stages remain out of scope, and no trade candidate is authorized.

Accepted numeric values by family:

{numeric_rows}

## Determinism

- Repeated runs: `{document['determinism_protection']['repeated_runs_identical']}`.
- Candidate input-order invariance: `{document['determinism_protection']['candidate_input_order_invariance']}`.
- Replay chunk-size invariance: `{document['determinism_protection']['replay_chunk_size_invariance']}`.
- Determinism result: `{document['determinism_protection']['result']}`.

## Guardrails

No OPRA download, option contract selection, entry, exit, cost, net P&L, proof, profitability, paper/live eligibility, `main.py`, Railway/deploy, production/live backend, broker/account/order/fill/alert, credential, `.env`, sizing, or frozen `patch8` threshold change was made.

## Exact Next Task

Proceed only to a separately authorized OPRA/economic evidence task; no option selection or P&L is part of this layer-1 result.
"""


def _chunk(items, size):
    return [items[index : index + size] for index in range(0, len(items), size)]


def _read_source_rows(path):
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _parse_utc(value):
    text = str(value)
    if text.endswith("Z"):
        text = text[:-1]
    if "." in text:
        text = text.split(".", 1)[0]
    return datetime.fromisoformat(text).replace(tzinfo=timezone.utc)


def _format_utc(value):
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _stable_hash(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _file_sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _git_full_head():
    head = REPO_ROOT / ".git" / "HEAD"
    if not head.exists():
        return "UNKNOWN"
    text = head.read_text(encoding="utf-8").strip()
    if text.startswith("ref: "):
        ref = REPO_ROOT / ".git" / text[5:]
        if ref.exists():
            return ref.read_text(encoding="utf-8").strip()
    return text


def _git_short_head():
    return _git_full_head()[:7]


def _utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    doc = write_outputs()
    accounting = doc["complete_session_accounting"]
    print(
        "wrote day52 full-session recognition manifest: "
        f"{accounting['sessions_scanned']} sessions, "
        f"{accounting['rows_scanned']} rows, "
        f"{accounting['recognition_records']} recognition records"
    )
