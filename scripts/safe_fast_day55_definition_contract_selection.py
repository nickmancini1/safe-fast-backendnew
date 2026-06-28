import json
import os
import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COST = ROOT / "historical_signal_replay" / "results" / "day55_definition_cost_check_for_replay_ready_candidates.json"
REQUEST = ROOT / "historical_signal_replay" / "results" / "day55_definition_cost_request_for_replay_ready_candidates.json"
OUT = ROOT / "historical_signal_replay" / "results" / "day55_definition_contract_selection_for_replay_ready_candidates.json"
DOC = ROOT / "SAFE_FAST_DAY55_DEFINITION_CONTRACT_SELECTION_FOR_REPLAY_READY_CANDIDATES.md"

def dec(v):
    try:
        if v is None:
            return None
        s = str(v).strip()
        if s == "" or s.lower() == "nan":
            return None
        d = Decimal(s)
        if d > Decimal("100000"):
            d = d / Decimal("1000000000")
        return d
    except (InvalidOperation, ValueError):
        return None

def clean(v):
    try:
        import pandas as pd
        if pd.isna(v):
            return None
        if hasattr(v, "isoformat"):
            return v.isoformat()
    except Exception:
        pass
    if isinstance(v, Decimal):
        return str(v)
    return str(v)

def col(df, choices):
    lower = {c.lower(): c for c in df.columns}
    for choice in choices:
        if choice in lower:
            return lower[choice]
    for c in df.columns:
        lc = c.lower()
        if any(choice in lc for choice in choices):
            return c
    return None

def exp_date(v):
    s = str(v).strip()
    if re.fullmatch(r"\d{8}", s):
        return datetime.strptime(s, "%Y%m%d").date()
    try:
        import pandas as pd
        return pd.to_datetime(v).date()
    except Exception:
        return None

def setup_date(value):
    return datetime.fromisoformat(value).date()

def row_dict(row):
    return {str(k): clean(v) for k, v in row.items()}

def choose_contract(df, candidate):
    df = df.reset_index()
    raw_col = col(df, ["raw_symbol", "symbol"])
    strike_col = col(df, ["strike_price", "strike"])
    exp_col = col(df, ["expiration", "expiration_date", "expire"])
    class_col = col(df, ["instrument_class", "put_call", "option_type", "side"])
    inst_col = col(df, ["instrument_id"])

    if not raw_col or not strike_col or not exp_col:
        return None, "definition_columns_missing_for_contract_selection"

    trigger = dec(candidate["accepted_trigger"])
    if trigger is None:
        return None, "accepted_trigger_not_parseable"

    sdate = setup_date(candidate["accepted_setup_time"])
    rows = []

    for _, r in df.iterrows():
        strike = dec(r.get(strike_col))
        exp = exp_date(r.get(exp_col))
        if strike is None or exp is None:
            continue

        dte = (exp - sdate).days
        if dte < 14 or dte > 30:
            continue

        cls = str(r.get(class_col, "")).upper() if class_col else ""
        raw = str(r.get(raw_col, "")).upper()
        is_call = ("C" in cls or "CALL" in cls or "C0" in raw or re.search(r"C\d{8}", raw) or "C00" in raw)
        if not is_call:
            continue

        rows.append({
            "strike": strike,
            "expiration": exp,
            "dte": dte,
            "raw_symbol": str(r.get(raw_col)),
            "instrument_id": clean(r.get(inst_col)) if inst_col else None,
            "row": row_dict(r),
        })

    calls = [r for r in rows if r["strike"] >= trigger]
    if not calls:
        return None, "no_call_definition_at_or_above_trigger_in_14_30_dte_window"

    long = sorted(calls, key=lambda x: (x["expiration"], x["strike"]))[0]
    shorts = [
        r for r in rows
        if r["expiration"] == long["expiration"] and Decimal("5") <= (r["strike"] - long["strike"]) <= Decimal("10")
    ]

    if not shorts:
        return None, "no_5_to_10_point_short_call_available_for_vertical"

    short = sorted(shorts, key=lambda x: x["strike"])[0]

    return {
        "long_contract": {
            "raw_symbol": long["raw_symbol"],
            "instrument_id": long["instrument_id"],
            "expiration": str(long["expiration"]),
            "dte": long["dte"],
            "strike": str(long["strike"]),
            "definition_row": long["row"],
        },
        "short_contract": {
            "raw_symbol": short["raw_symbol"],
            "instrument_id": short["instrument_id"],
            "expiration": str(short["expiration"]),
            "dte": short["dte"],
            "strike": str(short["strike"]),
            "definition_row": short["row"],
        },
        "spread_width": str(short["strike"] - long["strike"]),
    }, None

