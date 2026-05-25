import builtins
import importlib
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


REQUIRED_REPLAY_SUITE_MODULES = (
    "tests.test_watcher_replay_regression_runner",
    "tests.test_watcher_replay_regression_hardening",
    "tests.test_watcher_stable_winner_selection_replay",
)

RELIABILITY_MODULE = "tests.test_watcher_replay_validation_suite_reliability"

FORBIDDEN_REPLAY_FIELDS = FORBIDDEN_EXECUTION_FIELD_NAMES | {
    "live_trade_decision",
    "live_trade_decisions",
    "trade_decision",
    "trade_decision_status",
    "trade_decisions",
}


class WatcherReplayValidationSuiteReliabilityTests(unittest.TestCase):
    def _fixture_observation(self, setup_type="Ideal", **overrides):
        fixture_slug = setup_type.lower().replace(" ", "-")
        observation = {
            "candidate_id": f"SYNV-{fixture_slug}-candidate",
            "symbol": "SYNV",
            "watch_session_id": f"{fixture_slug}-validation-session",
            "setup_type": setup_type,
            "direction": "bullish/call-side",
            "regular_session_date": "2099-04-01",
            "first_seen_at": "2099-04-01T09:34:00-04:00",
            "last_seen_at": "2099-04-01T09:34:00-04:00",
            "stage": "near-trigger",
            "trigger_status": "near_trigger",
            "fresh_stale_spent_state": "fresh",
            "trigger_level_or_zone": f"{fixture_slug}-synthetic-zone",
            "trigger_zone_bucket": f"{fixture_slug}-synthetic-zone-bucket",
            "confirmation_timeframe_rule": "synthetic completed-candle review",
            "distance_to_trigger": "near",
            "invalidation_level_or_condition": "synthetic invalidation condition",
            "invalidation_bucket": f"{fixture_slug}-synthetic-invalidation",
            "source_kind": "local_fixture",
            "source_as_of": "2099-04-01T09:34:00-04:00",
            "evidence_rows": [f"{fixture_slug}-synthetic-evidence-1"],
            "evidence_quality": "deterministic",
            "unavailable_fields": [],
            "blockers": [],
            "cautions": [],
            "primary_blocker": "synthetic_local_validation_only",
            "no_trade_reason": "watch_only_shadow_review_no_live_trade_approval",
            "next_check_or_next_alert_condition": "new_material_change_required",
            "trigger_path_identifier": f"{fixture_slug}-validation-path",
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
        for field_name in FORBIDDEN_REPLAY_FIELDS:
            self.assertEqual(
                [],
                self._find_key_paths(value, field_name),
                f"Forbidden replay field leaked: {field_name}",
            )

    def test_local_validation_suite_includes_replay_regression_modules(self):
        suite_module = importlib.import_module(
            "tests.test_watcher_foundation_local_validation_suite"
        )

        for module_name in REQUIRED_REPLAY_SUITE_MODULES:
            with self.subTest(module_name=module_name):
                self.assertIn(module_name, suite_module.WATCHER_FOUNDATION_TEST_MODULES)
                loaded = unittest.defaultTestLoader.loadTestsFromName(module_name)
                self.assertGreater(loaded.countTestCases(), 0)

    def test_local_validation_suite_includes_reliability_module(self):
        suite_module = importlib.import_module(
            "tests.test_watcher_foundation_local_validation_suite"
        )

        self.assertIn(RELIABILITY_MODULE, suite_module.WATCHER_FOUNDATION_TEST_MODULES)
        loaded = unittest.defaultTestLoader.loadTestsFromName(RELIABILITY_MODULE)
        self.assertGreater(loaded.countTestCases(), 0)

    def test_local_validation_suite_test_count_is_stable_when_loaded_twice(self):
        first = unittest.defaultTestLoader.loadTestsFromName(
            "tests.test_watcher_foundation_local_validation_suite"
        )
        second = unittest.defaultTestLoader.loadTestsFromName(
            "tests.test_watcher_foundation_local_validation_suite"
        )

        self.assertEqual(first.countTestCases(), second.countTestCases())
        self.assertGreater(first.countTestCases(), 0)

    def test_replay_regression_uses_in_memory_fixture_without_external_calls(self):
        replay_case = ReplayRegressionCase(
            name="synthetic-local-only-validation",
            observations=[self._fixture_observation("Clean Fast Break")],
            expected_values={
                "final_state.setup_type": "Clean Fast Break",
                "final_focus_ranking.primary_focus_candidate_id": (
                    "SYNV-clean-fast-break-candidate"
                ),
                "watch_only": True,
                "no_trade_boundary.trade_approval": False,
            },
        )

        with mock.patch.object(
            builtins, "open", side_effect=AssertionError("file access is not allowed")
        ), mock.patch.object(
            socket,
            "create_connection",
            side_effect=AssertionError("network access is not allowed"),
        ), mock.patch.object(
            subprocess,
            "run",
            side_effect=AssertionError("external services are not allowed"),
        ), mock.patch.object(
            threading.Thread,
            "start",
            side_effect=AssertionError("scheduler loops are not allowed"),
        ):
            result = run_local_replay_regression([replay_case])

        self.assertEqual(result["cases_failed"], 0, result["case_results"])
        self.assertEqual(result["cases_processed"], 1)

    def test_same_replay_suite_cases_produce_stable_results_without_order_leakage(self):
        repeat_within_case = ReplayRegressionCase(
            name="synthetic-repeat-within-validation-case",
            observations=[
                self._fixture_observation("Ideal"),
                self._fixture_observation("Ideal"),
            ],
            expected_values={
                "final_duplicate_suppression.alert_decision": "suppress_duplicate"
            },
        )
        fresh_case = ReplayRegressionCase(
            name="synthetic-fresh-validation-case",
            observations=[self._fixture_observation("Ideal")],
            expected_values={
                "final_duplicate_suppression.alert_decision": "emit_material_change"
            },
        )

        first = run_local_replay_regression([repeat_within_case, fresh_case])
        second = run_local_replay_regression([fresh_case, repeat_within_case])

        self.assertEqual(first["cases_failed"], 0, first["case_results"])
        self.assertEqual(second["cases_failed"], 0, second["case_results"])
        self.assertEqual(
            first["case_results"][1]["result"]["alert_decisions"],
            ["emit_material_change"],
        )
        self.assertEqual(
            second["case_results"][0]["result"]["alert_decisions"],
            ["emit_material_change"],
        )

    def test_failure_details_cover_expected_value_contains_and_absent_field(self):
        result = run_local_replay_regression(
            [
                ReplayRegressionCase(
                    name="synthetic-expected-value-failure",
                    observations=[self._fixture_observation("Ideal")],
                    expected_values={"final_state.setup_type": "Continuation"},
                ),
                ReplayRegressionCase(
                    name="synthetic-expected-contains-failure",
                    observations=[self._fixture_observation("Clean Fast Break")],
                    expected_contains={
                        "final_duplicate_suppression.material_change_flags": [
                            "synthetic_missing_flag"
                        ]
                    },
                ),
                ReplayRegressionCase(
                    name="synthetic-expected-absent-field-failure",
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
        self.assertEqual(
            failures["synthetic-expected-value-failure"]["check"],
            "expected_value",
        )
        self.assertEqual(
            failures["synthetic-expected-value-failure"]["actual"],
            "Ideal",
        )
        self.assertEqual(
            failures["synthetic-expected-contains-failure"]["check"],
            "expected_contains",
        )
        self.assertEqual(
            failures["synthetic-expected-contains-failure"]["missing"],
            ["synthetic_missing_flag"],
        )
        self.assertEqual(
            failures["synthetic-expected-absent-field-failure"]["check"],
            "expected_absent_field",
        )
        self.assertTrue(failures["synthetic-expected-absent-field-failure"]["paths"])

    def test_forbidden_execution_and_trade_decision_fields_are_rejected(self):
        for field_name in sorted(FORBIDDEN_REPLAY_FIELDS):
            with self.subTest(field_name=field_name):
                with self.assertRaises(ValueError):
                    run_local_replay_regression(
                        [
                            ReplayRegressionCase(
                                name=f"synthetic-forbidden-{field_name}",
                                observations=[
                                    self._fixture_observation(
                                        "Ideal",
                                        nested_forbidden={field_name: "forbidden"},
                                    )
                                ],
                            )
                        ]
                    )

    def test_outputs_preserve_watch_only_and_no_live_trade_approval(self):
        result = run_local_replay_regression(
            [
                ReplayRegressionCase(
                    name="synthetic-boundary-validation",
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
                    expected_absent_fields=sorted(FORBIDDEN_REPLAY_FIELDS),
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
        self.assertTrue(result["watch_only"])
        self.assertTrue(result["no_trade_boundary"]["watch_only"])
        self.assertFalse(result["no_trade_boundary"]["trade_approval"])
        self.assertFalse(result["no_trade_boundary"]["live_trade_approval"])
        self._assert_no_forbidden_fields(result)


if __name__ == "__main__":
    unittest.main()
