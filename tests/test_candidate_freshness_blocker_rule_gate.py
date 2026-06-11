import io
import unittest
from contextlib import redirect_stdout

from watcher_foundation import candidate_freshness_blocker_rule_gate as gate
from watcher_foundation import candidate_source_pool_intake as intake


EXPECTED_RULE_FAMILIES = {
    "Clean Fast Break initial-break / higher-base / fresh-break expiry",
    "Clean Fast Break gap-context completeness",
    "Continuation next-session carry-forward freshness",
    "Continuation session-boundary freshness",
    "Ideal stale/spent expiry",
    "Ideal fast-swing freshness",
    "intrabar ordering / order-of-events inside 1H candles",
    "wide-risk / room threshold",
    "complete context/caution review",
    "primary blocker null is not enough",
}


class CandidateFreshnessBlockerRuleGateTests(unittest.TestCase):
    def test_rule_gate_covers_all_known_missing_rule_families(self):
        result = gate.build_rule_gate_result()
        families = {row["rule_family"] for row in result["gate_rows"]}

        self.assertEqual(families, EXPECTED_RULE_FAMILIES)
        self.assertEqual(result["rule_families_checked"], len(EXPECTED_RULE_FAMILIES))

    def test_every_seven_row_candidate_maps_to_at_least_one_rule_gate(self):
        result = gate.build_rule_gate_result()

        self.assertEqual(tuple(result["affected_candidate_ids"]), gate.STRICT_CANDIDATE_IDS)
        for candidate_id in gate.STRICT_CANDIDATE_IDS:
            self.assertGreaterEqual(len(result["gate_by_candidate"][candidate_id]), 1)

    def test_missing_rule_cannot_promote_candidate(self):
        self.assertEqual(
            gate.candidate_rule_gate_status("SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002"),
            "blocked",
        )
        self.assertFalse(
            gate.candidate_can_promote("SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002")
        )

    def test_source_data_insufficient_cannot_promote_candidate(self):
        self.assertFalse(
            gate.candidate_can_promote("QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001")
        )
        statuses = {
            row["gate_status"]
            for row in gate.build_rule_gate_result()["gate_by_candidate"][
                "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001"
            ]
        }
        self.assertIn("SOURCE_DATA_INSUFFICIENT", statuses)

    def test_lower_timeframe_required_cannot_promote_candidate(self):
        self.assertFalse(
            gate.candidate_can_promote("SPY-REAL-HISTORICAL-CONTINUATION-001")
        )
        statuses = {
            row["gate_status"]
            for row in gate.build_rule_gate_result()["gate_by_candidate"][
                "SPY-REAL-HISTORICAL-CONTINUATION-001"
            ]
        }
        self.assertIn("LOWER_TIMEFRAME_REQUIRED", statuses)

    def test_threshold_missing_cannot_promote_candidate(self):
        self.assertFalse(gate.candidate_can_promote("QQQ-REAL-HISTORICAL-IDEAL-001"))
        statuses = {
            row["gate_status"]
            for row in gate.build_rule_gate_result()["gate_by_candidate"][
                "QQQ-REAL-HISTORICAL-IDEAL-001"
            ]
        }
        self.assertIn("THRESHOLD_MISSING", statuses)

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

    def test_source_pool_intake_counts_remain_blocked(self):
        result = intake.build_source_pool_intake()

        self.assertEqual(result["source_pool_rows_inspected"], 60)
        self.assertEqual(result["accepted_intake_count"], 7)
        self.assertEqual(result["intake_ready_count"], 0)
        self.assertEqual(result["close_ready_count"], 7)
        self.assertEqual(result["rule_gate_families_checked"], len(EXPECTED_RULE_FAMILIES))
        self.assertEqual(result["rule_gate_source_backed_rule_count"], 1)
        self.assertEqual(result["rule_gate_missing_unresolved_rule_count"], 9)

    def test_rule_gate_report_prints_required_summary(self):
        report = gate.format_rule_gate_report(gate.build_rule_gate_result())

        self.assertIn("rule families checked: 10", report)
        self.assertIn("source-backed rule count: 1", report)
        self.assertIn("missing/unresolved rule count: 9", report)
        self.assertIn("exact", report.lower())
        self.assertIn("next_fix=", report)


if __name__ == "__main__":
    unittest.main()
