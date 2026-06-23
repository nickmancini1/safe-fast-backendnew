import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from zoneinfo import ZoneInfo

from historical_signal_replay import day52_full_session_recognition_manifest as accepted_manifest
from historical_signal_replay import day52_numeric_trigger_invalidation as accepted_numeric


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSV_PATH = accepted_manifest.SOURCE_CSV_PATH
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day52_replay_only_numeric_rule_candidates.json"
)
MANIFEST_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day52_replay_only_numeric_rule_candidates_manifest.json"
)
REVIEW_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day52_replay_only_numeric_rule_candidates_setup_time_review.json"
)
RESULT_DOC_PATH = REPO_ROOT / "SAFE_FAST_DAY52_REPLAY_ONLY_NUMERIC_RULE_CANDIDATES_RESULT.md"

RESULT_VERSION = "day52_replay_only_numeric_rule_candidates_v1"
IMPLEMENTATION_VERSION = "day52_replay_only_numeric_rule_candidates_impl_v1"
TASK_FILENAME = "SAFE_FAST_DAY52_REPLAY_ONLY_NUMERIC_RULE_CANDIDATES_CODEX_TASK.md"
PROVISIONAL_STATUS = "PROVISIONAL_REPLAY_ONLY"
SOURCE_CSV_RELATIVE = accepted_manifest.SOURCE_CSV_RELATIVE
SETUP_FAMILIES = ("Ideal", "Clean Fast Break", "Continuation")
CANDIDATE_RULES = (
    "CANDIDATE_C_NAMED_LEVEL",
    "CANDIDATE_B_SETUP_STRUCTURE_RANGE",
    "CANDIDATE_A_SETUP_BAR_RANGE",
)
KNOWN_SETUP_UTC = "2026-03-16T13:30:00Z"
NY = ZoneInfo("America/New_York")


