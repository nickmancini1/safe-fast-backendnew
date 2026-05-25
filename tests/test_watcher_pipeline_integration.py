import copy
import subprocess
import unittest

from watcher_foundation.constants import (
    EVIDENCE_ROWS_UNCONFIRMED,
    NEWS_UNCONFIRMED,
    SOURCE_AS_OF_UNCONFIRMED,
    TRIGGER_LEVEL_UNCONFIRMED,
)
from watcher_foundation.pipeline import PIPELINE_RESULT_FIELDS, run_local_watcher_pipeline


class WatcherPipelineIntegrationTests(unittest.TestCase):
    def _observation(self, **overrides):
        observation = {
            "candidate_id": "SPY-Ideal-1",
            "symbol": "SPY",
            "watch_session_id": "session-1",
            "setup_type": "Ideal",
            "direction": "bullish/call-side",
            "regular_session_date": "2026-05-24",
            "first_seen_at": "2026-05-24T09:35:00-04:00",
            "last_seen_at": "2026-05-24T09:35:00-04:00",
            "stage": "near-trigger",
            "trigger_status": "near_trigger",
            "fresh_stale_spent_state": "fresh",
            "trigger_level_or_zone": "accepted trigger zone",
            "trigger_zone_bucket": "accepted trigger zone",
            "confirmation_timeframe_rule": "completed 1h hold",
            "distance_to_trigger": "near",
            "invalidation_level_or_condition": "accepted invalidation",
            "invalidation_bucket": "accepted invalidation",
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
            "watch_only": True,
        }
        observation.update(overrides)
        return observation

    def test_pipeline_returns_expected_top_level_fields_and_watch_only(self):
        result = run_local_watcher_pipeline(self._observation())

        self.assertEqual(set(result), set(PIPELINE_RESULT_FIELDS))
        self.assertIs(result["watch_only"], True)
        self.assertIs(result["state"]["watch_only"], True)
        self.assertIs(result["trigger_card"]["watch_only"], True)
        self.assertIs(result["no_trade_boundary"]["no_live_trade_approval"], True)
        self.assertIs(result["no_trade_boundary"]["trade_approval"], False)

    def test_pipeline_rejects_watch_only_false(self):
        with self.assertRaisesRegex(ValueError, "watch_only=True"):
            run_local_watcher_pipeline(self._observation(watch_only=False))

    def test_pipeline_rejects_forbidden_execution_account_order_fields(self):
        with self.assertRaisesRegex(ValueError, "order_id"):
            run_local_watcher_pipeline(self._observation(order_id="abc"))

        with self.assertRaisesRegex(ValueError, "account_id"):
            run_local_watcher_pipeline(
                self._observation(nested={"account_id": "abc"})
            )

    def test_pipeline_does_not_mutate_input_observation(self):
        observation = self._observation(
            unavailable_fields=[TRIGGER_LEVEL_UNCONFIRMED],
            headline_news={"source_status": "source_unconfirmed"},
        )
        before = copy.deepcopy(observation)

        result = run_local_watcher_pipeline(observation)
        result["state"]["unavailable_fields"].append("changed")

        self.assertEqual(observation, before)

    def test_missing_news_source_stays_news_unconfirmed(self):
        result = run_local_watcher_pipeline(self._observation())

        self.assertEqual(result["state"]["headline_news_status"], NEWS_UNCONFIRMED)
        self.assertEqual(
            result["trigger_card"]["headline_news_status"], NEWS_UNCONFIRMED
        )
        self.assertEqual(
            result["diagnostics"]["headline_news_status"], NEWS_UNCONFIRMED
        )
        self.assertEqual(
            result["duplicate_suppression"]["headline_news_status"],
            NEWS_UNCONFIRMED,
        )

    def test_unavailable_markers_are_preserved_through_artifacts(self):
        observation = self._observation(
            source_as_of=SOURCE_AS_OF_UNCONFIRMED,
            evidence_rows=[EVIDENCE_ROWS_UNCONFIRMED],
            unavailable_fields=[TRIGGER_LEVEL_UNCONFIRMED, SOURCE_AS_OF_UNCONFIRMED],
        )

        result = run_local_watcher_pipeline(observation)

        self.assertIn(TRIGGER_LEVEL_UNCONFIRMED, result["state"]["unavailable_fields"])
        self.assertIn(SOURCE_AS_OF_UNCONFIRMED, result["trigger_card"]["unavailable_fields"])
        self.assertIn(SOURCE_AS_OF_UNCONFIRMED, result["diagnostics"]["unavailable_fields"])
        self.assertIn(SOURCE_AS_OF_UNCONFIRMED, result["shadow_log_record"]["unavailable_fields"])

    def test_stale_spent_no_fresh_trigger_remains_no_trade(self):
        result = run_local_watcher_pipeline(
            self._observation(
                stage="stale/spent/no-fresh-trigger",
                trigger_status="stale",
                fresh_stale_spent_state="stale",
                no_trade_reason="watch_only_no_fresh_trigger_no_trade",
            )
        )

        no_trade_reason = result["trigger_card"]["no_trade_reason"].lower()
        self.assertIn("no fresh trigger", no_trade_reason)
        self.assertIn("no-trade", no_trade_reason)
        self.assertIn("no fresh trigger", result["diagnostics"]["diagnostic_explanation"].lower())

    def test_triggered_signal_stage_remains_shadow_only(self):
        result = run_local_watcher_pipeline(
            self._observation(
                stage="triggered_signal_stage",
                trigger_status="triggered",
                no_trade_reason="triggered_for_shadow_signal_review_only_no_live_trade_approval",
            )
        )

        self.assertTrue(result["no_trade_boundary"]["shadow_signal_review_only"])
        self.assertIn(
            "shadow signal review only",
            result["diagnostics"]["diagnostic_explanation"],
        )
        self.assertIn("no_live_trade_approval", result["trigger_card"]["no_trade_reason"])

    def test_same_state_repeat_suppresses_when_prior_suppression_state_provided(self):
        first = run_local_watcher_pipeline(self._observation())
        repeat = run_local_watcher_pipeline(
            self._observation(),
            previous_state=first["state"],
            previous_suppression_state=first["duplicate_suppression"],
        )

        self.assertEqual(
            repeat["duplicate_suppression"]["alert_decision"],
            "suppress_duplicate",
        )
        self.assertEqual(
            repeat["duplicate_suppression"]["suppression_reason"],
            "same_state_repeat_no_material_change",
        )

    def test_material_stage_change_emits_material_change(self):
        first = run_local_watcher_pipeline(self._observation())
        changed = run_local_watcher_pipeline(
            self._observation(
                stage="pending_completed_candle_approval",
                trigger_status="pending_completed_candle",
            ),
            previous_state=first["state"],
            previous_suppression_state=first["duplicate_suppression"],
        )

        self.assertEqual(
            changed["duplicate_suppression"]["alert_decision"],
            "emit_material_change",
        )
        self.assertIn(
            "stage_changed",
            changed["duplicate_suppression"]["material_change_flags"],
        )

    def test_focus_ranking_returns_one_primary_focus_when_eligible(self):
        result = run_local_watcher_pipeline(
            self._observation(),
            focus_candidates=[
                self._observation(candidate_id="one"),
                self._observation(candidate_id="two", distance_to_trigger="far"),
            ],
        )

        primary = [
            candidate
            for candidate in result["focus_ranking"]["ranked_candidates"]
            if candidate["focus_rank_bucket"] == "primary_focus"
        ]
        self.assertEqual(len(primary), 1)
        self.assertEqual(result["focus_ranking"]["primary_focus_candidate_id"], "one")

    def test_shadow_log_record_includes_state_and_trigger_card_snapshots(self):
        result = run_local_watcher_pipeline(self._observation())

        self.assertIn("state_snapshot", result["shadow_log_record"])
        self.assertIn("trigger_card_snapshot", result["shadow_log_record"])
        self.assertEqual(
            result["shadow_log_record"]["state_snapshot"]["candidate_id"],
            "SPY-Ideal-1",
        )
        self.assertEqual(
            result["shadow_log_record"]["trigger_card_snapshot"]["symbol"],
            "SPY",
        )

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
