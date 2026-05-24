import copy
import subprocess
import unittest

from watcher_foundation.constants import (
    INVALIDATION_UNCONFIRMED,
    NEWS_UNCONFIRMED,
    TRIGGER_LEVEL_UNCONFIRMED,
)
from watcher_foundation.duplicate_suppression import (
    DUPLICATE_SUPPRESSION_KEY_FIELD_NAMES,
    decide_duplicate_suppression,
)


class DuplicateSuppressionRuntimeTests(unittest.TestCase):
    def _card(self, **overrides):
        card = {
            "candidate_id": "SPY-Ideal-1",
            "symbol": "SPY",
            "setup_type": "Ideal",
            "direction": "bullish/call-side",
            "stage": "near-trigger",
            "trigger_status": "near_trigger",
            "fresh_stale_spent_state": "fresh",
            "primary_blocker": "completed_candle_hold_unconfirmed",
            "trigger_zone_bucket": "spy_reclaim_zone",
            "trigger_level_or_zone": "SPY reclaim zone",
            "invalidation_bucket": "below_reclaim_base",
            "invalidation_level_or_condition": "fail below reclaim base",
            "blockers": [
                {
                    "reason_code": "completed_candle_hold_unconfirmed",
                    "severity": "block",
                }
            ],
            "cautions": [{"reason_code": "news_unconfirmed", "severity": "caution"}],
            "evidence_quality": "partial",
            "unavailable_fields": [TRIGGER_LEVEL_UNCONFIRMED, INVALIDATION_UNCONFIRMED],
            "headline_news_status": NEWS_UNCONFIRMED,
            "material_change_flags": ["no_material_change"],
            "trigger_path_identifier": "initial_reclaim",
            "regular_session_date": "2026-05-24",
            "best_candidate_id": "SPY-Ideal-1",
            "watch_only": True,
        }
        card.update(overrides)
        return card

    def test_same_state_repeat_suppresses_duplicate(self):
        first = decide_duplicate_suppression(self._card())
        repeat = decide_duplicate_suppression(self._card(), first)

        self.assertEqual(repeat["alert_decision"], "suppress_duplicate")
        self.assertEqual(repeat["repeat_count"], 1)
        self.assertEqual(repeat["material_change_flags"], [])

    def test_first_observation_emits_as_new_state(self):
        decision = decide_duplicate_suppression(self._card())

        self.assertEqual(decision["alert_decision"], "emit_material_change")
        self.assertEqual(decision["suppression_reason"], "new_state_observation")
        self.assertEqual(set(decision["duplicate_suppression_key_fields"]), set(DUPLICATE_SUPPRESSION_KEY_FIELD_NAMES))

    def test_stage_change_breaks_suppression(self):
        first = decide_duplicate_suppression(self._card())
        decision = decide_duplicate_suppression(
            self._card(stage="triggered_signal_stage"), first
        )

        self.assertEqual(decision["alert_decision"], "emit_material_change")
        self.assertIn("stage_changed", decision["material_change_flags"])

    def test_trigger_status_change_breaks_suppression(self):
        first = decide_duplicate_suppression(self._card())
        decision = decide_duplicate_suppression(
            self._card(trigger_status="pending_completed_candle"), first
        )

        self.assertIn("trigger_status_changed", decision["material_change_flags"])

    def test_freshness_change_breaks_suppression(self):
        first = decide_duplicate_suppression(self._card())
        decision = decide_duplicate_suppression(
            self._card(fresh_stale_spent_state="stale"), first
        )

        self.assertIn("freshness_changed", decision["material_change_flags"])

    def test_primary_blocker_change_breaks_suppression(self):
        first = decide_duplicate_suppression(self._card())
        decision = decide_duplicate_suppression(
            self._card(primary_blocker="trigger_level_unconfirmed"), first
        )

        self.assertIn("primary_blocker_changed", decision["material_change_flags"])

    def test_blocker_severity_change_breaks_suppression(self):
        first = decide_duplicate_suppression(self._card())
        decision = decide_duplicate_suppression(
            self._card(
                blockers=[
                    {
                        "reason_code": "completed_candle_hold_unconfirmed",
                        "severity": "warning",
                    }
                ]
            ),
            first,
        )

        self.assertIn("blocker_severity_changed", decision["material_change_flags"])

    def test_caution_severity_change_breaks_suppression(self):
        first = decide_duplicate_suppression(self._card())
        decision = decide_duplicate_suppression(
            self._card(
                cautions=[{"reason_code": "news_unconfirmed", "severity": "block"}]
            ),
            first,
        )

        self.assertIn("caution_severity_changed", decision["material_change_flags"])

    def test_trigger_zone_bucket_change_breaks_suppression(self):
        first = decide_duplicate_suppression(self._card())
        decision = decide_duplicate_suppression(
            self._card(trigger_zone_bucket="spy_breakout_zone"), first
        )

        self.assertIn("trigger_zone_changed", decision["material_change_flags"])

    def test_invalidation_bucket_change_breaks_suppression(self):
        first = decide_duplicate_suppression(self._card())
        decision = decide_duplicate_suppression(
            self._card(invalidation_bucket="below_prior_low"), first
        )

        self.assertIn("invalidation_changed", decision["material_change_flags"])

    def test_evidence_quality_change_breaks_suppression(self):
        first = decide_duplicate_suppression(self._card())
        decision = decide_duplicate_suppression(
            self._card(evidence_quality="deterministic"), first
        )

        self.assertIn("evidence_quality_changed", decision["material_change_flags"])

    def test_session_boundary_change_breaks_suppression(self):
        first = decide_duplicate_suppression(self._card())
        decision = decide_duplicate_suppression(
            self._card(regular_session_date="2026-05-25"), first
        )

        self.assertIn("session_boundary_changed", decision["material_change_flags"])

    def test_best_candidate_change_breaks_suppression(self):
        first = decide_duplicate_suppression(self._card())
        decision = decide_duplicate_suppression(
            self._card(best_candidate_id="SPY-Ideal-2"), first
        )

        self.assertIn("best_candidate_changed", decision["material_change_flags"])

    def test_trigger_path_change_breaks_suppression(self):
        first = decide_duplicate_suppression(self._card())
        decision = decide_duplicate_suppression(
            self._card(trigger_path_identifier="completed_break"), first
        )

        self.assertIn("trigger_path_changed", decision["material_change_flags"])

    def test_critical_field_became_available_breaks_suppression(self):
        first = decide_duplicate_suppression(self._card())
        decision = decide_duplicate_suppression(self._card(unavailable_fields=[]), first)

        self.assertIn("critical_field_became_available", decision["material_change_flags"])

    def test_critical_field_became_unavailable_breaks_suppression(self):
        first = decide_duplicate_suppression(self._card(unavailable_fields=[]))
        decision = decide_duplicate_suppression(
            self._card(unavailable_fields=[TRIGGER_LEVEL_UNCONFIRMED]), first
        )

        self.assertIn("critical_field_became_unavailable", decision["material_change_flags"])

    def test_news_unconfirmed_same_state_repeat_can_suppress(self):
        first = decide_duplicate_suppression(
            self._card(headline_news_status=NEWS_UNCONFIRMED)
        )
        repeat = decide_duplicate_suppression(
            self._card(headline_news_status=NEWS_UNCONFIRMED), first
        )

        self.assertEqual(repeat["alert_decision"], "suppress_duplicate")
        self.assertEqual(repeat["headline_news_status"], NEWS_UNCONFIRMED)

    def test_source_confirmed_news_caution_or_block_change_breaks_suppression(self):
        first = decide_duplicate_suppression(self._card())
        caution = decide_duplicate_suppression(
            self._card(
                headline_news_status="NEWS_CAUTION",
                headline_news_source_confirmed=True,
            ),
            first,
        )
        block = decide_duplicate_suppression(
            self._card(
                headline_news_status="NEWS_BLOCK",
                headline_news_source_confirmed=True,
            ),
            caution,
        )

        self.assertIn(
            "source_confirmed_headline_news_status_changed",
            caution["material_change_flags"],
        )
        self.assertIn(
            "source_confirmed_headline_news_status_changed",
            block["material_change_flags"],
        )

    def test_stale_spent_same_state_no_fresh_trigger_repeat_can_suppress(self):
        stale = self._card(
            stage="stale/spent/no-fresh-trigger",
            trigger_status="stale",
            fresh_stale_spent_state="stale",
            fresh_trigger_path_present=False,
        )
        first = decide_duplicate_suppression(stale)
        repeat = decide_duplicate_suppression(stale, first)

        self.assertEqual(repeat["alert_decision"], "suppress_duplicate")

    def test_fresh_trigger_path_after_stale_spent_breaks_suppression(self):
        stale = self._card(
            stage="stale/spent/no-fresh-trigger",
            trigger_status="stale",
            fresh_stale_spent_state="stale",
            fresh_trigger_path_present=False,
        )
        first = decide_duplicate_suppression(stale)
        decision = decide_duplicate_suppression(
            self._card(
                stage="rebuilding",
                trigger_status="waiting_for_trigger",
                fresh_stale_spent_state="rebuilding",
                fresh_trigger_path_present=True,
                trigger_path_identifier="fresh_current_session_rebuild",
            ),
            first,
        )

        self.assertIn("trigger_path_changed", decision["material_change_flags"])
        self.assertEqual(decision["alert_decision"], "emit_material_change")

    def test_watch_only_false_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "watch_only=True"):
            decide_duplicate_suppression(self._card(watch_only=False))

    def test_forbidden_execution_account_order_fields_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "order_id"):
            decide_duplicate_suppression(self._card(order_id="abc"))

        with self.assertRaisesRegex(ValueError, "account_id"):
            decide_duplicate_suppression(self._card(nested={"account_id": "abc"}))

    def test_input_is_not_mutated(self):
        card = self._card()
        before = copy.deepcopy(card)

        decision = decide_duplicate_suppression(card)
        decision["material_review_fields"]["critical_unavailable_fields"].append("changed")

        self.assertEqual(card, before)

    def test_headline_news_status_defaults_when_unavailable(self):
        card = self._card()
        card.pop("headline_news_status")

        decision = decide_duplicate_suppression(card)

        self.assertEqual(decision["headline_news_status"], NEWS_UNCONFIRMED)

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
