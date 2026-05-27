import copy
import os
import unittest
from unittest import mock

from watcher_foundation.shadow_review import (
    SHADOW_REVIEW_EXPORT_BUNDLE_REQUIRED_FIELDS,
    validate_shadow_review_export_bundle,
)


class ShadowReviewExportBundleFinalBoundarySweepTests(unittest.TestCase):
    def _export(self, **overrides):
        export = {
            "export_id": "local-shadow-review-export-final-boundary-001",
            "created_from": "local_shadow_review_workflow_summary",
            "schema_version": 1,
            "samples": [
                {
                    "sample_id": "SYNTH-BUNDLE-FINAL-IDEAL-001",
                    "setup_type": "Ideal",
                    "stage": "local_export_bundle_final_boundary_sweep",
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
            "label_counts": {
                "valid_watch_candidate": 1,
                "needs_more_evidence": 0,
            },
            "setup_type_counts": {"Ideal": 1},
            "rejected_samples": [
                {
                    "sample_id": "SYNTH-BUNDLE-FINAL-REJECTED-SAMPLE-001",
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
            "bundle_id": "local-shadow-review-export-bundle-final-boundary-001",
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
                    "export_id": "SYNTH-BUNDLE-FINAL-INVALID-EXPORT-001",
                    "reason": "shadow review export samples must be a list",
                },
                {
                    "export_id": "SYNTH-BUNDLE-FINAL-INVALID-EXPORT-002",
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

    def test_accepts_valid_in_memory_export_bundle_dicts(self):
        bundle = self._bundle()

        validated = validate_shadow_review_export_bundle(bundle)

        self.assertEqual(validated, bundle)
        self.assertIsNot(validated, bundle)
        self.assertIsNot(validated["exports"], bundle["exports"])
        self.assertIsNot(validated["exports"][0], bundle["exports"][0])
        self.assertIsNot(
            validated["no_trade_boundary_summary"],
            bundle["no_trade_boundary_summary"],
        )

    def test_rejects_invalid_export_bundles_with_useful_reasons(self):
        invalid_bundles = (
            (
                ["not", "a", "bundle"],
                TypeError,
                "shadow review export bundle must be a dict",
            ),
            (
                self._bundle(exports="not-a-list"),
                TypeError,
                "shadow review export bundle exports must be a list",
            ),
            (
                self._bundle(no_trade_boundary_summary={"watch_only": True}),
                ValueError,
                "shadow review export must preserve no-trade boundary",
            ),
            (
                self._bundle(bundle_counts={"nested": {"broker": "forbidden"}}),
                ValueError,
                "Forbidden execution/trade field: bundle_counts.nested.broker",
            ),
        )

        for bundle, error_type, reason in invalid_bundles:
            with self.subTest(reason=reason):
                with self.assertRaisesRegex(error_type, reason):
                    validate_shadow_review_export_bundle(bundle)

    def test_missing_required_bundle_fields_fail(self):
        for field_name in SHADOW_REVIEW_EXPORT_BUNDLE_REQUIRED_FIELDS:
            with self.subTest(field_name=field_name):
                bundle = self._bundle()
                bundle.pop(field_name)

                with self.assertRaisesRegex(ValueError, field_name):
                    validate_shadow_review_export_bundle(bundle)

    def test_bad_bundle_field_types_fail(self):
        invalid_type_cases = {
            "bundle_id": 1001,
            "created_from": ("exports",),
            "schema_version": "1",
            "exports": {"export_id": "SYNTH-INVALID"},
            "bundle_counts": [("exports_total", 1)],
            "rejected_exports": {"export_id": "SYNTH-INVALID"},
            "no_trade_boundary_summary": [("watch_only", True)],
            "reviewer_notes": ["local watch-only"],
            "unavailable_fields": "trigger_level",
        }

        for field_name, invalid_value in invalid_type_cases.items():
            with self.subTest(field_name=field_name):
                with self.assertRaisesRegex(TypeError, field_name):
                    validate_shadow_review_export_bundle(
                        self._bundle(**{field_name: invalid_value})
                    )

    def test_invalid_nested_exports_fail(self):
        invalid_exports = (
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
                self._export(samples=[{"nested": {"order": "forbidden"}}]),
                ValueError,
                "Forbidden execution/trade field: exports.0.samples.0.nested.order",
            ),
        )

        for invalid_export, error_type, reason in invalid_exports:
            with self.subTest(reason=reason):
                with self.assertRaisesRegex(error_type, reason):
                    validate_shadow_review_export_bundle(
                        self._bundle(exports=[invalid_export])
                    )

    def test_rejected_export_reasons_are_preserved(self):
        rejected_exports = [
            {
                "export_id": "SYNTH-BUNDLE-FINAL-INVALID-EXPORT-001",
                "reason": "shadow review export samples must be a list",
            },
            {
                "export_id": "SYNTH-BUNDLE-FINAL-INVALID-EXPORT-002",
                "reason": "shadow review export must preserve watch_only boundary",
            },
            {
                "export_id": "UNAVAILABLE",
                "reason": "shadow review export must be a dict",
            },
        ]

        validated = validate_shadow_review_export_bundle(
            self._bundle(rejected_exports=copy.deepcopy(rejected_exports))
        )

        self.assertEqual(validated["rejected_exports"], rejected_exports)
        self.assertIsNot(validated["rejected_exports"], rejected_exports)

    def test_nested_broker_order_account_option_pnl_and_trade_decision_fields_fail(self):
        forbidden_cases = {
            "broker": {"exports": [self._export(samples=[{"broker": "forbidden"}])]},
            "order": {"bundle_counts": {"nested": {"order_id": "forbidden"}}},
            "account": {"rejected_exports": [{"details": {"account": "forbidden"}}]},
            "option": {"exports": [self._export(unavailable_fields={"option": "x"})]},
            "option_symbol": {"unavailable_fields": [{"option_symbol": "forbidden"}]},
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
                    validate_shadow_review_export_bundle(self._bundle(**overrides))

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
            "approved_trades": {"rejected_exports": [{"approved_trades": []}]},
            "trade_approval": {"unavailable_fields": [{"trade_approval": "no"}]},
            "trade_decisions": {"exports": [self._export(reviewer_notes={"trade_decisions": []})]},
        }

        for field_name, overrides in live_approval_cases.items():
            with self.subTest(field_name=field_name):
                with self.assertRaisesRegex(
                    ValueError, "Forbidden execution/trade field"
                ):
                    validate_shadow_review_export_bundle(self._bundle(**overrides))

    def test_watch_only_no_trade_boundary_is_preserved(self):
        valid_boundary = {
            "watch_only": True,
            "no_trade_boundary_preserved": True,
            "exports_with_no_trade_boundary": 1,
        }
        invalid_boundaries = (
            {},
            {"watch_only": False, "no_trade_boundary_preserved": True},
            {"watch_only": True, "no_trade_boundary_preserved": False},
            {"watch_only": "true", "no_trade_boundary_preserved": True},
        )

        validated = validate_shadow_review_export_bundle(
            self._bundle(no_trade_boundary_summary=valid_boundary)
        )
        self.assertEqual(validated["no_trade_boundary_summary"], valid_boundary)

        for boundary_summary in invalid_boundaries:
            with self.subTest(boundary_summary=boundary_summary):
                with self.assertRaisesRegex(ValueError, "boundary"):
                    validate_shadow_review_export_bundle(
                        self._bundle(no_trade_boundary_summary=boundary_summary)
                    )

    def test_validation_is_deterministic_on_repeated_runs(self):
        bundle = self._bundle()
        original_bundle = copy.deepcopy(bundle)

        first = validate_shadow_review_export_bundle(bundle)
        second = validate_shadow_review_export_bundle(bundle)
        third = validate_shadow_review_export_bundle(copy.deepcopy(bundle))

        self.assertEqual(first, second)
        self.assertEqual(second, third)
        self.assertEqual(bundle, original_bundle)

    def test_validation_creates_no_files_reports_logs_or_external_calls(self):
        bundle = self._bundle()
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
            validated = validate_shadow_review_export_bundle(bundle)
        after = sorted(os.listdir(os.getcwd()))

        self.assertEqual(before, after)
        for forbidden_output in ("file", "report", "log", "alert"):
            self.assertNotIn(forbidden_output, validated)

    def test_final_boundary_sweep_is_included_in_local_validation_suite(self):
        from tests import test_watcher_foundation_local_validation_suite as suite_module

        self.assertIn(
            "tests.test_shadow_review_export_bundle_final_boundary_sweep",
            suite_module.WATCHER_FOUNDATION_TEST_MODULES,
        )


if __name__ == "__main__":
    unittest.main()
