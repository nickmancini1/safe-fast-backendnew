import copy
import unittest

from watcher_foundation.replacement_source_row_packet_population import (
    REPLACEMENT_SOURCE_ROW_PACKET_POPULATION_RESULT_FIELDS,
    populate_replacement_source_row_packet_batch,
    populate_replacement_source_row_packet_request,
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


class ReplacementSourceRowPacketPopulationTests(unittest.TestCase):
    def test_empty_unavailable_iwm_request_remains_missing_evidence_inconclusive(self):
        result = populate_replacement_source_row_packet_request(
            {
                "candidate_id": "IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001",
                "source_rows": [],
                "missing_evidence": ["IWM continuation source rows"],
            }
        )

        self.assertEqual(result["population_status"], "unavailable")
        self.assertEqual(result["readiness_status"], "missing_evidence_inconclusive")
        self.assertFalse(result["packet_built"])
        self.assertEqual(result["source_rows_supplied"], 0)
        self.assertIn("IWM continuation source rows", result["missing_evidence"])
        self.assertFalse(result["accepted_proof"])

    def test_empty_unavailable_gld_request_remains_missing_evidence_inconclusive(self):
        result = populate_replacement_source_row_packet_request(
            {
                "candidate_id": "GLD-REPLACEMENT-IDEAL-CANDIDATE-002",
                "unavailable_status": "source_rows_missing",
            }
        )

        self.assertEqual(result["population_status"], "unavailable")
        self.assertEqual(result["readiness_status"], "missing_evidence_inconclusive")
        self.assertFalse(result["packet_built"])
        self.assertIn("trigger evidence", result["missing_evidence"])
        self.assertIn("invalidation evidence", result["missing_evidence"])
        self.assertIn("freshness/final-signal evidence", result["missing_evidence"])
        self.assertFalse(result["accepted_proof"])

    def test_valid_gld_request_using_existing_builder_becomes_ready_but_not_accepted(self):
        result = populate_replacement_source_row_packet_request(valid_request())

        self.assertEqual(result["population_status"], "ready_for_packet_build_review")
        self.assertEqual(result["readiness_status"], "ready_for_acceptance_review")
        self.assertEqual(result["source_rows_supplied"], 2)
        self.assertTrue(result["packet_built"])
        self.assertEqual(result["missing_evidence"], [])
        self.assertTrue(result["watch_only"])
        self.assertTrue(result["no_trade_decision"])
        self.assertFalse(result["accepted_proof"])
        for field_name in REPLACEMENT_SOURCE_ROW_PACKET_POPULATION_RESULT_FIELDS:
            self.assertIn(field_name, result)

    def test_missing_trigger_request_is_blocked_with_missing_evidence_populated(self):
        request = valid_request()
        request["trigger_candidate"] = None

        result = populate_replacement_source_row_packet_request(request)

        self.assertEqual(result["population_status"], "blocked_missing_evidence")
        self.assertEqual(result["readiness_status"], "missing_evidence_inconclusive")
        self.assertIn("trigger_candidate", result["missing_evidence"])
        self.assertIn("missing_required_fields", result["rejected_reasons"])
        self.assertFalse(result["accepted_proof"])

    def test_unknown_candidate_id_is_rejected(self):
        result = populate_replacement_source_row_packet_request(
            {"candidate_id": "BAD-ID", "source_rows": []}
        )

        self.assertEqual(result["population_status"], "rejected")
        self.assertEqual(result["readiness_status"], "rejected")
        self.assertIn("unknown_candidate_id", result["rejected_reasons"])
        self.assertFalse(result["accepted_proof"])

    def test_invalid_candidate_symbol_setup_type_combination_is_rejected(self):
        request = valid_request()
        request["symbol"] = "IWM"
        request["setup_type"] = "Continuation"

        result = populate_replacement_source_row_packet_request(request)

        self.assertEqual(result["population_status"], "rejected")
        self.assertEqual(result["readiness_status"], "rejected")
        self.assertIn("symbol_does_not_match_candidate_id", result["rejected_reasons"])
        self.assertIn("setup_type_does_not_match_candidate_id", result["rejected_reasons"])
        self.assertFalse(result["packet_built"])

    def test_batch_summary_counts_ready_blocked_rejected_and_unavailable(self):
        blocked = valid_request("GLD-REPLACEMENT-IDEAL-CANDIDATE-002")
        blocked["trigger_candidate"] = None

        result = populate_replacement_source_row_packet_batch(
            [
                valid_request("GLD-REPLACEMENT-IDEAL-CANDIDATE-001"),
                blocked,
                {"candidate_id": "BAD-ID"},
                {
                    "candidate_id": "IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001",
                    "source_rows": [],
                },
            ]
        )

        self.assertEqual(result["total"], 4)
        self.assertEqual(result["ready_for_packet_build_review"], 1)
        self.assertEqual(result["blocked_missing_evidence"], 1)
        self.assertEqual(result["rejected"], 1)
        self.assertEqual(result["unavailable"], 1)
        self.assertEqual(result["accepted_proof_count"], 0)
        self.assertIn("GLD-REPLACEMENT-IDEAL-CANDIDATE-001", result["results"])
        self.assertIn("IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001", result["results"])

    def test_caller_input_is_not_mutated(self):
        request = valid_request()
        original = copy.deepcopy(request)

        result = populate_replacement_source_row_packet_request(request)
        result["evidence_used"][0]["source_file_reference"] = "mutated"
        result["missing_evidence"].append("mutated")

        self.assertEqual(request, original)

    def test_forbidden_broker_order_account_options_pnl_fields_are_rejected(self):
        request = valid_request()
        request["broker_order_id"] = "not-allowed"
        request["account_size"] = 100000
        request["options_pnl"] = 10

        result = populate_replacement_source_row_packet_request(request)

        self.assertEqual(result["population_status"], "rejected")
        self.assertEqual(result["readiness_status"], "rejected")
        self.assertIn("forbidden_live_or_broker_fields", result["rejected_reasons"])
        self.assertIn("forbidden_paths", result["missing_evidence"][0])
        self.assertFalse(result["packet_built"])
        self.assertFalse(result["accepted_proof"])


if __name__ == "__main__":
    unittest.main()
