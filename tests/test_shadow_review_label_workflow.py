import os
import unittest

from watcher_foundation.shadow_review import (
    ALLOWED_SHADOW_REVIEW_LABELS,
    SHADOW_REVIEW_WORKFLOW_SUMMARY_FIELDS,
    run_local_shadow_review_label_workflow,
)


class ShadowReviewLabelWorkflowTests(unittest.TestCase):
    def _sample(
        self,
        sample_id="LOCAL-ideal-review-001",
        setup_type="Ideal",
        reviewer_label="valid_watch_candidate",
        **overrides,
    ):
        sample = {
            "sample_id": sample_id,
            "setup_type": setup_type,
            "stage": "near-trigger",
            "trigger_status": "near_trigger",
            "headline_news_status": "NEWS_UNCONFIRMED",
            "duplicate_suppression_status": "not_duplicate",
            "focus_winner_status": "winner_review_only",
            "diagnostics_summary": (
                "local watch-only diagnostics preserve unavailable evidence"
            ),
            "reviewer_label": reviewer_label,
            "reviewer_notes": (
                "local-only watch-only review; no live trade decision"
            ),
            "no_trade_boundary_check": True,
        }
        sample.update(overrides)
        return sample

    def test_valid_multi_sample_workflow_passes(self):
        samples = [
            self._sample("LOCAL-ideal-review-001", "Ideal"),
            self._sample(
                "LOCAL-clean-fast-break-review-001",
                "Clean Fast Break",
                "winner_correct",
            ),
            self._sample(
                "LOCAL-continuation-review-001",
                "Continuation",
                "needs_more_evidence",
            ),
        ]

        summary = run_local_shadow_review_label_workflow(samples)

        self.assertEqual(
            tuple(summary.keys()), SHADOW_REVIEW_WORKFLOW_SUMMARY_FIELDS
        )
        self.assertEqual(summary["samples_processed"], 3)
        self.assertEqual(summary["samples_accepted"], 3)
        self.assertEqual(summary["samples_rejected"], 0)
        self.assertEqual(summary["rejected_samples"], [])
        self.assertIs(summary["watch_only"], True)

    def test_invalid_sample_is_rejected_with_useful_reason(self):
        samples = [
            self._sample("LOCAL-valid-review-001"),
            self._sample(
                "LOCAL-invalid-review-001",
                reviewer_label="approve_live_trade",
            ),
        ]

        summary = run_local_shadow_review_label_workflow(samples)

        self.assertEqual(summary["samples_processed"], 2)
        self.assertEqual(summary["samples_accepted"], 1)
        self.assertEqual(summary["samples_rejected"], 1)
        self.assertEqual(
            summary["rejected_samples"],
            [
                {
                    "sample_id": "LOCAL-invalid-review-001",
                    "reason": "Unsupported reviewer_label: approve_live_trade",
                }
            ],
        )

    def test_label_counts_are_correct(self):
        samples = [
            self._sample("LOCAL-valid-review-001", reviewer_label="winner_correct"),
            self._sample(
                "LOCAL-valid-review-002",
                reviewer_label="winner_correct",
            ),
            self._sample(
                "LOCAL-valid-review-003",
                reviewer_label="duplicate_suppressed",
            ),
            self._sample(
                "LOCAL-invalid-review-001",
                reviewer_label="not_an_allowed_label",
            ),
        ]

        summary = run_local_shadow_review_label_workflow(samples)

        self.assertEqual(summary["label_counts"]["winner_correct"], 2)
        self.assertEqual(summary["label_counts"]["duplicate_suppressed"], 1)
        self.assertEqual(summary["label_counts"]["valid_watch_candidate"], 0)
        self.assertEqual(sum(summary["label_counts"].values()), 3)

    def test_setup_type_counts_are_correct(self):
        samples = [
            self._sample("LOCAL-ideal-review-001", "Ideal"),
            self._sample("LOCAL-ideal-review-002", "Ideal"),
            self._sample(
                "LOCAL-clean-fast-break-review-001", "Clean Fast Break"
            ),
            self._sample("LOCAL-continuation-review-001", "Continuation"),
            self._sample(
                "LOCAL-invalid-review-001",
                "Continuation",
                no_trade_boundary_check=False,
            ),
        ]

        summary = run_local_shadow_review_label_workflow(samples)

        self.assertEqual(
            summary["setup_type_counts"],
            {
                "Ideal": 2,
                "Clean Fast Break": 1,
                "Continuation": 1,
            },
        )

    def test_all_allowed_labels_can_be_counted(self):
        samples = [
            self._sample(f"LOCAL-{label}-review-001", reviewer_label=label)
            for label in ALLOWED_SHADOW_REVIEW_LABELS
        ]

        summary = run_local_shadow_review_label_workflow(samples)

        self.assertEqual(
            summary["label_counts"],
            {label: 1 for label in ALLOWED_SHADOW_REVIEW_LABELS},
        )
        self.assertEqual(summary["samples_accepted"], len(ALLOWED_SHADOW_REVIEW_LABELS))

    def test_ideal_clean_fast_break_continuation_samples_are_accepted(self):
        samples = [
            self._sample("LOCAL-ideal-review-001", "Ideal"),
            self._sample(
                "LOCAL-clean-fast-break-review-001", "Clean Fast Break"
            ),
            self._sample("LOCAL-continuation-review-001", "Continuation"),
        ]

        summary = run_local_shadow_review_label_workflow(samples)

        self.assertEqual(summary["samples_accepted"], 3)
        self.assertEqual(summary["samples_rejected"], 0)
        self.assertEqual(
            summary["setup_type_counts"],
            {"Ideal": 1, "Clean Fast Break": 1, "Continuation": 1},
        )

    def test_no_trade_boundary_preserved_count_is_correct(self):
        samples = [
            self._sample("LOCAL-valid-review-001"),
            self._sample("LOCAL-valid-review-002"),
            self._sample(
                "LOCAL-invalid-review-001",
                no_trade_boundary_check=False,
            ),
        ]

        summary = run_local_shadow_review_label_workflow(samples)

        self.assertEqual(summary["samples_accepted"], 2)
        self.assertEqual(summary["samples_rejected"], 1)
        self.assertEqual(summary["no_trade_boundary_preserved_count"], 2)

    def test_forbidden_nested_execution_fields_are_rejected(self):
        forbidden_fields = (
            "broker",
            "order",
            "account",
            "option",
            "pnl",
            "trade",
        )
        for field_name in forbidden_fields:
            with self.subTest(field_name=field_name):
                sample = self._sample(
                    f"LOCAL-forbidden-{field_name}-review-001",
                    extra={"nested": {field_name: "forbidden"}},
                )

                summary = run_local_shadow_review_label_workflow([sample])

                self.assertEqual(summary["samples_accepted"], 0)
                self.assertEqual(summary["samples_rejected"], 1)
                self.assertEqual(
                    summary["rejected_samples"][0]["sample_id"],
                    f"LOCAL-forbidden-{field_name}-review-001",
                )
                self.assertIn(
                    "Forbidden execution/trade field",
                    summary["rejected_samples"][0]["reason"],
                )

    def test_workflow_is_deterministic_on_repeated_runs(self):
        samples = [
            self._sample("LOCAL-ideal-review-001", "Ideal"),
            self._sample(
                "LOCAL-invalid-review-001",
                reviewer_label="not_an_allowed_label",
            ),
        ]

        first_summary = run_local_shadow_review_label_workflow(samples)
        second_summary = run_local_shadow_review_label_workflow(samples)

        self.assertEqual(first_summary, second_summary)

    def test_no_files_reports_logs_or_live_calls_are_created(self):
        samples = [self._sample("LOCAL-valid-review-001")]
        before = sorted(os.listdir(os.getcwd()))

        run_local_shadow_review_label_workflow(samples)

        after = sorted(os.listdir(os.getcwd()))

        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
