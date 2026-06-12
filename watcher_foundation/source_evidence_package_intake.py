"""Structural intake for richer historical source-evidence packages.

The intake helper defines the exact manifest, file names, accepted formats,
and required fields for the nine source-evidence acquisition requests. It can
validate a future package directory or an in-memory synthetic package used by
tests. Structural validation does not reactivate parked rows, allow proof, or
claim profitability.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence

from watcher_foundation import source_evidence_acquisition_validator as validator


MANIFEST_FILE_NAME = "manifest.json"
MANIFEST_SCHEMA_VERSION = "safe-fast-richer-historical-export-package-v1"
ACCEPTED_FORMATS = ("csv", "jsonl")
INTAKE_READY_COUNT = validator.INTAKE_READY_COUNT
PARKED_COUNT = validator.PARKED_COUNT
REPLACE_COUNT = validator.REPLACE_COUNT
NO_PROOF_ACCEPTED = True
PROFITABILITY_CLAIMED = False
UNRESOLVED_MARKERS = validator.UNRESOLVED_MARKERS


@dataclass(frozen=True)
class PackageFileRequirement:
    evidence_name: str
    candidate_id: str
    setup_type: str
    symbol: str
    rule_resolved: str
    required_source_type: str
    required_timestamp_session_window: str
    required_file_name: str
    accepted_formats: tuple[str, ...]
    required_fields: tuple[str, ...]
    parked_status: str

    def as_row(self) -> dict[str, object]:
        return {
            "evidence_name": self.evidence_name,
            "candidate_id": self.candidate_id,
            "setup_type": self.setup_type,
            "symbol": self.symbol,
            "rule_resolved": self.rule_resolved,
            "required_source_type": self.required_source_type,
            "required_timestamp_session_window": (
                self.required_timestamp_session_window
            ),
            "required_file_name": self.required_file_name,
            "accepted_formats": self.accepted_formats,
            "required_fields": self.required_fields,
            "parked_status": self.parked_status,
        }


@dataclass(frozen=True)
class PackageValidationRow:
    evidence_name: str
    candidate_id: str
    required_file_name: str
    passed: bool
    file_present: bool
    format_valid: bool
    missing_fields: tuple[str, ...]
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
            "format_valid": self.format_valid,
            "missing_fields": self.missing_fields,
            "blocker_fields": self.blocker_fields,
            "parked_status": self.parked_status,
            "would_reactivate_parked_row": self.would_reactivate_parked_row,
            "proof_allowed": self.proof_allowed,
        }


def build_package_requirements() -> tuple[PackageFileRequirement, ...]:
    return tuple(
        PackageFileRequirement(
            evidence_name=definition.evidence_name,
            candidate_id=definition.candidate_id,
            setup_type=definition.setup_type,
            symbol=definition.symbol,
            rule_resolved=definition.rule_resolved,
            required_source_type=definition.accepted_source_type,
            required_timestamp_session_window=(
                definition.required_timestamp_session_window
            ),
            required_file_name=_file_name_for(definition.evidence_name),
            accepted_formats=ACCEPTED_FORMATS,
            required_fields=definition.required_fields,
            parked_status=definition.parked_status,
        )
        for definition in validator.build_request_definitions()
    )


def build_manifest_schema() -> dict[str, object]:
    return {
        "manifest_file_name": MANIFEST_FILE_NAME,
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "required_top_level_fields": (
            "schema_version",
            "package_name",
            "created_utc",
            "source_system",
            "evidence_files",
            "proof_accepted",
            "profitability_claimed",
        ),
        "evidence_file_required_fields": (
            "evidence_name",
            "candidate_id",
            "file_name",
            "format",
            "source_export_type",
            "timestamp_session_window",
        ),
        "accepted_formats": ACCEPTED_FORMATS,
        "required_evidence_files": tuple(
            requirement.as_row() for requirement in build_package_requirements()
        ),
    }


def build_required_package_checklist() -> dict[str, object]:
    requirements = build_package_requirements()
    return {
        "manifest_schema": build_manifest_schema(),
        "request_count": len(requirements),
        "file_requirements": [requirement.as_row() for requirement in requirements],
        "intake_ready_count": INTAKE_READY_COUNT,
        "parked_count": PARKED_COUNT,
        "replace_count": REPLACE_COUNT,
        "proof_accepted": False,
        "profitability_claimed": False,
        "no_generated_reports_or_logs": True,
    }


def validate_package_path(package_path: str | Path) -> dict[str, object]:
    root = Path(package_path)
    manifest_path = root / MANIFEST_FILE_NAME
    if not manifest_path.exists():
        return _validation_result(
            manifest_present=False,
            manifest_errors=(f"missing {MANIFEST_FILE_NAME}",),
            file_rows=tuple(
                _missing_file_row(requirement)
                for requirement in build_package_requirements()
            ),
        )

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return _validation_result(
            manifest_present=True,
            manifest_errors=(f"invalid manifest json: {exc}",),
            file_rows=tuple(
                _missing_file_row(requirement)
                for requirement in build_package_requirements()
            ),
        )

    return _validate_manifest_and_files(manifest, package_root=root)


def validate_in_memory_package(package: Mapping[str, object]) -> dict[str, object]:
    return _validate_manifest_and_files(package, package_root=None)


def format_package_checklist(result: dict[str, object]) -> str:
    lines = [
        "SAFE-FAST richer historical export package checklist",
        f"manifest file: {MANIFEST_FILE_NAME}",
        f"manifest schema version: {MANIFEST_SCHEMA_VERSION}",
        "accepted formats: CSV or JSONL",
        f"requests represented: {result['request_count']}",
        f"intake-ready count: {result['intake_ready_count']}",
        f"parked count: {result['parked_count']}",
        f"replace count: {result['replace_count']}",
        "required files:",
        _format_requirements_table(result["file_requirements"]),
        "proof accepted: NO",
        "profitability claim made: NO",
    ]
    return "\n".join(lines)


def format_package_validation(result: dict[str, object]) -> str:
    lines = [
        "SAFE-FAST richer historical export package validation",
        f"manifest present: {'YES' if result['manifest_present'] else 'NO'}",
        "manifest errors: "
        + ("; ".join(result["manifest_errors"]) or "none"),
        f"files passed: {result['passed_file_count']}",
        f"files failed: {result['failed_file_count']}",
        f"intake-ready count: {result['intake_ready_count']}",
        f"parked count: {result['parked_count']}",
        f"replace count: {result['replace_count']}",
        "file validation table:",
        _format_validation_table(result["file_results"]),
        "structural validation only: parked rows stay parked",
        "proof accepted: NO",
        "profitability claim made: NO",
    ]
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("package_path", nargs="?")
    args = parser.parse_args(argv)

    if args.package_path:
        print(format_package_validation(validate_package_path(args.package_path)))
    else:
        print(format_package_checklist(build_required_package_checklist()))


def _validate_manifest_and_files(
    manifest: Mapping[str, object], *, package_root: Path | None
) -> dict[str, object]:
    requirements = build_package_requirements()
    manifest_errors = _manifest_errors(manifest)
    file_rows = tuple(
        _validate_file_requirement(requirement, manifest, package_root)
        for requirement in requirements
    )
    return _validation_result(
        manifest_present=True,
        manifest_errors=manifest_errors,
        file_rows=file_rows,
    )


def _manifest_errors(manifest: Mapping[str, object]) -> tuple[str, ...]:
    errors: list[str] = []
    schema = build_manifest_schema()
    for field in schema["required_top_level_fields"]:
        if field not in manifest:
            errors.append(f"missing manifest field {field}")
    if manifest.get("schema_version") != MANIFEST_SCHEMA_VERSION:
        errors.append("invalid manifest schema_version")
    if manifest.get("proof_accepted") is not False:
        errors.append("manifest proof_accepted must be false")
    if manifest.get("profitability_claimed") is not False:
        errors.append("manifest profitability_claimed must be false")
    if "evidence_files" in manifest and not isinstance(
        manifest["evidence_files"], Sequence
    ):
        errors.append("manifest evidence_files must be a list")
    for requirement in build_package_requirements():
        if _manifest_entry(requirement, manifest) is None:
            errors.append(f"missing evidence file entry {requirement.evidence_name}")
    return tuple(errors)


def _validate_file_requirement(
    requirement: PackageFileRequirement,
    manifest: Mapping[str, object],
    package_root: Path | None,
) -> PackageValidationRow:
    entry = _manifest_entry(requirement, manifest)
    if entry is None:
        return _missing_file_row(requirement)

    file_name = str(entry.get("file_name", ""))
    file_format = str(entry.get("format", "")).lower()
    format_valid = (
        file_format in requirement.accepted_formats
        and file_name == requirement.required_file_name
        and str(entry.get("source_export_type", ""))
        == requirement.required_source_type
        and str(entry.get("timestamp_session_window", ""))
        == requirement.required_timestamp_session_window
    )
    fields = _fields_for_entry(entry, package_root)
    missing = tuple(field for field in requirement.required_fields if field not in fields)
    blockers = tuple(
        field
        for field in requirement.required_fields
        if field in fields and _is_unresolved(fields[field])
    )
    file_present = bool(fields)
    passed = format_valid and file_present and not missing and not blockers
    return PackageValidationRow(
        evidence_name=requirement.evidence_name,
        candidate_id=requirement.candidate_id,
        required_file_name=requirement.required_file_name,
        passed=passed,
        file_present=file_present,
        format_valid=format_valid,
        missing_fields=missing,
        blocker_fields=missing + blockers,
        parked_status=requirement.parked_status,
        would_reactivate_parked_row=False,
        proof_allowed=False,
    )


def _validation_result(
    *,
    manifest_present: bool,
    manifest_errors: tuple[str, ...],
    file_rows: tuple[PackageValidationRow, ...],
) -> dict[str, object]:
    manifest_passed = manifest_present and not manifest_errors
    rows = tuple(
        row if manifest_passed else _force_failed_by_manifest(row)
        for row in file_rows
    )
    return {
        "manifest_present": manifest_present,
        "manifest_errors": manifest_errors,
        "manifest_passed": manifest_passed,
        "request_count": len(rows),
        "file_results": [row.as_row() for row in rows],
        "passed_file_count": sum(1 for row in rows if row.passed),
        "failed_file_count": sum(1 for row in rows if not row.passed),
        "intake_ready_count": INTAKE_READY_COUNT,
        "parked_count": PARKED_COUNT,
        "replace_count": REPLACE_COUNT,
        "proof_accepted": False,
        "profitability_claimed": False,
        "no_generated_reports_or_logs": True,
    }


def _force_failed_by_manifest(row: PackageValidationRow) -> PackageValidationRow:
    return PackageValidationRow(
        evidence_name=row.evidence_name,
        candidate_id=row.candidate_id,
        required_file_name=row.required_file_name,
        passed=False,
        file_present=row.file_present,
        format_valid=row.format_valid,
        missing_fields=row.missing_fields,
        blocker_fields=row.blocker_fields,
        parked_status=row.parked_status,
        would_reactivate_parked_row=False,
        proof_allowed=False,
    )


def _missing_file_row(requirement: PackageFileRequirement) -> PackageValidationRow:
    return PackageValidationRow(
        evidence_name=requirement.evidence_name,
        candidate_id=requirement.candidate_id,
        required_file_name=requirement.required_file_name,
        passed=False,
        file_present=False,
        format_valid=False,
        missing_fields=requirement.required_fields,
        blocker_fields=requirement.required_fields,
        parked_status=requirement.parked_status,
        would_reactivate_parked_row=False,
        proof_allowed=False,
    )


def _manifest_entry(
    requirement: PackageFileRequirement, manifest: Mapping[str, object]
) -> Mapping[str, object] | None:
    entries = manifest.get("evidence_files", ())
    if not isinstance(entries, Sequence) or isinstance(entries, (str, bytes)):
        return None
    for entry in entries:
        if (
            isinstance(entry, Mapping)
            and entry.get("evidence_name") == requirement.evidence_name
            and entry.get("candidate_id") == requirement.candidate_id
        ):
            return entry
    return None


def _fields_for_entry(
    entry: Mapping[str, object], package_root: Path | None
) -> Mapping[str, object]:
    inline_fields = entry.get("fields")
    if isinstance(inline_fields, Mapping):
        return inline_fields
    if package_root is None:
        return {}
    file_name = str(entry.get("file_name", ""))
    file_format = str(entry.get("format", "")).lower()
    file_path = package_root / file_name
    if not file_path.exists():
        return {}
    if file_format == "csv":
        return _csv_fields(file_path)
    if file_format == "jsonl":
        return _jsonl_fields(file_path)
    return {}


def _csv_fields(path: Path) -> Mapping[str, object]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return rows[0] if rows else {}


def _jsonl_fields(path: Path) -> Mapping[str, object]:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            value = json.loads(line)
            return value if isinstance(value, Mapping) else {}
    return {}


def _is_unresolved(value: object) -> bool:
    text = "" if value is None else str(value).strip().lower()
    return text in UNRESOLVED_MARKERS


def _file_name_for(evidence_name: str) -> str:
    slug = (
        evidence_name.lower()
        .replace("/", "_")
        .replace("-", "_")
        .replace(" ", "_")
    )
    while "__" in slug:
        slug = slug.replace("__", "_")
    return f"{slug}.jsonl"


def _format_requirements_table(rows: object) -> str:
    table_rows = list(rows) if isinstance(rows, list) else []
    headers = ("evidence_name", "required_file_name", "required_fields")
    values = [
        [
            str(row["evidence_name"]),
            str(row["required_file_name"]),
            "; ".join(row["required_fields"]),
        ]
        for row in table_rows
    ]
    return _plain_table(headers, values)


def _format_validation_table(rows: object) -> str:
    table_rows = list(rows) if isinstance(rows, list) else []
    headers = (
        "evidence_name",
        "required_file_name",
        "passed",
        "file_present",
        "missing_fields",
        "proof_allowed",
    )
    values = [
        [
            str(row["evidence_name"]),
            str(row["required_file_name"]),
            "YES" if row["passed"] else "NO",
            "YES" if row["file_present"] else "NO",
            "; ".join(row["missing_fields"]),
            "YES" if row["proof_allowed"] else "NO",
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
