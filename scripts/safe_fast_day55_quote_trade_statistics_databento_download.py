import csv
import gc
import hashlib
import json
import os
import sys
from copy import deepcopy
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_REQUEST_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day55_quote_trade_statistics_cost_request_for_selected_contracts.json"
)
COST_CHECK_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day55_quote_trade_statistics_cost_check_for_selected_contracts.json"
)
OUTPUT_ROOT = (
    REPO_ROOT
    / "historical_signal_replay"
    / "source_data"
    / "external_option_data_drop"
    / "day55_quote_trade_statistics_selected_contracts"
)
MANIFEST_PATH = OUTPUT_ROOT / "day55_quote_trade_statistics_download_manifest.json"

ENV_VAR_NAME = "SAFE_FAST_DB_AUTH"
DATASET = "OPRA.PILLAR"
APPROVED_GROUPED_COST = Decimal("0.054846107958")
EXPECTED_REQUEST_COUNT = 32
REQUIRED_SCHEMAS = {"cmbp-1", "tcbbo", "trades", "statistics"}
RESULT_VERSION = "safe_fast_day55_quote_trade_statistics_download_manifest_v1"
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


def load_inputs(*, source_request_path=SOURCE_REQUEST_PATH, cost_check_path=COST_CHECK_PATH):
    return {
        "source_request": load_json(source_request_path),
        "cost_check": load_json(cost_check_path),
    }


def vendor_request(request):
    return {
        "dataset": request.get("dataset"),
        "end": request.get("end"),
        "schema": request.get("schema"),
        "start": request.get("start"),
        "stype_in": request.get("stype_in"),
        "symbols": request.get("symbols"),
    }


