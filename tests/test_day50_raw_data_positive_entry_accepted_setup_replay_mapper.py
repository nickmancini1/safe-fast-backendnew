import json
import unittest
from pathlib import Path

from historical_signal_replay import (
    day50_raw_data_positive_entry_accepted_setup_replay_mapper as mapper,
)
from watcher_foundation import (
    day50_raw_data_positive_entry_accepted_setup_replay_mapper_validator as validator,
)


class Day50AcceptedSetupReplayMapperTests(unittest.TestCase):
    def _rows(self):
        return mapper._read_source_rows(mapper.SOURCE_CSV_PATH)

    def _document(self):
        return mapper.build_mapper_document(
            source_commit="testsha",
            run_timestamp="2026-06-22T00:00:00Z",
        )

    def test_positive_mapping_produces_one_field_package_per_family(self):
        document = self._document()
        packages = document["setup_family_field_packages"]

        self.assertEqual(len(packages), 3)
        self.assertEqual(
            {package["setup_family"] for package in packages},
            {"Ideal", "Clean Fast Break", "Continuation"},
        )
        for package in packages:
            self.assertEqual(package["status"], "FIELD_PACKAGE_ESTABLISHED_REVIEW_ONLY")
            self.assertFalse(package["candidate_generated"])
            self.assertFalse(package["setup_qualified"])
            self.assertFalse(package["trade_candidate"])
            self.assertFalse(package["raw_vendor_bars_treated_as_safe_fast_labels"])
            self.assertEqual(set(package["fields"]), set(mapper.REQUIRED_SETUP_FIELDS))
            self.assertEqual(package["exact_failed_fields"], [])

    def test_field_packages_name_accepted_mapper_paths_not_raw_labels(self):
        document = self._document()

        for package in document["setup_family_field_packages"]:
            for field_name, field in package["fields"].items():
                self.assertEqual(field_name in mapper.REQUIRED_SETUP_FIELDS, True)
                self.assertIn("day50_bounded_accepted_setup_replay_mapper_v1", field["source_rule_path"])
                self.assertNotIn("later favorable", field["value"])
                self.assertTrue(field["timestamp_boundary"])
            self.assertIn("publisher-collapsed", package["fields"]["setup_time_row"]["source_boundary"])
            self.assertIn("not raw", package["fields"]["trigger"]["source_boundary"])

    def test_before_and_after_funnel_totals_are_bounded_to_field_packages(self):
        document = self._document()
        before = document["before_funnel_totals"]
        after = document["after_funnel_totals"]

        self.assertEqual(before["exact_setup_time_field_packages_established"], 0)
        self.assertEqual(before["new_exact_data_required_cases"], 3)
        self.assertEqual(after["raw_opportunities_mapped"], 3)
        self.assertEqual(after["exact_setup_time_field_packages_established"], 3)
        self.assertEqual(after["new_exact_data_required_cases"], 0)
        self.assertEqual(after["new_generated_candidates"], 0)
        self.assertEqual(after["new_setup_qualified_candidates"], 0)
        self.assertEqual(after["new_trade_candidates"], 0)
        self.assertEqual(after["new_selected_contracts"], 0)
        self.assertEqual(after["new_eligible_entries"], 0)
        self.assertEqual(after["new_recorded_entries"], 0)

    def test_missing_setup_time_row_rejects_exact_field(self):
        result = mapper.map_setup_packages([])

        self.assertEqual(result["scorecard"]["exact_setup_time_field_packages_established"], 0)
        self.assertEqual(result["scorecard"]["new_exact_data_required_cases"], 3)
        self.assertTrue(
            all(rejection["exact_failed_fields"] == ["setup_time_row"] for rejection in result["rejections"])
        )

    def test_missing_or_ambiguous_required_fields_reject_before_setup_qualified(self):
        rows = self._rows()
        for field in (
            "trigger",
            "invalidation",
            "freshness_final_signal_state",
            "blocker_caution_review",
        ):
            result = mapper.map_setup_packages(rows, disabled_fields={field})
            self.assertEqual(result["scorecard"]["exact_setup_time_field_packages_established"], 0)
            self.assertEqual(len(result["rejections"]), 3)
            self.assertTrue(all(field in rejection["exact_failed_fields"] for rejection in result["rejections"]))

    def test_same_session_boundary_accepts_authorized_rows_only(self):
        result = mapper.map_setup_packages(self._rows())

        self.assertEqual(result["rejections"], [])
        for package in result["field_packages"]:
            self.assertEqual(
                package["fields"]["session_boundary_behavior"]["value"],
                "same_session_reset_only_no_prior_session_carry",
            )

    def test_prior_session_and_wrong_window_rows_are_rejected(self):
        rows = self._rows()
        prior = dict(rows[0])
        prior["ts_event"] = "2026-03-13T19:59:00.000000000Z"
        future = dict(rows[-1])
        future["ts_event"] = "2026-03-16T20:00:00.000000000Z"

        prior_result = mapper.map_setup_packages([prior] + rows)
        future_result = mapper.map_setup_packages(rows + [future])

        self.assertEqual(prior_result["rejections"][0]["case_id"], "DAY50-SPY-WRONG-WINDOW")
        self.assertIn("session_boundary_behavior", prior_result["rejections"][0]["exact_failed_fields"])
        self.assertEqual(future_result["rejections"][0]["case_id"], "DAY50-SPY-WRONG-WINDOW")
        self.assertIn("session_boundary_behavior", future_result["rejections"][0]["exact_failed_fields"])

    def test_no_hindsight_future_rows_do_not_change_packages_and_future_dependency_rejects(self):
        rows = self._rows()
        full = mapper.map_setup_packages(rows)
        decision = full["field_packages"][0]["setup_time_utc"]
        truncated = [
            row
            for row in rows
            if mapper._format_source_timestamp(mapper._parse_utc(row["ts_event"])) <= decision
        ]
        truncated_result = mapper.map_setup_packages(truncated)
        forced = mapper.map_setup_packages(rows, force_future_dependency=True)

        self.assertEqual(full["field_packages"], truncated_result["field_packages"])
        self.assertTrue(
            any(rejection["reason"] == "future_bar_dependency_rejected" for rejection in forced["rejections"])
        )

    def test_wrong_symbol_rejects_before_setup_qualified(self):
        rows = self._rows()
        wrong = dict(rows[0])
        wrong["symbol"] = "QQQ"
        result = mapper.map_setup_packages([wrong] + rows[1:])

        self.assertEqual(result["rejections"][0]["case_id"], "DAY50-SPY-WRONG-SYMBOL")
        self.assertEqual(result["rejections"][0]["exact_failed_fields"], ["setup_time_row"])

    def test_duplicate_source_rows_and_duplicate_families_are_rejected(self):
        rows = self._rows()
        duplicate_source = mapper.map_setup_packages(rows + [dict(rows[0])])
        duplicate_family = mapper.map_setup_packages(
            rows,
            requested_families=("Ideal", "Ideal"),
        )

        self.assertTrue(
            any(rejection["reason"] == "duplicate_conflicted_source_row" for rejection in duplicate_source["rejections"])
        )
        self.assertTrue(
            any(rejection["reason"] == "duplicate_setup_family_package" for rejection in duplicate_family["rejections"])
        )

    def test_raw_vendor_label_rejection(self):
        result = mapper.map_setup_packages(
            self._rows(),
            raw_vendor_labels={"trend": "up", "candle": "breakout"},
        )

        self.assertEqual(result["scorecard"]["exact_setup_time_field_packages_established"], 0)
        self.assertEqual(result["rejections"][0]["case_id"], "DAY50-SPY-RAW-VENDOR-LABEL-REJECTION")
        self.assertEqual(set(result["rejections"][0]["exact_failed_fields"]), set(mapper.REQUIRED_SETUP_FIELDS))

    def test_all_accepted_regression_cases_are_present_and_pass(self):
        document = self._document()
        cases = document["regression_case_results"]

        self.assertEqual({case["case_id"] for case in cases}, set(mapper.CASE_IDS))
        self.assertTrue(all(case["status"] == "PASS" for case in cases))

    def test_determinism_and_guardrails(self):
        document = self._document()
        policy = document["mapper_policy"]
        guardrails = document["guardrails"]

        self.assertEqual(document["deterministic_comparison"]["result"], "PASS")
        self.assertEqual(document["first_run_hash"], document["second_run_hash"])
        self.assertFalse(policy["raw_vendor_bars_treated_as_safe_fast_labels"])
        self.assertFalse(policy["requested_more_data"])
        self.assertFalse(policy["requested_option_data"])
        self.assertFalse(policy["requested_exit_path_data"])
        self.assertFalse(policy["frozen_trading_rules_changed"])
        self.assertFalse(policy["main_py_changed"])
        self.assertFalse(policy["railway_or_deploy_changed"])
        self.assertFalse(guardrails["schwab_authenticated"])
        self.assertFalse(guardrails["broker_mutation_attempted"])
        self.assertFalse(guardrails["proof_accepted"])
        self.assertFalse(guardrails["profitability_claimed"])
        self.assertFalse(guardrails["paper_eligible"])
        self.assertFalse(guardrails["live_eligible"])

    def test_preserved_controls_and_scorecard(self):
        document = self._document()

        self.assertEqual(document["preserved_day50_controls"]["setup_qualified"], 13)
        self.assertEqual(document["preserved_day50_controls"]["trade_candidates"], 9)
        self.assertEqual(document["preserved_day50_controls"]["selected_contracts"], 5)
        self.assertEqual(document["preserved_day50_controls"]["eligible_entries"], 1)
        self.assertEqual(document["preserved_day50_controls"]["recorded_entries"], 1)
        self.assertEqual(document["preserved_day50_controls"]["closed_safety_rejections_reopened"], 0)
        self.assertEqual(document["preserved_scorecard"]["VALID_TRADE_CAPTURED"], 1)
        self.assertEqual(document["preserved_scorecard"]["TRUE_NO_TRADE"], 4)
        self.assertEqual(document["preserved_scorecard"]["MISSING_DATA"], 10)
        self.assertEqual(document["preserved_scorecard"]["UNRESOLVED"], 0)

    def test_writer_and_validator_accept_result(self):
        root = Path(__file__).resolve().parents[1]
        result_path = root / "historical_signal_replay" / "results" / "test_day50_accepted_mapper.json"
        doc_path = root / "test_day50_accepted_mapper_result.md"
        original_result = mapper.RESULT_PATH
        original_doc = mapper.RESULT_DOC_PATH
        try:
            mapper.RESULT_PATH = result_path
            mapper.RESULT_DOC_PATH = doc_path
            written = mapper.write_outputs(
                source_commit="testsha",
                run_timestamp="2026-06-22T00:00:00Z",
            )
            loaded = json.loads(result_path.read_text(encoding="utf-8"))
            validation = validator.validate_result_document(result_path)
        finally:
            mapper.RESULT_PATH = original_result
            mapper.RESULT_DOC_PATH = original_doc
            if result_path.exists():
                result_path.unlink()
            if doc_path.exists():
                doc_path.unlink()

        self.assertEqual(written, loaded)
        self.assertEqual(validation["status"], "PASS")
        self.assertEqual(validation["problems"], [])


if __name__ == "__main__":
    unittest.main()
