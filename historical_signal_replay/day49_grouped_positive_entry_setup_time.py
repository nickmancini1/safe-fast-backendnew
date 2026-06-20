import csv
import hashlib
import json
import os
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

from historical_signal_replay import databento_opra_normalizer as opra
from historical_signal_replay import execution_context_calculator as execution_context


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "source_data"
    / "richer_export_package_work"
    / "day48_grouped_positive_entry_setup_time_request_manifest.json"
)
RAW_OUTPUT_DIR = (
    REPO_ROOT
    / "historical_signal_replay"
    / "source_data"
    / "external_option_data_drop"
)
DOWNLOAD_MANIFEST_PATH = (
    RAW_OUTPUT_DIR
    / "SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_SETUP_TIME_DOWNLOAD_MANIFEST.json"
)

MAX_AUTHORIZED_COST = Decimal("0.01")
EXPECTED_MANIFEST_SHA256 = (
    "213dc93d2c08cd0653a78eb64c002b57673ab48a8a4f4b5ee727ff0c77b0f2bf"
)


def load_request_manifest(path=MANIFEST_PATH):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def manifest_sha256(path=MANIFEST_PATH):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def validate_request_manifest(manifest=None, *, expected_sha256=EXPECTED_MANIFEST_SHA256):
    manifest = manifest or load_request_manifest()
    problems = []
    requests = manifest.get("requests")
    if not isinstance(requests, list):
        return ["manifest requests must be a list"]
    if len(requests) != 4:
        problems.append(f"expected exactly 4 requests, found {len(requests)}")
    if manifest_sha256() != expected_sha256:
        problems.append("manifest sha256 changed from the approved request package")

    for request in requests:
        request_id = request.get("request_id", "")
        if not request_id:
            problems.append("request missing request_id")
        if request.get("dataset") != "OPRA.PILLAR":
            problems.append(f"{request_id} uses non-approved dataset")
        if request.get("schema") not in {"tcbbo", "trades"}:
            problems.append(f"{request_id} uses non-approved schema")
        if request.get("symbol_type") != "raw_symbol":
            problems.append(f"{request_id} uses non-approved symbol type")
        if request.get("conditional_exit_path_window") is not None:
            problems.append(f"{request_id} includes a conditional exit path")
        if not request.get("raw_symbol"):
            problems.append(f"{request_id} missing raw_symbol")
        if not request.get("start_timestamp_utc") or not request.get("end_timestamp_utc"):
            problems.append(f"{request_id} missing UTC request window")
    return problems


def check_manifest_cost(api_key=None, manifest=None):
    import databento as db

    manifest = manifest or load_request_manifest()
    api_key = api_key or os.environ.get("SAFE_FAST_DB_AUTH")
    if not api_key:
        raise RuntimeError("SAFE_FAST_DB_AUTH is not available")

    client = db.Historical(key=api_key)
    costs = []
    for request in manifest["requests"]:
        cost = Decimal(
            str(
                client.metadata.get_cost(
                    dataset=request["dataset"],
                    start=request["start_timestamp_utc"],
                    end=request["end_timestamp_utc"],
                    symbols=request["raw_symbol"],
                    schema=request["schema"],
                    stype_in="raw_symbol",
                )
            )
        )
        costs.append(
            {
                "request_id": request["request_id"],
                "candidate_id": request["candidate_id"],
                "schema": request["schema"],
                "raw_symbol": request["raw_symbol"],
                "start_timestamp_utc": request["start_timestamp_utc"],
                "end_timestamp_utc": request["end_timestamp_utc"],
                "checked_cost": str(cost),
            }
        )
    total = sum(Decimal(item["checked_cost"]) for item in costs)
    return {
        "checked_at_utc": _utc_now(),
        "checked_total": str(total),
        "checked_total_at_or_below_limit": total <= MAX_AUTHORIZED_COST,
        "requests": costs,
    }


def download_manifest_requests(api_key=None, manifest=None, cost_check=None):
    import databento as db

    manifest = manifest or load_request_manifest()
    problems = validate_request_manifest(manifest)
    if problems:
        raise RuntimeError("; ".join(problems))

    cost_check = cost_check or check_manifest_cost(api_key=api_key, manifest=manifest)
    if Decimal(cost_check["checked_total"]) > MAX_AUTHORIZED_COST:
        raise RuntimeError("fresh checked total exceeds the authorized one-cent limit")

    api_key = api_key or os.environ.get("SAFE_FAST_DB_AUTH")
    if not api_key:
        raise RuntimeError("SAFE_FAST_DB_AUTH is not available")

    client = db.Historical(key=api_key)
    RAW_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    downloaded = []
    for request in manifest["requests"]:
        stem = _safe_request_stem(request)
        dbn_path = RAW_OUTPUT_DIR / f"{stem}.dbn.zst"
        csv_path = RAW_OUTPUT_DIR / f"{stem}.csv"
        store = client.timeseries.get_range(
            dataset=request["dataset"],
            start=request["start_timestamp_utc"],
            end=request["end_timestamp_utc"],
            symbols=request["raw_symbol"],
            schema=request["schema"],
            stype_in="raw_symbol",
            path=dbn_path,
        )
        store.to_csv(csv_path, schema=request["schema"])
        downloaded.append(_validate_downloaded_request(request, dbn_path, csv_path, cost_check))

    summary = {
        "schema_version": "safe-fast-day49-setup-time-download-manifest-v1",
        "created_utc": _utc_now(),
        "request_manifest_path": str(MANIFEST_PATH.relative_to(REPO_ROOT)),
        "request_manifest_sha256": manifest_sha256(),
        "fresh_cost_check": cost_check,
        "actual_billed_cost": "NOT_AVAILABLE",
        "downloaded_requests": downloaded,
        "problems": [
            problem
            for item in downloaded
            for problem in item.get("validation_problems", [])
        ],
    }
    DOWNLOAD_MANIFEST_PATH.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return summary


