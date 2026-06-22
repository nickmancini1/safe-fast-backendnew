import json
import unittest
from pathlib import Path

from historical_signal_replay import (
    day50_raw_data_positive_entry_setup_time_replay_mapping as mapping,
)
from watcher_foundation import (
    day50_raw_data_positive_entry_setup_time_replay_mapping_validator as validator,
)


class Day50RawDataPositiveEntrySetupTimeReplayMappingTests(unittest.TestCase):
    def _document(self):
        return mapping.build_mapping_document(
            source_commit="testsha",
            run_timestamp="2026-06-22T00:00:00Z",
        )

    def test_source_csv_is_valid_acquired_spy_one_minute_evidence(self):
        document = self._document()
        summary = document["source_summary"]

        self.assertEqual(document["request_id"], mapping.REQUEST_ID)
        self.assertEqual(document["dataset_schema_stype"], "DBEQ.BASIC / ohlcv-1m / raw_symbol")
        self.assertEqual(summary["row_count"], 751)
        self.assertEqual(summary["symbol_set"], ["SPY"])
        self.assertTrue(summary["complete_chronological_rows"])
        self.assertTrue(summary["required_columns_present"])
        self.assertFalse(summary["raw_vendor_data_modified"])

    def test_three_setup_families_are_mapped_and_all_remain_rejected(self):
        document = self._document()
        records = document["setup_family_mapping_records"]

        self.assertEqual(len(records), 3)
        self.assertEqual(
            {record["setup_family"] for record in records},
            {"Ideal", "Clean Fast Break", "Continuation"},
        )
        for record in records:
            self.assertTrue(record["underlying_setup_time_evidence_supplied"])
            self.assertFalse(record["exact_setup_time_fields_established"])
            self.assertFalse(record["candidate_generated"])
            self.assertFalse(record["setup_qualified"])
            self.assertFalse(record["trade_candidate"])
            self.assertEqual(record["highest_stage_reached"], "SETUP_DEVELOPING")
            self.assertEqual(record["first_stage_not_reached"], "SETUP_QUALIFIED")
            self.assertEqual(record["final_classification"], "EXACT_DATA_REQUIRED")
            self.assertEqual(
                record["exclusion_reason"],
                "accepted_setup_time_replay_mapping_path_absent",
            )

    def test_all_exact_setup_time_fields_have_specific_blockers(self):
        document = self._document()
        required = set(mapping.REQUIRED_SETUP_FIELDS)

        for record in document["setup_family_mapping_records"]:
            self.assertEqual(set(record["exact_failed_fields"]), required)
            self.assertEqual(set(record["field_blockers"]), required)
            for field in required:
                blocker = record["field_blockers"][field]
                self.assertEqual(blocker["exact_field"], field)
                self.assertIn("SAFE-FAST", blocker["exact_source"])
                self.assertTrue(blocker["exact_dataset_schema_api_calculator"])
                self.assertTrue(blocker["exact_timestamp_window"].startswith("source timestamps <="))
                if field == "blocker_caution_review":
                    self.assertIn("trade", blocker["blocks"])
                    self.assertIn("bounded source capability audit", blocker["exact_next_action"])
                else:
                    self.assertIn("setup", blocker["blocks"])
                    self.assertIn("exclude candidate", blocker["exact_next_action"])

    def test_accepted_paths_checked_do_not_infer_from_ohlcv(self):
        document = self._document()

        for record in document["setup_family_mapping_records"]:
            self.assertGreaterEqual(len(record["accepted_paths_checked"]), 2)
            for path in record["accepted_paths_checked"]:
                self.assertEqual(path["mapping_result"], "not_applicable_to_raw_ohlcv_only")
                self.assertIn("raw OHLCV", path["blocking_reason"])

    def test_scorecard_and_determinism(self):
        document = self._document()
        scorecard = document["new_candidate_scorecard"]

        self.assertEqual(scorecard["raw_opportunities_mapped"], 3)
        self.assertEqual(scorecard["exact_setup_time_fields_established"], 0)
        self.assertEqual(scorecard["new_generated_candidates"], 0)
        self.assertEqual(scorecard["new_setup_qualified_candidates"], 0)
        self.assertEqual(scorecard["new_trade_candidates"], 0)
        self.assertEqual(scorecard["new_selected_contracts"], 0)
        self.assertEqual(scorecard["new_eligible_entries"], 0)
        self.assertEqual(scorecard["new_recorded_entries"], 0)
        self.assertEqual(scorecard["new_exact_data_required_cases"], 3)
        self.assertEqual(document["deterministic_comparison"]["result"], "PASS")
        self.assertEqual(document["first_run_hash"], document["second_run_hash"])

    def test_guardrails_block_new_data_and_readiness_claims(self):
        document = self._document()
        policy = document["mapping_policy"]
        guardrails = document["guardrails"]

        self.assertTrue(policy["used_only_acquired_day50_spy_underlying_evidence"])
        self.assertFalse(policy["requested_more_data"])
        self.assertFalse(policy["requested_option_data"])
        self.assertFalse(policy["requested_exit_path_data"])
        self.assertFalse(policy["raw_vendor_bars_treated_as_safe_fast_labels"])
        self.assertFalse(policy["frozen_rules_changed"])
        self.assertFalse(policy["main_py_changed"])
        self.assertFalse(policy["railway_or_deploy_changed"])
        self.assertFalse(guardrails["schwab_authenticated"])
        self.assertFalse(guardrails["proof_accepted"])
        self.assertFalse(guardrails["profitability_claimed"])
        self.assertFalse(guardrails["paper_eligible"])
        self.assertFalse(guardrails["live_eligible"])

    def test_writer_and_validator_accept_result(self):
        root = Path(__file__).resolve().parents[1]
        result_path = (
            root
            / "historical_signal_replay"
            / "results"
            / "test_day50_setup_time_mapping_tmp.json"
        )
        try:
            written = mapping.write_mapping_document(
                result_path,
                source_commit="testsha",
                run_timestamp="2026-06-22T00:00:00Z",
            )
            loaded = json.loads(result_path.read_text(encoding="utf-8"))
            validation = validator.validate_result_document(result_path)
        finally:
            if result_path.exists():
                result_path.unlink()

        self.assertEqual(written, loaded)
        self.assertEqual(validation["status"], "PASS")
        self.assertEqual(validation["problems"], [])


if __name__ == "__main__":
    unittest.main()
