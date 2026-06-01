import copy
import unittest
from unittest.mock import patch

from watcher_foundation import (
    DISCRETION_AUDIT_ALLOWED_HUMAN_DISCRETION,
    DISCRETION_AUDIT_AREAS,
    DISCRETION_AUDIT_RESULT_FIELDS,
    DISCRETION_AUDIT_VAGUE_PHRASES,
    audit_trading_plan_discretion,
)


class DiscretionAuditTests(unittest.TestCase):
    def _item(self, **overrides):
        item = {
            "item_id": "rule-1",
            "area": "trigger",
            "text": "Trigger must use explicit caller-provided proof.",
            "source": "caller-provided-contract",
            "review_context": "local discretion audit",
            "watch_only": True,
        }
        item.update(overrides)
        return item

    def test_accepts_caller_provided_in_memory_rule_and_contract_descriptions_only(self):
        items = [self._item()]
        before = copy.deepcopy(items)

        result = audit_trading_plan_discretion(items)

        self.assertEqual(items, before)
        self.assertEqual(set(DISCRETION_AUDIT_RESULT_FIELDS), set(result))
        self.assertIs(result["watch_only"], True)
        self.assertIs(result["discretion_audit_only"], True)
        self.assertEqual(result["items_reviewed"], 1)
        self.assertEqual(result["findings"], [])

    def test_hidden_discretionary_language_is_identified(self):
        result = audit_trading_plan_discretion(
            [
                self._item(
                    item_id="hidden-discretion",
                    area="setup recognition",
                    text="A good setup may be accepted when it looks good.",
                )
            ]
        )

        self.assertEqual(result["items_flagged"], 1)
        finding = result["findings"][0]
        self.assertEqual(finding["area"], "setup_recognition")
        self.assertTrue(finding["signal_discretion"])
        self.assertIn("looks good", finding["vague_phrases"])
        self.assertIn("good setup", finding["vague_phrases"])

    def test_required_vague_phrases_are_flagged(self):
        for phrase in DISCRETION_AUDIT_VAGUE_PHRASES:
            with self.subTest(phrase=phrase):
                result = audit_trading_plan_discretion(
                    [
                        self._item(
                            item_id=f"phrase-{phrase}",
                            text=f"The reviewer may use this if it {phrase}.",
                        )
                    ]
                )

                self.assertEqual(result["items_flagged"], 1)
                self.assertIn(phrase, result["findings"][0]["vague_phrases"])

    def test_discretion_is_classified_across_all_required_areas(self):
        area_inputs = {
            "setup_recognition": "setup recognition",
            "trigger": "trigger",
            "invalidation": "invalidation",
            "fresh_stale_spent": "fresh/stale/spent",
            "blocker_caution": "blocker/caution",
            "ranking_focus": "ranking/focus",
            "outcome_scoring": "outcome scoring",
            "diagnostics": "diagnostics",
            "user_workflow": "user workflow",
        }

        result = audit_trading_plan_discretion(
            [
                self._item(
                    item_id=area,
                    area=provided_area,
                    text="Reviewer may use judgment if the case looks good.",
                )
                for area, provided_area in area_inputs.items()
            ]
        )

        self.assertEqual({finding["area"] for finding in result["findings"]}, set(DISCRETION_AUDIT_AREAS))
        self.assertEqual(result["items_flagged"], len(DISCRETION_AUDIT_AREAS))

    def test_unsupported_area_is_marked_needs_review_without_fabricating_area(self):
        result = audit_trading_plan_discretion(
            [
                self._item(
                    item_id="unsupported-area",
                    area="new discretionary bucket",
                    text="Exact text without a vague phrase.",
                )
            ]
        )

        self.assertEqual(result["items_flagged"], 1)
        self.assertEqual(result["needs_review_count"], 1)
        self.assertEqual(result["findings"][0]["area"], "needs_review")
        self.assertEqual(result["findings"][0]["provided_area"], "new discretionary bucket")

    def test_safety_discretion_is_distinguished_from_signal_discretion(self):
        result = audit_trading_plan_discretion(
            [
                self._item(
                    item_id="safety",
                    area="user workflow",
                    text="Human review may apply a safety pause.",
                ),
                self._item(
                    item_id="signal",
                    area="trigger",
                    text="Human review may approve a trade.",
                ),
            ]
        )

        safety, signal = result["findings"]
        self.assertTrue(safety["safety_discretion"])
        self.assertFalse(safety["signal_discretion"])
        self.assertFalse(signal["safety_discretion"])
        self.assertTrue(signal["signal_discretion"])
        self.assertEqual(result["allowed_safety_discretion_count"], 1)
        self.assertEqual(result["forbidden_signal_discretion_count"], 1)

    def test_no_trade_veto_review_note_and_safety_pause_are_allowed(self):
        result = audit_trading_plan_discretion(
            [
                self._item(
                    item_id="veto",
                    area="user workflow",
                    text="Reviewer may record a no-trade veto.",
                ),
                self._item(
                    item_id="note",
                    area="user workflow",
                    text="Reviewer may add a review note.",
                ),
                self._item(
                    item_id="pause",
                    area="user workflow",
                    text="Reviewer may apply a safety pause.",
                ),
            ]
        )

        self.assertEqual(
            set(DISCRETION_AUDIT_ALLOWED_HUMAN_DISCRETION),
            {
                phrase
                for finding in result["findings"]
                for phrase in finding["allowed_human_discretion"]
            },
        )
        self.assertEqual(result["allowed_safety_discretion_count"], 3)
        self.assertEqual(result["forbidden_signal_discretion_count"], 0)

    def test_forbidden_signal_discretion_actions_are_flagged(self):
        forbidden_examples = {
            "create_signal": "Reviewer may create a signal when context helps.",
            "approve_trade": "Reviewer may approve a trade.",
            "override_missing_proof": "Reviewer may override missing proof.",
            "move_triggers": "Reviewer may move triggers.",
            "hide_failures": "Reviewer may hide failures.",
            "change_outcome_review_after_fact": (
                "Reviewer may change outcome review after the fact."
            ),
        }

        result = audit_trading_plan_discretion(
            [
                self._item(item_id=action, area="trigger", text=text)
                for action, text in forbidden_examples.items()
            ]
        )

        self.assertEqual(result["forbidden_signal_discretion_count"], 6)
        flagged_actions = {
            action
            for finding in result["findings"]
            for action in finding["forbidden_signal_actions"]
        }
        self.assertEqual(flagged_actions, set(forbidden_examples))

    def test_result_is_in_memory_only_and_boundaries_remain_false(self):
        result = audit_trading_plan_discretion([self._item()])

        self.assertIs(result["rules_changed"], False)
        self.assertIs(result["optimization_started"], False)
        self.assertIs(result["live_data_started"], False)
        self.assertIs(result["controlled_shadow_data_started"], False)
        self.assertIs(result["alerts_sent"], False)
        self.assertIs(result["files_written"], False)
        self.assertIs(result["broker_or_trade_behavior_enabled"], False)
        self.assertIs(result["no_trade_boundary_preserved"], True)

    def test_invalid_input_type_fails(self):
        with self.assertRaisesRegex(TypeError, "must be a list"):
            audit_trading_plan_discretion({"not": "a list"})

        with self.assertRaisesRegex(TypeError, "items\\[0\\] must be a dict"):
            audit_trading_plan_discretion(["not a dict"])

    def test_missing_required_item_field_fails(self):
        item = self._item()
        del item["review_context"]

        with self.assertRaisesRegex(ValueError, "review_context"):
            audit_trading_plan_discretion([item])

    def test_required_string_fields_must_be_strings(self):
        with self.assertRaisesRegex(TypeError, "text must be a string"):
            audit_trading_plan_discretion([self._item(text=["not", "text"])])

    def test_watch_only_false_fails(self):
        with self.assertRaisesRegex(ValueError, "watch_only must be True"):
            audit_trading_plan_discretion([self._item(watch_only=False)])

    def test_forbidden_broker_order_account_options_pnl_trade_decision_field_fails_recursively(self):
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
                item = self._item()
                item["nested"] = {"deeper": [{forbidden_field: "forbidden"}]}

                with self.assertRaisesRegex(
                    ValueError,
                    "Forbidden broker/order/trade field",
                ):
                    audit_trading_plan_discretion([item])

    def test_defensive_copies_are_returned(self):
        items = [
            self._item(
                item_id="copy-test",
                text="Reviewer may use judgment if the setup looks good.",
            )
        ]
        before = copy.deepcopy(items)

        first = audit_trading_plan_discretion(items)
        first["findings"][0]["vague_phrases"].append("mutated")
        first["findings"].append({"item_id": "mutated"})

        self.assertEqual(items, before)
        second = audit_trading_plan_discretion(items)
        self.assertEqual(len(second["findings"]), 1)
        self.assertNotIn("mutated", second["findings"][0]["vague_phrases"])

    def test_no_file_network_subprocess_live_data_controlled_shadow_or_alert_side_effects(self):
        items = [
            self._item(
                item_id="side-effects",
                text="Reviewer may add a review note.",
                area="user workflow",
            )
        ]
        before = copy.deepcopy(items)

        with patch("builtins.open") as open_mock, patch(
            "socket.socket"
        ) as socket_mock, patch("subprocess.run") as subprocess_mock, patch(
            "threading.Thread"
        ) as thread_mock:
            result = audit_trading_plan_discretion(items)

        self.assertEqual(items, before)
        self.assertIs(result["live_data_started"], False)
        self.assertIs(result["controlled_shadow_data_started"], False)
        self.assertIs(result["alerts_sent"], False)
        self.assertIs(result["broker_or_trade_behavior_enabled"], False)
        open_mock.assert_not_called()
        socket_mock.assert_not_called()
        subprocess_mock.assert_not_called()
        thread_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
