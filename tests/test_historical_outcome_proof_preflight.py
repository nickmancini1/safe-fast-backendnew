import copy
import unittest
from unittest.mock import patch

from watcher_foundation import (
    HISTORICAL_OUTCOME_PROOF_PREFLIGHT_RESULT_FIELDS,
    validate_historical_outcome_proof_batch,
    validate_historical_outcome_proof_row,
)


class HistoricalOutcomeProofPreflightTests(unittest.TestCase):
    def _unavailable_item(self, field_name):
        return {
            "field_name": field_name,
            "status": "unavailable",
            "reason": "caller did not provide source-backed proof value",
            "fabricated": False,
        }

    def _row(self, **overrides):
        row = {
            "outcome_row_id": "historical-proof-row-1",
            "source_review_packet_id": "review-packet-1",
            "symbol": "SPY",
            "timeframe": "1h_rth",
            "setup_type": "Ideal",
            "direction": "bullish/call-side",
            "detection_timestamp": "2026-05-24T09:35:00-04:00",
            "outcome_review_timestamp": "2026-05-25T16:00:00-04:00",
            "stage_at_detection": "near-trigger",
            "trigger_status_at_detection": "near_trigger",
            "trigger_reference": {
                "kind": "caller_provided_chart_reference",
                "value": "432 reclaim zone",
                "fabricated": False,
            },
            "invalidation_reference": {
                "kind": "caller_provided_chart_reference",
                "value": "below local shelf",
                "fabricated": False,
            },
            "outcome_window": {
                "start_timestamp": "2026-05-24T10:30:00-04:00",
                "end_timestamp": "2026-05-25T16:00:00-04:00",
                "caller_provided": True,
            },
            "outcome_status": "partial_follow_through",
            "follow_through_status": "observed",
            "failure_status": "not_observed",
            "mfe": {"value": 1.25, "unit": "R", "fabricated": False},
            "mae": {"value": -0.35, "unit": "R", "fabricated": False},
            "time_to_follow_through": "3h",
            "time_to_failure": None,
            "stale_spent_outcome": "not_stale_or_spent",
            "blocker_caution_outcome": "no_blocker_materialized",
            "evidence_refs": ["review-packet-1.accepted_rows[0]", "chart-row-218"],
            "unavailable_fields": [
                self._unavailable_item("time_to_failure"),
            ],
            "no_hindsight_boundary": {
                "evidence_available_at_or_before_review_timestamp": True,
                "future_evidence_not_used": True,
                "future_evidence_outside_declared_window_used": False,
                "no_backfilled_outcome_labels": True,
                "review_timestamp_field": "outcome_review_timestamp",
                "outcome_window_field": "outcome_window",
            },
            "diagnostics_placeholders": {
                "failure_category": {
                    "status": "placeholder_only_until_reviewed_outcomes_accumulate"
                }
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
            "historical_review_boundary": {
                "caller_provided": True,
                "historical_review_only": True,
                "no_live_data": True,
                "no_controlled_shadow_data": True,
                "no_generated_report": True,
            },
        }
        row.update(overrides)
        return row

    def test_valid_caller_provided_historical_outcome_proof_row_passes(self):
        result = validate_historical_outcome_proof_row(self._row())

        self.assertEqual(result["outcome_row_id"], "historical-proof-row-1")
        self.assertTrue(result["watch_only"])
        self.assertTrue(result["historical_review_boundary"]["caller_provided"])

    def test_row_shaped_for_existing_outcome_scoring_contract_is_accepted(self):
        result = validate_historical_outcome_proof_row(self._row())

        self.assertEqual(result["setup_type"], "Ideal")
        self.assertEqual(result["trigger_status_at_detection"], "near_trigger")
        self.assertEqual(result["evidence_refs"][0], "review-packet-1.accepted_rows[0]")

    def test_row_missing_required_outcome_scoring_contract_shape_is_rejected(self):
        row = self._row()
        del row["outcome_status"]

        with self.assertRaisesRegex(ValueError, "outcome_status"):
            validate_historical_outcome_proof_row(row)

    def test_no_hindsight_historical_review_boundary_is_required_and_preserved(self):
        row = self._row()
        del row["no_hindsight_boundary"]

        with self.assertRaisesRegex(ValueError, "no_hindsight_boundary"):
            validate_historical_outcome_proof_row(row)

        row = self._row()
        row["no_hindsight_boundary"]["future_evidence_outside_declared_window_used"] = True

        with self.assertRaisesRegex(ValueError, "outside the declared outcome_window"):
            validate_historical_outcome_proof_row(row)

        result = validate_historical_outcome_proof_batch([self._row()])

        self.assertTrue(result["no_hindsight_boundary_preserved"])

    def test_key_historical_proof_references_must_be_explicit(self):
        explicit_fields = (
            "symbol",
            "setup_type",
            "timeframe",
            "trigger_reference",
            "invalidation_reference",
            "outcome_window",
            "evidence_refs",
        )
        for field_name in explicit_fields:
            with self.subTest(field_name=field_name):
                row = self._row()
                row[field_name] = "" if field_name in {"symbol", "setup_type", "timeframe"} else []
                with self.assertRaisesRegex(
                    (TypeError, ValueError),
                    field_name,
                ):
                    validate_historical_outcome_proof_row(row)

        with self.assertRaisesRegex(TypeError, "unavailable_fields"):
            validate_historical_outcome_proof_row(
                self._row(unavailable_fields="not-explicit")
            )

    def test_fabricated_proof_values_are_rejected(self):
        for marker in (
            "FABRICATED",
            "MADE_UP",
            "ASSUMED_WITHOUT_EVIDENCE",
            "INVENTED",
            "UNKNOWN_BUT_FILLED",
            "FAKE",
        ):
            with self.subTest(marker=marker):
                with self.assertRaisesRegex(ValueError, "Fabricated proof marker"):
                    validate_historical_outcome_proof_row(
                        self._row(outcome_status=marker)
                    )

        row = self._row()
        row["trigger_reference"]["fabricated"] = True
        with self.assertRaisesRegex(ValueError, "Fabricated proof value"):
            validate_historical_outcome_proof_row(row)

    def test_forbidden_execution_field_is_rejected_recursively(self):
        row = self._row()
        row["nested"] = {"proof": [{"trade_decision": "approve"}]}

        with self.assertRaisesRegex(ValueError, "Forbidden execution/trade field"):
            validate_historical_outcome_proof_row(row)

    def test_batch_returns_in_memory_accepted_and_rejected_row_results(self):
        result = validate_historical_outcome_proof_batch(
            [
                self._row(),
                self._row(outcome_row_id="historical-proof-row-2"),
                self._row(outcome_row_id="bad-row", watch_only=False),
            ]
        )

        self.assertEqual(
            set(HISTORICAL_OUTCOME_PROOF_PREFLIGHT_RESULT_FIELDS),
            set(result),
        )
        self.assertEqual(result["rows_processed"], 3)
        self.assertEqual(result["rows_accepted"], 2)
        self.assertEqual(result["rows_rejected"], 1)
        self.assertEqual(result["rejected_rows"][0]["row_id"], "bad-row")
        self.assertIn("watch_only=True", result["rejected_rows"][0]["reason"])
        self.assertIs(result["historical_outcome_preflight_only"], True)
        self.assertIs(result["controlled_shadow_data_started"], False)

    def test_invalid_row_type_fails(self):
        with self.assertRaisesRegex(TypeError, "row must be a dict"):
            validate_historical_outcome_proof_row("bad")

    def test_invalid_batch_type_fails(self):
        with self.assertRaisesRegex(TypeError, "batch must be a list"):
            validate_historical_outcome_proof_batch((self._row(),))

    def test_watch_only_false_fails(self):
        with self.assertRaisesRegex(ValueError, "watch_only=True"):
            validate_historical_outcome_proof_row(self._row(watch_only=False))

    def test_live_data_or_controlled_shadow_boundary_failure_fails(self):
        row = self._row()
        row["historical_review_boundary"]["no_live_data"] = False

        with self.assertRaisesRegex(ValueError, "no_live_data=True"):
            validate_historical_outcome_proof_row(row)

        row = self._row()
        row["historical_review_boundary"]["no_controlled_shadow_data"] = False

        with self.assertRaisesRegex(ValueError, "no_controlled_shadow_data=True"):
            validate_historical_outcome_proof_row(row)

    def test_validator_returns_defensive_copies(self):
        row = self._row()
        before = copy.deepcopy(row)
        result = validate_historical_outcome_proof_row(row)

        result["mfe"]["value"] = 99
        result["historical_review_boundary"]["caller_provided"] = False

        self.assertEqual(row, before)
        self.assertEqual(row["mfe"]["value"], 1.25)
        self.assertTrue(row["historical_review_boundary"]["caller_provided"])

    def test_no_file_network_subprocess_or_live_workflow_side_effects(self):
        row = self._row()
        before = copy.deepcopy(row)

        with patch("builtins.open") as open_mock, patch(
            "socket.socket"
        ) as socket_mock, patch("subprocess.run") as subprocess_mock:
            result = validate_historical_outcome_proof_batch([row])

        self.assertEqual(row, before)
        self.assertEqual(result["rows_accepted"], 1)
        self.assertIs(result["watch_only"], True)
        self.assertIs(result["historical_outcome_preflight_only"], True)
        self.assertIs(result["no_hindsight_boundary_preserved"], True)
        self.assertIs(result["no_trade_boundary_preserved"], True)
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
