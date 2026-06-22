import json
import unittest
from pathlib import Path
from unittest import mock

from historical_signal_replay import (
    day50_end_to_end_raw_data_positive_entry_generation as generation,
)
from watcher_foundation import (
    day50_end_to_end_raw_data_positive_entry_generation_validator as validator,
)


class Day50EndToEndRawDataPositiveEntryGenerationTests(unittest.TestCase):
    def _document(self):
        with mock.patch.object(generation.day50_underlying, "load_download_manifest", return_value=None):
            return generation.build_generation_document(
                source_commit="testsha",
                run_timestamp="2026-06-21T00:00:00Z",
                check_cost=False,
            )

    def test_inventory_includes_tracked_and_ignored_underlying_data(self):
        document = self._document()
        inventory = document["raw_data_inventory"]

        self.assertEqual(inventory["inventory_status"], "complete_local_tracked_and_ignored_inventory")
        tracked = [
            item
            for item in inventory["underlying_files"]
            if item["tracked_or_ignored"] == "tracked"
        ]
        ignored = [
            item
            for item in inventory["underlying_files"]
            if item["tracked_or_ignored"] == "ignored_local_raw_data"
        ]
        self.assertGreaterEqual(len(tracked), 4)
        self.assertGreaterEqual(len(ignored), 7)
        self.assertTrue(inventory["ignored_local_raw_data_included"])
        for item in inventory["underlying_files"]:
            self.assertIn("path", item)
            self.assertIn("symbol", item)
            self.assertIn("timestamp_start", item)
            self.assertIn("timestamp_end", item)
            self.assertIn("bar_or_event_resolution", item)

    def test_raw_opportunities_are_rejected_with_exact_field_requirements(self):
        document = self._document()

        self.assertEqual(document["result_version"], generation.RESULT_VERSION)
        self.assertGreater(document["raw_opportunities_inspected"], 0)
        self.assertEqual(document["new_candidate_scorecard"]["candidates_generated"], 0)
        self.assertEqual(document["new_candidate_scorecard"]["setup_qualified_candidates"], 0)
        self.assertEqual(document["new_candidate_scorecard"]["trade_candidates"], 0)
        self.assertEqual(document["new_candidate_scorecard"]["selected_contracts"], 0)
        self.assertEqual(document["new_candidate_scorecard"]["eligible_entries"], 0)
        self.assertEqual(document["new_candidate_scorecard"]["recorded_entries"], 0)
        for opportunity in document["rejected_raw_data_opportunities"]:
            self.assertFalse(opportunity["candidate_generated"])
            self.assertIn(
                opportunity["exclusion_reason"],
                {
                    "underlying_resolution_insufficient_for_exact_setup_trigger",
                    "setup_time_replay_mapping_not_established",
                },
            )
            self.assertIn("trigger", opportunity["exact_failed_fields"])
            self.assertIn("no_hindsight_boundary", opportunity["exact_failed_fields"])
            self.assertIn("Databento DBEQ.BASIC / ohlcv-1m", opportunity["required_source"])

    def test_minimum_requirements_are_mapped_to_local_consumers(self):
        document = self._document()
        requirements = document["minimum_underlying_data_requirements"]
        by_family = {
            family: [
                item
                for item in requirements
                if item["setup_family"] == family
            ]
            for family in generation.SETUP_FAMILIES
        }

        for family, items in by_family.items():
            self.assertGreaterEqual(len(items), 8)
            self.assertTrue(
                all(item["minimum_resolution"] == "1m_rth_or_finer" for item in items)
            )
            consumers = {item["field_identifier"] for item in items}
            self.assertIn("setup_time_row", consumers)
            self.assertIn("trigger", consumers)
            self.assertIn("invalidation", consumers)
            self.assertIn("session_boundary_behavior", consumers)

    def test_generation_and_funnel_are_deterministic_across_two_runs(self):
        document = self._document()

        self.assertEqual(document["deterministic_comparison"]["result"], "PASS")
        self.assertEqual(
            document["full_trade_funnel_first_run"],
            document["full_trade_funnel_second_run"],
        )
        self.assertEqual(document["first_run_hash"], document["second_run_hash"])

    def test_exact_grouped_underlying_request_is_smallest_earliest_setup_time_request(self):
        document = self._document()
        request = document["exact_grouped_underlying_data_request"]

        self.assertTrue(request["created"])
        self.assertEqual(request["request_type"], "underlying_setup_time_data")
        self.assertEqual(request["symbols"], ["SPY"])
        self.assertEqual(request["dataset"], "DBEQ.BASIC")
        self.assertEqual(request["schema"], "ohlcv-1m")
        self.assertEqual(request["stype_in"], "raw_symbol")
        self.assertEqual(len(request["windows"]), 1)
        self.assertEqual(request["windows"][0]["start_timestamp"], "2026-03-16T09:30:00-04:00")
        self.assertEqual(request["windows"][0]["end_timestamp"], "2026-03-16T16:00:00-04:00")
        self.assertIn("setup_time_row", request["field_consumers"])
        self.assertIn("Ideal", request["setup_family_decisions_resolved"])
        self.assertIn("Clean Fast Break", request["setup_family_decisions_resolved"])
        self.assertIn("Continuation", request["setup_family_decisions_resolved"])
        self.assertFalse(request["downloaded"])

    def test_acquired_one_minute_evidence_is_inventoried_but_not_promoted_to_candidate(self):
        manifest = {
            "actual_billed_cost": "NOT_AVAILABLE",
            "downloaded_request": {
                "csv_path": (
                    "historical_signal_replay/source_data/external_underlying_data_drop/"
                    "SAFE_FAST_DAY50-RAW-POSITIVE-ENTRY-SPY-2026-03-16-DBEQ-BASIC-OHLCV-1M.csv"
                ),
                "row_count": 390,
            },
            "problems": [],
        }
        source = {
            "path": manifest["downloaded_request"]["csv_path"],
            "complete_chronological_rows": True,
            "tracked_or_ignored": "ignored_local_raw_data",
            "symbol": "SPY",
            "timestamp_start": "2026-03-16T14:30:00.000000000Z",
            "timestamp_end": "2026-03-16T19:59:00.000000000Z",
            "supports_exact_underlying_setup_time_evidence": True,
            "limitation": "one-minute evidence present but setup replay mapping missing",
        }

        opportunity = generation._rejected_opportunity(
            source,
            "Clean Fast Break",
            "DAY50-RAW-SPY-CLEAN-FAST-BREAK-2026-03-16T14:30:00.000000000Z-2026-03-16T19:59:00.000000000Z",
        )

        self.assertTrue(opportunity["underlying_setup_time_evidence_supplied"])
        self.assertEqual(
            opportunity["exclusion_reason"],
            "setup_time_replay_mapping_not_established",
        )
        self.assertIn("SAFE-FAST frozen local replay/calculators", opportunity["required_source"])

    def test_existing_regression_controls_are_reported_separately(self):
        document = self._document()
        existing = document["existing_regression_result"]

        self.assertEqual(existing["day50_evidence_backed_batch"]["setup_qualified_candidates"], 13)
        self.assertEqual(existing["day50_evidence_backed_batch"]["trade_candidates"], 9)
        self.assertEqual(existing["day50_evidence_backed_batch"]["selected_contracts"], 5)
        self.assertEqual(existing["day50_evidence_backed_batch"]["eligible_entries"], 1)
        self.assertEqual(existing["day50_evidence_backed_batch"]["recorded_entries"], 1)
        self.assertTrue(existing["day48_deterministic"])

    def test_policy_blocks_downloads_auth_and_readiness_claims(self):
        document = self._document()
        policy = document["generation_policy"]

        self.assertFalse(policy["future_option_performance_used"])
        self.assertFalse(policy["outcome_data_used_for_candidate_selection"])
        self.assertFalse(policy["frozen_rules_changed"])
        self.assertFalse(policy["main_py_changed"])
        self.assertFalse(policy["railway_or_deploy_changed"])
        self.assertFalse(document["databento_downloaded"])
        self.assertFalse(document["schwab_authenticated"])
        self.assertFalse(document["broker_mutation_attempted"])
        self.assertFalse(document["proof_accepted"])
        self.assertFalse(document["profitability_claimed"])
        self.assertFalse(document["paper_eligible"])
        self.assertFalse(document["live_eligible"])

    def test_writer_creates_result_and_manifest(self):
        root = Path(__file__).resolve().parents[1]
        result_path = root / "historical_signal_replay" / "results" / "test_day50_raw_generation.json"
        manifest_path = (
            root
            / "historical_signal_replay"
            / "fixtures"
            / "test_day50_raw_manifest.json"
        )
        original_result = generation.RESULT_PATH
        original_manifest = generation.MANIFEST_PATH
        try:
            generation.RESULT_PATH = result_path
            generation.MANIFEST_PATH = manifest_path
            with mock.patch.object(
                generation.day50_underlying, "load_download_manifest", return_value=None
            ):
                written = generation.write_generation_outputs(check_cost=False)
            loaded_result = json.loads(result_path.read_text(encoding="utf-8"))
            loaded_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        finally:
            generation.RESULT_PATH = original_result
            generation.MANIFEST_PATH = original_manifest
            if result_path.exists():
                result_path.unlink()
            if manifest_path.exists():
                manifest_path.unlink()

        self.assertEqual(written, loaded_result)
        self.assertEqual(written["candidate_manifest"], loaded_manifest)

    def test_validator_accepts_written_result_and_manifest(self):
        root = Path(__file__).resolve().parents[1]
        result_path = root / "historical_signal_replay" / "results" / "test_day50_raw_generation.json"
        manifest_path = (
            root
            / "historical_signal_replay"
            / "fixtures"
            / "test_day50_raw_manifest.json"
        )
        original_result = generation.RESULT_PATH
        original_manifest = generation.MANIFEST_PATH
        try:
            generation.RESULT_PATH = result_path
            generation.MANIFEST_PATH = manifest_path
            with mock.patch.object(
                generation.day50_underlying, "load_download_manifest", return_value=None
            ):
                generation.write_generation_outputs(check_cost=False)
            validation = validator.validate_result_document(result_path, manifest_path)
        finally:
            generation.RESULT_PATH = original_result
            generation.MANIFEST_PATH = original_manifest
            if result_path.exists():
                result_path.unlink()
            if manifest_path.exists():
                manifest_path.unlink()

        self.assertEqual(validation["status"], "PASS")
        self.assertEqual(validation["problems"], [])


if __name__ == "__main__":
    unittest.main()
