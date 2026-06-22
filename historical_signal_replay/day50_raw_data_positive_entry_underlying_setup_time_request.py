import csv
import hashlib
import json
import os
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_OUTPUT_DIR = (
    REPO_ROOT / "historical_signal_replay" / "source_data" / "external_underlying_data_drop"
)
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day50_raw_data_positive_entry_underlying_setup_time_costed_request.json"
)

REQUEST_ID = "DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M"
DATASET = "DBEQ.BASIC"
SCHEMA = "ohlcv-1m"
STYPE_IN = "raw_symbol"
SYMBOL = "SPY"
START_TIMESTAMP = "2026-03-16T09:30:00-04:00"
END_TIMESTAMP = "2026-03-16T16:00:00-04:00"
EXPECTED_CHECKED_COST = Decimal("0.001370869577")
MAX_AUTHORIZED_COST = EXPECTED_CHECKED_COST
CSV_FILENAME = f"SAFE_FAST_{REQUEST_ID}.csv"
DBN_FILENAME = f"SAFE_FAST_{REQUEST_ID}.dbn.zst"
MANIFEST_FILENAME = f"SAFE_FAST_{REQUEST_ID}_DOWNLOAD_MANIFEST.json"


def build_exact_request():
    return {
        "request_id": REQUEST_ID,
        "request_type": "underlying_setup_time_data",
        "dataset": DATASET,
        "schema": SCHEMA,
        "stype_in": STYPE_IN,
        "symbol": SYMBOL,
        "start_timestamp": START_TIMESTAMP,
        "end_timestamp": END_TIMESTAMP,
        "timezone": "America/New_York",
        "checked_cost": str(EXPECTED_CHECKED_COST),
        "authorized_ceiling": str(MAX_AUTHORIZED_COST),
        "forbidden_scope": [
            "option data",
            "exit-path data",
            "macro data",
            "headline data",
            "IV/Greeks",
            "fills",
            "P&L",
            "live broker decisions",
        ],
    }


def validate_exact_request_scope(request=None):
    request = request or build_exact_request()
    problems = []
    expected = build_exact_request()
    for field in (
        "request_id",
        "request_type",
        "dataset",
        "schema",
        "stype_in",
        "symbol",
        "start_timestamp",
        "end_timestamp",
    ):
        if request.get(field) != expected[field]:
            problems.append(f"unexpected_{field}")
    if Decimal(str(request.get("checked_cost", "0"))) != EXPECTED_CHECKED_COST:
        problems.append("checked_cost_changed_from_approved_scope")
    return sorted(set(problems))


def check_cost(api_key=None, request=None):
    import databento as db

    request = request or build_exact_request()
    problems = validate_exact_request_scope(request)
    if problems:
        raise RuntimeError("; ".join(problems))
    api_key = api_key or os.environ.get("SAFE_FAST_DB_AUTH")
    if not api_key:
        raise RuntimeError("SAFE_FAST_DB_AUTH is not available")

    client = db.Historical(key=api_key)
    cost = Decimal(
        str(
            client.metadata.get_cost(
                dataset=request["dataset"],
                start=request["start_timestamp"],
                end=request["end_timestamp"],
                symbols=request["symbol"],
                schema=request["schema"],
                stype_in=request["stype_in"],
            )
        )
    )
    return {
        "checked_at_utc": _utc_now(),
        "checked_cost": str(cost),
        "matches_prior_checked_cost": cost == EXPECTED_CHECKED_COST,
        "checked_cost_at_or_below_authorized_ceiling": cost <= MAX_AUTHORIZED_COST,
        "authorized_ceiling": str(MAX_AUTHORIZED_COST),
        "prior_checked_cost": str(EXPECTED_CHECKED_COST),
        "credential_used": True,
    }


