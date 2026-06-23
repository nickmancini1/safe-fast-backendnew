import json
import unittest
from pathlib import Path

from historical_signal_replay import day52_full_session_recognition_manifest as day52
from historical_signal_replay import day52_numeric_trigger_invalidation as numeric
from watcher_foundation import day52_numeric_trigger_invalidation_validator as validator


class Day52NumericTriggerInvalidationTests(unittest.TestCase):
    def _document(self, **kwargs):
        return numeric.build_numeric_trigger_invalidation_document(
            source_commit="testsha",
            run_timestamp="2026-06-23T00:00:00Z",
            **kwargs,
        )

    def _constructor(self, family):
        rows = numeric._read_source_rows(numeric.SOURCE_CSV_PATH)
        setup_rows = [
            row for row in rows if row["ts_event"] == "2026-03-16T13:30:00.000000000Z"
        ]
        return numeric.construct_family_numeric_fields(
            family=family,
            rows=setup_rows,
            cutoff_utc="2026-03-16T13:30:00Z",
        )

    def test_exact_ideal_trigger_and_invalidation_blockers(self):
        constructor = self._constructor("Ideal")

        self.assertEqual(
            constructor["trigger"]["blocker_code"],
            "NUMERIC_RULE_UNRESOLVED_IDEAL_TRIGGER",
        )
        self.assertEqual(
            constructor["invalidation"]["blocker_code"],
            "NUMERIC_RULE_UNRESOLVED_IDEAL_INVALIDATION",
        )
        self.assertIsNone(constructor["trigger"]["numeric_value"])
        self.assertIsNone(constructor["invalidation"]["numeric_value"])

    def test_exact_clean_fast_break_trigger_and_invalidation_blockers(self):
        constructor = self._constructor("Clean Fast Break")

        self.assertEqual(
            constructor["trigger"]["blocker_code"],
            "NUMERIC_RULE_UNRESOLVED_CLEAN_FAST_BREAK_TRIGGER",
        )
        self.assertEqual(
            constructor["invalidation"]["blocker_code"],
            "NUMERIC_RULE_UNRESOLVED_CLEAN_FAST_BREAK_INVALIDATION",
        )

    def test_exact_continuation_trigger_and_invalidation_blockers(self):
        constructor = self._constructor("Continuation")

        self.assertEqual(
            constructor["trigger"]["blocker_code"],
            "NUMERIC_RULE_UNRESOLVED_CONTINUATION_TRIGGER",
        )
        self.assertEqual(
            constructor["invalidation"]["blocker_code"],
            "NUMERIC_RULE_UNRESOLVED_CONTINUATION_INVALIDATION",
        )

    def test_source_rule_provenance_is_preserved(self):
        constructor = self._constructor("Clean Fast Break")
        trigger = constructor["trigger"]

        self.assertEqual(
            trigger["rule_identifier"],
            "day50_bounded_accepted_setup_replay_mapper_v1.frozen_family_trigger_contract",
        )
        self.assertEqual(trigger["source_bar_timestamp"], "2026-03-16T13:30:00Z")
        self.assertIn("high", trigger["observable_ohlcv_fields"])
        self.assertIn("does not bind", trigger["calculation"])
        self.assertEqual(trigger["source_file"], numeric.SOURCE_CSV_RELATIVE)

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

    def test_post_cutoff_mutation_does_not_change_setup_values(self):
        rows = numeric._read_source_rows(numeric.SOURCE_CSV_PATH)
        mutated = [dict(row) for row in rows]
        for row in mutated:
            if row["ts_event"] > "2026-03-16T13:30:00.000000000Z":
                row["high"] = "9999.000000000"
                row["low"] = "1.000000000"

        original = self._document(rows=rows)
        changed = self._document(rows=mutated)

        self.assertEqual(original["numeric_constructors"], changed["numeric_constructors"])

    def test_missing_source_field_blocker(self):
        rows = numeric._read_source_rows(numeric.SOURCE_CSV_PATH)
        setup_row = dict(rows[0])
        setup_row["high"] = ""

        constructor = numeric.construct_family_numeric_fields(
            family="Continuation",
            rows=[setup_row],
            cutoff_utc="2026-03-16T13:30:00Z",
        )

        self.assertEqual(
            constructor["trigger"]["blocker_code"],
            "NUMERIC_SOURCE_FIELD_MISSING_CONTINUATION_TRIGGER",
        )
        self.assertIn("high", constructor["trigger"]["missing_source_fields"])

    def test_ambiguous_evidence_blocker(self):
        rows = numeric._read_source_rows(numeric.SOURCE_CSV_PATH)
        row_a = dict(rows[0])
        row_b = dict(rows[0])
        row_b["close"] = "669.000000000"

        constructor = numeric.construct_family_numeric_fields(
            family="Clean Fast Break",
            rows=[row_a, row_b],
            cutoff_utc="2026-03-16T13:30:00Z",
        )

        self.assertEqual(
            constructor["invalidation"]["blocker_code"],
            "NUMERIC_AMBIGUOUS_EVIDENCE_CLEAN_FAST_BREAK_INVALIDATION",
        )

    def test_finite_numeric_and_directional_relationship_are_not_invented(self):
        document = self._document()

        for constructor in document["numeric_constructors"]:
            self.assertFalse(constructor["trigger"]["finite_numeric_value"])
            self.assertFalse(constructor["invalidation"]["finite_numeric_value"])
            self.assertFalse(constructor["trigger"]["directionally_valid"])
            self.assertFalse(constructor["invalidation"]["directionally_valid"])

    def test_full_session_stage_boundaries_stay_blocked_and_no_trade(self):
        document = day52.build_manifest_document(
            source_commit="testsha",
            run_timestamp="2026-06-23T00:00:00Z",
        )
        session = document["sessions"][0]

        for family_counts in session["counts_by_setup_family_and_final_disposition"].values():
            self.assertEqual(family_counts["setup-qualified"], 0)
            self.assertEqual(family_counts["blocked by missing evidence"], 1)
        self.assertEqual(session["winner_selection"]["selected_winner_count"], 0)
        self.assertEqual(session["strict_no_trade_behavior"]["trade_candidates"], 0)

    def test_replay_chunking_candidate_order_and_reruns_are_deterministic(self):
        rows = numeric._read_source_rows(numeric.SOURCE_CSV_PATH)
        first = self._document(rows=rows)
        second = self._document(rows=list(reversed(rows)))
        chunked = day52.build_manifest_document(
            source_commit="testsha",
            run_timestamp="2026-06-23T00:00:00Z",
            rows=rows,
            chunk_size=11,
        )

        self.assertEqual(first["numeric_constructors"], second["numeric_constructors"])
        self.assertEqual(chunked["determinism_protection"]["result"], "PASS")
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
