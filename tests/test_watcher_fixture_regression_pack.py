import unittest

from watcher_foundation.batch_runner import run_local_watcher_batch
from watcher_foundation.constants import NEWS_UNCONFIRMED


class WatcherFixtureRegressionPackTests(unittest.TestCase):
    def _fixture_observation(self, setup_type, **overrides):
        fixture_slug = setup_type.lower().replace(" ", "-")
        observation = {
            "candidate_id": f"LOCAL-{fixture_slug}-fixture",
            "symbol": "LOCAL",
            "watch_session_id": "local-fixture-session",
            "setup_type": setup_type,
            "direction": "bullish/call-side",
            "regular_session_date": "2026-05-24",
            "first_seen_at": "2026-05-24T09:35:00-04:00",
            "last_seen_at": "2026-05-24T09:35:00-04:00",
            "stage": "near-trigger",
            "trigger_status": "near_trigger",
            "fresh_stale_spent_state": "fresh",
            "trigger_level_or_zone": "local reclaim zone",
            "trigger_zone_bucket": f"{fixture_slug}-local-zone",
            "confirmation_timeframe_rule": "local completed-candle review",
            "distance_to_trigger": "near",
            "invalidation_level_or_condition": "local structure invalidation",
            "invalidation_bucket": f"{fixture_slug}-local-invalidation",
            "source_kind": "local_fixture",
            "source_as_of": "2026-05-24T09:35:00-04:00",
            "evidence_rows": [f"{fixture_slug}-fixture-row-1"],
            "evidence_quality": "deterministic",
            "unavailable_fields": [],
            "blockers": [],
            "cautions": [],
            "primary_blocker": "UNCONFIRMED",
            "no_trade_reason": "watch_only_shadow_review_no_live_trade_approval",
            "next_check_or_next_alert_condition": "new_material_change_required",
            "trigger_path_identifier": f"{fixture_slug}-initial-path",
            "fresh_trigger_path_present": True,
            "watch_only": True,
        }
        observation.update(overrides)
        return observation

    def _assert_common_batch_contract(self, result, setup_type):
        self.assertTrue(result["watch_only"])
        self.assertEqual(result["final_state"]["setup_type"], setup_type)
        self.assertEqual(result["final_trigger_card"]["setup_type"], setup_type)
        self.assertEqual(result["final_diagnostics"]["setup_type"], setup_type)
        self.assertIn("final_trigger_card", result)
        self.assertIn("final_diagnostics", result)
        self.assertIn("final_duplicate_suppression", result)
        self.assertIn("final_focus_ranking", result)
        self.assertIn("shadow_log_records", result)
        self.assertGreaterEqual(len(result["shadow_log_records"]), 1)
        self.assertTrue(result["final_trigger_card"]["watch_only"])
        self.assertTrue(result["final_diagnostics"]["watch_only"])
        self.assertTrue(result["final_duplicate_suppression"]["watch_only"])
        self.assertTrue(result["final_focus_ranking"]["watch_only"])
        self.assertFalse(result["no_trade_boundary"]["trade_approval"])
        self.assertFalse(result["no_trade_boundary"]["live_trade_approval"])
        self.assertTrue(result["no_trade_boundary"]["no_live_trade_approval"])

    def test_all_setup_fixture_sequences_flow_through_batch_runner(self):
        for setup_type in ("Ideal", "Clean Fast Break", "Continuation"):
            with self.subTest(setup_type=setup_type):
                result = run_local_watcher_batch(
                    [
                        self._fixture_observation(setup_type),
                        self._fixture_observation(
                            setup_type,
                            last_seen_at="2026-05-24T10:35:00-04:00",
                            stage="pending_completed_candle_approval",
                            trigger_status="pending_completed_candle",
                            trigger_path_identifier=(
                                setup_type.lower().replace(" ", "-")
                                + "-completed-candle-path"
                            ),
                        ),
                    ]
                )

                self.assertEqual(result["observations_processed"], 2)
                self._assert_common_batch_contract(result, setup_type)
                self.assertEqual(
                    result["final_duplicate_suppression"]["alert_decision"],
                    "emit_material_change",
                )
                self.assertIn(
                    "stage_changed",
                    result["final_duplicate_suppression"]["material_change_flags"],
                )

    def test_same_state_repeat_suppresses_without_hiding_material_change(self):
        repeat_result = run_local_watcher_batch(
            [
                self._fixture_observation("Ideal"),
                self._fixture_observation("Ideal"),
            ]
        )

        self.assertIn(
            repeat_result["final_duplicate_suppression"]["alert_decision"],
            {"suppress_duplicate", "no_alert_no_material_change"},
        )
        self.assertEqual(
            repeat_result["final_duplicate_suppression"]["suppression_reason"],
            "same_state_repeat_no_material_change",
        )

        changed_result = run_local_watcher_batch(
            [
                self._fixture_observation("Ideal"),
                self._fixture_observation("Ideal"),
                self._fixture_observation(
                    "Ideal",
                    last_seen_at="2026-05-24T10:35:00-04:00",
                    trigger_status="pending_completed_candle",
                    trigger_path_identifier="ideal-pending-candle-path",
                ),
            ]
        )

        self.assertEqual(
            changed_result["final_duplicate_suppression"]["alert_decision"],
            "emit_material_change",
        )
        self.assertIn(
            "trigger_status_changed",
            changed_result["final_duplicate_suppression"]["material_change_flags"],
        )

    def test_stale_spent_continuation_remains_no_trade_no_fresh_trigger(self):
        result = run_local_watcher_batch(
            [
                self._fixture_observation("Continuation"),
                self._fixture_observation(
                    "Continuation",
                    last_seen_at="2026-05-24T10:35:00-04:00",
                    stage="stale/spent/no-fresh-trigger",
                    trigger_status="stale",
                    fresh_stale_spent_state="stale",
                    no_trade_reason="watch_only_no_fresh_trigger_no_trade",
                    next_check_or_next_alert_condition="wait_for_rebuilt_structure",
                    trigger_path_identifier="continuation-expired-path",
                    fresh_trigger_path_present=False,
                ),
            ]
        )

        self._assert_common_batch_contract(result, "Continuation")
        self.assertEqual(result["final_state"]["fresh_stale_spent_state"], "stale")
        self.assertFalse(result["final_trigger_card"]["fresh_trigger_path_present"])
        self.assertIn(
            "no fresh trigger",
            result["final_trigger_card"]["no_trade_reason"].lower(),
        )
        self.assertIn(
            "no fresh trigger",
            result["final_diagnostics"]["diagnostic_explanation"].lower(),
        )
        self.assertFalse(result["no_trade_boundary"]["shadow_signal_review_only"])

    def test_news_unconfirmed_is_default_without_source_payload(self):
        for setup_type in ("Ideal", "Clean Fast Break", "Continuation"):
            with self.subTest(setup_type=setup_type):
                result = run_local_watcher_batch([self._fixture_observation(setup_type)])

                self.assertEqual(
                    result["final_state"]["headline_news_status"], NEWS_UNCONFIRMED
                )
                self.assertEqual(
                    result["final_trigger_card"]["headline_news_status"],
                    NEWS_UNCONFIRMED,
                )
                self.assertEqual(
                    result["final_diagnostics"]["headline_news_status"],
                    NEWS_UNCONFIRMED,
                )
                self.assertIn(
                    "news_unconfirmed_default",
                    result["final_state"]["news_policy_reason_codes"],
                )

    def test_fixture_outputs_do_not_imply_live_trade_approval(self):
        result = run_local_watcher_batch(
            [
                self._fixture_observation("Clean Fast Break"),
                self._fixture_observation(
                    "Clean Fast Break",
                    last_seen_at="2026-05-24T10:35:00-04:00",
                    stage="triggered_signal_stage",
                    trigger_status="triggered",
                    no_trade_reason=(
                        "triggered_for_shadow_signal_review_only_no_live_trade_approval"
                    ),
                    trigger_path_identifier="clean-fast-break-shadow-trigger-path",
                ),
            ]
        )

        self._assert_common_batch_contract(result, "Clean Fast Break")
        self.assertTrue(result["no_trade_boundary"]["shadow_signal_review_only"])
        self.assertFalse(result["no_trade_boundary"]["trade_approval"])
        self.assertFalse(result["no_trade_boundary"]["live_trade_approval"])
        self.assertEqual(
            result["alert_decisions"],
            ["emit_material_change", "emit_material_change"],
        )


if __name__ == "__main__":
    unittest.main()
