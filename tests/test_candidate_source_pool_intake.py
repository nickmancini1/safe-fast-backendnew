import io
import unittest
from contextlib import redirect_stdout

from watcher_foundation import candidate_source_pool_intake as intake


STRICT_SOURCE_BACKED_IDS = {
    "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001",
    "QQQ-REAL-HISTORICAL-CONTINUATION-001",
    "SPY-REAL-HISTORICAL-CONTINUATION-001",
    "SPY-REAL-HISTORICAL-IDEAL-001",
    "QQQ-REAL-HISTORICAL-IDEAL-001",
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002",
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003",
}

EXPECTED_SURVIVAL_STATUSES = {
    "QQQ-REAL-HISTORICAL-CONTINUATION-001": "replace",
    "QQQ-REAL-HISTORICAL-IDEAL-001": "replace",
    "SPY-REAL-HISTORICAL-CONTINUATION-001": "replace",
    "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001": "parked/source_data_insufficient",
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003": "parked/source_data_insufficient",
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002": "parked/source_data_insufficient",
    "SPY-REAL-HISTORICAL-IDEAL-001": "parked/source_data_insufficient",
}

EXPECTED_PARKED_SOURCE_DATA_INSUFFICIENT_IDS = {
    "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001",
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003",
    "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002",
    "SPY-REAL-HISTORICAL-IDEAL-001",
}


