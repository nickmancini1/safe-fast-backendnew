import copy
import unittest
from unittest.mock import patch

from watcher_foundation import (
    DISCRETION_AUDIT_COVERAGE_RESULT_FIELDS,
    DISCRETION_AUDIT_REQUIRED_COVERAGE_AREAS,
    evaluate_discretion_audit_coverage,
)


class DiscretionAuditCoverageTests(unittest.TestCase):
    def _finding(self, area, **overrides):
        finding = {
            "area": area,
            "coverage_status": "covered",
            "signal_discretion": False,
            "safety_discretion": False,
        }
        finding.update(overrides)
        return finding

    def _summary(self, findings=None, **overrides):
        summary = {
            "watch_only": True,
            "discretion_audit_only": True,
            "rules_changed": False,
            "optimization_started": False,
            "findings": (
                [self._finding(area) for area in DISCRETION_AUDIT_REQUIRED_COVERAGE_AREAS]
                if findings is None
                else findings
            ),
            "no_trade_boundary_preserved": True,
            "live_data_started": False,
            "controlled_shadow_data_started": False,
            "alerts_sent": False,
            "files_written": False,
            "broker_or_trade_behavior_enabled": False,
        }
        summary.update(overrides)
        return summary

    def test_accepts_in_memory_discretion_audit_summary_only(self):
        summary = self._summary()
        before = copy.deepcopy(summary)

        result = evaluate_discretion_audit_coverage(summary)

        self.assertEqual(summary, before)
        self.assertEqual(set(DISCRETION_AUDIT_COVERAGE_RESULT_FIELDS), set(result))
        self.assertIs(result["watch_only"], True)
        self.assertIs(result["discretion_audit_coverage_only"], True)
        self.assertEqual(
            result["required_areas"],
            list(DISCRETION_AUDIT_REQUIRED_COVERAGE_AREAS),
        )
        self.assertEqual(
            result["covered_areas"],
            list(DISCRETION_AUDIT_REQUIRED_COVERAGE_AREAS),
        )

    def test_all_required_trading_plan_areas_are_required_for_full_coverage(self):
        result = evaluate_discretion_audit_coverage(self._summary())

        self.assertEqual(
            result["required_areas"],
            [
                "setup_recognition",
                "trigger",
                "invalidation",
                "fresh_stale_spent",
                "blocker_caution",
                "ranking_focus",
                "outcome_scoring",
                "diagnostics",
                "user_workflow",
            ],
        )
        self.assertTrue(result["coverage_complete"])
        self.assertEqual(result["missing_areas"], [])

    def test_missing_audit_areas_are_identified(self):
        covered = [
            area
            for area in DISCRETION_AUDIT_REQUIRED_COVERAGE_AREAS
            if area not in {"setup_recognition", "trigger"}
        ]

        result = evaluate_discretion_audit_coverage(
            self._summary(findings=[self._finding(area) for area in covered])
        )

        self.assertEqual(result["missing_areas"], ["setup_recognition", "trigger"])
        self.assertFalse(result["coverage_complete"])

    def test_each_required_area_is_missing_when_not_supplied(self):
        for missing_area in DISCRETION_AUDIT_REQUIRED_COVERAGE_AREAS:
            with self.subTest(missing_area=missing_area):
                findings = [
                    self._finding(area)
                    for area in DISCRETION_AUDIT_REQUIRED_COVERAGE_AREAS
                    if area != missing_area
                ]

                result = evaluate_discretion_audit_coverage(
                    self._summary(findings=findings)
                )

                self.assertIn(missing_area, result["missing_areas"])
                self.assertFalse(result["coverage_complete"])

    def test_forbidden_signal_discretion_areas_are_identified_and_not_safe_coverage(self):
        findings = [
            self._finding("setup_recognition"),
            self._finding(
                "trigger",
                coverage_status="forbidden_signal_discretion",
                signal_discretion=True,
            ),
            *[
                self._finding(area)
                for area in DISCRETION_AUDIT_REQUIRED_COVERAGE_AREAS
                if area not in {"setup_recognition", "trigger"}
            ],
        ]

        result = evaluate_discretion_audit_coverage(self._summary(findings=findings))

        self.assertEqual(result["forbidden_signal_discretion_areas"], ["trigger"])
        self.assertIn("trigger", result["missing_areas"])
        self.assertNotIn("trigger", result["covered_areas"])
        self.assertFalse(result["coverage_complete"])

    def test_safety_discretion_only_areas_are_identified(self):
        result = evaluate_discretion_audit_coverage(
            self._summary(
                findings=[
                    self._finding(
                        "user_workflow",
                        coverage_status="allowed_safety_discretion",
                        safety_discretion=True,
                    ),
                    *[
                        self._finding(area)
                        for area in DISCRETION_AUDIT_REQUIRED_COVERAGE_AREAS
                        if area != "user_workflow"
                    ],
                ]
            )
        )

        self.assertEqual(result["safety_discretion_only_areas"], ["user_workflow"])
        self.assertIn("user_workflow", result["covered_areas"])
        self.assertTrue(result["coverage_complete"])

    def test_inconclusive_unavailable_evidence_and_needs_review_areas_are_identified(self):
        statuses = {
            "trigger": "inconclusive",
            "invalidation": "unavailable_evidence",
            "diagnostics": "needs_review",
        }
        findings = [
            self._finding(area, coverage_status=statuses.get(area, "covered"))
            for area in DISCRETION_AUDIT_REQUIRED_COVERAGE_AREAS
        ]

        result = evaluate_discretion_audit_coverage(self._summary(findings=findings))

        self.assertEqual(
            result["needs_review_areas"],
            ["trigger", "invalidation", "diagnostics"],
        )
        self.assertEqual(
            result["missing_areas"],
            ["trigger", "invalidation", "diagnostics"],
        )
        self.assertFalse(result["coverage_complete"])

    def test_result_is_in_memory_only_and_boundary_values_are_preserved(self):
        result = evaluate_discretion_audit_coverage(self._summary())

        self.assertIs(result["rules_changed"], False)
        self.assertIs(result["optimization_started"], False)
        self.assertIs(result["no_trade_boundary_preserved"], True)
        self.assertIs(result["live_data_started"], False)
        self.assertIs(result["controlled_shadow_data_started"], False)
        self.assertIs(result["alerts_sent"], False)
        self.assertIs(result["files_written"], False)
        self.assertIs(result["broker_or_trade_behavior_enabled"], False)

    def test_invalid_input_type_fails(self):
        with self.assertRaisesRegex(TypeError, "must be a dict"):
            evaluate_discretion_audit_coverage([])

    def test_missing_required_summary_field_fails(self):
        summary = self._summary()
        del summary["findings"]

        with self.assertRaisesRegex(ValueError, "findings"):
            evaluate_discretion_audit_coverage(summary)

    def test_boundary_failure_fails(self):
        for field_name, bad_value in {
            "watch_only": False,
            "discretion_audit_only": False,
            "rules_changed": True,
            "optimization_started": True,
            "no_trade_boundary_preserved": False,
            "live_data_started": True,
            "controlled_shadow_data_started": True,
            "alerts_sent": True,
            "files_written": True,
            "broker_or_trade_behavior_enabled": True,
        }.items():
            with self.subTest(field_name=field_name):
                with self.assertRaisesRegex(ValueError, field_name):
                    evaluate_discretion_audit_coverage(
                        self._summary(**{field_name: bad_value})
                    )

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
                summary = self._summary()
                summary["nested"] = {"deeper": [{forbidden_field: "forbidden"}]}

                with self.assertRaisesRegex(
                    ValueError,
                    "Forbidden broker/order/trade field",
                ):
                    evaluate_discretion_audit_coverage(summary)

    def test_defensive_copies_are_returned(self):
        summary = self._summary()
        before = copy.deepcopy(summary)

        first = evaluate_discretion_audit_coverage(summary)
        first["required_areas"].append("mutated")
        first["covered_areas"].append("mutated")
        first["missing_areas"].append("mutated")

        self.assertEqual(summary, before)
        second = evaluate_discretion_audit_coverage(summary)
        self.assertNotIn("mutated", second["required_areas"])
        self.assertNotIn("mutated", second["covered_areas"])
        self.assertNotIn("mutated", second["missing_areas"])

    def test_no_file_network_subprocess_live_data_controlled_shadow_or_alert_side_effects(self):
        summary = self._summary()
        before = copy.deepcopy(summary)

        with patch("builtins.open") as open_mock, patch(
            "socket.socket"
        ) as socket_mock, patch("subprocess.run") as subprocess_mock, patch(
            "threading.Thread"
        ) as thread_mock:
            result = evaluate_discretion_audit_coverage(summary)

        self.assertEqual(summary, before)
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
