import copy
import unittest
from unittest.mock import patch

from watcher_foundation import (
    SETUP_OUTCOME_REVIEW_READINESS_DECISIONS,
    SETUP_OUTCOME_REVIEW_READINESS_RESULT_FIELDS,
    aggregate_setup_outcome_proof_review,
    build_setup_outcome_evidence_packet,
    evaluate_setup_outcome_diagnostics,
    evaluate_setup_outcome_packet_readiness,
    evaluate_setup_outcome_proof,
    evaluate_setup_outcome_review_readiness,
)


class SetupOutcomeReviewReadinessTests(unittest.TestCase):
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

    def test_accepts_one_in_memory_review_aggregate_summary(self):
        result = evaluate_setup_outcome_review_readiness(
            self._full_coverage_aggregate()
        )

        self.assertEqual(set(SETUP_OUTCOME_REVIEW_READINESS_RESULT_FIELDS), set(result))
        self.assertIn(
            result["lower_tier_review_decision"],
            SETUP_OUTCOME_REVIEW_READINESS_DECISIONS,
        )
        self.assertIs(result["watch_only"], True)
        self.assertIs(result["setup_outcome_review_readiness_only"], True)
        self.assertIs(result["setup_outcome_review_aggregator_only"], True)
        self.assertIs(result["setup_outcome_packet_readiness_only"], True)
        self.assertIs(result["setup_outcome_evidence_packet_only"], True)
        self.assertIs(result["setup_outcome_diagnostics_only"], True)
        self.assertIs(result["setup_outcome_proof_only"], True)
        self.assertIs(result["final_viability_proven"], False)
        self.assertIs(result["optimization_started"], False)
        self.assertIs(result["no_rule_change_started"], True)
        self.assertIs(result["group_review_complete_enough_to_trust"], True)

    def test_invalid_input_type_missing_and_unexpected_fields_fail(self):
        with self.assertRaisesRegex(TypeError, "input must be a dict"):
            evaluate_setup_outcome_review_readiness([])

        aggregate = self._aggregate()
        del aggregate["reviewed_packets"]
        with self.assertRaisesRegex(ValueError, "reviewed_packets"):
            evaluate_setup_outcome_review_readiness(aggregate)

        aggregate = self._aggregate()
        aggregate["extra_review_file"] = "not allowed"
        with self.assertRaisesRegex(ValueError, "Unexpected"):
            evaluate_setup_outcome_review_readiness(aggregate)

    def test_required_boundaries_are_enforced(self):
        required_failures = {
            "watch_only": False,
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
            aggregate = self._aggregate()
            aggregate[field_name] = value
            with self.subTest(field_name=field_name):
                with self.assertRaisesRegex(ValueError, field_name):
                    evaluate_setup_outcome_review_readiness(aggregate)

    def test_preserves_packet_identifiers_and_setup_symbol_separation(self):
        result = evaluate_setup_outcome_review_readiness(self._aggregate())

        self.assertEqual(
            result["reviewed_packets"][0]["packet_identifier"],
            "UNAVAILABLE-1",
        )
        self.assertEqual(result["represented_setup_types"], ["Ideal"])
        self.assertEqual(result["represented_symbols"], ["SPY"])
        self.assertEqual(
            result["represented_setup_type_symbol_pairs"],
            [{"setup_type": "Ideal", "symbol": "SPY"}],
        )
        self.assertIs(result["setup_type_separated"], True)
        self.assertIs(result["symbol_separated"], True)

    def test_identifies_missing_setup_type_and_symbol_evidence(self):
        record = self._record_for_setup(
            "Continuation",
            "QQQ",
            outcome_evidence_state="unavailable_evidence",
            unavailable_fields=[self._unavailable_item("source_row_reference")],
        )
        aggregate = aggregate_setup_outcome_proof_review(
            [evaluate_setup_outcome_packet_readiness(self._packet([record]))]
        )

        result = evaluate_setup_outcome_review_readiness(aggregate)

        self.assertIn("Continuation", result["setup_types_needing_more_evidence"])
        self.assertIn("QQQ", result["symbols_needing_more_evidence"])
        self.assertIn(
            {"setup_type": "Continuation", "symbol": "QQQ"},
            result["setup_type_symbol_pairs_needing_more_evidence"],
        )
        self.assertIs(result["proof_gaps_blocking_review"], True)
        self.assertEqual(
            result["lower_tier_review_decision"],
            "blocked_by_review_contract_gap",
        )

    def test_requires_explicit_outcome_groups_before_trust(self):
        result = evaluate_setup_outcome_review_readiness(self._aggregate())

        self.assertIs(result["outcome_groups_explicit"], False)
        self.assertIn("failed", result["missing_outcome_groups"])
        self.assertIn("absent_outcome_coverage", str(result["review_contract_gaps"]))
        self.assertIs(result["group_review_complete_enough_to_trust"], False)

    def test_requires_clear_failure_diagnosis_fix_paths_and_regressions(self):
        aggregate = self._full_coverage_aggregate()
        aggregate["readiness_gap_counts"] = {
            "unclear_diagnosis": 1,
            "unclear_next_fix_path": 2,
            "missing_regression": 1,
        }
        aggregate["repeated_next_fix_paths"] = {"fix later": 2}
        aggregate["regression_needed"] = ["regression"]

        result = evaluate_setup_outcome_review_readiness(aggregate)

        self.assertIs(result["failure_diagnosis_clear_enough"], False)
        self.assertTrue(result["unclear_diagnoses"])
        self.assertIs(result["repeated_fix_paths_clear_enough"], False)
        self.assertTrue(result["unclear_repeated_fix_paths"])
        self.assertIs(result["regression_coverage_named"], False)
        self.assertTrue(result["missing_regression_coverage"])

    def test_proof_gaps_block_review_and_emit_lower_tier_decision(self):
        aggregate = self._aggregate()
        result = evaluate_setup_outcome_review_readiness(aggregate)

        self.assertIs(result["proof_gaps_blocking_review"], True)
        self.assertIs(result["lower_tier_handoff_required"], True)
        self.assertEqual(
            result["lower_tier_review_decision"],
            "blocked_by_review_contract_gap",
        )
        self.assertNotIn("profit", str(result).lower())
        self.assertNotIn("success_score", result)

    def test_preserves_no_trade_and_no_optimization_boundaries(self):
        result = evaluate_setup_outcome_review_readiness(
            self._full_coverage_aggregate()
        )

        self.assertIs(result["no_trade_boundary_preserved"], True)
        self.assertIs(result["no_live_data_boundary_preserved"], True)
        self.assertIs(result["no_controlled_shadow_boundary_preserved"], True)
        self.assertIs(result["no_alert_boundary_preserved"], True)
        self.assertIs(result["no_file_write_boundary_preserved"], True)
        self.assertIs(result["no_broker_boundary_preserved"], True)
        self.assertIs(result["no_optimization_boundary_preserved"], True)
        self.assertIs(result["no_trade_or_optimization_boundary_preserved"], True)
        self.assertIs(result["live_data_started"], False)
        self.assertIs(result["controlled_shadow_data_started"], False)
        self.assertIs(result["alerts_sent"], False)
        self.assertIs(result["files_written"], False)
        self.assertIs(result["broker_or_trade_behavior_enabled"], False)

    def test_rejects_forbidden_execution_fields(self):
        forbidden_cases = (
            {"nested": {"broker_order": "blocked"}},
            {"nested": {"option_pnl": 10}},
            {"nested": {"account_sizing": "blocked"}},
            {"nested": {"live_trade_decision": "approve"}},
        )

        for forbidden in forbidden_cases:
            aggregate = self._aggregate()
            aggregate["reviewed_packets"][0].update(forbidden)
            with self.subTest(forbidden=forbidden):
                with self.assertRaisesRegex(ValueError, "Forbidden execution/trade field"):
                    evaluate_setup_outcome_review_readiness(aggregate)

    def test_defensive_copy_behavior(self):
        aggregate = self._aggregate()
        before = copy.deepcopy(aggregate)

        result = evaluate_setup_outcome_review_readiness(aggregate)
        result["reviewed_packets"][0]["readiness_status"] = "MUTATED"
        result["represented_setup_types"].append("MUTATED")
        result["proof_gaps"].append({"reason": "mutated"})

        self.assertEqual(aggregate, before)
        second = evaluate_setup_outcome_review_readiness(aggregate)
        self.assertEqual(
            second["reviewed_packets"][0]["readiness_status"],
            "ready_for_lower_tier_review",
        )
        self.assertNotIn("MUTATED", second["represented_setup_types"])

    def test_no_file_network_subprocess_thread_or_live_side_effects(self):
        aggregate = self._aggregate()
        before = copy.deepcopy(aggregate)

        with patch("builtins.open") as open_mock, patch(
            "socket.socket"
        ) as socket_mock, patch("subprocess.run") as subprocess_mock, patch(
            "threading.Thread"
        ) as thread_mock:
            result = evaluate_setup_outcome_review_readiness(aggregate)

        self.assertEqual(aggregate, before)
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
