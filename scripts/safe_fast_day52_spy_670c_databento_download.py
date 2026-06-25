import csv
import hashlib
import json
import os
import subprocess
from copy import deepcopy
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_RESOLUTION_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day52_spy_opra_contract_resolution.json"
)
COST_RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day52_existing_setup_databento_cost_request_operator_output.json"
)
OUTPUT_ROOT = (
    REPO_ROOT
    / "historical_signal_replay"
    / "source_data"
    / "external_option_data_drop"
    / "day52_spy_670c"
)
MANIFEST_PATH = OUTPUT_ROOT / "day52_spy_670c_databento_download_manifest.json"

ENV_VAR_NAME = "SAFE_FAST_DB_AUTH"
DATASET = "OPRA.PILLAR"
RAW_SYMBOL = "SPY   260330C00670000"
INSTRUMENT_ID = 1241515301
PUBLISHER_ID = 30
EXPIRATION = "2026-03-30"
STRIKE = "670"
SIDE = "call"
APPROVED_COST_CEILING = Decimal("0.01")
EXPECTED_SCHEMAS = ("cmbp-1", "tcbbo", "trades", "statistics")
RESULT_VERSION = "day52_spy_670c_databento_download_manifest_v1"


class DownloadError(RuntimeError):
    def __init__(self, classification, detail):
        super().__init__(detail)
        self.classification = classification
        self.detail = detail


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_inputs(
    *,
    contract_resolution_path=CONTRACT_RESOLUTION_PATH,
    cost_result_path=COST_RESULT_PATH,
):
    return {
        "contract_resolution": load_json(contract_resolution_path),
        "cost_result": load_json(cost_result_path),
    }


def validate_preflight(
    *,
    contract_resolution,
    cost_result,
    output_root=OUTPUT_ROOT,
    manifest_path=MANIFEST_PATH,
    check_ignore=True,
    path_exists=None,
    git_ignore_checker=None,
):
    requests = _validated_requests(contract_resolution, cost_result)
    planned_files = planned_output_files(requests, output_root=output_root)
    planned_paths = [
        path
        for pair in planned_files.values()
        for path in pair.values()
    ]
    if check_ignore:
        ignored = (git_ignore_checker or paths_are_git_ignored)(
            [*planned_paths, manifest_path]
        )
        if not ignored:
            raise DownloadError(
                "OUTPUT_NOT_GIT_IGNORED",
                "planned raw output files or manifest are not Git-ignored",
            )
    exists = path_exists or (lambda path: Path(path).exists())
    existing = [
        _relative(path)
        for pair in planned_files.values()
        for path in pair.values()
        if exists(path)
    ]
    if exists(manifest_path):
        existing.append(_relative(manifest_path))
    if existing:
        raise DownloadError(
            "OUTPUT_OVERWRITE_REFUSED",
            f"refusing to overwrite existing output: {', '.join(sorted(existing))}",
        )
    return requests


def planned_output_files(requests, *, output_root=OUTPUT_ROOT):
    return {
        request["schema"]: {
            "dbn": Path(output_root) / f"day52_spy_670c_{request['schema']}.dbn.zst",
            "csv": Path(output_root) / f"day52_spy_670c_{request['schema']}.csv",
        }
        for request in requests
    }


