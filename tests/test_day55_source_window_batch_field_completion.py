import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "historical_signal_replay" / "results" / "day55_source_window_batch_field_completion.json"

class TestDay55SourceWindowBatchFieldCompletion(unittest.TestCase):
    def load(self):
        self.assertTrue(RESULT.is_file(), f"Missing result: {RESULT}")
        return json.loads(RESULT.read_text(encoding="utf-8-sig"))

    def test_batch_result_exists_and_has_candidates(self):
        result = self.load()
        self.assertEqual(result["decision"], "BATCH_FIELD_COMPLETION_COMPLETE")
        self.assertGreaterEqual(result["total_candidates"], 6)
        self.assertEqual(result["profitability_proof"], "NO")
        self.assertEqual(result["paper_live_eligibility"], "NO")

    def test_required_known_candidates_are_covered(self):
        result = self.load()
        ids = {row["candidate_id"] for row in result["candidates"]}
        self.assertIn("SPY-SOURCE-WINDOW-CONTINUATION-002", ids)
        self.assertIn("QQQ-SOURCE-WINDOW-CLEAN-FAST-BREAK-002", ids)
        self.assertIn("SPY-SOURCE-WINDOW-CLEAN-FAST-BREAK-003", ids)
        self.assertIn("SPY-SOURCE-WINDOW-CONTINUATION-004", ids)
        self.assertIn("SPY-SOURCE-WINDOW-CONTINUATION-005", ids)
        self.assertIn("QQQ-SOURCE-WINDOW-CONTINUATION-002", ids)

    def test_no_trade_or_profit_claim_is_made(self):
        result = self.load()
        for row in result["candidates"]:
            self.assertIn(row["batch_decision"], {"REPLAY_READY_SETUP_TIME_RECORD", "EXACT_BLOCKED_EVIDENCE_GAP"})
            self.assertEqual(row["entry_status"], "NOT_EVALUATED")
            self.assertEqual(row["exit_status"], "NOT_EVALUATED")
            self.assertIsNone(row["gross_pnl"])
            self.assertIsNone(row["net_pnl"])
            self.assertEqual(row["profitability_proof"], "NO")
            self.assertEqual(row["paper_live_eligibility"], "NO")

    def test_next_action_is_economics_or_blocker_not_single_candidate_loop(self):
        result = self.load()
        self.assertIn("economics/P&L", result["next_action"])
        self.assertIn("missing field list", result["next_action"])

if __name__ == "__main__":
    unittest.main()
