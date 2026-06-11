import io
import unittest
from contextlib import redirect_stdout

from watcher_foundation import source_evidence_gap_scanner as scanner


EXPECTED_PARKED_IDS = {
    "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001",
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003",
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002",
    "SPY-REAL-HISTORICAL-IDEAL-001",
}

EXPECTED_FAMILIES = {
    "QQQ gap-context completeness",
    "Clean Fast Break stale/spent expiry",
    "Clean Fast Break higher-base/fresh-break expiry",
    "Clean Fast Break initial-break expiry",
    "SPY Ideal stale/spent expiry",
    "complete context/caution fields",
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


class SourceEvidenceGapScannerTests(unittest.TestCase):
    def test_all_four_parked_rows_are_covered(self):
        result = scanner.build_gap_scan()

        self.assertEqual(set(result["parked_candidate_ids"]), EXPECTED_PARKED_IDS)
        self.assertEqual(set(result["current_repo_data_sufficient_by_candidate"]), EXPECTED_PARKED_IDS)
        self.assertEqual(result["parked_rows_covered"], 4)

    def test_every_required_evidence_family_is_represented(self):
        result = scanner.build_gap_scan()

        self.assertEqual(set(result["required_evidence_families"]), EXPECTED_FAMILIES)
        self.assertEqual(set(result["required_evidence_families_represented"]), EXPECTED_FAMILIES)

    def test_missing_repo_data_is_marked_no_for_every_gap_row(self):
        result = scanner.build_gap_scan()

        self.assertEqual(result["gap_row_count"], 9)
        for row in result["gap_rows"]:
            self.assertFalse(row["current_repo_has_required_evidence"])
            self.assertFalse(row["current_repo_data_sufficient_for_row"])
            self.assertNotEqual(row["missing_field_names_or_rule_names"], ())
            self.assertNotEqual(row["source_files_checked"], ())
            self.assertFalse(row["proof_allowed"])

    def test_every_missing_evidence_item_has_an_acquisition_request(self):
        result = scanner.build_gap_scan()
        requests_by_key = {
            (request["candidate_id"], request["rule_resolved"], request["evidence_name"]): request
            for request in result["acquisition_requests"]
        }
        request_pairs = {
            (request["candidate_id"], tuple(request["required_fields"]))
            for request in result["acquisition_requests"]
        }

        self.assertEqual(result["acquisition_request_count"], 9)
        self.assertEqual(set(result["acquisition_request_candidate_ids"]), EXPECTED_PARKED_IDS)
        self.assertEqual(set(result["acquisition_request_evidence_names"]), EXPECTED_REQUEST_NAMES)
        self.assertEqual(len(requests_by_key), 9)
        for row in result["gap_rows"]:
            self.assertIn(
                (row["candidate_id"], tuple(row["missing_field_names_or_rule_names"])),
                request_pairs,
            )

    def test_acquisition_requests_include_required_task_fields(self):
        result = scanner.build_gap_scan()

        for request in result["acquisition_requests"]:
            self.assertIn(request["candidate_id"], EXPECTED_PARKED_IDS)
            self.assertIn(request["symbol"], {"QQQ", "SPY"})
            self.assertIn(request["setup_type"], {"Clean Fast Break", "Ideal"})
            self.assertNotEqual(request["evidence_name"], "")
            self.assertNotEqual(request["required_source_export_type"], "")
            self.assertNotEqual(request["required_timestamp_session_window"], "")
            self.assertNotEqual(request["required_fields"], ())
            self.assertNotEqual(request["why_needed"], "")
            self.assertNotEqual(request["rule_resolved"], "")
            self.assertFalse(request["current_repo_data_can_supply"])
            self.assertIn("rerun", request["expected_action_after_acquisition"].lower())

    def test_current_repo_data_is_not_sufficient_for_any_parked_row(self):
        result = scanner.build_gap_scan()

        self.assertTrue(
            all(
                has_data is False
                for has_data in result["current_repo_data_sufficient_by_candidate"].values()
            )
        )

    def test_parked_rows_stay_parked_and_counts_do_not_change(self):
        result = scanner.build_gap_scan()

        self.assertEqual(result["intake_ready_count"], 0)
        self.assertEqual(result["parked_count"], 4)
        self.assertEqual(result["replace_count"], 3)
        for row in result["gap_rows"]:
            self.assertEqual(row["parked_status"], "parked/source_data_insufficient")

    def test_names_exact_missing_fields_by_row(self):
        result = scanner.build_gap_scan()
        by_id = {}
        for row in result["gap_rows"]:
            by_id.setdefault(row["candidate_id"], set()).update(
                row["missing_field_names_or_rule_names"]
            )

        self.assertIn("gap_context_status", by_id["QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001"])
        self.assertIn(
            "clean_fast_break_stale_spent_expiry_rule",
            by_id["QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001"],
        )
        self.assertIn(
            "clean_fast_break_higher_base_fresh_break_expiry_rule",
            by_id["SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003"],
        )
        self.assertIn(
            "clean_fast_break_initial_break_expiry_rule",
            by_id["SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002"],
        )
        self.assertIn("spy_ideal_stale_spent_expiry_rule", by_id["SPY-REAL-HISTORICAL-IDEAL-001"])
        self.assertIn("option_context_status", by_id["SPY-REAL-HISTORICAL-IDEAL-001"])
        self.assertIn("execution_context_status", by_id["SPY-REAL-HISTORICAL-IDEAL-001"])

    def test_existing_schema_fields_are_reported_without_treating_them_as_complete(self):
        result = scanner.build_gap_scan()
        context_rows = [
            row for row in result["gap_rows"] if row["evidence_family"] == "complete context/caution fields"
        ]

        self.assertEqual(len(context_rows), 4)
        for row in context_rows:
            self.assertIn("context_24h_status", row["existing_source_fields_found"])
            self.assertIn("macro_context_status", row["existing_source_fields_found"])
            self.assertIn("iv_context_status", row["existing_source_fields_found"])
            self.assertIn("event_context_status", row["existing_source_fields_found"])
            self.assertIn("option_context_status", row["missing_field_names_or_rule_names"])
            self.assertFalse(row["current_repo_has_required_evidence"])

    def test_no_proof_or_profitability_claims_are_present(self):
        result = scanner.build_gap_scan()
        report = scanner.format_gap_scan_report(result)

        self.assertTrue(scanner.NO_PROOF_ACCEPTED)
        self.assertFalse(scanner.PROFITABILITY_CLAIMED)
        self.assertFalse(result["proof_accepted"])
        self.assertFalse(result["profitability_claimed"])
        for request in result["acquisition_requests"]:
            self.assertFalse(request["current_repo_data_can_supply"])
        self.assertNotIn("proof accepted: yes", report.lower())
        self.assertNotIn("profitability claim made: yes", report.lower())

    def test_cli_runs_stdout_only(self):
        output = io.StringIO()

        with redirect_stdout(output):
            scanner.main()

        report = output.getvalue()
        self.assertIn("SAFE-FAST source-evidence gap scanner", report)
        self.assertIn("parked rows covered: 4", report)
        self.assertIn("intake-ready count: 0", report)
        self.assertIn("parked count: 4", report)
        self.assertIn("replace count: 3", report)
        self.assertIn("acquisition request path: SAFE_FAST_SOURCE_EVIDENCE_ACQUISITION_REQUEST.md", report)
        self.assertIn("acquisition requests: 9", report)
        self.assertIn("acquisition request summary:", report)
        self.assertIn("QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001=NO", report)
        self.assertIn("SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003=NO", report)
        self.assertIn("proof accepted: NO", report)
        self.assertIn("profitability claim made: NO", report)
        self.assertTrue(scanner.build_gap_scan()["no_generated_reports_or_logs"])


if __name__ == "__main__":
    unittest.main()
