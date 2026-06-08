import copy
import unittest

from watcher_foundation.replacement_source_row_setup_time_review_completion import (
    REPLACEMENT_SOURCE_ROW_SETUP_TIME_REVIEW_COMPLETION_RESULT_FIELDS,
    complete_replacement_source_row_setup_time_review,
    complete_replacement_source_row_setup_time_review_batch,
)


def request_packet(candidate_id="GLD-REPLACEMENT-IDEAL-CANDIDATE-001"):
    symbol = "IWM" if candidate_id.startswith("IWM") else "GLD"
    setup_type = "Continuation" if symbol == "IWM" else "Ideal"
    return {
        "candidate_id": candidate_id,
        "symbol": symbol,
        "setup_type": setup_type,
        "old_source_window_id": f"{symbol}-WINDOW-001",
        "old_source_sample_id": f"{symbol}-SAMPLE-001",
        "source_file_label": f"local_{symbol.lower()}_1h_rth_export.csv",
        "row_start": 10,
        "row_end": 12,
        "candidate_review_rows": [
            row(10, "2026-05-06T13:30:00-04:00"),
            row(11, "2026-05-06T14:30:00-04:00"),
            row(12, "2026-05-06T15:30:00-04:00"),
        ],
        "setup_time_review_request_status": "ready_for_setup_time_review_request",
        "watch_only": True,
        "no_trade_decision": True,
        "accepted_proof": False,
    }


def unavailable_request_packet():
    packet = request_packet("GLD-REPLACEMENT-IDEAL-CANDIDATE-002")
    packet["setup_time_review_request_status"] = "unavailable"
    packet["candidate_review_rows"] = []
    packet["missing_evidence"] = ["second exact GLD Ideal source window"]
    return packet


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


def completed_fields(candidate_id="GLD-REPLACEMENT-IDEAL-CANDIDATE-001"):
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
        "accepted_setup_identity": f"{symbol} {setup_type} identity accepted for setup-time review",
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


