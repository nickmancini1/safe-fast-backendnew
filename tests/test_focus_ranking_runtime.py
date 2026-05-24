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
from watcher_foundation.focus_ranking import rank_focus_candidates


class FocusRankingRuntimeTests(unittest.TestCase):
    def _candidate(self, candidate_id, **overrides):
        candidate = {
            "candidate_id": candidate_id,
            "symbol": "SPY",
            "setup_type": "Ideal",
            "direction": "bullish/call-side",
            "stage": "near-trigger",
            "trigger_status": "near_trigger",
            "fresh_stale_spent_state": "fresh",
            "trigger_level_or_zone": "accepted trigger zone",
            "distance_to_trigger": "medium",
            "invalidation_level_or_condition": "accepted invalidation",
            "source_as_of": "2026-05-24T09:35:00-04:00",
            "regular_session_date": "2026-05-24",
            "evidence_rows": ["row-1"],
            "evidence_quality": "deterministic",
            "unavailable_fields": [],
            "blockers": [],
            "cautions": [],
            "headline_news_status": NEWS_UNCONFIRMED,
            "watch_only": True,
        }
        candidate.update(overrides)
        return candidate

    def test_cleaner_current_candidate_outranks_closer_blocked_candidate(self):
        result = rank_focus_candidates(
            [
                self._candidate("clean", distance_to_trigger="medium"),
                self._candidate(
                    "blocked",
                    distance_to_trigger="near",
                    stage="blocked/no-trade",
                    blockers=[{"reason_code": "accepted_blocker", "severity": "block"}],
                ),
            ]
        )

        self.assertEqual(result["primary_focus_candidate_id"], "clean")
        self.assertEqual(
            self._by_id(result, "blocked")["focus_rank_bucket"], "watch_only_blocked"
        )

    def test_cleaner_current_candidate_outranks_stale_spent_candidate(self):
        result = rank_focus_candidates(
            [
                self._candidate("clean"),
                self._candidate(
                    "stale",
                    distance_to_trigger="near",
                    stage="stale/spent/no-fresh-trigger",
                    trigger_status="stale",
                    fresh_stale_spent_state="stale",
                ),
            ]
        )

        self.assertEqual(result["primary_focus_candidate_id"], "clean")
        self.assertEqual(
            self._by_id(result, "stale")["focus_rank_bucket"], "stale_spent_context"
        )

    def test_cleaner_current_candidate_outranks_evidence_poor_candidate(self):
        result = rank_focus_candidates(
            [
                self._candidate("clean", distance_to_trigger="medium"),
                self._candidate(
                    "evidence-poor",
                    distance_to_trigger="near",
                    evidence_quality="missing",
                ),
            ]
        )

        self.assertEqual(result["primary_focus_candidate_id"], "clean")
        self.assertEqual(
            self._by_id(result, "evidence-poor")["focus_rank_bucket"],
            "unavailable_unconfirmed",
        )

    def test_unavailable_proximity_does_not_improve_rank(self):
        result = rank_focus_candidates(
            [
                self._candidate("available", distance_to_trigger="far"),
                self._candidate(
                    "unavailable",
                    distance_to_trigger=DISTANCE_TO_TRIGGER_UNCONFIRMED,
                    unavailable_fields=[DISTANCE_TO_TRIGGER_UNCONFIRMED],
                ),
            ]
        )

        self.assertEqual(result["primary_focus_candidate_id"], "available")
        self.assertEqual(
            self._by_id(result, "unavailable")["focus_rank_bucket"],
            "unavailable_unconfirmed",
        )

    def test_news_unconfirmed_does_not_create_blocker_by_itself(self):
        result = rank_focus_candidates(
            [self._candidate("news-unconfirmed", headline_news_status=NEWS_UNCONFIRMED)]
        )

        self.assertEqual(result["primary_focus_candidate_id"], "news-unconfirmed")
        self.assertEqual(
            result["ranked_candidates"][0]["focus_rank_bucket"], "primary_focus"
        )

    def test_source_confirmed_news_block_demotes_to_blocked(self):
        result = rank_focus_candidates(
            [
                self._candidate("clean"),
                self._candidate(
                    "news-blocked",
                    headline_news_status="NEWS_BLOCK",
                    headline_news_source_confirmed=True,
                    distance_to_trigger="near",
                ),
            ]
        )

        self.assertEqual(result["primary_focus_candidate_id"], "clean")
        self.assertEqual(
            self._by_id(result, "news-blocked")["focus_rank_bucket"],
            "watch_only_blocked",
        )

    def test_no_setup_family_automatically_wins_by_name(self):
        result = rank_focus_candidates(
            [
                self._candidate(
                    "continuation-clean",
                    setup_type="Continuation",
                    distance_to_trigger="medium",
                ),
                self._candidate(
                    "ideal-blocked",
                    setup_type="Ideal",
                    distance_to_trigger="near",
                    blockers=[{"reason_code": "accepted_blocker", "severity": "block"}],
                ),
            ]
        )

        self.assertEqual(result["primary_focus_candidate_id"], "continuation-clean")

    def test_deterministic_tie_breaker_is_stable(self):
        first = rank_focus_candidates(
            [
                self._candidate("B-candidate", setup_type="Continuation"),
                self._candidate("A-candidate", setup_type="Clean Fast Break"),
            ]
        )
        second = rank_focus_candidates(
            [
                self._candidate("A-candidate", setup_type="Clean Fast Break"),
                self._candidate("B-candidate", setup_type="Continuation"),
            ]
        )

        self.assertEqual(first["primary_focus_candidate_id"], "A-candidate")
        self.assertEqual(second["primary_focus_candidate_id"], "A-candidate")

    def test_exactly_one_primary_focus_when_eligible_candidates_exist(self):
        result = rank_focus_candidates(
            [self._candidate("one"), self._candidate("two", distance_to_trigger="far")]
        )

        primary_count = sum(
            1
            for candidate in result["ranked_candidates"]
            if candidate["focus_rank_bucket"] == "primary_focus"
        )
        self.assertEqual(primary_count, 1)

    def test_blocked_candidates_go_to_watch_only_blocked(self):
        result = rank_focus_candidates(
            [
                self._candidate(
                    "blocked",
                    blockers=[{"reason_code": "accepted_blocker", "severity": "block"}],
                )
            ]
        )

        self.assertIsNone(result["primary_focus_candidate_id"])
        self.assertEqual(
            result["ranked_candidates"][0]["focus_rank_bucket"], "watch_only_blocked"
        )

    def test_stale_spent_candidates_go_to_stale_spent_context(self):
        result = rank_focus_candidates(
            [
                self._candidate(
                    "spent",
                    stage="stale/spent/no-fresh-trigger",
                    trigger_status="spent",
                    fresh_stale_spent_state="spent",
                )
            ]
        )

        self.assertIsNone(result["primary_focus_candidate_id"])
        self.assertEqual(
            result["ranked_candidates"][0]["focus_rank_bucket"], "stale_spent_context"
        )

    def test_critical_unavailable_candidates_go_to_unavailable_unconfirmed(self):
        result = rank_focus_candidates(
            [
                self._candidate(
                    "unavailable",
                    trigger_level_or_zone=TRIGGER_LEVEL_UNCONFIRMED,
                    invalidation_level_or_condition=INVALIDATION_UNCONFIRMED,
                    source_as_of=SOURCE_AS_OF_UNCONFIRMED,
                    evidence_rows=[EVIDENCE_ROWS_UNCONFIRMED],
                    unavailable_fields=[
                        TRIGGER_LEVEL_UNCONFIRMED,
                        INVALIDATION_UNCONFIRMED,
                        SOURCE_AS_OF_UNCONFIRMED,
                    ],
                )
            ]
        )

        self.assertIsNone(result["primary_focus_candidate_id"])
        self.assertEqual(
            result["ranked_candidates"][0]["focus_rank_bucket"],
            "unavailable_unconfirmed",
        )

    def test_best_candidate_changed_true_when_previous_primary_differs(self):
        result = rank_focus_candidates(
            [self._candidate("current")],
            previous_primary_focus_candidate_id="previous",
        )

        self.assertIs(result["best_candidate_changed"], True)

    def test_best_candidate_changed_false_when_previous_primary_matches(self):
        result = rank_focus_candidates(
            [self._candidate("current")],
            previous_primary_focus_candidate_id="current",
        )

        self.assertIs(result["best_candidate_changed"], False)

    def test_watch_only_false_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "watch_only=True"):
            rank_focus_candidates([self._candidate("unsafe", watch_only=False)])

    def test_forbidden_execution_account_order_fields_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "order_id"):
            rank_focus_candidates([self._candidate("unsafe", order_id="abc")])

        with self.assertRaisesRegex(ValueError, "account_id"):
            rank_focus_candidates(
                [self._candidate("unsafe", nested={"account_id": "abc"})]
            )

    def test_input_candidates_are_not_mutated(self):
        candidates = [
            self._candidate(
                "candidate",
                blockers=[{"reason_code": "none", "severity": "none"}],
            )
        ]
        before = copy.deepcopy(candidates)

        result = rank_focus_candidates(candidates)
        result["ranked_candidates"][0]["blockers"][0]["reason_code"] = "changed"

        self.assertEqual(candidates, before)

    def test_main_py_has_no_change(self):
        result = subprocess.run(
            ["git", "diff", "--quiet", "--", "main.py"],
            check=False,
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def _by_id(self, result, candidate_id):
        for candidate in result["ranked_candidates"]:
            if candidate["candidate_id"] == candidate_id:
                return candidate
        self.fail(f"candidate not found: {candidate_id}")


if __name__ == "__main__":
    unittest.main()