def paths_are_git_ignored(paths):
    for path in paths:
        completed = subprocess.run(
            ["git", "check-ignore", "--quiet", "--", _relative(path)],
            cwd=REPO_ROOT,
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if completed.returncode != 0:
            return False
    return True


def download_approved_requests(
    api_key,
    requests,
    *,
    client_factory=None,
    output_root=OUTPUT_ROOT,
):
    if not api_key:
        raise DownloadError("AUTH_MISSING", f"{ENV_VAR_NAME} is not configured")
    try:
        client = (
            client_factory(api_key)
            if client_factory is not None
            else _databento_client(api_key)
        )
        Path(output_root).mkdir(parents=True, exist_ok=True)
        outputs = []
        for request in requests:
            paths = planned_output_files([request], output_root=output_root)[request["schema"]]
            store = client.timeseries.get_range(
                dataset=request["dataset"],
                schema=request["schema"],
                stype_in=request["stype_in"],
                symbols=request["symbols"],
                start=request["start"],
                end=request["end"],
                path=paths["dbn"],
            )
            store.to_csv(paths["csv"], schema=request["schema"])
            outputs.append(_downloaded_file_summary(request, paths))
        return outputs
    except DownloadError:
        raise
    except Exception as exc:
        raise DownloadError("VENDOR_OR_NETWORK_FAILURE", f"{type(exc).__name__}: {exc}") from exc


def build_manifest(
    *,
    status,
    contract_resolution,
    cost_result,
    requests=None,
    outputs=None,
    failure=None,
    created_utc=None,
):
    selected = _selected_contract_from_cost(cost_result)
    manifest = {
        "result_version": RESULT_VERSION,
        "status": status,
        "created_utc": created_utc or _utc_now(),
        "credential_env_var": ENV_VAR_NAME,
        "credential_value_printed": False,
        "credential_value_persisted": False,
        "dataset": DATASET,
        "contract_identity": {
            "raw_symbol": RAW_SYMBOL,
            "instrument_id": INSTRUMENT_ID,
            "publisher_id": PUBLISHER_ID,
            "expiration": EXPIRATION,
            "strike": STRIKE,
            "side": SIDE,
            "cost_result_selected_contract": selected,
            "contract_resolution_status": contract_resolution.get("status"),
        },
        "approved_cost_ceiling": str(APPROVED_COST_CEILING),
        "checked_grouped_cost": cost_result.get("grouped_cost"),
        "exact_requests": deepcopy(requests or cost_result.get("requests", [])),
        "output_root": _relative(OUTPUT_ROOT),
        "manifest_path": _relative(MANIFEST_PATH),
        "download_performed": status == "SUCCESS",
        "output_files": outputs or [],
        "schema_status": _schema_status(outputs or [], requests or []),
        "vendor_failure": failure,
        "setup_entry_exit_pnl_decision_made": False,
        "proof": "NO",
        "profitability_proof": "NO",
        "paper_live_eligibility": "NO",
    }
    return manifest


def write_manifest(manifest, *, manifest_path=MANIFEST_PATH):
    path = Path(manifest_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def run_download(
    *,
    api_key=None,
    contract_resolution_path=CONTRACT_RESOLUTION_PATH,
    cost_result_path=COST_RESULT_PATH,
    output_root=OUTPUT_ROOT,
    manifest_path=MANIFEST_PATH,
    client_factory=None,
    git_ignore_checker=None,
    path_exists=None,
    write_failure_manifest=True,
):
    inputs = load_inputs(
        contract_resolution_path=contract_resolution_path,
        cost_result_path=cost_result_path,
    )
    try:
        requests = validate_preflight(
            contract_resolution=inputs["contract_resolution"],
            cost_result=inputs["cost_result"],
            output_root=output_root,
            manifest_path=manifest_path,
            git_ignore_checker=git_ignore_checker,
            path_exists=path_exists,
        )
        key = api_key if api_key is not None else os.environ.get(ENV_VAR_NAME)
        outputs = download_approved_requests(
            key,
            requests,
            client_factory=client_factory,
            output_root=output_root,
        )
        manifest = build_manifest(
            status="SUCCESS",
            contract_resolution=inputs["contract_resolution"],
            cost_result=inputs["cost_result"],
            requests=requests,
            outputs=outputs,
        )
        write_manifest(manifest, manifest_path=manifest_path)
        return 0, manifest
    except DownloadError as exc:
        failure = {"classification": exc.classification, "detail": exc.detail}
        manifest = build_manifest(
            status="FAILURE",
            contract_resolution=inputs["contract_resolution"],
            cost_result=inputs["cost_result"],
            requests=inputs["cost_result"].get("requests", []),
            failure=failure,
        )
        if write_failure_manifest:
            try:
                write_manifest(manifest, manifest_path=manifest_path)
            except Exception:
                pass
        return 1, manifest


def main():
    exit_code, manifest = run_download()
    print(f"wrote {MANIFEST_PATH}")
    print(f"status {manifest['status']}")
    if manifest["status"] != "SUCCESS":
        failure = manifest.get("vendor_failure") or {}
        print(f"failure {failure.get('classification')}: {failure.get('detail')}")
    return exit_code


def _validated_requests(contract_resolution, cost_result):
    problems = []
    if cost_result.get("status") != "SUCCESS":
        problems.append("cost_result_status_not_SUCCESS")
    if cost_result.get("cost_only") is not True:
        problems.append("cost_result_not_cost_only")
    if cost_result.get("download_performed") is not False:
        problems.append("cost_result_download_already_performed")
    try:
        if Decimal(str(cost_result.get("grouped_cost"))) > APPROVED_COST_CEILING:
            problems.append("grouped_cost_exceeds_approved_ceiling")
    except (InvalidOperation, TypeError):
        problems.append("grouped_cost_not_decimal")

    requests = deepcopy(cost_result.get("requests") or [])
    schemas = tuple(request.get("schema") for request in requests)
    if schemas != EXPECTED_SCHEMAS:
        problems.append(f"unexpected_schema_set_or_order_{schemas}")
    if "definition" in schemas:
        problems.append("definition_schema_forbidden")
    if len(requests) != len(EXPECTED_SCHEMAS):
        problems.append("unexpected_request_count")
    for request in requests:
        if request.get("dataset") != DATASET:
            problems.append("unexpected_dataset")
        if request.get("stype_in") != "raw_symbol":
            problems.append("unexpected_stype_in")
        if request.get("symbols") != RAW_SYMBOL:
            problems.append("unexpected_raw_symbol")

    schema_costs = cost_result.get("schema_costs") or []
    if tuple(row.get("schema") for row in schema_costs) != EXPECTED_SCHEMAS:
        problems.append("schema_costs_do_not_match_expected_schemas")
    for row in schema_costs:
        if row.get("symbols") != RAW_SYMBOL:
            problems.append("schema_costs_unexpected_raw_symbol")
        if row.get("schema") == "definition":
            problems.append("schema_costs_definition_forbidden")

    selected_resolution = contract_resolution.get("selected_contract") or {}
    selected_cost = _selected_contract_from_cost(cost_result)
    if contract_resolution.get("status") != "CONTRACT_RESOLVED_FROM_EXISTING_LOCAL_DEFINITION_EVIDENCE":
        problems.append("contract_resolution_status_unexpected")
    if contract_resolution.get("no_second_definition_download") is not True:
        problems.append("contract_resolution_allows_second_definition_download")
    if selected_resolution.get("raw_symbol") != RAW_SYMBOL:
        problems.append("contract_resolution_raw_symbol_mismatch")
    if selected_resolution.get("instrument_id") != INSTRUMENT_ID:
        problems.append("contract_resolution_instrument_mismatch")
    if selected_resolution.get("publisher_id") != PUBLISHER_ID:
        problems.append("contract_resolution_publisher_mismatch")
    if str(selected_resolution.get("expiration")) != EXPIRATION:
        problems.append("contract_resolution_expiration_mismatch")
    if Decimal(str(selected_resolution.get("strike"))) != Decimal(STRIKE):
        problems.append("contract_resolution_strike_mismatch")
    if selected_resolution.get("side") != SIDE:
        problems.append("contract_resolution_side_mismatch")

    if selected_cost.get("vendor_symbol") != RAW_SYMBOL:
        problems.append("cost_result_raw_symbol_mismatch")
    if selected_cost.get("instrument_id") != INSTRUMENT_ID:
        problems.append("cost_result_instrument_mismatch")
    if selected_cost.get("publisher_id") != PUBLISHER_ID:
        problems.append("cost_result_publisher_mismatch")
    if selected_cost.get("expiration") != EXPIRATION:
        problems.append("cost_result_expiration_mismatch")
    if str(selected_cost.get("strike")) != STRIKE:
        problems.append("cost_result_strike_mismatch")
    if selected_cost.get("call_or_put") != "C":
        problems.append("cost_result_side_mismatch")

    rejected = cost_result.get("rejected_contract") or {}
    if rejected.get("vendor_symbol") == RAW_SYMBOL:
        problems.append("rejected_contract_matches_selected_symbol")
    if rejected.get("reason") != "CONTRACT_UNLISTED":
        problems.append("rejected_669c_reason_missing")

    if problems:
        raise DownloadError("PREFLIGHT_FAILED", "; ".join(sorted(set(problems))))
    return requests


def _downloaded_file_summary(request, paths):
    dbn = Path(paths["dbn"])
    csv_path = Path(paths["csv"])
    record_count = _csv_row_count(csv_path)
    problems = []
    if not dbn.exists() or dbn.stat().st_size <= 0:
        problems.append("missing_or_empty_dbn")
    if not csv_path.exists():
        problems.append("missing_csv")
    if record_count < 0:
        problems.append("csv_parse_failed")
    if problems:
        raise DownloadError("PARSE_OR_OUTPUT_FAILURE", "; ".join(problems))
    return {
        "schema": request["schema"],
        "dataset": request["dataset"],
        "stype_in": request["stype_in"],
        "symbols": request["symbols"],
        "start": request["start"],
        "end": request["end"],
        "dbn_path": _relative(dbn),
        "csv_path": _relative(csv_path),
        "dbn_bytes": dbn.stat().st_size,
        "csv_bytes": csv_path.stat().st_size,
        "dbn_sha256": _file_sha256(dbn),
        "csv_sha256": _file_sha256(csv_path),
        "parsed_record_count": record_count,
        "empty": record_count == 0,
    }


def _schema_status(outputs, requests):
    by_schema = {output["schema"]: output for output in outputs}
    schemas = [request["schema"] for request in requests] or list(EXPECTED_SCHEMAS)
    return {
        schema: {
            "status": (
                "nonempty"
                if schema in by_schema and by_schema[schema]["parsed_record_count"] > 0
                else "empty"
                if schema in by_schema
                else "not_downloaded"
            ),
            "parsed_record_count": (
                by_schema[schema]["parsed_record_count"] if schema in by_schema else None
            ),
        }
        for schema in schemas
    }


def _databento_client(api_key):
    import databento as db

    return db.Historical(key=api_key)


def _selected_contract_from_cost(cost_result):
    return cost_result.get("selected_contract") or {}


def _csv_row_count(path):
    try:
        with Path(path).open(newline="", encoding="utf-8") as handle:
            reader = csv.reader(handle)
            next(reader, None)
            return sum(1 for _ in reader)
    except Exception:
        return -1


def _file_sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _relative(path):
    resolved = Path(path).resolve()
    try:
        return str(resolved.relative_to(REPO_ROOT)).replace("\\", "/")
    except ValueError:
        return str(resolved).replace("\\", "/")


def _utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
