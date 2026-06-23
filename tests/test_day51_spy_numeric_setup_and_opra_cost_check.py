import json
import unittest
from pathlib import Path
from unittest import mock

from historical_signal_replay import day51_spy_numeric_setup_and_opra_cost_check as day51
from watcher_foundation import day51_spy_numeric_setup_and_opra_cost_check_validator as validator


class Day51SpyNumericSetupAndOpraCostCheckTests(unittest.TestCase):
    def _document(self):
        return day51.build_day51_document(
            source_commit="testsha",
            run_timestamp="2026-06-23T00:00:00Z",
            check_cost=False,
        )

    def test_numeric_setup_contracts_cover_all_three_families_without_invention(self):
        document = self._document()
        records = document["numeric_setup_contracts"]

        self.assertEqual(
            {record["setup_family"] for record in records},
            {"Ideal", "Clean Fast Break", "Continuation"},
        )
        for record in records:
            self.assertEqual(record["symbol"], "SPY")
            self.assertEqual(record["setup_timestamp_utc"], "2026-03-16T13:30:00Z")
            self.assertEqual(record["numeric_underlying_evidence"]["rows_found"], 3)
            self.assertEqual(
                record["numeric_underlying_evidence"]["volume_weighted_close"],
                "668.1674118288091935803447593",
            )
            self.assertIsNone(record["trigger_numeric"])
            self.assertIsNone(record["invalidation_numeric"])
            self.assertEqual(
                record["trigger_numeric_status"],
                "RULE_GAP_NOT_NUMERICALLY_ESTABLISHED",
            )
            self.assertEqual(
                record["invalidation_numeric_status"],
                "RULE_GAP_NOT_NUMERICALLY_ESTABLISHED",
            )

    def test_no_hindsight_and_session_boundaries_are_preserved(self):
        document = self._document()

        for record in document["numeric_setup_contracts"]:
            self.assertEqual(
                record["no_hindsight_boundary"],
                "future_rows_ignored_for_setup_labels",
            )
            self.assertEqual(
                record["session_boundary_behavior"],
                "same_session_reset_only_no_prior_session_carry",
            )
            self.assertEqual(
                record["freshness_final_signal_state"],
                "fresh_final_signal_state_at_setup_time",
            )

    def test_option_specs_are_exact_and_not_unrestricted(self):
        document = self._document()

        for spec in document["exact_option_evidence_specifications"]:
            self.assertEqual(spec["dataset"], "OPRA.PILLAR")
            self.assertEqual(spec["stype_in"], "raw_symbol")
            self.assertEqual(spec["definition_window"]["symbols"], "SPY")
            self.assertEqual(spec["definition_window"]["query_type"], "parent_symbol")
            self.assertEqual(
                spec["permitted_expiration_range"]["start_date"],
                "2026-03-30",
            )
            self.assertEqual(
                spec["permitted_expiration_range"]["end_date"],
                "2026-03-30",
            )
            self.assertEqual(
                spec["quote_window"]["symbols"],
                "selected_raw_symbol_after_definition_filter",
            )
            self.assertEqual(
                spec["exit_evidence_window"]["end_timestamp_utc"],
                "2026-03-16T19:45:00Z",
            )

    def test_cost_check_records_api_failure_without_credentials(self):
        def failing_cost(**kwargs):
            raise RuntimeError("proxy refused test")

        fake_client = mock.Mock()
        fake_client.metadata.get_cost.side_effect = failing_cost
        fake_db = mock.Mock()
        fake_db.Historical.return_value = fake_client

        with mock.patch.dict("os.environ", {}, clear=True), mock.patch.dict(
            "sys.modules",
            {"databento": fake_db},
        ):
            document = day51.build_day51_document(
                source_commit="testsha",
                run_timestamp="2026-06-23T00:00:00Z",
                check_cost=True,
            )

        cost = document["grouped_opra_cost_check"]
        self.assertEqual(cost["status"], "NOT_AVAILABLE")
        self.assertEqual(cost["grouped_total"], "NOT_AVAILABLE")
        self.assertFalse(cost["credential_configured"])
        self.assertFalse(cost["credential_used"])
        self.assertTrue(cost["external_cost_api_called"])
        self.assertFalse(cost["download_created"])
        self.assertIn("Databento cost check failed", cost["reason"])
        self.assertEqual(cost["api_attempts"][0]["status"], "FAILED")
        self.assertIn("proxy refused test", cost["api_attempts"][0]["technical_failure"])
        self.assertEqual(
            document["approval_required"]["status"],
            "APPROVAL_REQUIRED_COST_ESTIMATE_BLOCKED",
        )

    def test_replay_stops_before_selected_contract_and_pnl(self):
        document = self._document()

        for result in document["costed_backtest_results_by_setup_family"].values():
            self.assertFalse(result["trade_candidate"])
            self.assertFalse(result["selected_contract_stage"])
            self.assertFalse(result["eligible_entry"])
            self.assertFalse(result["recorded_entry"])
            self.assertFalse(result["costed_exit_replay_run"])
            self.assertIsNone(result["selected_contract"])
            self.assertIsNone(result["entry_price"])
            self.assertIsNone(result["exit_price"])
            self.assertIsNone(result["net_pnl"])

    def test_required_regression_and_control_coverage_is_declared(self):
        document = self._document()
        coverage = document["test_coverage_contract"]

        for key in (
            "numeric_setup_contracts_all_three_families",
            "no_hindsight",
            "developing_stage_transitions",
            "session_boundaries_and_carry_forward",
            "deterministic_winner_selection",
            "stale_spent_and_blocker_rejection",
            "no_trade_preservation",
            "mapper_regressions",
            "mapper_to_generation_regressions",
            "package_to_candidate_regressions",
            "option_selection_and_execution_cost_controls",
            "day51_handoff_consistency",
            "focused_validators",
            "safe_checks_execution_policy_bypass",
            "git_diff_check",
        ):
            self.assertTrue(coverage[key])
        self.assertEqual(
            document["control_results"]["accepted_mapper_regression_case_count"],
            17,
        )

    def test_funnel_totals_preserve_no_trade_boundary(self):
        document = self._document()
        after = document["after_funnel_totals"]

        self.assertEqual(after["new_generated_candidates"], 3)
        self.assertEqual(after["new_setup_qualified_candidates"], 3)
        self.assertEqual(after["new_trade_candidates"], 0)
        self.assertEqual(after["new_selected_contracts"], 0)
        self.assertEqual(after["new_eligible_entries"], 0)
        self.assertEqual(after["new_recorded_entries"], 0)
        self.assertEqual(after["new_exact_option_contract_evidence_required_cases"], 3)
        self.assertEqual(after["new_invalid_trades_allowed"], 0)

    def test_writer_and_validator_accept_result(self):
        root = Path(__file__).resolve().parents[1]
        result_path = root / "historical_signal_replay" / "results" / "test_day51_result.json"
        doc_path = root / "test_day51_result.md"
        original_result = day51.RESULT_PATH
        original_doc = day51.RESULT_DOC_PATH
        fake_client = mock.Mock()
        fake_client.metadata.get_cost.side_effect = RuntimeError("proxy refused test")
        fake_db = mock.Mock()
        fake_db.Historical.return_value = fake_client
        try:
            day51.RESULT_PATH = result_path
            day51.RESULT_DOC_PATH = doc_path
            with mock.patch.dict("os.environ", {}, clear=True), mock.patch.dict(
                "sys.modules",
                {"databento": fake_db},
            ):
                written = day51.write_outputs(
                    source_commit="testsha",
                    run_timestamp="2026-06-23T00:00:00Z",
                    check_cost=True,
                )
            loaded = json.loads(result_path.read_text(encoding="utf-8"))
            validation = validator.validate_result_document(result_path)
        finally:
            day51.RESULT_PATH = original_result
            day51.RESULT_DOC_PATH = original_doc
            if result_path.exists():
                result_path.unlink()
            if doc_path.exists():
                doc_path.unlink()

        self.assertEqual(written, loaded)
        self.assertEqual(validation["status"], "PASS")
        self.assertEqual(validation["problems"], [])


if __name__ == "__main__":
    unittest.main()
