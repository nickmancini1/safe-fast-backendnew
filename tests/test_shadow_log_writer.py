import io
import json
import subprocess
import unittest

from watcher_foundation.constants import (
    DISTANCE_TO_TRIGGER_UNCONFIRMED,
    NEWS_UNCONFIRMED,
    SOURCE_AS_OF_UNCONFIRMED,
    TRIGGER_LEVEL_UNCONFIRMED,
)
from watcher_foundation.shadow_log import (
    ALLOWED_SHADOW_LOG_EVENT_TYPES,
    DEFAULT_REVIEW_LABEL,
    REQUIRED_SHADOW_LOG_FIELDS,
    append_shadow_log_line,
    create_shadow_log_record,
    serialize_shadow_log_line,
)
from watcher_foundation.state_tracker import WatcherTrackedState
from watcher_foundation.trigger_card import project_trigger_card


class ShadowLogWriterTests(unittest.TestCase):
    def _state_snapshot(self):
        return WatcherTrackedState(
            candidate_id="SPY-Ideal-1",
            symbol="SPY",
            watch_session_id="session-1",
            setup_type="Ideal",
            direction="bullish/call-side",
            state_version=3,
            unavailable_fields=(
                TRIGGER_LEVEL_UNCONFIRMED,
                DISTANCE_TO_TRIGGER_UNCONFIRMED,
            ),
            headline_news_status=NEWS_UNCONFIRMED,
        ).to_dict()

    def test_shadow_log_record_includes_all_required_fields(self):
        record = create_shadow_log_record(
            {
                "log_record_id": "record-1",
                "event_type": "state_observation",
                "event_at": "2026-05-24T09:31:00-04:00",
                "state_snapshot": self._state_snapshot(),
            }
        )

        self.assertTrue(set(REQUIRED_SHADOW_LOG_FIELDS).issubset(record))

    def test_allowed_event_types_include_schema_review_values(self):
        self.assertEqual(
            set(ALLOWED_SHADOW_LOG_EVENT_TYPES),
            {
                "state_observation",
                "lifecycle_transition",
                "trigger_card_snapshot",
                "alert_decision",
                "suppressed_duplicate",
                "blocker_caution_change",
                "unavailable_field_change",
                "evidence_quality_change",
                "best_candidate_snapshot",
                "manual_review_label",
                "shadow_review_summary",
            },
        )

    def test_default_review_label_is_unreviewed(self):
        record = create_shadow_log_record({"state_snapshot": self._state_snapshot()})

        self.assertEqual(record["review_label"], DEFAULT_REVIEW_LABEL)
        self.assertEqual(record["review_label"], "UNREVIEWED")

    def test_record_preserves_watch_only_true(self):
        record = create_shadow_log_record({"state_snapshot": self._state_snapshot()})

        self.assertIs(record["watch_only"], True)
        self.assertIs(record["state_snapshot"]["watch_only"], True)

    def test_record_rejects_watch_only_false(self):
        with self.assertRaisesRegex(ValueError, "watch_only=True"):
            create_shadow_log_record({"watch_only": False})

        with self.assertRaisesRegex(ValueError, "watch_only=True"):
            create_shadow_log_record(
                {"state_snapshot": {"symbol": "SPY", "watch_only": False}}
            )

    def test_record_rejects_forbidden_execution_account_order_fields(self):
        with self.assertRaisesRegex(ValueError, "order_id"):
            create_shadow_log_record({"order_id": "abc"})

        with self.assertRaisesRegex(ValueError, "account_id"):
            create_shadow_log_record(
                {"state_snapshot": {"symbol": "SPY", "account_id": "abc"}}
            )

    def test_record_preserves_unavailable_fields(self):
        state_snapshot = self._state_snapshot()

        record = create_shadow_log_record({"state_snapshot": state_snapshot})

        self.assertEqual(
            record["unavailable_fields"],
            [TRIGGER_LEVEL_UNCONFIRMED, DISTANCE_TO_TRIGGER_UNCONFIRMED],
        )
        self.assertEqual(
            record["state_snapshot"]["unavailable_fields"],
            [TRIGGER_LEVEL_UNCONFIRMED, DISTANCE_TO_TRIGGER_UNCONFIRMED],
        )

    def test_record_preserves_news_unconfirmed(self):
        record = create_shadow_log_record({"state_snapshot": self._state_snapshot()})

        self.assertEqual(
            record["state_snapshot"]["headline_news_status"], NEWS_UNCONFIRMED
        )

    def test_record_preserves_state_snapshot(self):
        state_snapshot = self._state_snapshot()

        record = create_shadow_log_record({"state_snapshot": state_snapshot})

        self.assertEqual(record["state_snapshot"], state_snapshot)
        self.assertEqual(record["candidate_id"], "SPY-Ideal-1")
        self.assertEqual(record["state_version"], 3)

    def test_record_preserves_trigger_card_snapshot(self):
        state_snapshot = self._state_snapshot()
        trigger_card_snapshot = project_trigger_card(state_snapshot)

        record = create_shadow_log_record(
            {
                "event_type": "trigger_card_snapshot",
                "state_snapshot": state_snapshot,
                "trigger_card_snapshot": trigger_card_snapshot,
            }
        )

        self.assertEqual(record["trigger_card_snapshot"], trigger_card_snapshot)
        self.assertEqual(
            record["trigger_card_snapshot"]["headline_news_status"], NEWS_UNCONFIRMED
        )

    def test_record_preserves_source_as_of_marker(self):
        record = create_shadow_log_record({"state_snapshot": self._state_snapshot()})

        self.assertEqual(record["source_as_of"], SOURCE_AS_OF_UNCONFIRMED)

    def test_jsonl_serialization_returns_one_valid_json_line(self):
        record = create_shadow_log_record({"state_snapshot": self._state_snapshot()})

        line = serialize_shadow_log_line(record)

        self.assertTrue(line.endswith("\n"))
        self.assertEqual(line.count("\n"), 1)
        parsed = json.loads(line)
        self.assertEqual(parsed["event_type"], "state_observation")

    def test_append_helper_appends_without_overwriting_prior_lines(self):
        buffer = io.StringIO()
        append_shadow_log_line(
            buffer,
            create_shadow_log_record(
                {
                    "log_record_id": "record-1",
                    "state_snapshot": self._state_snapshot(),
                }
            ),
        )
        append_shadow_log_line(
            buffer,
            create_shadow_log_record(
                {
                    "log_record_id": "record-2",
                    "state_snapshot": self._state_snapshot(),
                }
            ),
        )

        lines = buffer.getvalue().splitlines()
        self.assertEqual(len(lines), 2)
        self.assertEqual(json.loads(lines[0])["log_record_id"], "record-1")
        self.assertEqual(json.loads(lines[1])["log_record_id"], "record-2")

    def test_triggered_signal_stage_remains_shadow_only(self):
        state_snapshot = self._state_snapshot()
        state_snapshot["stage"] = "triggered_signal_stage"
        state_snapshot["no_trade_reason"] = (
            "triggered_for_review; shadow_signal_review_only; no_live_trade_approval"
        )

        record = create_shadow_log_record({"state_snapshot": state_snapshot})

        self.assertEqual(record["state_snapshot"]["stage"], "triggered_signal_stage")
        self.assertIn("shadow_signal_review_only", record["state_snapshot"]["no_trade_reason"])
        self.assertIn("no_live_trade_approval", record["state_snapshot"]["no_trade_reason"])

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
