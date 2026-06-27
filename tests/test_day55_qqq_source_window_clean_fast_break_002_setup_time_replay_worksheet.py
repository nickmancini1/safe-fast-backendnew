import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "historical_signal_replay" / "results" / "day55_qqq_source_window_clean_fast_break_002_setup_time_replay_worksheet.json"

class TestQQQCleanFastBreak002Worksheet(unittest.TestCase):
    def load(self):
        self.assertTrue(RESULT.is_file())
        return json.loads(RESULT.read_text(encoding="utf-8-sig"))

    def test_identity(self):
        r = self.load()
        self.assertEqual(r["candidate_id"], "QQQ-SOURCE-WINDOW-CLEAN-FAST-BREAK-002")
        self.assertEqual(r["ticker"], "QQQ")
        self.assertEqual(r["setup_type"], "Clean Fast Break")
        self.assertEqual(r["source_window"]["source_csv_lines"], "66-86")

    def test_blocked_not_trade(self):
        r = self.load()
        self.assertEqual(r["current_decision"], "EXACT_BLOCKED_EVIDENCE_GAP")
        self.assertEqual(r["blocker_category"], "CANDIDATE_QUALITY_GAP")
        self.assertEqual(r["blocker"], "missing_accepted_setup_time_replay_fields")
        self.assertEqual(r["entry_status"], "NOT_EVALUATED")
        self.assertEqual(r["exit_status"], "NOT_EVALUATED")
        self.assertIsNone(r["gross_pnl"])
        self.assertIsNone(r["net_pnl"])
        self.assertEqual(r["profitability_proof"], "NO")
        self.assertEqual(r["paper_live_eligibility"], "NO")

    def test_next_action(self):
        r = self.load()
        self.assertIn("66-86", r["next_action"])
        self.assertIn("before economics", r["next_action"])

if __name__ == "__main__":
    unittest.main()
