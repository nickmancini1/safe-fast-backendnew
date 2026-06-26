import csv
import hashlib
import json
import os
import shutil
import sys
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
RESULT_VERSION = "day52_spy_670c_databento_download_manifest_v2"
FINAL_STATUSES = {"COMPLETED_REUSED", "COMPLETED_DOWNLOADED"}


class DownloadError(RuntimeError):
    def __init__(self, classification, detail):
        super().__init__(detail)
        self.classification = classification
        self.detail = detail


class EvidenceValidationError(DownloadError):
    pass


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
    git_ignore_checker=None,
):
    requests = _validated_requests(contract_resolution, cost_result)
    planned_files = planned_output_files(requests, output_root=output_root)
    planned_paths = [path for pair in planned_files.values() for path in pair.values()]
    temp_paths = [path.with_name(f"{path.name}.tmp") for path in planned_paths]
    if check_ignore:
        ignored = (git_ignore_checker or paths_are_git_ignored)(
            [*planned_paths, *temp_paths, manifest_path]
        )
        if not ignored:
            raise DownloadError(
                "OUTPUT_NOT_GIT_IGNORED",
                "planned raw output files, temporary files, or manifest are not Git-ignored",
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
    import subprocess

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


def inspect_existing_outputs(
    requests,
    *,
    output_root=OUTPUT_ROOT,
    dbn_parser=None,
):
    by_schema = {}
    paths_by_schema = planned_output_files(requests, output_root=output_root)
    for request in requests:
        schema = request["schema"]
        paths = paths_by_schema[schema]
        dbn_exists = paths["dbn"].exists()
        csv_exists = paths["csv"].exists()
        if not dbn_exists and not csv_exists:
            by_schema[schema] = {
                "schema": schema,
                "status": "MISSING",
                "request": deepcopy(request),
                "paths": _relative_paths(paths),
            }
            continue
        if dbn_exists != csv_exists:
            raise EvidenceValidationError(
                "EXISTING_PAIR_INCOMPLETE",
                f"{schema} has only one final output file; refusing automatic redownload",
            )
        summary = validate_evidence_pair(
            request,
            paths,
            dbn_parser=dbn_parser,
        )
        summary["status"] = "COMPLETED_REUSED"
        by_schema[schema] = summary
    return by_schema


def validate_evidence_pair(
    request,
    paths,
    *,
    dbn_parser=None,
):
    dbn_path = Path(paths["dbn"])
    csv_path = Path(paths["csv"])
    schema = request["schema"]
    if not dbn_path.exists() or not csv_path.exists():
        raise EvidenceValidationError(
            "PAIR_MISSING",
            f"{schema} DBN/CSV pair is not complete",
        )
    if dbn_path.stat().st_size <= 0 or csv_path.stat().st_size <= 0:
        raise EvidenceValidationError(
            "PAIR_EMPTY",
            f"{schema} DBN/CSV pair contains an empty file",
        )

    dbn_summary = _parse_dbn(dbn_path, dbn_parser=dbn_parser)
    csv_summary = _parse_csv(csv_path)
    problems = []
    if dbn_summary["schema"] != schema:
        problems.append(f"wrong_dbn_schema_{dbn_summary['schema']}")
    if dbn_summary["record_count"] != csv_summary["record_count"]:
        problems.append(
            f"record_count_mismatch_dbn_{dbn_summary['record_count']}_csv_{csv_summary['record_count']}"
        )
    for summary_name, summary in (("dbn", dbn_summary), ("csv", csv_summary)):
        if summary["record_count"] > 0:
            if summary.get("instrument_id") not in (None, INSTRUMENT_ID):
                problems.append(f"{summary_name}_wrong_instrument")
            if summary.get("publisher_id") not in (None, PUBLISHER_ID, "__MULTIPLE__"):
                problems.append(f"{summary_name}_wrong_publisher")
            if summary.get("symbol") not in (None, RAW_SYMBOL):
                problems.append(f"{summary_name}_wrong_symbol")
            if _timestamp_outside_request(summary.get("min_ts_event"), request):
                problems.append(f"{summary_name}_start_out_of_window")
            if _timestamp_outside_request(summary.get("max_ts_event"), request):
                problems.append(f"{summary_name}_end_out_of_window")
    if csv_summary["record_count"] > 0 and not (
        csv_summary.get("symbol") == RAW_SYMBOL
        or csv_summary.get("instrument_id") == INSTRUMENT_ID
    ):
        problems.append("csv_contract_identity_missing")
    if dbn_summary["record_count"] > 0 and dbn_summary.get("instrument_id") != INSTRUMENT_ID:
        problems.append("dbn_contract_identity_missing")
    if problems:
        raise EvidenceValidationError(
            "EXISTING_PAIR_INVALID",
            f"{schema}: {'; '.join(sorted(set(problems)))}",
        )

    return {
        "schema": schema,
        "dataset": request["dataset"],
        "stype_in": request["stype_in"],
        "symbols": request["symbols"],
        "start": request["start"],
        "end": request["end"],
        "dbn_path": _relative(dbn_path),
        "csv_path": _relative(csv_path),
        "dbn_bytes": dbn_path.stat().st_size,
        "csv_bytes": csv_path.stat().st_size,
        "dbn_sha256": _file_sha256(dbn_path),
        "csv_sha256": _file_sha256(csv_path),
        "parsed_record_count": csv_summary["record_count"],
        "empty": csv_summary["record_count"] == 0,
        "dbn_schema": str(dbn_summary["schema"]),
        "min_ts_event": _normalize_ts(csv_summary.get("min_ts_event") or dbn_summary.get("min_ts_event")),
        "max_ts_event": _normalize_ts(csv_summary.get("max_ts_event") or dbn_summary.get("max_ts_event")),
        "contract_identity_validated": True,
    }


def download_missing_schema(
    api_key,
    request,
    *,
    client,
    output_root=OUTPUT_ROOT,
    dbn_parser=None,
):
    if not api_key:
        raise DownloadError("AUTH_MISSING", f"{ENV_VAR_NAME} is not configured")
    final_paths = planned_output_files([request], output_root=output_root)[request["schema"]]
    _refuse_unintended_overwrite(final_paths)
    temp_paths = _temp_output_files(final_paths)
    _remove_stale_temp_files(temp_paths)
    for path in temp_paths.values():
        if path.exists():
            raise DownloadError(
                "TEMP_OUTPUT_OVERWRITE_REFUSED",
                f"temporary output already exists: {_relative(path)}",
            )
    try:
        store = client.timeseries.get_range(
            dataset=request["dataset"],
            schema=request["schema"],
            stype_in=request["stype_in"],
            symbols=request["symbols"],
            start=request["start"],
            end=request["end"],
            path=temp_paths["dbn"],
        )
        store.to_csv(temp_paths["csv"], schema=request["schema"])
        summary = validate_evidence_pair(
            request,
            temp_paths,
            dbn_parser=dbn_parser,
        )
        Path(output_root).mkdir(parents=True, exist_ok=True)
        _atomic_publish_pair(temp_paths, final_paths)
        final_summary = validate_evidence_pair(
            request,
            final_paths,
            dbn_parser=dbn_parser,
        )
        final_summary["status"] = "COMPLETED_DOWNLOADED"
        return final_summary
    except DownloadError:
        _remove_stale_temp_files(temp_paths)
        raise
    except KeyboardInterrupt:
        raise
    except Exception as exc:
        _remove_stale_temp_files(temp_paths)
        raise DownloadError("VENDOR_OR_NETWORK_FAILURE", f"{type(exc).__name__}: {exc}") from exc


def build_manifest(
    *,
    status,
    contract_resolution,
    cost_result,
    requests=None,
    schema_results=None,
    failure=None,
    current_schema=None,
    created_utc=None,
    manifest_path=MANIFEST_PATH,
    output_root=OUTPUT_ROOT,
):
    selected = _selected_contract_from_cost(cost_result)
    request_list = deepcopy(requests or cost_result.get("requests", []))
    result_map = schema_results or {}
    outputs = [
        _public_schema_result(result_map[schema])
        for schema in EXPECTED_SCHEMAS
        if schema in result_map and result_map[schema].get("status") in FINAL_STATUSES
    ]
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
        "exact_requests": request_list,
        "output_root": _relative(output_root),
        "manifest_path": _relative(manifest_path),
        "download_performed": any(
            item.get("status") == "COMPLETED_DOWNLOADED" for item in result_map.values()
        ),
        "current_schema": current_schema,
        "completed_or_reused_schemas": [
            schema
            for schema in EXPECTED_SCHEMAS
            if result_map.get(schema, {}).get("status") in FINAL_STATUSES
        ],
        "remaining_schemas": [
            schema
            for schema in EXPECTED_SCHEMAS
            if result_map.get(schema, {}).get("status") not in FINAL_STATUSES
        ],
        "output_files": outputs,
        "schema_status": _schema_status(result_map, request_list),
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
    temp_path = path.with_name(f"{path.name}.tmp")
    temp_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temp_path.replace(path)
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
    dbn_parser=None,
    output_stream=None,
    write_failure_manifest=True,
):
    stream = output_stream or sys.stdout
    inputs = load_inputs(
        contract_resolution_path=contract_resolution_path,
        cost_result_path=cost_result_path,
    )
    requests = inputs["cost_result"].get("requests", [])
    schema_results = {}
    current_schema = None
    try:
        requests = validate_preflight(
            contract_resolution=inputs["contract_resolution"],
            cost_result=inputs["cost_result"],
            output_root=output_root,
            manifest_path=manifest_path,
            git_ignore_checker=git_ignore_checker,
        )
        Path(output_root).mkdir(parents=True, exist_ok=True)
        schema_results = inspect_existing_outputs(
            requests,
            output_root=output_root,
            dbn_parser=dbn_parser,
        )
        _write_checkpoint(
            "IN_PROGRESS",
            inputs,
            requests,
            schema_results,
            manifest_path,
            output_root,
            current_schema=None,
        )
        for request in requests:
            schema = request["schema"]
            current_schema = schema
            if schema_results[schema]["status"] == "COMPLETED_REUSED":
                _emit(stream, f"SCHEMA_REUSED={schema}")
                _write_checkpoint(
                    "IN_PROGRESS",
                    inputs,
                    requests,
                    schema_results,
                    manifest_path,
                    output_root,
                    current_schema=current_schema,
                )
                continue
            if schema_results[schema]["status"] != "MISSING":
                raise DownloadError(
                    "UNEXPECTED_SCHEMA_STATE",
                    f"{schema} state is {schema_results[schema]['status']}",
                )
            key = api_key if api_key is not None else os.environ.get(ENV_VAR_NAME)
            if not key:
                raise DownloadError("AUTH_MISSING", f"{ENV_VAR_NAME} is not configured")
            client = (
                client_factory(key)
                if client_factory is not None
                else _databento_client(key)
            )
            _emit(stream, _freeze_guidance(schema))
            _emit(stream, f"SCHEMA_START={schema}")
            downloaded = download_missing_schema(
                key,
                request,
                client=client,
                output_root=output_root,
                dbn_parser=dbn_parser,
            )
            schema_results[schema] = downloaded
            _emit(stream, f"SCHEMA_COMPLETE={schema}")
            _write_checkpoint(
                "IN_PROGRESS",
                inputs,
                requests,
                schema_results,
                manifest_path,
                output_root,
                current_schema=current_schema,
            )
        status = "SUCCESS" if _all_final(schema_results) else "FAILURE"
        failure = None if status == "SUCCESS" else {
            "classification": "INCOMPLETE_SCHEMA_SET",
            "detail": "not all four schemas are completed or reused",
        }
        manifest = build_manifest(
            status=status,
            contract_resolution=inputs["contract_resolution"],
            cost_result=inputs["cost_result"],
            requests=requests,
            schema_results=schema_results,
            failure=failure,
            current_schema=None,
            manifest_path=manifest_path,
            output_root=output_root,
        )
        write_manifest(manifest, manifest_path=manifest_path)
        return (0 if status == "SUCCESS" else 1), manifest
    except KeyboardInterrupt:
        manifest = build_manifest(
            status="INTERRUPTED",
            contract_resolution=inputs["contract_resolution"],
            cost_result=inputs["cost_result"],
            requests=requests,
            schema_results=schema_results,
            failure={"classification": "KEYBOARD_INTERRUPT", "detail": "operator pressed Ctrl+C"},
            current_schema=current_schema,
            manifest_path=manifest_path,
            output_root=output_root,
        )
        if write_failure_manifest:
            _try_write_manifest(manifest, manifest_path)
        return 130, manifest
    except DownloadError as exc:
        failure = {"classification": exc.classification, "detail": exc.detail}
        manifest = build_manifest(
            status="FAILURE",
            contract_resolution=inputs["contract_resolution"],
            cost_result=inputs["cost_result"],
            requests=requests,
            schema_results=schema_results,
            failure=failure,
            current_schema=current_schema,
            manifest_path=manifest_path,
            output_root=output_root,
        )
        if write_failure_manifest:
            _try_write_manifest(manifest, manifest_path)
        return 1, manifest


