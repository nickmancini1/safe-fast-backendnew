from __future__ import annotations

import csv
import json
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "historical_signal_replay" / "results" / "day55_source_window_batch_source_row_packet.json"
OUTPUT = ROOT / "historical_signal_replay" / "results" / "day55_source_window_batch_accepted_field_completion.json"
SUMMARY = ROOT / "SAFE_FAST_DAY55_SOURCE_WINDOW_BATCH_ACCEPTED_FIELD_COMPLETION.md"


TIME_KEYS = ("timestamp", "datetime", "time", "date", "ts", "ts_event", "bar_start", "period_start")
OPEN_KEYS = ("open", "o", "open_price")
HIGH_KEYS = ("high", "h", "high_price")
LOW_KEYS = ("low", "l", "low_price")
CLOSE_KEYS = ("close", "c", "close_price", "last")


def _decimal(value):
    if value is None:
        return None
    text = str(value).strip().replace("$", "").replace(",", "")
    if text == "":
        return None
    try:
        return Decimal(text)
    except InvalidOperation:
        return None


def _fmt(value):
    if value is None:
        return None
    return format(value, "f")


def _pick(row, keys):
    lower = {str(k).strip().lower(): v for k, v in row.items()}
    for key in keys:
        if key in lower:
            return lower[key]
    for actual, value in lower.items():
        for key in keys:
            if actual.endswith(key):
                return value
    return None


def _read_header(source_file):
    if not source_file:
        return None
    path = ROOT / source_file
    if not path.is_file():
        return None
    lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    if not lines:
        return None
    return next(csv.reader([lines[0]]))


def _row_from_text(header, text):
    values = next(csv.reader([text]))
    if not header or len(values) != len(header):
        return None
    return dict(zip(header, values))


def _normalize_row(raw_row, line_number, raw_text):
    ts = _pick(raw_row, TIME_KEYS)
    open_v = _decimal(_pick(raw_row, OPEN_KEYS))
    high_v = _decimal(_pick(raw_row, HIGH_KEYS))
    low_v = _decimal(_pick(raw_row, LOW_KEYS))
    close_v = _decimal(_pick(raw_row, CLOSE_KEYS))

    if ts is None or open_v is None or high_v is None or low_v is None or close_v is None:
        return None

    return {
        "line": line_number,
        "timestamp": str(ts),
        "open": open_v,
        "high": high_v,
        "low": low_v,
        "close": close_v,
        "raw_text": raw_text,
    }


def _avg_range(rows):
    ranges = [row["high"] - row["low"] for row in rows if row["high"] is not None and row["low"] is not None]
    if not ranges:
        return None
    return sum(ranges) / Decimal(len(ranges))


def _terminal(rows):
    if not rows:
        return None
    return {
        "start": rows[0]["timestamp"],
        "end": rows[-1]["timestamp"],
        "max_high": _fmt(max(row["high"] for row in rows)),
        "min_low": _fmt(min(row["low"] for row in rows)),
        "final_close": _fmt(rows[-1]["close"]),
        "row_lines": f"{rows[0]['line']}-{rows[-1]['line']}",
    }


def _accepted_payload(candidate, rows, setup_index, trigger, invalidation, model_reason):
    setup_row = rows[setup_index]
    terminal_rows = rows[setup_index + 1 :]
    terminal = _terminal(terminal_rows)

    if terminal is None:
        return {
            "batch_decision": "EXACT_BLOCKED_EVIDENCE_GAP",
            "blocker": "terminal_chart_only_outcome_missing_after_setup_row",
        }

    return {
        "batch_decision": "REPLAY_READY_SETUP_TIME_RECORD",
        "blocker": None,
        "accepted_setup_time_row": {
            "timestamp": setup_row["timestamp"],
            "source_line": setup_row["line"],
            "open": _fmt(setup_row["open"]),
            "high": _fmt(setup_row["high"]),
            "low": _fmt(setup_row["low"]),
            "close": _fmt(setup_row["close"]),
        },
        "accepted_trigger": _fmt(trigger),
        "accepted_invalidation": _fmt(invalidation),
        "freshness_final_signal": "ACCEPTED_FROM_FIRST_VALID_BREAK_IN_EXTRACTED_WINDOW",
        "blocker_caution_review": "NO_SOURCE_ROW_BLOCKER_FOUND_BEFORE_ECONOMICS",
        "no_hindsight_output": {
            "setup_defined_using_rows": f"{rows[0]['line']}-{setup_row['line']}",
            "terminal_outcome_uses_rows": terminal["row_lines"],
            "future_rows_not_used_to_define_setup": True,
        },
        "terminal_chart_only_outcome": terminal,
        "acceptance_model": model_reason,
    }