class CandidateSourcePoolIntakeTests(unittest.TestCase):
    def test_inspects_full_24_row_pool_but_accepts_only_strict_source_backed_rows(self):
        result = intake.build_source_pool_intake()

        self.assertEqual(result["existing_screen_rows_inspected"], 24)
        self.assertEqual(result["expansion_signal_rows_inspected"], 36)
        self.assertEqual(result["source_pool_rows_inspected"], 60)
        self.assertEqual(result["accepted_intake_count"], 7)
        self.assertEqual({row["candidate_id"] for row in result["accepted_rows"]}, STRICT_SOURCE_BACKED_IDS)

    def test_accepted_rows_have_required_intake_fields_without_missing_values(self):
        result = intake.build_source_pool_intake()

        for row in result["accepted_rows"]:
            self.assertEqual(set(intake.INTAKE_OUTPUT_FIELDS), set(row))
            for field in (
                "source_file",
                "source_lines_section",
                "setup_candle",
                "trigger",
                "invalidation",
                "no_hindsight_boundary",
                "outcome_window",
            ):
                self.assertNotIn("MISSING", row[field])
                self.assertNotEqual(row[field], "")

    def test_no_rows_are_intake_ready_until_freshness_and_blocker_are_resolved(self):
        result = intake.build_source_pool_intake()

        self.assertEqual(result["intake_ready_count"], 0)
        self.assertEqual(result["blocked_count"], 4)
        self.assertEqual(result["drop_count"], 0)
        self.assertEqual(result["replace_count"], 3)
        self.assertEqual(result["duplicate_count"], 0)
        self.assertEqual(result["close_ready_count"], 4)
        self.assertTrue(result["fewer_than_5_intake_ready_rows_remain"])
        self.assertFalse(result["at_least_5_intake_ready_or_close_ready"])
        self.assertIn("freshness/final-signal", result["top_remaining_blocker_family"])

    def test_survival_status_counts_match_source_pool_intake_result(self):
        result = intake.build_source_pool_intake()

        self.assertEqual(result["survival_status_by_candidate"], EXPECTED_SURVIVAL_STATUSES)
        self.assertEqual(result["survival_active_blocked_count"], 0)
        self.assertEqual(result["survival_replace_count"], 3)
        self.assertEqual(result["survival_parked_count"], 4)
        self.assertEqual(result["survival_intake_ready_count"], 0)
        self.assertEqual(len(result["survival_map_rows"]), 7)

    def test_active_path_evidence_requirements_are_exposed_without_changing_counts(self):
        result = intake.build_source_pool_intake()
        requirements = result["active_path_evidence_requirements"]

        self.assertEqual(
            set(requirements["covered_candidate_ids"]),
            EXPECTED_PARKED_SOURCE_DATA_INSUFFICIENT_IDS,
        )
        self.assertEqual(requirements["active_blocked_candidate_ids"], ())
        self.assertEqual(
            set(requirements["parked_source_data_insufficient_candidate_ids"]),
            EXPECTED_PARKED_SOURCE_DATA_INSUFFICIENT_IDS,
        )
        self.assertEqual(requirements["covered_count"], 4)
        self.assertEqual(requirements["requirements_count"], 9)
        self.assertEqual(requirements["proof_allowed_count"], 0)
        self.assertEqual(result["accepted_intake_count"], 7)
        self.assertEqual(result["intake_ready_count"], 0)
        self.assertEqual(result["survival_active_blocked_count"], 0)
        self.assertEqual(result["survival_replace_count"], 3)
        self.assertEqual(result["survival_parked_count"], 4)

    def test_active_path_evidence_requirements_have_no_current_data_by_row(self):
        result = intake.build_source_pool_intake()
        requirements = result["active_path_evidence_requirements"]

        self.assertEqual(
            set(requirements["current_repo_has_enough_data_by_candidate"]),
            EXPECTED_PARKED_SOURCE_DATA_INSUFFICIENT_IDS,
        )
        self.assertTrue(
            all(
                has_enough is False
                for has_enough in requirements[
                    "current_repo_has_enough_data_by_candidate"
                ].values()
            )
        )
        for row in requirements["requirements_rows"]:
            self.assertNotEqual(row["exact_missing_rule_or_evidence"], "")
            self.assertNotEqual(row["source_file_or_doc"], "")
            self.assertFalse(row["proof_allowed"])

    def test_qqq_cfb_survival_action_is_exposed_by_source_pool_intake(self):
        result = intake.build_source_pool_intake()
        action = result["qqq_cfb_survival_action"]

        self.assertTrue(action["action_applied"])
        self.assertEqual(action["candidate_id"], "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001")
        self.assertEqual(action["status"], "parked/source_data_insufficient")
        self.assertIn("gap-context", " ".join(action["exact_missing_evidence"]))
        self.assertIn("Clean Fast Break stale/spent expiry", " ".join(action["exact_missing_evidence"]))
        self.assertIn("context/caution", " ".join(action["exact_missing_evidence"]))
        self.assertEqual(action["clean_rule_evidence"], ())
        self.assertFalse(action["proof_accepted"])
        self.assertFalse(action["profitability_claimed"])

    def test_spy_cfb_003_survival_action_is_exposed_by_source_pool_intake(self):
        result = intake.build_source_pool_intake()
        action = result["spy_cfb_003_survival_action"]

        self.assertTrue(action["action_applied"])
        self.assertEqual(action["candidate_id"], "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003")
        self.assertEqual(action["status"], "parked/source_data_insufficient")
        self.assertIn("higher-base/fresh-break expiry", " ".join(action["exact_missing_evidence"]))
        self.assertIn("context/caution", " ".join(action["exact_missing_evidence"]))
        self.assertEqual(action["clean_rule_evidence"], ())
        self.assertFalse(action["proof_accepted"])
        self.assertFalse(action["profitability_claimed"])

    def test_spy_cfb_002_survival_action_is_exposed_by_source_pool_intake(self):
        result = intake.build_source_pool_intake()
        action = result["spy_cfb_002_survival_action"]

        self.assertTrue(action["action_applied"])
        self.assertEqual(action["candidate_id"], "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002")
        self.assertEqual(action["status"], "parked/source_data_insufficient")
        self.assertIn("initial-break expiry", " ".join(action["exact_missing_evidence"]))
        self.assertIn("context/caution", " ".join(action["exact_missing_evidence"]))
        self.assertEqual(action["clean_rule_evidence"], ())
        self.assertFalse(action["proof_accepted"])
        self.assertFalse(action["profitability_claimed"])

    def test_spy_ideal_survival_action_is_exposed_by_source_pool_intake(self):
        result = intake.build_source_pool_intake()
        action = result["spy_ideal_survival_action"]

        self.assertTrue(action["action_applied"])
        self.assertEqual(action["candidate_id"], "SPY-REAL-HISTORICAL-IDEAL-001")
        self.assertEqual(action["status"], "parked/source_data_insufficient")
        self.assertIn("SPY Ideal stale/spent expiry", " ".join(action["exact_missing_evidence"]))
        self.assertIn("context/caution", " ".join(action["exact_missing_evidence"]))
        self.assertEqual(action["clean_rule_evidence"], ())
        self.assertFalse(action["proof_accepted"])
        self.assertFalse(action["profitability_claimed"])

    def test_spy_ideal_missing_evidence_keeps_intake_ready_zero(self):
        result = intake.build_source_pool_intake()
        by_id = {row["candidate_id"]: row for row in result["accepted_rows"]}

        self.assertEqual(by_id["SPY-REAL-HISTORICAL-IDEAL-001"]["status"], "blocked")
        self.assertIn(
            "missing Ideal-specific stale/spent expiry rule",
            by_id["SPY-REAL-HISTORICAL-IDEAL-001"]["freshness_missing_evidence"],
        )
        self.assertIn(
            "complete Ideal gap/headline/room caution review missing",
            by_id["SPY-REAL-HISTORICAL-IDEAL-001"]["blocker_missing_evidence"],
        )
        self.assertEqual(result["intake_ready_count"], 0)

    def test_lowercase_incomplete_is_case_insensitive_unresolved_blocker(self):
        row = {
            "candidate_id": "STRICT-ROW-WITH-LOWERCASE-INCOMPLETE",
            "source_lines": "source.csv lines 1-2",
            "setup_candle": "2026-01-01T09:30:00-05:00",
            "trigger": "trigger recorded",
            "invalidation": "invalidation recorded",
            "freshness": "incomplete",
            "blocker": "clean blocker/caution review recorded",
            "no_hindsight_boundary": "boundary recorded",
            "outcome_window": "terminal input recorded",
            "duplicate": "no",
            "status": "blocked",
        }

        self.assertFalse(intake._has_resolved_value(row["freshness"]))
        self.assertEqual(intake._intake_status(row), "blocked")
        self.assertNotEqual(intake._intake_status(row), "intake-ready")

    def test_duplicate_drop_replace_and_chart_shape_only_rows_are_rejected_at_intake(self):
        result = intake.build_source_pool_intake()
        accepted_ids = {row["candidate_id"] for row in result["accepted_rows"]}

        self.assertNotIn("SPY-SOURCE-WINDOW-CONTINUATION-002", accepted_ids)
        self.assertNotIn("SPY-SOURCE-WINDOW-CONTINUATION-003", accepted_ids)
        self.assertNotIn("QQQ-SOURCE-WINDOW-CLEAN-FAST-BREAK-002", accepted_ids)
        self.assertNotIn("SPY-SOURCE-WINDOW-CLEAN-FAST-BREAK-003", accepted_ids)
        self.assertNotIn("SPY-SOURCE-WINDOW-CONTINUATION-005", accepted_ids)
        self.assertNotIn("SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-001", accepted_ids)

    def test_missing_no_hindsight_boundary_rejects_otherwise_source_backed_row(self):
        row = {
            "candidate_id": "STRICT-ROW-WITH-MISSING-NO-HINDSIGHT",
            "source_lines": "source.csv lines 1-2",
            "setup_candle": "2026-01-01T09:30:00-05:00",
            "trigger": "trigger recorded",
            "invalidation": "invalidation recorded",
            "no_hindsight_boundary": "MISSING",
            "outcome_window": "terminal input recorded",
            "duplicate": "no",
            "status": "blocked",
        }

        self.assertFalse(intake._strictly_source_backed(row))

    def test_reports_exact_blocker_when_local_sources_do_not_support_20_to_50_strict_rows(self):
        result = intake.build_source_pool_intake()

        self.assertEqual(result["maximum_strict_candidates_found"], 7)
        self.assertIn("do not support 20-50 strict candidates", result["exact_blocker"])
        self.assertGreaterEqual(len(result["source_files_inspected"]), 1)
        self.assertIn("Continuation has been narrowed", result["smallest_next_evidence_backed_fix"])
        self.assertIn("SPY Continuation intrabar-dependent rows", result["smallest_next_evidence_backed_fix"])
        self.assertIn("Ideal has been narrowed", result["smallest_next_evidence_backed_fix"])
        self.assertIn(
            "parked/source_data_insufficient",
            result["smallest_next_evidence_backed_fix"],
        )
        self.assertIn("context/caution review remains source-data insufficient", result["smallest_next_evidence_backed_fix"])
        self.assertIn("room/risk thresholds", result["smallest_next_evidence_backed_fix"])

    def test_real_historical_expansion_adds_one_non_duplicate_strict_blocked_row(self):
        result = intake.build_source_pool_intake()
        by_id = {row["candidate_id"]: row for row in result["accepted_rows"]}
        added = by_id["SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003"]

        self.assertEqual(result["new_candidates_added"], ["SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003"])
        self.assertIn("third_real_spy_clean_fast_break_replay_v1_signal_log.jsonl", added["source_file"])
        self.assertIn("signal log line 5", added["source_lines_section"])
        self.assertIn("source CSV line 154", added["source_lines_section"])
        self.assertIn("2026-04-15T14:30:00-04:00", added["setup_candle"])
        self.assertIn("698.65", added["trigger"])
        self.assertIn("694.2801", added["invalidation"])
        self.assertEqual(added["status"], "blocked")
        self.assertEqual(added["duplicate"], "no")
        self.assertIn("higher-base/fresh-break stale/spent expiry rule", added["reason"])

    def test_expansion_rejected_families_are_reported_without_promoting_no_trade_rows(self):
        result = intake.build_source_pool_intake()
        rejected = "; ".join(result["rejected_row_families"])

        self.assertIn("already-blocked six-row anchor preserved, not re-drilled: 6", rejected)
        self.assertIn("no-trade/rejected signal-log rows without completed trigger: 29", rejected)

    def test_blocked_row_reasons_preserve_specific_freshness_and_blocker_evidence(self):
        result = intake.build_source_pool_intake()
        by_id = {row["candidate_id"]: row for row in result["accepted_rows"]}

        self.assertIn(
            "outside narrowed Continuation path",
            by_id["QQQ-REAL-HISTORICAL-CONTINUATION-001"]["reason"],
        )
        self.assertEqual(by_id["QQQ-REAL-HISTORICAL-CONTINUATION-001"]["status"], "replace")
        self.assertEqual(by_id["SPY-REAL-HISTORICAL-CONTINUATION-001"]["status"], "replace")
        self.assertIn(
            "outside narrowed Continuation path",
            by_id["SPY-REAL-HISTORICAL-CONTINUATION-001"]["reason"],
        )
        self.assertIn(
            "only 1H OHLCV source rows exist",
            by_id["SPY-REAL-HISTORICAL-CONTINUATION-001"]["reason"],
        )
        self.assertEqual(by_id["QQQ-REAL-HISTORICAL-IDEAL-001"]["status"], "replace")
        self.assertIn(
            "outside narrowed Ideal path",
            by_id["QQQ-REAL-HISTORICAL-IDEAL-001"]["reason"],
        )
        self.assertIn(
            "no accepted risk/room threshold",
            by_id["QQQ-REAL-HISTORICAL-IDEAL-001"]["reason"],
        )
        self.assertEqual(by_id["SPY-REAL-HISTORICAL-IDEAL-001"]["status"], "blocked")
        self.assertIn(
            "Clean Fast Break initial-break expiry threshold",
            by_id["SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002"]["reason"],
        )

    def test_clean_fast_break_rows_remain_blocked_after_rule_decisions(self):
        result = intake.build_source_pool_intake()
        by_id = {row["candidate_id"]: row for row in result["accepted_rows"]}

        expected_reason_parts = {
            "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001": "gap-context and CFB expiry source insufficiency",
            "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003": (
                "CFB expiry and context/caution rule insufficiency"
            ),
            "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002": (
                "CFB expiry and context/caution rule insufficiency"
            ),
        }

        for candidate_id, reason_part in expected_reason_parts.items():
            self.assertEqual(by_id[candidate_id]["status"], "blocked")
            self.assertIn(reason_part, by_id[candidate_id]["reason"])

        self.assertEqual(result["intake_ready_count"], 0)

    def test_context_caution_decision_keeps_affected_rows_blocked(self):
        result = intake.build_source_pool_intake()
        by_id = {row["candidate_id"]: row for row in result["accepted_rows"]}
        affected = {
            "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001",
            "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003",
            "SPY-REAL-HISTORICAL-IDEAL-001",
            "SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002",
        }

        for candidate_id in affected:
            self.assertEqual(by_id[candidate_id]["status"], "blocked")
            self.assertIn(
                "applied context/caution source-data insufficiency decision",
                by_id[candidate_id]["reason"],
            )

        self.assertEqual(result["accepted_intake_count"], 7)
        self.assertEqual(result["intake_ready_count"], 0)
        self.assertEqual(result["close_ready_count"], 4)

    def test_integrated_rows_preserve_exact_missing_state_evidence(self):
        result = intake.build_source_pool_intake()
        by_id = {row["candidate_id"]: row for row in result["accepted_rows"]}

        self.assertIn(
            "missing source-backed gap_context field/rule",
            by_id["QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001"]["freshness_missing_evidence"],
        )
        self.assertIn(
            "missing next-session Continuation freshness/carry-forward rule",
            by_id["QQQ-REAL-HISTORICAL-CONTINUATION-001"]["freshness_missing_evidence"],
        )
        self.assertIn(
            "missing Ideal-specific stale/spent expiry rule",
            by_id["SPY-REAL-HISTORICAL-IDEAL-001"]["freshness_missing_evidence"],
        )
        self.assertIn(
            "missing accepted wide-risk or room threshold",
            by_id["QQQ-REAL-HISTORICAL-IDEAL-001"]["blocker_missing_evidence"],
        )
        self.assertIn(
            "CONTEXT_24H_DAILY_UNCONFIRMED",
            by_id["SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-002"]["blocker_missing_evidence"],
        )

    def test_no_proof_or_profitability_claims_are_present(self):
        result = intake.build_source_pool_intake()
        report = intake.format_intake_report(result)

        self.assertTrue(intake.NO_PROOF_ACCEPTED)
        self.assertFalse(intake.PROFITABILITY_CLAIMED)
        self.assertFalse(result["proof_accepted"])
        self.assertFalse(result["profitability_claimed"])
        self.assertNotIn("proof accepted: yes", report.lower())
        self.assertNotIn("profitability claimed: yes", report.lower())

    def test_command_line_stdout_report_path_works(self):
        output = io.StringIO()

        with redirect_stdout(output):
            intake.main()

        report = output.getvalue()
        self.assertIn("source-pool rows inspected: 60", report)
        self.assertIn("accepted intake count: 7", report)
        self.assertIn("blocked/drop/replace/duplicate counts: 4/0/3/0", report)
        self.assertIn("new strict candidates added: SPY-REAL-HISTORICAL-CLEAN-FAST-BREAK-003", report)
        self.assertIn("fewer than 5 intake-ready rows remain: YES", report)
        self.assertIn(
            "survival active_blocked/replace/parked/intake_ready counts: 0/3/4/0",
            report,
        )
        self.assertIn("active-path evidence rows covered: 4", report)
        self.assertIn("active-path proof allowed count: 0", report)
        self.assertIn(
            "QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001=NO",
            report,
        )
        self.assertIn("QQQ CFB survival action applied: YES", report)
        self.assertIn("QQQ CFB status: parked/source_data_insufficient", report)
        self.assertIn("SPY CFB 003 survival action applied: YES", report)
        self.assertIn("SPY CFB 003 status: parked/source_data_insufficient", report)
        self.assertIn("SPY CFB 002 survival action applied: YES", report)
        self.assertIn("SPY CFB 002 status: parked/source_data_insufficient", report)
        self.assertIn("SPY Ideal survival action applied: YES", report)
        self.assertIn("SPY Ideal status: parked/source_data_insufficient", report)
        self.assertIn("ranked intake table:", report)
        self.assertIn("QQQ-REAL-HISTORICAL-CLEAN-FAST-BREAK-001", report)


if __name__ == "__main__":
    unittest.main()
