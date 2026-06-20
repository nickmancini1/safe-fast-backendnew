import json
import unittest
from pathlib import Path

from historical_signal_replay import day49_positive_entry_setup_evidence_completion as completion
from watcher_foundation import day49_positive_entry_setup_evidence_completion_validator as validator


class Day49PositiveEntrySetupEvidenceCompletionTests(unittest.TestCase):
    def test_builds_eight_formal_candidate_slot_outcomes(self):
        document = completion.build_completion_document(
            source_commit="testsha",
            run_timestamp="2026-06-20T00:00:00Z",
        )

        self.assertEqual(document["result_version"], completion.RESULT_VERSION)
        self.assertEqual(document["candidate_slot_count"], 8)
        self.assertEqual(document["deterministic_comparison"]["result"], "PASS")
        self.assertFalse(document["databento_downloaded"])
        self.assertFalse(document["proof_accepted"])
        self.assertFalse(document["profitability_claimed"])
        self.assertEqual(validator.validate_result_document(document), [])

        classifications = document["scorecard"]["slot_classifications"]
        self.assertEqual(classifications["EXACT_EXTERNAL_SETUP_DATA_REQUIRED"], 4)
        self.assertEqual(classifications["SOURCE_CONTRADICTION"], 3)
        self.assertEqual(classifications["CANDIDATE_UNUSABLE"], 1)

    def test_missing_field_matrix_covers_every_required_setup_field(self):
        document = completion.build_completion_document(
            source_commit="testsha",
            run_timestamp="2026-06-20T00:00:00Z",
        )

        for record in document["candidate_slot_records"]:
            matrix = record["missing_field_matrix"]
            field_names = {field["field_name"] for field in matrix["fields"]}
            self.assertEqual(field_names, set(completion.REQUIRED_SETUP_FIELDS))
            for field in matrix["fields"]:
                self.assertIn(field["field_status"], {"present", "absent", "contradictory"})
                self.assertTrue(field["exact_rule_consumer"])
                self.assertTrue(field["smallest_evidence_needed"])
            self.assertTrue(record["formal_outcome_not_vague_missing_data"])

    def test_replacements_are_not_selected_without_complete_local_setup_evidence(self):
        document = completion.build_completion_document(
            source_commit="testsha",
            run_timestamp="2026-06-20T00:00:00Z",
        )
        replacement = document["replacement_selection"]

        self.assertEqual(replacement["selection_result"], "NO_REPLACEMENT_AVAILABLE")
        self.assertEqual(replacement["complete_local_replacement_count"], 0)
        self.assertEqual(replacement["selected_replacements"], [])
        self.assertEqual(document["scorecard"]["candidate_slots_replaced"], 0)

    def test_request_manifest_is_setup_only_and_cost_unavailable_without_download(self):
        document = completion.build_completion_document(
            source_commit="testsha",
            run_timestamp="2026-06-20T00:00:00Z",
        )
        manifest = document["exact_setup_data_request_manifest"]

        self.assertEqual(manifest["manifest_version"], completion.REQUEST_MANIFEST_VERSION)
        self.assertEqual(manifest["request_count"], 7)
        self.assertFalse(manifest["option_request_included"])
        self.assertFalse(manifest["exit_path_request_included"])
        self.assertFalse(manifest["databento_downloaded"])
        self.assertEqual(manifest["cost_check"]["checked_cost"], "NOT_AVAILABLE")
        self.assertFalse(manifest["cost_check"]["credential_used"])
        self.assertEqual(validator.validate_request_manifest_document(manifest), [])
        for request in manifest["requests"]:
            self.assertNotIn("options", request["schema"].lower())
            self.assertIn("options", request["forbidden_scope"])
            self.assertNotEqual(request["start_timestamp"], "EXACT_SOURCE_WINDOW_START_REQUIRED")
            self.assertNotEqual(request["end_timestamp"], "EXACT_SOURCE_WINDOW_END_REQUIRED")
            self.assertTrue(request["source_file"])
            self.assertTrue(request["source_rows"])

    def test_file_writer_creates_result_and_request_manifest(self):
        root = Path(__file__).resolve().parents[1]
        result_path = root / "historical_signal_replay" / "results" / "test_day49_setup_evidence_tmp.json"
        request_path = (
            root
            / "historical_signal_replay"
            / "source_data"
            / "richer_export_package_work"
            / "test_day49_setup_evidence_request_tmp.json"
        )
        try:
            written = completion.write_completion_document(
                result_path,
                request_path,
                source_commit="testsha",
                run_timestamp="2026-06-20T00:00:00Z",
            )
            loaded = json.loads(result_path.read_text(encoding="utf-8"))
            loaded_request = json.loads(request_path.read_text(encoding="utf-8"))
        finally:
            if result_path.exists():
                result_path.unlink()
            if request_path.exists():
                request_path.unlink()

        self.assertEqual(written, loaded)
        self.assertEqual(loaded_request, written["exact_setup_data_request_manifest"])


if __name__ == "__main__":
    unittest.main()