def validate_preflight(*, source_request, cost_check):
    problems = []
    if source_request.get("decision") != "QUOTE_TRADE_STATISTICS_COST_REQUEST_READY_FOR_OPERATOR_REVIEW":
        problems.append("source_request_decision_unexpected")
    if source_request.get("download_performed") is not False:
        problems.append("source_request_download_already_performed")
    if source_request.get("vendor_call_performed") is not False:
        problems.append("source_request_vendor_call_already_performed")
    if source_request.get("profitability_proof") != "NO":
        problems.append("source_request_profitability_proof_changed")
    if source_request.get("paper_live_eligibility") != "NO":
        problems.append("source_request_paper_live_eligibility_changed")

    if cost_check.get("status") != "SUCCESS":
        problems.append("cost_check_status_not_SUCCESS")
    if cost_check.get("cost_only") is not True:
        problems.append("cost_check_not_cost_only")
    if cost_check.get("download_performed") is not False:
        problems.append("cost_check_download_already_performed")
    if cost_check.get("vendor_metadata_call_performed") is not True:
        problems.append("cost_check_vendor_metadata_missing")
    if cost_check.get("profitability_proof") != "NO":
        problems.append("cost_check_profitability_proof_changed")
    if cost_check.get("paper_live_eligibility") != "NO":
        problems.append("cost_check_paper_live_eligibility_changed")
    if cost_check.get("gross_pnl") is not None or cost_check.get("net_pnl") is not None:
        problems.append("cost_check_pnl_invented")

    try:
        if Decimal(str(cost_check.get("grouped_cost"))) != APPROVED_GROUPED_COST:
            problems.append("grouped_cost_not_operator_approved_amount")
    except (InvalidOperation, TypeError):
        problems.append("grouped_cost_not_decimal")

    source_requests = deepcopy(source_request.get("requests") or [])
    cost_requests = deepcopy(cost_check.get("requests") or [])
    expected_vendor_requests = [vendor_request(request) for request in source_requests]
    if len(source_requests) != EXPECTED_REQUEST_COUNT:
        problems.append("source_request_count_not_32")
    if len(cost_requests) != EXPECTED_REQUEST_COUNT:
        problems.append("cost_check_request_count_not_32")
    if cost_check.get("request_count") != EXPECTED_REQUEST_COUNT:
        problems.append("cost_check_request_count_field_not_32")
    if cost_requests != expected_vendor_requests:
        problems.append("cost_check_requests_do_not_match_source_request")
    if len({request_key(request) for request in cost_requests}) != EXPECTED_REQUEST_COUNT:
        problems.append("request_keys_not_unique")

    schemas = {request.get("schema") for request in cost_requests}
    if schemas != REQUIRED_SCHEMAS:
        problems.append("request_schema_set_mismatch")
    if "definition" in schemas or "definition" in set(cost_check.get("forbidden_schemas", [])) - {"definition"}:
        problems.append("definition_schema_forbidden")
    if "definition" not in set(cost_check.get("forbidden_schemas", [])):
        problems.append("definition_not_marked_forbidden")

    schema_costs = cost_check.get("schema_costs") or []
    if [vendor_request(row) for row in schema_costs] != cost_requests:
        problems.append("schema_costs_do_not_match_requests")

    for index, request in enumerate(cost_requests):
        if sorted(request.keys()) != ["dataset", "end", "schema", "start", "stype_in", "symbols"]:
            problems.append("cost_request_contains_non_vendor_fields")
        if request.get("dataset") != DATASET:
            problems.append("request_dataset_mismatch")
        if request.get("schema") not in REQUIRED_SCHEMAS:
            problems.append(f"unexpected_schema_{request.get('schema')}")
        if request.get("stype_in") != "raw_symbol":
            problems.append("request_stype_in_not_raw_symbol")
        if not request.get("symbols") or not request.get("start") or not request.get("end"):
            problems.append(f"request_{index}_missing_symbol_or_window")

    for request in source_requests:
        if not request.get("candidate_ids"):
            problems.append("source_request_candidate_ids_missing")
        if request.get("leg") not in {"long", "short"}:
            problems.append("source_request_leg_missing")
        identities = request.get("contract_identities") or []
        if not identities:
            problems.append("source_request_contract_identity_missing")
        for identity in identities:
            if identity.get("raw_symbol") != request.get("symbols"):
                problems.append("identity_raw_symbol_mismatch")
            if identity.get("profitability_proof") != "NO":
                problems.append("identity_profitability_proof_changed")
            if identity.get("paper_live_eligibility") != "NO":
                problems.append("identity_paper_live_eligibility_changed")
            if identity.get("entry_status") != "NOT_EVALUATED":
                problems.append("identity_entry_status_changed")
            if identity.get("exit_status") != "NOT_EVALUATED":
                problems.append("identity_exit_status_changed")
            if identity.get("gross_pnl") is not None or identity.get("net_pnl") is not None:
                problems.append("identity_pnl_invented")

    if problems:
        raise DownloadError("PREFLIGHT_FAILED", "; ".join(sorted(set(problems))))
    return source_requests, cost_requests


def request_key(request):
    return (
        request.get("dataset"),
        request.get("schema"),
        request.get("stype_in"),
        request.get("symbols"),
        request.get("start"),
        request.get("end"),
    )


def request_id(index, request):
    symbol = "".join(str(request["symbols"]).split()).lower()
    start = _compact_ts(request["start"])
    end = _compact_ts(request["end"])
    return f"{index + 1:02d}_{symbol}_{request['schema'].replace('-', '')}_{start}_{end}"


def planned_output_files(cost_requests, *, output_root=OUTPUT_ROOT):
    result = {}
    for index, request in enumerate(cost_requests):
        rid = request_id(index, request)
        result[rid] = {
            "dbn": Path(output_root) / f"{rid}.dbn.zst",
            "csv": Path(output_root) / f"{rid}.csv",
        }
    return result


