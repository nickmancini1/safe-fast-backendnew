import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "historical_signal_replay" / "results" / "day55_spy_source_window_continuation_002_setup_time_replay_worksheet.json"


class TestDay55SpyContinuation002SetupTimeReplayWorksheet(unittest.TestCase):
    def load_result(self):
        self.assertTrue(RESULT.is_file(), f"Missing result JSON: {RESULT}")
        return json.loads(RESULT.read_text(encoding="utf-8-sig"))

    def test_candidate_identity_and_source_window_are_locked(self):
        result = self.load_result()
        self.assertEqual(result["candidate_id"], "SPY-SOURCE-WINDOW-CONTINUATION-002")
        self.assertEqual(result["ticker"], "SPY")
        self.assertEqual(result["setup_type"], "Continuation")
        self.assertEqual(result["source_window"]["source_csv_lines"], "156-169")
        self.assertEqual(result["source_window"]["source_start"], "2026-04-16T09:30:00-04:00")
        self.assertEqual(result["source_window"]["source_end"], "2026-04-17T15:30:00-04:00")

    def test_current_decision_is_blocked_evidence_gap_not_trade_proof(self):
        result = self.load_result()
        self.assertEqual(result["current_decision"], "EXACT_BLOCKED_EVIDENCE_GAP")
        self.assertEqual(result["blocker_category"], "CANDIDATE_QUALITY_GAP")
        self.assertEqual(result["blocker"], "missing_accepted_setup_time_replay_fields")
        self.assertEqual(result["accepted_proof_count"], 0)
        self.assertEqual(result["entry_status"], "NOT_EVALUATED")
        self.assertEqual(result["exit_status"], "NOT_EVALUATED")
        self.assertIsNone(result["gross_pnl"])
        self.assertIsNone(result["net_pnl"])
        self.assertEqual(result["profitability_proof"], "NO")
        self.assertEqual(result["paper_live_eligibility"], "NO")

    def test_required_missing_fields_are_explicit(self):
        result = self.load_result()
        required = set(result["required_before_proof_review"])
        self.assertIn("accepted replay fixture row", required)
        self.assertIn("accepted trigger", required)
        self.assertIn("accepted invalidation", required)
        self.assertIn("freshness/final-signal review", required)
        self.assertIn("blocker/caution review", required)
        self.assertIn("no-hindsight replay output", required)
        self.assertIn("exact terminal chart-only outcome review", required)
        self.assertIn("economics", required)

    def test_spy_670c_no_entry_result_remains_preserved(self):
        result = self.load_result()
        preserved = result["spy_670c_preserved"]
        self.assertEqual(preserved["result"], "NO_ENTRY_EXACT_REJECTION")
        self.assertEqual(preserved["first_blocker"], "open_interest_statistics_zero_rows")
        self.assertEqual(preserved["profitability_proof"], "NO")
        self.assertEqual(preserved["paper_live_eligibility"], "NO")


if __name__ == "__main__":
    unittest.main()