class ReplacementSourceRowSetupTimeReviewCompletionTests(unittest.TestCase):
    def test_valid_gld_completed_review_becomes_ready_and_not_accepted_proof(self):
        result = complete_replacement_source_row_setup_time_review(
            request_packet("GLD-REPLACEMENT-IDEAL-CANDIDATE-001"),
            completed_fields("GLD-REPLACEMENT-IDEAL-CANDIDATE-001"),
        )

        self.assertEqual(result["completion_status"], "ready_for_packet_build_review")
        self.assertEqual(result["setup_time_review_status"], "ready_for_packet_build_review")
        self.assertEqual(result["symbol"], "GLD")
        self.assertEqual(result["setup_type"], "Ideal")
        self.assertEqual(result["old_source_window_id"], "GLD-WINDOW-001")
        self.assertEqual(result["old_source_sample_id"], "GLD-SAMPLE-001")
        self.assertEqual(result["source_file_label"], "local_gld_1h_rth_export.csv")
        self.assertFalse(result["accepted_proof"])
        self.assertFalse(result["packet_population_seed"]["accepted_proof"])
        for field_name in REPLACEMENT_SOURCE_ROW_SETUP_TIME_REVIEW_COMPLETION_RESULT_FIELDS:
            self.assertIn(field_name, result)

    def test_valid_iwm_completed_review_becomes_ready_and_not_accepted_proof(self):
        result = complete_replacement_source_row_setup_time_review(
            request_packet("IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001"),
            completed_fields("IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001"),
        )

        self.assertEqual(result["completion_status"], "ready_for_packet_build_review")
        self.assertEqual(result["symbol"], "IWM")
        self.assertEqual(result["setup_type"], "Continuation")
        self.assertFalse(result["accepted_proof"])

    def test_missing_trigger_completion_remains_blocked_missing_evidence(self):
        completed = completed_fields()
        completed.pop("accepted_trigger_state")
        completed.pop("accepted_numeric_trigger")
        completed.pop("accepted_trigger_basis")

        result = complete_replacement_source_row_setup_time_review(request_packet(), completed)

        self.assertEqual(result["completion_status"], "blocked_missing_evidence")
        self.assertIn("accepted_trigger_state", result["missing_evidence"])
        self.assertIn("accepted_numeric_trigger", result["missing_evidence"])
        self.assertIn("accepted_trigger_basis", result["missing_evidence"])
        self.assertFalse(result["accepted_proof"])

    def test_missing_invalidation_completion_remains_blocked_missing_evidence(self):
        completed = completed_fields()
        completed.pop("accepted_numeric_invalidation")
        completed.pop("accepted_invalidation_basis")

        result = complete_replacement_source_row_setup_time_review(request_packet(), completed)

        self.assertEqual(result["completion_status"], "blocked_missing_evidence")
        self.assertIn("accepted_numeric_invalidation", result["missing_evidence"])
        self.assertIn("accepted_invalidation_basis", result["missing_evidence"])
        self.assertFalse(result["accepted_proof"])

    def test_missing_freshness_blocker_completion_remains_blocked_missing_evidence(self):
        completed = completed_fields()
        completed.pop("accepted_freshness_final_signal_decision")
        completed.pop("accepted_blocker_caution_decision")

        result = complete_replacement_source_row_setup_time_review(request_packet(), completed)

        self.assertEqual(result["completion_status"], "blocked_missing_evidence")
        self.assertIn("accepted_freshness_final_signal_decision", result["missing_evidence"])
        self.assertIn("accepted_blocker_caution_decision", result["missing_evidence"])
        self.assertFalse(result["accepted_proof"])

    def test_unavailable_gld_candidate_remains_unavailable(self):
        result = complete_replacement_source_row_setup_time_review(
            unavailable_request_packet(),
            completed_fields("GLD-REPLACEMENT-IDEAL-CANDIDATE-002"),
        )

        self.assertEqual(result["completion_status"], "unavailable")
        self.assertEqual(result["setup_time_review_status"], "unavailable")
        self.assertEqual(result["candidate_id"], "GLD-REPLACEMENT-IDEAL-CANDIDATE-002")
        self.assertFalse(result["accepted_proof"])

    def test_setup_time_row_outside_candidate_review_rows_is_rejected(self):
        completed = completed_fields()
        completed["setup_time_source_row_number"] = 99

        result = complete_replacement_source_row_setup_time_review(request_packet(), completed)

        self.assertEqual(result["completion_status"], "rejected")
        self.assertIn("setup_time_source_row_number_outside_candidate_review_rows", result["rejected_reasons"])
        self.assertFalse(result["accepted_proof"])

    def test_no_hindsight_outcome_window_before_or_equal_to_setup_time_row_is_rejected(self):
        completed = completed_fields()
        completed["after_setup_outcome_window_start"] = 11

        result = complete_replacement_source_row_setup_time_review(request_packet(), completed)

        self.assertEqual(result["completion_status"], "rejected")
        self.assertIn("after_setup_window_violates_no_hindsight_boundary", result["rejected_reasons"])
        self.assertFalse(result["accepted_proof"])

    def test_unknown_candidate_id_is_rejected(self):
        packet = request_packet()
        packet["candidate_id"] = "BAD-ID"

        result = complete_replacement_source_row_setup_time_review(packet, completed_fields())

        self.assertEqual(result["completion_status"], "rejected")
        self.assertIn("unknown_candidate_id", result["rejected_reasons"])
        self.assertFalse(result["accepted_proof"])

    def test_invalid_symbol_setup_type_combination_is_rejected(self):
        completed = completed_fields("GLD-REPLACEMENT-IDEAL-CANDIDATE-001")
        completed["symbol"] = "IWM"
        completed["setup_type"] = "Continuation"

        result = complete_replacement_source_row_setup_time_review(request_packet(), completed)

        self.assertEqual(result["completion_status"], "rejected")
        self.assertIn("symbol_does_not_match_candidate_id", result["rejected_reasons"])
        self.assertIn("setup_type_does_not_match_candidate_id", result["rejected_reasons"])
        self.assertFalse(result["accepted_proof"])

    def test_missing_request_packet_is_rejected(self):
        result = complete_replacement_source_row_setup_time_review(None, completed_fields())

        self.assertEqual(result["completion_status"], "rejected")
        self.assertIn("missing_request_packet", result["rejected_reasons"])
        self.assertFalse(result["accepted_proof"])

    def test_caller_input_is_not_mutated(self):
        packet = request_packet()
        completed = completed_fields()
        original_packet = copy.deepcopy(packet)
        original_completed = copy.deepcopy(completed)

        result = complete_replacement_source_row_setup_time_review(packet, completed)
        result["packet_population_seed"]["source_rows"][0]["open"] = 1
        result["completed_fields_used"].append("mutated")

        self.assertEqual(packet, original_packet)
        self.assertEqual(completed, original_completed)

    def test_forbidden_broker_order_account_options_pnl_fields_are_rejected_or_surfaced(self):
        packet = request_packet()
        packet["candidate_review_rows"][0]["broker_order_id"] = "not-allowed"
        completed = completed_fields()
        completed["account_size"] = 100000
        completed["options_pnl"] = 10

        result = complete_replacement_source_row_setup_time_review(packet, completed)

        self.assertEqual(result["completion_status"], "rejected")
        self.assertIn("forbidden_live_or_broker_fields", result["rejected_reasons"])
        self.assertIn("forbidden_paths", result["missing_evidence"][0])
        self.assertFalse(result["accepted_proof"])

    def test_batch_summary_counts_ready_blocked_rejected_unavailable_and_zero_accepted_proof_count(self):
        blocked = completed_fields("IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002")
        blocked.pop("accepted_numeric_trigger")
        rejected = completed_fields("GLD-REPLACEMENT-IDEAL-CANDIDATE-001")
        rejected["setup_time_source_row_number"] = 99

        result = complete_replacement_source_row_setup_time_review_batch(
            [
                {
                    "request_packet": request_packet("GLD-REPLACEMENT-IDEAL-CANDIDATE-001"),
                    "completed_review_fields": completed_fields("GLD-REPLACEMENT-IDEAL-CANDIDATE-001"),
                },
                {
                    "request_packet": request_packet("IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002"),
                    "completed_review_fields": blocked,
                },
                {
                    "request_packet": request_packet("GLD-REPLACEMENT-IDEAL-CANDIDATE-001"),
                    "completed_review_fields": rejected,
                },
                {
                    "request_packet": unavailable_request_packet(),
                    "completed_review_fields": completed_fields("GLD-REPLACEMENT-IDEAL-CANDIDATE-002"),
                },
            ]
        )

        self.assertEqual(result["total"], 4)
        self.assertEqual(result["ready_for_packet_build_review"], 1)
        self.assertEqual(result["blocked_missing_evidence"], 1)
        self.assertEqual(result["rejected"], 1)
        self.assertEqual(result["unavailable"], 1)
        self.assertEqual(result["accepted_proof_count"], 0)

    def test_output_preserves_watch_only_and_no_trade_decision(self):
        result = complete_replacement_source_row_setup_time_review(
            request_packet("IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002"),
            completed_fields("IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002"),
        )

        self.assertTrue(result["watch_only"])
        self.assertTrue(result["no_trade_decision"])
        self.assertTrue(result["packet_population_seed"]["watch_only"])
        self.assertTrue(result["packet_population_seed"]["no_trade_decision"])
        self.assertFalse(result["accepted_proof"])

    def test_output_can_pass_valid_completed_fields_into_existing_setup_time_review_gate(self):
        result = complete_replacement_source_row_setup_time_review(request_packet(), completed_fields())

        self.assertEqual(result["setup_time_review_status"], "ready_for_packet_build_review")
        self.assertEqual(result["packet_population_seed"]["setup_time_source_row_number"], 11)
        self.assertEqual(result["packet_population_seed"]["source_file_reference"], "local_gld_1h_rth_export.csv")
        self.assertFalse(result["packet_population_seed"]["accepted_proof"])

    def test_directionally_favorable_after_setup_movement_does_not_count_as_proof(self):
        completed = completed_fields()
        completed["after_setup_directional_move"] = "favorable"
        completed["accepted_proof"] = True

        result = complete_replacement_source_row_setup_time_review(request_packet(), completed)

        self.assertEqual(result["completion_status"], "ready_for_packet_build_review")
        self.assertFalse(result["accepted_proof"])
        self.assertFalse(result["packet_population_seed"]["accepted_proof"])


if __name__ == "__main__":
    unittest.main()
