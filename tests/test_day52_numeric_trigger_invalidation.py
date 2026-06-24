import json
import unittest
from pathlib import Path

from historical_signal_replay import day52_numeric_trigger_invalidation as numeric
from watcher_foundation import day52_numeric_trigger_invalidation_validator as validator


class Day52NumericTriggerInvalidationTests(unittest.TestCase):
    def _document(self, **kwargs):
        return numeric.build_numeric_trigger_invalidation_document(
            source_commit="testsha",
            run_timestamp="2026-06-23T00:00:00Z",
            **kwargs,
        )

    def test_family_specific_candidate_a_is_promoted(self):
        document = self._document()

        self.assertEqual(document["summary"]["numeric_values_established"], 6)
        self.assertEqual(document["summary"]["numeric_values_unresolved"], 0)
        for constructor in document["numeric_constructors"]:
            self.assertEqual(constructor["promotion_decision"], "PROMOTE_CANDIDATE_A")
            self.assertEqual(constructor["accepted_status"], "ACCEPTED")
            self.assertTrue(constructor["setup_qualified_allowed"])
            self.assertEqual(constructor["trigger"]["numeric_value"], "668.360000000")
            self.assertEqual(constructor["trigger"]["source_field"], "high")
            self.assertEqual(constructor["trigger"]["comparison_operator"], ">=")
            self.assertEqual(constructor["invalidation"]["numeric_value"], "667.870000000")
            self.assertEqual(constructor["invalidation"]["source_field"], "low")
            self.assertEqual(constructor["invalidation"]["comparison_operator"], "<=")

    def test_binding_audit_proves_legitimate_shared_row(self):
        document = self._document()

        self.assertEqual(
            {item["family"] for item in document["binding_audit"]},
            {"Ideal", "Clean Fast Break", "Continuation"},
        )
        for item in document["binding_audit"]:
            self.assertEqual(item["expected_opportunity_timestamp"], "2026-03-16T13:30:00Z")
            self.assertEqual(item["actual_bound_setup_time_timestamp"], "2026-03-16T13:30:00Z")
            self.assertEqual(item["source_row_index"], 2)
            self.assertEqual(item["source_row"]["publisher_id"], "39")
            self.assertEqual(item["source_row"]["high"], "668.360000000")
            self.assertEqual(item["source_row"]["low"], "667.870000000")
            self.assertEqual(item["binding_result"], "LEGITIMATE_SHARED_SETUP_TIME_ROW")

    def test_future_row_rejection(self):
        rows = numeric._read_source_rows(numeric.SOURCE_CSV_PATH)
        future_row = dict(rows[0])
        future_row["ts_event"] = "2026-03-16T13:31:00.000000000Z"

        constructor = numeric.construct_family_numeric_fields(
            family="Ideal",
            rows=[rows[0], future_row],
            cutoff_utc="2026-03-16T13:30:00Z",
        )

        self.assertEqual(
            constructor["trigger"]["blocker_code"],
            "NUMERIC_FUTURE_ROW_REJECTED_IDEAL_TRIGGER",
        )
        self.assertFalse(constructor["setup_qualified_allowed"])

    def test_post_cutoff_mutation_does_not_change_accepted_values(self):
        rows = numeric._read_source_rows(numeric.SOURCE_CSV_PATH)
        mutated = [dict(row) for row in rows]
        for row in mutated:
            if row["ts_event"] > "2026-03-16T13:30:00.000000000Z":
                row["high"] = "9999.000000000"
                row["low"] = "1.000000000"

        original = self._document(rows=rows)
        changed = self._document(rows=mutated)

        self.assertEqual(original["numeric_constructors"], changed["numeric_constructors"])

    def test_input_order_and_deterministic_comparison_pass(self):
        rows = numeric._read_source_rows(numeric.SOURCE_CSV_PATH)
        first = self._document(rows=rows)
        second = self._document(rows=list(reversed(rows)))

        self.assertEqual(first["numeric_constructors"], second["numeric_constructors"])
        self.assertEqual(first["deterministic_comparison"]["result"], "PASS")

    def test_writer_and_validator_accept_numeric_result(self):
        root = Path(__file__).resolve().parents[1]
        result_path = root / "historical_signal_replay" / "results" / "test_day52_numeric.json"
        doc_path = root / "test_day52_numeric.md"
        original_result = numeric.RESULT_PATH
        original_doc = numeric.RESULT_DOC_PATH
        try:
            numeric.RESULT_PATH = result_path
            numeric.RESULT_DOC_PATH = doc_path
            written = numeric.write_outputs(
                source_commit="testsha",
                run_timestamp="2026-06-23T00:00:00Z",
            )
            loaded = json.loads(result_path.read_text(encoding="utf-8"))
            validation = validator.validate_result_document(result_path)
        finally:
            numeric.RESULT_PATH = original_result
            numeric.RESULT_DOC_PATH = original_doc
            for path in (result_path, doc_path):
                if path.exists():
                    path.unlink()

        self.assertEqual(written, loaded)
        self.assertEqual(validation["status"], "PASS")
        self.assertEqual(validation["problems"], [])


if __name__ == "__main__":
    unittest.main()
