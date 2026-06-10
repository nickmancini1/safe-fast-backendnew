import io
import unittest
from contextlib import redirect_stdout

from watcher_foundation import candidate_source_pool_intake as intake


STRICT_SOURCE_BACKED_IDS = {
    "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001",
    "QQQ-REAL-HISTORICAL-CONTINUATION-001",
    "SPY-REAL-HISTORICAL-CONTINUATION-001",
    "SPY-REAL-HISTORICAL-IDEAL-001",
    "QQQ-REAL-HISTORICAL-IDEAL-001",
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002",
}


class CandidateSourcePoolIntakeTests(unittest.TestCase):
    def test_inspects_full_24_row_pool_but_accepts_only_strict_source_backed_rows(self):
        result = intake.build_source_pool_intake()

        self.assertEqual(result["source_pool_rows_inspected"], 24)
        self.assertEqual(result["accepted_intake_count"], 6)
        self.assertEqual({row["candidate_id"] for row in result["accepted_rows"]}, STRICT_SOURCE_BACKED_IDS)

    def test_accepted_rows_have_required_intake_fields_without_missing_values(self):
        result = intake.build_source_pool_intake()

        for row in result["accepted_rows"]:
            self.assertEqual(set(intake.INTAKE_OUTPUT_FIELDS), set(row))
            for field in (
                "source_file",
                "source_lines_section",
                "setup_candle",
                "trigger",
                "invalidation",
                "no_hindsight_boundary",
                "outcome_window",
            ):
                self.assertNotIn("MISSING", row[field])
                self.assertNotEqual(row[field], "")

    def test_no_rows_are_intake_ready_until_freshness_and_blocker_are_resolved(self):
        result = intake.build_source_pool_intake()

        self.assertEqual(result["intake_ready_count"], 0)
        self.assertEqual(result["blocked_count"], 6)
        self.assertEqual(result["drop_count"], 0)
        self.assertEqual(result["replace_count"], 0)
        self.assertEqual(result["duplicate_count"], 0)
        self.assertEqual(result["close_ready_count"], 6)
        self.assertTrue(result["at_least_5_intake_ready_or_close_ready"])
        self.assertIn("freshness/final-signal", result["top_remaining_blocker_family"])

    def test_duplicate_drop_replace_and_chart_shape_only_rows_are_rejected_at_intake(self):
        result = intake.build_source_pool_intake()
        accepted_ids = {row["candidate_id"] for row in result["accepted_rows"]}

        self.assertNotIn("SPY-SOURCE-WINDOW-CONTINUATION-002", accepted_ids)
        self.assertNotIn("SPY-SOURCE-WINDOW-CONTINUATION-003", accepted_ids)
        self.assertNotIn("QQQ-SOURCE-WINDOW-CLEAN-FAST-BREAK-002", accepted_ids)
        self.assertNotIn("SPY-SOURCE-WINDOW-CLEAN-FAST-BREAK-003", accepted_ids)
        self.assertNotIn("SPY-SOURCE-WINDOW-CONTINUATION-005", accepted_ids)
        self.assertNotIn("SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-001", accepted_ids)

    def test_missing_no_hindsight_boundary_rejects_otherwise_source_backed_row(self):
        row = {
            "candidate_id": "STRICT-ROW-WITH-MISSING-NO-HINDSIGHT",
            "source_lines": "source.csv lines 1-2",
            "setup_candle": "2026-01-01T09:30:00-05:00",
            "trigger": "trigger recorded",
            "invalidation": "invalidation recorded",
            "no_hindsight_boundary": "MISSING",
            "outcome_window": "terminal input recorded",
            "duplicate": "no",
            "status": "blocked",
        }

        self.assertFalse(intake._strictly_source_backed(row))

    def test_reports_exact_blocker_when_local_sources_do_not_support_20_to_50_strict_rows(self):
        result = intake.build_source_pool_intake()

        self.assertEqual(result["maximum_strict_candidates_found"], 6)
        self.assertIn("do not support 20-50 strict candidates", result["exact_blocker"])
        self.assertGreaterEqual(len(result["source_files_inspected"]), 1)
        self.assertIn("complete freshness/final-signal", result["smallest_next_evidence_backed_fix"])

    def test_no_proof_or_profitability_claims_are_present(self):
        result = intake.build_source_pool_intake()
        report = intake.format_intake_report(result)

        self.assertTrue(intake.NO_PROOF_ACCEPTED)
        self.assertFalse(intake.PROFITABILITY_CLAIMED)
        self.assertFalse(result["proof_accepted"])
        self.assertFalse(result["profitability_claimed"])
        self.assertNotIn("proof accepted: yes", report.lower())
        self.assertNotIn("profitability claimed: yes", report.lower())

    def test_command_line_stdout_report_path_works(self):
        output = io.StringIO()

        with redirect_stdout(output):
            intake.main()

        report = output.getvalue()
        self.assertIn("source-pool rows inspected: 24", report)
        self.assertIn("accepted intake count: 6", report)
        self.assertIn("ranked intake table:", report)
        self.assertIn("QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001", report)


if __name__ == "__main__":
    unittest.main()
