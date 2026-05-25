import copy
import subprocess
import unittest

from watcher_foundation.batch_runner import (
    BATCH_RUNNER_RESULT_FIELDS,
    run_local_watcher_batch,
)
from watcher_foundation.constants import NEWS_UNCONFIRMED, SOURCE_AS_OF_UNCONFIRMED


class WatcherBatchRunnerTests(unittest.TestCase):
    def _observation(self, **overrides):
        observation = {
            "candidate_id": "SPY-batch",
            "symbol": "SPY",
            "watch_session_id": "batch-session",
            "setup_type": "Ideal",
            "direction": "bullish/call-side",
            "regular_session_date": "2026-05-24",
            "first_seen_at": "2026-05-24T09:35:00-04:00",
            "last_seen_at": "2026-05-24T09:35:00-04:00",
            "stage": "near-trigger",
            "trigger_status": "near_trigger",
            "fresh_stale_spent_state": "fresh",
            "trigger_level_or_zone": "432 reclaim zone",
            "trigger_zone_bucket": "432-zone",
            "confirmation_timeframe_rule": "completed 1h hold",
            "distance_to_trigger": "near",
            "invalidation_level_or_condition": "below local shelf",
            "invalidation_bucket": "local-shelf",
            "source_kind": "local_fixture",
            "source_as_of": "2026-05-24T09:35:00-04:00",
            "evidence_rows": ["fixture-row-1"],
            "evidence_quality": "deterministic",
            "unavailable_fields": [],
            "blockers": [],
            "cautions": [],
            "primary_blocker": "UNCONFIRMED",
            "headline_news_status": NEWS_UNCONFIRMED,
            "no_trade_reason": "watch_only_shadow_review_no_live_trade_approval",
            "next_check_or_next_alert_condition": "new_material_change_required",
            "trigger_path_identifier": "initial-path",
            "fresh_trigger_path_present": True,
            "watch_only": True,
        }
        observation.update(overrides)
        return observation

    def test_empty_observation_list_returns_watch_only_empty_result(self):
        result = run_local_watcher_batch([])

        self.assertEqual(set(result), set(BATCH_RUNNER_RESULT_FIELDS))
        self.assertEqual(result["observations_processed"], 0)
        self.assertTrue(result["watch_only"])
        self.assertEqual(result["shadow_log_records"], [])
        self.assertEqual(result["alert_decisions"], [])
        self.assertEqual(result["final_state"], {})
        self.assertFalse(result["no_trade_boundary"]["trade_approval"])

    def test_single_observation_returns_full_pipeline_output_summary(self):
        result = run_local_watcher_batch([self._observation()])

        self.assertEqual(result["observations_processed"], 1)
        self.assertEqual(result["final_state"]["candidate_id"], "SPY-batch")
        self.assertEqual(result["final_trigger_card"]["symbol"], "SPY")
        self.assertIn("diagnostic_explanation", result["final_diagnostics"])
        self.assertEqual(
            result["final_duplicate_suppression"]["alert_decision"],
            "emit_material_change",
        )
        self.assertEqual(len(result["shadow_log_records"]), 1)
        self.assertEqual(result["alert_decisions"], ["emit_material_change"])
        self.assertTrue(result["no_trade_boundary"]["watch_only"])

    def test_multi_observation_sequence_preserves_prior_state(self):
        result = run_local_watcher_batch(
            [
                self._observation(),
                self._observation(last_seen_at="2026-05-24T09:40:00-04:00"),
            ]
        )

        self.assertEqual(result["observations_processed"], 2)
        self.assertEqual(result["final_state"]["previous_stage"], "near-trigger")
        self.assertEqual(result["final_duplicate_suppression"]["repeat_count"], 1)
        self.assertEqual(
            result["final_duplicate_suppression"]["alert_decision"],
            "suppress_duplicate",
        )
        self.assertEqual(
            result["alert_decisions"],
            ["emit_material_change", "suppress_duplicate"],
        )

    def test_same_state_repeat_produces_duplicate_no_alert_decision(self):
        result = run_local_watcher_batch([self._observation(), self._observation()])

        self.assertEqual(
            result["final_duplicate_suppression"]["alert_decision"],
            "suppress_duplicate",
        )
        self.assertEqual(
            result["final_duplicate_suppression"]["suppression_reason"],
            "same_state_repeat_no_material_change",
        )

    def test_material_stage_change_breaks_suppression(self):
        result = run_local_watcher_batch(
            [
                self._observation(),
                self._observation(
                    stage="pending_completed_candle_approval",
                    trigger_status="pending_completed_candle",
                    trigger_path_identifier="completed-candle-path",
                ),
            ]
        )

        self.assertEqual(
            result["final_duplicate_suppression"]["alert_decision"],
            "emit_material_change",
        )
        self.assertIn(
            "stage_changed",
            result["final_duplicate_suppression"]["material_change_flags"],
        )

    def test_stale_spent_sequence_remains_no_trade(self):
        result = run_local_watcher_batch(
            [
                self._observation(),
                self._observation(
                    stage="stale/spent/no-fresh-trigger",
                    trigger_status="stale",
                    fresh_stale_spent_state="stale",
                    no_trade_reason="watch_only_no_fresh_trigger_no_trade",
                    fresh_trigger_path_present=False,
                ),
            ]
        )

        self.assertEqual(result["final_state"]["fresh_stale_spent_state"], "stale")
        self.assertIn(
            "no fresh trigger",
            result["final_trigger_card"]["no_trade_reason"].lower(),
        )
        self.assertFalse(result["no_trade_boundary"]["trade_approval"])

    def test_fresh_trigger_after_stale_spent_breaks_suppression(self):
        result = run_local_watcher_batch(
            [
                self._observation(),
                self._observation(
                    stage="stale/spent/no-fresh-trigger",
                    trigger_status="stale",
                    fresh_stale_spent_state="stale",
                    no_trade_reason="watch_only_no_fresh_trigger_no_trade",
                    trigger_path_identifier="expired-path",
                    fresh_trigger_path_present=False,
                ),
                self._observation(
                    stage="rebuilding",
                    trigger_status="near_trigger",
                    fresh_stale_spent_state="rebuilding",
                    no_trade_reason=(
                        "watch_only_rebuilt_structure_review_no_live_trade_approval"
                    ),
                    trigger_path_identifier="rebuilt-fresh-path",
                    fresh_trigger_path_present=True,
                ),
            ]
        )

        self.assertEqual(result["final_state"]["fresh_stale_spent_state"], "rebuilding")
        self.assertEqual(
            result["final_duplicate_suppression"]["alert_decision"],
            "emit_material_change",
        )
        self.assertIn(
            "trigger_path_changed",
            result["final_duplicate_suppression"]["material_change_flags"],
        )

    def test_news_unconfirmed_remains_default_without_source_payload(self):
        result = run_local_watcher_batch([self._observation()])

        self.assertEqual(result["final_state"]["headline_news_status"], NEWS_UNCONFIRMED)
        self.assertEqual(
            result["final_trigger_card"]["headline_news_status"], NEWS_UNCONFIRMED
        )
        self.assertEqual(
            result["final_diagnostics"]["headline_news_status"], NEWS_UNCONFIRMED
        )

    def test_unavailable_markers_and_no_trade_reason_are_preserved(self):
        result = run_local_watcher_batch(
            [
                self._observation(
                    source_as_of=SOURCE_AS_OF_UNCONFIRMED,
                    evidence_rows=[],
                    unavailable_fields=["source_as_of", "evidence_rows"],
                    no_trade_reason="watch_only_unavailable_source_no_trade",
                )
            ]
        )

        self.assertIn("source_as_of", result["final_state"]["unavailable_fields"])
        self.assertIn("evidence_rows", result["final_trigger_card"]["unavailable_fields"])
        self.assertEqual(
            result["final_diagnostics"]["no_trade_reason"],
            "watch_only_unavailable_source_no_trade",
        )

    def test_triggered_signal_stage_remains_shadow_only(self):
        result = run_local_watcher_batch(
            [
                self._observation(
                    stage="triggered_signal_stage",
                    trigger_status="triggered",
                    no_trade_reason=(
                        "triggered_for_shadow_signal_review_only_no_live_trade_approval"
                    ),
                )
            ]
        )

        self.assertTrue(result["no_trade_boundary"]["shadow_signal_review_only"])
        self.assertIn(
            "shadow signal review only",
            result["final_diagnostics"]["diagnostic_explanation"],
        )

    def test_input_observations_are_not_mutated(self):
        observations = [
            self._observation(
                unavailable_fields=["source_as_of"],
                nested={"watch_only": True},
            )
        ]
        before = copy.deepcopy(observations)

        result = run_local_watcher_batch(observations)
        result["final_state"]["unavailable_fields"].append("changed")
        result["shadow_log_records"][0]["state_snapshot"]["symbol"] = "QQQ"

        self.assertEqual(observations, before)

    def test_watch_only_false_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "watch_only=True"):
            run_local_watcher_batch([self._observation(watch_only=False)])

    def test_observations_must_be_list_of_dicts(self):
        with self.assertRaisesRegex(TypeError, "list"):
            run_local_watcher_batch((self._observation(),))

        with self.assertRaisesRegex(TypeError, "dict"):
            run_local_watcher_batch([["not", "a", "dict"]])

    def test_forbidden_execution_account_order_fields_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "order_id"):
            run_local_watcher_batch([self._observation(order_id="abc")])

        with self.assertRaisesRegex(ValueError, "account_id"):
            run_local_watcher_batch(
                [self._observation(nested={"account_id": "abc"})]
            )

    def test_shadow_log_records_are_accumulated_in_memory_only(self):
        result = run_local_watcher_batch([self._observation(), self._observation()])

        self.assertEqual(len(result["shadow_log_records"]), 2)
        self.assertTrue(all(isinstance(record, dict) for record in result["shadow_log_records"]))
        self.assertEqual(
            result["shadow_log_records"][0]["state_snapshot"]["candidate_id"],
            "SPY-batch",
        )

        status = subprocess.run(
            ["git", "status", "-sb", "--untracked-files=all"],
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertNotIn(".jsonl", status.stdout)

    def test_main_py_has_no_change(self):
        result = subprocess.run(
            ["git", "diff", "--quiet", "--", "main.py"],
            check=False,
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
