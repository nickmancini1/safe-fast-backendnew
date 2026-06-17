import json
import unittest
from pathlib import Path

from historical_signal_replay import cfb_backtest_prep_harness as harness
from historical_signal_replay import cfb_trade_rule_checker as checker


FIXTURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "historical_signal_replay"
    / "fixtures"
    / "cfb_trade_rule_regression_fixtures.json"
)
EXACT_FIXTURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "historical_signal_replay"
    / "fixtures"
    / "cfb_exit_stop_cost_regression_fixtures.json"
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
        exact_fixture_data = json.loads(EXACT_FIXTURE_PATH.read_text(encoding="utf-8"))
        cls.exact_fixtures = exact_fixture_data["fixtures"]
        cls.exact_fixtures_by_id = {
            row["fixture_id"]: row
            for row in cls.exact_fixtures
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

    def test_all_13_exact_value_fixtures_pass(self):
        self.assertEqual(len(self.exact_fixtures), 13)

        for fixture in self.exact_fixtures:
            with self.subTest(fixture_id=fixture["fixture_id"]):
                result = checker.check_cfb_trade_rules_from_fixture(fixture)

                self.assertEqual(
                    result["trade_rule_status"],
                    fixture["expected_rule_status"],
                )
                self.assertEqual(
                    result["rejection_reason"],
                    fixture.get("expected_rejection_reason"),
                )
                self.assertEqual(
                    result["exit_reason"],
                    fixture.get("expected_exit_reason"),
                )

    def test_exact_spy_cfb_002_uses_ask_plus_slippage_without_pnl(self):
        result = self._check_exact(
            "spy_cfb_002_entry_rule_ready_awaiting_backtest_harness"
        )

        self.assertEqual(
            result["trade_rule_status"],
            "entry_rule_ready_awaiting_backtest_harness",
        )
        self.assertEqual(result["entry_fill_basis"], "ask_plus_slippage")
        self.assertEqual(result["cost_adjusted_entry_basis"], 6.37)
        self.assertNotIn("pnl", result)
        self.assertNotIn("proof", result)
        self.assertNotIn("readiness", result)

    def test_exact_profit_target_and_option_stop_values(self):
        profit_result = self._check_exact(
            "profit_target_exit_25_percent_from_adjusted_entry"
        )
        stop_result = self._check_exact(
            "option_premium_stop_15_percent_from_adjusted_entry"
        )

        self.assertEqual(profit_result["exit_reason"], "profit_target")
        self.assertEqual(profit_result["cost_adjusted_entry_basis"], 6.37)
        self.assertEqual(profit_result["cost_adjusted_exit_basis"], 7.98)
        self.assertEqual(stop_result["exit_reason"], "option_premium_stop")
        self.assertEqual(stop_result["cost_adjusted_entry_basis"], 6.37)
        self.assertEqual(stop_result["cost_adjusted_exit_basis"], 5.41)

    def test_exact_invalidation_and_time_exit_values(self):
        invalidation_result = self._check_exact(
            "setup_invalidation_stop_exits_selected_option"
        )
        time_result = self._check_exact("time_exit_1545_et_signal_day")

        self.assertEqual(
            invalidation_result["exit_reason"],
            "setup_invalidation_stop",
        )
        self.assertEqual(time_result["exit_reason"], "time_exit_1545_et")

    def test_exact_earliest_exit_priority_is_deterministic_without_pnl(self):
        result = checker.check_cfb_exact_trade_values(
            candidate_id="SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002",
            entry_ask=6.35,
            exit_bid=8.0,
            underlying_invalidation=678.45,
            underlying_price_at_review=678.44,
            review_time="2026-04-13T19:45:00Z",
            latest_exit_time_et="15:45:00",
            signal_session="2026-04-13",
        )

        self.assertEqual(result["exit_reason"], "profit_target")
        self.assertNotIn("pnl", result)

    def test_exact_zero_cost_failure_sample_and_promotion_blockers(self):
        zero_result = self._check_exact("slippage_buffer_rule_rejects_zero_cost_fill")
        sample_result = self._check_exact(
            "sample_size_gate_requires_20_valid_completed_cfb_examples"
        )
        promotion_result = self._check_exact(
            "promotion_gate_requires_rules_regression_sample_and_expectancy"
        )

        self.assertEqual(zero_result["rejection_reason"], "zero_cost_fill_forbidden")
        self.assertEqual(sample_result["rejection_reason"], "sample_size_below_20")
        self.assertEqual(
            promotion_result["rejection_reason"],
            "positive_expectancy_review_missing",
        )

    def test_backtest_prep_harness_prepares_rows_but_refuses_run_and_pnl(self):
        prepared = harness.prepare_cfb_backtest_prep_rows(self.exact_fixtures[:3])

        self.assertEqual(prepared["harness_status"], "prepared_not_run")
        self.assertFalse(prepared["backtest_run"])
        self.assertFalse(prepared["pnl_calculated"])
        self.assertFalse(prepared["candidate_marked_ready"])
        self.assertEqual(len(prepared["rows"]), 3)
        self.assertEqual(
            prepared["rows"][0]["trade_rule_status"],
            "entry_rule_ready_awaiting_backtest_harness",
        )
        self.assertEqual(prepared["rows"][1]["rejection_reason"], "quote_after_signal")
        self.assertEqual(
            prepared["rows"][2]["rejection_reason"],
            "quote_age_above_5_minutes",
        )

        with self.assertRaises(harness.BacktestRunNotAuthorizedError):
            harness.run_backtest(prepared)
        with self.assertRaises(harness.BacktestRunNotAuthorizedError):
            harness.calculate_pnl(prepared)

    def _check(self, fixture_id):
        return checker.check_cfb_trade_rules_from_fixture(
            self.fixtures_by_id[fixture_id]
        )

    def _check_exact(self, fixture_id):
        return checker.check_cfb_trade_rules_from_fixture(
            self.exact_fixtures_by_id[fixture_id]
        )


if __name__ == "__main__":
    unittest.main()
