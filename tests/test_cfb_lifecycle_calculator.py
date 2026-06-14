import json
import unittest
from pathlib import Path

from historical_signal_replay import cfb_lifecycle_calculator as calculator


FIXTURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "historical_signal_replay"
    / "fixtures"
    / "qqq_cfb_lifecycle_regression_fixtures.json"
)


class CfbLifecycleCalculatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture_data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        cls.fixtures = fixture_data["fixtures"]
        cls.fixtures_by_id = {
            row["fixture_id"]: row
            for row in cls.fixtures
        }

    def test_all_18_fixtures_pass(self):
        self.assertEqual(len(self.fixtures), 18)

        for fixture in self.fixtures:
            with self.subTest(fixture_id=fixture["fixture_id"]):
                result = calculator.calculate_lifecycle_from_fixture(fixture)

                self.assertEqual(
                    result["lifecycle_status"],
                    fixture["expected_lifecycle_status"],
                )
                self.assertEqual(result["lifecycle_as_of"], fixture["expected_as_of"])
                self.assertEqual(
                    result["reviewed_before_signal"],
                    fixture["expected_reviewed_before_signal"],
                )
                self.assertEqual(
                    result["rejection_reason"],
                    fixture["expected_rejection_reason"],
                )

    def test_future_replay_row_is_ignored_without_changing_fresh_status(self):
        result = self._calculate(
            "qqq_cfb_lifecycle_future_replay_row_rejected_for_setup_time_freshness"
        )

        self.assertEqual(result["lifecycle_status"], "fresh")
        self.assertEqual(result["rejection_reason"], "ignored_future_replay_row")
        self.assertIn("forbidden_future_replay_row_time", result["ignored_future_inputs"])
        self.assertEqual(result["errors"], [])

    def test_future_candle_is_ignored_without_changing_fresh_status(self):
        result = self._calculate(
            "qqq_cfb_lifecycle_future_candle_rejected_for_setup_time_freshness"
        )

        self.assertEqual(result["lifecycle_status"], "fresh")
        self.assertEqual(result["rejection_reason"], "ignored_future_candle")
        self.assertIn("forbidden_future_candle_time", result["ignored_future_inputs"])
        self.assertEqual(result["errors"], [])

    def test_higher_base_refresh_allowed_and_rejected(self):
        allowed = self._calculate(
            "qqq_cfb_lifecycle_higher_base_refresh_allowed_new_completed_breakout"
        )
        rejected = self._calculate(
            "qqq_cfb_lifecycle_higher_base_refresh_rejected_missing_new_trigger"
        )

        self.assertEqual(allowed["lifecycle_status"], "fresh")
        self.assertEqual(allowed["rejection_reason"], None)
        self.assertEqual(rejected["lifecycle_status"], "stale")
        self.assertEqual(
            rejected["rejection_reason"],
            "higher_base_refresh_missing_new_trigger",
        )

    def test_state_precedence_is_enforced(self):
        spent_over_expired = self._calculate(
            "qqq_cfb_lifecycle_precedence_spent_wins_over_expired"
        )
        unknown_over_spent = self._calculate(
            "qqq_cfb_lifecycle_precedence_unknown_wins_over_fresh_and_spent"
        )

        self.assertEqual(spent_over_expired["lifecycle_status"], "spent")
        self.assertEqual(unknown_over_spent["lifecycle_status"], "unknown")
        self.assertEqual(
            unknown_over_spent["rejection_reason"],
            "missing_required_trigger_state_precedence_unknown",
        )

    def test_missing_required_data_is_clear_unknown(self):
        missing_trigger = self._calculate("qqq_cfb_lifecycle_unknown_missing_trigger")
        missing_compound = self._calculate(
            "qqq_cfb_lifecycle_unknown_missing_timestamp_stage_prior_state"
        )

        self.assertEqual(missing_trigger["lifecycle_status"], "unknown")
        self.assertEqual(missing_trigger["rejection_reason"], "missing_required_trigger")
        self.assertIn("trigger is missing", missing_trigger["errors"])
        self.assertEqual(missing_compound["lifecycle_status"], "unknown")
        self.assertEqual(
            missing_compound["rejection_reason"],
            "missing_required_timestamp_stage_prior_state_or_row_ordering",
        )

    def test_no_field_implies_trade_choice_pnl_proof_or_readiness(self):
        result = self._calculate(
            "qqq_cfb_lifecycle_fresh_target_initial_break_2026_04_13_1230"
        )

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
        return calculator.calculate_lifecycle_from_fixture(
            self.fixtures_by_id[fixture_id]
        )


if __name__ == "__main__":
    unittest.main()
