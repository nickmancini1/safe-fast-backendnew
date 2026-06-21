import csv
import hashlib
import json
import os
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REQUEST_MANIFEST_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "source_data"
    / "richer_export_package_work"
    / "day49_positive_entry_exact_setup_data_request_manifest.json"
)
RAW_OUTPUT_DIR = (
    REPO_ROOT
    / "historical_signal_replay"
    / "source_data"
    / "external_underlying_data_drop"
)
DOWNLOAD_MANIFEST_PATH = (
    RAW_OUTPUT_DIR
    / "SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_OHLCV_DOWNLOAD_MANIFEST.json"
)

DATASET = "DBEQ.BASIC"
SCHEMA = "ohlcv-1h"
STYPE_IN = "raw_symbol"
MAX_AUTHORIZED_COST = Decimal("0.01")
EXPECTED_PRIOR_CHECKED_COST = Decimal("0.002040266989")
EXPECTED_REQUEST_SCOPE_SHA256 = (
    "a6086e1fae554716ab21207e65ac6d174a2fc5db8707cd0e90679655caae9a95"
)
AUTHORIZED_SYMBOLS = ("GLD", "SPY", "QQQ", "IWM")


def load_request_manifest(path=REQUEST_MANIFEST_PATH):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def request_manifest_sha256(path=REQUEST_MANIFEST_PATH):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def request_manifest_scope_sha256(manifest=None):
    manifest = manifest or load_request_manifest()
    scope = {
        "manifest_version": manifest.get("manifest_version"),
        "request_scope": manifest.get("request_scope"),
        "request_count": manifest.get("request_count"),
        "requests": manifest.get("requests"),
    }
    encoded = json.dumps(scope, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_ohlcv_requests(manifest=None):
    manifest = manifest or load_request_manifest()
    requests = []
    for request in manifest.get("requests", []):
        start = request["start_timestamp"]
        original_end = request["end_timestamp"]
        repaired_end = _add_one_hour(original_end)
        requests.append(
            {
                "request_id": f"{request['candidate_identifier']}-DBEQ-BASIC-OHLCV-1H-RAW-SYMBOL",
                "candidate_identifier": request["candidate_identifier"],
                "underlying": request["underlying"],
                "symbol": request["symbol"],
                "dataset": DATASET,
                "schema": SCHEMA,
                "stype_in": STYPE_IN,
                "start_timestamp": start,
                "original_manifest_end_timestamp": original_end,
                "end_timestamp": repaired_end,
                "end_exclusive_repair": "manifest_end_plus_one_hour",
                "forbidden_scope": [
                    "options",
                    "exit_path",
                    "macro",
                    "event",
                    "headline",
                    "IV",
                    "setup_labels",
                    "P&L",
                ],
            }
        )
    return requests


def validate_ohlcv_request_scope(manifest=None):
    manifest = manifest or load_request_manifest()
    problems = []
    if request_manifest_scope_sha256(manifest) != EXPECTED_REQUEST_SCOPE_SHA256:
        problems.append("request_manifest_scope_sha256_changed_from_prior_checked_subset")
    if manifest.get("request_count") != 7:
        problems.append(f"expected 7 setup request rows, found {manifest.get('request_count')}")
    if manifest.get("option_request_included"):
        problems.append("source manifest includes option request")
    if manifest.get("exit_path_request_included"):
        problems.append("source manifest includes exit-path request")
    requests = build_ohlcv_requests(manifest)
    if len(requests) != 7:
        problems.append(f"expected 7 OHLCV requests, found {len(requests)}")
    for request in requests:
        request_id = request["request_id"]
        if request["dataset"] != DATASET:
            problems.append(f"{request_id} uses non-authorized dataset")
        if request["schema"] != SCHEMA:
            problems.append(f"{request_id} uses non-authorized schema")
        if request["stype_in"] != STYPE_IN:
            problems.append(f"{request_id} uses non-authorized symbol type")
        if request["symbol"] not in AUTHORIZED_SYMBOLS:
            problems.append(f"{request_id} uses non-authorized symbol")
        if request["symbol"] != request["underlying"]:
            problems.append(f"{request_id} symbol/underlying mismatch")
        if _parse_timestamp(request["start_timestamp"]) >= _parse_timestamp(request["end_timestamp"]):
            problems.append(f"{request_id} has non-positive repaired time window")
    return sorted(set(problems))


def check_ohlcv_cost(api_key=None, manifest=None):
    import databento as db

    manifest = manifest or load_request_manifest()
    problems = validate_ohlcv_request_scope(manifest)
    if problems:
        raise RuntimeError("; ".join(problems))
    api_key = api_key or os.environ.get("SAFE_FAST_DB_AUTH")
    if not api_key:
        raise RuntimeError("SAFE_FAST_DB_AUTH is not available")

    client = db.Historical(key=api_key)
    costs = []
    for request in build_ohlcv_requests(manifest):
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
        costs.append({**request, "checked_cost": str(cost)})
    total = sum(Decimal(item["checked_cost"]) for item in costs)
    return {
        "checked_at_utc": _utc_now(),
        "checked_total": str(total),
        "checked_total_at_or_below_limit": total <= MAX_AUTHORIZED_COST,
        "authorized_ceiling": str(MAX_AUTHORIZED_COST),
        "prior_checked_total": str(EXPECTED_PRIOR_CHECKED_COST),
        "requests": costs,
    }


def download_ohlcv_requests(api_key=None, manifest=None, cost_check=None):
    import databento as db

    manifest = manifest or load_request_manifest()
    problems = validate_ohlcv_request_scope(manifest)
    if problems:
        raise RuntimeError("; ".join(problems))
    cost_check = cost_check or check_ohlcv_cost(api_key=api_key, manifest=manifest)
    if Decimal(cost_check["checked_total"]) > MAX_AUTHORIZED_COST:
        raise RuntimeError("fresh checked total exceeds the authorized one-cent limit")

    api_key = api_key or os.environ.get("SAFE_FAST_DB_AUTH")
    if not api_key:
        raise RuntimeError("SAFE_FAST_DB_AUTH is not available")

    client = db.Historical(key=api_key)
    RAW_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    downloaded = []
    for request in build_ohlcv_requests(manifest):
        stem = _safe_request_stem(request)
        dbn_path = RAW_OUTPUT_DIR / f"{stem}.dbn.zst"
        csv_path = RAW_OUTPUT_DIR / f"{stem}.csv"
        _remove_existing_download_file(dbn_path)
        _remove_existing_download_file(csv_path)
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
        downloaded.append(_validate_downloaded_request(request, dbn_path, csv_path, cost_check))

    summary = {
        "schema_version": "safe-fast-day49-positive-entry-ohlcv-download-manifest-v1",
        "created_utc": _utc_now(),
        "request_manifest_path": str(REQUEST_MANIFEST_PATH.relative_to(REPO_ROOT)),
        "request_manifest_sha256": request_manifest_sha256(),
        "authorized_scope": {
            "dataset": DATASET,
            "schema": SCHEMA,
            "stype_in": STYPE_IN,
            "symbols": list(AUTHORIZED_SYMBOLS),
            "fresh_cost_ceiling": str(MAX_AUTHORIZED_COST),
            "forbidden_data": [
                "option",
                "exit-path",
                "macro",
                "event",
                "headline",
                "IV",
                "setup-label",
            ],
        },
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


def affected_candidate_replay_summary(download_manifest=None):
    download_manifest = download_manifest or load_download_manifest()
    if not download_manifest:
        return {"status": "NO_DOWNLOAD_MANIFEST"}
    request_ids = {
        item["request_id"]
        for item in download_manifest.get("downloaded_requests", [])
        if not item.get("validation_problems")
    }
    affected = []
    for request in build_ohlcv_requests():
        affected.append(
            {
                "candidate_identifier": request["candidate_identifier"],
                "underlying": request["underlying"],
                "ohlcv_download_validated": request["request_id"] in request_ids,
                "replay_effect": (
                    "setup_qualified_still_blocked_ohlcv_does_not_supply_setup_labels_"
                    "trigger_invalidation_blocker_caution_macro_iv_event_headline_or_no_hindsight"
                ),
            }
        )
    return {
        "status": "REPLAYED_WITH_OHLCV_ONLY_EVIDENCE",
        "affected_candidate_count": len(affected),
        "affected_candidates": affected,
        "proof_accepted": False,
        "profitability_claimed": False,
        "promotion_decision_made": False,
    }


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
        "candidate_identifier": request["candidate_identifier"],
        "dataset": request["dataset"],
        "schema": request["schema"],
        "stype_in": request["stype_in"],
        "symbol": request["symbol"],
        "start_timestamp": request["start_timestamp"],
        "end_timestamp": request["end_timestamp"],
        "dbn_path": str(dbn_path.relative_to(REPO_ROOT)),
        "csv_path": str(csv_path.relative_to(REPO_ROOT)),
        "byte_count": dbn_path.stat().st_size if dbn_path.exists() else 0,
        "row_count": row_count,
        "sha256": _file_sha256(dbn_path) if dbn_path.exists() else None,
        "csv_sha256": _file_sha256(csv_path) if csv_path.exists() else None,
        "checked_cost": checked_cost,
        "actual_billed_cost": "NOT_AVAILABLE",
        "validation_problems": sorted(set(problems)),
    }


def _csv_scope_problems(request, csv_path):
    problems = []
    start = _parse_timestamp(request["start_timestamp"])
    end = _parse_timestamp(request["end_timestamp"])
    rows = _read_csv_dicts(csv_path)
    if not rows:
        return []
    present = set(rows[0])
    if not {"ts_event", "symbol"} <= present:
        return ["missing_required_ohlcv_scope_columns"]
    for row in rows:
        if row.get("symbol") != request["symbol"]:
            problems.append("contradictory_symbol")
            break
    for row in rows:
        ts_event = _parse_timestamp(row["ts_event"])
        if ts_event < start or ts_event >= end:
            problems.append("row_outside_authorized_window")
            break
    for row in rows:
        for field in ("open", "high", "low", "close", "volume"):
            if field in row and str(row[field]).strip() == "":
                problems.append(f"missing_{field}")
                break
    return sorted(set(problems))


def _read_csv_dicts(path):
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _csv_row_count(path):
    try:
        with Path(path).open(newline="", encoding="utf-8") as handle:
            reader = csv.reader(handle)
            next(reader, None)
            return sum(1 for _ in reader)
    except Exception:
        return -1


def _add_one_hour(value):
    return (_parse_timestamp(value) + timedelta(hours=1)).isoformat()


def _parse_timestamp(value):
    text = str(value)
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    return datetime.fromisoformat(text)


def _safe_request_stem(request):
    raw = "SAFE_FAST_DAY49_OHLCV_" + request["request_id"]
    return "".join(char if char.isalnum() or char in {"_", "-"} else "_" for char in raw)


def _file_sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _remove_existing_download_file(path):
    path = Path(path)
    if not path.exists():
        return
    if path.parent.resolve() != RAW_OUTPUT_DIR.resolve():
        raise RuntimeError(f"refusing to replace file outside raw output dir: {path}")
    if not path.name.startswith("SAFE_FAST_DAY49_OHLCV_"):
        raise RuntimeError(f"refusing to replace unexpected file: {path.name}")
    path.unlink()


def _utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _main():
    manifest = load_request_manifest()
    problems = validate_ohlcv_request_scope(manifest)
    if problems:
        for problem in problems:
            print(problem)
        raise SystemExit(1)
    cost = check_ohlcv_cost(manifest=manifest)
    if not cost["checked_total_at_or_below_limit"]:
        print("fresh checked total exceeds authorized limit")
        raise SystemExit(1)
    summary = download_ohlcv_requests(manifest=manifest, cost_check=cost)
    if summary["problems"]:
        for problem in summary["problems"]:
            print(problem)
        raise SystemExit(1)
    replay = affected_candidate_replay_summary(summary)
    print(
        "downloaded day49 OHLCV package: "
        f"{len(summary['downloaded_requests'])} requests, "
        f"fresh checked total ${summary['fresh_cost_check']['checked_total']}; "
        f"replayed {replay['affected_candidate_count']} affected candidates"
    )


if __name__ == "__main__":
    _main()
