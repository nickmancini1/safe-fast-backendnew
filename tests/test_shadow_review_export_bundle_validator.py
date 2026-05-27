import copy
import os
import tempfile
import unittest
from collections import UserDict
from unittest import mock

from watcher_foundation.shadow_review import (
    SHADOW_REVIEW_EXPORT_BUNDLE_REQUIRED_FIELDS,
    validate_shadow_review_export_bundle,
)


class ShadowReviewExportBundleValidatorTests(unittest.TestCase):
    def _export(self, **overrides):
        export = {
            "export_id": "local-shadow-review-export-001",
            "created_from": "local_shadow_review_workflow_summary",
            "schema_version": 1,
            "samples": [
                {
                    "sample_id": "SYNTH-BUNDLE-IDEAL-001",
                    "setup_type": "Ideal",
                    "stage": "local_export_bundle_validator",
                    "trigger_status": "artifact_supported_watch_candidate",
                    "headline_news_status": "NEWS_UNCONFIRMED",
                    "duplicate_suppression_status": "not_duplicate",
                    "focus_winner_status": "not_compared",
                    "diagnostics_summary": (
                        "local watch-only bundle export sample keeps unavailable "
                        "evidence explicit"
                    ),
                    "reviewer_label": "valid_watch_candidate",
                    "reviewer_notes": (
                        "local watch-only review does not approve live action"
                    ),
                    "no_trade_boundary_check": True,
                }
            ],
            "label_counts": {"valid_watch_candidate": 1},
            "setup_type_counts": {"Ideal": 1},
            "rejected_samples": [
                {
                    "sample_id": "SYNTH-BUNDLE-REJECTED-SAMPLE-001",
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
            "unavailable_fields": {
                "trigger_level": "TRIGGER_LEVEL_UNCONFIRMED",
                "invalidation_level": "INVALIDATION_UNCONFIRMED",
            },
        }
        export.update(overrides)
        return export

    def _bundle(self, **overrides):
        bundle = {
            "bundle_id": "local-shadow-review-export-bundle-001",
            "schema_version": 1,
            "created_from": "local_shadow_review_exports",
            "exports": [self._export()],
            "bundle_counts": {
                "exports_total": 1,
                "exports_validated": 1,
                "rejected_exports": 1,
            },
            "rejected_exports": [
                {
                    "export_id": "local-shadow-review-export-rejected-001",
                    "reason": "shadow review export samples must be a list",
                }
            ],
            "no_trade_boundary_summary": {
                "watch_only": True,
                "no_trade_boundary_preserved": True,
                "exports_with_no_trade_boundary": 1,
            },
            "reviewer_notes": (
                "local watch-only bundle preserves unavailable evidence and "
                "does not approve live action"
            ),
            "unavailable_fields": [
                "TRIGGER_LEVEL_UNCONFIRMED",
                "INVALIDATION_UNCONFIRMED",
            ],
        }
        bundle.update(overrides)
        return bundle

    def test_valid_export_bundle_passes(self):
        bundle = self._bundle()

        validated = validate_shadow_review_export_bundle(bundle)

        self.assertEqual(validated, bundle)
        self.assertIsNot(validated, bundle)
        self.assertIsNot(validated["exports"], bundle["exports"])
        self.assertIsNot(validated["exports"][0], bundle["exports"][0])

    def test_missing_required_bundle_fields_fail(self):
        for field_name in SHADOW_REVIEW_EXPORT_BUNDLE_REQUIRED_FIELDS:
            with self.subTest(field_name=field_name):
                bundle = self._bundle()
                bundle.pop(field_name)

                with self.assertRaisesRegex(ValueError, field_name):
                    validate_shadow_review_export_bundle(bundle)

    def test_non_dict_input_fails(self):
        with self.assertRaisesRegex(TypeError, "must be a dict"):
            validate_shadow_review_export_bundle(["not", "a", "bundle"])

        with self.assertRaisesRegex(TypeError, "must be a dict"):
            validate_shadow_review_export_bundle(UserDict(self._bundle()))

    def test_bad_container_types_fail(self):
        invalid_cases = {
            "exports": (self._export(),),
            "bundle_counts": [("exports_total", 1)],
            "rejected_exports": {"export_id": "SYNTH-INVALID-EXPORT"},
            "no_trade_boundary_summary": [
                ("watch_only", True),
                ("no_trade_boundary_preserved", True),
            ],
        }

        for field_name, invalid_value in invalid_cases.items():
            with self.subTest(field_name=field_name):
                bundle = self._bundle(**{field_name: invalid_value})

                with self.assertRaisesRegex(TypeError, field_name):
                    validate_shadow_review_export_bundle(bundle)

    def test_invalid_nested_export_fails_with_useful_reason(self):
        invalid_export = self._export(samples="not-a-list")

        with self.assertRaisesRegex(
            TypeError, "shadow review export samples must be a list"
        ):
            validate_shadow_review_export_bundle(
                self._bundle(exports=[invalid_export])
            )

    def test_rejected_export_reasons_are_preserved(self):
        rejected_exports = [
            {
                "export_id": "SYNTH-BUNDLE-INVALID-EXPORT-001",
                "reason": "shadow review export samples must be a list",
            },
            {
                "export_id": "SYNTH-BUNDLE-INVALID-EXPORT-002",
                "reason": "shadow review export must preserve no-trade boundary",
            },
        ]

        validated = validate_shadow_review_export_bundle(
            self._bundle(rejected_exports=copy.deepcopy(rejected_exports))
        )

        self.assertEqual(validated["rejected_exports"], rejected_exports)
        self.assertIsNot(validated["rejected_exports"], rejected_exports)

    def test_nested_forbidden_execution_trade_fields_fail(self):
        forbidden_cases = {
            "broker": {"exports": [self._export(samples=[{"broker": "forbidden"}])]},
            "order": {"bundle_counts": {"nested": {"order_id": "forbidden"}}},
            "account": {"rejected_exports": [{"account": "forbidden"}]},
            "option": {"unavailable_fields": [{"option_symbol": "forbidden"}]},
            "p_and_l": {"exports": [self._export(label_counts={"p_and_l": 1})]},
            "p&l": {"exports": [self._export(setup_type_counts={"p&l": 1})]},
            "trade_decision": {
                "no_trade_boundary_summary": {
                    "watch_only": True,
                    "no_trade_boundary_preserved": True,
                    "trade_decision": "forbidden",
                }
            },
        }

        for field_name, overrides in forbidden_cases.items():
            with self.subTest(field_name=field_name):
                with self.assertRaisesRegex(
                    ValueError, "Forbidden execution/trade field"
                ):
                    validate_shadow_review_export_bundle(
                        self._bundle(**overrides)
                    )

    def test_no_live_trade_approval_is_allowed(self):
        live_approval_cases = {
            "live_trade_approval": {
                "exports": [
                    self._export(
                        no_trade_boundary_summary={
                            "watch_only": True,
                            "no_trade_boundary_preserved": True,
                            "live_trade_approval": False,
                        }
                    )
                ]
            },
            "approved_trade": {"bundle_counts": {"approved_trade": 0}},
            "trade_approval": {"unavailable_fields": [{"trade_approval": "no"}]},
        }

        for field_name, overrides in live_approval_cases.items():
            with self.subTest(field_name=field_name):
                with self.assertRaisesRegex(
                    ValueError, "Forbidden execution/trade field"
                ):
                    validate_shadow_review_export_bundle(
                        self._bundle(**overrides)
                    )

    def test_watch_only_no_trade_boundary_is_preserved(self):
        invalid_boundaries = (
            {},
            {"watch_only": False, "no_trade_boundary_preserved": True},
            {"watch_only": True, "no_trade_boundary_preserved": False},
            {"watch_only": "true", "no_trade_boundary_preserved": True},
        )

        for boundary_summary in invalid_boundaries:
            with self.subTest(boundary_summary=boundary_summary):
                with self.assertRaisesRegex(ValueError, "boundary"):
                    validate_shadow_review_export_bundle(
                        self._bundle(
                            no_trade_boundary_summary=boundary_summary
                        )
                    )

    def test_deterministic_repeated_validation(self):
        bundle = self._bundle()
        original_bundle = copy.deepcopy(bundle)

        first = validate_shadow_review_export_bundle(bundle)
        second = validate_shadow_review_export_bundle(bundle)
        third = validate_shadow_review_export_bundle(copy.deepcopy(bundle))

        self.assertEqual(first, second)
        self.assertEqual(second, third)
        self.assertEqual(bundle, original_bundle)

    def test_no_files_reports_logs_or_live_calls_are_created(self):
        bundle = self._bundle()
        blocked = AssertionError("external side effect")
        original_cwd = os.getcwd()

        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                os.chdir(temp_dir)
                before = sorted(os.listdir(temp_dir))
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
                    validated = validate_shadow_review_export_bundle(bundle)
                after = sorted(os.listdir(temp_dir))
            finally:
                os.chdir(original_cwd)

        self.assertEqual(before, [])
        self.assertEqual(after, [])
        for forbidden_output in ("file", "report", "log", "alert"):
            self.assertNotIn(forbidden_output, validated)

    def test_local_validation_suite_includes_export_bundle_validator(self):
        from tests import test_watcher_foundation_local_validation_suite as suite_module

        self.assertIn(
            "tests.test_shadow_review_export_bundle_validator",
            suite_module.WATCHER_FOUNDATION_TEST_MODULES,
        )


if __name__ == "__main__":
    unittest.main()