def load_download_manifest(path=DOWNLOAD_MANIFEST_PATH):
    path = Path(path)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def build_setup_time_evidence(download_manifest=None):
    download_manifest = download_manifest or load_download_manifest()
    if not download_manifest:
        return {}
    request_records = {
        request["request_id"]: request
        for request in load_request_manifest()["requests"]
    }
    grouped = {}
    for item in download_manifest.get("downloaded_requests", []):
        request = request_records.get(item.get("request_id"))
        if not request or item.get("validation_problems"):
            continue
        grouped.setdefault(request["funnel_candidate_identifier"], {})[
            request["schema"]
        ] = {
            "request": request,
            "csv_path": REPO_ROOT / item["csv_path"],
            "row_count": item["row_count"],
        }

    evidence = {}
    for candidate_identifier, by_schema in grouped.items():
        if "tcbbo" not in by_schema or "trades" not in by_schema:
            continue
        quote_request = by_schema["tcbbo"]["request"]
        signal_time = quote_request["signal_timestamp_utc"]
        quote_rows = _load_quotes_or_empty(by_schema["tcbbo"]["csv_path"])
        trade_rows = _load_trades_or_empty(by_schema["trades"]["csv_path"])
        quote = opra.select_quote_at_or_before(
            quote_rows,
            signal_time,
            symbol=quote_request["raw_symbol"],
            instrument_id=quote_request.get("instrument_id_when_known"),
        )
        volume = _trade_volume_through_signal(
            trade_rows,
            signal_time,
            quote_request["raw_symbol"],
            quote_request.get("instrument_id_when_known"),
        )
        execution = _execution_result(signal_time, quote, volume)
        evidence[candidate_identifier] = {
            "candidate_id": quote_request["candidate_id"],
            "setup_family": quote_request["setup_family"],
            "raw_symbol": quote_request["raw_symbol"],
            "instrument_id": quote_request.get("instrument_id_when_known"),
            "signal_timestamp_utc": signal_time,
            "quote": _quote_summary(quote),
            "setup_time_trade_volume": str(volume),
            "contract_selection_result": _contract_selection_result(quote, volume, execution),
            "price_acceptability_result": execution,
            "entry_eligibility_result": _entry_eligibility_result(execution),
            "entry_recorded_result": "not_recorded_no_family_entry_rule_or_exit_path",
        }
    return evidence


def _validate_downloaded_request(request, dbn_path, csv_path, cost_check):
    row_count = _csv_row_count(csv_path)
    problems = []
    if not dbn_path.exists() or dbn_path.stat().st_size <= 0:
        problems.append("missing_or_empty_dbn")
    if not csv_path.exists():
        problems.append("missing_csv")
    if row_count < 0:
        problems.append("malformed_csv")
    if row_count == 0:
        problems.append("empty_csv")
    if csv_path.exists() and row_count >= 0:
        problems.extend(_csv_scope_problems(request, csv_path))

    checked_cost = next(
        item["checked_cost"]
        for item in cost_check["requests"]
        if item["request_id"] == request["request_id"]
    )
    return {
        "request_id": request["request_id"],
        "candidate_id": request["candidate_id"],
        "schema": request["schema"],
        "raw_symbol": request["raw_symbol"],
        "start_timestamp_utc": request["start_timestamp_utc"],
        "end_timestamp_utc": request["end_timestamp_utc"],
        "dbn_path": str(dbn_path.relative_to(REPO_ROOT)),
        "csv_path": str(csv_path.relative_to(REPO_ROOT)),
        "byte_count": dbn_path.stat().st_size if dbn_path.exists() else 0,
        "row_count": row_count,
        "sha256": _file_sha256(dbn_path) if dbn_path.exists() else None,
        "csv_sha256": _file_sha256(csv_path) if csv_path.exists() else None,
        "checked_cost": checked_cost,
        "actual_billed_cost": "NOT_AVAILABLE",
        "empty_malformed_late_stale_or_contradictory_evidence": problems or [],
        "validation_problems": problems,
    }


