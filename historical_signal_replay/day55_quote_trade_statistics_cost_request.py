import json
from datetime import datetime, time, timedelta, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day55_definition_contract_selection_for_replay_ready_candidates.json"
)
RESULT_PATH = (
    REPO_ROOT
    / "historical_signal_replay"
    / "results"
    / "day55_quote_trade_statistics_cost_request_for_selected_contracts.json"
)
RESULT_DOC_PATH = REPO_ROOT / "SAFE_FAST_DAY55_QUOTE_TRADE_STATISTICS_COST_REQUEST_RESULT.md"

RESULT_VERSION = "safe_fast_day55_quote_trade_statistics_cost_request_for_selected_contracts_v1"
DATASET = "OPRA.PILLAR"
REQUIRED_SCHEMAS = ("cmbp-1", "tcbbo", "trades", "statistics")
FORBIDDEN_SCHEMAS = ("definition",)
ENTRY_OFFSET_MINUTES = 1
ENTRY_WINDOW_MINUTES = 5
EXIT_TIME_ET = time(15, 45)


class CostRequestBuildError(ValueError):
    pass


def build_document(*, input_path=INPUT_PATH, run_timestamp=None, source_commit=None):
    source = _load_json(input_path)
    _validate_source(source)

    requests = _build_requests(source["candidates"])
    selected_candidates = [
        candidate
        for candidate in source["candidates"]
        if candidate.get("contract_selection_status")
        == "CONTRACTS_SELECTED_FOR_QUOTE_TRADE_STATISTICS_REQUEST"
    ]

    return {
        "result_version": RESULT_VERSION,
        "source_commit": source_commit or _git_short_head(),
        "run_timestamp": run_timestamp or _utc_now(),
        "source_selected_contract_result": _relative(input_path),
        "decision": "QUOTE_TRADE_STATISTICS_COST_REQUEST_READY_FOR_OPERATOR_REVIEW",
        "dataset": DATASET,
        "cost_only": True,
        "vendor_call_performed": False,
        "download_performed": False,
        "credential_env_var_read": False,
        "request_count": len(requests),
        "required_schemas": list(REQUIRED_SCHEMAS),
        "forbidden_schemas": list(FORBIDDEN_SCHEMAS),
        "requests": requests,
        "selected_candidate_count": len(selected_candidates),
        "selected_contract_leg_count": sum(
            1
            for candidate in selected_candidates
            for leg in ("long_contract", "short_contract")
            if candidate.get(leg)
        ),
        "unique_request_key_count": len(requests),
        "entry_status": "NOT_EVALUATED",
        "exit_status": "NOT_EVALUATED",
        "gross_pnl": None,
        "net_pnl": None,
        "profitability_proof": "NO",
        "paper_live_eligibility": "NO",
        "next_action": (
            "Operator review/cost-check these exact quote/trade/statistics requests. "
            "Do not download until cost is explicitly approved."
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


def _validate_source(source):
    if source.get("decision") != "DEFINITION_CONTRACT_SELECTION_COMPLETE":
        raise CostRequestBuildError("definition_contract_selection_not_complete")
    if source.get("quote_trade_statistics_download_performed") is not False:
        raise CostRequestBuildError("quote_trade_statistics_download_already_performed")
    if source.get("profitability_proof") != "NO":
        raise CostRequestBuildError("profitability_proof_not_no")
    if source.get("paper_live_eligibility") != "NO":
        raise CostRequestBuildError("paper_live_eligibility_not_no")
    if not source.get("candidates"):
        raise CostRequestBuildError("no_candidates")


def _build_requests(candidates):
    grouped = {}
    for candidate in candidates:
        if (
            candidate.get("contract_selection_status")
            != "CONTRACTS_SELECTED_FOR_QUOTE_TRADE_STATISTICS_REQUEST"
        ):
            continue
        if candidate.get("profitability_proof") != "NO":
            raise CostRequestBuildError(f"{candidate.get('candidate_id')}_profitability_proof_not_no")
        if candidate.get("paper_live_eligibility") != "NO":
            raise CostRequestBuildError(f"{candidate.get('candidate_id')}_paper_live_eligibility_not_no")

        windows = _candidate_windows(candidate["accepted_setup_time"])
        for leg_name in ("long_contract", "short_contract"):
            contract = candidate.get(leg_name)
            if not contract:
                raise CostRequestBuildError(f"{candidate.get('candidate_id')}_{leg_name}_missing")
            for schema in REQUIRED_SCHEMAS:
                request = _request_for(schema, contract["raw_symbol"], windows)
                key = (
                    request["schema"],
                    request["symbols"],
                    request["start"],
                    request["end"],
                    leg_name,
                )
                existing = grouped.setdefault(
                    key,
                    {
                        **request,
                        "leg": leg_name.replace("_contract", ""),
                        "candidate_ids": [],
                        "contract_identities": [],
                        "purpose": _purpose(schema),
                    },
                )
                existing["candidate_ids"].append(candidate["candidate_id"])
                existing["contract_identities"].append(_contract_identity(candidate, contract))

    requests = list(grouped.values())
    for request in requests:
        request["candidate_ids"] = sorted(set(request["candidate_ids"]))
        request["contract_identities"] = _dedupe_contract_identities(
            request["contract_identities"]
        )
    return sorted(
        requests,
        key=lambda item: (
            item["start"],
            item["symbols"],
            item["leg"],
            REQUIRED_SCHEMAS.index(item["schema"]),
        ),
    )


def _candidate_windows(accepted_setup_time):
    setup = _parse_time(accepted_setup_time)
    entry_start = setup.replace(
        second=0,
        microsecond=0,
    ) + timedelta(minutes=ENTRY_OFFSET_MINUTES)
    entry_end = entry_start + timedelta(minutes=ENTRY_WINDOW_MINUTES)
    exit_end = setup.replace(
        hour=EXIT_TIME_ET.hour,
        minute=EXIT_TIME_ET.minute,
        second=0,
        microsecond=0,
    )
    if exit_end < entry_start:
        exit_end = entry_end
    return {
        "setup_start": _iso_utc(setup),
        "entry_start": _iso_utc(entry_start),
        "entry_end": _iso_utc(entry_end),
        "exit_end": _iso_utc(exit_end),
    }


def _request_for(schema, symbol, windows):
    if schema == "cmbp-1":
        start = windows["entry_start"]
        end = windows["entry_end"]
    elif schema == "tcbbo":
        start = windows["entry_start"]
        end = windows["exit_end"]
    elif schema == "trades":
        start = windows["setup_start"]
        end = windows["exit_end"]
    elif schema == "statistics":
        start = windows["setup_start"]
        end = windows["entry_end"]
    else:
        raise CostRequestBuildError(f"unsupported_schema_{schema}")
    return {
        "dataset": DATASET,
        "schema": schema,
        "stype_in": "raw_symbol",
        "symbols": symbol,
        "start": start,
        "end": end,
    }


def _purpose(schema):
    return {
        "cmbp-1": "complete entry-window bid/ask stream for quote freshness and spread/liquidity gates",
        "tcbbo": "selected-contract bid path through the 15:45 ET exit boundary",
        "trades": "trade volume and trade context from setup through exit boundary",
        "statistics": "open-interest/statistics liquidity evidence through entry window",
    }[schema]


def _contract_identity(candidate, contract):
    row = contract.get("definition_row") or {}
    return {
        "candidate_id": candidate["candidate_id"],
        "ticker": candidate["ticker"],
        "setup_type": candidate["setup_type"],
        "accepted_setup_time": candidate["accepted_setup_time"],
        "accepted_trigger": candidate["accepted_trigger"],
        "accepted_invalidation": candidate["accepted_invalidation"],
        "raw_symbol": contract["raw_symbol"],
        "instrument_id": str(contract["instrument_id"]),
        "publisher_id": str(row.get("publisher_id")),
        "expiration": contract["expiration"],
        "strike": str(contract["strike"]),
        "entry_status": "NOT_EVALUATED",
        "exit_status": "NOT_EVALUATED",
        "gross_pnl": None,
        "net_pnl": None,
        "profitability_proof": "NO",
        "paper_live_eligibility": "NO",
    }


def _dedupe_contract_identities(rows):
    seen = set()
    out = []
    for row in rows:
        key = tuple(sorted(row.items()))
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return sorted(out, key=lambda item: item["candidate_id"])


def _load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def _parse_time(value):
    return datetime.fromisoformat(str(value).replace("Z", "+00:00"))


def _iso_utc(value):
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


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
    return f"""# SAFE-FAST Day 55 Quote/Trade/Statistics Cost Request Result

- Decision: `{document['decision']}`
- Cost only: `{str(document['cost_only']).lower()}`
- Vendor call performed: `{str(document['vendor_call_performed']).lower()}`
- Download performed: `{str(document['download_performed']).lower()}`
- Request count: `{document['request_count']}`
- Required schemas: `{', '.join(document['required_schemas'])}`
- Forbidden schemas: `{', '.join(document['forbidden_schemas'])}`
- Profitability proof: `{document['profitability_proof']}`
- Paper/live eligibility: `{document['paper_live_eligibility']}`

Next action: {document['next_action']}
"""


if __name__ == "__main__":
    doc = write_outputs()
    print(
        "wrote day55 quote/trade/statistics cost request: "
        f"{doc['request_count']} requests"
    )
