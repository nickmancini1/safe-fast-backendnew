import os
import tempfile
import unittest

from watcher_foundation.shadow_review import (
    run_local_shadow_review_label_workflow,
    validate_shadow_review_label,
)


class ShadowReviewSamplePackTests(unittest.TestCase):
    def _sample(
        self,
        sample_id="SYNTH-SHADOW-IDEAL-001",
        setup_type="Ideal",
        reviewer_label="valid_watch_candidate",
        **overrides,
    ):
        sample = {
            "sample_id": sample_id,
            "setup_type": setup_type,
            "stage": "local_review",
            "trigger_status": "artifact_supported_watch_candidate",
            "headline_news_status": "NEWS_UNCONFIRMED",
            "duplicate_suppression_status": "not_duplicate",
            "focus_winner_status": "not_compared",
            "diagnostics_summary": (
                "local watch-only sample uses synthetic in-memory evidence only"
            ),
            "reviewer_label": reviewer_label,
            "reviewer_notes": (
                "local watch-only review preserves unavailable evidence and "
                "does not approve live action"
            ),
            "no_trade_boundary_check": True,
        }
        sample.update(overrides)
        return sample

    def test_ideal_valid_watch_candidate_sample(self):
        sample = self._sample("SYNTH-SHADOW-IDEAL-VALID-001")

        validated = validate_shadow_review_label(sample)

        self.assertEqual(validated["setup_type"], "Ideal")
        self.assertEqual(validated["reviewer_label"], "valid_watch_candidate")
        self.assertIs(validated["no_trade_boundary_check"], True)

    def test_clean_fast_break_needs_more_evidence_sample(self):
        sample = self._sample(
            "SYNTH-SHADOW-CFB-EVIDENCE-001",
            setup_type="Clean Fast Break",
            reviewer_label="needs_more_evidence",
            trigger_status="supporting_evidence_unavailable",
            diagnostics_summary=(
                "local watch-only sample keeps missing evidence unavailable"
            ),
        )

        validated = validate_shadow_review_label(sample)

        self.assertEqual(validated["setup_type"], "Clean Fast Break")
        self.assertEqual(validated["reviewer_label"], "needs_more_evidence")
        self.assertEqual(
            validated["trigger_status"], "supporting_evidence_unavailable"
        )

    def test_continuation_stale_or_spent_sample(self):
        sample = self._sample(
            "SYNTH-SHADOW-CONTINUATION-STALE-001",
            setup_type="Continuation",
            reviewer_label="stale_or_spent",
            trigger_status="no_fresh_artifact_support",
            diagnostics_summary=(
                "local watch-only sample remains stale or spent by review"
            ),
        )

        validated = validate_shadow_review_label(sample)

        self.assertEqual(validated["setup_type"], "Continuation")
        self.assertEqual(validated["reviewer_label"], "stale_or_spent")
        self.assertEqual(validated["trigger_status"], "no_fresh_artifact_support")

    def test_duplicate_suppressed_sample(self):
        sample = self._sample(
            "SYNTH-SHADOW-DUPLICATE-001",
            reviewer_label="duplicate_suppressed",
            duplicate_suppression_status="duplicate_suppressed",
            diagnostics_summary=(
                "local watch-only sample remains suppressed in memory"
            ),
        )

        validated = validate_shadow_review_label(sample)

        self.assertEqual(
            validated["duplicate_suppression_status"], "duplicate_suppressed"
        )
        self.assertEqual(validated["reviewer_label"], "duplicate_suppressed")

    def test_winner_correct_sample(self):
        sample = self._sample(
            "SYNTH-SHADOW-WINNER-CORRECT-001",
            reviewer_label="winner_correct",
            focus_winner_status="winner_correct_by_local_artifact",
            diagnostics_summary=(
                "local watch-only sample compares only in-memory candidates"
            ),
        )

        validated = validate_shadow_review_label(sample)

        self.assertEqual(
            validated["focus_winner_status"], "winner_correct_by_local_artifact"
        )
        self.assertEqual(validated["reviewer_label"], "winner_correct")

    def test_winner_questionable_sample(self):
        sample = self._sample(
            "SYNTH-SHADOW-WINNER-QUESTIONABLE-001",
            reviewer_label="winner_questionable",
            focus_winner_status="winner_questionable_by_local_artifact",
            diagnostics_summary=(
                "local watch-only sample keeps winner comparison unresolved"
            ),
        )

        validated = validate_shadow_review_label(sample)

        self.assertEqual(
            validated["focus_winner_status"],
            "winner_questionable_by_local_artifact",
        )
        self.assertEqual(validated["reviewer_label"], "winner_questionable")

    def test_invalid_watch_candidate_sample(self):
        sample = self._sample(
            "SYNTH-SHADOW-INVALID-CANDIDATE-001",
            reviewer_label="invalid_watch_candidate",
            trigger_status="artifact_does_not_support_watch_candidate",
            diagnostics_summary=(
                "local watch-only sample remains invalid by review"
            ),
        )

        validated = validate_shadow_review_label(sample)

        self.assertEqual(validated["reviewer_label"], "invalid_watch_candidate")
        self.assertEqual(
            validated["trigger_status"],
            "artifact_does_not_support_watch_candidate",
        )

    def test_no_trade_boundary_preserved_sample(self):
        sample = self._sample(
            "SYNTH-SHADOW-BOUNDARY-001",
            reviewer_label="no_trade_boundary_preserved",
            diagnostics_summary=(
                "local watch-only sample confirms boundary preservation"
            ),
            reviewer_notes=(
                "local watch-only review confirms no approval or live action"
            ),
        )

        validated = validate_shadow_review_label(sample)

        self.assertEqual(
            validated["reviewer_label"], "no_trade_boundary_preserved"
        )
        self.assertIs(validated["no_trade_boundary_check"], True)

    def test_mixed_valid_invalid_workflow_rejects_invalid_samples_with_reasons(self):
        valid_sample = self._sample("SYNTH-SHADOW-MIXED-VALID-001")
        invalid_label_sample = self._sample(
            "SYNTH-SHADOW-MIXED-INVALID-LABEL-001",
            reviewer_label="unsupported_review_label",
        )
        invalid_boundary_sample = self._sample(
            "SYNTH-SHADOW-MIXED-INVALID-BOUNDARY-001",
            no_trade_boundary_check=False,
        )

        summary = run_local_shadow_review_label_workflow(
            [valid_sample, invalid_label_sample, invalid_boundary_sample]
        )

        self.assertEqual(summary["samples_processed"], 3)
        self.assertEqual(summary["samples_accepted"], 1)
        self.assertEqual(summary["samples_rejected"], 2)
        self.assertEqual(
            summary["rejected_samples"],
            [
                {
                    "sample_id": "SYNTH-SHADOW-MIXED-INVALID-LABEL-001",
                    "reason": (
                        "Unsupported reviewer_label: unsupported_review_label"
                    ),
                },
                {
                    "sample_id": "SYNTH-SHADOW-MIXED-INVALID-BOUNDARY-001",
                    "reason": "no_trade_boundary_check must be true",
                },
            ],
        )
        self.assertIs(summary["watch_only"], True)

    def test_sample_pack_remains_local_in_memory_and_creates_no_files(self):
        samples = [
            self._sample("SYNTH-SHADOW-LOCAL-IDEAL-001"),
            self._sample(
                "SYNTH-SHADOW-LOCAL-CFB-001",
                setup_type="Clean Fast Break",
                reviewer_label="needs_more_evidence",
            ),
            self._sample(
                "SYNTH-SHADOW-LOCAL-CONTINUATION-001",
                setup_type="Continuation",
                reviewer_label="stale_or_spent",
            ),
        ]
        original_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                os.chdir(temp_dir)
                before = sorted(os.listdir(temp_dir))

                summary = run_local_shadow_review_label_workflow(samples)

                after = sorted(os.listdir(temp_dir))
            finally:
                os.chdir(original_cwd)

        self.assertEqual(before, [])
        self.assertEqual(after, [])
        self.assertEqual(summary["samples_accepted"], 3)
        self.assertEqual(summary["samples_rejected"], 0)


if __name__ == "__main__":
    unittest.main()
