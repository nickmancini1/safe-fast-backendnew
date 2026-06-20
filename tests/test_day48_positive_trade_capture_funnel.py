import json
import unittest
from pathlib import Path

from historical_signal_replay import day48_positive_trade_capture_funnel as funnel
from watcher_foundation import day48_positive_trade_capture_funnel_validator as validator


class Day48PositiveTradeCaptureFunnelTests(unittest.TestCase):
    def test_funnel_builds_required_scorecards_and_deterministic_hashes(self):
        document = funnel.build_funnel_document(
            source_commit="testsha",
            run_timestamp="2026-06-20T00:00:00Z",
        )

        self.assertEqual([], validator.validate_funnel_document(document))
        self.assertEqual(document["source_commit"], "testsha")
        self.assertEqual(document["deterministic_comparison"]["result"], "PASS")
        self.assertEqual(document["first_run_hash"], document["second_run_hash"])
        self.assertEqual(len(document["candidate_records"]), 15)
        self.assertEqual(
            document["funnel_stages"],
            validator.REQUIRED_STAGES,
        )

        combined = document["combined_scorecard"]
        self.assertEqual(combined["valid_trades_captured"], 1)
        self.assertEqual(combined["true_no_trades"], 2)
        self.assertEqual(combined["missing_data_cases"], 8)
        self.assertEqual(combined["missed_valid_trades"], 0)
        self.assertEqual(combined["invalid_trades_allowed"], 0)
        self.assertEqual(combined["unresolved_cases"], 4)
        self.assertEqual(combined["winners"], 1)
        self.assertEqual(combined["losers"], 0)
        self.assertEqual(combined["deterministic_cases"], 15)
        self.assertEqual(combined["unstable_cases"], 0)

    def test_true_no_trade_missing_data_and_valid_capture_stay_separate(self):
        document = funnel.build_funnel_document(
            source_commit="testsha",
            run_timestamp="2026-06-20T00:00:00Z",
        )
        by_id = {
            row["candidate_identifier"]: row
            for row in document["candidate_records"]
        }

        spy_002 = by_id["SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002"]
        spy_003 = by_id["SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003"]
        qqq_001 = by_id["QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001"]
        spy_continuation = by_id["first_real_spy_continuation_replay_v1_fixture"]

        self.assertEqual(spy_002["final_classification"], "VALID_TRADE_CAPTURED")
        self.assertEqual(spy_002["winner_or_loser"], "winner")
        self.assertFalse(spy_002["proof_accepted"])
        self.assertFalse(spy_002["profitability_claimed"])

        self.assertEqual(spy_003["final_classification"], "TRUE_NO_TRADE")
        self.assertEqual(spy_003["exact_blocker_code"], "quote_age_above_5_minutes")
        self.assertEqual(spy_003["blocker_category"], "real frozen-rule failure")
        self.assertEqual(qqq_001["final_classification"], "TRUE_NO_TRADE")
        self.assertEqual(qqq_001["exact_blocker_code"], "quote_age_above_5_minutes")

        self.assertEqual(spy_continuation["final_classification"], "MISSING_DATA")
        self.assertEqual(
            spy_continuation["first_stage_not_reached"],
            "CONTRACT_SELECTED",
        )
        self.assertEqual(spy_continuation["blocker_category"], "missing data")

    def test_family_and_combined_scorecards_keep_positive_capture_visible(self):
        document = funnel.build_funnel_document(
            source_commit="testsha",
            run_timestamp="2026-06-20T00:00:00Z",
        )

        self.assertEqual(
            document["family_scorecards"]["Clean Fast Break"]["valid_trades_captured"],
            1,
        )
        self.assertEqual(
            document["family_scorecards"]["Ideal"]["valid_trades_captured"],
            0,
        )
        self.assertEqual(
            document["family_scorecards"]["Continuation"]["valid_trades_captured"],
            0,
        )
        self.assertEqual(
            document["combined_scorecard"]["first_blocker_totals_by_funnel_stage"][
                "CONTRACT_SELECTED"
            ],
            6,
        )
        self.assertEqual(
            document["combined_scorecard"]["first_blocker_totals_by_funnel_stage"][
                "ENTRY_ELIGIBLE"
            ],
            2,
        )

    def test_file_writer_creates_machine_readable_result(self):
        path = (
            Path(__file__).resolve().parents[1]
            / "historical_signal_replay"
            / "results"
            / "test_day48_positive_trade_capture_funnel_tmp.json"
        )
        try:
            written = funnel.write_funnel_document(
                path,
                source_commit="testsha",
                run_timestamp="2026-06-20T00:00:00Z",
            )
            loaded = json.loads(path.read_text(encoding="utf-8"))
        finally:
            if path.exists():
                path.unlink()

        self.assertEqual(written, loaded)
        self.assertEqual([], validator.validate_funnel_document(loaded))


if __name__ == "__main__":
    unittest.main()
