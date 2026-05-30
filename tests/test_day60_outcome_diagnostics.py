import copy
import unittest
from unittest.mock import patch

from watcher_foundation import (
    DAY60_OUTCOME_DIAGNOSTICS_RESULT_FIELDS,
    DAY60_OUTCOME_DIAGNOSTIC_FAILURE_CATEGORIES,
    DAY60_OUTCOME_DIAGNOSTIC_FIX_PATHS,
    evaluate_day60_outcome_diagnostics,
)


class Day60OutcomeDiagnosticsTests(unittest.TestCase):
    def _accepted_row(self, **overrides):
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
            "stale_spent_outcome": "fresh",
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
            "review_bucket": "partial_follow_through",
        }
        row.update(overrides)
        return row

    def _summary(self, **overrides):
        summary = {
            "watch_only": True,
            "outcome_scoring_summary_only": True,
            "rows_processed": 1,
            "rows_accepted": 1,
            "rows_rejected": 0,
            "accepted_rows": [self._accepted_row()],
            "rejected_rows": [],
            "bucket_counts": {
                "strong_follow_through": 0,
                "partial_follow_through": 1,
                "failed_trigger": 0,
                "stale_spent": 0,
                "blocked_correctly": 0,
                "blocked_incorrectly": 0,
                "inconclusive": 0,
                "unavailable_evidence": 0,
            },
            "unavailable_outcome_fields": [],
            "no_hindsight_boundary_preserved": True,
            "no_trade_boundary_preserved": True,
            "live_data_started": False,
            "alerts_sent": False,
            "files_written": False,
            "broker_or_trade_behavior_enabled": False,
        }
        summary.update(overrides)
        return summary

    def test_valid_outcome_summary_returns_in_memory_diagnostics_summary(self):
        result = evaluate_day60_outcome_diagnostics(self._summary())

        self.assertEqual(set(DAY60_OUTCOME_DIAGNOSTICS_RESULT_FIELDS), set(result))
        self.assertIs(result["watch_only"], True)
        self.assertIs(result["outcome_diagnostics_only"], True)
        self.assertIs(result["optimization_started"], False)
        self.assertEqual(result["rows_processed"], 1)
        self.assertEqual(result["rows_accepted"], 1)
        self.assertEqual(result["rows_rejected"], 0)

    def test_diagnostic_categories_are_identified_without_fabricated_facts(self):
        rows = [
            self._accepted_row(outcome_row_id="failed", review_bucket="failed_trigger"),
            self._accepted_row(outcome_row_id="stale", review_bucket="stale_spent"),
            self._accepted_row(
                outcome_row_id="blocked", review_bucket="blocked_incorrectly"
            ),
            self._accepted_row(outcome_row_id="partial", review_bucket="partial_follow_through"),
            self._accepted_row(outcome_row_id="strong", review_bucket="strong_follow_through"),
        ]

        result = evaluate_day60_outcome_diagnostics(
            self._summary(rows_processed=5, rows_accepted=5, accepted_rows=rows)
        )

        categories = {
            finding["diagnostic_category"] for finding in result["diagnostic_findings"]
        }
        self.assertIn("trigger_level_or_zone_review", categories)
        self.assertIn("fresh_stale_spent_review", categories)
        self.assertIn("blocker_caution_review", categories)
        self.assertIn("outcome_scoring_review", categories)
        self.assertNotIn("strong_follow_through", categories)
        self.assertTrue(set(categories).issubset(DAY60_OUTCOME_DIAGNOSTIC_FAILURE_CATEGORIES))
        for finding in result["diagnostic_findings"]:
            self.assertNotIn("fact", finding["likely_cause_candidates"][0]["label"])

    def test_evidence_and_affected_relationship_fields_are_preserved(self):
        row = self._accepted_row(
            outcome_row_id="failed-trigger-row",
            review_bucket="failed_trigger",
            setup_type="Clean Fast Break",
            symbol="QQQ",
            stage_at_detection="triggering",
            trigger_status_at_detection="triggered",
            stale_spent_outcome="fresh",
        )

        result = evaluate_day60_outcome_diagnostics(self._summary(accepted_rows=[row]))
        finding = result["diagnostic_findings"][0]

        self.assertEqual(finding["evidence_used"], row["evidence_refs"])
        self.assertEqual(finding["affected_setup_type"], "Clean Fast Break")
        self.assertEqual(finding["affected_symbol"], "QQQ")
        self.assertEqual(finding["affected_stage"], "triggering")
        relationship = finding["trigger_invalidation_freshness_relationship"]
        self.assertEqual(relationship["trigger_reference"], row["trigger_reference"])
        self.assertEqual(relationship["invalidation_reference"], row["invalidation_reference"])
        self.assertEqual(relationship["stale_spent_outcome"], "fresh")

    def test_missing_or_unavailable_evidence_remains_explicit(self):
        unavailable_item = {
            "field_name": "time_to_failure",
            "status": "unavailable",
            "reason": "caller did not provide source-backed proof value",
            "fabricated": False,
        }
        row = self._accepted_row(
            review_bucket="unavailable_evidence",
            evidence_refs=[],
            unavailable_fields=[unavailable_item],
        )

        result = evaluate_day60_outcome_diagnostics(
            self._summary(
                accepted_rows=[row],
                unavailable_outcome_fields=[
                    {
                        "row_id": "outcome-row-1",
                        "field_name": "time_to_failure",
                        "status": "unavailable",
                        "reason": "caller did not provide source-backed proof value",
                        "fabricated": False,
                        "missing_from_row": True,
                    }
                ],
            )
        )

        finding = result["diagnostic_findings"][0]
        self.assertEqual(finding["diagnostic_category"], "data_quality_or_missing_evidence")
        self.assertIn(unavailable_item, finding["unavailable_evidence"])
        self.assertTrue(
            any(item.get("field_name") == "evidence_refs" for item in result["unavailable_evidence"])
        )

    def test_likely_cause_candidates_are_candidates_only(self):
        result = evaluate_day60_outcome_diagnostics(self._summary())

        candidate = result["likely_cause_candidates"][0]
        self.assertEqual(candidate["label"], "candidate")
        self.assertIn("candidate:", candidate["candidate"])
        self.assertIn("evidence_basis", candidate)
        self.assertNotIn("root_cause", candidate)

    def test_each_diagnostic_gap_maps_to_next_fix_path(self):
        result = evaluate_day60_outcome_diagnostics(self._summary())

        for finding in result["diagnostic_findings"]:
            category = finding["diagnostic_category"]
            self.assertEqual(
                finding["next_fix_path"],
                DAY60_OUTCOME_DIAGNOSTIC_FIX_PATHS[category],
            )
            self.assertEqual(
                result["next_fix_paths"][category],
                DAY60_OUTCOME_DIAGNOSTIC_FIX_PATHS[category],
            )

    def test_rejected_row_reasons_are_preserved(self):
        rejected_rows = [
            {
                "index": 1,
                "row_id": "bad-row",
                "reason": "Day 60 outcome scoring rows must preserve watch_only=True",
            }
        ]

        result = evaluate_day60_outcome_diagnostics(
            self._summary(rows_rejected=1, rejected_rows=rejected_rows)
        )

        self.assertEqual(result["rejected_rows"], rejected_rows)
        rejected_finding = [
            finding
            for finding in result["diagnostic_findings"]
            if finding["diagnostic_category"] == "review_logging_review"
        ][0]
        self.assertEqual(rejected_finding["evidence_used"], rejected_rows)

    def test_invalid_input_type_fails(self):
        with self.assertRaisesRegex(TypeError, "outcome_summary must be a dict"):
            evaluate_day60_outcome_diagnostics([])

    def test_missing_required_summary_field_fails(self):
        summary = self._summary()
        del summary["bucket_counts"]

        with self.assertRaisesRegex(ValueError, "bucket_counts"):
            evaluate_day60_outcome_diagnostics(summary)

    def test_boundary_flag_failure_fails(self):
        with self.assertRaisesRegex(ValueError, "optimization|live_data_started"):
            evaluate_day60_outcome_diagnostics(
                self._summary(live_data_started=True)
            )

    def test_forbidden_execution_field_fails_recursively(self):
        summary = self._summary()
        summary["accepted_rows"][0]["nested"] = {"trade_decision": "buy"}

        with self.assertRaisesRegex(ValueError, "Forbidden execution/trade field"):
            evaluate_day60_outcome_diagnostics(summary)

    def test_evaluator_returns_defensive_copies(self):
        summary = self._summary()
        before = copy.deepcopy(summary)

        result = evaluate_day60_outcome_diagnostics(summary)
        result["diagnostic_findings"][0]["evidence_used"].append("mutated")
        result["rejected_rows"].append({"row_id": "mutated"})

        self.assertEqual(summary, before)
        self.assertNotIn("mutated", summary["accepted_rows"][0]["evidence_refs"])
        self.assertEqual(summary["rejected_rows"], [])

    def test_evaluator_has_no_file_network_subprocess_or_live_side_effects(self):
        summary = self._summary()
        before = copy.deepcopy(summary)

        with patch("builtins.open") as open_mock, patch(
            "socket.socket"
        ) as socket_mock, patch("subprocess.run") as subprocess_mock:
            result = evaluate_day60_outcome_diagnostics(summary)

        self.assertEqual(summary, before)
        self.assertIs(result["live_data_started"], False)
        self.assertIs(result["alerts_sent"], False)
        self.assertIs(result["files_written"], False)
        self.assertIs(result["broker_or_trade_behavior_enabled"], False)
        open_mock.assert_not_called()
        socket_mock.assert_not_called()
        subprocess_mock.assert_not_called()

    def test_evaluator_does_not_start_watcher_loops_or_make_trade_decisions(self):
        result = evaluate_day60_outcome_diagnostics(self._summary())

        self.assertIs(result["watch_only"], True)
        self.assertIs(result["outcome_diagnostics_only"], True)
        self.assertIs(result["optimization_started"], False)
        self.assertIs(result["live_data_started"], False)
        self.assertIs(result["alerts_sent"], False)
        self.assertIs(result["broker_or_trade_behavior_enabled"], False)
        self.assertIs(result["no_trade_boundary_preserved"], True)


if __name__ == "__main__":
    unittest.main()
