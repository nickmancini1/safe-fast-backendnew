import copy
import unittest

from watcher_foundation.replacement_source_row_setup_time_review import (
    review_replacement_source_row_setup_time,
)
from watcher_foundation.replacement_source_row_setup_time_review_request import (
    REPLACEMENT_SOURCE_ROW_SETUP_TIME_REVIEW_REQUEST_FIELDS,
    build_replacement_source_row_setup_time_review_request,
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
        "row_start": 10,
        "row_end": 12,
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


def accepted_fields():
    return {
        "setup_time_source_row_number": 11,
        "setup_time_timestamp": "2026-05-06T14:30:00-04:00",
        "setup_time_row_ohlcv": {
            "open": 430.0,
            "high": 435.0,
            "low": 429.0,
            "close": 434.0,
            "volume": 100000,
        },
        "accepted_setup_identity": "accepted identity for setup-time review",
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


class ReplacementSourceRowSetupTimeReviewRequestTests(unittest.TestCase):
    def test_valid_gld_rows_create_ready_request_but_not_accepted_proof(self):
        result = build_replacement_source_row_setup_time_review_request(
            extracted_bundle("GLD-REPLACEMENT-IDEAL-CANDIDATE-001"),
            {"candidate_row_numbers": [10, 11]},
        )

        self.assertEqual(result["setup_time_review_request_status"], "ready_for_setup_time_review_request")
        self.assertEqual(result["symbol"], "GLD")
        self.assertEqual(result["setup_type"], "Ideal")
        self.assertEqual(result["old_source_window_id"], "GLD-WINDOW-001")
        self.assertEqual(result["old_source_sample_id"], "GLD-SAMPLE-001")
        self.assertEqual(result["source_file_label"], "local_gld_1h_rth_export.csv")
        self.assertEqual([row["source_row_number"] for row in result["candidate_review_rows"]], [10, 11])
        self.assertIsNone(result["accepted_numeric_trigger"])
        self.assertFalse(result["accepted_proof"])
        for field_name in REPLACEMENT_SOURCE_ROW_SETUP_TIME_REVIEW_REQUEST_FIELDS:
            self.assertIn(field_name, result)

    def test_valid_iwm_rows_create_ready_request_but_not_accepted_proof(self):
        result = build_replacement_source_row_setup_time_review_request(
            extracted_bundle("IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001"),
            candidate_row_start=10,
            candidate_row_end=12,
        )

        self.assertEqual(result["setup_time_review_request_status"], "ready_for_setup_time_review_request")
        self.assertEqual(result["symbol"], "IWM")
        self.assertEqual(result["setup_type"], "Continuation")
        self.assertEqual(len(result["candidate_review_rows"]), 3)
        self.assertFalse(result["accepted_proof"])

    def test_request_output_can_be_completed_and_passed_into_existing_setup_time_gate(self):
        request = build_replacement_source_row_setup_time_review_request(extracted_bundle())
        completed = {
            "candidate_id": request["candidate_id"],
            "symbol": request["symbol"],
            "setup_type": request["setup_type"],
            **accepted_fields(),
        }

        result = review_replacement_source_row_setup_time(extracted_bundle(), completed)

        self.assertEqual(result["setup_time_review_status"], "ready_for_packet_build_review")
        self.assertFalse(result["accepted_proof"])
        self.assertFalse(result["packet_population_seed"]["accepted_proof"])

    def test_missing_accepted_trigger_invalidation_freshness_blocker_fields_are_listed(self):
        result = build_replacement_source_row_setup_time_review_request(extracted_bundle())

        for field_name in (
            "accepted_trigger_state",
            "accepted_numeric_trigger",
            "accepted_trigger_basis",
            "accepted_numeric_invalidation",
            "accepted_invalidation_basis",
            "accepted_freshness_final_signal_decision",
            "accepted_blocker_caution_decision",
        ):
            self.assertIn(field_name, result["required_fields_to_complete"])
            self.assertIn(field_name, result["missing_evidence"])

    def test_unknown_candidate_id_is_rejected(self):
        extracted = extracted_bundle()
        extracted["candidate_id"] = "BAD-ID"

        result = build_replacement_source_row_setup_time_review_request(extracted)

        self.assertEqual(result["setup_time_review_request_status"], "rejected")
        self.assertIn("unknown_candidate_id", result["rejected_reasons"])
        self.assertFalse(result["accepted_proof"])

    def test_invalid_symbol_setup_type_combination_is_rejected(self):
        result = build_replacement_source_row_setup_time_review_request(
            extracted_bundle("GLD-REPLACEMENT-IDEAL-CANDIDATE-001"),
            {"symbol": "IWM", "setup_type": "Continuation"},
        )

        self.assertEqual(result["setup_time_review_request_status"], "rejected")
        self.assertIn("symbol_does_not_match_candidate_id", result["rejected_reasons"])
        self.assertIn("setup_type_does_not_match_candidate_id", result["rejected_reasons"])
        self.assertFalse(result["accepted_proof"])

    def test_missing_extracted_rows_is_rejected(self):
        extracted = extracted_bundle()
        extracted["source_rows"] = []

        result = build_replacement_source_row_setup_time_review_request(extracted)

        self.assertEqual(result["setup_time_review_request_status"], "rejected")
        self.assertIn("missing_extracted_rows", result["rejected_reasons"])
        self.assertFalse(result["accepted_proof"])

    def test_candidate_row_outside_extracted_range_is_rejected(self):
        result = build_replacement_source_row_setup_time_review_request(
            extracted_bundle(),
            candidate_row_numbers=[99],
        )

        self.assertEqual(result["setup_time_review_request_status"], "rejected")
        self.assertIn("candidate_row_outside_extracted_range", result["rejected_reasons"])
        self.assertFalse(result["accepted_proof"])

    def test_caller_input_is_not_mutated(self):
        extracted = extracted_bundle()
        metadata = {"candidate_row_numbers": [10, 11]}
        original_extracted = copy.deepcopy(extracted)
        original_metadata = copy.deepcopy(metadata)

        result = build_replacement_source_row_setup_time_review_request(extracted, metadata)
        result["candidate_review_rows"][0]["open"] = 1
        result["evidence_used"].append("mutated")

        self.assertEqual(extracted, original_extracted)
        self.assertEqual(metadata, original_metadata)

    def test_forbidden_broker_order_account_options_pnl_fields_are_rejected_or_surfaced(self):
        extracted = extracted_bundle()
        extracted["source_rows"][0]["broker_order_id"] = "not-allowed"

        result = build_replacement_source_row_setup_time_review_request(
            extracted,
            {"account_size": 100000, "options_pnl": 10},
        )

        self.assertEqual(result["setup_time_review_request_status"], "rejected")
        self.assertIn("forbidden_live_or_broker_fields", result["rejected_reasons"])
        self.assertIn("forbidden_paths", result["missing_evidence"][0])
        self.assertFalse(result["accepted_proof"])

    def test_watch_only_and_no_trade_decision_are_preserved(self):
        result = build_replacement_source_row_setup_time_review_request(
            extracted_bundle("IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002")
        )

        self.assertTrue(result["watch_only"])
        self.assertTrue(result["no_trade_decision"])
        self.assertFalse(result["accepted_proof"])

    def test_accepted_proof_always_remains_false_even_if_input_claims_true(self):
        result = build_replacement_source_row_setup_time_review_request(
            extracted_bundle(),
            {"accepted_proof": True, "candidate_row_numbers": [10]},
        )

        self.assertEqual(result["setup_time_review_request_status"], "ready_for_setup_time_review_request")
        self.assertFalse(result["accepted_proof"])

    def test_unavailable_row_fields_are_preserved_explicitly(self):
        extracted = extracted_bundle()
        extracted["source_rows"][0].pop("volume")

        result = build_replacement_source_row_setup_time_review_request(
            extracted,
            {"candidate_row_numbers": [10]},
        )

        self.assertEqual(result["candidate_review_rows"][0]["volume"], "unavailable")
        self.assertIn("volume", result["candidate_review_rows"][0]["unavailable_fields"])


if __name__ == "__main__":
    unittest.main()
