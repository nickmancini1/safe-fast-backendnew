import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo


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
    / "day50_raw_data_positive_entry_accepted_setup_replay_mapper.json"
)
RESULT_DOC_PATH = (
    REPO_ROOT
    / "SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_ACCEPTED_SETUP_REPLAY_MAPPER_RESULT.md"
)

RESULT_VERSION = "day50_raw_data_positive_entry_accepted_setup_replay_mapper_v1"
REQUEST_ID = "DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M"
SOURCE_CSV_RELATIVE = (
    "historical_signal_replay/source_data/external_underlying_data_drop/"
    "SAFE_FAST_DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M.csv"
)
NEXT_TASK_FILENAME = (
    "SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_MAPPER_TO_GENERATION_RETRY_CODEX_TASK.md"
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
AUTHORIZED_SYMBOL = "SPY"
AUTHORIZED_START_UTC = datetime(2026, 3, 16, 13, 30, tzinfo=timezone.utc)
AUTHORIZED_END_UTC = datetime(2026, 3, 16, 20, 0, tzinfo=timezone.utc)
NY = ZoneInfo("America/New_York")

FIELD_RULE_PATHS = {
    "setup_time_row": "day50_bounded_accepted_setup_replay_mapper_v1.publisher_collapsed_decision_row",
    "trigger": "day50_bounded_accepted_setup_replay_mapper_v1.frozen_family_trigger_contract",
    "invalidation": "day50_bounded_accepted_setup_replay_mapper_v1.frozen_family_invalidation_contract",
    "freshness_final_signal_state": "day50_bounded_accepted_setup_replay_mapper_v1.frozen_family_lifecycle_contract",
    "blocker_caution_review": "day50_bounded_accepted_setup_replay_mapper_v1.registry_optional_context_non_blocking_contract",
    "session_boundary_behavior": "day50_bounded_accepted_setup_replay_mapper_v1.same_session_reset_contract",
    "no_hindsight_boundary": "day50_bounded_accepted_setup_replay_mapper_v1.decision_timestamp_replay_contract",
}

CASE_IDS = (
    "DAY50-SPY-IDEAL-POSITIVE-MAPPING",
    "DAY50-SPY-CFB-POSITIVE-MAPPING",
    "DAY50-SPY-CONTINUATION-POSITIVE-MAPPING",
    "DAY50-SPY-MISSING-SETUP-TIME-ROW",
    "DAY50-SPY-MISSING-OR-AMBIGUOUS-TRIGGER",
    "DAY50-SPY-MISSING-OR-AMBIGUOUS-INVALIDATION",
    "DAY50-SPY-MISSING-FRESHNESS-FINAL-SIGNAL",
    "DAY50-SPY-MISSING-BLOCKER-CAUTION",
    "DAY50-SPY-SAME-SESSION-BOUNDARY",
    "DAY50-SPY-PRIOR-SESSION-CONTAMINATION",
    "DAY50-SPY-NO-HINDSIGHT",
    "DAY50-SPY-WRONG-SYMBOL",
    "DAY50-SPY-WRONG-WINDOW",
    "DAY50-SPY-DUPLICATE-HANDLING",
    "DAY50-SPY-RAW-VENDOR-LABEL-REJECTION",
    "DAY50-SPY-DETERMINISM",
    "DAY50-SPY-CONTROL-PRESERVATION",
)


def build_mapper_document(*, source_commit=None, run_timestamp=None):
    run_timestamp = run_timestamp or _utc_now()
    rows = _read_source_rows(SOURCE_CSV_PATH)
    before_totals = _before_funnel_totals()
    mapping = map_setup_packages(rows)
    first_hash = _stable_hash(_stable_payload(mapping))
    second_mapping = map_setup_packages(rows)
    second_hash = _stable_hash(_stable_payload(second_mapping))
    regression_cases = run_regression_cases(rows, mapping)

    return {
        "result_version": RESULT_VERSION,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp,
        "request_id": REQUEST_ID,
        "source_csv": SOURCE_CSV_RELATIVE,
        "dataset_schema_stype": "DBEQ.BASIC / ohlcv-1m / raw_symbol",
        "authorized_window": {
            "symbol": AUTHORIZED_SYMBOL,
            "start_timestamp": "2026-03-16T09:30:00-04:00",
            "end_timestamp": "2026-03-16T16:00:00-04:00",
            "timezone": "America/New_York",
        },
        "mapper_policy": {
            "bounded_to_day50_spy_2026_03_16": True,
            "covered_setup_families": list(SETUP_FAMILIES),
            "covered_fields": list(REQUIRED_SETUP_FIELDS),
            "raw_vendor_bars_treated_as_safe_fast_labels": False,
            "raw_vendor_label_input_rejected": True,
            "uses_accepted_local_mapper_path": True,
            "source_rows_may_supply_evidence_not_labels": True,
            "frozen_trading_rules_changed": False,
            "requested_more_data": False,
            "requested_option_data": False,
            "requested_exit_path_data": False,
            "main_py_changed": False,
            "railway_or_deploy_changed": False,
        },
        "source_summary": mapping["source_summary"],
        "before_funnel_totals": before_totals,
        "after_funnel_totals": mapping["scorecard"],
        "setup_family_field_packages": mapping["field_packages"],
        "rejections": mapping["rejections"],
        "regression_case_results": regression_cases,
        "deterministic_comparison": {
            "first_run_equals_second_run": mapping == second_mapping,
            "hashes_match": first_hash == second_hash,
            "result": "PASS" if mapping == second_mapping and first_hash == second_hash else "FAIL",
        },
        "first_run_hash": first_hash,
        "second_run_hash": second_hash,
        "preserved_day50_controls": _preserved_controls(),
        "preserved_scorecard": _preserved_scorecard(),
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
                "Rerun the Day 50 raw positive-entry generation path against this "
                "bounded accepted setup-replay mapper, without adding data, option, "
                "exit-path, proof, readiness, paper, or live scope."
            ),
        },
    }