def main():
    exit_code, manifest = run_download()
    print(f"wrote {MANIFEST_PATH}", flush=True)
    print(f"status {manifest['status']}", flush=True)
    if manifest["status"] != "SUCCESS":
        failure = manifest.get("vendor_failure") or {}
        print(f"failure {failure.get('classification')}: {failure.get('detail')}", flush=True)
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


def _parse_dbn(path, *, dbn_parser=None):
    if dbn_parser is not None:
        try:
            return dbn_parser(path)
        except EvidenceValidationError:
            raise
        except Exception as exc:
            raise EvidenceValidationError(
                "DBN_PARSE_FAILED",
                f"{Path(path).name}: {type(exc).__name__}: {exc}",
            ) from exc
    try:
        import databento as db

        store = db.DBNStore.from_file(path)
        record_count = 0
        instrument_ids = set()
        publisher_ids = set()
        min_ts = None
        max_ts = None
        for record in store:
            record_count += 1
            instrument_id = getattr(record, "instrument_id", None)
            publisher_id = getattr(record, "publisher_id", None)
            if instrument_id is not None:
                instrument_ids.add(int(instrument_id))
            if publisher_id is not None:
                publisher_ids.add(int(publisher_id))
            pretty_ts = getattr(record, "pretty_ts_event", None)
            if pretty_ts is None and hasattr(record, "ts_event"):
                pretty_ts = _ns_to_iso_utc(int(record.ts_event))
            min_ts, max_ts = _min_max_ts(min_ts, max_ts, _normalize_ts(pretty_ts))
        return {
            "schema": str(store.schema),
            "record_count": record_count,
            "instrument_id": _only_value(instrument_ids),
            "publisher_id": _only_value(publisher_ids),
            "symbol": None,
            "min_ts_event": min_ts,
            "max_ts_event": max_ts,
        }
    except Exception as exc:
        raise EvidenceValidationError(
            "DBN_PARSE_FAILED",
            f"{Path(path).name}: {type(exc).__name__}: {exc}",
        ) from exc