def inspect_existing_outputs(source_requests, cost_requests, *, output_root=OUTPUT_ROOT, dbn_parser=None):
    by_id = {}
    paths_by_id = planned_output_files(cost_requests, output_root=output_root)
    for index, request in enumerate(cost_requests):
        rid = request_id(index, request)
        paths = paths_by_id[rid]
        dbn_exists = paths["dbn"].exists()
        csv_exists = paths["csv"].exists()
        if not dbn_exists and not csv_exists:
            by_id[rid] = {
                "request_id": rid,
                "request_index": index,
                "status": "MISSING",
                "request": deepcopy(request),
                "source_request": deepcopy(source_requests[index]),
                "paths": _relative_paths(paths),
            }
            continue
        if dbn_exists != csv_exists:
            recovered = _recover_interrupted_publish(
                source_requests[index],
                request,
                paths,
                request_id=rid,
                request_index=index,
                dbn_parser=dbn_parser,
            )
            if recovered is not None:
                recovered["status"] = "COMPLETED_REUSED"
                by_id[rid] = recovered
                continue
            raise EvidenceValidationError(
                "EXISTING_PAIR_INCOMPLETE",
                f"{rid} has only one final output file; refusing automatic redownload",
            )
        summary = validate_evidence_pair(
            source_requests[index],
            request,
            paths,
            request_id=rid,
            request_index=index,
            dbn_parser=dbn_parser,
        )
        summary["status"] = "COMPLETED_REUSED"
        by_id[rid] = summary
    return by_id


def _recover_interrupted_publish(source_request, request, paths, *, request_id, request_index, dbn_parser=None):
    dbn_path = Path(paths["dbn"])
    csv_path = Path(paths["csv"])
    if not dbn_path.exists() or csv_path.exists():
        return None
    csv_temps = sorted(csv_path.parent.glob(f"{csv_path.name}.tmp.*"))
    if len(csv_temps) != 1:
        return None
    temp_pair = {"dbn": dbn_path, "csv": csv_temps[0]}
    validate_evidence_pair(
        source_request,
        request,
        temp_pair,
        request_id=request_id,
        request_index=request_index,
        dbn_parser=dbn_parser,
    )
    csv_temps[0].replace(csv_path)
    for temp_dbn in dbn_path.parent.glob(f"{dbn_path.name}.tmp.*"):
        try:
            temp_dbn.unlink()
        except OSError:
            pass
    return validate_evidence_pair(
        source_request,
        request,
        paths,
        request_id=request_id,
        request_index=request_index,
        dbn_parser=dbn_parser,
    )


