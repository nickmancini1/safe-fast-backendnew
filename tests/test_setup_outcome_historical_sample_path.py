import copy
import unittest
from unittest.mock import patch

from watcher_foundation import (
    FIRST_CONTROLLED_HISTORICAL_SAMPLE_EVIDENCE_SET_ID,
    HISTORICAL_SAMPLE_PATH_OUTPUT_REVIEW_RESULT_FIELDS,
    HISTORICAL_SAMPLE_PATH_RESULT_FIELDS,
    build_first_controlled_historical_sample_evidence_set,
    review_first_controlled_historical_sample_path_output,
    review_setup_outcome_historical_sample_path_output,
    run_setup_outcome_historical_sample_path,
)
from watcher_foundation import setup_outcome_historical_sample_path as sample_path_module


class SetupOutcomeHistoricalSamplePathTests(unittest.TestCase):
    def _unavailable_item(self, field_name):
        return {
            "field_name": field_name,
            "status": "unavailable_evidence",
            "reason": "caller did not provide source-backed setup outcome evidence",
            "fabricated": False,
        }

    def _record(self, **overrides):
        record = {
            "proof_record_id": "proof-row-1",
            "source_record_id": "detected-row-1",
            "setup_id": "setup-1",
            "setup_type": "Ideal",
            "symbol": "SPY",
            "timeframe": "1h_rth",
            "stage": "near-trigger",
            "detection_timestamp": "2026-05-24T09:35:00-04:00",
            "frozen_setup_identity": {
                "caller_provided": True,
                "frozen_before_outcome_scan": True,
                "setup_id": "setup-1",
                "setup_type": "Ideal",
                "symbol": "SPY",
                "frozen_timestamp": "2026-05-24T09:35:00-04:00",
            },
            "setup_evidence_refs": ["detected-row-1", "setup-chart-row-218"],
            "after_setup_evidence": {
                "caller_provided": True,
                "start_timestamp": "2026-05-24T10:30:00-04:00",
                "end_timestamp": "2026-05-25T16:00:00-04:00",
                "source_row_reference": "chart-row-219",
                "post_setup_evidence": ["chart-row-219", "chart-row-220"],
                "future_evidence_used_to_define_setup": False,
            },
            "trigger_state": "triggered",
            "invalidation_state": "valid_by_rule",
            "freshness_state": "fresh",
            "blocker_caution_state": "none",
            "session_boundary_state": "valid_by_rule",
            "outcome_evidence_state": "valid_by_rule",
            "outcome_result_state": "worked",
            "evidence_refs": ["detected-row-1", "chart-row-219"],
            "unavailable_fields": [],
            "diagnostic_placeholders": {
                "next_fix_path": "review outcome proof contract if evidence is incomplete",
                "lower_tier_handoff": "not_required_for_complete_evidence",
            },
            "no_hindsight_boundary": {
                "setup_identity_frozen_before_outcome_scan": True,
                "future_evidence_not_used_to_define_setup": True,
                "no_backfilled_outcome_labels": True,
            },
            "no_trade_boundary": {
                "no_trade": True,
                "no_broker": True,
                "no_order": True,
                "no_account_sizing": True,
                "no_option_pnl": True,
                "no_live_trade_decision": True,
                "broker_enabled": False,
                "orders_enabled": False,
                "account_sizing_enabled": False,
                "option_pnl_enabled": False,
                "live_trade_decision_enabled": False,
            },
            "watch_only": True,
        }
        record.update(overrides)
        return record

    def _record_for_setup(self, setup_type, symbol, **overrides):
        record = self._record(
            proof_record_id=(
                f"{setup_type}-{symbol}-"
                f"{overrides.get('proof_record_id', overrides.get('outcome_result_state', 'worked'))}"
            ),
            setup_id=f"{setup_type}-{symbol}-setup",
            setup_type=setup_type,
            symbol=symbol,
        )
        record["frozen_setup_identity"].update(
            {
                "setup_id": record["setup_id"],
                "setup_type": setup_type,
                "symbol": symbol,
            }
        )
        record.update(overrides)
        return record

    def test_runs_caller_provided_in_memory_examples_through_full_chain(self):
        result = run_setup_outcome_historical_sample_path([self._record()])

        self.assertEqual(set(HISTORICAL_SAMPLE_PATH_RESULT_FIELDS), set(result))
        self.assertIs(result["historical_setup_sample_path_only"], True)
        self.assertIs(result["setup_outcome_proof_only"], True)
        self.assertIs(result["setup_outcome_diagnostics_only"], True)
        self.assertIs(result["setup_outcome_evidence_packet_only"], True)
        self.assertIs(result["setup_outcome_packet_readiness_only"], True)
        self.assertIs(result["setup_outcome_review_aggregator_only"], True)
        self.assertIs(result["setup_outcome_review_readiness_only"], True)
        self.assertIs(result["setup_outcome_proof_review_bundle_only"], True)
        self.assertIs(
            result["setup_outcome_proof_review_bundle_readiness_only"],
            True,
        )
        self.assertEqual(result["records_processed"], 1)
        self.assertEqual(result["records_accepted"], 1)
        self.assertEqual(result["proof_chain"]["setup_appeared"][0]["setup_id"], "setup-1")
        self.assertIn("bundle_readiness", result["proof_chain"])

    def test_first_controlled_sample_evidence_set_runs_through_existing_runner(self):
        sample = build_first_controlled_historical_sample_evidence_set()

        result = run_setup_outcome_historical_sample_path(sample)

        self.assertEqual(
            FIRST_CONTROLLED_HISTORICAL_SAMPLE_EVIDENCE_SET_ID,
            "first_controlled_historical_sample_evidence_set_v1",
        )
        self.assertEqual(result["records_processed"], 4)
        self.assertEqual(result["records_accepted"], 4)
        self.assertEqual(result["records_rejected"], 0)
        self.assertEqual(result["outcome_group_counts"]["worked"], 3)
        self.assertGreater(result["outcome_group_counts"]["failed"], 0)
        self.assertEqual(result["outcome_group_counts"]["missing_evidence"], 0)
        self.assertIs(result["historical_setup_sample_path_only"], True)
        self.assertIn("bundle_readiness", result["proof_chain"])

    def test_review_first_controlled_sample_uses_builder_and_runner(self):
        with patch.object(
            sample_path_module,
            "build_first_controlled_historical_sample_evidence_set",
            wraps=sample_path_module.build_first_controlled_historical_sample_evidence_set,
        ) as builder_mock, patch.object(
            sample_path_module,
            "run_setup_outcome_historical_sample_path",
            wraps=sample_path_module.run_setup_outcome_historical_sample_path,
        ) as runner_mock:
            review = review_first_controlled_historical_sample_path_output()

        builder_mock.assert_called_once_with()
        runner_mock.assert_called_once()
        self.assertEqual(
            set(HISTORICAL_SAMPLE_PATH_OUTPUT_REVIEW_RESULT_FIELDS),
            set(review),
        )
        self.assertEqual(
            review["review_conclusion"],
            "useful_but_not_final_viability_proof",
        )

    def test_review_accepts_caller_provided_in_memory_sample_path_output_only(self):
        sample_output = run_setup_outcome_historical_sample_path(
            build_first_controlled_historical_sample_evidence_set()
        )

        review = review_setup_outcome_historical_sample_path_output(sample_output)

        self.assertIs(review["accepted_in_memory_sample_path_output_only"], True)
        self.assertIs(review["historical_sample_path_output_review_only"], True)
        self.assertEqual(len(review["worked_samples"]), 3)
        self.assertEqual(len(review["failed_samples"]), 1)
        self.assertEqual(len(review["inconclusive_samples"]), 0)
        self.assertEqual(review["worked_samples"][0]["setup_type"], "Ideal")
        self.assertEqual(review["worked_samples"][0]["symbol"], "SPY")
        self.assertEqual(
            review["failed_samples"][0]["setup_type"], "Clean Fast Break"
        )
        self.assertEqual(review["failed_samples"][0]["symbol"], "QQQ")
        self.assertIn(
            ("Continuation", "GLD"),
            {
                (sample["setup_type"], sample["symbol"])
                for sample in review["worked_samples"]
            },
        )
        self.assertEqual(review["gld_continuation_review_status"], "reviewable")
        self.assertIs(review["gld_continuation_became_reviewable"], True)
        self.assertIs(review["gld_continuation_remains_inconclusive"], False)
        iwm_samples = [
            sample
            for sample in review["worked_samples"]
            if sample["symbol"] == "IWM"
        ]
        self.assertEqual(len(iwm_samples), 1)
        self.assertEqual(iwm_samples[0]["setup_type"], "Ideal")
        self.assertEqual(review["iwm_review_status"], "reviewable")
        self.assertIs(review["iwm_became_reviewable"], True)
        self.assertIs(review["iwm_remains_inconclusive"], False)
        self.assertEqual(review["iwm_sample_teaches"]["symbol"], "IWM")
        self.assertIn("small-cap IWM", review["iwm_sample_teaches"]["teaches"])

    def test_review_answers_proof_diagnosis_and_missing_evidence_questions(self):
        sample_output = run_setup_outcome_historical_sample_path(
            build_first_controlled_historical_sample_evidence_set()
        )

        review = review_setup_outcome_historical_sample_path_output(sample_output)

        self.assertIs(review["worked_sample_clear_proof"], True)
        self.assertIs(review["failed_sample_useful_diagnosis"], True)
        self.assertIs(review["inconclusive_sample_missing_evidence_clear"], False)
        self.assertEqual(review["gld_continuation_review_status"], "reviewable")
        self.assertEqual(review["iwm_review_status"], "reviewable")
        self.assertIn("worked_chart_behavior", str(review["useful_proof"]))
        self.assertIn(
            "failed_chart_behavior_with_diagnosis",
            str(review["useful_proof"]),
        )
        self.assertIn("bundle_readiness", str(review["weak_proof"]))

    def test_review_preserves_no_hindsight_setup_symbol_pair_and_boundaries(self):
        sample_output = run_setup_outcome_historical_sample_path(
            build_first_controlled_historical_sample_evidence_set()
        )

        review = review_setup_outcome_historical_sample_path_output(sample_output)

        self.assertIs(review["no_hindsight_boundary_preserved"], True)
        self.assertIs(review["setup_type_separated"], True)
        self.assertIs(review["symbol_separated"], True)
        self.assertIs(review["setup_type_symbol_pair_separated"], True)
        self.assertIs(review["boundary_review"]["no_trade_boundary_preserved"], True)
        self.assertIs(
            review["boundary_review"]["no_live_data_boundary_preserved"],
            True,
        )
        self.assertIs(
            review["boundary_review"]["no_controlled_shadow_boundary_preserved"],
            True,
        )
        self.assertIs(review["boundary_review"]["no_alert_boundary_preserved"], True)
        self.assertIs(
            review["boundary_review"]["no_file_write_boundary_preserved"],
            True,
        )
        self.assertIs(review["boundary_review"]["no_broker_boundary_preserved"], True)
        self.assertIs(
            review["boundary_review"]["no_optimization_boundary_preserved"],
            True,
        )
        self.assertIs(review["final_viability_proven"], False)
        self.assertIs(review["profitability_claimed"], False)
        self.assertIs(review["historical_success_claimed"], False)
        self.assertIs(review["optimization_started"], False)
        self.assertIs(review["no_rule_change_started"], True)

    def test_review_surfaces_fix_paths_regression_needs_and_lower_tier_material(self):
        sample_output = run_setup_outcome_historical_sample_path(
            build_first_controlled_historical_sample_evidence_set()
        )

        review = review_setup_outcome_historical_sample_path_output(sample_output)

        self.assertIn(
            "outcome_scoring_review",
            str(review["next_fix_paths"]),
        )
        self.assertNotEqual(
            review["smallest_next_fix_path"]["path"],
            "collect_or_preserve_missing_after_setup_evidence",
        )
        self.assertIn("required_regression_tests", str(review["regression_needs"]))
        self.assertIs(review["result_useful_for_lower_tier_review"], True)
        lower_tier = review["lower_tier_review_summary"]
        self.assertEqual(len(lower_tier["worked_samples"]), 3)
        self.assertEqual(len(lower_tier["failed_samples"]), 1)
        self.assertEqual(len(lower_tier["inconclusive_samples"]), 0)
        self.assertIs(lower_tier["no_trade_watch_only"], True)
        self.assertIs(lower_tier["no_live_data"], True)
        self.assertIs(lower_tier["no_controlled_shadow_data"], True)
        self.assertIs(lower_tier["no_alerts"], True)
        self.assertIs(lower_tier["no_broker"], True)
        self.assertIs(lower_tier["no_file_write"], True)
        self.assertIs(lower_tier["no_rule_change"], True)
        self.assertIs(lower_tier["no_optimization"], True)

    def test_review_rejects_non_output_shape_and_defensively_copies(self):
        with self.assertRaisesRegex(TypeError, "must be a dict"):
            review_setup_outcome_historical_sample_path_output([])
        with self.assertRaisesRegex(ValueError, "Missing historical sample path"):
            review_setup_outcome_historical_sample_path_output({"watch_only": True})

        sample_output = run_setup_outcome_historical_sample_path(
            build_first_controlled_historical_sample_evidence_set()
        )
        before = copy.deepcopy(sample_output)

        review = review_setup_outcome_historical_sample_path_output(sample_output)
        review["worked_samples"][0]["setup_time_evidence_refs"].append("mutated")
        review["diagnostics"][0]["evidence_used"].append("mutated")

        self.assertEqual(sample_output, before)
        second = review_setup_outcome_historical_sample_path_output(sample_output)
        self.assertNotIn(
            "mutated",
            second["worked_samples"][0]["setup_time_evidence_refs"],
        )
        self.assertNotIn("mutated", second["diagnostics"][0]["evidence_used"])

    def test_review_has_no_file_network_subprocess_thread_or_live_side_effects(self):
        sample_output = run_setup_outcome_historical_sample_path(
            build_first_controlled_historical_sample_evidence_set()
        )
        before = copy.deepcopy(sample_output)

        with patch("builtins.open") as open_mock, patch(
            "socket.socket"
        ) as socket_mock, patch("subprocess.run") as subprocess_mock, patch(
            "threading.Thread"
        ) as thread_mock:
            review = review_setup_outcome_historical_sample_path_output(sample_output)

        self.assertEqual(sample_output, before)
        self.assertIs(review["boundary_review"]["live_data_started"], False)
        self.assertIs(
            review["boundary_review"]["controlled_shadow_data_started"],
            False,
        )
        self.assertIs(review["boundary_review"]["alerts_sent"], False)
        self.assertIs(review["boundary_review"]["files_written"], False)
        self.assertIs(
            review["boundary_review"]["broker_or_trade_behavior_enabled"],
            False,
        )
        open_mock.assert_not_called()
        socket_mock.assert_not_called()
        subprocess_mock.assert_not_called()
        thread_mock.assert_not_called()

    def test_first_controlled_sample_preserves_setup_symbol_and_pair_separation(self):
        result = run_setup_outcome_historical_sample_path(
            build_first_controlled_historical_sample_evidence_set()
        )

        self.assertEqual(
            set(result["represented_setup_types"]),
            {"Ideal", "Clean Fast Break", "Continuation"},
        )
        self.assertEqual(set(result["represented_symbols"]), {"SPY", "QQQ", "GLD", "IWM"})
        self.assertEqual(
            {
                (item["setup_type"], item["symbol"])
                for item in result["represented_setup_type_symbol_pairs"]
            },
            {
                ("Ideal", "SPY"),
                ("Clean Fast Break", "QQQ"),
                ("Continuation", "GLD"),
                ("Ideal", "IWM"),
            },
        )
        self.assertIs(result["setup_type_separated"], True)
        self.assertIs(result["symbol_separated"], True)
        self.assertIs(result["setup_type_symbol_pair_separated"], True)

    def test_first_controlled_sample_preserves_no_hindsight_evidence_separation(self):
        result = run_setup_outcome_historical_sample_path(
            build_first_controlled_historical_sample_evidence_set()
        )

        appeared_by_id = {
            item["setup_id"]: item
            for item in result["proof_chain"]["setup_appeared"]
        }
        happened_by_id = {
            item["setup_id"]: item
            for item in result["proof_chain"]["what_happened_after"]
        }

        for setup_id, appeared in appeared_by_id.items():
            self.assertIn("setup_evidence_refs", appeared)
            self.assertIn("frozen_setup_identity", appeared)
            self.assertNotIn("after_setup_evidence", appeared)
            self.assertIs(
                appeared["no_hindsight_boundary"][
                    "future_evidence_not_used_to_define_setup"
                ],
                True,
            )

            happened = happened_by_id[setup_id]
            self.assertIn("after_setup_evidence", happened)
            self.assertNotIn("frozen_setup_identity", happened)
            self.assertIs(
                happened["after_setup_evidence"][
                    "future_evidence_used_to_define_setup"
                ],
                False,
            )

    def test_first_controlled_sample_adds_gld_after_setup_evidence_without_fabrication(self):
        result = run_setup_outcome_historical_sample_path(
            build_first_controlled_historical_sample_evidence_set()
        )

        self.assertNotIn("Continuation", result["missing_evidence_by_setup_type"])
        self.assertNotIn("GLD", result["missing_evidence_by_symbol"])
        happened_by_pair = {
            (item["setup_type"], item["symbol"]): item
            for item in result["proof_chain"]["what_happened_after"]
        }
        gld = happened_by_pair[("Continuation", "GLD")]
        self.assertEqual(gld["outcome_result_state"], "worked")
        self.assertEqual(gld["outcome_evidence_state"], "valid_by_rule")
        self.assertIn("source_row_reference", gld["after_setup_evidence"])
        self.assertIn("post_setup_evidence", gld["after_setup_evidence"])
        self.assertIs(
            gld["after_setup_evidence"]["future_evidence_used_to_define_setup"],
            False,
        )
        self.assertNotIn("fabricated': True", str(result["missing_evidence"]))

    def test_first_controlled_sample_adds_exactly_one_iwm_reviewable_example(self):
        sample = build_first_controlled_historical_sample_evidence_set()

        iwm_records = [record for record in sample if record["symbol"] == "IWM"]

        self.assertEqual(len(iwm_records), 1)
        iwm_record = iwm_records[0]
        self.assertEqual(iwm_record["setup_type"], "Ideal")
        self.assertEqual(iwm_record["setup_id"], "controlled-ideal-iwm-001")
        self.assertEqual(
            iwm_record["after_setup_evidence"]["source_row_reference"],
            "controlled-source-iwm-ideal-001:after-row-1",
        )
        self.assertTrue(iwm_record["after_setup_evidence"]["post_setup_evidence"])
        self.assertIs(
            iwm_record["after_setup_evidence"][
                "future_evidence_used_to_define_setup"
            ],
            False,
        )

        result = run_setup_outcome_historical_sample_path(sample)
        happened_by_pair = {
            (item["setup_type"], item["symbol"]): item
            for item in result["proof_chain"]["what_happened_after"]
        }
        iwm = happened_by_pair[("Ideal", "IWM")]
        self.assertEqual(iwm["outcome_result_state"], "worked")
        self.assertEqual(iwm["outcome_evidence_state"], "valid_by_rule")
        self.assertIn("source_row_reference", iwm["after_setup_evidence"])
        self.assertIn("post_setup_evidence", iwm["after_setup_evidence"])
        self.assertIs(
            iwm["after_setup_evidence"]["future_evidence_used_to_define_setup"],
            False,
        )
        self.assertNotIn("IWM", result["missing_evidence_by_symbol"])

    def test_review_reports_what_iwm_sample_teaches_without_viability_claim(self):
        sample_output = run_setup_outcome_historical_sample_path(
            build_first_controlled_historical_sample_evidence_set()
        )

        review = review_setup_outcome_historical_sample_path_output(sample_output)

        self.assertEqual(review["iwm_review_status"], "reviewable")
        self.assertIs(review["iwm_became_reviewable"], True)
        self.assertIs(review["iwm_remains_inconclusive"], False)
        self.assertEqual(review["iwm_sample_teaches"]["setup_type"], "Ideal")
        self.assertEqual(review["iwm_sample_teaches"]["symbol"], "IWM")
        self.assertEqual(
            review["iwm_sample_teaches"]["setup_type_symbol_pair"],
            {"setup_type": "Ideal", "symbol": "IWM"},
        )
        self.assertIn("small-cap IWM", review["iwm_sample_teaches"]["teaches"])
        self.assertIs(review["iwm_sample_teaches"]["profitability_claimed"], False)
        self.assertIs(review["iwm_sample_teaches"]["final_viability_proven"], False)
        self.assertIs(review["iwm_sample_teaches"]["optimization_started"], False)
        self.assertIs(review["final_viability_proven"], False)
        self.assertIs(review["profitability_claimed"], False)
        self.assertIs(review["historical_success_claimed"], False)
        self.assertIs(review["optimization_started"], False)

    def test_first_controlled_sample_preserves_boundaries_and_no_profitability_claim(self):
        result = run_setup_outcome_historical_sample_path(
            build_first_controlled_historical_sample_evidence_set()
        )
        summary = result["lower_tier_review_summary"]

        self.assertIs(result["watch_only"], True)
        self.assertIs(result["final_viability_proven"], False)
        self.assertIs(result["profitability_claimed"], False)
        self.assertIs(result["optimization_started"], False)
        self.assertIs(result["no_rule_change_started"], True)
        self.assertIs(result["no_trade_boundary_preserved"], True)
        self.assertIs(result["no_live_data_boundary_preserved"], True)
        self.assertIs(result["no_controlled_shadow_boundary_preserved"], True)
        self.assertIs(result["no_alert_boundary_preserved"], True)
        self.assertIs(result["no_file_write_boundary_preserved"], True)
        self.assertIs(result["no_broker_boundary_preserved"], True)
        self.assertIs(result["no_optimization_boundary_preserved"], True)
        self.assertIs(summary["no_trade_watch_only"], True)
        self.assertIs(summary["no_live_data"], True)
        self.assertIs(summary["no_alerts"], True)
        self.assertIs(summary["no_broker"], True)
        self.assertIs(summary["no_file_write"], True)
        self.assertIs(summary["no_rule_change"], True)
        self.assertIs(summary["no_optimization"], True)
        self.assertNotIn("profitability_score", result)

    def test_first_controlled_sample_builder_has_no_side_effects(self):
        with patch("builtins.open") as open_mock, patch(
            "socket.socket"
        ) as socket_mock, patch("subprocess.run") as subprocess_mock, patch(
            "threading.Thread"
        ) as thread_mock:
            first = build_first_controlled_historical_sample_evidence_set()
            first[0]["setup_evidence_refs"].append("mutated")
            second = build_first_controlled_historical_sample_evidence_set()

        self.assertNotIn("mutated", second[0]["setup_evidence_refs"])
        open_mock.assert_not_called()
        socket_mock.assert_not_called()
        subprocess_mock.assert_not_called()
        thread_mock.assert_not_called()

    def test_rejects_non_memory_path_live_alert_broker_and_trade_inputs(self):
        forbidden_cases = (
            {"file_path": "sample.json"},
            {"generated_report_path": "reports/out.json"},
            {"raw_log_path": "logs/raw.jsonl"},
            {"live_data": {"symbol": "SPY"}},
            {"controlled_shadow_data": {"symbol": "SPY"}},
            {"alert": "send"},
            {"broker_order": "blocked"},
            {"account_sizing": "blocked"},
            {"option_pnl": 10},
            {"live_trade_decision": "approve"},
            {"source": "main.py"},
        )

        for forbidden in forbidden_cases:
            record = self._record(nested=forbidden)
            with self.subTest(forbidden=forbidden):
                with self.assertRaisesRegex(ValueError, "Forbidden sample path"):
                    run_setup_outcome_historical_sample_path([record])

    def test_rejects_invalid_input_type(self):
        with self.assertRaisesRegex(TypeError, "must be a list"):
            run_setup_outcome_historical_sample_path({"not": "a list"})

    def test_preserves_no_hindsight_separation(self):
        result = run_setup_outcome_historical_sample_path([self._record()])

        appeared = result["proof_chain"]["setup_appeared"][0]
        happened = result["proof_chain"]["what_happened_after"][0]
        self.assertEqual(appeared["setup_evidence_refs"], ["detected-row-1", "setup-chart-row-218"])
        self.assertNotIn("after_setup_evidence", appeared)
        self.assertEqual(
            happened["after_setup_evidence"]["start_timestamp"],
            "2026-05-24T10:30:00-04:00",
        )
        self.assertNotIn("frozen_setup_identity", happened)
        self.assertIs(result["no_hindsight_boundary_preserved"], True)

    def test_preserves_setup_type_symbol_and_pair_separation(self):
        result = run_setup_outcome_historical_sample_path(
            [
                self._record_for_setup("Ideal", "SPY"),
                self._record_for_setup("Ideal", "QQQ"),
                self._record_for_setup("Continuation", "SPY"),
            ]
        )

        self.assertEqual(set(result["represented_setup_types"]), {"Ideal", "Continuation"})
        self.assertEqual(set(result["represented_symbols"]), {"SPY", "QQQ"})
        self.assertIn(
            {"setup_type": "Ideal", "symbol": "QQQ"},
            result["represented_setup_type_symbol_pairs"],
        )
        self.assertIs(result["setup_type_separated"], True)
        self.assertIs(result["symbol_separated"], True)
        self.assertIs(result["setup_type_symbol_pair_separated"], True)

    def test_carries_all_chart_outcome_groups_without_profitability_claim(self):
        records = [
            self._record_for_setup("Ideal", "SPY", outcome_result_state="worked"),
            self._record_for_setup("Ideal", "QQQ", outcome_result_state="failed"),
            self._record_for_setup(
                "Continuation",
                "SPY",
                proof_record_id="pending",
                setup_id="pending-setup",
                trigger_state="not_triggered",
                outcome_result_state="pending",
                frozen_setup_identity={
                    "caller_provided": True,
                    "frozen_before_outcome_scan": True,
                    "setup_id": "pending-setup",
                    "setup_type": "Continuation",
                    "symbol": "SPY",
                    "frozen_timestamp": "2026-05-24T09:35:00-04:00",
                },
            ),
            self._record_for_setup(
                "Clean Fast Break",
                "SPY",
                proof_record_id="stale",
                setup_id="stale-setup",
                trigger_state="not_triggered",
                freshness_state="stale",
                outcome_result_state="none",
                frozen_setup_identity={
                    "caller_provided": True,
                    "frozen_before_outcome_scan": True,
                    "setup_id": "stale-setup",
                    "setup_type": "Clean Fast Break",
                    "symbol": "SPY",
                    "frozen_timestamp": "2026-05-24T09:35:00-04:00",
                },
            ),
            self._record_for_setup(
                "Ideal",
                "SPY",
                proof_record_id="invalidated",
                setup_id="invalidated-setup",
                trigger_state="not_triggered",
                invalidation_state="invalidated",
                outcome_result_state="none",
                frozen_setup_identity={
                    "caller_provided": True,
                    "frozen_before_outcome_scan": True,
                    "setup_id": "invalidated-setup",
                    "setup_type": "Ideal",
                    "symbol": "SPY",
                    "frozen_timestamp": "2026-05-24T09:35:00-04:00",
                },
            ),
            self._record_for_setup(
                "Ideal",
                "QQQ",
                proof_record_id="inconclusive",
                setup_id="inconclusive-setup",
                outcome_result_state="inconclusive",
                frozen_setup_identity={
                    "caller_provided": True,
                    "frozen_before_outcome_scan": True,
                    "setup_id": "inconclusive-setup",
                    "setup_type": "Ideal",
                    "symbol": "QQQ",
                    "frozen_timestamp": "2026-05-24T09:35:00-04:00",
                },
            ),
            self._record_for_setup(
                "Continuation",
                "QQQ",
                proof_record_id="missing",
                setup_id="missing-setup",
                outcome_evidence_state="missing_evidence",
                unavailable_fields=[self._unavailable_item("post_setup_evidence")],
                frozen_setup_identity={
                    "caller_provided": True,
                    "frozen_before_outcome_scan": True,
                    "setup_id": "missing-setup",
                    "setup_type": "Continuation",
                    "symbol": "QQQ",
                    "frozen_timestamp": "2026-05-24T09:35:00-04:00",
                },
            ),
        ]
        del records[-1]["after_setup_evidence"]["post_setup_evidence"]

        result = run_setup_outcome_historical_sample_path(records)

        for group_name in (
            "worked",
            "failed",
            "inconclusive",
            "pending",
            "stale",
            "invalidated",
            "missing_evidence",
        ):
            self.assertGreater(result["outcome_group_counts"][group_name], 0)
        self.assertIs(result["profitability_claimed"], False)
        self.assertIs(result["final_viability_proven"], False)
        self.assertNotIn("success_score", result)
        self.assertNotIn("combined_viability_score", result)

    def test_identifies_missing_evidence_diagnostics_fix_paths_and_regressions(self):
        record = self._record_for_setup(
            "Continuation",
            "GLD",
            outcome_evidence_state="unavailable_evidence",
            unavailable_fields=[self._unavailable_item("source_row_reference")],
        )

        result = run_setup_outcome_historical_sample_path([record])

        self.assertTrue(result["missing_evidence"])
        self.assertIn("Continuation", result["missing_evidence_by_setup_type"])
        self.assertIn("GLD", result["missing_evidence_by_symbol"])
        self.assertIn(
            {"setup_type": "Continuation", "symbol": "GLD"},
            [
                {"setup_type": item["setup_type"], "symbol": item["symbol"]}
                for item in result["missing_evidence_by_setup_type_symbol_pair"]
            ],
        )
        self.assertTrue(result["diagnostics"])
        self.assertIn("data_quality_or_missing_evidence", str(result["diagnostics"]))
        self.assertTrue(result["next_fix_paths"])
        self.assertTrue(result["regression_needs"])

    def test_lower_tier_summary_preserves_boundaries_and_not_ready_state(self):
        result = run_setup_outcome_historical_sample_path([self._record()])
        summary = result["lower_tier_review_summary"]

        self.assertIn(summary["bundle_readiness_decision"], {
            "needs_more_evidence_before_lower_tier_review",
            "blocked_by_bundle_readiness_contract_gap",
            "ready_for_lower_tier_review",
        })
        self.assertIs(summary["no_trade_watch_only"], True)
        self.assertIs(summary["no_live_data"], True)
        self.assertIs(summary["no_alerts"], True)
        self.assertIs(summary["no_broker"], True)
        self.assertIs(summary["no_file_write"], True)
        self.assertIs(summary["no_rule_change"], True)
        self.assertIs(summary["no_optimization"], True)
        self.assertIs(summary["final_viability_proven"], False)
        self.assertIs(summary["profitability_claimed"], False)

    def test_rejected_records_run_through_chain_as_lower_tier_contract_gap(self):
        result = run_setup_outcome_historical_sample_path(
            [self._record(watch_only=False)]
        )

        self.assertEqual(result["records_processed"], 1)
        self.assertEqual(result["records_accepted"], 0)
        self.assertEqual(result["records_rejected"], 1)
        self.assertIn("watch_only=True", str(result["proof_chain"]))
        self.assertTrue(result["lower_tier_review_summary"]["exact_missing_review_items"])

    def test_defensive_copy_behavior(self):
        record = self._record()
        before = copy.deepcopy(record)

        result = run_setup_outcome_historical_sample_path([record])
        result["proof_chain"]["setup_appeared"][0]["setup_evidence_refs"].append("mutated")
        result["diagnostics"][0]["evidence_used"].append("mutated")
        result["lower_tier_review_summary"]["exact_missing_review_items"].append("mutated")

        self.assertEqual(record, before)
        second = run_setup_outcome_historical_sample_path([record])
        self.assertNotIn("mutated", second["proof_chain"]["setup_appeared"][0]["setup_evidence_refs"])
        self.assertNotIn("mutated", second["diagnostics"][0]["evidence_used"])

    def test_no_file_network_subprocess_thread_or_live_side_effects(self):
        record = self._record()
        before = copy.deepcopy(record)

        with patch("builtins.open") as open_mock, patch(
            "socket.socket"
        ) as socket_mock, patch("subprocess.run") as subprocess_mock, patch(
            "threading.Thread"
        ) as thread_mock:
            result = run_setup_outcome_historical_sample_path([record])

        self.assertEqual(record, before)
        self.assertIs(result["no_trade_boundary_preserved"], True)
        self.assertIs(result["no_live_data_boundary_preserved"], True)
        self.assertIs(result["no_controlled_shadow_boundary_preserved"], True)
        self.assertIs(result["no_alert_boundary_preserved"], True)
        self.assertIs(result["no_file_write_boundary_preserved"], True)
        self.assertIs(result["no_broker_boundary_preserved"], True)
        self.assertIs(result["no_optimization_boundary_preserved"], True)
        self.assertIs(result["live_data_started"], False)
        self.assertIs(result["controlled_shadow_data_started"], False)
        self.assertIs(result["alerts_sent"], False)
        self.assertIs(result["files_written"], False)
        self.assertIs(result["broker_or_trade_behavior_enabled"], False)
        open_mock.assert_not_called()
        socket_mock.assert_not_called()
        subprocess_mock.assert_not_called()
        thread_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
