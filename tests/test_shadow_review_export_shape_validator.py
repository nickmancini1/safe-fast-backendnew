import copy
import os
import unittest
from collections import UserDict
from unittest import mock

from watcher_foundation.shadow_review import (
    SHADOW_REVIEW_EXPORT_REQUIRED_FIELDS,
    validate_shadow_review_export_shape,
)


class ShadowReviewExportShapeValidatorTests(unittest.TestCase):
    def _export(self, **overrides):
        export = {
            "export_id": "local-shadow-review-export-001",
            "created_from": "local_shadow_review_workflow_summary",
            "schema_version": 1,
            "samples": [
                {
                    "sample_id": "SYNTH-SHADOW-IDEAL-001",
                    "setup_type": "Ideal",
                    "reviewer_label": "valid_watch_candidate",
                    "no_trade_boundary_check": True,
                }
            ],
            "label_counts": {"valid_watch_candidate": 1},
            "setup_type_counts": {"Ideal": 1},
            "rejected_samples": [
                {
                    "sample_id": "SYNTH-SHADOW-REJECTED-001",
                    "reason": "Unsupported reviewer_label: unsupported",
                }
            ],
            "no_trade_boundary_summary": {
                "watch_only": True,
                "no_trade_boundary_preserved": True,
                "samples_with_no_trade_boundary": 1,
            },
            "reviewer_notes": (
                "local watch-only export preserves unavailable evidence and "
                "does not approve live action"
            ),
            "unavailable_fields": [
                "TRIGGER_LEVEL_UNCONFIRMED",
                "INVALIDATION_UNCONFIRMED",
            ],
        }
        export.update(overrides)
        return export

    def test_valid_export_shape_passes(self):
        export = self._export()

        validated = validate_shadow_review_export_shape(export)

        self.assertEqual(validated, export)
        self.assertIsNot(validated, export)
        self.assertIsNot(validated["samples"], export["samples"])

    def test_missing_required_fields_fail(self):
        for field_name in SHADOW_REVIEW_EXPORT_REQUIRED_FIELDS:
            with self.subTest(field_name=field_name):
                export = self._export()
                export.pop(field_name)

                with self.assertRaisesRegex(ValueError, field_name):
                    validate_shadow_review_export_shape(export)

    def test_non_dict_input_fails(self):
        with self.assertRaisesRegex(TypeError, "must be a dict"):
            validate_shadow_review_export_shape(["not", "an", "export"])

        with self.assertRaisesRegex(TypeError, "must be a dict"):
            validate_shadow_review_export_shape(UserDict(self._export()))

    def test_invalid_container_types_fail(self):
        invalid_cases = {
            "samples": ("sample",),
            "label_counts": [("valid_watch_candidate", 1)],
            "setup_type_counts": [("Ideal", 1)],
            "rejected_samples": {"sample_id": "SYNTH-INVALID-001"},
            "no_trade_boundary_summary": [
                ("watch_only", True),
                ("no_trade_boundary_preserved", True),
            ],
        }

        for field_name, invalid_value in invalid_cases.items():
            with self.subTest(field_name=field_name):
                export = self._export(**{field_name: invalid_value})

                with self.assertRaisesRegex(TypeError, field_name):
                    validate_shadow_review_export_shape(export)

    def test_rejected_sample_reasons_are_preserved(self):
        rejected_samples = [
            {
                "sample_id": "SYNTH-SHADOW-INVALID-LABEL-001",
                "reason": "Unsupported reviewer_label: approve_real_trade",
            },
            {
                "sample_id": "SYNTH-SHADOW-INVALID-BOUNDARY-001",
                "reason": "no_trade_boundary_check must be true",
            },
        ]

        validated = validate_shadow_review_export_shape(
            self._export(rejected_samples=copy.deepcopy(rejected_samples))
        )

        self.assertEqual(validated["rejected_samples"], rejected_samples)

    def test_nested_forbidden_execution_trade_fields_fail(self):
        forbidden_cases = {
            "broker": {"samples": [{"artifact": {"broker": "forbidden"}}]},
            "order": {"samples": [{"artifact": [{"order_id": "forbidden"}]}]},
            "account": {"reviewer_notes": {"account": "forbidden"}},
            "option": {"unavailable_fields": [{"option_symbol": "forbidden"}]},
            "p_and_l": {"label_counts": {"nested": {"p_and_l": "forbidden"}}},
            "p&l": {"setup_type_counts": {"nested": {"p&l": "forbidden"}}},
            "trade_decision": {
                "samples": [{"artifact": {"trade_decision": "forbidden"}}]
            },
            "live_trade_approval": {
                "no_trade_boundary_summary": {
                    "watch_only": True,
                    "no_trade_boundary_preserved": True,
                    "live_trade_approval": False,
                }
            },
        }

        for field_name, overrides in forbidden_cases.items():
            with self.subTest(field_name=field_name):
                with self.assertRaisesRegex(
                    ValueError, "Forbidden execution/trade field"
                ):
                    validate_shadow_review_export_shape(self._export(**overrides))

    def test_watch_only_no_trade_boundary_is_required(self):
        invalid_boundary_cases = (
            {"no_trade_boundary_preserved": True},
            {"watch_only": False, "no_trade_boundary_preserved": True},
            {"watch_only": True},
            {"watch_only": True, "no_trade_boundary_preserved": False},
        )

        for boundary_summary in invalid_boundary_cases:
            with self.subTest(boundary_summary=boundary_summary):
                with self.assertRaisesRegex(ValueError, "boundary"):
                    validate_shadow_review_export_shape(
                        self._export(
                            no_trade_boundary_summary=boundary_summary
                        )
                    )

    def test_deterministic_repeated_validation(self):
        export = self._export()
        original_export = copy.deepcopy(export)

        first_validated = validate_shadow_review_export_shape(export)
        second_validated = validate_shadow_review_export_shape(export)

        self.assertEqual(first_validated, second_validated)
        self.assertEqual(export, original_export)

    def test_no_files_reports_logs_or_live_calls_are_created(self):
        export = self._export()
        blocked = AssertionError("external side effect")
        before = sorted(os.listdir(os.getcwd()))

        with mock.patch("builtins.open", side_effect=blocked), mock.patch(
            "logging.Logger._log", side_effect=blocked
        ), mock.patch(
            "threading.Thread.start", side_effect=blocked
        ), mock.patch(
            "sched.scheduler.run", side_effect=blocked
        ), mock.patch(
            "subprocess.Popen", side_effect=blocked
        ), mock.patch(
            "subprocess.run", side_effect=blocked
        ), mock.patch(
            "socket.socket", side_effect=blocked
        ), mock.patch(
            "urllib.request.urlopen", side_effect=blocked
        ):
            validated = validate_shadow_review_export_shape(export)
        after = sorted(os.listdir(os.getcwd()))

        self.assertEqual(before, after)
        self.assertNotIn("file", validated)
        self.assertNotIn("report", validated)
        self.assertNotIn("log", validated)
        self.assertNotIn("alert", validated)

    def test_local_validation_suite_includes_export_shape_validator(self):
        from tests import test_watcher_foundation_local_validation_suite as suite_module

        self.assertIn(
            "tests.test_shadow_review_export_shape_validator",
            suite_module.WATCHER_FOUNDATION_TEST_MODULES,
        )


if __name__ == "__main__":
    unittest.main()
