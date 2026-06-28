import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "historical_signal_replay" / "results" / "day55_source_window_batch_accepted_field_completion.json"

class TestDay55SourceWindowBatchAcceptedFieldCompletion(unittest.TestCase):
    def load(self):
        self.assertTrue(RESULT.is_file(), f"Missing result: {RESULT}")
        return json.loads(RESULT.read_text(encoding="utf-8-sig"))

    def test_batch_completion_exists(self):
        result = self.load()
        self.assertEqual(result["decision"], "BATCH_ACCEPTED_FIELD_COMPLETION_COMPLETE")
        self.assertGreaterEqual(result["total_candidates"], 6)
        self.assertEqual(result["profitability_proof"], "NO")
        self.assertEqual(result["paper_live_eligibility"], "NO")

    def test_no_economics_claim_yet(self):
        result = self.load()
        self.assertEqual(result["entry_status"], "NOT_EVALUATED")
        self.assertEqual(result["exit_status"], "NOT_EVALUATED")
        self.assertIsNone(result["gross_pnl"])
        self.assertIsNone(result["net_pnl"])

    def test_candidates_are_decided(self):
        result = self.load()
        allowed = {"REPLAY_READY_SETUP_TIME_RECORD", "EXACT_BLOCKED_EVIDENCE_GAP"}
        for row in result["candidates"]:
            self.assertIn(row["batch_decision"], allowed)
            if row["batch_decision"] == "REPLAY_READY_SETUP_TIME_RECORD":
                self.assertIsNotNone(row["accepted_setup_time_row"])
                self.assertIsNotNone(row["accepted_trigger"])
                self.assertIsNotNone(row["accepted_invalidation"])
                self.assertIsNotNone(row["terminal_chart_only_outcome"])
            else:
                self.assertTrue(row["blocker"])

    def test_next_action_matches_replay_ready_count(self):
        result = self.load()
        if result["replay_ready_count"] > 0:
            self.assertIn("economics/P&L", result["next_action"])
        else:
            self.assertIn("exact blocked", result["next_action"])

if __name__ == "__main__":
    unittest.main()
