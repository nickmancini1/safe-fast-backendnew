import json
import unittest
from pathlib import Path

from historical_signal_replay import gap_context_calculator as calculator


FIXTURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "historical_signal_replay"
    / "fixtures"
    / "qqq_gap_context_regression_fixtures.json"
)


class GapContextCalculatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture_data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        cls.fixtures = {
            row["fixture_id"]: row
            for row in fixture_data["fixtures"]
        }

    def test_clean_fixture_passes(self):
        result = _calculate("qqq_gap_clean_exact_030_up")

        self.assertEqual(result["gap_context_status"], "clean")
        self.assertAlmostEqual(result["gap_amount"], 0.3)
        self.assertAlmostEqual(result["gap_percent"], 0.3)
        self.assertEqual(result["direction"], "up")
        self.assertTrue(result["gap_context_reviewed_before_signal"])
        self.assertEqual(result["errors"], [])

    def test_caution_boundary_fixtures_pass(self):
        lower = _calculate("qqq_gap_caution_lower_boundary_just_over_030_up")
        upper = _calculate("qqq_gap_caution_upper_boundary_exact_075_up")

        self.assertEqual(lower["gap_context_status"], "caution")
        self.assertAlmostEqual(lower["gap_percent"], 0.3001)
        self.assertEqual(upper["gap_context_status"], "caution")
        self.assertAlmostEqual(upper["gap_percent"], 0.75)

    def test_fail_fixture_passes(self):
        result = _calculate("qqq_gap_fail_just_over_075_up")

        self.assertEqual(result["gap_context_status"], "fail")
        self.assertAlmostEqual(result["gap_amount"], 0.7501)
        self.assertAlmostEqual(result["gap_percent"], 0.7501)

    def test_missing_previous_close_becomes_unknown(self):
        result = _calculate("qqq_gap_unknown_missing_previous_close")

        self.assertEqual(result["gap_context_status"], "unknown")
        self.assertIsNone(result["gap_amount"])
        self.assertIsNone(result["gap_percent"])
        self.assertFalse(result["gap_context_reviewed_before_signal"])
        self.assertIn("previous_close is missing", result["errors"])

    def test_missing_signal_day_open_becomes_unknown(self):
        result = _calculate("qqq_gap_unknown_missing_signal_day_open")

        self.assertEqual(result["gap_context_status"], "unknown")
        self.assertIsNone(result["gap_amount"])
        self.assertIsNone(result["gap_percent"])
        self.assertFalse(result["gap_context_reviewed_before_signal"])
        self.assertIn("signal_day_open is missing", result["errors"])

    def test_future_data_example_is_rejected_without_changing_context(self):
        fixture = self.fixtures["qqq_gap_future_data_rejection_2026_04_13"]
        result = calculator.calculate_gap_context_from_fixture(fixture)

        self.assertEqual(result["gap_context_status"], fixture["expected_status"])
        self.assertAlmostEqual(result["gap_amount"], fixture["expected_gap_amount"])
        self.assertAlmostEqual(result["gap_percent"], fixture["expected_gap_percent"])
        self.assertEqual(
            result["gap_context_as_of"],
            fixture["latest_allowed_source_time"],
        )
        self.assertTrue(result["gap_context_reviewed_before_signal"])
        self.assertEqual(
            result["rejected_future_source_times"],
            ["2026-04-13T17:30:00+00:00"],
        )
        self.assertEqual(result["errors"], [])

    def test_known_qqq_example_returns_clean(self):
        fixture = self.fixtures["qqq_gap_known_target_2026_04_13_clean"]
        result = calculator.calculate_gap_context_from_fixture(fixture)

        self.assertEqual(result["gap_context_status"], "clean")
        self.assertAlmostEqual(result["gap_amount"], -1.565)
        self.assertAlmostEqual(result["gap_percent"], -0.2561290956106183)
        self.assertEqual(result["direction"], "down")
        self.assertEqual(
            result["gap_context_as_of"],
            fixture["latest_allowed_source_time"],
        )
        self.assertTrue(result["gap_context_reviewed_before_signal"])

    def test_no_field_implies_trade_choice_pnl_proof_or_readiness(self):
        result = _calculate("qqq_gap_known_target_2026_04_13_clean")

        forbidden_keys = calculator.FORBIDDEN_OUTPUT_FIELDS
        self.assertTrue(forbidden_keys.isdisjoint(result))

        for unsafe_call in (
            calculator.choose_trade,
            calculator.calculate_pnl,
            calculator.accept_proof,
            calculator.mark_ready,
        ):
            with self.assertRaises(calculator.UnsafeInferenceError):
                unsafe_call(result)


def _calculate(fixture_id):
    fixture_data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    fixtures = {
        row["fixture_id"]: row
        for row in fixture_data["fixtures"]
    }
    return calculator.calculate_gap_context_from_fixture(fixtures[fixture_id])


if __name__ == "__main__":
    unittest.main()
