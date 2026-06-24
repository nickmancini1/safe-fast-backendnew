import json
import unittest
from pathlib import Path

from historical_signal_replay import day52_replay_only_numeric_rule_candidates as candidates
from watcher_foundation import day52_replay_only_numeric_rule_candidates_validator as validator


class Day52ReplayOnlyNumericRuleCandidatesTests(unittest.TestCase):
    def _document(self, **kwargs):
        return candidates.build_replay_only_document(
            source_commit="testsha",
            run_timestamp="2026-06-23T00:00:00Z",
            **kwargs,
        )

    def _by_family(self, document):
        return {
            record["setup_family"]: record
            for record in document["setup_time_candidate_records"]
        }

    def test_actual_candidate_a_values_for_all_three_families(self):
        records = self._by_family(self._document())

        for family in ("Ideal", "Clean Fast Break", "Continuation"):
            record = records[family]
            self.assertEqual(record["candidate_rule_id"], "CANDIDATE_A_SETUP_BAR_RANGE")
            self.assertEqual(record["trigger"]["final_numeric_value"], "668.360000000")
            self.assertEqual(record["invalidation"]["final_numeric_value"], "667.870000000")
            self.assertEqual(record["trigger"]["source_field"], "high")
            self.assertEqual(record["invalidation"]["source_field"], "low")
            self.assertEqual(record["status"], "PROVISIONAL_REPLAY_ONLY")

    def test_candidate_b_and_c_structural_provenance_where_unavailable(self):
        records = self._by_family(self._document())

        self.assertEqual(
            {
                item["candidate_rule_id"]: item["missing_structural_field"]
                for item in records["Ideal"]["unavailable_higher_priority_candidates"]
            },
            {
                "CANDIDATE_B_SETUP_STRUCTURE_RANGE": "accepted_signal_or_setup_structure_boundary_field_missing",
                "CANDIDATE_C_NAMED_LEVEL": "explicit_named_level_field_missing",
            },
        )
        self.assertIn(
            "accepted_base_or_initial_break_structure_boundary_field_missing",
            [
                item["missing_structural_field"]
                for item in records["Clean Fast Break"]["unavailable_higher_priority_candidates"]
            ],
        )
        self.assertIn(
            "accepted_pullback_or_continuation_base_boundary_field_missing",
            [
                item["missing_structural_field"]
                for item in records["Continuation"]["unavailable_higher_priority_candidates"]
            ],
        )

    def test_bullish_and_bearish_calculations(self):
        row = {
            "ts_event": "2026-03-16T13:30:00.000000000Z",
            "publisher_id": "1",
            "instrument_id": "2",
            "open": "100",
            "high": "105",
            "low": "95",
            "close": "101",
            "volume": "10",
            "symbol": "SPY",
        }

        bullish = candidates.construct_candidate_pair(
            family="Ideal",
            row=row,
            direction="bullish",
            cutoff_utc="2026-03-16T13:30:00Z",
        )
        bearish = candidates.construct_candidate_pair(
            family="Ideal",
            row=row,
            direction="bearish",
            cutoff_utc="2026-03-16T13:30:00Z",
        )

        self.assertEqual(bullish["trigger"]["final_numeric_value"], "105")
        self.assertEqual(bullish["invalidation"]["final_numeric_value"], "95")
        self.assertEqual(bullish["trigger"]["comparison_operator"], ">=")
        self.assertEqual(bearish["trigger"]["final_numeric_value"], "95")
        self.assertEqual(bearish["invalidation"]["final_numeric_value"], "105")
        self.assertEqual(bearish["trigger"]["comparison_operator"], "<=")

    def test_future_row_rejection_and_post_cutoff_mutation_invariance(self):
        rows = candidates._read_source_rows(candidates.SOURCE_CSV_PATH)
        future = dict(rows[0])
        future["ts_event"] = "2026-03-16T13:31:00.000000000Z"

        rejected = candidates.construct_candidate_pair(
            family="Ideal",
            row=future,
            direction="bullish",
            cutoff_utc="2026-03-16T13:30:00Z",
        )
        self.assertEqual(rejected["blocked_reason"], "FUTURE_ROW_REJECTED")

        mutated = [dict(row) for row in rows]
        for row in mutated:
            if row["ts_event"] > "2026-03-16T13:30:00.000000000Z":
                row["high"] = "9999.000000000"
                row["low"] = "1.000000000"
        original = self._document(rows=rows)
        changed = self._document(rows=mutated)

        for original_record, changed_record in zip(
            original["setup_time_candidate_records"],
            changed["setup_time_candidate_records"],
        ):
            self.assertEqual(original_record["trigger"], changed_record["trigger"])
            self.assertEqual(original_record["invalidation"], changed_record["invalidation"])
            self.assertEqual(
                original_record["unavailable_higher_priority_candidates"],
                changed_record["unavailable_higher_priority_candidates"],
            )

    def test_finite_values_directional_validity_and_priority_independent_of_future_performance(self):
        document = self._document()

        for record in document["setup_time_candidate_records"]:
            self.assertTrue(record["finite_values"])
            self.assertTrue(record["directionally_valid"])
            self.assertFalse(record["selected_by_future_performance"])
            self.assertFalse(record["trigger_observation"]["outcome_used_to_select_candidate"])
            self.assertEqual(record["trigger_observation"]["which_occurred_first"], "trigger")

    def test_accepted_and_provisional_modes_remain_separate(self):
        document = self._document()
        accepted = document["accepted_mode_reference"]
        provisional = document["complete_session_opportunity_accounting"]

        self.assertEqual(accepted["numeric_values_established"], 6)
        self.assertEqual(accepted["numeric_values_unresolved"], 0)
        self.assertFalse(accepted["accepted_numeric_rules_remain_unresolved"])
        self.assertEqual(provisional["setup_qualified_under_provisional_mode_records"], 3)
        self.assertFalse(document["guardrails"]["accepted_blockers_overwritten"])

    def test_no_hindsight_review_strict_no_trade_stage_and_session_boundary_behavior(self):
        document = self._document()
        review = document["compact_setup_time_review"]
        session = document["provisional_manifest"]["sessions"][0]

        self.assertTrue(review["post_cutoff_fields_excluded"])
        for record in session["recognition_records"]:
            self.assertEqual(record["no_hindsight_cutoff"], record["observation_timestamp_utc"])
            self.assertFalse(record["stage_contract_predicates"]["illegal_stage_skipping_detected"])
            self.assertEqual(record["carry_forward_state"], "no_prior_session_carry_forward")
        self.assertEqual(session["coverage"]["start_timestamp_utc"], "2026-03-16T13:30:00Z")
        self.assertEqual(session["coverage"]["end_timestamp_utc"], "2026-03-16T19:59:00Z")
        self.assertEqual(session["strict_no_trade_behavior"]["trade_candidates"], 0)
        self.assertEqual(session["strict_no_trade_behavior"]["selected_contracts"], 0)

    def test_duplicate_suppression_stable_winner_selection_and_complete_session_accounting(self):
        document = self._document()
        accounting = document["complete_session_opportunity_accounting"]
        session = document["provisional_manifest"]["sessions"][0]

        self.assertEqual(accounting["sessions_scanned"], 1)
        self.assertEqual(accounting["rows_scanned"], 751)
        self.assertEqual(accounting["recognition_records"], 2253)
        self.assertEqual(accounting["duplicate_records"], 1083)
        self.assertEqual(accounting["setup_qualified_under_provisional_mode_records"], 3)
        self.assertEqual(accounting["selected_winner_records"], 1)
        self.assertEqual(accounting["suppressed_records"], 2)
        self.assertEqual(session["winner_selection"]["selected_winner_count"], 1)
        self.assertEqual(session["winner_selection"]["suppressed_count"], 2)

    def test_replay_chunking_candidate_order_and_deterministic_reruns(self):
        rows = candidates._read_source_rows(candidates.SOURCE_CSV_PATH)
        first = self._document(rows=rows)
        second = self._document(rows=list(reversed(rows)))
        chunked = self._document(rows=rows, chunk_size=11)
        reordered_candidates = self._document(
            rows=rows,
            candidate_rule_order=(
                "CANDIDATE_B_SETUP_STRUCTURE_RANGE",
                "CANDIDATE_C_NAMED_LEVEL",
                "CANDIDATE_A_SETUP_BAR_RANGE",
            ),
        )

        self.assertEqual(first["setup_time_candidate_records"], second["setup_time_candidate_records"])
        self.assertEqual(first["provisional_manifest"], chunked["provisional_manifest"])
        self.assertEqual(
            first["setup_time_candidate_records"],
            reordered_candidates["setup_time_candidate_records"],
        )
        self.assertEqual(first["determinism_protection"]["result"], "PASS")

    def test_writer_and_validator_accept_result(self):
        root = Path(__file__).resolve().parents[1]
        result_path = root / "historical_signal_replay" / "results" / "test_day52_candidates.json"
        manifest_path = root / "historical_signal_replay" / "results" / "test_day52_candidates_manifest.json"
        review_path = root / "historical_signal_replay" / "results" / "test_day52_candidates_review.json"
        doc_path = root / "test_day52_candidates.md"
        original = (
            candidates.RESULT_PATH,
            candidates.MANIFEST_PATH,
            candidates.REVIEW_PATH,
            candidates.RESULT_DOC_PATH,
        )
        try:
            candidates.RESULT_PATH = result_path
            candidates.MANIFEST_PATH = manifest_path
            candidates.REVIEW_PATH = review_path
            candidates.RESULT_DOC_PATH = doc_path
            written = candidates.write_outputs(
                source_commit="testsha",
                run_timestamp="2026-06-23T00:00:00Z",
            )
            loaded = json.loads(result_path.read_text(encoding="utf-8"))
            validation = validator.validate_result_document(result_path)
        finally:
            (
                candidates.RESULT_PATH,
                candidates.MANIFEST_PATH,
                candidates.REVIEW_PATH,
                candidates.RESULT_DOC_PATH,
            ) = original
            for path in (result_path, manifest_path, review_path, doc_path):
                if path.exists():
                    path.unlink()

        self.assertEqual(written, loaded)
        self.assertEqual(validation["status"], "PASS")
        self.assertEqual(validation["problems"], [])


if __name__ == "__main__":
    unittest.main()
