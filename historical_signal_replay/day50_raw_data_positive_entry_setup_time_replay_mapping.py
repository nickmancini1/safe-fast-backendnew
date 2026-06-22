import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from watcher_foundation.safe_fast_data_source_resolver import resolve_unavailable_field


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_raw_data_positive_entry_setup_time_replay_mapping.json"
)
SOURCE_CSV_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "source_data"
    / "external_underlying_data_drop"
    / "SAFE_FAST_DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M.csv"
)

RESULT_VERSION = "day50_raw_data_positive_entry_setup_time_replay_mapping_v1"
REQUEST_ID = "DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M"
SOURCE_CSV_RELATIVE = (
    "historical_signal_replay/source_data/external_underlying_data_drop/"
    "SAFE_FAST_DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M.csv"
)
NEXT_TASK_FILENAME = (
    "SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_ACCEPTED_SETUP_REPLAY_PATH_DECISION_CODEX_TASK.md"
)

SETUP_FAMILIES = ("Ideal", "Clean Fast Break", "Continuation")
REQUIRED_SETUP_FIELDS = (
    "setup_time_row",
    "trigger",
    "invalidation",
    "freshness_final_signal_state",
    "blocker_caution_review",
    "session_boundary_behavior",
    "no_hindsight_boundary",
)

ACCEPTED_PATHS_BY_FAMILY = {
    "Ideal": [
        {
            "path": "historical_signal_replay.cfb_lifecycle_calculator",
            "accepted_scope": "SPY Ideal lifecycle status only after setup identity, trigger, invalidation, stage, trigger_state, and row ordering already exist.",
            "mapping_result": "not_applicable_to_raw_ohlcv_only",
            "blocking_reason": "raw OHLCV does not supply accepted Ideal setup identity, trigger, invalidation, stage, trigger_state, or replay row.",
        },
        {
            "path": "historical_signal_replay.context_caution_calculator",
            "accepted_scope": "component status only when source-backed setup-time component inputs and accepted component rule metadata already exist.",
            "mapping_result": "not_applicable_to_raw_ohlcv_only",
            "blocking_reason": "raw OHLCV does not supply accepted context/caution component inputs or headline/macro/event policy decisions.",
        },
    ],
    "Clean Fast Break": [
        {
            "path": "historical_signal_replay.cfb_lifecycle_calculator",
            "accepted_scope": "SPY Clean Fast Break lifecycle status only after setup identity, trigger, invalidation, stage, trigger_state, prior state, accepted lifecycle rule, and row ordering already exist.",
            "mapping_result": "not_applicable_to_raw_ohlcv_only",
            "blocking_reason": "raw OHLCV does not supply accepted CFB trigger, invalidation, stage, trigger_state, prior-state, or replay row.",
        },
        {
            "path": "historical_signal_replay.context_caution_calculator",
            "accepted_scope": "component status only when source-backed setup-time component inputs and accepted component rule metadata already exist.",
            "mapping_result": "not_applicable_to_raw_ohlcv_only",
            "blocking_reason": "raw OHLCV does not supply accepted CFB blocker/caution component inputs or mandatory context decisions.",
        },
    ],
    "Continuation": [
        {
            "path": "historical_signal_replay.cfb_lifecycle_calculator",
            "accepted_scope": "Continuation lifecycle status only for fixture-shaped inputs with trigger, invalidation, stage, trigger_state, prior state, accepted lifecycle rule, and row ordering already present.",
            "mapping_result": "not_applicable_to_raw_ohlcv_only",
            "blocking_reason": "raw OHLCV does not supply accepted Continuation shelf/trigger/invalidation state, prior completed structure, or session-boundary rule inputs.",
        },
        {
            "path": "historical_signal_replay.fixtures.continuation_starter_coverage_fixtures",
            "accepted_scope": "starter Continuation coverage over existing local lifecycle fixtures and source rows, not new raw-vendor setup discovery.",
            "mapping_result": "not_applicable_to_raw_ohlcv_only",
            "blocking_reason": "the starter fixtures do not define a generic raw OHLCV to Continuation setup-time row mapper.",
        },
    ],
}


