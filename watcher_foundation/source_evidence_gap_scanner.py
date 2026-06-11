"""Source-evidence gap scanner for parked Day 39 rows.

The scanner inspects current local CSV/log schemas for the four parked paths
and reports the exact missing fields or source-backed rules. It does not
create report files, reactivate rows, accept proof, or claim profitability.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from watcher_foundation import candidate_freshness_blocker_rule_gate as rule_gate


ROOT = Path(__file__).resolve().parents[1]

NO_PROOF_ACCEPTED = True
PROFITABILITY_CLAIMED = False
INTAKE_READY_COUNT = 0
PARKED_COUNT = 4
REPLACE_COUNT = 3
PARKED_STATUS = "parked/source_data_insufficient"

PARKED_CANDIDATE_IDS = (
    "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001",
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003",
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002",
    "SPY-REAL-HISTORICAL-IDEAL-001",
)

REQUIRED_EVIDENCE_FAMILIES = (
    "QQQ gap-context completeness",
    "Clean Fast Break stale/spent expiry",
    "Clean Fast Break higher-base/fresh-break expiry",
    "Clean Fast Break initial-break expiry",
    "SPY Ideal stale/spent expiry",
    "complete context/caution fields",
)

SOURCE_FILES = {
    "qqq_csv": (
        "historical_signal_replay/source_data/incoming/"
        "first_real_historical_replay_v1_QQQ_source.csv"
    ),
    "spy_csv": (
        "historical_signal_replay/source_data/incoming/"
        "first_real_historical_replay_v1_SPY_source.csv"
    ),
    "qqq_cfb_log": (
        "historical_signal_replay/reports/"
        "first_real_qqq_clean_fast_break_replay_v1_signal_log.jsonl"
    ),
    "spy_cfb_log": (
        "historical_signal_replay/reports/"
        "third_real_spy_clean_fast_break_replay_v1_signal_log.jsonl"
    ),
    "spy_ideal_log": (
        "historical_signal_replay/reports/"
        "second_real_spy_ideal_replay_v1_signal_log.jsonl"
    ),
}

COMMON_CONTEXT_CAUTION_FIELDS = (
    "context_24h_status",
    "macro_context_status",
    "iv_context_status",
    "event_context_status",
    "room_status",
    "option_context_status",
    "headline_context_status",
    "execution_context_status",
    "complete_caution_review_status",
)


@dataclass(frozen=True)
class GapRequirement:
    candidate_id: str
    symbol: str
    setup_type: str
    evidence_family: str
    required_fields_or_rule_names: tuple[str, ...]
    source_files_checked: tuple[str, ...]
    source_rows_or_log_lines_checked: str
    existing_source_fields_found: tuple[str, ...]
    missing_field_names_or_rule_names: tuple[str, ...]
    current_repo_has_required_evidence: bool
    current_repo_data_sufficient_for_row: bool
    parked_status: str
    proof_allowed: bool

    def as_row(self) -> dict[str, object]:
        return {
            "candidate_id": self.candidate_id,
            "symbol": self.symbol,
            "setup_type": self.setup_type,
            "evidence_family": self.evidence_family,
            "required_fields_or_rule_names": self.required_fields_or_rule_names,
            "source_files_checked": self.source_files_checked,
            "source_rows_or_log_lines_checked": self.source_rows_or_log_lines_checked,
            "existing_source_fields_found": self.existing_source_fields_found,
            "missing_field_names_or_rule_names": self.missing_field_names_or_rule_names,
            "current_repo_has_required_evidence": self.current_repo_has_required_evidence,
            "current_repo_data_sufficient_for_row": self.current_repo_data_sufficient_for_row,
            "parked_status": self.parked_status,
            "proof_allowed": self.proof_allowed,
        }


def build_gap_scan() -> dict[str, object]:
    schemas = _load_source_schemas()
    rows = _build_gap_rows(schemas)
    current_repo_data_sufficient_by_candidate = {
        candidate_id: all(
            bool(row.current_repo_has_required_evidence)
            for row in rows
            if row.candidate_id == candidate_id
        )
        for candidate_id in PARKED_CANDIDATE_IDS
    }

    return {
        "parked_rows_covered": len(current_repo_data_sufficient_by_candidate),
        "parked_candidate_ids": PARKED_CANDIDATE_IDS,
        "required_evidence_families": REQUIRED_EVIDENCE_FAMILIES,
        "required_evidence_families_represented": tuple(
            sorted({row.evidence_family for row in rows})
        ),
        "gap_rows": [row.as_row() for row in rows],
        "gap_row_count": len(rows),
        "current_repo_data_sufficient_by_candidate": (
            current_repo_data_sufficient_by_candidate
        ),
        "intake_ready_count": INTAKE_READY_COUNT,
        "parked_count": PARKED_COUNT,
        "replace_count": REPLACE_COUNT,
        "proof_accepted": False,
        "profitability_claimed": False,
        "no_generated_reports_or_logs": True,
        "smallest_next_action": (
            "source the missing gap-context, setup-specific expiry-rule, and "
            "complete context/caution fields before any parked row can be reactivated"
        ),
    }


def format_gap_scan_report(result: dict[str, object]) -> str:
    lines = [
        "SAFE-FAST source-evidence gap scanner",
        f"parked rows covered: {result['parked_rows_covered']}",
        f"gap rows: {result['gap_row_count']}",
        f"intake-ready count: {result['intake_ready_count']}",
        f"parked count: {result['parked_count']}",
        f"replace count: {result['replace_count']}",
        "required evidence families represented: "
        + "; ".join(result["required_evidence_families_represented"]),
        "current repo data sufficient by row: "
        + "; ".join(
            f"{candidate_id}={'YES' if has_data else 'NO'}"
            for candidate_id, has_data in result[
                "current_repo_data_sufficient_by_candidate"
            ].items()
        ),
        "gap table:",
        _format_table(result["gap_rows"]),
        f"smallest next action: {result['smallest_next_action']}",
        "proof accepted: NO",
        "profitability claim made: NO",
    ]
    return "\n".join(lines)


def main() -> None:
    print(format_gap_scan_report(build_gap_scan()))


def _load_source_schemas() -> dict[str, object]:
    return {
        "qqq_csv_headers": _csv_headers(SOURCE_FILES["qqq_csv"]),
        "spy_csv_headers": _csv_headers(SOURCE_FILES["spy_csv"]),
        "qqq_cfb_log_keys": _jsonl_keys(SOURCE_FILES["qqq_cfb_log"]),
        "spy_cfb_log_keys": _jsonl_keys(SOURCE_FILES["spy_cfb_log"]),
        "spy_ideal_log_keys": _jsonl_keys(SOURCE_FILES["spy_ideal_log"]),
    }


def _build_gap_rows(schemas: dict[str, object]) -> tuple[GapRequirement, ...]:
    qqq_csv_headers = tuple(schemas["qqq_csv_headers"])
    spy_csv_headers = tuple(schemas["spy_csv_headers"])
    qqq_cfb_log_keys = tuple(schemas["qqq_cfb_log_keys"])
    spy_cfb_log_keys = tuple(schemas["spy_cfb_log_keys"])
    spy_ideal_log_keys = tuple(schemas["spy_ideal_log_keys"])

    rows = (
        _requirement(
            candidate_id="QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001",
            symbol="QQQ",
            setup_type="Clean Fast Break",
            evidence_family="QQQ gap-context completeness",
            required=("gap_context_status", "gap_context_as_of", "gap_context_reviewed_before_signal"),
            checked=(SOURCE_FILES["qqq_csv"], SOURCE_FILES["qqq_cfb_log"]),
            checked_lines="QQQ source CSV line 132; QQQ Clean Fast Break log lines 3-4",
            available_fields=qqq_csv_headers + qqq_cfb_log_keys,
        ),
        _requirement(
            candidate_id="QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001",
            symbol="QQQ",
            setup_type="Clean Fast Break",
            evidence_family="Clean Fast Break stale/spent expiry",
            required=(
                "clean_fast_break_stale_spent_expiry_rule",
                "clean_fast_break_expiry_regression_rows",
            ),
            checked=(
                SOURCE_FILES["qqq_cfb_log"],
                "SAFE_FAST_RULE_FAMILY_DECISION_TABLE.md",
                "tests/test_candidate_freshness_blocker_rule_gate.py",
            ),
            checked_lines=(
                "QQQ Clean Fast Break log lines 3-6; decision table marks "
                "Clean Fast Break expiry SOURCE_DATA_INSUFFICIENT"
            ),
            available_fields=qqq_cfb_log_keys,
        ),
        _context_requirement(
            candidate_id="QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001",
            symbol="QQQ",
            setup_type="Clean Fast Break",
            checked=(SOURCE_FILES["qqq_csv"], SOURCE_FILES["qqq_cfb_log"]),
            checked_lines="QQQ source CSV line 132; QQQ Clean Fast Break log line 3",
            available_fields=qqq_csv_headers + qqq_cfb_log_keys,
        ),
        _requirement(
            candidate_id="SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003",
            symbol="SPY",
            setup_type="Clean Fast Break",
            evidence_family="Clean Fast Break higher-base/fresh-break expiry",
            required=(
                "clean_fast_break_higher_base_fresh_break_expiry_rule",
                "higher_base_fresh_break_expiry_regression_rows",
            ),
            checked=(SOURCE_FILES["spy_cfb_log"], SOURCE_FILES["spy_csv"]),
            checked_lines="SPY source CSV line 154; SPY Clean Fast Break log lines 5-6",
            available_fields=spy_csv_headers + spy_cfb_log_keys,
        ),
        _context_requirement(
            candidate_id="SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003",
            symbol="SPY",
            setup_type="Clean Fast Break",
            checked=(SOURCE_FILES["spy_csv"], SOURCE_FILES["spy_cfb_log"]),
            checked_lines="SPY source CSV line 154; SPY Clean Fast Break log line 5",
            available_fields=spy_csv_headers + spy_cfb_log_keys,
        ),
        _requirement(
            candidate_id="SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002",
            symbol="SPY",
            setup_type="Clean Fast Break",
            evidence_family="Clean Fast Break initial-break expiry",
            required=(
                "clean_fast_break_initial_break_expiry_rule",
                "initial_break_expiry_regression_rows",
            ),
            checked=(SOURCE_FILES["spy_cfb_log"], SOURCE_FILES["spy_csv"]),
            checked_lines="SPY source CSV line 138; SPY Clean Fast Break log lines 2-3",
            available_fields=spy_csv_headers + spy_cfb_log_keys,
        ),
        _context_requirement(
            candidate_id="SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002",
            symbol="SPY",
            setup_type="Clean Fast Break",
            checked=(SOURCE_FILES["spy_csv"], SOURCE_FILES["spy_cfb_log"]),
            checked_lines="SPY source CSV line 138; SPY Clean Fast Break log line 2",
            available_fields=spy_csv_headers + spy_cfb_log_keys,
        ),
        _requirement(
            candidate_id="SPY-REAL-HISTORICAL-IDEAL-001",
            symbol="SPY",
            setup_type="Ideal",
            evidence_family="SPY Ideal stale/spent expiry",
            required=("spy_ideal_stale_spent_expiry_rule", "spy_ideal_expiry_regression_rows"),
            checked=(SOURCE_FILES["spy_ideal_log"], SOURCE_FILES["spy_csv"]),
            checked_lines="SPY source CSV line 291; SPY Ideal log lines 5-6",
            available_fields=spy_csv_headers + spy_ideal_log_keys,
        ),
        _context_requirement(
            candidate_id="SPY-REAL-HISTORICAL-IDEAL-001",
            symbol="SPY",
            setup_type="Ideal",
            checked=(SOURCE_FILES["spy_csv"], SOURCE_FILES["spy_ideal_log"]),
            checked_lines="SPY source CSV line 291; SPY Ideal log line 5",
            available_fields=spy_csv_headers + spy_ideal_log_keys,
            required=(
                "gap_context_status",
                "headline_context_status",
                "room_status",
                "context_24h_status",
                "macro_context_status",
                "iv_context_status",
                "event_context_status",
                "option_context_status",
                "execution_context_status",
                "complete_caution_review_status",
            ),
        ),
    )
    return rows


def _context_requirement(
    *,
    candidate_id: str,
    symbol: str,
    setup_type: str,
    checked: tuple[str, ...],
    checked_lines: str,
    available_fields: Iterable[str],
    required: tuple[str, ...] = COMMON_CONTEXT_CAUTION_FIELDS,
) -> GapRequirement:
    return _requirement(
        candidate_id=candidate_id,
        symbol=symbol,
        setup_type=setup_type,
        evidence_family="complete context/caution fields",
        required=required,
        checked=checked,
        checked_lines=checked_lines,
        available_fields=tuple(available_fields),
    )


def _requirement(
    *,
    candidate_id: str,
    symbol: str,
    setup_type: str,
    evidence_family: str,
    required: tuple[str, ...],
    checked: tuple[str, ...],
    checked_lines: str,
    available_fields: Iterable[str],
) -> GapRequirement:
    available = tuple(dict.fromkeys(str(field) for field in available_fields))
    found = tuple(field for field in required if field in available)
    missing = tuple(field for field in required if field not in available)
    return GapRequirement(
        candidate_id=candidate_id,
        symbol=symbol,
        setup_type=setup_type,
        evidence_family=evidence_family,
        required_fields_or_rule_names=required,
        source_files_checked=checked,
        source_rows_or_log_lines_checked=checked_lines,
        existing_source_fields_found=found,
        missing_field_names_or_rule_names=missing,
        current_repo_has_required_evidence=False,
        current_repo_data_sufficient_for_row=False,
        parked_status=rule_gate.candidate_survival_status(candidate_id),
        proof_allowed=False,
    )


def _csv_headers(relative_path: str) -> tuple[str, ...]:
    with (ROOT / relative_path).open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        return tuple(next(reader))


def _jsonl_keys(relative_path: str) -> tuple[str, ...]:
    keys: set[str] = set()
    for line in (ROOT / relative_path).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        keys.update(json.loads(line).keys())
    return tuple(sorted(keys))


def _format_table(rows: object) -> str:
    table_rows = list(rows) if isinstance(rows, list) else []
    headers = (
        "candidate_id",
        "evidence_family",
        "current_repo_has_required_evidence",
        "source_rows_or_log_lines_checked",
        "missing_field_names_or_rule_names",
        "parked_status",
        "proof_allowed",
    )
    values = [
        [
            str(row["candidate_id"]),
            str(row["evidence_family"]),
            "YES" if row["current_repo_has_required_evidence"] else "NO",
            str(row["source_rows_or_log_lines_checked"]),
            "; ".join(row["missing_field_names_or_rule_names"]),
            str(row["parked_status"]),
            "YES" if row["proof_allowed"] else "NO",
        ]
        for row in table_rows
    ]
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
