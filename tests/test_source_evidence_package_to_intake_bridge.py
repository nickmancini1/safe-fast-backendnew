import io
import unittest
from contextlib import redirect_stdout

from watcher_foundation import source_evidence_package_intake as intake
from watcher_foundation import source_evidence_package_to_intake_bridge as bridge


class SourceEvidencePackageToIntakeBridgeTests(unittest.TestCase):
    def test_all_nine_requests_are_mapped(self):
        result = bridge.bridge_in_memory_rows(_complete_rows_by_file())

        self.assertEqual(result["request_count"], 9)
        self.assertEqual(result["requests_mapped_count"], 9)
        self.assertEqual(len(result["bridge_request_results"]), 9)
        self.assertEqual(
            {row["evidence_name"] for row in result["bridge_request_results"]},
            {requirement.evidence_name for requirement in intake.build_package_requirements()},
        )

    def test_all_four_parked_candidates_are_mapped(self):
        result = bridge.bridge_in_memory_rows(_complete_rows_by_file())

        self.assertEqual(result["parked_candidate_count"], 4)
        self.assertEqual(result["parked_candidates_mapped_count"], 4)
        self.assertEqual(
            {row["candidate_id"] for row in result["candidate_bridge_results"]},
            set(bridge.CANDIDATE_EVIDENCE_REQUIREMENTS),
        )

    def test_candidate_stays_parked_when_any_required_request_fails(self):
        rows_by_file = _complete_rows_by_file()
        first_requirement = intake.build_package_requirements()[0]
        rows_by_file[first_requirement.required_file_name][0]["fill_status"] = "unfilled"

        result = bridge.bridge_in_memory_rows(rows_by_file)
        qqq_row = _candidate(result, "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001")

        self.assertFalse(qqq_row["all_required_requests_passed"])
        self.assertEqual(qqq_row["decision"], bridge.PARKED_STATUS)
        self.assertFalse(qqq_row["intake_ready_after_bridge"])
        self.assertIn(first_requirement.evidence_name, qqq_row["failed_evidence_names"])

    def test_candidate_becomes_reconsideration_eligible_only_when_all_required_pass(self):
        rows_by_file = {}
        for requirement in intake.build_package_requirements():
            if requirement.candidate_id == "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003":
                rows_by_file[requirement.required_file_name] = [_complete_row(requirement)]

        partial_result = bridge.bridge_in_memory_rows(rows_by_file)
        spy_cfb_003 = _candidate(
            partial_result, "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003"
        )
        qqq_cfb = _candidate(
            partial_result, "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001"
        )

        self.assertTrue(spy_cfb_003["all_required_requests_passed"])
        self.assertEqual(spy_cfb_003["decision"], bridge.RECONSIDERATION_STATUS)
        self.assertFalse(spy_cfb_003["intake_ready_after_bridge"])
        self.assertFalse(qqq_cfb["all_required_requests_passed"])
        self.assertEqual(qqq_cfb["decision"], bridge.PARKED_STATUS)

    def test_current_empty_work_package_has_zero_reconsideration_eligible_candidates(self):
        result = bridge.bridge_work_package_path()

        self.assertEqual(result["passed_request_count"], 0)
        self.assertEqual(result["failed_request_count"], 9)
        self.assertEqual(result["reconsideration_eligible_count"], 0)
        for row in result["candidate_bridge_results"]:
            self.assertEqual(row["decision"], bridge.PARKED_STATUS)

    def test_counts_remain_unchanged(self):
        result = bridge.bridge_work_package_path()

        self.assertEqual(result["intake_ready_count"], 0)
        self.assertEqual(result["parked_count"], 4)
        self.assertEqual(result["replace_count"], 3)

    def test_proof_and_profitability_claims_are_absent(self):
        result = bridge.bridge_in_memory_rows(_complete_rows_by_file())

        self.assertFalse(result["proof_accepted"])
        self.assertFalse(result["profitability_claimed"])
        self.assertTrue(bridge.NO_PROOF_ACCEPTED)
        self.assertFalse(bridge.PROFITABILITY_CLAIMED)
        for row in result["candidate_bridge_results"]:
            self.assertFalse(row["proof_allowed"])

    def test_cli_runs_stdout_only(self):
        output = io.StringIO()

        with redirect_stdout(output):
            bridge.main([])

        report = output.getvalue()
        self.assertIn("SAFE-FAST evidence package to intake bridge", report)
        self.assertIn("requests mapped: 9", report)
        self.assertIn("parked candidates mapped: 4", report)
        self.assertIn("passed requests: 0", report)
        self.assertIn("failed requests: 9", report)
        self.assertIn("reconsideration-eligible candidates: 0", report)
        self.assertIn("intake-ready count: 0", report)
        self.assertIn("parked count: 4", report)
        self.assertIn("replace count: 3", report)
        self.assertIn("proof accepted: NO", report)
        self.assertIn("profitability claim made: NO", report)


def _candidate(result, candidate_id):
    for row in result["candidate_bridge_results"]:
        if row["candidate_id"] == candidate_id:
            return row
    raise AssertionError(f"missing candidate {candidate_id}")


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
