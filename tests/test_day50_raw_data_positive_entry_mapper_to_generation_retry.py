import json
import unittest
from pathlib import Path

from historical_signal_replay import (
    day50_raw_data_positive_entry_mapper_to_generation_retry as retry,
)
from watcher_foundation import (
    day50_raw_data_positive_entry_mapper_to_generation_retry_validator as validator,
)


class Day50MapperToGenerationRetryTests(unittest.TestCase):
    def _document(self):
        return retry.build_retry_document(
            source_commit="testsha",
            run_timestamp="2026-06-22T00:00:00Z",
        )

    def test_retry_processes_each_family_separately(self):
        document = self._document()
        records = document["setup_family_retry_records"]

        self.assertEqual(len(records), 3)
        self.assertEqual(
            {record["setup_family"] for record in records},
            {"Ideal", "Clean Fast Break", "Continuation"},
        )
        self.assertEqual(set(document["family_scorecards"]), {"Ideal", "Clean Fast Break", "Continuation"})

    def test_review_only_packages_stop_before_generated_candidate(self):
        document = self._document()

        for record in document["setup_family_retry_records"]:
            self.assertTrue(record["stage_reached"]["mapped_package"])
            self.assertEqual(record["highest_stage_reached"], "mapped_package")
            self.assertEqual(record["first_stage_not_reached"], "generated_candidate")
            self.assertFalse(record["candidate_generated"])
            self.assertFalse(record["setup_qualified"])
            self.assertFalse(record["trade_candidate"])
            self.assertFalse(record["selected_contract"])
            self.assertFalse(record["eligible_entry"])
            self.assertFalse(record["recorded_entry"])
            self.assertEqual(
                record["failure_category"],
                "accepted_mapper_package_review_only_not_generation_input",
            )

    def test_no_hindsight_session_and_blocker_boundaries_are_preserved(self):
        document = self._document()
        policy = document["retry_policy"]

        self.assertTrue(policy["setup_time_boundary_frozen"])
        self.assertTrue(policy["no_hindsight_preserved"])
        self.assertTrue(policy["session_boundary_preserved"])
        self.assertTrue(policy["developing_stage_transitions_validated"])
        self.assertTrue(policy["stable_winner_selection_preserved"])
        self.assertTrue(policy["no_trade_preservation_validated"])
        for record in document["setup_family_retry_records"]:
            self.assertEqual(record["no_hindsight_boundary"], "future_rows_ignored_for_setup_labels")
            self.assertEqual(record["session_boundary_behavior"], "same_session_reset_only_no_prior_session_carry")
            self.assertEqual(
                record["blocker_caution_review"],
                "optional_context_absent_non_blocking_under_registry_rule",
            )

    def test_all_accepted_mapper_cases_are_carried_into_retry(self):
        document = self._document()

        self.assertEqual(document["accepted_mapper_regression_case_count"], 17)
        self.assertTrue(all(case["status"] == "PASS" for case in document["accepted_mapper_regression_cases"]))

    def test_funnel_totals_and_controls_are_separate(self):
        document = self._document()
        after = document["after_funnel_totals"]

        self.assertEqual(after["raw_opportunities_mapped"], 3)
        self.assertEqual(after["exact_setup_time_field_packages_established"], 3)
        self.assertEqual(after["new_generated_candidates"], 0)
        self.assertEqual(after["new_setup_qualified_candidates"], 0)
        self.assertEqual(after["new_trade_candidates"], 0)
        self.assertEqual(after["new_selected_contracts"], 0)
        self.assertEqual(after["new_eligible_entries"], 0)
        self.assertEqual(after["new_recorded_entries"], 0)
        self.assertEqual(after["new_exact_generation_contract_required_cases"], 3)
        self.assertEqual(document["preserved_day50_controls"]["setup_qualified"], 13)
        self.assertEqual(document["preserved_day50_controls"]["trade_candidates"], 9)
        self.assertEqual(document["preserved_day50_controls"]["selected_contracts"], 5)
        self.assertEqual(document["preserved_day50_controls"]["eligible_entries"], 1)
        self.assertEqual(document["preserved_day50_controls"]["recorded_entries"], 1)

    def test_no_option_exit_or_paid_data_scope_is_created(self):
        document = self._document()
        policy = document["retry_policy"]

        self.assertFalse(document["exact_grouped_evidence_request"]["created"])
        self.assertFalse(policy["raw_vendor_bars_treated_as_safe_fast_labels"])
        self.assertFalse(policy["frozen_trading_rules_changed"])
        self.assertFalse(policy["thresholds_loosened"])
        self.assertFalse(policy["missing_fields_invented"])
        self.assertFalse(policy["option_evidence_invented"])
        self.assertFalse(policy["main_py_changed"])
        self.assertFalse(policy["railway_or_deploy_changed"])
        self.assertFalse(policy["paid_data_downloaded"])
        for result in document["costed_results_by_setup_family"].values():
            self.assertEqual(result["status"], "NOT_RUN_NO_TRADE_CANDIDATE")
            self.assertFalse(result["option_or_exit_evidence_requested"])

    def test_retry_is_deterministic(self):
        document = self._document()

        self.assertEqual(document["deterministic_comparison"]["result"], "PASS")
        self.assertEqual(document["first_run_hash"], document["second_run_hash"])

    def test_writer_and_validator_accept_result(self):
        root = Path(__file__).resolve().parents[1]
        result_path = root / "historical_signal_replay" / "results" / "test_day50_mapper_retry.json"
        doc_path = root / "test_day50_mapper_retry_result.md"
        original_result = retry.RESULT_PATH
        original_doc = retry.RESULT_DOC_PATH
        try:
            retry.RESULT_PATH = result_path
            retry.RESULT_DOC_PATH = doc_path
            written = retry.write_outputs(
                source_commit="testsha",
                run_timestamp="2026-06-22T00:00:00Z",
            )
            loaded = json.loads(result_path.read_text(encoding="utf-8"))
            validation = validator.validate_result_document(result_path)
        finally:
            retry.RESULT_PATH = original_result
            retry.RESULT_DOC_PATH = original_doc
            if result_path.exists():
                result_path.unlink()
            if doc_path.exists():
                doc_path.unlink()

        self.assertEqual(written, loaded)
        self.assertEqual(validation["status"], "PASS")
        self.assertEqual(validation["problems"], [])


if __name__ == "__main__":
    unittest.main()
