import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "historical_signal_replay" / "results" / "day55_spy_source_window_continuation_002_field_completion_result.json"

class TestSpyContinuation002FieldCompletionResult(unittest.TestCase):
    def load(self):
        self.assertTrue(RESULT.is_file())
        return json.loads(RESULT.read_text(encoding="utf-8-sig"))

    def test_exact_blocked_gap(self):
        r = self.load()
        self.assertEqual(r["candidate_id"], "SPY-SOURCE-WINDOW-CONTINUATION-002")
        self.assertEqual(r["decision"], "EXACT_BLOCKED_EVIDENCE_GAP")
        self.assertEqual(r["blocker"], "accepted_setup_time_replay_fields_not_completed")

    def test_no_trade_or_profit_claim(self):
        r = self.load()
        self.assertEqual(r["entry_status"], "NOT_EVALUATED")
        self.assertEqual(r["exit_status"], "NOT_EVALUATED")
        self.assertIsNone(r["gross_pnl"])
        self.assertIsNone(r["net_pnl"])
        self.assertEqual(r["profitability_proof"], "NO")
        self.assertEqual(r["paper_live_eligibility"], "NO")

    def test_next_action_is_explicit(self):
        r = self.load()
        self.assertIn("156-169", r["next_source_action"])
        self.assertIn("before economics", r["next_source_action"])

if __name__ == "__main__":
    unittest.main()