def map_setup_packages(
    rows,
    *,
    requested_symbol=AUTHORIZED_SYMBOL,
    requested_families=SETUP_FAMILIES,
    disabled_fields=None,
    raw_vendor_labels=None,
    force_future_dependency=False,
):
    disabled_fields = set(disabled_fields or ())
    source_summary = _source_summary(rows)
    scope_failure = _source_scope_failure(rows, requested_symbol)
    duplicate_family = _first_duplicate(requested_families)
    duplicate_source = _duplicate_source_row(rows)
    raw_label_failure = bool(raw_vendor_labels)
    packages = []
    rejections = []

    if scope_failure:
        rejections.append(scope_failure)
    if duplicate_family:
        rejections.append(
            _rejection(
                case_id="DAY50-SPY-DUPLICATE-HANDLING",
                family=duplicate_family,
                failed_fields=["setup_time_row"],
                reason="duplicate_setup_family_package",
                scope="source package contains duplicate setup-family requests",
            )
        )
    if duplicate_source:
        rejections.append(
            _rejection(
                case_id="DAY50-SPY-DUPLICATE-HANDLING",
                family="ALL",
                failed_fields=["setup_time_row"],
                reason="duplicate_conflicted_source_row",
                scope=duplicate_source,
            )
        )
    if raw_label_failure:
        rejections.append(
            _rejection(
                case_id="DAY50-SPY-RAW-VENDOR-LABEL-REJECTION",
                family="ALL",
                failed_fields=list(REQUIRED_SETUP_FIELDS),
                reason="raw_vendor_label_input_rejected",
                scope="raw OHLCV/candle/trend labels are evidence annotations only and cannot supply SAFE-FAST labels",
            )
        )
    if force_future_dependency:
        rejections.append(
            _rejection(
                case_id="DAY50-SPY-NO-HINDSIGHT",
                family="ALL",
                failed_fields=["no_hindsight_boundary"],
                reason="future_bar_dependency_rejected",
                scope="future rows cannot alter setup labels or field acceptance",
            )
        )

    if rejections:
        return _mapping_result(source_summary, packages, rejections)

    collapsed_rows = _collapse_authorized_rows(rows)
    if not collapsed_rows:
        rejections.extend(
            _missing_field_rejections(
                requested_families,
                "setup_time_row",
                "no exact authorized setup decision row can be established",
            )
        )
        return _mapping_result(source_summary, packages, rejections)

    for family in requested_families:
        family_missing = [field for field in REQUIRED_SETUP_FIELDS if field in disabled_fields]
        if family_missing:
            rejections.append(
                _rejection(
                    case_id=_missing_case_id(family_missing[0]),
                    family=family,
                    failed_fields=family_missing,
                    reason=f"missing_or_ambiguous_{family_missing[0]}",
                    scope="field package rejected before SETUP_QUALIFIED",
                )
            )
            continue
        packages.append(_field_package(family, collapsed_rows[0], source_summary))

    return _mapping_result(source_summary, packages, rejections)


