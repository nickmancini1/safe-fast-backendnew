import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from watcher_foundation import source_evidence_package_intake as intake


EXPECTED_REQUEST_NAMES = {
    "QQQ CFB gap-context completeness fields/rule",
    "QQQ CFB stale/spent expiry rule/regressions",
    "QQQ CFB complete context/caution fields",
    "SPY CFB 003 higher-base/fresh-break expiry rule/regressions",
    "SPY CFB 003 complete context/caution fields",
    "SPY CFB 002 initial-break expiry rule/regressions",
    "SPY CFB 002 complete context/caution fields",
    "SPY Ideal stale/spent expiry rule/regressions",
    "SPY Ideal gap/headline/option/execution/complete caution fields",
}


class SourceEvidencePackageIntakeTests(unittest.TestCase):
    def test_all_nine_acquisition_requests_are_represented_in_export_spec(self):
        requirements = intake.build_package_requirements()

        self.assertEqual(len(requirements), 9)
        self.assertEqual(
            {requirement.evidence_name for requirement in requirements},
            EXPECTED_REQUEST_NAMES,
        )
        for requirement in requirements:
            self.assertIn("jsonl", requirement.accepted_formats)
            self.assertIn("csv", requirement.accepted_formats)
            self.assertTrue(requirement.required_file_name.endswith(".jsonl"))
            self.assertNotEqual(requirement.required_fields, ())

    def test_package_intake_helper_exposes_required_files_and_fields(self):
        checklist = intake.build_required_package_checklist()

        self.assertEqual(checklist["request_count"], 9)
        self.assertEqual(len(checklist["file_requirements"]), 9)
        for row in checklist["file_requirements"]:
            self.assertIn("required_file_name", row)
            self.assertIn("required_fields", row)
            self.assertNotEqual(row["required_fields"], ())
            self.assertEqual(row["accepted_formats"], ("csv", "jsonl"))

    def test_manifest_schema_is_required(self):
        schema = intake.build_manifest_schema()

        self.assertEqual(schema["manifest_file_name"], "manifest.json")
        self.assertEqual(
            schema["schema_version"],
            "safe-fast-richer-historical-export-package-v1",
        )
        self.assertIn("evidence_files", schema["required_top_level_fields"])
        self.assertIn("proof_accepted", schema["required_top_level_fields"])
        self.assertIn("profitability_claimed", schema["required_top_level_fields"])

    def test_missing_manifest_fails_validation(self):
        result = intake.validate_package_path(Path.cwd() / "missing_package_dir")

        self.assertFalse(result["manifest_present"])
        self.assertFalse(result["manifest_passed"])
        self.assertIn("missing manifest.json", result["manifest_errors"])
        self.assertEqual(result["passed_file_count"], 0)
        self.assertEqual(result["failed_file_count"], 9)

    def test_missing_required_file_fails_validation(self):
        package = _complete_package()
        package["evidence_files"] = package["evidence_files"][:-1]

        result = intake.validate_in_memory_package(package)

        self.assertFalse(result["manifest_passed"])
        self.assertEqual(result["passed_file_count"], 0)
        self.assertEqual(result["failed_file_count"], 9)
        self.assertTrue(
            any(not row["file_present"] for row in result["file_results"])
        )

    def test_missing_required_field_fails_validation(self):
        package = _complete_package()
        first_entry = package["evidence_files"][0]
        first_required = intake.build_package_requirements()[0].required_fields[0]
        first_entry["fields"].pop(first_required)

        result = intake.validate_in_memory_package(package)
        first_row = result["file_results"][0]

        self.assertFalse(first_row["passed"])
        self.assertIn(first_required, first_row["missing_fields"])
        self.assertEqual(result["passed_file_count"], 8)
        self.assertEqual(result["failed_file_count"], 1)

    def test_complete_synthetic_in_memory_package_passes_structural_validation(self):
        result = intake.validate_in_memory_package(_complete_package())

        self.assertTrue(result["manifest_present"])
        self.assertTrue(result["manifest_passed"])
        self.assertEqual(result["passed_file_count"], 9)
        self.assertEqual(result["failed_file_count"], 0)
        for row in result["file_results"]:
            self.assertTrue(row["passed"])
            self.assertTrue(row["file_present"])
            self.assertTrue(row["format_valid"])
            self.assertEqual(row["missing_fields"], ())

    def test_no_parked_row_is_reactivated_by_structural_validation_alone(self):
        result = intake.validate_in_memory_package(_complete_package())

        for row in result["file_results"]:
            self.assertFalse(row["would_reactivate_parked_row"])
            self.assertEqual(row["parked_status"], "parked/source_data_insufficient")
            self.assertFalse(row["proof_allowed"])

    def test_counts_and_claims_remain_unchanged(self):
        result = intake.validate_in_memory_package(_complete_package())

        self.assertEqual(result["intake_ready_count"], 0)
        self.assertEqual(result["parked_count"], 4)
        self.assertEqual(result["replace_count"], 3)
        self.assertFalse(result["proof_accepted"])
        self.assertFalse(result["profitability_claimed"])
        self.assertTrue(intake.NO_PROOF_ACCEPTED)
        self.assertFalse(intake.PROFITABILITY_CLAIMED)

    def test_cli_runs_stdout_only_without_package(self):
        output = io.StringIO()

        with redirect_stdout(output):
            intake.main([])

        report = output.getvalue()
        self.assertIn("SAFE-FAST richer historical export package checklist", report)
        self.assertIn("requests represented: 9", report)
        self.assertIn("intake-ready count: 0", report)
        self.assertIn("parked count: 4", report)
        self.assertIn("replace count: 3", report)
        self.assertIn("proof accepted: NO", report)
        self.assertIn("profitability claim made: NO", report)
        self.assertTrue(
            intake.build_required_package_checklist()["no_generated_reports_or_logs"]
        )

    def test_template_folder_and_manifest_example_exist(self):
        result = intake.validate_template_path()

        self.assertTrue(result["template_dir_exists"])
        self.assertTrue(result["manifest_example_present"])
        self.assertEqual(result["request_count"], 9)

    def test_all_nine_template_files_exist_with_required_headers(self):
        result = intake.validate_template_path()

        self.assertEqual(result["passed_template_file_count"], 9)
        self.assertEqual(result["failed_template_file_count"], 0)
        for row in result["template_results"]:
            self.assertTrue(row["passed"])
            self.assertTrue(row["file_present"])
            self.assertTrue(row["format_valid"])
            self.assertEqual(row["missing_fields"], ())

    def test_template_structure_does_not_reactivate_or_claim_proof(self):
        result = intake.validate_template_path()

        self.assertFalse(result["template_counts_as_real_evidence"])
        self.assertEqual(result["intake_ready_count"], 0)
        self.assertEqual(result["parked_count"], 4)
        self.assertEqual(result["replace_count"], 3)
        self.assertFalse(result["proof_accepted"])
        self.assertFalse(result["profitability_claimed"])
        for row in result["template_results"]:
            self.assertFalse(row["would_reactivate_parked_row"])
            self.assertFalse(row["proof_allowed"])

    def test_template_cli_runs_stdout_only(self):
        output = io.StringIO()

        with redirect_stdout(output):
            intake.main(["--validate-template"])

        report = output.getvalue()
        self.assertIn(
            "SAFE-FAST richer historical export package template validation",
            report,
        )
        self.assertIn("template directory exists: YES", report)
        self.assertIn("manifest example present: YES", report)
        self.assertIn("template files passed: 9", report)
        self.assertIn("intake-ready count: 0", report)
        self.assertIn("proof accepted: NO", report)
        self.assertIn("profitability claim made: NO", report)

    def test_work_package_folder_and_manifest_exist(self):
        result = intake.validate_work_package_path()

        self.assertTrue(result["work_package_dir_exists"])
        self.assertTrue(result["manifest_present"])
        self.assertEqual(result["request_count"], 9)

    def test_all_nine_work_package_files_exist_with_required_headers(self):
        result = intake.validate_work_package_path()

        self.assertEqual(result["passed_work_file_count"], 9)
        self.assertEqual(result["failed_work_file_count"], 0)
        for row in result["work_results"]:
            self.assertTrue(row["passed"])
            self.assertTrue(row["file_present"])
            self.assertTrue(row["format_valid"])
            self.assertEqual(row["missing_fields"], ())

    def test_work_package_structure_does_not_count_as_real_evidence(self):
        result = intake.validate_work_package_path()

        self.assertTrue(result["manifest_passed"])
        self.assertFalse(result["work_package_counts_as_real_evidence"])
        self.assertEqual(result["intake_ready_count"], 0)
        self.assertEqual(result["parked_count"], 4)
        self.assertEqual(result["replace_count"], 3)
        self.assertFalse(result["proof_accepted"])
        self.assertFalse(result["profitability_claimed"])
        for row in result["work_results"]:
            self.assertFalse(row["would_reactivate_parked_row"])
            self.assertFalse(row["proof_allowed"])

    def test_work_package_cli_runs_stdout_only(self):
        output = io.StringIO()

        with redirect_stdout(output):
            intake.main(["--validate-work-package"])

        report = output.getvalue()
        self.assertIn(
            "SAFE-FAST richer historical export work package validation",
            report,
        )
        self.assertIn("work package directory exists: YES", report)
        self.assertIn("manifest present: YES", report)
        self.assertIn("work files passed: 9", report)
        self.assertIn("work package validation only: does not count as real evidence", report)
        self.assertIn("intake-ready count: 0", report)
        self.assertIn("parked count: 4", report)
        self.assertIn("replace count: 3", report)
        self.assertIn("proof accepted: NO", report)
        self.assertIn("profitability claim made: NO", report)


def _complete_package(*, include_inline_fields=True):
    entries = []
    for requirement in intake.build_package_requirements():
        entry = {
            "evidence_name": requirement.evidence_name,
            "candidate_id": requirement.candidate_id,
            "file_name": requirement.required_file_name,
            "format": "jsonl",
            "source_export_type": requirement.required_source_type,
            "timestamp_session_window": (
                requirement.required_timestamp_session_window
            ),
        }
        if include_inline_fields:
            entry["fields"] = {
                field: "source-backed complete"
                for field in requirement.required_fields
            }
        entries.append(entry)

    return {
        "schema_version": intake.MANIFEST_SCHEMA_VERSION,
        "package_name": "synthetic-test-package",
        "created_utc": "2026-06-12T00:00:00Z",
        "source_system": "synthetic-unit-test",
        "evidence_files": entries,
        "proof_accepted": False,
        "profitability_claimed": False,
    }


if __name__ == "__main__":
    unittest.main()
