import io
import unittest
from contextlib import redirect_stdout

from watcher_foundation import candidate_freshness_blocker_rule_gate as gate
from watcher_foundation import candidate_source_pool_intake as intake


EXPECTED_RULE_FAMILIES = {
    "Clean Fast Break expiry",
    "Clean Fast Break gap context",
    "Continuation next-session freshness",
    "Continuation session-boundary freshness",
    "Ideal stale/spent expiry",
    "Ideal fast-swing freshness",
    "Intrabar ordering",
    "Wide-risk / room threshold",
    "Context/caution review",
}


class CandidateFreshnessBlockerRuleGateTests(unittest.TestCase):
    def test_rule_gate_covers_exactly_the_nine_decision_families(self):
        result = gate.build_rule_gate_result()
        families = {row["rule_family"] for row in result["gate_rows"]}

        self.assertEqual(families, EXPECTED_RULE_FAMILIES)
        self.assertEqual(result["rule_families_checked"], 9)

    def test_each_family_has_one_allowed_hard_decision(self):
        result = gate.build_rule_gate_result()

        for row in result["gate_rows"]:
            self.assertIn(row["hard_decision"], gate.HARD_DECISIONS)
            self.assertNotIn("maybe", row["hard_decision"].lower())
            self.assertNotIn("unclear", row["hard_decision"].lower())
            self.assertNotIn("unresolved", row["hard_decision"].lower())

    def test_every_seven_row_candidate_maps_to_at_least_one_decision(self):
        result = gate.build_rule_gate_result()

        self.assertEqual(tuple(result["affected_candidate_ids"]), gate.STRICT_CANDIDATE_IDS)
        for candidate_id in gate.STRICT_CANDIDATE_IDS:
            self.assertGreaterEqual(len(result["gate_by_candidate"][candidate_id]), 1)

    def test_source_data_insufficient_cannot_promote_candidate(self):
        self.assertFalse(
            gate.candidate_can_promote("QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001")
        )
        decisions = {
            row["hard_decision"]
            for row in gate.build_rule_gate_result()["gate_by_candidate"][
                "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001"
            ]
        }
        self.assertIn("SOURCE_DATA_INSUFFICIENT", decisions)

    def test_cfb_expiry_source_data_insufficiency_blocks_intake_ready(self):
        for candidate_id in gate.CLEAN_FAST_BREAK_SOURCE_DATA_INSUFFICIENT_CANDIDATE_IDS:
            decisions = {
                row["rule_family"]: row["hard_decision"]
                for row in gate.build_rule_gate_result()["gate_by_candidate"][candidate_id]
            }

            self.assertEqual(decisions["Clean Fast Break expiry"], "SOURCE_DATA_INSUFFICIENT")
            self.assertEqual(gate.candidate_rule_gate_status(candidate_id), "blocked")
            self.assertFalse(
                gate.candidate_can_promote(
                    candidate_id,
                    final_verdict="TRADE",
                    primary_blocker="complete blocker review",
                    complete_context_caution_review=True,
                )
            )

    def test_cfb_gap_context_source_data_insufficiency_blocks_intake_ready(self):
        candidate_id = "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001"
        decisions = {
            row["rule_family"]: row["hard_decision"]
            for row in gate.build_rule_gate_result()["gate_by_candidate"][candidate_id]
        }

        self.assertEqual(decisions["Clean Fast Break gap context"], "SOURCE_DATA_INSUFFICIENT")
        self.assertIn("gap-context", gate.candidate_cfb_source_data_insufficiency_reason(candidate_id))
        self.assertFalse(
            gate.candidate_can_promote(
                candidate_id,
                final_verdict="TRADE",
                primary_blocker="complete blocker review",
                complete_context_caution_review=True,
            )
        )

    def test_specific_clean_fast_break_rows_stay_blocked(self):
        expected_reason_parts = {
            "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001": "gap-context",
            "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003": "context/caution",
            "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002": "context/caution",
        }

        for candidate_id, reason_part in expected_reason_parts.items():
            self.assertEqual(gate.candidate_rule_gate_status(candidate_id), "blocked")
            self.assertIn(
                reason_part,
                gate.candidate_cfb_source_data_insufficiency_reason(candidate_id),
            )

    def test_kill_or_narrow_cannot_promote_candidate(self):
        self.assertFalse(
            gate.candidate_can_promote("SPY-REAL-HISTORICAL-CONTINUATION-001")
        )
        decisions = {
            row["hard_decision"]
            for row in gate.build_rule_gate_result()["gate_by_candidate"][
                "SPY-REAL-HISTORICAL-CONTINUATION-001"
            ]
        }
        self.assertIn("KILL_OR_NARROW_SETUP_SYMBOL_PATH", decisions)

    def test_next_session_continuation_is_outside_narrowed_path(self):
        candidate_id = "QQQ-REAL-HISTORICAL-CONTINUATION-001"

        self.assertTrue(gate.candidate_is_outside_narrowed_path(candidate_id))
        self.assertEqual(gate.candidate_rule_gate_status(candidate_id), "outside_narrowed_path")
        self.assertFalse(
            gate.candidate_can_promote(
                candidate_id,
                final_verdict="TRADE",
                primary_blocker="complete blocker review",
                complete_context_caution_review=True,
            )
        )

    def test_intrabar_ordering_narrows_spy_continuation_outside_path(self):
        candidate_id = "SPY-REAL-HISTORICAL-CONTINUATION-001"
        decisions = {
            row["rule_family"]: row["hard_decision"]
            for row in gate.build_rule_gate_result()["gate_by_candidate"][candidate_id]
        }

        self.assertEqual(decisions["Intrabar ordering"], "KILL_OR_NARROW_SETUP_SYMBOL_PATH")
        self.assertTrue(gate.candidate_is_outside_narrowed_path(candidate_id))
        self.assertEqual(gate.candidate_rule_gate_status(candidate_id), "outside_narrowed_path")
        self.assertIn("order-of-events", gate.candidate_outside_narrowed_path_reason(candidate_id))
        self.assertFalse(
            gate.candidate_can_promote(
                candidate_id,
                final_verdict="TRADE",
                primary_blocker="complete blocker review",
                complete_context_caution_review=True,
            )
        )

    def test_fast_swing_ideal_is_outside_narrowed_path_without_source_backed_rule(self):
        candidate_id = "QQQ-REAL-HISTORICAL-IDEAL-001"

        self.assertTrue(gate.candidate_is_outside_narrowed_path(candidate_id))
        self.assertEqual(gate.candidate_rule_gate_status(candidate_id), "outside_narrowed_path")
        self.assertIn("fast-swing", gate.candidate_outside_narrowed_path_reason(candidate_id))
        self.assertFalse(
            gate.candidate_can_promote(
                candidate_id,
                final_verdict="TRADE",
                primary_blocker="complete blocker review",
                complete_context_caution_review=True,
            )
        )

    def test_wide_risk_ideal_cannot_promote_without_room_risk_threshold(self):
        candidate_id = "QQQ-REAL-HISTORICAL-IDEAL-001"
        decisions = {
            row["rule_family"]: row["hard_decision"]
            for row in gate.build_rule_gate_result()["gate_by_candidate"][candidate_id]
        }

        self.assertEqual(decisions["Wide-risk / room threshold"], "KILL_OR_NARROW_SETUP_SYMBOL_PATH")
        self.assertIn("room threshold", " ".join(decisions))
        self.assertFalse(gate.candidate_can_promote(candidate_id))

    def test_spy_ideal_stays_blocked_until_stale_spent_and_context_clean(self):
        candidate_id = "SPY-REAL-HISTORICAL-IDEAL-001"

        self.assertFalse(gate.candidate_is_outside_narrowed_path(candidate_id))
        self.assertEqual(gate.candidate_rule_gate_status(candidate_id), "blocked")
        self.assertFalse(
            gate.candidate_can_promote(
                candidate_id,
                final_verdict="TRADE",
                primary_blocker="complete blocker review",
                complete_context_caution_review=True,
            )
        )

    def test_final_verdict_trade_alone_cannot_satisfy_rule_gate(self):
        self.assertFalse(
            gate.candidate_can_promote(
                "QQQ-REAL-HISTORICAL-CONTINUATION-001",
                final_verdict="TRADE",
                primary_blocker="blocker review complete",
                complete_context_caution_review=False,
            )
        )

    def test_primary_blocker_null_alone_cannot_satisfy_blocker_caution_gate(self):
        self.assertFalse(
            gate.candidate_can_promote(
                "SPY-REAL-HISTORICAL-IDEAL-001",
                primary_blocker=None,
                complete_context_caution_review=False,
            )
        )

    def test_no_positive_proof_or_profitability_claim_text_appears(self):
        output = io.StringIO()
        with redirect_stdout(output):
            gate.main()

        report = output.getvalue().lower()
        self.assertIn("proof accepted: no", report)
        self.assertIn("profitability claim made: no", report)
        self.assertNotIn("proof accepted: yes", report)
        self.assertNotIn("profitability claim made: yes", report)

    def test_intake_ready_remains_zero_without_source_backed_clean_rules(self):
        result = gate.build_rule_gate_result()

        self.assertEqual(result["source_backed_rule_count"], 0)
        self.assertEqual(result["missing_unresolved_rule_count"], 9)
        self.assertEqual(result["intake_ready_count"], 0)
        for candidate_id in gate.STRICT_CANDIDATE_IDS:
            expected = (
                "outside_narrowed_path"
                if candidate_id
                in {
                    "QQQ-REAL-HISTORICAL-CONTINUATION-001",
                    "QQQ-REAL-HISTORICAL-IDEAL-001",
                    "SPY-REAL-HISTORICAL-CONTINUATION-001",
                }
                else "blocked"
            )
            self.assertEqual(gate.candidate_rule_gate_status(candidate_id), expected)

    def test_source_pool_intake_counts_remain_blocked(self):
        result = intake.build_source_pool_intake()

        self.assertEqual(result["source_pool_rows_inspected"], 60)
        self.assertEqual(result["accepted_intake_count"], 7)
        self.assertEqual(result["intake_ready_count"], 0)
        self.assertEqual(result["close_ready_count"], 4)
        self.assertEqual(result["replace_count"], 3)
        self.assertEqual(result["rule_gate_families_checked"], 9)
        self.assertEqual(result["rule_gate_source_backed_rule_count"], 0)
        self.assertEqual(result["rule_gate_missing_unresolved_rule_count"], 9)

    def test_rule_gate_report_prints_the_nine_decisions(self):
        report = gate.format_rule_gate_report(gate.build_rule_gate_result())

        self.assertIn("rule families checked: 9", report)
        self.assertIn("source-backed clean decision count: 0", report)
        self.assertIn("blocking decision count: 9", report)
        self.assertIn("decision=SOURCE_DATA_INSUFFICIENT", report)
        self.assertIn("decision=KILL_OR_NARROW_SETUP_SYMBOL_PATH", report)


if __name__ == "__main__":
    unittest.main()
