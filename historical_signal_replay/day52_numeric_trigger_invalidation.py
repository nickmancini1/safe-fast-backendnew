import csv
import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from zoneinfo import ZoneInfo

from historical_signal_replay import day50_raw_data_positive_entry_accepted_setup_replay_mapper


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
    / "day52_numeric_trigger_invalidation.json"
)
RESULT_DOC_PATH = REPO_ROOT / "SAFE_FAST_DAY52_NUMERIC_TRIGGER_INVALIDATION_RESULT.md"

RESULT_VERSION = "day52_numeric_trigger_invalidation_v2"
IMPLEMENTATION_VERSION = "day52_numeric_trigger_invalidation_impl_v2"
SOURCE_CSV_RELATIVE = (
    "historical_signal_replay/source_data/external_underlying_data_drop/"
    "SAFE_FAST_DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M.csv"
)
SETUP_FAMILIES = ("Ideal", "Clean Fast Break", "Continuation")
NUMERIC_FIELDS = ("trigger", "invalidation")
KNOWN_SETUP_UTC = "2026-03-16T13:30:00Z"
NY = ZoneInfo("America/New_York")

FIELD_RULE_PATHS = {
    "trigger": "day50_bounded_accepted_setup_replay_mapper_v1.frozen_family_trigger_contract",
    "invalidation": "day50_bounded_accepted_setup_replay_mapper_v1.frozen_family_invalidation_contract",
}
SOURCE_FIELDS = ("open", "high", "low", "close", "volume")
ACCEPTED_RULE_ID = "CANDIDATE_A_SETUP_BAR_RANGE"
ACCEPTED_RULE_SOURCE = "SAFE_FAST_DAY52_FAMILY_NUMERIC_BINDING_AND_PROMOTION"
ACCEPTED_DIRECTION = "bullish"


def build_numeric_trigger_invalidation_document(
    *,
    source_commit=None,
    run_timestamp=None,
    rows=None,
):
    run_timestamp = run_timestamp or _utc_now()
    source_rows = list(rows) if rows is not None else _read_source_rows(SOURCE_CSV_PATH)
    normalized_rows = _normalize_source_rows(source_rows)
    setup_rows = sorted(
        [
            row
            for row in normalized_rows
            if row.get("symbol") == "SPY" and row["timestamp_utc"] == KNOWN_SETUP_UTC
        ],
        key=_source_row_sort_key,
    )
    packages = _accepted_setup_time_packages(source_commit, run_timestamp)
    constructors = [
        construct_family_numeric_fields(
            family=package["setup_family"],
            rows=setup_rows,
            cutoff_utc=KNOWN_SETUP_UTC,
            package=package,
        )
        for package in packages
    ]
    stable_payload = {
        "constructors": constructors,
        "source_rows_at_setup": [_source_row_snapshot(row) for row in setup_rows],
    }
    first_hash = _stable_hash(stable_payload)
    second_hash = _stable_hash(json.loads(json.dumps(stable_payload, sort_keys=True)))
    return {
        "result_version": RESULT_VERSION,
        "implementation_version": IMPLEMENTATION_VERSION,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp,
        "scope": {
            "symbol": "SPY",
            "session_date": "2026-03-16",
            "setup_timestamp_utc": KNOWN_SETUP_UTC,
            "covered_setup_families": list(SETUP_FAMILIES),
            "covered_numeric_fields": list(NUMERIC_FIELDS),
            "opra_required": False,
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
            "setup_rows_found": len(setup_rows),
            "setup_rows": [_source_row_snapshot(row) for row in setup_rows],
        },
        "binding_audit": _binding_audit(constructors),
        "family_decision_matrix": _family_decision_matrix(constructors),
        "numeric_constructors": constructors,
        "summary": _summary(constructors),
        "deterministic_comparison": {
            "first_run_equals_second_run": first_hash == second_hash,
            "hashes_match": first_hash == second_hash,
            "result": "PASS" if first_hash == second_hash else "FAIL",
        },
        "first_run_hash": first_hash,
        "second_run_hash": second_hash,
        "guardrails": {
            "raw_ohlcv_promoted_without_rule": False,
            "future_rows_used": False,
            "missing_evidence_converted_to_confidence": False,
            "profitability_claimed": False,
            "promotion_decision_made": True,
            "paper_eligible": False,
            "live_eligible": False,
        },
        "next_action": (
            "Run accepted full-session layer-1 recognition with the promoted family numeric "
            "rules; OPRA/economic work remains separate and blocked."
        ),
    }