def main():
    import databento as db

    api_key = os.environ.get("SAFE_FAST_DB_AUTH")
    if not api_key:
        raise SystemExit("SAFE_FAST_DB_AUTH missing")

    cost = json.loads(COST.read_text(encoding="utf-8-sig"))
    source = json.loads(REQUEST.read_text(encoding="utf-8-sig"))

    client = db.Historical(key=api_key)

    frames = {}
    downloaded = []
    for req in cost["requests"]:
        api_req = {
            "dataset": req["dataset"],
            "schema": req["schema"],
            "stype_in": req["stype_in"],
            "symbols": req["symbols"],
            "start": req["start"],
            "end": req["end"],
        }
        data = client.timeseries.get_range(**api_req)
        df = data.to_df()
        key = tuple(req["candidate_ids"])
        frames[key] = df
        downloaded.append({
            **api_req,
            "candidate_ids": req["candidate_ids"],
            "definition_rows": int(len(df)),
            "columns": [str(c) for c in df.reset_index().columns],
        })

    candidates = []
    for cand in source["requests"]:
        match_key = None
        for key in frames:
            if cand["candidate_id"] in key:
                match_key = key
                break

        if match_key is None:
            candidates.append({
                "candidate_id": cand["candidate_id"],
                "ticker": cand["ticker"],
                "contract_selection_status": "EXACT_BLOCKED_EVIDENCE_GAP",
                "blocker": "definition_request_group_not_found_for_candidate",
                "profitability_proof": "NO",
                "paper_live_eligibility": "NO",
            })
            continue

        selected, blocker = choose_contract(frames[match_key], cand)

        base = {
            "candidate_id": cand["candidate_id"],
            "ticker": cand["ticker"],
            "setup_type": cand["setup_type"],
            "accepted_setup_time": cand["accepted_setup_time"],
            "accepted_trigger": cand["accepted_trigger"],
            "accepted_invalidation": cand["accepted_invalidation"],
            "entry_status": "NOT_EVALUATED",
            "exit_status": "NOT_EVALUATED",
            "gross_pnl": None,
            "net_pnl": None,
            "profitability_proof": "NO",
            "paper_live_eligibility": "NO",
        }

        if blocker:
            base.update({
                "contract_selection_status": "EXACT_BLOCKED_EVIDENCE_GAP",
                "blocker": blocker,
            })
        else:
            base.update({
                "contract_selection_status": "CONTRACTS_SELECTED_FOR_QUOTE_TRADE_STATISTICS_REQUEST",
                "blocker": None,
                **selected,
            })

        candidates.append(base)

    selected_count = sum(1 for c in candidates if c["contract_selection_status"] == "CONTRACTS_SELECTED_FOR_QUOTE_TRADE_STATISTICS_REQUEST")
    blocked_count = len(candidates) - selected_count

    result = {
        "schema": "safe_fast_day55_definition_contract_selection_for_replay_ready_candidates_v1",
        "source_cost_result": "historical_signal_replay/results/day55_definition_cost_check_for_replay_ready_candidates.json",
        "source_definition_request": "historical_signal_replay/results/day55_definition_cost_request_for_replay_ready_candidates.json",
        "decision": "DEFINITION_CONTRACT_SELECTION_COMPLETE",
        "vendor_call_performed": True,
        "download_performed": True,
        "downloaded_schema": "definition",
        "quote_trade_statistics_download_performed": False,
        "candidate_count": len(candidates),
        "contracts_selected_count": selected_count,
        "exact_blocked_count": blocked_count,
        "definition_requests": downloaded,
        "candidates": candidates,
        "profitability_proof": "NO",
        "paper_live_eligibility": "NO",
        "next_action": "Move selected contracts to exact quote/trade/statistics cost request; blocked candidates remain exact contract-selection blockers.",
    }

    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")

    lines = [
        "# SAFE-FAST Day 55 Definition Contract Selection for Replay-Ready Candidates",
        "",
        "- Decision: `DEFINITION_CONTRACT_SELECTION_COMPLETE`",
        "- Vendor call performed: `true`",
        "- Download performed: `true`",
        "- Downloaded schema: `definition`",
        "- Quote/trade/statistics download performed: `false`",
        f"- Candidate count: `{len(candidates)}`",
        f"- Contracts selected: `{selected_count}`",
        f"- Exact blocked: `{blocked_count}`",
        "- Profitability proof: `NO`",
        "- Paper/live eligibility: `NO`",
        "",
        "## Next action",
        "",
        "Move selected contracts to exact quote/trade/statistics cost request.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")

    print("decision:", result["decision"])
    print("contracts_selected_count:", selected_count)
    print("exact_blocked_count:", blocked_count)
    print("next_action:", result["next_action"])

if __name__ == "__main__":
    main()
