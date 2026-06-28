import json
import os
import subprocess
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "historical_signal_replay" / "results" / "day55_definition_cost_request_for_replay_ready_candidates.json"
OUTPUT = ROOT / "historical_signal_replay" / "results" / "day55_definition_cost_check_for_replay_ready_candidates.json"
DOC = ROOT / "SAFE_FAST_DAY55_DEFINITION_COST_CHECK_FOR_REPLAY_READY_CANDIDATES.md"

ENV_VAR = "SAFE_FAST_DB_AUTH"
DATASET = "OPRA.PILLAR"


def git_head():
    return subprocess.check_output(["git", "--no-pager", "log", "-1", "--oneline"], text=True).strip()


def session_date(value):
    dt = datetime.fromisoformat(value)
    return dt.date()


def build_definition_requests(source):
    unique = {}
    for item in source["requests"]:
        ticker = item["ticker"]
        day = session_date(item["accepted_setup_time"])
        key = (ticker, str(day))
        unique.setdefault(key, {
            "dataset": DATASET,
            "schema": "definition",
            "stype_in": "parent",
            "symbols": f"{ticker}.OPT",
            "start": f"{day}T00:00:00Z",
            "end": f"{day + timedelta(days=1)}T00:00:00Z",
            "candidate_ids": [],
        })
        unique[key]["candidate_ids"].append(item["candidate_id"])
    return list(unique.values())


def base_output(status, requests, **extra):
    out = {
        "schema": "safe_fast_day55_definition_cost_check_for_replay_ready_candidates_v1",
        "created_from_head": git_head(),
        "source_request": "historical_signal_replay/results/day55_definition_cost_request_for_replay_ready_candidates.json",
        "status": status,
        "dataset": DATASET,
        "request_count": len(requests),
        "requests": requests,
        "cost_only": True,
        "download_performed": False,
        "vendor_metadata_call_performed": False,
        "contract_selection_ready": False,
        "economics_ready_count": 0,
        "grouped_cost": None,
        "currency": "USD",
        "profitability_proof": "NO",
        "paper_live_eligibility": "NO",
    }
    out.update(extra)
    return out


def write_doc(out):
    lines = [
        "# SAFE-FAST Day 55 Definition Cost Check for Replay-Ready Candidates",
        "",
        f"- Status: `{out['status']}`",
        f"- Request count: `{out['request_count']}`",
        f"- Cost only: `{str(out['cost_only']).lower()}`",
        f"- Download performed: `{str(out['download_performed']).lower()}`",
        f"- Vendor metadata call performed: `{str(out['vendor_metadata_call_performed']).lower()}`",
        f"- Grouped cost: `{out['grouped_cost']}`",
        f"- Profitability proof: `{out['profitability_proof']}`",
        f"- Paper/live eligibility: `{out['paper_live_eligibility']}`",
        "",
        "## Next action",
        "",
        out["next_action"],
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main():
    source = json.loads(INPUT.read_text(encoding="utf-8-sig"))
    requests = build_definition_requests(source)

    if not requests:
        out = base_output(
            "FAILURE",
            requests,
            failure_reason="NO_DEFINITION_REQUESTS_BUILT",
            next_action="Fix definition request construction before cost check.",
        )
        OUTPUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
        write_doc(out)
        return 1

    api_key = os.environ.get(ENV_VAR)
    if not api_key:
        out = base_output(
            "BLOCKED",
            requests,
            failure_reason=f"{ENV_VAR}_NOT_CONFIGURED",
            next_action="Configure SAFE_FAST_DB_AUTH, then rerun this cost-only checker. No download is performed.",
        )
        OUTPUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
        write_doc(out)
        return 0

    try:
        import databento as db
        client = db.Historical(key=api_key)
        schema_costs = []
        total = Decimal("0")
        for req in requests:
            vendor_req = {k: v for k, v in req.items() if k != "candidate_ids"}
            cost = Decimal(str(client.metadata.get_cost(**vendor_req)))
            total += cost
            schema_costs.append({**req, "checked_cost": str(cost), "currency": "USD"})

        out = base_output(
            "SUCCESS",
            requests,
            vendor_metadata_call_performed=True,
            schema_costs=schema_costs,
            grouped_cost=str(total),
            next_action="Operator review grouped definition cost. If approved, use definitions only for contract selection before quote/trade/statistics evidence.",
        )
        OUTPUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
        write_doc(out)
        print(f"grouped_cost {total} USD")
        return 0

    except Exception as exc:
        out = base_output(
            "FAILURE",
            requests,
            vendor_metadata_call_performed=True,
            failure_reason=type(exc).__name__,
            failure_detail=str(exc)[:500],
            next_action="Fix the exact Databento definition request fields, then rerun cost-only check. No download was performed.",
        )
        OUTPUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
        write_doc(out)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
