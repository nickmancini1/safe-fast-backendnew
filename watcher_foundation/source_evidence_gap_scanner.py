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


@dataclass(frozen=True)
class AcquisitionRequest:
    evidence_name: str
    candidate_id: str
    setup_type: str
    symbol: str
    required_source_export_type: str
    required_timestamp_session_window: str
    required_fields: tuple[str, ...]
    why_needed: str
    rule_resolved: str
    current_repo_data_can_supply: bool
    expected_action_after_acquisition: str

    def as_row(self) -> dict[str, object]:
        return {
            "evidence_name": self.evidence_name,
            "candidate_id": self.candidate_id,
            "setup_type": self.setup_type,
            "symbol": self.symbol,
            "required_source_export_type": self.required_source_export_type,
            "required_timestamp_session_window": (
                self.required_timestamp_session_window
            ),
            "required_fields": self.required_fields,
            "why_needed": self.why_needed,
            "rule_resolved": self.rule_resolved,
            "current_repo_data_can_supply": self.current_repo_data_can_supply,
            "expected_action_after_acquisition": (
                self.expected_action_after_acquisition
            ),
        }


def build_gap_scan() -> dict[str, object]:
    schemas = _load_source_schemas()
    rows = _build_gap_rows(schemas)
    acquisition_requests = _build_acquisition_requests(rows)
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
        "acquisition_request_path": (
            "SAFE_FAST_SOURCE_EVIDENCE_ACQUISITION_REQUEST.md"
        ),
        "acquisition_requests": [
            request.as_row() for request in acquisition_requests
        ],
        "acquisition_request_count": len(acquisition_requests),
        "acquisition_request_candidate_ids": tuple(
            sorted({request.candidate_id for request in acquisition_requests})
        ),
        "acquisition_request_evidence_names": tuple(
            request.evidence_name for request in acquisition_requests
        ),
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
            "use SAFE_FAST_SOURCE_EVIDENCE_ACQUISITION_REQUEST.md to source "
            "the missing gap-context, setup-specific expiry-rule, and complete "
            "context/caution fields before any parked row can be reactivated"
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
        f"acquisition request path: {result['acquisition_request_path']}",
        f"acquisition requests: {result['acquisition_request_count']}",
        "acquisition request candidates covered: "
        + "; ".join(result["acquisition_request_candidate_ids"]),
        "current repo data sufficient by row: "
        + "; ".join(
            f"{candidate_id}={'YES' if has_data else 'NO'}"
            for candidate_id, has_data in result[
                "current_repo_data_sufficient_by_candidate"
            ].items()
        ),
        "gap table:",
        _format_table(result["gap_rows"]),
        "acquisition request summary:",
        _format_acquisition_table(result["acquisition_requests"]),
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


