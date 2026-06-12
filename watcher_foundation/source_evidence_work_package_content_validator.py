"""Content validator for the richer historical export work package.

The structural package-intake helper verifies that the fillable work package is
present and shaped correctly. This validator is stricter: it checks whether the
work files contain real evidence rows for the nine acquisition requests. Passing
content validation does not reactivate parked rows, allow proof, or claim
profitability.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence

from watcher_foundation import source_evidence_package_intake as intake


WORK_PACKAGE_DIR = intake.WORK_PACKAGE_DIR
INTAKE_READY_COUNT = intake.INTAKE_READY_COUNT
PARKED_COUNT = intake.PARKED_COUNT
REPLACE_COUNT = intake.REPLACE_COUNT
NO_PROOF_ACCEPTED = True
PROFITABILITY_CLAIMED = False
PLACEHOLDER_FILL_STATUSES = (
    "",
    "placeholder",
    "needs_real_evidence",
    "unfilled",
)
CONTENT_METADATA_FIELDS = (
    "fill_status",
    "candidate_id",
    "rule_family",
    "source_time",
    "source_session",
    "source_window",
)


@dataclass(frozen=True)
class ContentValidationRow:
    evidence_name: str
    candidate_id: str
    required_file_name: str
    passed: bool
    file_present: bool
    headers_present: bool
    real_evidence_row_present: bool
    required_fields_present: bool
    required_fields_non_empty: bool
    fill_status_valid: bool
    candidate_id_valid: bool
    rule_family_valid: bool
    source_time_session_window_present: bool
    missing_headers: tuple[str, ...]
    missing_required_fields: tuple[str, ...]
    blocker_fields: tuple[str, ...]
    parked_status: str
    would_reactivate_parked_row: bool
    proof_allowed: bool

    def as_row(self) -> dict[str, object]:
        return {
            "evidence_name": self.evidence_name,
            "candidate_id": self.candidate_id,
            "required_file_name": self.required_file_name,
            "passed": self.passed,
            "file_present": self.file_present,
            "headers_present": self.headers_present,
            "real_evidence_row_present": self.real_evidence_row_present,
            "required_fields_present": self.required_fields_present,
            "required_fields_non_empty": self.required_fields_non_empty,
            "fill_status_valid": self.fill_status_valid,
            "candidate_id_valid": self.candidate_id_valid,
            "rule_family_valid": self.rule_family_valid,
            "source_time_session_window_present": (
                self.source_time_session_window_present
            ),
            "missing_headers": self.missing_headers,
            "missing_required_fields": self.missing_required_fields,
            "blocker_fields": self.blocker_fields,
            "parked_status": self.parked_status,
            "would_reactivate_parked_row": self.would_reactivate_parked_row,
            "proof_allowed": self.proof_allowed,
        }


def validate_work_package_content_path(
    work_package_path: str | Path = WORK_PACKAGE_DIR,
) -> dict[str, object]:
    root = Path(work_package_path)
    requirements = intake.build_package_requirements()
    rows = tuple(_validate_requirement_content(requirement, root) for requirement in requirements)
    return _content_result(root, rows)


def validate_in_memory_rows(
    rows_by_file: Mapping[str, Sequence[Mapping[str, object]]],
) -> dict[str, object]:
    requirements = intake.build_package_requirements()
    rows = tuple(
        _validate_requirement_rows(
            requirement,
            tuple(rows_by_file.get(requirement.required_file_name, ())),
            file_present=requirement.required_file_name in rows_by_file,
            headers=tuple(_headers_from_rows(rows_by_file.get(requirement.required_file_name, ()))),
        )
        for requirement in requirements
    )
    return _content_result(WORK_PACKAGE_DIR, rows)


def format_content_validation(result: dict[str, object]) -> str:
    lines = [
        "SAFE-FAST richer historical export work package content validation",
        f"work package directory: {result['work_package_dir']}",
        f"work files checked: {result['request_count']}",
        f"passed requests: {result['passed_request_count']}",
        f"failed requests: {result['failed_request_count']}",
        "content validation only: parked rows stay parked",
        f"intake-ready count: {result['intake_ready_count']}",
        f"parked count: {result['parked_count']}",
        f"replace count: {result['replace_count']}",
        "content validation table:",
        _format_content_table(result["content_results"]),
        "proof accepted: NO",
        "profitability claim made: NO",
    ]
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("work_package_path", nargs="?")
    args = parser.parse_args(argv)
    print(
        format_content_validation(
            validate_work_package_content_path(args.work_package_path or WORK_PACKAGE_DIR)
        )
    )


def _validate_requirement_content(
    requirement: intake.PackageFileRequirement,
    root: Path,
) -> ContentValidationRow:
    file_path = root / requirement.required_file_name
    headers, rows = _read_csv_file(file_path)
    return _validate_requirement_rows(
        requirement,
        rows,
        file_present=file_path.exists(),
        headers=headers,
    )


def _validate_requirement_rows(
    requirement: intake.PackageFileRequirement,
    rows: tuple[Mapping[str, object], ...],
    *,
    file_present: bool,
    headers: tuple[str, ...],
) -> ContentValidationRow:
    required_headers = (*CONTENT_METADATA_FIELDS, *requirement.required_fields)
    missing_headers = tuple(field for field in required_headers if field not in headers)
    first_real_row = _first_real_row(rows)
    row_present = first_real_row is not None
    row = first_real_row or {}
    missing_required = tuple(
        field for field in requirement.required_fields if field not in row
    )
    unresolved_required = tuple(
        field
        for field in requirement.required_fields
        if field in row and _is_unresolved(row[field])
    )
    missing_metadata = tuple(
        field for field in CONTENT_METADATA_FIELDS if field not in row
    )
    unresolved_metadata = tuple(
        field
        for field in CONTENT_METADATA_FIELDS
        if field in row and _is_unresolved(row[field])
    )
    fill_status_valid = (
        row_present
        and str(row.get("fill_status", "")).strip().lower()
        not in PLACEHOLDER_FILL_STATUSES
    )
    candidate_id_valid = row_present and str(row.get("candidate_id", "")) == requirement.candidate_id
    rule_family_valid = row_present and str(row.get("rule_family", "")) == requirement.rule_resolved
    source_present = row_present and all(
        not _is_unresolved(row.get(field))
        for field in ("source_time", "source_session", "source_window")
    )
    required_fields_present = not missing_required
    required_fields_non_empty = required_fields_present and not unresolved_required
    blocker_fields = tuple(
        dict.fromkeys(
            (
                *missing_headers,
                *missing_required,
                *unresolved_required,
                *missing_metadata,
                *unresolved_metadata,
                *(() if fill_status_valid else ("fill_status",)),
                *(() if candidate_id_valid else ("candidate_id",)),
                *(() if rule_family_valid else ("rule_family",)),
                *(
                    ()
                    if source_present
                    else ("source_time", "source_session", "source_window")
                ),
            )
        )
    )
    passed = (
        file_present
        and not missing_headers
        and row_present
        and required_fields_present
        and required_fields_non_empty
        and fill_status_valid
        and candidate_id_valid
        and rule_family_valid
        and source_present
    )
    return ContentValidationRow(
        evidence_name=requirement.evidence_name,
        candidate_id=requirement.candidate_id,
        required_file_name=requirement.required_file_name,
        passed=passed,
        file_present=file_present,
        headers_present=not missing_headers,
        real_evidence_row_present=row_present,
        required_fields_present=required_fields_present,
        required_fields_non_empty=required_fields_non_empty,
        fill_status_valid=fill_status_valid,
        candidate_id_valid=candidate_id_valid,
        rule_family_valid=rule_family_valid,
        source_time_session_window_present=source_present,
        missing_headers=missing_headers,
        missing_required_fields=missing_required,
        blocker_fields=blocker_fields,
        parked_status=requirement.parked_status,
        would_reactivate_parked_row=False,
        proof_allowed=False,
    )


def _content_result(
    root: Path,
    rows: tuple[ContentValidationRow, ...],
) -> dict[str, object]:
    return {
        "work_package_dir": str(root),
        "request_count": len(rows),
        "content_results": [row.as_row() for row in rows],
        "passed_request_count": sum(1 for row in rows if row.passed),
        "failed_request_count": sum(1 for row in rows if not row.passed),
        "intake_ready_count": INTAKE_READY_COUNT,
        "parked_count": PARKED_COUNT,
        "replace_count": REPLACE_COUNT,
        "proof_accepted": False,
        "profitability_claimed": False,
        "no_generated_reports_or_logs": True,
    }


def _read_csv_file(path: Path) -> tuple[tuple[str, ...], tuple[Mapping[str, object], ...]]:
    if not path.exists():
        return (), ()
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        headers = tuple(reader.fieldnames or ())
        rows = tuple(dict(row) for row in reader)
    return headers, rows


def _headers_from_rows(rows: Sequence[Mapping[str, object]]) -> tuple[str, ...]:
    for row in rows:
        return tuple(str(key) for key in row.keys())
    return ()


def _first_real_row(
    rows: tuple[Mapping[str, object], ...]
) -> Mapping[str, object] | None:
    for row in rows:
        if any(not _is_unresolved(value) for value in row.values()):
            return row
    return None


def _is_unresolved(value: object) -> bool:
    text = "" if value is None else str(value).strip().lower()
    return text in intake.UNRESOLVED_MARKERS


def _format_content_table(rows: object) -> str:
    table_rows = list(rows) if isinstance(rows, list) else []
    headers = (
        "evidence_name",
        "required_file_name",
        "passed",
        "real_row",
        "fill_status",
        "candidate_id",
        "rule_family",
        "blocker_fields",
    )
    values = [
        [
            str(row["evidence_name"]),
            str(row["required_file_name"]),
            "YES" if row["passed"] else "NO",
            "YES" if row["real_evidence_row_present"] else "NO",
            "YES" if row["fill_status_valid"] else "NO",
            "YES" if row["candidate_id_valid"] else "NO",
            "YES" if row["rule_family_valid"] else "NO",
            "; ".join(row["blocker_fields"]),
        ]
        for row in table_rows
    ]
    return _plain_table(headers, values)


def _plain_table(headers: tuple[str, ...], values: list[list[str]]) -> str:
    widths = [
        max(len(header), *(len(value_row[index]) for value_row in values))
        for index, header in enumerate(headers)
    ]
    header_line = " | ".join(
        header.ljust(widths[index]) for index, header in enumerate(headers)
    )
    separator = " | ".join("-" * widths[index] for index in range(len(headers)))
    body = [
        " | ".join(value.ljust(widths[index]) for index, value in enumerate(row))
        for row in values
    ]
    return "\n".join([header_line, separator, *body])


if __name__ == "__main__":
    main()
