import io
import unittest
from contextlib import redirect_stdout

from watcher_foundation import candidate_completeness_screen as screen


FORBIDDEN_FIELD_PARTS = (
    "broker",
    "order",
    "account",
    "option",
    "p&l",
    "pnl",
    "sizing",
)

REPAIRED_SOURCE_BACKED_IDS = (
    "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001",
    "QQQ-REAL-HISTORICAL-CONTINUATION-001",
    "SPY-REAL-HISTORICAL-CONTINUATION-001",
    "SPY-REAL-HISTORICAL-IDEAL-001",
    "QQQ-REAL-HISTORICAL-IDEAL-001",
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002",
)


class CandidateCompletenessScreenTests(unittest.TestCase):
    def test_exactly_24_candidates_are_represented(self):
        rows = screen.build_candidate_pool()

        self.assertEqual(len(rows), 24)
        self.assertEqual(len({row["candidate_id"] for row in rows}), 24)

    def test_required_output_fields_exist_for_every_row(self):
        rows = screen.build_candidate_pool()

        for row in rows:
            self.assertEqual(set(screen.REQUIRED_OUTPUT_FIELDS), set(row))
            for field in screen.REQUIRED_OUTPUT_FIELDS:
                self.assertNotEqual(row[field], "")

    def test_missing_evidence_is_blocked_not_low_confidence(self):
        rows = screen.build_candidate_pool()
        blocked_rows = [row for row in rows if row["status"] == "blocked"]

        self.assertGreater(len(blocked_rows), 0)
        self.assertTrue(any("missing" in row["reason"].lower() for row in blocked_rows))
        self.assertFalse(any("low confidence" in row["reason"].lower() for row in rows))

    def test_pool_status_counts_match_day_39_helper_contract(self):
        rows = screen.build_candidate_pool()
        counts = {status: 0 for status in ("ready", "blocked", "replace", "drop")}
        for row in rows:
            counts[row["status"]] += 1

        self.assertEqual(counts, {"ready": 0, "blocked": 20, "replace": 3, "drop": 1})

    def test_duplicate_drop_replace_handling_works(self):
        rows = screen.build_candidate_pool()
        by_id = {row["candidate_id"]: row for row in rows}

        self.assertEqual(by_id["SPY-SOURCE-WINDOW-CONTINUATION-002"]["duplicate"], "yes")
        self.assertEqual(by_id["SPY-SOURCE-WINDOW-CONTINUATION-003"]["duplicate"], "yes")
        self.assertEqual(by_id["QQQ-SOURCE-WINDOW-CLEAN-FAST-BREAK-002"]["duplicate"], "yes")
        self.assertNotEqual(by_id["SPY-SOURCE-WINDOW-CONTINUATION-002"]["status"], "ready")
        self.assertIn("duplicate/already counted", by_id["SPY-SOURCE-WINDOW-CONTINUATION-002"]["reason"])
        self.assertIn("duplicate/already counted", by_id["SPY-SOURCE-WINDOW-CONTINUATION-003"]["reason"])
        self.assertIn("duplicate/already counted", by_id["QQQ-SOURCE-WINDOW-CLEAN-FAST-BREAK-002"]["reason"])
        self.assertEqual(by_id["SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-001"]["status"], "drop")
        self.assertEqual(by_id["SPY-SOURCE-WINDOW-CONTINUATION-005"]["status"], "replace")
        self.assertEqual(by_id["QQQ-SOURCE-WINDOW-CONTINUATION-002"]["status"], "replace")

    def test_duplicate_rows_are_blocked_even_if_source_decision_would_keep(self):
        status = screen._screen_status("keep", "keep_for_deeper_review", duplicate=True)

        self.assertEqual(status, "blocked")

    def test_source_backed_repaired_rows_do_not_show_false_missing_setup_fields(self):
        rows = screen.build_candidate_pool()
        by_id = {row["candidate_id"]: row for row in rows}

        for candidate_id in REPAIRED_SOURCE_BACKED_IDS:
            row = by_id[candidate_id]
            self.assertEqual(row["status"], "blocked")
            for field in ("source_lines", "setup_candle", "trigger", "invalidation", "outcome_window"):
                self.assertNotIn("MISSING", row[field])
            self.assertIn("UNCLEAR", row["freshness"])
            self.assertIn("UNCLEAR", row["blocker"])
            self.assertNotIn("MISSING", row["reason"])

    def test_ready_status_cannot_be_assigned_without_minimum_setup_time_completeness(self):
        rows = screen.build_candidate_pool()

        for row in rows:
            if row["status"] == "ready":
                for field in (
                    "setup_candle",
                    "trigger",
                    "invalidation",
                    "freshness",
                    "blocker",
                    "outcome_window",
                ):
                    self.assertNotIn("MISSING", row[field])
                    self.assertNotIn("UNCLEAR", row[field])
                self.assertEqual(row["duplicate"], "no")
        self.assertFalse(any(row["status"] == "ready" for row in rows))

    def test_no_proof_or_profitability_claims_are_present(self):
        rows = screen.build_candidate_pool()
        table = screen.format_ranked_table(rows)

        self.assertTrue(screen.NO_PROOF_ACCEPTED)
        self.assertFalse(screen.PROFITABILITY_CLAIMED)
        self.assertNotIn("proof accepted: yes", table.lower())
        self.assertNotIn("profitability claimed: yes", table.lower())

    def test_no_forbidden_live_broker_options_pnl_order_account_sizing_fields_are_introduced(self):
        self.assertFalse(
            any(part in field.lower() for field in screen.REQUIRED_OUTPUT_FIELDS for part in FORBIDDEN_FIELD_PARTS)
        )

        rows = screen.build_candidate_pool()
        for row in rows:
            self.assertFalse(any(part in key.lower() for key in row for part in FORBIDDEN_FIELD_PARTS))

    def test_command_line_stdout_table_path_works(self):
        output = io.StringIO()

        with redirect_stdout(output):
            screen.main()

        table = output.getvalue()
        self.assertIn("candidate_id", table)
        self.assertIn("source_lines", table)
        self.assertIn("SPY-SOURCE-WINDOW-CONTINUATION-002", table)
        self.assertEqual(len(table.strip().splitlines()), 26)


if __name__ == "__main__":
    unittest.main()