def download_exact_underlying_setup_time_evidence(api_key=None, cost_check=None):
    import databento as db

    request = build_exact_request()
    cost_check = cost_check or check_cost(api_key=api_key, request=request)
    if not cost_check["checked_cost_at_or_below_authorized_ceiling"]:
        raise RuntimeError("fresh checked cost exceeds exact authorized ceiling")
    if not cost_check["matches_prior_checked_cost"]:
        raise RuntimeError("fresh checked cost changed from the exact prior checked scope")

    api_key = api_key or os.environ.get("SAFE_FAST_DB_AUTH")
    if not api_key:
        raise RuntimeError("SAFE_FAST_DB_AUTH is not available")

    RAW_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    dbn_path = RAW_OUTPUT_DIR / DBN_FILENAME
    csv_path = RAW_OUTPUT_DIR / CSV_FILENAME
    manifest_path = RAW_OUTPUT_DIR / MANIFEST_FILENAME
    _remove_existing_day50_file(dbn_path)
    _remove_existing_day50_file(csv_path)
    _remove_existing_day50_file(manifest_path)

    client = db.Historical(key=api_key)
    store = client.timeseries.get_range(
        dataset=request["dataset"],
        start=request["start_timestamp"],
        end=request["end_timestamp"],
        symbols=request["symbol"],
        schema=request["schema"],
        stype_in=request["stype_in"],
        path=dbn_path,
    )
    store.to_csv(csv_path, schema=request["schema"])
    downloaded = _validate_downloaded_file(request, dbn_path, csv_path, cost_check)
    manifest = {
        "schema_version": "safe-fast-day50-raw-positive-entry-underlying-setup-time-v1",
        "created_utc": _utc_now(),
        "approval_scope_confirmed_by_task": True,
        "exact_request": request,
        "fresh_cost_check": cost_check,
        "actual_billed_cost": "NOT_AVAILABLE",
        "download_created": True,
        "downloaded_request": downloaded,
        "forbidden_scope_requested": False,
        "option_data_requested": False,
        "exit_path_data_requested": False,
        "proof_accepted": False,
        "profitability_claimed": False,
        "paper_eligible": False,
        "live_eligible": False,
        "problems": downloaded["validation_problems"],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    RESULT_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def load_download_manifest(path=None):
    path = Path(path) if path else RAW_OUTPUT_DIR / MANIFEST_FILENAME
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _validate_downloaded_file(request, dbn_path, csv_path, cost_check):
    rows = _read_csv_dicts(csv_path) if csv_path.exists() else []
    problems = []
    if not dbn_path.exists() or dbn_path.stat().st_size <= 0:
        problems.append("missing_or_empty_dbn")
    if not csv_path.exists():
        problems.append("missing_csv")
    if not rows:
        problems.append("empty_csv")
    if rows:
        problems.extend(_csv_scope_problems(request, rows))

    return {
        "request_id": request["request_id"],
        "dataset": request["dataset"],
        "schema": request["schema"],
        "stype_in": request["stype_in"],
        "symbol": request["symbol"],
        "start_timestamp": request["start_timestamp"],
        "end_timestamp": request["end_timestamp"],
        "dbn_path": _relative(dbn_path),
        "csv_path": _relative(csv_path),
        "byte_count": dbn_path.stat().st_size if dbn_path.exists() else 0,
        "row_count": len(rows),
        "sha256": _file_sha256(dbn_path) if dbn_path.exists() else None,
        "csv_sha256": _file_sha256(csv_path) if csv_path.exists() else None,
        "checked_cost": cost_check["checked_cost"],
        "actual_billed_cost": "NOT_AVAILABLE",
        "validation_problems": sorted(set(problems)),
    }


def _csv_scope_problems(request, rows):
    problems = []
    start = _parse_timestamp(request["start_timestamp"])
    end = _parse_timestamp(request["end_timestamp"])
    present = set(rows[0])
    if not {"ts_event", "symbol", "open", "high", "low", "close", "volume"} <= present:
        problems.append("missing_required_ohlcv_scope_columns")
    previous = None
    for row in rows:
        if row.get("symbol") != request["symbol"]:
            problems.append("contradictory_symbol")
        ts_event = _parse_timestamp(row["ts_event"])
        if ts_event < start or ts_event >= end:
            problems.append("row_outside_authorized_window")
        if previous and ts_event < previous:
            problems.append("non_chronological_rows")
        previous = ts_event
        for field in ("open", "high", "low", "close", "volume"):
            if str(row.get(field, "")).strip() == "":
                problems.append(f"missing_{field}")
    return sorted(set(problems))


def _read_csv_dicts(path):
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _parse_timestamp(value):
    text = str(value)
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    return datetime.fromisoformat(text)


def _file_sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _remove_existing_day50_file(path):
    path = Path(path)
    if not path.exists():
        return
    if path.parent.resolve() != RAW_OUTPUT_DIR.resolve():
        raise RuntimeError(f"refusing to replace file outside raw output dir: {path}")
    if REQUEST_ID not in path.name:
        raise RuntimeError(f"refusing to replace unexpected file: {path.name}")
    path.unlink()


def _relative(path):
    return str(Path(path).relative_to(REPO_ROOT)).replace("\\", "/")


def _utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _main():
    manifest = download_exact_underlying_setup_time_evidence()
    if manifest["problems"]:
        for problem in manifest["problems"]:
            print(problem)
        raise SystemExit(1)
    downloaded = manifest["downloaded_request"]
    print(
        "downloaded day50 exact underlying setup-time evidence: "
        f"{downloaded['row_count']} rows, checked cost {manifest['fresh_cost_check']['checked_cost']}, "
        f"actual billed cost {manifest['actual_billed_cost']}"
    )


if __name__ == "__main__":
    _main()
