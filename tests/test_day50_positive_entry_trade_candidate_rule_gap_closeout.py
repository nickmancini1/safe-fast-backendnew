import json
import unittest
from pathlib import Path

from historical_signal_replay import (
    day50_positive_entry_trade_candidate_rule_gap_closeout as closeout,
)


class Day50PositiveEntryTradeCandidateRuleGapCloseoutTests(unittest.TestCase):
    def test_reviews_only_trade_candidate_rule_gap_cases(self):
        document = closeout.build_closeout_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        scorecard = document["scorecard"]

        self.assertEqual(document["result_version"], closeout.RESULT_VERSION)
        self.assertEqual(
            scorecard["affected_trade_candidate_rule_gap_cases_reviewed"],
            4,
        )
        self.assertEqual(scorecard["affected_cases_selected_contracts_after_closeout"], 0)
        self.assertEqual(scorecard["affected_cases_entry_eligible_after_closeout"], 0)
        self.assertEqual(scorecard["affected_cases_entries_recorded_after_closeout"], 0)
        self.assertEqual(scorecard["additional_entries_established"], 0)
        self.assertEqual(document["deterministic_comparison"]["result"], "PASS")

    def test_trade_candidate_cases_name_exact_fields_sources_and_actions(self):
        document = closeout.build_closeout_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        records = document["affected_trade_candidate_rule_gap_records"]
        self.assertEqual(
            {record["batch_exact_blocker"] for record in records},
            {"fresh_or_spent_unconfirmed", "prior_completed_shelf_break_spent_TO_REVIEW"},
        )
        for record in records:
            self.assertEqual(record["batch_first_stage_not_reached"], "TRADE_CANDIDATE")
            self.assertNotEqual(record["field"], "")
            self.assertNotEqual(record["source"], "")
            self.assertIn("signal_replay", record["dataset_schema_or_api"])
            self.assertIn("signal_time", record["timestamp_window"])
            self.assertIn("blocks TRADE_CANDIDATE", record["blocking_scope"])
            self.assertIn("before any selected-contract", record["next_action"])
            self.assertFalse(record["selected_contract_after_closeout"])
            self.assertFalse(record["additional_entry_established"])

    def test_qqq_ideal_selected_contract_gap_is_resolved_by_frozen_rule_evidence(self):
        document = closeout.build_closeout_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        qqq_ideal = document["qqq_ideal_selected_contract_rule_gap_closeout"]

        self.assertEqual(qqq_ideal["business_candidate_id"], closeout.QQQ_IDEAL_CANDIDATE_ID)
        self.assertEqual(qqq_ideal["accepted_frozen_evidence_status"], "replace")
        self.assertEqual(qqq_ideal["prior_fresh_raw_quote_symbol"], "QQQ   260529C00720000")
        self.assertIn("fast-swing", qqq_ideal["unavailable_or_failure_reason"])
        self.assertIn("wide-risk", qqq_ideal["unavailable_or_failure_reason"])
        self.assertIn("blocks QQQ Ideal selected-contract", qqq_ideal["blocking_scope"])
        self.assertFalse(qqq_ideal["selected_contract_after_closeout"])
        self.assertFalse(qqq_ideal["entry_recorded_after_closeout"])
        self.assertTrue(
            document["scorecard"][
                "qqq_ideal_selected_contract_rule_gap_resolved_from_frozen_evidence"
            ]
        )

    def test_batch_funnel_totals_and_classifications_are_preserved(self):
        document = closeout.build_closeout_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        scorecard = document["scorecard"]

        self.assertEqual(scorecard["trade_candidates"], 9)
        self.assertEqual(scorecard["selected_contracts"], 5)
        self.assertEqual(scorecard["eligible_entries"], 1)
        self.assertEqual(scorecard["recorded_entries"], 1)
        self.assertEqual(document["final_classifications"]["VALID_TRADE_CAPTURED"], 1)
        self.assertEqual(document["final_classifications"]["TRUE_NO_TRADE"], 4)
        self.assertEqual(document["final_classifications"]["MISSING_DATA"], 6)
        self.assertEqual(document["final_classifications"]["MISSED_VALID_TRADE"], 0)
        self.assertEqual(document["final_classifications"]["INVALID_TRADE_ALLOWED"], 0)
        self.assertEqual(document["final_classifications"]["UNRESOLVED"], 4)

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
        self.assertFalse(document["paid_data_request_created"])
        self.assertFalse(document["databento_downloaded"])
        self.assertFalse(document["schwab_authenticated"])
        self.assertFalse(document["proof_accepted"])
        self.assertFalse(document["profitability_claimed"])
        self.assertFalse(document["paper_eligible"])
        self.assertFalse(document["live_eligible"])

    def test_next_task_is_exactly_one_grouped_task(self):
        document = closeout.build_closeout_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        self.assertEqual(document["next_task"]["filename"], closeout.NEXT_TASK_FILENAME)
        self.assertEqual(
            document["next_task"]["route"],
            "positive_entry_active_path_rule_evidence_repair",
        )

    def test_file_writer_creates_result(self):
        root = Path(__file__).resolve().parents[1]
        result_path = (
            root
            / "historical_signal_replay"
            / "results"
            / "test_day50_positive_entry_trade_candidate_rule_gap_closeout_tmp.json"
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
