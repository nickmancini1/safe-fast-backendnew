"""Bridge validated source-evidence package content into intake decisions.

The content validator decides whether each of the nine richer historical work
package requests is filled with request-shaped source evidence. This bridge
aggregates those request results by parked candidate. A candidate becomes
eligible for reconsideration only when every required request for that candidate
passes. Reconsideration is not proof review, intake promotion, or profitability.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence

from watcher_foundation import source_evidence_package_intake as intake
from watcher_foundation import source_evidence_work_package_content_validator as content_validator


WORK_PACKAGE_DIR = content_validator.WORK_PACKAGE_DIR
INTAKE_READY_COUNT = intake.INTAKE_READY_COUNT
PARKED_COUNT = intake.PARKED_COUNT
REPLACE_COUNT = intake.REPLACE_COUNT
NO_PROOF_ACCEPTED = True
PROFITABILITY_CLAIMED = False
PARKED_STATUS = "parked/source_data_insufficient"
RECONSIDERATION_STATUS = "reconsideration_eligible"

CANDIDATE_EVIDENCE_REQUIREMENTS: Mapping[str, tuple[str, ...]] = {
    "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001": (
        "QQQ CFB gap-context completeness fields/rule",
        "QQQ CFB stale/spent expiry rule/regressions",
        "QQQ CFB complete context/caution fields",
    ),
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003": (
        "SPY CFB 003 higher-base/fresh-break expiry rule/regressions",
        "SPY CFB 003 complete context/caution fields",
    ),
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002": (
        "SPY CFB 002 initial-break expiry rule/regressions",
        "SPY CFB 002 complete context/caution fields",
    ),
    "SPY-REAL-HISTORICAL-IDEAL-001": (
        "SPY Ideal stale/spent expiry rule/regressions",
        "SPY Ideal gap/headline/option/execution/complete caution fields",
    ),
}


@dataclass(frozen=True)
class BridgeRequestRow:
    evidence_name: str
    candidate_id: str
    rule_family: str
    passed: bool
    required_file_name: str

    def as_row(self) -> dict[str, object]:
        return {
            "evidence_name": self.evidence_name,
            "candidate_id": self.candidate_id,
            "rule_family": self.rule_family,
            "passed": self.passed,
            "required_file_name": self.required_file_name,
        }


@dataclass(frozen=True)
class CandidateBridgeRow:
    candidate_id: str
    required_evidence_names: tuple[str, ...]
    passed_evidence_names: tuple[str, ...]
    failed_evidence_names: tuple[str, ...]
    all_required_requests_passed: bool
    decision: str
    intake_ready_after_bridge: bool
    proof_allowed: bool

    def as_row(self) -> dict[str, object]:
        return {
            "candidate_id": self.candidate_id,
            "required_evidence_names": self.required_evidence_names,
            "passed_evidence_names": self.passed_evidence_names,
            "failed_evidence_names": self.failed_evidence_names,
            "all_required_requests_passed": self.all_required_requests_passed,
            "decision": self.decision,
            "intake_ready_after_bridge": self.intake_ready_after_bridge,
            "proof_allowed": self.proof_allowed,
        }


def bridge_work_package_path(
    work_package_path: str | Path = WORK_PACKAGE_DIR,
) -> dict[str, object]:
    return bridge_content_validation_result(
        content_validator.validate_work_package_content_path(work_package_path)
    )


def bridge_in_memory_rows(
    rows_by_file: Mapping[str, Sequence[Mapping[str, object]]],
) -> dict[str, object]:
    return bridge_content_validation_result(
        content_validator.validate_in_memory_rows(rows_by_file)
    )


def bridge_content_validation_result(
    content_result: Mapping[str, object],
) -> dict[str, object]:
    request_rows = tuple(_request_row(row) for row in content_result["content_results"])
    candidate_rows = tuple(
        _candidate_row(candidate_id, request_rows)
        for candidate_id in CANDIDATE_EVIDENCE_REQUIREMENTS
    )
    eligible_count = sum(
        1 for row in candidate_rows if row.all_required_requests_passed
    )
    return {
        "work_package_dir": content_result.get("work_package_dir", str(WORK_PACKAGE_DIR)),
        "request_count": len(request_rows),
        "requests_mapped_count": len(request_rows),
        "parked_candidate_count": len(candidate_rows),
        "parked_candidates_mapped_count": len(candidate_rows),
        "bridge_request_results": [row.as_row() for row in request_rows],
        "candidate_bridge_results": [row.as_row() for row in candidate_rows],
        "passed_request_count": sum(1 for row in request_rows if row.passed),
        "failed_request_count": sum(1 for row in request_rows if not row.passed),
        "reconsideration_eligible_count": eligible_count,
        "intake_ready_count": INTAKE_READY_COUNT,
        "parked_count": PARKED_COUNT,
        "replace_count": REPLACE_COUNT,
        "proof_accepted": False,
        "profitability_claimed": False,
        "no_generated_reports_or_logs": True,
    }


def format_bridge_report(result: Mapping[str, object]) -> str:
    lines = [
        "SAFE-FAST evidence package to intake bridge",
        f"work package directory: {result['work_package_dir']}",
        f"requests mapped: {result['requests_mapped_count']}",
        f"parked candidates mapped: {result['parked_candidates_mapped_count']}",
        f"passed requests: {result['passed_request_count']}",
        f"failed requests: {result['failed_request_count']}",
        f"reconsideration-eligible candidates: {result['reconsideration_eligible_count']}",
        f"intake-ready count: {result['intake_ready_count']}",
        f"parked count: {result['parked_count']}",
        f"replace count: {result['replace_count']}",
        "request bridge table:",
        _format_request_table(result["bridge_request_results"]),
        "candidate bridge table:",
        _format_candidate_table(result["candidate_bridge_results"]),
        "proof accepted: NO",
        "profitability claim made: NO",
    ]
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("work_package_path", nargs="?")
    args = parser.parse_args(argv)
    print(format_bridge_report(bridge_work_package_path(args.work_package_path or WORK_PACKAGE_DIR)))


def _request_row(row: Mapping[str, object]) -> BridgeRequestRow:
    return BridgeRequestRow(
        evidence_name=str(row["evidence_name"]),
        candidate_id=str(row["candidate_id"]),
        rule_family=str(row["rule_family"]),
        passed=bool(row["passed"]),
        required_file_name=str(row["required_file_name"]),
    )


def _candidate_row(
    candidate_id: str,
    request_rows: tuple[BridgeRequestRow, ...],
) -> CandidateBridgeRow:
    required = CANDIDATE_EVIDENCE_REQUIREMENTS[candidate_id]
    by_name = {row.evidence_name: row for row in request_rows}
    passed = tuple(
        evidence_name
        for evidence_name in required
        if evidence_name in by_name and by_name[evidence_name].passed
    )
    failed = tuple(
        evidence_name
        for evidence_name in required
        if evidence_name not in by_name or not by_name[evidence_name].passed
    )
    all_passed = len(passed) == len(required)
    return CandidateBridgeRow(
        candidate_id=candidate_id,
        required_evidence_names=required,
        passed_evidence_names=passed,
        failed_evidence_names=failed,
        all_required_requests_passed=all_passed,
        decision=RECONSIDERATION_STATUS if all_passed else PARKED_STATUS,
        intake_ready_after_bridge=False,
        proof_allowed=False,
    )


def _format_request_table(rows: object) -> str:
    table_rows = list(rows) if isinstance(rows, list) else []
    headers = ("evidence_name", "candidate_id", "rule_family", "passed")
    values = [
        [
            str(row["evidence_name"]),
            str(row["candidate_id"]),
            str(row["rule_family"]),
            "YES" if row["passed"] else "NO",
        ]
        for row in table_rows
    ]
    return _plain_table(headers, values)


def _format_candidate_table(rows: object) -> str:
    table_rows = list(rows) if isinstance(rows, list) else []
    headers = (
        "candidate_id",
        "all_required_passed",
        "decision",
        "failed_evidence",
        "intake_ready",
        "proof_allowed",
    )
    values = [
        [
            str(row["candidate_id"]),
            "YES" if row["all_required_requests_passed"] else "NO",
            str(row["decision"]),
            "; ".join(row["failed_evidence_names"]),
            "YES" if row["intake_ready_after_bridge"] else "NO",
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