def _parse_csv(path):
    try:
        with Path(path).open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                raise ValueError("missing header")
            record_count = 0
            symbols = set()
            instrument_ids = set()
            publisher_ids = set()
            min_ts = None
            max_ts = None
            for row in reader:
                record_count += 1
                if "symbol" in row and row["symbol"]:
                    symbols.add(row["symbol"])
                if "instrument_id" in row and row["instrument_id"]:
                    instrument_ids.add(int(row["instrument_id"]))
                if "publisher_id" in row and row["publisher_id"]:
                    publisher_ids.add(int(row["publisher_id"]))
                ts_event = row.get("ts_event")
                if ts_event:
                    _iso_to_ns(ts_event)
                    min_ts, max_ts = _min_max_ts(min_ts, max_ts, ts_event)
            return {
                "record_count": record_count,
                "symbol": _only_value(symbols),
                "instrument_id": _only_value(instrument_ids),
                "publisher_id": _only_value(publisher_ids),
                "min_ts_event": min_ts,
                "max_ts_event": max_ts,
            }
    except Exception as exc:
        raise EvidenceValidationError(
            "CSV_PARSE_FAILED",
            f"{Path(path).name}: {type(exc).__name__}: {exc}",
        ) from exc


def _schema_status(schema_results, requests):
    by_request = {request["schema"]: request for request in requests}
    result = {}
    for schema in EXPECTED_SCHEMAS:
        row = schema_results.get(schema) or {"status": "MISSING"}
        result[schema] = {
            "status": row["status"],
            "parsed_record_count": row.get("parsed_record_count"),
            "request": deepcopy(by_request.get(schema)),
        }
    return result


