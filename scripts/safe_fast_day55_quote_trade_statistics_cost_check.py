import json
import os
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day55_quote_trade_statistics_cost_request_for_selected_contracts.json"
)
OUTPUT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day55_quote_trade_statistics_cost_check_for_selected_contracts.json"
)
DOC_PATH = REPO_ROOT / "SAFE_FAST_DAY55_QUOTE_TRADE_STATISTICS_COST_CHECK_REVIEW.md"

RESULT_VERSION = "safe_fast_day55_quote_trade_statistics_cost_check_for_selected_contracts_v1"
SOURCE_RESULT_VERSION = "safe_fast_day55_quote_trade_statistics_cost_request_for_selected_contracts_v1"
ENV_VAR_NAME = "SAFE_FAST_DB_AUTH"
DATASET = "OPRA.PILLAR"
REQUIRED_SCHEMAS = {"cmbp-1", "tcbbo", "trades", "statistics"}
VENDOR_REQUEST_FIELDS = ("dataset", "schema", "stype_in", "symbols", "start", "end")


class CostCheckError(ValueError):
    pass


def _utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _load_source(input_path=INPUT_PATH):
    source = json.loads(Path(input_path).read_text(encoding="utf-8-sig"))
    validate_source_request(source)
    return source


def validate_source_request(source):
    problems = []
    if source.get("result_version") != SOURCE_RESULT_VERSION:
        problems.append("unexpected_source_result_version")
    if source.get("decision") != "QUOTE_TRADE_STATISTICS_COST_REQUEST_READY_FOR_OPERATOR_REVIEW":
        problems.append("source_not_ready_for_operator_review")
    if source.get("dataset") != DATASET:
        problems.append("unexpected_source_dataset")
    if source.get("cost_only") is not True:
        problems.append("source_cost_only_not_true")
    if source.get("vendor_call_performed") is not False:
        problems.append("source_vendor_call_already_performed")
    if source.get("download_performed") is not False:
        problems.append("source_download_already_performed")
    if source.get("profitability_proof") != "NO":
        problems.append("source_profitability_proof_not_no")
    if source.get("paper_live_eligibility") != "NO":
        problems.append("source_paper_live_eligibility_not_no")

    requests = source.get("requests", [])
    if source.get("request_count") != len(requests):
        problems.append("source_request_count_mismatch")
    if not requests:
        problems.append("source_requests_missing")

    schemas = {request.get("schema") for request in requests}
    if schemas != REQUIRED_SCHEMAS:
        problems.append("source_required_schema_set_mismatch")
    if "definition" in schemas:
        problems.append("source_definition_schema_present")

    for request in requests:
        if request.get("dataset") != DATASET:
            problems.append("request_dataset_mismatch")
        if request.get("schema") not in REQUIRED_SCHEMAS:
            problems.append(f"unexpected_request_schema_{request.get('schema')}")
        if request.get("stype_in") != "raw_symbol":
            problems.append("request_stype_in_not_raw_symbol")
        for field in ("symbols", "start", "end"):
            if not request.get(field):
                problems.append(f"request_{field}_missing")

    if problems:
        raise CostCheckError(",".join(sorted(set(problems))))


def vendor_request(request):
    clean = {field: request[field] for field in VENDOR_REQUEST_FIELDS}
    if clean["schema"] == "definition":
        raise CostCheckError("definition_schema_forbidden")
    return clean


def build_base_output(source, *, status, checked_at_utc=None):
    return {
        "result_version": RESULT_VERSION,
        "source_request": "historical_signal_replay/results/day55_quote_trade_statistics_cost_request_for_selected_contracts.json",
        "status": status,
        "checked_at_utc": checked_at_utc or _utc_now(),
        "credential_env_var": ENV_VAR_NAME,
        "credential_value_printed": False,
        "cost_only": True,
        "vendor_metadata_call_performed": False,
        "download_performed": False,
        "dataset": DATASET,
        "request_count": len(source["requests"]),
        "required_schemas": sorted(REQUIRED_SCHEMAS),
        "forbidden_schemas": ["definition"],
        "requests": [vendor_request(request) for request in source["requests"]],
        "entry_status": "NOT_EVALUATED",
        "exit_status": "NOT_EVALUATED",
        "gross_pnl": None,
        "net_pnl": None,
        "profitability_proof": "NO",
        "paper_live_eligibility": "NO",
        "schema_costs": [],
        "grouped_cost": None,
        "currency": "USD",
    }


