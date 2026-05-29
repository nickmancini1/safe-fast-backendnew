import copy
import unittest
from unittest.mock import patch

from watcher_foundation import (
    DAY60_SHADOW_CONTRACT_DIAGNOSTIC_PLACEHOLDER_FIELDS,
    DAY60_SHADOW_REVIEW_PACKET_DIAGNOSTIC_PLACEHOLDER_FIELDS,
    DAY60_SHADOW_REVIEW_PACKET_OUTCOME_PLACEHOLDER_FIELDS,
    DAY60_SHADOW_REVIEW_PACKET_RESULT_FIELDS,
    DAY60_SHADOW_REVIEW_PACKET_VIABILITY_PLACEHOLDER_FIELDS,
    build_day60_shadow_review_packet,
    run_day60_shadow_session_dry_run,
)


class Day60ShadowReviewPacketTests(unittest.TestCase):
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

    def _dry_run_result(self):
        return run_day60_shadow_session_dry_run(
            [
                self._row(),
                self._row(row_id="day60-row-2"),
                self._row(row_id="bad-row", watch_only=False),
            ],
            session_metadata={
                "session_id": "day60-session",
                "review": {"owner": "local-only"},
            },
        )

    def test_valid_dry_run_result_produces_review_packet(self):
        packet = build_day60_shadow_review_packet(self._dry_run_result())

        self.assertEqual(set(DAY60_SHADOW_REVIEW_PACKET_RESULT_FIELDS), set(packet))
        self.assertIs(packet["watch_only"], True)
        self.assertIs(packet["review_packet_only"], True)
        self.assertIs(packet["dry_run_only"], True)
        self.assertEqual(packet["rows_processed"], 3)
        self.assertEqual(packet["rows_accepted"], 2)
        self.assertEqual(packet["rows_rejected"], 1)
        self.assertIs(packet["no_trade_boundary_preserved"], True)
        self.assertIs(packet["live_data_started"], False)
        self.assertIs(packet["alerts_sent"], False)
        self.assertIs(packet["files_written"], False)
        self.assertIs(packet["broker_or_trade_behavior_enabled"], False)

    def test_accepted_rows_are_preserved_defensively(self):
        dry_run = self._dry_run_result()
        packet = build_day60_shadow_review_packet(dry_run)

        packet["accepted_rows"][0]["trigger_card"]["blockers"].append("changed")
        packet["accepted_rows"][0]["unavailable_fields"][0]["reason"] = "changed"

        self.assertEqual(dry_run["accepted_rows"][0]["trigger_card"]["blockers"], [])
        self.assertEqual(
            dry_run["accepted_rows"][0]["unavailable_fields"][0]["reason"],
            "future diagnostic category preserved",
        )

    def test_rejected_row_reasons_are_preserved_defensively(self):
        dry_run = self._dry_run_result()
        packet = build_day60_shadow_review_packet(dry_run)

        self.assertEqual(packet["rejected_rows"][0]["row_id"], "bad-row")
        self.assertIn("watch_only=True", packet["rejected_rows"][0]["reason"])

        packet["rejected_rows"][0]["reason"] = "changed"

        self.assertIn("watch_only=True", dry_run["rejected_rows"][0]["reason"])

    def test_session_metadata_is_preserved_defensively(self):
        dry_run = self._dry_run_result()
        packet = build_day60_shadow_review_packet(dry_run)

        packet["session_metadata"]["review"]["owner"] = "changed"

        self.assertEqual(dry_run["session_metadata"]["review"]["owner"], "local-only")

    def test_diagnostic_placeholders_exist(self):
        packet = build_day60_shadow_review_packet(self._dry_run_result())

        self.assertEqual(
            set(DAY60_SHADOW_REVIEW_PACKET_DIAGNOSTIC_PLACEHOLDER_FIELDS),
            set(packet["diagnostic_placeholders"]),
        )
        for placeholder in packet["diagnostic_placeholders"].values():
            self.assertIs(placeholder["placeholder_preserved"], True)
            self.assertIs(placeholder["review_required_later"], True)

    def test_outcome_scoring_placeholders_exist(self):
        packet = build_day60_shadow_review_packet(self._dry_run_result())

        self.assertEqual(
            set(DAY60_SHADOW_REVIEW_PACKET_OUTCOME_PLACEHOLDER_FIELDS),
            set(packet["outcome_scoring_placeholders"]),
        )
        for placeholder in packet["outcome_scoring_placeholders"].values():
            self.assertIs(placeholder["placeholder_preserved"], True)
            self.assertIs(placeholder["review_required_later"], True)

    def test_viability_review_placeholders_exist(self):
        packet = build_day60_shadow_review_packet(self._dry_run_result())

        self.assertEqual(
            set(DAY60_SHADOW_REVIEW_PACKET_VIABILITY_PLACEHOLDER_FIELDS),
            set(packet["viability_review_placeholders"]),
        )
        for placeholder in packet["viability_review_placeholders"].values():
            self.assertIs(placeholder["placeholder_preserved"], True)
            self.assertIs(placeholder["review_required_later"], True)

    def test_invalid_dry_run_result_type_fails(self):
        with self.assertRaisesRegex(TypeError, "input must be a dict"):
            build_day60_shadow_review_packet([self._dry_run_result()])

    def test_missing_required_dry_run_field_fails(self):
        dry_run = self._dry_run_result()
        del dry_run["accepted_rows"]

        with self.assertRaisesRegex(ValueError, "accepted_rows"):
            build_day60_shadow_review_packet(dry_run)

    def test_unexpected_dry_run_field_fails(self):
        dry_run = self._dry_run_result()
        dry_run["extra_review_field"] = "not from dry-run adapter"

        with self.assertRaisesRegex(ValueError, "Unexpected"):
            build_day60_shadow_review_packet(dry_run)

    def test_boundary_flag_failure_fails(self):
        failing_cases = (
            ("watch_only", False, "watch_only=True"),
            ("dry_run_only", False, "dry_run_only=True"),
            ("no_trade_boundary_preserved", False, "no_trade_boundary_preserved=True"),
            ("live_data_started", True, "live_data_started=False"),
            ("alerts_sent", True, "alerts_sent=False"),
            ("files_written", True, "files_written=False"),
            (
                "broker_or_trade_behavior_enabled",
                True,
                "broker_or_trade_behavior_enabled=False",
            ),
        )

        for field_name, value, message in failing_cases:
            with self.subTest(field_name=field_name):
                dry_run = self._dry_run_result()
                dry_run[field_name] = value

                with self.assertRaisesRegex(ValueError, message):
                    build_day60_shadow_review_packet(dry_run)

    def test_forbidden_nested_broker_order_account_options_pnl_trade_decision_field_fails(self):
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
                dry_run = self._dry_run_result()
                dry_run["accepted_rows"][0].update(forbidden)

                with self.assertRaisesRegex(ValueError, "Forbidden execution/trade field"):
                    build_day60_shadow_review_packet(dry_run)

    def test_no_file_network_subprocess_live_data_side_effects(self):
        dry_run = self._dry_run_result()
        before = copy.deepcopy(dry_run)

        with patch("builtins.open") as open_mock, patch(
            "socket.socket"
        ) as socket_mock, patch("subprocess.run") as subprocess_mock:
            packet = build_day60_shadow_review_packet(dry_run)

        self.assertEqual(dry_run, before)
        self.assertIs(packet["live_data_started"], False)
        self.assertIs(packet["alerts_sent"], False)
        self.assertIs(packet["files_written"], False)
        self.assertIs(packet["broker_or_trade_behavior_enabled"], False)
        open_mock.assert_not_called()
        socket_mock.assert_not_called()
        subprocess_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
