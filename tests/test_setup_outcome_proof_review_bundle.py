import copy
import unittest
from unittest.mock import patch

from watcher_foundation import (
    SETUP_OUTCOME_PROOF_REVIEW_BUNDLE_DECISIONS,
    SETUP_OUTCOME_PROOF_REVIEW_BUNDLE_RESULT_FIELDS,
    aggregate_setup_outcome_proof_review,
    build_setup_outcome_evidence_packet,
    build_setup_outcome_proof_review_bundle,
    evaluate_setup_outcome_diagnostics,
    evaluate_setup_outcome_packet_readiness,
    evaluate_setup_outcome_proof,
    evaluate_setup_outcome_review_readiness,
)


class SetupOutcomeProofReviewBundleTests(unittest.TestCase):
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
                f"{overrides.get('outcome_result_state', 'worked')}"
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

    def _packet(self, records=None):
        if records is None:
            records = [self._record()]
        proof = evaluate_setup_outcome_proof(records)
        diagnostics = evaluate_setup_outcome_diagnostics(proof)
        return build_setup_outcome_evidence_packet(diagnostics)

    def _review_ready_packet(self, records=None):
        packet = self._packet(records)
        for item in packet["packet_items"]:
            item["setup_identifier"] = (
                f"{item['setup_type']}-{item['symbol']}-setup"
                if type(item["setup_type"]) is str and type(item["symbol"]) is str
                else "setup-1"
            )
            item["what_setup_appeared"]["setup_identifier"] = item["setup_identifier"]
            item["missing_evidence"] = []
            item["evidence_state"] = "evidence_supported"
            item["lower_tier_handoff_required"] = False
            item["lower_tier_handoff_reason"] = (
                "not required by complete caller-provided packet"
            )
        packet["missing_evidence"] = []
        packet["lower_tier_handoff_required"] = False
        packet["lower_tier_handoff_items"] = []
        packet["proof_limited_records"] = []
        packet["packet_items_by_setup_type"] = {}
        for item in packet["packet_items"]:
            packet["packet_items_by_setup_type"].setdefault(item["setup_type"], {})
            packet["packet_items_by_setup_type"][item["setup_type"]].setdefault(
                item["symbol"],
                [],
            )
            packet["packet_items_by_setup_type"][item["setup_type"]][
                item["symbol"]
            ].append(copy.deepcopy(item))
        readiness = evaluate_setup_outcome_packet_readiness(packet)
        by_id = {
            item["packet_item_id"]: item["outcome_status"]
            for item in packet["packet_items"]
        }
        for item in readiness["packet_items"]:
            item["outcome_status"] = by_id[item["packet_item_id"]]
        return readiness

    def _aggregate(self, records=None):
        return aggregate_setup_outcome_proof_review(
            [self._review_ready_packet(records)]
        )

    def _full_coverage_aggregate(self):
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
        aggregate = self._aggregate(records)
        aggregate["proof_gaps"] = []
        aggregate["missing_evidence"] = []
        aggregate["readiness_gap_counts"] = {}
        aggregate["repeated_next_fix_paths"] = {}
        aggregate["repeated_regression_needs"] = {}
        aggregate["regression_needed"] = []
        aggregate["lower_tier_handoff_required"] = False
        aggregate["lower_tier_handoff_items"] = []
        aggregate["rejected_records"] = []
        aggregate["proof_limited_records"] = []
        aggregate["sufficient_proof_to_continue_review"] = True
        aggregate["proof_continuation_decision"] = "continue_review_with_ready_packets"
        return aggregate

    def _ready_summary(self):
        return evaluate_setup_outcome_review_readiness(
            self._full_coverage_aggregate()
        )

    def _not_ready_summary_with_missing_evidence(self):
        record = self._record_for_setup(
            "Continuation",
            "QQQ",
            outcome_evidence_state="unavailable_evidence",
            unavailable_fields=[self._unavailable_item("source_row_reference")],
        )
        packet = evaluate_setup_outcome_packet_readiness(self._packet([record]))
        aggregate = aggregate_setup_outcome_proof_review(
            [packet, copy.deepcopy(packet)]
        )
        return evaluate_setup_outcome_review_readiness(aggregate)

    def test_accepts_only_in_memory_review_readiness_summary_list(self):
        result = build_setup_outcome_proof_review_bundle([self._ready_summary()])

        self.assertEqual(set(SETUP_OUTCOME_PROOF_REVIEW_BUNDLE_RESULT_FIELDS), set(result))
        self.assertIn(
            result["bundle_review_decision"],
            SETUP_OUTCOME_PROOF_REVIEW_BUNDLE_DECISIONS,
        )
        self.assertIs(result["watch_only"], True)
        self.assertIs(result["setup_outcome_proof_review_bundle_only"], True)
        self.assertIs(result["setup_outcome_review_readiness_only"], True)
        self.assertIs(result["setup_outcome_review_aggregator_only"], True)
        self.assertIs(result["setup_outcome_packet_readiness_only"], True)
        self.assertIs(result["setup_outcome_evidence_packet_only"], True)
        self.assertIs(result["setup_outcome_diagnostics_only"], True)
        self.assertIs(result["setup_outcome_proof_only"], True)
        self.assertIs(result["final_viability_proven"], False)
        self.assertIs(result["optimization_started"], False)
        self.assertIs(result["no_rule_change_started"], True)

    def test_invalid_input_type_missing_and_unexpected_fields_fail(self):
        with self.assertRaisesRegex(TypeError, "input must be a list"):
            build_setup_outcome_proof_review_bundle({})

        summary = self._ready_summary()
        del summary["reviewed_packets"]
        with self.assertRaisesRegex(ValueError, "reviewed_packets"):
            build_setup_outcome_proof_review_bundle([summary])

        summary = self._ready_summary()
        summary["extra_bundle_source"] = "not allowed"
        with self.assertRaisesRegex(ValueError, "Unexpected"):
            build_setup_outcome_proof_review_bundle([summary])

    def test_required_boundaries_are_enforced(self):
        required_failures = {
            "watch_only": False,
            "setup_outcome_review_readiness_only": False,
            "setup_outcome_review_aggregator_only": False,
            "setup_outcome_packet_readiness_only": False,
            "setup_outcome_evidence_packet_only": False,
            "setup_outcome_diagnostics_only": False,
            "setup_outcome_proof_only": False,
            "final_viability_proven": True,
            "optimization_started": True,
            "no_rule_change_started": False,
            "no_hindsight_boundary_preserved": False,
            "no_trade_boundary_preserved": False,
            "no_live_data_boundary_preserved": False,
            "no_controlled_shadow_boundary_preserved": False,
            "no_alert_boundary_preserved": False,
            "no_file_write_boundary_preserved": False,
            "no_broker_boundary_preserved": False,
            "no_optimization_boundary_preserved": False,
            "live_data_started": True,
            "controlled_shadow_data_started": True,
            "alerts_sent": True,
            "files_written": True,
            "broker_or_trade_behavior_enabled": True,
        }

        for field_name, value in required_failures.items():
            summary = self._ready_summary()
            summary[field_name] = value
            with self.subTest(field_name=field_name):
                with self.assertRaisesRegex(ValueError, field_name):
                    build_setup_outcome_proof_review_bundle([summary])

    def test_includes_ready_reviews_and_preserves_reviewed_packet_identifiers(self):
        result = build_setup_outcome_proof_review_bundle([self._ready_summary()])

        self.assertEqual(result["included_group_review_count"], 1)
        self.assertFalse(result["excluded_group_reviews"])
        self.assertEqual(
            result["included_group_reviews"][0]["reviewed_packets"][0][
                "packet_identifier"
            ],
            "UNAVAILABLE-1",
        )
        self.assertIn("Ideal", result["represented_setup_types"])
        self.assertIn("SPY", result["represented_symbols"])
        self.assertIn(
            {"setup_type": "Continuation", "symbol": "QQQ"},
            result["represented_setup_type_symbol_pairs"],
        )

    def test_excludes_not_ready_reviews_without_fabricating_readiness(self):
        result = build_setup_outcome_proof_review_bundle(
            [self._ready_summary(), self._not_ready_summary_with_missing_evidence()]
        )

        self.assertEqual(result["included_group_review_count"], 1)
        self.assertEqual(len(result["excluded_group_reviews"]), 1)
        self.assertIn(
            "readiness summary",
            result["excluded_group_reviews"][0]["exclusion_reason"],
        )
        self.assertEqual(
            result["bundle_review_decision"],
            "needs_more_evidence_before_lower_tier_review",
        )
        self.assertIs(result["ready_for_lower_tier_review"], False)

    def test_keeps_setup_type_symbol_and_pairs_separate(self):
        result = build_setup_outcome_proof_review_bundle([self._ready_summary()])

        self.assertIs(result["setup_type_separated"], True)
        self.assertIs(result["symbol_separated"], True)
        self.assertIn("Continuation", result["represented_setup_types"])
        self.assertIn("QQQ", result["represented_symbols"])
        self.assertIn(
            {"setup_type": "Continuation", "symbol": "QQQ"},
            result["represented_setup_type_symbol_pairs"],
        )
        self.assertNotIn("Continuation/QQQ", result["represented_setup_types"])

    def test_aggregates_worked_failed_and_unresolved_patterns(self):
        result = build_setup_outcome_proof_review_bundle(
            [self._ready_summary(), self._ready_summary()]
        )

        self.assertEqual(result["outcome_group_counts"]["worked"], 2)
        self.assertEqual(result["outcome_group_counts"]["failed"], 2)
        self.assertTrue(result["worked_patterns"])
        self.assertTrue(result["failed_patterns"])
        self.assertTrue(result["pending_patterns"])
        self.assertTrue(result["stale_patterns"])
        self.assertTrue(result["invalidated_patterns"])
        self.assertTrue(result["missing_evidence_patterns"])
        self.assertTrue(result["repeated_worked_patterns"])
        self.assertTrue(result["repeated_failed_patterns"])
        self.assertTrue(
            result[
                "repeated_inconclusive_pending_stale_invalidated_or_missing_evidence_patterns"
            ]
        )
        self.assertNotIn("profit", str(result).lower())
        self.assertNotIn("combined_viability_score", result)

    def test_identifies_missing_evidence_by_setup_symbol_and_pair(self):
        result = build_setup_outcome_proof_review_bundle(
            [self._ready_summary(), self._not_ready_summary_with_missing_evidence()]
        )

        self.assertIn("Continuation", result["setup_types_needing_more_evidence"])
        self.assertIn("QQQ", result["symbols_needing_more_evidence"])
        self.assertIn(
            {"setup_type": "Continuation", "symbol": "QQQ"},
            result["setup_type_symbol_pairs_needing_more_evidence"],
        )
        self.assertIn("Continuation", result["missing_evidence_by_setup_type"])
        self.assertIn("QQQ", result["missing_evidence_by_symbol"])
        self.assertIn(
            {"setup_type": "Continuation", "symbol": "QQQ"},
            [
                {"setup_type": item["setup_type"], "symbol": item["symbol"]}
                for item in result["missing_evidence_by_setup_type_symbol_pair"]
            ],
        )

    def test_counts_repeated_fix_paths_and_required_regressions(self):
        gap_summary_one = self._not_ready_summary_with_missing_evidence()
        gap_summary_two = self._not_ready_summary_with_missing_evidence()

        result = build_setup_outcome_proof_review_bundle(
            [self._ready_summary(), gap_summary_one, gap_summary_two]
        )

        self.assertTrue(result["repeated_fix_paths"])
        self.assertTrue(result["repeated_regression_needs"])
        self.assertTrue(result["required_regression_tests"])
        self.assertIn("regression", str(result["required_regression_tests"]).lower())

    def test_empty_input_is_bundle_contract_gap(self):
        result = build_setup_outcome_proof_review_bundle([])

        self.assertEqual(result["review_summary_count"], 0)
        self.assertEqual(
            result["bundle_review_decision"],
            "blocked_by_bundle_contract_gap",
        )
        self.assertTrue(result["bundle_contract_gaps"])
        self.assertIs(result["lower_tier_handoff_required"], True)

    def test_rejects_forbidden_execution_fields(self):
        forbidden_cases = (
            {"nested": {"broker_order": "blocked"}},
            {"nested": {"option_pnl": 10}},
            {"nested": {"account_sizing": "blocked"}},
            {"nested": {"live_trade_decision": "approve"}},
        )

        for forbidden in forbidden_cases:
            summary = self._ready_summary()
            summary["reviewed_packets"][0].update(forbidden)
            with self.subTest(forbidden=forbidden):
                with self.assertRaisesRegex(ValueError, "Forbidden execution/trade field"):
                    build_setup_outcome_proof_review_bundle([summary])

    def test_defensive_copy_behavior(self):
        summary = self._ready_summary()
        before = copy.deepcopy(summary)

        result = build_setup_outcome_proof_review_bundle([summary])
        result["included_group_reviews"][0]["reviewed_packets"][0][
            "readiness_status"
        ] = "MUTATED"
        result["represented_setup_types"].append("MUTATED")
        result["worked_patterns"][0]["represented_symbols"].append("MUTATED")

        self.assertEqual(summary, before)
        second = build_setup_outcome_proof_review_bundle([summary])
        self.assertEqual(
            second["included_group_reviews"][0]["reviewed_packets"][0][
                "readiness_status"
            ],
            "ready_for_lower_tier_review",
        )
        self.assertNotIn("MUTATED", second["represented_setup_types"])

    def test_no_file_network_subprocess_thread_or_live_side_effects(self):
        summary = self._ready_summary()
        before = copy.deepcopy(summary)

        with patch("builtins.open") as open_mock, patch(
            "socket.socket"
        ) as socket_mock, patch("subprocess.run") as subprocess_mock, patch(
            "threading.Thread"
        ) as thread_mock:
            result = build_setup_outcome_proof_review_bundle([summary])

        self.assertEqual(summary, before)
        self.assertIs(result["proof_review_only"], True)
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
