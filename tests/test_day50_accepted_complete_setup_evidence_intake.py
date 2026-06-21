import json
import unittest
from pathlib import Path

from historical_signal_replay import day50_accepted_complete_setup_evidence_intake as intake


class Day50AcceptedCompleteSetupEvidenceIntakeTests(unittest.TestCase):
    def test_ingests_only_accepted_complete_setup_evidence(self):
        document = intake.build_intake_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        self.assertEqual(document["result_version"], intake.RESULT_VERSION)
        self.assertEqual(document["candidate_count"], 4)
        self.assertEqual(document["deterministic_comparison"]["result"], "PASS")

        scorecard = document["scorecard"]
        self.assertEqual(scorecard["accepted_complete_setup_evidence_ingested"], 1)
        self.assertEqual(scorecard["setup_qualified_candidates"], 1)
        self.assertEqual(scorecard["trade_candidates"], 0)
        self.assertEqual(scorecard["trade_blocked_by_accepted_caution_fail"], 1)
        self.assertEqual(scorecard["missing_data_cases"], 0)

    def test_qqq_cfb_is_accepted_but_not_trade_candidate(self):
        document = intake.build_intake_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        record = _candidate(document, "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001")

        self.assertEqual(
            record["setup_evidence_intake_status"],
            "ACCEPTED_COMPLETE_SETUP_EVIDENCE_INGESTED",
        )
        self.assertEqual(record["highest_stage_reached"], "SETUP_QUALIFIED")
        self.assertEqual(record["first_stage_not_reached"], "TRADE_CANDIDATE")
        self.assertTrue(record["setup_qualified"])
        self.assertFalse(record["trade_candidate"])
        self.assertEqual(
            record["final_classification"],
            "ACCEPTED_COMPLETE_SETUP_EVIDENCE_TRADE_BLOCKED",
        )
        self.assertEqual(record["field_results"]["blocker_caution_review"]["value"], "fail")

    def test_incomplete_context_candidates_are_rejected_with_exact_fields(self):
        document = intake.build_intake_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        rejected_ids = {
            record["candidate_identifier"]
            for record in document["rejected_candidate_records"]
        }

        self.assertEqual(
            rejected_ids,
            {
                "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002",
                "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003",
                "SPY-REAL-HISTORICAL-IDEAL-001",
            },
        )
        for candidate_id in rejected_ids:
            record = _candidate(document, candidate_id)
            self.assertIn(
                "blocker_caution_review",
                record["incomplete_or_unaccepted_setup_fields"],
            )
            self.assertEqual(
                record["setup_evidence_intake_status"],
                "NOT_ACCEPTED_COMPLETE_SETUP_EVIDENCE",
            )

    def test_closed_setup_source_candidates_remain_regression_only(self):
        document = intake.build_intake_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        closed = document["closed_candidates_regression_records"]
        self.assertEqual(len(closed), 4)
        self.assertTrue(all(record["regression_only"] for record in closed))
        candidate_ids = {
            record["candidate_identifier"] for record in document["candidate_records"]
        }
        self.assertTrue(
            candidate_ids.isdisjoint(
                {record["candidate_identifier"] for record in closed}
            )
        )

    def test_no_data_download_or_option_exit_request_is_created(self):
        document = intake.build_intake_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        self.assertFalse(document["option_request_included"])
        self.assertFalse(document["exit_path_request_included"])
        self.assertFalse(document["databento_downloaded"])
        self.assertFalse(document["raw_vendor_data_changed"])
        self.assertFalse(document["schwab_authenticated"])
        self.assertFalse(document["proof_accepted"])
        self.assertFalse(document["profitability_claimed"])
        self.assertEqual(document["databento_cost_check"]["checked_cost"], "NOT_AVAILABLE")

    def test_next_task_routes_to_replay_after_intake(self):
        document = intake.build_intake_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        self.assertEqual(document["next_task"]["filename"], intake.NEXT_TASK_FILENAME)
        self.assertEqual(
            document["next_task"]["route"],
            "accepted_setup_evidence_replay_after_intake",
        )

    def test_file_writer_creates_result(self):
        root = Path(__file__).resolve().parents[1]
        result_path = (
            root
            / "historical_signal_replay"
            / "results"
            / "test_day50_accepted_complete_setup_evidence_intake_tmp.json"
        )
        try:
            written = intake.write_intake_document(
                result_path,
                source_commit="testsha",
                run_timestamp="2026-06-21T00:00:00Z",
            )
            loaded = json.loads(result_path.read_text(encoding="utf-8"))
        finally:
            if result_path.exists():
                result_path.unlink()

        self.assertEqual(written, loaded)


def _candidate(document, candidate_id):
    for record in document["candidate_records"]:
        if record["candidate_identifier"] == candidate_id:
            return record
    raise AssertionError(f"missing candidate {candidate_id}")


if __name__ == "__main__":
    unittest.main()
