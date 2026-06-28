import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "historical_signal_replay" / "results" / "day55_definition_cost_check_for_replay_ready_candidates.json"


class TestDay55DefinitionCostCheckForReplayReadyCandidates(unittest.TestCase):
    def load(self):
        self.assertTrue(RESULT.is_file(), f"Missing result: {RESULT}")
        return json.loads(RESULT.read_text(encoding="utf-8-sig"))

    def test_cost_check_has_real_definition_requests(self):
        r = self.load()
        self.assertIn(r["status"], {"SUCCESS", "BLOCKED", "FAILURE"})
        self.assertGreater(r["request_count"], 0)
        for req in r["requests"]:
            self.assertEqual(req["dataset"], "OPRA.PILLAR")
            self.assertEqual(req["schema"], "definition")
            self.assertEqual(req["stype_in"], "parent")
            self.assertTrue(req["symbols"].endswith(".OPT"))
            self.assertTrue(req["candidate_ids"])

    def test_cost_only_no_download_no_profit_claim(self):
        r = self.load()
        self.assertTrue(r["cost_only"])
        self.assertFalse(r["download_performed"])
        self.assertEqual(r["profitability_proof"], "NO")
        self.assertEqual(r["paper_live_eligibility"], "NO")
        self.assertEqual(r["economics_ready_count"], 0)

    def test_success_or_exact_blocker(self):
        r = self.load()
        if r["status"] == "SUCCESS":
            self.assertIsNotNone(r["grouped_cost"])
            self.assertTrue(r["vendor_metadata_call_performed"])
        else:
            self.assertIn("failure_reason", r)
            self.assertIsNone(r["grouped_cost"])
            self.assertIn("next_action", r)


if __name__ == "__main__":
    unittest.main()
