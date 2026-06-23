import json
import unittest
from copy import deepcopy
from pathlib import Path

from historical_signal_replay import (
    day50_raw_data_positive_entry_accepted_setup_replay_mapper as mapper,
)
from historical_signal_replay import (
    day50_raw_data_positive_entry_mapper_to_generation_retry as retry,
)
from historical_signal_replay import (
    day50_raw_data_positive_entry_review_only_package_to_candidate_contract as contract,
)
from watcher_foundation import (
    day50_raw_data_positive_entry_review_only_package_to_candidate_contract_validator as validator,
)


class Day50ReviewOnlyPackageToCandidateContractTests(unittest.TestCase):
    def _document(self):
        return contract.build_contract_document(
            source_commit="testsha",
            run_timestamp="2026-06-22T00:00:00Z",
        )

    def test_ideal_package_to_candidate_contract(self):
        document = self._document()
        record = _record(document, "Ideal")

        self.assertTrue(record["candidate_generated"])
        self.assertTrue(record["setup_qualified"])
        self.assertEqual(record["exact_outcome"], "setup_qualified_created")
        self.assertEqual(record["highest_stage_reached"], "setup_qualified")
        self.assertEqual(record["first_stage_not_reached"], "trade_candidate")

    def test_clean_fast_break_package_to_candidate_contract(self):
        document = self._document()
        record = _record(document, "Clean Fast Break")

        self.assertTrue(record["candidate_generated"])
        self.assertTrue(record["setup_qualified"])
        self.assertFalse(record["trade_candidate"])
        self.assertEqual(
            record["exact_remaining_blocker"],
            "selected_contract_option_evidence_missing",
        )

    def test_continuation_package_to_candidate_contract(self):
        document = self._document()
        record = _record(document, "Continuation")

        self.assertTrue(record["candidate_generated"])
        self.assertTrue(record["setup_qualified"])
        self.assertEqual(record["symbol"], "SPY")
        self.assertEqual(record["setup_time_utc"], "2026-03-16T13:30:00Z")

    def test_contract_rejection_with_exact_missing_fields(self):
        mapper_doc = mapper.build_mapper_document(
            source_commit="testsha",
            run_timestamp="2026-06-22T00:00:00Z",
        )
        package = deepcopy(mapper_doc["setup_family_field_packages"][0])
        package["fields"]["trigger"]["value"] = ""

        record = contract._contract_record(package)

        self.assertFalse(record["candidate_generated"])
        self.assertFalse(record["setup_qualified"])
        self.assertEqual(record["exact_outcome"], "rejected_with_exact_contract_gap")
        self.assertEqual(record["first_stage_not_reached"], "generated_candidate")
        self.assertEqual(record["contract_gap"]["missing_setup_fields"], ["trigger"])

    def test_no_hindsight_and_session_boundary_preservation(self):
        document = self._document()
        policy = document["contract_policy"]

        self.assertTrue(policy["no_hindsight_preserved"])
        self.assertTrue(policy["session_boundary_preserved"])
        for record in document["setup_family_contract_records"]:
            self.assertEqual(record["no_hindsight_boundary"], "future_rows_ignored_for_setup_labels")
            self.assertEqual(record["session_boundary_behavior"], "same_session_reset_only_no_prior_session_carry")
            self.assertFalse(record["raw_vendor_bars_treated_as_safe_fast_labels"])

    def test_stable_winner_and_no_trade_preservation(self):
        document = self._document()

        self.assertTrue(document["contract_policy"]["stable_winner_selection_preserved"])
        self.assertTrue(document["contract_policy"]["no_trade_preservation_validated"])
        self.assertEqual(document["preserved_scorecard"]["VALID_TRADE_CAPTURED"], 1)
        self.assertEqual(document["preserved_scorecard"]["TRUE_NO_TRADE"], 4)
        self.assertEqual(document["preserved_scorecard"]["WINNERS"], 1)
        self.assertEqual(document["preserved_scorecard"]["LOSERS"], 0)

    def test_grouped_evidence_request_names_exact_missing_option_fields(self):
        document = self._document()
        request = document["exact_grouped_evidence_request"]

        self.assertTrue(request["created"])
        self.assertEqual(len(request["requests"]), 3)
        for item in request["requests"]:
            self.assertEqual(item["contract"], "NOT_KNOWN_BEFORE_SELECTED_CONTRACT_EVIDENCE")
            self.assertEqual(
                item["exact_fields_missing"],
                [
                    "selected_contract_identity",
                    "selected_contract_quote_freshness",
                    "selected_contract_liquidity",
                    "entry_execution_context",
                ],
            )
            self.assertIn("trade_candidate", item["blocks"])
            self.assertIn("entry", item["blocks"])
            self.assertIn("costs", item["blocks"])
            self.assertIn("P&L", item["blocks"])

    def test_unchanged_17_mapper_regression_cases(self):
        document = self._document()

        self.assertEqual(document["accepted_mapper_regression_case_count"], 17)
        self.assertTrue(all(case["status"] == "PASS" for case in document["accepted_mapper_regression_cases"]))

    def test_unchanged_mapper_to_generation_retry_controls(self):
        document = self._document()
        retry_doc = retry.build_retry_document(
            source_commit="testsha",
            run_timestamp="2026-06-22T00:00:00Z",
        )

        self.assertEqual(document["retry_control_result"]["deterministic_result"], "PASS")
        self.assertEqual(
            document["retry_control_result"]["original_generation_contract_required_cases"],
            retry_doc["after_funnel_totals"]["new_exact_generation_contract_required_cases"],
        )
        self.assertEqual(document["preserved_day50_controls"]["setup_qualified"], 13)
        self.assertEqual(document["preserved_day50_controls"]["trade_candidates"], 9)
        self.assertEqual(document["preserved_day50_controls"]["selected_contracts"], 5)

    def test_funnel_totals_and_costed_backtest_boundary(self):
        document = self._document()
        after = document["after_funnel_totals"]

        self.assertEqual(after["new_generated_candidates"], 3)
        self.assertEqual(after["new_setup_qualified_candidates"], 3)
        self.assertEqual(after["new_trade_candidates"], 0)
        self.assertEqual(after["new_selected_contracts"], 0)
        self.assertEqual(after["new_eligible_entries"], 0)
        self.assertEqual(after["new_recorded_entries"], 0)
        self.assertEqual(after["new_exact_option_contract_evidence_required_cases"], 3)
        for result in document["costed_results_by_setup_family"].values():
            self.assertEqual(result["status"], "NOT_RUN_NO_TRADE_CANDIDATE")
            self.assertFalse(result["costed_entry_exit_replay_run"])

    def test_writer_and_validator_accept_result(self):
        root = Path(__file__).resolve().parents[1]
        result_path = root / "historical_signal_replay" / "results" / "test_day50_contract.json"
        doc_path = root / "test_day50_contract_result.md"
        original_result = contract.RESULT_PATH
        original_doc = contract.RESULT_DOC_PATH
        try:
            contract.RESULT_PATH = result_path
            contract.RESULT_DOC_PATH = doc_path
            written = contract.write_outputs(
                source_commit="testsha",
                run_timestamp="2026-06-22T00:00:00Z",
            )
            loaded = json.loads(result_path.read_text(encoding="utf-8"))
            validation = validator.validate_result_document(result_path)
        finally:
            contract.RESULT_PATH = original_result
            contract.RESULT_DOC_PATH = original_doc
            if result_path.exists():
                result_path.unlink()
            if doc_path.exists():
                doc_path.unlink()

        self.assertEqual(written, loaded)
        self.assertEqual(validation["status"], "PASS")
        self.assertEqual(validation["problems"], [])


def _record(document, family):
    for record in document["setup_family_contract_records"]:
        if record["setup_family"] == family:
            return record
    raise AssertionError(f"missing family record: {family}")


if __name__ == "__main__":
    unittest.main()
