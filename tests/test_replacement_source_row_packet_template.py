import unittest

from watcher_foundation.replacement_source_row_packet_template import (
    build_all_replacement_source_row_packet_templates,
    build_replacement_source_row_packet_template,
    classify_source_row_packet,
)


def valid_packet():
    return {
        "candidate_id": "IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001",
        "symbol": "IWM",
        "setup_type": "Continuation",
        "timeframe": "1h_rth",
        "source_file_reference": "local_iwm_export.csv",
        "source_row_reference": "rows 10-40",
        "source_window_start": "2026-04-20T09:30:00-04:00",
        "source_window_end": "2026-04-24T15:30:00-04:00",
        "setup_time_candidate_row_timestamp": "2026-04-22T13:30:00-04:00",
        "setup_time_candidate_row_ohlcv": {
            "open": 275.0,
            "high": 278.0,
            "low": 274.0,
            "close": 277.5,
            "volume": 123456,
        },
        "trigger_candidate": 278.0,
        "trigger_basis": "completed 1H reclaim hold",
        "invalidation_candidate": 274.0,
        "invalidation_basis": "setup-time rebuild low",
        "freshness_final_signal_candidate": "fresh continuation candidate",
        "blocker_caution_status": "no primary blocker",
        "unavailable_fields": ["macro", "iv"],
        "no_hindsight_boundary": "setup-time row selected first",
        "after_setup_outcome_window_start": "2026-04-22T14:30:00-04:00",
        "after_setup_outcome_window_end": "2026-04-24T15:30:00-04:00",
    }


class ReplacementSourceRowPacketTemplateTests(unittest.TestCase):
    def test_template_for_known_candidate_requires_source_rows(self):
        result = build_replacement_source_row_packet_template(
            "GLD-REPLACEMENT-IDEAL-CANDIDATE-001"
        )

        self.assertEqual(result["template_status"], "source_rows_required")
        self.assertFalse(result["ready_for_acceptance_review"])
        self.assertEqual(result["decision"], "missing_evidence_inconclusive")
        self.assertEqual(result["packet"]["symbol"], "GLD")
        self.assertEqual(result["packet"]["setup_type"], "Ideal")
        self.assertTrue(result["watch_only"])
        self.assertTrue(result["no_trade_decision"])

    def test_unknown_candidate_template_is_rejected(self):
        result = build_replacement_source_row_packet_template("BAD-ID")

        self.assertEqual(result["template_status"], "unknown_candidate_id")
        self.assertFalse(result["ready_for_acceptance_review"])
        self.assertEqual(result["decision"], "missing_evidence_inconclusive")

    def test_all_templates_cover_four_candidate_ids(self):
        result = build_all_replacement_source_row_packet_templates()

        self.assertEqual(result["template_count"], 4)
        self.assertEqual(result["ready_for_acceptance_review"], 0)
        self.assertEqual(result["missing_evidence_or_rejected"], 4)
        self.assertEqual(result["batch_validation"]["missing_candidate_ids"], [])
        self.assertTrue(result["watch_only"])
        self.assertTrue(result["no_trade_decision"])

    def test_classify_valid_packet_ready(self):
        result = classify_source_row_packet(valid_packet())

        self.assertEqual(result["classification"], "ready_for_acceptance_review")
        self.assertTrue(result["validation"]["ready_for_acceptance_review"])

    def test_classify_missing_field_packet_inconclusive(self):
        packet = valid_packet()
        packet["trigger_candidate"] = None

        result = classify_source_row_packet(packet)

        self.assertEqual(result["classification"], "missing_evidence_inconclusive")
        self.assertFalse(result["validation"]["ready_for_acceptance_review"])
        self.assertIn("trigger_candidate", result["validation"]["missing_fields"])

    def test_classify_does_not_mutate_input(self):
        packet = valid_packet()
        result = classify_source_row_packet(packet)

        result["input_copy"]["symbol"] = "BROKEN"
        self.assertEqual(packet["symbol"], "IWM")


if __name__ == "__main__":
    unittest.main()