def _public_schema_result(row):
    public = deepcopy(row)
    public.pop("request", None)
    public.pop("paths", None)
    return public


def _write_checkpoint(status, inputs, requests, schema_results, manifest_path, output_root, *, current_schema):
    manifest = build_manifest(
        status=status,
        contract_resolution=inputs["contract_resolution"],
        cost_result=inputs["cost_result"],
        requests=requests,
        schema_results=schema_results,
        current_schema=current_schema,
        manifest_path=manifest_path,
        output_root=output_root,
    )
    write_manifest(manifest, manifest_path=manifest_path)


def _try_write_manifest(manifest, manifest_path):
    try:
        write_manifest(manifest, manifest_path=manifest_path)
    except Exception:
        pass


def _all_final(schema_results):
    return all(schema_results.get(schema, {}).get("status") in FINAL_STATUSES for schema in EXPECTED_SCHEMAS)


def _databento_client(api_key):
    import databento as db

    return db.Historical(key=api_key)


def _selected_contract_from_cost(cost_result):
    return cost_result.get("selected_contract") or {}


def _refuse_unintended_overwrite(paths):
    existing = [name for name, path in paths.items() if Path(path).exists()]
    if existing:
        raise DownloadError(
            "OUTPUT_OVERWRITE_REFUSED",
            f"refusing to overwrite existing final output files: {', '.join(existing)}",
        )