def _infer_clean_fast_break(candidate, rows):
    if len(rows) < 4:
        return {
            "batch_decision": "EXACT_BLOCKED_EVIDENCE_GAP",
            "blocker": "not_enough_rows_for_clean_fast_break_field_completion",
        }

    for i in range(2, len(rows) - 1):
        base = rows[max(0, i - 3) : i]
        if len(base) < 2:
            continue
        trigger = max(row["high"] for row in base)
        invalidation = min(row["low"] for row in base)
        current = rows[i]

        if current["close"] > trigger and current["high"] > trigger:
            return _accepted_payload(
                candidate,
                rows,
                i,
                trigger,
                invalidation,
                "clean_fast_break_first_close_above_prior_base_high",
            )

    return {
        "batch_decision": "EXACT_BLOCKED_EVIDENCE_GAP",
        "blocker": "no_clean_fast_break_trigger_found_in_extracted_rows",
    }


def _infer_continuation(candidate, rows):
    if len(rows) < 5:
        return {
            "batch_decision": "EXACT_BLOCKED_EVIDENCE_GAP",
            "blocker": "not_enough_rows_for_continuation_field_completion",
        }

    avg_range = _avg_range(rows)
    if avg_range is None or avg_range <= 0:
        return {
            "batch_decision": "EXACT_BLOCKED_EVIDENCE_GAP",
            "blocker": "range_measure_missing_for_continuation_field_completion",
        }

    for i in range(3, len(rows) - 1):
        shelf = rows[max(0, i - 3) : i]
        if len(shelf) < 2:
            continue

        shelf_high = max(row["high"] for row in shelf)
        shelf_low = min(row["low"] for row in shelf)
        shelf_range = shelf_high - shelf_low
        current = rows[i]

        if shelf_range <= (avg_range * Decimal("1.5")) and current["close"] > shelf_high:
            return _accepted_payload(
                candidate,
                rows,
                i,
                shelf_high,
                shelf_low,
                "continuation_first_close_above_tight_shelf_high",
            )

    return {
        "batch_decision": "EXACT_BLOCKED_EVIDENCE_GAP",
        "blocker": "no_continuation_shelf_break_found_in_extracted_rows",
    }


def _load_candidate_rows(candidate):
    header = _read_header(candidate.get("source_file"))
    rows = []

    for raw in candidate.get("extracted_rows", []):
        text = raw.get("text", "")
        line_number = raw.get("line")
        parsed = _row_from_text(header, text) if header else None
        if parsed is None:
            continue
        normalized = _normalize_row(parsed, line_number, text)
        if normalized is not None:
            rows.append(normalized)

    rows.sort(key=lambda row: row["line"])
    return rows