def validate_evidence_pair(source_request, request, paths, *, request_id, request_index, dbn_parser=None):
    dbn_path = Path(paths["dbn"])
    csv_path = Path(paths["csv"])
    if not dbn_path.exists() or not csv_path.exists():
        raise EvidenceValidationError("PAIR_MISSING", f"{request_id} DBN/CSV pair is not complete")
    if dbn_path.stat().st_size <= 0 or csv_path.stat().st_size <= 0:
        raise EvidenceValidationError("PAIR_EMPTY", f"{request_id} DBN/CSV pair contains an empty file")

    dbn_summary = _parse_dbn(dbn_path, dbn_parser=dbn_parser)
    csv_summary = _parse_csv(csv_path)
    expected_instruments = {
        int(identity["instrument_id"])
        for identity in source_request.get("contract_identities", [])
        if identity.get("instrument_id") is not None
    }
    expected_publishers = {
        int(identity["publisher_id"])
        for identity in source_request.get("contract_identities", [])
        if identity.get("publisher_id") is not None
    }
    problems = []
    if dbn_summary["schema"] != request["schema"]:
        problems.append(f"wrong_dbn_schema_{dbn_summary['schema']}")
    if dbn_summary["record_count"] != csv_summary["record_count"]:
        problems.append(
            f"record_count_mismatch_dbn_{dbn_summary['record_count']}_csv_{csv_summary['record_count']}"
        )
    for summary_name, summary in (("dbn", dbn_summary), ("csv", csv_summary)):
        if summary["record_count"] > 0:
            if summary.get("instrument_id") not in (None, "__MULTIPLE__", *expected_instruments):
                problems.append(f"{summary_name}_wrong_instrument")
            if summary.get("publisher_id") not in (None, "__MULTIPLE__", *expected_publishers):
                problems.append(f"{summary_name}_wrong_publisher")
            if summary.get("symbol") not in (None, request["symbols"]):
                problems.append(f"{summary_name}_wrong_symbol")
            if _timestamp_outside_request(summary.get("min_ts_event"), request):
                problems.append(f"{summary_name}_start_out_of_window")
            if _timestamp_outside_request(summary.get("max_ts_event"), request):
                problems.append(f"{summary_name}_end_out_of_window")
    if csv_summary["record_count"] > 0 and not (
        csv_summary.get("symbol") == request["symbols"]
        or csv_summary.get("instrument_id") in expected_instruments
        or csv_summary.get("instrument_id") == "__MULTIPLE__"
    ):
        problems.append("csv_contract_identity_missing")
    if dbn_summary["record_count"] > 0 and not (
        dbn_summary.get("instrument_id") in expected_instruments
        or dbn_summary.get("instrument_id") == "__MULTIPLE__"
    ):
        problems.append("dbn_contract_identity_missing")
    if problems:
        raise EvidenceValidationError(
            "EXISTING_PAIR_INVALID",
            f"{request_id}: {'; '.join(sorted(set(problems)))}",
        )

    return {
        "request_id": request_id,
        "request_index": request_index,
        "schema": request["schema"],
        "dataset": request["dataset"],
        "stype_in": request["stype_in"],
        "symbols": request["symbols"],
        "start": request["start"],
        "end": request["end"],
        "candidate_ids": deepcopy(source_request.get("candidate_ids", [])),
        "leg": source_request.get("leg"),
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


def download_missing_request(api_key, source_request, request, *, request_id, request_index, client, output_root=OUTPUT_ROOT, dbn_parser=None):
    if not api_key:
        raise DownloadError("AUTH_MISSING", f"{ENV_VAR_NAME} is not configured")
    final_paths = planned_output_files([request], output_root=output_root)
    final_paths = {key: value for key, value in next(iter(final_paths.values())).items()}
    final_paths = {
        "dbn": Path(output_root) / f"{request_id}.dbn.zst",
        "csv": Path(output_root) / f"{request_id}.csv",
    }
    _refuse_unintended_overwrite(final_paths)
    temp_paths = _temp_output_files(final_paths)
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
        del store
        gc.collect()
        validate_evidence_pair(
            source_request,
            request,
            temp_paths,
            request_id=request_id,
            request_index=request_index,
            dbn_parser=dbn_parser,
        )
        Path(output_root).mkdir(parents=True, exist_ok=True)
        _atomic_publish_pair(temp_paths, final_paths)
        final_summary = validate_evidence_pair(
            source_request,
            request,
            final_paths,
            request_id=request_id,
            request_index=request_index,
            dbn_parser=dbn_parser,
        )
        final_summary["status"] = "COMPLETED_DOWNLOADED"
        return final_summary
    except DownloadError:
        _remove_temp_files(temp_paths)
        raise
    except KeyboardInterrupt:
        raise
    except Exception as exc:
        _remove_temp_files(temp_paths)
        raise DownloadError("VENDOR_OR_NETWORK_FAILURE", f"{type(exc).__name__}: {exc}") from exc


def build_manifest(
    *,
    status,
    source_request,
    cost_check,
    cost_requests=None,
    request_results=None,
    failure=None,
    current_request_id=None,
    created_utc=None,
    manifest_path=MANIFEST_PATH,
    output_root=OUTPUT_ROOT,
):
    result_map = request_results or {}
    request_list = deepcopy(cost_requests or cost_check.get("requests", []))
    output_files = [
        _public_request_result(result_map[request_id(index, request)])
        for index, request in enumerate(request_list)
        if request_id(index, request) in result_map
        and result_map[request_id(index, request)].get("status") in FINAL_STATUSES
    ]
    completed = [
        request_id(index, request)
        for index, request in enumerate(request_list)
        if result_map.get(request_id(index, request), {}).get("status") in FINAL_STATUSES
    ]
    remaining = [
        request_id(index, request)
        for index, request in enumerate(request_list)
        if result_map.get(request_id(index, request), {}).get("status") not in FINAL_STATUSES
    ]
    return {
        "result_version": RESULT_VERSION,
        "status": status,
        "created_utc": created_utc or _utc_now(),
        "credential_env_var": ENV_VAR_NAME,
        "credential_value_printed": False,
        "credential_value_persisted": False,
        "dataset": DATASET,
        "source_request": _relative(SOURCE_REQUEST_PATH),
        "source_cost_check": _relative(COST_CHECK_PATH),
        "operator_approved_grouped_cost_usd": str(APPROVED_GROUPED_COST),
        "checked_grouped_cost_usd": cost_check.get("grouped_cost"),
        "download_allowed_for_exact_cost_checked_requests": True,
        "request_count": len(request_list),
        "required_schemas": sorted(REQUIRED_SCHEMAS),
        "forbidden_schemas": ["definition"],
        "exact_requests": request_list,
        "output_root": _relative(output_root),
        "manifest_path": _relative(manifest_path),
        "download_performed": any(
            row.get("status") == "COMPLETED_DOWNLOADED" for row in result_map.values()
        ),
        "current_request_id": current_request_id,
        "completed_or_reused_request_ids": completed,
        "remaining_request_ids": remaining,
        "output_files": output_files,
        "request_status": _request_status(result_map, request_list),
        "vendor_failure": failure,
        "entry_status": "NOT_EVALUATED",
        "exit_status": "NOT_EVALUATED",
        "gross_pnl": None,
        "net_pnl": None,
        "profitability_proof": "NO",
        "paper_live_eligibility": "NO",
        "setup_entry_exit_pnl_decision_made": False,
    }


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
    source_request_path=SOURCE_REQUEST_PATH,
    cost_check_path=COST_CHECK_PATH,
    output_root=OUTPUT_ROOT,
    manifest_path=MANIFEST_PATH,
    client_factory=None,
    dbn_parser=None,
    output_stream=None,
    write_failure_manifest=True,
):
    stream = output_stream or sys.stdout
    inputs = load_inputs(source_request_path=source_request_path, cost_check_path=cost_check_path)
    source_requests = []
    cost_requests = inputs["cost_check"].get("requests", [])
    request_results = {}
    current_request_id = None
    try:
        source_requests, cost_requests = validate_preflight(
            source_request=inputs["source_request"],
            cost_check=inputs["cost_check"],
        )
        Path(output_root).mkdir(parents=True, exist_ok=True)
        request_results = inspect_existing_outputs(
            source_requests,
            cost_requests,
            output_root=output_root,
            dbn_parser=dbn_parser,
        )
        _write_checkpoint("IN_PROGRESS", inputs, cost_requests, request_results, manifest_path, output_root, current_request_id=None)
        for index, request in enumerate(cost_requests):
            rid = request_id(index, request)
            current_request_id = rid
            if request_results[rid]["status"] == "COMPLETED_REUSED":
                _emit(stream, f"REQUEST_REUSED={rid}")
                _write_checkpoint("IN_PROGRESS", inputs, cost_requests, request_results, manifest_path, output_root, current_request_id=rid)
                continue
            key = api_key if api_key is not None else os.environ.get(ENV_VAR_NAME)
            if not key:
                raise DownloadError("AUTH_MISSING", f"{ENV_VAR_NAME} is not configured")
            client = client_factory(key) if client_factory is not None else _databento_client(key)
            _emit(stream, _freeze_guidance(rid, request))
            _emit(stream, f"REQUEST_START={rid}")
            request_results[rid] = download_missing_request(
                key,
                source_requests[index],
                request,
                request_id=rid,
                request_index=index,
                client=client,
                output_root=output_root,
                dbn_parser=dbn_parser,
            )
            _emit(stream, f"REQUEST_COMPLETE={rid}")
            _write_checkpoint("IN_PROGRESS", inputs, cost_requests, request_results, manifest_path, output_root, current_request_id=rid)
        status = "SUCCESS" if _all_final(request_results, cost_requests) else "FAILURE"
        failure = None if status == "SUCCESS" else {
            "classification": "INCOMPLETE_REQUEST_SET",
            "detail": "not all 32 requests are completed or reused",
        }
        manifest = build_manifest(
            status=status,
            source_request=inputs["source_request"],
            cost_check=inputs["cost_check"],
            cost_requests=cost_requests,
            request_results=request_results,
            failure=failure,
            manifest_path=manifest_path,
            output_root=output_root,
        )
        write_manifest(manifest, manifest_path=manifest_path)
        return (0 if status == "SUCCESS" else 1), manifest
    except KeyboardInterrupt:
        manifest = build_manifest(
            status="INTERRUPTED",
            source_request=inputs["source_request"],
            cost_check=inputs["cost_check"],
            cost_requests=cost_requests,
            request_results=request_results,
            failure={"classification": "KEYBOARD_INTERRUPT", "detail": "operator pressed Ctrl+C"},
            current_request_id=current_request_id,
            manifest_path=manifest_path,
            output_root=output_root,
        )
        if write_failure_manifest:
            _try_write_manifest(manifest, manifest_path)
        return 130, manifest
    except DownloadError as exc:
        manifest = build_manifest(
            status="FAILURE",
            source_request=inputs["source_request"],
            cost_check=inputs["cost_check"],
            cost_requests=cost_requests,
            request_results=request_results,
            failure={"classification": exc.classification, "detail": exc.detail},
            current_request_id=current_request_id,
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


def _request_status(request_results, requests):
    result = {}
    for index, request in enumerate(requests):
        rid = request_id(index, request)
        row = request_results.get(rid) or {"status": "MISSING"}
        result[rid] = {
            "status": row["status"],
            "parsed_record_count": row.get("parsed_record_count"),
            "request": deepcopy(request),
        }
    return result


def _public_request_result(row):
    public = deepcopy(row)
    public.pop("request", None)
    public.pop("source_request", None)
    public.pop("paths", None)
    return public


def _write_checkpoint(status, inputs, cost_requests, request_results, manifest_path, output_root, *, current_request_id):
    manifest = build_manifest(
        status=status,
        source_request=inputs["source_request"],
        cost_check=inputs["cost_check"],
        cost_requests=cost_requests,
        request_results=request_results,
        current_request_id=current_request_id,
        manifest_path=manifest_path,
        output_root=output_root,
    )
    write_manifest(manifest, manifest_path=manifest_path)


def _try_write_manifest(manifest, manifest_path):
    try:
        write_manifest(manifest, manifest_path=manifest_path)
    except Exception:
        pass


def _all_final(request_results, requests):
    return all(
        request_results.get(request_id(index, request), {}).get("status") in FINAL_STATUSES
        for index, request in enumerate(requests)
    )


def _databento_client(api_key):
    import databento as db

    return db.Historical(key=api_key)


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
        try:
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
            schema = str(store.schema)
        finally:
            del store
            gc.collect()
        return {
            "schema": schema,
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
                if row.get("symbol"):
                    symbols.add(row["symbol"])
                if row.get("instrument_id"):
                    instrument_ids.add(int(row["instrument_id"]))
                if row.get("publisher_id"):
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


def _remove_temp_files(paths):
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
    Path(temp_paths["dbn"]).replace(final_paths["dbn"])
    try:
        Path(temp_paths["csv"]).replace(final_paths["csv"])
    except Exception:
        if Path(final_paths["dbn"]).exists() and not Path(final_paths["csv"]).exists():
            Path(final_paths["dbn"]).unlink()
        raise


def _freeze_guidance(rid, request):
    return (
        f"REQUESTING={rid}; schema={request['schema']}; symbol={request['symbols']}; "
        "PowerShell may be quiet while Databento responds. If it appears frozen and is not "
        "requesting hidden input, press Ctrl+C once. Do not rerun before inspecting the "
        "checkpoint manifest, partial files, output, and Git status."
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


def _compact_ts(value):
    return (
        str(value)
        .replace("-", "")
        .replace(":", "")
        .replace(".", "")
        .replace("Z", "z")
        .lower()
    )


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
    return ts_ns < _iso_to_ns(request["start"]) or ts_ns >= _iso_to_ns(request["end"])


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
