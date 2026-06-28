import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "historical_signal_replay" / "results" / "day55_definition_cost_request_for_replay_ready_candidates.json"

class TestDay55DefinitionCostRequestForReplayReadyCandidates(unittest.TestCase):
    def load(self):
        self.assertTrue(RESULT.is_file())
        return json.loads(RESULT.read_text(encoding="utf-8-sig"))

    def test_definition_request_ready_for_operator_review(self):
        r = self.load()
        self.assertEqual(r["decision"], "DEFINITION_COST_REQUEST_READY_FOR_OPERATOR_REVIEW")
        self.assertGreater(r["request_count"], 0)
        self.assertFalse(r["vendor_call_performed"])
        self.assertFalse(r["contract_selection_ready"])
        self.assertEqual(r["economics_ready_count"], 0)

    def test_definition_schema_only_now(self):
        r = self.load()
        for item in r["requests"]:
            self.assertEqual(item["request_stage"], "DEFINITION_FOR_CONTRACT_SELECTION")
            self.assertEqual(item["schema_to_cost"], "definition")
            self.assertIn("cmbp-1", item["later_required_schemas"])
            self.assertIn("tcbbo", item["later_required_schemas"])
            self.assertIn("trades", item["later_required_schemas"])
            self.assertIn("statistics", item["later_required_schemas"])
            self.assertFalse(item["vendor_call_performed"])
            self.assertFalse(item["contract_selected"])

    def test_no_trade_or_profit_claim(self):
        r = self.load()
        self.assertEqual(r["profitability_proof"], "NO")
        self.assertEqual(r["paper_live_eligibility"], "NO")
        for item in r["requests"]:
            self.assertEqual(item["entry_status"], "NOT_EVALUATED")
            self.assertEqual(item["exit_status"], "NOT_EVALUATED")
            self.assertIsNone(item["gross_pnl"])
            self.assertIsNone(item["net_pnl"])
            self.assertEqual(item["profitability_proof"], "NO")
            self.assertEqual(item["paper_live_eligibility"], "NO")

if __name__ == "__main__":
    unittest.main()
