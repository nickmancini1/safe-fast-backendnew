import copy
import unittest

from watcher_foundation.replacement_source_row_csv_intake import (
    intake_replacement_source_row_csv_text,
)
from watcher_foundation.replacement_source_row_window_extractor import (
    REPLACEMENT_SOURCE_ROW_WINDOW_EXTRACTOR_RESULT_FIELDS,
    extract_replacement_source_row_window,
)


def csv_text(symbol="GLD", setup_type="Ideal", include_evidence=True):
    header = ["Date Time", "Open", "High", "Low", "Close", "Volume", "symbol", "setup_type"]
    row1 = ["2026-05-06T13:30:00-04:00", "430.0", "435.0", "429.0", "434.0", "100000", symbol, setup_type]
    row2 = ["2026-05-06T14:30:00-04:00", "434.0", "436.0", "432.0", "435.5", "120000", symbol, setup_type]
    row3 = ["2026-05-06T15:30:00-04:00", "435.5", "437.0", "434.5", "436.5", "130000", symbol, setup_type]
    if include_evidence:
        header.extend(
            [
                "trigger",
                "invalidation",
                "trigger_basis",
                "invalidation_basis",
                "freshness",
                "blocker_status",
            ]
        )
        for row in (row1, row2, row3):
            row.extend(
                [
                    "436.0",
                    "432.0",
                    "completed 1H recovery hold",
                    "setup-time low",
                    "fresh setup-time signal",
                    "no primary blocker",
                ]
            )
    return "\n".join([",".join(header), ",".join(row1), ",".join(row2), ",".join(row3)])


def metadata(prefix="gld"):
    return {
        "source_window_id": f"{prefix.upper()}-WINDOW-001",
        "source_sample_id": f"{prefix.upper()}-SAMPLE-001",
        "source_file_label": f"local_{prefix}_1h_rth_export.csv",
        "source_file_reference": f"local_{prefix}_1h_rth_export.csv",
        "source_row_reference": "rows 1-3",
        "source_window_start": "2026-05-06T13:30:00-04:00",
        "source_window_end": "2026-05-06T15:30:00-04:00",
        "after_setup_outcome_window_start": "2026-05-06T16:30:00-04:00",
        "after_setup_outcome_window_end": "2026-05-08T15:30:00-04:00",
        "unavailable_fields": ["macro unavailable"],
    }


