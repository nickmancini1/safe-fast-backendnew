import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "historical_signal_replay" / "results" / "day55_source_window_batch_source_row_packet.json"

class TestDay55SourceWindowBatchSourceRowPacket(unittest.TestCase):
    def load(self):
        self.assertTrue(RESULT.is_file(), f"Missing result: {RESULT}")
        return json.loads(RESULT.read_text(encoding="utf-8-sig"))

    def test_packet_exists_and_preserves_no_trade_state(self):
        result = self.load()
        self.assertEqual(result["decision"], "BATCH_SOURCE_ROW_PACKET_COMPLETE")
        self.assertGreaterEqual(result["total_candidates"], 6)
        self.assertEqual(result["entry_status"], "NOT_EVALUATED")
        self.assertEqual(result["exit_status"], "NOT_EVALUATED")
        self.assertIsNone(result["gross_pnl"])
        self.assertIsNone(result["net_pnl"])
        self.assertEqual(result["profitability_proof"], "NO")
        self.assertEqual(result["paper_live_eligibility"], "NO")

    def test_required_candidates_are_present(self):
        result = self.load()
        ids = {row["candidate_id"] for row in result["candidates"]}
        self.assertIn("SPY-SOURCE-WINDOW-CONTINUATION-002", ids)
        self.assertIn("QQQ-SOURCE-WINDOW-CLEAN-FAST-BREAK-002", ids)
        self.assertIn("SPY-SOURCE-WINDOW-CLEAN-FAST-BREAK-003", ids)
        self.assertIn("SPY-SOURCE-WINDOW-CONTINUATION-004", ids)
        self.assertIn("SPY-SOURCE-WINDOW-CONTINUATION-005", ids)
        self.assertIn("QQQ-SOURCE-WINDOW-CONTINUATION-002", ids)

    def test_each_candidate_has_source_file_decision(self):
        result = self.load()
        allowed = {
            "SOURCE_ROWS_EXTRACTED",
            "SOURCE_CSV_NOT_FOUND",
            "SOURCE_CSV_AMBIGUOUS",
            "SOURCE_ROWS_MISSING",
        }
        for row in result["candidates"]:
            self.assertIn(row["source_file_status"], allowed)
            self.assertIn(row["decision"], {
                "SOURCE_ROWS_EXTRACTED_FOR_FIELD_ACCEPTANCE",
                "EXACT_BLOCKED_EVIDENCE_GAP",
            })

    def test_next_action_points_to_field_acceptance_or_source_file_fix(self):
        result = self.load()
        self.assertIn("accepted setup-time row", result["next_action"])
        self.assertIn("economics/P&L", result["next_action"])

if __name__ == "__main__":
    unittest.main()
