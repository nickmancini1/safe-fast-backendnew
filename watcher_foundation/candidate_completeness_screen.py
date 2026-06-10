"""Local Day 39 candidate completeness screen.

Builds a structured 24-candidate pool from repo markdown handoff files and
prints a ranked stdout table. This module does not read live paths or make
trade decisions.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


ROOT = Path(__file__).resolve().parents[1]

FULL_20_WORKLIST = "SAFE_FAST_DAY38_FULL_20_CANDIDATE_BATCH_WORKLIST.md"
ADDED_4_REVIEW = "SAFE_FAST_DAY38_ADDED_4_FIXTURE_READY_REPLAY_REVIEW.md"
LARGE_POOL_PASS = "SAFE_FAST_DAY38_LARGE_SPY_QQQ_SOURCE_POOL_EXPANSION_PASS.md"
REPLACEMENT_PASS = "SAFE_FAST_DAY38_REPLACEMENT_SOURCE_POOL_PASS_FOR_BAD_ADDED_CANDIDATES.md"

REQUIRED_OUTPUT_FIELDS = (
    "candidate_id",
    "symbol",
    "setup_type",
    "source_lines",
    "setup_candle",
    "trigger",
    "invalidation",
    "freshness",
    "blocker",
    "outcome_window",
    "duplicate",
    "status",
    "reason",
    "next_action",
)

MINIMUM_READY_FIELDS = (
    "setup_candle",
    "trigger",
    "invalidation",
    "freshness",
    "blocker",
    "no_hindsight_boundary",
    "outcome_window",
)

NO_PROOF_ACCEPTED = True
PROFITABILITY_CLAIMED = False

_SOURCE_LINE_RE = re.compile(r"(CSV lines? \d+-\d+[^|.]*)")
_BACKTICK_RE = re.compile(r"`([^`]+)`")


@dataclass(frozen=True)
class Candidate:
    candidate_id: str
    symbol: str
    setup_type: str
    source_lines: str
    setup_candle: str
    trigger: str
    invalidation: str
    freshness: str
    blocker: str
    outcome_window: str
    no_hindsight_boundary: str
    duplicate: str
    status: str
    reason: str
    next_action: str

    def as_row(self) -> dict[str, str]:
        return {
            "candidate_id": self.candidate_id,
            "symbol": self.symbol,
            "setup_type": self.setup_type,
            "source_lines": self.source_lines,
            "setup_candle": self.setup_candle,
            "trigger": self.trigger,
            "invalidation": self.invalidation,
            "freshness": self.freshness,
            "blocker": self.blocker,
            "outcome_window": self.outcome_window,
            "duplicate": self.duplicate,
            "status": self.status,
            "reason": self.reason,
            "next_action": self.next_action,
        }


def build_candidate_pool() -> list[dict[str, str]]:
    """Return the normalized Day 39 24-candidate screen pool."""

    full_20 = _parse_full_20_worklist()
    added_4 = _parse_added_4_current_review()
    pool = full_20 + added_4
    if len(pool) != 24:
        raise ValueError(f"expected 24 candidates, found {len(pool)}")
    return [candidate.as_row() for candidate in rank_candidates(pool)]


def rank_candidates(candidates: Sequence[Candidate | dict[str, str]]) -> list[Candidate]:
    normalized = [
        candidate if isinstance(candidate, Candidate) else _candidate_from_row(candidate)
        for candidate in candidates
    ]
    return sorted(normalized, key=_rank_key)


def format_ranked_table(rows: Sequence[dict[str, str]]) -> str:
    headers = REQUIRED_OUTPUT_FIELDS
    table_rows = [[str(row[field]) for field in headers] for row in rows]
    widths = [
        max(len(header), *(len(row[index]) for row in table_rows))
        for index, header in enumerate(headers)
    ]
    header_line = " | ".join(header.ljust(widths[index]) for index, header in enumerate(headers))
    separator = " | ".join("-" * widths[index] for index in range(len(headers)))
    body = [
        " | ".join(value.ljust(widths[index]) for index, value in enumerate(row))
        for row in table_rows
    ]
    return "\n".join([header_line, separator, *body])


def main() -> None:
    print(format_ranked_table(build_candidate_pool()))


def _parse_full_20_worklist() -> list[Candidate]:
    rows = _markdown_table_candidate_lines(FULL_20_WORKLIST)
    candidates: list[Candidate] = []
    for line_number, cells in rows:
        if len(cells) != 8 or not cells[0].strip().isdigit():
            continue
        candidate_id = _strip_code(cells[1])
        symbol = cells[2].strip()
        setup_type = cells[3].strip()
        worklist_status = _strip_code(cells[4])
        proof_missing = cells[5].strip()
        decision = cells[6].strip()
        next_action = cells[7].strip()
        source_lines = _known_source_lines(candidate_id, FULL_20_WORKLIST, line_number, next_action)
        status = _screen_status(decision, worklist_status, duplicate=False)
        missing = _missing_fields_for_full_20(worklist_status, proof_missing)
        candidates.append(
            Candidate(
                candidate_id=candidate_id,
                symbol=symbol,
                setup_type=setup_type,
                source_lines=source_lines,
                setup_candle=_field_value("setup_candle", candidate_id, missing),
                trigger=_field_value("trigger", candidate_id, missing),
                invalidation=_field_value("invalidation", candidate_id, missing),
                freshness=_field_value("freshness", candidate_id, missing),
                blocker=_field_value("blocker", candidate_id, missing),
                outcome_window=_field_value("outcome_window", candidate_id, missing),
                no_hindsight_boundary=_field_value("no_hindsight_boundary", candidate_id, missing),
                duplicate=_duplicate_flag(candidate_id),
                status=status,
                reason=_reason(status, missing, worklist_status),
                next_action=next_action,
            )
        )
    return candidates


def _parse_added_4_current_review() -> list[Candidate]:
    large_rows = {
        _strip_code(cells[0]): (line_number, cells)
        for line_number, cells in _markdown_table_candidate_lines(LARGE_POOL_PASS)
        if len(cells) == 10 and _strip_code(cells[0]).startswith(("SPY-", "QQQ-"))
    }
    current = {
        "SPY-SOURCE-WINDOW-CONTINUATION-005": {
            "line": 40,
            "status": "replace",
            "freshness": "UNCLEAR",
            "blocker": "MISSING complete same-lifecycle/freshness and blocker/caution review",
            "next_action": "Replace with a cleaner non-overlapping SPY/QQQ Continuation or Clean Fast Break candidate.",
        },
        "QQQ-SOURCE-WINDOW-CONTINUATION-002": {
            "line": 55,
            "status": "replace",
            "freshness": "UNCLEAR",
            "blocker": "MISSING complete same-context/freshness and blocker/caution review",
            "next_action": "Replace with a cleaner non-overlapping QQQ Continuation or QQQ Clean Fast Break candidate.",
        },
        "SPY-SOURCE-WINDOW-CLEAN-FAST-BREAK-003": {
            "line": 70,
            "status": "blocked",
            "freshness": "MISSING",
            "blocker": "MISSING complete blocker/caution review",
            "next_action": "Keep blocked as a batch candidate only until a real replay fixture pass fills exact fields.",
        },
        "SPY-SOURCE-WINDOW-CONTINUATION-004": {
            "line": 85,
            "status": "blocked",
            "freshness": "UNCLEAR",
            "blocker": "MISSING complete blocker/caution review",
            "next_action": "Keep blocked as a batch candidate only until a real replay fixture pass fills exact fields.",
        },
    }
    candidates: list[Candidate] = []
    for candidate_id, info in current.items():
        line_number, cells = large_rows[candidate_id]
        source_file = _strip_code(cells[3])
        csv_lines = cells[4].strip()
        status = str(info["status"])
        freshness = str(info["freshness"])
        missing = [
            "setup_candle",
            "trigger",
            "invalidation",
            "outcome_window",
            "no_hindsight_boundary",
        ]
        if freshness == "MISSING":
            missing.append("freshness")
        missing.append("blocker")
        candidates.append(
            Candidate(
                candidate_id=candidate_id,
                symbol=cells[1].strip(),
                setup_type=cells[2].strip(),
                source_lines=(
                    f"{source_file} {csv_lines}; {LARGE_POOL_PASS}:{line_number}; "
                    f"{ADDED_4_REVIEW}:{info['line']}"
                ),
                setup_candle="MISSING",
                trigger="MISSING",
                invalidation="MISSING",
                freshness=freshness,
                blocker=str(info["blocker"]),
                outcome_window="MISSING",
                no_hindsight_boundary="MISSING",
                duplicate="no",
                status=status,
                reason=_reason(status, missing, "fixture_ready_review"),
                next_action=str(info["next_action"]),
            )
        )
    return candidates


def _markdown_table_candidate_lines(file_name: str) -> list[tuple[int, list[str]]]:
    path = ROOT / file_name
    result: list[tuple[int, list[str]]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and not set(cells[0]) <= {"-", ":", " "}:
            result.append((line_number, cells))
    return result


def _known_source_lines(candidate_id: str, file_name: str, line_number: int, next_action: str) -> str:
    known = {
        "SPY-SOURCE-WINDOW-CONTINUATION-002": (
            "historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv "
            "CSV lines 156-169"
        ),
        "SPY-SOURCE-WINDOW-CONTINUATION-003": (
            "historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_SPY_source.csv "
            "CSV lines 170-197"
        ),
        "QQQ-SOURCE-WINDOW-CLEAN-FAST-BREAK-002": (
            "historical_signal_replay/source_data/incoming/first_real_historical_replay_v1_QQQ_source.csv "
            "CSV lines 66-86"
        ),
    }
    match = _SOURCE_LINE_RE.search(next_action)
    source = known.get(candidate_id, match.group(1) if match else "source rows MISSING")
    replacement_ref = ""
    if candidate_id in known:
        replacement_ref = f"; {REPLACEMENT_PASS}:{_replacement_line(candidate_id)}"
    return f"{source}; {file_name}:{line_number}{replacement_ref}"


def _replacement_line(candidate_id: str) -> int:
    lines = {
        "SPY-SOURCE-WINDOW-CONTINUATION-002": 66,
        "SPY-SOURCE-WINDOW-CONTINUATION-003": 67,
        "QQQ-SOURCE-WINDOW-CLEAN-FAST-BREAK-002": 68,
    }
    return lines[candidate_id]


def _screen_status(decision: str, worklist_status: str, *, duplicate: bool) -> str:
    if duplicate:
        return "blocked"
    decision_text = decision.strip().lower()
    status_text = worklist_status.strip().lower()
    if decision_text == "drop" or "drop" in status_text:
        return "drop"
    if decision_text == "replace" or "unavailable" in status_text:
        return "replace"
    return "blocked"


def _missing_fields_for_full_20(worklist_status: str, proof_missing: str) -> list[str]:
    lower = f"{worklist_status} {proof_missing}".lower()
    missing: list[str] = []
    if "setup-time" in lower or "setup_time" in lower or "setup-time review" in lower:
        missing.append("setup_candle")
    if "trigger" in lower:
        missing.append("trigger")
    if "invalidation" in lower or "failure level" in lower:
        missing.append("invalidation")
    if "freshness" in lower or "final-signal" in lower:
        missing.append("freshness")
    if "blocker" in lower or "caution" in lower:
        missing.append("blocker")
    if "no-hindsight" in lower:
        missing.append("no_hindsight_boundary")
    if "terminal outcome" in lower or "outcome" in lower:
        missing.append("outcome_window")
    if not missing:
        missing.extend(MINIMUM_READY_FIELDS)
    return sorted(set(missing))


def _field_value(field_name: str, candidate_id: str, missing: Sequence[str]) -> str:
    if field_name in missing:
        return "MISSING"
    known_values = {
        "SPY-SOURCE-WINDOW-CONTINUATION-002": {
            "setup_candle": "2026-04-17T09:30:00-04:00",
            "trigger": "702.78 candidate level",
            "invalidation": "698.53 candidate level",
            "no_hindsight_boundary": "source-only boundary recorded",
        }
    }
    return known_values.get(candidate_id, {}).get(field_name, "MISSING")


def _duplicate_flag(candidate_id: str) -> str:
    duplicates = {
        "SPY-SOURCE-WINDOW-CONTINUATION-002",
        "SPY-SOURCE-WINDOW-CONTINUATION-003",
        "QQQ-SOURCE-WINDOW-CLEAN-FAST-BREAK-002",
    }
    return "yes" if candidate_id in duplicates else "no"


def _reason(status: str, missing: Sequence[str], prior_status: str) -> str:
    if status == "drop":
        return f"drop/replace path only; prior status {prior_status}"
    if status == "replace":
        return f"replace path only; missing {', '.join(missing) or 'complete source window'}"
    if missing:
        return f"blocked: missing {', '.join(missing)}"
    return "blocked: ready promotion is not allowed without minimum setup-time completeness"


def _rank_key(candidate: Candidate) -> tuple[int, int, str]:
    status_rank = {"ready": 0, "blocked": 1, "replace": 2, "drop": 3}
    completeness = _completeness_score(candidate)
    duplicate_penalty = 1 if candidate.duplicate == "yes" else 0
    return (status_rank.get(candidate.status, 9), duplicate_penalty, -completeness, candidate.candidate_id)


def _completeness_score(candidate: Candidate) -> int:
    values = {
        "setup_candle": candidate.setup_candle,
        "trigger": candidate.trigger,
        "invalidation": candidate.invalidation,
        "freshness": candidate.freshness,
        "blocker": candidate.blocker,
        "no_hindsight_boundary": candidate.no_hindsight_boundary,
        "outcome_window": candidate.outcome_window,
    }
    return sum(1 for value in values.values() if value and "MISSING" not in value and "UNCLEAR" not in value)


def _candidate_from_row(row: dict[str, str]) -> Candidate:
    return Candidate(
        candidate_id=row["candidate_id"],
        symbol=row["symbol"],
        setup_type=row["setup_type"],
        source_lines=row["source_lines"],
        setup_candle=row["setup_candle"],
        trigger=row["trigger"],
        invalidation=row["invalidation"],
        freshness=row["freshness"],
        blocker=row["blocker"],
        outcome_window=row["outcome_window"],
        no_hindsight_boundary=row.get("no_hindsight_boundary", "MISSING"),
        duplicate=row["duplicate"],
        status=row["status"],
        reason=row["reason"],
        next_action=row["next_action"],
    )


def _strip_code(value: str) -> str:
    match = _BACKTICK_RE.search(value.strip())
    return match.group(1) if match else value.strip()


if __name__ == "__main__":
    main()
