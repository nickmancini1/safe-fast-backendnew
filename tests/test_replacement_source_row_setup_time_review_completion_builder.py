import copy
import unittest

from watcher_foundation.replacement_source_row_setup_time_review_completion import (
    complete_replacement_source_row_setup_time_review,
)
from watcher_foundation.replacement_source_row_setup_time_review_completion_builder import (
    REPLACEMENT_SOURCE_ROW_SETUP_TIME_REVIEW_COMPLETION_DRAFT_FIELDS,
    build_replacement_source_row_setup_time_review_completion_draft,
    build_replacement_source_row_setup_time_review_completion_draft_batch,
)


def row_context_packet(candidate_id="GLD-REPLACEMENT-IDEAL-CANDIDATE-001"):
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
        "row_context_packet_status": "ready_for_setup_time_review_completion",
        "setup_time_review_request_status": "ready_for_setup_time_review_request",
        "watch_only": True,
        "no_trade_decision": True,
        "accepted_proof": False,
    }


def unavailable_row_context_packet():
    packet = row_context_packet("GLD-REPLACEMENT-IDEAL-CANDIDATE-002")
    packet["row_context_packet_status"] = "unavailable"
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


def completion_choices(candidate_id="GLD-REPLACEMENT-IDEAL-CANDIDATE-001"):
    symbol = "IWM" if candidate_id.startswith("IWM") else "GLD"
    setup_type = "Continuation" if symbol == "IWM" else "Ideal"
    return {
        "candidate_id": candidate_id,
        "symbol": symbol,
        "setup_type": setup_type,
        "setup_time_source_row_number": 11,
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


class ReplacementSourceRowSetupTimeReviewCompletionBuilderTests(unittest.TestCase):
    def test_valid_gld_completion_draft_becomes_ready_and_not_accepted_proof(self):
        result = build_replacement_source_row_setup_time_review_completion_draft(
            row_context_packet("GLD-REPLACEMENT-IDEAL-CANDIDATE-001"),
            completion_choices("GLD-REPLACEMENT-IDEAL-CANDIDATE-001"),
        )

        self.assertEqual(result["completion_draft_status"], "completion_draft_ready")
        self.assertEqual(result["symbol"], "GLD")
        self.assertEqual(result["setup_type"], "Ideal")
        self.assertEqual(result["setup_time_timestamp"], "2026-05-06T14:30:00-04:00")
        self.assertEqual(result["setup_time_row_ohlcv"]["close"], 434.0)
        self.assertEqual(result["source_file_label"], "local_gld_1h_rth_export.csv")
        self.assertFalse(result["accepted_proof"])
        self.assertFalse(result["completion_payload"]["request_packet"]["accepted_proof"])
        self.assertFalse(result["completion_payload"]["completed_review_fields"]["accepted_proof"])
        for field_name in REPLACEMENT_SOURCE_ROW_SETUP_TIME_REVIEW_COMPLETION_DRAFT_FIELDS:
            self.assertIn(field_name, result)

    def test_valid_iwm_completion_draft_becomes_ready_and_not_accepted_proof(self):
        result = build_replacement_source_row_setup_time_review_completion_draft(
            row_context_packet("IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001"),
            completion_choices("IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001"),
        )

        self.assertEqual(result["completion_draft_status"], "completion_draft_ready")
        self.assertEqual(result["symbol"], "IWM")
        self.assertEqual(result["setup_type"], "Continuation")
        self.assertFalse(result["accepted_proof"])

    def test_valid_draft_output_can_pass_into_existing_completion_helper(self):
        draft = build_replacement_source_row_setup_time_review_completion_draft(
            row_context_packet(),
            completion_choices(),
        )

        payload = draft["completion_payload"]
        result = complete_replacement_source_row_setup_time_review(
            payload["request_packet"],
            payload["completed_review_fields"],
        )

        self.assertEqual(result["completion_status"], "ready_for_packet_build_review")
        self.assertEqual(result["setup_time_review_status"], "ready_for_packet_build_review")
        self.assertFalse(result["accepted_proof"])
        self.assertFalse(result["packet_population_seed"]["accepted_proof"])

    def test_missing_trigger_completion_choice_remains_blocked_missing_evidence(self):
        choices = completion_choices()
        choices.pop("accepted_trigger_state")
        choices.pop("accepted_numeric_trigger")
        choices.pop("accepted_trigger_basis")

        result = build_replacement_source_row_setup_time_review_completion_draft(row_context_packet(), choices)

        self.assertEqual(result["completion_draft_status"], "blocked_missing_evidence")
        self.assertIn("accepted_trigger_state", result["missing_evidence"])
        self.assertIn("accepted_numeric_trigger", result["missing_evidence"])
        self.assertIn("accepted_trigger_basis", result["missing_evidence"])
        self.assertFalse(result["accepted_proof"])

    def test_missing_invalidation_completion_choice_remains_blocked_missing_evidence(self):
        choices = completion_choices()
        choices.pop("accepted_numeric_invalidation")
        choices.pop("accepted_invalidation_basis")

        result = build_replacement_source_row_setup_time_review_completion_draft(row_context_packet(), choices)

        self.assertEqual(result["completion_draft_status"], "blocked_missing_evidence")
        self.assertIn("accepted_numeric_invalidation", result["missing_evidence"])
        self.assertIn("accepted_invalidation_basis", result["missing_evidence"])
        self.assertFalse(result["accepted_proof"])

    def test_missing_freshness_blocker_completion_choice_remains_blocked_missing_evidence(self):
        choices = completion_choices()
        choices.pop("accepted_freshness_final_signal_decision")
        choices.pop("accepted_blocker_caution_decision")

        result = build_replacement_source_row_setup_time_review_completion_draft(row_context_packet(), choices)

        self.assertEqual(result["completion_draft_status"], "blocked_missing_evidence")
        self.assertIn("accepted_freshness_final_signal_decision", result["missing_evidence"])
        self.assertIn("accepted_blocker_caution_decision", result["missing_evidence"])
        self.assertFalse(result["accepted_proof"])

    def test_unavailable_gld_candidate_remains_unavailable(self):
        result = build_replacement_source_row_setup_time_review_completion_draft(
            unavailable_row_context_packet(),
            completion_choices("GLD-REPLACEMENT-IDEAL-CANDIDATE-002"),
        )

        self.assertEqual(result["completion_draft_status"], "unavailable")
        self.assertEqual(result["candidate_id"], "GLD-REPLACEMENT-IDEAL-CANDIDATE-002")
        self.assertFalse(result["accepted_proof"])

    def test_setup_time_row_outside_row_context_rows_is_rejected(self):
        choices = completion_choices()
        choices["setup_time_source_row_number"] = 99

        result = build_replacement_source_row_setup_time_review_completion_draft(row_context_packet(), choices)

        self.assertEqual(result["completion_draft_status"], "rejected")
        self.assertIn("setup_time_source_row_number_outside_row_context_rows", result["rejected_reasons"])
        self.assertFalse(result["accepted_proof"])

    def test_after_setup_outcome_window_before_or_equal_to_setup_time_row_is_rejected(self):
        choices = completion_choices()
        choices["after_setup_outcome_window_start"] = 11

        result = build_replacement_source_row_setup_time_review_completion_draft(row_context_packet(), choices)

        self.assertEqual(result["completion_draft_status"], "rejected")
        self.assertIn("after_setup_window_violates_no_hindsight_boundary", result["rejected_reasons"])
        self.assertFalse(result["accepted_proof"])

    def test_unknown_candidate_id_is_rejected(self):
        packet = row_context_packet()
        packet["candidate_id"] = "BAD-ID"

        result = build_replacement_source_row_setup_time_review_completion_draft(packet, completion_choices())

        self.assertEqual(result["completion_draft_status"], "rejected")
        self.assertIn("unknown_candidate_id", result["rejected_reasons"])
        self.assertFalse(result["accepted_proof"])

    def test_invalid_symbol_setup_type_combination_is_rejected(self):
        choices = completion_choices("GLD-REPLACEMENT-IDEAL-CANDIDATE-001")
        choices["symbol"] = "IWM"
        choices["setup_type"] = "Continuation"

        result = build_replacement_source_row_setup_time_review_completion_draft(row_context_packet(), choices)

        self.assertEqual(result["completion_draft_status"], "rejected")
        self.assertIn("symbol_does_not_match_candidate_id", result["rejected_reasons"])
        self.assertIn("setup_type_does_not_match_candidate_id", result["rejected_reasons"])
        self.assertFalse(result["accepted_proof"])

    def test_caller_input_is_not_mutated(self):
        packet = row_context_packet()
        choices = completion_choices()
        original_packet = copy.deepcopy(packet)
        original_choices = copy.deepcopy(choices)

        result = build_replacement_source_row_setup_time_review_completion_draft(packet, choices)
        result["completion_payload"]["request_packet"]["candidate_review_rows"][0]["open"] = 1
        result["completed_fields_used"].append("mutated")

        self.assertEqual(packet, original_packet)
        self.assertEqual(choices, original_choices)

    def test_forbidden_broker_order_account_options_pnl_fields_are_rejected_or_surfaced(self):
        packet = row_context_packet()
        packet["candidate_review_rows"][0]["broker_order_id"] = "not-allowed"
        choices = completion_choices()
        choices["account_size"] = 100000
        choices["options_pnl"] = 10

        result = build_replacement_source_row_setup_time_review_completion_draft(packet, choices)

        self.assertEqual(result["completion_draft_status"], "rejected")
        self.assertIn("forbidden_live_or_broker_fields", result["rejected_reasons"])
        self.assertIn("forbidden_paths", result["missing_evidence"][0])
        self.assertFalse(result["accepted_proof"])

    def test_batch_summary_counts_ready_blocked_rejected_unavailable_and_zero_accepted_proof_count(self):
        blocked = completion_choices("IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002")
        blocked.pop("accepted_numeric_trigger")
        rejected = completion_choices("GLD-REPLACEMENT-IDEAL-CANDIDATE-001")
        rejected["setup_time_source_row_number"] = 99

        result = build_replacement_source_row_setup_time_review_completion_draft_batch(
            [
                {
                    "row_context_packet": row_context_packet("GLD-REPLACEMENT-IDEAL-CANDIDATE-001"),
                    "reviewer_completion_choices": completion_choices("GLD-REPLACEMENT-IDEAL-CANDIDATE-001"),
                },
                {
                    "row_context_packet": row_context_packet("IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002"),
                    "reviewer_completion_choices": blocked,
                },
                {
                    "row_context_packet": row_context_packet("GLD-REPLACEMENT-IDEAL-CANDIDATE-001"),
                    "reviewer_completion_choices": rejected,
                },
                {
                    "row_context_packet": unavailable_row_context_packet(),
                    "reviewer_completion_choices": completion_choices("GLD-REPLACEMENT-IDEAL-CANDIDATE-002"),
                },
            ]
        )

        self.assertEqual(result["total"], 4)
        self.assertEqual(result["completion_draft_ready"], 1)
        self.assertEqual(result["blocked_missing_evidence"], 1)
        self.assertEqual(result["rejected"], 1)
        self.assertEqual(result["unavailable"], 1)
        self.assertEqual(result["accepted_proof_count"], 0)

    def test_output_preserves_watch_only_and_no_trade_decision(self):
        result = build_replacement_source_row_setup_time_review_completion_draft(
            row_context_packet("IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002"),
            completion_choices("IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002"),
        )

        self.assertTrue(result["watch_only"])
        self.assertTrue(result["no_trade_decision"])
        self.assertTrue(result["completion_payload"]["request_packet"]["watch_only"])
        self.assertTrue(result["completion_payload"]["request_packet"]["no_trade_decision"])
        self.assertFalse(result["accepted_proof"])


if __name__ == "__main__":
    unittest.main()
