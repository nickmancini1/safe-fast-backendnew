import json
import unittest
from pathlib import Path

from historical_signal_replay import (
    day50_positive_entry_remaining_evidence_gap_closeout as closeout,
)


class Day50PositiveEntryRemainingEvidenceGapCloseoutTests(unittest.TestCase):
    def test_reviews_active_path_and_contract_selected_remaining_gaps(self):
        document = closeout.build_closeout_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        scorecard = document["scorecard"]

        self.assertEqual(document["result_version"], closeout.RESULT_VERSION)
        self.assertEqual(scorecard["remaining_evidence_gap_records_reviewed"], 6)
        self.assertEqual(scorecard["active_path_requirements_open_after_closeout"], 4)
        self.assertEqual(scorecard["contract_selected_gaps_closed_after_closeout"], 2)
        self.assertEqual(scorecard["additional_entries_established"], 0)
        self.assertEqual(document["deterministic_comparison"]["result"], "PASS")

    def test_before_and_after_totals_are_concrete_and_preserved(self):
        document = closeout.build_closeout_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        scorecard = document["scorecard"]

        self.assertEqual(scorecard["selected_contracts_before_closeout"], 5)
        self.assertEqual(scorecard["selected_contracts_after_closeout"], 5)
        self.assertEqual(scorecard["eligible_entries_before_closeout"], 1)
        self.assertEqual(scorecard["eligible_entries_after_closeout"], 1)
        self.assertEqual(scorecard["recorded_entries_before_closeout"], 1)
        self.assertEqual(scorecard["recorded_entries_after_closeout"], 1)
        self.assertEqual(scorecard["affected_cases_selected_contracts_before_closeout"], 0)
        self.assertEqual(scorecard["affected_cases_selected_contracts_after_closeout"], 0)
        self.assertEqual(scorecard["affected_cases_entry_eligible_after_closeout"], 0)
        self.assertEqual(scorecard["affected_cases_entries_recorded_after_closeout"], 0)

    def test_records_name_exact_fields_sources_datasets_calculators_and_windows(self):
        document = closeout.build_closeout_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        for record in document["remaining_evidence_gap_closeout_records"]:
            self.assertNotEqual(record["field"], "")
            self.assertNotEqual(record["source"], "")
            self.assertNotEqual(record["dataset_schema_or_api"], "")
            self.assertNotEqual(record["calculator"], "")
            self.assertIn("signal_time", record["timestamp_window"])
            self.assertNotEqual(record["unavailable_or_failure_reason"], "")
            self.assertNotEqual(record["blocking_scope"], "")
            self.assertNotEqual(record["next_action"], "")

    def test_active_path_records_remain_blocked_before_selected_contract(self):
        document = closeout.build_closeout_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        records = document["active_path_requirement_records"]
        self.assertEqual(len(records), 4)
        self.assertEqual(
            {record["exact_blocker"] for record in records},
            {"fresh_or_spent_unconfirmed", "prior_completed_shelf_break_spent_TO_REVIEW"},
        )
        for record in records:
            self.assertEqual(record["gap_type"], "active_path_requirement")
            self.assertTrue(record["open_after_closeout"])
            self.assertEqual(
                record["closeout_determination"],
                "closed_to_exact_active_path_regression_requirement",
            )
            self.assertFalse(record["selected_contract_after_closeout"])
            self.assertFalse(record["entry_recorded_after_closeout"])

    def test_contract_selected_remaining_gaps_are_preserved_without_paid_request(self):
        document = closeout.build_closeout_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        records = document["contract_selected_gap_records"]
        self.assertEqual(len(records), 2)
        determinations = {record["closeout_determination"] for record in records}
        self.assertEqual(
            determinations,
            {
                "closed_as_local_no_entry_blocker",
                "closed_as_outside_narrowed_ideal_path",
            },
        )
        for record in records:
            self.assertFalse(record["open_after_closeout"])
            self.assertFalse(record["additional_entry_established"])
            self.assertFalse(record["entry_recorded_after_closeout"])

    def test_qqq_controls_are_preserved(self):
        document = closeout.build_closeout_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        policy = document["closeout_policy"]
        qqq_ideal = document["qqq_ideal_outside_path_preservation"]

        self.assertTrue(policy["qqq_clean_fast_break_001_preserved_regression_only"])
        self.assertTrue(policy["qqq_ideal_preserved_outside_narrowed_path"])
        self.assertEqual(qqq_ideal["accepted_frozen_evidence_status"], "replace")
        self.assertTrue(qqq_ideal["fresh_raw_quote_preserved"])
        self.assertFalse(qqq_ideal["paid_option_request_valid_after_closeout"])
        self.assertFalse(qqq_ideal["selected_contract_after_closeout"])

    def test_policy_blocks_scans_downloads_reopens_and_readiness_claims(self):
        document = closeout.build_closeout_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        policy = document["closeout_policy"]

        self.assertFalse(policy["new_candidate_scan_run"])
        self.assertFalse(policy["new_setup_source_pass_run"])
        self.assertFalse(policy["closed_setup_source_candidates_reopened"])
        self.assertFalse(policy["rejected_intake_rows_replayed"])
        self.assertFalse(policy["confirmed_qqq_safety_rejection_rerun_as_live_candidate"])
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

    def test_scorecard_classifications_remain_separate(self):
        document = closeout.build_closeout_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        self.assertEqual(document["final_classifications"]["VALID_TRADE_CAPTURED"], 1)
        self.assertEqual(document["final_classifications"]["TRUE_NO_TRADE"], 4)
        self.assertEqual(document["final_classifications"]["MISSING_DATA"], 6)
        self.assertEqual(document["final_classifications"]["MISSED_VALID_TRADE"], 0)
        self.assertEqual(document["final_classifications"]["INVALID_TRADE_ALLOWED"], 0)
        self.assertEqual(document["final_classifications"]["UNRESOLVED"], 4)

    def test_next_task_is_exactly_one_grouped_task(self):
        document = closeout.build_closeout_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        self.assertEqual(document["next_task"]["filename"], closeout.NEXT_TASK_FILENAME)
        self.assertEqual(
            document["next_task"]["route"],
            "positive_entry_active_path_requirement_regression",
        )

    def test_file_writer_creates_result(self):
        root = Path(__file__).resolve().parents[1]
        result_path = (
            root
            / "historical_signal_replay"
            / "results"
            / "test_day50_positive_entry_remaining_evidence_gap_closeout_tmp.json"
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
