"""Validator for future source-evidence acquisition packages.

The validator loads the nine acquisition requests from the source-evidence
gap scanner and checks in-memory evidence records against those requests. It
does not read future evidence files, create reports, reactivate parked rows,
accept proof, or claim profitability.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from watcher_foundation import source_evidence_gap_scanner as gap_scanner


NO_PROOF_ACCEPTED = True
PROFITABILITY_CLAIMED = False
INTAKE_READY_COUNT = 0
PARKED_COUNT = 4
REPLACE_COUNT = 3
PARKED_STATUS = gap_scanner.PARKED_STATUS

UNRESOLVED_MARKERS = ("", "none", "missing", "unclear", "incomplete")


@dataclass(frozen=True)
class AcquisitionRequestDefinition:
    evidence_name: str
    candidate_id: str
    setup_type: str
    symbol: str
    accepted_source_type: str
    required_timestamp_session_window: str
    required_fields: tuple[str, ...]
    rule_resolved: str
    parked_status: str

    def as_row(self) -> dict[str, object]:
        return {
            "evidence_name": self.evidence_name,
            "candidate_id": self.candidate_id,
            "setup_type": self.setup_type,
            "symbol": self.symbol,
            "accepted_source_type": self.accepted_source_type,
            "required_timestamp_session_window": (
                self.required_timestamp_session_window
            ),
            "required_fields": self.required_fields,
            "rule_resolved": self.rule_resolved,
            "parked_status": self.parked_status,
        }


@dataclass(frozen=True)
class ValidationResult:
    evidence_name: str
    candidate_id: str
    setup_type: str
    symbol: str
    rule_resolved: str
    accepted_source_type: str
    passed: bool
    missing_fields: tuple[str, ...]
    blocker_fields: tuple[str, ...]
    source_type_valid: bool
    matching_record_found: bool
    parked_status: str
    would_reactivate_parked_row: bool
    proof_allowed: bool

    def as_row(self) -> dict[str, object]:
        return {
            "evidence_name": self.evidence_name,
            "candidate_id": self.candidate_id,
            "setup_type": self.setup_type,
            "symbol": self.symbol,
            "rule_resolved": self.rule_resolved,
            "accepted_source_type": self.accepted_source_type,
            "passed": self.passed,
            "missing_fields": self.missing_fields,
            "blocker_fields": self.blocker_fields,
            "source_type_valid": self.source_type_valid,
            "matching_record_found": self.matching_record_found,
            "parked_status": self.parked_status,
            "would_reactivate_parked_row": self.would_reactivate_parked_row,
            "proof_allowed": self.proof_allowed,
        }


def build_request_definitions() -> tuple[AcquisitionRequestDefinition, ...]:
    scan = gap_scanner.build_gap_scan()
    return tuple(
        AcquisitionRequestDefinition(
            evidence_name=str(row["evidence_name"]),
            candidate_id=str(row["candidate_id"]),
            setup_type=str(row["setup_type"]),
            symbol=str(row["symbol"]),
            accepted_source_type=str(row["required_source_export_type"]),
            required_timestamp_session_window=str(
                row["required_timestamp_session_window"]
            ),
            required_fields=tuple(str(field) for field in row["required_fields"]),
            rule_resolved=str(row["rule_resolved"]),
            parked_status=PARKED_STATUS,
        )
        for row in scan["acquisition_requests"]
    )


def validate_evidence_package(
    evidence_package: object | None = None,
) -> dict[str, object]:
    definitions = build_request_definitions()
    records = _coerce_records(evidence_package)
    results = tuple(_validate_request(definition, records) for definition in definitions)
    covered_candidates = tuple(sorted({definition.candidate_id for definition in definitions}))

    return {
        "request_definitions": [definition.as_row() for definition in definitions],
        "request_count": len(definitions),
        "parked_candidate_ids": covered_candidates,
        "parked_rows_covered": len(covered_candidates),
        "validation_results": [result.as_row() for result in results],
        "passed_request_count": sum(1 for result in results if result.passed),
        "failed_request_count": sum(1 for result in results if not result.passed),
        "blocker_count": sum(len(result.blocker_fields) for result in results),
        "intake_ready_count": INTAKE_READY_COUNT,
        "parked_count": PARKED_COUNT,
        "replace_count": REPLACE_COUNT,
        "proof_accepted": False,
        "profitability_claimed": False,
        "no_generated_reports_or_logs": True,
        "validator_result_with_no_new_evidence": (
            "all acquisition requests fail validation as blockers; parked rows stay parked"
            if not records
            else "supplied records validate individual requests only; parked rows stay parked"
        ),
    }


def format_validator_report(result: dict[str, object]) -> str:
    lines = [
        "SAFE-FAST source-evidence acquisition validator",
        f"acquisition requests represented: {result['request_count']}",
        f"parked rows covered: {result['parked_rows_covered']}",
        f"passed requests: {result['passed_request_count']}",
        f"failed requests: {result['failed_request_count']}",
        f"blocker fields: {result['blocker_count']}",
        f"intake-ready count: {result['intake_ready_count']}",
        f"parked count: {result['parked_count']}",
        f"replace count: {result['replace_count']}",
        "validator result: "
        + str(result["validator_result_with_no_new_evidence"]),
        "request validation table:",
        _format_validation_table(result["validation_results"]),
        "proof accepted: NO",
        "profitability claim made: NO",
    ]
    return "\n".join(lines)


def main() -> None:
    print(format_validator_report(validate_evidence_package()))


def _validate_request(
    definition: AcquisitionRequestDefinition,
    records: tuple[Mapping[str, object], ...],
) -> ValidationResult:
    record = _matching_record(definition, records)
    if record is None:
        return _validation_result(
            definition,
            passed=False,
            missing_fields=definition.required_fields,
            blocker_fields=definition.required_fields,
            source_type_valid=False,
            matching_record_found=False,
        )

    source_type_valid = (
        str(record.get("source_export_type", ""))
        == definition.accepted_source_type
    )
    fields = _record_fields(record)
    missing = tuple(field for field in definition.required_fields if field not in fields)
    blockers = tuple(
        field
        for field in definition.required_fields
        if field in fields and _is_unresolved(fields[field])
    )
    passed = source_type_valid and not missing and not blockers
    return _validation_result(
        definition,
        passed=passed,
        missing_fields=missing,
        blocker_fields=missing + blockers,
        source_type_valid=source_type_valid,
        matching_record_found=True,
    )


def _validation_result(
    definition: AcquisitionRequestDefinition,
    *,
    passed: bool,
    missing_fields: tuple[str, ...],
    blocker_fields: tuple[str, ...],
    source_type_valid: bool,
    matching_record_found: bool,
) -> ValidationResult:
    return ValidationResult(
        evidence_name=definition.evidence_name,
        candidate_id=definition.candidate_id,
        setup_type=definition.setup_type,
        symbol=definition.symbol,
        rule_resolved=definition.rule_resolved,
        accepted_source_type=definition.accepted_source_type,
        passed=passed,
        missing_fields=missing_fields,
        blocker_fields=blocker_fields,
        source_type_valid=source_type_valid,
        matching_record_found=matching_record_found,
        parked_status=definition.parked_status,
        would_reactivate_parked_row=False,
        proof_allowed=False,
    )


def _matching_record(
    definition: AcquisitionRequestDefinition,
    records: tuple[Mapping[str, object], ...],
) -> Mapping[str, object] | None:
    for record in records:
        if (
            str(record.get("evidence_name", "")) == definition.evidence_name
            and str(record.get("candidate_id", "")) == definition.candidate_id
            and str(record.get("rule_resolved", "")) == definition.rule_resolved
        ):
            return record
    return None


def _coerce_records(evidence_package: object | None) -> tuple[Mapping[str, object], ...]:
    if evidence_package is None:
        return ()
    if isinstance(evidence_package, Mapping):
        records = evidence_package.get("records")
        if records is None:
            return (evidence_package,)
    else:
        records = evidence_package
    if isinstance(records, Sequence) and not isinstance(records, (str, bytes)):
        return tuple(record for record in records if isinstance(record, Mapping))
    return ()


def _record_fields(record: Mapping[str, object]) -> Mapping[str, object]:
    fields = record.get("fields", {})
    if isinstance(fields, Mapping):
        return fields
    return {}


def _is_unresolved(value: object) -> bool:
    text = "" if value is None else str(value).strip().lower()
    return text in UNRESOLVED_MARKERS


def _format_validation_table(rows: object) -> str:
    table_rows = list(rows) if isinstance(rows, list) else []
    headers = (
        "evidence_name",
        "candidate_id",
        "passed",
        "missing_fields",
        "blocker_fields",
        "parked_status",
        "proof_allowed",
    )
    values = [
        [
            str(row["evidence_name"]),
            str(row["candidate_id"]),
            "YES" if row["passed"] else "NO",
            "; ".join(row["missing_fields"]),
            "; ".join(row["blocker_fields"]),
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
