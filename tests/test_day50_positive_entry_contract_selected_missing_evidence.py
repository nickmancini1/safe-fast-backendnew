import json
import unittest
from pathlib import Path

from historical_signal_replay import (
    day50_positive_entry_contract_selected_missing_evidence as closeout,
)


class Day50PositiveEntryContractSelectedMissingEvidenceTests(unittest.TestCase):
    def test_reviews_only_active_contract_selected_blocker_cases(self):
        document = closeout.build_closeout_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        scorecard = document["scorecard"]

        self.assertEqual(document["result_version"], closeout.RESULT_VERSION)
        self.assertEqual(scorecard["active_selected_contract_cases_reviewed"], 3)
        self.assertEqual(scorecard["fresh_quote_cases"], 2)
        self.assertEqual(scorecard["genuinely_stale_cases"], 1)
        self.assertEqual(scorecard["additional_entries_established"], 0)
        self.assertEqual(scorecard["entry_eligible_after_closeout"], 0)
        self.assertEqual(scorecard["entries_recorded_after_closeout"], 0)
        self.assertEqual(document["deterministic_comparison"]["result"], "PASS")

    def test_qqq_continuation_has_fresh_quote_but_spread_blocker(self):
        document = closeout.build_closeout_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        records = {
            row["candidate_identifier"]: row
            for row in document["active_selected_contract_records"]
        }
        qqq_continuation = records["first_real_qqq_continuation_replay_v1_fixture"]

        self.assertEqual(qqq_continuation["quote_evidence"]["quote_freshness_bucket"], "fresh")
        self.assertEqual(qqq_continuation["quote_evidence"]["raw_symbol"], "QQQ   260514C00665000")
        self.assertEqual(qqq_continuation["quote_evidence"]["rejection_reason"], "spread_above_0_15")
        self.assertEqual(qqq_continuation["resolved_classification"], "TRUE_NO_TRADE")
        self.assertFalse(qqq_continuation["additional_entry_established"])

    def test_qqq_ideal_fresh_raw_quote_still_has_selected_contract_gap(self):
        document = closeout.build_closeout_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        records = {
            row["candidate_identifier"]: row
            for row in document["active_selected_contract_records"]
        }
        qqq_ideal = records["first_real_qqq_ideal_replay_v1_fixture"]

        self.assertEqual(qqq_ideal["quote_evidence"]["quote_freshness_bucket"], "fresh")
        self.assertEqual(qqq_ideal["evidence_scope"], "raw_quote_universe")
        self.assertEqual(qqq_ideal["resolved_classification"], "MISSING_DATA")
        self.assertEqual(
            qqq_ideal["remaining_evidence_gaps"][0]["field"],
            "selected_contract_identity",
        )

    def test_spy_cfb_003_is_genuinely_stale_from_local_selected_quote(self):
        document = closeout.build_closeout_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        records = {
            row["candidate_identifier"]: row
            for row in document["active_selected_contract_records"]
        }
        spy = records["third_real_spy_clean_fast_break_replay_v1_fixture"]

        self.assertEqual(spy["quote_evidence"]["quote_freshness_bucket"], "stale")
        self.assertEqual(spy["quote_evidence"]["raw_symbol"], "SPY   260429C00700000")
        self.assertEqual(spy["quote_evidence"]["rejection_reason"], "quote_age_above_5_minutes")
        self.assertEqual(spy["resolved_classification"], "TRUE_NO_TRADE")

    def test_policy_preserves_qqq_cfb_regression_only_and_blocks_downloads(self):
        document = closeout.build_closeout_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        policy = document["closeout_policy"]

        self.assertTrue(policy["qqq_clean_fast_break_001_preserved_regression_only"])
        self.assertTrue(document["regression_only_record"]["regression_only"])
        self.assertFalse(policy["new_candidate_scan_run"])
        self.assertFalse(policy["closed_setup_source_candidates_reopened"])
        self.assertFalse(policy["rejected_intake_rows_replayed"])
        self.assertFalse(policy["frozen_rules_weakened"])
        self.assertFalse(document["paid_data_request_created"])
        self.assertFalse(document["databento_downloaded"])
        self.assertEqual(document["databento_cost_check"]["checked_cost"], "NOT_AVAILABLE")

    def test_classification_categories_remain_separate_and_next_task_is_single(self):
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
        self.assertEqual(document["next_task"]["filename"], closeout.NEXT_TASK_FILENAME)

    def test_file_writer_creates_result(self):
        root = Path(__file__).resolve().parents[1]
        result_path = (
            root
            / "historical_signal_replay"
            / "results"
            / "test_day50_positive_entry_contract_selected_missing_evidence_tmp.json"
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
