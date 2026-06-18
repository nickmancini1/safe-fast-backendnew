import unittest

from historical_signal_replay import cfb_backtest_runner as runner


class CfbBacktestRunnerTests(unittest.TestCase):
    def test_rejection_controls_remain_named_no_trades(self):
        spy_003 = runner.run_cfb_backtest_row(
            runner.load_prepared_candidate_row(runner.SPY_CFB_003_CANDIDATE_ID)
        )
        qqq_001 = runner.run_cfb_backtest_row(
            runner.load_prepared_candidate_row(runner.QQQ_CFB_001_CANDIDATE_ID)
        )

        self.assertEqual(spy_003["result_status"], "no_trade")
        self.assertEqual(spy_003["failure_reason"], "quote_after_signal")
        self.assertEqual(qqq_001["result_status"], "no_trade")
        self.assertEqual(qqq_001["failure_reason"], "quote_age_above_5_minutes")

    def test_spy_cfb_002_exit_path_completes_on_profit_target(self):
        result = runner.run_first_cfb_backtest_path()
        spy_002 = result["results"][0]

        self.assertEqual(result["review_status"], "local_review_output")
        self.assertEqual(
            spy_002["result_status"],
            "completed_review_only",
        )
        self.assertEqual(spy_002["result_name"], "completed_profit_target")
        self.assertEqual(spy_002["entry_time"], "2026-04-13T16:30:00+00:00")
        self.assertEqual(
            spy_002["entry_quote_time"], "2026-04-13T16:29:04.514819+00:00"
        )
        self.assertEqual(spy_002["entry_ask"], 6.35)
        self.assertEqual(spy_002["cost_adjusted_entry_basis"], 6.37)
        self.assertEqual(spy_002["profit_target_adjusted_exit_threshold"], 7.9625)
        self.assertEqual(spy_002["option_stop_adjusted_exit_threshold"], 5.4145)
        self.assertEqual(spy_002["exit_time"], "2026-04-13T19:37:14.335714+00:00")
        self.assertEqual(spy_002["exit_reason"], "profit_target")
        self.assertEqual(spy_002["exit_bid"], 8.0)
        self.assertEqual(spy_002["cost_adjusted_exit_basis"], 7.98)
        self.assertEqual(spy_002["gross_result"], 1.65)
        self.assertEqual(spy_002["cost_slippage_adjusted_result"], 1.61)
        self.assertEqual(spy_002["missing_fields"], [])
        self.assertFalse(spy_002["candidate_marked_ready"])
        self.assertFalse(spy_002["proof_accepted"])
        self.assertFalse(spy_002["profitability_claimed"])

    def test_day47_downloaded_spy_cfb_003_setup_quote_changes_blocker_to_stale_quote(self):
        result = runner.run_day47_grouped_cfb_selected_contract_replay()
        spy_003 = result["results"][1]

        self.assertEqual(
            result["downloaded_data_used"],
            "SPY_CFB_003_selected_contract_setup_window_only",
        )
        self.assertFalse(result["conditional_exit_path_used"])
        self.assertEqual(spy_003["result_status"], "no_trade")
        self.assertEqual(spy_003["failure_reason"], "quote_age_above_5_minutes")
        self.assertEqual(spy_003["entry_time"], "2026-04-15T18:30:00+00:00")
        self.assertEqual(
            spy_003["entry_quote_time"], "2026-04-15T18:22:33.366710+00:00"
        )
        self.assertEqual(spy_003["entry_ask"], 7.66)
        self.assertIsNone(spy_003["exit_time"])
        self.assertFalse(spy_003["candidate_marked_ready"])
        self.assertFalse(spy_003["proof_accepted"])
        self.assertFalse(spy_003["profitability_claimed"])

    def test_spy_cfb_003_downloaded_setup_quote_uses_raw_symbol_mapping_not_failed_local_id(self):
        row = runner.apply_spy_cfb_003_downloaded_setup_quote(
            runner.load_prepared_candidate_row(runner.SPY_CFB_003_CANDIDATE_ID),
            runner.load_local_option_quotes_for_spy_cfb_003_setup_window(),
        )

        self.assertEqual(row["selected_contract"], "SPY   260429C00700000")
        self.assertEqual(row["quote_time"], "2026-04-15T18:22:33.366710979Z")
        self.assertEqual(row["ask"], "7.660000000")
        self.assertEqual(row["bid"], "7.630000000")

    def test_profit_target_exit_uses_bid_minus_slippage(self):
        row = runner.load_prepared_candidate_row(runner.FIRST_REFERENCE_CANDIDATE_ID)
        result = runner.run_cfb_backtest_row(
            row,
            option_quote_rows=[
                self._quote("2026-04-13T16:31:00Z", "8.00"),
                self._quote("2026-04-13T19:45:00Z", "8.10"),
            ],
            underlying_rows=[self._underlying("2026-04-13T19:45:00Z", "680.00")],
        )

        self.assertEqual(result["result_status"], "completed_review_only")
        self.assertEqual(result["exit_reason"], "profit_target")
        self.assertEqual(result["exit_fill_basis"], "bid_minus_slippage")
        self.assertEqual(result["cost_adjusted_exit_basis"], 7.98)

    def test_option_stop_exit_uses_bid_minus_slippage(self):
        row = runner.load_prepared_candidate_row(runner.FIRST_REFERENCE_CANDIDATE_ID)
        result = runner.run_cfb_backtest_row(
            row,
            option_quote_rows=[
                self._quote("2026-04-13T16:31:00Z", "5.43"),
                self._quote("2026-04-13T19:45:00Z", "5.40"),
            ],
            underlying_rows=[self._underlying("2026-04-13T19:45:00Z", "680.00")],
        )

        self.assertEqual(result["exit_reason"], "option_premium_stop")
        self.assertEqual(result["cost_adjusted_exit_basis"], 5.41)

    def test_invalidation_exit_uses_first_option_quote_at_or_after_invalidation(self):
        row = runner.load_prepared_candidate_row(runner.FIRST_REFERENCE_CANDIDATE_ID)
        result = runner.run_cfb_backtest_row(
            row,
            option_quote_rows=[
                self._quote("2026-04-13T17:00:00Z", "6.10"),
                self._quote("2026-04-13T19:45:00Z", "6.20"),
            ],
            underlying_rows=[
                self._underlying("2026-04-13T16:45:00Z", "678.44"),
                self._underlying("2026-04-13T19:45:00Z", "680.00"),
            ],
        )

        self.assertEqual(result["exit_reason"], "setup_invalidation_stop")
        self.assertEqual(result["exit_time"], "2026-04-13T17:00:00+00:00")
        self.assertEqual(result["cost_adjusted_exit_basis"], 6.08)

    def test_time_exit_uses_1545_et_when_no_prior_exit_triggers(self):
        row = runner.load_prepared_candidate_row(runner.FIRST_REFERENCE_CANDIDATE_ID)
        result = runner.run_cfb_backtest_row(
            row,
            option_quote_rows=[
                self._quote("2026-04-13T17:00:00Z", "6.45"),
                self._quote("2026-04-13T19:44:00Z", "6.60"),
            ],
            underlying_rows=[self._underlying("2026-04-13T19:45:00Z", "680.00")],
        )

        self.assertEqual(result["exit_reason"], "time_exit_1545_et")
        self.assertEqual(result["exit_time"], "2026-04-13T19:44:00+00:00")
        self.assertEqual(result["cost_adjusted_exit_basis"], 6.58)

    def _quote(self, ts_event, bid):
        return {
            "symbol": "SPY   260427C00685000",
            "ts_event": ts_event,
            "bid_px_00": bid,
        }

    def _underlying(self, timestamp, low):
        return {
            "timestamp": timestamp,
            "low": low,
        }


if __name__ == "__main__":
    unittest.main()
