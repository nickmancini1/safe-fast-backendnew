import io
import unittest
from contextlib import redirect_stdout

from watcher_foundation import source_evidence_package_intake as intake
from watcher_foundation import source_evidence_work_package_content_validator as validator


class SourceEvidenceWorkPackageContentValidatorTests(unittest.TestCase):
    def test_all_nine_work_files_are_checked(self):
        result = validator.validate_work_package_content_path()

        self.assertEqual(result["request_count"], 9)
        self.assertEqual(len(result["content_results"]), 9)
        self.assertEqual(
            {
                row["required_file_name"]
                for row in result["content_results"]
            },
            {
                requirement.required_file_name
                for requirement in intake.build_package_requirements()
            },
        )

    def test_current_work_files_are_prefilled_partial_rows(self):
        result = validator.validate_work_package_content_path()

        self.assertEqual(result["passed_request_count"], 0)
        self.assertEqual(result["failed_request_count"], 9)
        self.assertEqual(result["partial_row_count"], 9)
        self.assertEqual(result["header_only_count"], 0)
        for row in result["content_results"]:
            self.assertFalse(row["passed"])
            self.assertTrue(row["real_evidence_row_present"])
            self.assertTrue(row["partial_row_present"])
            self.assertFalse(row["header_only"])
            self.assertEqual(row["row_status"], validator.PARTIAL_FILL_STATUS)

    def test_all_nine_work_files_have_prefill_or_explicit_reason(self):
        result = validator.validate_work_package_content_path()

        handled_files = {
            row["required_file_name"]
            for row in result["content_results"]
            if row["partial_row_present"] or row["header_only"]
        }

        self.assertEqual(len(handled_files), 9)
        self.assertEqual(result["partial_row_count"], 9)
        self.assertEqual(result["header_only_count"], 0)

    def test_placeholder_fill_status_fails_validation(self):
        rows_by_file = _complete_rows_by_file()
        first_requirement = intake.build_package_requirements()[0]
        rows_by_file[first_requirement.required_file_name][0]["fill_status"] = "placeholder"

        result = validator.validate_in_memory_rows(rows_by_file)
        first_row = result["content_results"][0]

        self.assertFalse(first_row["passed"])
        self.assertFalse(first_row["fill_status_valid"])
        self.assertIn("fill_status", first_row["blocker_fields"])
        self.assertEqual(result["passed_request_count"], 8)
        self.assertEqual(result["failed_request_count"], 1)

    def test_missing_required_field_fails_validation(self):
        rows_by_file = _complete_rows_by_file()
        first_requirement = intake.build_package_requirements()[0]
        missing_field = first_requirement.required_fields[0]
        rows_by_file[first_requirement.required_file_name][0].pop(missing_field)

        result = validator.validate_in_memory_rows(rows_by_file)
        first_row = result["content_results"][0]

        self.assertFalse(first_row["passed"])
        self.assertFalse(first_row["required_fields_present"])
        self.assertIn(missing_field, first_row["missing_required_fields"])

    def test_partial_missing_required_evidence_fails_validation(self):
        first_requirement = intake.build_package_requirements()[0]
        row = _complete_row(first_requirement)
        row["fill_status"] = validator.PARTIAL_FILL_STATUS
        row[first_requirement.required_fields[0]] = "MISSING_REQUIRED_EVIDENCE"

        result = validator.validate_in_memory_rows(
            {first_requirement.required_file_name: [row]}
        )
        first_row = result["content_results"][0]

        self.assertFalse(first_row["passed"])
        self.assertTrue(first_row["partial_row_present"])
        self.assertEqual(first_row["row_status"], validator.PARTIAL_FILL_STATUS)
        self.assertIn(first_requirement.required_fields[0], first_row["blocker_fields"])

    def test_annotated_missing_required_evidence_fails_validation(self):
        first_requirement = intake.build_package_requirements()[0]
        row = _complete_row(first_requirement)
        row["fill_status"] = validator.PARTIAL_FILL_STATUS
        row[first_requirement.required_fields[0]] = (
            "MISSING_REQUIRED_EVIDENCE: gap_context_status absent from source"
        )

        result = validator.validate_in_memory_rows(
            {first_requirement.required_file_name: [row]}
        )
        first_row = result["content_results"][0]

        self.assertFalse(first_row["passed"])
        self.assertTrue(first_row["partial_row_present"])
        self.assertIn(first_requirement.required_fields[0], first_row["blocker_fields"])

    def test_tastytrade_data_not_available_fails_validation(self):
        first_requirement = intake.build_package_requirements()[0]
        row = _complete_row(first_requirement)
        row["fill_status"] = validator.PARTIAL_FILL_STATUS
        row[first_requirement.required_fields[0]] = (
            "TASTYTRADE_DATA_NOT_AVAILABLE: dxLink source CSV has OHLCV only"
        )

        result = validator.validate_in_memory_rows(
            {first_requirement.required_file_name: [row]}
        )
        first_row = result["content_results"][0]

        self.assertFalse(first_row["passed"])
        self.assertTrue(first_row["partial_row_present"])
        self.assertIn(first_requirement.required_fields[0], first_row["blocker_fields"])

    def test_complete_synthetic_row_passes_content_validation_for_its_request(self):
        first_requirement = intake.build_package_requirements()[0]
        rows_by_file = {
            first_requirement.required_file_name: [
                _complete_row(first_requirement)
            ]
        }

        result = validator.validate_in_memory_rows(rows_by_file)
        first_row = result["content_results"][0]

        self.assertTrue(first_row["passed"])
        self.assertTrue(first_row["real_evidence_row_present"])
        self.assertTrue(first_row["fill_status_valid"])
        self.assertTrue(first_row["candidate_id_valid"])
        self.assertTrue(first_row["rule_family_valid"])
        self.assertTrue(first_row["source_time_session_window_present"])
        self.assertEqual(result["passed_request_count"], 1)
        self.assertEqual(result["failed_request_count"], 8)

    def test_complete_synthetic_rows_pass_all_content_requests(self):
        result = validator.validate_in_memory_rows(_complete_rows_by_file())

        self.assertEqual(result["passed_request_count"], 9)
        self.assertEqual(result["failed_request_count"], 0)
        for row in result["content_results"]:
            self.assertTrue(row["passed"])
            self.assertFalse(row["would_reactivate_parked_row"])
            self.assertFalse(row["proof_allowed"])

    def test_current_work_package_has_zero_passed_and_nine_failed(self):
        result = validator.validate_work_package_content_path()

        self.assertEqual(result["passed_request_count"], 0)
        self.assertEqual(result["failed_request_count"], 9)
        self.assertEqual(result["partial_row_count"], 9)

    def test_parked_rows_stay_parked_and_intake_ready_remains_zero(self):
        result = validator.validate_in_memory_rows(_complete_rows_by_file())

        self.assertEqual(result["intake_ready_count"], 0)
        self.assertEqual(result["parked_count"], 4)
        self.assertEqual(result["replace_count"], 3)
        for row in result["content_results"]:
            self.assertEqual(row["parked_status"], "parked/source_data_insufficient")
            self.assertFalse(row["would_reactivate_parked_row"])

    def test_proof_and_profitability_claims_are_absent(self):
        result = validator.validate_in_memory_rows(_complete_rows_by_file())

        self.assertFalse(result["proof_accepted"])
        self.assertFalse(result["profitability_claimed"])
        self.assertTrue(validator.NO_PROOF_ACCEPTED)
        self.assertFalse(validator.PROFITABILITY_CLAIMED)

    def test_cli_runs_stdout_only(self):
        output = io.StringIO()

        with redirect_stdout(output):
            validator.main([])

        report = output.getvalue()
        self.assertIn(
            "SAFE-FAST richer historical export work package content validation",
            report,
        )
        self.assertIn("work files checked: 9", report)
        self.assertIn("passed requests: 0", report)
        self.assertIn("failed requests: 9", report)
        self.assertIn("partial rows: 9", report)
        self.assertIn("header-only rows: 0", report)
        self.assertIn("intake-ready count: 0", report)
        self.assertIn("parked count: 4", report)
        self.assertIn("replace count: 3", report)
        self.assertIn("proof accepted: NO", report)
        self.assertIn("profitability claim made: NO", report)


def _complete_rows_by_file():
    return {
        requirement.required_file_name: [_complete_row(requirement)]
        for requirement in intake.build_package_requirements()
    }


def _complete_row(requirement):
    row = {
        "fill_status": "source_backed_filled",
        "candidate_id": requirement.candidate_id,
        "rule_family": requirement.rule_resolved,
        "source_time": "2026-06-12T14:30:00Z",
        "source_session": "2026-06-12 regular session",
        "source_window": requirement.required_timestamp_session_window,
    }
    for field in requirement.required_fields:
        row[field] = "source-backed complete"
    return row


if __name__ == "__main__":
    unittest.main()
