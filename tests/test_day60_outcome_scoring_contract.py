import copy
import unittest
from unittest.mock import patch

from watcher_foundation import (
    DAY60_OUTCOME_SCORING_CONTRACT_RESULT_FIELDS,
    validate_day60_outcome_scoring_batch,
    validate_day60_outcome_scoring_row,
)


class Day60OutcomeScoringContractTests(unittest.TestCase):
    def _unavailable_item(self, field_name):
        return {
            "field_name": field_name,
            "status": "unavailable",
            "reason": "caller did not provide source-backed proof value",
            "fabricated": False,
        }

    def _row(self, **overrides):
        row = {
            "outcome_row_id": "outcome-row-1",
            "source_review_packet_id": "review-packet-1",
            "symbol": "SPY",
            "timeframe": "1h_rth",
            "setup_type": "Ideal",
            "direction": "bullish/call-side",
            "detection_timestamp": "2026-05-24T09:35:00-04:00",
            "outcome_review_timestamp": "2026-05-25T16:00:00-04:00",
            "stage_at_detection": "near-trigger",
            "trigger_status_at_detection": "near_trigger",
            "trigger_reference": {
                "kind": "caller_provided_chart_reference",
                "value": "432 reclaim zone",
                "fabricated": False,
            },
            "invalidation_reference": {
                "kind": "caller_provided_chart_reference",
                "value": "below local shelf",
                "fabricated": False,
            },
            "outcome_window": {
                "start_timestamp": "2026-05-24T10:30:00-04:00",
                "end_timestamp": "2026-05-25T16:00:00-04:00",
                "caller_provided": True,
            },
            "outcome_status": "partial_follow_through",
            "follow_through_status": "observed",
            "failure_status": "not_observed",
            "mfe": {"value": 1.25, "unit": "R", "fabricated": False},
            "mae": {"value": -0.35, "unit": "R", "fabricated": False},
            "time_to_follow_through": "3h",
            "time_to_failure": None,
            "stale_spent_outcome": "not_stale_or_spent",
            "blocker_caution_outcome": "no_blocker_materialized",
            "evidence_refs": ["review-packet-1.accepted_rows[0]", "chart-row-218"],
            "unavailable_fields": [
                self._unavailable_item("time_to_failure"),
            ],
            "no_hindsight_boundary": {
                "evidence_available_at_or_before_review_timestamp": True,
                "future_evidence_not_used": True,
                "no_backfilled_outcome_labels": True,
                "review_timestamp_field": "outcome_review_timestamp",
            },
            "diagnostics_placeholders": {
                "failure_category": {
                    "status": "placeholder_only_until_reviewed_outcomes_accumulate"
                }
            },
            "no_trade_boundary": {
                "no_trade": True,
                "no_broker": True,
                "no_order": True,
                "no_account_sizing": True,
                "no_option_pnl": True,
                "no_live_trade_decision": True,
                "broker_enabled": False,
                "orders_enabled": False,
                "account_sizing_enabled": False,
                "option_pnl_enabled": False,
                "live_trade_decision_enabled": False,
            },
            "watch_only": True,
        }
        row.update(overrides)
        return row

    def test_complete_caller_provided_in_memory_outcome_review_row_passes(self):
        result = validate_day60_outcome_scoring_row(self._row())

        self.assertEqual(result["outcome_row_id"], "outcome-row-1")
        self.assertTrue(result["watch_only"])
        self.assertEqual(result["evidence_refs"], [
            "review-packet-1.accepted_rows[0]",
            "chart-row-218",
        ])

    def test_required_viability_proof_fields_are_enforced(self):
        row = self._row()
        del row["outcome_status"]

        with self.assertRaisesRegex(ValueError, "outcome_status"):
            validate_day60_outcome_scoring_row(row)

    def test_missing_or_unavailable_proof_fields_remain_explicit_not_fabricated(self):
        row = self._row()
        del row["time_to_failure"]

        result = validate_day60_outcome_scoring_row(row)

        self.assertNotIn("time_to_failure", result)
        self.assertEqual(result["unavailable_fields"][0]["field_name"], "time_to_failure")
        self.assertIs(result["unavailable_fields"][0]["fabricated"], False)

    def test_no_hindsight_outcome_review_boundary_fields_are_enforced(self):
        row = self._row()
        row["no_hindsight_boundary"]["future_evidence_not_used"] = False

        with self.assertRaisesRegex(ValueError, "future_evidence_not_used=True"):
            validate_day60_outcome_scoring_row(row)

        row = self._row()
        row["no_hindsight_boundary"]["review_timestamp_field"] = "detection_timestamp"

        with self.assertRaisesRegex(ValueError, "outcome_review_timestamp"):
            validate_day60_outcome_scoring_row(row)

    def test_fabricated_proof_values_are_rejected(self):
        for marker in (
            "FABRICATED",
            "MADE_UP",
            "ASSUMED_WITHOUT_EVIDENCE",
            "INVENTED",
            "UNKNOWN_BUT_FILLED",
            "FAKE",
        ):
            with self.subTest(marker=marker):
                row = self._row(outcome_status=marker)

                with self.assertRaisesRegex(ValueError, "Fabricated proof marker"):
                    validate_day60_outcome_scoring_row(row)

        row = self._row()
        row["mfe"]["fabricated"] = True
        with self.assertRaisesRegex(ValueError, "Fabricated proof value"):
            validate_day60_outcome_scoring_row(row)

    def test_forbidden_execution_fields_are_rejected_recursively(self):
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
                row = self._row()
                row.update(forbidden)

                with self.assertRaisesRegex(ValueError, "Forbidden execution/trade field"):
                    validate_day60_outcome_scoring_row(row)

    def test_multiple_in_memory_rows_return_row_level_results_without_file_outputs(self):
        result = validate_day60_outcome_scoring_batch(
            [
                self._row(),
                self._row(outcome_row_id="outcome-row-2"),
                self._row(outcome_row_id="bad-row", watch_only=False),
            ]
        )

        self.assertEqual(set(DAY60_OUTCOME_SCORING_CONTRACT_RESULT_FIELDS), set(result))
        self.assertEqual(result["rows_processed"], 3)
        self.assertEqual(result["rows_accepted"], 2)
        self.assertEqual(result["rows_rejected"], 1)
        self.assertEqual(result["rejected_rows"][0]["row_id"], "bad-row")
        self.assertIn("watch_only=True", result["rejected_rows"][0]["reason"])
        self.assertIs(result["files_written"], False)
        self.assertIs(result["live_data_started"], False)
        self.assertIs(result["alerts_sent"], False)

    def test_invalid_row_type_fails(self):
        with self.assertRaisesRegex(TypeError, "row must be a dict"):
            validate_day60_outcome_scoring_row("bad")

    def test_invalid_batch_type_fails(self):
        with self.assertRaisesRegex(TypeError, "batch must be a list"):
            validate_day60_outcome_scoring_batch((self._row(),))

    def test_watch_only_false_fails(self):
        with self.assertRaisesRegex(ValueError, "watch_only=True"):
            validate_day60_outcome_scoring_row(self._row(watch_only=False))

    def test_no_trade_boundary_failure_fails(self):
        row = self._row()
        row["no_trade_boundary"]["no_broker"] = False

        with self.assertRaisesRegex(ValueError, "no_broker=True"):
            validate_day60_outcome_scoring_row(row)

        row = self._row()
        row["no_trade_boundary"]["broker_enabled"] = True

        with self.assertRaisesRegex(ValueError, "broker_enabled=False"):
            validate_day60_outcome_scoring_row(row)

    def test_unsupported_setup_direction_stage_trigger_values_fail(self):
        with self.assertRaisesRegex(ValueError, "Unsupported setup_type"):
            validate_day60_outcome_scoring_row(self._row(setup_type="Breakout"))

        with self.assertRaisesRegex(ValueError, "Unsupported direction"):
            validate_day60_outcome_scoring_row(self._row(direction="long"))

        with self.assertRaisesRegex(ValueError, "Unsupported stage_at_detection"):
            validate_day60_outcome_scoring_row(
                self._row(stage_at_detection="live-ready")
            )

        with self.assertRaisesRegex(
            ValueError, "Unsupported trigger_status_at_detection"
        ):
            validate_day60_outcome_scoring_row(
                self._row(trigger_status_at_detection="approved")
            )

    def test_empty_evidence_refs_fail(self):
        with self.assertRaisesRegex(ValueError, "evidence_refs must be non-empty"):
            validate_day60_outcome_scoring_row(self._row(evidence_refs=[]))

    def test_validator_returns_defensive_copies(self):
        row = self._row()
        before = copy.deepcopy(row)
        result = validate_day60_outcome_scoring_row(row)

        result["mfe"]["value"] = 99
        result["unavailable_fields"][0]["reason"] = "changed"

        self.assertEqual(row, before)
        self.assertEqual(row["mfe"]["value"], 1.25)
        self.assertEqual(
            row["unavailable_fields"][0]["reason"],
            "caller did not provide source-backed proof value",
        )

    def test_no_file_network_subprocess_live_data_side_effects(self):
        row = self._row()
        before = copy.deepcopy(row)

        with patch("builtins.open") as open_mock, patch(
            "socket.socket"
        ) as socket_mock, patch("subprocess.run") as subprocess_mock:
            result = validate_day60_outcome_scoring_batch([row])

        self.assertEqual(row, before)
        self.assertEqual(result["rows_accepted"], 1)
        self.assertIs(result["watch_only"], True)
        self.assertIs(result["outcome_scoring_contract_only"], True)
        self.assertIs(result["no_trade_boundary_preserved"], True)
        self.assertIs(result["live_data_started"], False)
        self.assertIs(result["alerts_sent"], False)
        self.assertIs(result["files_written"], False)
        self.assertIs(result["broker_or_trade_behavior_enabled"], False)
        open_mock.assert_not_called()
        socket_mock.assert_not_called()
        subprocess_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
