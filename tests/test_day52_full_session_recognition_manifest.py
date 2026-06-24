import json
import unittest
from pathlib import Path

from historical_signal_replay import day52_full_session_recognition_manifest as day52
from watcher_foundation import day52_full_session_recognition_manifest_validator as validator


class Day52FullSessionRecognitionManifestTests(unittest.TestCase):
    def _document(self, **kwargs):
        return day52.build_manifest_document(
            source_commit="testsha",
            run_timestamp="2026-06-23T00:00:00Z",
            **kwargs,
        )

    def _records(self, document):
        return document["sessions"][0]["recognition_records"]

    def test_full_session_accepted_mode_counts(self):
        document = self._document()
        accounting = document["complete_session_accounting"]

        self.assertEqual(accounting["sessions_scanned"], 1)
        self.assertEqual(accounting["rows_scanned"], 751)
        self.assertEqual(accounting["recognition_records"], 2253)
        self.assertEqual(accounting["primary_timestamp_family_records"], 1170)
        self.assertEqual(accounting["duplicate_records"], 1083)
        self.assertEqual(accounting["rejected_records"], 1167)
        self.assertEqual(accounting["blocked_missing_evidence_records"], 0)
        self.assertEqual(accounting["setup_qualified_records"], 3)
        self.assertEqual(accounting["selected_winner_records"], 1)
        self.assertEqual(accounting["suppressed_records"], 2)
        self.assertEqual(accounting["trade_candidates"], 0)

    def test_family_counts_and_stable_winner_selection(self):
        document = self._document()
        counts = document["sessions"][0]["counts_by_setup_family_and_final_disposition"]

        for family in ("Ideal", "Clean Fast Break", "Continuation"):
            self.assertEqual(counts[family]["rejected"], 389)
            self.assertEqual(counts[family]["duplicate"], 361)
            self.assertEqual(counts[family]["blocked by missing evidence"], 0)
        self.assertEqual(counts["Clean Fast Break"]["selected winner"], 1)
        self.assertEqual(counts["Ideal"]["suppressed"], 1)
        self.assertEqual(counts["Continuation"]["suppressed"], 1)

        winner = document["sessions"][0]["winner_selection"]
        self.assertEqual(winner["selected_winner_count"], 1)
        self.assertEqual(winner["suppressed_count"], 2)
        self.assertEqual(winner["stable_rule_result"], "ACCEPTED_LAYER1_WINNER_SELECTED")

    def test_primary_setup_records_have_accepted_numeric_values(self):
        document = self._document()
        records = [
            record
            for record in self._records(document)
            if record["observation_timestamp_utc"] == "2026-03-16T13:30:00Z"
            and record["duplicate_sequence"] == 0
        ]

        self.assertEqual(len(records), 3)
        for record in records:
            self.assertTrue(record["stage_contract_predicates"]["setup_qualified_predicate_passed"])
            self.assertEqual(record["missing_required_evidence"], [])
            self.assertEqual(record["trigger"]["numeric_value"], "668.360000000")
            self.assertEqual(record["invalidation"]["numeric_value"], "667.870000000")
            stages = [item["stage"] for item in record["stage_transition_history"]]
            self.assertEqual(stages[:4], ["observed", "developing", "setup_time_fields", "setup_qualified"])

    def test_no_hindsight_session_boundary_carry_forward_and_no_trade(self):
        document = self._document()
        session = document["sessions"][0]

        self.assertEqual(session["coverage"]["start_timestamp_utc"], "2026-03-16T13:30:00Z")
        self.assertEqual(session["coverage"]["end_timestamp_utc"], "2026-03-16T19:59:00Z")
        self.assertEqual(session["coverage"]["missing_intervals"], [])
        self.assertEqual(session["strict_no_trade_behavior"]["trade_candidates"], 0)
        self.assertEqual(session["strict_no_trade_behavior"]["selected_contracts"], 0)
        for record in self._records(document):
            self.assertEqual(record["no_hindsight_cutoff"], record["observation_timestamp_utc"])
            self.assertEqual(record["carry_forward_state"], "no_prior_session_carry_forward")
            self.assertFalse(record["stage_contract_predicates"]["illegal_stage_skipping_detected"])

    def test_duplicate_suppression_remains_deterministic(self):
        document = self._document()
        duplicates = [record for record in self._records(document) if record["final_disposition"] == "duplicate"]

        self.assertEqual(len(duplicates), 1083)
        self.assertTrue(all(record["duplicate_sequence"] > 0 for record in duplicates))
        self.assertEqual(
            {record["exact_rejection_or_blocker_code"] for record in duplicates},
            {"duplicate_same_timestamp_publisher_row"},
        )

    def test_replay_chunking_candidate_order_and_reruns_are_deterministic(self):
        rows = day52._read_source_rows(day52.SOURCE_CSV_PATH)
        normal = self._document(rows=rows)
        reversed_order = self._document(rows=list(reversed(rows)))
        chunked = self._document(rows=rows, chunk_size=7)

        self.assertEqual(normal["sessions"], reversed_order["sessions"])
        self.assertEqual(normal["sessions"], chunked["sessions"])
        self.assertEqual(normal["determinism_protection"]["result"], "PASS")

    def test_writer_and_validator_accept_manifest(self):
        root = Path(__file__).resolve().parents[1]
        result_path = root / "historical_signal_replay" / "results" / "test_day52_manifest.json"
        review_path = root / "historical_signal_replay" / "results" / "test_day52_review.json"
        doc_path = root / "test_day52_result.md"
        numeric_path = root / "historical_signal_replay" / "results" / "test_day52_numeric_sidecar.json"
        numeric_doc_path = root / "test_day52_numeric_sidecar.md"
        original = (
            day52.RESULT_PATH,
            day52.REVIEW_PATH,
            day52.RESULT_DOC_PATH,
            day52.NUMERIC_RESULT_PATH,
            day52.NUMERIC_RESULT_DOC_PATH,
        )
        try:
            day52.RESULT_PATH = result_path
            day52.REVIEW_PATH = review_path
            day52.RESULT_DOC_PATH = doc_path
            day52.NUMERIC_RESULT_PATH = numeric_path
            day52.NUMERIC_RESULT_DOC_PATH = numeric_doc_path
            written = day52.write_outputs(
                source_commit="testsha",
                run_timestamp="2026-06-23T00:00:00Z",
            )
            loaded = json.loads(result_path.read_text(encoding="utf-8"))
            validation = validator.validate_result_document(result_path)
        finally:
            (
                day52.RESULT_PATH,
                day52.REVIEW_PATH,
                day52.RESULT_DOC_PATH,
                day52.NUMERIC_RESULT_PATH,
                day52.NUMERIC_RESULT_DOC_PATH,
            ) = original
            for path in (result_path, review_path, doc_path, numeric_path, numeric_doc_path):
                if path.exists():
                    path.unlink()

        self.assertEqual(written, loaded)
        self.assertEqual(validation["status"], "PASS")
        self.assertEqual(validation["problems"], [])


if __name__ == "__main__":
    unittest.main()