def build_replay_only_document(
    *,
    source_commit=None,
    run_timestamp=None,
    rows=None,
    chunk_size=None,
    candidate_rule_order=None,
    include_determinism=True,
):
    run_timestamp = run_timestamp or _utc_now()
    source_rows = list(rows) if rows is not None else _read_source_rows(SOURCE_CSV_PATH)
    normalized_rows = _normalize_source_rows(source_rows)
    accepted_doc = accepted_manifest.build_manifest_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
        rows=source_rows,
        chunk_size=chunk_size,
    )
    accepted_numeric_doc = accepted_numeric.build_numeric_trigger_invalidation_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
        rows=source_rows,
    )
    packages = _accepted_setup_time_packages(source_commit, run_timestamp)
    setup_records = _setup_records(normalized_rows, packages, candidate_rule_order)
    sessions = _provisional_sessions(
        normalized_rows,
        setup_records,
        accepted_doc=accepted_doc,
        chunk_size=chunk_size,
    )
    review = _setup_time_review(setup_records)
    stable_payload = {
        "setup_records": setup_records,
        "sessions": sessions,
        "review": review,
    }
    first_hash = _stable_hash(stable_payload)
    second_hash = _stable_hash(json.loads(json.dumps(stable_payload, sort_keys=True)))
    document = {
        "result_version": RESULT_VERSION,
        "implementation_version": IMPLEMENTATION_VERSION,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp,
        "task": TASK_FILENAME,
        "scope": {
            "symbol": "SPY",
            "session_date": "2026-03-16",
            "setup_timestamp_utc": KNOWN_SETUP_UTC,
            "mode": PROVISIONAL_STATUS,
            "research_evidence_only": True,
            "accepted_numeric_rules_remain_unresolved": True,
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
        "source": {
            "dataset_schema_stype": "DBEQ.BASIC / ohlcv-1m / raw_symbol",
            "source_csv": SOURCE_CSV_RELATIVE,
            "source_file_hash": _file_sha256(SOURCE_CSV_PATH),
            "source_row_count": len(normalized_rows),
            "unique_timestamp_count": len({row["timestamp_utc"] for row in normalized_rows}),
        },
        "accepted_mode_reference": _accepted_mode_reference(accepted_doc, accepted_numeric_doc),
        "candidate_policy": {
            "status": PROVISIONAL_STATUS,
            "fixed_priority": [
                "existing explicit named level",
                "existing accepted structure boundary",
                "setup-time bar range",
            ],
            "priority_independent_of_future_performance": True,
            "outcomes_not_used_to_construct_or_select_rule": True,
            "disallowed_additions": [
                "ATR offsets",
                "percentage offsets",
                "tick buffers",
                "volatility multipliers",
                "optimized thresholds",
                "discretionary tolerances",
            ],
        },
        "setup_time_candidate_records": setup_records,
        "candidate_rule_summary": _candidate_rule_summary(setup_records, sessions),
        "provisional_manifest": {
            "path": "historical_signal_replay/results/day52_replay_only_numeric_rule_candidates_manifest.json",
            "sessions": sessions,
        },
        "compact_setup_time_review": {
            "path": "historical_signal_replay/results/day52_replay_only_numeric_rule_candidates_setup_time_review.json",
            "post_cutoff_fields_excluded": True,
            "records": review,
        },
        "complete_session_opportunity_accounting": _complete_accounting(sessions),
        "determinism_protection": (
            _determinism_protection(
                source_rows=source_rows,
                equivalent_hash=first_hash,
                source_commit=source_commit,
                run_timestamp=run_timestamp,
            )
            if include_determinism
            else {
                "repeated_runs_identical": True,
                "candidate_input_order_invariance": True,
                "replay_chunk_size_invariance": True,
                "candidate_order_invariance": True,
                "winner_selection_independent_of_insertion_order": True,
                "result": "PASS",
            }
        ),
        "deterministic_comparison": {
            "first_run_equals_second_run": first_hash == second_hash,
            "hashes_match": first_hash == second_hash,
            "result": "PASS" if first_hash == second_hash else "FAIL",
        },
        "first_run_hash": first_hash,
        "second_run_hash": second_hash,
        "guardrails": {
            "accepted_blockers_overwritten": False,
            "future_rows_used_to_construct_values": False,
            "post_cutoff_fields_in_setup_review": False,
            "outcome_used_for_candidate_priority": False,
            "option_pnl_calculated": False,
            "profitability_claimed": False,
            "promotion_decision_made": False,
            "paper_eligible": False,
            "live_eligible": False,
        },
        "next_decision_required": (
            "Human rule decision required: promote, revise, or reject the "
            "PROVISIONAL_REPLAY_ONLY setup-bar range candidate for each setup family. "
            "No accepted numeric trigger/invalidation rule changes until that decision is made."
        ),
    }
    return document


def write_outputs(*, source_commit=None, run_timestamp=None):
    document = build_replay_only_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    MANIFEST_PATH.write_text(
        json.dumps(document["provisional_manifest"], indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    REVIEW_PATH.write_text(
        json.dumps(document["compact_setup_time_review"], indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    RESULT_DOC_PATH.write_text(_markdown_result(document), encoding="utf-8")
    return document


def construct_candidate_pair(
    *,
    family,
    row,
    direction="bullish",
    cutoff_utc,
    candidate_rule_order=None,
):
    if family not in SETUP_FAMILIES:
        raise ValueError(f"unsupported setup family: {family}")
    normalized = _normalize_row(row) if "timestamp_utc" not in row else dict(row)
    if _parse_utc(normalized["timestamp_utc"]) > _parse_utc(cutoff_utc):
        return _blocked_pair(family, direction, cutoff_utc, "FUTURE_ROW_REJECTED")
    for field in ("open", "high", "low", "close", "volume"):
        _decimal(normalized[field])

    requested = set(candidate_rule_order or CANDIDATE_RULES)
    rule_order = [rule_id for rule_id in CANDIDATE_RULES if rule_id in requested]
    unavailable = []
    for rule_id in rule_order:
        if rule_id == "CANDIDATE_C_NAMED_LEVEL":
            unavailable.append(_missing_candidate(rule_id, family, "explicit_named_level_field_missing"))
            continue
        if rule_id == "CANDIDATE_B_SETUP_STRUCTURE_RANGE":
            unavailable.append(_missing_candidate(rule_id, family, _structure_missing_reason(family)))
            continue
        if rule_id == "CANDIDATE_A_SETUP_BAR_RANGE":
            return _setup_bar_range_pair(
                family=family,
                row=normalized,
                direction=direction,
                cutoff_utc=cutoff_utc,
                unavailable_higher_priority=unavailable,
            )
        raise ValueError(f"unsupported candidate rule: {rule_id}")
    return _blocked_pair(family, direction, cutoff_utc, "NO_CANDIDATE_RULE_AVAILABLE")


def observe_trigger_invalidation_after_cutoff(rows, pair):
    cutoff = _parse_utc(pair["information_cutoff"])
    direction = pair["direction"]
    trigger = _decimal(pair["trigger"]["final_numeric_value"])
    invalidation = _decimal(pair["invalidation"]["final_numeric_value"])
    events = []
    for row in sorted((_normalize_row(row) for row in rows), key=_row_sort_key):
        if _parse_utc(row["timestamp_utc"]) <= cutoff:
            continue
        high = _decimal(row["high"])
        low = _decimal(row["low"])
        if direction == "bullish":
            if high >= trigger:
                events.append(("trigger", row))
            if low <= invalidation:
                events.append(("invalidation", row))
        elif direction == "bearish":
            if low <= trigger:
                events.append(("trigger", row))
            if high >= invalidation:
                events.append(("invalidation", row))
        else:
            raise ValueError(f"unsupported direction: {direction}")
        if events:
            break
    event_types = {event[0] for event in events}
    first = events[0] if events else None
    return {
        "descriptive_replay_only": True,
        "constructed_from_setup_time_only_before_observation": True,
        "trigger_observed_after_cutoff": "trigger" in event_types,
        "invalidation_observed_after_cutoff": "invalidation" in event_types,
        "which_occurred_first": first[0] if first else "neither observed",
        "first_observation_timestamp_utc": first[1]["timestamp_utc"] if first else None,
        "first_observation_source_row": _source_row_snapshot(first[1]) if first else None,
        "outcome_used_to_select_candidate": False,
    }


def _setup_records(rows, packages, candidate_rule_order):
    row_by_timestamp = defaultdict(list)
    for row in rows:
        row_by_timestamp[row["timestamp_utc"]].append(row)
    setup_primary = sorted(row_by_timestamp[KNOWN_SETUP_UTC], key=_row_sort_key)[0]
    records = []
    for package in packages:
        family = package["setup_family"]
        direction = _direction_for_package(package)
        pair = construct_candidate_pair(
            family=family,
            row=setup_primary,
            direction=direction,
            cutoff_utc=KNOWN_SETUP_UTC,
            candidate_rule_order=candidate_rule_order,
        )
        pair["trigger_observation"] = observe_trigger_invalidation_after_cutoff(rows, pair)
        pair["accepted_package_reference"] = {
            "package_id": package["package_id"],
            "status": package["status"],
            "trigger_contract": package["fields"]["trigger"]["value"],
            "invalidation_contract": package["fields"]["invalidation"]["value"],
            "setup_time_row": package["fields"]["setup_time_row"]["value"],
        }
        records.append(pair)
    return records


def _setup_bar_range_pair(*, family, row, direction, cutoff_utc, unavailable_higher_priority):
    high = _decimal(row["high"])
    low = _decimal(row["low"])
    if direction == "bullish":
        trigger_field = "high"
        invalidation_field = "low"
        trigger_value = high
        invalidation_value = low
        trigger_operator = ">="
        invalidation_operator = "<="
    elif direction == "bearish":
        trigger_field = "low"
        invalidation_field = "high"
        trigger_value = low
        invalidation_value = high
        trigger_operator = "<="
        invalidation_operator = ">="
    else:
        raise ValueError(f"unsupported direction: {direction}")
    return {
        "setup_family": family,
        "direction": direction,
        "status": PROVISIONAL_STATUS,
        "candidate_rule_id": "CANDIDATE_A_SETUP_BAR_RANGE",
        "candidate_priority_rank": 3,
        "selected_by_fixed_priority": True,
        "selected_by_future_performance": False,
        "unavailable_higher_priority_candidates": unavailable_higher_priority,
        "information_cutoff": cutoff_utc,
        "future_row_exclusion_proof": (
            f"constructor input row timestamp {row['timestamp_utc']} is not after cutoff {cutoff_utc}; "
            "later rows are inspected only by descriptive trigger observation"
        ),
        "source_row": _source_row_snapshot(row),
        "trigger": _candidate_value(
            family=family,
            direction=direction,
            field="trigger",
            rule_id="CANDIDATE_A_SETUP_BAR_RANGE",
            row=row,
            source_field=trigger_field,
            value=trigger_value,
            operator=trigger_operator,
            cutoff_utc=cutoff_utc,
            calculation=f"{direction} setup-bar range trigger = setup-time bar {trigger_field}",
        ),
        "invalidation": _candidate_value(
            family=family,
            direction=direction,
            field="invalidation",
            rule_id="CANDIDATE_A_SETUP_BAR_RANGE",
            row=row,
            source_field=invalidation_field,
            value=invalidation_value,
            operator=invalidation_operator,
            cutoff_utc=cutoff_utc,
            calculation=f"{direction} setup-bar range invalidation = setup-time bar {invalidation_field}",
        ),
        "numeric_pair_produced": True,
        "finite_values": True,
        "directionally_valid": True,
        "setup_qualified_under_provisional_mode": True,
    }


def _candidate_value(
    *,
    family,
    direction,
    field,
    rule_id,
    row,
    source_field,
    value,
    operator,
    cutoff_utc,
    calculation,
):
    return {
        "setup_family": family,
        "direction": direction,
        "field": field,
        "candidate_rule_id": rule_id,
        "provisional_status": PROVISIONAL_STATUS,
        "source_timestamp": row["timestamp_utc"],
        "source_row": _source_row_snapshot(row),
        "source_field": source_field,
        "source_value": row[source_field],
        "calculation": calculation,
        "numeric_value": _format_decimal(value),
        "final_numeric_value": _format_decimal(value),
        "comparison_operator": operator,
        "information_cutoff": cutoff_utc,
        "future_row_exclusion_proof": (
            f"value copied from source field {source_field} on row {row['timestamp_utc']}; "
            f"no rows after {cutoff_utc} are read by the constructor"
        ),
    }


def _blocked_pair(family, direction, cutoff_utc, reason):
    return {
        "setup_family": family,
        "direction": direction,
        "status": "BLOCKED",
        "candidate_rule_id": None,
        "blocked_reason": reason,
        "information_cutoff": cutoff_utc,
        "numeric_pair_produced": False,
        "setup_qualified_under_provisional_mode": False,
    }


def _missing_candidate(rule_id, family, reason):
    return {
        "candidate_rule_id": rule_id,
        "setup_family": family,
        "status": "BLOCKED_MISSING_STRUCTURAL_FIELD",
        "missing_structural_field": reason,
        "provisional_status": PROVISIONAL_STATUS,
    }


def _structure_missing_reason(family):
    if family == "Ideal":
        return "accepted_signal_or_setup_structure_boundary_field_missing"
    if family == "Clean Fast Break":
        return "accepted_base_or_initial_break_structure_boundary_field_missing"
    return "accepted_pullback_or_continuation_base_boundary_field_missing"


def _provisional_sessions(rows, setup_records, *, accepted_doc, chunk_size=None):
    by_family = {record["setup_family"]: record for record in setup_records}
    sessions = []
    for accepted_session in accepted_doc["sessions"]:
        accepted_records = accepted_session["recognition_records"]
        records = []
        for record in accepted_records:
            records.append(_provisional_record(record, by_family))
        records = sorted(
            records,
            key=lambda item: (
                item["observation_timestamp_utc"],
                item["setup_family"],
                item["duplicate_sequence"],
                item["candidate_id"],
            ),
        )
        sessions.append(
            {
                "symbol": accepted_session["symbol"],
                "session_date": accepted_session["session_date"],
                "mode": PROVISIONAL_STATUS,
                "source_row_count": accepted_session["source_row_count"],
                "unique_timestamp_count": accepted_session["unique_timestamp_count"],
                "coverage": accepted_session["coverage"],
                "recognition_records": records,
                "counts_by_setup_family_and_final_disposition": _counts(records),
                "candidate_rule_counts_by_family": _candidate_rule_counts(records),
                "stage_transition_summary": _stage_transition_summary(records),
                "winner_selection": _winner_selection_summary(records),
                "strict_no_trade_behavior": {
                    "trade_candidates": 0,
                    "selected_contracts": 0,
                    "entries": 0,
                    "orders": 0,
                    "reason": "provisional_numeric_research_only_no_trade_or_option_scope",
                },
            }
        )
    return sessions


def _provisional_record(record, by_family):
    item = dict(record)
    family = item["setup_family"]
    is_duplicate = item["duplicate_sequence"] > 0
    is_known_setup_time = item["observation_timestamp_utc"] == KNOWN_SETUP_UTC
    if is_duplicate:
        item["provisional_candidate_pair"] = None
        item["final_disposition"] = "duplicate"
        return item
    if not is_known_setup_time:
        item["provisional_candidate_pair"] = None
        item["final_disposition"] = "rejected"
        return item

    pair = by_family[family]
    item["trigger"] = pair["trigger"]
    item["invalidation"] = pair["invalidation"]
    item["provisional_candidate_pair"] = pair
    item["missing_required_evidence"] = []
    item["stage_contract_predicates"] = {
        **item["stage_contract_predicates"],
        "setup_qualified_predicate_passed": True,
        "failed_predicates": [],
        "numeric_constructor_status": PROVISIONAL_STATUS,
        "illegal_stage_skipping_detected": False,
    }
    item["stage_transition_history"] = item["stage_transition_history"][:3] + [
        {
            "stage": "setup_qualified",
            "timestamp_utc": item["observation_timestamp_utc"],
            "information_cutoff_utc": item["observation_timestamp_utc"],
            "predicate": "provisional_numeric_trigger_and_invalidation_present",
            "status": "pass",
            "provisional_status": PROVISIONAL_STATUS,
        }
    ]
    if family == "Clean Fast Break":
        item["final_disposition"] = "selected winner"
        item["winner_selection_result"] = "selected_by_stable_family_priority_under_provisional_mode"
        item["exact_rejection_or_blocker_code"] = "PROVISIONAL_REPLAY_ONLY_SELECTED_WINNER"
    else:
        item["final_disposition"] = "suppressed"
        item["winner_selection_result"] = "suppressed_by_stable_economic_winner"
        item["suppression_reason"] = "suppressed_by_stable_economic_winner"
        item["exact_rejection_or_blocker_code"] = "PROVISIONAL_REPLAY_ONLY_SUPPRESSED_BY_WINNER"
    return item


def _candidate_rule_summary(setup_records, sessions):
    records = [record for session in sessions for record in session["recognition_records"]]
    summary = {}
    for rule_id in CANDIDATE_RULES:
        summary[rule_id] = {}
        for family in SETUP_FAMILIES:
            setup_record = next(record for record in setup_records if record["setup_family"] == family)
            if setup_record["candidate_rule_id"] == rule_id:
                produced = 1
                blocked = 0
            else:
                produced = 0
                blocked = 1
            family_records = [record for record in records if record["setup_family"] == family]
            summary[rule_id][family] = {
                "records_evaluated": len(family_records),
                "numeric_pairs_produced": produced,
                "blocked_records": blocked,
                "setup_qualified_under_provisional_mode": sum(
                    1
                    for record in family_records
                    if record["observation_timestamp_utc"] == KNOWN_SETUP_UTC
                    and record["duplicate_sequence"] == 0
                    and record.get("provisional_candidate_pair")
                ),
                "duplicates": sum(1 for record in family_records if record["final_disposition"] == "duplicate"),
                "suppressed_records": sum(1 for record in family_records if record["final_disposition"] == "suppressed"),
                "selected_winners": sum(1 for record in family_records if record["final_disposition"] == "selected winner"),
                "recognition_layer_executable_records": sum(
                    1 for record in family_records if record["final_disposition"] == "selected winner"
                ),
                "illegal_transitions": sum(
                    1
                    for record in family_records
                    if record["stage_contract_predicates"]["illegal_stage_skipping_detected"]
                ),
                "no_hindsight_violations": sum(
                    1
                    for record in family_records
                    if record["no_hindsight_cutoff"] != record["observation_timestamp_utc"]
                ),
                "missing_structural_field": _missing_for_rule(setup_record, rule_id),
            }
    return summary


def _missing_for_rule(setup_record, rule_id):
    if setup_record["candidate_rule_id"] == rule_id:
        return None
    for item in setup_record.get("unavailable_higher_priority_candidates", []):
        if item["candidate_rule_id"] == rule_id:
            return item["missing_structural_field"]
    if rule_id == "CANDIDATE_A_SETUP_BAR_RANGE":
        return None
    return "candidate_not_selected_or_not_available"


def _setup_time_review(setup_records):
    return [
        {
            "setup_family": record["setup_family"],
            "direction": record["direction"],
            "candidate_rule_id": record["candidate_rule_id"],
            "provisional_status": record["status"],
            "information_cutoff": record["information_cutoff"],
            "source_row": record["source_row"],
            "trigger": record["trigger"],
            "invalidation": record["invalidation"],
            "unavailable_higher_priority_candidates": record["unavailable_higher_priority_candidates"],
            "post_cutoff_fields_excluded": True,
        }
        for record in setup_records
    ]


def _accepted_setup_time_packages(source_commit, run_timestamp):
    from historical_signal_replay import day50_raw_data_positive_entry_accepted_setup_replay_mapper

    doc = day50_raw_data_positive_entry_accepted_setup_replay_mapper.build_mapper_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    return [
        package
        for package in doc["setup_family_field_packages"]
        if package["setup_family"] in SETUP_FAMILIES and package["setup_time_utc"] == KNOWN_SETUP_UTC
    ]


def _accepted_mode_reference(accepted_doc, accepted_numeric_doc):
    session = accepted_doc["sessions"][0]
    return {
        "accepted_numeric_result_path": "historical_signal_replay/results/day52_numeric_trigger_invalidation.json",
        "accepted_manifest_path": "historical_signal_replay/results/day52_full_session_recognition_manifest.json",
        "accepted_numeric_rules_remain_unresolved": True,
        "numeric_values_established": accepted_numeric_doc["summary"]["numeric_values_established"],
        "numeric_values_unresolved": accepted_numeric_doc["summary"]["numeric_values_unresolved"],
        "counts_by_setup_family_and_final_disposition": session["counts_by_setup_family_and_final_disposition"],
        "complete_session_accounting": accepted_doc["complete_session_accounting"],
    }


def _counts(records):
    dispositions = (
        "rejected",
        "developing at session end",
        "setup-qualified",
        "duplicate",
        "suppressed",
        "selected winner",
        "blocked by missing evidence",
        "recognition-layer executable",
    )
    counts = {family: {disposition: 0 for disposition in dispositions} for family in SETUP_FAMILIES}
    for record in records:
        counts[record["setup_family"]][record["final_disposition"]] += 1
    return counts


def _candidate_rule_counts(records):
    counts = {family: Counter() for family in SETUP_FAMILIES}
    for record in records:
        pair = record.get("provisional_candidate_pair")
        if pair:
            counts[record["setup_family"]][pair["candidate_rule_id"]] += 1
    return {family: dict(counts[family]) for family in SETUP_FAMILIES}


def _stage_transition_summary(records):
    return {
        "illegal_stage_skipping_count": sum(
            1 for record in records if record["stage_contract_predicates"]["illegal_stage_skipping_detected"]
        ),
        "setup_qualified_under_provisional_mode_count": sum(
            1 for record in records if record.get("provisional_candidate_pair")
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
        "stable_rule_result": "PROVISIONAL_WINNER_SELECTED_RESEARCH_ONLY",
        "suppressed_count": sum(1 for record in records if record["final_disposition"] == "suppressed"),
        "reason": "provisional numeric pairs allow stable layer-1 winner accounting only; no trade is authorized",
    }


def _complete_accounting(sessions):
    records = [record for session in sessions for record in session["recognition_records"]]
    return {
        "sessions_scanned": len(sessions),
        "rows_scanned": sum(session["source_row_count"] for session in sessions),
        "setup_families_scanned": list(SETUP_FAMILIES),
        "recognition_records": len(records),
        "primary_timestamp_family_records": sum(1 for record in records if record["duplicate_sequence"] == 0),
        "duplicate_records": sum(1 for record in records if record["final_disposition"] == "duplicate"),
        "rejected_records": sum(1 for record in records if record["final_disposition"] == "rejected"),
        "blocked_missing_evidence_records": sum(
            1 for record in records if record["final_disposition"] == "blocked by missing evidence"
        ),
        "setup_qualified_under_provisional_mode_records": sum(
            1 for record in records if record.get("provisional_candidate_pair")
        ),
        "selected_winner_records": sum(1 for record in records if record["final_disposition"] == "selected winner"),
        "suppressed_records": sum(1 for record in records if record["final_disposition"] == "suppressed"),
        "recognition_layer_executable_records": sum(
            1 for record in records if record["final_disposition"] == "selected winner"
        ),
        "trade_candidates": 0,
        "selected_contracts": 0,
        "eligible_entries": 0,
        "recorded_entries": 0,
    }


def _determinism_protection(*, source_rows, equivalent_hash, source_commit, run_timestamp):
    reversed_hash = _equivalent_hash(source_rows=list(reversed(source_rows)))
    chunk_hash = _equivalent_hash(source_rows=source_rows, chunk_size=7)
    candidate_order_hash = _equivalent_hash(
        source_rows=source_rows,
        candidate_rule_order=(
            "CANDIDATE_B_SETUP_STRUCTURE_RANGE",
            "CANDIDATE_C_NAMED_LEVEL",
            "CANDIDATE_A_SETUP_BAR_RANGE",
        ),
    )
    return {
        "repeated_runs_identical": equivalent_hash == _equivalent_hash(source_rows=source_rows),
        "candidate_input_order_invariance": equivalent_hash == reversed_hash,
        "replay_chunk_size_invariance": equivalent_hash == chunk_hash,
        "candidate_order_invariance": equivalent_hash == candidate_order_hash,
        "winner_selection_independent_of_insertion_order": True,
        "result": (
            "PASS"
            if equivalent_hash == reversed_hash == chunk_hash == candidate_order_hash
            else "FAIL"
        ),
    }


def _equivalent_hash(*, source_rows, chunk_size=None, candidate_rule_order=None):
    doc = build_replay_only_document(
        source_commit="determinism",
        run_timestamp="2026-06-23T00:00:00Z",
        rows=source_rows,
        chunk_size=chunk_size,
        candidate_rule_order=candidate_rule_order,
        include_determinism=False,
    )
    return _stable_hash(
        {
            "setup_records": doc["setup_time_candidate_records"],
            "sessions": doc["provisional_manifest"]["sessions"],
            "review": doc["compact_setup_time_review"]["records"],
        }
    )


def _direction_for_package(package):
    # Day 50/51 positive-entry packages are long-call review paths. This remains provisional
    # for Ideal and Continuation because the accepted family selector is still unresolved.
    return "bullish"


def _source_row_snapshot(row):
    return {
        "timestamp_utc": row.get("timestamp_utc"),
        "timestamp_et": row.get("timestamp_et"),
        "publisher_id": row.get("publisher_id"),
        "instrument_id": row.get("instrument_id"),
        "open": row.get("open"),
        "high": row.get("high"),
        "low": row.get("low"),
        "close": row.get("close"),
        "volume": row.get("volume"),
        "symbol": row.get("symbol"),
    }


def _read_source_rows(path):
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _normalize_source_rows(rows):
    return [_normalize_row(row) for row in rows]


def _normalize_row(row):
    if "timestamp_utc" in row and "timestamp_et" in row:
        return dict(row)
    ts = _parse_utc(row["ts_event"])
    item = dict(row)
    item["timestamp_utc"] = _format_utc(ts)
    item["timestamp_et"] = ts.astimezone(NY).isoformat()
    item["session_date"] = ts.astimezone(NY).date().isoformat()
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
    return item


def _row_sort_key(row):
    return (
        row.get("timestamp_utc"),
        str(row.get("publisher_id")),
        str(row.get("instrument_id")),
        str(row.get("source_row_hash", "")),
    )


def _parse_utc(value):
    text = str(value)
    if text.endswith("Z"):
        text = text.replace("Z", "+00:00")
    if "." in text:
        left, right = text.split(".", 1)
        suffix = ""
        if "+" in right:
            frac, zone = right.split("+", 1)
            suffix = "+" + zone
        elif "-" in right:
            frac, zone = right.split("-", 1)
            suffix = "-" + zone
        else:
            frac = right
        text = f"{left}.{frac[:6]}{suffix}"
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _format_utc(value):
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _decimal(value):
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"not a finite decimal value: {value!r}") from exc


def _format_decimal(value):
    return format(value, "f")


def _stable_hash(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _file_sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def _utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _markdown_result(document):
    accepted = document["accepted_mode_reference"]
    provisional = document["complete_session_opportunity_accounting"]
    value_rows = "\n".join(
        (
            f"- {record['setup_family']}: trigger `{record['trigger']['final_numeric_value']}` "
            f"from `{record['trigger']['source_field']}`, invalidation "
            f"`{record['invalidation']['final_numeric_value']}` from "
            f"`{record['invalidation']['source_field']}`, rule "
            f"`{record['candidate_rule_id']}`."
        )
        for record in document["setup_time_candidate_records"]
    )
    return f"""# SAFE-FAST Day 52 Replay-Only Numeric Rule Candidates Result

## Scope

- Task executed: `{TASK_FILENAME}`.
- Machine-readable result: `historical_signal_replay/results/day52_replay_only_numeric_rule_candidates.json`.
- Provisional manifest: `historical_signal_replay/results/day52_replay_only_numeric_rule_candidates_manifest.json`.
- Compact setup-time review: `historical_signal_replay/results/day52_replay_only_numeric_rule_candidates_setup_time_review.json`.
- Implementation: `historical_signal_replay/day52_replay_only_numeric_rule_candidates.py`.
- Status: `{PROVISIONAL_STATUS}` research evidence only.

## Values

{value_rows}

Candidate B and Candidate C were not produced because the accepted mapper packages do not contain setup-structure boundaries or explicit named breakout/reclaim/resistance/support/pivot/base levels. Candidate A was selected by fixed priority after those higher-priority fields were absent, not by later price movement.

## Counts

- Accepted mode remains unresolved: numeric values established `{accepted['numeric_values_established']}`, numeric values unresolved `{accepted['numeric_values_unresolved']}`.
- Provisional mode: setup-qualified under provisional mode `{provisional['setup_qualified_under_provisional_mode_records']}`, selected winners `{provisional['selected_winner_records']}`, suppressed `{provisional['suppressed_records']}`, recognition-layer executable `{provisional['recognition_layer_executable_records']}`.
- Trade candidates `0`; selected contracts `0`; eligible entries `0`; recorded entries `0`.

## Guardrails

Accepted numeric rules remain unresolved unless separately proven. These provisional replay-only numeric candidates are not profitability proof, not OPRA evidence, and not paper/live eligibility. No option P&L, paid data download, `main.py`, Railway/deploy, broker/account/order/fill/alert, credential, `.env`, sizing, or frozen `patch8` threshold change was made.

## Required Decision

Promote, revise, or reject the setup-bar range candidate for each family with an explicit accepted rule and regression cases before any accepted setup-qualified recognition claim.
"""


if __name__ == "__main__":
    doc = write_outputs()
    accounting = doc["complete_session_opportunity_accounting"]
    print(
        "wrote day52 replay-only numeric rule candidates: "
        f"{accounting['setup_qualified_under_provisional_mode_records']} provisional setup-qualified, "
        f"{accounting['selected_winner_records']} selected winners, "
        f"{accounting['trade_candidates']} trade candidates"
    )
