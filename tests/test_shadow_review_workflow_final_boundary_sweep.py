import copy
import os
import tempfile
import unittest
from unittest import mock

from watcher_foundation.shadow_review import (
    ALLOWED_SHADOW_REVIEW_LABELS,
    SHADOW_REVIEW_WORKFLOW_SUMMARY_FIELDS,
    run_local_shadow_review_label_workflow,
)


class ShadowReviewWorkflowFinalBoundarySweepTests(unittest.TestCase):
    def _sample(
        self,
        sample_id="SYNTH-BOUNDARY-IDEAL-001",
        setup_type="Ideal",
        reviewer_label="valid_watch_candidate",
        **overrides,
    ):
        sample = {
            "sample_id": sample_id,
            "setup_type": setup_type,
            "stage": "local_final_boundary_sweep",
            "trigger_status": "artifact_supported_watch_candidate",
            "headline_news_status": "NEWS_UNCONFIRMED",
            "duplicate_suppression_status": "not_duplicate",
            "focus_winner_status": "not_compared",
            "diagnostics_summary": (
                "local watch-only synthetic sample uses in-memory evidence only"
            ),
            "reviewer_label": reviewer_label,
            "reviewer_notes": (
                "local watch-only review preserves no-trade boundary wording "
                "and does not approve live action"
            ),
            "no_trade_boundary_check": True,
        }
        sample.update(overrides)
        return sample

    def test_workflow_accepts_valid_in_memory_samples_only(self):
        samples = [
            self._sample("SYNTH-BOUNDARY-IDEAL-VALID-001", "Ideal"),
            self._sample(
                "SYNTH-BOUNDARY-CFB-VALID-001",
                "Clean Fast Break",
                "needs_more_evidence",
            ),
            self._sample(
                "SYNTH-BOUNDARY-CONTINUATION-VALID-001",
                "Continuation",
                "stale_or_spent",
            ),
        ]

        summary = run_local_shadow_review_label_workflow(samples)

        self.assertEqual(tuple(summary.keys()), SHADOW_REVIEW_WORKFLOW_SUMMARY_FIELDS)
        self.assertEqual(summary["samples_processed"], 3)
        self.assertEqual(summary["samples_accepted"], 3)
        self.assertEqual(summary["samples_rejected"], 0)
        self.assertEqual(summary["rejected_samples"], [])
        self.assertIs(summary["watch_only"], True)

        with self.assertRaisesRegex(TypeError, "samples must be a list"):
            run_local_shadow_review_label_workflow(tuple(samples))

        summary = run_local_shadow_review_label_workflow([copy.deepcopy(samples[0])])

        self.assertEqual(summary["samples_accepted"], 1)
        self.assertEqual(summary["samples_rejected"], 0)

    def test_workflow_rejects_invalid_samples_with_reasons(self):
        samples = [
            self._sample("SYNTH-BOUNDARY-VALID-001"),
            self._sample(
                "SYNTH-BOUNDARY-INVALID-LABEL-001",
                reviewer_label="approve_real_trade",
            ),
            self._sample(
                "SYNTH-BOUNDARY-INVALID-WORDING-001",
                diagnostics_summary="missing boundary text",
                reviewer_notes="also missing boundary text",
            ),
            ["not", "a", "sample"],
        ]

        summary = run_local_shadow_review_label_workflow(samples)

        self.assertEqual(summary["samples_processed"], 4)
        self.assertEqual(summary["samples_accepted"], 1)
        self.assertEqual(summary["samples_rejected"], 3)
        self.assertEqual(
            summary["rejected_samples"],
            [
                {
                    "sample_id": "SYNTH-BOUNDARY-INVALID-LABEL-001",
                    "reason": "Unsupported reviewer_label: approve_real_trade",
                },
                {
                    "sample_id": "SYNTH-BOUNDARY-INVALID-WORDING-001",
                    "reason": (
                        "shadow review wording must preserve local and "
                        "watch-only boundaries"
                    ),
                },
                {
                    "sample_id": "UNAVAILABLE",
                    "reason": "shadow review sample must be a dict",
                },
            ],
        )

    def test_nested_broker_order_account_option_pnl_trade_decision_fields_fail(self):
        forbidden_cases = {
            "broker": {"artifact": {"broker": "forbidden"}},
            "order": {"artifact": [{"order": "forbidden"}]},
            "account": {"artifact": {"nested": {"account": "forbidden"}}},
            "option": {"artifact": {"nested": [{"option": "forbidden"}]}},
            "p_and_l": {"artifact": {"nested": {"p_and_l": "forbidden"}}},
            "p&l": {"artifact": {"nested": {"p&l": "forbidden"}}},
            "trade_decision": {
                "artifact": {"nested": {"trade_decision": "forbidden"}}
            },
        }

        for field_name, extra in forbidden_cases.items():
            with self.subTest(field_name=field_name):
                sample = self._sample(
                    f"SYNTH-BOUNDARY-FORBIDDEN-{field_name.upper()}-001",
                    extra=extra,
                )

                summary = run_local_shadow_review_label_workflow([sample])

                self.assertEqual(summary["samples_accepted"], 0)
                self.assertEqual(summary["samples_rejected"], 1)
                self.assertIn(
                    "Forbidden execution/trade field",
                    summary["rejected_samples"][0]["reason"],
                )

    def test_workflow_summary_is_in_memory_only_and_creates_no_side_effects(self):
        samples = [self._sample("SYNTH-BOUNDARY-IN-MEMORY-001")]
        original_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                os.chdir(temp_dir)
                before = sorted(os.listdir(temp_dir))
                with mock.patch("builtins.open", side_effect=AssertionError("open")):
                    summary = run_local_shadow_review_label_workflow(samples)
                after = sorted(os.listdir(temp_dir))
            finally:
                os.chdir(original_cwd)

        self.assertEqual(before, [])
        self.assertEqual(after, [])
        self.assertEqual(tuple(summary.keys()), SHADOW_REVIEW_WORKFLOW_SUMMARY_FIELDS)
        self.assertNotIn("file", summary)
        self.assertNotIn("report", summary)
        self.assertNotIn("log", summary)
        self.assertNotIn("alert", summary)

    def test_workflow_makes_no_logs_alerts_loops_schedulers_subprocesses_or_network_calls(self):
        samples = [self._sample("SYNTH-BOUNDARY-NO-CALLS-001")]
        blocked = AssertionError("external side effect")

        with mock.patch("logging.Logger._log", side_effect=blocked), mock.patch(
            "threading.Thread.start", side_effect=blocked
        ), mock.patch("sched.scheduler.run", side_effect=blocked), mock.patch(
            "subprocess.Popen", side_effect=blocked
        ), mock.patch(
            "subprocess.run", side_effect=blocked
        ), mock.patch(
            "socket.socket", side_effect=blocked
        ), mock.patch(
            "urllib.request.urlopen", side_effect=blocked
        ):
            summary = run_local_shadow_review_label_workflow(samples)

        self.assertEqual(summary["samples_accepted"], 1)
        self.assertIs(summary["watch_only"], True)

    def test_workflow_remains_deterministic_and_does_not_mutate_samples(self):
        samples = [
            self._sample("SYNTH-BOUNDARY-DETERMINISTIC-001"),
            self._sample(
                "SYNTH-BOUNDARY-DETERMINISTIC-INVALID-001",
                no_trade_boundary_check=False,
            ),
        ]
        original_samples = copy.deepcopy(samples)

        first_summary = run_local_shadow_review_label_workflow(samples)
        second_summary = run_local_shadow_review_label_workflow(samples)

        self.assertEqual(first_summary, second_summary)
        self.assertEqual(samples, original_samples)

    def test_no_trade_boundary_wording_is_preserved(self):
        samples = [
            self._sample(
                "SYNTH-BOUNDARY-WORDING-001",
                reviewer_label="no_trade_boundary_preserved",
                diagnostics_summary=(
                    "local watch-only diagnostics preserve unavailable evidence"
                ),
                reviewer_notes=(
                    "local watch-only review preserves no-trade boundary wording"
                ),
            ),
            self._sample(
                "SYNTH-BOUNDARY-WORDING-INVALID-001",
                diagnostics_summary="synthetic diagnostics omit boundary language",
                reviewer_notes="review notes also omit boundary language",
            ),
        ]

        summary = run_local_shadow_review_label_workflow(samples)

        self.assertEqual(summary["samples_accepted"], 1)
        self.assertEqual(summary["samples_rejected"], 1)
        self.assertEqual(summary["no_trade_boundary_preserved_count"], 1)
        self.assertEqual(
            summary["label_counts"]["no_trade_boundary_preserved"],
            1,
        )
        self.assertIn("local and watch-only", summary["rejected_samples"][0]["reason"])

    def test_workflow_covers_all_labels_and_core_setup_families(self):
        setup_cycle = ("Ideal", "Clean Fast Break", "Continuation")
        samples = [
            self._sample(
                f"SYNTH-BOUNDARY-{label.upper()}-001",
                setup_cycle[index % len(setup_cycle)],
                label,
            )
            for index, label in enumerate(ALLOWED_SHADOW_REVIEW_LABELS)
        ]

        summary = run_local_shadow_review_label_workflow(samples)

        self.assertEqual(summary["samples_accepted"], len(ALLOWED_SHADOW_REVIEW_LABELS))
        self.assertEqual(
            summary["label_counts"],
            {label: 1 for label in ALLOWED_SHADOW_REVIEW_LABELS},
        )
        self.assertEqual(
            set(summary["setup_type_counts"]),
            {"Ideal", "Clean Fast Break", "Continuation"},
        )
        self.assertEqual(
            sum(summary["setup_type_counts"].values()),
            len(ALLOWED_SHADOW_REVIEW_LABELS),
        )

    def test_samples_do_not_invent_real_market_facts_or_trade_outputs(self):
        samples = [
            self._sample(
                "SYNTH-BOUNDARY-NO-REAL-FACTS-001",
                setup_type="Ideal",
                headline_news_status="NEWS_UNCONFIRMED",
                trigger_status="synthetic_artifact_supported_watch_candidate",
                diagnostics_summary=(
                    "local watch-only synthetic sample has no ticker headline "
                    "macro event outcome trade p&l or live fact"
                ),
                reviewer_notes=(
                    "local watch-only review uses synthetic sample ids only and "
                    "does not approve outcomes trades p&l or live facts"
                ),
            ),
        ]

        summary = run_local_shadow_review_label_workflow(samples)

        self.assertEqual(summary["samples_accepted"], 1)
        self.assertEqual(summary["samples_rejected"], 0)
        self.assertEqual(summary["setup_type_counts"], {"Ideal": 1})
        sample_text = repr(samples)
        for forbidden_text in (
            "SPY",
            "QQQ",
            "IWM",
            "GLD",
            "headline:",
            "macro event:",
            "outcome:",
            "trade:",
            "P&L:",
            "live fact:",
        ):
            self.assertNotIn(forbidden_text, sample_text)

    def test_final_boundary_sweep_is_included_in_local_validation_suite(self):
        from tests import test_watcher_foundation_local_validation_suite as suite_module

        self.assertIn(
            "tests.test_shadow_review_workflow_final_boundary_sweep",
            suite_module.WATCHER_FOUNDATION_TEST_MODULES,
        )


if __name__ == "__main__":
    unittest.main()
