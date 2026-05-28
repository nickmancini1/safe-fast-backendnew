import copy
import os
import unittest
from unittest import mock

from watcher_foundation.shadow_review import (
    SHADOW_REVIEW_EXPORT_BUNDLE_REVIEW_PACKAGE_REQUIRED_FIELDS,
    validate_shadow_review_export_bundle_review_package,
)


class ShadowReviewExportBundleReviewPackageFinalBoundarySweepTests(
    unittest.TestCase
):
    def _export(self, **overrides):
        export = {
            "export_id": "local-shadow-review-package-final-export-001",
            "created_from": "local_shadow_review_workflow_summary",
            "schema_version": 1,
            "samples": [
                {
                    "sample_id": "SYNTH-PACKAGE-FINAL-IDEAL-001",
                    "setup_type": "Ideal",
                    "stage": "local_review_package_final_boundary_sweep",
                    "trigger_status": "artifact_supported_watch_candidate",
                    "headline_news_status": "NEWS_UNCONFIRMED",
                    "duplicate_suppression_status": "not_duplicate",
                    "focus_winner_status": "not_compared",
                    "diagnostics_summary": (
                        "local watch-only review-package export sample keeps "
                        "unavailable evidence explicit"
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
                    "sample_id": "SYNTH-PACKAGE-FINAL-REJECTED-SAMPLE-001",
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

    def _bundle(self, **overrides):
        bundle = {
            "bundle_id": "local-shadow-review-package-final-bundle-001",
            "schema_version": 1,
            "created_from": "local_shadow_review_exports",
            "exports": [self._export()],
            "bundle_counts": {
                "exports_total": 1,
                "exports_validated": 1,
                "rejected_exports": 2,
            },
            "rejected_exports": [
                {
                    "export_id": "SYNTH-PACKAGE-FINAL-INVALID-EXPORT-001",
                    "reason": "shadow review export samples must be a list",
                },
                {
                    "export_id": "SYNTH-PACKAGE-FINAL-INVALID-EXPORT-002",
                    "reason": (
                        "shadow review export must preserve no-trade boundary"
                    ),
                },
            ],
            "no_trade_boundary_summary": {
                "watch_only": True,
                "no_trade_boundary_preserved": True,
                "exports_with_no_trade_boundary": 1,
                "live_trade_decision_status": "not_created",
            },
            "reviewer_notes": (
                "local watch-only bundle is for review only and preserves "
                "unavailable evidence"
            ),
            "unavailable_fields": {
                "trigger_level": "UNCONFIRMED",
                "invalidation_level": "UNCONFIRMED",
                "option_p_and_l": "NOT_CREATED",
            },
        }
        bundle.update(overrides)
        return bundle

    def _package(self, **overrides):
        package = {
            "package_id": "local-shadow-review-package-final-boundary-001",
            "schema_version": 1,
            "created_from": "patch8_shadow_review_export_bundle_artifacts",
            "source_exports": [self._export()],
            "source_bundles": [self._bundle()],
            "review_summary": {
                "exports_total": 1,
                "bundles_total": 1,
                "watch_only": True,
                "no_trade_boundary_preserved": True,
                "live_trade_decision_status": "not_created",
            },
            "rejected_items": [
                {
                    "item_id": "SYNTH-PACKAGE-FINAL-INVALID-EXPORT-001",
                    "reason": "shadow review export samples must be a list",
                },
                {
                    "item_id": "SYNTH-PACKAGE-FINAL-INVALID-BUNDLE-001",
                    "reason": (
                        "shadow review export bundle exports must be a list"
                    ),
                },
            ],
            "no_trade_boundary_summary": {
                "watch_only": True,
                "no_trade_boundary_preserved": True,
                "packages_with_no_trade_boundary": 1,
                "live_trade_decision_status": "not_created",
            },
            "unavailable_fields": {
                "trigger_level": "UNCONFIRMED",
                "invalidation_level": "UNCONFIRMED",
                "headline_news_context": "NEWS_UNCONFIRMED",
            },
            "reviewer_notes": (
                "local watch-only review package is for review only and "
                "preserves unavailable evidence"
            ),
        }
        package.update(overrides)
        return package

    def test_accepts_valid_in_memory_review_package_dicts(self):
        package = self._package()

        validated = validate_shadow_review_export_bundle_review_package(package)

        self.assertEqual(validated, package)
        self.assertIsNot(validated, package)
        self.assertIsNot(validated["source_exports"], package["source_exports"])
        self.assertIsNot(validated["source_exports"][0], package["source_exports"][0])
        self.assertIsNot(validated["source_bundles"], package["source_bundles"])
        self.assertIsNot(validated["source_bundles"][0], package["source_bundles"][0])
        self.assertIsNot(
            validated["no_trade_boundary_summary"],
            package["no_trade_boundary_summary"],
        )

    def test_rejects_invalid_review_packages_with_useful_reasons(self):
        invalid_packages = (
            (
                ["not", "a", "package"],
                TypeError,
                "shadow review export bundle review package must be a dict",
            ),
            (
                self._package(source_exports="not-a-list"),
                TypeError,
                "shadow review export bundle review package source_exports "
                "must be a list",
            ),
            (
                self._package(no_trade_boundary_summary={"watch_only": True}),
                ValueError,
                "shadow review export must preserve no-trade boundary",
            ),
            (
                self._package(review_summary={"nested": {"broker": "forbidden"}}),
                ValueError,
                "Forbidden execution/trade field: review_summary.nested.broker",
            ),
        )

        for package, error_type, reason in invalid_packages:
            with self.subTest(reason=reason):
                with self.assertRaisesRegex(error_type, reason):
                    validate_shadow_review_export_bundle_review_package(package)

    def test_missing_required_package_fields_fail(self):
        for field_name in SHADOW_REVIEW_EXPORT_BUNDLE_REVIEW_PACKAGE_REQUIRED_FIELDS:
            with self.subTest(field_name=field_name):
                package = self._package()
                package.pop(field_name)

                with self.assertRaisesRegex(ValueError, field_name):
                    validate_shadow_review_export_bundle_review_package(package)

    def test_bad_package_field_types_fail(self):
        invalid_type_cases = {
            "package_id": 1001,
            "created_from": ("exports", "bundles"),
            "schema_version": "1",
            "source_exports": {"export_id": "SYNTH-INVALID"},
            "source_bundles": {"bundle_id": "SYNTH-INVALID"},
            "review_summary": [("watch_only", True)],
            "rejected_items": {"item_id": "SYNTH-INVALID"},
            "no_trade_boundary_summary": [("watch_only", True)],
            "reviewer_notes": ["local watch-only"],
            "unavailable_fields": "trigger_level",
        }

        for field_name, invalid_value in invalid_type_cases.items():
            with self.subTest(field_name=field_name):
                with self.assertRaisesRegex(TypeError, field_name):
                    validate_shadow_review_export_bundle_review_package(
                        self._package(**{field_name: invalid_value})
                    )

    def test_invalid_nested_exports_fail_with_source_index(self):
        invalid_exports = (
            (
                self._export(samples="not-a-list"),
                TypeError,
                r"source_exports\[0\]: shadow review export samples must be a list",
            ),
            (
                self._export(no_trade_boundary_summary={"watch_only": True}),
                ValueError,
                r"source_exports\[0\]: shadow review export must preserve "
                "no-trade boundary",
            ),
            (
                self._export(samples=[{"nested": {"order": "forbidden"}}]),
                ValueError,
                r"Forbidden execution/trade field: "
                r"source_exports.0.samples.0.nested.order",
            ),
        )

        for invalid_export, error_type, reason in invalid_exports:
            with self.subTest(reason=reason):
                with self.assertRaisesRegex(error_type, reason):
                    validate_shadow_review_export_bundle_review_package(
                        self._package(source_exports=[invalid_export])
                    )

    def test_invalid_nested_bundles_fail_with_source_index(self):
        invalid_bundles = (
            (
                self._bundle(exports="not-a-list"),
                TypeError,
                r"source_bundles\[0\]: shadow review export bundle exports "
                "must be a list",
            ),
            (
                self._bundle(no_trade_boundary_summary={"watch_only": True}),
                ValueError,
                r"source_bundles\[0\]: shadow review export must preserve "
                "no-trade boundary",
            ),
            (
                self._bundle(exports=[self._export(samples=[{"account": "x"}])]),
                ValueError,
                r"Forbidden execution/trade field: "
                r"source_bundles.0.exports.0.samples.0.account",
            ),
        )

        for invalid_bundle, error_type, reason in invalid_bundles:
            with self.subTest(reason=reason):
                with self.assertRaisesRegex(error_type, reason):
                    validate_shadow_review_export_bundle_review_package(
                        self._package(source_bundles=[invalid_bundle])
                    )

    def test_rejected_item_reasons_are_preserved(self):
        rejected_items = [
            {
                "item_id": "SYNTH-PACKAGE-FINAL-INVALID-EXPORT-001",
                "reason": "shadow review export samples must be a list",
            },
            {
                "item_id": "SYNTH-PACKAGE-FINAL-INVALID-BUNDLE-001",
                "reason": "shadow review export bundle exports must be a list",
            },
            {
                "item_id": "UNAVAILABLE",
                "reason": "shadow review export bundle review package must be a dict",
            },
        ]

        validated = validate_shadow_review_export_bundle_review_package(
            self._package(rejected_items=copy.deepcopy(rejected_items))
        )

        self.assertEqual(validated["rejected_items"], rejected_items)
        self.assertIsNot(validated["rejected_items"], rejected_items)

    def test_nested_broker_order_account_option_pnl_and_trade_decision_fields_fail(
        self,
    ):
        forbidden_cases = {
            "broker": {"source_exports": [self._export(samples=[{"broker": "x"}])]},
            "order": {"source_bundles": [self._bundle(bundle_counts={"order": 0})]},
            "account": {"rejected_items": [{"details": {"account": "x"}}]},
            "option": {"source_exports": [self._export(unavailable_fields={"option": "x"})]},
            "option_symbol": {"unavailable_fields": [{"option_symbol": "x"}]},
            "p_and_l": {"review_summary": {"nested": {"p_and_l": "x"}}},
            "p&l": {"source_bundles": [self._bundle(bundle_counts={"p&l": 0})]},
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
                    validate_shadow_review_export_bundle_review_package(
                        self._package(**overrides)
                    )

    def test_no_live_trade_approval_is_allowed(self):
        live_approval_cases = {
            "live_trade_approval": {
                "review_summary": {"live_trade_approval": False}
            },
            "approved_trade": {"source_exports": [self._export(label_counts={"approved_trade": 0})]},
            "approved_trades": {"rejected_items": [{"approved_trades": []}]},
            "trade_approval": {"unavailable_fields": [{"trade_approval": "no"}]},
            "trade_decisions": {
                "source_bundles": [
                    self._bundle(reviewer_notes={"trade_decisions": []})
                ]
            },
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
        valid_boundary = {
            "watch_only": True,
            "no_trade_boundary_preserved": True,
            "packages_with_no_trade_boundary": 1,
        }
        invalid_boundaries = (
            {},
            {"watch_only": False, "no_trade_boundary_preserved": True},
            {"watch_only": True, "no_trade_boundary_preserved": False},
            {"watch_only": "true", "no_trade_boundary_preserved": True},
        )

        validated = validate_shadow_review_export_bundle_review_package(
            self._package(no_trade_boundary_summary=valid_boundary)
        )
        self.assertEqual(validated["no_trade_boundary_summary"], valid_boundary)

        for boundary_summary in invalid_boundaries:
            with self.subTest(boundary_summary=boundary_summary):
                with self.assertRaisesRegex(ValueError, "boundary"):
                    validate_shadow_review_export_bundle_review_package(
                        self._package(no_trade_boundary_summary=boundary_summary)
                    )

    def test_validation_is_deterministic_on_repeated_runs(self):
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

    def test_validation_creates_no_files_reports_logs_or_external_calls(self):
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

    def test_final_boundary_sweep_is_included_in_local_validation_suite(self):
        from tests import test_watcher_foundation_local_validation_suite as suite_module

        self.assertIn(
            "tests.test_shadow_review_export_bundle_review_package_final_boundary_sweep",
            suite_module.WATCHER_FOUNDATION_TEST_MODULES,
        )


if __name__ == "__main__":
    unittest.main()
