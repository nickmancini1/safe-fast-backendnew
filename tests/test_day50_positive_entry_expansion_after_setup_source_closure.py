import json
import unittest
from pathlib import Path

from historical_signal_replay import (
    day50_positive_entry_expansion_after_setup_source_closure as expansion,
)


class Day50PositiveEntryExpansionAfterSetupSourceClosureTests(unittest.TestCase):
    def test_builds_zero_candidate_gate_after_closure(self):
        document = expansion.build_expansion_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        self.assertEqual(document["result_version"], expansion.RESULT_VERSION)
        self.assertEqual(document["source_pool_count"], 24)
        self.assertEqual(document["candidate_count"], 0)
        self.assertEqual(document["candidate_records"], [])
        self.assertEqual(document["deterministic_comparison"]["result"], "PASS")

        scorecard = document["combined_scorecard"]
        self.assertEqual(scorecard["candidates_found"], 0)
        self.assertEqual(scorecard["trade_candidate_count"], 0)
        self.assertEqual(scorecard["missing_data_cases"], 0)
        self.assertEqual(scorecard["true_no_trades"], 0)
        self.assertEqual(scorecard["valid_trades_captured"], 0)

    def test_closed_candidates_are_regression_only_not_selected(self):
        document = expansion.build_expansion_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        closed = {
            record["candidate_identifier"]: record
            for record in document["closed_candidates_regression_records"]
        }
        scan = {
            record["candidate_identifier"]: record
            for record in document["scan_records"]
        }

        self.assertEqual(set(closed), expansion.CLOSED_SETUP_SOURCE_CANDIDATE_IDS)
        for candidate_id in expansion.CLOSED_SETUP_SOURCE_CANDIDATE_IDS:
            self.assertTrue(closed[candidate_id]["regression_only"])
            self.assertFalse(scan[candidate_id]["eligible_for_expansion"])
            self.assertIn(
                "closed_setup_source_regression_only",
                scan[candidate_id]["ineligible_reasons"],
            )

    def test_no_vague_missing_data_batch_or_data_request_is_created(self):
        document = expansion.build_expansion_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        self.assertFalse(document["option_request_included"])
        self.assertFalse(document["exit_path_request_included"])
        self.assertFalse(document["databento_downloaded"])
        self.assertFalse(document["databento_cost_check"]["credential_used"])
        self.assertEqual(document["databento_cost_check"]["checked_cost"], "NOT_AVAILABLE")
        self.assertIn(
            "accepted_complete_setup_evidence_absent",
            document["ineligible_reason_totals"],
        )
        self.assertGreater(
            document["ineligible_reason_totals"]["accepted_complete_setup_evidence_absent"],
            0,
        )

    def test_existing_regression_controls_are_preserved(self):
        document = expansion.build_expansion_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        existing = document["existing_regression_control_result"]
        self.assertEqual(existing["candidate_count"], 15)
        self.assertEqual(existing["deterministic_result"], "PASS")
        self.assertEqual(existing["combined_scorecard"]["valid_trades_captured"], 1)
        self.assertEqual(existing["combined_scorecard"]["true_no_trades"], 4)

    def test_next_task_routes_to_accepted_setup_evidence_intake(self):
        document = expansion.build_expansion_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        self.assertEqual(
            document["next_task"]["filename"],
            expansion.NEXT_TASK_FILENAME,
        )
        self.assertEqual(
            document["next_task"]["route"],
            "accepted_complete_setup_evidence_intake_before_next_expansion",
        )
        self.assertFalse(document["proof_accepted"])
        self.assertFalse(document["profitability_claimed"])
        self.assertFalse(document["promotion_decision_made"])

    def test_file_writer_creates_result(self):
        root = Path(__file__).resolve().parents[1]
        result_path = (
            root
            / "historical_signal_replay"
            / "results"
            / "test_day50_post_closure_expansion_tmp.json"
        )
        try:
            written = expansion.write_expansion_document(
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
