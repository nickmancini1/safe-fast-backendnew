import copy
import unittest

from watcher_foundation.replacement_source_row_setup_time_review import (
    REPLACEMENT_SOURCE_ROW_SETUP_TIME_REVIEW_RESULT_FIELDS,
    review_replacement_source_row_setup_time,
    review_replacement_source_row_setup_time_batch,
)


def extracted_bundle(candidate_id="GLD-REPLACEMENT-IDEAL-CANDIDATE-001"):
    symbol = "IWM" if candidate_id.startswith("IWM") else "GLD"
    setup_type = "Continuation" if symbol == "IWM" else "Ideal"
    return {
        "candidate_id": candidate_id,
        "symbol": symbol,
        "setup_type": setup_type,
        "source_window_id": f"{symbol}-WINDOW-001",
        "source_sample_id": f"{symbol}-SAMPLE-001",
        "source_file_label": f"local_{symbol.lower()}_1h_rth_export.csv",
        "source_rows": [
            row(10, "2026-05-06T13:30:00-04:00"),
            row(11, "2026-05-06T14:30:00-04:00"),
            row(12, "2026-05-06T15:30:00-04:00"),
        ],
    }


def row(source_row_number, timestamp):
    return {
        "source_row_number": source_row_number,
        "timestamp": timestamp,
        "open": 430.0,
        "high": 435.0,
        "low": 429.0,
        "close": 434.0,
        "volume": 100000,
    }


def setup_review(candidate_id="GLD-REPLACEMENT-IDEAL-CANDIDATE-001"):
    symbol = "IWM" if candidate_id.startswith("IWM") else "GLD"
    setup_type = "Continuation" if symbol == "IWM" else "Ideal"
    return {
        "candidate_id": candidate_id,
        "symbol": symbol,
        "setup_type": setup_type,
        "setup_time_source_row_number": 11,
        "setup_time_timestamp": "2026-05-06T14:30:00-04:00",
        "setup_time_row_ohlcv": {
            "open": 430.0,
            "high": 435.0,
            "low": 429.0,
            "close": 434.0,
            "volume": 100000,
        },
        "accepted_setup_identity": f"{symbol} {setup_type} setup-time identity accepted for review",
        "accepted_final_verdict": "accepted for packet-build review only",
        "accepted_trigger_state": "trigger defined at setup time",
        "accepted_numeric_trigger": 435.0,
        "accepted_trigger_basis": "setup-time recovery hold",
        "accepted_numeric_invalidation": 429.0,
        "accepted_invalidation_basis": "setup-time low",
        "accepted_freshness_final_signal_decision": "fresh setup-time signal",
        "accepted_blocker_caution_decision": "no primary blocker",
        "no_hindsight_boundary_statement": "setup-time row selected before outcome review",
        "after_setup_outcome_window_start": 12,
        "after_setup_outcome_window_end": 14,
    }


