import json
import unittest
from pathlib import Path

from historical_signal_replay import (
    day50_accepted_setup_evidence_replay_after_intake_closeout as closeout,
)


class Day50AcceptedSetupEvidenceReplayAfterIntakeCloseoutTests(unittest.TestCase):
    def test_closeout_closes_confirmed_safety_rejection_as_regression_only(self):
        document = closeout.build_closeout_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        record = document["closeout_record"]

        self.assertEqual(document["result_version"], closeout.RESULT_VERSION)
        self.assertEqual(record["candidate_identifier"], closeout.TARGET_CANDIDATE_ID)
        self.assertEqual(record["closeout_status"], "CLOSED_CONFIRMED_SAFETY_REJECTION")
        self.assertEqual(record["final_classification"], "TRUE_NO_TRADE_REGRESSION_ONLY")
        self.assertTrue(record["regression_only"])
        self.assertTrue(record["safety_rejection_legitimate"])
        self.assertFalse(record["evidence_or_harness_problem"])

    def test_closeout_preserves_positive_entry_gate_and_quote_age_anchor(self):
        document = closeout.build_closeout_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        record = document["closeout_record"]

        self.assertEqual(record["highest_stage_reached"], "SETUP_QUALIFIED")
        self.assertEqual(record["first_stage_not_reached"], "TRADE_CANDIDATE")
        self.assertTrue(record["setup_qualified"])
        self.assertFalse(record["trade_candidate"])
        self.assertEqual(record["blocker_caution_review"], "fail")
        self.assertEqual(record["exact_blocker_field"], "blocker_caution_review")
        self.assertEqual(record["exact_blocker_code"], "quote_age_above_5_minutes")
        self.assertEqual(record["day48_regression_classification"], "TRUE_NO_TRADE")

    def test_policy_does_not_reopen_or_replay_forbidden_inputs(self):
        document = closeout.build_closeout_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        policy = document["closeout_policy"]

        self.assertTrue(policy["close_confirmed_safety_rejection_as_regression_only"])
        self.assertTrue(policy["route_to_next_evidence_backed_positive_entry_batch"])
        self.assertFalse(policy["new_candidate_scan_run"])
        self.assertFalse(policy["closed_setup_source_candidates_reopened"])
        self.assertFalse(policy["rejected_intake_rows_replayed"])
        self.assertFalse(policy["governance_only_chain_created"])
        self.assertFalse(policy["frozen_rules_weakened"])

    def test_scorecard_has_no_trade_candidate_or_missing_data(self):
        document = closeout.build_closeout_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        scorecard = document["scorecard"]

        self.assertEqual(scorecard["accepted_replay_records_closed"], 1)
        self.assertEqual(scorecard["confirmed_safety_rejections_closed"], 1)
        self.assertEqual(scorecard["regression_only_true_no_trades"], 1)
        self.assertEqual(scorecard["trade_candidates"], 0)
        self.assertEqual(scorecard["evidence_or_harness_problems"], 0)
        self.assertEqual(scorecard["missing_data_cases"], 0)
        self.assertEqual(scorecard["unresolved_cases"], 0)
        self.assertEqual(scorecard["closed_setup_source_candidates_reopened"], 0)
        self.assertEqual(scorecard["rejected_intake_rows_replayed"], 0)

    def test_routes_to_next_evidence_backed_positive_entry_batch(self):
        document = closeout.build_closeout_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        self.assertEqual(
            document["next_task"]["filename"],
            closeout.NEXT_TASK_FILENAME,
        )
        self.assertEqual(
            document["next_task"]["route"],
            "evidence_backed_positive_entry_testing_batch",
        )
        self.assertIn("positive-entry", document["next_task"]["reason"])
        self.assertIn("governance-only", document["next_task"]["reason"])

    def test_no_data_download_or_option_exit_request_is_created(self):
        document = closeout.build_closeout_document(
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
            / "test_day50_accepted_setup_evidence_replay_after_intake_closeout_tmp.json"
        )
        try:
            written = closeout.write_closeout_document(
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
