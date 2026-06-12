import io
import unittest
from contextlib import redirect_stdout

from watcher_foundation import source_evidence_acquisition_validator as validator


EXPECTED_PARKED_IDS = {
    "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001",
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003",
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002",
    "SPY-REAL-HISTORICAL-IDEAL-001",
}

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


class SourceEvidenceAcquisitionValidatorTests(unittest.TestCase):
    def test_all_nine_acquisition_requests_are_represented(self):
        definitions = validator.build_request_definitions()

        self.assertEqual(len(definitions), 9)
        self.assertEqual(
            {definition.evidence_name for definition in definitions},
            EXPECTED_REQUEST_NAMES,
        )
        for definition in definitions:
            self.assertIn(definition.candidate_id, EXPECTED_PARKED_IDS)
            self.assertNotEqual(definition.required_fields, ())
            self.assertNotEqual(definition.accepted_source_type, "")
            self.assertNotEqual(definition.rule_resolved, "")

    def test_all_four_parked_rows_are_covered(self):
        result = validator.validate_evidence_package()

        self.assertEqual(set(result["parked_candidate_ids"]), EXPECTED_PARKED_IDS)
        self.assertEqual(result["parked_rows_covered"], 4)

    def test_missing_required_fields_fail_validation_as_blockers(self):
        definition = validator.build_request_definitions()[0]
        incomplete_record = _record_for(definition, fields={definition.required_fields[0]: "source-backed"})

        result = validator.validate_evidence_package({"records": [incomplete_record]})
        row = _result_for(result, definition.evidence_name)

        self.assertFalse(row["passed"])
        self.assertTrue(row["matching_record_found"])
        self.assertTrue(row["source_type_valid"])
        self.assertNotEqual(row["missing_fields"], ())
        self.assertEqual(row["blocker_fields"], row["missing_fields"])

    def test_unresolved_required_fields_fail_validation_as_blockers(self):
        definition = validator.build_request_definitions()[0]
        fields = {field: "source-backed" for field in definition.required_fields}
        fields[definition.required_fields[0]] = "MISSING"

        result = validator.validate_evidence_package({"records": [_record_for(definition, fields=fields)]})
        row = _result_for(result, definition.evidence_name)

        self.assertFalse(row["passed"])
        self.assertEqual(row["missing_fields"], ())
        self.assertIn(definition.required_fields[0], row["blocker_fields"])

    def test_complete_synthetic_records_pass_for_their_request_only(self):
        for definition in validator.build_request_definitions():
            with self.subTest(definition.evidence_name):
                result = validator.validate_evidence_package(
                    {"records": [_complete_record_for(definition)]}
                )
                rows = result["validation_results"]
                passing = [row for row in rows if row["passed"]]

                self.assertEqual(len(passing), 1)
                self.assertEqual(passing[0]["evidence_name"], definition.evidence_name)
                self.assertEqual(result["passed_request_count"], 1)
                self.assertEqual(result["failed_request_count"], 8)

    def test_wrong_source_type_fails_even_when_fields_are_complete(self):
        definition = validator.build_request_definitions()[0]
        record = _complete_record_for(definition)
        record["source_export_type"] = "unsupported export"

        result = validator.validate_evidence_package({"records": [record]})
        row = _result_for(result, definition.evidence_name)

        self.assertFalse(row["passed"])
        self.assertFalse(row["source_type_valid"])
        self.assertEqual(row["missing_fields"], ())

    def test_no_request_reactivates_a_parked_row_without_supplied_evidence(self):
        result = validator.validate_evidence_package()

        self.assertEqual(result["passed_request_count"], 0)
        self.assertEqual(result["failed_request_count"], 9)
        for row in result["validation_results"]:
            self.assertFalse(row["passed"])
            self.assertFalse(row["matching_record_found"])
            self.assertFalse(row["would_reactivate_parked_row"])
            self.assertEqual(row["parked_status"], "parked/source_data_insufficient")
            self.assertFalse(row["proof_allowed"])

    def test_richer_historical_inventory_checks_all_requests_explicitly(self):
        result = validator.build_richer_historical_evidence_inventory()

        self.assertEqual(result["request_count"], 9)
        self.assertEqual(
            {row["evidence_name"] for row in result["inventory_results"]},
            EXPECTED_REQUEST_NAMES,
        )
        for row in result["inventory_results"]:
            self.assertIn(row["candidate_id"], EXPECTED_PARKED_IDS)
            self.assertIn("exist, but", row["local_sources_inspected"])
            self.assertFalse(row["local_evidence_found"])
            self.assertFalse(row["validator_passed"])

    def test_failed_inventory_requests_name_needed_export_or_file(self):
        result = validator.build_richer_historical_evidence_inventory()

        self.assertEqual(result["passed_request_count"], 0)
        self.assertEqual(result["failed_request_count"], 9)
        self.assertEqual(len(result["exact_missing_export_file_list"]), 9)
        for row in result["inventory_results"]:
            needed = row["exact_export_or_file_still_needed"]
            self.assertIn(row["evidence_name"], needed)
            self.assertIn("containing", needed)
            self.assertNotIn("proof accepted", needed.lower())
            self.assertNotIn("profitability", needed.lower())

    def test_inventory_does_not_reactivate_parked_rows_or_change_counts(self):
        result = validator.build_richer_historical_evidence_inventory()

        self.assertEqual(result["intake_ready_count"], 0)
        self.assertEqual(result["parked_count"], 4)
        self.assertEqual(result["replace_count"], 3)
        self.assertFalse(result["proof_accepted"])
        self.assertFalse(result["profitability_claimed"])
        for row in result["inventory_results"]:
            self.assertFalse(row["would_reactivate_parked_row"])
            self.assertEqual(row["parked_status"], "parked/source_data_insufficient")
            self.assertFalse(row["proof_allowed"])

    def test_counts_and_claims_remain_unchanged(self):
        result = validator.validate_evidence_package()

        self.assertEqual(result["intake_ready_count"], 0)
        self.assertEqual(result["parked_count"], 4)
        self.assertEqual(result["replace_count"], 3)
        self.assertFalse(result["proof_accepted"])
        self.assertFalse(result["profitability_claimed"])
        self.assertTrue(validator.NO_PROOF_ACCEPTED)
        self.assertFalse(validator.PROFITABILITY_CLAIMED)

    def test_cli_runs_stdout_only(self):
        output = io.StringIO()

        with redirect_stdout(output):
            validator.main()

        report = output.getvalue()
        self.assertIn("SAFE-FAST source-evidence acquisition validator", report)
        self.assertIn("acquisition requests represented: 9", report)
        self.assertIn("parked rows covered: 4", report)
        self.assertIn("intake-ready count: 0", report)
        self.assertIn("parked count: 4", report)
        self.assertIn("replace count: 3", report)
        self.assertIn("SAFE-FAST richer historical evidence inventory", report)
        self.assertIn("acquisition requests checked: 9", report)
        self.assertIn("local evidence found count: 0", report)
        self.assertIn("proof accepted: NO", report)
        self.assertIn("profitability claim made: NO", report)
        self.assertTrue(validator.validate_evidence_package()["no_generated_reports_or_logs"])
        self.assertTrue(
            validator.build_richer_historical_evidence_inventory()[
                "no_generated_reports_or_logs"
            ]
        )


def _complete_record_for(definition):
    return _record_for(
        definition,
        fields={field: "source-backed complete" for field in definition.required_fields},
    )


def _record_for(definition, *, fields):
    return {
        "evidence_name": definition.evidence_name,
        "candidate_id": definition.candidate_id,
        "rule_resolved": definition.rule_resolved,
        "source_export_type": definition.accepted_source_type,
        "fields": fields,
    }


def _result_for(result, evidence_name):
    for row in result["validation_results"]:
        if row["evidence_name"] == evidence_name:
            return row
    raise AssertionError(f"missing validation row for {evidence_name}")


if __name__ == "__main__":
    unittest.main()