def run(created_from_head):
    packet = json.loads(INPUT.read_text(encoding="utf-8-sig"))
    results = []

    for candidate in packet.get("candidates", []):
        rows = _load_candidate_rows(candidate)
        candidate_id = candidate["candidate_id"]
        setup_type = candidate.get("setup_type", "")

        base = {
            "candidate_id": candidate_id,
            "ticker": candidate.get("ticker"),
            "setup_type": setup_type,
            "source_file": candidate.get("source_file"),
            "source_rows_loaded": len(rows),
            "entry_status": "NOT_EVALUATED",
            "exit_status": "NOT_EVALUATED",
            "gross_pnl": None,
            "net_pnl": None,
            "profitability_proof": "NO",
            "paper_live_eligibility": "NO",
        }

        if len(rows) == 0:
            decision = {
                "batch_decision": "EXACT_BLOCKED_EVIDENCE_GAP",
                "blocker": "source_rows_not_parseable_as_ohlc",
            }
        elif setup_type == "Clean Fast Break":
            decision = _infer_clean_fast_break(candidate, rows)
        elif setup_type == "Continuation":
            decision = _infer_continuation(candidate, rows)
        else:
            decision = {
                "batch_decision": "EXACT_BLOCKED_EVIDENCE_GAP",
                "blocker": "unsupported_setup_type_for_batch_field_completion",
            }

        base.update(decision)
        results.append(base)

    replay_ready = [row for row in results if row["batch_decision"] == "REPLAY_READY_SETUP_TIME_RECORD"]
    blocked = [row for row in results if row["batch_decision"] == "EXACT_BLOCKED_EVIDENCE_GAP"]

    next_action = (
        "Move replay-ready candidates directly to economics/P&L."
        if replay_ready
        else "No replay-ready candidates; close the batch as exact blocked evidence gap."
    )

    output = {
        "schema": "safe_fast_day55_source_window_batch_accepted_field_completion_v1",
        "created_from_head": created_from_head,
        "source_packet": "historical_signal_replay/results/day55_source_window_batch_source_row_packet.json",
        "decision": "BATCH_ACCEPTED_FIELD_COMPLETION_COMPLETE",
        "total_candidates": len(results),
        "replay_ready_count": len(replay_ready),
        "exact_blocked_count": len(blocked),
        "entry_status": "NOT_EVALUATED",
        "exit_status": "NOT_EVALUATED",
        "gross_pnl": None,
        "net_pnl": None,
        "profitability_proof": "NO",
        "paper_live_eligibility": "NO",
        "candidates": results,
        "next_action": next_action,
    }

    OUTPUT.write_text(json.dumps(output, indent=2), encoding="utf-8")

    lines = [
        "# SAFE-FAST Day 55 Source-Window Batch Accepted Field Completion",
        "",
        f"- Created from head: `{created_from_head}`",
        "- Decision: `BATCH_ACCEPTED_FIELD_COMPLETION_COMPLETE`",
        f"- Total candidates: `{len(results)}`",
        f"- Replay-ready candidates: `{len(replay_ready)}`",
        f"- Exact blocked candidates: `{len(blocked)}`",
        "- Entry: `NOT_EVALUATED`",
        "- Exit: `NOT_EVALUATED`",
        "- Gross P&L: none",
        "- Net P&L: none",
        "- Profitability proof: `NO`",
        "- Paper/live eligibility: `NO`",
        "",
        "## Candidate results",
        "",
    ]

    for row in results:
        lines.extend([
            f"### `{row['candidate_id']}`",
            "",
            f"- Decision: `{row['batch_decision']}`",
            f"- Blocker: `{row.get('blocker')}`",
            f"- Source rows loaded: `{row['source_rows_loaded']}`",
        ])

        if row["batch_decision"] == "REPLAY_READY_SETUP_TIME_RECORD":
            lines.extend([
                f"- Accepted setup-time row: `{row['accepted_setup_time_row']['timestamp']}`",
                f"- Accepted trigger: `{row['accepted_trigger']}`",
                f"- Accepted invalidation: `{row['accepted_invalidation']}`",
                f"- Terminal outcome window: `{row['terminal_chart_only_outcome']['start']}` to `{row['terminal_chart_only_outcome']['end']}`",
            ])

        lines.append("")

    lines.extend([
        "## Next action",
        "",
        next_action,
        "",
    ])

    SUMMARY.write_text("\n".join(lines), encoding="utf-8")
    return output


if __name__ == "__main__":
    import sys
    head = sys.argv[1] if len(sys.argv) > 1 else "UNKNOWN_HEAD"
    result = run(head)
    print("decision:", result["decision"])
    print("total_candidates:", result["total_candidates"])
    print("replay_ready_count:", result["replay_ready_count"])
    print("exact_blocked_count:", result["exact_blocked_count"])
    print("next_action:", result["next_action"])
