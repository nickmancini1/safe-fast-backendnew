import copy
import unittest
from unittest.mock import patch

from watcher_foundation import (
    SETUP_OUTCOME_PROOF_REVIEW_BUNDLE_READINESS_DECISIONS,
    SETUP_OUTCOME_PROOF_REVIEW_BUNDLE_READINESS_RESULT_FIELDS,
    evaluate_setup_outcome_proof_review_bundle_readiness,
)


class SetupOutcomeProofReviewBundleReadinessTests(unittest.TestCase):
    def _pattern(self, outcome_group, setup_type="Ideal", symbol="SPY"):
        return {
            "group_review_index": 0,
            "outcome_group": outcome_group,
            "count": 2,
            "represented_setup_types": [setup_type],
            "represented_symbols": [symbol],
            "represented_setup_type_symbol_pairs": [
                {"setup_type": setup_type, "symbol": symbol}
            ],
        }

    def _bundle(self, **overrides):
        bundle = {
            "watch_only": True,
            "setup_outcome_proof_review_bundle_only": True,
            "setup_outcome_review_readiness_only": True,
            "setup_outcome_review_aggregator_only": True,
            "setup_outcome_packet_readiness_only": True,
            "setup_outcome_evidence_packet_only": True,
            "setup_outcome_diagnostics_only": True,
            "setup_outcome_proof_only": True,
            "final_viability_proven": False,
            "optimization_started": False,
            "no_rule_change_started": True,
            "review_summary_count": 1,
            "included_group_review_count": 1,
            "included_group_reviews": [
                {
                    "group_review_index": 0,
                    "reviewed_packets": [
                        {
                            "packet_identifier": "packet-1",
                            "readiness_status": "ready_for_lower_tier_review",
                        }
                    ],
                    "packet_summary_count": 1,
                    "represented_setup_types": [
                        "Ideal",
                        "Clean Fast Break",
                        "Continuation",
                    ],
                    "represented_symbols": ["SPY", "QQQ", "IWM", "GLD"],
                    "represented_setup_type_symbol_pairs": [
                        {"setup_type": "Ideal", "symbol": "SPY"},
                        {"setup_type": "Clean Fast Break", "symbol": "QQQ"},
                        {"setup_type": "Continuation", "symbol": "IWM"},
                    ],
                    "outcome_group_counts": {
                        "worked": 2,
                        "failed": 2,
                        "inconclusive": 1,
                        "pending": 1,
                        "stale": 1,
                        "invalidated": 1,
                        "missing_evidence": 1,
                    },
                }
            ],
            "excluded_group_reviews": [],
            "represented_setup_types": [
                "Ideal",
                "Clean Fast Break",
                "Continuation",
            ],
            "setup_types_needing_more_evidence": [],
            "represented_symbols": ["SPY", "QQQ", "IWM", "GLD"],
            "symbols_needing_more_evidence": [],
            "represented_setup_type_symbol_pairs": [
                {"setup_type": "Ideal", "symbol": "SPY"},
                {"setup_type": "Clean Fast Break", "symbol": "QQQ"},
                {"setup_type": "Continuation", "symbol": "IWM"},
            ],
            "setup_type_symbol_pairs_needing_more_evidence": [],
            "outcome_group_counts": {
                "worked": 2,
                "failed": 2,
                "inconclusive": 1,
                "pending": 1,
                "stale": 1,
                "invalidated": 1,
                "missing_evidence": 1,
            },
            "worked_patterns": [self._pattern("worked")],
            "failed_patterns": [self._pattern("failed", "Ideal", "QQQ")],
            "inconclusive_patterns": [
                self._pattern("inconclusive", "Clean Fast Break", "SPY")
            ],
            "pending_patterns": [self._pattern("pending", "Continuation", "SPY")],
            "stale_patterns": [self._pattern("stale", "Clean Fast Break", "IWM")],
            "invalidated_patterns": [
                self._pattern("invalidated", "Continuation", "QQQ")
            ],
            "missing_evidence_patterns": [
                self._pattern("missing_evidence", "Ideal", "GLD")
            ],
            "repeated_worked_patterns": [
                {
                    "outcome_group": "worked",
                    "setup_type": "Ideal",
                    "symbol": "SPY",
                    "count": 2,
                }
            ],
            "repeated_failed_patterns": [
                {
                    "outcome_group": "failed",
                    "setup_type": "Ideal",
                    "symbol": "QQQ",
                    "count": 2,
                }
            ],
            "repeated_inconclusive_pending_stale_invalidated_or_missing_evidence_patterns": [],
            "missing_evidence": [],
            "missing_evidence_by_setup_type": {},
            "missing_evidence_by_symbol": {},
            "missing_evidence_by_setup_type_symbol_pair": [],
            "repeated_fix_paths": {
                "return to setup outcome evidence packet regression review": 2
            },
            "repeated_regression_needs": {
                "add regression coverage preserving bundle readiness gaps": 2
            },
            "required_regression_tests": [
                "add regression test coverage preserving bundle readiness gaps"
            ],
            "missing_regression_coverage": [],
            "proof_gaps": [],
            "bundle_contract_gaps": [],
            "lower_tier_handoff_required": False,
            "lower_tier_handoff_items": [],
            "ready_for_lower_tier_review": True,
            "bundle_review_decision": "ready_for_lower_tier_review",
            "setup_type_separated": True,
            "symbol_separated": True,
            "proof_review_only": True,
            "no_hindsight_boundary_preserved": True,
            "no_trade_boundary_preserved": True,
            "no_live_data_boundary_preserved": True,
            "no_controlled_shadow_boundary_preserved": True,
            "no_alert_boundary_preserved": True,
            "no_file_write_boundary_preserved": True,
            "no_broker_boundary_preserved": True,
            "no_optimization_boundary_preserved": True,
            "no_trade_or_optimization_boundary_preserved": True,
            "live_data_started": False,
            "controlled_shadow_data_started": False,
            "alerts_sent": False,
            "files_written": False,
            "broker_or_trade_behavior_enabled": False,
        }
        bundle.update(overrides)
        return bundle

    def test_accepts_one_in_memory_historical_proof_bundle_summary(self):
        result = evaluate_setup_outcome_proof_review_bundle_readiness(
            self._bundle()
        )

        self.assertEqual(
            set(SETUP_OUTCOME_PROOF_REVIEW_BUNDLE_READINESS_RESULT_FIELDS),
            set(result),
        )
        self.assertIn(
            result["bundle_readiness_decision"],
            SETUP_OUTCOME_PROOF_REVIEW_BUNDLE_READINESS_DECISIONS,
        )
        self.assertIs(result["watch_only"], True)
        self.assertIs(
            result["setup_outcome_proof_review_bundle_readiness_only"],
            True,
        )
        self.assertIs(result["setup_outcome_proof_review_bundle_only"], True)
        self.assertIs(result["setup_outcome_review_readiness_only"], True)
        self.assertIs(result["setup_outcome_review_aggregator_only"], True)
        self.assertIs(result["setup_outcome_packet_readiness_only"], True)
        self.assertIs(result["setup_outcome_evidence_packet_only"], True)
        self.assertIs(result["setup_outcome_diagnostics_only"], True)
        self.assertIs(result["setup_outcome_proof_only"], True)
        self.assertIs(result["final_viability_proven"], False)
        self.assertIs(result["optimization_started"], False)
        self.assertIs(result["no_rule_change_started"], True)

    def test_invalid_input_type_missing_and_unexpected_fields_fail(self):
        with self.assertRaisesRegex(TypeError, "input must be a dict"):
            evaluate_setup_outcome_proof_review_bundle_readiness([])

        bundle = self._bundle()
        del bundle["included_group_reviews"]
        with self.assertRaisesRegex(ValueError, "included_group_reviews"):
            evaluate_setup_outcome_proof_review_bundle_readiness(bundle)

        bundle = self._bundle()
        bundle["extra_raw_log_path"] = "not allowed"
        with self.assertRaisesRegex(ValueError, "Unexpected"):
            evaluate_setup_outcome_proof_review_bundle_readiness(bundle)

    def test_required_boundaries_are_enforced(self):
        required_failures = {
            "watch_only": False,
            "setup_outcome_proof_review_bundle_only": False,
            "setup_outcome_review_readiness_only": False,
            "setup_outcome_review_aggregator_only": False,
            "setup_outcome_packet_readiness_only": False,
            "setup_outcome_evidence_packet_only": False,
            "setup_outcome_diagnostics_only": False,
            "setup_outcome_proof_only": False,
            "final_viability_proven": True,
            "optimization_started": True,
            "no_rule_change_started": False,
            "proof_review_only": False,
            "no_hindsight_boundary_preserved": False,
            "no_trade_boundary_preserved": False,
            "no_live_data_boundary_preserved": False,
            "no_controlled_shadow_boundary_preserved": False,
            "no_alert_boundary_preserved": False,
            "no_file_write_boundary_preserved": False,
            "no_broker_boundary_preserved": False,
            "no_optimization_boundary_preserved": False,
            "no_trade_or_optimization_boundary_preserved": False,
            "live_data_started": True,
            "controlled_shadow_data_started": True,
            "alerts_sent": True,
            "files_written": True,
            "broker_or_trade_behavior_enabled": True,
        }

        for field_name, value in required_failures.items():
            bundle = self._bundle()
            bundle[field_name] = value
            with self.subTest(field_name=field_name):
                with self.assertRaisesRegex(ValueError, field_name):
                    evaluate_setup_outcome_proof_review_bundle_readiness(bundle)

    def test_ready_decision_requires_complete_review_evidence(self):
        result = evaluate_setup_outcome_proof_review_bundle_readiness(
            self._bundle()
        )

        self.assertIs(result["bundle_complete_enough_to_review"], True)
        self.assertIs(result["ready_for_lower_tier_review"], True)
        self.assertEqual(result["exact_missing_review_items"], [])
        self.assertEqual(
            result["bundle_readiness_decision"],
            "ready_for_lower_tier_review",
        )
        self.assertIs(result["setup_type_evidence_complete"], True)
        self.assertIs(result["symbol_evidence_complete"], True)
        self.assertIs(result["setup_type_symbol_pair_evidence_complete"], True)
        self.assertIs(result["worked_patterns_clear_enough"], True)
        self.assertIs(result["failed_patterns_clear_enough"], True)
        self.assertIs(result["repeated_fix_paths_clear_enough"], True)
        self.assertIs(result["regression_coverage_named"], True)
        self.assertNotIn("profit", str(result).lower())
        self.assertNotIn("final_viability_success", result)

    def test_identifies_missing_setup_symbol_and_pair_evidence_separately(self):
        result = evaluate_setup_outcome_proof_review_bundle_readiness(
            self._bundle(
                setup_types_needing_more_evidence=["Continuation"],
                symbols_needing_more_evidence=["GLD"],
                setup_type_symbol_pairs_needing_more_evidence=[
                    {"setup_type": "Continuation", "symbol": "GLD"}
                ],
                missing_evidence=[
                    {
                        "setup_type": "Continuation",
                        "symbol": "GLD",
                        "field_name": "post_setup_evidence",
                    }
                ],
                missing_evidence_by_setup_type={
                    "Continuation": [{"field_name": "post_setup_evidence"}]
                },
                missing_evidence_by_symbol={
                    "GLD": [{"field_name": "post_setup_evidence"}]
                },
                missing_evidence_by_setup_type_symbol_pair=[
                    {
                        "setup_type": "Continuation",
                        "symbol": "GLD",
                        "missing_evidence": [
                            {"field_name": "post_setup_evidence"}
                        ],
                    }
                ],
                ready_for_lower_tier_review=False,
                bundle_review_decision="needs_more_evidence_before_lower_tier_review",
            )
        )

        self.assertIs(result["setup_type_evidence_complete"], False)
        self.assertEqual(result["setup_types_needing_more_evidence"], ["Continuation"])
        self.assertIs(result["symbol_evidence_complete"], False)
        self.assertEqual(result["symbols_needing_more_evidence"], ["GLD"])
        self.assertIs(result["setup_type_symbol_pair_evidence_complete"], False)
        self.assertEqual(
            result["setup_type_symbol_pairs_needing_more_evidence"],
            [{"setup_type": "Continuation", "symbol": "GLD"}],
        )
        self.assertIn(
            "setup_type_needs_more_evidence",
            str(result["exact_missing_review_items"]),
        )
        self.assertIn(
            "setup_type_symbol_pair_needs_more_evidence",
            str(result["exact_missing_review_items"]),
        )
        self.assertEqual(
            result["bundle_readiness_decision"],
            "needs_more_evidence_before_lower_tier_review",
        )

    def test_identifies_unclear_worked_failed_and_repeated_fix_paths(self):
        result = evaluate_setup_outcome_proof_review_bundle_readiness(
            self._bundle(
                worked_patterns=[],
                failed_patterns=[
                    {
                        "outcome_group": "failed",
                        "count": 1,
                        "represented_setup_types": ["Ideal"],
                        "represented_symbols": [],
                        "represented_setup_type_symbol_pairs": [],
                    }
                ],
                repeated_fix_paths={"fix later": 2},
                ready_for_lower_tier_review=False,
                bundle_review_decision="needs_more_evidence_before_lower_tier_review",
            )
        )

        self.assertIs(result["worked_patterns_clear_enough"], False)
        self.assertTrue(result["unclear_worked_patterns"])
        self.assertIs(result["failed_patterns_clear_enough"], False)
        self.assertTrue(result["unclear_failed_patterns"])
        self.assertIs(result["repeated_fix_paths_clear_enough"], False)
        self.assertTrue(result["unclear_repeated_fix_paths"])
        self.assertFalse(result["ready_for_lower_tier_review"])

    def test_requires_named_regressions_when_proof_gaps_remain(self):
        result = evaluate_setup_outcome_proof_review_bundle_readiness(
            self._bundle(
                proof_gaps=[
                    {
                        "gap_type": "proof_gap",
                        "field_name": "outcome_evidence",
                        "reason": "post setup evidence unavailable",
                    }
                ],
                required_regression_tests=[],
                ready_for_lower_tier_review=False,
                bundle_review_decision="needs_more_evidence_before_lower_tier_review",
            )
        )

        self.assertIs(result["proof_gaps_blocking_review"], True)
        self.assertIs(result["regression_coverage_named"], False)
        self.assertTrue(result["missing_regression_coverage"])
        self.assertFalse(result["bundle_complete_enough_to_review"])

    def test_bundle_contract_gaps_block_review(self):
        result = evaluate_setup_outcome_proof_review_bundle_readiness(
            self._bundle(
                review_summary_count=0,
                included_group_review_count=0,
                included_group_reviews=[],
                represented_setup_types=[],
                represented_symbols=[],
                represented_setup_type_symbol_pairs=[],
                bundle_contract_gaps=[
                    {
                        "gap_type": "bundle_contract_gap",
                        "field_name": "included_group_reviews",
                        "reason": "no included group reviews",
                    }
                ],
                ready_for_lower_tier_review=False,
                bundle_review_decision="blocked_by_bundle_contract_gap",
                setup_type_separated=False,
                symbol_separated=False,
            )
        )

        self.assertIs(result["bundle_contract_gaps_blocking_review"], True)
        self.assertTrue(result["bundle_readiness_contract_gaps"])
        self.assertEqual(
            result["bundle_readiness_decision"],
            "blocked_by_bundle_readiness_contract_gap",
        )
        self.assertIn(
            "included_group_reviews",
            str(result["exact_missing_review_items"]),
        )

    def test_rejects_forbidden_execution_fields(self):
        forbidden_cases = (
            {"nested": {"broker_order": "blocked"}},
            {"nested": {"option_pnl": 10}},
            {"nested": {"account_sizing": "blocked"}},
            {"nested": {"live_trade_decision": "approve"}},
        )

        for forbidden in forbidden_cases:
            bundle = self._bundle()
            bundle["included_group_reviews"][0].update(forbidden)
            with self.subTest(forbidden=forbidden):
                with self.assertRaisesRegex(
                    ValueError,
                    "Forbidden execution/trade field",
                ):
                    evaluate_setup_outcome_proof_review_bundle_readiness(bundle)

    def test_defensive_copy_behavior(self):
        bundle = self._bundle()
        before = copy.deepcopy(bundle)

        result = evaluate_setup_outcome_proof_review_bundle_readiness(bundle)
        result["included_group_reviews"][0]["reviewed_packets"][0][
            "readiness_status"
        ] = "MUTATED"
        result["represented_setup_types"].append("MUTATED")
        result["worked_patterns"][0]["represented_symbols"].append("MUTATED")

        self.assertEqual(bundle, before)
        second = evaluate_setup_outcome_proof_review_bundle_readiness(bundle)
        self.assertEqual(
            second["included_group_reviews"][0]["reviewed_packets"][0][
                "readiness_status"
            ],
            "ready_for_lower_tier_review",
        )
        self.assertNotIn("MUTATED", second["represented_setup_types"])

    def test_no_file_network_subprocess_thread_or_live_side_effects(self):
        bundle = self._bundle()
        before = copy.deepcopy(bundle)

        with patch("builtins.open") as open_mock, patch(
            "socket.socket"
        ) as socket_mock, patch("subprocess.run") as subprocess_mock, patch(
            "threading.Thread"
        ) as thread_mock:
            result = evaluate_setup_outcome_proof_review_bundle_readiness(bundle)

        self.assertEqual(bundle, before)
        self.assertIs(result["proof_review_only"], True)
        self.assertIs(result["no_hindsight_boundary_preserved"], True)
        self.assertIs(result["no_trade_boundary_preserved"], True)
        self.assertIs(result["no_live_data_boundary_preserved"], True)
        self.assertIs(result["no_controlled_shadow_boundary_preserved"], True)
        self.assertIs(result["no_alert_boundary_preserved"], True)
        self.assertIs(result["no_file_write_boundary_preserved"], True)
        self.assertIs(result["no_broker_boundary_preserved"], True)
        self.assertIs(result["no_optimization_boundary_preserved"], True)
        self.assertIs(result["live_data_started"], False)
        self.assertIs(result["controlled_shadow_data_started"], False)
        self.assertIs(result["alerts_sent"], False)
        self.assertIs(result["files_written"], False)
        self.assertIs(result["broker_or_trade_behavior_enabled"], False)
        open_mock.assert_not_called()
        socket_mock.assert_not_called()
        subprocess_mock.assert_not_called()
        thread_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
