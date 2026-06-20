import json
import unittest
from pathlib import Path

from historical_signal_replay import day49_grouped_positive_entry_setup_field_completion as completion


class Day49GroupedPositiveEntrySetupFieldCompletionTests(unittest.TestCase):
    def test_completion_reviews_exactly_the_frozen_eight_candidates(self):
        document = completion.build_setup_field_completion_document(
            source_commit="testsha",
            run_timestamp="2026-06-20T00:00:00Z",
        )

        self.assertEqual(document["result_version"], completion.RESULT_VERSION)
        self.assertEqual(document["candidate_count"], 8)
        self.assertEqual(document["deterministic_comparison"]["result"], "PASS")
        self.assertFalse(document["proof_accepted"])
        self.assertFalse(document["profitability_claimed"])
        self.assertFalse(document["databento_downloaded"])

        candidate_ids = {record["candidate_identifier"] for record in document["candidate_records"]}
        self.assertEqual(candidate_ids, set(completion.FIELD_COMPLETION_EVIDENCE))

    def test_all_candidates_remain_missing_data_before_trade_candidate_stage(self):
        document = completion.build_setup_field_completion_document(
            source_commit="testsha",
            run_timestamp="2026-06-20T00:00:00Z",
        )
        combined = document["combined_scorecard"]

        self.assertEqual(combined["candidates_found"], 8)
        self.assertEqual(combined["setup_developing_count"], 8)
        self.assertEqual(combined["setup_qualified_count"], 0)
        self.assertEqual(combined["trade_candidate_count"], 0)
        self.assertEqual(combined["contracts_selected"], 0)
        self.assertEqual(combined["true_no_trades"], 0)
        self.assertEqual(combined["missing_data_cases"], 8)
        self.assertEqual(combined["missed_valid_trades"], 0)
        self.assertEqual(combined["invalid_trades_allowed"], 0)
        self.assertEqual(combined["first_blocker_totals_by_funnel_stage"], {"SETUP_QUALIFIED": 8})

        for record in document["candidate_records"]:
            self.assertFalse(record["setup_qualified"])
            self.assertFalse(record["trade_candidate"])
            self.assertEqual(record["final_classification"], "MISSING_DATA")
            self.assertTrue(record["missing_data_not_true_no_trade"])
            self.assertEqual(record["highest_stage_reached"], "SETUP_DEVELOPING")
            self.assertEqual(record["first_stage_not_reached"], "SETUP_QUALIFIED")

    def test_iwm_gld_replacement_evidence_is_blocked_or_unavailable_not_promoted(self):
        document = completion.build_setup_field_completion_document(
            source_commit="testsha",
            run_timestamp="2026-06-20T00:00:00Z",
        )
        by_id = {record["candidate_identifier"]: record for record in document["candidate_records"]}

        self.assertEqual(
            by_id["GLD-REPLACEMENT-IDEAL-CANDIDATE-001"]["setup_field_review_status"],
            "blocked_missing_evidence",
        )
        self.assertIn("GLD source rows 204-238 exist", by_id["GLD-REPLACEMENT-IDEAL-CANDIDATE-001"]["setup_time_row"])
        self.assertEqual(
            by_id["GLD-REPLACEMENT-IDEAL-CANDIDATE-002"]["setup_field_review_status"],
            "unavailable",
        )
        self.assertIn("no second exact GLD Ideal source window", by_id["GLD-REPLACEMENT-IDEAL-CANDIDATE-002"]["setup_time_row"])
        self.assertIn("IWM source rows 141-210 exist", by_id["IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001"]["setup_time_row"])
        self.assertIn("IWM source rows 190-210 exist", by_id["IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002"]["setup_time_row"])

    def test_spy_qqq_source_windows_preserve_unclear_freshness_and_session_boundaries(self):
        document = completion.build_setup_field_completion_document(
            source_commit="testsha",
            run_timestamp="2026-06-20T00:00:00Z",
        )
        by_id = {record["candidate_identifier"]: record for record in document["candidate_records"]}

        self.assertIn("SPY source CSV lines 79-99", by_id["SPY-SOURCE-WINDOW-CLEAN-FAST-BREAK-003"]["setup_time_row"])
        self.assertEqual(
            by_id["SPY-SOURCE-WINDOW-CONTINUATION-004"]["session_boundary_behavior"],
            "unclear_2026_04_07_recovery_or_invalidation",
        )
        self.assertEqual(
            by_id["SPY-SOURCE-WINDOW-CONTINUATION-005"]["session_boundary_behavior"],
            "unclear_same_lifecycle_follow_through_after_2026_04_30",
        )
        self.assertEqual(
            by_id["QQQ-SOURCE-WINDOW-CONTINUATION-002"]["session_boundary_behavior"],
            "unclear_same_rebound_context_after_q_q_q_lines_66_86",
        )

    def test_no_option_cost_check_is_created_without_trade_candidates(self):
        document = completion.build_setup_field_completion_document(
            source_commit="testsha",
            run_timestamp="2026-06-20T00:00:00Z",
        )

        cost_check = document["setup_time_option_cost_check"]
        self.assertFalse(cost_check["created"])
        self.assertEqual(cost_check["checked_cost"], "NOT_AVAILABLE")
        self.assertEqual(cost_check["actual_billed_cost"], "NOT_AVAILABLE")
        self.assertEqual(cost_check["candidates_reaching_trade_candidate"], [])
        self.assertEqual(
            document["next_routing"]["next_task_file"],
            "SAFE_FAST_DAY49_GROUPED_POSITIVE_ENTRY_NEXT_DETERMINISTIC_CANDIDATE_BATCH_CODEX_TASK.md",
        )

    def test_file_writer_creates_machine_readable_result(self):
        root = Path(__file__).resolve().parents[1]
        result_path = root / "historical_signal_replay" / "results" / "test_day49_setup_field_completion_tmp.json"
        try:
            written = completion.write_setup_field_completion_document(
                result_path,
                source_commit="testsha",
                run_timestamp="2026-06-20T00:00:00Z",
            )
            loaded = json.loads(result_path.read_text(encoding="utf-8"))
        finally:
            if result_path.exists():
                result_path.unlink()

        self.assertEqual(written, loaded)
        self.assertEqual(loaded["combined_scorecard"]["missing_data_cases"], 8)


if __name__ == "__main__":
    unittest.main()
