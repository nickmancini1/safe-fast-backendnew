import json
import unittest
from pathlib import Path

from historical_signal_replay import day50_required_setup_source_resolution as resolution


class Day50RequiredSetupSourceResolutionTests(unittest.TestCase):
    def test_builds_required_eight_candidate_resolution(self):
        document = resolution.build_resolution_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        self.assertEqual(document["result_version"], resolution.RESULT_VERSION)
        self.assertEqual(document["candidate_count"], 8)
        self.assertEqual(document["deterministic_comparison"]["result"], "PASS")
        self.assertFalse(document["databento_downloaded"])
        self.assertFalse(document["schwab_authenticated"])
        self.assertFalse(document["proof_accepted"])
        self.assertFalse(document["profitability_claimed"])

        scorecard = document["scorecard"]
        self.assertEqual(scorecard["external_data_cases_resolved_by_source_routing"], 4)
        self.assertEqual(scorecard["external_data_cases_still_requiring_exact_requests"], 4)
        self.assertEqual(scorecard["source_conflicts_resolved"], 3)
        self.assertEqual(scorecard["source_conflicts_excluded"], 3)
        self.assertEqual(scorecard["unusable_candidates"], 1)
        self.assertEqual(scorecard["setup_qualified_candidates"], 0)
        self.assertEqual(scorecard["trade_candidates"], 0)

    def test_source_conflicts_are_formally_excluded(self):
        document = resolution.build_resolution_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        records = {
            record["candidate_identifier"]: record
            for record in document["candidate_records"]
        }

        for candidate_id in resolution.SOURCE_CONFLICT_CANDIDATES:
            record = records[candidate_id]
            self.assertEqual(record["final_classification"], "SOURCE_CONFLICT_EXCLUDED")
            self.assertEqual(
                record["source_resolution_result"],
                "source_conflict_closed_by_registry_priority",
            )
            conflict = record["source_conflict_resolution"]
            self.assertEqual(conflict["chosen_value_or_exclusion"], "SOURCE_CONFLICT_EXCLUDED")
            self.assertIn("SAFE-FAST frozen local chronological replay", conflict["registry_priority"])

    def test_external_requests_are_setup_source_only(self):
        document = resolution.build_resolution_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )
        request = document["remaining_exact_external_setup_request"]

        self.assertEqual(request["request_count"], 4)
        self.assertFalse(request["option_request_included"])
        self.assertFalse(request["exit_path_request_included"])
        self.assertEqual(request["cost_check"]["checked_cost"], "NOT_AVAILABLE")
        self.assertFalse(request["cost_check"]["credential_used"])

        request_ids = {item["candidate_identifier"] for item in request["requests"]}
        self.assertEqual(request_ids, resolution.EXTERNAL_DATA_CANDIDATES)
        for item in request["requests"]:
            self.assertEqual(item["paid_vendor_dataset"], "NOT_APPLICABLE_FOR_SETUP_LABELS")
            self.assertEqual(item["paid_vendor_schema"], "NOT_APPLICABLE_FOR_SETUP_LABELS")
            self.assertIn("complete only the named setup fields", item["smallest_valid_request"])

    def test_candidate_field_resolutions_name_sources_and_blocking_scope(self):
        document = resolution.build_resolution_document(
            source_commit="testsha",
            run_timestamp="2026-06-21T00:00:00Z",
        )

        for record in document["candidate_records"]:
            self.assertEqual(len(record["field_resolutions"]), len(resolution.REQUIRED_SETUP_FIELDS))
            for field in record["field_resolutions"]:
                self.assertIn(field["field_name"], resolution.REQUIRED_SETUP_FIELDS)
                self.assertTrue(field["primary_source"])
                self.assertTrue(field["fallback_source"])
                self.assertTrue(field["local_calculator_or_consumer"])
                self.assertTrue(field["timestamp_window"])
                self.assertIn(field["local_evidence_status"], {"present", "absent", "contradictory"})
                self.assertIn("1h RTH OHLCV", field["required_timestamp_resolution"])

    def test_file_writer_creates_day50_result(self):
        root = Path(__file__).resolve().parents[1]
        result_path = root / "historical_signal_replay" / "results" / "test_day50_resolution_tmp.json"
        try:
            written = resolution.write_resolution_document(
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