def _temp_output_files(final_paths):
    pid = os.getpid()
    return {
        key: Path(path).with_name(f"{Path(path).name}.tmp.{pid}")
        for key, path in final_paths.items()
    }


def _remove_stale_temp_files(paths):
    for path in paths.values():
        if Path(path).exists():
            Path(path).unlink()


def _atomic_publish_pair(temp_paths, final_paths):
    for final_path in final_paths.values():
        if Path(final_path).exists():
            raise DownloadError(
                "OUTPUT_OVERWRITE_REFUSED",
                f"final output appeared during download: {_relative(final_path)}",
            )
    shutil.move(str(temp_paths["dbn"]), str(final_paths["dbn"]))
    try:
        shutil.move(str(temp_paths["csv"]), str(final_paths["csv"]))
    except Exception:
        if Path(final_paths["dbn"]).exists() and not Path(final_paths["csv"]).exists():
            Path(final_paths["dbn"]).unlink()
        raise


def _freeze_guidance(schema):
    return (
        f"REQUESTING_SCHEMA={schema}; PowerShell may be quiet while Databento responds. "
        "If it appears frozen and is not requesting hidden input, press Ctrl+C once. "
        "Do not rerun before inspecting the checkpoint manifest, partial files, output, and Git status."
    )


def _emit(stream, line):
    print(line, file=stream, flush=True)
    if hasattr(stream, "flush"):
        stream.flush()


def _relative_paths(paths):
    return {key: _relative(path) for key, path in paths.items()}


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


def _min_max_ts(min_ts, max_ts, candidate):
    if not candidate:
        return min_ts, max_ts
    if min_ts is None or _iso_to_ns(candidate) < _iso_to_ns(min_ts):
        min_ts = candidate
    if max_ts is None or _iso_to_ns(candidate) > _iso_to_ns(max_ts):
        max_ts = candidate
    return min_ts, max_ts


def _timestamp_outside_request(ts_event, request):
    if ts_event is None:
        return False
    ts_ns = _iso_to_ns(ts_event)
    start_ns = _iso_to_ns(request["start"])
    end_ns = _iso_to_ns(request["end"])
    return ts_ns < start_ns or ts_ns >= end_ns


def _iso_to_ns(value):
    value = _normalize_ts(value)
    if not isinstance(value, str) or not value.endswith("Z") or "T" not in value:
        raise ValueError(f"unsupported timestamp: {value!r}")
    body = value[:-1]
    date_part, time_part = body.split("T", 1)
    if "." in time_part:
        clock, fraction = time_part.split(".", 1)
    else:
        clock, fraction = time_part, ""
    dt = datetime.fromisoformat(f"{date_part}T{clock}+00:00")
    fraction = (fraction + "000000000")[:9]
    return int(dt.timestamp()) * 1_000_000_000 + int(fraction)


def _normalize_ts(value):
    if value is None:
        return None
    if not isinstance(value, str) and hasattr(value, "isoformat"):
        value = value.isoformat()
    if isinstance(value, str) and value.endswith("+00:00"):
        value = value[:-6] + "Z"
    if isinstance(value, str) and value.endswith("+0000"):
        value = value[:-5] + "Z"
    if isinstance(value, str) and " " in value and "T" not in value:
        value = value.replace(" ", "T", 1)
    return value


def _ns_to_iso_utc(value):
    seconds, nanos = divmod(value, 1_000_000_000)
    dt = datetime.fromtimestamp(seconds, tz=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%S") + f".{nanos:09d}Z"


def _only_value(values):
    if not values:
        return None
    if len(values) == 1:
        return next(iter(values))
    return "__MULTIPLE__"


if __name__ == "__main__":
    raise SystemExit(main())
