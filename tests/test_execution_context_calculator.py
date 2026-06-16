import json
import unittest
from pathlib import Path

from historical_signal_replay import execution_context_calculator as calculator


FIXTURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "historical_signal_replay"
    / "fixtures"
    / "qqq_cfb_execution_context_regression_fixtures.json"
)
SPY_FIXTURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "historical_signal_replay"
    / "fixtures"
    / "spy_cfb_execution_context_regression_fixtures.json"
)
SPY_IDEAL_FIXTURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "historical_signal_replay"
    / "fixtures"
    / "spy_ideal_execution_context_regression_fixtures.json"
)


class ExecutionContextCalculatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture_data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        cls.fixtures = fixture_data["fixtures"]
        cls.fixtures_by_id = {
            row["fixture_id"]: row
            for row in cls.fixtures
        }
        spy_fixture_data = json.loads(SPY_FIXTURE_PATH.read_text(encoding="utf-8"))
        cls.spy_fixtures = spy_fixture_data["fixtures"]
        cls.spy_fixtures_by_id = {
            row["fixture_id"]: row
            for row in cls.spy_fixtures
        }
        spy_ideal_fixture_data = json.loads(
            SPY_IDEAL_FIXTURE_PATH.read_text(encoding="utf-8")
        )
        cls.spy_ideal_fixtures = spy_ideal_fixture_data["fixtures"]
        cls.spy_ideal_fixtures_by_id = {
            row["fixture_id"]: row
            for row in cls.spy_ideal_fixtures
        }

    def test_all_13_fixtures_pass(self):
        self.assertEqual(len(self.fixtures), 13)

        for fixture in self.fixtures:
            with self.subTest(fixture_id=fixture["fixture_id"]):
                result = calculator.calculate_execution_context_from_fixture(fixture)

                self.assertEqual(
                    result["execution_context_status"],
                    fixture["expected_execution_context_status"],
                )
                self.assertEqual(
                    result["rejection_reason"],
                    fixture["expected_rejection_reason"],
                )
                if fixture["expected_quote_age_seconds"] is None:
                    self.assertIsNone(result["quote_age_seconds"])
                else:
                    self.assertAlmostEqual(
                        result["quote_age_seconds"],
                        fixture["expected_quote_age_seconds"],
                    )

    def test_quote_age_boundaries_are_classified(self):
        clean = self._calculate("qqq_cfb_execution_clean_quote_age_60_seconds")
        caution_lower = self._calculate(
            "qqq_cfb_execution_caution_quote_age_61_seconds"
        )
        caution_upper = self._calculate(
            "qqq_cfb_execution_caution_quote_age_300_seconds"
        )
        stale = self._calculate("qqq_cfb_execution_fail_quote_age_301_seconds")

        self.assertEqual(clean["execution_context_status"], "clean")
        self.assertEqual(caution_lower["execution_context_status"], "caution")
        self.assertEqual(caution_upper["execution_context_status"], "caution")
        self.assertEqual(stale["execution_context_status"], "fail")
        self.assertEqual(stale["rejection_reason"], "quote_age_above_5_minutes")

    def test_known_qqq_target_stale_quote_fails(self):
        result = self._calculate("qqq_cfb_execution_known_target_stale_quote_fail")

        self.assertEqual(result["execution_context_status"], "fail")
        self.assertAlmostEqual(result["quote_age_seconds"], 1409.359699)
        self.assertEqual(result["rejection_reason"], "quote_age_above_5_minutes")

    def test_future_quote_missing_fields_and_no_fallback_reject(self):
        future = self._calculate("qqq_cfb_execution_quote_after_signal_rejected")
        missing_source = self._calculate("qqq_cfb_execution_missing_source_data_unknown")
        no_fallback = self._calculate(
            "qqq_cfb_execution_no_fallback_and_forbidden_fields_rejected"
        )

        self.assertEqual(future["rejection_reason"], "quote_after_signal")
        self.assertEqual(missing_source["execution_context_status"], "unknown")
        self.assertEqual(missing_source["rejection_reason"], "missing_source_data")
        self.assertEqual(
            no_fallback["rejection_reason"],
            "top_ranked_contract_failed_no_fallback",
        )
        self.assertIn("pnl", no_fallback["ignored_forbidden_inputs"])
        self.assertIn("proof_label", no_fallback["ignored_forbidden_inputs"])
        self.assertIn("readiness_label", no_fallback["ignored_forbidden_inputs"])

    def test_no_field_implies_trade_choice_pnl_proof_or_readiness(self):
        result = self._calculate("qqq_cfb_execution_clean_quote_age_60_seconds")

        self.assertTrue(calculator.FORBIDDEN_OUTPUT_FIELDS.isdisjoint(result))

        for unsafe_call in (
            calculator.choose_trade,
            calculator.calculate_pnl,
            calculator.accept_proof,
            calculator.mark_ready,
        ):
            with self.assertRaises(calculator.UnsafeInferenceError):
                unsafe_call(result)

    def test_all_3_spy_cfb_execution_fixtures_pass(self):
        self.assertEqual(len(self.spy_fixtures), 3)

        for fixture in self.spy_fixtures:
            with self.subTest(fixture_id=fixture["fixture_id"]):
                result = calculator.calculate_execution_context_from_fixture(fixture)

                self.assertEqual(
                    result["execution_context_status"],
                    fixture["expected_execution_context_status"],
                )
                self.assertEqual(
                    result["rejection_reason"],
                    fixture["expected_rejection_reason"],
                )
                if fixture["expected_quote_age_seconds"] is None:
                    self.assertIsNone(result["quote_age_seconds"])
                else:
                    self.assertAlmostEqual(
                        result["quote_age_seconds"],
                        fixture["expected_quote_age_seconds"],
                    )

    def test_spy_cfb_002_starter_execution_is_clean(self):
        result = calculator.calculate_execution_context_from_fixture(
            self.spy_fixtures_by_id["spy_cfb_002_starter_execution_clean"]
        )

        self.assertEqual(result["execution_context_status"], "clean")
        self.assertAlmostEqual(result["quote_age_seconds"], 55.485181)

    def test_spy_cfb_003_starter_execution_stays_unknown_without_selected_quote(self):
        result = calculator.calculate_execution_context_from_fixture(
            self.spy_fixtures_by_id[
                "spy_cfb_003_starter_execution_unknown_no_selected_quote"
            ]
        )

        self.assertEqual(result["execution_context_status"], "unknown")
        self.assertEqual(result["rejection_reason"], "missing_source_data")

    def test_all_2_spy_ideal_execution_fixtures_pass(self):
        self.assertEqual(len(self.spy_ideal_fixtures), 2)

        for fixture in self.spy_ideal_fixtures:
            with self.subTest(fixture_id=fixture["fixture_id"]):
                result = calculator.calculate_execution_context_from_fixture(fixture)

                self.assertEqual(
                    result["execution_context_status"],
                    fixture["expected_execution_context_status"],
                )
                self.assertEqual(
                    result["rejection_reason"],
                    fixture["expected_rejection_reason"],
                )
                if fixture["expected_quote_age_seconds"] is None:
                    self.assertIsNone(result["quote_age_seconds"])
                else:
                    self.assertAlmostEqual(
                        result["quote_age_seconds"],
                        fixture["expected_quote_age_seconds"],
                    )

    def test_spy_ideal_execution_stays_unknown_without_selected_quote(self):
        result = calculator.calculate_execution_context_from_fixture(
            self.spy_ideal_fixtures_by_id[
                "spy_ideal_starter_execution_unknown_no_selected_quote"
            ]
        )

        self.assertEqual(result["execution_context_status"], "unknown")
        self.assertEqual(result["rejection_reason"], "missing_source_data")

    def _calculate(self, fixture_id):
        return calculator.calculate_execution_context_from_fixture(
            self.fixtures_by_id[fixture_id]
        )


if __name__ == "__main__":
    unittest.main()
