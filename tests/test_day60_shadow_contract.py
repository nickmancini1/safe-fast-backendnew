import copy
import unittest
from unittest.mock import patch

from watcher_foundation import (
    DAY60_SHADOW_CONTRACT_DIAGNOSTIC_PLACEHOLDER_FIELDS,
    validate_day60_shadow_contract_batch,
    validate_day60_shadow_contract_row,
)


class Day60ShadowContractTests(unittest.TestCase):
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

    def test_valid_row_passes(self):
        result = validate_day60_shadow_contract_row(self._row())

        self.assertEqual(result["row_id"], "day60-row-1")
        self.assertTrue(result["watch_only"])

    def test_valid_batch_passes(self):
        result = validate_day60_shadow_contract_batch(
            [self._row(), self._row(row_id="day60-row-2")]
        )

        self.assertEqual(result["rows_processed"], 2)
        self.assertEqual(result["accepted_count"], 2)
        self.assertEqual(result["rejected_count"], 0)
        self.assertEqual([row["row_id"] for row in result["accepted_rows"]], [
            "day60-row-1",
            "day60-row-2",
        ])

    def test_missing_required_field_fails(self):
        row = self._row()
        del row["timestamp"]

        with self.assertRaisesRegex(ValueError, "timestamp"):
            validate_day60_shadow_contract_row(row)

    def test_invalid_type_fails(self):
        with self.assertRaisesRegex(TypeError, "row_id"):
            validate_day60_shadow_contract_row(self._row(row_id=123))

        with self.assertRaisesRegex(TypeError, "batch must be a list"):
            validate_day60_shadow_contract_batch((self._row(),))

    def test_unsupported_setup_stage_trigger_values_fail(self):
        with self.assertRaisesRegex(ValueError, "Unsupported setup_type"):
            validate_day60_shadow_contract_row(self._row(setup_type="Breakout"))

        with self.assertRaisesRegex(ValueError, "Unsupported stage"):
            validate_day60_shadow_contract_row(self._row(stage="live-ready"))

        with self.assertRaisesRegex(ValueError, "Unsupported trigger_status"):
            validate_day60_shadow_contract_row(
                self._row(trigger_status="approved")
            )

    def test_forbidden_nested_broker_order_account_option_pnl_trade_decision_field_fails(self):
        row = self._row()
        row["nested"] = {"review": [{"broker": "blocked"}]}
        with self.assertRaisesRegex(ValueError, "broker"):
            validate_day60_shadow_contract_row(row)

        row = self._row()
        row["nested"] = {"order_id": "abc"}
        with self.assertRaisesRegex(ValueError, "order_id"):
            validate_day60_shadow_contract_row(row)

        row = self._row()
        row["nested"] = {"account": {"id": "abc"}}
        with self.assertRaisesRegex(ValueError, "account"):
            validate_day60_shadow_contract_row(row)

        row = self._row()
        row["nested"] = {"option_pnl": 12.34}
        with self.assertRaisesRegex(ValueError, "option_pnl"):
            validate_day60_shadow_contract_row(row)

        row = self._row()
        row["nested"] = {"trade_decision": "approve"}
        with self.assertRaisesRegex(ValueError, "trade_decision"):
            validate_day60_shadow_contract_row(row)

    def test_watch_only_false_fails(self):
        with self.assertRaisesRegex(ValueError, "watch_only=True"):
            validate_day60_shadow_contract_row(self._row(watch_only=False))

    def test_no_trade_boundary_failure_fails(self):
        row = self._row()
        row["no_trade_boundary"]["no_broker"] = False

        with self.assertRaisesRegex(ValueError, "no_broker=True"):
            validate_day60_shadow_contract_row(row)

        row = self._row()
        row["no_trade_boundary"]["live_decision_allowed"] = True

        with self.assertRaisesRegex(ValueError, "live_decision_allowed=False"):
            validate_day60_shadow_contract_row(row)

    def test_provenance_showing_live_data_fetch_fails(self):
        row = self._row()
        row["provenance"]["live_data_fetch"] = True

        with self.assertRaisesRegex(ValueError, "live_data_fetch=False"):
            validate_day60_shadow_contract_row(row)

    def test_missing_diagnostics_placeholder_fails(self):
        row = self._row()
        del row["diagnostics_placeholders"]["headline_news"]

        with self.assertRaisesRegex(ValueError, "headline_news"):
            validate_day60_shadow_contract_row(row)

    def test_unavailable_fields_missing_or_invalid_fails(self):
        with self.assertRaisesRegex(ValueError, "unavailable_fields"):
            validate_day60_shadow_contract_row(self._row(unavailable_fields=[]))

        row = self._row()
        row["unavailable_fields"][0]["fabricated"] = True
        with self.assertRaisesRegex(ValueError, "fabricated=False"):
            validate_day60_shadow_contract_row(row)

    def test_no_hindsight_boundary_missing_or_invalid_fails(self):
        row = self._row()
        del row["no_hindsight_boundary"]
        with self.assertRaisesRegex(ValueError, "no_hindsight_boundary"):
            validate_day60_shadow_contract_row(row)

        row = self._row()
        row["no_hindsight_boundary"]["future_rows_not_used_for_candidate"] = False
        with self.assertRaisesRegex(ValueError, "future_rows_not_used_for_candidate=True"):
            validate_day60_shadow_contract_row(row)

    def test_validator_returns_defensive_copies(self):
        row = self._row()
        result = validate_day60_shadow_contract_row(row)

        result["trigger_card"]["blockers"].append("changed")
        result["unavailable_fields"][0]["reason"] = "changed"

        self.assertEqual(row["trigger_card"]["blockers"], [])
        self.assertEqual(
            row["unavailable_fields"][0]["reason"],
            "future diagnostic category preserved",
        )

    def test_batch_preserves_rejected_row_reasons(self):
        invalid = self._row(row_id="bad-row", watch_only=False)
        result = validate_day60_shadow_contract_batch([self._row(), invalid, "bad"])

        self.assertEqual(result["accepted_count"], 1)
        self.assertEqual(result["rejected_count"], 2)
        self.assertEqual(result["rejected_rows"][0]["row_id"], "bad-row")
        self.assertIn("watch_only=True", result["rejected_rows"][0]["reason"])
        self.assertEqual(result["rejected_rows"][1]["row_id"], "UNAVAILABLE")
        self.assertIn("must be a dict", result["rejected_rows"][1]["reason"])

    def test_no_file_network_subprocess_live_data_side_effects(self):
        row = self._row()
        before = copy.deepcopy(row)

        with patch("builtins.open") as open_mock, patch(
            "socket.socket"
        ) as socket_mock, patch("subprocess.run") as subprocess_mock:
            result = validate_day60_shadow_contract_batch([row])

        self.assertEqual(row, before)
        self.assertEqual(result["accepted_count"], 1)
        open_mock.assert_not_called()
        socket_mock.assert_not_called()
        subprocess_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