class ReplacementSourceRowSetupTimeReviewTests(unittest.TestCase):
    def test_valid_gld_setup_time_review_becomes_ready_but_not_accepted_proof(self):
        result = review_replacement_source_row_setup_time(
            extracted_bundle("GLD-REPLACEMENT-IDEAL-CANDIDATE-001"),
            setup_review("GLD-REPLACEMENT-IDEAL-CANDIDATE-001"),
        )

        self.assertEqual(result["setup_time_review_status"], "ready_for_packet_build_review")
        self.assertEqual(result["symbol"], "GLD")
        self.assertEqual(result["setup_type"], "Ideal")
        self.assertEqual(result["old_source_window_id"], "GLD-WINDOW-001")
        self.assertEqual(result["old_source_sample_id"], "GLD-SAMPLE-001")
        self.assertEqual(result["missing_evidence"], [])
        self.assertFalse(result["accepted_proof"])
        for field_name in REPLACEMENT_SOURCE_ROW_SETUP_TIME_REVIEW_RESULT_FIELDS:
            self.assertIn(field_name, result)

    def test_valid_iwm_setup_time_review_becomes_ready_but_not_accepted_proof(self):
        result = review_replacement_source_row_setup_time(
            extracted_bundle("IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001"),
            setup_review("IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001"),
        )

        self.assertEqual(result["setup_time_review_status"], "ready_for_packet_build_review")
        self.assertEqual(result["symbol"], "IWM")
        self.assertEqual(result["setup_type"], "Continuation")
        self.assertFalse(result["accepted_proof"])

    def test_missing_trigger_fields_remain_blocked_missing_evidence(self):
        review = setup_review()
        review.pop("accepted_trigger_state")
        review.pop("accepted_numeric_trigger")
        review.pop("accepted_trigger_basis")

        result = review_replacement_source_row_setup_time(extracted_bundle(), review)

        self.assertEqual(result["setup_time_review_status"], "blocked_missing_evidence")
        self.assertIn("accepted_trigger_state", result["missing_evidence"])
        self.assertIn("accepted_numeric_trigger", result["missing_evidence"])
        self.assertIn("accepted_trigger_basis", result["missing_evidence"])
        self.assertFalse(result["accepted_proof"])

    def test_missing_invalidation_fields_remain_blocked_missing_evidence(self):
        review = setup_review()
        review.pop("accepted_numeric_invalidation")
        review.pop("accepted_invalidation_basis")

        result = review_replacement_source_row_setup_time(extracted_bundle(), review)

        self.assertEqual(result["setup_time_review_status"], "blocked_missing_evidence")
        self.assertIn("accepted_numeric_invalidation", result["missing_evidence"])
        self.assertIn("accepted_invalidation_basis", result["missing_evidence"])
        self.assertFalse(result["accepted_proof"])

    def test_missing_freshness_blocker_fields_remain_blocked_missing_evidence(self):
        review = setup_review()
        review.pop("accepted_freshness_final_signal_decision")
        review.pop("accepted_blocker_caution_decision")

        result = review_replacement_source_row_setup_time(extracted_bundle(), review)

        self.assertEqual(result["setup_time_review_status"], "blocked_missing_evidence")
        self.assertIn("accepted_freshness_final_signal_decision", result["missing_evidence"])
        self.assertIn("accepted_blocker_caution_decision", result["missing_evidence"])
        self.assertFalse(result["accepted_proof"])

    def test_setup_time_row_outside_extracted_range_is_rejected(self):
        review = setup_review()
        review["setup_time_source_row_number"] = 99

        result = review_replacement_source_row_setup_time(extracted_bundle(), review)

        self.assertEqual(result["setup_time_review_status"], "rejected")
        self.assertIn("setup_time_source_row_number_outside_extracted_rows", result["rejected_reasons"])
        self.assertFalse(result["accepted_proof"])

    def test_after_setup_outcome_window_before_or_equal_to_setup_time_row_is_rejected(self):
        review = setup_review()
        review["after_setup_outcome_window_start"] = 11

        result = review_replacement_source_row_setup_time(extracted_bundle(), review)

        self.assertEqual(result["setup_time_review_status"], "rejected")
        self.assertIn("after_setup_window_violates_no_hindsight_boundary", result["rejected_reasons"])
        self.assertFalse(result["accepted_proof"])

    def test_unknown_candidate_id_is_rejected(self):
        result = review_replacement_source_row_setup_time(
            extracted_bundle(),
            setup_review("BAD-ID"),
        )

        self.assertEqual(result["setup_time_review_status"], "rejected")
        self.assertIn("unknown_candidate_id", result["rejected_reasons"])
        self.assertFalse(result["accepted_proof"])

    def test_invalid_symbol_setup_type_combination_is_rejected(self):
        review = setup_review("GLD-REPLACEMENT-IDEAL-CANDIDATE-001")
        review["symbol"] = "IWM"
        review["setup_type"] = "Continuation"

        result = review_replacement_source_row_setup_time(extracted_bundle(), review)

        self.assertEqual(result["setup_time_review_status"], "rejected")
        self.assertIn("symbol_does_not_match_candidate_id", result["rejected_reasons"])
        self.assertIn("setup_type_does_not_match_candidate_id", result["rejected_reasons"])
        self.assertFalse(result["accepted_proof"])

    def test_missing_extracted_rows_is_rejected(self):
        extracted = extracted_bundle()
        extracted["source_rows"] = []

        result = review_replacement_source_row_setup_time(extracted, setup_review())

        self.assertEqual(result["setup_time_review_status"], "rejected")
        self.assertIn("missing_extracted_rows", result["rejected_reasons"])
        self.assertFalse(result["accepted_proof"])

    def test_caller_input_is_not_mutated(self):
        extracted = extracted_bundle()
        review = setup_review()
        original_extracted = copy.deepcopy(extracted)
        original_review = copy.deepcopy(review)

        result = review_replacement_source_row_setup_time(extracted, review)
        result["packet_population_seed"]["source_rows"][0]["open"] = 1
        result["evidence_used"].append("mutated")

        self.assertEqual(extracted, original_extracted)
        self.assertEqual(review, original_review)

    def test_forbidden_broker_order_account_options_pnl_fields_are_rejected_or_surfaced(self):
        extracted = extracted_bundle()
        extracted["source_rows"][0]["broker_order_id"] = "not-allowed"
        review = setup_review()
        review["account_size"] = 100000
        review["options_pnl"] = 10

        result = review_replacement_source_row_setup_time(extracted, review)

        self.assertEqual(result["setup_time_review_status"], "rejected")
        self.assertIn("forbidden_live_or_broker_fields", result["rejected_reasons"])
        self.assertIn("forbidden_paths", result["missing_evidence"][0])
        self.assertFalse(result["accepted_proof"])

    def test_batch_summary_counts_ready_blocked_rejected_and_zero_accepted_proof_count(self):
        blocked = setup_review("IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002")
        blocked.pop("accepted_numeric_trigger")
        rejected = setup_review("GLD-REPLACEMENT-IDEAL-CANDIDATE-002")
        rejected["setup_time_source_row_number"] = 99

        result = review_replacement_source_row_setup_time_batch(
            [
                {
                    "extracted_source_window": extracted_bundle("GLD-REPLACEMENT-IDEAL-CANDIDATE-001"),
                    "setup_time_review": setup_review("GLD-REPLACEMENT-IDEAL-CANDIDATE-001"),
                },
                {
                    "extracted_source_window": extracted_bundle("IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002"),
                    "setup_time_review": blocked,
                },
                {
                    "extracted_source_window": extracted_bundle("GLD-REPLACEMENT-IDEAL-CANDIDATE-002"),
                    "setup_time_review": rejected,
                },
            ]
        )

        self.assertEqual(result["total"], 3)
        self.assertEqual(result["ready_for_packet_build_review"], 1)
        self.assertEqual(result["blocked_missing_evidence"], 1)
        self.assertEqual(result["rejected"], 1)
        self.assertEqual(result["accepted_proof_count"], 0)
        self.assertIn("GLD-REPLACEMENT-IDEAL-CANDIDATE-001", result["results"])

    def test_output_packet_population_seed_preserves_watch_only_and_no_trade_decision(self):
        result = review_replacement_source_row_setup_time(
            extracted_bundle("IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002"),
            setup_review("IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002"),
        )

        self.assertEqual(result["setup_time_review_status"], "ready_for_packet_build_review")
        self.assertTrue(result["packet_population_seed"]["watch_only"])
        self.assertTrue(result["packet_population_seed"]["no_trade_decision"])
        self.assertFalse(result["packet_population_seed"]["accepted_proof"])
        self.assertFalse(result["accepted_proof"])


if __name__ == "__main__":
    unittest.main()
