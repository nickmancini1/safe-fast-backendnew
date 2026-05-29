import copy
import unittest
from unittest.mock import patch

from watcher_foundation import (
    DAY60_SHADOW_CONTRACT_DIAGNOSTIC_PLACEHOLDER_FIELDS,
    DAY60_SHADOW_READINESS_RESULT_FIELDS,
    build_day60_shadow_review_packet,
    evaluate_day60_shadow_readiness,
    run_day60_shadow_session_dry_run,
)


class Day60ShadowReadinessTests(unittest.TestCase):
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

    def _review_packet(self):
        dry_run = run_day60_shadow_session_dry_run(
            [self._row(), self._row(row_id="day60-row-2")],
            session_metadata={"session_id": "day60-session"},
        )
        return build_day60_shadow_review_packet(dry_run)

    def test_complete_packet_returns_in_memory_readiness_summary(self):
        summary = evaluate_day60_shadow_readiness(self._review_packet())

        self.assertEqual(set(DAY60_SHADOW_READINESS_RESULT_FIELDS), set(summary))
        self.assertIs(summary["watch_only"], True)
        self.assertIs(summary["readiness_evaluation_only"], True)
        self.assertIs(summary["review_packet_only"], True)
        self.assertIs(summary["diagnostic_placeholders_present"], True)
        self.assertIs(summary["outcome_scoring_placeholders_present"], True)
        self.assertIs(summary["viability_review_placeholders_present"], True)
        self.assertEqual(summary["diagnostic_gaps"], [])
        self.assertEqual(summary["missing_proof_fields"], [])
        self.assertIs(summary["ready_for_controlled_shadow_review"], True)

    def test_missing_diagnostic_placeholders_are_reported_as_diagnostic_gaps(self):
        packet = self._review_packet()
        del packet["diagnostic_placeholders"]["trigger_quality_review"]

        summary = evaluate_day60_shadow_readiness(packet)

        self.assertIs(summary["diagnostic_placeholders_present"], False)
        self.assertIn(
            "missing_diagnostic_placeholders:trigger_quality_review",
            summary["diagnostic_gaps"],
        )
        self.assertIs(summary["ready_for_controlled_shadow_review"], False)

    def test_missing_outcome_scoring_placeholders_are_reported_as_diagnostic_gaps(self):
        packet = self._review_packet()
        del packet["outcome_scoring_placeholders"]["future_mfe_mae"]

        summary = evaluate_day60_shadow_readiness(packet)

        self.assertIs(summary["outcome_scoring_placeholders_present"], False)
        self.assertIn(
            "missing_outcome_scoring_placeholders:future_mfe_mae",
            summary["diagnostic_gaps"],
        )

    def test_missing_viability_review_placeholders_are_reported_as_diagnostic_gaps(self):
        packet = self._review_packet()
        del packet["viability_review_placeholders"]["diagnostics_usefulness"]

        summary = evaluate_day60_shadow_readiness(packet)

        self.assertIs(summary["viability_review_placeholders_present"], False)
        self.assertIn(
            "missing_viability_review_placeholders:diagnostics_usefulness",
            summary["diagnostic_gaps"],
        )

    def test_missing_proof_fields_are_reported_without_fabricated_values(self):
        packet = self._review_packet()
        del packet["accepted_rows"][0]["evidence_refs"]

        summary = evaluate_day60_shadow_readiness(packet)

        self.assertIn("accepted_rows[0].evidence_refs", summary["missing_proof_fields"])
        self.assertIn(
            "missing_proof_field:accepted_rows[0].evidence_refs",
            summary["diagnostic_gaps"],
        )
        self.assertNotIn("evidence_refs", packet["accepted_rows"][0])
        self.assertIs(summary["ready_for_controlled_shadow_review"], False)

    def test_no_go_boundaries_are_preserved_in_summary(self):
        summary = evaluate_day60_shadow_readiness(self._review_packet())

        self.assertIs(summary["ready_for_live_data"], False)
        self.assertIs(summary["ready_for_alerts"], False)
        self.assertIs(summary["ready_for_trading"], False)
        self.assertIs(summary["no_trade_boundary_preserved"], True)
        self.assertIs(summary["live_data_started"], False)
        self.assertIs(summary["alerts_sent"], False)
        self.assertIs(summary["files_written"], False)
        self.assertIs(summary["broker_or_trade_behavior_enabled"], False)

    def test_invalid_packet_type_fails(self):
        with self.assertRaisesRegex(TypeError, "input must be a dict"):
            evaluate_day60_shadow_readiness([self._review_packet()])

    def test_missing_required_packet_field_fails(self):
        packet = self._review_packet()
        del packet["accepted_rows"]

        with self.assertRaisesRegex(ValueError, "accepted_rows"):
            evaluate_day60_shadow_readiness(packet)

    def test_boundary_flag_failure_fails(self):
        failing_cases = (
            ("watch_only", False, "watch_only=True"),
            ("review_packet_only", False, "review_packet_only=True"),
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
                packet = self._review_packet()
                packet[field_name] = value

                with self.assertRaisesRegex(ValueError, message):
                    evaluate_day60_shadow_readiness(packet)

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
                packet = self._review_packet()
                packet["accepted_rows"][0].update(forbidden)

                with self.assertRaisesRegex(ValueError, "Forbidden execution/trade field"):
                    evaluate_day60_shadow_readiness(packet)

    def test_evaluator_has_no_file_log_report_live_or_trade_side_effects(self):
        packet = self._review_packet()
        before = copy.deepcopy(packet)

        with patch("builtins.open") as open_mock, patch(
            "socket.socket"
        ) as socket_mock, patch("subprocess.run") as subprocess_mock:
            summary = evaluate_day60_shadow_readiness(packet)

        self.assertEqual(packet, before)
        self.assertIs(summary["live_data_started"], False)
        self.assertIs(summary["alerts_sent"], False)
        self.assertIs(summary["files_written"], False)
        self.assertIs(summary["broker_or_trade_behavior_enabled"], False)
        self.assertIs(summary["ready_for_live_data"], False)
        self.assertIs(summary["ready_for_alerts"], False)
        self.assertIs(summary["ready_for_trading"], False)
        open_mock.assert_not_called()
        socket_mock.assert_not_called()
        subprocess_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
