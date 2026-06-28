import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "historical_signal_replay" / "results" / "day55_definition_contract_selection_for_replay_ready_candidates.json"

class TestDay55DefinitionContractSelectionForReplayReadyCandidates(unittest.TestCase):
    def load(self):
        self.assertTrue(RESULT.is_file(), f"Missing result: {RESULT}")
        return json.loads(RESULT.read_text(encoding="utf-8-sig"))

    def test_definition_selection_completed(self):
        r = self.load()
        self.assertEqual(r["decision"], "DEFINITION_CONTRACT_SELECTION_COMPLETE")
        self.assertTrue(r["vendor_call_performed"])
        self.assertTrue(r["download_performed"])
        self.assertEqual(r["downloaded_schema"], "definition")
        self.assertFalse(r["quote_trade_statistics_download_performed"])
        self.assertGreater(r["candidate_count"], 0)

    def test_selected_contracts_or_exact_blockers(self):
        r = self.load()
        self.assertEqual(r["candidate_count"], r["contracts_selected_count"] + r["exact_blocked_count"])
        for c in r["candidates"]:
            if c["contract_selection_status"] == "CONTRACTS_SELECTED_FOR_QUOTE_TRADE_STATISTICS_REQUEST":
                self.assertTrue(c["long_contract"]["raw_symbol"])
                self.assertTrue(c["short_contract"]["raw_symbol"])
                self.assertTrue(c["spread_width"])
            else:
                self.assertEqual(c["contract_selection_status"], "EXACT_BLOCKED_EVIDENCE_GAP")
                self.assertTrue(c["blocker"])

    def test_no_profit_or_live_claim(self):
        r = self.load()
        self.assertEqual(r["profitability_proof"], "NO")
        self.assertEqual(r["paper_live_eligibility"], "NO")
        for c in r["candidates"]:
            self.assertEqual(c["entry_status"], "NOT_EVALUATED")
            self.assertEqual(c["exit_status"], "NOT_EVALUATED")
            self.assertIsNone(c["gross_pnl"])
            self.assertIsNone(c["net_pnl"])
            self.assertEqual(c["profitability_proof"], "NO")
            self.assertEqual(c["paper_live_eligibility"], "NO")

if __name__ == "__main__":
    unittest.main()