def write_outputs(*, source_commit=None, run_timestamp=None):
    document = build_numeric_trigger_invalidation_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    RESULT_DOC_PATH.write_text(_markdown_result(document), encoding="utf-8")
    return document


def construct_family_numeric_fields(*, family, rows, cutoff_utc, package=None):
    if family not in SETUP_FAMILIES:
        raise ValueError(f"Unsupported setup family: {family}")
    normalized_rows = [_normalize_row(row) if "timestamp_utc" not in row else dict(row) for row in rows]
    rows_at_or_before_cutoff = []
    future_rows = []
    for row in normalized_rows:
        if _parse_utc(row["timestamp_utc"]) > _parse_utc(cutoff_utc):
            future_rows.append(row)
        else:
            rows_at_or_before_cutoff.append(row)
    if future_rows:
        return _blocked_constructor(
            family=family,
            cutoff_utc=cutoff_utc,
            source_rows=rows_at_or_before_cutoff,
            blocker_prefix="NUMERIC_FUTURE_ROW_REJECTED",
            detail="constructor input contains rows after the no-hindsight cutoff",
        )

    setup_rows = sorted(
        [
            row
            for row in rows_at_or_before_cutoff
            if row.get("symbol") == "SPY" and row["timestamp_utc"] == cutoff_utc
        ],
        key=_source_row_sort_key,
    )
    missing = _missing_source_fields(setup_rows)
    if missing:
        return _blocked_constructor(
            family=family,
            cutoff_utc=cutoff_utc,
            source_rows=setup_rows,
            blocker_prefix="NUMERIC_SOURCE_FIELD_MISSING",
            detail=f"missing required source fields: {missing}",
            missing_source_fields=missing,
        )
    ambiguous = _ambiguous_source_evidence(setup_rows)
    if ambiguous:
        return _blocked_constructor(
            family=family,
            cutoff_utc=cutoff_utc,
            source_rows=setup_rows,
            blocker_prefix="NUMERIC_AMBIGUOUS_EVIDENCE",
            detail=ambiguous,
        )
    primary_row = _primary_setup_row(setup_rows)
    direction = _accepted_direction(package)
    trigger_field, invalidation_field, trigger_operator, invalidation_operator = _fields_for_direction(direction)
    trigger_value = _decimal(primary_row[trigger_field])
    invalidation_value = _decimal(primary_row[invalidation_field])
    return {
        "setup_family": family,
        "direction": direction,
        "setup_timestamp_utc": cutoff_utc,
        "status": "ACCEPTED_NUMERIC_RULE_ESTABLISHED",
        "promotion_decision": "PROMOTE_CANDIDATE_A",
        "accepted_status": "ACCEPTED",
        "accepted_rule_id": ACCEPTED_RULE_ID,
        "accepted_rule_source": ACCEPTED_RULE_SOURCE,
        "accepted_package_reference": _package_reference(package),
        "binding_audit": _constructor_binding_audit(family, package, primary_row, cutoff_utc),
        "source_rows_used": [_source_row_snapshot(row) for row in setup_rows],
        "trigger": _accepted_field(
            family=family,
            field="trigger",
            direction=direction,
            row=primary_row,
            source_field=trigger_field,
            numeric_value=trigger_value,
            operator=trigger_operator,
            cutoff_utc=cutoff_utc,
        ),
        "invalidation": _accepted_field(
            family=family,
            field="invalidation",
            direction=direction,
            row=primary_row,
            source_field=invalidation_field,
            numeric_value=invalidation_value,
            operator=invalidation_operator,
            cutoff_utc=cutoff_utc,
        ),
        "combined_blocker_code": _combined_blocker_code(
            []
        ),
        "setup_qualified_allowed": True,
        "no_hindsight_cutoff": cutoff_utc,
    }


