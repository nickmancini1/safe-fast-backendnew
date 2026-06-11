"""Strict local source-pool intake for Day 39 candidate expansion.

The helper inspects the existing repo-backed 24-candidate screen and admits
only rows with setup-time row, trigger, invalidation, source reference,
no-hindsight boundary, and outcome input already present. It prints to stdout
only and does not create reports.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Sequence

from watcher_foundation import candidate_completeness_screen as screen


INTAKE_OUTPUT_FIELDS = (
    "candidate_id",
    "symbol",
    "setup_type",
    "source_file",
    "source_lines_section",
    "setup_candle",
    "trigger",
    "invalidation",
    "freshness",
    "blocker",
    "no_hindsight_boundary",
    "outcome_window",
    "duplicate",
    "status",
    "reason",
    "next_action",
)

MINIMUM_STRICT_INTAKE_TARGET = 20
MINIMUM_CLOSE_READY_TARGET = 5

NO_PROOF_ACCEPTED = True
PROFITABILITY_CLAIMED = False

UNRESOLVED_MARKERS = ("missing", "unclear", "incomplete")


@dataclass(frozen=True)
class IntakeRow:
    candidate_id: str
    symbol: str
    setup_type: str
    source_file: str
    source_lines_section: str
    setup_candle: str
    trigger: str
    invalidation: str
    freshness: str
    blocker: str
    no_hindsight_boundary: str
    outcome_window: str
    duplicate: str
    status: str
    reason: str
    next_action: str

    def as_row(self) -> dict[str, str]:
        return {
            "candidate_id": self.candidate_id,
            "symbol": self.symbol,
            "setup_type": self.setup_type,
            "source_file": self.source_file,
            "source_lines_section": self.source_lines_section,
            "setup_candle": self.setup_candle,
            "trigger": self.trigger,
            "invalidation": self.invalidation,
            "freshness": self.freshness,
            "blocker": self.blocker,
            "no_hindsight_boundary": self.no_hindsight_boundary,
            "outcome_window": self.outcome_window,
            "duplicate": self.duplicate,
            "status": self.status,
            "reason": self.reason,
            "next_action": self.next_action,
        }


def build_source_pool_intake() -> dict[str, object]:
    inspected = screen.build_candidate_pool()
    accepted = [_to_intake_row(row) for row in inspected if _strictly_source_backed(row)]
    ranked = sorted(accepted, key=_rank_key)
    status_counts = Counter(row.status for row in ranked)
    duplicate_count = sum(1 for row in ranked if row.duplicate == "yes")
    close_ready_count = sum(1 for row in ranked if _is_close_ready(row))
    top_blocker = _top_remaining_blocker_family(ranked, len(inspected))

    return {
        "source_pool_rows_inspected": len(inspected),
        "accepted_intake_count": len(ranked),
        "intake_ready_count": status_counts.get("intake-ready", 0),
        "blocked_count": status_counts.get("blocked", 0),
        "drop_count": status_counts.get("drop", 0),
        "replace_count": status_counts.get("replace", 0),
        "duplicate_count": duplicate_count,
        "close_ready_count": close_ready_count,
        "at_least_5_intake_ready_or_close_ready": (
            status_counts.get("intake-ready", 0) >= MINIMUM_CLOSE_READY_TARGET
            or close_ready_count >= MINIMUM_CLOSE_READY_TARGET
        ),
        "maximum_strict_candidates_found": len(ranked),
        "exact_blocker": _exact_blocker(len(ranked), top_blocker),
        "source_files_inspected": _source_files_inspected(inspected),
        "smallest_next_evidence_backed_fix": (
            "complete freshness/final-signal and blocker/caution review for the six source-backed rows, "
            "then add more strict rows only from accepted local source/replay material"
        ),
        "top_remaining_blocker_family": top_blocker,
        "accepted_rows": [row.as_row() for row in ranked],
        "no_generated_reports_or_logs": True,
        "proof_accepted": False,
        "profitability_claimed": False,
    }


def format_intake_report(result: dict[str, object]) -> str:
    lines = [
        f"source-pool rows inspected: {result['source_pool_rows_inspected']}",
        f"accepted intake count: {result['accepted_intake_count']}",
        f"intake-ready count: {result['intake_ready_count']}",
        (
            "blocked/drop/replace/duplicate counts: "
            f"{result['blocked_count']}/{result['drop_count']}/"
            f"{result['replace_count']}/{result['duplicate_count']}"
        ),
        f"close-ready count: {result['close_ready_count']}",
        (
            "at least 5 intake-ready or close-ready candidates now exist: "
            f"{'YES' if result['at_least_5_intake_ready_or_close_ready'] else 'NO'}"
        ),
        f"maximum strict candidates found: {result['maximum_strict_candidates_found']}",
        f"exact blocker: {result['exact_blocker']}",
        f"source files inspected: {', '.join(result['source_files_inspected'])}",
        f"smallest next evidence-backed fix: {result['smallest_next_evidence_backed_fix']}",
        f"top remaining blocker family: {result['top_remaining_blocker_family']}",
        "ranked intake table:",
        _format_table(result["accepted_rows"]),
    ]
    return "\n".join(lines)


def main() -> None:
    print(format_intake_report(build_source_pool_intake()))


def _strictly_source_backed(row: dict[str, str]) -> bool:
    if row["duplicate"] == "yes" or row["status"] in {"drop", "replace"}:
        return False
    required = (
        "source_lines",
        "setup_candle",
        "trigger",
        "invalidation",
        "no_hindsight_boundary",
        "outcome_window",
    )
    return all(_has_strict_value(row.get(field, "MISSING")) for field in required)


def _to_intake_row(row: dict[str, str]) -> IntakeRow:
    source_file, source_section = _split_source(row["source_lines"])
    status = _intake_status(row)
    return IntakeRow(
        candidate_id=row["candidate_id"],
        symbol=row["symbol"],
        setup_type=row["setup_type"],
        source_file=_source_file_only(source_file),
        source_lines_section=_source_section(source_file, source_section),
        setup_candle=row["setup_candle"],
        trigger=row["trigger"],
        invalidation=row["invalidation"],
        freshness=row["freshness"],
        blocker=row["blocker"],
        no_hindsight_boundary=row["no_hindsight_boundary"],
        outcome_window=row["outcome_window"],
        duplicate=row["duplicate"],
        status=status,
        reason=_reason(status, row),
        next_action=row["next_action"],
    )


def _intake_status(row: dict[str, str]) -> str:
    if row["status"] in {"drop", "replace"}:
        return row["status"]
    if row["duplicate"] == "yes":
        return "blocked"
    if _has_resolved_value(row["freshness"]) and _has_resolved_value(row["blocker"]):
        return "intake-ready"
    return "blocked"


def _reason(status: str, row: dict[str, str]) -> str:
    if status == "intake-ready":
        return "strict source-backed fields complete for intake only; not proof"
    if row["duplicate"] == "yes":
        return "duplicate/already counted; not eligible for intake-ready"
    if _has_unresolved_marker(row["freshness"]) and _has_unresolved_marker(row["blocker"]):
        return "blocked: freshness/final-signal and blocker/caution remain unclear"
    if _has_unresolved_marker(row["freshness"]):
        return "blocked: freshness/final-signal remains unclear"
    if _has_unresolved_marker(row["blocker"]):
        return "blocked: blocker/caution remains unclear"
    return "blocked: strict source intake accepted but proof remains unavailable"


def _rank_key(row: IntakeRow) -> tuple[int, int, str]:
    status_rank = {"intake-ready": 0, "blocked": 1, "replace": 2, "drop": 3}
    completeness = sum(
        1
        for value in (
            row.setup_candle,
            row.trigger,
            row.invalidation,
            row.freshness,
            row.blocker,
            row.no_hindsight_boundary,
            row.outcome_window,
        )
        if _has_resolved_value(value)
    )
    return (status_rank.get(row.status, 9), -completeness, row.candidate_id)


def _is_close_ready(row: IntakeRow) -> bool:
    return (
        row.status == "blocked"
        and row.duplicate == "no"
        and _has_strict_value(row.setup_candle)
        and _has_strict_value(row.trigger)
        and _has_strict_value(row.invalidation)
        and _has_strict_value(row.no_hindsight_boundary)
        and _has_strict_value(row.outcome_window)
        and (_has_unresolved_marker(row.freshness) or _has_unresolved_marker(row.blocker))
    )


def _top_remaining_blocker_family(rows: Sequence[IntakeRow], inspected_count: int) -> str:
    if not rows:
        return f"strict_intake_gap: 0 accepted from {inspected_count} inspected rows"
    unclear_freshness = sum(1 for row in rows if _has_unresolved_marker(row.freshness))
    unclear_blocker = sum(1 for row in rows if _has_unresolved_marker(row.blocker))
    if unclear_freshness and unclear_blocker:
        return "freshness/final-signal plus blocker/caution unresolved"
    if unclear_freshness:
        return "freshness/final-signal unresolved"
    if unclear_blocker:
        return "blocker/caution unresolved"
    return "no blocker family among accepted strict rows"


def _exact_blocker(accepted_count: int, top_blocker: str) -> str:
    if accepted_count < MINIMUM_STRICT_INTAKE_TARGET:
        return (
            f"only {accepted_count} strict candidates found; current local docs/data do not support "
            f"{MINIMUM_STRICT_INTAKE_TARGET}-50 strict candidates; {top_blocker}"
        )
    return top_blocker


def _source_files_inspected(rows: Sequence[dict[str, str]]) -> list[str]:
    files = {_source_file_only(_split_source(row["source_lines"])[0]) for row in rows}
    files.discard("")
    return sorted(files)


def _split_source(source_lines: str) -> tuple[str, str]:
    if ";" not in source_lines:
        return source_lines, source_lines
    first, rest = source_lines.split(";", 1)
    return first.strip(), rest.strip()


def _source_file_only(value: str) -> str:
    if "source rows MISSING" in value:
        return ""
    for marker in (".csv", ".jsonl", ".md"):
        if marker in value:
            return value[: value.index(marker) + len(marker)]
    return value


def _source_section(source_file: str, source_section: str) -> str:
    file_only = _source_file_only(source_file)
    prefix = source_file[len(file_only) :].strip()
    if prefix:
        return f"{prefix}; {source_section}"
    return source_section


def _has_strict_value(value: object) -> bool:
    text = _normalized_text(value)
    return bool(text) and "missing" not in text and "source rows missing" not in text


def _has_resolved_value(value: object) -> bool:
    return _has_strict_value(value) and not _has_unresolved_marker(value)


def _has_unresolved_marker(value: object) -> bool:
    text = _normalized_text(value)
    return not text or any(marker in text for marker in UNRESOLVED_MARKERS)


def _normalized_text(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()


def _format_table(rows: object) -> str:
    table_rows = list(rows) if isinstance(rows, list) else []
    headers = INTAKE_OUTPUT_FIELDS
    if not table_rows:
        return "NO STRICT INTAKE ROWS"
    values = [[str(row[field]) for field in headers] for row in table_rows]
    widths = [
        max(len(header), *(len(value_row[index]) for value_row in values))
        for index, header in enumerate(headers)
    ]
    header_line = " | ".join(header.ljust(widths[index]) for index, header in enumerate(headers))
    separator = " | ".join("-" * widths[index] for index in range(len(headers)))
    body = [
        " | ".join(value.ljust(widths[index]) for index, value in enumerate(value_row))
        for value_row in values
    ]
    return "\n".join([header_line, separator, *body])


if __name__ == "__main__":
    main()
