import subprocess
import unittest

from watcher_foundation.constants import (
    DISTANCE_TO_TRIGGER_UNCONFIRMED,
    EVIDENCE_ROWS_UNCONFIRMED,
    INVALIDATION_UNCONFIRMED,
    NEWS_UNCONFIRMED,
    SOURCE_AS_OF_UNCONFIRMED,
    TRIGGER_LEVEL_UNCONFIRMED,
)
from watcher_foundation.state_tracker import WatcherTrackedState, update_watcher_state


class WatcherStateTrackingTests(unittest.TestCase):
    def test_previous_lifecycle_values_are_preserved_on_update(self):
        previous = WatcherTrackedState(
            candidate_id="SPY-Ideal-1",
            symbol="SPY",
            watch_session_id="session-1",
            setup_type="Ideal",
            direction="bullish/call-side",
            stage="forming/developing",
            trigger_status="waiting_for_trigger",
            fresh_stale_spent_state="fresh",
        )

        updated = update_watcher_state(
            previous,
            {
                "stage": "near-trigger",
                "trigger_status": "near_trigger",
                "fresh_stale_spent_state": "fresh",
                "watch_only": True,
            },
        )

        self.assertEqual(updated.previous_stage, previous.stage)
        self.assertEqual(updated.previous_trigger_status, previous.trigger_status)
        self.assertEqual(
            updated.previous_fresh_stale_spent_state,
            previous.fresh_stale_spent_state,
        )

    def test_state_version_increments_on_material_stage_change(self):
        previous = WatcherTrackedState(
            stage="forming/developing",
            trigger_status="waiting_for_trigger",
            fresh_stale_spent_state="fresh",
            state_version=4,
        )

        updated = update_watcher_state(
            previous,
            {"stage": "near-trigger", "watch_only": True},
        )

        self.assertEqual(updated.state_version, 5)
        self.assertIn("stage_changed", updated.material_change_flags)
        self.assertTrue(updated.state_changed)

    def test_state_version_does_not_increment_on_no_material_repeat(self):
        previous = WatcherTrackedState(
            stage="near-trigger",
            trigger_status="near_trigger",
            fresh_stale_spent_state="fresh",
            state_version=7,
            repeat_count=2,
        )

        updated = update_watcher_state(
            previous,
            {
                "stage": "near-trigger",
                "trigger_status": "near_trigger",
                "fresh_stale_spent_state": "fresh",
                "watch_only": True,
            },
        )

        self.assertEqual(updated.state_version, 7)
        self.assertEqual(updated.repeat_count, 3)
        self.assertEqual(updated.material_change_flags, ("no_material_change",))
        self.assertFalse(updated.state_changed)

    def test_first_seen_is_preserved_and_last_seen_updates(self):
        previous = WatcherTrackedState(
            first_seen_at="2026-05-24T09:30:00-04:00",
            last_seen_at="2026-05-24T09:30:00-04:00",
        )

        updated = update_watcher_state(
            previous,
            {"last_seen_at": "2026-05-24T09:35:00-04:00", "watch_only": True},
        )

        self.assertEqual(updated.first_seen_at, "2026-05-24T09:30:00-04:00")
        self.assertEqual(updated.last_seen_at, "2026-05-24T09:35:00-04:00")

    def test_watch_only_stays_true(self):
        updated = update_watcher_state(None, {"candidate_id": "x", "watch_only": True})

        self.assertIs(updated.watch_only, True)
        self.assertIs(updated.to_dict()["watch_only"], True)

        with self.assertRaisesRegex(ValueError, "watch_only=True"):
            update_watcher_state(updated, {"watch_only": False})

    def test_unavailable_markers_and_news_default_are_preserved(self):
        state = update_watcher_state(None, {"candidate_id": "x", "watch_only": True})
        output = state.to_dict()

        self.assertEqual(output["trigger_level_or_zone"], TRIGGER_LEVEL_UNCONFIRMED)
        self.assertEqual(output["distance_to_trigger"], DISTANCE_TO_TRIGGER_UNCONFIRMED)
        self.assertEqual(
            output["invalidation_level_or_condition"], INVALIDATION_UNCONFIRMED
        )
        self.assertEqual(output["source_as_of"], SOURCE_AS_OF_UNCONFIRMED)
        self.assertEqual(output["evidence_rows"], [EVIDENCE_ROWS_UNCONFIRMED])
        self.assertEqual(output["headline_news_status"], NEWS_UNCONFIRMED)
        self.assertIn(TRIGGER_LEVEL_UNCONFIRMED, output["unavailable_fields"])

    def test_forbidden_execution_account_order_fields_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "order_id"):
            update_watcher_state(None, {"candidate_id": "x", "order_id": "abc"})

        with self.assertRaisesRegex(ValueError, "account_id"):
            update_watcher_state(
                WatcherTrackedState(),
                {"nested": {"account_id": "abc"}, "watch_only": True},
            )

    def test_material_flags_cover_stage_status_and_freshness_changes(self):
        previous = WatcherTrackedState(
            stage="forming/developing",
            trigger_status="waiting_for_trigger",
            fresh_stale_spent_state="fresh",
        )

        updated = update_watcher_state(
            previous,
            {
                "stage": "blocked/no-trade",
                "trigger_status": "no_valid_trigger",
                "fresh_stale_spent_state": "stale",
                "watch_only": True,
            },
        )

        self.assertIn("stage_changed", updated.material_change_flags)
        self.assertIn("trigger_status_changed", updated.material_change_flags)
        self.assertIn("freshness_changed", updated.material_change_flags)

    def test_material_flags_cover_context_and_critical_availability_changes(self):
        previous = WatcherTrackedState()

        updated = update_watcher_state(
            previous,
            {
                "trigger_level_or_zone": "SPY 530-531 reclaim zone",
                "trigger_zone_bucket": "reclaim_zone",
                "invalidation_level_or_condition": "fail back below 528",
                "invalidation_bucket": "below_reclaim_base",
                "primary_blocker": "completed_candle_hold_unconfirmed",
                "evidence_quality": "partial",
                "unavailable_fields": [SOURCE_AS_OF_UNCONFIRMED],
                "watch_only": True,
            },
        )

        self.assertIn("trigger_zone_changed", updated.material_change_flags)
        self.assertIn("invalidation_changed", updated.material_change_flags)
        self.assertIn("primary_blocker_changed", updated.material_change_flags)
        self.assertIn("evidence_quality_changed", updated.material_change_flags)
        self.assertIn(
            "critical_field_became_available", updated.material_change_flags
        )

    def test_candidate_identity_fields_are_preserved_from_previous_state(self):
        previous = WatcherTrackedState(
            candidate_id="SPY-Ideal-1",
            symbol="SPY",
            watch_session_id="session-1",
            setup_type="Ideal",
            direction="bullish/call-side",
        )

        updated = update_watcher_state(
            previous,
            {
                "candidate_id": "DIFFERENT",
                "symbol": "QQQ",
                "setup_type": "Continuation",
                "direction": "neutral/unknown",
                "watch_session_id": "session-2",
                "watch_only": True,
            },
        )

        self.assertEqual(updated.candidate_id, "SPY-Ideal-1")
        self.assertEqual(updated.symbol, "SPY")
        self.assertEqual(updated.setup_type, "Ideal")
        self.assertEqual(updated.direction, "bullish/call-side")
        self.assertEqual(updated.watch_session_id, "session-1")

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
