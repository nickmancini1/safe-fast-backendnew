import copy
import os
import unittest
from unittest import mock

from watcher_foundation.shadow_review import (
    SHADOW_REVIEW_EXPORT_REQUIRED_FIELDS,
    validate_shadow_review_export_shape,
)


class ShadowReviewExportShapeFinalBoundarySweepTests(unittest.TestCase):
    def _export(self, **overrides):
        export = {
            "export_id": "local-shadow-review-final-boundary-001",
            "created_from": "local_shadow_review_workflow_summary",
            "schema_version": 1,
            "samples": [
                {
                    "sample_id": "SYNTH-EXPORT-FINAL-IDEAL-001",
                    "setup_type": "Ideal",
                    "stage": "local_export_shape_final_boundary_sweep",
                    "trigger_status": "artifact_supported_watch_candidate",
                    "headline_news_status": "NEWS_UNCONFIRMED",
                    "duplicate_suppression_status": "not_duplicate",
                    "focus_winner_status": "not_compared",
                    "diagnostics_summary": (
                        "local watch-only export sample keeps unavailable "
                        "evidence explicit"
                    ),
                    "reviewer_label": "valid_watch_candidate",
                    "reviewer_notes": (
                        "local watch-only review does not approve live action"
                    ),
                    "no_trade_boundary_check": True,
                }
            ],
            "label_counts": {
                "valid_watch_candidate": 1,
                "needs_more_evidence": 0,
            },
            "setup_type_counts": {"Ideal": 1},
            "rejected_samples": [
                {
                    "sample_id": "SYNTH-EXPORT-FINAL-REJECTED-001",
                    "reason": (
                        "shadow review wording must preserve local and "
                        "watch-only boundaries"
                    ),
                }
            ],
            "no_trade_boundary_summary": {
                "watch_only": True,
                "no_trade_boundary_preserved": True,
                "samples_with_no_trade_boundary": 1,
                "live_trade_decision_status": "not_created",
            },
            "reviewer_notes": (
                "local watch-only export is for review only and preserves "
                "unavailable evidence"
            ),
            "unavailable_fields": {
                "trigger_level": "UNCONFIRMED",
                "invalidation_level": "UNCONFIRMED",
                "headline_news_context": "NEWS_UNCONFIRMED",
            },
        }
        export.update(overrides)
        return export

    def test_accepts_valid_in_memory_export_dicts(self):
        export = self._export()

        validated = validate_shadow_review_export_shape(export)

        self.assertEqual(validated, export)
        self.assertIsNot(validated, export)
        self.assertIsNot(validated["samples"], export["samples"])
        self.assertIsNot(validated["unavailable_fields"], export["unavailable_fields"])

    def test_rejects_invalid_export_dicts_with_useful_reasons(self):
        invalid_exports = (
            (
                ["not", "a", "dict"],
                TypeError,
                "shadow review export must be a dict",
            ),
            (
                self._export(samples="not-a-list"),
                TypeError,
                "shadow review export samples must be a list",
            ),
            (
                self._export(no_trade_boundary_summary={"watch_only": True}),
                ValueError,
                "shadow review export must preserve no-trade boundary",
            ),
            (
                self._export(samples=[{"nested": {"broker": "forbidden"}}]),
                ValueError,
                "Forbidden execution/trade field: samples.0.nested.broker",
            ),
        )

        for export, error_type, reason in invalid_exports:
            with self.subTest(reason=reason):
                with self.assertRaisesRegex(error_type, reason):
                    validate_shadow_review_export_shape(export)

    def test_missing_required_fields_fail(self):
        for field_name in SHADOW_REVIEW_EXPORT_REQUIRED_FIELDS:
            with self.subTest(field_name=field_name):
                export = self._export()
                export.pop(field_name)

                with self.assertRaisesRegex(ValueError, field_name):
                    validate_shadow_review_export_shape(export)

    def test_bad_field_types_fail(self):
        invalid_type_cases = {
            "export_id": 1001,
            "created_from": ("workflow",),
            "schema_version": "1",
            "samples": {"sample_id": "SYNTH-INVALID"},
            "label_counts": [("valid_watch_candidate", 1)],
            "setup_type_counts": [("Ideal", 1)],
            "rejected_samples": {"sample_id": "SYNTH-INVALID"},
            "no_trade_boundary_summary": [("watch_only", True)],
            "reviewer_notes": ["local watch-only"],
            "unavailable_fields": "trigger_level",
        }

        for field_name, invalid_value in invalid_type_cases.items():
            with self.subTest(field_name=field_name):
                with self.assertRaisesRegex(TypeError, field_name):
                    validate_shadow_review_export_shape(
                        self._export(**{field_name: invalid_value})
                    )

    def test_nested_broker_order_account_option_pnl_and_trade_decision_fields_fail(self):
        forbidden_cases = {
            "broker": {"samples": [{"review": {"broker": "forbidden"}}]},
            "order": {"samples": [{"review": [{"order": "forbidden"}]}]},
            "account": {"reviewer_notes": {"account": "forbidden"}},
            "option": {"unavailable_fields": {"nested": {"option": "forbidden"}}},
            "p_and_l": {"label_counts": {"nested": {"p_and_l": "forbidden"}}},
            "p&l": {"setup_type_counts": {"nested": {"p&l": "forbidden"}}},
            "trade_decision": {
                "rejected_samples": [
                    {
                        "sample_id": "SYNTH-INVALID-TRADE-DECISION",
                        "reason": "invalid local review",
                        "details": {"trade_decision": "forbidden"},
                    }
                ]
            },
        }

        for field_name, overrides in forbidden_cases.items():
            with self.subTest(field_name=field_name):
                with self.assertRaisesRegex(
                    ValueError, "Forbidden execution/trade field"
                ):
                    validate_shadow_review_export_shape(self._export(**overrides))

    def test_no_live_trade_approval_is_allowed(self):
        live_approval_cases = {
            "live_trade_approval": {
                "samples": [{"review": {"live_trade_approval": False}}]
            },
            "approved_trade": {
                "no_trade_boundary_summary": {
                    "watch_only": True,
                    "no_trade_boundary_preserved": True,
                    "approved_trade": False,
                }
            },
            "trade_approval": {
                "unavailable_fields": [{"trade_approval": "not_allowed"}]
            },
        }

        for field_name, overrides in live_approval_cases.items():
            with self.subTest(field_name=field_name):
                with self.assertRaisesRegex(
                    ValueError, "Forbidden execution/trade field"
                ):
                    validate_shadow_review_export_shape(self._export(**overrides))

    def test_watch_only_no_trade_boundary_is_preserved(self):
        valid_boundary = {
            "watch_only": True,
            "no_trade_boundary_preserved": True,
            "samples_with_no_trade_boundary": 1,
        }
        invalid_boundaries = (
            {},
            {"watch_only": False, "no_trade_boundary_preserved": True},
            {"watch_only": True, "no_trade_boundary_preserved": False},
            {"watch_only": "true", "no_trade_boundary_preserved": True},
        )

        validated = validate_shadow_review_export_shape(
            self._export(no_trade_boundary_summary=valid_boundary)
        )
        self.assertEqual(validated["no_trade_boundary_summary"], valid_boundary)

        for boundary_summary in invalid_boundaries:
            with self.subTest(boundary_summary=boundary_summary):
                with self.assertRaisesRegex(ValueError, "boundary"):
                    validate_shadow_review_export_shape(
                        self._export(no_trade_boundary_summary=boundary_summary)
                    )

    def test_rejected_sample_reasons_are_preserved(self):
        rejected_samples = [
            {
                "sample_id": "SYNTH-EXPORT-FINAL-INVALID-LABEL-001",
                "reason": "Unsupported reviewer_label: approve_real_trade",
            },
            {
                "sample_id": "SYNTH-EXPORT-FINAL-INVALID-BOUNDARY-001",
                "reason": "no_trade_boundary_check must be true",
            },
            {
                "sample_id": "UNAVAILABLE",
                "reason": "shadow review sample must be a dict",
            },
        ]

        validated = validate_shadow_review_export_shape(
            self._export(rejected_samples=copy.deepcopy(rejected_samples))
        )

        self.assertEqual(validated["rejected_samples"], rejected_samples)
        self.assertIsNot(validated["rejected_samples"], rejected_samples)

    def test_validation_is_deterministic_on_repeated_runs(self):
        export = self._export()
        original_export = copy.deepcopy(export)

        first = validate_shadow_review_export_shape(export)
        second = validate_shadow_review_export_shape(export)
        third = validate_shadow_review_export_shape(copy.deepcopy(export))

        self.assertEqual(first, second)
        self.assertEqual(second, third)
        self.assertEqual(export, original_export)

    def test_validation_creates_no_files_reports_logs_or_external_calls(self):
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
        for forbidden_output in ("file", "report", "log", "alert"):
            self.assertNotIn(forbidden_output, validated)

    def test_final_boundary_sweep_is_included_in_local_validation_suite(self):
        from tests import test_watcher_foundation_local_validation_suite as suite_module

        self.assertIn(
            "tests.test_shadow_review_export_shape_final_boundary_sweep",
            suite_module.WATCHER_FOUNDATION_TEST_MODULES,
        )


if __name__ == "__main__":
    unittest.main()
