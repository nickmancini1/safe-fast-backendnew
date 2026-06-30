import json
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EVALUATION_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day55_spy_670c_entry_exit_pnl_evaluation.json"
)
COST_SOURCE_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day52_existing_setup_databento_cost_request_operator_output.json"
)
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day55_spy_670c_target_cost_only_request.json"
)
RESULT_DOC_PATH = REPO_ROOT / "SAFE_FAST_DAY55_SPY_670C_TARGET_COST_ONLY_REQUEST_RESULT.md"

RESULT_VERSION = "day55_spy_670c_target_cost_only_request_v1"
DATASET = "OPRA.PILLAR"
RAW_SYMBOL = "SPY   260330C00670000"
REQUIRED_SCHEMAS = ("cmbp-1", "tcbbo", "trades", "statistics")
FORBIDDEN_SCHEMAS = ("definition",)
DESTINATION = (
    "historical_signal_replay/source_data/external_option_data_drop/"
    "day55_spy_670c_target_only"
)
EXPECTED_REQUESTS = [
    {
        "dataset": DATASET,
        "schema": "cmbp-1",
        "stype_in": "raw_symbol",
        "symbols": RAW_SYMBOL,
        "start": "2026-03-16T13:31:00Z",
        "end": "2026-03-16T13:36:00Z",
    },
    {
        "dataset": DATASET,
        "schema": "tcbbo",
        "stype_in": "raw_symbol",
        "symbols": RAW_SYMBOL,
        "start": "2026-03-16T13:31:00Z",
        "end": "2026-03-16T19:45:00Z",
    },
    {
        "dataset": DATASET,
        "schema": "trades",
        "stype_in": "raw_symbol",
        "symbols": RAW_SYMBOL,
        "start": "2026-03-16T13:30:00Z",
        "end": "2026-03-16T19:45:00Z",
    },
    {
        "dataset": DATASET,
        "schema": "statistics",
        "stype_in": "raw_symbol",
        "symbols": RAW_SYMBOL,
        "start": "2026-03-16T13:30:00Z",
        "end": "2026-03-16T13:36:00Z",
    },
]


class TargetCostRequestError(ValueError):
    pass


def build_document(
    *,
    evaluation_path=EVALUATION_PATH,
    cost_source_path=COST_SOURCE_PATH,
    run_timestamp=None,
    source_commit=None,
):
    evaluation = _load_json(evaluation_path)
    exact_window_problem = _window_problem(evaluation)
    if exact_window_problem:
        return _blocked_document(
            exact_window_problem,
            evaluation_path=evaluation_path,
            cost_source_path=cost_source_path,
            run_timestamp=run_timestamp,
            source_commit=source_commit,
        )

    cost_source = _load_json(cost_source_path)
    schema_costs = _schema_costs(cost_source)
    return {
        "result_version": RESULT_VERSION,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp or _utc_now(),
        "decision": "TARGET_COST_ONLY_REQUEST_READY_FOR_OPERATOR_APPROVAL",
        "dataset": DATASET,
        "exact_symbol": RAW_SYMBOL,
        "selected_contract": {
            "raw_symbol": RAW_SYMBOL,
            "underlying": "SPY",
            "expiration": "2026-03-30",
            "strike": "670",
            "side": "call",
            "instrument_id": 1241515301,
            "publisher_id": 30,
        },
        "cost_only": True,
        "vendor_call_performed": False,
        "download_performed": False,
        "credential_env_var_read": False,
        "required_schemas": list(REQUIRED_SCHEMAS),
        "forbidden_schemas": list(FORBIDDEN_SCHEMAS),
        "request_count": len(EXPECTED_REQUESTS),
        "requests": EXPECTED_REQUESTS,
        "schema_costs": schema_costs,
        "exact_estimated_cost": cost_source["grouped_cost"],
        "currency": cost_source.get("currency", "USD"),
        "cost_source": _relative(cost_source_path),
        "window_sources": [
            _relative(evaluation_path),
            "historical_signal_replay/results/day52_existing_setup_option_evidence_end_to_end_backtest.json",
            "historical_signal_replay/results/day52_existing_setup_databento_cost_request_operator_output.json",
        ],
        "destination_for_approved_download": DESTINATION,
        "operator_approval_text": (
            "Approve cost-only Databento OPRA.PILLAR request for "
            "SPY   260330C00670000 using schemas cmbp-1, tcbbo, trades, "
            "statistics only, no definition request, estimated cost "
            f"{cost_source['grouped_cost']} {cost_source.get('currency', 'USD')}; "
            f"if approved, download only to {DESTINATION}."
        ),
        "entry_status": "NOT_EVALUATED",
        "exit_status": "NOT_EVALUATED",
        "gross_pnl": None,
        "net_pnl": None,
        "profitability_proof": "NO",
        "paper_live_eligibility": "NO",
        "next_action": (
            "Operator approval is required before any Databento download. "
            "No Codex download was performed."
        ),
    }


def write_outputs(*, run_timestamp=None, source_commit=None):
    document = build_document(run_timestamp=run_timestamp, source_commit=source_commit)
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    RESULT_DOC_PATH.write_text(_markdown(document), encoding="utf-8")
    return document


