import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "historical_signal_replay" / "results" / "day55_source_window_batch_exact_blocker_closeout.json"

class TestDay55SourceWindowBatchExactBlockerCloseout(unittest.TestCase):
    def load(self):
        self.assertTrue(RESULT.is_file(), f"Missing result: {RESULT}")
        return json.loads(RESULT.read_text(encoding="utf-8-sig"))

    def test_batch_is_closed_as_exact_blocker(self):
        result = self.load()
        self.assertEqual(result["decision"], "BATCH_CLOSED_EXACT_BLOCKED_EVIDENCE_GAP")
        self.assertEqual(result["blocker_category"], "CANDIDATE_QUALITY_GAP")
        self.assertEqual(result["replay_ready_count"], 0)
        self.assertEqual(result["total_candidates"], result["exact_blocked_count"])

    def test_no_economics_or_profit_claim(self):
        result = self.load()
        self.assertEqual(result["entry_status"], "NOT_EVALUATED")
        self.assertEqual(result["exit_status"], "NOT_EVALUATED")
        self.assertIsNone(result["gross_pnl"])
        self.assertIsNone(result["net_pnl"])
        self.assertEqual(result["profitability_proof"], "NO")
        self.assertEqual(result["paper_live_eligibility"], "NO")

    def test_each_candidate_has_exact_missing_fields(self):
        result = self.load()
        self.assertGreaterEqual(len(result["candidates"]), 6)
        for row in result["candidates"]:
            self.assertEqual(row["final_decision"], "EXACT_BLOCKED_EVIDENCE_GAP")
            self.assertTrue(row["missing_or_unaccepted_fields"])
            self.assertEqual(row["entry_status"], "NOT_EVALUATED")
            self.assertEqual(row["exit_status"], "NOT_EVALUATED")

    def test_next_action_blocks_single_candidate_loop(self):
        result = self.load()
        self.assertIn("do not run another single-candidate worksheet loop", result["next_action"].lower())

if __name__ == "__main__":
    unittest.main()