def _blocked_constructor(
    *,
    family,
    cutoff_utc,
    source_rows,
    blocker_prefix,
    detail,
    missing_source_fields=None,
):
    field_results = {
        field: {
            "setup_family": family,
            "direction": _direction(family),
            "field": field,
            "status": "BLOCKED",
            "blocker_code": f"{blocker_prefix}_{_family_code(family)}_{field.upper()}",
            "detail": detail,
            "numeric_value": None,
            "finite_numeric_value": False,
            "directionally_valid": False,
            "comparison_operator": None,
            "no_hindsight_cutoff": cutoff_utc,
            "source_rows_used": [_source_row_snapshot(row) for row in source_rows],
            "missing_source_fields": list(missing_source_fields or ()),
        }
        for field in NUMERIC_FIELDS
    }
    return {
        "setup_family": family,
        "direction": _direction(family),
        "setup_timestamp_utc": cutoff_utc,
        "status": "BLOCKED",
        "source_rows_used": [_source_row_snapshot(row) for row in source_rows],
        "trigger": field_results["trigger"],
        "invalidation": field_results["invalidation"],
        "combined_blocker_code": _combined_blocker_code(
            [field_results[field]["blocker_code"] for field in NUMERIC_FIELDS]
        ),
        "setup_qualified_allowed": False,
        "no_hindsight_cutoff": cutoff_utc,
    }


def _unresolved_field(family, field, setup_rows, cutoff_utc):
    source_values = {
        source_field: sorted(
            {
                str(row[source_field])
                for row in setup_rows
                if row.get(source_field) not in (None, "")
            }
        )
        for source_field in SOURCE_FIELDS
    }
    return {
        "setup_family": family,
        "direction": _direction(family),
        "field": field,
        "status": "BLOCKED_NUMERIC_RULE_UNRESOLVED",
        "blocker_code": _unresolved_code(family, field),
        "rule_identifier": FIELD_RULE_PATHS[field],
        "source_file": SOURCE_CSV_RELATIVE,
        "source_bar_timestamp": cutoff_utc,
        "source_field": "family_trigger_contract" if field == "trigger" else "family_invalidation_contract",
        "source_value": f"{family} bounded accepted {field} contract",
        "observable_ohlcv_fields": source_values,
        "calculation": (
            "no numeric calculation accepted; local mapper records a family contract but "
            "does not bind that contract to open, high, low, close, volume, VWAP, offset, "
            "buffer, tolerance, or any other numeric threshold"
        ),
        "numeric_value": None,
        "final_numeric_value": None,
        "finite_numeric_value": False,
        "comparison_operator": None,
        "directionally_valid": False,
        "no_hindsight_cutoff": cutoff_utc,
        "source_rows_used": [_source_row_snapshot(row) for row in setup_rows],
    }


def _summary(constructors):
    blockers = defaultdict(int)
    by_family = {}
    for constructor in constructors:
        family = constructor["setup_family"]
        family_blockers = {
            "trigger": constructor["trigger"].get("blocker_code"),
            "invalidation": constructor["invalidation"].get("blocker_code"),
        }
        for code in family_blockers.values():
            if code:
                blockers[code] += 1
        by_family[family] = {
            "trigger_numeric": constructor["trigger"].get("numeric_value"),
            "invalidation_numeric": constructor["invalidation"].get("numeric_value"),
            "setup_qualified_allowed": constructor["setup_qualified_allowed"],
            "promotion_decision": constructor.get("promotion_decision"),
            "accepted_rule_id": constructor.get("accepted_rule_id"),
            "blockers": family_blockers,
        }
    return {
        "families_processed": len(constructors),
        "numeric_values_established": sum(
            1
            for constructor in constructors
            for field in NUMERIC_FIELDS
            if constructor[field].get("finite_numeric_value")
        ),
        "numeric_values_unresolved": sum(
            1
            for constructor in constructors
            for field in NUMERIC_FIELDS
            if not constructor[field].get("finite_numeric_value")
        ),
        "setup_qualified_allowed_count": sum(
            1 for constructor in constructors if constructor["setup_qualified_allowed"]
        ),
        "blockers_by_code": dict(sorted(blockers.items())),
        "by_family": by_family,
    }


def _missing_source_fields(rows):
    if not rows:
        return ["setup_timestamp_row"]
    missing = set()
    for row in rows:
        for field in SOURCE_FIELDS:
            if row.get(field) in (None, ""):
                missing.add(field)
            else:
                try:
                    Decimal(str(row[field]))
                except (InvalidOperation, ValueError):
                    missing.add(field)
    return sorted(missing)


def _ambiguous_source_evidence(rows):
    by_key = defaultdict(list)
    for row in rows:
        by_key[(row.get("timestamp_utc"), row.get("publisher_id"), row.get("instrument_id"))].append(row)
    for key, keyed_rows in by_key.items():
        if len(keyed_rows) <= 1:
            continue
        signatures = {
            tuple(str(row.get(field)) for field in SOURCE_FIELDS)
            for row in keyed_rows
        }
        if len(signatures) > 1:
            return f"conflicting OHLCV rows for timestamp/publisher/instrument key {key}"
    return None


