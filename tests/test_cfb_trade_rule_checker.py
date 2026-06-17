import json
import unittest
from pathlib import Path

from historical_signal_replay import cfb_trade_rule_checker as checker


FIXTURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "historical_signal_replay"
    / "fixtures"
    / "cfb_trade_rule_regression_fixtures.json"
)


class CfbTradeRuleCheckerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture_data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        cls.fixtures = fixture_data["fixtures"]
        cls.fixtures_by_id = {
            row["fixture_id"]: row
            for row in cls.fixtures
        }

    def test_all_11_grouped_fixtures_pass(self):
        self.assertEqual(len(self.fixtures), 11)

        for fixture in self.fixtures:
            with self.subTest(fixture_id=fixture["fixture_id"]):
                result = checker.check_cfb_trade_rules_from_fixture(fixture)

                self.assertEqual(
                    result["trade_rule_status"],
                    fixture["expected_trade_rule_status"],
                )
                self.assertEqual(
                    result["rejection_reason"],
                    fixture["expected_rejection_reason"],
                )

    def test_spy_cfb_002_reaches_pre_backtest_block_not_bad_entry(self):
        result = self._check("spy_cfb_002_first_usable_reference_gate_passes_pre_exit")

        self.assertEqual(result["trade_rule_status"], "blocked_pre_backtest")
        self.assertEqual(result["rejection_reason"], "missing_exit_rule")
        self.assertEqual(result["entry_fill_basis"], "ask")
        self.assertEqual(result["entry_price"], 6.35)
        self.assertAlmostEqual(result["quote_age_seconds"], 55.485181)
        self.assertNotIn("missing_selected_contract", result["blocking_reasons"])
        self.assertNotIn("missing_entry_quote", result["blocking_reasons"])
        self.assertIn("missing_cost_slippage", result["blocking_reasons"])
        self.assertIn("sample_size_gate_missing", result["blocking_reasons"])
        self.assertIn("promotion_gate_missing", result["blocking_reasons"])

    def test_spy_cfb_003_quote_after_signal_returns_no_trade(self):
        result = self._check("spy_cfb_003_quote_after_signal_no_trade")

        self.assertEqual(result["trade_rule_status"], "no_trade")
        self.assertEqual(result["rejection_reason"], "quote_after_signal")
        self.assertLess(result["quote_age_seconds"], 0)

    def test_qqq_cfb_001_stale_quote_returns_no_trade(self):
        result = self._check("qqq_cfb_001_stale_quote_failed_execution")

        self.assertEqual(result["trade_rule_status"], "no_trade")
        self.assertEqual(result["rejection_reason"], "quote_age_above_5_minutes")
        self.assertAlmostEqual(result["quote_age_seconds"], 1409.359699)

    def test_missing_selected_contract_blocks_entry(self):
        result = self._check("missing_selected_contract_blocks_entry")

        self.assertEqual(result["trade_rule_status"], "blocked")
        self.assertEqual(result["rejection_reason"], "missing_selected_contract")

    def test_missing_entry_quote_blocks_entry(self):
        result = self._check("missing_entry_quote_blocks_entry")

        self.assertEqual(result["trade_rule_status"], "blocked")
        self.assertEqual(result["rejection_reason"], "missing_entry_quote")

    def test_missing_exit_rule_blocks_countable_results(self):
        result = self._check("missing_exit_rule_blocks_counting")

        self.assertEqual(result["trade_rule_status"], "blocked_pre_backtest")
        self.assertEqual(result["rejection_reason"], "missing_exit_rule")

    def test_missing_invalidation_blocks_entry(self):
        result = self._check("missing_stop_invalidation_blocks_entry")

        self.assertEqual(result["trade_rule_status"], "blocked")
        self.assertEqual(result["rejection_reason"], "missing_invalidation")

    def test_missing_cost_slippage_blocks_countable_results(self):
        result = self._check("missing_cost_slippage_blocks_counting")

        self.assertEqual(result["trade_rule_status"], "blocked_pre_backtest")
        self.assertEqual(result["rejection_reason"], "missing_cost_slippage")

    def test_missing_failure_diagnosis_blocks_known_blockers(self):
        result = self._check("failure_diagnosis_required_for_known_blocker")

        self.assertEqual(result["trade_rule_status"], "blocked")
        self.assertEqual(result["rejection_reason"], "failure_diagnosis_required")

    def test_missing_sample_size_gate_blocks_promotion(self):
        result = self._check("sample_size_gate_required_before_promotion")

        self.assertEqual(result["trade_rule_status"], "blocked_promotion")
        self.assertEqual(result["rejection_reason"], "sample_size_gate_missing")

    def test_missing_promotion_gate_blocks_readiness(self):
        result = self._check("promotion_gate_required_before_readiness")

        self.assertEqual(result["trade_rule_status"], "blocked_promotion")
        self.assertEqual(result["rejection_reason"], "promotion_gate_missing")

    def test_forbidden_fields_cannot_improve_status_or_infer_outputs(self):
        result = self._check("promotion_gate_required_before_readiness")

        self.assertEqual(result["trade_rule_status"], "blocked_promotion")
        self.assertEqual(result["rejection_reason"], "promotion_gate_missing")
        self.assertIn("pnl", result["ignored_forbidden_inputs"])
        self.assertIn("proof_label", result["ignored_forbidden_inputs"])
        self.assertIn("profitability_label", result["ignored_forbidden_inputs"])
        self.assertIn("readiness_label", result["ignored_forbidden_inputs"])
        self.assertTrue(checker.FORBIDDEN_OUTPUT_FIELDS.isdisjoint(result))

        for unsafe_call in (
            checker.choose_trade,
            checker.calculate_pnl,
            checker.accept_proof,
            checker.mark_ready,
        ):
            with self.assertRaises(checker.UnsafeInferenceError):
                unsafe_call(result)

    def _check(self, fixture_id):
        return checker.check_cfb_trade_rules_from_fixture(
            self.fixtures_by_id[fixture_id]
        )


if __name__ == "__main__":
    unittest.main()
