import json
import unittest
from pathlib import Path

from historical_signal_replay import (
    day50_positive_entry_active_path_rule_evidence_repair as repair,
)


class Day50PositiveEntryActivePathRuleEvidenceRepairTests(unittest.TestCase):
    def test_repairs_only_affected_trade_candidate_active_path_records(self):
        document = repair.build_repair_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        scorecard = document["scorecard"]

        self.assertEqual(document["result_version"], repair.RESULT_VERSION)
        self.assertEqual(scorecard["affected_trade_candidate_rule_gap_cases_repaired"], 4)
        self.assertEqual(scorecard["accepted_active_path_rule_evidence_records"], 4)
        self.assertEqual(scorecard["affected_cases_selected_contracts_after_repair"], 0)
        self.assertEqual(scorecard["affected_cases_entry_eligible_after_repair"], 0)
        self.assertEqual(scorecard["affected_cases_entries_recorded_after_repair"], 0)
        self.assertEqual(scorecard["additional_entries_established"], 0)
        self.assertEqual(document["deterministic_comparison"]["result"], "PASS")

    def test_repaired_records_name_exact_fields_sources_datasets_and_windows(self):
        document = repair.build_repair_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        records = document["active_path_rule_evidence_repair_records"]
        self.assertEqual(
            {record["exact_blocker"] for record in records},
            {"fresh_or_spent_unconfirmed", "prior_completed_shelf_break_spent_TO_REVIEW"},
        )
        for record in records:
            self.assertEqual(record["batch_first_stage_not_reached"], "TRADE_CANDIDATE")
            self.assertTrue(record["accepted_active_path_rule_evidence_repaired"])
            self.assertEqual(record["repair_type"], "exact_active_path_requirement_record")
            self.assertNotEqual(record["field"], "")
            self.assertNotEqual(record["source"], "")
            self.assertIn("signal_replay", record["dataset_schema_or_api"])
            self.assertNotEqual(record["calculator"], "")
            self.assertIn("signal_time", record["timestamp_window"])
            self.assertIn("blocks TRADE_CANDIDATE", record["blocking_scope"])
            self.assertFalse(record["selected_contract_after_repair"])
            self.assertFalse(record["entry_recorded_after_repair"])

    def test_repaired_requirements_preserve_no_promotion_and_no_proof(self):
        document = repair.build_repair_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        for record in document["active_path_rule_evidence_repair_records"]:
            requirement = record["repaired_requirement"]
            self.assertNotEqual(requirement["exact_missing_rule_or_evidence"], "")
            self.assertNotEqual(requirement["required_source_field_or_log_evidence"], "")
            self.assertEqual(requirement["decision_if_missing"], "blocks TRADE_CANDIDATE")
            self.assertFalse(requirement["current_repo_has_enough_data"])
            self.assertFalse(requirement["proof_allowed"])
            self.assertFalse(record["proof_accepted"])
            self.assertFalse(record["profitability_claimed"])
            self.assertFalse(record["paper_eligible"])
            self.assertFalse(record["live_eligible"])

    def test_before_and_after_batch_totals_are_preserved(self):
        document = repair.build_repair_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        scorecard = document["scorecard"]

        self.assertEqual(scorecard["trade_candidates_before_repair"], 9)
        self.assertEqual(scorecard["trade_candidates_after_repair"], 9)
        self.assertEqual(scorecard["selected_contracts_before_repair"], 5)
        self.assertEqual(scorecard["selected_contracts_after_repair"], 5)
        self.assertEqual(scorecard["eligible_entries_before_repair"], 1)
        self.assertEqual(scorecard["eligible_entries_after_repair"], 1)
        self.assertEqual(scorecard["recorded_entries_before_repair"], 1)
        self.assertEqual(scorecard["recorded_entries_after_repair"], 1)

    def test_qqq_ideal_and_regression_only_controls_are_preserved(self):
        document = repair.build_repair_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        qqq_ideal = document["qqq_ideal_outside_path_preservation"]
        policy = document["repair_policy"]

        self.assertEqual(qqq_ideal["accepted_frozen_evidence_status"], "replace")
        self.assertEqual(qqq_ideal["preserved_as"], "outside_narrowed_ideal_path")
        self.assertFalse(qqq_ideal["paid_option_request_valid_after_repair"])
        self.assertTrue(policy["qqq_clean_fast_break_001_preserved_regression_only"])
        self.assertTrue(policy["qqq_ideal_preserved_outside_narrowed_path"])
        self.assertEqual(policy["contract_selected_closeout_additional_entries_preserved"], 0)

    def test_policy_blocks_scans_downloads_reopens_and_readiness_claims(self):
        document = repair.build_repair_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        policy = document["repair_policy"]

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
        document = repair.build_repair_document(
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
        document = repair.build_repair_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        self.assertEqual(document["next_task"]["filename"], repair.NEXT_TASK_FILENAME)
        self.assertEqual(
            document["next_task"]["route"],
            "positive_entry_remaining_evidence_gap_closeout",
        )

    def test_file_writer_creates_result(self):
        root = Path(__file__).resolve().parents[1]
        result_path = (
            root
            / "historical_signal_replay"
            / "results"
            / "test_day50_positive_entry_active_path_rule_evidence_repair_tmp.json"
        )
        try:
            written = repair.write_repair_document(
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
