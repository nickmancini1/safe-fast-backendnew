import json
import unittest
from pathlib import Path

from historical_signal_replay import (
    day50_accepted_setup_evidence_replay_after_intake as replay,
)


class Day50AcceptedSetupEvidenceReplayAfterIntakeTests(unittest.TestCase):
    def test_replays_only_accepted_intake_record(self):
        document = replay.build_replay_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        self.assertEqual(document["result_version"], replay.RESULT_VERSION)
        self.assertEqual(document["accepted_intake_record_count"], 1)
        self.assertEqual(document["replay_record_count"], 1)
        self.assertEqual(
            document["replay_policy"]["accepted_record_ids"],
            [replay.TARGET_CANDIDATE_ID],
        )
        self.assertFalse(document["replay_policy"]["new_candidate_scan_run"])
        self.assertFalse(document["replay_policy"]["closed_setup_source_candidates_reopened"])
        self.assertFalse(document["replay_policy"]["rejected_intake_rows_replayed"])

    def test_accepted_fail_is_legitimate_safety_rejection(self):
        document = replay.build_replay_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        record = document["replay_records"][0]

        self.assertEqual(record["candidate_identifier"], replay.TARGET_CANDIDATE_ID)
        self.assertEqual(record["highest_stage_reached"], "SETUP_QUALIFIED")
        self.assertEqual(record["first_stage_not_reached"], "TRADE_CANDIDATE")
        self.assertTrue(record["setup_qualified"])
        self.assertFalse(record["trade_candidate"])
        self.assertEqual(record["blocker_caution_review"], "fail")
        self.assertEqual(
            record["final_classification"],
            "TRUE_NO_TRADE_LEGITIMATE_SAFETY_REJECTION",
        )
        self.assertTrue(record["safety_rejection_legitimate"])
        self.assertFalse(record["evidence_or_harness_problem"])

    def test_replay_anchors_to_existing_quote_age_failure(self):
        document = replay.build_replay_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        record = document["replay_records"][0]

        self.assertEqual(record["exact_blocker_field"], "blocker_caution_review")
        self.assertEqual(record["exact_blocker_code"], "quote_age_above_5_minutes")
        self.assertEqual(record["day48_regression_classification"], "TRUE_NO_TRADE")
        self.assertEqual(
            record["day48_regression_blocker_category"],
            "real frozen-rule failure",
        )
        self.assertEqual(
            record["day48_regression_failure_reason"],
            "quote_age_above_5_minutes",
        )

    def test_scorecard_has_no_missing_or_harness_problem(self):
        document = replay.build_replay_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        scorecard = document["scorecard"]

        self.assertEqual(scorecard["accepted_intake_records_replayed"], 1)
        self.assertEqual(scorecard["setup_qualified_candidates"], 1)
        self.assertEqual(scorecard["trade_candidates"], 0)
        self.assertEqual(scorecard["legitimate_safety_rejections"], 1)
        self.assertEqual(scorecard["evidence_or_harness_problems"], 0)
        self.assertEqual(scorecard["true_no_trades"], 1)
        self.assertEqual(scorecard["missing_data_cases"], 0)
        self.assertEqual(scorecard["unresolved_cases"], 0)

    def test_determination_is_safety_rejection_not_evidence_problem(self):
        document = replay.build_replay_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        self.assertEqual(
            document["determination"]["result"],
            "LEGITIMATE_SAFETY_REJECTION",
        )
        self.assertFalse(document["determination"]["harness_problem_found"])
        self.assertFalse(document["determination"]["evidence_problem_found"])

    def test_no_data_download_or_option_exit_request_is_created(self):
        document = replay.build_replay_document(
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

    def test_file_writer_creates_result(self):
        root = Path(__file__).resolve().parents[1]
        result_path = (
            root
            / "historical_signal_replay"
            / "results"
            / "test_day50_accepted_setup_evidence_replay_after_intake_tmp.json"
        )
        try:
            written = replay.write_replay_document(
                result_path,
                source_commit="testsha",
                run_timestamp="2026-06-21T00:00:00Z",
            )
            loaded = json.loads(result_path.read_text(encoding="utf-8"))
        finally:
            if result_path.exists():
                result_path.unlink()

        self.assertEqual(written, loaded)


if __name__ == "__main__":
    unittest.main()
