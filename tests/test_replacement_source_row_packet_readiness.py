import copy
import unittest

from watcher_foundation.replacement_source_row_packet_builder import (
    build_replacement_source_row_packet_from_rows,
)
from watcher_foundation.replacement_source_row_packet_readiness import (
    REPLACEMENT_SOURCE_ROW_PACKET_READINESS_RESULT_FIELDS,
    review_replacement_source_row_packet_readiness,
    review_replacement_source_row_packet_readiness_batch,
)


def row(timestamp="2026-05-06T14:30:00-04:00"):
    return {
        "timestamp": timestamp,
        "open": "430.0",
        "high": "435.0",
        "low": "429.0",
        "close": "434.0",
        "volume": "100000",
    }


def valid_request(candidate_id="GLD-REPLACEMENT-IDEAL-CANDIDATE-001"):
    return {
        "candidate_id": candidate_id,
        "source_rows": [row("2026-05-06T13:30:00-04:00"), row()],
        "setup_time_row_index": 1,
        "source_file_reference": "local_gld_1h_rth_export.csv",
        "source_row_reference": "rows 10-20",
        "source_window_start": "2026-05-06T13:30:00-04:00",
        "source_window_end": "2026-05-08T15:30:00-04:00",
        "trigger_candidate": 435.0,
        "trigger_basis": "completed 1H recovery hold",
        "invalidation_candidate": 429.0,
        "invalidation_basis": "setup-time low",
        "freshness_final_signal_candidate": "fresh setup-time signal",
        "blocker_caution_status": "no primary blocker",
        "unavailable_fields": ["macro", "iv"],
        "after_setup_outcome_window_start": "2026-05-06T15:30:00-04:00",
        "after_setup_outcome_window_end": "2026-05-08T15:30:00-04:00",
    }


def valid_gld_packet():
    built = build_replacement_source_row_packet_from_rows(**valid_request())
    return built["packet"]


class ReplacementSourceRowPacketReadinessTests(unittest.TestCase):
    def test_unavailable_iwm_slot_remains_inconclusive_with_handoff(self):
        result = review_replacement_source_row_packet_readiness(
            {
                "candidate_id": "IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001",
                "unavailable_status": "source_rows_missing",
                "missing_evidence": ["IWM continuation replacement source row packet"],
            }
        )

        self.assertEqual(result["readiness_status"], "missing_evidence_inconclusive")
        self.assertFalse(result["accepted_proof"])
        self.assertTrue(result["watch_only"])
        self.assertTrue(result["no_trade_decision"])
        self.assertEqual(result["symbol"], "IWM")
        self.assertEqual(result["setup_type"], "Continuation")
        self.assertIn("lower-tier source row evidence", result["lower_tier_handoff_summary"])
        self.assertIn("IWM continuation replacement source row packet", result["missing_evidence"])

    def test_unavailable_gld_slot_includes_trigger_invalidation_freshness(self):
        result = review_replacement_source_row_packet_readiness(
            {
                "candidate_id": "GLD-REPLACEMENT-IDEAL-CANDIDATE-002",
                "template_status": "source_rows_required",
            }
        )

        self.assertEqual(result["readiness_status"], "missing_evidence_inconclusive")
        self.assertIn("trigger evidence", result["missing_evidence"])
        self.assertIn("invalidation evidence", result["missing_evidence"])
        self.assertIn("freshness/final-signal evidence", result["missing_evidence"])

    def test_valid_gld_packet_from_builder_ready_but_not_accepted_proof(self):
        result = review_replacement_source_row_packet_readiness(valid_gld_packet())

        self.assertEqual(result["readiness_status"], "ready_for_acceptance_review")
        self.assertFalse(result["accepted_proof"])
        self.assertTrue(result["watch_only"])
        self.assertTrue(result["no_trade_decision"])
        self.assertEqual(result["missing_evidence"], [])
        for field_name in REPLACEMENT_SOURCE_ROW_PACKET_READINESS_RESULT_FIELDS:
            self.assertIn(field_name, result)

    def test_packet_missing_trigger_is_blocked_with_missing_evidence(self):
        packet = valid_gld_packet()
        packet["trigger_candidate"] = None

        result = review_replacement_source_row_packet_readiness(packet)

        self.assertEqual(result["readiness_status"], "missing_evidence_inconclusive")
        self.assertIn("trigger_candidate", result["missing_evidence"])
        self.assertFalse(result["accepted_proof"])

    def test_unknown_candidate_id_is_rejected(self):
        result = review_replacement_source_row_packet_readiness(
            {
                "candidate_id": "BAD-ID",
                "symbol": "GLD",
                "setup_type": "Ideal",
            }
        )

        self.assertEqual(result["readiness_status"], "rejected")
        self.assertIn("known replacement candidate id", result["missing_evidence"])
        self.assertFalse(result["accepted_proof"])

    def test_batch_summary_counts_ready_blocked_rejected(self):
        blocked = valid_gld_packet()
        blocked["trigger_candidate"] = None

        result = review_replacement_source_row_packet_readiness_batch(
            [
                valid_gld_packet(),
                blocked,
                {"candidate_id": "BAD-ID"},
            ]
        )

        self.assertEqual(result["records_processed"], 3)
        self.assertEqual(result["ready_for_acceptance_review"], 1)
        self.assertEqual(result["blocked_missing_evidence_inconclusive"], 1)
        self.assertEqual(result["rejected"], 1)
        self.assertFalse(result["accepted_proof"])

    def test_caller_input_is_not_mutated(self):
        packet = valid_gld_packet()
        original = copy.deepcopy(packet)

        result = review_replacement_source_row_packet_readiness(packet)
        result["evidence_used"][0]["source_file_reference"] = "mutated"
        result["validation"]["input_copy"]["symbol"] = "IWM"

        self.assertEqual(packet, original)

    def test_forbidden_broker_order_account_options_pnl_fields_are_surfaced(self):
        packet = valid_gld_packet()
        packet["broker_order_id"] = "not-allowed"
        packet["account_size"] = 100000
        packet["options_pnl"] = 10

        result = review_replacement_source_row_packet_readiness(packet)

        self.assertEqual(result["readiness_status"], "rejected")
        self.assertIn("forbidden_paths", result["missing_evidence"][-1])
        self.assertIn("forbidden_live_or_broker_fields", result["validation"]["rejected_reasons"])
        self.assertFalse(result["accepted_proof"])

    def test_invalid_candidate_symbol_setup_type_combination_is_rejected(self):
        packet = valid_gld_packet()
        packet["symbol"] = "IWM"
        packet["setup_type"] = "Continuation"

        result = review_replacement_source_row_packet_readiness(packet)

        self.assertEqual(result["readiness_status"], "rejected")
        self.assertIn("symbol_does_not_match_candidate_id", result["validation"]["rejected_reasons"])
        self.assertIn("setup_type_does_not_match_candidate_id", result["validation"]["rejected_reasons"])


if __name__ == "__main__":
    unittest.main()
