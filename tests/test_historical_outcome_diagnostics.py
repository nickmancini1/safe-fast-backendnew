import copy
import unittest
from unittest.mock import patch

from watcher_foundation import (
    HISTORICAL_OUTCOME_DIAGNOSTICS_RESULT_FIELDS,
    HISTORICAL_OUTCOME_DIAGNOSTIC_FAILURE_CATEGORIES,
    HISTORICAL_OUTCOME_DIAGNOSTIC_FIX_PATHS,
    evaluate_historical_outcome_diagnostics,
)


class HistoricalOutcomeDiagnosticsTests(unittest.TestCase):
    def _unavailable_item(self, field_name):
        return {
            "field_name": field_name,
            "status": "unavailable",
            "reason": "caller did not provide source-backed proof value",
            "fabricated": False,
        }

    def _accepted_row(self, **overrides):
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
            "review_bucket": "partial_follow_through",
            "no_hindsight_boundary": {
                "evidence_available_at_or_before_review_timestamp": True,
                "future_evidence_not_used": True,
                "future_evidence_outside_declared_window_used": False,
                "no_backfilled_outcome_labels": True,
                "review_timestamp_field": "outcome_review_timestamp",
                "outcome_window_field": "outcome_window",
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

    def _summary(self, **overrides):
        accepted_rows = overrides.pop("accepted_rows", [self._accepted_row()])
        rejected_rows = overrides.pop("rejected_rows", [])
        unavailable_evidence = overrides.pop("unavailable_evidence", [])
        summary = {
            "watch_only": True,
            "historical_outcome_summary_only": True,
            "final_viability_proven": False,
            "rows_processed": len(accepted_rows) + len(rejected_rows),
            "rows_accepted": len(accepted_rows),
            "rows_rejected": len(rejected_rows),
            "accepted_rows": accepted_rows,
            "rejected_rows": rejected_rows,
            "bucket_counts": {
                "strong_follow_through": 0,
                "partial_follow_through": 0,
                "failed_trigger": 0,
                "stale_spent": 0,
                "blocked_correctly": 0,
                "blocked_incorrectly": 0,
                "inconclusive": 0,
                "unavailable_evidence": 0,
            },
            "unavailable_evidence": unavailable_evidence,
            "no_hindsight_boundary_preserved": True,
            "no_trade_boundary_preserved": True,
            "live_data_started": False,
            "controlled_shadow_data_started": False,
            "alerts_sent": False,
            "files_written": False,
            "broker_or_trade_behavior_enabled": False,
        }
        for row in accepted_rows:
            if type(row) is dict:
                bucket = row.get("review_bucket")
                if bucket in summary["bucket_counts"]:
                    summary["bucket_counts"][bucket] += 1
        summary.update(overrides)
        return summary

    def test_valid_summary_returns_in_memory_diagnostics_summary(self):
        result = evaluate_historical_outcome_diagnostics(self._summary())

        self.assertEqual(set(HISTORICAL_OUTCOME_DIAGNOSTICS_RESULT_FIELDS), set(result))
        self.assertIs(result["watch_only"], True)
        self.assertIs(result["historical_outcome_diagnostics_only"], True)
        self.assertIs(result["optimization_started"], False)
        self.assertEqual(result["rows_processed"], 1)
        self.assertEqual(result["rows_accepted"], 1)
        self.assertEqual(result["rows_rejected"], 0)

    def test_historical_categories_are_identified_without_fabricated_facts(self):
        rows = [
            self._accepted_row(outcome_row_id="strong", review_bucket="strong_follow_through"),
            self._accepted_row(outcome_row_id="failed", review_bucket="failed_trigger"),
            self._accepted_row(outcome_row_id="stale", review_bucket="stale_spent"),
            self._accepted_row(outcome_row_id="blocked", review_bucket="blocked_incorrectly"),
            self._accepted_row(outcome_row_id="inconclusive", review_bucket="inconclusive"),
            self._accepted_row(outcome_row_id="missing", review_bucket="unavailable_evidence"),
        ]

        result = evaluate_historical_outcome_diagnostics(
            self._summary(accepted_rows=rows)
        )
        categories = {
            finding["diagnostic_category"]
            for finding in result["diagnostic_findings"]
        }

        self.assertIn("trigger_level_or_zone_review", categories)
        self.assertIn("fresh_stale_spent_review", categories)
        self.assertIn("blocker_caution_review", categories)
        self.assertIn("outcome_scoring_review", categories)
        self.assertIn("data_quality_or_missing_evidence", categories)
        self.assertNotIn("strong_follow_through", categories)
        self.assertEqual(
            set(HISTORICAL_OUTCOME_DIAGNOSTIC_FAILURE_CATEGORIES),
            set(result["diagnostic_gap_counts"]),
        )
        self.assertFalse(
            any("asserted" in str(finding) for finding in result["diagnostic_findings"])
        )

    def test_evidence_and_affected_context_are_preserved(self):
        row = self._accepted_row(
            review_bucket="failed_trigger",
            symbol="QQQ",
            setup_type="Continuation",
            stage_at_detection="trigger-test",
            evidence_refs=["packet.row-9", {"source": "chart", "row": 9}],
            trigger_reference={"kind": "level", "value": "525.50", "fabricated": False},
            invalidation_reference={"kind": "zone", "value": "under shelf", "fabricated": False},
            stale_spent_outcome="fresh",
        )

        result = evaluate_historical_outcome_diagnostics(
            self._summary(accepted_rows=[row])
        )
        finding = result["diagnostic_findings"][0]

        self.assertEqual(finding["evidence_used"], row["evidence_refs"])
        self.assertEqual(finding["affected_setup_type"], "Continuation")
        self.assertEqual(finding["affected_symbol"], "QQQ")
        self.assertEqual(finding["affected_stage"], "trigger-test")
        relationship = finding["trigger_invalidation_freshness_relationship"]
        self.assertEqual(relationship["trigger_reference"], row["trigger_reference"])
        self.assertEqual(
            relationship["invalidation_reference"], row["invalidation_reference"]
        )
        self.assertEqual(relationship["stale_spent_outcome"], "fresh")

    def test_missing_or_unavailable_evidence_remains_explicit(self):
        row = self._accepted_row(
            review_bucket="unavailable_evidence",
            unavailable_fields=[self._unavailable_item("time_to_failure")],
            evidence_refs=[],
        )
        summary_unavailable = [
            {
                "row_id": "historical-proof-row-1",
                "field_name": "time_to_failure",
                "status": "unavailable",
                "reason": "caller did not provide source-backed proof value",
                "fabricated": False,
                "missing_from_row": False,
            }
        ]

        result = evaluate_historical_outcome_diagnostics(
            self._summary(accepted_rows=[row], unavailable_evidence=summary_unavailable)
        )

        self.assertIn(summary_unavailable[0], result["unavailable_evidence"])
        row_finding = result["diagnostic_findings"][0]
        self.assertIn(
            self._unavailable_item("time_to_failure"),
            row_finding["unavailable_evidence"],
        )
        self.assertIn(
            {
                "field_name": "evidence_refs",
                "status": "unavailable",
                "reason": "no evidence_refs were present for this diagnostic finding",
            },
            row_finding["unavailable_evidence"],
        )

    def test_diagnostic_gaps_map_to_next_fix_paths(self):
        result = evaluate_historical_outcome_diagnostics(
            self._summary(
                accepted_rows=[
                    self._accepted_row(review_bucket="failed_trigger"),
                    self._accepted_row(review_bucket="stale_spent"),
                ]
            )
        )

        self.assertEqual(
            result["next_fix_paths"]["trigger_level_or_zone_review"],
            HISTORICAL_OUTCOME_DIAGNOSTIC_FIX_PATHS[
                "trigger_level_or_zone_review"
            ],
        )
        self.assertEqual(
            result["next_fix_paths"]["fresh_stale_spent_review"],
            HISTORICAL_OUTCOME_DIAGNOSTIC_FIX_PATHS["fresh_stale_spent_review"],
        )

    def test_likely_causes_are_candidates_only(self):
        result = evaluate_historical_outcome_diagnostics(self._summary())

        self.assertTrue(result["likely_cause_candidates"])
        for candidate in result["likely_cause_candidates"]:
            self.assertEqual(candidate["label"], "candidate")
            self.assertTrue(candidate["candidate"].startswith("candidate:"))
            self.assertNotIn("fact", candidate)

    def test_rejected_row_reasons_are_preserved(self):
        rejected_rows = [
            {
                "index": 1,
                "row_id": "bad-row",
                "reason": "Missing required historical outcome proof preflight fields",
            }
        ]

        result = evaluate_historical_outcome_diagnostics(
            self._summary(rejected_rows=rejected_rows)
        )

        self.assertEqual(result["rejected_rows"], rejected_rows)
        rejected_finding = result["diagnostic_findings"][-1]
        self.assertEqual(rejected_finding["diagnostic_category"], "review_logging_review")
        self.assertEqual(rejected_finding["evidence_used"], rejected_rows)

    def test_invalid_input_type_fails(self):
        with self.assertRaisesRegex(TypeError, "historical_summary must be a dict"):
            evaluate_historical_outcome_diagnostics([])

    def test_missing_required_summary_field_fails(self):
        summary = self._summary()
        del summary["bucket_counts"]

        with self.assertRaisesRegex(ValueError, "Missing required"):
            evaluate_historical_outcome_diagnostics(summary)

    def test_boundary_flag_failure_fails(self):
        with self.assertRaisesRegex(ValueError, "watch_only=True"):
            evaluate_historical_outcome_diagnostics(self._summary(watch_only=False))

        with self.assertRaisesRegex(ValueError, "live_data_started=False"):
            evaluate_historical_outcome_diagnostics(
                self._summary(live_data_started=True)
            )

    def test_optimization_started_true_fails(self):
        with self.assertRaisesRegex(ValueError, "must not start optimization"):
            evaluate_historical_outcome_diagnostics(
                self._summary(optimization_started=True)
            )

    def test_forbidden_trade_decision_field_fails_recursively(self):
        summary = self._summary()
        summary["nested"] = {"proof": [{"trade_decision": "approve"}]}

        with self.assertRaisesRegex(ValueError, "Forbidden execution/trade field"):
            evaluate_historical_outcome_diagnostics(summary)

    def test_evaluator_returns_defensive_copies(self):
        summary = self._summary()
        before = copy.deepcopy(summary)

        result = evaluate_historical_outcome_diagnostics(summary)
        result["diagnostic_findings"][0]["evidence_used"].append("mutated")
        result["likely_cause_candidates"][0]["candidate"] = "mutated"
        result["rejected_rows"].append({"reason": "mutated"})

        self.assertEqual(summary, before)
        second_result = evaluate_historical_outcome_diagnostics(summary)
        self.assertNotIn("mutated", second_result["diagnostic_findings"][0]["evidence_used"])
        self.assertNotEqual(
            second_result["likely_cause_candidates"][0]["candidate"],
            "mutated",
        )
        self.assertEqual(second_result["rejected_rows"], [])

    def test_no_file_network_subprocess_loop_or_live_side_effects(self):
        summary = self._summary()
        before = copy.deepcopy(summary)

        with patch("builtins.open") as open_mock, patch(
            "socket.socket"
        ) as socket_mock, patch("subprocess.run") as subprocess_mock, patch(
            "threading.Thread"
        ) as thread_mock:
            result = evaluate_historical_outcome_diagnostics(summary)

        self.assertEqual(summary, before)
        self.assertIs(result["live_data_started"], False)
        self.assertIs(result["controlled_shadow_data_started"], False)
        self.assertIs(result["alerts_sent"], False)
        self.assertIs(result["files_written"], False)
        self.assertIs(result["broker_or_trade_behavior_enabled"], False)
        self.assertIs(result["no_trade_boundary_preserved"], True)
        self.assertIs(result["no_hindsight_boundary_preserved"], True)
        open_mock.assert_not_called()
        socket_mock.assert_not_called()
        subprocess_mock.assert_not_called()
        thread_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