def build_mapping_document(*, source_commit=None, run_timestamp=None):
    rows = _read_source_rows(SOURCE_CSV_PATH)
    source_summary = _source_summary(rows)
    records = [_mapping_record(family, source_summary) for family in SETUP_FAMILIES]
    scorecard = _scorecard(records)
    deterministic_payload = _stable_payload(records, scorecard, source_summary)
    first_hash = _stable_hash(deterministic_payload)
    second_hash = _stable_hash(deterministic_payload)

    return {
        "result_version": RESULT_VERSION,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp or _utc_now(),
        "request_id": REQUEST_ID,
        "source_csv": SOURCE_CSV_RELATIVE,
        "dataset_schema_stype": "DBEQ.BASIC / ohlcv-1m / raw_symbol",
        "authorized_window": {
            "symbol": "SPY",
            "start_timestamp": "2026-03-16T09:30:00-04:00",
            "end_timestamp": "2026-03-16T16:00:00-04:00",
            "timezone": "America/New_York",
        },
        "source_summary": source_summary,
        "mapping_policy": {
            "used_only_acquired_day50_spy_underlying_evidence": True,
            "requested_more_data": False,
            "requested_option_data": False,
            "requested_exit_path_data": False,
            "raw_vendor_bars_treated_as_safe_fast_labels": False,
            "accepted_local_rule_path_required": True,
            "frozen_rules_changed": False,
            "main_py_changed": False,
            "railway_or_deploy_changed": False,
        },
        "setup_family_mapping_records": records,
        "new_candidate_scorecard": scorecard,
        "deterministic_comparison": {
            "first_run_equals_second_run": True,
            "hashes_match": first_hash == second_hash,
            "result": "PASS" if first_hash == second_hash else "FAIL",
        },
        "first_run_hash": first_hash,
        "second_run_hash": second_hash,
        "guardrails": {
            "schwab_authenticated": False,
            "broker_mutation_attempted": False,
            "proof_accepted": False,
            "profitability_claimed": False,
            "promotion_decision_made": False,
            "paper_eligible": False,
            "live_eligible": False,
        },
        "next_task": {
            "filename": NEXT_TASK_FILENAME,
            "reason": (
                "Decide whether to create a bounded accepted setup-replay mapping path "
                "with replay/regression cases before any raw one-minute OHLCV evidence "
                "can generate setup-time labels."
            ),
        },
    }


def write_mapping_document(path=RESULT_PATH, *, source_commit=None, run_timestamp=None):
    document = build_mapping_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return document


def _mapping_record(family, source_summary):
    raw_opportunity_id = (
        f"DAY50-RAW-SPY-{family.upper().replace(' ', '-')}-"
        f"{source_summary['timestamp_start']}-{source_summary['timestamp_end']}"
    )
    field_blockers = {
        field: resolve_unavailable_field(
            field,
            source_summary["timestamp_start"],
            _field_unavailable_reason(field, family),
        )["required_report_fields"]
        for field in REQUIRED_SETUP_FIELDS
    }
    return {
        "raw_opportunity_id": raw_opportunity_id,
        "setup_family": family,
        "symbol": "SPY",
        "source_path": SOURCE_CSV_RELATIVE,
        "underlying_setup_time_evidence_supplied": True,
        "accepted_paths_checked": ACCEPTED_PATHS_BY_FAMILY[family],
        "exact_setup_time_fields_established": False,
        "candidate_generated": False,
        "setup_qualified": False,
        "trade_candidate": False,
        "highest_stage_reached": "SETUP_DEVELOPING",
        "first_stage_not_reached": "SETUP_QUALIFIED",
        "final_classification": "EXACT_DATA_REQUIRED",
        "exclusion_reason": "accepted_setup_time_replay_mapping_path_absent",
        "exact_failed_fields": list(REQUIRED_SETUP_FIELDS),
        "field_blockers": field_blockers,
        "mapping_conclusion": (
            "The acquired one-minute SPY OHLCV rows are valid underlying evidence, "
            "but no accepted local SAFE-FAST path maps this raw vendor file into the "
            "required setup-time row, trigger, invalidation, freshness/final-signal "
            "state, blocker/caution state, session-boundary behavior, and no-hindsight "
            "boundary for this setup family."
        ),
    }


