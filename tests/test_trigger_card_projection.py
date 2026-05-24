import copy
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
from watcher_foundation.models import WatchOnlyCandidateState
from watcher_foundation.state_tracker import WatcherTrackedState
from watcher_foundation.trigger_card import (
    REQUIRED_TRIGGER_CARD_FIELDS,
    project_trigger_card,
)


class TriggerCardProjectionTests(unittest.TestCase):
    def test_projection_returns_all_required_trigger_card_fields(self):
        card = project_trigger_card(WatcherTrackedState(symbol="SPY"))

        self.assertTrue(set(REQUIRED_TRIGGER_CARD_FIELDS).issubset(card))

    def test_projection_preserves_watch_only_true(self):
        card = project_trigger_card({"symbol": "SPY", "watch_only": True})

        self.assertIs(card["watch_only"], True)

    def test_projection_defaults_headline_news_status_to_news_unconfirmed(self):
        card = project_trigger_card({"symbol": "SPY", "watch_only": True})

        self.assertEqual(card["headline_news_status"], NEWS_UNCONFIRMED)

    def test_projection_preserves_unavailable_markers(self):
        state = WatcherTrackedState(
            unavailable_fields=(
                TRIGGER_LEVEL_UNCONFIRMED,
                DISTANCE_TO_TRIGGER_UNCONFIRMED,
                INVALIDATION_UNCONFIRMED,
                SOURCE_AS_OF_UNCONFIRMED,
            )
        )

        card = project_trigger_card(state)

        self.assertEqual(card["trigger_level_or_zone"], TRIGGER_LEVEL_UNCONFIRMED)
        self.assertEqual(card["distance_to_trigger"], DISTANCE_TO_TRIGGER_UNCONFIRMED)
        self.assertEqual(
            card["invalidation_level_or_condition"], INVALIDATION_UNCONFIRMED
        )
        self.assertEqual(card["source_as_of"], SOURCE_AS_OF_UNCONFIRMED)
        self.assertEqual(card["evidence_rows"], [EVIDENCE_ROWS_UNCONFIRMED])
        self.assertIn(TRIGGER_LEVEL_UNCONFIRMED, card["unavailable_fields"])

    def test_projection_preserves_blockers_cautions_and_no_trade_reason(self):
        source = {
            "symbol": "QQQ",
            "watch_only": True,
            "blockers": [{"severity": "block", "reason_code": "missing_trigger"}],
            "cautions": [{"severity": "caution", "reason_code": "news_unconfirmed"}],
            "no_trade_reason": "blocked_no_trade_until_trigger_is_confirmed",
        }

        card = project_trigger_card(source)

        self.assertEqual(card["blockers"], source["blockers"])
        self.assertEqual(card["cautions"], source["cautions"])
        self.assertIn(source["no_trade_reason"], card["no_trade_reason"])

    def test_projection_preserves_stale_spent_no_fresh_trigger_no_trade_wording(self):
        card = project_trigger_card(
            {
                "symbol": "IWM",
                "watch_only": True,
                "stage": "stale/spent/no-fresh-trigger",
                "trigger_status": "stale",
                "fresh_stale_spent_state": "stale",
                "no_trade_reason": "stale_context",
            }
        )

        self.assertIn("no fresh trigger", card["no_trade_reason"])
        self.assertIn("no-trade", card["no_trade_reason"])

    def test_triggered_signal_stage_remains_shadow_only(self):
        card = project_trigger_card(
            {
                "symbol": "SPY",
                "watch_only": True,
                "stage": "triggered_signal_stage",
                "trigger_status": "triggered",
                "no_trade_reason": "triggered_for_review",
            }
        )

        self.assertIn("shadow_signal_review_only", card["no_trade_reason"])
        self.assertIn("no_live_trade_approval", card["no_trade_reason"])

    def test_projection_includes_duplicate_suppression_key_fields(self):
        card = project_trigger_card(
            WatcherTrackedState(
                symbol="SPY",
                setup_type="Ideal",
                direction="bullish/call-side",
                trigger_zone_bucket="reclaim_zone",
                invalidation_bucket="below_reclaim",
            )
        )

        key_fields = card["duplicate_suppression_key_fields"]
        self.assertEqual(key_fields["symbol"], "SPY")
        self.assertEqual(key_fields["setup_family"], "Ideal")
        self.assertEqual(key_fields["trigger_zone_bucket"], "reclaim_zone")
        self.assertEqual(key_fields["invalidation_bucket"], "below_reclaim")

    def test_projection_includes_best_candidate_ranking_inputs(self):
        card = project_trigger_card(
            {
                "candidate_id": "GLD-Continuation-1",
                "symbol": "GLD",
                "watch_only": True,
                "stage": "near-trigger",
                "fresh_stale_spent_state": "fresh",
                "distance_to_trigger": "near",
                "evidence_quality": "partial",
            }
        )

        ranking = card["best_candidate_ranking_inputs"]
        self.assertEqual(ranking["eligibility_stage"], "near-trigger")
        self.assertEqual(ranking["freshness"], "fresh")
        self.assertEqual(ranking["trigger_proximity"], "near")
        self.assertEqual(ranking["deterministic_tie_breaker"], "GLD-Continuation-1")

    def test_projection_rejects_forbidden_execution_account_order_fields(self):
        with self.assertRaisesRegex(ValueError, "order_id"):
            project_trigger_card({"symbol": "SPY", "watch_only": True, "order_id": "1"})

        with self.assertRaisesRegex(ValueError, "account_id"):
            project_trigger_card(
                {"symbol": "SPY", "watch_only": True, "nested": {"account_id": "1"}}
            )

    def test_projection_does_not_mutate_input_state(self):
        source = {
            "symbol": "SPY",
            "watch_only": True,
            "blockers": [{"reason_code": "missing_trigger"}],
            "unavailable_fields": [TRIGGER_LEVEL_UNCONFIRMED],
        }
        before = copy.deepcopy(source)

        card = project_trigger_card(source)
        card["blockers"][0]["reason_code"] = "changed"

        self.assertEqual(source, before)

    def test_candidate_state_projection_uses_scaffold_field_names(self):
        candidate = WatchOnlyCandidateState(
            symbol="SPY",
            trigger_level="SPY 530 reclaim zone",
            invalidation="fail below 528",
        )

        card = project_trigger_card(candidate)

        self.assertEqual(card["trigger_level_or_zone"], "SPY 530 reclaim zone")
        self.assertEqual(card["invalidation_level_or_condition"], "fail below 528")

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
