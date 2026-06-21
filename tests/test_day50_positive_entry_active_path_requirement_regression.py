import json
import unittest
from pathlib import Path

from historical_signal_replay import (
    day50_positive_entry_active_path_requirement_regression as regression,
)


class Day50PositiveEntryActivePathRequirementRegressionTests(unittest.TestCase):
    def test_tests_exactly_four_open_active_path_requirements(self):
        document = regression.build_regression_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        scorecard = document["scorecard"]

        self.assertEqual(document["result_version"], regression.RESULT_VERSION)
        self.assertEqual(scorecard["active_path_requirements_tested"], 4)
        self.assertEqual(scorecard["active_path_requirements_advanced_to_trade_candidate"], 0)
        self.assertEqual(scorecard["active_path_requirements_permanently_closed"], 4)
        self.assertEqual(scorecard["active_path_requirements_open_after_regression"], 0)
        self.assertEqual(document["deterministic_comparison"]["result"], "PASS")

    def test_each_case_is_closed_with_exact_failed_requirement(self):
        document = regression.build_regression_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        records = document["active_path_requirement_regression_records"]

        self.assertEqual(
            {record["tested_requirement"] for record in records},
            {"fresh_or_spent_unconfirmed", "prior_completed_shelf_break_spent_TO_REVIEW"},
        )
        for record in records:
            self.assertTrue(record["permanently_closed"])
            self.assertFalse(record["accepted_frozen_evidence_available_to_advance"])
            self.assertFalse(record["advanced_to_trade_candidate"])
            self.assertEqual(
                record["closeout_determination"],
                "permanently_closed_exact_failed_requirement",
            )
            self.assertNotEqual(record["exact_failed_requirement"], "")
            self.assertIn(record["tested_requirement"], record["fixture_primary_blocker"])
            self.assertEqual(record["classification_after_regression"], "MISSING_DATA")

    def test_records_name_exact_fields_sources_datasets_calculators_and_windows(self):
        document = regression.build_regression_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        for record in document["active_path_requirement_regression_records"]:
            self.assertNotEqual(record["field"], "")
            self.assertNotEqual(record["source"], "")
            self.assertNotEqual(record["fixture_path"], "")
            self.assertNotEqual(record["dataset_schema_or_api"], "")
            self.assertNotEqual(record["calculator"], "")
            self.assertIn("signal_time", record["timestamp_window"])
            self.assertEqual(
                record["timestamp_window"]["signal_time"],
                record["fixture_final_timestamp"],
            )
            self.assertNotEqual(record["failure_source_evidence"], "")
            self.assertIn("blocks TRADE_CANDIDATE", record["blocking_scope"])

    def test_before_and_after_totals_are_reported_and_preserved(self):
        document = regression.build_regression_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        scorecard = document["scorecard"]

        self.assertEqual(scorecard["trade_candidates_before_regression"], 9)
        self.assertEqual(scorecard["trade_candidates_after_regression"], 9)
        self.assertEqual(scorecard["selected_contracts_before_regression"], 5)
        self.assertEqual(scorecard["selected_contracts_after_regression"], 5)
        self.assertEqual(scorecard["eligible_entries_before_regression"], 1)
        self.assertEqual(scorecard["eligible_entries_after_regression"], 1)
        self.assertEqual(scorecard["recorded_entries_before_regression"], 1)
        self.assertEqual(scorecard["recorded_entries_after_regression"], 1)
        self.assertEqual(scorecard["additional_entries_established"], 0)

    def test_scorecard_reclassifies_open_unresolved_cases_as_exact_missing_data(self):
        document = regression.build_regression_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        before = document["final_classifications_before_regression"]
        after = document["final_classifications_after_regression"]
        self.assertEqual(before["VALID_TRADE_CAPTURED"], 1)
        self.assertEqual(before["TRUE_NO_TRADE"], 4)
        self.assertEqual(before["MISSING_DATA"], 6)
        self.assertEqual(before["UNRESOLVED"], 4)
        self.assertEqual(after["VALID_TRADE_CAPTURED"], 1)
        self.assertEqual(after["TRUE_NO_TRADE"], 4)
        self.assertEqual(after["MISSING_DATA"], 10)
        self.assertEqual(after["UNRESOLVED"], 0)
        self.assertEqual(after["MISSED_VALID_TRADE"], 0)
        self.assertEqual(after["INVALID_TRADE_ALLOWED"], 0)

    def test_policy_blocks_scans_downloads_reopens_and_readiness_claims(self):
        document = regression.build_regression_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        policy = document["regression_policy"]

        self.assertFalse(policy["new_candidate_scan_run"])
        self.assertFalse(policy["new_setup_source_pass_run"])
        self.assertFalse(policy["closed_setup_source_candidates_reopened"])
        self.assertFalse(policy["rejected_intake_rows_replayed"])
        self.assertFalse(policy["confirmed_qqq_safety_rejection_rerun_as_live_candidate"])
        self.assertTrue(policy["qqq_clean_fast_break_001_preserved_regression_only"])
        self.assertTrue(policy["qqq_ideal_preserved_outside_narrowed_path"])
        self.assertFalse(policy["frozen_rules_weakened"])
        self.assertFalse(policy["governance_only_chain_created"])
        self.assertFalse(policy["option_request_included"])
        self.assertFalse(policy["exit_path_request_included"])
        self.assertFalse(document["paid_data_request_created"])
        self.assertFalse(document["databento_downloaded"])
        self.assertFalse(document["schwab_authenticated"])
        self.assertFalse(document["proof_accepted"])
        self.assertFalse(document["profitability_claimed"])
        self.assertFalse(document["paper_eligible"])
        self.assertFalse(document["live_eligible"])

    def test_next_task_is_exactly_one_grouped_task(self):
        document = regression.build_regression_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        self.assertEqual(document["next_task"]["filename"], regression.NEXT_TASK_FILENAME)
        self.assertEqual(
            document["next_task"]["route"],
            "positive_entry_closed_requirement_scorecard_reconciliation",
        )

    def test_file_writer_creates_result(self):
        root = Path(__file__).resolve().parents[1]
        result_path = (
            root
            / "historical_signal_replay"
            / "results"
            / "test_day50_positive_entry_active_path_requirement_regression_tmp.json"
        )
        try:
            written = regression.write_regression_document(
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