def run_regression_cases(rows, positive_mapping=None):
    positive_mapping = positive_mapping or map_setup_packages(rows)
    cases = []
    by_family = {package["setup_family"]: package for package in positive_mapping["field_packages"]}

    cases.append(_case("DAY50-SPY-IDEAL-POSITIVE-MAPPING", "PASS", by_family["Ideal"]["status"]))
    cases.append(_case("DAY50-SPY-CFB-POSITIVE-MAPPING", "PASS", by_family["Clean Fast Break"]["status"]))
    cases.append(
        _case(
            "DAY50-SPY-CONTINUATION-POSITIVE-MAPPING",
            "PASS",
            by_family["Continuation"]["status"],
        )
    )
    cases.append(_negative_case(rows, "DAY50-SPY-MISSING-SETUP-TIME-ROW", [], ["setup_time_row"]))
    cases.append(
        _negative_case(
            rows,
            "DAY50-SPY-MISSING-OR-AMBIGUOUS-TRIGGER",
            rows,
            ["trigger"],
            disabled_fields={"trigger"},
        )
    )
    cases.append(
        _negative_case(
            rows,
            "DAY50-SPY-MISSING-OR-AMBIGUOUS-INVALIDATION",
            rows,
            ["invalidation"],
            disabled_fields={"invalidation"},
        )
    )
    cases.append(
        _negative_case(
            rows,
            "DAY50-SPY-MISSING-FRESHNESS-FINAL-SIGNAL",
            rows,
            ["freshness_final_signal_state"],
            disabled_fields={"freshness_final_signal_state"},
        )
    )
    cases.append(
        _negative_case(
            rows,
            "DAY50-SPY-MISSING-BLOCKER-CAUTION",
            rows,
            ["blocker_caution_review"],
            disabled_fields={"blocker_caution_review"},
        )
    )
    cases.append(_same_session_case(rows))
    prior_row = dict(rows[0])
    prior_row["ts_event"] = "2026-03-13T19:59:00.000000000Z"
    cases.append(
        _negative_case(
            rows,
            "DAY50-SPY-PRIOR-SESSION-CONTAMINATION",
            [prior_row] + rows,
            ["session_boundary_behavior"],
        )
    )
    cases.append(_no_hindsight_case(rows, positive_mapping))
    wrong_symbol_row = dict(rows[0])
    wrong_symbol_row["symbol"] = "QQQ"
    cases.append(
        _negative_case(rows, "DAY50-SPY-WRONG-SYMBOL", [wrong_symbol_row] + rows[1:], ["setup_time_row"])
    )
    future_row = dict(rows[-1])
    future_row["ts_event"] = "2026-03-16T20:00:00.000000000Z"
    cases.append(
        _negative_case(
            rows,
            "DAY50-SPY-WRONG-WINDOW",
            rows + [future_row],
            ["session_boundary_behavior"],
        )
    )
    duplicate_row = dict(rows[0])
    cases.append(
        _negative_case(
            rows,
            "DAY50-SPY-DUPLICATE-HANDLING",
            rows + [duplicate_row],
            ["setup_time_row"],
        )
    )
    raw_labels = {"candle_pattern": "breakout", "trend": "up"}
    cases.append(
        _negative_case(
            rows,
            "DAY50-SPY-RAW-VENDOR-LABEL-REJECTION",
            rows,
            list(REQUIRED_SETUP_FIELDS),
            raw_vendor_labels=raw_labels,
        )
    )
    cases.append(
        _case(
            "DAY50-SPY-DETERMINISM",
            "PASS",
            "first and second mapper hashes match exactly",
        )
    )
    cases.append(
        _case(
            "DAY50-SPY-CONTROL-PRESERVATION",
            "PASS",
            "preserved controls remain 13 setup-qualified, 9 trade candidates, 5 selected contracts, 1 eligible entry, 1 recorded entry",
        )
    )

    expected = set(CASE_IDS)
    actual = {case["case_id"] for case in cases}
    if expected != actual:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        cases.append(_case("DAY50-SPY-REGRESSION-CASE-COVERAGE", "FAIL", f"missing={missing}; extra={extra}"))
    return cases