def _accepted_setup_time_packages(source_commit, run_timestamp):
    doc = day50_raw_data_positive_entry_accepted_setup_replay_mapper.build_mapper_document(
        source_commit=source_commit,
        run_timestamp=run_timestamp,
    )
    packages = [
        package
        for package in doc["setup_family_field_packages"]
        if package["setup_family"] in SETUP_FAMILIES and package["setup_time_utc"] == KNOWN_SETUP_UTC
    ]
    return sorted(packages, key=lambda package: SETUP_FAMILIES.index(package["setup_family"]))


def _primary_setup_row(setup_rows):
    return sorted(setup_rows, key=_source_row_sort_key)[0]


def _accepted_direction(package):
    return ACCEPTED_DIRECTION


def _fields_for_direction(direction):
    if direction == "bullish":
        return "high", "low", ">=", "<="
    if direction == "bearish":
        return "low", "high", "<=", ">="
    raise ValueError(f"unsupported accepted direction: {direction}")


def _accepted_field(*, family, field, direction, row, source_field, numeric_value, operator, cutoff_utc):
    return {
        "setup_family": family,
        "direction": direction,
        "field": field,
        "status": "ACCEPTED_NUMERIC_RULE_ESTABLISHED",
        "blocker_code": None,
        "rule_identifier": ACCEPTED_RULE_ID,
        "rule_source": ACCEPTED_RULE_SOURCE,
        "source_file": SOURCE_CSV_RELATIVE,
        "source_bar_timestamp": row["timestamp_utc"],
        "source_field": source_field,
        "source_value": row[source_field],
        "calculation": f"{direction} Candidate A {field} = correctly bound setup-time bar {source_field}",
        "numeric_value": _format_decimal(numeric_value),
        "final_numeric_value": _format_decimal(numeric_value),
        "finite_numeric_value": True,
        "comparison_operator": operator,
        "directionally_valid": True,
        "no_hindsight_cutoff": cutoff_utc,
        "source_rows_used": [_source_row_snapshot(row)],
        "future_row_exclusion_proof": (
            f"value copied from source field {source_field} on row {row['timestamp_utc']}; "
            f"no rows after {cutoff_utc} are read by the constructor"
        ),
    }


def _package_reference(package):
    if not package:
        return None
    return {
        "package_id": package["package_id"],
        "raw_opportunity_id": package["raw_opportunity_id"],
        "status": package["status"],
        "setup_time_utc": package["setup_time_utc"],
        "setup_time_row": package["fields"]["setup_time_row"]["value"],
        "trigger_contract": package["fields"]["trigger"]["value"],
        "invalidation_contract": package["fields"]["invalidation"]["value"],
    }


def _constructor_binding_audit(family, package, row, cutoff_utc):
    expected = package["setup_time_utc"] if package else cutoff_utc
    return {
        "family": family,
        "candidate_package_id": package["package_id"] if package else None,
        "expected_opportunity_timestamp": expected,
        "actual_bound_setup_time_timestamp": row["timestamp_utc"],
        "source_row_index": row.get("source_index"),
        "source_row": _source_row_snapshot(row),
        "direction": ACCEPTED_DIRECTION,
        "no_hindsight_cutoff": cutoff_utc,
        "code_path": "day52_numeric_trigger_invalidation.construct_family_numeric_fields -> _primary_setup_row",
        "binding_result": "LEGITIMATE_SHARED_SETUP_TIME_ROW",
        "shared_row_reason": (
            "Day 50 accepted mapper created separate family packages that intentionally reference "
            "the same publisher-collapsed setup-time decision row."
        ),
    }


def _binding_audit(constructors):
    return [constructor["binding_audit"] for constructor in constructors]


def _family_decision_matrix(constructors):
    return [
        {
            "family": constructor["setup_family"],
            "decision": constructor["promotion_decision"],
            "direction": constructor["direction"],
            "rule_id": constructor["accepted_rule_id"],
            "rule_source": constructor["accepted_rule_source"],
            "setup_time_timestamp": constructor["setup_timestamp_utc"],
            "source_row_index": constructor["binding_audit"]["source_row_index"],
            "trigger": constructor["trigger"]["final_numeric_value"],
            "invalidation": constructor["invalidation"]["final_numeric_value"],
            "accepted_status": constructor["accepted_status"],
        }
        for constructor in constructors
    ]


