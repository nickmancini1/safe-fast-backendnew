import copy
import unittest
from unittest.mock import patch

from watcher_foundation import (
    DAY60_SHADOW_CONTRACT_DIAGNOSTIC_PLACEHOLDER_FIELDS,
    DAY60_SHADOW_SESSION_RESULT_FIELDS,
    run_day60_shadow_session_dry_run,
)


class Day60ShadowSessionTests(unittest.TestCase):
    def _diagnostics_placeholders(self):
        return {
            field_name: {
                "status": "placeholder_only_future_diagnostic_category",
                "placeholder_preserved": True,
            }
            for field_name in DAY60_SHADOW_CONTRACT_DIAGNOSTIC_PLACEHOLDER_FIELDS
        }

    def _trigger_card(self):
        return {
            "symbol": "SPY",
            "setup_type": "Ideal",
            "direction": "bullish/call-side",
            "stage": "near-trigger",
            "trigger_status": "near_trigger",
            "trigger_level_or_zone": "432 reclaim zone",
            "confirmation_timeframe_rule": "completed 1h hold",
            "distance_to_trigger": "near",
            "invalidation_level_or_condition": "below local shelf",
            "fresh_stale_spent_state": "fresh",
            "next_check_or_next_alert_condition": "new_material_change_required",
            "blockers": [],
            "cautions": [],
            "unavailable_fields": ["headline_news_status"],
            "source_as_of": "2026-05-24T09:35:00-04:00",
            "evidence_rows": ["fixture-row-1"],
            "headline_news_status": "NEWS_UNCONFIRMED",
            "diagnostic_reason_codes": [],
            "no_trade_reason": "watch_only_shadow_review_no_live_trade_approval",
            "duplicate_suppression_key_fields": {
                "symbol": "SPY",
                "setup_family": "Ideal",
                "direction": "bullish/call-side",
                "stage": "near-trigger",
                "trigger_status": "near_trigger",
                "freshness_state": "fresh",
                "primary_blocker": "UNCONFIRMED",
                "trigger_zone_bucket": "432-zone",
                "invalidation_bucket": "local-shelf",
            },
            "best_candidate_ranking_inputs": {
                "eligibility_stage": "near-trigger",
                "freshness": "fresh",
                "setup_type": "Ideal",
                "trigger_proximity": "near",
                "blocker_count": 0,
                "caution_count": 0,
                "headline_news_status": "NEWS_UNCONFIRMED",
                "evidence_quality": "deterministic",
                "deterministic_tie_breaker": "SPY-day60",
            },
            "watch_only": True,
        }

    def _row(self, **overrides):
        row = {
            "row_id": "day60-row-1",
            "watch_session_id": "day60-session",
            "symbol": "SPY",
            "timestamp": "2026-05-24T09:35:00-04:00",
            "timeframe": "1h_rth",
            "setup_type": "Ideal",
            "direction": "bullish/call-side",
            "stage": "near-trigger",
            "trigger_status": "near_trigger",
            "trigger_card": self._trigger_card(),
            "provenance": {
                "input_source": "caller_provided_in_memory",
                "caller_provided": True,
                "live_data_fetch": False,
                "data_created_by_validator": False,
            },
            "diagnostics_placeholders": self._diagnostics_placeholders(),
            "unavailable_fields": [
                {
                    "field_name": "headline_news_status",
                    "status": "unconfirmed",
                    "reason": "future diagnostic category preserved",
                    "fabricated": False,
                }
            ],
            "evidence_refs": ["fixture-row-1"],
            "no_hindsight_boundary": {
                "evidence_frozen_before_review": True,
                "future_rows_not_used_for_candidate": True,
                "no_backfilled_trigger_labels": True,
            },
            "no_trade_boundary": {
                "no_trade": True,
                "no_broker": True,
                "no_order": True,
                "no_live_decision": True,
                "no_trade_decision": True,
                "no_option_pnl": True,
                "no_account_sizing": True,
                "live_decision_allowed": False,
            },
            "watch_only": True,
        }
        row.update(overrides)
        return row

    def test_valid_caller_provided_rows_produce_accepted_dry_run_summary(self):
        result = run_day60_shadow_session_dry_run(
            [self._row(), self._row(row_id="day60-row-2")]
        )

        self.assertEqual(set(DAY60_SHADOW_SESSION_RESULT_FIELDS), set(result))
        self.assertEqual(result["rows_processed"], 2)
        self.assertEqual(result["rows_accepted"], 2)
        self.assertEqual(result["rows_rejected"], 0)
        self.assertEqual(
            [row["row_id"] for row in result["accepted_rows"]],
            ["day60-row-1", "day60-row-2"],
        )
        self.assertEqual(result["rejected_rows"], [])

    def test_invalid_row_is_rejected_with_reason(self):
        result = run_day60_shadow_session_dry_run(
            [self._row(row_id="bad-row", watch_only=False)]
        )

        self.assertEqual(result["rows_accepted"], 0)
        self.assertEqual(result["rows_rejected"], 1)
        self.assertEqual(result["rejected_rows"][0]["row_id"], "bad-row")
        self.assertIn("watch_only=True", result["rejected_rows"][0]["reason"])

    def test_mixed_valid_invalid_rows_preserve_accepted_rows_and_rejected_reasons(self):
        result = run_day60_shadow_session_dry_run(
            [self._row(), self._row(row_id="bad-row", watch_only=False), "bad"]
        )

        self.assertEqual(result["rows_processed"], 3)
        self.assertEqual(result["rows_accepted"], 1)
        self.assertEqual(result["rows_rejected"], 2)
        self.assertEqual(result["accepted_rows"][0]["row_id"], "day60-row-1")
        self.assertIn("watch_only=True", result["rejected_rows"][0]["reason"])
        self.assertIn("must be a dict", result["rejected_rows"][1]["reason"])

    def test_session_metadata_is_copied_defensively(self):
        metadata = {
            "session_id": "session-1",
            "review": {"owner": "local-only"},
        }
        result = run_day60_shadow_session_dry_run(
            [self._row()],
            session_metadata=metadata,
        )

        result["session_metadata"]["review"]["owner"] = "changed"

        self.assertEqual(metadata["review"]["owner"], "local-only")

    def test_accepted_rows_are_copied_defensively(self):
        row = self._row()
        original = copy.deepcopy(row)
        result = run_day60_shadow_session_dry_run([row])

        result["accepted_rows"][0]["trigger_card"]["blockers"].append("changed")
        result["accepted_rows"][0]["unavailable_fields"][0]["reason"] = "changed"

        self.assertEqual(row, original)
        self.assertEqual(row["trigger_card"]["blockers"], [])
        self.assertEqual(
            row["unavailable_fields"][0]["reason"],
            "future diagnostic category preserved",
        )

    def test_input_rows_must_be_a_list(self):
        with self.assertRaisesRegex(TypeError, "rows must be a list"):
            run_day60_shadow_session_dry_run((self._row(),))

    def test_forbidden_broker_order_account_options_pnl_trade_decision_fields_are_rejected(self):
        forbidden_cases = (
            {"nested": {"broker": "blocked"}},
            {"nested": {"order_id": "blocked"}},
            {"nested": {"account": {"id": "blocked"}}},
            {"nested": {"option_pnl": 1.23}},
            {"nested": {"p&l": 1.23}},
            {"nested": {"trade_decision": "approve"}},
        )

        for forbidden in forbidden_cases:
            with self.subTest(forbidden=forbidden):
                row = self._row(row_id="bad-row")
                row.update(forbidden)

                result = run_day60_shadow_session_dry_run([row])

                self.assertEqual(result["rows_accepted"], 0)
                self.assertEqual(result["rows_rejected"], 1)
                self.assertIn(
                    "Forbidden execution/trade field",
                    result["rejected_rows"][0]["reason"],
                )

    def test_dry_run_result_preserves_no_go_flags(self):
        result = run_day60_shadow_session_dry_run([self._row()])

        self.assertIs(result["watch_only"], True)
        self.assertIs(result["dry_run_only"], True)
        self.assertIs(result["no_trade_boundary_preserved"], True)
        self.assertIs(result["live_data_started"], False)
        self.assertIs(result["alerts_sent"], False)
        self.assertIs(result["files_written"], False)
        self.assertIs(result["broker_or_trade_behavior_enabled"], False)

    def test_no_file_network_subprocess_live_data_side_effects(self):
        row = self._row()
        before = copy.deepcopy(row)

        with patch("builtins.open") as open_mock, patch(
            "socket.socket"
        ) as socket_mock, patch("subprocess.run") as subprocess_mock:
            result = run_day60_shadow_session_dry_run([row])

        self.assertEqual(row, before)
        self.assertEqual(result["rows_accepted"], 1)
        self.assertIs(result["live_data_started"], False)
        open_mock.assert_not_called()
        socket_mock.assert_not_called()
        subprocess_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