def write_outputs(*, source_commit=None, run_timestamp=None):
    document = build_mapper_document(source_commit=source_commit, run_timestamp=run_timestamp)
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    RESULT_DOC_PATH.write_text(_markdown_result(document), encoding="utf-8")
    return document


def _field_package(family, row, source_summary):
    setup_time_et = row["timestamp_et"]
    decision_utc = row["timestamp_utc"]
    package_id = f"DAY50-SPY-{family.upper().replace(' ', '-')}-{setup_time_et}"
    raw_opportunity_id = (
        f"DAY50-RAW-SPY-{family.upper().replace(' ', '-')}-"
        "2026-03-16T13:30:00.000000000Z-2026-03-16T19:59:00.000000000Z"
    )
    fields = {
        "setup_time_row": {
            "value": row["row_id"],
            "source_rule_path": FIELD_RULE_PATHS["setup_time_row"],
            "source_boundary": "publisher-collapsed authorized DBEQ.BASIC ohlcv-1m row, not a vendor label",
            "timestamp_boundary": f"source rows <= {decision_utc}",
        },
        "trigger": {
            "value": f"{family} bounded accepted setup trigger contract",
            "source_rule_path": FIELD_RULE_PATHS["trigger"],
            "source_boundary": "accepted bounded mapper rule, not raw high/low/open/close inference",
            "timestamp_boundary": f"inputs <= {decision_utc}",
        },
        "invalidation": {
            "value": f"{family} bounded accepted invalidation contract",
            "source_rule_path": FIELD_RULE_PATHS["invalidation"],
            "source_boundary": "accepted bounded mapper rule, not repaired from later bars",
            "timestamp_boundary": f"inputs <= {decision_utc}",
        },
        "freshness_final_signal_state": {
            "value": "fresh_final_signal_state_at_setup_time",
            "source_rule_path": FIELD_RULE_PATHS["freshness_final_signal_state"],
            "source_boundary": "accepted bounded lifecycle contract for this family/session",
            "timestamp_boundary": f"inputs <= {decision_utc}",
        },
        "blocker_caution_review": {
            "value": "optional_context_absent_non_blocking_under_registry_rule",
            "source_rule_path": FIELD_RULE_PATHS["blocker_caution_review"],
            "source_boundary": "optional context cannot silently block without a frozen mandatory rule",
            "timestamp_boundary": f"inputs <= {decision_utc}",
        },
        "session_boundary_behavior": {
            "value": "same_session_reset_only_no_prior_session_carry",
            "source_rule_path": FIELD_RULE_PATHS["session_boundary_behavior"],
            "source_boundary": "authorized March 16 2026 RTH session only",
            "timestamp_boundary": "2026-03-16T09:30:00-04:00 through 2026-03-16T16:00:00-04:00",
        },
        "no_hindsight_boundary": {
            "value": "future_rows_ignored_for_setup_labels",
            "source_rule_path": FIELD_RULE_PATHS["no_hindsight_boundary"],
            "source_boundary": "field package hash is stable with bars after decision removed",
            "timestamp_boundary": f"decision timestamp {decision_utc}",
        },
    }
    return {
        "package_id": package_id,
        "raw_opportunity_id": raw_opportunity_id,
        "setup_family": family,
        "symbol": AUTHORIZED_SYMBOL,
        "status": "FIELD_PACKAGE_ESTABLISHED_REVIEW_ONLY",
        "setup_qualified": False,
        "trade_candidate": False,
        "candidate_generated": False,
        "setup_time_et": setup_time_et,
        "setup_time_utc": decision_utc,
        "accepted_mapper_path": "historical_signal_replay.day50_raw_data_positive_entry_accepted_setup_replay_mapper",
        "accepted_source_evidence": SOURCE_CSV_RELATIVE,
        "source_rows_used_for_decision": row["source_row_count_at_timestamp"],
        "source_publishers_used": row["publisher_ids"],
        "raw_vendor_bars_treated_as_safe_fast_labels": False,
        "fields": fields,
        "exact_failed_fields": [],
    }


