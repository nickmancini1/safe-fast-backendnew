import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "historical_signal_replay" / "results" / "day55_replay_ready_candidates_option_evidence_request.json"

class TestDay55ReplayReadyCandidatesOptionEvidenceRequest(unittest.TestCase):
    def load(self):
        self.assertTrue(RESULT.is_file())
        return json.loads(RESULT.read_text(encoding="utf-8-sig"))

    def test_ready_for_operator_cost_check(self):
        r = self.load()
        self.assertEqual(r["decision"], "OPTION_EVIDENCE_REQUEST_READY_FOR_OPERATOR_COST_CHECK")
        self.assertGreater(r["request_count"], 0)
        self.assertFalse(r["vendor_call_performed"])
        self.assertEqual(r["economics_ready_count"], 0)

    def test_required_option_evidence(self):
        r = self.load()
        for item in r["requests"]:
            required = set(item["required_option_evidence"])
            self.assertIn("candidate contract selection", required)
            self.assertIn("entry-window quotes", required)
            self.assertIn("entry-window trades", required)
            self.assertIn("entry-window statistics/OI", required)
            self.assertIn("exit-window quotes", required)
            self.assertIn("gross P&L", required)
            self.assertIn("net P&L", required)

    def test_no_profit_or_live_claim(self):
        r = self.load()
        self.assertEqual(r["profitability_proof"], "NO")
        self.assertEqual(r["paper_live_eligibility"], "NO")

if __name__ == "__main__":
    unittest.main()
