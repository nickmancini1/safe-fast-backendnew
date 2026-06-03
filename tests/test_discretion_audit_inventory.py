import copy
import unittest
from unittest.mock import patch

from watcher_foundation import (
    DISCRETION_AUDIT_INVENTORY_ALLOWED_AREAS,
    DISCRETION_AUDIT_INVENTORY_REQUIRED_FIELDS,
    DISCRETION_AUDIT_INVENTORY_RESULT_FIELDS,
    validate_discretion_audit_inventory,
    validate_discretion_audit_inventory_item,
)


class DiscretionAuditInventoryTests(unittest.TestCase):
    def _item(self, area="setup recognition", **overrides):
        item = {
            "item_id": f"rule-{area}",
            "area": area,
            "source": "caller-provided-rule-contract",
            "text": "Rule text supplied by caller for inventory validation.",
            "rule_purpose": "Document the rule purpose before later audit work.",
            "audit_readiness": "ready_for_later_audit",
            "unavailable_fields": ["numeric_trigger_level_unavailable"],
            "watch_only": True,
        }
        item.update(overrides)
        return item

    def test_valid_caller_provided_in_memory_inventory_items_pass(self):
        items = [self._item(area) for area in DISCRETION_AUDIT_INVENTORY_ALLOWED_AREAS]
        before = copy.deepcopy(items)

        result = validate_discretion_audit_inventory(items)

        self.assertEqual(items, before)
        self.assertEqual(set(DISCRETION_AUDIT_INVENTORY_RESULT_FIELDS), set(result))
        self.assertEqual(result["items_processed"], len(items))
        self.assertEqual(result["items_accepted"], len(items))
        self.assertEqual(result["items_rejected"], 0)
        self.assertEqual(
            result["covered_areas"],
            list(DISCRETION_AUDIT_INVENTORY_ALLOWED_AREAS),
        )
        self.assertEqual(result["missing_required_areas"], [])

    def test_single_item_validation_returns_accepted_defensive_copy(self):
        item = self._item(unavailable_fields={"trigger": "unavailable"})
        accepted = validate_discretion_audit_inventory_item(item)

        self.assertTrue(accepted["accepted"])
        self.assertEqual(accepted["area"], "setup recognition")
        self.assertEqual(accepted["unavailable_fields"], {"trigger": "unavailable"})

        accepted["unavailable_fields"]["trigger"] = "mutated"
        self.assertEqual(item["unavailable_fields"], {"trigger": "unavailable"})

    def test_missing_required_fields_fail(self):
        for field_name in DISCRETION_AUDIT_INVENTORY_REQUIRED_FIELDS:
            with self.subTest(field_name=field_name):
                item = self._item()
                del item[field_name]

                with self.assertRaisesRegex(ValueError, field_name):
                    validate_discretion_audit_inventory_item(item)

    def test_unsupported_area_fails(self):
        with self.assertRaisesRegex(ValueError, "allowed SAFE-FAST area"):
            validate_discretion_audit_inventory_item(self._item(area="position sizing"))

    def test_unavailable_fields_are_preserved_explicitly(self):
        item = self._item(
            area="trigger",
            unavailable_fields={
                "numeric_trigger": "unavailable",
                "source_note": "not caller-provided",
            },
        )

        result = validate_discretion_audit_inventory([item])

        self.assertEqual(
            result["accepted_items"][0]["unavailable_fields"],
            {
                "numeric_trigger": "unavailable",
                "source_note": "not caller-provided",
            },
        )
        self.assertEqual(
            result["unavailable_fields"],
            [
                {
                    "item_id": "rule-trigger",
                    "unavailable_fields": {
                        "numeric_trigger": "unavailable",
                        "source_note": "not caller-provided",
                    },
                }
            ],
        )

    def test_broker_order_account_options_pnl_trade_decision_fields_are_rejected_recursively(self):
        forbidden_fields = (
            "broker",
            "order_id",
            "account",
            "options",
            "option_pnl",
            "pnl",
            "trade_decision",
        )
        for forbidden_field in forbidden_fields:
            with self.subTest(forbidden_field=forbidden_field):
                item = self._item(unavailable_fields={"nested": [{forbidden_field: "x"}]})

                with self.assertRaisesRegex(
                    ValueError,
                    "Forbidden broker/order/trade field",
                ):
                    validate_discretion_audit_inventory_item(item)

    def test_inventory_summary_returns_accepted_and_rejected_items_in_memory(self):
        valid_item = self._item(area="trigger")
        invalid_item = self._item(area="position sizing", item_id="bad-area")

        result = validate_discretion_audit_inventory([valid_item, invalid_item])

        self.assertEqual(result["items_processed"], 2)
        self.assertEqual(result["items_accepted"], 1)
        self.assertEqual(result["items_rejected"], 1)
        self.assertEqual(result["accepted_items"][0]["item_id"], "rule-trigger")
        self.assertEqual(result["rejected_items"][0]["item_id"], "bad-area")
        self.assertFalse(result["rejected_items"][0]["accepted"])

    def test_missing_required_coverage_areas_are_identified(self):
        result = validate_discretion_audit_inventory(
            [
                self._item(area="setup recognition"),
                self._item(area="trigger"),
            ]
        )

        self.assertEqual(result["covered_areas"], ["setup recognition", "trigger"])
        self.assertEqual(
            result["missing_required_areas"],
            [
                "invalidation",
                "fresh/stale/spent",
                "blocker/caution",
                "ranking/focus",
                "outcome scoring",
                "diagnostics",
                "user workflow",
            ],
        )

    def test_audit_rules_and_optimization_remain_false(self):
        result = validate_discretion_audit_inventory([self._item()])

        self.assertIs(result["audit_started"], False)
        self.assertIs(result["rules_changed"], False)
        self.assertIs(result["optimization_started"], False)

    def test_invalid_input_type_fails(self):
        with self.assertRaisesRegex(TypeError, "must be a list"):
            validate_discretion_audit_inventory({})

    def test_invalid_item_type_fails(self):
        with self.assertRaisesRegex(TypeError, "items\\[0\\] must be a dict"):
            validate_discretion_audit_inventory(["not-a-dict"])

    def test_invalid_field_types_fail(self):
        for field_name in (
            "item_id",
            "area",
            "source",
            "text",
            "rule_purpose",
            "audit_readiness",
        ):
            with self.subTest(field_name=field_name):
                with self.assertRaisesRegex(TypeError, field_name):
                    validate_discretion_audit_inventory_item(
                        self._item(**{field_name: 123})
                    )

        with self.assertRaisesRegex(TypeError, "unavailable_fields"):
            validate_discretion_audit_inventory_item(
                self._item(unavailable_fields="not-explicit-list-or-dict")
            )

    def test_watch_only_false_fails(self):
        with self.assertRaisesRegex(ValueError, "watch_only"):
            validate_discretion_audit_inventory_item(self._item(watch_only=False))

        result = validate_discretion_audit_inventory([self._item(watch_only=False)])
        self.assertEqual(result["items_accepted"], 0)
        self.assertEqual(result["items_rejected"], 1)

    def test_defensive_copies_are_returned(self):
        items = [self._item(area="trigger")]
        before = copy.deepcopy(items)

        first = validate_discretion_audit_inventory(items)
        first["accepted_items"][0]["unavailable_fields"].append("mutated")
        first["unavailable_fields"][0]["unavailable_fields"].append("mutated")
        first["covered_areas"].append("mutated")

        self.assertEqual(items, before)
        second = validate_discretion_audit_inventory(items)
        self.assertNotIn("mutated", second["accepted_items"][0]["unavailable_fields"])
        self.assertNotIn("mutated", second["unavailable_fields"][0]["unavailable_fields"])
        self.assertNotIn("mutated", second["covered_areas"])

    def test_no_file_network_subprocess_live_data_controlled_shadow_or_alert_side_effects(self):
        items = [self._item(area="diagnostics")]
        before = copy.deepcopy(items)

        with patch("builtins.open") as open_mock, patch(
            "socket.socket"
        ) as socket_mock, patch("subprocess.run") as subprocess_mock, patch(
            "threading.Thread"
        ) as thread_mock:
            result = validate_discretion_audit_inventory(items)

        self.assertEqual(items, before)
        self.assertIs(result["watch_only"], True)
        self.assertIs(result["discretion_audit_inventory_only"], True)
        self.assertIs(result["no_trade_boundary_preserved"], True)
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