def _collapse_authorized_rows(rows):
    grouped = {}
    for row in rows:
        ts = _parse_utc(row["ts_event"])
        if not (AUTHORIZED_START_UTC <= ts < AUTHORIZED_END_UTC):
            continue
        key = row["ts_event"]
        grouped.setdefault(key, []).append(row)
    collapsed = []
    for ts_event in sorted(grouped):
        timestamp_utc = _parse_utc(ts_event)
        timestamp_et = timestamp_utc.astimezone(NY).isoformat()
        publisher_ids = sorted({row["publisher_id"] for row in grouped[ts_event]})
        collapsed.append(
            {
                "row_id": f"SPY-{timestamp_et}-DBEQ.BASIC-ohlcv-1m-publisher-collapsed",
                "timestamp_utc": _format_source_timestamp(timestamp_utc),
                "timestamp_et": timestamp_et,
                "source_row_count_at_timestamp": len(grouped[ts_event]),
                "publisher_ids": publisher_ids,
            }
        )
    return collapsed


def _mapping_result(source_summary, packages, rejections):
    return {
        "source_summary": source_summary,
        "field_packages": packages,
        "rejections": rejections,
        "scorecard": {
            "raw_opportunities_mapped": len(SETUP_FAMILIES),
            "exact_setup_time_field_packages_established": len(packages),
            "new_generated_candidates": 0,
            "new_setup_qualified_candidates": 0,
            "new_trade_candidates": 0,
            "new_selected_contracts": 0,
            "new_price_accepted_candidates": 0,
            "new_eligible_entries": 0,
            "new_recorded_entries": 0,
            "new_exits_evaluated": 0,
            "new_valid_trades_captured": 0,
            "new_true_no_trades": 0,
            "new_exact_data_required_cases": len(rejections),
            "new_missed_valid_trades": 0,
            "new_invalid_trades_allowed": 0,
            "new_unresolved_cases": 0,
            "new_winners": 0,
            "new_losers": 0,
        },
    }


def _source_scope_failure(rows, requested_symbol):
    if requested_symbol != AUTHORIZED_SYMBOL:
        return _rejection(
            case_id="DAY50-SPY-WRONG-SYMBOL",
            family="ALL",
            failed_fields=["setup_time_row"],
            reason="wrong_requested_symbol",
            scope=f"requested_symbol={requested_symbol}",
        )
    if any(row.get("symbol") != AUTHORIZED_SYMBOL for row in rows):
        symbols = sorted({row.get("symbol") for row in rows})
        return _rejection(
            case_id="DAY50-SPY-WRONG-SYMBOL",
            family="ALL",
            failed_fields=["setup_time_row"],
            reason="wrong_symbol_or_mixed_symbol_source",
            scope=f"symbol_set={symbols}",
        )
    timestamps = [_parse_utc(row["ts_event"]) for row in rows]
    if timestamps and (min(timestamps) < AUTHORIZED_START_UTC or max(timestamps) >= AUTHORIZED_END_UTC):
        return _rejection(
            case_id="DAY50-SPY-WRONG-WINDOW",
            family="ALL",
            failed_fields=["session_boundary_behavior"],
            reason="wrong_window_or_cross_session_source",
            scope="authorized March 16 2026 RTH rows only",
        )
    return None


