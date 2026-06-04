import copy
import unittest
from unittest.mock import patch

from watcher_foundation import (
    SETUP_OUTCOME_DIAGNOSTIC_FIX_PATHS,
    SETUP_OUTCOME_PROOF_RESULT_FIELDS,
    SETUP_OUTCOME_PROOF_STATUSES,
    evaluate_setup_outcome_proof,
    validate_setup_outcome_proof_record,
)


class SetupOutcomeProofTests(unittest.TestCase):
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

    def _record_for_setup(self, setup_type, symbol, **overrides):
        record = self._record(
            proof_record_id=f"{setup_type}-{symbol}",
            setup_id=f"{setup_type}-{symbol}-setup",
            setup_type=setup_type,
            symbol=symbol,
        )
        record["frozen_setup_identity"].update(
            {
                "setup_id": record["setup_id"],
                "setup_type": setup_type,
                "symbol": symbol,
            }
        )
        record.update(overrides)
        return record

    def test_accepts_valid_caller_provided_in_memory_outcome_records(self):
        result = evaluate_setup_outcome_proof([self._record()])

        self.assertEqual(set(SETUP_OUTCOME_PROOF_RESULT_FIELDS), set(result))
        self.assertEqual(result["records_processed"], 1)
        self.assertEqual(result["records_accepted"], 1)
        row = result["accepted_records_by_setup_type"]["Ideal"]["SPY"][0]
        self.assertEqual(row["outcome_status"], "triggered_worked")
        self.assertIs(row["watch_only"], True)
        self.assertEqual(row["setup_evidence_refs"], ["detected-row-1", "setup-chart-row-218"])

    def test_rejects_invalid_records(self):
        result = evaluate_setup_outcome_proof([self._record(watch_only=False)])

        self.assertEqual(result["records_accepted"], 0)
        self.assertEqual(result["records_rejected"], 1)
        self.assertIn("watch_only=True", result["rejected_records"][0]["reason"])

    def test_required_fields_are_enforced_before_scoring(self):
        record = self._record()
        del record["frozen_setup_identity"]

        with self.assertRaisesRegex(ValueError, "frozen_setup_identity"):
            validate_setup_outcome_proof_record(record)

    def test_setup_type_separation_is_preserved(self):
        result = evaluate_setup_outcome_proof(
            [
                self._record_for_setup("Ideal", "SPY"),
                self._record_for_setup("Clean Fast Break", "SPY"),
                self._record_for_setup("Continuation", "SPY"),
            ]
        )

        self.assertEqual(
            set(result["accepted_records_by_setup_type"]),
            {"Ideal", "Clean Fast Break", "Continuation"},
        )

    def test_symbol_separation_is_preserved(self):
        result = evaluate_setup_outcome_proof(
            [
                self._record_for_setup("Ideal", "SPY"),
                self._record_for_setup("Ideal", "QQQ"),
            ]
        )

        self.assertEqual(
            set(result["accepted_records_by_setup_type"]["Ideal"]),
            {"SPY", "QQQ"},
        )

    def test_trigger_outcome_statuses_are_classified(self):
        cases = (
            ("triggered_worked", self._record(outcome_result_state="worked")),
            ("triggered_failed", self._record(outcome_result_state="failed")),
            ("triggered_inconclusive", self._record(outcome_result_state="inconclusive")),
        )

        result = evaluate_setup_outcome_proof([record for _, record in cases])

        statuses = [
            row["outcome_status"]
            for rows_by_symbol in result["accepted_records_by_setup_type"].values()
            for rows in rows_by_symbol.values()
            for row in rows
        ]
        for expected_status, _ in cases:
            self.assertIn(expected_status, statuses)

    def test_invalidation_outcome_is_classified(self):
        result = evaluate_setup_outcome_proof(
            [
                self._record(
                    trigger_state="not_triggered",
                    invalidation_state="invalidated",
                    outcome_result_state="none",
                )
            ]
        )

        row = result["accepted_records_by_setup_type"]["Ideal"]["SPY"][0]
        self.assertEqual(row["outcome_status"], "invalidated_before_trigger")

    def test_stale_and_spent_outcomes_are_classified(self):
        result = evaluate_setup_outcome_proof(
            [
                self._record(
                    proof_record_id="stale",
                    trigger_state="not_triggered",
                    freshness_state="stale",
                    outcome_result_state="none",
                ),
                self._record(
                    proof_record_id="spent",
                    setup_id="setup-2",
                    frozen_setup_identity={
                        "caller_provided": True,
                        "frozen_before_outcome_scan": True,
                        "setup_id": "setup-2",
                        "setup_type": "Ideal",
                        "symbol": "SPY",
                        "frozen_timestamp": "2026-05-24T09:35:00-04:00",
                    },
                    trigger_state="not_triggered",
                    freshness_state="spent",
                    outcome_result_state="none",
                ),
            ]
        )

        rows = result["accepted_records_by_setup_type"]["Ideal"]["SPY"]
        self.assertEqual([row["outcome_status"] for row in rows], [
            "stale_without_trigger",
            "stale_without_trigger",
        ])

    def test_stayed_valid_pending_is_classified(self):
        result = evaluate_setup_outcome_proof(
            [
                self._record(
                    trigger_state="not_triggered",
                    invalidation_state="valid_by_rule",
                    freshness_state="fresh",
                    outcome_result_state="pending",
                )
            ]
        )

        row = result["accepted_records_by_setup_type"]["Ideal"]["SPY"][0]
        self.assertEqual(row["outcome_status"], "stayed_valid_pending")

    def test_missing_evidence_becomes_insufficient_evidence_and_proof_limited(self):
        record = self._record(
            outcome_evidence_state="missing_evidence",
            unavailable_fields=[self._unavailable_item("post_setup_evidence")],
        )
        del record["after_setup_evidence"]["post_setup_evidence"]

        result = evaluate_setup_outcome_proof([record])

        row = result["accepted_records_by_setup_type"]["Ideal"]["SPY"][0]
        self.assertEqual(row["outcome_status"], "insufficient_evidence")
        self.assertTrue(row["proof_limited"])
        self.assertEqual(
            result["proof_limited_records"][0]["proof_limited_fields"][0]["field_name"],
            "post_setup_evidence",
        )

    def test_unavailable_evidence_remains_explicit(self):
        result = evaluate_setup_outcome_proof(
            [
                self._record(
                    outcome_evidence_state="unavailable_evidence",
                    unavailable_fields=[self._unavailable_item("source_row_reference")],
                )
            ]
        )

        row = result["accepted_records_by_setup_type"]["Ideal"]["SPY"][0]
        self.assertEqual(row["outcome_status"], "insufficient_evidence")
        self.assertEqual(row["unavailable_fields"][0]["status"], "unavailable_evidence")

    def test_blocker_caution_state_is_preserved_in_diagnostics(self):
        result = evaluate_setup_outcome_proof(
            [self._record(blocker_caution_state="blocked")]
        )

        finding = result["diagnostic_findings"][0]
        self.assertEqual(finding["diagnostic_category"], "blocker_caution_review")
        self.assertEqual(
            finding["trigger_invalidation_freshness_relationship"]["trigger_state"],
            "triggered",
        )

    def test_session_boundary_state_is_preserved_in_diagnostics(self):
        result = evaluate_setup_outcome_proof(
            [self._record(session_boundary_state="needs_review")]
        )

        finding = result["diagnostic_findings"][0]
        self.assertEqual(finding["diagnostic_category"], "session_boundary_review")
        self.assertEqual(
            finding["trigger_invalidation_freshness_relationship"][
                "session_boundary_state"
            ],
            "needs_review",
        )

    def test_diagnostics_and_fix_path_placeholders_are_emitted(self):
        result = evaluate_setup_outcome_proof([self._record(outcome_result_state="failed")])
        finding = result["diagnostic_findings"][0]

        self.assertEqual(finding["affected_setup_type"], "Ideal")
        self.assertEqual(finding["affected_symbol"], "SPY")
        self.assertEqual(finding["affected_stage"], "near-trigger")
        self.assertEqual(
            finding["next_fix_path"],
            SETUP_OUTCOME_DIAGNOSTIC_FIX_PATHS[finding["diagnostic_category"]],
        )
        self.assertEqual(finding["likely_cause_candidates"][0]["label"], "candidate")
        self.assertIn("candidate:", finding["likely_cause_candidates"][0]["candidate"])

    def test_vague_labels_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "Vague setup outcome label"):
            validate_setup_outcome_proof_record(
                self._record(outcome_result_state="bad")
            )

    def test_no_combined_viability_claim_or_success_score_is_returned(self):
        result = evaluate_setup_outcome_proof([self._record()])

        self.assertIs(result["final_viability_proven"], False)
        self.assertNotIn("success_score", result)
        self.assertNotIn("combined_viability_score", result)
        self.assertEqual(set(result["outcome_status_counts"]), set(SETUP_OUTCOME_PROOF_STATUSES))

    def test_defensive_copy_behavior(self):
        record = self._record()
        before = copy.deepcopy(record)

        result = evaluate_setup_outcome_proof([record])
        result["accepted_records_by_setup_type"]["Ideal"]["SPY"][0][
            "after_setup_evidence"
        ]["post_setup_evidence"].append("mutated")
        result["diagnostic_findings"][0]["evidence_used"].append("mutated")

        self.assertEqual(record, before)
        self.assertNotIn("mutated", record["after_setup_evidence"]["post_setup_evidence"])
        self.assertNotIn("mutated", record["evidence_refs"])

    def test_watch_only_boundary_is_required_and_preserved(self):
        with self.assertRaisesRegex(ValueError, "watch_only=True"):
            validate_setup_outcome_proof_record(self._record(watch_only=False))

        result = evaluate_setup_outcome_proof([self._record()])
        self.assertIs(result["watch_only"], True)
        self.assertIs(result["no_trade_boundary_preserved"], True)
        row = result["accepted_records_by_setup_type"]["Ideal"]["SPY"][0]
        self.assertIs(row["watch_only"], True)
        self.assertIs(row["no_trade_boundary"]["no_live_trade_decision"], True)

    def test_no_hindsight_ordering_is_enforced(self):
        with self.assertRaisesRegex(ValueError, "future evidence"):
            validate_setup_outcome_proof_record(
                self._record(
                    after_setup_evidence={
                        "caller_provided": True,
                        "start_timestamp": "2026-05-24T10:30:00-04:00",
                        "future_evidence_used_to_define_setup": True,
                    }
                )
            )

        with self.assertRaisesRegex(ValueError, "start after detection_timestamp"):
            validate_setup_outcome_proof_record(
                self._record(
                    after_setup_evidence={
                        "caller_provided": True,
                        "start_timestamp": "2026-05-24T09:00:00-04:00",
                        "future_evidence_used_to_define_setup": False,
                    }
                )
            )

    def test_forbidden_execution_fields_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "Forbidden execution/trade field"):
            validate_setup_outcome_proof_record(
                self._record(nested={"trade_decision": "approve"})
            )

    def test_evaluator_has_no_file_network_subprocess_or_live_side_effects(self):
        record = self._record()
        before = copy.deepcopy(record)

        with patch("builtins.open") as open_mock, patch(
            "socket.socket"
        ) as socket_mock, patch("subprocess.run") as subprocess_mock:
            result = evaluate_setup_outcome_proof([record])

        self.assertEqual(record, before)
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
