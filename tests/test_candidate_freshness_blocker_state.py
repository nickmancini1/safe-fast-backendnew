import unittest

from watcher_foundation import candidate_freshness_blocker_state as state_model


STRICT_IDS = {
    "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001",
    "QQQ-REAL-HISTORICAL-CONTINUATION-001",
    "QQQ-REAL-HISTORICAL-IDEAL-001",
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003",
    "SPY-REAL-HISTORICAL-CONTINUATION-001",
    "SPY-REAL-HISTORICAL-IDEAL-001",
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002",
}


class CandidateFreshnessBlockerStateTests(unittest.TestCase):
    def test_allowed_states_are_explicit(self):
        self.assertEqual(
            state_model.ALLOWED_FRESHNESS_STATES,
            (
                "clean",
                "stale",
                "spent",
                "session_boundary_unclear",
                "gap_context_incomplete",
                "intrabar_ordering_incomplete",
                "setup_specific_rules_incomplete",
                "unresolved",
                "missing",
            ),
        )
        self.assertEqual(
            state_model.ALLOWED_BLOCKER_STATES,
            (
                "clean",
                "blocker_present",
                "caution_incomplete",
                "context_incomplete",
                "wide_risk_caution",
                "unresolved",
                "missing",
            ),
        )

    def test_each_strict_row_receives_freshness_and_blocker_state(self):
        result = state_model.build_freshness_blocker_states()
        by_id = result["state_by_id"]

        self.assertEqual(set(by_id), STRICT_IDS)
        for row in by_id.values():
            self.assertIn(row["freshness_state"], state_model.ALLOWED_FRESHNESS_STATES)
            self.assertIn(row["blocker_state"], state_model.ALLOWED_BLOCKER_STATES)
            self.assertNotEqual(row["freshness_source"], "")
            self.assertNotEqual(row["blocker_source"], "")
            self.assertNotEqual(row["freshness_reason"], "")
            self.assertNotEqual(row["blocker_reason"], "")
            self.assertNotEqual(row["freshness_missing_evidence"], "")
            self.assertNotEqual(row["blocker_missing_evidence"], "")

    def test_unresolved_and_incomplete_markers_block_case_insensitively(self):
        for value in ("UNCLEAR", "unclear", "Incomplete", "incomplete", "MISSING", None, ""):
            self.assertTrue(state_model.unresolved_marker_blocks(value))

    def test_primary_blocker_null_alone_cannot_make_blocker_clean(self):
        self.assertEqual(
            state_model.blocker_state_from_primary_blocker(None, complete_review_present=False),
            "context_incomplete",
        )
        self.assertEqual(
            state_model.blocker_state_from_primary_blocker("none", complete_review_present=False),
            "context_incomplete",
        )

    def test_no_row_is_promoted_without_clean_freshness_and_clean_blocker(self):
        result = state_model.build_freshness_blocker_states()

        for row in result["state_rows"]:
            if row["decision"] == "intake-ready":
                self.assertEqual(row["freshness_state"], "clean")
                self.assertEqual(row["blocker_state"], "clean")
            else:
                self.assertTrue(row["freshness_state"] != "clean" or row["blocker_state"] != "clean")

        self.assertEqual(result["intake_ready_count"], 0)
        self.assertEqual(result["blocked_count"], 5)
        self.assertEqual(result["replace_count"], 2)

    def test_decision_for_states_requires_both_clean(self):
        self.assertEqual(state_model.decision_for_states("clean", "clean"), "intake-ready")
        self.assertEqual(state_model.decision_for_states("clean", "context_incomplete"), "blocked")
        self.assertEqual(state_model.decision_for_states("setup_specific_rules_incomplete", "clean"), "blocked")

    def test_row_specific_states_are_preserved(self):
        by_id = state_model.build_freshness_blocker_states()["state_by_id"]

        self.assertEqual(
            by_id["QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001"]["freshness_state"],
            "gap_context_incomplete",
        )
        self.assertEqual(
            by_id["QQQ-REAL-HISTORICAL-CONTINUATION-001"]["freshness_state"],
            "session_boundary_unclear",
        )
        self.assertEqual(
            by_id["QQQ-REAL-HISTORICAL-CONTINUATION-001"]["decision"],
            "replace",
        )
        self.assertEqual(
            by_id["SPY-REAL-HISTORICAL-CONTINUATION-001"]["freshness_state"],
            "intrabar_ordering_incomplete",
        )
        self.assertEqual(
            by_id["SPY-REAL-HISTORICAL-CONTINUATION-001"]["decision"],
            "blocked",
        )
        self.assertEqual(
            by_id["QQQ-REAL-HISTORICAL-IDEAL-001"]["blocker_state"],
            "wide_risk_caution",
        )
        self.assertEqual(
            by_id["QQQ-REAL-HISTORICAL-IDEAL-001"]["decision"],
            "replace",
        )
        self.assertEqual(
            by_id["SPY-REAL-HISTORICAL-IDEAL-001"]["decision"],
            "blocked",
        )

    def test_state_family_missing_evidence_is_exact(self):
        by_id = state_model.build_freshness_blocker_states()["state_by_id"]

        self.assertIn(
            "missing source-backed gap_context field/rule",
            by_id["QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001"]["freshness_missing_evidence"],
        )
        self.assertIn(
            "missing next-session Continuation freshness/carry-forward rule",
            by_id["QQQ-REAL-HISTORICAL-CONTINUATION-001"]["freshness_missing_evidence"],
        )
        self.assertIn(
            "excludes this next-session/session-boundary-dependent row",
            by_id["QQQ-REAL-HISTORICAL-CONTINUATION-001"]["freshness_reason"],
        )
        self.assertIn(
            "missing lower-timeframe or order-of-events evidence",
            by_id["SPY-REAL-HISTORICAL-CONTINUATION-001"]["freshness_missing_evidence"],
        )
        self.assertIn(
            "missing accepted wide-risk or room threshold",
            by_id["QQQ-REAL-HISTORICAL-IDEAL-001"]["blocker_missing_evidence"],
        )
        self.assertIn(
            "applied Ideal narrowing excludes this fast-swing/wide-risk row",
            by_id["QQQ-REAL-HISTORICAL-IDEAL-001"]["freshness_reason"],
        )
        self.assertIn(
            "CONTEXT_24H_DAILY_UNCONFIRMED",
            by_id["SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003"]["blocker_missing_evidence"],
        )

    def test_command_line_stdout_report_path_works(self):
        result = state_model.build_freshness_blocker_states()
        report = state_model.format_state_report(result)

        self.assertIn("accepted state count: 7", report)
        self.assertIn("intake-ready count: 0", report)
        self.assertIn("freshness_missing=", report)
        self.assertIn("QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001", report)

    def test_no_proof_or_profitability_claims(self):
        result = state_model.build_freshness_blocker_states()

        self.assertTrue(state_model.NO_PROOF_ACCEPTED)
        self.assertFalse(state_model.PROFITABILITY_CLAIMED)
        self.assertFalse(result["proof_accepted"])
        self.assertFalse(result["profitability_claimed"])


if __name__ == "__main__":
    unittest.main()
