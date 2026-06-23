import json
import unittest
from pathlib import Path

from historical_signal_replay import (
    day50_raw_data_positive_entry_option_contract_evidence_request_review as review,
)
from watcher_foundation import (
    day50_raw_data_positive_entry_option_contract_evidence_request_review_validator as validator,
)


class Day50OptionContractEvidenceRequestReviewTests(unittest.TestCase):
    def _document(self):
        return review.build_option_contract_evidence_document(
            source_commit="testsha",
            run_timestamp="2026-06-22T00:00:00Z",
        )

    def test_all_three_setup_families_processed_separately(self):
        document = self._document()
        records = document["setup_records"]

        self.assertEqual(
            {record["setup_family"] for record in records},
            {"Ideal", "Clean Fast Break", "Continuation"},
        )
        self.assertEqual(len(records), 3)
        for record in records:
            self.assertEqual(record["symbol"], "SPY")
            self.assertEqual(record["setup_time_utc"], "2026-03-16T13:30:00Z")
            self.assertEqual(record["underlying_price_evidence"]["rows_found"], 3)

    def test_frozen_setup_fields_recovered_without_numeric_invention(self):
        document = self._document()

        for record in document["setup_records"]:
            self.assertIn("bounded accepted setup trigger contract", record["trigger"])
            self.assertIn("bounded accepted invalidation contract", record["invalidation"])
            self.assertIsNone(record["trigger_numeric"])
            self.assertIsNone(record["invalidation_numeric"])
            self.assertEqual(
                record["freshness_final_signal_state"],
                "fresh_final_signal_state_at_setup_time",
            )
            self.assertEqual(
                record["no_hindsight_boundary"],
                "future_rows_ignored_for_setup_labels",
            )
            self.assertEqual(
                record["session_boundary_behavior"],
                "same_session_reset_only_no_prior_session_carry",
            )

    def test_contract_selection_abstains_on_exact_local_blockers(self):
        document = self._document()

        for record in document["setup_records"]:
            result = record["winner_selection_result"]
            self.assertEqual(result["contract_selection_status"], "abstain")
            self.assertIsNone(result["selected_contract"])
            self.assertIn(
                "numeric_trigger_missing_for_strike_selection",
                result["blocking_reasons"],
            )
            self.assertIn(
                "local_march16_option_evidence_missing",
                result["blocking_reasons"],
            )

    def test_clean_fast_break_uses_existing_selector_boundary_when_possible(self):
        document = self._document()
        cfb = _record(document, "Clean Fast Break")

        self.assertEqual(
            cfb["contract_selection_rule"],
            "historical_signal_replay.cfb_contract_selector",
        )
        self.assertTrue(cfb["contract_selection_inputs"]["rule_applies_to_family"])
        self.assertEqual(cfb["contract_selection_inputs"]["expected_setup_type"], "Clean Fast Break")
        self.assertTrue(cfb["contract_selection_inputs"]["open_interest_required"])

    def test_ideal_and_continuation_do_not_reuse_cfb_selector_by_assumption(self):
        document = self._document()

        for family in ("Ideal", "Continuation"):
            record = _record(document, family)
            self.assertEqual(record["contract_selection_rule"], "NO_ACCEPTED_LOCAL_FAMILY_SELECTOR")
            self.assertIn(
                "no_accepted_local_selector_for_setup_family",
                record["winner_selection_result"]["blocking_reasons"],
            )

    def test_costed_backtest_fields_are_present_but_not_invented(self):
        document = self._document()

        for result in document["costed_results_by_setup_family"].values():
            self.assertEqual(result["status"], "NOT_RUN_NO_SELECTED_CONTRACT")
            self.assertFalse(result["costed_entry_exit_replay_run"])
            self.assertFalse(result["eligible_entry"])
            self.assertFalse(result["recorded_entry"])
            for field in (
                "bid",
                "ask",
                "midpoint",
                "spread",
                "entry_price",
                "exit_price",
                "gross_pnl",
                "net_pnl",
            ):
                self.assertIsNone(result[field])

    def test_grouped_request_names_exact_dataset_fields_and_cost_status(self):
        document = self._document()
        request = document["exact_grouped_evidence_request"]

        self.assertTrue(request["created"])
        self.assertFalse(request["downloaded"])
        self.assertEqual(request["cost_check"]["checked_cost"], "NOT_AVAILABLE")
        self.assertTrue(request["cost_check"]["attempted"])
        self.assertFalse(request["cost_check"]["external_cost_api_called"])
        self.assertEqual(len(request["requests"]), 3)
        for item in request["requests"]:
            self.assertEqual(item["dataset"], "OPRA.PILLAR")
            self.assertEqual(item["stype_in"], "raw_symbol")
            self.assertEqual(item["start_timestamp_utc"], "2026-03-16T13:30:00Z")
            self.assertEqual(
                item["exact_contract_identifier"],
                "NOT_DERIVABLE_FROM_LOCAL_EVIDENCE",
            )
            self.assertIn("definition", item["schemas"])
            self.assertIn("tcbbo", item["schemas"])
            self.assertIn("trades", item["schemas"])
            self.assertIn("statistics", item["schemas"])

    def test_funnel_totals_preserve_stage_boundary(self):
        document = self._document()
        after = document["after_funnel_totals"]

        self.assertEqual(after["new_generated_candidates"], 3)
        self.assertEqual(after["new_setup_qualified_candidates"], 3)
        self.assertEqual(after["new_trade_candidates"], 0)
        self.assertEqual(after["new_selected_contracts"], 0)
        self.assertEqual(after["new_eligible_entries"], 0)
        self.assertEqual(after["new_recorded_entries"], 0)
        self.assertEqual(after["new_exact_option_contract_evidence_required_cases"], 3)

    def test_preserved_controls_and_mapper_count_unchanged(self):
        document = self._document()

        self.assertEqual(document["accepted_mapper_regression_case_count"], 17)
        self.assertEqual(document["package_to_candidate_control_result"]["deterministic_result"], "PASS")
        self.assertEqual(document["preserved_day50_controls"]["setup_qualified"], 13)
        self.assertEqual(document["preserved_day50_controls"]["trade_candidates"], 9)
        self.assertEqual(document["preserved_day50_controls"]["selected_contracts"], 5)
        self.assertEqual(document["preserved_scorecard"]["VALID_TRADE_CAPTURED"], 1)
        self.assertEqual(document["preserved_scorecard"]["TRUE_NO_TRADE"], 4)

    def test_deterministic_result(self):
        document = self._document()

        self.assertEqual(document["deterministic_comparison"]["result"], "PASS")
        self.assertEqual(document["first_run_hash"], document["second_run_hash"])

    def test_writer_and_validator_accept_result(self):
        root = Path(__file__).resolve().parents[1]
        result_path = root / "historical_signal_replay" / "results" / "test_day50_option_review.json"
        doc_path = root / "test_day50_option_review_result.md"
        original_result = review.RESULT_PATH
        original_doc = review.RESULT_DOC_PATH
        try:
            review.RESULT_PATH = result_path
            review.RESULT_DOC_PATH = doc_path
            written = review.write_outputs(
                source_commit="testsha",
                run_timestamp="2026-06-22T00:00:00Z",
            )
            loaded = json.loads(result_path.read_text(encoding="utf-8"))
            validation = validator.validate_result_document(result_path)
        finally:
            review.RESULT_PATH = original_result
            review.RESULT_DOC_PATH = original_doc
            if result_path.exists():
                result_path.unlink()
            if doc_path.exists():
                doc_path.unlink()

        self.assertEqual(written, loaded)
        self.assertEqual(validation["status"], "PASS")
        self.assertEqual(validation["problems"], [])


def _record(document, family):
    for record in document["setup_records"]:
        if record["setup_family"] == family:
            return record
    raise AssertionError(f"missing family record: {family}")


if __name__ == "__main__":
    unittest.main()