def _csv_scope_problems(request, csv_path):
    problems = []
    start = opra.normalize_timestamp(request["start_timestamp_utc"])
    end = opra.normalize_timestamp(request["end_timestamp_utc"])
    required = opra.QUOTE_COLUMNS if request["schema"] == "tcbbo" else opra.TRADE_COLUMNS
    try:
        rows = _read_csv_dicts(csv_path, required)
    except Exception:
        return ["malformed_csv"]
    for row in rows:
        symbol = row.get("symbol") or row.get("raw_symbol")
        if symbol != request["raw_symbol"]:
            problems.append("contradictory_symbol")
            break
    for row in rows:
        ts_event = opra.normalize_timestamp(row["ts_event"])
        if ts_event < start or ts_event > end:
            problems.append("row_outside_authorized_window")
            break
    return sorted(set(problems))


def _load_quotes_or_empty(path):
    try:
        return opra.load_quotes_csv(path)
    except Exception:
        return []


def _load_trades_or_empty(path):
    try:
        return opra.load_trades_csv(path)
    except Exception:
        return []


def _trade_volume_through_signal(rows, signal_time, symbol, instrument_id):
    signal_at = opra.normalize_timestamp(signal_time)
    total = Decimal("0")
    for row in rows:
        if row["symbol"] != symbol:
            continue
        if instrument_id is not None and str(row["instrument_id"]) != str(instrument_id):
            continue
        if row["ts_event"] <= signal_at and row.get("trade_size") is not None:
            total += Decimal(str(row["trade_size"]))
    return total


def _execution_result(signal_time, quote, volume):
    if quote is None:
        return execution_context.calculate_execution_context(
            signal_time=signal_time,
            quote_time=None,
            bid=None,
            ask=None,
            spread=None,
            bid_size=None,
            ask_size=None,
            setup_time_trade_volume=None,
        )
    return execution_context.calculate_execution_context(
        signal_time=signal_time,
        quote_time=quote["ts_event"].isoformat().replace("+00:00", "Z"),
        bid=quote["bid"],
        ask=quote["ask"],
        spread=quote["spread"],
        bid_size=quote["bid_size"],
        ask_size=quote["ask_size"],
        setup_time_trade_volume=volume,
    )


def _contract_selection_result(quote, volume, execution):
    del execution
    if quote is None:
        return {
            "contract_selection_status": "abstain",
            "selected_contract": None,
            "rejection_reason": "missing_setup_safe_quote",
        }
    if volume < Decimal("1"):
        return {
            "contract_selection_status": "abstain",
            "selected_contract": None,
            "rejection_reason": "trade_volume_below_1",
        }
    return {
        "contract_selection_status": "selected",
        "selected_contract": quote["symbol"],
        "rejection_reason": None,
    }


def _entry_eligibility_result(execution):
    if execution["execution_context_status"] == "fail":
        return {
            "entry_eligibility_status": "blocked",
            "rejection_reason": execution["rejection_reason"],
        }
    if execution["execution_context_status"] == "unknown":
        return {
            "entry_eligibility_status": "unknown",
            "rejection_reason": execution["rejection_reason"],
        }
    return {
        "entry_eligibility_status": "missing_data",
        "rejection_reason": "missing_accepted_entry_exit_rule_for_non_cfb_family",
    }


def _quote_summary(quote):
    if quote is None:
        return None
    return {
        "ts_event": quote["ts_event"].isoformat().replace("+00:00", "Z"),
        "ts_recv": quote["ts_recv"].isoformat().replace("+00:00", "Z"),
        "instrument_id": quote["instrument_id"],
        "symbol": quote["symbol"],
        "bid": str(quote["bid"]),
        "ask": str(quote["ask"]),
        "spread": str(quote["spread"]),
        "spread_pct": str(quote["spread_pct"]),
        "bid_size": str(quote["bid_size"]),
        "ask_size": str(quote["ask_size"]),
    }


def _safe_request_stem(request):
    return "SAFE_FAST_DAY49_" + "".join(
        char if char.isalnum() or char in {"_", "-"} else "_"
        for char in request["request_id"]
    )


def _csv_row_count(path):
    try:
        with Path(path).open(newline="", encoding="utf-8") as handle:
            reader = csv.reader(handle)
            next(reader, None)
            return sum(1 for _ in reader)
    except Exception:
        return -1


def _read_csv_dicts(path, required_columns):
    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        present = set(reader.fieldnames or ())
        missing = set(required_columns) - present
        if missing:
            raise ValueError(f"missing columns: {sorted(missing)}")
        return list(reader)


def _file_sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _main():
    manifest = load_request_manifest()
    problems = validate_request_manifest(manifest)
    if problems:
        for problem in problems:
            print(problem)
        raise SystemExit(1)
    cost = check_manifest_cost(manifest=manifest)
    if not cost["checked_total_at_or_below_limit"]:
        print("fresh checked total exceeds authorized limit")
        raise SystemExit(1)
    summary = download_manifest_requests(manifest=manifest, cost_check=cost)
    if summary["problems"]:
        for problem in summary["problems"]:
            print(problem)
        raise SystemExit(1)
    print(
        "downloaded day49 setup-time package: "
        f"{len(summary['downloaded_requests'])} requests, "
        f"fresh checked total ${summary['fresh_cost_check']['checked_total']}"
    )


if __name__ == "__main__":
    _main()
