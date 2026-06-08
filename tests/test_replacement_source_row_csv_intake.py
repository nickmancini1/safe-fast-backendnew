import copy
import unittest

from watcher_foundation.replacement_source_row_csv_intake import (
    REPLACEMENT_SOURCE_ROW_CSV_INTAKE_RESULT_FIELDS,
    intake_replacement_source_row_csv_text,
    intake_replacement_source_row_dicts,
)
from watcher_foundation.replacement_source_row_packet_population import (
    populate_replacement_source_row_packet_request,
)


def csv_text(symbol="GLD", setup_type="Ideal"):
    return "\n".join(
        [
            "Date Time,Open,High,Low,Close,Volume,trigger,invalidation,trigger_basis,invalidation_basis,freshness,blocker_status,symbol,setup_type",
            f"2026-05-06T13:30:00-04:00,430.0,435.0,429.0,434.0,100000,435.0,429.0,completed 1H recovery hold,setup-time low,fresh setup-time signal,no primary blocker,{symbol},{setup_type}",
            f"2026-05-06T14:30:00-04:00,434.0,436.0,432.0,435.5,120000,435.0,429.0,completed 1H recovery hold,setup-time low,fresh setup-time signal,no primary blocker,{symbol},{setup_type}",
        ]
    )


def source_metadata(prefix="gld"):
    return {
        "source_file_reference": f"local_{prefix}_1h_rth_export.csv",
        "source_row_reference": "rows 10-11",
        "source_window_start": "2026-05-06T13:30:00-04:00",
        "source_window_end": "2026-05-06T14:30:00-04:00",
        "after_setup_outcome_window_start": "2026-05-06T15:30:00-04:00",
        "after_setup_outcome_window_end": "2026-05-08T15:30:00-04:00",
    }


