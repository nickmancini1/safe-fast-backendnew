import json
import unittest
from pathlib import Path

from historical_signal_replay import day52_family_numeric_binding_and_promotion as binding
from watcher_foundation import day52_family_numeric_binding_and_promotion_validator as validator


class Day52FamilyNumericBindingAndPromotionTests(unittest.TestCase):
    def _document(self):
        return binding.build_family_numeric_binding_and_promotion_document(
            source_commit="testsha",
            run_timestamp="2026-06-23T00:00:00Z",
        )

    def test_binding_audit_and_decision_matrix(self):
        document = self._document()

        self.assertEqual(document["binding_audit_result"], "LEGITIMATE_SHARED_SETUP_TIME_ROW")
        self.assertEqual(
            {item["family"] for item in document["binding_audit"]},
            {"Ideal", "Clean Fast Break", "Continuation"},
        )
        for audit in document["binding_audit"]:
            self.assertEqual(audit["expected_opportunity_timestamp"], "2026-03-16T13:30:00Z")
            self.assertEqual(audit["actual_bound_setup_time_timestamp"], "2026-03-16T13:30:00Z")
            self.assertEqual(audit["source_row_index"], 2)
            self.assertEqual(audit["source_row"]["publisher_id"], "39")

        for decision in document["family_decision_matrix"]:
            self.assertEqual(decision["decision"], "PROMOTE_CANDIDATE_A")
            self.assertEqual(decision["direction"], "bullish")
            self.assertEqual(decision["trigger"], "668.360000000")
            self.assertEqual(decision["invalidation"], "667.870000000")
            self.assertEqual(decision["accepted_status"], "ACCEPTED")

    def test_accepted_and_provisional_modes_remain_separate_and_no_trade(self):
        document = self._document()
        counts = document["accepted_mode_full_session_counts"]["complete_session_accounting"]

        self.assertTrue(
            document["separation_from_provisional_mode"][
                "accepted_and_provisional_modes_remain_separate"
            ]
        )
        self.assertEqual(counts["setup_qualified_records"], 3)
        self.assertEqual(counts["selected_winner_records"], 1)
        self.assertEqual(counts["suppressed_records"], 2)
        self.assertEqual(counts["trade_candidates"], 0)
        self.assertEqual(counts["selected_contracts"], 0)
        self.assertEqual(document["scope"]["profitability_proof"], "NO")
        self.assertEqual(document["scope"]["paper_live_eligibility"], "NO")

    def test_writer_and_validator_accept_result(self):
        root = Path(__file__).resolve().parents[1]
        result_path = root / "historical_signal_replay" / "results" / "test_day52_binding.json"
        doc_path = root / "test_day52_binding.md"
        original = (binding.RESULT_PATH, binding.RESULT_DOC_PATH)
        try:
            binding.RESULT_PATH = result_path
            binding.RESULT_DOC_PATH = doc_path
            written = binding.write_outputs(
                source_commit="testsha",
                run_timestamp="2026-06-23T00:00:00Z",
            )
            loaded = json.loads(result_path.read_text(encoding="utf-8"))
            validation = validator.validate_result_document(result_path)
        finally:
            binding.RESULT_PATH, binding.RESULT_DOC_PATH = original
            for path in (result_path, doc_path):
                if path.exists():
                    path.unlink()

        self.assertEqual(written, loaded)
        self.assertEqual(validation["status"], "PASS")
        self.assertEqual(validation["problems"], [])


if __name__ == "__main__":
    unittest.main()