def _window_problem(evaluation):
    if evaluation.get("result_version") != "day55_spy_670c_entry_exit_pnl_evaluation_v1":
        return "evaluation_result_version_mismatch"
    selected = evaluation.get("selected_contract", {})
    if selected.get("raw_symbol") != RAW_SYMBOL:
        return "target_symbol_not_found"
    accepted_setup = evaluation.get("accepted_setup", {})
    entry_window = accepted_setup.get("entry_window", {})
    if accepted_setup.get("setup_timestamp") != "2026-03-16T13:30:00Z":
        return "setup_timestamp_not_found"
    if entry_window.get("start") != "2026-03-16T13:31:00Z":
        return "entry_window_start_not_found"
    if entry_window.get("end") != "2026-03-16T13:36:00Z":
        return "entry_window_end_not_found"
    if accepted_setup.get("trigger_timestamp") != "2026-03-16T13:31:00Z":
        return "trigger_timestamp_not_found"
    return None


def _schema_costs(cost_source):
    if cost_source.get("status") != "SUCCESS":
        raise TargetCostRequestError("cost_source_not_success")
    if cost_source.get("cost_only") is not True:
        raise TargetCostRequestError("cost_source_not_cost_only")
    if cost_source.get("download_performed") is not False:
        raise TargetCostRequestError("cost_source_download_performed")
    if cost_source.get("dataset") != DATASET:
        raise TargetCostRequestError("cost_source_dataset_mismatch")
    if cost_source.get("request_count") != len(EXPECTED_REQUESTS):
        raise TargetCostRequestError("cost_source_request_count_mismatch")
    if _sorted_requests(cost_source.get("requests", [])) != _sorted_requests(EXPECTED_REQUESTS):
        raise TargetCostRequestError("cost_source_request_mismatch")

    schema_costs = cost_source.get("schema_costs", [])
    cost_rows = [{k: v for k, v in row.items() if k != "checked_cost" and k != "currency"} for row in schema_costs]
    if _sorted_requests(cost_rows) != _sorted_requests(EXPECTED_REQUESTS):
        raise TargetCostRequestError("cost_source_schema_cost_request_mismatch")
    return schema_costs


def _blocked_document(
    reason,
    *,
    evaluation_path,
    cost_source_path,
    run_timestamp,
    source_commit,
):
    return {
        "result_version": RESULT_VERSION,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp or _utc_now(),
        "decision": "EXACT_WINDOW_NOT_FOUND",
        "first_blocker": reason,
        "dataset": DATASET,
        "exact_symbol": RAW_SYMBOL,
        "cost_only": True,
        "vendor_call_performed": False,
        "download_performed": False,
        "credential_env_var_read": False,
        "required_schemas": list(REQUIRED_SCHEMAS),
        "forbidden_schemas": list(FORBIDDEN_SCHEMAS),
        "request_count": 0,
        "requests": [],
        "schema_costs": [],
        "exact_estimated_cost": None,
        "currency": "USD",
        "cost_source": _relative(cost_source_path),
        "window_sources": [_relative(evaluation_path)],
        "destination_for_approved_download": DESTINATION,
        "operator_approval_text": None,
        "profitability_proof": "NO",
        "paper_live_eligibility": "NO",
        "next_action": "Stop; exact windows were not proven from repo evidence.",
    }


def _sorted_requests(rows):
    return sorted(
        rows,
        key=lambda row: (
            row.get("schema"),
            row.get("symbols"),
            row.get("start"),
            row.get("end"),
        ),
    )


def _load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def _relative(path):
    return str(Path(path).resolve().relative_to(REPO_ROOT)).replace("\\", "/")


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


def _utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _markdown(document):
    if document["decision"] == "EXACT_WINDOW_NOT_FOUND":
        return f"""# SAFE-FAST Day 55 SPY 670C Target Cost-Only Request Result

- Decision: `{document['decision']}`
- First blocker: `{document['first_blocker']}`
- Exact symbol: `{document['exact_symbol']}`
- Cost only: `true`
- Download performed: `false`
- Required schemas: `{', '.join(document['required_schemas'])}`
- Forbidden schemas: `{', '.join(document['forbidden_schemas'])}`
- Profitability proof: `{document['profitability_proof']}`
- Paper/live eligibility: `{document['paper_live_eligibility']}`

Next: {document['next_action']}
"""

    request_lines = "\n".join(
        "- `{schema}` `{start}` to `{end}`".format(**request)
        for request in document["requests"]
    )
    return f"""# SAFE-FAST Day 55 SPY 670C Target Cost-Only Request Result

- Decision: `{document['decision']}`
- Exact symbol: `{document['exact_symbol']}`
- Dataset: `{document['dataset']}`
- Exact schemas: `{', '.join(document['required_schemas'])}`
- Forbidden schemas: `{', '.join(document['forbidden_schemas'])}`
- Exact estimated cost: `{document['exact_estimated_cost']} {document['currency']}`
- Destination for approved download: `{document['destination_for_approved_download']}`
- Cost only: `true`
- Vendor call performed: `false`
- Download performed: `false`
- Profitability proof: `{document['profitability_proof']}`
- Paper/live eligibility: `{document['paper_live_eligibility']}`

## Exact Windows

{request_lines}

## Operator Approval Text

{document['operator_approval_text']}

Next: {document['next_action']}
"""


if __name__ == "__main__":
    doc = write_outputs()
    print(
        "wrote day55 SPY 670C target cost-only request: "
        f"{doc['decision']}"
    )
