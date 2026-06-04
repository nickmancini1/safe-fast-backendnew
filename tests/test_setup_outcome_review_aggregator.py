import copy
import unittest
from unittest.mock import patch

from watcher_foundation import (
    SETUP_OUTCOME_REVIEW_AGGREGATOR_DECISIONS,
    SETUP_OUTCOME_REVIEW_AGGREGATOR_RESULT_FIELDS,
    SETUP_OUTCOME_REVIEW_OUTCOME_GROUPS,
    aggregate_setup_outcome_proof_review,
    build_setup_outcome_evidence_packet,
    evaluate_setup_outcome_diagnostics,
    evaluate_setup_outcome_packet_readiness,
    evaluate_setup_outcome_proof,
)


class SetupOutcomeReviewAggregatorTests(unittest.TestCase):
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
            proof_record_id=f"{setup_type}-{symbol}-{overrides.get('outcome_result_state', 'worked')}",
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
            item["lower_tier_handoff_reason"] = "not required by complete caller-provided packet"
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
        return evaluate_setup_outcome_packet_readiness(packet)

    def _review_ready_with_outcomes(self, records):
        readiness = self._review_ready_packet(records)
        by_id = {
            item["packet_item_id"]: item["outcome_status"]
            for item in self._packet(records)["packet_items"]
        }
        for item in readiness["packet_items"]:
            item["outcome_status"] = by_id[item["packet_item_id"]]
        return readiness

    def test_accepts_only_in_memory_packet_readiness_summary_list(self):
        result = aggregate_setup_outcome_proof_review([self._review_ready_packet()])

        self.assertEqual(set(SETUP_OUTCOME_REVIEW_AGGREGATOR_RESULT_FIELDS), set(result))
        self.assertIn(
            result["proof_continuation_decision"],
            SETUP_OUTCOME_REVIEW_AGGREGATOR_DECISIONS,
        )
        self.assertEqual(set(result["outcome_groups"]), set(SETUP_OUTCOME_REVIEW_OUTCOME_GROUPS))
        self.assertIs(result["watch_only"], True)
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
            aggregate_setup_outcome_proof_review({})

        readiness = self._review_ready_packet()
        del readiness["packet_items"]
        with self.assertRaisesRegex(ValueError, "packet_items"):
            aggregate_setup_outcome_proof_review([readiness])

        readiness = self._review_ready_packet()
        readiness["extra_review_source"] = "not allowed"
        with self.assertRaisesRegex(ValueError, "Unexpected"):
            aggregate_setup_outcome_proof_review([readiness])

    def test_required_boundaries_are_enforced(self):
        required_failures = {
            "watch_only": False,
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
            readiness = self._review_ready_packet()
            readiness[field_name] = value
            with self.subTest(field_name=field_name):
                with self.assertRaisesRegex(ValueError, field_name):
                    aggregate_setup_outcome_proof_review([readiness])

    def test_lists_packets_setup_types_symbols_and_separate_pairs(self):
        readiness = self._review_ready_packet(
            [
                self._record_for_setup("Ideal", "SPY"),
                self._record_for_setup("Ideal", "QQQ"),
                self._record_for_setup("Continuation", "SPY"),
            ]
        )

        result = aggregate_setup_outcome_proof_review([readiness])

        self.assertEqual(
            result["reviewed_packets"][0]["packet_identifier"],
            "UNAVAILABLE-1",
        )
        self.assertEqual(set(result["represented_setup_types"]), {"Ideal", "Continuation"})
        self.assertEqual(set(result["represented_symbols"]), {"SPY", "QQQ"})
        self.assertIn(
            {"setup_type": "Ideal", "symbol": "QQQ"},
            result["represented_setup_type_symbol_pairs"],
        )
        self.assertIs(result["setup_type_separated"], True)
        self.assertIs(result["symbol_separated"], True)

    def test_groups_worked_failed_pending_stale_invalidated_and_missing_evidence(self):
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

        result = aggregate_setup_outcome_proof_review(
            [self._review_ready_with_outcomes(records)]
        )

        for group_name in SETUP_OUTCOME_REVIEW_OUTCOME_GROUPS:
            self.assertTrue(result["outcome_groups"][group_name], group_name)
        self.assertEqual(
            result["outcome_groups"]["worked"][0]["setup_type"],
            "Ideal",
        )
        self.assertEqual(
            result["outcome_groups"]["failed"][0]["symbol"],
            "QQQ",
        )
        self.assertNotIn("success_score", result)
        self.assertNotIn("combined_viability_score", result)

    def test_missing_evidence_and_readiness_gaps_require_more_evidence(self):
        readiness = evaluate_setup_outcome_packet_readiness(
            self._packet(
                [
                    self._record(
                        outcome_evidence_state="unavailable_evidence",
                        unavailable_fields=[self._unavailable_item("source_row_reference")],
                    )
                ]
            )
        )

        result = aggregate_setup_outcome_proof_review([readiness])

        self.assertEqual(
            result["proof_continuation_decision"],
            "needs_more_evidence_before_review",
        )
        self.assertIs(result["lower_tier_handoff_required"], True)
        self.assertIs(result["sufficient_proof_to_continue_review"], False)
        self.assertTrue(result["missing_evidence"])
        self.assertIn("proof_limited_records", str(result["readiness_gap_counts"]))
        self.assertIn("packet_not_ready_for_review", str(result["proof_gaps"]))

    def test_counts_repeated_fix_paths_and_regression_needs(self):
        readiness_one = evaluate_setup_outcome_packet_readiness(self._packet())
        readiness_two = evaluate_setup_outcome_packet_readiness(self._packet())

        result = aggregate_setup_outcome_proof_review([readiness_one, readiness_two])

        self.assertTrue(result["repeated_readiness_gaps"])
        self.assertTrue(result["repeated_next_fix_paths"])
        self.assertTrue(result["repeated_regression_needs"])
        self.assertTrue(result["regression_needed"])
        self.assertIn("missing_evidence", result["readiness_gap_counts"])
        self.assertNotIn("optimize", str(result["repeated_next_fix_paths"]).lower())

    def test_empty_input_needs_more_evidence_without_fabrication(self):
        result = aggregate_setup_outcome_proof_review([])

        self.assertEqual(
            result["proof_continuation_decision"],
            "needs_more_evidence_before_review",
        )
        self.assertEqual(result["packet_summary_count"], 0)
        self.assertFalse(result["represented_setup_types"])
        self.assertFalse(result["represented_symbols"])
        self.assertIn("no_ready_packets", str(result["proof_gaps"]))

    def test_rejects_forbidden_execution_fields_in_nested_readiness_items(self):
        forbidden_cases = (
            {"nested": {"broker_order": "blocked"}},
            {"nested": {"option_pnl": 10}},
            {"nested": {"account_sizing": "blocked"}},
            {"nested": {"live_trade_decision": "approve"}},
        )

        for forbidden in forbidden_cases:
            readiness = self._review_ready_packet()
            readiness["packet_items"][0].update(forbidden)
            with self.subTest(forbidden=forbidden):
                with self.assertRaisesRegex(ValueError, "Forbidden execution/trade field"):
                    aggregate_setup_outcome_proof_review([readiness])

    def test_defensive_copy_behavior(self):
        readiness = self._review_ready_with_outcomes([self._record()])
        before = copy.deepcopy(readiness)

        result = aggregate_setup_outcome_proof_review([readiness])
        result["outcome_groups"]["worked"][0]["symbol"] = "MUTATED"
        result["reviewed_packets"][0]["readiness_status"] = "MUTATED"
        result["missing_evidence"].append("mutated")

        self.assertEqual(readiness, before)
        second = aggregate_setup_outcome_proof_review([readiness])
        self.assertEqual(second["outcome_groups"]["worked"][0]["symbol"], "SPY")
        self.assertEqual(
            second["reviewed_packets"][0]["readiness_status"],
            "ready_for_lower_tier_review",
        )

    def test_no_file_network_subprocess_thread_or_live_side_effects(self):
        readiness = self._review_ready_packet()
        before = copy.deepcopy(readiness)

        with patch("builtins.open") as open_mock, patch(
            "socket.socket"
        ) as socket_mock, patch("subprocess.run") as subprocess_mock, patch(
            "threading.Thread"
        ) as thread_mock:
            result = aggregate_setup_outcome_proof_review([readiness])

        self.assertEqual(readiness, before)
        self.assertIs(result["live_data_started"], False)
        self.assertIs(result["controlled_shadow_data_started"], False)
        self.assertIs(result["alerts_sent"], False)
        self.assertIs(result["files_written"], False)
        self.assertIs(result["broker_or_trade_behavior_enabled"], False)
        self.assertIs(result["no_trade_or_optimization_boundary_preserved"], True)
        open_mock.assert_not_called()
        socket_mock.assert_not_called()
        subprocess_mock.assert_not_called()
        thread_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