def build_blocked_output(source, reason, *, checked_at_utc=None):
    output = build_base_output(source, status="BLOCKED", checked_at_utc=checked_at_utc)
    output.update(
        {
            "failure_reason": reason,
            "next_action": (
                "Configure SAFE_FAST_DB_AUTH and rerun this cost-only checker. "
                "Do not download until the grouped quote/trade/statistics cost is explicitly approved."
            ),
        }
    )
    return output


def build_success_output(source, schema_costs, *, checked_at_utc=None):
    total = sum((Decimal(str(row["checked_cost"])) for row in schema_costs), Decimal("0"))
    output = build_base_output(source, status="SUCCESS", checked_at_utc=checked_at_utc)
    output.update(
        {
            "vendor_metadata_call_performed": True,
            "schema_costs": schema_costs,
            "grouped_cost": str(total),
            "next_action": (
                "Operator review grouped quote/trade/statistics cost. "
                "If explicitly approved, perform the matching download in a separate authorized task."
            ),
        }
    )
    return output


def build_failure_output(source, reason, detail=None, *, checked_at_utc=None):
    output = build_base_output(source, status="FAILURE", checked_at_utc=checked_at_utc)
    output.update(
        {
            "vendor_metadata_call_performed": True,
            "failure_reason": reason,
            "failure_detail": (detail or "")[:500],
            "next_action": (
                "Resolve the exact Databento metadata.get_cost failure, then rerun the "
                "cost-only checker. Do not download until the grouped quote/trade/statistics "
                "cost is explicitly approved."
            ),
        }
    )
    return output


def run_cost_check(api_key, requests):
    import databento as db

    client = db.Historical(key=api_key)
    rows = []
    for request in requests:
        clean_request = vendor_request(request)
        cost = Decimal(str(client.metadata.get_cost(**clean_request)))
        rows.append({**clean_request, "checked_cost": str(cost), "currency": "USD"})
    return rows


def write_output(output, output_path=OUTPUT_PATH, doc_path=DOC_PATH):
    resolved_output = Path(output_path).resolve()
    expected_parent = (REPO_ROOT / "historical_signal_replay" / "results").resolve()
    if expected_parent not in resolved_output.parents:
        raise ValueError(f"output path must be inside {expected_parent}")
    resolved_output.parent.mkdir(parents=True, exist_ok=True)
    resolved_output.write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    Path(doc_path).write_text(_markdown(output), encoding="utf-8")
    return resolved_output


def _markdown(output):
    return f"""# SAFE-FAST Day 55 Quote/Trade/Statistics Cost Check Review

- Status: `{output['status']}`
- Dataset: `{output['dataset']}`
- Request count: `{output['request_count']}`
- Required schemas: `{', '.join(output['required_schemas'])}`
- Forbidden schemas: `{', '.join(output['forbidden_schemas'])}`
- Cost only: `{str(output['cost_only']).lower()}`
- Vendor metadata call performed: `{str(output['vendor_metadata_call_performed']).lower()}`
- Download performed: `{str(output['download_performed']).lower()}`
- Grouped cost: `{output['grouped_cost']}`
- Currency: `{output['currency']}`
- Profitability proof: `{output['profitability_proof']}`
- Paper/live eligibility: `{output['paper_live_eligibility']}`

Next action: {output['next_action']}
"""


def main():
    source = _load_source()
    api_key = os.environ.get(ENV_VAR_NAME)
    if not api_key:
        output = build_blocked_output(source, f"{ENV_VAR_NAME}_NOT_CONFIGURED")
        write_output(output)
        print(f"wrote {OUTPUT_PATH}")
        return 0

    try:
        schema_costs = run_cost_check(api_key, source["requests"])
        output = build_success_output(source, schema_costs)
    except Exception as exc:
        output = build_failure_output(source, type(exc).__name__, str(exc))
        write_output(output)
        print(f"wrote {OUTPUT_PATH}")
        return 0

    write_output(output)
    print(f"wrote {OUTPUT_PATH}")
    print(f"grouped_cost {output['grouped_cost']} USD")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