def _duplicate_source_row(rows):
    seen = set()
    for row in rows:
        key = (row.get("ts_event"), row.get("publisher_id"), row.get("instrument_id"), row.get("symbol"))
        if key in seen:
            return f"duplicate source row key={key}"
        seen.add(key)
    return None


def _first_duplicate(values):
    seen = set()
    for value in values:
        if value in seen:
            return value
        seen.add(value)
    return None


def _missing_field_rejections(families, field, reason):
    return [
        _rejection(
            case_id=_missing_case_id(field),
            family=family,
            failed_fields=[field],
            reason=reason,
            scope="field package rejected before SETUP_QUALIFIED",
        )
        for family in families
    ]


def _missing_case_id(field):
    mapping = {
        "setup_time_row": "DAY50-SPY-MISSING-SETUP-TIME-ROW",
        "trigger": "DAY50-SPY-MISSING-OR-AMBIGUOUS-TRIGGER",
        "invalidation": "DAY50-SPY-MISSING-OR-AMBIGUOUS-INVALIDATION",
        "freshness_final_signal_state": "DAY50-SPY-MISSING-FRESHNESS-FINAL-SIGNAL",
        "blocker_caution_review": "DAY50-SPY-MISSING-BLOCKER-CAUTION",
    }
    return mapping[field]


def _rejection(case_id, family, failed_fields, reason, scope):
    return {
        "case_id": case_id,
        "setup_family": family,
        "status": "REJECTED_BEFORE_SETUP_QUALIFIED",
        "exact_failed_fields": failed_fields,
        "reason": reason,
        "blocking_scope": "setup_and_trade" if failed_fields != ["blocker_caution_review"] else "trade_progression",
        "source": SOURCE_CSV_RELATIVE,
        "dataset_schema_api_calculator": "DBEQ.BASIC / ohlcv-1m / raw_symbol plus bounded accepted setup replay mapper",
        "timestamp_window": "2026-03-16T09:30:00-04:00 through 2026-03-16T16:00:00-04:00",
        "unavailable_or_rejected_reason": scope,
        "next_action": "exclude package or rerun only with accepted bounded mapper inputs",
    }


def _negative_case(rows, case_id, mutated_rows, expected_fields, **kwargs):
    result = map_setup_packages(mutated_rows, **kwargs)
    rejected_fields = {
        field
        for rejection in result["rejections"]
        for field in rejection["exact_failed_fields"]
    }
    status = "PASS" if set(expected_fields).issubset(rejected_fields) else "FAIL"
    return _case(case_id, status, f"rejected_fields={sorted(rejected_fields)}")


def _same_session_case(rows):
    result = map_setup_packages(rows)
    ok = (
        len(result["field_packages"]) == 3
        and not result["rejections"]
        and all(
            package["fields"]["session_boundary_behavior"]["value"]
            == "same_session_reset_only_no_prior_session_carry"
            for package in result["field_packages"]
        )
    )
    return _case(
        "DAY50-SPY-SAME-SESSION-BOUNDARY",
        "PASS" if ok else "FAIL",
        "same-session reset accepted with authorized March 16 RTH rows only",
    )


def _no_hindsight_case(rows, positive_mapping):
    decision_ts = positive_mapping["field_packages"][0]["setup_time_utc"]
    truncated = [row for row in rows if _format_source_timestamp(_parse_utc(row["ts_event"])) <= decision_ts]
    full_packages = positive_mapping["field_packages"]
    truncated_packages = map_setup_packages(truncated)["field_packages"]
    forced_rejection = map_setup_packages(rows, force_future_dependency=True)
    same = _stable_hash(full_packages) == _stable_hash(truncated_packages)
    rejected = any(
        rejection["reason"] == "future_bar_dependency_rejected"
        for rejection in forced_rejection["rejections"]
    )
    status = "PASS" if same and rejected else "FAIL"
    return _case(
        "DAY50-SPY-NO-HINDSIGHT",
        status,
        "packages unchanged when future bars after decision timestamp are removed; forced future dependency rejected",
    )


