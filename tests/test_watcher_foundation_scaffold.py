import subprocess
import unittest

from watcher_foundation.constants import (
    ACCEPTED_HEADLINE_NEWS_STATUSES,
    ACCEPTED_SETUP_TYPES,
    ACCEPTED_STAGES,
    ACCEPTED_TRIGGER_STATUSES,
    DISTANCE_TO_TRIGGER_UNCONFIRMED,
    EVIDENCE_ROWS_UNCONFIRMED,
    EXPLICIT_UNCONFIRMED_MARKERS,
    FRESHNESS_UNCONFIRMED,
    INVALIDATION_UNCONFIRMED,
    NEWS_UNCONFIRMED,
    SOURCE_AS_OF_UNCONFIRMED,
    TRIGGER_LEVEL_UNCONFIRMED,
)
from watcher_foundation.models import (
    WatchOnlyCandidateState,
    reject_forbidden_execution_fields,
)


class WatcherFoundationScaffoldTests(unittest.TestCase):
    def test_default_state_is_watch_only(self):
        state = WatchOnlyCandidateState()

        self.assertIs(state.watch_only, True)
        self.assertIs(state.to_dict()["watch_only"], True)

    def test_default_headline_news_status_is_news_unconfirmed(self):
        state = WatchOnlyCandidateState()

        self.assertEqual(state.headline_news_status, NEWS_UNCONFIRMED)
        self.assertEqual(state.to_dict()["headline_news_status"], NEWS_UNCONFIRMED)

    def test_unavailable_markers_are_preserved_in_dict_output(self):
        output = WatchOnlyCandidateState().to_dict()

        self.assertEqual(output["trigger_level"], TRIGGER_LEVEL_UNCONFIRMED)
        self.assertEqual(
            output["distance_to_trigger"], DISTANCE_TO_TRIGGER_UNCONFIRMED
        )
        self.assertEqual(output["invalidation"], INVALIDATION_UNCONFIRMED)
        self.assertEqual(output["source_as_of"], SOURCE_AS_OF_UNCONFIRMED)
        self.assertEqual(output["evidence_rows"], [EVIDENCE_ROWS_UNCONFIRMED])
        self.assertEqual(output["freshness_state"], FRESHNESS_UNCONFIRMED)
        self.assertTrue(
            set(EXPLICIT_UNCONFIRMED_MARKERS).issubset(output["unavailable_fields"])
        )

    def test_accepted_enum_status_constants_include_required_values(self):
        self.assertEqual(
            set(ACCEPTED_SETUP_TYPES),
            {
                "Ideal",
                "Clean Fast Break",
                "Continuation",
                "UNCONFIRMED",
            },
        )
        self.assertEqual(
            set(ACCEPTED_STAGES),
            {
                "forming/developing",
                "near-trigger",
                "pending_completed_candle_approval",
                "triggered_signal_stage",
                "blocked/no-trade",
                "stale/spent/no-fresh-trigger",
                "rebuilding",
                "unavailable/unconfirmed",
            },
        )
        self.assertEqual(
            set(ACCEPTED_TRIGGER_STATUSES),
            {
                "no_valid_trigger",
                "waiting_for_trigger",
                "near_trigger",
                "pending_completed_candle",
                "triggered",
                "failed_hold",
                "stale",
                "spent",
                "unconfirmed",
            },
        )
        self.assertEqual(
            set(ACCEPTED_HEADLINE_NEWS_STATUSES),
            {
                "NEWS_CLEAR",
                "NEWS_CAUTION",
                "NEWS_BLOCK",
                "NEWS_UNCONFIRMED",
            },
        )

    def test_forbidden_execution_fields_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "order_id"):
            reject_forbidden_execution_fields(
                {"candidate_id": "x", "order_id": "123"}
            )

        with self.assertRaisesRegex(ValueError, "account_id"):
            reject_forbidden_execution_fields({"nested": {"account_id": "abc"}})

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
