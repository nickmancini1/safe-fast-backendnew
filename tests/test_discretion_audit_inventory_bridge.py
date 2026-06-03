import copy
import unittest
from unittest.mock import patch

from watcher_foundation import (
    DISCRETION_AUDIT_INVENTORY_ALLOWED_AREAS,
    DISCRETION_AUDIT_INVENTORY_BRIDGE_RESULT_FIELDS,
    evaluate_discretion_audit_inventory_bridge,
)


class DiscretionAuditInventoryBridgeTests(unittest.TestCase):
    def _item(self, area="trigger", **overrides):
        item = {
            "item_id": f"rule-{area}",
            "area": area,
            "source": "caller-provided-rule-contract",
            "text": "Trigger must use explicit caller-provided proof.",
            "rule_purpose": "Document the rule purpose before later audit work.",
            "audit_readiness": "ready_for_later_audit",
            "unavailable_fields": [],
            "watch_only": True,
        }
        item.update(overrides)
        return item

    def test_accepts_caller_provided_in_memory_inventory_items_only(self):
        items = [self._item()]
        before = copy.deepcopy(items)

        result = evaluate_discretion_audit_inventory_bridge(items)

        self.assertEqual(items, before)
        self.assertEqual(set(DISCRETION_AUDIT_INVENTORY_BRIDGE_RESULT_FIELDS), set(result))
        self.assertIs(result["local_only"], True)
        self.assertIs(result["in_memory_only"], True)
        self.assertEqual(result["inventory_validation"]["items_processed"], 1)

    def test_runs_existing_inventory_validator_before_audit_conversion(self):
        validation = {
            "watch_only": True,
            "discretion_audit_inventory_only": True,
            "audit_started": False,
            "rules_changed": False,
            "optimization_started": False,
            "items_processed": 1,
            "items_accepted": 0,
            "items_rejected": 1,
            "accepted_items": [],
            "rejected_items": [
                {
                    "index": 0,
                    "item_id": "bad",
                    "accepted": False,
                    "reasons": ["validator rejected before conversion"],
                }
            ],
            "covered_areas": [],
            "missing_required_areas": list(DISCRETION_AUDIT_INVENTORY_ALLOWED_AREAS),
            "unavailable_fields": [],
            "no_trade_boundary_preserved": True,
            "live_data_started": False,
            "controlled_shadow_data_started": False,
            "alerts_sent": False,
            "files_written": False,
            "broker_or_trade_behavior_enabled": False,
        }

        with patch(
            "watcher_foundation.discretion_audit_inventory_bridge.validate_discretion_audit_inventory",
            return_value=validation,
        ) as validator_mock, patch(
            "watcher_foundation.discretion_audit_inventory_bridge.audit_trading_plan_discretion"
        ) as audit_mock:
            result = evaluate_discretion_audit_inventory_bridge([self._item()])

        validator_mock.assert_called_once()
        audit_mock.assert_not_called()
        self.assertFalse(result["audit_executed"])
        self.assertEqual(result["rejected_inventory_items"][0]["reasons"], ["validator rejected before conversion"])

    def test_rejects_invalid_inventory_through_existing_validator_behavior(self):
        valid_item = self._item(area="trigger")
        invalid_item = self._item(area="position sizing", item_id="bad-area")

        result = evaluate_discretion_audit_inventory_bridge([valid_item, invalid_item])

        self.assertEqual(result["inventory_validation"]["items_accepted"], 1)
        self.assertEqual(result["inventory_validation"]["items_rejected"], 1)
        self.assertEqual(result["rejected_inventory_items"][0]["item_id"], "bad-area")
        self.assertEqual(result["audit_summary"]["items_reviewed"], 1)

    def test_converts_only_accepted_inventory_items_into_existing_audit_shape(self):
        valid_item = self._item(
            area="setup recognition",
            item_id="accepted",
            text="Setup recognition must use the caller text exactly.",
        )
        invalid_item = self._item(area="position sizing", item_id="rejected")

        result = evaluate_discretion_audit_inventory_bridge([valid_item, invalid_item])

        self.assertEqual(len(result["audit_input_items"]), 1)
        audit_item = result["audit_input_items"][0]
        self.assertEqual(
            set(audit_item),
            {"item_id", "area", "text", "source", "review_context", "watch_only"},
        )
        self.assertEqual(audit_item["item_id"], "accepted")
        self.assertEqual(audit_item["text"], valid_item["text"])

    def test_preserves_required_inventory_fields_and_watch_only_boundary(self):
        item = self._item(
            area="diagnostics",
            item_id="preserve",
            source="source-a",
            text="Diagnostics must identify evidence and next fix path.",
            rule_purpose="Preserve diagnostics contract.",
            audit_readiness="ready_with_known_limits",
            unavailable_fields={"headline_news": "not caller-provided"},
        )

        result = evaluate_discretion_audit_inventory_bridge([item])
        accepted = result["accepted_inventory_items"][0]

        for field_name in (
            "item_id",
            "area",
            "source",
            "text",
            "rule_purpose",
            "audit_readiness",
            "unavailable_fields",
            "watch_only",
        ):
            self.assertEqual(accepted[field_name], item[field_name])
        self.assertIs(result["watch_only_boundary_preserved"], True)

    def test_does_not_invent_or_rewrite_rule_text(self):
        item = self._item(text="Exact caller rule text. Do not improve this.")

        result = evaluate_discretion_audit_inventory_bridge([item])

        self.assertEqual(result["accepted_inventory_items"][0]["text"], item["text"])
        self.assertEqual(result["audit_input_items"][0]["text"], item["text"])

    def test_preserves_unavailable_fields_explicitly_in_combined_summary(self):
        item = self._item(
            area="invalidation",
            unavailable_fields={
                "numeric_invalidation": "unavailable",
                "proof_rows": ["not caller-provided"],
            },
        )

        result = evaluate_discretion_audit_inventory_bridge([item])

        self.assertEqual(
            result["unavailable_fields"],
            [
                {
                    "item_id": "rule-invalidation",
                    "unavailable_fields": item["unavailable_fields"],
                }
            ],
        )
        self.assertEqual(result["unavailable_field_blockers"][0]["unavailable_fields"], item["unavailable_fields"])
        self.assertEqual(result["audit_confidence"], "blocked_by_explicit_unavailable_fields")
        self.assertEqual(result["coverage_confidence"], "blocked_by_explicit_unavailable_fields")

    def test_runs_existing_discretion_audit_under_watch_only_boundaries(self):
        item = self._item(
            area="user workflow",
            text="Reviewer may add a review note.",
        )

        result = evaluate_discretion_audit_inventory_bridge([item])

        self.assertTrue(result["audit_execution_eligible"])
        self.assertTrue(result["audit_executed"])
        self.assertIs(result["audit_summary"]["watch_only"], True)
        self.assertEqual(result["audit_summary"]["allowed_safety_discretion_count"], 1)
        self.assertIs(result["audit_summary"]["broker_or_trade_behavior_enabled"], False)

    def test_runs_existing_coverage_only_when_valid_audit_output_is_available(self):
        accepted_result = evaluate_discretion_audit_inventory_bridge(
            [self._item(area="user workflow", text="Reviewer may add a review note.")]
        )
        rejected_result = evaluate_discretion_audit_inventory_bridge(
            [self._item(area="position sizing")]
        )

        self.assertTrue(accepted_result["coverage_execution_eligible"])
        self.assertTrue(accepted_result["coverage_executed"])
        self.assertIsNotNone(accepted_result["coverage_summary"])
        self.assertFalse(rejected_result["coverage_execution_eligible"])
        self.assertFalse(rejected_result["coverage_executed"])
        self.assertIsNone(rejected_result["coverage_summary"])

    def test_returns_combined_in_memory_readiness_audit_coverage_summary_only(self):
        result = evaluate_discretion_audit_inventory_bridge([self._item()])

        self.assertIn("inventory_validation", result)
        self.assertIn("audit_summary", result)
        self.assertIn("coverage_summary", result)
        self.assertIn("bridge_ready", result)
        self.assertIs(result["files_written"], False)
        self.assertIs(result["live_data_started"], False)

    def test_handles_partial_inventory_coverage_without_claiming_complete_coverage(self):
        result = evaluate_discretion_audit_inventory_bridge([self._item(area="trigger")])

        self.assertFalse(result["coverage_complete"])
        self.assertFalse(result["bridge_ready"])
        self.assertIn("setup_recognition", result["coverage_summary"]["missing_areas"])

    def test_identifies_coverage_gaps_through_existing_coverage_evaluator_behavior(self):
        result = evaluate_discretion_audit_inventory_bridge(
            [
                self._item(
                    area="trigger",
                    text="Reviewer may approve a trade.",
                )
            ]
        )

        self.assertEqual(result["audit_summary"]["forbidden_signal_discretion_count"], 1)
        self.assertEqual(result["coverage_summary"]["forbidden_signal_discretion_areas"], ["trigger"])
        self.assertIn("trigger", result["coverage_summary"]["missing_areas"])

    def test_preserves_all_no_go_boundaries(self):
        result = evaluate_discretion_audit_inventory_bridge([self._item()])

        for field_name in (
            "no_trade",
            "no_rule_change",
            "no_optimization",
            "no_file_write",
            "no_live_data",
            "no_controlled_shadow_data",
            "no_alert",
            "no_broker",
            "no_trade_boundary_preserved",
        ):
            self.assertIs(result[field_name], True)
        self.assertIs(result["rules_changed"], False)
        self.assertIs(result["optimization_started"], False)
        self.assertIs(result["files_written"], False)
        self.assertIs(result["live_data_started"], False)
        self.assertIs(result["controlled_shadow_data_started"], False)
        self.assertIs(result["alerts_sent"], False)
        self.assertIs(result["broker_or_trade_behavior_enabled"], False)

    def test_rejects_broker_order_account_options_pnl_trade_decision_fields_through_validator(self):
        forbidden_fields = (
            "broker",
            "order_id",
            "account",
            "options",
            "option_pnl",
            "trade_decision",
        )
        for forbidden_field in forbidden_fields:
            with self.subTest(forbidden_field=forbidden_field):
                result = evaluate_discretion_audit_inventory_bridge(
                    [self._item(unavailable_fields={"nested": [{forbidden_field: "x"}]})]
                )

                self.assertEqual(result["inventory_validation"]["items_accepted"], 0)
                self.assertEqual(result["inventory_validation"]["items_rejected"], 1)
                self.assertFalse(result["audit_executed"])

    def test_defensively_copies_nested_audit_and_coverage_summaries(self):
        result = evaluate_discretion_audit_inventory_bridge(
            [self._item(text="Reviewer may approve a trade.")]
        )

        result["audit_summary"]["findings"][0]["forbidden_signal_actions"].append("mutated")
        result["coverage_summary"]["missing_areas"].append("mutated")
        second = evaluate_discretion_audit_inventory_bridge(
            [self._item(text="Reviewer may approve a trade.")]
        )

        self.assertNotIn(
            "mutated",
            second["audit_summary"]["findings"][0]["forbidden_signal_actions"],
        )
        self.assertNotIn("mutated", second["coverage_summary"]["missing_areas"])

    def test_does_not_scan_fetch_start_threads_invoke_subprocesses_or_write_files(self):
        items = [self._item(area="diagnostics")]
        before = copy.deepcopy(items)

        with patch("builtins.open") as open_mock, patch(
            "socket.socket"
        ) as socket_mock, patch("subprocess.run") as subprocess_mock, patch(
            "threading.Thread"
        ) as thread_mock:
            result = evaluate_discretion_audit_inventory_bridge(items)

        self.assertEqual(items, before)
        self.assertIs(result["local_only"], True)
        self.assertIs(result["in_memory_only"], True)
        self.assertIs(result["files_written"], False)
        self.assertIs(result["live_data_started"], False)
        self.assertIs(result["controlled_shadow_data_started"], False)
        self.assertIs(result["alerts_sent"], False)
        open_mock.assert_not_called()
        socket_mock.assert_not_called()
        subprocess_mock.assert_not_called()
        thread_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
