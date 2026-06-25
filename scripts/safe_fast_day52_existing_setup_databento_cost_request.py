import json
import os
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day52_existing_setup_databento_cost_request_operator_output.json"
)
ENV_VAR_NAME = "SAFE_FAST_DB_AUTH"
DATASET = "OPRA.PILLAR"
SELECTED_RAW_SYMBOL = "SPY   260330C00670000"
REJECTED_RAW_SYMBOL = "SPY   260330C00669000"

REQUESTS = [
    {
        "dataset": DATASET,
        "schema": "cmbp-1",
        "stype_in": "raw_symbol",
        "symbols": SELECTED_RAW_SYMBOL,
        "start": "2026-03-16T13:31:00Z",
        "end": "2026-03-16T13:36:00Z",
    },
    {
        "dataset": DATASET,
        "schema": "tcbbo",
        "stype_in": "raw_symbol",
        "symbols": SELECTED_RAW_SYMBOL,
        "start": "2026-03-16T13:31:00Z",
        "end": "2026-03-16T19:45:00Z",
    },
    {
        "dataset": DATASET,
        "schema": "trades",
        "stype_in": "raw_symbol",
        "symbols": SELECTED_RAW_SYMBOL,
        "start": "2026-03-16T13:30:00Z",
        "end": "2026-03-16T19:45:00Z",
    },
    {
        "dataset": DATASET,
        "schema": "statistics",
        "stype_in": "raw_symbol",
        "symbols": SELECTED_RAW_SYMBOL,
        "start": "2026-03-16T13:30:00Z",
        "end": "2026-03-16T13:36:00Z",
    },
]


def _utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def validate_output_path(output_path=OUTPUT_PATH):
    resolved = Path(output_path).resolve()
    expected_parent = (
        REPO_ROOT / "historical_signal_replay" / "results"
    ).resolve()
    if resolved.parent != expected_parent:
        raise ValueError(f"output path must be inside {expected_parent}")
    if resolved.name != OUTPUT_PATH.name:
        raise ValueError(f"unexpected output filename {resolved.name}")
    return resolved


def _base_output(*, status, checked_at_utc=None):
    return {
        "result_version": "day52_existing_setup_databento_cost_request_operator_output_v1",
        "status": status,
        "checked_at_utc": checked_at_utc or _utc_now(),
        "credential_env_var": ENV_VAR_NAME,
        "credential_value_printed": False,
        "download_performed": False,
        "cost_only": True,
        "dataset": DATASET,
        "selected_contract": {
            "underlying": "SPY",
            "expiration": "2026-03-30",
            "strike": "670",
            "call_or_put": "C",
            "vendor_symbol": SELECTED_RAW_SYMBOL,
            "instrument_id": 1241515301,
            "publisher_id": 30,
        },
        "rejected_contract": {
            "expiration": "2026-03-30",
            "strike": "669",
            "call_or_put": "C",
            "vendor_symbol": REJECTED_RAW_SYMBOL,
            "reason": "CONTRACT_UNLISTED",
        },
        "request_count": len(REQUESTS),
        "requests": REQUESTS,
    }


def build_success_output(schema_costs, *, checked_at_utc=None):
    total = sum((Decimal(str(row["checked_cost"])) for row in schema_costs), Decimal("0"))
    output = _base_output(status="SUCCESS", checked_at_utc=checked_at_utc)
    output.update(
        {
            "schema_costs": schema_costs,
            "grouped_cost": str(total),
            "currency": "USD",
            "stages_unlocked_after_approval_and_download": [
                "complete_entry_window_validation",
                "eligible_entry_or_exact_no_trade",
                "exit_replay",
                "gross_and_net_pnl_if_entry_exists",
            ],
        }
    )
    return output


def build_failure_output(reason, *, checked_at_utc=None):
    output = _base_output(status="FAILURE", checked_at_utc=checked_at_utc)
    output.update(
        {
            "failure_reason": reason,
            "schema_costs": [],
            "grouped_cost": None,
            "currency": "USD",
        }
    )
    return output


def write_output(output, output_path=OUTPUT_PATH):
    resolved = validate_output_path(output_path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return resolved


def run_cost_check(api_key):
    import databento as db

    client = db.Historical(key=api_key)
    rows = []
    for request in REQUESTS:
        cost = Decimal(str(client.metadata.get_cost(**request)))
        rows.append({**request, "checked_cost": str(cost), "currency": "USD"})
    return rows


def main():
    api_key = os.environ.get(ENV_VAR_NAME)
    if not api_key:
        output = build_failure_output(f"{ENV_VAR_NAME} is not configured")
        write_output(output)
        print(f"wrote {OUTPUT_PATH}")
        return 1

    try:
        rows = run_cost_check(api_key)
        output = build_success_output(rows)
        write_output(output)
    except Exception as exc:
        output = build_failure_output(type(exc).__name__)
        write_output(output)
        print(f"wrote {OUTPUT_PATH}")
        return 1

    print(f"wrote {OUTPUT_PATH}")
    print(f"grouped_cost {output['grouped_cost']} USD")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
