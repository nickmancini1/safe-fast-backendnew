import json
import unittest
from pathlib import Path

from historical_signal_replay import cfb_contract_selector as selector


FIXTURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "historical_signal_replay"
    / "fixtures"
    / "qqq_cfb_contract_selection_regression_fixtures.json"
)
NEW_CONTRACT_OI_EXCEPTION_FIXTURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "historical_signal_replay"
    / "fixtures"
    / "qqq_cfb_new_contract_oi_exception_regression_fixtures.json"
)


class CfbContractSelectorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture_data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        cls.fixtures = fixture_data["fixtures"]
        cls.fixtures_by_id = {
            row["fixture_id"]: row
            for row in cls.fixtures
        }
        exception_fixture_data = json.loads(
            NEW_CONTRACT_OI_EXCEPTION_FIXTURE_PATH.read_text(encoding="utf-8")
        )
        cls.exception_fixtures = exception_fixture_data["fixtures"]
        cls.exception_fixtures_by_id = {
            row["fixture_id"]: row
            for row in cls.exception_fixtures
        }

    def test_all_18_fixtures_pass(self):
        self.assertEqual(len(self.fixtures), 18)

        for fixture in self.fixtures:
            with self.subTest(fixture_id=fixture["fixture_id"]):
                result = selector.select_contract_from_fixture(fixture)

                self.assertEqual(
                    result["contract_selection_status"],
                    fixture["expected_status"],
                )
                self.assertEqual(
                    result["selected_contract"],
                    fixture["expected_selected_contract"],
                )
                self.assertEqual(
                    result["rejection_reason"],
                    fixture["expected_rejection_reason"],
                )

    def test_ranking_prefers_nearest_expiration_then_lowest_strike(self):
        expiration = self._select(
            "qqq_cfb_contract_selection_nearest_valid_expiration_selected"
        )
        strike = self._select(
            "qqq_cfb_contract_selection_lowest_strike_at_or_above_trigger_selected"
        )

        self.assertEqual(expiration["selected_contract"], "QQQ   260430C00614000")
        self.assertEqual(strike["selected_contract"], "QQQ   260427C00614000")

    def test_no_fallback_after_top_ranked_contract_fails(self):
        result = self._select("qqq_cfb_contract_selection_no_fallback_if_top_ranked_fails")

        self.assertEqual(result["contract_selection_status"], "abstain")
        self.assertEqual(
            result["rejection_reason"],
            "top_ranked_contract_failed_no_fallback",
        )
        self.assertIsNone(result["selected_contract"])

    def test_timestamp_gates_reject_future_quote_and_statistics(self):
        quote = self._select("qqq_cfb_contract_selection_quote_after_signal_rejected")
        statistics = self._select(
            "qqq_cfb_contract_selection_statistics_after_signal_rejected"
        )

        self.assertEqual(quote["rejection_reason"], "quote_ts_event_after_signal")
        self.assertEqual(
            statistics["rejection_reason"],
            "statistics_ts_event_after_signal",
        )

    def test_spread_size_volume_and_open_interest_gates_reject(self):
        fixture_ids = {
            "qqq_cfb_contract_selection_spread_above_absolute_cap_rejected":
                "spread_above_0_15",
            "qqq_cfb_contract_selection_spread_percent_above_cap_rejected":
                "spread_pct_above_2_percent",
            "qqq_cfb_contract_selection_bid_size_below_minimum_rejected":
                "bid_size_below_1",
            "qqq_cfb_contract_selection_ask_size_below_minimum_rejected":
                "ask_size_below_1",
            "qqq_cfb_contract_selection_volume_below_minimum_rejected":
                "trade_volume_below_1",
            "qqq_cfb_contract_selection_open_interest_below_minimum_rejected":
                "open_interest_below_1",
        }

        for fixture_id, reason in fixture_ids.items():
            with self.subTest(fixture_id=fixture_id):
                self.assertEqual(self._select(fixture_id)["rejection_reason"], reason)

    def test_no_field_implies_trade_choice_pnl_proof_or_readiness(self):
        result = self._select("qqq_cfb_contract_selection_valid_selected_contract")

        self.assertTrue(selector.FORBIDDEN_OUTPUT_FIELDS.isdisjoint(result))

        for unsafe_call in (
            selector.choose_trade,
            selector.calculate_pnl,
            selector.accept_proof,
            selector.mark_ready,
        ):
            with self.assertRaises(selector.UnsafeInferenceError):
                unsafe_call(result)

    def test_all_13_new_contract_oi_exception_fixtures_pass(self):
        self.assertEqual(len(self.exception_fixtures), 13)

        for fixture in self.exception_fixtures:
            with self.subTest(fixture_id=fixture["fixture_id"]):
                result = selector.evaluate_new_contract_oi_exception_from_fixture(
                    fixture
                )

                self.assertEqual(
                    result["option_context_status"],
                    fixture["expected_option_context_status"],
                )
                self.assertEqual(
                    result["rejection_reason"],
                    fixture["expected_rejection_reason"],
                )

    def test_new_contract_oi_exception_valid_case_returns_caution(self):
        result = self._evaluate_exception(
            "qqq_cfb_new_contract_oi_exception_valid_returns_caution"
        )

        self.assertEqual(result["option_context_status"], "caution")
        self.assertIsNone(result["rejection_reason"])

    def test_new_contract_oi_exception_rejects_prior_day_present_missing_oi(self):
        result = self._evaluate_exception(
            "qqq_cfb_new_contract_oi_exception_prior_day_present_oi_missing_rejected"
        )

        self.assertEqual(result["option_context_status"], "unknown")
        self.assertEqual(
            result["rejection_reason"],
            "prior_day_contract_present_open_interest_missing",
        )

    def test_new_contract_oi_exception_preserves_no_fallback(self):
        result = self._evaluate_exception(
            "qqq_cfb_new_contract_oi_exception_fallback_rejected"
        )

        self.assertEqual(result["option_context_status"], "unknown")
        self.assertEqual(
            result["rejection_reason"],
            "top_ranked_contract_failed_no_fallback",
        )

    def test_new_contract_oi_exception_rejects_future_data(self):
        result = self._evaluate_exception(
            "qqq_cfb_new_contract_oi_exception_future_data_rejected"
        )

        self.assertEqual(result["option_context_status"], "unknown")
        self.assertEqual(result["rejection_reason"], "future_data_detected")

    def test_new_contract_oi_exception_output_does_not_infer_trade_results(self):
        result = self._evaluate_exception(
            "qqq_cfb_new_contract_oi_exception_valid_returns_caution"
        )

        self.assertTrue(selector.FORBIDDEN_OUTPUT_FIELDS.isdisjoint(result))

    def _select(self, fixture_id):
        return selector.select_contract_from_fixture(self.fixtures_by_id[fixture_id])

    def _evaluate_exception(self, fixture_id):
        return selector.evaluate_new_contract_oi_exception_from_fixture(
            self.exception_fixtures_by_id[fixture_id]
        )


if __name__ == "__main__":
    unittest.main()
