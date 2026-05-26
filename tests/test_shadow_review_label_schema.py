import os
import tempfile
import unittest
from collections import UserDict

from watcher_foundation.shadow_review import (
    ALLOWED_SHADOW_REVIEW_LABELS,
    REQUIRED_SHADOW_REVIEW_FIELDS,
    validate_shadow_review_label,
)


class ShadowReviewLabelSchemaTests(unittest.TestCase):
    def _sample(self, setup_type="Ideal", **overrides):
        sample = {
            "sample_id": f"LOCAL-{setup_type.lower().replace(' ', '-')}-review-001",
            "setup_type": setup_type,
            "stage": "near-trigger",
            "trigger_status": "near_trigger",
            "headline_news_status": "NEWS_UNCONFIRMED",
            "duplicate_suppression_status": "not_duplicate",
            "focus_winner_status": "winner_review_only",
            "diagnostics_summary": (
                "local watch-only diagnostics preserve unavailable evidence"
            ),
            "reviewer_label": "valid_watch_candidate",
            "reviewer_notes": (
                "local-only watch-only review; no live trade decision"
            ),
            "no_trade_boundary_check": True,
        }
        sample.update(overrides)
        return sample

    def test_valid_sample_passes(self):
        sample = self._sample()

        validated = validate_shadow_review_label(sample)

        self.assertEqual(validated, sample)
        self.assertIsNot(validated, sample)

    def test_non_dict_input_fails(self):
        with self.assertRaisesRegex(TypeError, "must be a dict"):
            validate_shadow_review_label(["not", "a", "dict"])

        with self.assertRaisesRegex(TypeError, "must be a dict"):
            validate_shadow_review_label(UserDict(self._sample()))

    def test_missing_required_fields_fail(self):
        for field_name in REQUIRED_SHADOW_REVIEW_FIELDS:
            with self.subTest(field_name=field_name):
                sample = self._sample()
                sample.pop(field_name)

                with self.assertRaisesRegex(ValueError, field_name):
                    validate_shadow_review_label(sample)

    def test_unknown_label_fails(self):
        with self.assertRaisesRegex(ValueError, "Unsupported reviewer_label"):
            validate_shadow_review_label(
                self._sample(reviewer_label="approve_trade")
            )

    def test_no_trade_boundary_check_false_fails(self):
        with self.assertRaisesRegex(ValueError, "no_trade_boundary_check"):
            validate_shadow_review_label(
                self._sample(no_trade_boundary_check=False)
            )

    def test_nested_forbidden_execution_trade_fields_fail(self):
        forbidden_samples = (
            self._sample(extra={"nested": [{"broker": "forbidden"}]}),
            self._sample(extra={"nested": {"order_id": "forbidden"}}),
            self._sample(extra={"nested": {"account": "forbidden"}}),
            self._sample(extra={"nested": {"option_pnl": "forbidden"}}),
            self._sample(extra={"nested": {"trade_decision": "forbidden"}}),
            self._sample(extra={"nested": {"live_trade_approval": False}}),
        )

        for sample in forbidden_samples:
            with self.subTest(sample=sample):
                with self.assertRaisesRegex(
                    ValueError, "Forbidden execution/trade field"
                ):
                    validate_shadow_review_label(sample)

    def test_all_allowed_labels_are_accepted(self):
        for label in ALLOWED_SHADOW_REVIEW_LABELS:
            with self.subTest(label=label):
                validated = validate_shadow_review_label(
                    self._sample(reviewer_label=label)
                )

                self.assertEqual(validated["reviewer_label"], label)

    def test_ideal_clean_fast_break_continuation_samples_are_accepted(self):
        for setup_type in ("Ideal", "Clean Fast Break", "Continuation"):
            with self.subTest(setup_type=setup_type):
                validated = validate_shadow_review_label(self._sample(setup_type))

                self.assertEqual(validated["setup_type"], setup_type)

    def test_local_watch_only_wording_is_required_and_preserved(self):
        sample = self._sample(
            diagnostics_summary="local watch-only diagnostics unchanged",
            reviewer_notes="local-only watch-only note unchanged",
        )

        validated = validate_shadow_review_label(sample)

        self.assertEqual(
            validated["diagnostics_summary"],
            "local watch-only diagnostics unchanged",
        )
        self.assertEqual(
            validated["reviewer_notes"],
            "local-only watch-only note unchanged",
        )

        with self.assertRaisesRegex(ValueError, "local and watch-only"):
            validate_shadow_review_label(
                self._sample(
                    diagnostics_summary="diagnostics without boundary wording",
                    reviewer_notes="review note without boundary wording",
                )
            )

    def test_no_files_reports_logs_or_live_calls_are_created(self):
        sample = self._sample()
        original_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                os.chdir(temp_dir)
                before = sorted(os.listdir(temp_dir))

                validate_shadow_review_label(sample)

                after = sorted(os.listdir(temp_dir))
            finally:
                os.chdir(original_cwd)

        self.assertEqual(before, [])
        self.assertEqual(after, [])


if __name__ == "__main__":
    unittest.main()
