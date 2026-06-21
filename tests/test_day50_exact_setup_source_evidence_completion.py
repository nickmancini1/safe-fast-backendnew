import json
import unittest
from pathlib import Path

from historical_signal_replay import day50_exact_setup_source_evidence_completion as completion


class Day50ExactSetupSourceEvidenceCompletionTests(unittest.TestCase):
    def test_builds_four_candidate_closure_without_promotion(self):
        document = completion.build_completion_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        self.assertEqual(document["result_version"], completion.RESULT_VERSION)
        self.assertEqual(document["candidate_count"], 4)
        self.assertEqual(document["deterministic_comparison"]["result"], "PASS")
        self.assertEqual(document["setup_source_requests_remaining"], 0)
        self.assertFalse(document["option_request_included"])
        self.assertFalse(document["exit_path_request_included"])
        self.assertFalse(document["databento_downloaded"])
        self.assertFalse(document["schwab_authenticated"])
        self.assertFalse(document["proof_accepted"])
        self.assertFalse(document["profitability_claimed"])

        scorecard = document["scorecard"]
        self.assertEqual(scorecard["current_setup_source_slots_reviewed"], 4)
        self.assertEqual(scorecard["setup_source_slots_completed_with_accepted_evidence"], 0)
        self.assertEqual(scorecard["setup_source_slots_formally_closed"], 4)
        self.assertEqual(scorecard["setup_source_requests_remaining"], 0)
        self.assertEqual(scorecard["setup_qualified_candidates"], 0)
        self.assertEqual(scorecard["trade_candidates"], 0)

    def test_all_target_candidates_are_formally_closed(self):
        document = completion.build_completion_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        records = {
            record["candidate_identifier"]: record
            for record in document["candidate_records"]
        }

        self.assertEqual(set(records), set(completion.TARGET_CANDIDATES))
        for candidate_id, record in records.items():
            self.assertEqual(
                record["final_classification"],
                "SETUP_SOURCE_CLOSED_NO_ACCEPTED_EVIDENCE",
            )
            self.assertEqual(record["highest_stage_reached"], "SETUP_DEVELOPING")
            self.assertFalse(record["setup_qualified"])
            self.assertFalse(record["trade_candidate"])
            self.assertFalse(record["proof_accepted"])
            self.assertTrue(record["source_file"])
            self.assertTrue(record["source_rows"])
            self.assertIn("SETUP_SOURCE_EVIDENCE_CLOSED", record["chronological_rerun_path"])

    def test_required_fields_are_resolved_or_closed_with_sources(self):
        document = completion.build_completion_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        for record in document["candidate_records"]:
            fields = record["field_resolutions"]
            self.assertEqual(
                {field["field_name"] for field in fields},
                set(completion.REQUIRED_SETUP_FIELDS),
            )
            for field in fields:
                self.assertEqual(field["local_evidence_status"], "closed_not_accepted")
                self.assertEqual(
                    field["final_resolution"],
                    "SETUP_SOURCE_CLOSED_NO_ACCEPTED_EVIDENCE",
                )
                self.assertTrue(field["primary_source"])
                self.assertTrue(field["local_calculator_or_consumer"])
                self.assertTrue(field["timestamp_window"])
                self.assertTrue(field["closure_note"])

    def test_next_task_routes_to_positive_entry_expansion(self):
        document = completion.build_completion_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        next_task = document["next_task"]
        self.assertEqual(
            next_task["filename"],
            "SAFE_FAST_DAY50_POSITIVE_ENTRY_EXPANSION_AFTER_SETUP_SOURCE_CLOSURE_CODEX_TASK.md",
        )
        self.assertEqual(
            next_task["route"],
            "positive_entry_expansion_after_all_current_slots_resolved_or_closed",
        )
        self.assertEqual(document["databento_cost_check"]["checked_cost"], "NOT_AVAILABLE")
        self.assertFalse(document["databento_cost_check"]["credential_used"])

    def test_file_writer_creates_result(self):
        root = Path(__file__).resolve().parents[1]
        result_path = (
            root
            / "historical_signal_replay"
            / "results"
            / "test_day50_exact_setup_source_completion_tmp.json"
        )
        try:
            written = completion.write_completion_document(
                result_path,
                source_commit="testsha",
                run_timestamp="2026-06-21T00:00:00Z",
            )
            loaded = json.loads(result_path.read_text(encoding="utf-8"))
        finally:
            if result_path.exists():
                result_path.unlink()

        self.assertEqual(written, loaded)


if __name__ == "__main__":
    unittest.main()
