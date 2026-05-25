import builtins
import os
import pathlib
import socket
import subprocess
import threading
import unittest
from unittest import mock

from watcher_foundation.constants import FORBIDDEN_EXECUTION_FIELD_NAMES
from watcher_foundation.replay_regression import (
    ReplayRegressionCase,
    run_local_replay_regression,
)


FINAL_SWEEP_FORBIDDEN_FIELDS = FORBIDDEN_EXECUTION_FIELD_NAMES | {
    "live_trade_decision",
    "live_trade_decisions",
    "trade_decision",
    "trade_decision_status",
    "trade_decisions",
}


class WatcherReplayBoundaryFinalSweepTests(unittest.TestCase):
    def _fixture_observation(self, setup_type="Ideal", **overrides):
        fixture_slug = setup_type.lower().replace(" ", "-")
        observation = {
            "candidate_id": f"SYNF-{fixture_slug}-candidate",
            "symbol": "SYNF",
            "watch_session_id": f"{fixture_slug}-final-sweep-session",
            "setup_type": setup_type,
            "direction": "bullish/call-side",
            "regular_session_date": "2099-05-01",
            "first_seen_at": "2099-05-01T09:32:00-04:00",
            "last_seen_at": "2099-05-01T09:32:00-04:00",
            "stage": "near-trigger",
            "trigger_status": "near_trigger",
            "fresh_stale_spent_state": "fresh",
            "trigger_level_or_zone": f"{fixture_slug}-synthetic-review-zone",
            "trigger_zone_bucket": f"{fixture_slug}-synthetic-zone-bucket",
            "confirmation_timeframe_rule": "synthetic completed-candle review",
            "distance_to_trigger": "near",
            "invalidation_level_or_condition": (
                "synthetic review invalidation condition"
            ),
            "invalidation_bucket": f"{fixture_slug}-synthetic-invalidation",
            "source_kind": "local_fixture",
            "source_as_of": "2099-05-01T09:32:00-04:00",
            "evidence_rows": [f"{fixture_slug}-synthetic-evidence-1"],
            "evidence_quality": "deterministic",
            "unavailable_fields": [],
            "blockers": [],
            "cautions": [],
            "primary_blocker": "synthetic_local_final_sweep_only",
            "no_trade_reason": "watch_only_shadow_review_no_live_trade_approval",
            "next_check_or_next_alert_condition": "new_material_change_required",
            "trigger_path_identifier": f"{fixture_slug}-final-sweep-path",
            "fresh_trigger_path_present": True,
            "watch_only": True,
        }
        observation.update(overrides)
        return observation

    def _find_key_paths(self, value, field_name, path=()):
        matches = []
        if isinstance(value, dict):
            for key, nested_value in value.items():
                nested_path = (*path, str(key))
                if str(key).lower() == field_name:
                    matches.append(".".join(nested_path))
                matches.extend(
                    self._find_key_paths(nested_value, field_name, nested_path)
                )
        elif isinstance(value, (list, tuple)):
            for index, nested_value in enumerate(value):
                matches.extend(
                    self._find_key_paths(nested_value, field_name, (*path, str(index)))
                )
        return matches

    def _assert_no_forbidden_fields(self, value):
        for field_name in FINAL_SWEEP_FORBIDDEN_FIELDS:
            self.assertEqual(
                [],
                self._find_key_paths(value, field_name),
                f"Forbidden replay boundary field leaked: {field_name}",
            )

    def _assert_watch_only_true_everywhere(self, value, path=()):
        if isinstance(value, dict):
            for key, nested_value in value.items():
                nested_path = (*path, str(key))
                if str(key) == "watch_only":
                    self.assertIs(
                        nested_value,
                        True,
                        f"watch_only was not true at {'.'.join(nested_path)}",
                    )
                self._assert_watch_only_true_everywhere(nested_value, nested_path)
        elif isinstance(value, (list, tuple)):
            for index, nested_value in enumerate(value):
                self._assert_watch_only_true_everywhere(
                    nested_value, (*path, str(index))
                )

    def test_boundary_outputs_emit_no_execution_or_trade_decision_fields(self):
        result = run_local_replay_regression(
            [
                ReplayRegressionCase(
                    name="synthetic-final-sweep-triggered-boundary",
                    observations=[
                        self._fixture_observation(
                            "Clean Fast Break",
                            stage="triggered_signal_stage",
                            trigger_status="triggered",
                            no_trade_reason=(
                                "triggered_for_shadow_signal_review_only_no_live_trade_approval"
                            ),
                        )
                    ],
                    expected_absent_fields=sorted(FINAL_SWEEP_FORBIDDEN_FIELDS),
                    expected_values={
                        "watch_only": True,
                        "no_trade_boundary.watch_only": True,
                        "no_trade_boundary.no_live_trade_approval": True,
                        "no_trade_boundary.trade_approval": False,
                        "no_trade_boundary.live_trade_approval": False,
                    },
                )
            ]
        )

        self.assertEqual(result["cases_failed"], 0, result["case_results"])
        self._assert_no_forbidden_fields(result)
        self._assert_watch_only_true_everywhere(result)
        self.assertFalse(result["no_trade_boundary"]["trade_approval"])
        self.assertFalse(result["no_trade_boundary"]["live_trade_approval"])

    def test_nested_forbidden_inputs_are_rejected_for_each_boundary_family(self):
        forbidden_payloads = {
            "broker": {"outer": [{"inner": {"broker": "forbidden"}}]},
            "order_id": {"outer": [{"inner": {"order_id": "forbidden"}}]},
            "account_id": {"outer": [{"inner": {"account_id": "forbidden"}}]},
            "option_symbol": {"outer": [{"inner": {"option_symbol": "forbidden"}}]},
            "pnl": {"outer": [{"inner": {"pnl": "forbidden"}}]},
            "trade_decision": {
                "outer": [{"inner": {"trade_decision": "forbidden"}}]
            },
            "live_trade_decision": {
                "outer": [{"inner": {"live_trade_decision": "forbidden"}}]
            },
        }

        for field_name, payload in forbidden_payloads.items():
            with self.subTest(field_name=field_name):
                with self.assertRaises(ValueError):
                    run_local_replay_regression(
                        [
                            ReplayRegressionCase(
                                name=f"synthetic-final-sweep-forbidden-{field_name}",
                                observations=[
                                    self._fixture_observation("Ideal", **payload)
                                ],
                            )
                        ]
                    )

    def test_success_and_failure_results_preserve_watch_only_boundary(self):
        result = run_local_replay_regression(
            [
                ReplayRegressionCase(
                    name="synthetic-final-sweep-success",
                    observations=[self._fixture_observation("Ideal")],
                    expected_values={"final_state.setup_type": "Ideal"},
                ),
                ReplayRegressionCase(
                    name="synthetic-final-sweep-failure",
                    observations=[self._fixture_observation("Continuation")],
                    expected_values={"final_state.setup_type": "Ideal"},
                ),
            ]
        )

        self.assertEqual(result["cases_processed"], 2)
        self.assertEqual(result["cases_passed"], 1)
        self.assertEqual(result["cases_failed"], 1)
        self._assert_watch_only_true_everywhere(result)
        self.assertTrue(result["no_trade_boundary"]["no_live_trade_approval"])
        self.assertFalse(result["no_trade_boundary"]["trade_approval"])
        self.assertFalse(result["no_trade_boundary"]["live_trade_approval"])

    def test_replay_execution_is_local_in_memory_only(self):
        replay_case = ReplayRegressionCase(
            name="synthetic-final-sweep-local-only",
            observations=[self._fixture_observation("Continuation")],
            expected_values={
                "final_state.setup_type": "Continuation",
                "final_focus_ranking.primary_focus_candidate_id": (
                    "SYNF-continuation-candidate"
                ),
                "watch_only": True,
                "no_trade_boundary.trade_approval": False,
            },
        )

        with mock.patch.object(
            builtins, "open", side_effect=AssertionError("file access is not allowed")
        ), mock.patch.object(
            pathlib.Path,
            "open",
            side_effect=AssertionError("path file access is not allowed"),
        ), mock.patch.object(
            os, "open", side_effect=AssertionError("os file access is not allowed")
        ), mock.patch.object(
            socket,
            "create_connection",
            side_effect=AssertionError("network access is not allowed"),
        ), mock.patch.object(
            socket,
            "socket",
            side_effect=AssertionError("network sockets are not allowed"),
        ), mock.patch.object(
            subprocess,
            "run",
            side_effect=AssertionError("external subprocesses are not allowed"),
        ), mock.patch.object(
            subprocess,
            "Popen",
            side_effect=AssertionError("external services are not allowed"),
        ), mock.patch.object(
            threading.Thread,
            "start",
            side_effect=AssertionError("thread loops are not allowed"),
        ), mock.patch.object(
            threading.Timer,
            "start",
            side_effect=AssertionError("scheduler loops are not allowed"),
        ):
            result = run_local_replay_regression([replay_case])

        self.assertEqual(result["cases_failed"], 0, result["case_results"])
        self.assertEqual(result["cases_processed"], 1)

    def test_multi_case_run_covers_all_setup_types_in_one_in_memory_call(self):
        cases = [
            ReplayRegressionCase(
                name=f"synthetic-final-sweep-{setup_type.lower().replace(' ', '-')}",
                observations=[self._fixture_observation(setup_type)],
                expected_values={
                    "final_state.setup_type": setup_type,
                    "final_trigger_card.setup_type": setup_type,
                    "final_diagnostics.setup_type": setup_type,
                    "final_focus_ranking.primary_focus_candidate_id": candidate_id,
                    "watch_only": True,
                    "no_trade_boundary.trade_approval": False,
                },
            )
            for setup_type, candidate_id in (
                ("Ideal", "SYNF-ideal-candidate"),
                ("Clean Fast Break", "SYNF-clean-fast-break-candidate"),
                ("Continuation", "SYNF-continuation-candidate"),
            )
        ]

        result = run_local_replay_regression(cases)

        self.assertEqual(result["cases_processed"], 3)
        self.assertEqual(result["cases_passed"], 3)
        self.assertEqual(result["cases_failed"], 0, result["case_results"])

    def test_repeated_run_stable_selected_output_fields_are_deterministic(self):
        replay_case = ReplayRegressionCase(
            name="synthetic-final-sweep-deterministic-repeat",
            observations=[
                self._fixture_observation(
                    "Ideal",
                    stage="forming/developing",
                    trigger_status="waiting_for_trigger",
                    distance_to_trigger="medium",
                    trigger_path_identifier="synthetic-final-forming-path",
                ),
                self._fixture_observation(
                    "Ideal",
                    last_seen_at="2099-05-01T10:32:00-04:00",
                    stage="near-trigger",
                    trigger_status="near_trigger",
                    distance_to_trigger="near",
                    trigger_path_identifier="synthetic-final-near-path",
                ),
                self._fixture_observation(
                    "Ideal",
                    last_seen_at="2099-05-01T11:32:00-04:00",
                    stage="pending_completed_candle_approval",
                    trigger_status="pending_completed_candle",
                    trigger_path_identifier="synthetic-final-pending-path",
                ),
            ],
        )

        first = run_local_replay_regression([replay_case])
        second = run_local_replay_regression([replay_case])
        stable_fields = (
            "cases_processed",
            "cases_passed",
            "cases_failed",
            "case_results",
            "no_trade_boundary",
        )

        self.assertEqual(
            {field: first[field] for field in stable_fields},
            {field: second[field] for field in stable_fields},
        )

    def test_stage_stale_and_session_boundary_semantics_are_preserved(self):
        result = run_local_replay_regression(
            [
                ReplayRegressionCase(
                    name="synthetic-final-sweep-stage-session-sequence",
                    observations=[
                        self._fixture_observation(
                            "Ideal",
                            regular_session_date="2099-05-01",
                            first_seen_at="2099-05-01T15:52:00-04:00",
                            last_seen_at="2099-05-01T15:52:00-04:00",
                            stage="forming/developing",
                            trigger_status="waiting_for_trigger",
                            distance_to_trigger="medium",
                            trigger_path_identifier="synthetic-final-developing-path",
                        ),
                        self._fixture_observation(
                            "Ideal",
                            regular_session_date="2099-05-02",
                            last_seen_at="2099-05-02T09:32:00-04:00",
                            stage="near-trigger",
                            trigger_status="near_trigger",
                            distance_to_trigger="near",
                            trigger_path_identifier="synthetic-final-near-path",
                        ),
                        self._fixture_observation(
                            "Ideal",
                            regular_session_date="2099-05-02",
                            last_seen_at="2099-05-02T10:32:00-04:00",
                            stage="pending_completed_candle_approval",
                            trigger_status="pending_completed_candle",
                            trigger_path_identifier="synthetic-final-pending-path",
                        ),
                        self._fixture_observation(
                            "Ideal",
                            regular_session_date="2099-05-02",
                            last_seen_at="2099-05-02T11:32:00-04:00",
                            stage="stale/spent/no-fresh-trigger",
                            trigger_status="stale",
                            fresh_stale_spent_state="stale",
                            fresh_trigger_path_present=False,
                            no_trade_reason="watch_only_no_fresh_trigger_no_trade",
                            trigger_path_identifier="synthetic-final-stale-path",
                        ),
                    ],
                    expected_values={
                        "observations_processed": 4,
                        "final_state.first_seen_at": "2099-05-01T15:52:00-04:00",
                        "final_state.last_seen_at": "2099-05-02T11:32:00-04:00",
                        "final_state.regular_session_date": "2099-05-01",
                        "final_state.previous_stage": (
                            "pending_completed_candle_approval"
                        ),
                        "final_state.stage": "stale/spent/no-fresh-trigger",
                        "final_state.trigger_status": "stale",
                        "final_trigger_card.fresh_trigger_path_present": False,
                    },
                    expected_contains={
                        "final_duplicate_suppression.material_change_flags": [
                            "stage_changed",
                            "trigger_status_changed",
                            "freshness_changed",
                        ]
                    },
                )
            ]
        )

        self.assertEqual(result["cases_failed"], 0, result["case_results"])
        case_result = result["case_results"][0]["result"]
        self.assertEqual(
            [
                record["state_snapshot"]["stage"]
                for record in case_result["shadow_log_records"]
            ],
            [
                "forming/developing",
                "near-trigger",
                "pending_completed_candle_approval",
                "stale/spent/no-fresh-trigger",
            ],
        )
        self.assertIn(
            "no fresh trigger",
            case_result["final_diagnostics"]["diagnostic_explanation"].lower(),
        )

    def test_failure_records_include_check_type_and_path_or_field_detail(self):
        result = run_local_replay_regression(
            [
                ReplayRegressionCase(
                    name="synthetic-final-sweep-expected-value-failure",
                    observations=[self._fixture_observation("Ideal")],
                    expected_values={"final_state.setup_type": "Continuation"},
                ),
                ReplayRegressionCase(
                    name="synthetic-final-sweep-expected-contains-failure",
                    observations=[self._fixture_observation("Clean Fast Break")],
                    expected_contains={
                        "final_duplicate_suppression.material_change_flags": [
                            "synthetic_missing_flag"
                        ]
                    },
                ),
                ReplayRegressionCase(
                    name="synthetic-final-sweep-expected-absent-field-failure",
                    observations=[self._fixture_observation("Continuation")],
                    expected_absent_fields=["headline_news_status"],
                ),
            ]
        )

        self.assertEqual(result["cases_failed"], 3)
        failures = {
            case_result["case_name"]: case_result["failures"][0]
            for case_result in result["case_results"]
        }
        value_failure = failures["synthetic-final-sweep-expected-value-failure"]
        contains_failure = failures["synthetic-final-sweep-expected-contains-failure"]
        absent_failure = failures["synthetic-final-sweep-expected-absent-field-failure"]

        self.assertEqual(value_failure["check"], "expected_value")
        self.assertEqual(value_failure["path"], "final_state.setup_type")
        self.assertEqual(value_failure["expected"], "Continuation")
        self.assertEqual(value_failure["actual"], "Ideal")
        self.assertEqual(contains_failure["check"], "expected_contains")
        self.assertEqual(
            contains_failure["path"],
            "final_duplicate_suppression.material_change_flags",
        )
        self.assertEqual(contains_failure["missing"], ["synthetic_missing_flag"])
        self.assertEqual(absent_failure["check"], "expected_absent_field")
        self.assertEqual(absent_failure["field"], "headline_news_status")
        self.assertTrue(absent_failure["paths"])

    def test_local_validation_suite_includes_final_sweep_module(self):
        from tests import test_watcher_foundation_local_validation_suite as suite_module

        module_name = "tests.test_watcher_replay_boundary_final_sweep"
        self.assertIn(module_name, suite_module.WATCHER_FOUNDATION_TEST_MODULES)
        loaded = unittest.defaultTestLoader.loadTestsFromName(module_name)
        self.assertEqual(loaded.countTestCases(), 9)


if __name__ == "__main__":
    unittest.main()
