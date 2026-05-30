import copy
import unittest
from unittest.mock import patch

from watcher_foundation import (
    DAY60_OUTCOME_REVIEW_BUCKETS,
    DAY60_OUTCOME_SCORING_SUMMARY_RESULT_FIELDS,
    build_day60_outcome_scoring_summary,
)


class Day60OutcomeScoringSummaryTests(unittest.TestCase):
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
            "time_to_failure": "not_observed_in_window",
            "stale_spent_outcome": "not_stale_or_spent",
            "blocker_caution_outcome": "no_blocker_materialized",
            "evidence_refs": ["review-packet-1.accepted_rows[0]", "chart-row-218"],
            "unavailable_fields": [],
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

    def test_rows_are_validated_through_existing_contract_validator(self):
        row = self._row()

        with patch(
            "watcher_foundation.day60_outcome_scoring_summary."
            "validate_day60_outcome_scoring_row",
            side_effect=lambda value: copy.deepcopy(value),
        ) as validate_mock:
            result = build_day60_outcome_scoring_summary([row])

        validate_mock.assert_called_once_with(row)
        self.assertEqual(result["rows_accepted"], 1)

    def test_accepted_rows_are_counted_and_summarized_in_memory(self):
        result = build_day60_outcome_scoring_summary(
            [
                self._row(outcome_row_id="row-1", outcome_status="strong_follow_through"),
                self._row(outcome_row_id="row-2", outcome_status="partial_follow_through"),
            ]
        )

        self.assertEqual(set(DAY60_OUTCOME_SCORING_SUMMARY_RESULT_FIELDS), set(result))
        self.assertEqual(result["rows_processed"], 2)
        self.assertEqual(result["rows_accepted"], 2)
        self.assertEqual(result["rows_rejected"], 0)
        self.assertEqual(result["bucket_counts"]["strong_follow_through"], 1)
        self.assertEqual(result["bucket_counts"]["partial_follow_through"], 1)
        self.assertEqual(result["accepted_rows"][0]["review_bucket"], "strong_follow_through")

    def test_rejected_rows_preserve_row_id_and_rejection_reason(self):
        result = build_day60_outcome_scoring_summary(
            [
                self._row(outcome_row_id="good-row"),
                self._row(outcome_row_id="bad-row", watch_only=False),
            ]
        )

        self.assertEqual(result["rows_accepted"], 1)
        self.assertEqual(result["rows_rejected"], 1)
        self.assertEqual(result["rejected_rows"][0]["row_id"], "bad-row")
        self.assertIn("watch_only=True", result["rejected_rows"][0]["reason"])

    def test_missing_or_unavailable_outcome_fields_remain_explicit(self):
        row = self._row(
            outcome_row_id="missing-proof-row",
            unavailable_fields=[self._unavailable_item("time_to_failure")],
        )
        del row["time_to_failure"]

        result = build_day60_outcome_scoring_summary([row])

        self.assertEqual(result["rows_accepted"], 1)
        self.assertNotIn("time_to_failure", result["accepted_rows"][0])
        self.assertEqual(
            result["accepted_rows"][0]["unavailable_fields"][0]["field_name"],
            "time_to_failure",
        )
        self.assertEqual(
            result["unavailable_outcome_fields"],
            [
                {
                    "row_id": "missing-proof-row",
                    "field_name": "time_to_failure",
                    "status": "unavailable",
                    "reason": "caller did not provide source-backed proof value",
                    "fabricated": False,
                    "missing_from_row": True,
                }
            ],
        )
        self.assertEqual(
            result["accepted_rows"][0]["review_bucket"],
            "unavailable_evidence",
        )

    def test_each_review_bucket_is_reachable(self):
        cases = (
            (
                "strong_follow_through",
                self._row(
                    outcome_row_id="strong",
                    outcome_status="strong_follow_through",
                    stale_spent_outcome="fresh",
                ),
            ),
            (
                "partial_follow_through",
                self._row(
                    outcome_row_id="partial",
                    outcome_status="partial_follow_through",
                    stale_spent_outcome="fresh",
                ),
            ),
            (
                "failed_trigger",
                self._row(
                    outcome_row_id="failed",
                    outcome_status="no_follow_through",
                    failure_status="failed_trigger",
                    stale_spent_outcome="fresh",
                ),
            ),
            (
                "stale_spent",
                self._row(
                    outcome_row_id="stale",
                    outcome_status="no_follow_through",
                    stale_spent_outcome="stale",
                ),
            ),
            (
                "blocked_correctly",
                self._row(
                    outcome_row_id="blocked-correct",
                    outcome_status="no_follow_through",
                    stale_spent_outcome="fresh",
                    blocker_caution_outcome="correctly_blocked",
                ),
            ),
            (
                "blocked_incorrectly",
                self._row(
                    outcome_row_id="blocked-incorrect",
                    outcome_status="no_follow_through",
                    stale_spent_outcome="fresh",
                    blocker_caution_outcome="incorrectly_blocked",
                ),
            ),
            (
                "inconclusive",
                self._row(
                    outcome_row_id="inconclusive",
                    outcome_status="inconclusive",
                    stale_spent_outcome="fresh",
                ),
            ),
            (
                "unavailable_evidence",
                self._row(
                    outcome_row_id="unavailable",
                    unavailable_fields=[self._unavailable_item("outcome_status")],
                    outcome_status=None,
                    stale_spent_outcome="fresh",
                ),
            ),
        )

        result = build_day60_outcome_scoring_summary([row for _, row in cases])

        self.assertEqual(set(DAY60_OUTCOME_REVIEW_BUCKETS), set(result["bucket_counts"]))
        self.assertEqual(result["rows_accepted"], len(DAY60_OUTCOME_REVIEW_BUCKETS))
        for bucket, accepted_row in zip(DAY60_OUTCOME_REVIEW_BUCKETS, result["accepted_rows"]):
            self.assertEqual(accepted_row["review_bucket"], bucket)
            self.assertEqual(result["bucket_counts"][bucket], 1)

    def test_no_hindsight_and_no_trade_boundaries_are_preserved(self):
        result = build_day60_outcome_scoring_summary([self._row()])

        self.assertIs(result["watch_only"], True)
        self.assertIs(result["outcome_scoring_summary_only"], True)
        self.assertIs(result["no_hindsight_boundary_preserved"], True)
        self.assertIs(result["no_trade_boundary_preserved"], True)

    def test_invalid_input_type_fails(self):
        with self.assertRaisesRegex(TypeError, "rows must be a list"):
            build_day60_outcome_scoring_summary((self._row(),))

    def test_defensive_copies_are_returned(self):
        row = self._row()
        before = copy.deepcopy(row)

        result = build_day60_outcome_scoring_summary([row])
        result["accepted_rows"][0]["mfe"]["value"] = 99
        result["accepted_rows"][0]["unavailable_fields"].append(
            self._unavailable_item("mae")
        )

        self.assertEqual(row, before)
        self.assertEqual(row["mfe"]["value"], 1.25)
        self.assertEqual(row["unavailable_fields"], [])

    def test_evaluator_has_no_file_network_subprocess_or_live_side_effects(self):
        row = self._row()
        before = copy.deepcopy(row)

        with patch("builtins.open") as open_mock, patch(
            "socket.socket"
        ) as socket_mock, patch("subprocess.run") as subprocess_mock:
            result = build_day60_outcome_scoring_summary([row])

        self.assertEqual(row, before)
        self.assertIs(result["live_data_started"], False)
        self.assertIs(result["alerts_sent"], False)
        self.assertIs(result["files_written"], False)
        self.assertIs(result["broker_or_trade_behavior_enabled"], False)
        open_mock.assert_not_called()
        socket_mock.assert_not_called()
        subprocess_mock.assert_not_called()

    def test_evaluator_does_not_start_watcher_loops_or_make_trade_decisions(self):
        result = build_day60_outcome_scoring_summary([self._row()])

        self.assertIs(result["watch_only"], True)
        self.assertIs(result["live_data_started"], False)
        self.assertIs(result["alerts_sent"], False)
        self.assertIs(result["broker_or_trade_behavior_enabled"], False)
        self.assertIs(result["accepted_rows"][0]["watch_only"], True)
        self.assertTrue(result["accepted_rows"][0]["no_trade_boundary"]["no_trade"])
        self.assertFalse(
            result["accepted_rows"][0]["no_trade_boundary"][
                "live_trade_decision_enabled"
            ]
        )


if __name__ == "__main__":
    unittest.main()
