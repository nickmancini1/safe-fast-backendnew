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

REQUESTS = [
    {
        "dataset": "OPRA.PILLAR",
        "schema": "definition",
        "stype_in": "raw_symbol",
        "symbols": "SPY",
        "start": "2026-03-16T13:30:00Z",
        "end": "2026-03-16T13:32:00Z",
    },
    {
        "dataset": "OPRA.PILLAR",
        "schema": "cmbp-1",
        "stype_in": "raw_symbol",
        "symbols": "SPY   260330C00669000",
        "start": "2026-03-16T13:31:00Z",
        "end": "2026-03-16T13:36:00Z",
    },
    {
        "dataset": "OPRA.PILLAR",
        "schema": "tcbbo",
        "stype_in": "raw_symbol",
        "symbols": "SPY   260330C00669000",
        "start": "2026-03-16T13:31:00Z",
        "end": "2026-03-16T19:45:00Z",
    },
    {
        "dataset": "OPRA.PILLAR",
        "schema": "trades",
        "stype_in": "raw_symbol",
        "symbols": "SPY   260330C00669000",
        "start": "2026-03-16T13:30:00Z",
        "end": "2026-03-16T19:45:00Z",
    },
    {
        "dataset": "OPRA.PILLAR",
        "schema": "statistics",
        "stype_in": "raw_symbol",
        "symbols": "SPY   260330C00669000",
        "start": "2026-03-16T13:30:00Z",
        "end": "2026-03-16T13:36:00Z",
    },
]


def main():
    api_key = os.environ.get("SAFE_FAST_DB_AUTH")
    if not api_key:
        raise SystemExit("SAFE_FAST_DB_AUTH is not configured")

    import databento as db

    client = db.Historical(key=api_key)
    rows = []
    total = Decimal("0")
    for request in REQUESTS:
        cost = Decimal(str(client.metadata.get_cost(**request)))
        rows.append({**request, "checked_cost": str(cost), "currency": "USD"})
        total += cost

    output = {
        "result_version": "day52_existing_setup_databento_cost_request_operator_output_v1",
        "checked_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "download_performed": False,
        "dataset": "OPRA.PILLAR",
        "selected_contract": {
            "underlying": "SPY",
            "expiration": "2026-03-30",
            "strike": "669",
            "call_or_put": "C",
            "vendor_symbol": "SPY   260330C00669000",
        },
        "schema_costs": rows,
        "grouped_cost": str(total),
        "currency": "USD",
        "stages_unlocked_after_approval_and_download": [
            "contract_definition_confirmation",
            "deterministic_contract_selection",
            "complete_entry_window_validation",
            "eligible_entry_or_exact_no_trade",
            "exit_replay",
            "gross_and_net_pnl_if_entry_exists",
        ],
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT_PATH}")
    print(f"grouped_cost {total} USD")


if __name__ == "__main__":
    main()
