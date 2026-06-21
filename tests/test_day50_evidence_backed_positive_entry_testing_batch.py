import json
import unittest
from pathlib import Path

from historical_signal_replay import (
    day50_evidence_backed_positive_entry_testing_batch as batch,
)


class Day50EvidenceBackedPositiveEntryTestingBatchTests(unittest.TestCase):
    def test_batch_preserves_concrete_positive_entry_totals(self):
        document = batch.build_batch_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        scorecard = document["scorecard"]

        self.assertEqual(document["result_version"], batch.RESULT_VERSION)
        self.assertEqual(document["candidate_count"], 15)
        self.assertEqual(scorecard["setup_qualified_candidates"], 13)
        self.assertEqual(scorecard["trade_candidates"], 9)
        self.assertEqual(scorecard["selected_contracts"], 5)
        self.assertEqual(scorecard["eligible_entries"], 1)
        self.assertEqual(scorecard["recorded_entries"], 1)
        self.assertEqual(scorecard["exits_evaluated"], 1)
        self.assertEqual(document["deterministic_comparison"]["result"], "PASS")

    def test_scorecard_keeps_required_classifications_separate(self):
        document = batch.build_batch_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        self.assertEqual(document["final_classifications"]["VALID_TRADE_CAPTURED"], 1)
        self.assertEqual(document["final_classifications"]["TRUE_NO_TRADE"], 4)
        self.assertEqual(document["final_classifications"]["MISSING_DATA"], 6)
        self.assertEqual(document["final_classifications"]["MISSED_VALID_TRADE"], 0)
        self.assertEqual(document["final_classifications"]["INVALID_TRADE_ALLOWED"], 0)
        self.assertEqual(document["final_classifications"]["UNRESOLVED"], 4)

    def test_closed_qqq_safety_rejection_is_regression_only(self):
        document = batch.build_batch_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        by_id = {
            record["candidate_identifier"]: record
            for record in document["candidate_records"]
        }
        qqq = by_id[batch.QQQ_CLOSED_CANDIDATE_ID]

        self.assertTrue(qqq["regression_only"])
        self.assertTrue(qqq["blocks_live_candidate_replay"])
        self.assertEqual(
            qqq["day50_closeout_status"],
            "CLOSED_CONFIRMED_SAFETY_REJECTION",
        )
        self.assertEqual(
            qqq["day50_closeout_classification"],
            "TRUE_NO_TRADE_REGRESSION_ONLY",
        )
        self.assertEqual(
            document["closed_safety_rejection_control"]["exact_blocker_code"],
            "quote_age_above_5_minutes",
        )
        self.assertEqual(
            document["scorecard"]["closed_safety_rejections_rerun_as_live_candidates"],
            0,
        )

    def test_policy_forbids_new_scans_rejected_rows_and_closed_source_reopens(self):
        document = batch.build_batch_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        policy = document["batch_policy"]

        self.assertFalse(policy["new_candidate_scan_run"])
        self.assertFalse(policy["closed_setup_source_candidates_reopened"])
        self.assertFalse(policy["rejected_intake_rows_replayed"])
        self.assertFalse(policy["confirmed_qqq_safety_rejection_rerun_as_live_candidate"])
        self.assertTrue(policy["qqq_closed_candidate_preserved_as_regression_only"])
        self.assertFalse(policy["frozen_rules_weakened"])
        self.assertFalse(policy["governance_only_chain_created"])

    def test_no_data_download_auth_or_readiness_claim_is_created(self):
        document = batch.build_batch_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        self.assertFalse(document["option_request_included"])
        self.assertFalse(document["exit_path_request_included"])
        self.assertFalse(document["databento_downloaded"])
        self.assertFalse(document["raw_vendor_data_changed"])
        self.assertFalse(document["schwab_authenticated"])
        self.assertFalse(document["broker_mutation_attempted"])
        self.assertFalse(document["proof_accepted"])
        self.assertFalse(document["profitability_claimed"])
        self.assertFalse(document["promotion_decision_made"])
        self.assertFalse(document["paper_eligible"])
        self.assertFalse(document["live_eligible"])
        self.assertEqual(document["databento_cost_check"]["checked_cost"], "NOT_AVAILABLE")

    def test_next_task_is_exactly_one_grouped_task(self):
        document = batch.build_batch_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        self.assertEqual(document["next_task"]["filename"], batch.NEXT_TASK_FILENAME)
        self.assertEqual(
            document["next_task"]["route"],
            "positive_entry_selected_contract_blocker_closeout",
        )

    def test_file_writer_creates_result(self):
        root = Path(__file__).resolve().parents[1]
        result_path = (
            root
            / "historical_signal_replay"
            / "results"
            / "test_day50_evidence_backed_positive_entry_testing_batch_tmp.json"
        )
        try:
            written = batch.write_batch_document(
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
