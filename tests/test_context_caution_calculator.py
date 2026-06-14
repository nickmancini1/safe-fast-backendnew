import json
import unittest
from pathlib import Path

from historical_signal_replay import context_caution_calculator as calculator


FIXTURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "historical_signal_replay"
    / "fixtures"
    / "qqq_cfb_context_caution_regression_fixtures.json"
)


class ContextCautionCalculatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture_data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        cls.fixtures = fixture_data["fixtures"]
        cls.fixtures_by_id = {
            row["fixture_id"]: row
            for row in cls.fixtures
        }

    def test_all_22_fixtures_pass(self):
        self.assertEqual(len(self.fixtures), 22)

        for fixture in self.fixtures:
            with self.subTest(fixture_id=fixture["fixture_id"]):
                result = calculator.calculate_context_caution_from_fixture(fixture)

                self.assertEqual(
                    result["context_caution_status"],
                    fixture["expected_status"],
                )
                self.assertEqual(
                    result["context_caution_as_of"],
                    fixture["expected_as_of"],
                )
                self.assertEqual(
                    result["reviewed_before_signal"],
                    fixture["expected_reviewed_before_signal"],
                )
                self.assertEqual(
                    result["rejection_reason"],
                    fixture["expected_rejection_reason"],
                )

    def test_component_statuses_are_classified(self):
        option = self._calculate("qqq_cfb_option_context_framework_clean")
        headline = self._calculate("qqq_cfb_headline_context_framework_caution")
        execution = self._calculate("qqq_cfb_execution_context_framework_fail")

        self.assertEqual(option["option_context_status"], "clean")
        self.assertEqual(headline["headline_context_status"], "caution")
        self.assertEqual(execution["execution_context_status"], "fail")

    def test_missing_decision_defaults_remain_unknown(self):
        option = self._calculate(
            "qqq_cfb_option_context_unknown_missing_contract_selection"
        )
        headline = self._calculate(
            "qqq_cfb_headline_context_unknown_missing_source_policy"
        )
        execution = self._calculate(
            "qqq_cfb_execution_context_unknown_missing_entry_fill_rules"
        )

        self.assertEqual(option["option_context_status"], "unknown")
        self.assertEqual(
            option["rejection_reason"],
            "missing_selected_contract_policy",
        )
        self.assertEqual(headline["headline_context_status"], "unknown")
        self.assertEqual(
            headline["rejection_reason"],
            "missing_historical_headline_source_policy",
        )
        self.assertEqual(execution["execution_context_status"], "unknown")
        self.assertEqual(
            execution["rejection_reason"],
            "missing_entry_timing_and_fill_assumption",
        )

    def test_complete_caution_precedence_is_enforced(self):
        all_clean = self._calculate("qqq_cfb_complete_caution_all_clean")
        one_caution = self._calculate(
            "qqq_cfb_complete_caution_one_caution_no_fail_unknown"
        )
        fail = self._calculate(
            "qqq_cfb_complete_caution_fail_beats_unknown_caution_clean"
        )
        unknown = self._calculate(
            "qqq_cfb_complete_caution_unknown_beats_caution_clean"
        )

        self.assertEqual(all_clean["complete_caution_review_status"], "clean")
        self.assertEqual(one_caution["complete_caution_review_status"], "caution")
        self.assertEqual(fail["complete_caution_review_status"], "fail")
        self.assertEqual(unknown["complete_caution_review_status"], "unknown")
        self.assertEqual(
            unknown["rejection_reason"],
            "required_component_unknown",
        )

    def test_future_and_forbidden_inputs_are_ignored(self):
        future_option = self._calculate(
            "qqq_cfb_context_future_option_quote_rejected"
        )
        future_headline = self._calculate(
            "qqq_cfb_context_future_headline_rejected"
        )
        forbidden_complete = self._calculate(
            "qqq_cfb_context_forbidden_fill_pnl_profitability_readiness_rejected"
        )

        self.assertEqual(future_option["option_context_status"], "unknown")
        self.assertEqual(future_option["rejection_reason"], "ignored_future_option_quote")
        self.assertIn(
            "forbidden_future_option_quote_time",
            future_option["ignored_forbidden_inputs"],
        )
        self.assertEqual(future_headline["headline_context_status"], "unknown")
        self.assertEqual(
            future_headline["rejection_reason"],
            "ignored_future_headline",
        )
        self.assertEqual(
            forbidden_complete["rejection_reason"],
            "ignored_fill_broker_order_account_outcome_pnl_profitability_readiness",
        )

    def test_wrong_identity_rejected(self):
        wrong_symbol = self._calculate("qqq_cfb_context_wrong_symbol_unknown")
        wrong_setup = self._calculate("qqq_cfb_context_wrong_setup_unknown")

        self.assertEqual(wrong_symbol["context_caution_status"], "unknown")
        self.assertEqual(wrong_symbol["rejection_reason"], "wrong_symbol")
        self.assertEqual(wrong_setup["context_caution_status"], "unknown")
        self.assertEqual(wrong_setup["rejection_reason"], "wrong_setup_type")

    def test_no_field_implies_trade_choice_pnl_proof_or_readiness(self):
        result = self._calculate("qqq_cfb_complete_caution_all_clean")

        self.assertTrue(calculator.FORBIDDEN_OUTPUT_FIELDS.isdisjoint(result))

        for unsafe_call in (
            calculator.choose_trade,
            calculator.calculate_pnl,
            calculator.accept_proof,
            calculator.mark_ready,
        ):
            with self.assertRaises(calculator.UnsafeInferenceError):
                unsafe_call(result)

    def _calculate(self, fixture_id):
        return calculator.calculate_context_caution_from_fixture(
            self.fixtures_by_id[fixture_id]
        )


if __name__ == "__main__":
    unittest.main()
