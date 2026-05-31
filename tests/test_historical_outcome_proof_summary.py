import copy
import unittest
from unittest.mock import patch

from watcher_foundation import (
    DAY60_OUTCOME_REVIEW_BUCKETS,
    HISTORICAL_OUTCOME_PROOF_SUMMARY_RESULT_FIELDS,
    build_historical_outcome_proof_summary,
)


class HistoricalOutcomeProofSummaryTests(unittest.TestCase):
    def _unavailable_item(self, field_name):
        return {
            "field_name": field_name,
            "status": "unavailable",
            "reason": "caller did not provide source-backed proof value",
            "fabricated": False,
        }

    def _row(self, **overrides):
        row = {
            "outcome_row_id": "historical-proof-row-1",
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
            "time_to_failure": "not_observed_in_window",
            "stale_spent_outcome": "not_stale_or_spent",
            "blocker_caution_outcome": "no_blocker_materialized",
            "evidence_refs": ["review-packet-1.accepted_rows[0]", "chart-row-218"],
            "unavailable_fields": [],
            "no_hindsight_boundary": {
                "evidence_available_at_or_before_review_timestamp": True,
                "future_evidence_not_used": True,
                "future_evidence_outside_declared_window_used": False,
                "no_backfilled_outcome_labels": True,
                "review_timestamp_field": "outcome_review_timestamp",
                "outcome_window_field": "outcome_window",
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
            "historical_review_boundary": {
                "caller_provided": True,
                "historical_review_only": True,
                "no_live_data": True,
                "no_controlled_shadow_data": True,
                "no_generated_report": True,
            },
        }
        row.update(overrides)
        return row

    def test_valid_caller_provided_rows_produce_in_memory_summary(self):
        result = build_historical_outcome_proof_summary([self._row()])

        self.assertEqual(set(HISTORICAL_OUTCOME_PROOF_SUMMARY_RESULT_FIELDS), set(result))
        self.assertEqual(result["rows_processed"], 1)
        self.assertEqual(result["rows_accepted"], 1)
        self.assertEqual(result["rows_rejected"], 0)
        self.assertEqual(
            result["accepted_rows"][0]["outcome_row_id"],
            "historical-proof-row-1",
        )
        self.assertIs(result["watch_only"], True)
        self.assertIs(result["historical_outcome_summary_only"], True)

    def test_rows_are_validated_through_existing_preflight_validator(self):
        row = self._row()

        with patch(
            "watcher_foundation.historical_outcome_proof_summary."
            "validate_historical_outcome_proof_row",
            side_effect=lambda value: copy.deepcopy(value),
        ) as validate_mock:
            result = build_historical_outcome_proof_summary([row])

        validate_mock.assert_called_once_with(row)
        self.assertEqual(result["rows_accepted"], 1)

    def test_accepted_and_rejected_rows_preserve_reasons(self):
        result = build_historical_outcome_proof_summary(
            [
                self._row(outcome_row_id="good-row"),
                self._row(outcome_row_id="bad-row", watch_only=False),
            ]
        )

        self.assertEqual(result["rows_processed"], 2)
        self.assertEqual(result["rows_accepted"], 1)
        self.assertEqual(result["rows_rejected"], 1)
        self.assertEqual(result["rejected_rows"][0]["row_id"], "bad-row")
        self.assertIn("watch_only=True", result["rejected_rows"][0]["reason"])

    def test_outcome_buckets_are_summarized_when_possible(self):
        result = build_historical_outcome_proof_summary(
            [
                self._row(
                    outcome_row_id="strong",
                    outcome_status="strong_follow_through",
                    stale_spent_outcome="fresh",
                ),
                self._row(
                    outcome_row_id="failed",
                    outcome_status="no_follow_through",
                    failure_status="failed_trigger",
                    stale_spent_outcome="fresh",
                ),
            ]
        )

        self.assertEqual(set(DAY60_OUTCOME_REVIEW_BUCKETS), set(result["bucket_counts"]))
        self.assertEqual(result["bucket_counts"]["strong_follow_through"], 1)
        self.assertEqual(result["bucket_counts"]["failed_trigger"], 1)
        self.assertEqual(result["accepted_rows"][0]["review_bucket"], "strong_follow_through")
        self.assertEqual(result["accepted_rows"][1]["review_bucket"], "failed_trigger")

    def test_unavailable_evidence_remains_explicit(self):
        row = self._row(
            outcome_row_id="missing-proof-row",
            unavailable_fields=[self._unavailable_item("time_to_failure")],
            time_to_failure=None,
        )

        result = build_historical_outcome_proof_summary([row])

        self.assertEqual(result["rows_accepted"], 1)
        self.assertIsNone(result["accepted_rows"][0]["time_to_failure"])
        self.assertEqual(
            result["accepted_rows"][0]["review_bucket"],
            "unavailable_evidence",
        )
        self.assertEqual(
            result["unavailable_evidence"],
            [
                {
                    "row_id": "missing-proof-row",
                    "field_name": "time_to_failure",
                    "status": "unavailable",
                    "reason": "caller did not provide source-backed proof value",
                    "fabricated": False,
                    "missing_from_row": False,
                }
            ],
        )

    def test_no_hindsight_and_no_trade_boundaries_are_preserved(self):
        result = build_historical_outcome_proof_summary([self._row()])

        self.assertIs(result["no_hindsight_boundary_preserved"], True)
        self.assertIs(result["no_trade_boundary_preserved"], True)
        self.assertTrue(
            result["accepted_rows"][0]["no_hindsight_boundary"][
                "future_evidence_not_used"
            ]
        )
        self.assertTrue(result["accepted_rows"][0]["no_trade_boundary"]["no_trade"])
        self.assertFalse(
            result["accepted_rows"][0]["no_trade_boundary"][
                "live_trade_decision_enabled"
            ]
        )

    def test_final_viability_remains_false(self):
        result = build_historical_outcome_proof_summary(
            [self._row(outcome_status="strong_follow_through")]
        )

        self.assertIs(result["final_viability_proven"], False)

    def test_invalid_input_type_fails(self):
        with self.assertRaisesRegex(TypeError, "rows must be a list"):
            build_historical_outcome_proof_summary((self._row(),))

    def test_boundary_failure_fails(self):
        result = build_historical_outcome_proof_summary(
            [
                self._row(
                    historical_review_boundary={
                        "caller_provided": True,
                        "historical_review_only": True,
                        "no_live_data": False,
                        "no_controlled_shadow_data": True,
                        "no_generated_report": True,
                    }
                )
            ]
        )

        self.assertEqual(result["rows_accepted"], 0)
        self.assertEqual(result["rows_rejected"], 1)
        self.assertIn("no_live_data=True", result["rejected_rows"][0]["reason"])

    def test_forbidden_trade_decision_field_fails_recursively(self):
        row = self._row()
        row["nested"] = {"proof": [{"trade_decision": "approve"}]}

        result = build_historical_outcome_proof_summary([row])

        self.assertEqual(result["rows_accepted"], 0)
        self.assertEqual(result["rows_rejected"], 1)
        self.assertIn(
            "Forbidden execution/trade field",
            result["rejected_rows"][0]["reason"],
        )

    def test_defensive_copies_are_returned(self):
        row = self._row()
        before = copy.deepcopy(row)

        result = build_historical_outcome_proof_summary([row])
        result["accepted_rows"][0]["mfe"]["value"] = 99
        result["accepted_rows"][0]["historical_review_boundary"][
            "caller_provided"
        ] = False

        self.assertEqual(row, before)
        self.assertEqual(row["mfe"]["value"], 1.25)
        self.assertTrue(row["historical_review_boundary"]["caller_provided"])

    def test_no_file_network_subprocess_or_live_data_side_effects(self):
        row = self._row()
        before = copy.deepcopy(row)

        with patch("builtins.open") as open_mock, patch(
            "socket.socket"
        ) as socket_mock, patch("subprocess.run") as subprocess_mock:
            result = build_historical_outcome_proof_summary([row])

        self.assertEqual(row, before)
        self.assertIs(result["live_data_started"], False)
        self.assertIs(result["controlled_shadow_data_started"], False)
        self.assertIs(result["alerts_sent"], False)
        self.assertIs(result["files_written"], False)
        self.assertIs(result["broker_or_trade_behavior_enabled"], False)
        open_mock.assert_not_called()
        socket_mock.assert_not_called()
        subprocess_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
