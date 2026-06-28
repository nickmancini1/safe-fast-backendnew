import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "historical_signal_replay" / "results" / "day55_replay_ready_candidates_economic_preflight.json"

class TestDay55ReplayReadyCandidatesEconomicPreflight(unittest.TestCase):
    def load(self):
        self.assertTrue(RESULT.is_file(), f"Missing result: {RESULT}")
        return json.loads(RESULT.read_text(encoding="utf-8-sig"))

    def test_preflight_moves_to_economic_layer(self):
        r = self.load()
        self.assertEqual(r["decision"], "ECONOMIC_PREFLIGHT_COMPLETE")
        self.assertGreater(r["replay_ready_candidates"], 0)
        self.assertEqual(r["economics_ready_count"], 0)
        self.assertEqual(r["exact_blocked_count"], r["replay_ready_candidates"])

    def test_blocker_is_economic_evidence_not_setup_work(self):
        r = self.load()
        for c in r["candidates"]:
            self.assertEqual(c["blocker_category"], "ECONOMIC_EVIDENCE_GAP")
            self.assertEqual(c["blocker"], "missing_candidate_option_chain_quote_trade_statistics_evidence")
            self.assertIn("option evidence request", c["next_source_action"])

    def test_no_profit_or_live_claim(self):
        r = self.load()
        self.assertEqual(r["profitability_proof"], "NO")
        self.assertEqual(r["paper_live_eligibility"], "NO")
        for c in r["candidates"]:
            self.assertEqual(c["entry_status"], "NOT_EVALUATED")
            self.assertEqual(c["exit_status"], "NOT_EVALUATED")
            self.assertIsNone(c["gross_pnl"])
            self.assertIsNone(c["net_pnl"])

if __name__ == "__main__":
    unittest.main()