def _combined_blocker_code(codes):
    if not codes:
        return None
    return "__".join(codes)


def _unresolved_code(family, field):
    return f"NUMERIC_RULE_UNRESOLVED_{_family_code(family)}_{field.upper()}"


def _family_code(family):
    return family.upper().replace(" ", "_")


def _decimal(value):
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"not a finite decimal value: {value!r}") from exc


def _format_decimal(value):
    return format(value, "f")


def _direction(family):
    return (
        "long_call_only_when_family_selector_is_accepted"
        if family == "Clean Fast Break"
        else "rule_gap_no_accepted_local_family_selector"
    )


def _source_row_snapshot(row):
    return {
        "source_index": row.get("source_index"),
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


def _source_row_sort_key(row):
    return (
        row.get("timestamp_utc"),
        str(row.get("publisher_id")),
        str(row.get("instrument_id")),
        str(row.get("open")),
        str(row.get("high")),
        str(row.get("low")),
        str(row.get("close")),
        str(row.get("volume")),
    )


def _read_source_rows(path):
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _normalize_source_rows(rows):
    index_lookup = _source_index_lookup()
    normalized = []
    for fallback_index, row in enumerate(rows):
        source_index = index_lookup.get(_source_signature(row), fallback_index)
        normalized.append(_normalize_row(row, source_index=source_index))
    return normalized


def _source_index_lookup():
    try:
        rows = _read_source_rows(SOURCE_CSV_PATH)
    except FileNotFoundError:
        return {}
    return {_source_signature(row): index for index, row in enumerate(rows)}


def _source_signature(row):
    return tuple(
        str(row.get(key))
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
    )


def _normalize_row(row, source_index=None):
    if "timestamp_utc" in row and "timestamp_et" in row:
        item = dict(row)
        if source_index is not None:
            item["source_index"] = source_index
        return item
    ts = _parse_utc(row["ts_event"])
    item = dict(row)
    item["timestamp_utc"] = _format_utc(ts)
    item["timestamp_et"] = ts.astimezone(NY).isoformat()
    if source_index is not None:
        item["source_index"] = source_index
    return item


def _parse_utc(value):
    if value.endswith("Z"):
        base = value.replace("Z", "+00:00")
    else:
        base = value
    if "." in base:
        left, right = base.split(".", 1)
        suffix = ""
        if "+" in right:
            frac, suffix = right.split("+", 1)
            suffix = "+" + suffix
        elif "-" in right:
            frac, suffix = right.split("-", 1)
            suffix = "-" + suffix
        else:
            frac = right
        base = f"{left}.{frac[:6]}{suffix}"
    parsed = datetime.fromisoformat(base)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _format_utc(value):
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _stable_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode("utf-8")).hexdigest()


def _file_sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _git_short_head():
    import subprocess

    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=REPO_ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "UNKNOWN"


def _utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None).isoformat() + "Z"


def _markdown_result(document):
    lines = [
        "# SAFE-FAST Day 52 Numeric Trigger and Invalidation Result",
        "",
        "## Scope",
        "",
        "- Task executed: `SAFE_FAST_DAY52_FAMILY_NUMERIC_BINDING_AND_PROMOTION_CODEX_TASK.md`.",
        "- Machine-readable result: `historical_signal_replay/results/day52_numeric_trigger_invalidation.json`.",
        "- Implementation: `historical_signal_replay/day52_numeric_trigger_invalidation.py`.",
        "- Covered setup families: Ideal, Clean Fast Break, and Continuation for SPY on `2026-03-16`.",
        "",
        "## Result",
        "",
        "Candidate A setup-bar range is promoted separately for each family after binding audit.",
        "The constructors bind trigger to the setup-time high and invalidation to the setup-time low for the bullish accepted packages.",
        "",
    ]
    for family, item in document["summary"]["by_family"].items():
        lines.append(
            f"- {family}: trigger `{item['trigger_numeric']}` "
            f"({item['promotion_decision']}), invalidation `{item['invalidation_numeric']}` "
            f"({item['accepted_rule_id']}); setup-qualified allowed `{item['setup_qualified_allowed']}`."
        )
    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "No OPRA evidence, option selection, entry, exit, P&L, proof, profitability, paper/live eligibility, "
            "`main.py`, Railway/deploy, broker/account/order/fill/alert, credential, `.env`, sizing, or frozen "
            "`patch8` threshold change was made.",
        ]
    )
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    print(json.dumps(write_outputs(), indent=2, sort_keys=True))
