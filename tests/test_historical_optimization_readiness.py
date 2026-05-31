import copy
import unittest
from unittest.mock import patch

from watcher_foundation import (
    HISTORICAL_OPTIMIZATION_ALLOWED_SYSTEM_AREAS,
    HISTORICAL_OPTIMIZATION_READINESS_REQUIRED_FIELDS,
    HISTORICAL_OPTIMIZATION_READINESS_RESULT_FIELDS,
    evaluate_historical_optimization_readiness,
)


class HistoricalOptimizationReadinessTests(unittest.TestCase):
    def _finding(self, **overrides):
        finding = {
            "diagnostic_category": "trigger_level_or_zone_review",
            "row_id": "historical-diagnostic-row-1",
            "affected_setup_type": "Ideal",
            "affected_symbol": "SPY",
            "affected_stage": "near-trigger",
            "trigger_invalidation_freshness_relationship": {
                "trigger_reference": {
                    "kind": "caller_provided_chart_reference",
                    "value": "432 reclaim zone",
                    "fabricated": False,
                },
                "trigger_status_at_detection": "near_trigger",
                "invalidation_reference": {
                    "kind": "caller_provided_chart_reference",
                    "value": "below local shelf",
                    "fabricated": False,
                },
                "stale_spent_outcome": "not_stale_or_spent",
            },
            "affected_system_area": "trigger_level_or_zone",
            "evidence_used": ["review-packet-1.accepted_rows[0]", "chart-row-218"],
            "unavailable_evidence": [],
            "likely_cause_candidates": [
                {
                    "label": "candidate",
                    "candidate": "candidate: trigger level evidence may need review",
                    "evidence_basis": {
                        "evidence_used": [
                            "review-packet-1.accepted_rows[0]",
                            "chart-row-218",
                        ],
                        "unavailable_evidence": [],
                    },
                }
            ],
            "next_fix_path": "review trigger level evidence before any rule change",
            "regression_test_path": (
                "tests/test_historical_trigger_level_or_zone_regression.py"
            ),
            "no_trade_boundary_preserved": True,
        }
        finding.update(overrides)
        return finding

    def _summary(self, **overrides):
        summary = {
            "watch_only": True,
            "historical_outcome_diagnostics_only": True,
            "optimization_started": False,
            "rows_processed": 1,
            "rows_accepted": 1,
            "rows_rejected": 0,
            "diagnostic_findings": [self._finding()],
            "diagnostic_gap_counts": {"trigger_level_or_zone_review": 1},
            "likely_cause_candidates": [
                {
                    "label": "candidate",
                    "candidate": "candidate: trigger level evidence may need review",
                    "evidence_basis": {"evidence_used": ["chart-row-218"]},
                }
            ],
            "next_fix_paths": {
                "trigger_level_or_zone_review": (
                    "review trigger level evidence before any rule change"
                )
            },
            "unavailable_evidence": [],
            "rejected_rows": [],
            "no_hindsight_boundary_preserved": True,
            "no_trade_boundary_preserved": True,
            "live_data_started": False,
            "controlled_shadow_data_started": False,
            "alerts_sent": False,
            "files_written": False,
            "broker_or_trade_behavior_enabled": False,
        }
        summary.update(overrides)
        return summary

    def test_valid_historical_diagnostics_summary_returns_in_memory_readiness_summary(self):
        result = evaluate_historical_optimization_readiness(self._summary())

        self.assertEqual(set(HISTORICAL_OPTIMIZATION_READINESS_RESULT_FIELDS), set(result))
        self.assertIs(result["watch_only"], True)
        self.assertIs(result["historical_optimization_readiness_only"], True)
        self.assertIs(result["optimization_started"], False)
        self.assertIs(result["ready_for_optimization"], True)
        self.assertEqual(result["rows_processed"], 1)
        self.assertEqual(result["diagnostic_findings_reviewed"], 1)
        item = result["readiness_items"][0]
        self.assertEqual(item["affected_setup_type"], "Ideal")
        self.assertEqual(item["affected_symbol"], "SPY")
        self.assertEqual(item["affected_stage"], "near-trigger")
        self.assertEqual(
            item["trigger_invalidation_freshness_relationship"][
                "trigger_status_at_detection"
            ],
            "near_trigger",
        )

    def test_required_public_constants_cover_readiness_contract(self):
        for field_name in (
            "diagnosed_failure_category",
            "evidence_or_explicit_unavailable",
            "affected_system_area",
            "next_fix_path",
            "regression_test_path",
            "no_trade_boundary_preserved",
        ):
            self.assertIn(field_name, HISTORICAL_OPTIMIZATION_READINESS_REQUIRED_FIELDS)
        for area in (
            "setup_recognition",
            "stage_transition",
            "trigger_card",
            "trigger_level_or_zone",
            "invalidation",
            "fresh_stale_spent",
            "blocker_caution",
            "duplicate_suppression",
            "ranking_focus",
            "session_boundary",
            "data_quality",
            "market_context",
            "outcome_scoring",
            "review_logging",
            "user_facing_workflow",
        ):
            self.assertIn(area, HISTORICAL_OPTIMIZATION_ALLOWED_SYSTEM_AREAS)

    def test_ready_for_optimization_true_only_when_all_required_fields_exist(self):
        ready = evaluate_historical_optimization_readiness(self._summary())
        self.assertIs(ready["ready_for_optimization"], True)

        blocked = evaluate_historical_optimization_readiness(
            self._summary(
                diagnostic_findings=[
                    self._finding(),
                    self._finding(row_id="missing-path", regression_test_path=""),
                ]
            )
        )

        self.assertIs(blocked["ready_for_optimization"], False)
        self.assertEqual(len(blocked["blocked_items"]), 1)

    def test_missing_failure_category_blocks_readiness(self):
        finding = self._finding()
        del finding["diagnostic_category"]

        result = evaluate_historical_optimization_readiness(
            self._summary(diagnostic_findings=[finding])
        )

        self.assertIs(result["ready_for_optimization"], False)
        self.assertIn(
            "diagnosed failure category is missing",
            result["blocked_items"][0]["blocked_reasons"],
        )

    def test_missing_evidence_without_explicit_unavailable_marker_blocks_readiness(self):
        result = evaluate_historical_optimization_readiness(
            self._summary(
                diagnostic_findings=[
                    self._finding(evidence_used=[], unavailable_evidence=[])
                ]
            )
        )

        self.assertIs(result["ready_for_optimization"], False)
        self.assertEqual(len(result["missing_evidence_items"]), 1)

    def test_explicit_unavailable_evidence_marker_satisfies_evidence_requirement(self):
        result = evaluate_historical_optimization_readiness(
            self._summary(
                diagnostic_findings=[
                    self._finding(
                        evidence_used=[],
                        unavailable_evidence=[
                            {
                                "field_name": "evidence_refs",
                                "status": "unavailable",
                                "reason": "caller did not provide source-backed proof",
                            }
                        ],
                    )
                ]
            )
        )

        self.assertIs(result["ready_for_optimization"], True)
        self.assertEqual(result["missing_evidence_items"], [])

    def test_missing_affected_system_area_blocks_readiness(self):
        result = evaluate_historical_optimization_readiness(
            self._summary(diagnostic_findings=[self._finding(affected_system_area="")])
        )

        self.assertIs(result["ready_for_optimization"], False)
        self.assertIn(
            "affected system area is missing or unsupported",
            result["blocked_items"][0]["blocked_reasons"],
        )

    def test_missing_next_fix_path_blocks_readiness(self):
        result = evaluate_historical_optimization_readiness(
            self._summary(diagnostic_findings=[self._finding(next_fix_path="")])
        )

        self.assertIs(result["ready_for_optimization"], False)
        self.assertIn(
            "next fix path is missing",
            result["blocked_items"][0]["blocked_reasons"],
        )

    def test_missing_regression_test_path_blocks_readiness(self):
        result = evaluate_historical_optimization_readiness(
            self._summary(diagnostic_findings=[self._finding(regression_test_path="")])
        )

        self.assertIs(result["ready_for_optimization"], False)
        self.assertIn(
            "regression test path is missing",
            result["blocked_items"][0]["blocked_reasons"],
        )

    def test_shallow_labels_are_rejected_without_evidence(self):
        for shallow_label in ("failed setup", "bad alert", "weak signal", "bad trade"):
            with self.subTest(shallow_label=shallow_label):
                with self.assertRaisesRegex(ValueError, "shallow optimization labels"):
                    evaluate_historical_optimization_readiness(
                        self._summary(
                            diagnostic_findings=[
                                self._finding(
                                    diagnostic_category=shallow_label,
                                    evidence_used=[],
                                    unavailable_evidence=[],
                                    next_fix_path="",
                                )
                            ]
                        )
                    )

    def test_optimization_started_remains_false(self):
        result = evaluate_historical_optimization_readiness(self._summary())

        self.assertIs(result["optimization_started"], False)
        self.assertIs(result["historical_optimization_readiness_only"], True)

    def test_invalid_input_type_fails(self):
        with self.assertRaisesRegex(
            TypeError,
            "historical_diagnostics_summary must be a dict",
        ):
            evaluate_historical_optimization_readiness([])

    def test_missing_required_diagnostics_field_fails(self):
        summary = self._summary()
        del summary["diagnostic_gap_counts"]

        with self.assertRaisesRegex(ValueError, "diagnostic_gap_counts"):
            evaluate_historical_optimization_readiness(summary)

    def test_boundary_flag_failure_fails(self):
        with self.assertRaisesRegex(ValueError, "live_data_started=False"):
            evaluate_historical_optimization_readiness(
                self._summary(live_data_started=True)
            )

    def test_optimization_started_input_failure_fails(self):
        with self.assertRaisesRegex(ValueError, "optimization_started=False"):
            evaluate_historical_optimization_readiness(
                self._summary(optimization_started=True)
            )

    def test_forbidden_broker_order_account_options_pnl_trade_field_fails_recursively(self):
        forbidden_fields = (
            "broker",
            "order",
            "account",
            "option_pnl",
            "trade_decision",
        )
        for forbidden_field in forbidden_fields:
            with self.subTest(forbidden_field=forbidden_field):
                summary = self._summary()
                summary["diagnostic_findings"][0]["nested"] = {forbidden_field: "x"}

                with self.assertRaisesRegex(
                    ValueError,
                    "Forbidden execution/trade field",
                ):
                    evaluate_historical_optimization_readiness(summary)

    def test_likely_causes_must_remain_candidate_language(self):
        with self.assertRaisesRegex(ValueError, "candidate language"):
            evaluate_historical_optimization_readiness(
                self._summary(
                    diagnostic_findings=[
                        self._finding(
                            likely_cause_candidates=[
                                {"label": "root_cause", "candidate": "confirmed cause"}
                            ]
                        )
                    ]
                )
            )

    def test_evaluator_returns_defensive_copies(self):
        summary = self._summary()
        before = copy.deepcopy(summary)

        result = evaluate_historical_optimization_readiness(summary)
        result["readiness_items"][0]["next_fix_path"] = "mutated"
        result["blocked_items"].append({"row_id": "mutated"})
        result["regression_test_paths"].append("mutated")

        self.assertEqual(summary, before)
        self.assertEqual(
            summary["diagnostic_findings"][0]["next_fix_path"],
            "review trigger level evidence before any rule change",
        )
        second_result = evaluate_historical_optimization_readiness(summary)
        self.assertNotIn("mutated", second_result["regression_test_paths"])

    def test_evaluator_writes_no_files_logs_reports_or_fetches_data(self):
        summary = self._summary()
        before = copy.deepcopy(summary)

        with patch("builtins.open") as open_mock, patch(
            "socket.socket"
        ) as socket_mock, patch("subprocess.run") as subprocess_mock:
            result = evaluate_historical_optimization_readiness(summary)

        self.assertEqual(summary, before)
        self.assertIs(result["files_written"], False)
        open_mock.assert_not_called()
        socket_mock.assert_not_called()
        subprocess_mock.assert_not_called()

    def test_evaluator_starts_no_live_or_controlled_shadow_data(self):
        result = evaluate_historical_optimization_readiness(self._summary())

        self.assertIs(result["live_data_started"], False)
        self.assertIs(result["controlled_shadow_data_started"], False)

    def test_evaluator_creates_no_watcher_loops(self):
        with patch("threading.Thread") as thread_mock:
            result = evaluate_historical_optimization_readiness(self._summary())

        self.assertIs(result["watch_only"], True)
        thread_mock.assert_not_called()

    def test_evaluator_sends_no_alerts(self):
        result = evaluate_historical_optimization_readiness(self._summary())

        self.assertIs(result["alerts_sent"], False)

    def test_evaluator_touches_no_broker_order_account_options_pnl_systems(self):
        result = evaluate_historical_optimization_readiness(self._summary())

        self.assertIs(result["broker_or_trade_behavior_enabled"], False)
        self.assertIs(result["no_trade_boundary_preserved"], True)

    def test_evaluator_makes_no_live_trade_decisions(self):
        result = evaluate_historical_optimization_readiness(self._summary())

        self.assertIs(result["watch_only"], True)
        self.assertIs(result["historical_optimization_readiness_only"], True)
        self.assertIs(result["optimization_started"], False)
        self.assertIs(result["broker_or_trade_behavior_enabled"], False)


if __name__ == "__main__":
    unittest.main()
