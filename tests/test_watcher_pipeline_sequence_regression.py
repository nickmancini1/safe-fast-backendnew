import subprocess
import unittest

from watcher_foundation.constants import NEWS_UNCONFIRMED, SOURCE_AS_OF_UNCONFIRMED
from watcher_foundation.pipeline import run_local_watcher_pipeline


class WatcherPipelineSequenceRegressionTests(unittest.TestCase):
    def _observation(self, **overrides):
        observation = {
            "candidate_id": "SPY-Ideal-sequence",
            "symbol": "SPY",
            "watch_session_id": "sequence-session",
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

    def _run_next(self, observation, previous):
        return run_local_watcher_pipeline(
            observation,
            previous_state=previous["state"],
            previous_suppression_state=previous["duplicate_suppression"],
            previous_primary_focus_candidate_id=previous["focus_ranking"][
                "primary_focus_candidate_id"
            ],
        )

    def test_local_observation_sequence_regression(self):
        first = run_local_watcher_pipeline(self._observation())

        self.assertTrue(first["watch_only"])
        self.assertEqual(first["state"]["stage"], "near-trigger")
        self.assertEqual(first["trigger_card"]["trigger_status"], "near_trigger")
        self.assertEqual(
            first["duplicate_suppression"]["alert_decision"], "emit_material_change"
        )
        self.assertEqual(
            first["focus_ranking"]["primary_focus_candidate_id"],
            "SPY-Ideal-sequence",
        )
        self.assertEqual(first["state"]["headline_news_status"], NEWS_UNCONFIRMED)
        self.assertIn("state_snapshot", first["shadow_log_record"])
        self.assertIn("trigger_card_snapshot", first["shadow_log_record"])
        self.assertIn("watch_only", first["diagnostics"]["no_trade_reason"])

        repeat = self._run_next(self._observation(), first)
        self.assertEqual(
            repeat["duplicate_suppression"]["alert_decision"], "suppress_duplicate"
        )

        stage_changed = self._run_next(
            self._observation(
                last_seen_at="2026-05-24T10:35:00-04:00",
                stage="pending_completed_candle_approval",
                trigger_status="pending_completed_candle",
                trigger_path_identifier="completed-candle-path",
            ),
            repeat,
        )
        self.assertEqual(
            stage_changed["duplicate_suppression"]["alert_decision"],
            "emit_material_change",
        )
        self.assertIn(
            "stage_changed",
            stage_changed["duplicate_suppression"]["material_change_flags"],
        )

        trigger_changed = self._run_next(
            self._observation(
                last_seen_at="2026-05-24T11:35:00-04:00",
                stage="pending_completed_candle_approval",
                trigger_status="triggered",
                trigger_path_identifier="triggered-path",
            ),
            stage_changed,
        )
        self.assertIn(
            "trigger_status_changed",
            trigger_changed["duplicate_suppression"]["material_change_flags"],
        )
        self.assertEqual(
            trigger_changed["duplicate_suppression"]["alert_decision"],
            "emit_material_change",
        )

        stale = self._run_next(
            self._observation(
                last_seen_at="2026-05-24T12:35:00-04:00",
                stage="stale/spent/no-fresh-trigger",
                trigger_status="stale",
                fresh_stale_spent_state="stale",
                no_trade_reason="watch_only_no_fresh_trigger_no_trade",
                next_check_or_next_alert_condition="wait_for_rebuilt_structure",
                trigger_path_identifier="expired-path",
                fresh_trigger_path_present=False,
            ),
            trigger_changed,
        )
        self.assertEqual(stale["state"]["fresh_stale_spent_state"], "stale")
        self.assertIn("no fresh trigger", stale["trigger_card"]["no_trade_reason"].lower())
        self.assertIn("no fresh trigger", stale["diagnostics"]["diagnostic_explanation"].lower())
        self.assertFalse(stale["no_trade_boundary"]["trade_approval"])

        stale_repeat = self._run_next(
            self._observation(
                last_seen_at="2026-05-24T12:35:00-04:00",
                stage="stale/spent/no-fresh-trigger",
                trigger_status="stale",
                fresh_stale_spent_state="stale",
                no_trade_reason="watch_only_no_fresh_trigger_no_trade",
                next_check_or_next_alert_condition="wait_for_rebuilt_structure",
                trigger_path_identifier="expired-path",
                fresh_trigger_path_present=False,
            ),
            stale,
        )
        self.assertEqual(
            stale_repeat["duplicate_suppression"]["alert_decision"],
            "suppress_duplicate",
        )

        rebuilt = self._run_next(
            self._observation(
                last_seen_at="2026-05-24T13:35:00-04:00",
                stage="rebuilding",
                trigger_status="near_trigger",
                fresh_stale_spent_state="rebuilding",
                no_trade_reason="watch_only_rebuilt_structure_review_no_live_trade_approval",
                next_check_or_next_alert_condition="fresh_path_requires_review",
                trigger_path_identifier="rebuilt-fresh-path",
                fresh_trigger_path_present=True,
            ),
            stale_repeat,
        )
        self.assertEqual(
            rebuilt["duplicate_suppression"]["alert_decision"],
            "emit_material_change",
        )
        self.assertIn(
            "trigger_path_changed",
            rebuilt["duplicate_suppression"]["material_change_flags"],
        )
        self.assertTrue(rebuilt["trigger_card"]["fresh_trigger_path_present"])

        no_source = run_local_watcher_pipeline(self._observation(headline_news_source={}))
        self.assertEqual(no_source["state"]["headline_news_status"], NEWS_UNCONFIRMED)
        self.assertIn("news_unconfirmed_default", no_source["state"]["news_policy_reason_codes"])

        caution = run_local_watcher_pipeline(
            self._observation(),
            headline_news_source={
                "headline_news_status": "NEWS_CAUTION",
                "source_status": "source_confirmed",
                "source_as_of": "2026-05-24T09:40:00-04:00",
                "evidence_refs": ["caller-news-ref-1"],
                "watch_only": True,
            },
        )
        self.assertEqual(caution["state"]["headline_news_status"], "NEWS_CAUTION")
        self.assertIn(
            "caution.news_source_confirmed_caution",
            caution["diagnostics"]["diagnostic_reason_codes"]["caution"],
        )
        self.assertEqual(caution["state"]["news_evidence_refs"], ["caller-news-ref-1"])

        blocked_news = run_local_watcher_pipeline(
            self._observation(candidate_id="SPY-news-block"),
            headline_news_source={
                "headline_news_status": "NEWS_BLOCK",
                "source_status": "source_confirmed",
                "source_as_of": "2026-05-24T09:45:00-04:00",
                "evidence_refs": ["caller-news-ref-2"],
                "watch_only": True,
            },
        )
        self.assertEqual(blocked_news["state"]["headline_news_status"], "NEWS_BLOCK")
        self.assertIn(
            "blocker.news_source_confirmed_block",
            blocked_news["diagnostics"]["diagnostic_reason_codes"]["blocker"],
        )

        focus_changed = run_local_watcher_pipeline(
            self._observation(candidate_id="cleaner-farther", distance_to_trigger="medium"),
            focus_candidates=[
                self._observation(
                    candidate_id="blocked-closer",
                    stage="blocked/no-trade",
                    distance_to_trigger="near",
                    blockers=[{"reason_code": "source_confirmed_block", "severity": "block"}],
                    primary_blocker="source_confirmed_block",
                ),
                self._observation(
                    candidate_id="stale-closer",
                    stage="stale/spent/no-fresh-trigger",
                    trigger_status="stale",
                    fresh_stale_spent_state="stale",
                    distance_to_trigger="near",
                ),
                self._observation(
                    candidate_id="cleaner-farther",
                    distance_to_trigger="medium",
                ),
            ],
            previous_primary_focus_candidate_id="blocked-closer",
        )
        self.assertEqual(
            focus_changed["focus_ranking"]["primary_focus_candidate_id"],
            "cleaner-farther",
        )
        self.assertTrue(focus_changed["focus_ranking"]["best_candidate_changed"])

        sequence = [first, repeat, stage_changed, trigger_changed, stale, stale_repeat, rebuilt]
        for result in sequence:
            self.assertEqual(
                result["shadow_log_record"]["state_snapshot"]["candidate_id"],
                result["state"]["candidate_id"],
            )
            self.assertEqual(
                result["shadow_log_record"]["trigger_card_snapshot"]["stage"],
                result["trigger_card"]["stage"],
            )
            self.assertTrue(result["shadow_log_record"]["watch_only"])

        unavailable = run_local_watcher_pipeline(
            self._observation(
                candidate_id="unavailable-sequence",
                source_as_of=SOURCE_AS_OF_UNCONFIRMED,
                evidence_rows=[],
                unavailable_fields=["source_as_of", "evidence_rows"],
                no_trade_reason="",
            )
        )
        self.assertIn(
            "unconfirmed",
            unavailable["diagnostics"]["diagnostic_explanation"].lower(),
        )
        self.assertIn(
            "source_as_of",
            unavailable["diagnostics"]["diagnostic_explanation"],
        )
        self.assertFalse(unavailable["no_trade_boundary"]["trade_approval"])

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