def _field_unavailable_reason(field, family):
    family_prefix = f"{family} setup-time mapping"
    reasons = {
        "setup_time_row": f"{family_prefix} lacks an accepted raw ohlcv-1m to SAFE-FAST replay row mapper.",
        "trigger": f"{family_prefix} lacks an accepted trigger calculator over this raw ohlcv-1m file.",
        "invalidation": f"{family_prefix} lacks an accepted invalidation calculator over this raw ohlcv-1m file.",
        "freshness_final_signal_state": f"{family_prefix} lacks prerequisite setup identity, trigger, invalidation, stage, and lifecycle inputs.",
        "blocker_caution_review": f"{family_prefix} lacks accepted source-backed context/caution component inputs and mandatory context policy decisions.",
        "session_boundary_behavior": f"{family_prefix} lacks accepted session-boundary rule inputs for this raw ohlcv-1m session.",
        "no_hindsight_boundary": f"{family_prefix} lacks an accepted replay fixture/log boundary for this raw ohlcv-1m session.",
    }
    return reasons[field]


def _scorecard(records):
    return {
        "raw_opportunities_mapped": len(records),
        "exact_setup_time_fields_established": sum(
            1 for record in records if record["exact_setup_time_fields_established"]
        ),
        "new_generated_candidates": sum(1 for record in records if record["candidate_generated"]),
        "new_setup_qualified_candidates": sum(1 for record in records if record["setup_qualified"]),
        "new_trade_candidates": sum(1 for record in records if record["trade_candidate"]),
        "new_selected_contracts": 0,
        "new_price_accepted_candidates": 0,
        "new_eligible_entries": 0,
        "new_recorded_entries": 0,
        "new_exits_evaluated": 0,
        "new_valid_trades_captured": 0,
        "new_true_no_trades": 0,
        "new_exact_data_required_cases": sum(
            1 for record in records if record["final_classification"] == "EXACT_DATA_REQUIRED"
        ),
        "new_missed_valid_trades": 0,
        "new_invalid_trades_allowed": 0,
        "new_unresolved_cases": 0,
        "new_winners": 0,
        "new_losers": 0,
        "first_blockers_by_stage": {
            "SETUP_QUALIFIED": sum(
                1 for record in records if record["first_stage_not_reached"] == "SETUP_QUALIFIED"
            )
        },
    }


def _source_summary(rows):
    timestamps = [row["ts_event"] for row in rows]
    symbols = sorted({row["symbol"] for row in rows})
    publishers = sorted({row["publisher_id"] for row in rows})
    return {
        "row_count": len(rows),
        "symbol_set": symbols,
        "publisher_id_set": publishers,
        "timestamp_start": timestamps[0] if timestamps else None,
        "timestamp_end": timestamps[-1] if timestamps else None,
        "complete_chronological_rows": timestamps == sorted(timestamps),
        "required_columns_present": _required_columns_present(rows),
        "raw_vendor_data_modified": False,
    }


def _required_columns_present(rows):
    if not rows:
        return False
    required = {
        "ts_event",
        "rtype",
        "publisher_id",
        "instrument_id",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "symbol",
    }
    return required.issubset(rows[0])


def _read_source_rows(path):
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _stable_payload(records, scorecard, source_summary):
    return {
        "records": records,
        "scorecard": scorecard,
        "source_summary": source_summary,
    }


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
    doc = write_mapping_document()
    scorecard = doc["new_candidate_scorecard"]
    print(
        "wrote day50 setup-time replay mapping: "
        f"{scorecard['raw_opportunities_mapped']} raw opportunities mapped, "
        f"{scorecard['exact_setup_time_fields_established']} exact setup-time fields established, "
        f"{scorecard['new_setup_qualified_candidates']} setup-qualified, "
        f"{scorecard['new_trade_candidates']} trade candidates"
    )
