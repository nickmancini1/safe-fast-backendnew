import copy
import unittest
from unittest.mock import patch

from watcher_foundation import (
    SETUP_OUTCOME_DIAGNOSTICS_RESULT_FIELDS,
    SETUP_OUTCOME_DIAGNOSTIC_FAILURE_CATEGORIES,
    SETUP_OUTCOME_DIAGNOSTIC_FIX_PATHS,
    evaluate_setup_outcome_diagnostics,
    evaluate_setup_outcome_proof,
)


class SetupOutcomeDiagnosticsTests(unittest.TestCase):
    def _unavailable_item(self, field_name):
        return {
            "field_name": field_name,
            "status": "unavailable_evidence",
            "reason": "caller did not provide source-backed setup outcome evidence",
            "fabricated": False,
        }

    def _record(self, **overrides):
        record = {
            "proof_record_id": "proof-row-1",
            "source_record_id": "detected-row-1",
            "setup_id": "setup-1",
            "setup_type": "Ideal",
            "symbol": "SPY",
            "timeframe": "1h_rth",
            "stage": "near-trigger",
            "detection_timestamp": "2026-05-24T09:35:00-04:00",
            "frozen_setup_identity": {
                "caller_provided": True,
                "frozen_before_outcome_scan": True,
                "setup_id": "setup-1",
                "setup_type": "Ideal",
                "symbol": "SPY",
                "frozen_timestamp": "2026-05-24T09:35:00-04:00",
            },
            "setup_evidence_refs": ["detected-row-1", "setup-chart-row-218"],
            "after_setup_evidence": {
                "caller_provided": True,
                "start_timestamp": "2026-05-24T10:30:00-04:00",
                "end_timestamp": "2026-05-25T16:00:00-04:00",
                "source_row_reference": "chart-row-219",
                "post_setup_evidence": ["chart-row-219", "chart-row-220"],
                "future_evidence_used_to_define_setup": False,
            },
            "trigger_state": "triggered",
            "invalidation_state": "valid_by_rule",
            "freshness_state": "fresh",
            "blocker_caution_state": "none",
            "session_boundary_state": "valid_by_rule",
            "outcome_evidence_state": "valid_by_rule",
            "outcome_result_state": "worked",
            "evidence_refs": ["detected-row-1", "chart-row-219"],
            "unavailable_fields": [],
            "diagnostic_placeholders": {
                "next_fix_path": "review outcome proof contract if evidence is incomplete",
                "lower_tier_handoff": "not_required_for_complete_evidence",
            },
            "no_hindsight_boundary": {
                "setup_identity_frozen_before_outcome_scan": True,
                "future_evidence_not_used_to_define_setup": True,
                "no_backfilled_outcome_labels": True,
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
        record.update(overrides)
        return record

    def _summary(self, records=None):
        if records is None:
            records = [self._record()]
        return evaluate_setup_outcome_proof(records)

    def _single_finding(self, record):
        result = evaluate_setup_outcome_diagnostics(self._summary([record]))
        return result["diagnostic_findings"][0]

    def test_accepts_only_in_memory_setup_outcome_proof_summary_shape(self):
        result = evaluate_setup_outcome_diagnostics(self._summary())

        self.assertEqual(set(SETUP_OUTCOME_DIAGNOSTICS_RESULT_FIELDS), set(result))
        self.assertIs(result["watch_only"], True)
        self.assertIs(result["setup_outcome_diagnostics_only"], True)
        self.assertIs(result["setup_outcome_proof_only"], True)
        self.assertIs(result["final_viability_proven"], False)
        self.assertIs(result["optimization_started"], False)
        self.assertEqual(result["records_processed"], 1)
        self.assertEqual(result["records_accepted"], 1)

    def test_invalid_input_type_and_missing_proof_field_fail(self):
        with self.assertRaisesRegex(TypeError, "proof_summary must be a dict"):
            evaluate_setup_outcome_diagnostics([])

        summary = self._summary()
        del summary["accepted_records_by_setup_type"]

        with self.assertRaisesRegex(ValueError, "accepted_records_by_setup_type"):
            evaluate_setup_outcome_diagnostics(summary)

    def test_required_boundaries_are_enforced(self):
        required_failures = {
            "watch_only": False,
            "setup_outcome_proof_only": False,
            "final_viability_proven": True,
            "optimization_started": True,
            "live_data_started": True,
            "controlled_shadow_data_started": True,
            "alerts_sent": True,
            "files_written": True,
            "broker_or_trade_behavior_enabled": True,
        }

        for field_name, value in required_failures.items():
            summary = self._summary()
            summary[field_name] = value
            with self.subTest(field_name=field_name):
                with self.assertRaisesRegex(ValueError, field_name):
                    evaluate_setup_outcome_diagnostics(summary)

    def test_preserves_accepted_records_by_setup_type_and_symbol(self):
        records = [
            self._record(
                proof_record_id="spy",
                setup_id="setup-spy",
                frozen_setup_identity={
                    "caller_provided": True,
                    "frozen_before_outcome_scan": True,
                    "setup_id": "setup-spy",
                    "setup_type": "Ideal",
                    "symbol": "SPY",
                    "frozen_timestamp": "2026-05-24T09:35:00-04:00",
                },
            ),
            self._record(
                proof_record_id="qqq",
                setup_id="setup-qqq",
                setup_type="Continuation",
                symbol="QQQ",
                frozen_setup_identity={
                    "caller_provided": True,
                    "frozen_before_outcome_scan": True,
                    "setup_id": "setup-qqq",
                    "setup_type": "Continuation",
                    "symbol": "QQQ",
                    "frozen_timestamp": "2026-05-24T09:35:00-04:00",
                },
            ),
        ]

        result = evaluate_setup_outcome_diagnostics(self._summary(records))

        self.assertEqual(set(result["diagnostics_by_setup_type"]), {"Ideal", "Continuation"})
        self.assertEqual(set(result["diagnostics_by_setup_type"]["Ideal"]), {"SPY"})
        self.assertEqual(set(result["diagnostics_by_setup_type"]["Continuation"]), {"QQQ"})
        self.assertEqual(
            result["diagnostics_by_setup_type"]["Continuation"]["QQQ"][0][
                "affected_symbol"
            ],
            "QQQ",
        )

    def test_triggered_worked_emits_evidence_without_viability_claim(self):
        finding = self._single_finding(self._record(outcome_result_state="worked"))

        self.assertEqual(finding["outcome_status"], "triggered_worked")
        self.assertEqual(finding["diagnostic_category"], "outcome_scoring_review")
        self.assertIn("trigger evidence was present", finding["what_happened"])
        self.assertEqual(finding["affected_setup_type"], "Ideal")
        self.assertEqual(finding["affected_symbol"], "SPY")
        self.assertEqual(finding["affected_stage"], "near-trigger")
        self.assertEqual(finding["evidence_used"], ["detected-row-1", "chart-row-219"])
        self.assertNotIn("viability", str(finding).lower())

    def test_triggered_failed_uses_outcome_or_trigger_invalidation_fix_path(self):
        failed_finding = self._single_finding(self._record(outcome_result_state="failed"))
        trigger_limited_finding = self._single_finding(
            self._record(
                outcome_result_state="failed",
                unavailable_fields=[self._unavailable_item("trigger_level")],
            )
        )
        invalidation_limited_finding = self._single_finding(
            self._record(
                outcome_result_state="failed",
                unavailable_fields=[self._unavailable_item("invalidation_level")],
            )
        )

        self.assertEqual(failed_finding["diagnostic_category"], "outcome_scoring_review")
        self.assertEqual(trigger_limited_finding["diagnostic_category"], "trigger_card_review")
        self.assertEqual(
            invalidation_limited_finding["diagnostic_category"],
            "invalidation_review",
        )
        for finding in (
            failed_finding,
            trigger_limited_finding,
            invalidation_limited_finding,
        ):
            self.assertEqual(
                finding["next_fix_path"],
                SETUP_OUTCOME_DIAGNOSTIC_FIX_PATHS[finding["diagnostic_category"]],
            )
            self.assertIn("regression", finding["regression_needed"])

    def test_all_setup_outcome_statuses_emit_diagnostics(self):
        cases = {
            "triggered_inconclusive": self._record(outcome_result_state="inconclusive"),
            "stayed_valid_pending": self._record(
                trigger_state="not_triggered",
                invalidation_state="valid_by_rule",
                freshness_state="fresh",
                outcome_result_state="pending",
            ),
            "stale_without_trigger": self._record(
                trigger_state="not_triggered",
                freshness_state="stale",
                outcome_result_state="none",
            ),
            "invalidated_before_trigger": self._record(
                trigger_state="not_triggered",
                invalidation_state="invalidated",
                outcome_result_state="none",
            ),
            "insufficient_evidence": self._record(
                outcome_evidence_state="missing_evidence",
                unavailable_fields=[self._unavailable_item("post_setup_evidence")],
            ),
        }
        del cases["insufficient_evidence"]["after_setup_evidence"]["post_setup_evidence"]

        result = evaluate_setup_outcome_diagnostics(self._summary(list(cases.values())))
        statuses = {finding["outcome_status"] for finding in result["diagnostic_findings"]}
        categories = {finding["diagnostic_category"] for finding in result["diagnostic_findings"]}

        self.assertEqual(statuses, set(cases))
        self.assertIn("outcome_scoring_review", categories)
        self.assertIn("setup_recognition_review", categories)
        self.assertIn("fresh_stale_spent_review", categories)
        self.assertIn("invalidation_review", categories)
        self.assertIn("data_quality_or_missing_evidence", categories)

    def test_blocker_and_session_boundary_matter_when_present(self):
        blocker = self._single_finding(self._record(blocker_caution_state="blocked"))
        session = self._single_finding(self._record(session_boundary_state="needs_review"))

        self.assertEqual(blocker["diagnostic_category"], "blocker_caution_review")
        self.assertIs(blocker["lower_tier_handoff_required"], True)
        self.assertEqual(session["diagnostic_category"], "session_boundary_review")
        self.assertIs(session["lower_tier_handoff_required"], True)

    def test_proof_limited_fields_become_missing_evidence_diagnostics(self):
        record = self._record(
            outcome_evidence_state="unavailable_evidence",
            unavailable_fields=[self._unavailable_item("source_row_reference")],
        )
        result = evaluate_setup_outcome_diagnostics(self._summary([record]))
        finding = result["diagnostic_findings"][0]

        self.assertEqual(finding["diagnostic_category"], "data_quality_or_missing_evidence")
        self.assertTrue(finding["proof_limited_fields"])
        self.assertTrue(result["proof_limited_records"])
        self.assertTrue(result["unavailable_evidence"])
        self.assertIs(finding["lower_tier_handoff_required"], True)

    def test_rejected_proof_reasons_require_lower_tier_handoff(self):
        result = evaluate_setup_outcome_diagnostics(
            self._summary([self._record(watch_only=False)])
        )

        self.assertEqual(result["records_rejected"], 1)
        rejected_finding = result["diagnostic_findings"][0]
        self.assertEqual(
            rejected_finding["diagnostic_category"],
            "lower_tier_handoff_review",
        )
        self.assertIs(rejected_finding["lower_tier_handoff_required"], True)
        self.assertEqual(result["rejected_records"][0]["record_id"], "proof-row-1")

    def test_gap_counts_next_fix_paths_and_candidates_are_evidence_based(self):
        result = evaluate_setup_outcome_diagnostics(
            self._summary(
                [
                    self._record(outcome_result_state="failed"),
                    self._record(
                        proof_record_id="stale",
                        setup_id="setup-stale",
                        frozen_setup_identity={
                            "caller_provided": True,
                            "frozen_before_outcome_scan": True,
                            "setup_id": "setup-stale",
                            "setup_type": "Ideal",
                            "symbol": "SPY",
                            "frozen_timestamp": "2026-05-24T09:35:00-04:00",
                        },
                        trigger_state="not_triggered",
                        freshness_state="stale",
                        outcome_result_state="none",
                    ),
                ]
            )
        )

        self.assertEqual(
            set(result["diagnostic_gap_counts"]),
            set(SETUP_OUTCOME_DIAGNOSTIC_FAILURE_CATEGORIES),
        )
        self.assertEqual(result["diagnostic_gap_counts"]["outcome_scoring_review"], 1)
        self.assertEqual(result["diagnostic_gap_counts"]["fresh_stale_spent_review"], 1)
        for candidate in result["likely_cause_candidates"]:
            self.assertEqual(candidate["label"], "candidate")
            self.assertTrue(candidate["candidate"].startswith("candidate:"))
            self.assertIn("evidence_basis", candidate)
            self.assertNotIn("root_cause", candidate)
        for category, fix_path in result["next_fix_paths"].items():
            self.assertEqual(fix_path, SETUP_OUTCOME_DIAGNOSTIC_FIX_PATHS[category])

    def test_forbidden_execution_fields_are_rejected_recursively(self):
        summary = self._summary()
        summary["accepted_records_by_setup_type"]["Ideal"]["SPY"][0]["nested"] = {
            "trade_decision": "approve"
        }

        with self.assertRaisesRegex(ValueError, "Forbidden execution/trade field"):
            evaluate_setup_outcome_diagnostics(summary)

    def test_defensive_copy_behavior(self):
        summary = self._summary()
        before = copy.deepcopy(summary)

        result = evaluate_setup_outcome_diagnostics(summary)
        result["diagnostic_findings"][0]["evidence_used"].append("mutated")
        result["diagnostics_by_setup_type"]["Ideal"]["SPY"][0][
            "likely_cause_candidates"
        ][0]["candidate"] = "mutated"
        result["rejected_records"].append({"reason": "mutated"})

        self.assertEqual(summary, before)
        second = evaluate_setup_outcome_diagnostics(summary)
        self.assertNotIn("mutated", second["diagnostic_findings"][0]["evidence_used"])
        self.assertNotEqual(
            second["diagnostics_by_setup_type"]["Ideal"]["SPY"][0][
                "likely_cause_candidates"
            ][0]["candidate"],
            "mutated",
        )

    def test_no_file_network_subprocess_thread_or_live_side_effects(self):
        summary = self._summary()
        before = copy.deepcopy(summary)

        with patch("builtins.open") as open_mock, patch(
            "socket.socket"
        ) as socket_mock, patch("subprocess.run") as subprocess_mock, patch(
            "threading.Thread"
        ) as thread_mock:
            result = evaluate_setup_outcome_diagnostics(summary)

        self.assertEqual(summary, before)
        self.assertIs(result["no_rule_change_started"], True)
        self.assertIs(result["live_data_started"], False)
        self.assertIs(result["controlled_shadow_data_started"], False)
        self.assertIs(result["alerts_sent"], False)
        self.assertIs(result["files_written"], False)
        self.assertIs(result["broker_or_trade_behavior_enabled"], False)
        self.assertIs(result["no_trade_boundary_preserved"], True)
        open_mock.assert_not_called()
        socket_mock.assert_not_called()
        subprocess_mock.assert_not_called()
        thread_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
