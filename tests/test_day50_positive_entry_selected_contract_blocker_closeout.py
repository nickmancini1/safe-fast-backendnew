import json
import unittest
from pathlib import Path

from historical_signal_replay import (
    day50_positive_entry_selected_contract_blocker_closeout as closeout,
)


class Day50PositiveEntrySelectedContractBlockerCloseoutTests(unittest.TestCase):
    def test_closeout_reruns_selected_contract_failures_before_entry(self):
        document = closeout.build_closeout_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        scorecard = document["scorecard"]

        self.assertEqual(document["result_version"], closeout.RESULT_VERSION)
        self.assertEqual(scorecard["selected_contracts_in_batch"], 5)
        self.assertEqual(scorecard["selected_contracts_failed_before_entry"], 4)
        self.assertEqual(scorecard["affected_cases_rerun"], 4)
        self.assertEqual(scorecard["affected_cases_entry_eligible"], 0)
        self.assertEqual(scorecard["affected_cases_entries_recorded"], 0)
        self.assertEqual(scorecard["additional_entries_established"], 0)
        self.assertEqual(document["deterministic_comparison"]["result"], "PASS")

    def test_each_affected_selected_contract_has_exact_first_blocker(self):
        document = closeout.build_closeout_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        records = document["affected_selected_contract_records"]

        self.assertEqual(len(records), 4)
        self.assertEqual(
            document["selected_contract_first_blockers"]["ENTRY_ELIGIBLE"][
                "affected_candidate_count"
            ],
            4,
        )
        self.assertEqual(
            document["selected_contract_first_blockers"]["ENTRY_ELIGIBLE"][
                "common_causes"
            ],
            {"quote_age_above_5_minutes": 4},
        )
        for record in records:
            blocker = record["first_blocker"]
            self.assertEqual(blocker["stage"], "ENTRY_ELIGIBLE")
            self.assertEqual(blocker["field"], "option_quote_freshness")
            self.assertEqual(blocker["exact_blocker_code"], "quote_age_above_5_minutes")
            self.assertIn("OPRA.PILLAR", blocker["dataset_schema_or_api"])
            self.assertIn("calculator", blocker["dataset_schema_or_api"])
            self.assertEqual(blocker["blocking_scope"], "blocks ENTRY_ELIGIBLE and ENTRY_RECORDED")
            self.assertFalse(record["rerun_result"]["additional_entry_established"])

    def test_classifications_remain_separate_and_qqq_stays_regression_only(self):
        document = closeout.build_closeout_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        scorecard = document["scorecard"]
        by_id = {
            record["candidate_identifier"]: record
            for record in document["affected_selected_contract_records"]
        }

        self.assertEqual(scorecard["valid_trades_captured"], 1)
        self.assertEqual(scorecard["true_no_trades"], 4)
        self.assertEqual(scorecard["missing_data_cases"], 6)
        self.assertEqual(scorecard["missed_valid_trades"], 0)
        self.assertEqual(scorecard["invalid_trades_allowed"], 0)
        self.assertEqual(scorecard["unresolved_cases"], 4)
        self.assertTrue(by_id[closeout.QQQ_CLOSED_CANDIDATE_ID]["regression_only"])
        self.assertEqual(
            by_id[closeout.QQQ_CLOSED_CANDIDATE_ID][
                "classification_after_closeout"
            ],
            "TRUE_NO_TRADE_REGRESSION_ONLY",
        )
        self.assertEqual(scorecard["closed_safety_rejections_rerun_as_live_candidates"], 0)

    def test_policy_forbids_scope_expansion_and_data_requests(self):
        document = closeout.build_closeout_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        policy = document["closeout_policy"]

        self.assertFalse(policy["new_candidate_scan_run"])
        self.assertFalse(policy["closed_setup_source_candidates_reopened"])
        self.assertFalse(policy["rejected_intake_rows_replayed"])
        self.assertFalse(policy["confirmed_qqq_safety_rejection_rerun_as_live_candidate"])
        self.assertTrue(policy["qqq_closed_candidate_preserved_as_regression_only"])
        self.assertFalse(policy["frozen_rules_weakened"])
        self.assertFalse(policy["governance_only_chain_created"])
        self.assertFalse(document["option_request_included"])
        self.assertFalse(document["exit_path_request_included"])
        self.assertFalse(document["databento_downloaded"])
        self.assertEqual(document["databento_cost_check"]["checked_cost"], "NOT_AVAILABLE")

    def test_next_task_is_exactly_one_grouped_task(self):
        document = closeout.build_closeout_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        self.assertEqual(document["next_task"]["filename"], closeout.NEXT_TASK_FILENAME)
        self.assertEqual(
            document["next_task"]["route"],
            "positive_entry_contract_selected_missing_evidence",
        )

    def test_file_writer_creates_result(self):
        root = Path(__file__).resolve().parents[1]
        result_path = (
            root
            / "historical_signal_replay"
            / "results"
            / "test_day50_positive_entry_selected_contract_blocker_closeout_tmp.json"
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