class ReplacementSourceRowCsvIntakeTests(unittest.TestCase):
    def test_valid_gld_csv_text_creates_population_request_but_not_accepted_proof(self):
        result = intake_replacement_source_row_csv_text(
            candidate_id="GLD-REPLACEMENT-IDEAL-CANDIDATE-001",
            csv_text=csv_text(),
            source_metadata=source_metadata(),
            unavailable_fields=["macro unavailable"],
        )

        self.assertEqual(result["population_status"], "ready_for_packet_build_review")
        self.assertEqual(result["readiness_status"], "ready_for_acceptance_review")
        self.assertEqual(result["population_request"]["candidate_id"], "GLD-REPLACEMENT-IDEAL-CANDIDATE-001")
        self.assertEqual(result["population_request"]["symbol"], "GLD")
        self.assertEqual(result["population_request"]["setup_type"], "Ideal")
        self.assertEqual(result["normalized_rows"][0]["volume"], 100000)
        self.assertTrue(result["watch_only"])
        self.assertTrue(result["no_trade_decision"])
        self.assertFalse(result["accepted_proof"])
        for field_name in REPLACEMENT_SOURCE_ROW_CSV_INTAKE_RESULT_FIELDS:
            self.assertIn(field_name, result)

    def test_valid_iwm_csv_text_creates_population_request_but_not_accepted_proof(self):
        result = intake_replacement_source_row_csv_text(
            candidate_id="IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001",
            csv_text=csv_text("IWM", "Continuation"),
            source_metadata=source_metadata("iwm"),
            unavailable_fields=["macro unavailable"],
        )

        self.assertEqual(result["population_status"], "ready_for_packet_build_review")
        self.assertEqual(result["readiness_status"], "ready_for_acceptance_review")
        self.assertEqual(result["population_request"]["symbol"], "IWM")
        self.assertEqual(result["population_request"]["setup_type"], "Continuation")
        self.assertFalse(result["accepted_proof"])

    def test_missing_trigger_invalidation_freshness_fields_remain_blocked(self):
        text = "\n".join(
            [
                "timestamp,open,high,low,close,volume",
                "2026-05-06T14:30:00-04:00,430.0,435.0,429.0,434.0,100000",
            ]
        )

        result = intake_replacement_source_row_csv_text(
            candidate_id="GLD-REPLACEMENT-IDEAL-CANDIDATE-002",
            csv_text=text,
            source_metadata=source_metadata(),
        )

        self.assertEqual(result["population_status"], "blocked_missing_evidence")
        self.assertEqual(result["readiness_status"], "missing_evidence_inconclusive")
        self.assertIn("trigger_candidate", result["missing_evidence"])
        self.assertIn("invalidation_candidate", result["missing_evidence"])
        self.assertIn("freshness_final_signal_candidate", result["missing_evidence"])
        self.assertFalse(result["accepted_proof"])

    def test_unknown_candidate_id_is_rejected(self):
        result = intake_replacement_source_row_csv_text(
            candidate_id="BAD-ID",
            csv_text=csv_text(),
            source_metadata=source_metadata(),
        )

        self.assertIn("unknown_candidate_id", result["rejected_reasons"])
        self.assertIsNone(result["population_request"])
        self.assertFalse(result["accepted_proof"])

    def test_invalid_symbol_setup_type_combination_is_rejected(self):
        result = intake_replacement_source_row_csv_text(
            candidate_id="GLD-REPLACEMENT-IDEAL-CANDIDATE-001",
            csv_text=csv_text(),
            symbol="IWM",
            setup_type="Continuation",
            source_metadata=source_metadata(),
        )

        self.assertIn("symbol_does_not_match_candidate_id", result["rejected_reasons"])
        self.assertIn("setup_type_does_not_match_candidate_id", result["rejected_reasons"])
        self.assertIsNone(result["population_request"])

    def test_empty_csv_is_rejected(self):
        result = intake_replacement_source_row_csv_text(
            candidate_id="GLD-REPLACEMENT-IDEAL-CANDIDATE-001",
            csv_text="",
            source_metadata=source_metadata(),
        )

        self.assertIn("empty_csv_text", result["rejected_reasons"])
        self.assertIsNone(result["population_request"])

    def test_malformed_csv_is_rejected(self):
        result = intake_replacement_source_row_csv_text(
            candidate_id="GLD-REPLACEMENT-IDEAL-CANDIDATE-001",
            csv_text='timestamp,open\n"2026-05-06T14:30:00-04:00,430.0',
            source_metadata=source_metadata(),
        )

        self.assertIn("malformed_csv_text", result["rejected_reasons"])
        self.assertIsNone(result["population_request"])

    def test_forbidden_broker_order_account_options_pnl_fields_are_rejected_or_surfaced(self):
        text = "\n".join(
            [
                "timestamp,open,high,low,close,volume,trigger,invalidation,trigger_basis,invalidation_basis,freshness,blocker_status,broker_order_id,options_pnl",
                "2026-05-06T14:30:00-04:00,430.0,435.0,429.0,434.0,100000,435.0,429.0,completed 1H recovery hold,setup-time low,fresh setup-time signal,no primary blocker,abc,10",
            ]
        )

        result = intake_replacement_source_row_csv_text(
            candidate_id="GLD-REPLACEMENT-IDEAL-CANDIDATE-001",
            csv_text=text,
            source_metadata={**source_metadata(), "account_size": 100000},
        )

        self.assertEqual(result["population_status"], "rejected")
        self.assertIn("forbidden_live_or_broker_fields", result["rejected_reasons"])
        self.assertFalse(result["accepted_proof"])

    def test_caller_input_csv_text_and_row_dicts_are_not_mutated(self):
        text = csv_text()
        rows = [
            {
                "timestamp": "2026-05-06T14:30:00-04:00",
                "open": "430.0",
                "high": "435.0",
                "low": "429.0",
                "close": "434.0",
                "volume": "100000",
                "trigger": "435.0",
                "invalidation": "429.0",
                "trigger_basis": "completed 1H recovery hold",
                "invalidation_basis": "setup-time low",
                "freshness": "fresh setup-time signal",
                "blocker_status": "no primary blocker",
            }
        ]
        original_rows = copy.deepcopy(rows)

        csv_result = intake_replacement_source_row_csv_text(
            candidate_id="GLD-REPLACEMENT-IDEAL-CANDIDATE-001",
            csv_text=text,
            source_metadata=source_metadata(),
        )
        dict_result = intake_replacement_source_row_dicts(
            candidate_id="GLD-REPLACEMENT-IDEAL-CANDIDATE-001",
            row_dicts=rows,
            source_metadata=source_metadata(),
        )
        csv_result["normalized_rows"][0]["open"] = 1
        dict_result["population_request"]["source_rows"][0]["open"] = 1

        self.assertEqual(text, csv_text())
        self.assertEqual(rows, original_rows)

    def test_output_population_request_can_be_passed_to_existing_population_gate(self):
        result = intake_replacement_source_row_csv_text(
            candidate_id="GLD-REPLACEMENT-IDEAL-CANDIDATE-001",
            csv_text=csv_text(),
            source_metadata=source_metadata(),
            unavailable_fields=["macro unavailable"],
        )

        population = populate_replacement_source_row_packet_request(result["population_request"])

        self.assertEqual(population["population_status"], "ready_for_packet_build_review")
        self.assertFalse(population["accepted_proof"])

    def test_watch_only_and_no_trade_decision_are_preserved(self):
        result = intake_replacement_source_row_csv_text(
            candidate_id="IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002",
            csv_text=csv_text("IWM", "Continuation"),
            source_metadata=source_metadata("iwm"),
        )

        self.assertTrue(result["watch_only"])
        self.assertTrue(result["no_trade_decision"])
        self.assertTrue(result["population_request"]["no_hindsight_boundary"])
        self.assertFalse(result["accepted_proof"])


if __name__ == "__main__":
    unittest.main()