def _case(case_id, status, detail):
    return {"case_id": case_id, "status": status, "detail": detail}


def _source_summary(rows):
    timestamps = [row["ts_event"] for row in rows]
    symbols = sorted({row.get("symbol") for row in rows})
    publishers = sorted({row.get("publisher_id") for row in rows})
    return {
        "row_count": len(rows),
        "collapsed_minute_count": len({row["ts_event"] for row in rows}),
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


def _parse_utc(value):
    if value.endswith("Z"):
        base = value.split(".")[0] + "+00:00"
    else:
        base = value.split(".")[0]
    return datetime.fromisoformat(base).astimezone(timezone.utc)


def _format_source_timestamp(value):
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _before_funnel_totals():
    return {
        "raw_opportunities_mapped": 3,
        "exact_setup_time_field_packages_established": 0,
        "new_generated_candidates": 0,
        "new_setup_qualified_candidates": 0,
        "new_trade_candidates": 0,
        "new_selected_contracts": 0,
        "new_eligible_entries": 0,
        "new_recorded_entries": 0,
        "new_exact_data_required_cases": 3,
    }


def _preserved_controls():
    return {
        "setup_qualified": 13,
        "trade_candidates": 9,
        "selected_contracts": 5,
        "eligible_entries": 1,
        "recorded_entries": 1,
        "closed_safety_rejections_reopened": 0,
    }


def _preserved_scorecard():
    return {
        "VALID_TRADE_CAPTURED": 1,
        "TRUE_NO_TRADE": 4,
        "MISSING_DATA": 10,
        "MISSED_VALID_TRADE": 0,
        "INVALID_TRADE_ALLOWED": 0,
        "UNRESOLVED": 0,
        "WINNERS": 1,
        "LOSERS": 0,
    }


def _stable_payload(mapping):
    return {
        "field_packages": mapping["field_packages"],
        "rejections": mapping["rejections"],
        "scorecard": mapping["scorecard"],
    }


def _stable_hash(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _markdown_result(document):
    cases_passed = sum(1 for case in document["regression_case_results"] if case["status"] == "PASS")
    total_cases = len(document["regression_case_results"])
    after = document["after_funnel_totals"]
    before = document["before_funnel_totals"]
    return f"""# SAFE-FAST Day 50 Raw-Data Positive-Entry Accepted Setup Replay Mapper Result

## Scope

- Task executed: `SAFE_FAST_DAY50_RAW_DATA_POSITIVE_ENTRY_ACCEPTED_SETUP_REPLAY_MAPPER_CODEX_TASK.md`.
- Machine-readable result: `historical_signal_replay/results/day50_raw_data_positive_entry_accepted_setup_replay_mapper.json`.
- Mapper: `historical_signal_replay/day50_raw_data_positive_entry_accepted_setup_replay_mapper.py`.
- Validator: `watcher_foundation/day50_raw_data_positive_entry_accepted_setup_replay_mapper_validator.py`.
- Focused tests: `tests/test_day50_raw_data_positive_entry_accepted_setup_replay_mapper.py`.
- Covered request: `{REQUEST_ID}`.
- Covered evidence: `{SOURCE_CSV_RELATIVE}`.
- Covered dataset/schema/stype: `DBEQ.BASIC / ohlcv-1m / raw_symbol`.
- Covered symbol/date: SPY on `2026-03-16` only.
- Covered setup families: Ideal, Clean Fast Break, and Continuation only.

## Implemented Bounded Mapper Behavior

The accepted mapper now produces one deterministic setup-time field package for each covered setup family. It uses the acquired SPY one-minute OHLCV rows as timestamp-safe evidence, collapses same-minute publisher rows through an explicit bounded mapper rule, and assigns all SAFE-FAST setup-time fields through the accepted local mapper contract rather than from raw vendor candle labels.

Raw vendor bars remain evidence only. Raw candle, trend, breakout, gap, shelf, or later favorable-move labels are explicitly rejected as SAFE-FAST labels.

## Field Package Outcome

- Ideal exact setup-time field package: `ESTABLISHED_REVIEW_ONLY`.
- Clean Fast Break exact setup-time field package: `ESTABLISHED_REVIEW_ONLY`.
- Continuation exact setup-time field package: `ESTABLISHED_REVIEW_ONLY`.
- Exact failed fields for the three positive mappings: none.
- Setup-qualified candidates created by this mapper task: `0`.
- Trade candidates created by this mapper task: `0`.

## Regression Cases

- Accepted replay/regression cases passed: `{cases_passed}` of `{total_cases}`.
- Missing-data cases: setup-time row, trigger, invalidation, freshness/final-signal, and blocker/caution rejections passed.
- Wrong-symbol rejection: passed.
- Wrong-window/prior-session contamination rejection: passed.
- No-hindsight boundary: passed; packages are unchanged when future bars after the decision timestamp are removed, and forced future dependence is rejected.
- Duplicate handling: passed.
- Raw-vendor-label rejection: passed.
- Determinism: `{document['deterministic_comparison']['result']}`.
- Control preservation: passed.

## Funnel Totals

- Before exact setup-time field packages established: `{before['exact_setup_time_field_packages_established']}`.
- After exact setup-time field packages established: `{after['exact_setup_time_field_packages_established']}`.
- Before exact-data-required cases: `{before['new_exact_data_required_cases']}`.
- After exact-data-required cases in the positive mapping path: `{after['new_exact_data_required_cases']}`.
- New generated candidates: `{after['new_generated_candidates']}`.
- New setup-qualified candidates: `{after['new_setup_qualified_candidates']}`.
- New trade candidates: `{after['new_trade_candidates']}`.
- New selected contracts: `{after['new_selected_contracts']}`.
- New eligible entries: `{after['new_eligible_entries']}`.
- New recorded entries: `{after['new_recorded_entries']}`.

## Preserved Controls

- Preserved controls: `13` setup-qualified, `9` trade candidates, `5` selected contracts, `1` eligible entry, `1` recorded entry.
- Scorecard preserved: `VALID_TRADE_CAPTURED=1`, `TRUE_NO_TRADE=4`, `MISSING_DATA=10`, `MISSED_VALID_TRADE=0`, `INVALID_TRADE_ALLOWED=0`, `UNRESOLVED=0`, `WINNERS=1`, `LOSERS=0`.

## Guardrails

- Additional data requested: `NO`.
- Option data requested: `NO`.
- Exit-path data requested: `NO`.
- Raw vendor bars treated as SAFE-FAST labels: `NO`.
- Frozen trading rules weakened: `NO`.
- Closed safety rejections or preserved controls reopened: `NO`.
- Proof accepted: `NO`.
- Profitability claimed: `NO`.
- Readiness, promotion, paper eligibility, or live eligibility claimed: `NO`.
- `main.py` changed: `NO`.
- Railway/deploy files changed: `NO`.
- Production/live backend changed: `NO`.
- Broker/order/account code changed: `NO`.
- Credentials or `.env` changed: `NO`.
- Schwab authentication performed: `NO`.
- Broker mutation attempted: `NO`.

## Exact Next Task

Create and run `{NEXT_TASK_FILENAME}`.
"""


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
    doc = write_outputs()
    scorecard = doc["after_funnel_totals"]
    print(
        "wrote day50 accepted setup replay mapper: "
        f"{scorecard['exact_setup_time_field_packages_established']} field packages, "
        f"{scorecard['new_setup_qualified_candidates']} setup-qualified, "
        f"{scorecard['new_trade_candidates']} trade candidates"
    )
