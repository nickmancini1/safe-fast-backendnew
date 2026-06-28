import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "historical_signal_replay" / "results" / "day55_option_evidence_cost_check_review.json"

class TestDay55OptionEvidenceCostCheckReview(unittest.TestCase):
    def load(self):
        self.assertTrue(RESULT.is_file())
        return json.loads(RESULT.read_text(encoding="utf-8-sig"))

    def test_cost_check_is_blocked_exactly(self):
        r = self.load()
        self.assertEqual(r["decision"], "COST_CHECK_BLOCKED_BY_MISSING_EXACT_OPTION_REQUEST_FIELDS")
        self.assertGreater(r["request_count"], 0)
        self.assertEqual(r["priceable_now_count"], 0)
        self.assertEqual(r["blocked_count"], r["request_count"])
        self.assertFalse(r["vendor_call_performed"])

    def test_missing_contract_fields_are_explicit(self):
        r = self.load()
        for c in r["candidates"]:
            self.assertEqual(c["blocker"], "exact_contract_selection_and_quote_windows_missing")
            self.assertIn("exact option expiration", c["missing_before_cost"])
            self.assertIn("exact long contract", c["missing_before_cost"])
            self.assertIn("entry quote window", c["missing_before_cost"])
            self.assertIn("exit quote window", c["missing_before_cost"])

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