def _build_acquisition_requests(
    gap_rows: Iterable[GapRequirement],
) -> tuple[AcquisitionRequest, ...]:
    by_key = {
        (row.candidate_id, row.evidence_family): row for row in gap_rows
    }

    return (
        _acquisition_request(
            by_key,
            candidate_id="QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001",
            evidence_family="QQQ gap-context completeness",
            evidence_name="QQQ CFB gap-context completeness fields/rule",
            export_type=(
                "setup-time QQQ source CSV export or replay-log enrichment"
            ),
            window="2026-04 QQQ Clean Fast Break setup window; source CSV line 132; replay log lines 3-4",
            why=(
                "Proves whether the QQQ gap context was known and reviewed "
                "before the Clean Fast Break signal."
            ),
            rule="Clean Fast Break gap context",
            action=(
                "rerun the gap scanner and, only if fields are source-backed "
                "and regression-covered, consider un-parking this requirement"
            ),
        ),
        _acquisition_request(
            by_key,
            candidate_id="QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001",
            evidence_family="Clean Fast Break stale/spent expiry",
            evidence_name="QQQ CFB stale/spent expiry rule/regressions",
            export_type=(
                "rule document plus regression fixture rows for QQQ Clean Fast Break"
            ),
            window="QQQ Clean Fast Break log lines 3-6, including fresh and later spent lifecycle rows",
            why=(
                "Defines when the QQQ Clean Fast Break signal remains fresh "
                "or becomes stale/spent before proof review."
            ),
            rule="Clean Fast Break stale/spent expiry",
            action=(
                "add rule-gate regression rows, rerun scanners, then reassess "
                "parked status without accepting proof"
            ),
        ),
        _acquisition_request(
            by_key,
            candidate_id="QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001",
            evidence_family="complete context/caution fields",
            evidence_name="QQQ CFB complete context/caution fields",
            export_type="setup-time QQQ source CSV export or replay-log enrichment",
            window="QQQ Clean Fast Break setup-time row at source CSV line 132 and replay log line 3",
            why=(
                "Replaces unconfirmed context with source-backed blocker and "
                "caution evidence; primary blocker null is not enough."
            ),
            rule="Context/caution review",
            action=(
                "rerun scanner and intake helper; keep parked unless every "
                "context/caution field is source-backed"
            ),
        ),
        _acquisition_request(
            by_key,
            candidate_id="SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003",
            evidence_family="Clean Fast Break higher-base/fresh-break expiry",
            evidence_name="SPY CFB 003 higher-base/fresh-break expiry rule/regressions",
            export_type=(
                "rule document plus regression fixture rows for SPY Clean Fast Break"
            ),
            window="2026-04-15 14:30 SPY signal row and later spent lifecycle row; log lines 5-6",
            why=(
                "Defines whether a higher-base/fresh-break Clean Fast Break "
                "is still fresh at setup time or already stale/spent."
            ),
            rule="Clean Fast Break expiry",
            action=(
                "add higher-base/fresh-break expiry regressions, rerun scanners, "
                "then reassess parked status without proof promotion"
            ),
        ),
        _acquisition_request(
            by_key,
            candidate_id="SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003",
            evidence_family="complete context/caution fields",
            evidence_name="SPY CFB 003 complete context/caution fields",
            export_type="setup-time SPY source CSV export or replay-log enrichment",
            window="2026-04-15 14:30 SPY setup-time row; source CSV line 154; replay log line 5",
            why=(
                "Completes source-backed blocker/caution context for the "
                "fresh-break row before any intake-ready decision."
            ),
            rule="Context/caution review",
            action=(
                "rerun scanner and intake helper; keep parked unless context "
                "and caution fields are complete"
            ),
        ),
        _acquisition_request(
            by_key,
            candidate_id="SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002",
            evidence_family="Clean Fast Break initial-break expiry",
            evidence_name="SPY CFB 002 initial-break expiry rule/regressions",
            export_type=(
                "rule document plus regression fixture rows for SPY Clean Fast Break"
            ),
            window="2026-04-13 12:30 SPY signal row and same-session follow-through/spent row; log lines 2-3",
            why=(
                "Defines whether an initial-break Clean Fast Break is fresh "
                "or stale/spent at setup time."
            ),
            rule="Clean Fast Break expiry",
            action=(
                "add initial-break expiry regressions, rerun scanners, then "
                "reassess parked status without proof promotion"
            ),
        ),
        _acquisition_request(
            by_key,
            candidate_id="SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002",
            evidence_family="complete context/caution fields",
            evidence_name="SPY CFB 002 complete context/caution fields",
            export_type="setup-time SPY source CSV export or replay-log enrichment",
            window="2026-04-13 12:30 SPY setup-time row; source CSV line 138; replay log line 2",
            why=(
                "Completes source-backed blocker/caution context for the "
                "initial-break row before any intake-ready decision."
            ),
            rule="Context/caution review",
            action=(
                "rerun scanner and intake helper; keep parked unless context "
                "and caution fields are complete"
            ),
        ),
        _acquisition_request(
            by_key,
            candidate_id="SPY-REAL-HISTORICAL-IDEAL-001",
            evidence_family="SPY Ideal stale/spent expiry",
            evidence_name="SPY Ideal stale/spent expiry rule/regressions",
            export_type="rule document plus regression fixture rows for SPY Ideal",
            window="2026-05-13 11:30 SPY Ideal signal row and later spent lifecycle row; log lines 5-6",
            why=(
                "Defines whether the same-session SPY Ideal signal is still "
                "fresh or has become stale/spent before proof review."
            ),
            rule="Ideal stale/spent expiry",
            action=(
                "add SPY Ideal stale/spent regressions, rerun scanners, then "
                "reassess parked status without proof promotion"
            ),
        ),
        _acquisition_request(
            by_key,
            candidate_id="SPY-REAL-HISTORICAL-IDEAL-001",
            evidence_family="complete context/caution fields",
            evidence_name="SPY Ideal gap/headline/option/execution/complete caution fields",
            export_type="setup-time SPY source CSV export or replay-log enrichment",
            window="2026-05-13 11:30 SPY Ideal setup-time row; source CSV line 291; replay log line 5",
            why=(
                "Completes gap, headline, room, option, execution, and caution "
                "context for the Ideal setup before any intake-ready decision."
            ),
            rule="Context/caution review",
            action=(
                "rerun scanner and intake helper; keep parked unless every "
                "Ideal context/caution field is source-backed"
            ),
        ),
    )


def _acquisition_request(
    gap_rows_by_key: dict[tuple[str, str], GapRequirement],
    *,
    candidate_id: str,
    evidence_family: str,
    evidence_name: str,
    export_type: str,
    window: str,
    why: str,
    rule: str,
    action: str,
) -> AcquisitionRequest:
    gap_row = gap_rows_by_key[(candidate_id, evidence_family)]
    return AcquisitionRequest(
        evidence_name=evidence_name,
        candidate_id=gap_row.candidate_id,
        setup_type=gap_row.setup_type,
        symbol=gap_row.symbol,
        required_source_export_type=export_type,
        required_timestamp_session_window=window,
        required_fields=gap_row.missing_field_names_or_rule_names,
        why_needed=why,
        rule_resolved=rule,
        current_repo_data_can_supply=False,
        expected_action_after_acquisition=action,
    )


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


def _format_acquisition_table(rows: object) -> str:
    table_rows = list(rows) if isinstance(rows, list) else []
    headers = (
        "evidence_name",
        "candidate_id",
        "required_source_export_type",
        "required_fields",
        "current_repo_data_can_supply",
    )
    values = [
        [
            str(row["evidence_name"]),
            str(row["candidate_id"]),
            str(row["required_source_export_type"]),
            "; ".join(row["required_fields"]),
            "YES" if row["current_repo_data_can_supply"] else "NO",
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
