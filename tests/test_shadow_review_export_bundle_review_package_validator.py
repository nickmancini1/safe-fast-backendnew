import copy
import os
import unittest
from collections import UserDict
from unittest import mock

from watcher_foundation.shadow_review import (
    SHADOW_REVIEW_EXPORT_BUNDLE_REVIEW_PACKAGE_REQUIRED_FIELDS,
    validate_shadow_review_export_bundle_review_package,
)


class ShadowReviewExportBundleReviewPackageValidatorTests(unittest.TestCase):
    def _export(self, **overrides):
        export = {
            "export_id": "local-shadow-review-export-001",
            "created_from": "local_shadow_review_workflow_summary",
            "schema_version": 1,
            "samples": [
                {
                    "sample_id": "SYNTH-PACKAGE-IDEAL-001",
                    "setup_type": "Ideal",
                    "stage": "local_review_package_validator",
                    "trigger_status": "artifact_supported_watch_candidate",
                    "headline_news_status": "NEWS_UNCONFIRMED",
                    "duplicate_suppression_status": "not_duplicate",
                    "focus_winner_status": "not_compared",
                    "diagnostics_summary": (
                        "local watch-only review-package sample keeps "
                        "unavailable evidence explicit"
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
                    "sample_id": "SYNTH-PACKAGE-REJECTED-SAMPLE-001",
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

    def _package(self, **overrides):
        package = {
            "package_id": "local-shadow-review-export-bundle-review-package-001",
            "schema_version": 1,
            "created_from": "patch8_shadow_review_export_bundle_artifacts",
            "source_exports": [self._export()],
            "source_bundles": [self._bundle()],
            "review_summary": {
                "exports_total": 1,
                "bundles_total": 1,
                "watch_only": True,
                "no_trade_boundary_preserved": True,
            },
            "rejected_items": [
                {
                    "item_id": "local-shadow-review-rejected-item-001",
                    "reason": "shadow review export samples must be a list",
                }
            ],
            "no_trade_boundary_summary": {
                "watch_only": True,
                "no_trade_boundary_preserved": True,
                "packages_with_no_trade_boundary": 1,
            },
            "unavailable_fields": [
                "TRIGGER_LEVEL_UNCONFIRMED",
                "INVALIDATION_UNCONFIRMED",
            ],
            "reviewer_notes": (
                "local watch-only review package preserves unavailable evidence "
                "and does not approve live action"
            ),
        }
        package.update(overrides)
        return package

    def test_valid_review_package_passes(self):
        package = self._package()

        validated = validate_shadow_review_export_bundle_review_package(package)

        self.assertEqual(validated, package)
        self.assertIsNot(validated, package)
        self.assertIsNot(validated["source_exports"], package["source_exports"])
        self.assertIsNot(validated["source_exports"][0], package["source_exports"][0])
        self.assertIsNot(validated["source_bundles"], package["source_bundles"])
        self.assertIsNot(validated["source_bundles"][0], package["source_bundles"][0])

    def test_missing_required_fields_fail(self):
        for field_name in SHADOW_REVIEW_EXPORT_BUNDLE_REVIEW_PACKAGE_REQUIRED_FIELDS:
            with self.subTest(field_name=field_name):
                package = self._package()
                package.pop(field_name)

                with self.assertRaisesRegex(ValueError, field_name):
                    validate_shadow_review_export_bundle_review_package(package)

    def test_non_dict_input_fails(self):
        with self.assertRaisesRegex(TypeError, "must be a dict"):
            validate_shadow_review_export_bundle_review_package(["not", "a", "dict"])

        with self.assertRaisesRegex(TypeError, "must be a dict"):
            validate_shadow_review_export_bundle_review_package(
                UserDict(self._package())
            )

    def test_bad_required_container_types_fail(self):
        invalid_cases = {
            "source_exports": (self._export(),),
            "source_bundles": (self._bundle(),),
            "review_summary": [("watch_only", True)],
            "rejected_items": {"item_id": "SYNTH-INVALID-ITEM"},
            "no_trade_boundary_summary": [
                ("watch_only", True),
                ("no_trade_boundary_preserved", True),
            ],
        }

        for field_name, invalid_value in invalid_cases.items():
            with self.subTest(field_name=field_name):
                package = self._package(**{field_name: invalid_value})

                with self.assertRaisesRegex(TypeError, field_name):
                    validate_shadow_review_export_bundle_review_package(package)

    def test_invalid_nested_export_fails_with_useful_reason(self):
        invalid_export = self._export(samples="not-a-list")

        with self.assertRaisesRegex(
            TypeError,
            r"source_exports\[0\]: shadow review export samples must be a list",
        ):
            validate_shadow_review_export_bundle_review_package(
                self._package(source_exports=[invalid_export])
            )

    def test_invalid_nested_bundle_fails_with_useful_reason(self):
        invalid_bundle = self._bundle(exports="not-a-list")

        with self.assertRaisesRegex(
            TypeError,
            r"source_bundles\[0\]: shadow review export bundle exports must be a list",
        ):
            validate_shadow_review_export_bundle_review_package(
                self._package(source_bundles=[invalid_bundle])
            )

    def test_rejected_reasons_are_preserved(self):
        rejected_items = [
            {
                "item_id": "SYNTH-PACKAGE-INVALID-EXPORT-001",
                "reason": "shadow review export samples must be a list",
            },
            {
                "item_id": "SYNTH-PACKAGE-INVALID-BUNDLE-001",
                "reason": "shadow review export bundle exports must be a list",
            },
        ]

        validated = validate_shadow_review_export_bundle_review_package(
            self._package(rejected_items=copy.deepcopy(rejected_items))
        )

        self.assertEqual(validated["rejected_items"], rejected_items)
        self.assertIsNot(validated["rejected_items"], rejected_items)

    def test_nested_forbidden_execution_trade_fields_fail(self):
        forbidden_cases = {
            "broker": {"review_summary": {"nested": {"broker": "forbidden"}}},
            "order": {"rejected_items": [{"order_id": "forbidden"}]},
            "account": {"source_exports": [self._export(samples=[{"account": "x"}])]},
            "option": {"unavailable_fields": [{"option_symbol": "forbidden"}]},
            "p_and_l": {"source_bundles": [self._bundle(bundle_counts={"p_and_l": 0})]},
            "p&l": {"review_summary": {"nested": {"p&l": "forbidden"}}},
            "trade_decision": {
                "no_trade_boundary_summary": {
                    "watch_only": True,
                    "no_trade_boundary_preserved": True,
                    "trade_decision": "forbidden",
                }
            },
            "execution": {"reviewer_notes": {"execution": "forbidden"}},
        }

        for field_name, overrides in forbidden_cases.items():
            with self.subTest(field_name=field_name):
                with self.assertRaisesRegex(
                    ValueError, "Forbidden execution/trade field"
                ):
                    validate_shadow_review_export_bundle_review_package(
                        self._package(**overrides)
                    )

    def test_no_live_trade_approval_is_allowed(self):
        live_approval_cases = {
            "live_trade_approval": {"review_summary": {"live_trade_approval": False}},
            "approved_trade": {"rejected_items": [{"approved_trade": False}]},
            "trade_approval": {"unavailable_fields": [{"trade_approval": "no"}]},
        }

        for field_name, overrides in live_approval_cases.items():
            with self.subTest(field_name=field_name):
                with self.assertRaisesRegex(
                    ValueError, "Forbidden execution/trade field"
                ):
                    validate_shadow_review_export_bundle_review_package(
                        self._package(**overrides)
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
                    validate_shadow_review_export_bundle_review_package(
                        self._package(
                            no_trade_boundary_summary=boundary_summary
                        )
                    )

    def test_deterministic_repeated_validation(self):
        package = self._package()
        original_package = copy.deepcopy(package)

        first = validate_shadow_review_export_bundle_review_package(package)
        second = validate_shadow_review_export_bundle_review_package(package)
        third = validate_shadow_review_export_bundle_review_package(
            copy.deepcopy(package)
        )

        self.assertEqual(first, second)
        self.assertEqual(second, third)
        self.assertEqual(package, original_package)

    def test_no_files_reports_logs_or_live_calls_are_created(self):
        package = self._package()
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
            validated = validate_shadow_review_export_bundle_review_package(package)
        after = sorted(os.listdir(os.getcwd()))

        self.assertEqual(before, after)
        for forbidden_output in ("file", "report", "log", "alert"):
            self.assertNotIn(forbidden_output, validated)

    def test_local_validation_suite_includes_review_package_validator(self):
        from tests import test_watcher_foundation_local_validation_suite as suite_module

        self.assertIn(
            "tests.test_shadow_review_export_bundle_review_package_validator",
            suite_module.WATCHER_FOUNDATION_TEST_MODULES,
        )


if __name__ == "__main__":
    unittest.main()