class ReplacementSourceRowWindowExtractorTests(unittest.TestCase):
    def test_valid_gld_csv_text_with_1_based_row_range_extracts_rows_but_not_accepted_proof(self):
        result = extract_replacement_source_row_window(
            candidate_id="GLD-REPLACEMENT-IDEAL-CANDIDATE-001",
            csv_text=csv_text(),
            row_start=2,
            row_end=3,
            source_metadata=metadata(),
        )

        self.assertEqual(result["symbol"], "GLD")
        self.assertEqual(result["setup_type"], "Ideal")
        self.assertEqual(result["rows_extracted"], 2)
        self.assertEqual([row["source_row_number"] for row in result["source_rows"]], [2, 3])
        self.assertEqual(result["source_window_id"], "GLD-WINDOW-001")
        self.assertEqual(result["source_sample_id"], "GLD-SAMPLE-001")
        self.assertEqual(result["source_file_label"], "local_gld_1h_rth_export.csv")
        self.assertIn("source_row_number", result["csv_text_for_extracted_rows"])
        self.assertEqual(result["population_status"], "ready_for_packet_build_review")
        self.assertTrue(result["watch_only"])
        self.assertTrue(result["no_trade_decision"])
        self.assertFalse(result["accepted_proof"])
        for field_name in REPLACEMENT_SOURCE_ROW_WINDOW_EXTRACTOR_RESULT_FIELDS:
            self.assertIn(field_name, result)

    def test_valid_iwm_csv_text_with_1_based_row_range_extracts_rows_but_not_accepted_proof(self):
        result = extract_replacement_source_row_window(
            candidate_id="IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001",
            csv_text=csv_text("IWM", "Continuation"),
            row_start=1,
            row_end=2,
            source_metadata=metadata("iwm"),
        )

        self.assertEqual(result["symbol"], "IWM")
        self.assertEqual(result["setup_type"], "Continuation")
        self.assertEqual(result["rows_extracted"], 2)
        self.assertEqual([row["source_row_number"] for row in result["source_rows"]], [1, 2])
        self.assertEqual(result["population_status"], "ready_for_packet_build_review")
        self.assertFalse(result["accepted_proof"])

    def test_extracted_gld_rows_can_be_passed_into_existing_csv_intake_helper(self):
        result = extract_replacement_source_row_window(
            candidate_id="GLD-REPLACEMENT-IDEAL-CANDIDATE-001",
            csv_text=csv_text(),
            row_start=1,
            row_end=2,
            source_metadata=metadata(),
        )

        intake = intake_replacement_source_row_csv_text(
            candidate_id=result["candidate_id"],
            csv_text=result["csv_text_for_extracted_rows"],
            source_metadata=metadata(),
        )

        self.assertEqual(intake["population_status"], "ready_for_packet_build_review")
        self.assertFalse(intake["accepted_proof"])

    def test_extracted_iwm_rows_can_be_passed_into_existing_csv_intake_helper(self):
        result = extract_replacement_source_row_window(
            candidate_id="IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002",
            csv_text=csv_text("IWM", "Continuation"),
            row_start=2,
            row_end=3,
            source_metadata=metadata("iwm"),
        )

        intake = intake_replacement_source_row_csv_text(
            candidate_id=result["candidate_id"],
            csv_text=result["csv_text_for_extracted_rows"],
            source_metadata=metadata("iwm"),
        )

        self.assertEqual(intake["population_status"], "ready_for_packet_build_review")
        self.assertFalse(intake["accepted_proof"])

    def test_missing_trigger_invalidation_freshness_fields_remain_missing_evidence_not_accepted_proof(self):
        result = extract_replacement_source_row_window(
            candidate_id="GLD-REPLACEMENT-IDEAL-CANDIDATE-002",
            csv_text=csv_text(include_evidence=False),
            row_start=1,
            row_end=2,
            source_metadata=metadata(),
        )

        self.assertEqual(result["population_status"], "blocked_missing_evidence")
        self.assertIn("trigger_candidate", result["missing_evidence"])
        self.assertIn("invalidation_candidate", result["missing_evidence"])
        self.assertIn("freshness_final_signal_candidate", result["missing_evidence"])
        self.assertFalse(result["accepted_proof"])

    def test_unknown_candidate_id_is_rejected(self):
        result = extract_replacement_source_row_window(
            candidate_id="BAD-ID",
            csv_text=csv_text(),
            row_start=1,
            row_end=2,
            source_metadata=metadata(),
        )

        self.assertIn("unknown_candidate_id", result["rejected_reasons"])
        self.assertIsNone(result["population_request_seed"])
        self.assertFalse(result["accepted_proof"])

    def test_invalid_symbol_setup_type_combination_is_rejected(self):
        result = extract_replacement_source_row_window(
            candidate_id="GLD-REPLACEMENT-IDEAL-CANDIDATE-001",
            csv_text=csv_text(),
            row_start=1,
            row_end=2,
            symbol="IWM",
            setup_type="Continuation",
            source_metadata=metadata(),
        )

        self.assertIn("symbol_does_not_match_candidate_id", result["rejected_reasons"])
        self.assertIn("setup_type_does_not_match_candidate_id", result["rejected_reasons"])
        self.assertIsNone(result["population_request_seed"])

    def test_empty_csv_is_rejected(self):
        result = extract_replacement_source_row_window(
            candidate_id="GLD-REPLACEMENT-IDEAL-CANDIDATE-001",
            csv_text="",
            row_start=1,
            row_end=2,
            source_metadata=metadata(),
        )

        self.assertIn("empty_csv_text", result["rejected_reasons"])
        self.assertIsNone(result["population_request_seed"])

    def test_malformed_csv_is_rejected(self):
        result = extract_replacement_source_row_window(
            candidate_id="GLD-REPLACEMENT-IDEAL-CANDIDATE-001",
            csv_text='timestamp,open\n"2026-05-06T14:30:00-04:00,430.0',
            row_start=1,
            row_end=1,
            source_metadata=metadata(),
        )

        self.assertIn("malformed_csv_text", result["rejected_reasons"])
        self.assertIsNone(result["population_request_seed"])

    def test_missing_row_range_is_rejected(self):
        result = extract_replacement_source_row_window(
            candidate_id="GLD-REPLACEMENT-IDEAL-CANDIDATE-001",
            csv_text=csv_text(),
            row_start=None,
            row_end=2,
            source_metadata=metadata(),
        )

        self.assertIn("missing_row_range", result["rejected_reasons"])
        self.assertIsNone(result["population_request_seed"])

    def test_out_of_range_row_range_is_rejected(self):
        result = extract_replacement_source_row_window(
            candidate_id="GLD-REPLACEMENT-IDEAL-CANDIDATE-001",
            csv_text=csv_text(),
            row_start=2,
            row_end=4,
            source_metadata=metadata(),
        )

        self.assertIn("row_range_out_of_range", result["rejected_reasons"])
        self.assertIsNone(result["population_request_seed"])

    def test_caller_input_csv_text_and_metadata_are_not_mutated(self):
        text = csv_text()
        source_metadata = metadata()
        original_metadata = copy.deepcopy(source_metadata)

        result = extract_replacement_source_row_window(
            candidate_id="GLD-REPLACEMENT-IDEAL-CANDIDATE-001",
            csv_text=text,
            row_start=1,
            row_end=2,
            source_metadata=source_metadata,
        )
        result["source_rows"][0]["open"] = 1
        result["population_request_seed"]["source_rows"][0]["open"] = 1

        self.assertEqual(text, csv_text())
        self.assertEqual(source_metadata, original_metadata)

    def test_forbidden_broker_order_account_options_pnl_fields_are_rejected_or_surfaced(self):
        text = "\n".join(
            [
                "timestamp,open,high,low,close,volume,broker_order_id,options_pnl",
                "2026-05-06T14:30:00-04:00,430.0,435.0,429.0,434.0,100000,abc,10",
            ]
        )

        result = extract_replacement_source_row_window(
            candidate_id="GLD-REPLACEMENT-IDEAL-CANDIDATE-001",
            csv_text=text,
            row_start=1,
            row_end=1,
            source_metadata={**metadata(), "account_size": 100000},
        )

        self.assertIn("forbidden_live_or_broker_fields", result["rejected_reasons"])
        self.assertIn("forbidden_paths", result["missing_evidence"][0])
        self.assertFalse(result["accepted_proof"])

    def test_watch_only_and_no_trade_decision_are_preserved(self):
        result = extract_replacement_source_row_window(
            candidate_id="IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002",
            csv_text=csv_text("IWM", "Continuation"),
            row_start=1,
            row_end=3,
            source_metadata=metadata("iwm"),
        )

        self.assertTrue(result["watch_only"])
        self.assertTrue(result["no_trade_decision"])
        self.assertTrue(result["population_request_seed"]["no_hindsight_boundary"])
        self.assertFalse(result["accepted_proof"])


if __name__ == "__main__":
    unittest.main()
