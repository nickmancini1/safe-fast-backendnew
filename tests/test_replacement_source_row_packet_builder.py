import unittest

from watcher_foundation.replacement_source_row_packet_builder import (
    build_replacement_source_row_packet_batch_from_rows,
    build_replacement_source_row_packet_from_rows,
    extract_setup_time_ohlcv,
    extract_setup_time_timestamp,
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


class ReplacementSourceRowPacketBuilderTests(unittest.TestCase):
    def test_extracts_timestamp_and_ohlcv(self):
        source_row = row()

        self.assertEqual(
            extract_setup_time_timestamp(source_row),
            "2026-05-06T14:30:00-04:00",
        )
        self.assertEqual(
            extract_setup_time_ohlcv(source_row),
            {
                "open": 430,
                "high": 435,
                "low": 429,
                "close": 434,
                "volume": 100000,
            },
        )

    def test_builds_ready_packet_from_valid_rows(self):
        result = build_replacement_source_row_packet_from_rows(**valid_request())

        self.assertTrue(result["ready_for_acceptance_review"])
        self.assertEqual(result["decision"], "ready_for_acceptance_review")
        self.assertEqual(result["packet"]["symbol"], "GLD")
        self.assertEqual(result["packet"]["setup_type"], "Ideal")
        self.assertTrue(result["watch_only"])
        self.assertTrue(result["no_trade_decision"])

    def test_rejects_missing_trigger(self):
        request = valid_request()
        request["trigger_candidate"] = None

        result = build_replacement_source_row_packet_from_rows(**request)

        self.assertFalse(result["ready_for_acceptance_review"])
        self.assertEqual(result["decision"], "missing_evidence_inconclusive")
        self.assertIn(
            "trigger_candidate",
            result["validation"]["missing_fields"],
        )

    def test_rejects_unknown_candidate(self):
        request = valid_request("BAD-ID")

        result = build_replacement_source_row_packet_from_rows(**request)

        self.assertFalse(result["ready_for_acceptance_review"])
        self.assertIn("unknown_candidate_id", result["validation"]["rejected_reasons"])

    def test_rejects_out_of_range_setup_row(self):
        request = valid_request()
        request["setup_time_row_index"] = 10

        result = build_replacement_source_row_packet_from_rows(**request)

        self.assertFalse(result["ready_for_acceptance_review"])
        self.assertIn(
            "setup_time_row_index_out_of_range",
            result["validation"]["rejected_reasons"],
        )

    def test_batch_builds_and_validates(self):
        result = build_replacement_source_row_packet_batch_from_rows(
            [
                valid_request("GLD-REPLACEMENT-IDEAL-CANDIDATE-001"),
                valid_request("IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001"),
            ]
        )

        self.assertEqual(result["records_processed"], 2)
        self.assertEqual(result["ready_for_acceptance_review"], 2)
        self.assertEqual(result["missing_evidence_or_rejected"], 0)
        self.assertTrue(result["watch_only"])
        self.assertTrue(result["no_trade_decision"])


if __name__ == "__main__":
    unittest.main()
