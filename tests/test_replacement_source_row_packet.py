import unittest

from watcher_foundation.replacement_source_row_packet import (
    validate_replacement_source_row_packet,
    validate_replacement_source_row_packet_batch,
)


def valid_packet():
    return {
        "candidate_id": "GLD-REPLACEMENT-IDEAL-CANDIDATE-001",
        "symbol": "GLD",
        "setup_type": "Ideal",
        "timeframe": "1h_rth",
        "source_file_reference": "local_export_gld_1h_rth.csv",
        "source_row_reference": "rows 100-130",
        "source_window_start": "2026-05-04T09:30:00-04:00",
        "source_window_end": "2026-05-08T15:30:00-04:00",
        "setup_time_candidate_row_timestamp": "2026-05-06T14:30:00-04:00",
        "setup_time_candidate_row_ohlcv": {
            "open": 430.0,
            "high": 435.0,
            "low": 429.0,
            "close": 434.0,
            "volume": 100000,
        },
        "trigger_candidate": 435.0,
        "trigger_basis": "completed 1H recovery hold",
        "invalidation_candidate": 429.0,
        "invalidation_basis": "setup-time shelf low",
        "freshness_final_signal_candidate": "fresh candidate at setup time",
        "blocker_caution_status": "no primary blocker in setup-time row",
        "unavailable_fields": ["macro", "iv"],
        "no_hindsight_boundary": "setup-time row selected before terminal outcome review",
        "after_setup_outcome_window_start": "2026-05-06T15:30:00-04:00",
        "after_setup_outcome_window_end": "2026-05-08T15:30:00-04:00",
    }


class ReplacementSourceRowPacketTests(unittest.TestCase):
    def test_valid_packet_ready_for_acceptance_review(self):
        result = validate_replacement_source_row_packet(valid_packet())

        self.assertTrue(result["ready_for_acceptance_review"])
        self.assertEqual(result["decision"], "ready_for_acceptance_review")
        self.assertEqual(result["missing_fields"], [])
        self.assertEqual(result["rejected_reasons"], [])
        self.assertTrue(result["watch_only"])
        self.assertTrue(result["no_trade_decision"])

    def test_missing_trigger_stays_missing_evidence(self):
        packet = valid_packet()
        packet["trigger_candidate"] = None

        result = validate_replacement_source_row_packet(packet)

        self.assertFalse(result["ready_for_acceptance_review"])
        self.assertEqual(result["decision"], "missing_evidence_inconclusive")
        self.assertIn("trigger_candidate", result["missing_fields"])
        self.assertIn("missing_required_fields", result["rejected_reasons"])

    def test_forbidden_broker_field_rejected(self):
        packet = valid_packet()
        packet["broker_order_id"] = "never-allowed"

        result = validate_replacement_source_row_packet(packet)

        self.assertFalse(result["ready_for_acceptance_review"])
        self.assertIn("forbidden_live_or_broker_fields", result["rejected_reasons"])
        self.assertIn("broker_order_id", result["forbidden_paths"])

    def test_wrong_symbol_for_candidate_rejected(self):
        packet = valid_packet()
        packet["symbol"] = "IWM"

        result = validate_replacement_source_row_packet(packet)

        self.assertFalse(result["ready_for_acceptance_review"])
        self.assertIn("symbol_does_not_match_candidate_id", result["rejected_reasons"])

    def test_after_setup_window_must_follow_setup_time(self):
        packet = valid_packet()
        packet["after_setup_outcome_window_start"] = packet["setup_time_candidate_row_timestamp"]

        result = validate_replacement_source_row_packet(packet)

        self.assertFalse(result["ready_for_acceptance_review"])
        self.assertIn("after_setup_window_violates_no_hindsight_boundary", result["rejected_reasons"])

    def test_batch_reports_missing_candidate_ids(self):
        result = validate_replacement_source_row_packet_batch([valid_packet()])

        self.assertEqual(result["records_processed"], 1)
        self.assertEqual(result["ready_for_acceptance_review"], 1)
        self.assertIn("IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001", result["missing_candidate_ids"])
        self.assertTrue(result["watch_only"])
        self.assertTrue(result["no_trade_decision"])


if __name__ == "__main__":
    unittest.main()
