import json
import unittest
from pathlib import Path

from historical_signal_replay import (
    day52_existing_setup_option_evidence_end_to_end_backtest as day52_option,
)
from watcher_foundation import (
    day52_existing_setup_option_evidence_end_to_end_backtest_validator as validator,
)


class Day52ExistingSetupOptionEvidenceEndToEndBacktestTests(unittest.TestCase):
    def _document(self):
        return day52_option.build_document(
            source_commit="testsha",
            run_timestamp="2026-06-24T00:00:00Z",
        )

    def test_selected_winner_and_duplicate_suppression_are_stable(self):
        document = self._document()
        decision = document["first_required_decision"]

        self.assertEqual(
            decision["selected_winner_id"],
            "DAY52-SPY-2026-03-16-CLEAN-FAST-BREAK-20260316T133000Z-P39",
        )
        self.assertEqual(decision["setup_family_used_for_economic_winner"], "Clean Fast Break")
        self.assertEqual(document["selected_winner"]["duplicate_group_trade_count"], 1)
        self.assertEqual(
            document["selected_winner"]["suppressed_family_labels"],
            ["Ideal", "Continuation"],
        )

    def test_contract_selection_uses_frozen_cfb_rule_without_future_outcome(self):
        document = self._document()
        result = document["contract_selection_result"]
        candidate = result["deterministic_candidate_if_listed"]

        self.assertEqual(result["status"], "BLOCKED_DEFINITION_EVIDENCE_MISSING")
        self.assertIsNone(result["selected_contract"])
        self.assertEqual(candidate["expiration"], "2026-03-30")
        self.assertEqual(candidate["strike"], "669")
        self.assertEqual(candidate["call_or_put"], "C")
        self.assertEqual(candidate["vendor_symbol"], "SPY   260330C00669000")
        self.assertFalse(
            candidate["selection_inputs_available_by_cutoff"]["definition_evidence"]
        )

    def test_complete_entry_window_is_required_before_entry(self):
        document = self._document()
        timing = document["first_required_decision"]["option_entry_timing_rule"]
        entry = document["complete_entry_window_result"]

        self.assertEqual(timing["earliest_allowed_option_price"], "2026-03-16T13:31:00Z")
        self.assertEqual(timing["latest_allowed_option_price"], "2026-03-16T13:36:00Z")
        self.assertEqual(timing["field_used_for_entry"], "ask")
        self.assertEqual(timing["maximum_quote_age_seconds_for_clean_entry"], 60)
        self.assertEqual(timing["maximum_quote_age_seconds_absolute_no_trade"], 300)
        self.assertEqual(entry["status"], "BLOCKED_COMPLETE_OPTION_PRICE_WINDOW_MISSING")
        self.assertEqual(entry["updates_inspected"], [])
        self.assertIsNone(entry["first_valid_price"])

    def test_rejection_reasons_cover_price_window_and_liquidity_cases(self):
        document = self._document()
        timing = document["first_required_decision"]["option_entry_timing_rule"]
        guardrails = document["guardrails"]

        self.assertEqual(
            timing["pre_trigger_price_rejection_reason"],
            "pre_trigger_quote_not_permitted_for_entry",
        )
        self.assertEqual(
            timing["late_price_rejection_reason"],
            "entry_quote_after_latest_allowed_window",
        )
        self.assertEqual(
            timing["stale_quote_rejection_reason"],
            "quote_age_above_clean_entry_limit_or_above_5_minutes",
        )
        self.assertEqual(
            timing["spread_liquidity_rejection_reason"],
            "spread_or_liquidity_gate_failed",
        )
        self.assertTrue(guardrails["pre_trigger_price_rejected"])
        self.assertTrue(guardrails["late_price_rejected"])
        self.assertTrue(guardrails["stale_quote_rejected"])
        self.assertTrue(guardrails["spread_liquidity_rejected_when_over_limits"])

    def test_tastytrade_limitation_and_databento_network_classification(self):
        document = self._document()

        self.assertEqual(document["tastytrade_result"]["status"], "FIELD_LIMITATION_BLOCKED")
        self.assertFalse(document["tastytrade_result"]["historical_bid_ask_supplied"])
        self.assertEqual(document["databento_result"]["status"], "NETWORK_EXECUTION_BLOCKED")
        self.assertFalse(document["databento_result"]["cost_check_run_in_sandbox"])
        self.assertIn(
            "safe_fast_day52_existing_setup_databento_cost_request.py",
            document["databento_result"]["operator_script"],
        )

    def test_no_entry_exit_or_pnl_is_invented(self):
        document = self._document()
        replay = document["entry_exit_pnl_result"]

        self.assertEqual(replay["stage_reached"], "EXACT_EVIDENCE_REQUEST")
        self.assertIsNone(replay["contract"])
        self.assertIsNone(replay["entry_timestamp"])
        self.assertIsNone(replay["entry_price"])
        self.assertIsNone(replay["exit_timestamp"])
        self.assertIsNone(replay["exit_price"])
        self.assertIsNone(replay["net_pnl"])
        self.assertEqual(document["scope"]["profitability_proof"], "NO")
        self.assertEqual(document["scope"]["paper_live_eligibility"], "NO")

    def test_exact_request_groups_all_required_databento_schemas(self):
        document = self._document()
        request = document["exact_evidence_request"]
        schemas = {item["schema"] for item in request["schemas"]}

        self.assertEqual(
            request["request_status"],
            "EXACT_PRICED_REQUEST_PENDING_OPERATOR_COST_OUTPUT",
        )
        self.assertEqual(
            schemas,
            {"definition", "cmbp-1", "tcbbo", "trades", "statistics"},
        )
        self.assertEqual(request["numerical_cost"], "PENDING_OPERATOR_COST_OUTPUT")

    def test_stage_transition_and_strict_no_trade_counts(self):
        document = self._document()
        after = document["after_funnel_totals"]

        self.assertEqual(after["selected_duplicate_groups_processed"], 1)
        self.assertEqual(after["selected_winner_records"], 1)
        self.assertEqual(after["suppressed_duplicate_records"], 2)
        self.assertEqual(after["trade_candidates"], 0)
        self.assertEqual(after["selected_contracts"], 0)
        self.assertEqual(after["eligible_entries"], 0)
        self.assertEqual(after["recorded_entries"], 0)
        self.assertEqual(after["net_pnl_results"], 0)
        self.assertEqual(after["exact_priced_requests"], 1)
        self.assertEqual(after["invalid_trades_allowed"], 0)

    def test_writer_and_validator_accept_result(self):
        root = Path(__file__).resolve().parents[1]
        result_path = root / "historical_signal_replay" / "results" / "test_day52_option.json"
        doc_path = root / "test_day52_option.md"
        original_result = day52_option.RESULT_PATH
        original_doc = day52_option.RESULT_DOC_PATH
        try:
            day52_option.RESULT_PATH = result_path
            day52_option.RESULT_DOC_PATH = doc_path
            written = day52_option.write_outputs(
                source_commit="testsha",
                run_timestamp="2026-06-24T00:00:00Z",
            )
            loaded = json.loads(result_path.read_text(encoding="utf-8"))
            validation = validator.validate_result_document(result_path)
        finally:
            day52_option.RESULT_PATH = original_result
            day52_option.RESULT_DOC_PATH = original_doc
            if result_path.exists():
                result_path.unlink()
            if doc_path.exists():
                doc_path.unlink()

        self.assertEqual(written, loaded)
        self.assertEqual(validation["status"], "PASS")
        self.assertEqual(validation["problems"], [])


if __name__ == "__main__":
    unittest.main()
