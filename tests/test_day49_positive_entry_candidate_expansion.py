import json
import unittest
from pathlib import Path

from historical_signal_replay import day49_positive_entry_candidate_expansion as expansion
from watcher_foundation import day49_positive_entry_candidate_expansion_validator as validator


class Day49PositiveEntryCandidateExpansionTests(unittest.TestCase):
    def test_manifest_freezes_unused_development_candidates_deterministically(self):
        manifest = expansion.build_manifest(
            source_commit="testsha",
            run_timestamp="2026-06-20T00:00:00Z",
        )

        self.assertEqual([], validator.validate_manifest_document(manifest))
        self.assertEqual(manifest["deterministic_selection"]["result"], "PASS")
        self.assertEqual(manifest["source_pool_count"], 24)
        self.assertEqual(manifest["candidate_count"], 8)
        self.assertFalse(manifest["proof_accepted"])
        self.assertFalse(manifest["profitability_claimed"])

        selected_ids = {row["candidate_identifier"] for row in manifest["candidates"]}
        self.assertEqual(
            selected_ids,
            {
                "GLD-REPLACEMENT-IDEAL-CANDIDATE-001",
                "GLD-REPLACEMENT-IDEAL-CANDIDATE-002",
                "SPY-SOURCE-WINDOW-CLEAN-FAST-BREAK-003",
                "IWM-REPLACEMENT-CONTINUATION-CANDIDATE-001",
                "IWM-REPLACEMENT-CONTINUATION-CANDIDATE-002",
                "SPY-SOURCE-WINDOW-CONTINUATION-004",
                "QQQ-SOURCE-WINDOW-CONTINUATION-002",
                "SPY-SOURCE-WINDOW-CONTINUATION-005",
            },
        )

    def test_manifest_excludes_existing_controls_duplicates_and_drop_rows(self):
        manifest = expansion.build_manifest(
            source_commit="testsha",
            run_timestamp="2026-06-20T00:00:00Z",
        )
        exclusions = {
            row["candidate_identifier"]: row["exclusion_reason"]
            for row in manifest["exclusions"]
        }

        self.assertEqual(
            exclusions["SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002"],
            "existing_measured_funnel_or_positive_rejection_control",
        )
        self.assertEqual(
            exclusions["QQQ-SOURCE-WINDOW-CLEAN-FAST-BREAK-002"],
            "duplicate_signal_same_underlying_opportunity",
        )
        self.assertEqual(
            exclusions["SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-001"],
            "dropped_from_current_proof_path_before_this_task",
        )

    def test_expansion_result_keeps_missing_data_separate_from_true_no_trade(self):
        document = expansion.build_expansion_document(
            source_commit="testsha",
            run_timestamp="2026-06-20T00:00:00Z",
        )

        self.assertEqual([], validator.validate_result_document(document))
        self.assertEqual(document["deterministic_comparison"]["result"], "PASS")
        self.assertEqual(document["existing_regression_control_result"]["candidate_count"], 15)

        combined = document["new_combined_scorecard"]
        self.assertEqual(combined["candidates_found"], 8)
        self.assertEqual(combined["setup_developing_count"], 8)
        self.assertEqual(combined["setup_qualified_count"], 0)
        self.assertEqual(combined["trade_candidate_count"], 0)
        self.assertEqual(combined["contracts_selected"], 0)
        self.assertEqual(combined["valid_trades_captured"], 0)
        self.assertEqual(combined["true_no_trades"], 0)
        self.assertEqual(combined["missing_data_cases"], 8)
        self.assertEqual(combined["missed_valid_trades"], 0)
        self.assertEqual(combined["invalid_trades_allowed"], 0)
        self.assertEqual(combined["unresolved_cases"], 0)
        self.assertEqual(combined["winners"], 0)
        self.assertEqual(combined["losers"], 0)
        self.assertFalse(document["setup_time_request_package"]["request_created"])
        self.assertEqual(document["setup_time_request_package"]["checked_cost"], "NOT_AVAILABLE")

    def test_family_scorecards_are_split_for_new_candidates(self):
        document = expansion.build_expansion_document(
            source_commit="testsha",
            run_timestamp="2026-06-20T00:00:00Z",
        )

        self.assertEqual(document["new_family_scorecards"]["Ideal"]["candidates_found"], 2)
        self.assertEqual(
            document["new_family_scorecards"]["Clean Fast Break"]["candidates_found"],
            1,
        )
        self.assertEqual(
            document["new_family_scorecards"]["Continuation"]["candidates_found"],
            5,
        )

    def test_file_writers_create_machine_readable_manifest_and_result(self):
        root = Path(__file__).resolve().parents[1]
        manifest_path = root / "historical_signal_replay" / "fixtures" / "test_day49_manifest_tmp.json"
        result_path = root / "historical_signal_replay" / "results" / "test_day49_expansion_tmp.json"
        try:
            manifest = expansion.write_manifest(
                manifest_path,
                source_commit="testsha",
                run_timestamp="2026-06-20T00:00:00Z",
            )
            result = expansion.write_expansion_document(
                result_path,
                source_commit="testsha",
                run_timestamp="2026-06-20T00:00:00Z",
            )
            loaded_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            loaded_result = json.loads(result_path.read_text(encoding="utf-8"))
        finally:
            if manifest_path.exists():
                manifest_path.unlink()
            if result_path.exists():
                result_path.unlink()

        self.assertEqual(manifest, loaded_manifest)
        self.assertEqual(result, loaded_result)
        self.assertEqual([], validator.validate_manifest_document(loaded_manifest))
        self.assertEqual([], validator.validate_result_document(loaded_result))


if __name__ == "__main__":
    unittest.main()
