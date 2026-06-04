import copy
import unittest
from unittest.mock import patch

from watcher_foundation import (
    SETUP_OUTCOME_EVIDENCE_PACKET_ITEM_FIELDS,
    SETUP_OUTCOME_EVIDENCE_PACKET_RESULT_FIELDS,
    build_setup_outcome_evidence_packet,
    evaluate_setup_outcome_diagnostics,
    evaluate_setup_outcome_proof,
)


class SetupOutcomeEvidencePacketTests(unittest.TestCase):
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
            proof_record_id=f"{setup_type}-{symbol}",
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

    def _diagnostics(self, records=None):
        if records is None:
            records = [self._record()]
        return evaluate_setup_outcome_diagnostics(evaluate_setup_outcome_proof(records))

    def test_accepts_only_in_memory_setup_outcome_diagnostics_summary_shape(self):
        packet = build_setup_outcome_evidence_packet(self._diagnostics())

        self.assertEqual(set(SETUP_OUTCOME_EVIDENCE_PACKET_RESULT_FIELDS), set(packet))
        self.assertIs(packet["watch_only"], True)
        self.assertIs(packet["setup_outcome_evidence_packet_only"], True)
        self.assertIs(packet["setup_outcome_diagnostics_only"], True)
        self.assertIs(packet["setup_outcome_proof_only"], True)
        self.assertIs(packet["final_viability_proven"], False)
        self.assertIs(packet["optimization_started"], False)
        self.assertIs(packet["no_rule_change_started"], True)
        self.assertEqual(packet["packet_item_count"], 1)

    def test_invalid_input_type_missing_and_unexpected_fields_fail(self):
        with self.assertRaisesRegex(TypeError, "input must be a dict"):
            build_setup_outcome_evidence_packet([])

        diagnostics = self._diagnostics()
        del diagnostics["diagnostic_findings"]
        with self.assertRaisesRegex(ValueError, "diagnostic_findings"):
            build_setup_outcome_evidence_packet(diagnostics)

        diagnostics = self._diagnostics()
        diagnostics["extra_packet_source"] = "not allowed"
        with self.assertRaisesRegex(ValueError, "Unexpected"):
            build_setup_outcome_evidence_packet(diagnostics)

    def test_required_boundaries_are_enforced(self):
        required_failures = {
            "watch_only": False,
            "setup_outcome_diagnostics_only": False,
            "setup_outcome_proof_only": False,
            "final_viability_proven": True,
            "optimization_started": True,
            "no_rule_change_started": False,
            "live_data_started": True,
            "controlled_shadow_data_started": True,
            "alerts_sent": True,
            "files_written": True,
            "broker_or_trade_behavior_enabled": True,
        }

        for field_name, value in required_failures.items():
            diagnostics = self._diagnostics()
            diagnostics[field_name] = value
            with self.subTest(field_name=field_name):
                with self.assertRaisesRegex(ValueError, field_name):
                    build_setup_outcome_evidence_packet(diagnostics)

    def test_preserves_setup_type_and_symbol_as_separate_grouping_keys(self):
        packet = build_setup_outcome_evidence_packet(
            self._diagnostics(
                [
                    self._record_for_setup("Ideal", "SPY"),
                    self._record_for_setup("Ideal", "QQQ"),
                    self._record_for_setup("Continuation", "SPY"),
                ]
            )
        )

        self.assertEqual(set(packet["packet_items_by_setup_type"]), {"Ideal", "Continuation"})
        self.assertEqual(set(packet["packet_items_by_setup_type"]["Ideal"]), {"SPY", "QQQ"})
        self.assertEqual(packet["packet_items_by_setup_type"]["Ideal"]["QQQ"][0]["symbol"], "QQQ")

    def test_packet_item_contains_required_plain_english_review_fields(self):
        packet = build_setup_outcome_evidence_packet(self._diagnostics())
        item = packet["packet_items"][0]

        self.assertEqual(set(SETUP_OUTCOME_EVIDENCE_PACKET_ITEM_FIELDS), set(item))
        self.assertEqual(item["setup_type"], "Ideal")
        self.assertEqual(item["symbol"], "SPY")
        self.assertEqual(item["what_setup_appeared"]["stage"], "near-trigger")
        self.assertIn("trigger evidence was present", item["what_happened_after_setup"])
        self.assertEqual(item["outcome_status"], "triggered_worked")
        self.assertEqual(item["evidence_state"], "missing_or_unavailable_evidence")
        self.assertTrue(item["evidence_support"]["evidence_refs"])
        self.assertTrue(item["missing_evidence"])
        self.assertTrue(item["next_fix_path"])
        self.assertIn("regression", item["regression_needed"])
        self.assertIs(item["no_hindsight_boundary_confirmed"], True)
        self.assertIs(item["no_trade_boundary_confirmed"], True)

    def test_rejected_proof_reasons_are_lower_tier_handoff_packet_evidence(self):
        packet = build_setup_outcome_evidence_packet(
            self._diagnostics([self._record(watch_only=False)])
        )

        self.assertEqual(packet["records_rejected"], 1)
        self.assertIs(packet["lower_tier_handoff_required"], True)
        item = packet["packet_items"][0]
        self.assertEqual(item["diagnostic_category"], "lower_tier_handoff_review")
        self.assertIs(item["lower_tier_handoff_required"], True)
        self.assertIn("watch_only=True", str(item["evidence_support"]))

    def test_missing_and_proof_limited_evidence_are_carried_without_fabrication(self):
        record = self._record(
            outcome_evidence_state="unavailable_evidence",
            unavailable_fields=[self._unavailable_item("source_row_reference")],
        )
        packet = build_setup_outcome_evidence_packet(self._diagnostics([record]))
        item = packet["packet_items"][0]

        self.assertEqual(item["evidence_state"], "missing_or_unavailable_evidence")
        self.assertIn("source_row_reference", str(item["missing_evidence"]))
        self.assertIn("source_row_reference", str(item["proof_limited_reason"]))
        self.assertIn("source_row_reference", str(packet["missing_evidence"]))
        self.assertNotIn("fabricated': True", str(packet))

    def test_all_setup_outcome_statuses_are_preserved(self):
        cases = {
            "triggered_worked": self._record(outcome_result_state="worked"),
            "triggered_failed": self._record(outcome_result_state="failed"),
            "triggered_inconclusive": self._record(outcome_result_state="inconclusive"),
            "stayed_valid_pending": self._record(
                proof_record_id="pending",
                setup_id="setup-pending",
                trigger_state="not_triggered",
                invalidation_state="valid_by_rule",
                freshness_state="fresh",
                outcome_result_state="pending",
                frozen_setup_identity={
                    "caller_provided": True,
                    "frozen_before_outcome_scan": True,
                    "setup_id": "setup-pending",
                    "setup_type": "Ideal",
                    "symbol": "SPY",
                    "frozen_timestamp": "2026-05-24T09:35:00-04:00",
                },
            ),
            "stale_without_trigger": self._record(
                proof_record_id="stale",
                setup_id="setup-stale",
                trigger_state="not_triggered",
                freshness_state="stale",
                outcome_result_state="none",
                frozen_setup_identity={
                    "caller_provided": True,
                    "frozen_before_outcome_scan": True,
                    "setup_id": "setup-stale",
                    "setup_type": "Ideal",
                    "symbol": "SPY",
                    "frozen_timestamp": "2026-05-24T09:35:00-04:00",
                },
            ),
            "invalidated_before_trigger": self._record(
                proof_record_id="invalidated",
                setup_id="setup-invalidated",
                trigger_state="not_triggered",
                invalidation_state="invalidated",
                outcome_result_state="none",
                frozen_setup_identity={
                    "caller_provided": True,
                    "frozen_before_outcome_scan": True,
                    "setup_id": "setup-invalidated",
                    "setup_type": "Ideal",
                    "symbol": "SPY",
                    "frozen_timestamp": "2026-05-24T09:35:00-04:00",
                },
            ),
            "insufficient_evidence": self._record(
                proof_record_id="insufficient",
                setup_id="setup-insufficient",
                outcome_evidence_state="missing_evidence",
                unavailable_fields=[self._unavailable_item("post_setup_evidence")],
                frozen_setup_identity={
                    "caller_provided": True,
                    "frozen_before_outcome_scan": True,
                    "setup_id": "setup-insufficient",
                    "setup_type": "Ideal",
                    "symbol": "SPY",
                    "frozen_timestamp": "2026-05-24T09:35:00-04:00",
                },
            ),
        }
        del cases["insufficient_evidence"]["after_setup_evidence"]["post_setup_evidence"]

        packet = build_setup_outcome_evidence_packet(self._diagnostics(list(cases.values())))
        statuses = {item["outcome_status"] for item in packet["packet_items"]}

        self.assertEqual(statuses, set(cases))

    def test_rejects_shallow_packet_conclusions_without_evidence(self):
        diagnostics = self._diagnostics()
        finding = diagnostics["diagnostic_findings"][0]
        finding["evidence_used"] = []
        finding["evidence_supports"] = {}
        finding["unavailable_evidence"] = []
        finding["proof_limited_fields"] = []

        with self.assertRaisesRegex(ValueError, "explicit evidence support"):
            build_setup_outcome_evidence_packet(diagnostics)

    def test_forbidden_execution_fields_are_rejected_or_quarantined(self):
        forbidden_cases = (
            {"nested": {"broker_order": "blocked"}},
            {"nested": {"option_pnl": 10}},
            {"nested": {"account_sizing": "blocked"}},
            {"nested": {"live_trade_decision": "approve"}},
        )

        for forbidden in forbidden_cases:
            diagnostics = self._diagnostics()
            diagnostics["diagnostic_findings"][0].update(forbidden)
            with self.subTest(forbidden=forbidden):
                with self.assertRaisesRegex(ValueError, "Forbidden execution/trade field"):
                    build_setup_outcome_evidence_packet(diagnostics)

    def test_defensive_copy_behavior(self):
        diagnostics = self._diagnostics()
        before = copy.deepcopy(diagnostics)

        packet = build_setup_outcome_evidence_packet(diagnostics)
        packet["packet_items"][0]["evidence_support"]["evidence_refs"].append("mutated")
        packet["packet_items_by_setup_type"]["Ideal"]["SPY"][0]["symbol"] = "MUTATED"
        packet["rejected_records"].append({"reason": "mutated"})

        self.assertEqual(diagnostics, before)
        second = build_setup_outcome_evidence_packet(diagnostics)
        self.assertNotIn("mutated", second["packet_items"][0]["evidence_support"]["evidence_refs"])
        self.assertEqual(second["packet_items_by_setup_type"]["Ideal"]["SPY"][0]["symbol"], "SPY")

    def test_no_file_network_subprocess_thread_or_live_side_effects(self):
        diagnostics = self._diagnostics()
        before = copy.deepcopy(diagnostics)

        with patch("builtins.open") as open_mock, patch(
            "socket.socket"
        ) as socket_mock, patch("subprocess.run") as subprocess_mock, patch(
            "threading.Thread"
        ) as thread_mock:
            packet = build_setup_outcome_evidence_packet(diagnostics)

        self.assertEqual(diagnostics, before)
        self.assertIs(packet["live_data_started"], False)
        self.assertIs(packet["controlled_shadow_data_started"], False)
        self.assertIs(packet["alerts_sent"], False)
        self.assertIs(packet["files_written"], False)
        self.assertIs(packet["broker_or_trade_behavior_enabled"], False)
        self.assertIs(packet["no_trade_boundary_preserved"], True)
        open_mock.assert_not_called()
        socket_mock.assert_not_called()
        subprocess_mock.assert_not_called()
        thread_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
