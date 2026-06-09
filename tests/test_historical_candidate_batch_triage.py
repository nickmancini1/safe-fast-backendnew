import copy
import unittest

from watcher_foundation.historical_candidate_batch_triage import (
    HISTORICAL_CANDIDATE_BATCH_TRIAGE_RESULT_FIELDS,
    triage_historical_candidate_batch,
)


def candidate(candidate_id="SPY-IDEAL-001", symbol="SPY", setup_type="Ideal", **overrides):
    base = {
        "candidate_id": candidate_id,
        "symbol": symbol,
        "setup_type": setup_type,
        "source_window_id": f"{symbol}-{setup_type}-WINDOW-001",
        "row_count": 12,
        "has_setup_time_row": True,
        "has_trigger": True,
        "has_invalidation": True,
        "has_freshness": True,
        "has_blocker_review": True,
        "has_terminal_outcome": True,
        "has_no_hindsight_boundary": True,
        "has_after_setup_outcome_window": True,
        "evidence_used": ["caller_provided_setup_time_fields"],
        "missing_evidence": [],
        "notes": "directionally favorable movement is not proof",
        "watch_only": True,
        "no_trade_decision": True,
    }
    base.update(overrides)
    return base


class HistoricalCandidateBatchTriageTests(unittest.TestCase):
    def test_batch_with_multiple_symbols_and_setup_types_produces_counts_by_symbol_setup_pair(self):
        result = triage_historical_candidate_batch(
            [
                candidate("SPY-IDEAL-001", "SPY", "Ideal"),
                candidate("QQQ-CFB-001", "QQQ", "Clean Fast Break"),
                candidate("IWM-CONT-001", "IWM", "Continuation"),
                candidate("GLD-IDEAL-001", "GLD", "Ideal"),
            ],
            minimum_sample_size=4,
        )

        self.assertEqual(result["total_candidates"], 4)
        self.assertEqual(result["symbol_counts"]["SPY"], 1)
        self.assertEqual(result["symbol_counts"]["QQQ"], 1)
        self.assertEqual(result["symbol_counts"]["IWM"], 1)
        self.assertEqual(result["symbol_counts"]["GLD"], 1)
        self.assertEqual(result["setup_type_counts"]["Ideal"], 2)
        self.assertEqual(result["setup_type_counts"]["Clean Fast Break"], 1)
        self.assertEqual(result["setup_type_counts"]["Continuation"], 1)
        self.assertEqual(result["pair_counts"]["SPY|Ideal"], 1)
        self.assertEqual(result["pair_counts"]["QQQ|Clean Fast Break"], 1)
        self.assertEqual(result["pair_counts"]["IWM|Continuation"], 1)
        self.assertEqual(result["pair_counts"]["GLD|Ideal"], 1)

    def test_complete_candidate_becomes_ready_for_deeper_review_but_not_accepted_proof(self):
        result = triage_historical_candidate_batch([candidate()], minimum_sample_size=1)

        self.assertEqual(result["status_counts"]["ready_for_deeper_review"], 1)
        ready = result["ready_candidates"][0]
        self.assertEqual(ready["triage_status"], "ready_for_deeper_review")
        self.assertFalse(ready["accepted_proof"])
        self.assertFalse(ready["profitability_claimed"])
        for field_name in HISTORICAL_CANDIDATE_BATCH_TRIAGE_RESULT_FIELDS:
            self.assertIn(field_name, result)

    def test_missing_trigger_blocks_candidate(self):
        result = triage_historical_candidate_batch(
            [candidate(has_trigger=False)],
            minimum_sample_size=1,
        )

        self.assertEqual(result["status_counts"]["blocked_missing_evidence"], 1)
        self.assertIn("trigger", result["blocked_candidates"][0]["missing_evidence"])

    def test_missing_invalidation_blocks_candidate(self):
        result = triage_historical_candidate_batch(
            [candidate(has_invalidation=False)],
            minimum_sample_size=1,
        )

        self.assertEqual(result["status_counts"]["blocked_missing_evidence"], 1)
        self.assertIn("invalidation", result["blocked_candidates"][0]["missing_evidence"])

    def test_missing_freshness_blocks_candidate(self):
        result = triage_historical_candidate_batch(
            [candidate(has_freshness=False)],
            minimum_sample_size=1,
        )

        self.assertEqual(result["status_counts"]["blocked_missing_evidence"], 1)
        self.assertIn("freshness", result["blocked_candidates"][0]["missing_evidence"])

    def test_missing_blocker_review_blocks_candidate(self):
        result = triage_historical_candidate_batch(
            [candidate(has_blocker_review=False)],
            minimum_sample_size=1,
        )

        self.assertEqual(result["status_counts"]["blocked_missing_evidence"], 1)
        self.assertIn("blocker_review", result["blocked_candidates"][0]["missing_evidence"])

    def test_missing_no_hindsight_boundary_blocks_candidate(self):
        result = triage_historical_candidate_batch(
            [candidate(has_no_hindsight_boundary=False)],
            minimum_sample_size=1,
        )

        self.assertEqual(result["status_counts"]["blocked_missing_evidence"], 1)
        self.assertIn("no_hindsight_boundary", result["blocked_candidates"][0]["missing_evidence"])

    def test_missing_terminal_outcome_blocks_unless_not_required(self):
        blocked = triage_historical_candidate_batch(
            [candidate(has_terminal_outcome=False)],
            minimum_sample_size=1,
        )
        ready = triage_historical_candidate_batch(
            [candidate(has_terminal_outcome=False)],
            minimum_sample_size=1,
            terminal_outcome_required=False,
        )

        self.assertEqual(blocked["status_counts"]["blocked_missing_evidence"], 1)
        self.assertIn("terminal_outcome", blocked["blocked_candidates"][0]["missing_evidence"])
        self.assertEqual(ready["status_counts"]["ready_for_deeper_review"], 1)

    def test_unknown_symbol_is_invalid_input(self):
        result = triage_historical_candidate_batch(
            [candidate(symbol="DIA")],
            minimum_sample_size=1,
        )

        self.assertEqual(result["status_counts"]["invalid_input"], 1)
        self.assertIn("unknown_symbol", result["invalid_candidates"][0]["invalid_reasons"])

    def test_unknown_setup_type_is_invalid_input(self):
        result = triage_historical_candidate_batch(
            [candidate(setup_type="Breakout")],
            minimum_sample_size=1,
        )

        self.assertEqual(result["status_counts"]["invalid_input"], 1)
        self.assertIn("unknown_setup_type", result["invalid_candidates"][0]["invalid_reasons"])

    def test_unavailable_candidate_stays_unavailable(self):
        result = triage_historical_candidate_batch(
            [candidate(status="unavailable", missing_evidence=["source_window_unavailable"])],
            minimum_sample_size=1,
        )

        self.assertEqual(result["status_counts"]["unavailable"], 1)
        self.assertEqual(result["unavailable_candidates"][0]["triage_status"], "unavailable")
        self.assertEqual(result["fastest_next_actions"][0]["next_action"], "find cleaner replacement")

    def test_reject_not_clean_enough_candidate_is_counted_as_rejected(self):
        result = triage_historical_candidate_batch(
            [candidate(triage_status="reject_not_clean_enough")],
            minimum_sample_size=1,
        )

        self.assertEqual(result["status_counts"]["reject_not_clean_enough"], 1)
        self.assertEqual(result["rejected_candidates"][0]["triage_status"], "reject_not_clean_enough")
        self.assertEqual(result["fastest_next_actions"][0]["next_action"], "reject/drop candidate")

    def test_tiny_sample_warning_appears_under_minimum_sample_size(self):
        result = triage_historical_candidate_batch([candidate()], minimum_sample_size=2)

        self.assertIn("tiny_sample_risk", result["tiny_sample_warning"])

    def test_caller_can_override_minimum_sample_size(self):
        result = triage_historical_candidate_batch([candidate()], minimum_sample_size=1)

        self.assertIsNone(result["tiny_sample_warning"])

    def test_forbidden_broker_order_account_options_pnl_fields_are_rejected_or_surfaced(self):
        result = triage_historical_candidate_batch(
            [
                candidate(
                    broker_order_id="not-allowed",
                    nested={"account": "not-allowed", "options_pnl": 1},
                )
            ],
            minimum_sample_size=1,
        )

        invalid = result["invalid_candidates"][0]
        self.assertEqual(invalid["triage_status"], "invalid_input")
        self.assertIn(
            "forbidden_live_broker_order_account_options_or_pnl_fields",
            invalid["invalid_reasons"],
        )
        self.assertIn("forbidden_paths", invalid["missing_evidence"][0])

    def test_caller_input_is_not_mutated(self):
        payload = [candidate()]
        original = copy.deepcopy(payload)

        result = triage_historical_candidate_batch(payload, minimum_sample_size=1)
        result["ready_candidates"][0]["evidence_used"].append("mutated")
        result["ready_candidates"][0]["missing_evidence"].append("mutated")

        self.assertEqual(payload, original)

    def test_batch_output_never_claims_profitability(self):
        result = triage_historical_candidate_batch([candidate()], minimum_sample_size=1)

        self.assertFalse(result["profitability_claimed"])
        self.assertFalse(result["ready_candidates"][0]["profitability_claimed"])

    def test_batch_output_accepted_proof_count_is_always_zero(self):
        result = triage_historical_candidate_batch(
            [candidate(accepted_proof=True), candidate(profitability_claimed=True)],
            minimum_sample_size=1,
        )

        self.assertEqual(result["accepted_proof_count"], 0)
        self.assertFalse(result["ready_candidates"][0]["accepted_proof"])
        self.assertFalse(result["ready_candidates"][1]["accepted_proof"])


if __name__ == "__main__":
    unittest.main()
