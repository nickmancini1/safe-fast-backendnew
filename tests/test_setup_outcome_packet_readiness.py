import copy
import unittest
from unittest.mock import patch

from watcher_foundation import (
    SETUP_OUTCOME_PACKET_READINESS_ITEM_FIELDS,
    SETUP_OUTCOME_PACKET_READINESS_RESULT_FIELDS,
    SETUP_OUTCOME_PACKET_READINESS_STATUSES,
    build_setup_outcome_evidence_packet,
    evaluate_setup_outcome_diagnostics,
    evaluate_setup_outcome_packet_readiness,
    evaluate_setup_outcome_proof,
)


class SetupOutcomePacketReadinessTests(unittest.TestCase):
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

    def _packet(self, records=None):
        if records is None:
            records = [self._record()]
        proof = evaluate_setup_outcome_proof(records)
        diagnostics = evaluate_setup_outcome_diagnostics(proof)
        return build_setup_outcome_evidence_packet(diagnostics)

    def _review_ready_packet(self):
        packet = self._packet()
        item = packet["packet_items"][0]
        item["setup_identifier"] = "setup-1"
        item["what_setup_appeared"]["setup_identifier"] = "setup-1"
        item["missing_evidence"] = []
        item["evidence_state"] = "evidence_supported"
        item["lower_tier_handoff_required"] = False
        item["lower_tier_handoff_reason"] = "not required by complete caller-provided packet"
        packet["missing_evidence"] = []
        packet["lower_tier_handoff_required"] = False
        packet["lower_tier_handoff_items"] = []
        packet["proof_limited_records"] = []
        packet["packet_items_by_setup_type"] = {"Ideal": {"SPY": [copy.deepcopy(item)]}}
        return packet

    def test_accepts_only_in_memory_evidence_packet_summary_shape(self):
        result = evaluate_setup_outcome_packet_readiness(self._review_ready_packet())

        self.assertEqual(set(SETUP_OUTCOME_PACKET_READINESS_RESULT_FIELDS), set(result))
        self.assertEqual(
            set(SETUP_OUTCOME_PACKET_READINESS_ITEM_FIELDS),
            set(result["packet_items"][0]),
        )
        self.assertIn(
            result["readiness_status"],
            SETUP_OUTCOME_PACKET_READINESS_STATUSES,
        )
        self.assertIs(result["watch_only"], True)
        self.assertIs(result["setup_outcome_packet_readiness_only"], True)
        self.assertIs(result["setup_outcome_evidence_packet_only"], True)
        self.assertIs(result["setup_outcome_diagnostics_only"], True)
        self.assertIs(result["setup_outcome_proof_only"], True)
        self.assertIs(result["final_viability_proven"], False)
        self.assertIs(result["optimization_started"], False)
        self.assertIs(result["no_rule_change_started"], True)

    def test_invalid_input_type_missing_and_unexpected_fields_fail(self):
        with self.assertRaisesRegex(TypeError, "input must be a dict"):
            evaluate_setup_outcome_packet_readiness([])

        packet = self._review_ready_packet()
        del packet["packet_items"]
        with self.assertRaisesRegex(ValueError, "packet_items"):
            evaluate_setup_outcome_packet_readiness(packet)

        packet = self._review_ready_packet()
        packet["extra_readiness_source"] = "not allowed"
        with self.assertRaisesRegex(ValueError, "Unexpected"):
            evaluate_setup_outcome_packet_readiness(packet)

    def test_required_boundaries_are_enforced(self):
        required_failures = {
            "watch_only": False,
            "setup_outcome_evidence_packet_only": False,
            "setup_outcome_diagnostics_only": False,
            "setup_outcome_proof_only": False,
            "final_viability_proven": True,
            "optimization_started": True,
            "no_rule_change_started": False,
            "no_hindsight_boundary_preserved": False,
            "no_trade_boundary_preserved": False,
            "live_data_started": True,
            "controlled_shadow_data_started": True,
            "alerts_sent": True,
            "files_written": True,
            "broker_or_trade_behavior_enabled": True,
        }

        for field_name, value in required_failures.items():
            packet = self._review_ready_packet()
            packet[field_name] = value
            with self.subTest(field_name=field_name):
                with self.assertRaisesRegex(ValueError, field_name):
                    evaluate_setup_outcome_packet_readiness(packet)

    def test_marks_complete_packet_ready_for_lower_tier_review(self):
        result = evaluate_setup_outcome_packet_readiness(self._review_ready_packet())

        self.assertEqual(result["readiness_status"], "ready_for_lower_tier_review")
        self.assertIs(result["complete_enough_to_review"], True)
        self.assertIs(result["ready_for_lower_tier_review"], True)
        self.assertFalse(result["readiness_gaps"])
        self.assertFalse(result["missing_evidence"])
        self.assertIs(result["lower_tier_handoff_required"], False)
        self.assertIs(result["no_trade_or_optimization_boundary_preserved"], True)

    def test_builder_packet_missing_setup_identifier_requires_lower_tier_evidence_fix(self):
        result = evaluate_setup_outcome_packet_readiness(self._packet())

        self.assertEqual(result["readiness_status"], "needs_lower_tier_evidence_fix")
        self.assertIs(result["complete_enough_to_review"], False)
        self.assertIs(result["lower_tier_handoff_required"], True)
        self.assertIn("setup_identifier", str(result["missing_evidence"]))
        self.assertIn("missing_evidence", str(result["readiness_gaps"]))

    def test_setup_type_and_symbol_must_remain_separate_in_items_and_grouping(self):
        packet = self._review_ready_packet()
        packet["packet_items"][0]["setup_type"] = "Ideal/SPY"
        packet["packet_items_by_setup_type"] = {
            "Ideal/SPY": {"UNAVAILABLE": [copy.deepcopy(packet["packet_items"][0])]}
        }

        result = evaluate_setup_outcome_packet_readiness(packet)

        self.assertEqual(result["readiness_status"], "blocked_by_packet_contract_gap")
        self.assertIs(result["setup_type_separated"], False)
        self.assertIn("setup_symbol_merged", str(result["readiness_gaps"]))

    def test_unclear_diagnosis_next_fix_path_and_missing_regression_are_gaps(self):
        packet = self._review_ready_packet()
        item = packet["packet_items"][0]
        item["why_it_happened"] = "bad"
        item["next_fix_path"] = "fix later"
        item["affected_system_area"] = ""
        item["regression_needed"] = "regression"
        packet["packet_items_by_setup_type"] = {"Ideal": {"SPY": [copy.deepcopy(item)]}}

        result = evaluate_setup_outcome_packet_readiness(packet)

        self.assertIs(result["diagnosis_clear_enough"], False)
        self.assertIs(result["next_fix_path_clear_enough"], False)
        self.assertIs(result["regression_named"], False)
        self.assertIn("unclear_diagnosis", str(result["readiness_gaps"]))
        self.assertIn("unclear_next_fix_path", str(result["readiness_gaps"]))
        self.assertIn("missing_regression", str(result["readiness_gaps"]))

    def test_rejected_and_proof_limited_packets_require_handoff(self):
        rejected_result = evaluate_setup_outcome_packet_readiness(
            self._packet([self._record(watch_only=False)])
        )
        proof_limited_record = self._record(
            outcome_evidence_state="unavailable_evidence",
            unavailable_fields=[self._unavailable_item("source_row_reference")],
        )
        proof_limited_result = evaluate_setup_outcome_packet_readiness(
            self._packet([proof_limited_record])
        )

        self.assertEqual(
            rejected_result["readiness_status"],
            "blocked_by_packet_contract_gap",
        )
        self.assertIs(rejected_result["lower_tier_handoff_required"], True)
        self.assertIn("rejected_proof_records", str(rejected_result["readiness_gaps"]))
        self.assertEqual(
            proof_limited_result["readiness_status"],
            "needs_lower_tier_evidence_fix",
        )
        self.assertIn("proof_limited_records", str(proof_limited_result["readiness_gaps"]))

    def test_forbidden_execution_fields_are_rejected_or_quarantined(self):
        forbidden_cases = (
            {"nested": {"broker_order": "blocked"}},
            {"nested": {"option_pnl": 10}},
            {"nested": {"account_sizing": "blocked"}},
            {"nested": {"live_trade_decision": "approve"}},
        )

        for forbidden in forbidden_cases:
            packet = self._review_ready_packet()
            packet["packet_items"][0].update(forbidden)
            with self.subTest(forbidden=forbidden):
                with self.assertRaisesRegex(ValueError, "Forbidden execution/trade field"):
                    evaluate_setup_outcome_packet_readiness(packet)

    def test_defensive_copy_behavior(self):
        packet = self._review_ready_packet()
        before = copy.deepcopy(packet)

        result = evaluate_setup_outcome_packet_readiness(packet)
        result["packet_items"][0]["missing_evidence"].append("mutated")
        result["items_by_setup_type"]["Ideal"]["SPY"][0]["symbol"] = "MUTATED"
        result["rejected_records"].append({"reason": "mutated"})

        self.assertEqual(packet, before)
        second = evaluate_setup_outcome_packet_readiness(packet)
        self.assertNotIn("mutated", second["packet_items"][0]["missing_evidence"])
        self.assertEqual(second["items_by_setup_type"]["Ideal"]["SPY"][0]["symbol"], "SPY")

    def test_no_file_network_subprocess_thread_or_live_side_effects(self):
        packet = self._review_ready_packet()
        before = copy.deepcopy(packet)

        with patch("builtins.open") as open_mock, patch(
            "socket.socket"
        ) as socket_mock, patch("subprocess.run") as subprocess_mock, patch(
            "threading.Thread"
        ) as thread_mock:
            result = evaluate_setup_outcome_packet_readiness(packet)

        self.assertEqual(packet, before)
        self.assertIs(result["live_data_started"], False)
        self.assertIs(result["controlled_shadow_data_started"], False)
        self.assertIs(result["alerts_sent"], False)
        self.assertIs(result["files_written"], False)
        self.assertIs(result["broker_or_trade_behavior_enabled"], False)
        self.assertIs(result["no_optimization_boundary_preserved"], True)
        open_mock.assert_not_called()
        socket_mock.assert_not_called()
        subprocess_mock.assert_not_called()
        thread_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
