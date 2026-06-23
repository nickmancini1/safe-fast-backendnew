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

    def test_ideal_full_session_recognition_is_accounted(self):
        document = self._document()
        counts = document["sessions"][0]["counts_by_setup_family_and_final_disposition"]["Ideal"]

        self.assertEqual(counts["rejected"], 389)
        self.assertEqual(counts["duplicate"], 361)
        self.assertEqual(counts["blocked by missing evidence"], 1)
        self.assertEqual(counts["setup-qualified"], 0)

    def test_clean_fast_break_full_session_recognition_is_accounted(self):
        document = self._document()
        counts = document["sessions"][0]["counts_by_setup_family_and_final_disposition"][
            "Clean Fast Break"
        ]

        self.assertEqual(counts["rejected"], 389)
        self.assertEqual(counts["duplicate"], 361)
        self.assertEqual(counts["blocked by missing evidence"], 1)
        self.assertEqual(counts["selected winner"], 0)

    def test_continuation_full_session_recognition_is_accounted(self):
        document = self._document()
        counts = document["sessions"][0]["counts_by_setup_family_and_final_disposition"][
            "Continuation"
        ]

        self.assertEqual(counts["rejected"], 389)
        self.assertEqual(counts["duplicate"], 361)
        self.assertEqual(counts["blocked by missing evidence"], 1)
        self.assertEqual(counts["suppressed"], 0)

    def test_complete_session_opportunity_accounting(self):
        document = self._document()
        accounting = document["complete_session_accounting"]

        self.assertEqual(accounting["sessions_scanned"], 1)
        self.assertEqual(accounting["rows_scanned"], 751)
        self.assertEqual(accounting["recognition_records"], 2253)
        self.assertEqual(accounting["primary_timestamp_family_records"], 1170)
        self.assertEqual(accounting["duplicate_records"], 1083)
        self.assertEqual(accounting["rejected_records"], 1167)
        self.assertEqual(accounting["blocked_missing_evidence_records"], 3)

    def test_numeric_trigger_invalidation_reference_is_exact(self):
        document = self._document()
        summary = document["numeric_trigger_invalidation_reference"]["summary"]

        self.assertEqual(summary["numeric_values_established"], 0)
        self.assertEqual(summary["numeric_values_unresolved"], 6)
        self.assertEqual(summary["setup_qualified_allowed_count"], 0)
        self.assertEqual(
            summary["by_family"]["Clean Fast Break"]["blockers"]["trigger"],
            "NUMERIC_RULE_UNRESOLVED_CLEAN_FAST_BREAK_TRIGGER",
        )

    def test_known_window_versus_complete_session_bias_exposure(self):
        document = self._document()
        bias = document["known_window_bias_exposure"]

        self.assertTrue(bias["bias_exposed"])
        self.assertEqual(bias["known_window_primary_records"], 3)
        self.assertEqual(bias["complete_session_primary_records"], 1170)
        self.assertEqual(bias["known_window_only_would_omit_primary_records"], 1167)
        self.assertTrue(bias["known_window_records_all_blocked_by_missing_numeric_evidence"])

    def test_legal_stage_transitions_are_recorded_without_skipping(self):
        document = self._document()

        for record in self._records(document):
            self.assertFalse(
                record["stage_contract_predicates"]["illegal_stage_skipping_detected"]
            )
            observed_stages = [
                item["stage"] for item in record["stage_transition_history"]
            ]
            self.assertEqual(observed_stages[0], "observed")
            self.assertEqual(observed_stages[1], "developing")

    def test_illegal_stage_skipping_fails_validation(self):
        document = self._document()
        document["sessions"][0]["recognition_records"][0]["stage_contract_predicates"][
            "illegal_stage_skipping_detected"
        ] = True
        path = Path(__file__).resolve().parents[1] / "historical_signal_replay" / "results" / "test_day52_illegal.json"
        try:
            path.write_text(json.dumps(document, indent=2), encoding="utf-8")
            result = validator.validate_result_document(path)
        finally:
            if path.exists():
                path.unlink()

        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("illegal" in problem for problem in result["problems"]))

    def test_exact_blocker_and_rejection_codes_are_stable(self):
        document = self._document()
        records = self._records(document)
        reason_codes = {record["exact_rejection_or_blocker_code"] for record in records}

        self.assertEqual(
            reason_codes,
            {
                "no_accepted_setup_signal_at_timestamp",
                "NUMERIC_RULE_UNRESOLVED_IDEAL_TRIGGER__NUMERIC_RULE_UNRESOLVED_IDEAL_INVALIDATION",
                "NUMERIC_RULE_UNRESOLVED_CLEAN_FAST_BREAK_TRIGGER__NUMERIC_RULE_UNRESOLVED_CLEAN_FAST_BREAK_INVALIDATION",
                "NUMERIC_RULE_UNRESOLVED_CONTINUATION_TRIGGER__NUMERIC_RULE_UNRESOLVED_CONTINUATION_INVALIDATION",
                "duplicate_same_timestamp_publisher_row",
            },
        )

    def test_no_hindsight_cutoffs_equal_observation_time(self):
        document = self._document()

        for record in self._records(document):
            self.assertEqual(record["no_hindsight_cutoff"], record["observation_timestamp_utc"])
            for transition in record["stage_transition_history"]:
                self.assertLessEqual(
                    transition["information_cutoff_utc"],
                    record["observation_timestamp_utc"],
                )

    def test_setup_time_review_excludes_future_and_economic_fields(self):
        document = self._document()
        review = document["setup_time_review_output"]

        self.assertTrue(review["post_cutoff_fields_excluded"])
        self.assertEqual(len(review["records"]), 3)
        forbidden = {
            "future_high",
            "future_low",
            "later_favorable_move",
            "selected_contract",
            "entry",
            "exit",
            "pnl",
            "net_pnl",
        }
        for record in review["records"]:
            self.assertTrue(record["post_cutoff_fields_excluded"])
            self.assertFalse(forbidden.intersection(record))

    def test_session_boundary_behavior(self):
        document = self._document()
        session = document["sessions"][0]

        self.assertEqual(session["coverage"]["start_timestamp_utc"], "2026-03-16T13:30:00Z")
        self.assertEqual(session["coverage"]["end_timestamp_utc"], "2026-03-16T19:59:00Z")
        self.assertTrue(session["coverage"]["complete_expected_rth_minute_coverage"])
        self.assertEqual(session["coverage"]["missing_intervals"], [])

    def test_carry_forward_behavior(self):
        document = self._document()

        self.assertTrue(
            all(
                record["carry_forward_state"] == "no_prior_session_carry_forward"
                for record in self._records(document)
            )
        )

    def test_stale_and_spent_behavior_remains_unpromoted(self):
        document = self._document()

        self.assertEqual(
            document["complete_session_accounting"]["blocked_missing_evidence_records"],
            3,
        )
        self.assertFalse(
            any(record["final_disposition"] == "setup-qualified" for record in self._records(document))
        )

    def test_duplicate_grouping(self):
        document = self._document()
        records = self._records(document)
        duplicates = [record for record in records if record["final_disposition"] == "duplicate"]

        self.assertEqual(len(duplicates), 1083)
        self.assertTrue(all(record["duplicate_sequence"] > 0 for record in duplicates))
        self.assertTrue(all(record["suppression_reason"] == "duplicate_same_timestamp_publisher_row" for record in duplicates))

    def test_deterministic_suppression(self):
        document = self._document()
        duplicates = [record for record in self._records(document) if record["final_disposition"] == "duplicate"]

        self.assertEqual(
            {record["exact_rejection_or_blocker_code"] for record in duplicates},
            {"duplicate_same_timestamp_publisher_row"},
        )

    def test_stable_winner_selection_has_no_eligible_winner(self):
        document = self._document()
        winner = document["sessions"][0]["winner_selection"]

        self.assertEqual(winner["selected_winner_count"], 0)
        self.assertEqual(winner["stable_rule_result"], "NO_ELIGIBLE_SETUP_QUALIFIED_WINNER")
        self.assertTrue(winner["stable_rule_executed"])

    def test_strict_no_trade_behavior(self):
        document = self._document()
        no_trade = document["sessions"][0]["strict_no_trade_behavior"]

        self.assertEqual(no_trade["trade_candidates"], 0)
        self.assertEqual(no_trade["selected_contracts"], 0)
        self.assertEqual(no_trade["entries"], 0)
        self.assertEqual(no_trade["orders"], 0)

    def test_missing_evidence_blocks_advancement(self):
        document = self._document()
        blocked = [
            record for record in self._records(document)
            if record["final_disposition"] == "blocked by missing evidence"
        ]

        self.assertEqual(len(blocked), 3)
        for record in blocked:
            self.assertEqual(record["missing_required_evidence"], ["numeric_trigger", "numeric_invalidation"])
            self.assertIsNone(record["trigger"]["numeric_value"])
            self.assertIsNone(record["invalidation"]["numeric_value"])
            self.assertTrue(record["trigger"]["blocker_code"].startswith("NUMERIC_RULE_UNRESOLVED_"))
            self.assertTrue(record["invalidation"]["blocker_code"].startswith("NUMERIC_RULE_UNRESOLVED_"))
            self.assertFalse(record["stage_contract_predicates"]["setup_qualified_predicate_passed"])

    def test_repeated_run_determinism(self):
        first = self._document()
        second = self._document()

        self.assertEqual(first["sessions"], second["sessions"])
        self.assertEqual(first["setup_time_review_output"], second["setup_time_review_output"])
        self.assertEqual(first["determinism_protection"]["result"], "PASS")

    def test_replay_chunking_invariance(self):
        full = self._document()
        chunked = self._document(chunk_size=7)

        self.assertEqual(full["sessions"], chunked["sessions"])
        self.assertEqual(full["setup_time_review_output"], chunked["setup_time_review_output"])

    def test_candidate_input_order_invariance(self):
        rows = day52._read_source_rows(day52.SOURCE_CSV_PATH)
        normal = self._document(rows=rows)
        reversed_order = self._document(rows=list(reversed(rows)))

        self.assertEqual(normal["sessions"], reversed_order["sessions"])
        self.assertEqual(normal["setup_time_review_output"], reversed_order["setup_time_review_output"])

    def test_writer_and_validator_accept_manifest(self):
        root = Path(__file__).resolve().parents[1]
        result_path = root / "historical_signal_replay" / "results" / "test_day52_manifest.json"
        review_path = root / "historical_signal_replay" / "results" / "test_day52_review.json"
        doc_path = root / "test_day52_result.md"
        numeric_path = root / "historical_signal_replay" / "results" / "test_day52_numeric_sidecar.json"
        numeric_doc_path = root / "test_day52_numeric_sidecar.md"
        original_result = day52.RESULT_PATH
        original_review = day52.REVIEW_PATH
        original_doc = day52.RESULT_DOC_PATH
        original_numeric = day52.NUMERIC_RESULT_PATH
        original_numeric_doc = day52.NUMERIC_RESULT_DOC_PATH
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
            day52.RESULT_PATH = original_result
            day52.REVIEW_PATH = original_review
            day52.RESULT_DOC_PATH = original_doc
            day52.NUMERIC_RESULT_PATH = original_numeric
            day52.NUMERIC_RESULT_DOC_PATH = original_numeric_doc
            for path in (result_path, review_path, doc_path, numeric_path, numeric_doc_path):
                if path.exists():
                    path.unlink()

        self.assertEqual(written, loaded)
        self.assertEqual(validation["status"], "PASS")
        self.assertEqual(validation["problems"], [])


if __name__ == "__main__":
    unittest.main()
